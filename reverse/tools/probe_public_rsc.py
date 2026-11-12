#!/usr/bin/env python3
"""对 paywall 之后的 app 路由做公开 RSC 探针（无登录态、无凭据、无写操作）。

Next.js App Router 的 `?_rsc` + `RSC: 1` 响应是公开的 flight 数据，
即使无订阅态也返回路由段树与静态资源引用（不含用户业务数据）。
本脚本用它补齐「后面页面」的结构信息，并下载其中新出现的 CSS chunk。

产物：
  capture-public/rsc-<route>.txt   逐路由 flight 原件
  analysis/public-rsc-probe.json   汇总清单
  mirror/app.arcads.ai/_next/static/chunks/*.css  补下载 CSS
"""
import concurrent.futures as cf
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "capture-cfg.json"
OUTDIR = ROOT / "capture-public"
ANALYSIS = ROOT / "analysis"
HOST_DIR = ROOT / "mirror" / "app.arcads.ai"

CSS_RE = re.compile(r'HL\["(/_next/static/[^"\]]+\.css)"')
JS_RE = re.compile(r'["\'](/_next/static/[^"\']+\.js)["\']')
SEG_RE = re.compile(r'"children":\["([^"]+)"')


def probe(route):
    name, url = route["name"], route["url"]
    sep = "&" if "?" in url else "?"
    target = f"{url}{sep}_rsc=probe"
    dest = OUTDIR / f"rsc-{name}.txt"
    cmd = [
        "curl", "-sS", "-L", "--max-time", "30",
        "-H", "RSC: 1", "-H", "Accept: */*",
        "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
        "-o", str(dest), "-w", "%{http_code}|%{content_type}|%{size_download}",
        target,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        code, ctype, size = (p.stdout or "000|||0").split("|", 2)
        status = int(code) if code.isdigit() else 0
        data = dest.read_bytes() if dest.exists() else b""
        text = data.decode("utf8", "replace")
        return {
            "route": name, "url": target, "status": status,
            "contentType": ctype, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "isFlight": "text/x-component" in ctype or text.lstrip().startswith(("0:", "1:")),
            "cssRefs": sorted(set(CSS_RE.findall(text))),
            "jsRefs": sorted(set(JS_RE.findall(text))),
            "segments": list(dict.fromkeys(SEG_RE.findall(text)))[:12],
            "bodyFile": str(dest.relative_to(ROOT)),
            "error": None if status == 200 else (p.stderr or "")[:160],
        }
    except Exception as e:
        return {"route": name, "url": target, "status": 0, "error": str(e)[:160],
                "cssRefs": [], "jsRefs": [], "segments": [], "isFlight": False, "bytes": 0}


def download(path):
    dest = HOST_DIR / path.lstrip("/")
    if dest.exists() and dest.stat().st_size > 0:
        return {"path": path, "status": "already", "bytes": dest.stat().st_size}
    tmp = dest.with_suffix(dest.suffix + ".part")
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-sS", "-L", "-o", str(tmp), "-w", "%{http_code}",
           "--max-time", "30", "https://app.arcads.ai" + path]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        code = (p.stdout or "").strip()[-3:]
        if code == "200" and tmp.exists() and tmp.stat().st_size:
            data = tmp.read_bytes()
            tmp.replace(dest)
            return {"path": path, "status": 200, "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest()}
        if tmp.exists():
            tmp.unlink()
        return {"path": path, "status": int(code) if code.isdigit() else 0, "bytes": 0}
    except Exception as e:
        return {"path": path, "status": 0, "bytes": 0, "error": str(e)[:120]}


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(CFG.read_text("utf8"))
    routes = [r for r in cfg["routes"]
              if urlsplit(r["url"]).netloc.split(":")[0].lower() == "app.arcads.ai"]
    print(f"app 路由 {len(routes)} 条，开始公开 RSC 探针", flush=True)
    results = []
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        for res in pool.map(probe, routes):
            results.append(res)
    ok = [r for r in results if r["status"] == 200 and r["isFlight"]]
    print(f"RSC flight 200：{len(ok)}/{len(routes)}", flush=True)

    css = sorted({p for r in results for p in r["cssRefs"]})
    print(f"flight 引用 CSS {len(css)} 个，检查/补下载", flush=True)
    css_result = []
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        for res in pool.map(download, css):
            css_result.append(res)

    report = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "method": "public GET <url>?_rsc=probe with RSC:1 header; no cookie, no auth, no writes",
        "why": "Next.js App Router flight payload exposes route segment tree and static asset refs even without a subscription",
        "routesProbed": len(routes),
        "flightOk": len(ok),
        "flightFailed": len(routes) - len(ok),
        "distinctCssRefs": len(css),
        "cssDownloaded": sum(1 for x in css_result if x["status"] == 200),
        "cssAlready": sum(1 for x in css_result if x["status"] == "already"),
        "cssFailed": [x for x in css_result if x["status"] not in (200, "already")],
        "limit": "flight 里没有用户项目/视频/积分等真实业务数据；本探针不提供登录态，不绕过 paywall 的业务授权",
        "results": results,
        "css": css_result,
    }
    (ANALYSIS / "public-rsc-probe.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), "utf8")
    print(f"写入 analysis/public-rsc-probe.json", flush=True)
    for r in ok[:6]:
        print(f"  {r['route']:32s} {r['bytes']:7d}B segs={r['segments'][:5]} css={len(r['cssRefs'])}")


if __name__ == "__main__":
    main()
