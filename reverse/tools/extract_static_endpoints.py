#!/usr/bin/env python3
"""从 Turbopack chunk 静态还原 makeEndpoint 声明式后端契约。

站点用如下形态声明接口（在 app.arcads.ai/_next/static/chunks/*.js 中）：
  (0,t.makeEndpoint)({newBackend:!0,url:()=>"/admin/featured-models",
    method:"POST",queryParamsSchema:z.void(),
    requestSchema:z.object({name:z.string()}),responseSchema:z.array(a)})

本脚本只做本地静态解析，不发网络请求、不模拟调用、不虚构请求体样本。
zod schema 仅提取顶层字段名/类型，作为「请求体结构」的静态证据，
与抓包得到的真实 sample_body 严格区分。

产物：
  analysis/static-endpoint-contracts.json
  analysis/paywall-behind-static.json
"""
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = ROOT / "mirror" / "app.arcads.ai" / "_next" / "static" / "chunks"
CAPTURE = ROOT / "capture"
ANALYSIS = ROOT / "analysis"

URL_RE = re.compile(
    r'url:\s*(?:\([^)]*\)\s*=>|\w+\s*=>)\s*("(?:[^"\\]|\\.)*"|`(?:[^`\\]|\\.)*`)'
)
METHOD_RE = re.compile(r'method:\s*"(\w+)"')
BACKEND_RE = re.compile(r'newBackend:\s*(!0|!1|true|false)')
CHUNK_REF_RE = re.compile(r'/_next/static/[A-Za-z0-9_\-./]+\.js')
FIELD_RE = re.compile(r'([A-Za-z_$][\w$]*)\s*:\s*[A-Za-z_$][\w$]*\.default\.(\w+)')
EXPORT_RE = re.compile(r'"([A-Za-z0-9_]*Endpoint)"\s*,\s*0\s*,\s*([A-Za-z0-9_$]+)')

ROUTE_PAGES = {
    "dashboard": "page-dashboard.html",
    "flow": "page-flow.html",
    "flow-use": "page-flow-use.html",
    "dashboard-settings": "page-dashboard-settings.html",
    "dashboard-settings-billing": "page-dashboard-settings-billing.html",
    "dashboard-settings-public-api": "page-dashboard-settings-public-api.html",
    "admin": "page-admin.html",
    "onboarding-paywall": "page-onboarding-paywall.html",
    "onboarding-attribution": "page-onboarding-attribution.html",
}


def object_end(s: str, start: int) -> int:
    """从 '{' 起做平衡花括号扫描，跳过字符串/模板字符串内容。"""
    depth = 0
    quote = None
    i = start
    n = len(s)
    while i < n:
        c = s[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in "'\"`":
            quote = c
            i += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def norm_path(raw: str):
    """把 url 字面量/模板归一化成可比较的路径。"""
    v = raw[1:-1]
    v = v.split("?", 1)[0]
    v = re.sub(r"\$\{[^}]*\}", ":param", v)
    if not v.startswith("/"):
        v = "/" + v
    return v


def schema_segment(block: str, key: str) -> str:
    """粗略截取 requestSchema/queryParamsSchema 的值文本（到下一个同级 key）。"""
    i = block.find(key + ":")
    if i < 0:
        return ""
    j = i + len(key) + 1
    # 到下一个 ",xxxSchema:" 或对象结束
    m = re.search(r',\s*\w+Schema\s*:', block[j:])
    end = j + m.start() if m else len(block)
    return block[j:end]


def top_fields(seg: str):
    """从 zod object({...}) 里取顶层字段名/类型，忽略嵌套。"""
    if "void()" in seg[:80] or ".void()" in seg[:80]:
        return []
    return [{"name": a, "zodType": b} for a, b in FIELD_RE.findall(seg[:1800])][:40]


def main():
    files = sorted(CHUNKS.glob("*.js"))
    out = {}
    calls = 0
    parsed = 0
    unparsed = []
    for p in files:
        s = p.read_text("utf8", "replace")
        export_names = {}
        for name, var in EXPORT_RE.findall(s):
            export_names.setdefault(var, name)
        pos = 0
        while True:
            i = s.find("makeEndpoint", pos)
            if i < 0:
                break
            pos = i + 12
            brace = s.find("{", i, i + 60)
            if brace < 0:
                continue
            end = object_end(s, brace)
            if end < 0 or end - brace > 20000:
                continue
            block = s[brace:end]
            calls += 1
            mu = URL_RE.search(block)
            mm = METHOD_RE.search(block)
            if not mu or not mm:
                unparsed.append({
                    "chunk": p.name,
                    "reason": "url_not_literal" if not mu else "method_missing",
                    "snippet": block[:180],
                })
                continue
            raw = mu.group(1)
            path = norm_path(raw)
            path_unresolved = raw.startswith("`") and path.startswith("/:param")
            method = mm.group(1).upper()
            nb = BACKEND_RE.search(block)
            backend = "https://api.arcads.ai" if (nb and nb.group(1) in ("!0", "true")) else (
                "legacy-aws-lambda" if nb else "unspecified"
            )
            req = schema_segment(block, "requestSchema")
            query = schema_segment(block, "queryParamsSchema")
            resp = schema_segment(block, "responseSchema")
            key = f"{method} {path}"
            rec = out.setdefault(key, {
                "method": method,
                "path": path,
                "pathRaw": raw,
                "pathUnresolved": path_unresolved,
                "backend": backend,
                "requestFields": [],
                "queryFields": [],
                "responseShape": "",
                "exportNames": [],
                "sources": [],
                "hits": 0,
            })
            rec["hits"] += 1
            if p.name not in rec["sources"]:
                rec["sources"].append(p.name)
            if not rec["requestFields"]:
                rec["requestFields"] = top_fields(req)
            if not rec["queryFields"]:
                rec["queryFields"] = top_fields(query)
            if not rec["responseShape"]:
                if "array" in resp[:120]:
                    rec["responseShape"] = "array"
                elif "object" in resp[:120]:
                    rec["responseShape"] = "object"
                elif "void" in resp[:120]:
                    rec["responseShape"] = "void"
                elif "string" in resp[:120]:
                    rec["responseShape"] = "string"
                else:
                    rec["responseShape"] = "unknown"
            # 找该端点变量名，反查 Turbopack 的 e.s(["XxxEndpoint",0,var]) 导出名
            window = s[max(0, i - 100):i + 20]
            vm = re.search(r'([A-Za-z0-9_$]+)\s*=\s*\(0,\s*[A-Za-z0-9_$]+\.makeEndpoint', window)
            if not vm:
                vm = re.search(r'([A-Za-z0-9_$]+)\s*=\s*\([^)]*\)\s*makeEndpoint', window)
            if vm and vm.group(1) in export_names:
                nm = export_names[vm.group(1)]
                if nm not in rec["exportNames"]:
                    rec["exportNames"].append(nm)
            parsed += 1

    endpoints = sorted(out.values(), key=lambda x: (x["path"], x["method"]))
    with_body = [e for e in endpoints if e["requestFields"]]

    # ---- 与抓包得到的 api-spec 比对 ----
    spec = json.loads((ROOT / "docs" / "api-spec.json").read_text("utf8"))
    spec_paths = set()
    for e in spec.get("endpoints", []):
        p = e.get("path") or ""
        spec_paths.add(p.split("?", 1)[0])
    for e in endpoints:
        e["inCapturedApiSpec"] = e["path"] in spec_paths
    new_paths = [e for e in endpoints if not e["inCapturedApiSpec"]]

    contracts = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "method": "static parsing of makeEndpoint({...}) declarations in local mirror chunks",
        "evidenceType": "static-code-derived schema, NOT captured request bodies",
        "disclaimer": "requestFields 来自 zod 顶层字段，代表代码声明的请求体形状；不等于抓包观测到的真实请求体，也不代表已实际调用成功。",
        "chunksScanned": len(files),
        "makeEndpointCalls": calls,
        "definitionsParsed": parsed,
        "definitionsUnparsed": len(unparsed),
        "unparsedReasons": dict(Counter(x["reason"] for x in unparsed)),
        "unparsedSamples": unparsed[:20],
        "distinctContracts": len(endpoints),
        "withRequestFields": len(with_body),
        "withExportNames": sum(1 for e in endpoints if e["exportNames"]),
        "pathUnresolved": sum(1 for e in endpoints if e["pathUnresolved"]),
        "byMethod": dict(Counter(e["method"] for e in endpoints)),
        "notInCapturedSpec": len(new_paths),
        "comparisonNote": "api-spec.json 是抓包观测到的 URL path（含 SSR 页面与第三方域），本文件是代码声明的相对后端 base 的业务 API；两者口径不同，非交集不等于抓包遗漏。",
        "capturedSpecEndpoints": spec.get("endpoint_count"),
        "endpoints": endpoints,
    }
    (ANALYSIS / "static-endpoint-contracts.json").write_text(
        json.dumps(contracts, ensure_ascii=False, indent=2), "utf8")

    # ---- 人读清单（可复核、按路径首段分组） ----
    lines = [
        "# Arcads 静态还原接口契约清单",
        "",
        f"- 生成时间：{contracts['generatedAt']}",
        f"- 来源：本地 `mirror/app.arcads.ai/_next/static/chunks/*.js` 共 {len(files)} 个 chunk 中的 `makeEndpoint({{...}})` 声明，**纯静态解析**",
        f"- 规模：{calls} 处声明 / 解析 {parsed} 处 / 去重 **{len(endpoints)} 条契约**；其中 {len(with_body)} 条带请求体字段",
        f"- 方法分布：" + "、".join(f"{k} {v}" for k, v in sorted(contracts['byMethod'].items())),
        "",
        "> `请求体字段` 来自 zod `requestSchema` 顶层字段，是**代码声明的形状**，不是抓包观测到的真实请求体；",
        "> 也不代表接口已被实际调用成功。真实 sample_body 见 `analysis/api-contracts.json`。",
        "> 后端 base：`newBackend:!0` → `https://api.arcads.ai`，否则 → 旧 AWS Lambda 网关。",
        "> 路径中 `:param` 为模板变量归一化结果；标 `?` 的路径前缀本身是变量，无法从静态代码确定基路径。",
        "",
    ]
    groups = defaultdict(list)
    for e in endpoints:
        seg = e["path"].strip("/").split("/", 1)[0] or "(root)"
        groups[seg].append(e)
    for seg in sorted(groups):
        items = groups[seg]
        lines += [f"## /{seg}（{len(items)} 条）", "",
                  "| 方法 | 路径 | 请求体字段（zod 顶层） | 导出名 |", "|---|---|---|---|"]
        for e in sorted(items, key=lambda x: (x["path"], x["method"])):
            fields = ", ".join(f["name"] for f in e["requestFields"]) or "—"
            names = ", ".join(e["exportNames"][:2]) or "—"
            p = ("? " if e["pathUnresolved"] else "") + e["path"]
            lines.append(f"| `{e['method']}` | `{p}` | {fields} | {names} |")
        lines.append("")
    (ROOT / "docs" / "静态接口契约清单.md").write_text("\n".join(lines), "utf8")

    # ---- 路由域 -> 专属 chunk 差集 ----
    def refs(name):
        p = CAPTURE / name
        if not p.exists():
            return None
        return set(x.split("?")[0] for x in CHUNK_REF_RE.findall(p.read_text("utf8", "replace")))

    R = {k: refs(v) for k, v in ROUTE_PAGES.items()}
    base = R.get("onboarding-paywall") or set()
    attribution = R.get("onboarding-attribution") or set()
    baseline = base | attribution
    domains = {}
    for k, v in R.items():
        if v is None:
            continue
        only = sorted(v - baseline)
        domains[k] = {
            "htmlRefs": len(v),
            "exclusiveVsOnboarding": len(only),
            "exclusiveChunks": [x.rsplit("/", 1)[-1] for x in only],
            "bytes": sum((CHUNKS / x.rsplit("/", 1)[-1]).stat().st_size
                         for x in only if (CHUNKS / x.rsplit("/", 1)[-1]).exists()),
        }
    # paywall 后业务代码特征（以 dashboard 专属集为样本）
    biz = domains.get("dashboard", {}).get("exclusiveChunks", [])
    kw = ["credits", "generate", "video", "actor", "voice", "workspace", "folder",
          "project", "subscription", "stripe", "paywall", "flow", "upload", "render",
          "canvas", "template", "library", "billing"]
    kw_hits = Counter()
    for n in biz:
        p = CHUNKS / n
        if not p.exists():
            continue
        s = p.read_text("utf8", "replace").lower()
        for w in kw:
            if w in s:
                kw_hits[w] += 1

    lazy = json.loads((ANALYSIS / "lazy-chunks.json").read_text("utf8"))
    rsc_file = ANALYSIS / "public-rsc-probe.json"
    rsc_summary = None
    if rsc_file.exists():
        rd = json.loads(rsc_file.read_text("utf8"))
        segs = Counter()
        for x in rd["results"]:
            for s in x["segments"]:
                if not s.startswith("$"):
                    segs[s] += 1
        rsc_summary = {
            "routesProbed": rd["routesProbed"],
            "flightOk": rd["flightOk"],
            "http404": rd["flightFailed"],
            "distinctCssRefs": rd["distinctCssRefs"],
            "cssDownloaded": rd["cssDownloaded"],
            "topSegments": dict(segs.most_common(12)),
            "file": "analysis/public-rsc-probe.json",
            "originals": "capture-public/rsc-*.txt",
        }
    behind = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "question": "能否直接获取 paywall 之后页面的 JS 等信息",
        "answer": "能：Turbopack 路由级 chunk 是构建期静态产物，由 CDN 公开返回；paywall 只挡 SSR 渲染与业务数据，不挡静态资源。",
        "evidence": {
            "publicGetProbe": "https://app.arcads.ai/_next/static/chunks/<real-name>.js -> HTTP 200 text/javascript；伪造名 -> 403",
            "htmlChunkUnion": len(set().union(*[v for v in R.values() if v])),
            "chunksBefore": lazy["seed"]["chunksBefore"],
            "chunksAfter": lazy["chunksAfter"],
            "lazyChunksAdded": lazy["downloadedCount"],
            "lazyChunkNature": "Turbopack 懒加载 vendor 库（hls.js M3U8 解析、PostCSS/sourcemap 等），非页面业务代码",
            "dashboardExclusiveChunks": len(biz),
            "businessKeywordCoverage": dict(kw_hits.most_common()),
        },
        "routeDomains": domains,
        "publicRsc": rsc_summary,
        "staticEndpointContracts": {
            "file": "analysis/static-endpoint-contracts.json",
            "distinct": len(endpoints),
            "withRequestFields": len(with_body),
            "newVsCapturedSpec": len(new_paths),
        },
        "limits": [
            "静态代码不等于运行时数据：页面 SSR/RSC 响应仍会被重定向到 onboarding/paywall，没有订阅态的真实数据。",
            "requestFields 是 zod 声明形状，不是抓包观测到的 sample_body；真实 POST/PUT 请求体仍需授权交互。",
            "新补 chunk 尚未全部纳入 REA per-file 分析（单文件最长 900s 超时），本轮只做静态字符串级取证。",
        ],
    }
    (ANALYSIS / "paywall-behind-static.json").write_text(
        json.dumps(behind, ensure_ascii=False, indent=2), "utf8")

    print(f"chunks={len(files)} makeEndpoint={calls} parsed={parsed} unparsed={len(unparsed)}")
    print(f"distinct contracts={len(endpoints)} withRequestFields={len(with_body)} "
          f"withExportNames={contracts['withExportNames']} pathUnresolved={contracts['pathUnresolved']} "
          f"notInCapturedSpec={len(new_paths)} byMethod={contracts['byMethod']}")
    for k, v in domains.items():
        print(f"  {k:34s} htmlRefs={v['htmlRefs']:3d} exclusive={v['exclusiveVsOnboarding']:3d} bytes={v['bytes']}")
    print("wrote analysis/static-endpoint-contracts.json, analysis/paywall-behind-static.json")


if __name__ == "__main__":
    main()
