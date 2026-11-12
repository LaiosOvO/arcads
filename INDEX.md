# Arcads 逆向

生成时间：2026-11-12 19:32:01 +0800
父目录：`/Users/admin/Desktop/data/fde/marketing/product/arcads`

## 状态总表

| 项目 | 目录 | 入口 | 资源(清单/磁盘) | 体积 | sha256 不符 | 错误 | REA 证据 |
|---|---|---|---|---|---|---|---|
| reverse | `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse` | https://www.arcads.ai/ | 1986/3603 | 277.8 MiB | 0 | 317 | 0.0 MiB / 35 文件 |

## 各项目交付物

### reverse

- 索引：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/INDEX.md`
- 清单：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/manifest.json` ｜ 校验：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/checksums.sha256`
- 抓包证据：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/capture` ｜ 分析：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis`
- 镜像：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/mirror`（3603 文件 / 277.8 MiB）
- REA 静态逆向：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/REA-摘要.md`（证据包 0.0 MiB，输入 35 文件，退出码 0）

## 通用口径

- **seen**：已落盘文件 / 已抓到的抓包证据；**unknown**：未抓到，不代表不存在。
- 未登录、未点开的页面其私有接口不会出现，一律记 unknown，禁止推测补全。
- `capture/` 已脱敏（Bearer/JWT/Cookie/token 键/邮箱/会话 ID）；业务 UUID 保留便于核查。
- 静态命中的 API/路由是**候选**，实际契约以 `capture/network-requests.json` 与 `cdp-response-bodies.json` 为准。
- REA 证据包给的是技术栈与语义结构；REA 命中的字段只证明代码里存在，取值仍以抓包/DOM 实测为准。
