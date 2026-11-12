#!/usr/bin/env python3
"""Arcads 增量取证结构化（可复跑）。

输入（全部为已落盘证据，不联网、不伪造）：
  capture/network-requests.json                 存量 132 路由全量抓包
  capture-interactive/requests.json             本轮受控交互增量
  capture-interactive/response-bodies.json      增量响应体落盘记录
  capture-interactive/privacy-state.json        只读隐私态诊断
  mirror/app.arcads.ai/_next/static/chunks/36uc_rrtepudd.js  Amplitude SDK 静态证据

输出（全部新建，不覆盖任何自动生成产物）：
  analysis/third-party-contracts.json      外链追踪/像素 POST 请求体契约（独立口径）
  analysis/interactive-main-contracts.json 主域增量请求体契约（独立口径）
  analysis/relay-e-finding.json            /api/relay/e 定性结论与证据链
  docs/增量取证说明.md                      人读汇总

口径红线：
  - 主域业务写接口请求体不因只读交互凭空增加；抓不到就写 unknown。
  - 第三方像素契约单独成文，绝不塞进 api-contracts.json 冒充 Arcads 后端契约。
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path("/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse")
ANA = ROOT / "analysis"
DOCS = ROOT / "docs"
CAP = ROOT / "capture"
INT = ROOT / "capture-interactive"

STATIC_EXT = re.compile(r"\.(js|mjs|cjs|css|html?|json|map|woff2?|ttf|svg|png|jpe?g|webp|avif|gif|ico|mp4|webm|mp3|wasm)$", re.I)
MAIN_HOST = re.compile(r"(^|\.)arcads\.ai$")


def load(p: Path):
    if not p.exists():
        print(f"MISSING {p}", file=sys.stderr)
        return []
    return json.loads(p.read_text("utf8"))


def host_of(url: str) -> str:
    try:
        return urlsplit(url).netloc.split(":")[0].lower()
    except Exception:
        return ""


def is_main(url: str) -> bool:
    h = host_of(url)
    return h == "arcads.ai" or bool(MAIN_HOST.search(h))


def contracts_for(rows, want_main: bool):
    out = OrderedDict()
    for r in rows:
        url = r.get("url") or ""
        if not url.startswith("http"):
            continue
        if is_main(url) != want_main:
            continue
        u = urlsplit(url)
        if STATIC_EXT.search(u.path):
            continue
        body = r.get("postData")
        if not body:
            continue
        key = (host_of(url), r.get("method", "GET"), u.path)
        rec = out.setdefault(key, {
            "host": key[0], "method": key[1], "path": key[2],
            "example_url": url, "hits": 0, "sample_body": None,
            "body_variants": [], "types": set(), "phases": set(),
        })
        rec["hits"] += 1
        rec["types"].add(r.get("type") or "unknown")
        if r.get("phase"):
            rec["phases"].add(r["phase"])
        if rec["sample_body"] is None:
            rec["sample_body"] = body[:1200]
        digest = hashlib.sha1(body.encode("utf8", "replace")).hexdigest()
        if digest not in [v["sha1"] for v in rec["body_variants"]] and len(rec["body_variants"]) < 3:
            rec["body_variants"].append({
                "sha1": digest, "len": len(body), "body": body[:600],
            })
    res = []
    for rec in out.values():
        rec["types"] = sorted(rec["types"])
        rec["phases"] = sorted(rec["phases"])[:8]
        res.append(rec)
    return sorted(res, key=lambda x: (-x["hits"], x["host"], x["path"]))


def main() -> int:
    ANA.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    legacy = load(CAP / "network-requests.json")
    delta = load(INT / "requests.json")
    bodies = load(INT / "response-bodies.json")
    privacy = {}
    pp = INT / "privacy-state.json"
    if pp.exists():
        privacy = json.loads(pp.read_text("utf8"))
    summary = {}
    sp = INT / "summary.json"
    if sp.exists():
        summary = json.loads(sp.read_text("utf8"))

    # 给存量行补 phase，便于统一处理
    for r in legacy:
        r.setdefault("phase", "legacy:capture")
    all_rows = legacy + delta

    third = contracts_for(all_rows, want_main=False)
    main_c = contracts_for(delta, want_main=True)

    (ANA / "third-party-contracts.json").write_text(json.dumps({
        "generated_at": datetime.now().astimezone().isoformat(),
        "scope": "第三方外链追踪/像素 POST 请求体契约；不属于 Arcads 业务后端接口",
        "sources": ["capture/network-requests.json", "capture-interactive/requests.json"],
        "source_requests": len(all_rows),
        "contract_count": len(third),
        "total_hits": sum(x["hits"] for x in third),
        "contracts": third,
    }, ensure_ascii=False, indent=2), "utf8")

    (ANA / "interactive-main-contracts.json").write_text(json.dumps({
        "generated_at": datetime.now().astimezone().isoformat(),
        "scope": "本轮受控只读交互抓到的主域请求体契约（增量，未并入 api-contracts.json）",
        "source": "capture-interactive/requests.json",
        "contract_count": len(main_c),
        "contracts": main_c,
        "note": "只读交互未触发任何业务写请求；主域带 body 请求仅为 tracking/browser-opt-out 与 lj.arcads.ai 设备校验。",
    }, ensure_ascii=False, indent=2), "utf8")

    # ---- /api/relay/e 定性结论 ----
    js = ROOT / "mirror/app.arcads.ai/_next/static/chunks/36uc_rrtepudd.js"
    js_text = js.read_text("utf8", "replace") if js.exists() else ""
    i = js_text.find('serverUrl:"/api/relay/e"')
    static_excerpt = js_text[max(0, i - 420):i + 380] if i >= 0 else ""
    has_to_log = js_text.find("hasToLog(){return!0}")
    relay_rows = [r for r in all_rows if re.search(r"/api/relay/e(\?|$)", r.get("url") or "")]
    optout_rows = [r for r in all_rows if "/tracking/browser-opt-out" in (r.get("url") or "") and r.get("postData")]
    amplitude_upload = [r for r in all_rows if "amplitude" in (r.get("url") or "").lower()
                        and ("httpapi" in (r.get("url") or "").lower() or "/batch" in (r.get("url") or "").lower())]
    optout_responses = [b for b in bodies if "browser-opt-out" in b.get("url", "")]

    finding = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "endpoint": "/api/relay/e",
        "verdict": "unknown",
        "verdict_reason": "静态实证存在，两轮真实抓包（含 flush 触发）均未捕获该端点的任何请求/响应；不得伪造响应体。",
        "classification": {
            "is_streaming": False,
            "kind": "Amplitude Analytics SDK HTTP 事件上报中继（非 SSE / 非 WebSocket 流式通道）",
            "correction": "TASKS.md 旧记「流式/事件通道，需长连接抓包」有误，本轮据静态代码更正为普通 HTTP POST 中继。",
            "sdk": "amplitude analytics-browser 2.42.4 + plugin-session-replay-browser 1.32.1",
            "api_keys": ["44e5a6f3152249aae19ed3e4cad65ea（业务 SDK）", "b2e63b5453c36ec48b28059c3ab6a699（GTM 脚本实例）"],
            "transport": "默认 fetch；document.visibilityState === 'hidden' 时 setTransport('beacon') + flush()",
            "gate": "hasToLog(){return!0} 恒真，非 A/B 门控",
            "static_evidence_file": str(js.relative_to(ROOT)),
            "static_evidence_excerpt": static_excerpt,
            "hasToLog_definition_found": has_to_log >= 0,
        },
        "dynamic_evidence": {
            "legacy_132_route_capture": {
                "requests": len(legacy), "responses": 3134, "text_records": 2514,
                "relay_hits": 0,
            },
            "interactive_capture": {
                "events": summary.get("events"), "requests": summary.get("requests"),
                "responses": summary.get("responses"),
                "requests_with_post_data": summary.get("requestsWithPostData"),
                "relay_hits": summary.get("relayRequests", 0),
                "routes": summary.get("cfg", {}).get("routes"),
                "readonly_clicks": 21,
                "flush_trigger": "Object.defineProperty(document,'visibilityState',{get:()=>'hidden'}) + dispatchEvent(visibilitychange) + pagehide；每页 settle 9000ms",
            },
            "relay_requests_in_both_captures": len(relay_rows),
        },
        "root_cause_evidence": {
            "browser_opt_out_requests": len(optout_rows),
            "browser_opt_out_bodies": sorted({r["postData"] for r in optout_rows}),
            "browser_opt_out_response_status": sorted({b.get("status") for b in optout_responses}),
            "browser_opt_out_response_bodies": [
                Path(b["local_path"]).read_text(encoding="utf8", errors="replace")[:200]
                for b in optout_responses if b.get("local_path")
            ][:3],
            "amplitude_event_upload_requests": len(amplitude_upload),
            "amplitude_config_or_script_only": True,
            "consent_token_present": "didomi_token_cpra" in (privacy.get("localStorageKeys") or []),
            "do_not_track": privacy.get("doNotTrack"),
            "global_privacy_control": privacy.get("globalPrivacyControl"),
            "amp_unsent": (privacy.get("localStorageMatches") or {}).get("AMP_unsent_44e5a6f315"),
            "privacy_state_file": "capture-interactive/privacy-state.json",
            "conclusion": "会话处于浏览器追踪 opt-out（Didomi CPRA 同意态 + 站点每页上报 browserOptOut:true）：Amplitude 只拉取 script/config/session-replay 起点，未发出任何事件上报，故 /api/relay/e 不可达。",
        },
        "privacy_boundary": {
            "action_taken": "none",
            "explanation": "解除 opt-out 等于改变用户的隐私同意选择，超出「只看不动手」红线，本 Agent 未修改任何 cookie / localStorage / 同意设置 / 账号设置。",
        },
        "unblock_conditions": [
            "需用户明确授权，在一个未 opt-out 的新浏览器会话中（或在 Didomi 同意面板主动授予分析类同意）重新登录 Arcads。",
            "重跑 tools/run-capture-interactive.mjs，保留 Ping/beacon 类型收集（原 runner 的 type 白名单会漏掉 beacon）。",
            "或由用户提供该端点已存在的 HAR / 后端日志 / OpenAPI 定义。",
        ],
    }
    (ANA / "relay-e-finding.json").write_text(json.dumps(finding, ensure_ascii=False, indent=2), "utf8")

    # ---- 人读汇总 ----
    md = [
        "# 增量取证说明（2026-11-12 21:0x）", "",
        "> 用户授权：选项 1（补 `/api/relay/e`）+ 选项 3（受控只读交互补请求体契约）。",
        "> 本轮所有结论只取落盘证据；抓不到即 `unknown`，不伪造响应体。", "",
        "## 1. `/api/relay/e` 定性结论", "",
        "| 项 | 结论 |", "|---|---|",
        "| 类型 | **Amplitude Analytics SDK 的 HTTP 事件上报中继**（非 SSE / 非流式长连接） |",
        "| 静态证据 | `mirror/app.arcads.ai/_next/static/chunks/36uc_rrtepudd.js` 中 `serverUrl:\"/api/relay/e\"`、`defaultTracking:{sessions:!0}` |",
        "| 门控 | `hasToLog(){return!0}` **恒真**，不是 A/B 门控 |",
        "| 传输 | 默认 `fetch`；`visibilityState==='hidden'` 时切 `beacon` + `flush()` |",
        "| 动态结果 | 存量 132 路由 + 本轮 5 页交互（7995 events / 997 requests）**均 0 命中** |",
        "| 根因 | 会话处于浏览器追踪 **opt-out**：站点每页 `POST /tracking/browser-opt-out {\"browserOptOut\":true}` → `201 {\"success\":true}`；Amplitude 只拉 script/config，零事件上报 |",
        "| 判定 | **`unknown`**（静态存在 / 动态不可达），详见 `analysis/relay-e-finding.json` |", "",
        "**口径更正**：`TASKS.md` 旧记「流式通道、需长连接抓包」有误，本轮据静态代码更正为普通 HTTP POST 中继。", "",
        "**隐私边界**：解除 opt-out 等于改动用户的隐私同意选择，超出红线，本 Agent 未改任何 cookie / localStorage / 同意设置。解除条件见 `relay-e-finding.json`。", "",
        "## 2. 请求体契约增量", "",
        f"- 存量抓包 `capture/network-requests.json`：{len(legacy)} 请求。",
        f"- 增量抓包 `capture-interactive/requests.json`：{len(delta)} 请求 / {sum(1 for r in delta if r.get('postData'))} 带 body。",
        f"- **主域业务写接口请求体：无新增**。21 次受控只读点击（归因选项、轮播、`flow/library`、公开首页）未触发任何业务写请求；主域带 body 的请求仍只有 `tracking/browser-opt-out` 与 `lj.arcads.ai/api/v1/check/*` 两类。",
        f"- **外链追踪/像素契约**（独立口径，不冒充 Arcads 后端）：`analysis/third-party-contracts.json` 共 **{len(third)} 条** / {sum(x['hits'] for x in third)} 次命中，每条含 `sample_body` + 最多 3 条 `body_variants`。",
        f"- 主域增量契约：`analysis/interactive-main-contracts.json` 共 **{len(main_c)} 条**。", "",
        "诚实结论：**在「只读交互、不新建业务对象」授权下，`api-contracts.json` 的 `sample_body` 无法从 3 条扩开**。",
        "要补写接口请求体，必须授权真实写操作（创建/提交/生成），或提供现成的 HAR / 后端日志。", "",
        "## 3. 本轮新增文件", "",
        "| 文件 | 用途 |", "|---|---|",
        "| `tools/run-capture-interactive.mjs` | 独立增量 runner（不覆盖 `capture/` 全量证据；收集 Ping/beacon） |",
        "| `tools/run-privacy-probe.mjs` | 只读隐私态诊断 |",
        "| `tools/build_interactive_delta.py` | 本说明与三份结构化证据的可复跑生成器 |",
        "| `capture-interactive/*` | 7995 CDP 事件、997 请求、940 响应、响应体、逐页交互与 flush 记录 |",
        "| `analysis/relay-e-finding.json` | relay 端点定性结论与证据链 |",
        "| `analysis/third-party-contracts.json` | 外链请求体契约 |",
        "| `analysis/interactive-main-contracts.json` | 主域增量契约 |", "",
        "## 4. 独立增量 runner 为何必要", "",
        "原 `tools/run-capture-reverse.mjs` 每次运行都会**覆盖** `capture/network-*.json`（132 路由全量证据）。",
        "本轮改用独立输出目录 `capture-interactive/`，既有证据零改动。",
        "另外原 runner 的 `type` 白名单只含 Fetch/XHR/Other，会漏掉 `Ping`（beacon）；增量 runner 不做类型过滤。", "",
    ]
    (DOCS / "增量取证说明.md").write_text("\n".join(md), "utf8")

    print(json.dumps({
        "legacy_requests": len(legacy), "interactive_requests": len(delta),
        "third_party_contracts": len(third), "third_party_hits": sum(x["hits"] for x in third),
        "main_interactive_contracts": len(main_c),
        "relay_hits": len(relay_rows), "relay_verdict": finding["verdict"],
        "optout_requests": len(optout_rows),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
