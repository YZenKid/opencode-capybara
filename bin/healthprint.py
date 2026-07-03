#!/usr/bin/env python3
import json, sys
p = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h.json"
try:
    d = json.load(open(p))
except Exception as e:
    print("PARSE_ERR", e); raise SystemExit(1)
top = d.get("lastOpenCodeLaunchDiagnostics", {}) or {}
print("READY=" + str(d.get("isOpenCodeReady")) +
      " OCRUN=" + str(d.get("openCodeRunning")) +
      " BIN=" + str(d.get("opencodeBinaryResolved")) +
      " SHD=" + str(top.get("hasShellEnv")) +
      " K=" + str(top.get("shellEnvKeysCount")) +
      " ERR=" + str(d.get("lastOpenCodeError")))
