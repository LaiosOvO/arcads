# Arcads 逆向 · 问题清单（issue.md）

> 每条按「症状 → 根因 → 处置 → 影响 → 状态 → 证据」写清。分类：**P = 流水线/工具缺陷**、**B = 业务发现**、**E = 环境阻塞**、**U = 诚实缺口（unknown）**。
> 关联：[trace.md](./trace.md) · [../../AGENTS.md](../../AGENTS.md)

**状态图例**：✅ 已处置 / 🔧 已修上游 skill / ⏳ 未处置（如实标注）

---

## P 类：流水线与工具缺陷

### I-01 · 登录态跨会话不共享，`login` 持续报 `NEED_LOGIN`
- **症状**：用户在**普通浏览器**已登录 Arcads（截图 `app.arcads.ai/onboarding`，账号 1691517500qq@gmail.com），但 `capture_ctl.py login` 两次均输出 `arcads: NEED_LOGIN`，按红线被迫停在公开面。
- **根因**：`ego-browser` 是**独立 Chromium 会话 + 独立 profile**，不继承用户普通浏览器的 Cookie/IndexedDB。`probe_login.mjs` 在 ego 会话内探测，自然拿不到登录态——这是**设计使然**，不是探测逻辑错误（与本轮 Bramble 的「营销页 Log in 文案误报」是两码事）。
- **处置**：向用户说明鸿沟 → 用户改在 **ego-browser 窗口内**登录 → 复探得到 `LOGGED_IN_OR_PUBLIC`，落点 `app.arcads.ai/onboarding/attribution`。此后全部鉴权抓包复用该会话。
- **影响**：首次公开面取证因此只覆盖 4 条路由；后续补抓 132 路由时已带鉴权。
- **状态**：✅ 已处置（流程层面），非代码缺陷。
- **证据**：`evidence/login-probe.json`（前后两次内容不同）。

### I-02 · REA 逐文件分析首轮 7/24 失败 → 补全轮收敛到 2/34
- **症状**：首轮 `rea --perfile` 分析 24 个 JS chunk，**17 成功 / 7 失败**，证据包 74.9 MiB。
- **根因**：两类。① `2ixnvjih1wvzt.js`、`36uc_rrtepudd.js` 超出单文件 **240 s** 时间预算；② `frame-modern` / `main` / `oaiq.min` / `sdk` / `vendor-modern` 命中 **worker 存储失败**（REA 子进程写证据包异常）。日志尾部实证为清理阶段 `spawn EPERM`（读进程表被沙箱拦），失败信息以 `Provider cleanup could not be fully confirmed` 呈现，**容易被误读成预算不足**。
- **处置**：① 用新收敛的 `mirror/`（344 个 JS）重建输入，`build_rea_input.py --limit 48 --max-kb 1200 --min-hits 2` 得 31 件，再手工补入 4 个漏选包（关键词命中不足）→ **35 件（34 JS + 1 CSS）**；② `run_rea_perfile.py --budget-s 900 --heap-mb 4096 --max-files 40 --include .js` 重跑；③ 按门禁契约重生成 `rea-summary.json`（`input_files=35`）与 `REA-cli-output.md`。
- **结果**：**33 成功（27 ok + 6 cached）/ 1 失败**，证据包 **216.8 MiB**（74.9 → 216.8 MiB，覆盖 17/24 → 33/34）。首轮 7 个失败包中 **6 个转成功**（5 个存储失败大包 + `36uc_rrtepudd.js` 在 833.9 s 拿下）；仅剩 `2ixnvjih1wvzt.js` 在 900 s 预算下仍不收敛。
- **影响**：仅剩 1 个 chunk 的符号/依赖结构缺失，标 `unknown`；接口契约不受影响（以 `capture/` 流量为准）。
- **状态**：✅ 已收敛（7 → 1）；最后 1 个为 U 类，属工具侧解析瓶颈（240 s / 400 s / 900 s 三次同一模式超时），再提预算收益极低，不再追。
- **证据**：`analysis/rea-perfile.json`（34 条）、`analysis/REA-cli-output/*.log`、`analysis/REA-cli-output.md`、`analysis/rea-summary.json`、`evidence/evidence-gate.json`（PASS 17/17）。

### I-03 · `download_errors` 未分类 → 门禁反复 FAIL（63 → 317）
- **症状**：`check_evidence.py --stage all --strict` 长期卡在 **16/17**，唯一 FAIL 是 `download_errors_classified`；分类后一旦重跑 `finalize` 又变回 FAIL。
- **根因**：`finalize_project.py` 每次**整体重写** `verification.json`，把人工补的 `notes` 字段抹掉；而门禁要求「有 download_errors 就必须有分类说明」。
- **处置**：① 逐条解析 `manifest.json.errors`，确认全部为 **316×HTTP 404 + 1×HTTP 403**（315 条来自 `www.arcads.ai` 的陈旧哈希 chunk、1 条 `www.societe.com`、1 条 Webflow CDN 403）；② 写入结构化 `notes` 说明其「非工作包必需的陈旧/外部引用」性质；③ 用 `finalize --preserve-notes` 保证后续重跑不丢。
- **影响**：门禁恢复 17/17 稳定通过。
- **状态**：🔧 已修上游（`--preserve-notes`，见 I-04）。
- **证据**：`analysis/verification.json` 的 `notes` 字段、`manifest.json` 的 `errors[]`。

### I-04 · `finalize` 重跑抹掉手工分类（`notes`）
- **症状**：每次 `finalize` 后 `verification.json` 的 `notes` 消失，门禁立刻掉回 11/12 或 16/17。
- **根因**：`finalize_project.py` 无条件 `write_text` 覆盖整个 `verification.json`，没有保留人工字段的入口。
- **处置**：新增 `--preserve-notes`：重写前读旧文件，若存在 `notes` 则带到新结构里。实测重跑后 `notes preserved = True`。
- **影响**：消除了「跑一次流水线就要手工补一次 notes」的重复劳动。
- **状态**：🔧 已修（`ego-site-capture/scripts/finalize_project.py`）。
- **证据**：`finalize --preserve-notes` 执行后 `verification.json` 仍含 317 条分类说明。

### I-05 · `finalize` 把 `api-contracts.json` 写成 0 条（hosts 逗号切分 bug）
- **症状**：抓包有 3317 条请求、985 条 JSON 响应，但 `analysis/api-contracts.json` 每次都是 **0 条**；而 `api-docs` 能出 188 端点（因为它走另一套抽取）。
- **根因**：`finalize_project.py` 用 `a.hosts.split(",")` 按**逗号**切 host，但 `capture-cfg.json` 传的是**空格分隔**的 `"arcads.ai app.arcads.ai"` → 切成单个字符串 → host 匹配全部失败 → 契约集为空。
- **处置**：改为 `re.split(r"[,\s]+", a.hosts)` + `strip().lower()`，同时在 `fetch_project.py` / `new_project.py` 同步；commit `3bf8d6f` 已推送 origin。实测空格、逗号两种写法解析结果一致，Arcads 抓包直接产出 **46 条契约**。
- **影响**：`api-contracts.json` 从「永远 0」变成「finalize 自动产出」，不再需要手工回填。
- **状态**：🔧 已修上游并推送。
- **证据**：`analysis/api-contracts.json`（46 条）、`git log --oneline` 中 `fix(skills): split --hosts on comma or whitespace in capture scripts`。

### I-06 · `capture_ctl.py unwrap-media` 参数不匹配，子命令必然报错
- **症状**：`python3 $CAP unwrap-media --root $ROOT --workers 12 --timeout 900` 直接 `error: unrecognized arguments: --workers 12 --timeout 900`，unwrap-media 环节从未真正跑过。
- **根因**：封装层 `cmd_unwrap_media` 把 `--workers/--timeout` 透传给 `unwrap_nested_media.py`，但底层只声明了 `--root/--rewrite/--download`。**接口契约漂移**。
- **处置**：按治理约定「只改真源」，改 `rea-rebuild/scripts/unwrap_nested_media.py`：新增 `--workers`（默认 8）/ `--timeout`（默认 30）并**真正生效**（下载改为 `ThreadPoolExecutor` 并发、先剔除已缓存项），再 `sync_skill_scripts.py --apply` 同步到两个镜像。实测：扫描 1369 HTML、解包 280 处、103 个内层媒体全部命中缓存、0 失败。
- **影响**：该子命令首次可用；Bramble 工程当时只能绕过（其 issue.md I-03 记录的同一缺陷）。
- **状态**：🔧 已修上游 + 已同步 3 份。
- **证据**：`unwrap_nested_media.py --help` 输出含两个参数；`sync_skill_scripts.py --apply` → `inSync=90, drift=0`。

### I-07 · `mirror_media.py` 不落盘失败明细（102 项失败只存在 stdout）
- **症状**：`media` 报「成功 0 / 缓存 417 / **失败 102**」，但工程里没有任何文件记录这 102 个 URL 和失败原因，无法复核、无法分类。
- **根因**：`mirror_media.py` 只做 `print` 计数，没有 `json.dump`/`write_text`。
- **处置**：新增 `analysis/media-mirror.json` 报告（总量/成功/缓存/失败、`okBytes`、`failedByClass`、`failedByHost`、`failedItems` 前 500 条）+ `classify_failure()` 分类器（404 / 400 预签名过期 / 403 / timeout / dns / tls / conn / other）。
- **实测分类**：`http_400_presigned_expired` **90**（全部 `argoseyes.s3-accelerate.amazonaws.com`，S3 预签名过期）、`http_403` **9**（`cdn.prod.website-files.com` 8 + `player.vimeo.com` 1）、`tls` **3**（`t.arcads.ai`）。
- **影响**：102 项失败从「不可解释」变成「可复核且已定性为外部/时效资源」。
- **状态**：🔧 已修（`ego-site-capture/scripts/mirror_media.py`）。
- **证据**：`analysis/media-mirror.json`。

### I-08 · `bundle` 触发 safe-delete 确认而阻塞
- **症状**：首轮 `python3 $CAP bundle --root $ROOT` 停在 safe-delete 交互确认，未继续。
- **根因**：`build_bundle_view.py` 重建 `bundle/` 前会先清理旧目录，触发安全删除确认。
- **处置**：不在交互环境下强行放行；确认目标目录只含上次生成的分类视图后，改在受控环境重建。最终产物 449 文件 / 178,660,068 B。
- **影响**：仅延迟一步，未丢失证据（`bundle/` 是 `mirror/` 的分类视图，可随时重建）。
- **状态**：✅ 已处置。
- **证据**：`bundle/_index.json`（`files=449`、`counts` 分类型）。

### I-09 · `handoff --scaffold` 依赖的两个脚本未镜像进 ego-site-capture
- **症状**：`capture_ctl.py handoff --scaffold` 需要 `build_rebuild_report.py` 与 `build_rebuild_scaffold.py`，但 `ego-site-capture/scripts/` 里没有；`handoff --strict` 因此长期 `FAIL`（`rebuild` 段 WARN 被升级）。
- **根因**：`find_script()` 会回退到 6 个 skill 目录，所以在**三 skill 共存**的机器上侥幸能跑；但同步清单 `CAPTURE_MIRROR` 从未纳入这两个脚本 → **ego-site-capture 单独安装时该子命令必然抛「缺脚本」**。
- **处置**：把两个脚本加入 `sync_skill_scripts.py` 的 `CAPTURE_MIRROR`，跑 `--apply` 同步（`inSync 88 → 90`，`drift=0`）。实测 `handoff --scaffold` 产出 `REA-逆向分析报告.md`（endpoints=188 / rea_files=17 / gaps=1）与 `rebuild/`（BACKEND families=51 / endpoints=188 / fixtures=35；FRONTEND pages=6；111 文件），`handoff: PASS`。
- **影响**：`gate --strict` 从「evidence PASS + handoff FAIL」变成**三项全 PASS**。
- **状态**：🔧 已修上游 + 已同步。
- **证据**：`evidence/handoff.json`（`gate: PASS`）、`rebuild/`、`analysis/REA-逆向分析报告.md`。

### I-10 · `unwrap-media` 未开 `--rewrite` 却打印 `REWRITTEN`（口径误导）
- **症状**：输出大量 `[REWRITTEN] page-xxx.html: 2 proxy URLs`，但这些文件在 `capture/`，属只读证据，实际**没有**被改写。
- **根因**：打印逻辑用 `res["modified"]`（内容是否「会变」）判定标签，而落盘条件是 `rewrite and modified`；`cmd_unwrap_media` 按 V-43 只传 `--download`，故 `rewrite=False`。
- **处置**：标签改为 `REWRITTEN if (args.rewrite and modified) else FOUND`，并同步三份。
- **影响**：避免把「发现」谎报成「改写」，保护 `capture/` 只读口径。
- **状态**：🔧 已修上游 + 已同步。
- **证据**：重跑输出 `[FOUND]`；`capture/page-*.html` mtime 未变。

---

## E 类：环境阻塞

### I-11 · macOS BSD `grep` 不支持 `\|`，导致多模式检索静默返回空
- **症状**：`grep -n "urllib\|^import\|def " unwrap_nested_media.py` 返回空，让人误判「文件里没有 urllib」；实际文件明确使用了 `urllib.request`。
- **根因**：BSD grep 的 BRE 不认 `\|` 作为「或」，把它当字面量 → 匹配失败且**不报错**。
- **处置**：全流程改用 `grep -E` 或 `Grep` 工具做多分支匹配。
- **影响**：曾一度让「unwrap-media 失败原因」的初判跑偏（误以为是 urllib 未定义），后经实读源码纠正为 I-06 的参数漂移。
- **状态**：✅ 已规避。
- **证据**：本 issue 本身即教训记录。

---

## B 类：业务发现

### I-12 · Arcads 是纯网页 SaaS，无原生桌面端
- **证据**：REA 证据包命中 `next` 1663 / Turbopack / SSE 650 / WebSocket 17 / stripe 11 / credits-subscription / canvas 视频渲染，**无 Electron / Tauri / PyQt / Qt / Sparkle 痕迹**；应用面为 `app.arcads.ai` 的 SSR 路由。
- **结论**：不适用 `rea-desktop-reverse`（桌面端 SOP），落 `ego-site-capture` 网页取证路线——与用户「有桌面端的优先逆向桌面端」的规则一致（本站无桌面端，故选它不违反规则）。
- **状态**：✅ 已确认。

### I-13 · 后端为「工作区 + 积分 + 订阅 + 多集成」的多租户模型
- **证据**（均来自抓包，非推断）：`/workspaces`、`/workspaces/api-credentials`、`/payment/free-trial`、`/pricing/catalog`、`/credit-codes/{me,creator}`、`/integrations/catalog` + 8 个 `connection-status`、`/media/cloudfront-cookies`、`/offers/arcads10`、`/package/latest/{id}/`。
- **结论**：产品骨架 = AI 广告视频生成 SaaS + 租户/积分/订阅计费 + 8 类第三方集成 + 面向开发者的 API 凭证与 MCP 入口。
- **状态**：✅ 已确认（字段取值仍需真实请求或 UI 实测，不从命中直推）。

---

## U 类：诚实缺口

### I-14 · 写接口请求体缺失（只有 3 条示例）
- **症状**：46 条 XHR/Fetch 契约中仅 3 条带 `sample_body`。
- **根因**：本轮为**被动导航抓取**（逐路由 goto，不点击/不填表/不提交），从未触发 POST/PUT 的真实负载。
- **影响**：写接口的 body schema 属 `unknown`，不得据路径猜测。
- **状态**：⏳ **仍未补（2026-11-12 21:0x 已做受控交互验证）**。本轮在用户授权下做了 21 次只读点击（归因选项 / 轮播 / tab）+ 5 页增量抓包，主域**未产生任何新的业务写请求**，故 `sample_body` 仍为 3 条。结论：**只读交互在架构上无法扩开写接口请求体**；要补必须授权真实写操作（提交表单 / 创建项目 / 生成视频），或提供现成 HAR / 后端日志。本轮已把可拿到的外链请求体单独落成 `analysis/third-party-contracts.json`（13 条 / 274 命中，独立口径，不冒充业务后端契约）。
- **证据**：`analysis/api-contracts.json`（47 条 / `with_body=3` / 3 条含 `body_variants`）、`analysis/interactive-main-contracts.json`（2 条）、`capture-interactive/summary.json`。

### I-15 · 137 份 `page-*.html` 含多轮增量，非单轮 132 路
- **症状**：`capture/page-*.html` 计 137 份，多于本轮 132 条路由。
- **根因**：`capture` 为**增量写入**，前几轮（4 路由 + 19 路由）的页面文件仍在，与本轮 132 条合并成 137（部分路由重名文件被覆盖）。
- **影响**：不影响证据有效性；但「页面数」不等于「本轮路由数」，报告中已分别标注（`capturePages=137` / `routes=132`）。
- **状态**：✅ 已说明（口径澄清，非缺陷）。

### I-16 · `/api/relay/e` 静态存在、动态不可达（隐私 opt-out 阻塞）
- **症状**：`coverage-gaps.json` 记 `/api/relay/e` 为唯一「JS 中出现但抓包未捕获」的端点；`TASKS.md` 旧记「流式通道，需长连接抓包」。本轮 132 路由全量 + 5 页交互（合计 4314 请求）**均 0 命中**。
- **根因（三层实证）**：
  1. **静态**：`mirror/app.arcads.ai/_next/static/chunks/36uc_rrtepudd.js` 中 `serverUrl:"/api/relay/e"` 是 **Amplitude `analytics-browser 2.42.4` 事件上报中继**，普通 HTTP POST，默认 `fetch`、页面 hidden 时切 `beacon` + `flush()`；`hasToLog(){return!0}` **恒真**，不是 A/B 门控。→ 旧「流式长连接」口径错误。
  2. **环境**：会话有 `didomi_token_cpra` 同意 token；站点每页 `POST https://api.arcads.ai/tracking/browser-opt-out {"browserOptOut":true}` → `201 {"success":true}`（4 次）。Amplitude 只拉 `cdn.amplitude.com` script 与 `sr-client-cfg` config，**零事件上报端点**；`AMP_unsent=[]`。
  3. **行为**：本轮显式注入 `visibilitychange(hidden)` + `pagehide` 并 settle 9 s/页，仍无请求。
- **处置**：判 `unknown`，落 `analysis/relay-e-finding.json`（静态摘录 + 两轮抓包统计 + opt-out 证据链 + 解除条件）。**未修改任何 cookie / localStorage / 同意设置** —— 解除 opt-out 等于改变用户隐私选择，超出红线。
- **影响**：该端点响应体、请求体 schema 属 `unknown`，不得推断补全；`coverage-gaps` 的数字不变，避免污染自动生成产物。
- **状态**：⏳ **已定性、未取证**。解除条件：用户明确授权后，在未 opt-out 的新会话（或 Didomi 同意面板授予分析类同意）重跑 `tools/run-capture-interactive.mjs`；或提供 HAR / 后端日志。
- **证据**：`analysis/relay-e-finding.json`、`capture-interactive/{summary,privacy-state,response-bodies}.json`、`docs/增量取证说明.md`。

---

## P 类：流水线缺陷（本轮新修）

### I-17 · `extract_contracts` 漏 `Ping` 类型且不读增量抓包目录
- **症状**：`finalize` 产出的 `api-contracts.json` 每次都被重算为只看 `capture/network-requests.json`，且 `type` 白名单为 `(Fetch, XHR, Other, None)`。
- **根因**：`navigator.sendBeacon` 的请求类型是 **`Ping`**（正是 Amplitude/GTM 在 `visibilitychange` / `pagehide` 的上报方式），整类被过滤；另外「独立目录增量抓包」这种不覆盖全量证据的做法，其请求也无法进入契约。
- **处置**：改 `ego-site-capture/scripts/finalize_project.py::extract_contracts`（该文件为 ego-site-capture 独有，不在 `sync_skill_scripts.py` 镜像清单内）：
  1. type 白名单纳入 `Ping`；
  2. 自动合并 `root/capture-interactive/requests.json`（存在才读）；
  3. 每条契约保留最多 3 份去重 `body_variants`，不只留第一条 `sample_body`；
  4. 调用处把 `root` 传入。
  端到端验证：`finalize --preserve-notes --strict` → 契约 **46 → 47**、`body_variants` 3 条、`verification.json.notes` 保留、`capture 12/12 PASS`；`gate --strict` → **17/17 + handoff PASS + 24/24 ok**。
- **影响**：`capture/` 的 132 路由 / 3317 请求全量证据零改动；后续增量抓包可被 finalize 自动吸收。
- **状态**：🔧 已修上游（已提交推送）。
- **证据**：`analysis/api-contracts.json`、`evidence/evidence-gate.json`、`tools/capture-interactive.log`。

---

## Q 类：口径 / 覆盖误判（F12 发现并纠正）

### I-18 · 误以为「dashboard / admin 无登录跳转」，实际 132 路由大半被重定向到 onboarding
- **症状**：`capture/routes-summary.json` 里 `dashboard`、`flow`、`admin-*` 等路由 `title` 仍是 `Arcads`、响应数 100–250，早期据此判定这些后台页已成功访问。
- **根因**：逐行核对该文件的 `url` 字段，绝大多数实际落在 `https://app.arcads.ai/onboarding/attribution` 或 `/onboarding/paywall`；用户截图（信用卡 3 天试用页）印证是**无订阅态的渲染层门禁**，不是登录失效。
- **处置**：不改抓包原件，改口径。补证：以 onboarding 两页 HTML 的 chunk 引用为基线做差集，dashboard 有 **51 个专属业务 chunk**（2.50 MB）、flow 49 个（3.07 MB）早已落盘；静态资源本身由 CDN 公开返回（真实名 200 / 伪造名 403）。
- **影响**：**后面页面的 JS 其实已获取**，此前只是没识别；运行时 SSR 数据仍不可得，标 `unknown`，不得用静态代码冒充。
- **状态**：✅ 已纠正（`trace.md` §九、`docs/paywall后页面静态代码说明.md`）。
- **证据**：`capture/routes-summary.json`、`analysis/paywall-behind-static.json`、`analysis/lazy-chunks.json`。

### I-19 · `docs/接口文档.md` 鉴权段混入了其他站点的模板内容
- **症状**：文档写「Cookie `sessionid` + `GET /passport/web/account/info/`、`msToken`/`a_bogus`/`X-Bogus`/`device_id`/`aid` 签名、统一信封 `{ret,errmsg,log_id,data}`」，与 Arcads 实证完全不符。
- **根因**：自动生成文档时套用了跨站点模板，未做逐字段校验。
- **处置**：按本轮静态代码证据改正为 `Bearer <token>` + `/auth/{google-login,apple-login,renew-token,link-token}` + `https://api.arcads.ai`（旧网关 `u5wouxsctc.execute-api.eu-west-3.amazonaws.com`）+ CloudFront cookie / socket.io；同时在文档头挂上静态契约清单索引与三种口径说明。
- **影响**：端点表（188 条）与响应样本未动，门禁 `api_spec.endpoints > 0` 不受影响。
- **状态**：✅ 已修文档。
- **证据**：`docs/接口文档.md` 头部、`analysis/static-endpoint-contracts.json`。

### I-20 · 懒加载 chunk 从未下载；静态契约此前完全未覆盖
- **症状**：镜像 288 个 chunk，但已有 JS 内部引用了 94 个 `static/chunks/*.js` 未落盘；`api-contracts.json` 仅 47 条 / 3 条 `sample_body`，写接口契约几乎空白。
- **根因**：`capture` 只镜像「页面 HTML 引用 + 运行时请求」到的资源；Turbopack 懒加载 vendor chunk 与 `makeEndpoint` 声明式接口既不会出现在 HTML，也不会在被动导航里发请求。
- **处置**：① `tools/fetch_lazy_chunks.py` BFS 两轮收敛补齐 94 个（2.50 MiB / 0 失败，chunk 288 → 382）；② `tools/extract_static_endpoints.py` 从 1167 处 `makeEndpoint` 声明静态还原 **525 条契约 / 160 条 zod 请求体字段**，44 条运行时拼接 URL 与 22 条变量前缀路径如实标不可解析。
- **影响**：写接口**形状**已补齐，但真实 `sample_body` 仍为 3 条；新 chunk 未跑 REA per-file（历史 900 s 超时），标为待办不谎报覆盖。
- **状态**：✅ 静态部分已补；真实请求体 / REA 覆盖仍受外部条件阻塞。
- **证据**：`analysis/lazy-chunks.json`、`analysis/static-endpoint-contracts.json`、`docs/静态接口契约清单.md`。

### I-21 · 132 路由配置里有 24 个 app 路由并不存在（公开 RSC 探针实证）
- **症状**：对 `capture-cfg.json` 中 98 个 `app.arcads.ai` 路由做公开 `?_rsc=probe` 请求，**74 个返回 flight 200，24 个返回 404**（`text/x-component`，段树 `/_not-found`）。
- **根因**：这些是早期按命名规律推测加入的路由（如 `product`、`onboarding-payment`、`project`、`users-me`、若干 `admin-*`），站点并未实现；与 `analysis/verification.json` 里 316 个 HTTP 404 属同一现象。
- **处置**：不改抓包原件，在 `analysis/public-rsc-probe.json` 逐条记录状态码 / SHA-256 / 段树，24 份 404 响应体同样留痕；`docs/paywall后页面静态代码说明.md` 如实写 74/98，不把 404 伪装成已覆盖页面。
- **影响**：`132 路由` 是**探测过的 URL 数**，不等于有效页面数；后端契约覆盖以静态 525 条与抓包 188 端点为准，不受影响。
- **状态**：✅ 已说明（口径澄清，非缺陷）。
- **证据**：`analysis/public-rsc-probe.json`、`capture-public/rsc-*.txt`、`tools/probe_public_rsc.py`。

