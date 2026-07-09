#!/usr/bin/env python3
"""External legal/source inventory helper.

Purpose:
- inventory external sources before code/asset reuse,
- classify license/permission posture,
- flag high-risk reuse patterns early,
- discover likely license/terms pages and aggregate their evidence.

Usage:
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://example.com --kind website --json
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://github.com/user/repo --kind repo --summary-only
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://cdn.example.com/logo.svg --kind asset --intent direct-reuse --json
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://example.com --out /tmp/legal.json
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://example.com --project-root /tmp/proj --task-id demo \\
      # writes to /tmp/proj/.opencode/evidence/demo/legal-source-check.json
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://cdn.jsdelivr.net/npm/lucide-static@0.469.0/icons/star.svg \\
      --image-prompt "use Lucide icon for star rating" --summary-only

Exit codes:
  0 = report emitted, no blocking risk detected
  1 = emitted, but needs clarification / high-risk / restricted / unknown for requested intent
  2 = invocation error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Any

LICENSE_PATTERNS = [
    (re.compile(r"\bMIT\b", re.I), "MIT"),
    (re.compile(r"\bApache(?:\s+License)?\s*2(?:\.0)?\b", re.I), "Apache-2.0"),
    (re.compile(r"\bBSD(?:[- ](?:2|3)[- ]Clause)?\b", re.I), "BSD"),
    (re.compile(r"\bISC\b", re.I), "ISC"),
    (re.compile(r"\bMPL\s*2(?:\.0)?\b", re.I), "MPL-2.0"),
    (re.compile(r"\bCC0(?:[- ]1\.0)?\b", re.I), "CC0-1.0"),
    (re.compile(r"\bUnlicense\b", re.I), "Unlicense"),
    (re.compile(r"\bLGPL\b", re.I), "LGPL"),
    (re.compile(r"\bGPL\b", re.I), "GPL"),
    (re.compile(r"\bAGPL\b", re.I), "AGPL"),
    (re.compile(r"\bSSPL\b", re.I), "SSPL"),
]

RESTRICTED_PATTERNS = [
    re.compile(r"all rights reserved", re.I),
    re.compile(r"do not (?:copy|reuse|redistribute)", re.I),
    re.compile(r"no scraping", re.I),
    re.compile(r"automated access prohibited", re.I),
    re.compile(r"watermark", re.I),
    re.compile(r"copyright\s+(?:all rights reserved|notice: do not copy|notice: reuse prohibited)", re.I),
]

PERMISSION_PATTERNS = [
    re.compile(r"licensed under", re.I),
    re.compile(r"permission granted", re.I),
    re.compile(r"open source", re.I),
    re.compile(r"creative commons", re.I),
]

HIGH_RISK_INTENTS = {"clone", "1:1", "copy-from", "direct-reuse"}
ADAPTIVE_INTENTS = {"reference-only", "style-equivalent"}

CDN_HINTS = [
    {
        "match": ("cdn.jsdelivr.net", "jsdelivr.net"),
        "provider": "jsDelivr",
        "default_license": "unknown",
        "kind": "cdn",
        "hint": "jsDelivr is a public CDN; hotlinking is permitted under jsDelivr terms but the underlying package retains its own license. Pin a specific package version, do not pin to `latest`, and download + commit a copy under the project asset path so the source is reproducible.",
    },
    {
        "match": ("unpkg.com",),
        "provider": "unpkg",
        "default_license": "unknown",
        "kind": "cdn",
        "hint": "unpkg is a public CDN; do not hotlink in production. Pin a specific version, then download + commit a copy under the project asset path so the source is reproducible.",
    },
    {
        "match": ("esm.sh",),
        "provider": "esm.sh",
        "default_license": "unknown",
        "kind": "cdn",
        "hint": "esm.sh rewrites and serves public npm packages; do not hotlink in production. Pin a specific version and download + commit a copy under the project asset path.",
    },
    {
        "match": ("cdn.skypack.dev", "skypack.dev"),
        "provider": "Skypack",
        "default_license": "unknown",
        "kind": "cdn",
        "hint": "Skypack is a public CDN for ESM; do not hotlink in production. Pin a specific version and download + commit a copy under the project asset path.",
    },
    {
        "match": ("cdnjs.com", "cdnjs.cloudflare.com"),
        "provider": "cdnjs",
        "default_license": "unknown",
        "kind": "cdn",
        "hint": "cdnjs is a public CDN; do not hotlink in production. Pin a specific version, then download + commit a copy under the project asset path so the source is reproducible.",
    },
    {
        "match": ("fonts.googleapis.com", "fonts.gstatic.com"),
        "provider": "Google Fonts",
        "default_license": "OFL/Apache-2.0",
        "kind": "cdn",
        "hint": "Google Fonts is generally safe to hotlink; for offline-first apps or strict CSP, self-host the font files under the project asset path.",
    },
    {
        "match": ("use.fontawesome.com", "kit.fontawesome.com", "pro.fontawesome.com"),
        "provider": "Font Awesome",
        "default_license": "CC-BY-4.0 (Free) / Pro License",
        "kind": "cdn",
        "hint": "Font Awesome requires attribution on the Free plan and a Pro license for Pro assets. Do not hotlink the Pro CDN without a valid kit token; download + commit only assets your project license covers.",
    },
    {
        "match": ("kit-pro.fontawesome.com",),
        "provider": "Font Awesome Pro",
        "default_license": "Pro License",
        "kind": "cdn",
        "hint": "Font Awesome Pro is paid; do not hotlink without an active Pro subscription and a project-scoped kit token. Audit license coverage per asset before reuse.",
    },
    {
        "match": ("icons8.com", "img.icons8.com", "static.icons8.com"),
        "provider": "Icons8",
        "default_license": "icons8 license (paid / free with attribution)",
        "kind": "cdn",
        "hint": "Icons8 has tier-dependent terms; verify the asset's license posture (free-with-attribution vs paid) before reuse and do not silently hotlink paid assets.",
    },
    {
        "match": ("flaticon.com", "static.flaticon.com"),
        "provider": "Flaticon",
        "default_license": "Flaticon License (free-with-attribution / Premium)",
        "kind": "cdn",
        "hint": "Flaticon is attribution-required on the free tier; verify per-asset license and attribution posture, and avoid hotlinking in production.",
    },
    {
        "match": ("lottie.host", "assets-v1.lottiefiles.com", "assets-vN.lottiefiles.com", "lottiefiles.com"),
        "provider": "LottieFiles",
        "default_license": "per-asset (LottieFiles Standard / Premium / CC variants)",
        "kind": "motion-asset",
        "package_aliases": ("lottie", "lottie-react", "lottie-web", "lottie-player", "@lottiefiles/react-lottie-player", "@lottiefiles/dotlottie-player", "@lottiefiles/lottie-player", "react-lottie", "lottie-ios", "lottie-android"),
        "hint": "LottieFiles hosts motion assets; per-animation license varies (Standard / Premium / CC-BY). Verify the specific animation's license before reuse, attribute when required, and prefer downloading the .json/.lottie and committing it under the project asset path so motion is reproducible offline.",
    },
    {
        "match": ("cdn.rive.app", "rive.app", "cdn.riveusercontent.com"),
        "provider": "Rive",
        "default_license": "Rive Standard / Pro (per-asset / per-runtime)",
        "kind": "motion-asset",
        "package_aliases": ("rive", "rive-react", "rive-react-canvas", "@rive-app/react-canvas", "@rive-app/canvas", "rive-ios", "rive-android"),
        "hint": "Rive hosts interactive motion (.riv) assets; per-asset license posture depends on whether the asset is free or from the Rive marketplace (some require Pro). Verify the asset's license, attribute when required, and download + commit the .riv file under the project asset path so motion is reproducible offline.",
    },
    {
        "match": ("lordicon.com", "assets.lordicon.com", "cdn.lordicon.com"),
        "provider": "Lordicon",
        "default_license": "Lordicon Free (with link) / Premium",
        "kind": "motion-asset",
        "hint": "Lordicon hosts animated icon sets; free assets require a credit link and premium assets require a paid plan. Verify the icon's license, attribute or upgrade before reuse, and download + commit the JSON under the project asset path.",
    },
    {
        "match": ("lottielab.com", "assets.lottielab.com"),
        "provider": "LottieLab",
        "default_license": "per-asset / LottieLab terms",
        "kind": "motion-asset",
        "hint": "LottieLab hosts interactive motion assets; verify the asset's license posture (free vs paid) and download + commit the JSON under the project asset path so motion is reproducible offline.",
    },
]

ASSET_CDN_HINTS = [
    {
        "match": ("raw.githubusercontent.com",),
        "provider": "raw.githubusercontent.com",
        "default_license": "per-repo",
        "kind": "3d-asset",
        "hint": "Direct raw GitHub content host; the license is the upstream repository's LICENSE. Record repo + commit SHA + LICENSE in evidence before reuse.",
    },
    {
        "match": ("market.pmnd.rs",),
        "provider": "pmndrs market",
        "default_license": "CC0 / MIT (per-asset)",
        "kind": "3d-asset",
        "hint": "pmndrs community market hosts glTF/HDR/prefab assets; verify the per-asset license (CC0 vs MIT) and download + commit the asset under the project asset path so the source is reproducible.",
    },
    {
        "match": ("poly.pizza", "poly.pizza"),
        "provider": "Poly Pizza",
        "default_license": "per-model (CC0/CC-BY/Sketchfab CC variants)",
        "kind": "3d-asset",
        "hint": "Poly Pizza aggregates low-poly 3D models; per-model license varies (CC0/CC-BY/Sketchfab CC). Verify the exact model license and attribution posture before reuse.",
    },
    {
        "match": ("sketchfab.com", "cdn.sketchfab.com", "sketchfab-assets.akamaized.net", "media.sketchfab.com"),
        "provider": "Sketchfab",
        "default_license": "per-model (CC0/CC-BY/Editorial/etc.)",
        "kind": "3d-asset",
        "hint": "Sketchfab hosts 3D models and assets; per-asset license varies. Filter to CC-friendly models, record the exact model URL + license + attribution requirement.",
    },
    {
        "match": ("prod.spline.design", "spline.design", "cdn.spline.design", "assets.spline.design"),
        "provider": "Spline",
        "default_license": "Spline Standard / Pro (per-asset / per-runtime)",
        "kind": "runtime-asset",
        "hint": "Spline hosts interactive 3D scenes; the per-scene license posture depends on the plan (Free scenes vs Pro) and on the runtime embed policy. Verify the scene's license, attribute when required, and avoid hotlinking the Pro runtime without an active Pro subscription.",
    },
    {
        "match": ("assets.glitch.com", "glitch.com"),
        "provider": "Glitch",
        "default_license": "MIT (per-project) / per-asset",
        "kind": "runtime-asset",
        "hint": "Glitch hosts project assets and remixable apps; verify the per-asset license (MIT for the project template vs per-asset) and avoid hotlinking without attribution.",
    },
    {
        "match": ("market-assets.fra1.cdn.digitaloceanspaces.com", "market-assets.ams1.cdn.digitaloceanspaces.com", "market-assets.sgp1.cdn.digitaloceanspaces.com", "cdn.digitaloceanspaces.com"),
        "provider": "DigitalOcean Spaces (market-assets)",
        "default_license": "per-bucket",
        "kind": "runtime-asset",
        "hint": "DigitalOcean Spaces (market-assets.*) is a generic S3-compatible CDN used by some 3D / runtime marketplaces; license is per-bucket. Verify the bucket's terms and download + commit the asset under the project asset path.",
    },
    {
        "match": ("threejs.org",),
        "provider": "Three.js",
        "default_license": "MIT (reference code only)",
        "kind": "3d-runtime",
        "hint": "Three.js is a runtime library, not an asset host; for glTF sample assets, use Khronos glTF-Sample-Models instead and record the per-asset license.",
    },
    {
        "match": ("pmndrs.github.io", "docs.pmnd.rs",),
        "provider": "pmndrs",
        "default_license": "MIT (code) / per-asset (assets)",
        "kind": "3d-runtime",
        "hint": "pmndrs docs / demos; treat as code (MIT) and verify per-asset license for any embedded 3D assets.",
    },
]

LOOKALIKE_PATTERNS = [
    {
        "needles": ("logos", "logo", "brands", "brand", "brand-assets", "brand-kit"),
        "match_mode": "segment-or-hyphen",
        "label": "brand-or-logo path pattern",
        "hint": "Potential trademark/logo source; verify ownership/permission before reuse and avoid generated lookalikes for functional branding.",
    },
    {
        "needles": ("celebrity", "celeb", "public-figure", "portrait-of-", "headshot-of-"),
        "match_mode": "segment-or-hyphen",
        "label": "celebrity-or-public-figure path pattern",
        "hint": "Potential likeness/personality-rights source; verify model/personality rights separately from copyright.",
    },
    {
        "needles": ("characters", "character", "fan-art", "fandom", "anime", "pokemon", "marvel", "disney", "star-wars"),
        "match_mode": "segment-or-hyphen",
        "label": "character-or-fan-art path pattern",
        "hint": "Potential copyrighted character / franchise source; prefer omission, licensed source, or style-equivalent non-infringing output.",
    },
    {
        "needles": ("lookalike", "in-the-style-of", "style-of", "face-swap", "deepfake"),
        "match_mode": "query-or-path",
        "label": "lookalike-imitation path or query pattern",
        "hint": "Potential imitation/lookalike source; do not use for celebrity, artist-style, or identity-dependent replication.",
    },
]

PROVIDER_HINTS = [
    {
        "match": ("lucide.dev",),
        "provider": "Lucide",
        "category": "icon-library",
        "default_license": "ISC",
        "aliases": ("lucide", "lucide-react", "lucide-static", "lucide-vue", "lucide-svelte", "react-icons/lu"),
        "hint": "Functional UI icon library; prefer reuse over generated icon substitutes.",
    },
    {
        "match": ("phosphoricons.com",),
        "provider": "Phosphor Icons",
        "category": "icon-library",
        "default_license": "MIT",
        "aliases": ("phosphor", "phosphor-icons", "phosphor-react", "phosphor-vue", "react-icons/pi"),
        "hint": "Multiple icon weights available; keep one weight system per project.",
    },
    {
        "match": ("heroicons.com",),
        "provider": "Heroicons",
        "category": "icon-library",
        "default_license": "MIT",
        "aliases": ("heroicons", "heroicons-react", "@heroicons/react", "react-icons/hi", "react-icons/hi2"),
        "hint": "Safe for functional UI icons; do not generate lookalike replacements.",
    },
    {
        "match": ("tabler.io", "tabler-icons.io"),
        "provider": "Tabler Icons",
        "category": "icon-library",
        "default_license": "MIT",
        "aliases": ("tabler", "tabler-icons", "tabler-icons-react", "tabler-icons-vue", "@tabler/icons", "@tabler/icons-react", "react-icons/tb"),
        "hint": "Large outline icon set; keep stroke width consistent across the app.",
    },
    {
        "match": ("iconoir.com",),
        "provider": "Iconoir",
        "category": "icon-library",
        "default_license": "MIT",
        "aliases": ("iconoir", "iconoir-react", "@iconoir/react"),
        "hint": "Safe icon-library source; verify package name and version in evidence.",
    },
    {
        "match": ("fonts.google.com/icons",),
        "provider": "Material Symbols",
        "category": "icon-library",
        "default_license": "Apache-2.0",
        "aliases": ("material-symbols", "material-icons", "react-material-symbols", "@mui/icons-material"),
        "hint": "Variable icon font/symbols; record chosen weight/fill axis in design notes.",
    },
    {
        "match": ("undraw.co",),
        "provider": "unDraw",
        "category": "illustration-library",
        "default_license": "unknown",
        "hint": "Illustration source; check the current upstream free-use terms before bulk reuse.",
    },
    {
        "match": ("opendoodles.com",),
        "provider": "Open Doodles",
        "category": "illustration-library",
        "default_license": "CC-BY-4.0",
        "hint": "Attribution may be required; record attribution posture in evidence.",
    },
    {
        "match": ("storyset.com",),
        "provider": "Storyset",
        "category": "illustration-library",
        "default_license": "unknown",
        "hint": "Illustration service with tier-dependent terms; verify current commercial-use posture.",
    },
    {
        "match": ("blush.design",),
        "provider": "Blush",
        "category": "illustration-library",
        "default_license": "unknown",
        "hint": "Check per-collection/per-tier terms before reuse.",
    },
    {
        "match": ("humaaans.com",),
        "provider": "Humaaans",
        "category": "illustration-library",
        "default_license": "unknown",
        "hint": "Mix-and-match illustration source; verify current license page before reuse.",
    },
    {
        "match": ("unsplash.com",),
        "provider": "Unsplash",
        "category": "stock-photo",
        "default_license": "Unsplash License",
        "hint": "Record the exact photo URL and license posture; do not imply trademark/personality rights are cleared.",
    },
    {
        "match": ("pexels.com",),
        "provider": "Pexels",
        "category": "stock-photo",
        "default_license": "Pexels License",
        "hint": "Free stock source; verify person/product/trademark context separately.",
    },
    {
        "match": ("pixabay.com",),
        "provider": "Pixabay",
        "category": "stock-photo",
        "default_license": "Pixabay License",
        "hint": "Free stock source; verify releases for portraits and branded products.",
    },
    {
        "match": ("commons.wikimedia.org",),
        "provider": "Wikimedia Commons",
        "category": "stock-photo",
        "default_license": "per-file",
        "hint": "Per-file license varies; attribution and share-alike may apply.",
    },
    {
        "match": ("polyhaven.com",),
        "provider": "Poly Haven",
        "category": "3d-library",
        "default_license": "CC0",
        "hint": "Strong default for 3D/HDRI/textures; record model/HDRI URL in evidence.",
    },
    {
        "match": ("quaternius.com",),
        "provider": "Quaternius",
        "category": "3d-library",
        "default_license": "CC0",
        "hint": "Good low-risk 3D source; verify pack scope and attribution expectations.",
    },
    {
        "match": ("kenney.nl",),
        "provider": "Kenney",
        "category": "3d-library",
        "default_license": "CC0",
        "hint": "Safe prototype/game asset source; keep style consistent with the project.",
    },
    {
        "match": ("sketchfab.com",),
        "provider": "Sketchfab",
        "category": "3d-library",
        "default_license": "per-model",
        "hint": "License varies by model; filter to CC-friendly models and record the exact model license.",
    },
]


def fetch_text(url: str, limit: int = 50000) -> tuple[str, dict[str, str], str | None]:
    req = Request(url, headers={"User-Agent": "OpenCode legal-source-check/1.0"})
    with urlopen(req, timeout=15) as resp:
        raw = resp.read(limit)
        headers = {k.lower(): v for k, v in resp.headers.items()}
        charset = "utf-8"
        ctype = headers.get("content-type", "")
        m = re.search(r"charset=([^;\s]+)", ctype, re.I)
        if m:
            charset = m.group(1)
        text = raw.decode(charset, errors="replace")
        return text, headers, resp.geturl()


def classify_license(text: str) -> str:
    for pattern, label in LICENSE_PATTERNS:
        if pattern.search(text):
            return label
    return "unknown"


def source_classification(kind: str, headers: dict[str, str], text: str, license_label: str) -> str:
    robots = headers.get("x-robots-tag", "")
    if any(p.search(text) for p in RESTRICTED_PATTERNS) or "noindex" in robots.lower() or "nofollow" in robots.lower():
        return "restricted"
    if license_label != "unknown" or any(p.search(text) for p in PERMISSION_PATTERNS):
        return "licensed"
    if kind in {"website", "asset"}:
        return "public-but-unlicensed"
    return "unknown"


def license_risk(license_label: str) -> str:
    if license_label in {"MIT", "Apache-2.0", "BSD", "ISC", "MPL-2.0", "CC0-1.0", "Unlicense"}:
        return "permissive"
    if license_label in {"LGPL", "GPL", "AGPL", "SSPL"}:
        return "copyleft-or-caution"
    return "unknown"


def kind_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    if "github.com" in urlparse(url).netloc.lower():
        return "repo"
    if any(path.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".mp4", ".pdf")):
        return "asset"
    return "website"


def detect_high_risk(url: str, kind: str, intent: str, text: str) -> list[str]:
    out: list[str] = []
    host = urlparse(url).netloc.lower()
    if intent in HIGH_RISK_INTENTS and kind == "website":
        out.append("requested verbatim reuse from website source")
    if re.search(r"logo|trademark|brand assets?", text, re.I):
        out.append("source mentions logos/trademarks/brand assets")
    if re.search(r"watermark", text, re.I):
        out.append("source mentions watermark")
    if any(x in host for x in ("gettyimages", "shutterstock", "istockphoto", "adobe.com")):
        out.append("stock/media provider source detected")
    return out


def detect_provider(url: str) -> dict[str, Any] | None:
    """Return a curated provider record when the source URL matches a known icon/illustration/stock/3D library."""
    host = urlparse(url).netloc.lower()
    host_no_www = host[4:] if host.startswith("www.") else host
    for entry in PROVIDER_HINTS:
        for needle in entry["match"]:
            target = needle.lower()
            if target in host or target in host_no_www:
                return {
                    "provider": entry["provider"],
                    "category": entry["category"],
                    "default_license": entry["default_license"],
                    "hint": entry["hint"],
                    "matched_host": host,
                }
    return None


def detect_lookalike_pattern(url: str) -> list[dict[str, Any]]:
    """Detect URL patterns that frequently indicate brand/celebrity/character lookalike or imitation intent.

    Matching is segment-aware by default: a needle like `marvel` only matches a full path
    segment (`/marvel/...`) or a hyphenated form (`pokemon-cards`), not arbitrary substrings
    like `marvelous` or `pokemonshop`. Query-or-path mode allows substring match in either
    path or query, used for hints that often show up as search params (lookalike, in-the-style-of).
    """
    parsed = urlparse(url)
    path_segments = [seg for seg in parsed.path.lower().split("/") if seg]
    path_lower = parsed.path.lower()
    query_lower = parsed.query.lower()
    matched: list[dict[str, Any]] = []

    def segment_match(needle: str) -> bool:
        n = needle.lower()
        if n in path_segments:
            return True
        # hyphenated form (pokemon-cards, brand-kit)
        for seg in path_segments:
            if seg == n:
                return True
            for part in seg.split("-"):
                if part == n:
                    return True
        # filename inside segment (logos/acme.svg, characters/marvel/spider.svg)
        for seg in path_segments:
            if n in seg.split(".")[0:1]:
                return True
        return False

    def query_or_path(needle: str) -> bool:
        n = needle.lower()
        return n in path_lower or n in query_lower

    for entry in LOOKALIKE_PATTERNS:
        mode = entry.get("match_mode", "segment-or-hyphen")
        check = segment_match if mode == "segment-or-hyphen" else query_or_path
        for needle in entry["needles"]:
            if check(needle):
                matched.append({
                    "label": entry["label"],
                    "needle": needle,
                    "match_mode": mode,
                    "hint": entry["hint"],
                })
                break
    return matched


def detect_cdn_provider(url: str) -> dict[str, Any] | None:
    """Detect public CDN providers (icon/font/JS asset CDNs and motion asset hosts) and return a hotlink-policy hint."""
    host = urlparse(url).netloc.lower()
    host_no_www = host[4:] if host.startswith("www.") else host
    for entry in CDN_HINTS:
        for needle in entry["match"]:
            target = needle.lower()
            if target in host or target in host_no_www:
                return {
                    "provider": entry["provider"],
                    "kind": entry["kind"],
                    "default_license": entry["default_license"],
                    "hint": entry["hint"],
                    "matched_host": host,
                }
    return None


def detect_asset_cdn(url: str) -> dict[str, Any] | None:
    """Detect 3D asset CDNs / runtime asset hosts (GitHub raw, pmndrs market, poly.pizza, Spline, Glitch, DO Spaces, etc.)."""
    host = urlparse(url).netloc.lower()
    host_no_www = host[4:] if host.startswith("www.") else host
    for entry in ASSET_CDN_HINTS:
        for needle in entry["match"]:
            target = needle.lower()
            if target in host or target in host_no_www:
                return {
                    "provider": entry["provider"],
                    "kind": entry["kind"],
                    "default_license": entry["default_license"],
                    "hint": entry["hint"],
                    "matched_host": host,
                }
    return None


def candidate_license_urls(source: str) -> list[str]:
    """Build likely license/terms page URLs to probe, based on source kind."""
    parsed = urlparse(source)
    netloc = parsed.netloc.lower()
    scheme = parsed.scheme or "https"
    base = f"{scheme}://{parsed.netloc}"
    path = parsed.path
    candidates: list[str] = []

    if "github.com" in netloc:
        # owner/repo
        parts = [p for p in path.split("/") if p][:2]
        if len(parts) == 2:
            owner, repo = parts
            for branch in ("HEAD", "main", "master"):
                for tail in ("/LICENSE", "/LICENSE.md", "/License.md", "/license.txt", "/COPYING"):
                    candidates.append(f"{scheme}://raw.githubusercontent.com/{owner}/{repo}/{branch}{tail}")
            for tail in ("/blob/HEAD/LICENSE", "/blob/HEAD/LICENSE.md", "/blob/HEAD/license.txt", "/blob/main/LICENSE", "/blob/master/LICENSE"):
                candidates.append(f"{base}/{owner}/{repo}{tail}")
            candidates.append(f"{base}/{owner}/{repo}")
        return candidates

    # generic website: probe common paths (try both bare and .html/.txt forms)
    for tail in ("/license", "/licence", "/legal", "/terms", "/terms-of-service", "/terms-and-conditions", "/copyright", "/about/license"):
        candidates.append(urljoin(base, tail))
        for ext in (".html", ".htm", ".txt", ".md"):
            candidates.append(urljoin(base, tail + ext))
    candidates.append(base)
    return candidates


def probe_license_pages(source: str, primary_text: str, limit: int = 20000) -> list[dict[str, Any]]:
    """Fetch each candidate license/terms URL and extract license + restriction hints."""
    out: list[dict[str, Any]] = []
    primary_host = urlparse(source).netloc.lower()
    for url in candidate_license_urls(source):
        try:
            text, headers, final = fetch_text(url, limit=limit)
        except (URLError, HTTPError, TimeoutError, ValueError):
            continue
        if urlparse(final).netloc.lower() != primary_host:
            # keep on the same host only
            continue
        ctype = headers.get("content-type", "").lower()
        if "html" not in ctype and "text" not in ctype:
            continue
        license_label = classify_license(text)
        restricted_hits = [p.pattern for p in RESTRICTED_PATTERNS if p.search(text)]
        permission_hits = [p.pattern for p in PERMISSION_PATTERNS if p.search(text)]
        if license_label == "unknown" and not restricted_hits and not permission_hits:
            continue
        out.append({
            "url": final,
            "license": license_label,
            "license_risk": license_risk(license_label),
            "restricted_hits": restricted_hits,
            "permission_hits": permission_hits,
            "byte_sample": len(text),
        })
    return out


def license_variant_from_label(label: str) -> str:
    """Collapse raw license strings into a smaller set of variant tags.

    Used for motion/3D providers whose license surface is freer-form than SPDX.
    Examples: `Premium`, `CC-BY`, `CC0`, `editorial`, `standard`, `free`, `commercial`.
    """
    l = (label or "").strip().lower()
    if not l or l == "unknown":
        return "unknown"
    if "premium" in l or "pro" in l:
        return "premium-or-pro"
    if "cc-by" in l or "cc by" in l:
        return "cc-by"
    if "cc0" in l or "cc-0" in l or "creative commons zero" in l:
        return "cc0"
    if "editorial" in l:
        return "editorial"
    if "free" in l:
        return "free-tier"
    if "standard" in l:
        return "standard"
    if "commercial" in l:
        return "commercial"
    return "other"


def probe_motion_metadata(source: str, limit: int = 8000) -> dict[str, Any] | None:
    """Best-effort motion asset metadata probe for LottieFiles public API.

    Rive has no public metadata API, so Rive assets fall through to per-asset license verification.
    Returns:
        {
            "host": "lottiefiles.com",
            "asset_id": "...",
            "url": "<api url>",
            "fetched": True/False,
            "license": "<license label>" or "unknown",
            "license_variant": "premium-or-pro" | "cc-by" | "cc0" | "free-tier" | "unknown" | ...,
            "raw": <small dict of useful fields>,
        }
    """
    parsed = urlparse(source)
    host = parsed.netloc.lower()
    asset_id: str | None = None
    if "lottiefiles.com" in host or "lottie.host" in host:
        # LottieFiles URLs look like https://lottie.host/<id>/<slug>.json
        # or https://assets-vN.lottiefiles.com/...
        path = parsed.path.strip("/")
        if path:
            first = path.split("/")[0]
            if first and re.fullmatch(r"[A-Za-z0-9_-]{4,}", first):
                asset_id = first
    if not asset_id:
        return None
    api_url = f"https://api.lottiefiles.com/v1/animation/{asset_id}"
    try:
        text, headers, _ = fetch_text(api_url, limit=limit)
    except (URLError, HTTPError, TimeoutError, ValueError):
        return {
            "host": "lottiefiles.com",
            "asset_id": asset_id,
            "url": api_url,
            "fetched": False,
            "license": "unknown",
            "license_variant": "unknown",
            "raw": {},
        }
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {
            "host": "lottiefiles.com",
            "asset_id": asset_id,
            "url": api_url,
            "fetched": True,
            "license": "unknown",
            "license_variant": "unknown",
            "raw": {"raw_sample": text[:200]},
        }
    license_label = str(
        data.get("license")
        or data.get("licenseName")
        or data.get("licenseType")
        or "unknown"
    ).strip()
    summary = {
        "host": "lottiefiles.com",
        "asset_id": asset_id,
        "url": api_url,
        "fetched": True,
        "license": license_label or "unknown",
        "license_variant": license_variant_from_label(license_label),
        "raw": {
            "name": data.get("name"),
            "tags": data.get("tags"),
            "categories": data.get("categories"),
            "premium": data.get("premium"),
            "creator": (data.get("creator") or {}).get("name") if isinstance(data.get("creator"), dict) else None,
        },
    }
    return summary


def probe_rive_metadata(source: str, limit: int = 30000) -> dict[str, Any] | None:
    """Best-effort Rive asset page scrape.

    Rive has no public metadata API as of 2026-07. Public hosted assets live at
    https://cdn.rive.app/.../<file>.riv, but the canonical human-friendly page is
    the Rive editor share URL. We attempt to scrape the page (when given one) for
    license hints in JSON-LD, og:description, or embedded JSON.
    """
    parsed = urlparse(source)
    host = parsed.netloc.lower()
    is_rive_cdn = "rive.app" in host or "cdn.rive" in host
    if not (is_rive_cdn or "rive.app" in host):
        return None
    info: dict[str, Any] = {
        "host": "rive.app" if "rive.app" in host else host,
        "asset_id": None,
        "url": source,
        "fetched": False,
        "license": "unknown",
        "license_variant": "unknown",
        "raw": {},
    }
    # Try to derive a slug from the URL path; some Rive share URLs end with /<id>
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if parts:
        info["asset_id"] = parts[-1].split(".")[0]
    # Page scrape: if the URL is a cdn.rive.app raw asset, we have no JSON to scrape;
    # we treat that as "host detected, no per-asset metadata" rather than fake a fetch.
    if is_rive_cdn and not parsed.scheme.startswith("http"):
        return info
    try:
        text, headers, _ = fetch_text(source, limit=limit)
    except (URLError, HTTPError, TimeoutError, ValueError) as exc:
        info["raw"]["reason"] = f"page fetch failed: {exc}"
        return info
    # JSON-LD license
    m = re.search(r'"@type"\s*:\s*"CreativeWork".*?"license"\s*:\s*"([^"]+)"', text, re.S | re.I)
    if m:
        info["license"] = m.group(1).strip()
        info["license_variant"] = license_variant_from_label(info["license"])
        info["fetched"] = True
        info["raw"]["path"] = "json-ld"
    if info["license"] == "unknown":
        m = re.search(r'"license"\s*:\s*"([^"]{2,40})"', text, re.I)
        if m:
            info["license"] = m.group(1).strip()
            info["license_variant"] = license_variant_from_label(info["license"])
            info["fetched"] = True
            info["raw"]["path"] = "inline-json"
    if info["license"] == "unknown":
        m = re.search(r'<meta[^>]+name=["\']og:description["\'][^>]+content=["\']([^"\']+)', text, re.I)
        if m:
            info["raw"]["og_description"] = m.group(1).strip()[:300]
            info["fetched"] = True
            info["raw"]["path"] = "og-description"
    return info


def _sketchfab_extract_uid(url: str) -> str | None:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    parts = [p for p in path.split("/") if p]
    # Canonical: /3d-models/<slug>-<uid>, uid is a hex string at the end.
    if len(parts) >= 2 and parts[0] in {"3d-models", "models"}:
        tail = parts[-1]
        m = re.search(r"([a-f0-9]{16,})$", tail)
        if m:
            return m.group(1)
    # Fallback: any path segment that is a long hex string
    for seg in parts:
        m = re.search(r"([a-f0-9]{16,})", seg)
        if m:
            return m.group(1)
    return None


def _sketchfab_scrape_license(html: str) -> dict[str, Any]:
    """Best-effort license scrape from a Sketchfab model page.

    Tries: 1) embedded JSON-LD `license` field, 2) og:description hint, 3) '__NEXT_DATA__'
    JSON payload's license / user license fields.
    """
    info: dict[str, Any] = {"license": "unknown", "license_variant": "unknown", "raw": {}}

    # JSON-LD
    m = re.search(r'"@type"\s*:\s*"3DModel".*?"license"\s*:\s*"([^"]+)"', html, re.S | re.I)
    if m:
        info["license"] = m.group(1).strip()
        info["license_variant"] = license_variant_from_label(m.group(1))
    if info["license"] == "unknown":
        m = re.search(r'"license"\s*:\s*"([^"]{2,40})"', html, re.I)
        if m:
            info["license"] = m.group(1).strip()
            info["license_variant"] = license_variant_from_label(m.group(1))
    if info["license"] == "unknown":
        m = re.search(r'<meta[^>]+name=["\']og:description["\'][^>]+content=["\']([^"\']+)', html, re.I)
        if m:
            info["raw"]["og_description"] = m.group(1).strip()[:300]
    # __NEXT_DATA__ JSON (Sketchfab Next.js app often embeds license / name)
    m = re.search(r"__NEXT_DATA__\s*=\s*(\{.+?\})\s*</script>", html, re.S)
    if m:
        try:
            data = json.loads(m.group(1))
            payload = data.get("props", {}).get("pageProps", {}).get("model", {}) if isinstance(data, dict) else {}
            if payload:
                lic = payload.get("license") or payload.get("licenseLabel") or "unknown"
                if isinstance(lic, dict):
                    lic = lic.get("label") or lic.get("name") or "unknown"
                info["license"] = str(lic).strip() or info["license"]
                info["license_variant"] = license_variant_from_label(info["license"])
                info["raw"]["name"] = payload.get("name")
                info["raw"]["uid"] = payload.get("uid")
        except (json.JSONDecodeError, AttributeError):
            pass
    return info


def probe_polyhaven_metadata(source: str, limit: int = 30000) -> dict[str, Any] | None:
    """Best-effort Poly Haven metadata probe.

    Poly Haven pages and APIs usually expose license posture clearly (typically CC0).
    We try page JSON-LD / inline JSON first; if the source is a direct asset URL, we
    still return provider-default metadata when the host matches.
    """
    parsed = urlparse(source)
    host = parsed.netloc.lower()
    if "polyhaven.com" not in host and "dl.polyhaven.org" not in host:
        return None
    info: dict[str, Any] = {
        "host": "polyhaven.com",
        "asset_id": None,
        "url": source,
        "fetched": False,
        "license": "CC0-1.0",
        "license_variant": "cc0",
        "raw": {"reason": "provider default"},
    }
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if parts:
        info["asset_id"] = parts[-1].split(".")[0]
    try:
        text, headers, _ = fetch_text(source, limit=limit)
    except (URLError, HTTPError, TimeoutError, ValueError):
        return info
    m = re.search(r'"license"\s*:\s*"([^"]+)"', text, re.I)
    if m:
        info["license"] = m.group(1).strip()
        info["license_variant"] = license_variant_from_label(info["license"])
        info["fetched"] = True
        info["raw"] = {"path": "inline-json"}
    return info


def probe_khronos_gltf_metadata(source: str, limit: int = 30000) -> dict[str, Any] | None:
    """Best-effort metadata for Khronos glTF sample models.

    The canonical sample-model repo is public; many assets are CC-BY 4.0, but not all.
    We detect the known repository/paths and return a conservative per-asset posture.
    """
    parsed = urlparse(source)
    host = parsed.netloc.lower()
    normalized = source.lower()
    if "github.com" not in host and "raw.githubusercontent.com" not in host:
        return None
    if "gltf-sample-models" not in normalized and "khronosgroup" not in normalized:
        return None
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    asset_id = None
    # Tree URLs: github.com/<org>/glTF-Sample-Models/tree/<sha>/2.0/<ModelName>
    # Blob URLs: github.com/<org>/glTF-Sample-Models/blob/main/2.0/<ModelName>/README.md
    # Raw URLs: raw.githubusercontent.com/<org>/glTF-Sample-Models/<sha>/2.0/<ModelName>/...
    for idx, part in enumerate(parts):
        if part == "2.0" and 0 < idx < len(parts) - 1:
            asset_id = parts[idx + 1]
            break
    if asset_id is None and "2.0" in parts:
        idx = parts.index("2.0")
        if idx > 0:
            asset_id = parts[idx - 1]
    info: dict[str, Any] = {
        "host": host,
        "asset_id": asset_id,
        "url": source,
        "fetched": False,
        "license": "per-model (often CC-BY-4.0)",
        "license_variant": "cc-by",
        "raw": {"reason": "repo-pattern default"},
    }
    try:
        text, headers, _ = fetch_text(source, limit=limit)
        if "CC-BY" in text or "Creative Commons Attribution" in text:
            info["license"] = "CC-BY-4.0"
            info["license_variant"] = "cc-by"
            info["fetched"] = True
            info["raw"] = {"path": "body-match"}
        elif "CC0" in text:
            info["license"] = "CC0-1.0"
            info["license_variant"] = "cc0"
            info["fetched"] = True
            info["raw"] = {"path": "body-match"}
    except (URLError, HTTPError, TimeoutError, ValueError):
        pass
    return info


def probe_sketchfab_metadata(source: str, limit: int = 30000) -> dict[str, Any] | None:
    """Best-effort Sketchfab per-asset license probe.

    Strategy:
      1. Extract model UID from URL.
      2. Try the public Sketchfab API endpoint (no auth, may rate-limit).
      3. Fall back to scraping the public model page.
    """
    parsed = urlparse(source)
    host = parsed.netloc.lower()
    if "sketchfab" not in host:
        return None
    uid = _sketchfab_extract_uid(source)
    if not uid:
        return {
            "host": "sketchfab.com",
            "uid": None,
            "fetched": False,
            "license": "unknown",
            "license_variant": "unknown",
            "raw": {"reason": "no model uid found in URL"},
        }
    api_url = f"https://api.sketchfab.com/v3/models/{uid}"
    info: dict[str, Any] = {
        "host": "sketchfab.com",
        "uid": uid,
        "fetched": False,
        "license": "unknown",
        "license_variant": "unknown",
        "raw": {},
    }
    try:
        text, headers, _ = fetch_text(api_url, limit=limit)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {}
        lic = (
            data.get("license")
            or data.get("licenseLabel")
            or data.get("user", {}).get("license")
            if isinstance(data.get("user"), dict)
            else data.get("user", {}).get("license")
        )
        if lic is not None:
            if isinstance(lic, dict):
                label = lic.get("label") or lic.get("name") or lic.get("slug") or "unknown"
                info["raw"]["license_slug"] = lic.get("slug")
            else:
                label = str(lic)
            info["license"] = label.strip() or "unknown"
            info["license_variant"] = license_variant_from_label(info["license"])
            info["fetched"] = True
            info["raw"]["name"] = data.get("name")
            info["raw"]["uid"] = data.get("uid")
    except (URLError, HTTPError, TimeoutError, ValueError):
        pass
    if info["license"] == "unknown":
        try:
            page_url = f"https://sketchfab.com/3d-models/{uid}"
            text, headers, _ = fetch_text(page_url, limit=limit)
            scraped = _sketchfab_scrape_license(text)
            if scraped.get("license") and scraped["license"] != "unknown":
                info.update(scraped)
                info["fetched"] = True
                info["raw"]["scrape_path"] = page_url
        except (URLError, HTTPError, TimeoutError, ValueError):
            pass
    return info


def infer_metadata_authority(meta: dict[str, Any] | None) -> str | None:
    if not meta:
        return None
    if meta.get("fetched") and meta.get("raw", {}).get("path") in {"json-ld", "inline-json", "body-match"}:
        return "scraped_page"
    if meta.get("fetched") and meta.get("url", "").startswith("https://api."):
        return "confirmed_docs"
    if meta.get("raw", {}).get("reason") == "provider default":
        return "provider-default"
    return "manual-needed"


def infer_metadata_confidence(meta: dict[str, Any] | None) -> str | None:
    authority = infer_metadata_authority(meta)
    if authority in {"confirmed_docs", "scraped_page"}:
        return "high"
    if authority == "provider-default":
        return "medium"
    if authority == "manual-needed":
        return "low"
    return None


def infer_reuse_posture(classification: str, risk: str, high_risk_flags: list[str], intent: str) -> str:
    if classification == "restricted":
        return "blocked"
    if risk == "copyleft-or-caution":
        return "blocked"
    if high_risk_flags:
        if intent in ADAPTIVE_INTENTS:
            return "allowed-adapt-with-risk"
        return "allowed-direct-with-risk"
    if classification in {"licensed", "user-owned", "user-provided"}:
        if intent in ADAPTIVE_INTENTS:
            return "allowed-adapt"
        return "allowed-direct"
    if classification in {"public-but-unlicensed", "unknown"}:
        if intent in ADAPTIVE_INTENTS:
            return "allowed-adapt"
        return "allowed-direct-with-risk"
    return "allowed-adapt-with-risk"


def aggregate_license_evidence(discovery: list[dict[str, Any]]) -> str:
    """Combine license label from primary page + discovered pages; prefer the most specific non-unknown."""
    for entry in discovery:
        if entry["license"] not in {"", "unknown"}:
            return entry["license"]
    return "unknown"


def build_report(source: str, kind: str, intent: str, image_prompt: str = "") -> dict[str, Any]:
    text = ""
    headers: dict[str, str] = {}
    final_url = source
    fetch_error = None
    try:
        text, headers, final_url = fetch_text(source)
        final_url = str(final_url or source)
    except (URLError, HTTPError, TimeoutError, ValueError) as exc:
        fetch_error = str(exc)

    normalized_final_url: str = str(final_url or source)
    image_prompt_lower = image_prompt.lower().strip()
    primary_license = classify_license(text) if text else "unknown"
    primary_classification = source_classification(kind, headers, text, primary_license) if text else "unknown"

    discovery = probe_license_pages(source, text) if text and kind in {"website", "repo"} else []
    aggregated_license = aggregate_license_evidence([{"license": primary_license}] + discovery)
    classification = primary_classification
    license_label = primary_license
    if aggregated_license != "unknown":
        license_label = aggregated_license
        if primary_classification in {"public-but-unlicensed", "unknown"} and license_risk(license_label) == "permissive":
            classification = "licensed"

    risk = license_risk(license_label)
    high_risk_flags = detect_high_risk(normalized_final_url, kind, intent, text)
    for entry in discovery:
        if entry["restricted_hits"]:
            high_risk_flags.append(f"license page exposes restrictions: {entry['url']}")

    provider = detect_provider(normalized_final_url)
    cdn_provider = detect_cdn_provider(normalized_final_url)
    asset_cdn = detect_asset_cdn(normalized_final_url)
    lookalike_hits = detect_lookalike_pattern(normalized_final_url)
    motion_metadata = None
    sketchfab_metadata = None
    rive_metadata = None
    polyhaven_metadata = None
    khronos_gltf_metadata = None
    if cdn_provider is not None and cdn_provider.get("kind") == "motion-asset":
        if cdn_provider.get("provider") == "LottieFiles":
            motion_metadata = probe_motion_metadata(normalized_final_url)
        elif cdn_provider.get("provider") == "Rive":
            rive_metadata = probe_rive_metadata(normalized_final_url)
    if asset_cdn is not None and asset_cdn.get("provider") == "Sketchfab":
        sketchfab_metadata = probe_sketchfab_metadata(normalized_final_url)
    polyhaven_metadata = probe_polyhaven_metadata(normalized_final_url)
    if polyhaven_metadata is None:
        khronos_gltf_metadata = probe_khronos_gltf_metadata(normalized_final_url)
    if provider and license_label == "unknown" and provider["default_license"] not in {"per-file", "unknown"}:
        license_label = provider["default_license"]
        risk = license_risk(license_label)
        if primary_classification in {"public-but-unlicensed", "unknown"} and risk == "permissive":
            classification = "licensed"

    recommendations: list[str] = []
    needs_clarification = False
    if lookalike_hits:
        needs_clarification = True
        for hit in lookalike_hits:
            high_risk_flags.append(f"lookalike risk: {hit['label']} (matched '{hit['needle']}')")
    if classification == "restricted" and intent in HIGH_RISK_INTENTS:
        needs_clarification = True
        recommendations.append("Source is restricted (paywall/auth/robots/watermark); bypass is not allowed. Switch to structure-only analysis or ask for permission.")
    elif classification in {"public-but-unlicensed", "unknown"} and intent in HIGH_RISK_INTENTS:
        needs_clarification = True
        recommendations.append("Source classification is unknown or public-but-unlicensed; direct verbatim reuse needs explicit user approval. Adaptation (layout, structure, composition, spacing, visual anatomy) is allowed; record source + risk in evidence.")
    if risk == "copyleft-or-caution":
        needs_clarification = True
        recommendations.append("License is copyleft / nonstandard (LGPL/GPL/AGPL/SSPL/custom). Escalate to user with risk note before reuse; do not auto-replace either — ask.")
    if high_risk_flags and intent in HIGH_RISK_INTENTS:
        needs_clarification = True
        recommendations.append("Asset/brand risk signal detected (logo, premium, celebrity, character, lookalike). Prefer substitute, omit, or ask for explicit ownership/permission; adaptation only.")
    if not discovery and primary_license == "unknown" and kind in {"website", "repo"}:
        recommendations.append("No license/terms page found; treat as unknown and record reason in evidence. Adaptation is allowed; direct verbatim reuse needs explicit user approval.")
    if provider is not None:
        cat = provider["category"]
        if cat == "icon-library":
            if intent in {"direct-reuse", "copy-from", "clone", "1:1"}:
                recommendations.append(f"Matched icon library {provider['provider']}; use the official package directly (npm) and record version + license in evidence.")
            else:
                recommendations.append(f"Matched icon library {provider['provider']}; preferred path is the official package over ad-hoc asset downloads.")
        elif cat == "illustration-library":
            recommendations.append(f"Matched illustration source {provider['provider']}; adaptation is allowed. {provider['hint']}")
        elif cat == "stock-photo":
            recommendations.append(f"Matched stock photo source {provider['provider']}; cite the photo URL, check model/trademark releases separately, and record license in evidence. {provider['hint']}")
        elif cat == "3d-library":
            recommendations.append(f"Matched 3D source {provider['provider']}; adaptation is allowed. {provider['hint']}")
    if cdn_provider is not None:
        recommendations.append(f"Matched public CDN {cdn_provider['provider']} ({cdn_provider['kind']}); {cdn_provider['hint']}")
    if asset_cdn is not None:
        recommendations.append(f"Matched asset CDN {asset_cdn['provider']} ({asset_cdn['kind']}); {asset_cdn['hint']}")
    if motion_metadata is not None:
        if motion_metadata.get("fetched"):
            variant = motion_metadata.get("license_variant") or "unknown"
            if variant == "premium-or-pro":
                if intent in HIGH_RISK_INTENTS:
                    needs_clarification = True
                recommendations.append(
                    f"Probed LottieFiles API for asset {motion_metadata['asset_id']}; reported license = {motion_metadata['license']} (variant: premium-or-pro). "
                    f"Premium/Pro animation needs an active LottieFiles plan for redistribution; record asset id + license + creator; download and commit the .json under the project asset path."
                )
            elif variant in {"cc-by", "cc0", "free-tier", "standard"}:
                recommendations.append(
                    f"Probed LottieFiles API for asset {motion_metadata['asset_id']}; reported license = {motion_metadata['license']} (variant: {variant}). "
                    f"Allowed for reuse. Download the .json and commit it under the project asset path; apply attribution when required (CC-BY)."
                )
            else:
                recommendations.append(
                    f"Probed LottieFiles API for asset {motion_metadata['asset_id']}; reported license = {motion_metadata['license']} (variant: {variant}). "
                    f"Treat as allowed-adaptation; record asset id + license + creator in evidence and download the .json under the project asset path."
                )
        else:
            recommendations.append(
                f"LottieFiles API probe for asset {motion_metadata['asset_id']} did not return a body; treat license as unknown. Adaptation is allowed; for verbatim redistribution verify manually at https://lottiefiles.com/{motion_metadata['asset_id']} and record the license in evidence."
            )
    if rive_metadata is not None:
        if rive_metadata.get("fetched") and rive_metadata.get("license") not in {"unknown", ""}:
            variant = rive_metadata.get("license_variant") or "unknown"
            recommendations.append(
                f"Rive page scrape for {rive_metadata.get('url')} reported license = {rive_metadata['license']} (variant: {variant}). "
                f"Treat as scraped_page evidence; record the runtimes it is bound to (Standard/Pro/Team) and the asset's redistribution license in evidence."
            )
        else:
            recommendations.append(
                f"Rive has no public metadata API; the URL {rive_metadata.get('url')} could not be probed. "
                f"Open the asset in the Rive editor, record the runtimes (Standard/Pro/Team) and redistribution license, and download the .riv under the project asset path."
            )
    if polyhaven_metadata is not None:
        if polyhaven_metadata.get("fetched"):
            recommendations.append(
                f"Poly Haven page scrape for {polyhaven_metadata.get('url')} reported license = {polyhaven_metadata['license']} (variant: {polyhaven_metadata.get('license_variant', 'unknown')}). "
                f"Poly Haven assets are typically CC0-1.0; download the original .glb/.exr/.hdr and commit under the project asset path; record attribution as 'Poly Haven'."
            )
        else:
            recommendations.append(
                f"Poly Haven URL {polyhaven_metadata.get('url')} matched; provider default is CC0-1.0. "
                f"Adaptation is allowed; for verbatim redistribution, open the asset page on polyhaven.com, download the .glb/.exr/.hdr, and confirm the license in evidence."
            )
    if khronos_gltf_metadata is not None:
        if khronos_gltf_metadata.get("fetched"):
            recommendations.append(
                f"Khronos glTF Sample-Models probe for {khronos_gltf_metadata.get('asset_id') or khronos_gltf_metadata.get('url')} reported license = {khronos_gltf_metadata['license']} (variant: {khronos_gltf_metadata.get('license_variant', 'unknown')}). "
                f"Pin the repo path + commit sha in evidence; many models are CC-BY-4.0 and require attribution."
            )
        else:
            recommendations.append(
                f"Khronos glTF Sample-Models URL {khronos_gltf_metadata.get('url')} matched; default posture is CC-BY-4.0. "
                f"Adaptation is allowed; for verbatim redistribution, open the model folder in github.com/KhronosGroup/glTF-Sample-Models, confirm the license, and pin the commit sha in evidence."
            )
    if sketchfab_metadata is not None:
        uid = sketchfab_metadata.get("uid")
        if sketchfab_metadata.get("fetched") and sketchfab_metadata.get("license") not in {"unknown", ""}:
            variant = sketchfab_metadata.get("license_variant") or "unknown"
            if variant == "premium-or-pro":
                if intent in HIGH_RISK_INTENTS:
                    needs_clarification = True
                recommendations.append(
                    f"Sketchfab per-asset probe for model {uid or '?'} succeeded; reported license = {sketchfab_metadata['license']} (variant: premium-or-pro). "
                    f"Sketchfab Premium downloads need a paid plan; record model id + license + creator; download the .glb under the project asset path."
                )
            elif variant in {"cc-by", "cc0", "free-tier", "standard"}:
                recommendations.append(
                    f"Sketchfab per-asset probe for model {uid or '?'} succeeded; reported license = {sketchfab_metadata['license']} (variant: {variant}). "
                    f"Allowed for reuse. Record model id + license + creator; download the .glb and commit under the project asset path; apply attribution when required (CC-BY)."
                )
            else:
                recommendations.append(
                    f"Sketchfab per-asset probe for model {uid or '?'} succeeded; reported license = {sketchfab_metadata['license']} (variant: {variant}). "
                    f"Treat as allowed-adaptation; record model id + license + creator and download the .glb under the project asset path."
                )
        else:
            reason = sketchfab_metadata.get("raw", {}).get("reason", "API and page scrape both failed or no uid")
            recommendations.append(
                f"Sketchfab per-asset probe for model {uid or '?'} could not confirm license ({reason}). "
                f"Adaptation is allowed; for verbatim redistribution, verify the model license at https://sketchfab.com/search?type=models and record it in evidence."
            )
    if image_prompt_lower:
        prompt_provider = None
        for entry in PROVIDER_HINTS:
            if entry["provider"].lower() in image_prompt_lower:
                prompt_provider = entry
                break
            for alias in (entry.get("aliases") or ()):
                if alias.lower() in image_prompt_lower:
                    prompt_provider = entry
                    break
            if prompt_provider is not None:
                break
        prompt_motion_host = None
        for entry in CDN_HINTS:
            for alias in (entry.get("package_aliases") or ()):
                if alias.lower() in image_prompt_lower:
                    prompt_motion_host = entry
                    break
            if prompt_motion_host is not None:
                break
        if prompt_provider is not None and provider is not None and prompt_provider["provider"] == provider["provider"]:
            recommendations.append(
                f"Image prompt names the curated provider {provider['provider']}; the URL also matches the same provider. "
                f"Skip the CDN, install the official package locally (npm/pip/cargo/etc as applicable) or commit the assets under the project path, "
                f"and record the version + license in evidence."
            )
        elif prompt_provider is not None and cdn_provider is not None:
            recommendations.append(
                f"Image prompt names the curated provider {prompt_provider['provider']} but the URL is on the public CDN {cdn_provider['provider']}. "
                f"Self-host the official {prompt_provider['provider']} package instead of hotlinking the CDN, "
                f"and record the version + license in evidence."
            )
        elif prompt_provider is not None and provider is None and cdn_provider is None:
            recommendations.append(
                f"Image prompt names the curated provider {prompt_provider['provider']}; preferred path is to install the official {prompt_provider['provider']} package locally rather than fetching a remote URL."
            )
        elif prompt_motion_host is not None and cdn_provider is not None and prompt_motion_host["provider"] == cdn_provider["provider"]:
            aliases_preview = ", ".join((prompt_motion_host.get("package_aliases") or ())[:3]) or "lottie/rive"
            recommendations.append(
                f"Image prompt names a {cdn_provider['provider']} package ({aliases_preview}); the URL is on the same motion-asset host. "
                f"Prefer the official npm package (e.g. install via npm) over hotlinking the .json/.riv; record the version + license in evidence."
            )
        elif prompt_motion_host is not None and cdn_provider is not None and cdn_provider.get("kind") == "cdn":
            aliases_preview = ", ".join((prompt_motion_host.get("package_aliases") or ())[:3]) or "lottie/rive"
            recommendations.append(
                f"Image prompt names a {prompt_motion_host['provider']} package ({aliases_preview}) but the URL is on the public CDN {cdn_provider['provider']}. "
                f"Install the official {prompt_motion_host['provider']} package via npm (e.g. @lottiefiles/lottie-player) and commit a self-hosted copy under the project asset path; record the version + license in evidence."
            )
    if image_prompt_lower and cdn_provider is not None and cdn_provider.get("kind") == "motion-asset":
        motion_keywords = ("lottie", "rive", "lordicon", "motion", "animation", "animated")
        motion_packages: tuple[str, ...] = cdn_provider.get("package_aliases") or ()
        if any(k in image_prompt_lower for k in motion_keywords) or any(pkg in image_prompt_lower for pkg in motion_packages):
            recommendations.append(
                f"Image prompt mentions motion/animation (or a motion package like {', '.join(motion_packages[:3]) or 'lottie/rive'}) and the URL is on the motion-asset host {cdn_provider['provider']}. "
                f"Download the .json/.riv/.lottie asset and commit it under the project asset path so motion is reproducible offline; "
                f"record the asset's exact license + attribution posture in evidence."
            )
    if image_prompt_lower and asset_cdn is not None:
        spatial_keywords = ("3d", "gltf", "glb", "three.js", "threejs", "r3f", "react-three-fiber", "spline", "model-viewer", "babylon", "scene", "mesh")
        if any(k in image_prompt_lower for k in spatial_keywords):
            recommendations.append(
                f"Image prompt mentions 3D/spatial content and the URL is on the asset host {asset_cdn['provider']}. "
                f"Download the asset locally (glb/gltf/usdz/scene bundle as applicable), pin its source/commit/version, and record the exact model/runtime license in evidence instead of hotlinking the remote asset at runtime."
            )
    if lookalike_hits:
        for hit in lookalike_hits:
            recommendations.append(f"Lookalike pattern: {hit['hint']}")
    reuse_posture = infer_reuse_posture(classification, risk, high_risk_flags, intent)
    if not recommendations:
        recommendations.append("No immediate blocker detected from fetched metadata; adaptation is allowed. Record source + permission status in evidence before direct verbatim reuse.")

    return {
        "schema": "legal-source-check/v1",
        "source": source,
        "final_url": normalized_final_url,
        "kind": kind,
        "intent": intent,
        "image_prompt": image_prompt,
        "fetch_error": fetch_error,
        "headers": {
            "content-type": headers.get("content-type", ""),
            "x-robots-tag": headers.get("x-robots-tag", ""),
        },
        "license": license_label,
        "primary_license": primary_license,
        "license_risk": risk,
        "source_classification": classification,
        "reuse_posture": reuse_posture,
        "high_risk_flags": high_risk_flags,
        "license_pages_probed": discovery,
        "provider": provider,
        "cdn_provider": cdn_provider,
        "asset_cdn": asset_cdn,
        "motion_metadata": motion_metadata,
        "rive_metadata": rive_metadata,
        "polyhaven_metadata": polyhaven_metadata,
        "khronos_gltf_metadata": khronos_gltf_metadata,
        "metadata_authority": {
            "lottie": infer_metadata_authority(motion_metadata),
            "rive": infer_metadata_authority(rive_metadata),
            "sketchfab": infer_metadata_authority(sketchfab_metadata),
            "polyhaven": infer_metadata_authority(polyhaven_metadata),
            "khronos_gltf": infer_metadata_authority(khronos_gltf_metadata),
        },
        "metadata_confidence": {
            "lottie": infer_metadata_confidence(motion_metadata),
            "rive": infer_metadata_confidence(rive_metadata),
            "sketchfab": infer_metadata_confidence(sketchfab_metadata),
            "polyhaven": infer_metadata_confidence(polyhaven_metadata),
            "khronos_gltf": infer_metadata_confidence(khronos_gltf_metadata),
        },
        "lookalike_hits": lookalike_hits,
        "needs_user_clarification": needs_clarification,
        "recommendations": recommendations,
    }


def resolve_evidence_path(args: argparse.Namespace) -> Path | None:
    if args.out:
        return Path(args.out).resolve()
    if args.project_root and args.task_id:
        safe_task = re.sub(r"[^A-Za-z0-9_.-]", "_", args.task_id)
        return (Path(args.project_root).resolve() / ".opencode" / "evidence" / safe_task / "legal-source-check.json")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventory external source + license/risk posture before reuse")
    ap.add_argument("--source", required=True, help="External URL to inspect")
    ap.add_argument("--kind", choices=["website", "repo", "asset", "auto"], default="auto")
    ap.add_argument("--intent", choices=["reference-only", "style-equivalent", "direct-reuse", "copy-from", "clone", "1:1"], default="reference-only")
    ap.add_argument("--json", action="store_true", help="Emit JSON to stdout")
    ap.add_argument("--summary-only", action="store_true", help="Emit short human summary to stdout")
    ap.add_argument("--out", help="Write report JSON to this file (parent dirs are created)")
    ap.add_argument("--project-root", help="Project root for default evidence path (paired with --task-id)")
    ap.add_argument("--task-id", help="Task id for default evidence path; required with --project-root")
    ap.add_argument("--image-prompt", default="", help="Optional image-generation or asset prompt to combine with CDN/provider hints")
    args = ap.parse_args()

    parsed = urlparse(args.source)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        print(f"error: source must be a valid http/https URL: {args.source}", file=sys.stderr)
        return 2
    if (args.project_root and not args.task_id) or (args.task_id and not args.project_root):
        print("error: --project-root and --task-id must be used together", file=sys.stderr)
        return 2

    kind = kind_from_url(args.source) if args.kind == "auto" else args.kind
    report = build_report(args.source, kind, args.intent, image_prompt=args.image_prompt)

    out_path = resolve_evidence_path(args)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.summary_only:
        print(f"source: {report['source']}")
        print(f"final_url: {report['final_url']}")
        print(f"kind: {report['kind']}")
        print(f"intent: {report['intent']}")
        if report.get("image_prompt"):
            print(f"image_prompt: {report['image_prompt']}")
        print(f"license: {report['license']} ({report['license_risk']})")
        print(f"classification: {report['source_classification']}")
        if "reuse_posture" in report:
            print(f"reuse_posture: {report['reuse_posture']}")
        print(f"needs_user_clarification: {report['needs_user_clarification']}")
        if report.get("provider"):
            prov = report["provider"]
            print(f"provider: {prov['provider']} ({prov['category']}) default_license={prov['default_license']}")
            print(f"provider_hint: {prov['hint']}")
        if report.get("cdn_provider"):
            cdn = report["cdn_provider"]
            print(f"cdn_provider: {cdn['provider']} ({cdn['kind']}) default_license={cdn['default_license']}")
            print(f"cdn_hint: {cdn['hint']}")
        if report.get("asset_cdn"):
            asset = report["asset_cdn"]
            print(f"asset_cdn: {asset['provider']} ({asset['kind']}) default_license={asset['default_license']}")
            print(f"asset_cdn_hint: {asset['hint']}")
        if report.get("motion_metadata"):
            mm = report["motion_metadata"]
            fetched = mm.get("fetched", False)
            print(f"motion_metadata: host={mm.get('host')} asset_id={mm.get('asset_id')} fetched={fetched} license={mm.get('license')} variant={mm.get('license_variant')}")
        if report.get("sketchfab_metadata"):
            sm = report["sketchfab_metadata"]
            fetched = sm.get("fetched", False)
            print(f"sketchfab_metadata: uid={sm.get('uid')} fetched={fetched} license={sm.get('license')} variant={sm.get('license_variant')}")
        if report.get("rive_metadata"):
            rm = report["rive_metadata"]
            fetched = rm.get("fetched", False)
            print(f"rive_metadata: asset_id={rm.get('asset_id')} fetched={fetched} license={rm.get('license')} variant={rm.get('license_variant')}")
        if report.get("polyhaven_metadata"):
            pm = report["polyhaven_metadata"]
            fetched = pm.get("fetched", False)
            print(f"polyhaven_metadata: asset_id={pm.get('asset_id')} fetched={fetched} license={pm.get('license')} variant={pm.get('license_variant')}")
        if report.get("khronos_gltf_metadata"):
            km = report["khronos_gltf_metadata"]
            fetched = km.get("fetched", False)
            print(f"khronos_gltf_metadata: asset_id={km.get('asset_id')} fetched={fetched} license={km.get('license')} variant={km.get('license_variant')}")
        if report.get("metadata_authority"):
            print(f"metadata_authority: {report['metadata_authority']}")
        if report.get("metadata_confidence"):
            print(f"metadata_confidence: {report['metadata_confidence']}")
        if report.get("lookalike_hits"):
            print("lookalike_hits:")
            for hit in report["lookalike_hits"]:
                print(f"  - {hit['label']} matched '{hit['needle']}': {hit['hint']}")
        if report.get("license_pages_probed"):
            print("license_pages_probed:")
            for entry in report["license_pages_probed"]:
                print(f"  - {entry['url']} license={entry['license']} restricted_hits={len(entry['restricted_hits'])}")
        if report['high_risk_flags']:
            print("high_risk_flags:")
            for item in report['high_risk_flags']:
                print(f"  - {item}")
        if report['recommendations']:
            print("recommendations:")
            for item in report['recommendations']:
                print(f"  - {item}")
        if out_path:
            print(f"wrote: {out_path}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if out_path:
            print(f"wrote: {out_path}", file=sys.stderr)

    if report["needs_user_clarification"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
