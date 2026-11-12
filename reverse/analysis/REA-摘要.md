# REA 静态逆向摘要（逐文件模式）

- 输入子集：`rea-input/`　源文件 34 个，成功 **33**，失败 1　总耗时 1754.6s
- 证据包目录：`analysis/rea-evidence/`（合计 216.8 MiB）
- 失败清单见 `analysis/rea-perfile.json` 的 `error` 字段

## 技术栈命中（全部证据包累计）

| 关键词 | 次数 |
|---|---|
| stripe | 28322 |
| webpack | 5846 |
| sse | 2177 |
| next | 902 |
| websocket | 110 |
| react | 58 |
| turbopack | 48 |
| redux | 9 |
| i18n | 6 |
| three | 4 |
| sentry | 3 |
| antd | 3 |

## 业务语义命中

| 关键词 | 次数 |
|---|---|
| project | 2709 |
| export | 1442 |
| endpoint | 1257 |
| request | 600 |
| credit | 484 |
| token | 445 |
| fetch | 419 |
| model | 260 |
| response | 205 |
| upload | 180 |
| price | 122 |
| websocket | 110 |
| canvas | 92 |
| subscription | 52 |
| localstorage | 43 |
| timeline | 13 |
| authorization | 12 |

## 口径提醒

- 证据给的是「代码里有什么」；字段**取值**仍以抓包/UI 实测为准。
- 逐文件模式的证据是分片的：要查某文件的结构就看 `analysis/rea-evidence/<file>.json`。
