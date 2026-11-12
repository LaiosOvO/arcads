# Arcads 逆向 · 执行轨迹（trace.md）

> 文档单写者：本轮抓取员。每一步写清「命令 → 产物 → 实测结果 → 判定」，数字只取落盘证据文件，不凭记忆。
> 关联：[issue.md](./issue.md)（问题清单） · [../../AGENTS.md](../../AGENTS.md)（总领取登记）

| 项 | 值 |
|---|---|
| 领取站点 | Arcads `https://www.arcads.ai/`（应用域 `https://app.arcads.ai/`） |
| 主用 Skill | `/Users/admin/skills/ego-site-capture`（Ego Site Capture v12），配套 `rea-rebuild` / `ego-rea-fullstack-rebuild` |
| 浏览器运行时 | `ego-browser v2.2.0`（真实 Chromium + CDP，**独立会话**） |
| 静态逆向 | `rea 6.8.0`（`analyze-javascript-application --per-file`） |
| 工程 ROOT | `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/` |
| 执行窗口 | 2026-11-12 14:52 – 19:32（GMT+8；含 19:00–19:30 的 REA 补全轮） |
| 最终准出 | `evidence gate PASS 17/17` + `handoff PASS`（`gate --strict` 三项全过） |
| 红线 | 只看不动手；`seen` / `unknown` 分开；SSR 原文作基线；`mirror/` 与 `capture/` 只读；不伪造任何凭据 |

统一变量：

```bash
export SKILLS=/Users/admin/skills
export CAP=$SKILLS/ego-site-capture/scripts/capture_ctl.py
export BASE=/Users/admin/Desktop/data/fde/marketing/product/arcads
export ROOT=$BASE/reverse
```

---

## 一、站点选型与桌面端优先复盘

| 动作 | 结果 | 判定 |
|---|---|---|
| 读 `/Users/admin/skills` 下 4 份逆向 skill | `ego-site-capture`（网页取证）、`rea-rebuild`（复刻路线）、`ego-rea-fullstack-rebuild`（全栈重建）、`rea-desktop-reverse`（后补：桌面端原生逆向） | ✅ |
| 桌面端优先核查（用户 14:59 指令） | 四候选中**仅 Bramble 有真实 GUI 桌面端**（Mac dmg + Windows exe 已发布）；Arcads 为纯网页 SaaS（REA 证据包仅命中 next/turbopack/SSR/SSE，无 Electron/Tauri/PyQt 痕迹），PostPlus 为 CLI + MCP 无 GUI | ✅ Arcads 落网页逆向路线，符合技能适用范围 |
| 站点归属 | 15:08 Bramble 移交他人；15:29 曾改领 PostPlus；后经用户拍板**本 Agent 继续 Arcads** | ✅ 见 `AGENTS.md` §8.3 |

---

## 二、公开面取证（第 0–5 步）

| # | 步骤 | 命令 | 产物 | 实测结果 | 判定 |
|---|---|---|---|---|---|
| 0 | 环境自检 | `python3 $CAP guide --root $ROOT` | `evidence/runtime-probe.json` | `ego-browser=OK` | ✅ |
| 1 | init | `python3 $CAP init --base $BASE --name reverse --target https://www.arcads.ai/ --routes … --hosts "arcads.ai app.arcads.ai"` | `capture-cfg.json`、`tools/run-capture-reverse.mjs` | 4 路由（home/login/privacy/terms） | ✅ |
| 2 | login 探测 | `python3 $CAP login --root $ROOT --sites "arcads=https://app.arcads.ai/onboarding"` | `evidence/login-probe.json` | **`NEED_LOGIN`**（两次）。ego-browser 是独立 Chromium 会话，拿不到用户普通浏览器的登录态 | ⚠️ 见 I-01，按红线停下未伪造 |
| 3 | 公开面抓包 | `python3 $CAP capture --root $ROOT` | `capture/` | 4 路由 `err=null`，SSR 原文 + DOM + 网络事件齐全 | ✅ |
| 4 | 静态收敛 | `python3 $CAP fetch --root $ROOT --rounds 3 --workers 24` | `mirror/` | **334 资源 / 146,897,948 B（≈140 MiB）**；92 JS / 6 CSS / 9 HTML | ✅ |
| 4.5 | 嵌套媒体解包 | `python3 $CAP unwrap-media --root $ROOT --workers 12 --timeout …` | — | **argparse 报错** `unrecognized arguments: --workers` | ❌ 见 I-06，当轮跳过 |
| 5 | finalize | `python3 $CAP finalize --root $ROOT --name Arcads` | `analysis/verification.json` 等 | `assets=334 disk=449 bytes=146897948`；`hash_mismatches=0`、`query_collisions=0` | ✅ |
| 5.5 | 分类视图 | `python3 $CAP bundle --root $ROOT` | `bundle/` | 449 文件 / 178,660,068 B（html 59 / js 92 / img 189 / media 27 / json 12 / css 6 / font 7 / other 57） | ⚠️ 见 I-08（safe-delete 确认） |
| 6 | 接口文档（公开面） | `python3 $CAP api-docs --root $ROOT --name Arcads` | `docs/接口文档.md`、`docs/api-spec.json` | **33 端点 / 13 有响应 / 29 families** | ✅ |

---

## 三、静态逆向（REA，逐文件）

| # | 步骤 | 命令 | 产物 | 实测结果 | 判定 |
|---|---|---|---|---|---|
| 7 | 构建 REA 输入（首轮） | `build_rea_input.py`（由 `rea` 子命令驱动） | `rea-input/` | **28 件**：24 业务 JS chunk + 2 CSS + 2 SSR HTML | ✅ |
| 8 | REA 逐文件分析（首轮） | `python3 $CAP rea --root $ROOT --perfile` | `analysis/rea-evidence/`、`rea-perfile.json`、`REA-cli-output/` | 分析 24 个 JS：**17 成功 / 7 失败**；耗时 761.7 s；证据包 **78,489,913 B（≈74.9 MiB）** | ⚠️ 失败项见 I-02 |
| 8b | 构建 REA 输入（补全轮） | `build_rea_input.py --limit 48 --max-kb 1200 --min-hits 2` + 手工补入 4 个漏选包 | `rea-input/` | **35 件**：34 业务 JS chunk + 1 CSS；**7 个首轮失败包全部纳入** | ✅ |
| 8c | REA 逐文件分析（补全轮） | `run_rea_perfile.py --budget-s 900 --heap-mb 4096 --max-files 40 --include .js` | `analysis/rea-evidence/`、`rea-perfile.json`、`REA-cli-output/` | **33 成功（27 ok + 6 cached）/ 1 失败**；耗时 1754.6 s；证据包 **227,284,044 B（≈216.8 MiB）** | ✅ 见 I-02（首轮 7 个失败中 6 个转成功） |
| 9 | 技术栈画像（补全轮证据包命中） | — | `analysis/rea-evidence.json` | `stripe` 28322、`webpack` 5846、`SSE` 2177、`next` 902、`WebSocket` 110、`react` 58、`turbopack` 48、`redux` 9 → **纯网页 SaaS，无原生桌面端** | ✅ 与桌面端优先复盘一致 |
| 10 | 补齐 rea 门禁两件 | 按 `check_evidence.py` 契约生成 | `analysis/REA-cli-output.md`、`analysis/rea-summary.json` | `input_files=35`（与 `rea-input/` 实数一致）；`files_ok=33 / files_failed=1` | ✅ |
| 11 | 证据门禁 | `python3 check_evidence.py --root $ROOT --stage all --strict` | `evidence/evidence-gate.json` | 首轮 **16/17**，唯一 FAIL 为 `download_errors_classified`（63 条 404 未分类）→ 补 `notes` 后 **17/17 PASS** | ✅ 见 I-03 |

---

## 四、鉴权态扩展（用户在 ego-browser 内登录后）

用户于 **ego-browser 窗口内**完成 Arcads 登录（不是普通浏览器），因此会话被 CDP 复用。

| # | 步骤 | 命令 | 产物 | 实测结果 | 判定 |
|---|---|---|---|---|---|
| 12 | 登录态复探 | `python3 $CAP login --root $ROOT --sites "arcads=https://app.arcads.ai/onboarding"` | `evidence/login-probe.json` | **`LOGGED_IN_OR_PUBLIC`**，落点 `app.arcads.ai/onboarding/attribution` | ✅ 会话打通 |
| 13 | 路由扩展（鉴权面） | 改写 `capture-cfg.json`（19 路由）+ `init --regen` | `tools/run-capture-reverse.mjs` | 覆盖 `dashboard` / `dashboard/settings/{billing,mcp,public-api,integrations,members,account,general}` / `onboarding/*` / `flow/library` / `admin/video-templates` | ✅ |
| 14 | 鉴权抓包 | `python3 $CAP capture --root $ROOT --timeout 2400` | `capture/` | **828 请求 / 796 响应 / 611 文本记录**；`application/json` 198 条、`text/javascript` 200 条 | ✅ |
| 15 | 鉴权有效性核验 | 解析 `capture/page-*.html` | — | dashboard/settings/onboarding/flow-library/admin 页面 **50–189 KB 真实内容，无 sign-in/log-in 关键字**，非登录重定向 | ✅ 真鉴权内容 |
| 16 | 静态再收敛 | `python3 $CAP fetch --root $ROOT --rounds 3 --workers 24` | `mirror/` | **680 资源 / 225,570,648 B（≈215 MiB）** | ✅ |
| 17 | 接口文档重生成 | `python3 $CAP api-docs --root $ROOT --name Arcads` | `docs/接口文档.md` | **33 → 92 端点**（33 有响应 / 58 families） | ✅ |

**从抓包实证的业务 API 面（去噪）：** `/api/auth/session` · `/auth/renew-token` · `/users/me` · `/workspaces` · `/workspaces/api-credentials` · `/payment/free-trial` · `/pricing/catalog` · `/credit-codes/{me,creator}` · `/integrations/catalog` + 8×`connection-status`（Slack/Dropbox/GDrive/Meta-Ads/Notion/X/TikTok/TikTok-Ads） · `/media/cloudfront-cookies` · `/onboarding/{intent,attribution,payment,paywall}` · `/offers/arcads10`。

---

## 五、全量抓取 + 全量文件 + 后端接口契约

| # | 步骤 | 命令 | 产物 | 实测结果 | 判定 |
|---|---|---|---|---|---|
| 18 | 全量路由挖掘 | 从 `mirror/` 的 JS/HTML 正则抽取路由 | — | 185 条候选 → 剔除资源/纯 API/外部端点后保留 **132 条真实页面**（公开营销 + 鉴权 App + 完整 `/admin/*` 后台），**132 条命名全部唯一** | ✅ |
| 19 | runner 重生成 | `python3 $CAP init --base $BASE --name reverse --regen` | `tools/run-capture-reverse.mjs` | 132 路由全部内联 | ✅ |
| 20 | **全量抓包** | `python3 $CAP capture --root $ROOT --timeout 5400` | `capture/` | **31 分 42 秒；3317 请求 / 3134 响应 / 2514 文本记录 / 985 条 JSON 响应**；`/admin/*` 全部 `err=null`，无登录跳转 | ✅ |
| 21 | **全量文件收敛** | `python3 $CAP fetch --root $ROOT --rounds 5 --workers 24` | `mirror/` | **1986 资源 / 291,342,811 B（≈278 MiB）**；742 JS / 230 HTML / 159 GIF / 90 WEBP / 52 MP4 / 24 WEBM + 字体/JSON | ✅ |
| 22 | finalize | `python3 $CAP finalize --root $ROOT --name Arcads` | `analysis/verification.json` | `assets=1986 disk=3479 bytes=291342811`；`download_errors=317` | ✅ |
| 23 | **后端接口契约** | `python3 $CAP api-docs --root $ROOT --name Arcads` | `docs/接口文档.md`、`api-spec.json` | **92 → 188 端点 / 127 families**（含 **60 个 `/admin/*`**：pricing/catalogs、credit-codes/batches、voices、actors、video-templates、workflows、situations、moderation、featured-models… + 48 个内部业务端点） | ✅ |
| 24 | 结构化契约 | `finalize` 内部 `extract_contracts` | `analysis/api-contracts.json` | 首次被写成 **0 条**（hosts 切分 bug）→ 修复后 **46 条**（46 有 method+path，3 条带请求体示例） | ✅ 见 I-05 |
| 25 | 媒体镜像 | `python3 $CAP media --root $ROOT --workers 16` | `mirror/`、`analysis/media-mirror.json` | 目标 **519 项**：落盘 0（均已在 mirror）/ 缓存 417 / 失败 **102** → 分类 `http_400_presigned_expired` 90（`argoseyes.s3-accelerate.amazonaws.com` 预签名过期）、`http_403` 9（Webflow CDN 8 + Vimeo 1）、`tls` 3（`t.arcads.ai`） | ✅ 见 I-07 |
| 26 | 嵌套媒体解包 | `python3 $CAP unwrap-media --root $ROOT --workers 12 --timeout 25` | — | 扫描 **1369 个 HTML**，解包 **280 处**代理 URL，得 **103 个内层媒体**，全部缓存命中、**0 失败** | ✅ 见 I-06（修复后首次跑通） |
| 27 | 复刻骨架交接 | `python3 $CAP handoff --root $ROOT --name Arcads --scaffold` | `rebuild/`（111 文件）、`analysis/REA-逆向分析报告.md` | `BACKEND families=51 endpoints=188 fixtures=35`；`FRONTEND pages=6`；`handoff: PASS` | ✅ 见 I-09（补脚本后可用） |
| 28 | 索引 | `python3 $CAP index --root $ROOT --base $BASE --title "Arcads 逆向"` | `arcads/INDEX.md` | `projects=1` | ✅ |
| 29 | **最终准出** | `python3 $CAP gate --root $ROOT --strict` | `evidence/evidence-gate.json`、`evidence/handoff.json` | `evidence gate: PASS (17/17)`；`handoff: PASS`；`sync_issue_docs: ok (24/24 in sync)` | ✅ **全部通过** |

---

## 六、产物清单（全部落盘，可复核）

| 产物 | 路径 | 规模 |
|---|---|---|
| 抓包原始件 | `capture/` | 3317 请求 / 3134 响应 / 2514 文本；`page-*.html` 137 份（含前几轮增量） |
| 全量静态资源 | `mirror/` | 1986 资源 / 291,342,811 B |
| 资源清单 | `manifest.json`、`checksums.sha256` | URL→本地路径 + sha256 |
| 接口契约（人读） | `docs/接口文档.md` | 188 端点 / 127 families |
| 接口契约（机读） | `docs/api-spec.json`、`analysis/api-contracts.json` | 188 端点；46 条 XHR/Fetch 契约（3 带请求体） |
| 媒体清单 | `analysis/media-mirror.json` | 519 目标，失败 102 已分类 |
| 静态逆向证据 | `analysis/rea-evidence/`（**44 份**：33 份覆盖本轮 34 件输入 + 11 份首轮输入集遗留）、`REA-cli-output/`（34 份日志）、`rea-evidence.json` | 本轮汇总 **227,284,044 B（≈216.8 MiB）**；目录实占 269 MiB |
| 逆向报告 | `analysis/Arcads-逆向报告.md`、`analysis/REA-逆向分析报告.md`、`analysis/REA-摘要.md` | — |
| 分类视图 | `bundle/` | 449 文件 / 178,660,068 B |
| 复刻骨架 | `rebuild/`（`backend/` + `frontend/`） | 111 文件 |
| 准出证据 | `evidence/{evidence-gate,handoff,login-probe,runtime-probe}.json` | — |

---

## 七、口径与未取证（诚实边界）

1. **188 vs 46 的口径差异**：`接口文档.md` 的 188 是「全部网络请求」，含 **134 条 Document（SSR 页面路由）**；`api-contracts.json` 的 46 才是程序化 **XHR/Fetch** 契约（495 Fetch + 1 XHR + 10 Other 去重）。两者不可混用。
2. **请求体只有 3 条**：本轮为**被动导航抓取**（只 goto，不点击/不填表/不提交），未触发写接口。要补全 POST/PUT 请求体需做**交互式抓包**——属 `unknown`，未虚构。**2026-11-12 21:0x 补验**：见 §八，在「只读交互」授权下仍无法扩开，诚实结论不变。
3. **REA 失败面已从 7 收敛到 1**：补全轮把首轮 7 个失败包中的 6 个转成功（5 个「worker 存储失败」大包 + `36uc_rrtepudd.js` 833.9 s 拿下）；仅剩 `2ixnvjih1wvzt.js`（531 KB）在 **900 s** 单文件预算下仍未收敛（该工具对超长行/minified 病态结构的解析瓶颈），对应结构仍标 `unknown`，未做任何推断。
4. **102 个媒体失败**：90 为 S3 预签名过期（400）、9 为外部 CDN 403、3 为 TLS，全部属**外部/时效性资源**，非抓取缺口；分类已落 `media-mirror.json`。
5. **`capture/` 与 `mirror/` 只读**：`unwrap-media` 全程未开 `--rewrite`（V-43），`page-*.html` 未被改写，仅做「发现 + 计数」。
6. **登录态归属**：登录发生在 `ego-browser` 独立会话内，凭据不在本工程任何文件中；`capture/` 中不含账号密码，`sanitization-report.json` 已脱敏。

---

## 八、增量取证：relay 端点定性 + 受控只读交互（2026-11-12 21:0x）

> 用户授权：选项 1（补 `/api/relay/e`）+ 选项 3（受控只读交互补请求体契约）。
> **红线**：只做只读类交互（切 tab / 展开 / 选项 / 轮播），不新建、不删除、不改名业务对象，不发消息、不点生成、不购买、不改账号设置，**不修改任何隐私/同意设置**。
> **工程约束**：原 `run-capture-reverse.mjs` 每次运行都会覆盖 `capture/network-*.json`（132 路由全量证据），故本轮全部走独立目录 `capture-interactive/`。

| # | 步骤 | 命令 | 产物 | 实测结果 | 判定 |
|---|---|---|---|---|---|
| 30 | 登录态复探 | `python3 $CAP login --root $ROOT --sites "arcads=https://app.arcads.ai/dashboard"` | `evidence/login-probe.json` | `LOGGED_IN_OR_PUBLIC`，落点 `app.arcads.ai/onboarding/attribution` | ✅ 会话有效，免重登 |
| 31 | relay 端点静态定性 | 解析 `mirror/app.arcads.ai/_next/static/chunks/36uc_rrtepudd.js` | — | `serverUrl:"/api/relay/e"`、`defaultTracking:{sessions:!0}`、`sessionReplayPlugin({sampleRate:.045})`；`hasToLog(){return!0}` **恒真**；`visibilityState==='hidden'` → `setTransport("beacon")+flush()` | ✅ **更正旧口径**：Amplitude HTTP 事件上报中继，非 SSE/流式长连接、非 A/B 门控 |
| 32 | 独立增量 runner | 新建 `tools/run-capture-interactive.mjs` | — | 独立输出 `capture-interactive/`；**不做 type 过滤**（原 runner 白名单漏 `Ping`/beacon）；点击前动态枚举控件并按危险词黑名单过滤 | ✅ |
| 33 | **增量抓包** | `ego-browser nodejs < tools/run-capture-interactive.mjs` | `capture-interactive/` | 5 页（onboarding attribution/intent/paywall、flow/library、公开首页）/ **21 次受控只读点击** / 每页 `visibilitychange(hidden)+pagehide` flush 钩子 + 9 s settle → **7995 events / 997 requests / 940 responses / 128 带 postData** | ✅ 全量证据零改动 |
| 34 | relay 命中检查 | 正则统计 `/api/relay/e` | `capture-interactive/summary.json` | **0 命中** | ⚠️ `unknown`，不伪造 |
| 35 | 隐私态只读诊断 | `ego-browser nodejs < tools/run-privacy-probe.mjs` | `capture-interactive/privacy-state.json` | `didomi_token_cpra`、Amplitude 双实例（`44e5a6f315` / `b2e63b5453`）、`AMP_unsent=[]`、DNT/GPC 均为 null | ✅ |
| 36 | 根因坐实 | 比对 opt-out 请求与响应体 | `capture-interactive/response-bodies.json` | 4 次 `POST https://api.arcads.ai/tracking/browser-opt-out {"browserOptOut":true}` → `201 {"success":true}`；Amplitude 仅拉 `cdn.amplitude.com` script、`sr-client-cfg` config、session-replay 起点，**零事件上报端点** | ✅ 追踪被 opt-out |
| 37 | 增量结构化 | `python3 tools/build_interactive_delta.py` | `analysis/{relay-e-finding,third-party-contracts,interactive-main-contracts}.json`、`docs/增量取证说明.md` | 外链契约 **13 条 / 274 次命中**（含 `sample_body` + 最多 3 条 `body_variants`）；主域增量契约 **2 条**；relay 定 `unknown` | ✅ |
| 38 | **skill 源码修复** | 改 `ego-site-capture/scripts/finalize_project.py::extract_contracts`；`python3 $CAP finalize --root $ROOT --preserve-notes --strict` | `analysis/api-contracts.json` | 纳入 `Ping` 类型 + 自动合并 `capture-interactive/requests.json` + `body_variants`；契约 **46 → 47**，3 条契约带多份 body 变体；`verification.json.notes` 保留；`capture/` 仍为 **132 路由 / 3317 请求** | ✅ capture 12/12 |
| 39 | **准出复验** | `check_evidence.py --stage all --strict` + `python3 $CAP gate --root $ROOT --strict` | `evidence/evidence-gate.json`、`evidence/handoff.json` | **17/17 PASS** + `handoff: PASS` + `sync_issue_docs 24/24 ok` | ✅ 三项全绿 |

### 8.1 本轮新增产物

| 产物 | 路径 | 规模 / 内容 |
|---|---|---|
| 增量抓包原件 | `capture-interactive/` | `network-events.json`（7995）、`requests.json`（997）、`responses.json`（940）、`response-bodies.json`、`loading.json`、逐页 `page-*.json`、`bodies/`、`summary.json`、`privacy-state.json` |
| 增量 runner | `tools/run-capture-interactive.mjs`、`tools/run-privacy-probe.mjs`、`tools/build_interactive_delta.py` | 可复跑；独立输出，不覆盖全量证据 |
| relay 定性 | `analysis/relay-e-finding.json` | 静态证据摘录 + 两轮抓包统计 + opt-out 证据链 + 解除条件 |
| 外链请求体契约 | `analysis/third-party-contracts.json` | 13 条 / 274 命中（独立口径，**不冒充 Arcads 后端契约**） |
| 主域增量契约 | `analysis/interactive-main-contracts.json` | 2 条 |
| 人读汇总 | `docs/增量取证说明.md` | 口径更正 + 诚实结论 + 文件地图 |

### 8.2 口径与未取证（本轮新增）

1. **`TASKS.md` 旧记「relay/e 是流式通道、需长连接抓包」有误** —— 静态代码实证为 Amplitude `analytics-browser 2.42.4` 的普通 HTTP POST 中继，`hasToLog(){return!0}` 恒真，不是 A/B 门控。已更正。
2. **`/api/relay/e` 判 `unknown`**：静态存在、动态不可达。根因是会话处于浏览器追踪 opt-out，而非抓包时长或路由覆盖不足。132 路由全量 + 5 页交互 + flush 钩子共 4314 请求均 0 命中。
3. **`sample_body` 仍为 3 条，本轮无法扩开**：21 次受控只读点击未触发任何业务写请求；主域带 body 的增量请求仅 `tracking/browser-opt-out` 与 `lj.arcads.ai/api/v1/check/*`（均与存量同类）。要补写接口请求体，必须授权真实写操作（创建 / 提交 / 生成），或提供现成 HAR / 后端日志。**不把第三方像素塞进主域契约凑数**。
4. **隐私边界**：解除 opt-out 等于改变用户的隐私同意选择（Didomi CPRA），超出「只看不动手」红线。本轮**未修改**任何 cookie / localStorage / 同意设置 / 账号设置；解除条件写在 `relay-e-finding.json`。
5. **交互副作用核查**：归因选项、轮播、tab 点击后主域未出现任何新增写请求（仅站点自发的 opt-out 上报），未改账号数据，符合红线。

---

## 九、paywall 后页面静态代码与接口契约（2026-11-12 22:0x，F12）

触发：用户截图 `app.arcads.ai/onboarding/paywall` 信用卡试用页，问「能否直接获取到后面的页面的 js 等信息」。结论 **能，无需付费 / 无需绕过鉴权 / 无需交互**；全程只做公开静态 GET 与本地静态解析。

| # | 动作 | 命令 / 依据 | 产物 | 实测结果 | 判定 |
|---|---|---|---|---|---|
| 40 | 复核路由落地 | `capture/routes-summary.json` | — | 132 路由中 dashboard / flow / 多数 admin 的最终 URL 被重定向到 `onboarding/attribution` 或 `onboarding/paywall`，截图印证 | ✅ 澄清此前「dashboard/admin 无登录跳转」的误读 |
| 41 | 静态资源可达性验证 | 普通 `curl` 公开 GET（**不带登录态**） | — | 真实 chunk `1dnwnqmacsgde.js` / `0-o851mvv5qyx.js` / `0cz1d0mv5g_q7.js` 均 `200 text/javascript`；伪造名 `definitely-not-real-000000.js` → `403 AccessDenied` | ✅ paywall 只挡渲染，不挡 `/_next/static/` |
| 42 | HTML chunk 引用差集 | 137 份 `capture/page-*.html` 正则提取 `_next/static/*.js` | `analysis/paywall-behind-static.json` | 并集 **288**（全在镜像）；以 onboarding 两页为基线，dashboard 专属 **51**、flow **49**、settings-billing **41**、public-api **38**、settings **37**、admin **2**；业务词 `video/generate/credits/actor/voice/workspace/stripe/paywall` 高命中 | ✅ **后面页面的业务 JS 早已落盘**，此前未识别 |
| 43 | 补懒加载 chunk | `python3 tools/fetch_lazy_chunks.py`（BFS 两轮收敛） | `analysis/lazy-chunks.json`、`mirror/.../chunks/` | 从已有 JS 的 `static/chunks/*.js` 依赖发现 **94 个未下载 chunk**，全部 `200`、**2.50 MiB / 0 失败**；chunk **288 → 382**；核对 12 条 CSS；1 个裸 token 判非 chunk | ✅ 定性为 Turbopack 懒加载 vendor 库（hls.js / PostCSS 等），**不冒充页面业务代码** |
| 44 | 声明式端点发现 | 读 `0s29-njx_rxds.js` 等 | — | 站点用 `makeEndpoint({newBackend, url, method, queryParamsSchema, requestSchema, responseSchema})` + zod 定义接口；后端 base `https://api.arcads.ai`（旧网关为 `u5wouxsctc.execute-api.eu-west-3.amazonaws.com`） | ✅ 找到无需交互即可补契约的路径 |
| 45 | 静态契约还原 | `python3 tools/extract_static_endpoints.py`（平衡花括号解析 382 个 chunk） | `analysis/static-endpoint-contracts.json`、`docs/静态接口契约清单.md` | **1167 处声明 / 1123 解析 / 525 条去重契约**；**160 条带 zod 请求体字段**、465 条带导出端点名、22 条路径前缀变量标 `?`、44 条 URL 运行时拼接如实记未解析；POST 207 / GET 192 / PUT 60 / DELETE 54 / PATCH 12 | ✅ 补上此前 `sample_body=3` 无法覆盖的写接口**形状** |
| 46 | 文档纠错与口径澄清 | 改 `docs/接口文档.md` 鉴权段；写 `docs/paywall后页面静态代码说明.md` | 同左 | 原鉴权段 `sessionid` / `msToken` / `a_bogus` / `{ret,errmsg,log_id,data}` 系他站模板串味，改为 `Bearer <token>` + `/auth/renew-token` 等静态实证；明确 188 抓包端点 / 47 抓包契约 / 525 静态契约三种口径互不冒充 | ✅ |
| 47 | 准出复验 | `check_evidence --stage all --strict` + `gate --strict` | `evidence/evidence-gate.json` | **17/17 PASS** + `handoff PASS` + `sync_issue_docs 24/24 ok` | ✅ |
| 48 | **公开 RSC 探针（补充实证）** | `python3 tools/probe_public_rsc.py`（98 个 app 路由，`<url>?_rsc=probe` + `RSC:1`，**无 cookie / 无登录态**） | `capture-public/rsc-*.txt`（98 份 / 1.62 MB）、`analysis/public-rsc-probe.json` | 不带登录态 `GET /dashboard` 已返回 **200 / 44 KB 壳页**；`RSC:1` 返回 **200 `text/x-component` / 28,569 B flight**，含 `(shell) → dashboard → __PAGE__` 段树；**74/98 flight 200**（24 个 404 为配置中本身不存在的路由）；段覆盖 `admin` 44 / `dashboard` 15 / `onboarding` 10 / `settings` 8 / `flow` 4；11 个 CSS 引用全部已在镜像；逐文件检查无 email/token/session 串 | ✅ 后面页面的服务端组件树亦可公开取 |
| 49 | 最终准出复验 | 同 47 | `evidence/evidence-gate.json` | RSC 探针与文档更新后仍 **17/17 + handoff PASS + 24/24** | ✅ |

### 9.1 本轮新增产物

| 产物 | 内容 |
|---|---|
| `tools/fetch_lazy_chunks.py` | 公开 GET + BFS 依赖收敛，逐文件 URL / 状态 / SHA-256 清单 |
| `tools/extract_static_endpoints.py` | 平衡括号解析 `makeEndpoint`，还原契约 + 路由域差集 + 生成人读清单 |
| `analysis/lazy-chunks.json` | 94 个新增 chunk / CSS / 失败与非 chunk 记录 |
| `analysis/paywall-behind-static.json` | 四层证据、路由域专属 chunk、业务词覆盖、边界 |
| `analysis/public-rsc-probe.json` | 98 路由公开 RSC 探针逐条状态 / SHA-256 / 段树 / CSS 引用 |
| `capture-public/rsc-*.txt` | 74 份有效 flight 原件 + 24 份 404 留痕，1.62 MB |
| `tools/probe_public_rsc.py` | 公开 RSC 探针（无登录态），可复跑 |
| `analysis/static-endpoint-contracts.json` | 525 条静态契约（method / path / backend / zod 字段 / 导出名 / 来源 chunk） |
| `docs/静态接口契约清单.md` | 525 条按路径首段分组，781 行 |
| `docs/paywall后页面静态代码说明.md` | 人读结论 + 复现命令 + 产物索引 |

### 9.2 口径与边界（本轮新增）

1. **静态 `requestFields` ≠ 真实请求体**：来自 zod `requestSchema` 顶层字段，是代码声明形状；`analysis/api-contracts.json` 的 `sample_body` 仍是 3 条，未变。
2. **525 静态契约 vs 188 抓包端点 vs 47 抓包契约**：口径不同，464 条静态 path 未出现在抓包 spec 中是被动导航未触发，不是抓包遗漏。
3. **运行时数据仍 `unknown`**：SSR 壳页与 RSC flight 可公开取（步骤 48），但无订阅态下不含用户项目/视频/积分真实数据，hydration 后仍跳 onboarding；静态代码也不含这些数据。
4. **未做**：未跑新 chunk 的 REA per-file（历史单文件 900 s 超时）、未改隐私设置、未填支付信息、未调用任何写接口、未使用 ego-browser 登录态下载。
5. **`/api/relay/e`** 状态不变（§八，opt-out 阻塞）。

