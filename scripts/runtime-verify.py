#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def http_check(base_url, path):
    url = base_url.rstrip('/') + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OpenCodeRuntimeVerify/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = resp.getcode()
            ctype = resp.headers.get('Content-Type', '')
            body = resp.read(200).decode('utf-8', 'ignore')
            return {"path": path, "ok": 200 <= status < 400, "status": status, "content_type": ctype, "sample": body}
    except urllib.error.HTTPError as e:
        body = e.read(200).decode('utf-8', 'ignore')
        return {"path": path, "ok": False, "status": e.code, "content_type": e.headers.get('Content-Type', ''), "sample": body}
    except Exception as e:
        return {"path": path, "ok": False, "status": None, "error": str(e)}


def file_check(root, rel_path, min_size=1):
    p = Path(root) / rel_path.lstrip('/')
    if not p.exists():
        return {"path": rel_path, "ok": False, "exists": False, "size": 0}
    size = p.stat().st_size
    return {"path": rel_path, "ok": size >= min_size, "exists": True, "size": size}


def env_check(key):
    val = os.environ.get(key)
    return {"key": key, "ok": bool(val), "present": bool(val)}


def main():
    ap = argparse.ArgumentParser(description='Runtime verifier for OpenCode tasks')
    ap.add_argument('--base-url', default='')
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--route', action='append', default=[])
    ap.add_argument('--asset', action='append', default=[])
    ap.add_argument('--env', action='append', default=[])
    ap.add_argument('--output', default='')
    args = ap.parse_args()

    result = {
        'base_url': args.base_url,
        'project_root': str(Path(args.project_root).resolve()),
        'routes': [],
        'assets': [],
        'env': [],
        'summary': {},
    }

    if args.base_url:
        for route in args.route:
            result['routes'].append(http_check(args.base_url, route))

    for asset in args.asset:
        result['assets'].append(file_check(args.project_root, asset))

    for key in args.env:
        result['env'].append(env_check(key))

    route_fail = [x for x in result['routes'] if not x.get('ok')]
    asset_fail = [x for x in result['assets'] if not x.get('ok')]
    env_fail = [x for x in result['env'] if not x.get('ok')]
    result['summary'] = {
        'route_failures': len(route_fail),
        'asset_failures': len(asset_fail),
        'env_failures': len(env_fail),
        'ok': not (route_fail or asset_fail or env_fail),
    }

    text = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text)
    print(text)
    return 0 if result['summary']['ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
