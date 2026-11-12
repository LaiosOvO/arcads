# REA 静态逆向 CLI 运行记录（逐文件模式 · 补全轮）

- 项目根：`/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse`
- 输入子集：`rea-input/`（35 件：34 业务 JS chunk + 1 CSS）
- 分析模式：`rea analyze-javascript-application --detail summary --per-file`；单文件预算 900s / 堆 4096 MiB
- 结果：**33 成功**、**1 失败**；汇总耗时 1754.6 s
- 证据包：`analysis/rea-evidence/`（44 份，216.8 MiB）

## 逐文件状态

| # | 文件 | 状态 | 证据(MiB) | 耗时(s) | 备注 |
|---|---|---|---|---|---|
| 1 | 0gaw_nbtlfkp7.js | cached | 4.3 | - | 缓存复用 |
| 2 | 0kn7q9qwe55aq.js | cached | 3.6 | - | 缓存复用 |
| 3 | 0wn23v4b_tezt.js | cached | 2.5 | - | 缓存复用 |
| 4 | 143888573.js | cached | 6.6 | - | 缓存复用 |
| 5 | 162_iewo-akst.js | cached | 3.1 | - | 缓存复用 |
| 6 | 19ekwenty1wjj.js | cached | 2.3 | - | 缓存复用 |
| 7 | 1a6qwbp1h7k79.js | cached | 3.8 | - | 缓存复用 |
| 8 | 1r5s4-apsz6r7.js | cached | 2.5 | - | 缓存复用 |
| 9 | 1s65bzv6465hr.js | cached | 2.4 | - | 缓存复用 |
| 10 | 1tget77wi4xtj.js | cached | 3.1 | - | 缓存复用 |
| 11 | 21fxxjks_usoz.js | cached | 3.5 | - | 缓存复用 |
| 12 | 26dio4keg7x5l.js | cached | 4.2 | - | 缓存复用 |
| 13 | 26mwnd5hm_53p.js | cached | 6.6 | - | 缓存复用 |
| 14 | 29gqqkjrhea9d.js | cached | 2.9 | - | 缓存复用 |
| 15 | 2_6mitb_441ob.js | cached | 2.3 | - | 缓存复用 |
| 16 | 2apl0snz0wit5.js | cached | 3.5 | - | 缓存复用 |
| 17 | 2e_l8wsapyxcm.js | cached | 6.1 | - | 缓存复用 |
| 18 | 2ixnvjih1wvzt.js | failed | 0.0 | 913.6 | Provider cleanup could not be fully confirmed. Review the reported |
| 19 | 2ub59fy_2i454.js | cached | 3.3 | - | 缓存复用 |
| 20 | 2x669bobi7-9_.js | cached | 7.8 | - | 缓存复用 |
| 21 | 2ymtu4wdqg7vz.js | cached | 3.5 | - | 缓存复用 |
| 22 | 33aagglnpy5gk.js | cached | 2.5 | - | 缓存复用 |
| 23 | 35y1a7r6hhmyj.js | cached | 2.8 | - | 缓存复用 |
| 24 | 36uc_rrtepudd.js | ok | 7.3 | 833.9 |  |
| 25 | 3bzd7pat927hy.js | cached | 14.4 | - | 缓存复用 |
| 26 | 3i3_h784q36n6.js | cached | 2.7 | - | 缓存复用 |
| 27 | app_tooltips-modern.2959f864.js | cached | 14.1 | - | 缓存复用 |
| 28 | frame-modern.2762eddb.js | cached | 18.4 | - | 缓存复用 |
| 29 | main.MTkyOWEyMGMwMQ.js | cached | 16.3 | - | 缓存复用 |
| 30 | oaiq.min.js | cached | 5.4 | - | 缓存复用 |
| 31 | sdk.6be5dfc02bbd61b83a465667402bfd77489a7a04.js | cached | 18.1 | - | 缓存复用 |
| 32 | stripe.js | cached | 19.9 | - | 缓存复用 |
| 33 | ui-web-en-web.6be5dfc02bbd61b83a465667402bfd77489a7a04.js | cached | 7.6 | - | 缓存复用 |
| 34 | vendor-modern.e5315bcd.js | cached | 9.3 | - | 缓存复用 |

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

## 三轮收敛过程

| 轮次 | 输入 | 分析 JS | 成功 | 失败 | 预算 | 证据包 |
|---|---|---|---|---|---|---|
| 首轮 | 28 件（24 JS + 2 CSS + 2 HTML） | 24 | 17 | 7 | 240 s | 74.9 MiB |
| 补全 A | 35 件（34 JS + 1 CSS） | 34 | 32 | 2 | 400 s | 209.4 MiB |
| 补全 B | 35 件（34 JS + 1 CSS） | 34 | **33** | **1** | 900 s | **216.8 MiB** |

收敛路径：首轮 7 个失败 = 2 个超时 + 5 个「worker 存储失败」（日志实证为清理阶段 `spawn EPERM`，读进程表被沙箱拦，报错文案 `Provider cleanup could not be fully confirmed` 具误导性）。
补全 A 把 5 个存储失败包全部转成功；补全 B 把 `36uc_rrtepudd.js`（833.9 s）也拿下。
仅剩 `2ixnvjih1wvzt.js`（531 KB）在 900 s 仍未收敛 → 标 `unknown`，属工具对超长行/minified 病态结构的解析瓶颈，不再追预算。

## 口径提醒

- 证据包给的是**语义结构与技术栈**；接口契约以 `capture/` 流量 + `analysis/api-contracts.json` 为准。
- REA 命中字段名只证明**代码里存在**，取值仍需真实请求或 UI 实测。

