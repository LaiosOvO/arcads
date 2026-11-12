# paywall 之后页面的 JS / 接口信息：能否直接获取

- 生成时间：2026-11-12 22:05（GMT+8）
- 触发：用户截图 `app.arcads.ai/onboarding/paywall` 信用卡试用页，问「能不能直接获取到后面的页面的 js 等信息」
- 结论：**能，而且不需要付费、不需要绕过鉴权、不需要交互**。本轮已把可静态获取的部分全部落盘。

---

## 一、结论与机制

`/onboarding/paywall` 是**渲染层门禁**：服务端在用户没有有效订阅时把 dashboard / flow / admin 等路由重定向到 onboarding。但 Arcads 用的是 Next.js + Turbopack，所有路由级 JS 都是**构建期生成的静态产物**，放在 `https://app.arcads.ai/_next/static/...` 下由 CDN 直接返回，不经过任何业务鉴权。

实测对照（普通公开 GET，不带任何会话）：

| 请求 | 结果 |
|---|---|
| `GET /_next/static/chunks/1dnwnqmacsgde.js` | `200`，92,004 B，`text/javascript` |
| `GET /_next/static/chunks/0-o851mvv5qyx.js` | `200`，22,390 B，`text/javascript` |
| `GET /_next/static/chunks/0cz1d0mv5g_q7.js` | `200`，112,594 B，`text/javascript` |
| `GET /_next/static/chunks/definitely-not-real-000000.js` | `403` XML `AccessDenied` |

伪造文件名返回 403，说明 200 是真实构建的 chunk，不是通配回退页。**未使用 ego-browser 登录态、未填任何支付信息、未修改任何 cookie / 隐私设置。**

---

## 二、四层证据

### 第 1 层：paywall 后页面的业务 JS 其实早就在镜像里

132 路由抓包时，多数 dashboard / admin 路由最终 URL 被重定向到 `onboarding/attribution` 或 `onboarding/paywall`（`capture/routes-summary.json` 可复核），此前据此判断「后面页面没抓到」。但**重定向前的 SSR HTML 已经把这些路由所需的 chunk preload 进 `<script>` / `<link rel=preload>`**。以 onboarding 两页的引用集合为基线做差集：

| 页面 HTML | `_next` JS 引用 | 相对 onboarding 的专属 chunk | 专属代码体积 |
|---|---:|---:|---:|
| `page-dashboard.html` | 121 | **51** | 2.50 MB |
| `page-flow.html` / `page-flow-use.html` | 119 | **49** | 3.07 MB |
| `page-dashboard-settings-billing.html` | 111 | 41 | 1.98 MB |
| `page-dashboard-settings-public-api.html` | 108 | 38 | 1.69 MB |
| `page-dashboard-settings.html` | 106 | 37 | 1.61 MB |
| `page-admin.html` | 56 | 2 | 34 KB |
| `page-onboarding-paywall.html` | 70 | 0（基线） | — |

这 51 个 dashboard 专属 chunk 的业务词命中：`video` / `generate` / `credits` / `actor` / `voice` / `workspace` / `folder` / `project` / `subscription` / `stripe` / `paywall` / `flow` / `upload` / `render` / `canvas` / `template` / `billing` —— 确认是业务页面代码，不是 vendor 库。全站 137 份 HTML 的 `_next` JS 引用并集为 **288**，全部已在镜像中。

### 第 2 层：补齐从未被 HTML 引用的懒加载 chunk

从已有 JS 里的 `static/chunks/*.js` 依赖引用做 BFS（两轮收敛），发现 **94 个从未下载过的 chunk**，全部公开 GET 成功，共 2.50 MiB，`0` 失败：

- `analysis/lazy-chunks.json`：逐个文件的 URL / 状态 / 字节 / SHA-256 / 引用轮次
- chunk 总数 **288 → 382**；另核对 12 条 CSS 引用
- 内容定性：这批是 Turbopack 懒加载的 **vendor 库**（hls.js 的 M3U8 解析、PostCSS / source-map 等），属于构建产物但不是页面业务代码 —— 如实标注，不冒充页面代码

### 第 3 层：从 JS 直接还原后端接口契约（本轮最大增量）

站点用声明式 `makeEndpoint({...})` 定义后端调用，形态为：

```js
(0,t.makeEndpoint)({
  newBackend:!0,
  url:()=>"/admin/featured-models",
  method:"POST",
  queryParamsSchema:z.void(),
  requestSchema:z.object({name:z.string()}),
  responseSchema:z.array(a)
})
```

因此**不必触发任何写操作**，即可从静态代码还原 method + path + zod 请求体字段。对 382 个 chunk 全量解析：

| 指标 | 值 |
|---|---:|
| `makeEndpoint` 声明 | 1,167 |
| 成功解析 | 1,123（44 条 URL 由运行时函数拼接，如实记为未解析） |
| 去重契约 | **525** |
| 带请求体字段（zod 顶层） | **160** |
| 带导出端点名 | 465 |
| 方法分布 | POST 207 / GET 192 / PUT 60 / DELETE 54 / PATCH 12 |
| 路径前缀为变量、基路径不可判定 | 22（标 `?`，不猜测） |

后端 base 也从代码坐实：`newBackend:!0` → `https://api.arcads.ai`；否则 → 旧网关 `https://u5wouxsctc.execute-api.eu-west-3.amazonaws.com`。另见 `/auth/{google-login,apple-login,renew-token,link-token}`、`/media/cloudfront-cookies`、`/agent/stream`（SSE）、`socket.io` WebSocket 连接。

### 第 4 层：公开 RSC flight 带出 paywall 后页面的路由段树

不带任何登录态的 `GET /dashboard` 返回 **200、44 KB 壳页**（不是 307）；加 `RSC: 1` 头请求 `<url>?_rsc=probe` 则返回 **200 `text/x-component`、28,569 B 的 RSC flight 数据**，其中明确含 `(shell) → dashboard → __PAGE__` 段树与 CSS chunk 引用。对配置里全部 **98 个 app 路由**做同一公开探针：

| 项 | 结果 |
|---|---:|
| 返回 flight 200 | **74 / 98** |
| 404 | 24（配置里本身不存在的路由，与 `verification.json` 的 404 面一致） |
| 段树覆盖 | `admin` 44、`dashboard` 15、`onboarding` 10、`settings` 8、`flow` 4、`actors` 5、`pricing` 5、`credit-codes` 3、`video-templates` 3、`voices` 3、`workflows` 3 |
| flight 引用 CSS | 11 个，**全部已在镜像**（0 需下载） |
| 落盘原件 | `capture-public/rsc-*.txt` 98 份 / 1.62 MB |

即「后面页面」的**服务端组件树与路由结构**也能公开取，且 flight 中无 email / token / session 串（已逐文件检查）。脚本 `tools/probe_public_rsc.py`，汇总 `analysis/public-rsc-probe.json`。

---

## 三、口径澄清（重要）

| 产物 | 口径 | 数量 |
|---|---|---:|
| `docs/api-spec.json` / `docs/接口文档.md` | **抓包实测**的 URL path，含 SSR 页面、第三方域、CDN 请求 | 188 端点 |
| `analysis/api-contracts.json` | 抓包实测的主域 XHR/Fetch 契约，含真实 `sample_body` | 47 契约 / 3 条 body |
| `analysis/static-endpoint-contracts.json`（本轮新增） | **代码静态声明**的业务 API，含 zod 请求体形状，未经实际调用 | 525 契约 / 160 条字段 |

三者不是同一口径，静态清单里 464 条 path 不出现在抓包 spec 中，**不代表抓包漏了 464 个请求** —— 是被动导航没触发这些接口。静态 `requestFields` 是代码声明的形状，**不等于抓包观测到的真实请求体**，也不代表接口已调用成功。两类证据分别存放、互不冒充。

---

## 四、仍然拿不到的部分

1. **运行时业务数据**：SSR 壳页与 RSC flight 可公开取（第 4 层），但在无订阅态下不含用户项目、视频、积分余额等真实数据，客户端 hydration 后仍会跳到 onboarding。静态代码不含这些数据。
2. **真实 POST/PUT 请求体样本**：`sample_body` 仍是 3 条；zod 声明只能给字段形状，给不出实际取值。要真实样本仍需授权写操作或提供 HAR / 后端日志。
3. **`/api/relay/e` 响应体**：上一轮已定性为追踪 opt-out 导致零上报，本轮未改隐私设置。
4. **REA 覆盖**：新补 94 个 chunk 与 51 个业务专属 chunk 尚未全部跑 `rea analyze-javascript-application --per-file`（单文件最长曾 900 s 超时），本轮只做静态字符串级取证，不谎报 REA 覆盖。

---

## 五、复现

```bash
cd /Users/admin/Desktop/data/fde/marketing/product/arcads/reverse

# 1) 递归补全懒加载 chunk + CSS（公开 GET，BFS 至引用图收敛）
python3 tools/fetch_lazy_chunks.py

# 3) 公开 RSC 探针（无登录态），落盘 98 份 flight 原件
python3 tools/probe_public_rsc.py

# 4) 重跑汇总（会吸收 lazy-chunks.json 与 public-rsc-probe.json）
python3 tools/extract_static_endpoints.py
```

## 六、产物索引

| 产物 | 内容 |
|---|---|
| `analysis/lazy-chunks.json` | 94 个新增 chunk 的 URL / 状态 / SHA-256 / 轮次；CSS 核对；失败与非 chunk 记录 |
| `analysis/paywall-behind-static.json` | 结论、四层证据、路由域专属 chunk 差集、业务词覆盖、边界 |
| `analysis/static-endpoint-contracts.json` | 525 条静态契约（method / path / backend / zod 字段 / 导出名 / 来源 chunk） |
| `docs/静态接口契约清单.md` | 525 条按路径首段分组的人读表（781 行） |
| `docs/paywall后页面静态代码说明.md` | 本文 |
| `mirror/app.arcads.ai/_next/static/chunks/` | 288 → 382 个 JS chunk |
| `analysis/public-rsc-probe.json`、`capture-public/rsc-*.txt` | 98 路由公开 RSC 探针汇总 + 74 份有效 flight 原件（另有 24 份 404 响应留痕） |
| `tools/fetch_lazy_chunks.py`、`tools/extract_static_endpoints.py`、`tools/probe_public_rsc.py` | 可复跑脚本 |
