#!/usr/bin/env python3
"""递归补全 Turbopack 懒加载 chunk（paywall 之后路由的静态代码）。

原理：Next.js/Turbopack 的路由级 JS 是构建期产物，放在 /_next/static/ 下由 CDN
公开返回；paywall 只挡 SSR 渲染，不挡静态资源。本脚本只做公开 GET，
不使用任何登录态、不绕过鉴权、不触碰支付/隐私设置。

种子：mirror/ 已有文件 + capture/page-*.html 里的 _next/static 引用。
收敛：每下载一个新 chunk，再解析它内部的 static/chunks/*.js 引用，BFS 至无新增。

产物：
  mirror/app.arcads.ai/_next/static/chunks/<name>.js   （补入既有镜像）
  mirror/app.arcads.ai/_next/static/<...>.css          （补 CSS）
  analysis/lazy-chunks.json                            （可复核清单）
"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
HOST_DIR = ROOT / "mirror" / "app.arcads.ai"
CHUNKS_DIR = HOST_DIR / "_next" / "static" / "chunks"
CAPTURE = ROOT / "capture"
ANALYSIS = ROOT / "analysis"
OUT = ANALYSIS / "lazy-chunks.json"
BASE = "https://app.arcads.ai"

PREFIX_RE = re.compile(r"(?:static/chunks/|_next/static/chunks/)([A-Za-z0-9_\-]+\.js)")
BARE_RE = re.compile(r"\b([0-9a-z][0-9a-z_\-]{9,19}\.js)\b")
STATIC_PATH_RE = re.compile(r"/_next/static/[A-Za-z0-9_\-./]+\.(?:js|css)")
# 第三方脚本名，不属本站 chunk
BARE_DENY = {"enterprise.js", "lite-yt-embed.js", "oaiq.min.js", "main.js"}

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def log(msg):
    print(msg, flush=True)


def http_get(url: str, dest: Path, timeout: int = 40):
    """返回 (status, bytes, sha256, err)。非 200 不落盘。"""
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = [
        "curl", "-sS", "-L", "-o", str(tmp),
        "-w", "%{http_code}", "--max-time", str(timeout),
        "-A", UA, "-H", "Accept: */*", url,
    ]
    for attempt in range(2):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)
            code = (p.stdout or "").strip()[-3:]
            if code == "200" and tmp.exists() and tmp.stat().st_size > 0:
                data = tmp.read_bytes()
                dest.parent.mkdir(parents=True, exist_ok=True)
                tmp.replace(dest)
                return 200, len(data), hashlib.sha256(data).hexdigest(), None
            if tmp.exists():
                tmp.unlink()
            if attempt == 1:
                return (int(code) if code.isdigit() else 0), 0, None, (p.stderr or "")[:200]
        except Exception as e:
            if tmp.exists():
                tmp.unlink()
            if attempt == 1:
                return 0, 0, None, str(e)[:200]
        time.sleep(0.6)
    return 0, 0, None, "unreachable"


def rel_dest(path: str) -> Path:
    """把 /_next/static/... 映射到 mirror/app.arcads.ai/..."""
    return HOST_DIR / path.lstrip("/")


def scan_refs(text: str):
    """返回 (带前缀的 chunk 名, 裸候选名)"""
    return set(PREFIX_RE.findall(text)), set(x for x in BARE_RE.findall(text) if x not in BARE_DENY)


def main():
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS.mkdir(parents=True, exist_ok=True)

    # ---------- 种子 ----------
    html_paths = sorted(CAPTURE.glob("page-*.html"))
    html_refs = set()
    for p in html_paths:
        html_refs |= set(x.split("?")[0] for x in STATIC_PATH_RE.findall(p.read_text("utf8", "replace")))
    log(f"HTML 页面 {len(html_paths)} 份，静态路径引用 {len(html_refs)} 条")

    have_chunks = set(p.name for p in CHUNKS_DIR.glob("*.js"))
    initial_count = len(have_chunks)
    log(f"镜像已有 chunk {initial_count} 个")

    # 已有 JS 内部引用的 chunk 名（含懒加载）
    seeds = set()
    bare_candidates = set()
    for p in sorted(CHUNKS_DIR.glob("*.js")):
        pref, bare = scan_refs(p.read_text("utf8", "replace"))
        seeds |= pref
        bare_candidates |= bare
    for path in html_refs:
        if "/chunks/" in path and path.endswith(".js"):
            seeds.add(path.rsplit("/", 1)[-1])

    known = set(seeds)
    queue = sorted(known - have_chunks)
    log(f"引用到的 chunk 名 {len(known)} 个，待下载 {len(queue)} 个")

    # ---------- BFS 下载 ----------
    downloaded, failed, not_chunk = [], [], []
    round_no = 0
    total_bytes = 0
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        while queue:
            round_no += 1
            log(f"--- round {round_no}: {len(queue)} 个 ---")
            futs = {
                pool.submit(http_get, f"{BASE}/_next/static/chunks/{n}", CHUNKS_DIR / n): n
                for n in queue
            }
            new_refs = set()
            for fut in cf.as_completed(futs):
                n = futs[fut]
                code, size, sha, err = fut.result()
                if code == 200:
                    total_bytes += size
                    downloaded.append({
                        "name": n, "round": round_no,
                        "url": f"{BASE}/_next/static/chunks/{n}",
                        "status": code, "bytes": size, "sha256": sha,
                    })
                    text = (CHUNKS_DIR / n).read_text("utf8", "replace")
                    pref, bare = scan_refs(text)
                    new_refs |= pref
                    bare_candidates |= bare
                elif code in (403, 404):
                    not_chunk.append({"name": n, "status": code})
                else:
                    failed.append({"name": n, "status": code, "error": err})
            have_chunks = set(p.name for p in CHUNKS_DIR.glob("*.js"))
            known |= new_refs
            queue = sorted(known - have_chunks - set(x["name"] for x in failed) - set(x["name"] for x in not_chunk))
            log(f"    ok={sum(1 for d in downloaded if d['round']==round_no)} "
                f"new_refs={len(new_refs)} next_round={len(queue)}")

    # ---------- 裸候选（仅做轻量探测，403/404 视为第三方名） ----------
    bare_pool = sorted(bare_candidates - have_chunks - set(d["name"] for d in downloaded)
                       - set(x["name"] for x in failed) - set(x["name"] for x in not_chunk)
                       - set(path.rsplit("/", 1)[-1] for path in html_refs))
    log(f"裸 token 候选 {len(bare_pool)} 个，逐个探测")
    bare_results = []
    if bare_pool:
        with cf.ThreadPoolExecutor(max_workers=8) as pool:
            futs = {pool.submit(http_get, f"{BASE}/_next/static/chunks/{n}", CHUNKS_DIR / n): n for n in bare_pool}
            for fut in cf.as_completed(futs):
                n = futs[fut]
                code, size, sha, err = fut.result()
                if code == 200:
                    total_bytes += size
                    downloaded.append({
                        "name": n, "round": "bare", "url": f"{BASE}/_next/static/chunks/{n}",
                        "status": code, "bytes": size, "sha256": sha,
                    })
                    bare_results.append({"name": n, "status": 200, "bytes": size})
                else:
                    bare_results.append({"name": n, "status": code})
                    not_chunk.append({"name": n, "status": code})

    # ---------- CSS ----------
    css_result = []
    css_paths = sorted(p for p in html_refs if p.endswith(".css"))
    for path in css_paths:
        dest = rel_dest(path)
        if dest.exists() and dest.stat().st_size > 0:
            css_result.append({"path": path, "status": "already", "bytes": dest.stat().st_size})
            continue
        code, size, sha, err = http_get(BASE + path, dest)
        css_result.append({"path": path, "status": code, "bytes": size, "sha256": sha, "error": err})

    # ---------- HTML 引用但缺失的普通 js（非 chunk 目录） ----------
    extra_result = []
    for path in sorted(html_refs):
        if not path.endswith(".js") or "/chunks/" in path:
            continue
        dest = rel_dest(path)
        if dest.exists() and dest.stat().st_size > 0:
            continue
        code, size, sha, err = http_get(BASE + path, dest)
        extra_result.append({"path": path, "status": code, "bytes": size, "sha256": sha, "error": err})

    final_count = len(list(CHUNKS_DIR.glob("*.js")))
    report = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "method": "public CDN GET of /_next/static/* ; no auth, no paywall bypass, no writes",
        "why": "Next.js/Turbopack route chunks are build-time static assets; paywall gates SSR rendering only",
        "seed": {
            "htmlPages": len(html_paths),
            "htmlStaticRefs": len(html_refs),
            "chunksBefore": initial_count,
            "referencedChunkNames": len(known),
        },
        "rounds": round_no,
        "downloaded": sorted(downloaded, key=lambda x: x["name"]),
        "downloadedCount": len(downloaded),
        "downloadedBytes": total_bytes,
        "failed": sorted(failed, key=lambda x: x["name"]),
        "notAChunk": sorted(not_chunk, key=lambda x: x["name"]),
        "bareCandidates": bare_results,
        "css": css_result,
        "extraStaticJs": extra_result,
        "chunksAfter": final_count,
        "note": "403 的裸 token 是第三方脚本名或不存在；静态资源返回 200 不代表业务接口可调用",
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), "utf8")
    log(f"\n完成：新增 {len(downloaded)} 个 chunk / {total_bytes/1048576:.2f} MiB；"
        f"chunk 总数 {initial_count} -> {final_count}")
    log(f"CSS {len(css_result)} 条；额外静态 JS {len(extra_result)} 条；失败 {len(failed)} 条；非 chunk {len(not_chunk)} 条")
    log(f"清单：{OUT}")


if __name__ == "__main__":
    main()
