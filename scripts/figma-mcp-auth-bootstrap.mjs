#!/usr/bin/env node

import { createServer } from "node:http"
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs"
import { homedir } from "node:os"
import { dirname, join } from "node:path"
import { spawn } from "node:child_process"
import { UnauthorizedError } from "@modelcontextprotocol/sdk/client/auth.js"
import { Client } from "@modelcontextprotocol/sdk/client/index.js"
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js"

const DEFAULT_SERVER_URL = "https://mcp.figma.com/mcp"
const CALLBACK_PORT = 3000
const CALLBACK_PATH = "/callback"
const AUTH_FILE = join(homedir(), ".local", "share", "opencode", "mcp-auth.json")

function serverKey(serverUrl) {
  const host = new URL(serverUrl).hostname.replace(/^www\./, "")
  const parts = host.split(".")
  return parts.length >= 2 ? parts[parts.length - 2] : parts[0]
}

function stateKey(key) {
  return key.charAt(0).toUpperCase() + key.slice(1)
}

function readAuthFile() {
  if (!existsSync(AUTH_FILE)) return {}
  try {
    return JSON.parse(readFileSync(AUTH_FILE, "utf8"))
  } catch {
    return {}
  }
}

function writeAuthFile(data) {
  mkdirSync(dirname(AUTH_FILE), { recursive: true })
  writeFileSync(AUTH_FILE, `${JSON.stringify(data, null, 2)}\n`, "utf8")
}

class AuthStorage {
  constructor(serverUrl) {
    this.serverUrl = serverUrl
    this.key = serverKey(serverUrl)
    this.sKey = stateKey(this.key)
  }

  loadClientInformation() {
    const data = readAuthFile()
    const info = data[this.key]?.clientInfo
    if (!info?.clientId) return undefined
    return {
      client_id: info.clientId,
      ...(info.clientSecret !== undefined ? { client_secret: info.clientSecret } : {}),
      ...(info.clientIdIssuedAt !== undefined ? { client_id_issued_at: info.clientIdIssuedAt } : {}),
      ...(info.clientSecretExpiresAt !== undefined ? { client_secret_expires_at: info.clientSecretExpiresAt } : {}),
    }
  }

  saveClientInformation(info) {
    const data = readAuthFile()
    const entry = data[this.key] ?? {}
    entry.serverUrl = this.serverUrl
    entry.clientInfo = {
      clientId: info.client_id,
      ...("client_secret" in info && info.client_secret !== undefined ? { clientSecret: info.client_secret } : {}),
      ...("client_id_issued_at" in info && info.client_id_issued_at !== undefined
        ? { clientIdIssuedAt: info.client_id_issued_at }
        : {}),
      ...("client_secret_expires_at" in info && info.client_secret_expires_at !== undefined
        ? { clientSecretExpiresAt: info.client_secret_expires_at }
        : {}),
    }
    data[this.key] = entry
    writeAuthFile(data)
    console.log(`[OAuth] Client registered: ${info.client_id}`)
  }

  loadTokens() {
    const data = readAuthFile()
    const tokens = data[this.key]?.tokens
    if (!tokens?.accessToken) return undefined
    const now = Date.now() / 1000
    return {
      access_token: tokens.accessToken,
      token_type: "bearer",
      ...(tokens.refreshToken !== undefined ? { refresh_token: tokens.refreshToken } : {}),
      ...(tokens.expiresAt !== undefined ? { expires_in: Math.max(0, Math.round(tokens.expiresAt - now)) } : {}),
    }
  }

  saveTokens(tokens) {
    const data = readAuthFile()
    const entry = data[this.key] ?? {}
    const now = Date.now() / 1000
    entry.serverUrl = this.serverUrl
    entry.tokens = {
      accessToken: tokens.access_token,
      ...(tokens.refresh_token !== undefined ? { refreshToken: tokens.refresh_token } : {}),
      ...(tokens.expires_in !== undefined ? { expiresAt: now + tokens.expires_in } : {}),
    }
    data[this.key] = entry
    writeAuthFile(data)
    console.log(`[OAuth] Tokens saved to ${AUTH_FILE}`)
  }

  saveCodeVerifier(codeVerifier) {
    const data = readAuthFile()
    const entry = data[this.sKey] ?? {}
    entry.codeVerifier = codeVerifier
    data[this.sKey] = entry
    writeAuthFile(data)
  }

  loadCodeVerifier() {
    const data = readAuthFile()
    return data[this.sKey]?.codeVerifier
  }
}

class McpOAuthProvider {
  constructor(serverUrl, clientId) {
    this.serverUrl = serverUrl
    this.clientId = clientId
    this.storage = new AuthStorage(serverUrl)
    this.authorizationCodePromise = new Promise((resolve) => {
      this.resolveAuthorizationCode = resolve
    })
  }

  get redirectUrl() {
    return `http://localhost:${CALLBACK_PORT}${CALLBACK_PATH}`
  }

  get clientMetadata() {
    return {
      redirect_uris: [this.redirectUrl],
      client_name: "Codex",
      grant_types: ["authorization_code", "refresh_token"],
      response_types: ["code"],
      token_endpoint_auth_method: "none",
    }
  }

  clientInformation() {
    if (this.clientId) return { client_id: this.clientId }
    return this.storage.loadClientInformation()
  }

  saveClientInformation(info) {
    this.storage.saveClientInformation(info)
  }

  tokens() {
    return this.storage.loadTokens()
  }

  saveTokens(tokens) {
    this.storage.saveTokens(tokens)
  }

  redirectToAuthorization(authorizationUrl) {
    const url = authorizationUrl.toString()
    console.log(`\n[OAuth] Open this URL in your browser if it does not open automatically:\n${url}\n`)
    const command = process.platform === "darwin" ? "open" : process.platform === "win32" ? "start" : "xdg-open"
    const child = spawn(command, [url], { stdio: "ignore", detached: false, shell: process.platform === "win32" })
    child.on("error", () => {
      console.warn("[warn] Browser auto-open gagal. Buka URL manual di atas.")
    })
  }

  saveCodeVerifier(codeVerifier) {
    this.storage.saveCodeVerifier(codeVerifier)
  }

  codeVerifier() {
    const verifier = this.storage.loadCodeVerifier()
    if (!verifier) throw new Error("No code verifier saved")
    return verifier
  }

  waitForAuthorizationCode() {
    return this.authorizationCodePromise
  }

  receiveAuthorizationCode(code) {
    this.resolveAuthorizationCode(code)
  }
}

function startCallbackServer(provider) {
  const server = createServer((req, res) => {
    const url = new URL(req.url ?? "/", `http://localhost:${CALLBACK_PORT}`)
    if (req.method !== "GET" || url.pathname !== CALLBACK_PATH) {
      res.statusCode = 404
      res.end("Not found")
      return
    }

    const error = url.searchParams.get("error")
    const code = url.searchParams.get("code")

    if (error) {
      res.statusCode = 400
      res.end(`Authorization failed: ${error}`)
      return
    }

    if (!code) {
      res.statusCode = 400
      res.end("Missing authorization code")
      return
    }

    res.statusCode = 200
    res.setHeader("content-type", "text/html; charset=utf-8")
    res.end("<h1>Authorization successful</h1><p>Kembali ke terminal. Token sedang disimpan untuk OpenCode.</p>")
    provider.receiveAuthorizationCode(code)
  })

  return new Promise((resolve) => {
    server.listen(CALLBACK_PORT, () => {
      console.log(`[OAuth] Callback server listening on http://localhost:${CALLBACK_PORT}${CALLBACK_PATH}`)
      resolve(server)
    })
  })
}

async function connectWithAuth(serverUrl, provider) {
  const url = new URL(serverUrl)
  const transport = new StreamableHTTPClientTransport(url, { authProvider: provider })
  const client = new Client({ name: "Codex", version: "1.0.0" }, { capabilities: {} })

  try {
    await client.connect(transport)
    console.log("[MCP] Connected successfully.")
    return client
  } catch (error) {
    if (!(error instanceof UnauthorizedError)) throw error
    console.log("[OAuth] Waiting for authorization code via browser...")
    const code = await provider.waitForAuthorizationCode()
    console.log("[OAuth] Authorization code received. Finishing auth...")
    await transport.finishAuth(code)
    const retryTransport = new StreamableHTTPClientTransport(url, { authProvider: provider })
    const retryClient = new Client({ name: "Codex", version: "1.0.0" }, { capabilities: {} })
    await retryClient.connect(retryTransport)
    console.log("[MCP] Connected successfully after authentication.")
    return retryClient
  }
}

async function main() {
  const serverUrl = process.argv[2] || DEFAULT_SERVER_URL
  const clientId = process.argv[3]
  const provider = new McpOAuthProvider(serverUrl, clientId)
  const callbackServer = await startCallbackServer(provider)
  let client

  try {
    client = await connectWithAuth(serverUrl, provider)
    const tools = await client.listTools()
    console.log(`[MCP] ${tools.tools.length} tool(s) tersedia.`)
    console.log(`[pass] Auth bootstrap selesai. File token: ${AUTH_FILE}`)
  } finally {
    if (client) await client.close().catch(() => {})
    callbackServer.close()
  }
}

main().catch((error) => {
  console.error("[fail] Auth bootstrap gagal")
  console.error(error)
  process.exit(1)
})
