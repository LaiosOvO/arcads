# Arcads REA 逆向分析报告（可实现版）

- 生成时间：2026-11-12 19:31:59 +0800
- 证据来源：抓包镜像 `mirror/`（1986 资源 / 277.8 MiB）＋ REA 证据包 `analysis/rea-evidence/`（44 个文件 / 268.8 MiB）
- 校验：清单 1986 / 磁盘 3479，sha256 不符 0，查询串碰撞 0
- 口径：**实证** = 抓包或代码证据直接支持；**推断** = 由两者交叉得出；**unknown** = 没有证据，不猜。

## 一、技术栈定性

| 信号 | 强度（命中次数） | 判据 |
|---|---|---|
| React | 116 | REA 证据包字符串命中 |
| Ant Design | 6 | REA 证据包字符串命中 |
| Redux | 18 | REA 证据包字符串命中 |
| webpack | 11692 | REA 证据包字符串命中 |
| Turbopack | 96 | REA 证据包字符串命中 |
| Next.js | 902 | REA 证据包字符串命中 |
| Stripe | 56644 | REA 证据包字符串命中 |
| WebSocket | 220 | REA 证据包字符串命中 |
| Sentry | 6 | REA 证据包字符串命中 |
| i18n | 12 | REA 证据包字符串命中 |
| three.js | 8 | REA 证据包字符串命中 |

静态侧（镜像内文件名与内容形态）作为交叉验证：

- bundle 分类：{'other': 57, 'html': 59, 'js': 92, 'img': 189, 'media': 27, 'json': 12, 'css': 6, 'font': 7}

## 二、接口面结构

抓包实证端点 **188** 个，分布在 127 个家族；其中 35 个有完整响应体。

| 家族 | 端点数 |
|---|---|
| `dashboard/settings` | 8 |
| `admin/pricing` | 7 |
| `admin/actors` | 5 |
| `admin/workflows` | 5 |
| `admin/agent` | 4 |
| `api/v2` | 4 |
| `admin/asset-swipe` | 3 |
| `admin/credit-codes` | 3 |
| `admin/scripts` | 3 |
| `admin/situations` | 3 |
| `admin/video-templates` | 3 |
| `admin/voices` | 3 |
| `messenger/web` | 3 |
| `ab-tests/features` | 2 |
| `admin/camera-movement` | 2 |
| `admin/featured-models` | 2 |
| `admin/global` | 2 |
| `admin/landing-tests` | 2 |
| `admin/personalActors` | 2 |
| `admin/products` | 2 |
| `api/v1` | 2 |
| `auth/renew-token` | 2 |
| `cdn-cgi/challenge-platform` | 2 |
| `config/private` | 2 |
| `e/t` | 2 |
| `g/s` | 2 |
| `sdk/v2` | 2 |
| `tr` | 2 |
| `video/1199693188` | 2 |
| `workflows/use` | 2 |
| `workspaces/77a46767-0e96-4b87-b393-267643c7adc2` | 2 |
| `workspaces/credit-consumption-history` | 2 |
| `workspaces/members` | 2 |
| `_/set_cookie` | 1 |
| `admin/contents` | 1 |
| `admin/creator-codes` | 1 |
| `admin/editingRequests` | 1 |
| `admin/events` | 1 |
| `admin/first-generations` | 1 |
| `admin/lipsync` | 1 |
| `admin/moderation` | 1 |
| `admin/releases` | 1 |
| `admin/workspaces` | 1 |
| `api/4506948625170432` | 1 |
| `api/auth` | 1 |
| `ccm/collect` | 1 |
| `config/44e5a6f3152249aae19ed3e4cad65ea` | 1 |
| `config/b2e63b5453c36ec48b28059c3ab6a699` | 1 |
| `consents/users` | 1 |
| `credit-codes/creator` | 1 |
| `credit-codes/me` | 1 |
| `cu6vrvqykjig/dkjmj` | 1 |
| `dashboard/addProduct` | 1 |
| `dashboard/folder` | 1 |
| `dashboard/paywall` | 1 |
| `dashboard/product` | 1 |
| `dashboard/project` | 1 |
| `dashboard/script` | 1 |
| `dropbox/connection-status` | 1 |
| `features/ai-actors` | 1 |
| `features/ai-ads` | 1 |
| `features/ai-avatars` | 1 |
| `features/ai-content-generator` | 1 |
| `features/ai-for-affiliate` | 1 |
| `features/ai-lipsync` | 1 |
| `features/ai-product-video-generator` | 1 |
| `features/ai-shorts-generator` | 1 |
| `features/ai-tik-tok-ads-generator` | 1 |
| `features/ai-ugc-video` | 1 |
| `features/ai-video-api` | 1 |
| `features/ai-video-generator` | 1 |
| `features/facebook-ai-ads-generator` | 1 |
| `features/talking-avatar-ai` | 1 |
| `features/text-to-speech` | 1 |
| `flow/library` | 1 |
| `flow/try` | 1 |
| `flow/use` | 1 |
| `google-drive/connection-status` | 1 |
| `industries/e-commerce` | 1 |
| `industries/insurance` | 1 |
| `industries/law-firms` | 1 |
| `industries/lead-gen` | 1 |
| `industries/marketing-agencies` | 1 |
| `industries/mobile-apps` | 1 |
| `industries/real-estate-agencies` | 1 |
| `industries/saas` | 1 |
| `integrations/catalog` | 1 |
| `libs/analytics-browser-2.42.4-min.js.gz` | 1 |
| `libs/plugin-session-replay-browser-1.32.1-min.js.gz` | 1 |
| `media/cloudfront-cookies` | 1 |
| `meta-ads/connection-status` | 1 |
| `notion/connection-status` | 1 |
| `offers/arcads10` | 1 |
| `onboarding/ad-spend` | 1 |
| `onboarding/attribution` | 1 |
| `onboarding/business-type` | 1 |
| `onboarding/contact` | 1 |
| `onboarding/intent` | 1 |
| `onboarding/payment` | 1 |
| `onboarding/paywall` | 1 |
| `onboarding/success` | 1 |
| `onboarding/team-size` | 1 |
| `onboarding/website` | 1 |
| `package/latest` | 1 |
| `pagead/1p-user-list` | 1 |
| `payment/free-trial` | 1 |
| `payment/local` | 1 |
| `pixel-config/v1` | 1 |
| `pricing/catalog` | 1 |
| `pricing/catalog-version` | 1 |
| `rmkt/collect` | 1 |
| `slack/connection-status` | 1 |
| `tiktok-ads/connection-status` | 1 |
| `tiktok/connection-status` | 1 |
| `tracking/browser-opt-out` | 1 |
| `tracking/payment-success` | 1 |
| `use-cases/ad-creative-testing` | 1 |
| `use-cases/ai-facebook-video-ad-generator` | 1 |
| `use-cases/ai-tik-tok-video-generator` | 1 |
| `use-cases/ai-youtube-video-generator` | 1 |
| `users/me` | 1 |
| `v1/lst` | 1 |
| `v1/sdk` | 1 |
| `wa` | 1 |
| `widget/t4j1iryr` | 1 |
| `workspaces/api-credentials` | 1 |
| `x-twitter/connection-status` | 1 |

### 调用最频繁的端点（= 首屏/核心链路的真实形态）

| 方法 | 路径 | 调用次数 | 有响应样本 |
|---|---|---|---|
| POST | `/ccm/collect` | 492 | — |
| POST | `/rmkt/collect/16604571238/` | 264 | — |
| GET | `/pagead/1p-user-list/16604571238/` | 262 | — |
| POST | `/v1/sdk/events` | 140 | — |
| GET | `/tr/` | 120 | — |
| GET | `/v1/lst/universal-script` | 98 | — |
| GET | `/g/s/collect` | 71 | — |
| GET | `/_/set_cookie` | 70 | — |
| GET | `/cu6vrvqykjig/dkjmj` | 20 | — |
| GET | `/onboarding/paywall` | 14 | — |
| GET | `/onboarding/attribution` | 4 | — |
| GET | `/dashboard/settings/general` | 3 | — |
| GET | `/integrations/catalog` | 3 | ✅ |
| GET | `/users/me` | 3 | ✅ |
| GET | `/workspaces/members` | 3 | ✅ |

### 鉴权与信封（实证）

- 统一信封：`{ret, errmsg, log_id, data}`；`ret=="0"` 代表成功。
- 部分 commerce 接口把业务体放在 `response`（**JSON 字符串**），需二次解析——这一点在抓包响应里可直接验证。
- 请求普遍带 `msToken` / `a_bogus` / `device_id` / `aid` 签名参数，由前端 SDK 生成；复刻时不能用别人的值，只能改成自建鉴权。

## 三、代码层证据（REA）

- 逐文件证据 44 份 / 268.8 MiB；成功 33 个源文件，失败 1 个（明细见 `analysis/rea-perfile.json`）。

| 源文件 | 证据 | 模块 | 函数 | 绑定 | 参数 | 语义关系 | 应用节点/边 |
|---|---|---|---|---|---|---|---|
| `0-2ymy8ig50nu.js` | 2.4 MiB | 1 | 82 | 148 | 99 | 1093 | 19/22 |
| `0bi35wm2b7iw3.js` | 4.6 MiB | 1 | 420 | 447 | 332 | 281 | 14/13 |
| `0gaw_nbtlfkp7.js` | 4.3 MiB | 1 | 241 | 491 | 192 | 1369 | 37/45 |
| `0kn7q9qwe55aq.js` | 3.6 MiB | 1 | 193 | 359 | 207 | 809 | 20/21 |
| `0lnnzrynaox35.js` | 2.2 MiB | 1 | 51 | 69 | 56 | 1498 | 5/4 |
| `0wn23v4b_tezt.js` | 2.5 MiB | 1 | 148 | 220 | 171 | 535 | 16/16 |
| `143888573.js` | 6.6 MiB | 1 | 629 | 351 | 219 | 112 | 284/338 |
| `162_iewo-akst.js` | 3.1 MiB | 1 | 110 | 270 | 75 | 968 | 55/66 |
| `19ekwenty1wjj.js` | 2.3 MiB | 1 | 71 | 103 | 98 | 164 | 3/2 |
| `1a6qwbp1h7k79.js` | 3.8 MiB | 1 | 193 | 406 | 260 | 1049 | 27/35 |
| `1g1wgh-1l8qz4.js` | 3.4 MiB | 1 | 139 | 265 | 194 | 514 | 4/3 |
| `1r5s4-apsz6r7.js` | 2.5 MiB | 1 | 84 | 185 | 124 | 917 | 8/7 |
| `1s65bzv6465hr.js` | 2.4 MiB | 1 | 129 | 186 | 141 | 401 | 13/15 |
| `1tget77wi4xtj.js` | 3.1 MiB | 1 | 170 | 345 | 264 | 424 | 12/13 |
| `21fxxjks_usoz.js` | 3.5 MiB | 1 | 204 | 466 | 134 | 846 | 34/48 |
| `26dio4keg7x5l.js` | 4.2 MiB | 1 | 100 | 201 | 171 | 64 | 3/2 |
| `26mwnd5hm_53p.js` | 6.6 MiB | 1 | 537 | 463 | 199 | 894 | 67/83 |
| `29gqqkjrhea9d.js` | 2.9 MiB | 1 | 160 | 332 | 233 | 638 | 6/6 |
| `2_6mitb_441ob.js` | 2.3 MiB | 1 | 63 | 119 | 45 | 212 | 3/2 |
| `2apl0snz0wit5.js` | 3.5 MiB | 1 | 150 | 368 | 154 | 1053 | 36/59 |
| `2bszo13wi4a30.js` | 2.4 MiB | 1 | 110 | 188 | 90 | 992 | 9/9 |
| `2e_l8wsapyxcm.js` | 6.1 MiB | 1 | 133 | 870 | 139 | 136 | 3/2 |
| `2jlzajy9j5_i9.js` | 3.9 MiB | 1 | 394 | 341 | 464 | 273 | 13/12 |
| `2ub59fy_2i454.js` | 3.3 MiB | 1 | 232 | 381 | 277 | 628 | 8/9 |
| `2x669bobi7-9_.js` | 7.8 MiB | 1 | 1116 | 83 | 0 | 4 | 20/19 |
| `2ymtu4wdqg7vz.js` | 3.5 MiB | 1 | 137 | 184 | 159 | 360 | 4/3 |
| `33aagglnpy5gk.js` | 2.5 MiB | 1 | 137 | 192 | 148 | 377 | 13/15 |
| `35y1a7r6hhmyj.js` | 2.8 MiB | 1 | 138 | 237 | 211 | 325 | 12/13 |
| `36uc_rrtepudd.js` | 7.3 MiB | 1 | 1084 | 108 | 7 | 2 | 14/13 |
| `3bzd7pat927hy.js` | 14.4 MiB | 1 | 1199 | 0 | 0 | 0 | 216/387 |
| `3i3_h784q36n6.js` | 2.7 MiB | 1 | 119 | 252 | 106 | 976 | 13/12 |
| `3joc1yl7us7f6.js` | 2.6 MiB | 1 | 142 | 244 | 269 | 528 | 10/13 |
| `3pkkkio9y67ig.js` | 3.9 MiB | 1 | 250 | 532 | 239 | 781 | 47/53 |
| `3qwsyarphz1_n.js` | 5.2 MiB | 1 | 661 | 319 | 219 | 135 | 7/7 |
| `app_tooltips-modern.2959f864.js` | 14.1 MiB | 1 | 1199 | 0 | 0 | 0 | 439/1228 |
| `cu6vrvqykjig__q883e60b7.js` | 18.1 MiB | 1 | 1199 | 0 | 0 | 0 | 327/816 |
| `frame-modern.2762eddb.js` | 18.4 MiB | 1 | 1199 | 0 | 0 | 0 | 341/1247 |
| `main.MTkyOWEyMGMwMQ.js` | 16.3 MiB | 1 | 1199 | 0 | 0 | 0 | 96/134 |
| `oaiq.min.js` | 5.4 MiB | 1 | 611 | 577 | 11 | 122 | 46/48 |
| `script__q013a6651.js` | 3.5 MiB | 1 | 301 | 593 | 221 | 633 | 18/19 |
| `sdk.6be5dfc02bbd61b83a465667402bfd77489a7a04.js` | 18.1 MiB | 1 | 1199 | 0 | 0 | 0 | 261/835 |
| `stripe.js` | 19.9 MiB | 1 | 1199 | 0 | 0 | 0 | 741/2074 |
| `ui-web-en-web.6be5dfc02bbd61b83a465667402bfd77489a7a04.js` | 7.6 MiB | 1 | 761 | 314 | 124 | 476 | 140/332 |
| `vendor-modern.e5315bcd.js` | 9.3 MiB | 1 | 1199 | 0 | 0 | 0 | 209/450 |

- 合计：函数 **19792** 个、绑定 **11209** 个、语义关系 **20589** 条——这就是可被复刻逻辑引用的代码面规模。
- REA 的 summary 模式**只保留结构不保留字符串值**，所以「哪些接口路径写在代码里」要回源码字面量里取（下面这段就是）：
- 镜像 JS 字面量里出现的接口路径 2 条，抓包命中 174 条，差集 1 条 → `analysis/coverage-gaps.json`。

## 四、数据模型（从实测响应聚合）

按「在多少个端点的响应里出现」排序，这些就是核心实体字段：

| 字段 | 出现端点数 | 说明 |
|---|---|---|
| `connected` | 8 | 实测响应字段 |
| `name` | 4 | 实测响应字段 |
| `email` | 3 | 实测响应字段 |
| `message` | 3 | 实测响应字段 |
| `statusCode` | 3 | 实测响应字段 |
| `amount` | 3 | 实测响应字段 |
| `priceId` | 3 | 实测响应字段 |
| `variant` | 3 | 实测响应字段 |
| `catalogId` | 3 | 实测响应字段 |
| `feature` | 2 | 实测响应字段 |
| `cohort` | 2 | 实测响应字段 |
| `user` | 2 | 实测响应字段 |
| `success` | 2 | 实测响应字段 |
| `configs` | 2 | 实测响应字段 |
| `diagnostics` | 2 | 实测响应字段 |
| `browserSDK` | 2 | 实测响应字段 |
| `sampleRate` | 2 | 实测响应字段 |
| `sessionReplay` | 2 | 实测响应字段 |
| `analyticsSDK` | 2 | 实测响应字段 |
| `status` | 2 | 实测响应字段 |
| `features` | 2 | 实测响应字段 |
| `error` | 2 | 实测响应字段 |

## 五、覆盖度与待补清单

- 已实证：端点 188 个、响应样本 35 个、资源 1986 个。
- 未实证（必须记 unknown，不得在实现里编造）：

  1. 真实生成调用链（提交任务/轮询进度）——需要真实点一次生成才会发出。
  2. 每个模型的积分单价 —— 同上。
  3. 画布保存协议与自动保存节流 —— 需要在编辑器里改一次才会发写请求。
  4. 导出格式与 task_type —— 需要真实导出。
  5. 支付下单与回调 —— 按纪律不碰。

- 代码里出现、但本轮抓包**没命中**的接口（下一轮优先补抓）：

| 路径（代码内形态） | 代码命中次数 |
|---|---|
| `/api/relay/e` | 1 |

## 六、复刻实现路径（对应 `rebuild/` 工程）

| 层 | 实现方式 | 证据基础 |
|---|---|---|
| 后端路由 | 每个实测端点一个 handler（`rebuild/backend/app/r_*.py`） | `docs/api-spec.json` |
| 后端响应 | 先原样回放抓包 fixture，再逐项替换为真实业务 | `app/fixtures/*.json` |
| 前端路由 | 按站点真实路由建页（`/home`、`/novel/list`、`/marketing-agent`、`/project`…） | 抓包 `routes-summary.json` |
| 前端样式 | 复用 `bundle/css/` 里原厂样式与类名，而不是自己发明主题 | `mirror` 内 CSS |
| 类型 | 由响应字段表生成（`docs/api-spec.json.response_fields`） | 实测响应 |

落地顺序建议：先把「有响应样本的端点」跑通（骨架已可跑），再补 unknown 的五类。

