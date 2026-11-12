# reverse 抓取交付索引

生成时间：2026-11-12 21:23:44 +0800 ｜ 入口：`https://www.arcads.ai/`

| 路径 | 内容 |
|---|---|
| `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/mirror` | 原始字节镜像（host/path 结构，3603 文件 / 277.8 MiB） |
| `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/manifest.json` | URL→本地路径 + sha256 + 字节数 + content-type |
| `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/checksums.sha256` | 全量 sha256 校验清单 |
| `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/capture` | CDP 抓包：page-*.html、dom-*.json、network-events/responses/requests、cdp-response-bodies、performance-resources、截图（已脱敏） |
| `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis` | 逆向报告、静态切片、校验、脱敏报告 |
| `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/tools` | 可复现脚本（抓包/收敛/收尾） |

## paywall 之后页面的静态代码（F12 · 2026-11-12 22:0x）

无需付费 / 无需绕过鉴权：`/_next/static/` 是构建期静态产物，由 CDN 公开返回，paywall 只挡 SSR 渲染。

- 结论与边界：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/docs/paywall后页面静态代码说明.md`
- 静态接口契约（人读，525 条）：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/docs/静态接口契约清单.md`
- 静态接口契约（机读，含 zod 请求体字段）：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/static-endpoint-contracts.json`
- 补下载 94 个懒加载 chunk 的 SHA-256 清单：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/lazy-chunks.json`
- 公开 RSC 探针（74/98 路由拿到 flight 段树）：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/public-rsc-probe.json`；原件 `capture-public/rsc-*.txt`
- 三层证据与路由域差集：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/paywall-behind-static.json`（四层，含 RSC 摘要）
- 复跑脚本：`tools/fetch_lazy_chunks.py`、`tools/extract_static_endpoints.py`、`tools/probe_public_rsc.py`

> 口径：188 = 抓包实测端点；47 = 抓包主域契约（真实 `sample_body` 3 条）；525 = 代码静态声明契约（160 条 zod 请求体形状，未经实际调用）。三者互不冒充。

## 报告

- 逆向报告：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/reverse-逆向报告.md`
- 真实 API 契约：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/api-contracts.json`
- 静态切片：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/static-findings.json`
- 校验：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/verification.json`
- 脱敏记录：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/sanitization-report.json`
