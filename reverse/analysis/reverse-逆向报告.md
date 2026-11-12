# reverse 逆向抓取报告

- 生成时间：2026-11-12 21:23:44 +0800
- 入口：`https://www.arcads.ai/`
- 方法：ego-browser（真实 Chromium）CDP `Network.getResponseBody` 实抓 + 按前端构建清单递归收敛全量静态资源。
- 证据口径：**seen** = 已落盘文件/抓包；**unknown** = 未抓到，不代表不存在。

## 一、抓取结果

- 资源总数：**1986**；总字节：**291,342,811**（277.8 MiB）
- 下载/解析错误：317（多为构建运行时字符串误提取导致的 404，或 CDP 缓冲淘汰）
- 校验：清单 1986 / 磁盘 3603；sha256 抽查 600，不符 0；查询串同路径碰撞 0（同 URL 路径不同 `?query` 的 API 响应，最后一次覆盖前者）

| 扩展名 | 数量 |
|---|---|
| `(none)` | 556 |
| `.js*` | 398 |
| `.js` | 344 |
| `.html*` | 176 |
| `.gif` | 159 |
| `.webp` | 90 |
| `.json*` | 53 |
| `.mp4` | 52 |
| `.png` | 46 |
| `.jpg` | 45 |
| `.webm` | 24 |
| `.css` | 14 |
| `.woff2` | 6 |
| `.avif` | 6 |
| `.otf` | 5 |
| `.html` | 4 |
| `.svg` | 3 |
| `.gz` | 2 |
| `.json` | 1 |
| `.ico` | 1 |
| `.ttf` | 1 |

> 带 `*` 的类别表示 URL 本身无扩展名（如 `/`、`/docs`），按 content-type 归类。

## 二、抓取路由（CDP 实测）

| 路由 | URL | 事件 | 响应 | 文本落盘 | 失败 |
|---|---|---|---|---|---|
| home | https://www.arcads.ai/ | 1179 | 164 | 49 | 12 |
| privacy | https://www.arcads.ai/privacy | 464 | 70 | 9 | 10 |
| terms | https://www.arcads.ai/terms | 424 | 64 | 9 | 10 |
| login | https://app.arcads.ai/onboarding/attribution | 910 | 149 | 100 | 12 |
| blog | https://www.arcads.ai/blog | 572 | 78 | 10 | 8 |
| product | https://app.arcads.ai/onboarding/attribution | 865 | 142 | 18 | 11 |
| usecases | https://www.arcads.ai/usecases | 776 | 88 | 14 | 12 |
| payment_success | https://www.arcads.ai/payment_success | 456 | 68 | 10 | 9 |
| tracking-payment-success | https://www.arcads.ai/tracking/payment-success | 456 | 69 | 10 | 10 |
| features-ai-actors | https://www.arcads.ai/features/ai-actors | 932 | 151 | 9 | 9 |
| features-ai-ads | https://www.arcads.ai/features/ai-ads | 912 | 161 | 15 | 10 |
| features-ai-avatars | https://www.arcads.ai/features/ai-avatars | 900 | 157 | 12 | 9 |
| features-ai-content-generator | https://www.arcads.ai/features/ai-content-generator | 1062 | 163 | 13 | 10 |
| features-ai-for-affiliate | https://www.arcads.ai/features/ai-for-affiliate | 938 | 152 | 8 | 10 |
| features-ai-lipsync | https://www.arcads.ai/features/ai-lipsync | 886 | 154 | 10 | 9 |
| features-ai-product-video-generator | https://www.arcads.ai/features/ai-product-video-generator | 877 | 154 | 10 | 9 |
| features-ai-shorts-generator | https://www.arcads.ai/features/ai-shorts-generator | 943 | 153 | 9 | 11 |
| features-ai-tik-tok-ads-generator | https://www.arcads.ai/features/ai-tik-tok-ads-generator | 906 | 159 | 9 | 11 |
| features-ai-ugc-video | https://www.arcads.ai/features/ai-ugc-video | 964 | 165 | 11 | 12 |
| features-ai-video-api | https://www.arcads.ai/features/ai-video-api | 923 | 155 | 9 | 9 |
| features-ai-video-generator | https://www.arcads.ai/features/ai-video-generator | 1174 | 162 | 9 | 8 |
| features-facebook-ai-ads-generator | https://www.arcads.ai/features/facebook-ai-ads-generator | 935 | 151 | 8 | 10 |
| features-talking-avatar-ai | https://www.arcads.ai/features/talking-avatar-ai | 1006 | 170 | 13 | 11 |
| features-text-to-speech | https://www.arcads.ai/features/text-to-speech | 897 | 155 | 8 | 10 |
| industries-e-commerce | https://www.arcads.ai/industries/e-commerce | 1080 | 153 | 9 | 11 |
| industries-insurance | https://www.arcads.ai/industries/insurance | 923 | 155 | 10 | 9 |
| industries-law-firms | https://www.arcads.ai/industries/law-firms | 1051 | 166 | 13 | 10 |
| industries-lead-gen | https://www.arcads.ai/industries/lead-gen | 1031 | 155 | 8 | 10 |
| industries-marketing-agencies | https://www.arcads.ai/industries/marketing-agencies | 933 | 154 | 9 | 10 |
| industries-mobile-apps | https://www.arcads.ai/industries/mobile-apps | 1127 | 157 | 12 | 9 |
| industries-real-estate-agencies | https://www.arcads.ai/industries/real-estate-agencies | 989 | 157 | 10 | 11 |
| industries-saas | https://www.arcads.ai/industries/saas | 1171 | 161 | 13 | 10 |
| use-cases-ad-creative-testing | https://www.arcads.ai/use-cases/ad-creative-testing | 1044 | 155 | 9 | 9 |
| use-cases-ai-facebook-video-ad-generator | https://www.arcads.ai/use-cases/ai-facebook-video-ad-generator | 879 | 154 | 10 | 8 |
| use-cases-ai-tik-tok-video-generator | https://www.arcads.ai/use-cases/ai-tik-tok-video-generator | 1021 | 166 | 10 | 21 |
| use-cases-ai-youtube-video-generator | https://www.arcads.ai/use-cases/ai-youtube-video-generator | 1114 | 153 | 11 | 9 |
| dashboard | https://app.arcads.ai/onboarding/attribution | 1351 | 237 | 104 | 12 |
| dashboard-addProduct | https://app.arcads.ai/onboarding/attribution | 1184 | 202 | 23 | 12 |
| dashboard-folder | https://app.arcads.ai/onboarding/attribution | 1125 | 192 | 28 | 3 |
| dashboard-paywall | https://app.arcads.ai/onboarding/attribution | 1157 | 198 | 20 | 12 |
| dashboard-product | https://app.arcads.ai/onboarding/attribution | 1135 | 199 | 24 | 12 |
| dashboard-project | https://app.arcads.ai/onboarding/attribution | 1111 | 194 | 18 | 13 |
| dashboard-script | https://app.arcads.ai/onboarding/attribution | 1178 | 203 | 24 | 12 |
| dashboard-settings | https://app.arcads.ai/dashboard/settings | 958 | 174 | 14 | 10 |
| dashboard-settings-account | https://app.arcads.ai/onboarding/attribution | 1381 | 234 | 24 | 10 |
| dashboard-settings-billing | https://app.arcads.ai/onboarding/attribution | 1310 | 231 | 30 | 13 |
| dashboard-settings-general | https://app.arcads.ai/onboarding/paywall | 1164 | 215 | 18 | 10 |
| dashboard-settings-integrations | https://app.arcads.ai/onboarding/attribution | 1474 | 254 | 35 | 16 |
| dashboard-settings-mcp | https://app.arcads.ai/onboarding/paywall | 963 | 175 | 14 | 9 |
| dashboard-settings-members | https://app.arcads.ai/onboarding/attribution | 1537 | 256 | 29 | 19 |
| dashboard-settings-public-api | https://app.arcads.ai/onboarding/attribution | 1299 | 229 | 26 | 16 |
| onboarding | https://app.arcads.ai/onboarding/attribution | 815 | 137 | 18 | 11 |
| onboarding-ad-spend | https://app.arcads.ai/onboarding/attribution | 759 | 122 | 24 | 3 |
| onboarding-attribution | https://app.arcads.ai/onboarding/attribution | 682 | 115 | 13 | 9 |
| onboarding-business-type | https://app.arcads.ai/onboarding/business-type | 694 | 119 | 17 | 10 |
| onboarding-contact | https://app.arcads.ai/onboarding/contact | 837 | 136 | 16 | 12 |
| onboarding-intent | https://app.arcads.ai/onboarding/attribution | 861 | 142 | 19 | 11 |
| onboarding-payment | https://app.arcads.ai/onboarding/payment | 700 | 117 | 13 | 14 |
| onboarding-paywall | https://app.arcads.ai/onboarding/attribution | 996 | 168 | 20 | 11 |
| onboarding-success | https://app.arcads.ai/onboarding/success | 694 | 118 | 15 | 11 |
| onboarding-team-size | https://app.arcads.ai/onboarding/team-size | 689 | 118 | 16 | 10 |
| onboarding-website | https://app.arcads.ai/onboarding/website | 788 | 132 | 28 | 11 |
| flow | https://app.arcads.ai/onboarding/attribution | 1517 | 248 | 51 | 3 |
| flow-library | https://app.arcads.ai/flow/library | 2056 | 166 | 13 | 9 |
| flow-try | https://app.arcads.ai/flow/try | 1041 | 134 | 14 | 8 |
| flow-use | https://app.arcads.ai/onboarding/attribution | 1385 | 245 | 22 | 10 |
| integrations-catalog | https://app.arcads.ai/onboarding/attribution | 901 | 147 | 20 | 15 |
| consents-users | https://app.arcads.ai/onboarding/attribution | 843 | 141 | 19 | 10 |
| project | https://app.arcads.ai/onboarding/attribution | 868 | 139 | 24 | 4 |
| users | https://app.arcads.ai/onboarding/attribution | 849 | 140 | 18 | 11 |
| users-me | https://app.arcads.ai/onboarding/attribution | 843 | 140 | 17 | 11 |
| admin | https://app.arcads.ai/onboarding/attribution | 861 | 144 | 23 | 9 |
| admin-actors | https://app.arcads.ai/onboarding/attribution | 869 | 144 | 21 | 9 |
| admin-actors-checkVoices | https://app.arcads.ai/onboarding/attribution | 928 | 147 | 29 | 2 |
| admin-actors-new | https://app.arcads.ai/ | 758 | 129 | 19 | 12 |
| admin-actors-stats | https://app.arcads.ai/ | 790 | 130 | 21 | 10 |
| admin-actors-validationProcess | https://app.arcads.ai/ | 827 | 140 | 20 | 11 |
| admin-agent-animation-studio | https://app.arcads.ai/ | 724 | 127 | 20 | 9 |
| admin-agent-motion-templates | https://app.arcads.ai/ | 742 | 126 | 18 | 11 |
| admin-agent-skills | https://app.arcads.ai/ | 818 | 138 | 22 | 9 |
| admin-agent-skills-import | https://app.arcads.ai/onboarding/attribution | 854 | 139 | 17 | 10 |
| admin-asset-swipe | https://app.arcads.ai/onboarding/attribution | 873 | 145 | 22 | 9 |
| admin-asset-swipe-next | https://app.arcads.ai/onboarding/attribution | 886 | 141 | 27 | 2 |
| admin-asset-swipe-votes | https://app.arcads.ai/onboarding/attribution | 871 | 140 | 18 | 10 |
| admin-camera-movement | https://app.arcads.ai/onboarding/attribution | 900 | 150 | 22 | 10 |
| admin-camera-movement-situations | https://app.arcads.ai/onboarding/attribution | 824 | 136 | 15 | 11 |
| admin-contents | https://app.arcads.ai/ | 743 | 128 | 19 | 12 |
| admin-creator-codes | https://app.arcads.ai/ | 735 | 122 | 16 | 11 |
| admin-credit-codes | https://app.arcads.ai/ | 766 | 131 | 15 | 11 |
| admin-credit-codes-batches | https://app.arcads.ai/onboarding/attribution | 830 | 141 | 22 | 9 |
| admin-credit-codes-cost-rate | https://app.arcads.ai/ | 742 | 126 | 14 | 11 |
| admin-editingRequests | https://app.arcads.ai/onboarding/attribution | 899 | 148 | 22 | 9 |
| admin-events | https://app.arcads.ai/onboarding/attribution | 883 | 149 | 22 | 10 |
| admin-featured-models | https://app.arcads.ai/onboarding/attribution | 862 | 142 | 20 | 10 |
| admin-featured-models-reorder | https://app.arcads.ai/onboarding/attribution | 856 | 142 | 18 | 12 |
| admin-first-generations | https://app.arcads.ai/onboarding/attribution | 897 | 150 | 22 | 10 |
| admin-global | https://app.arcads.ai/ | 705 | 123 | 15 | 11 |
| admin-global-featured-models | https://app.arcads.ai/ | 956 | 161 | 31 | 12 |
| admin-landing-tests | https://app.arcads.ai/ | 718 | 124 | 16 | 12 |
| admin-landing-tests-new | https://app.arcads.ai/ | 712 | 124 | 16 | 9 |
| admin-lipsync-actors | https://app.arcads.ai/onboarding/attribution | 885 | 145 | 18 | 11 |
| admin-moderation | https://app.arcads.ai/onboarding/attribution | 856 | 138 | 19 | 9 |
| admin-personalActors | https://app.arcads.ai/ | 785 | 133 | 24 | 4 |
| admin-personalActors-stats | https://app.arcads.ai/ | 786 | 132 | 17 | 11 |
| admin-pricing-ab-tests | https://app.arcads.ai/onboarding/attribution | 891 | 146 | 19 | 11 |
| admin-pricing-ab-tests-new | https://app.arcads.ai/ | 746 | 126 | 14 | 13 |
| admin-pricing-catalogs | https://app.arcads.ai/ | 716 | 124 | 17 | 9 |
| admin-pricing-catalogs-active | https://app.arcads.ai/ | 770 | 135 | 18 | 11 |
| admin-pricing-margin-simulator | https://app.arcads.ai/onboarding/attribution | 940 | 151 | 21 | 11 |
| admin-pricing-plans | https://app.arcads.ai/onboarding/attribution | 841 | 141 | 17 | 11 |
| admin-pricing-stripe-products | https://app.arcads.ai/onboarding/attribution | 866 | 142 | 16 | 11 |
| admin-products | https://app.arcads.ai/ | 728 | 126 | 15 | 12 |
| admin-products-create | https://app.arcads.ai/ | 725 | 126 | 17 | 11 |
| admin-releases-whats-new | https://app.arcads.ai/ | 855 | 133 | 19 | 11 |
| admin-scripts | https://app.arcads.ai/onboarding/attribution | 883 | 145 | 19 | 10 |
| admin-scripts-all | https://app.arcads.ai/ | 719 | 125 | 14 | 12 |
| admin-scripts-moderated | https://app.arcads.ai/onboarding/attribution | 914 | 148 | 21 | 10 |
| admin-situations | https://app.arcads.ai/onboarding/attribution | 895 | 142 | 19 | 12 |
| admin-situations-data | https://app.arcads.ai/onboarding/attribution | 885 | 144 | 20 | 9 |
| admin-situations-gestures-create | https://app.arcads.ai/onboarding/attribution | 853 | 141 | 19 | 10 |
| admin-video-templates | https://app.arcads.ai/onboarding/attribution | 905 | 152 | 31 | 4 |
| admin-video-templates-categories | https://app.arcads.ai/ | 737 | 127 | 17 | 11 |
| admin-video-templates-new | https://app.arcads.ai/ | 774 | 129 | 19 | 13 |
| admin-voices | https://app.arcads.ai/onboarding/attribution | 919 | 153 | 20 | 11 |
| admin-voices-new | https://app.arcads.ai/ | 762 | 131 | 20 | 12 |
| admin-voices-stats | https://app.arcads.ai/onboarding/attribution | 910 | 152 | 21 | 9 |
| admin-workflows | https://app.arcads.ai/ | 707 | 123 | 16 | 11 |
| admin-workflows-library | https://app.arcads.ai/ | 767 | 130 | 17 | 11 |
| admin-workflows-library-order | https://app.arcads.ai/onboarding/attribution | 884 | 141 | 20 | 9 |
| admin-workflows-library-settings | https://app.arcads.ai/onboarding/attribution | 828 | 140 | 19 | 10 |
| admin-workflows-top | https://app.arcads.ai/ | 739 | 126 | 17 | 12 |
| admin-workspaces-arcads10-offer-links | https://app.arcads.ai/onboarding/attribution | 888 | 141 | 18 | 9 |

## 三、技术栈信号（字符串命中文件数）

- turbopack：386 个文件
- sentry：297 个文件
- next.js：106 个文件
- stripe：71 个文件
- react：56 个文件
- gsap：37 个文件
- antd：14 个文件
- redux：10 个文件
- sse：3 个文件
- zustand：1 个文件

## 四、真实 API 契约（抓包实证 47 条，按命中次数排序）

| 方法 | 路径 | 命中 | 示例请求体 |
|---|---|---|---|
| GET | `/cu6vrvqykjig` | 375 | - |
| GET | `/onboarding` | 70 | - |
| GET | `/api/auth/session` | 35 | - |
| GET | `/` | 21 | - |
| GET | `/onboarding/paywall` | 12 | - |
| POST | `/cu6vrvqykjig` | 7 | - |
| GET | `/ab-tests/features` | 4 | - |
| GET | `/auth/renew-token` | 4 | - |
| GET | `/config/private` | 4 | - |
| GET | `/onboarding/attribution` | 4 | - |
| GET | `/payment/local/USD` | 4 | - |
| GET | `/pricing/catalog-version` | 4 | - |
| POST | `/tracking/browser-opt-out` | 4 | `{"browserOptOut":true}` |
| GET | `/users/me` | 4 | - |
| GET | `/workspaces` | 4 | - |
| POST | `/api/v1/check/a2378073-dfcc-4ce0-b9cf-cc4866dac6e2` | 2 | `{"datetime":"2026-11-12T08:33:13.490Z","os":"MacOS","os_type":"MacIntel","os_version":"10.15","client_user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_…` |
| OPTIONS | `/api/v1/check/a2378073-dfcc-4ce0-b9cf-cc4866dac6e2` | 2 | - |
| GET | `/payment/free-trial` | 2 | - |
| GET | `/workspaces/members` | 2 | - |
| OPTIONS | `/workspaces/members` | 2 | - |
| OPTIONS | `/ab-tests/features` | 1 | - |
| OPTIONS | `/auth/renew-token` | 1 | - |
| OPTIONS | `/config/private` | 1 | - |
| GET | `/credit-codes/creator` | 1 | - |
| GET | `/credit-codes/me` | 1 | - |
| GET | `/dashboard/settings/general` | 1 | - |
| GET | `/dropbox/connection-status` | 1 | - |
| GET | `/flow` | 1 | - |
| GET | `/fonts/Redaction20-Italic.otf` | 1 | - |
| GET | `/google-drive/connection-status` | 1 | - |
| GET | `/integrations/catalog` | 1 | - |
| GET | `/media/cloudfront-cookies` | 1 | - |
| GET | `/meta-ads/connection-status` | 1 | - |
| GET | `/notion/connection-status` | 1 | - |
| GET | `/offers/arcads10` | 1 | - |
| GET | `/pricing/catalog` | 1 | - |
| GET | `/slack/connection-status` | 1 | - |
| GET | `/tiktok-ads/connection-status` | 1 | - |
| GET | `/tiktok/connection-status` | 1 | - |
| OPTIONS | `/workflows/use/editor-state` | 1 | - |

完整清单见 `/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/analysis/api-contracts.json`。

## 五、API 路径（静态命中 7 条，候选）

- `/api/`
- `/api/relay/e`
- `/api/v2/pixel`
- `/v1/chooseServer`
- `/v1/elements/sessions`
- `/v1/payment_pages/.../init`
- `/v1/refreshCreds`

## 六、前端路由（静态命中 7 条，抽样）

- `/ag/g/c`
- `/as/d`
- `/as/d/ccm/conversion`
- `/as/p/c`
- `/ga/g/c`
- `/gs/ccm/conversion`
- `/mc/collect`

## 七、外部域（Top）

- `cdn.prod.website-files.com`：5136
- `andreatuysuzian.com`：3215
- `www.w3.org`：1047
- `load.tss.arcads.ai`：722
- `www.arcads.ai`：579
- `tss.arcads.ai`：526
- `www.google.com`：355
- `privacy.arcads.ai`：294
- `fonts.gstatic.com`：224
- `app.arcads.ai`：217
- `api.arcads.ai`：205
- `www.youtube.com`：182
- `www.facebook.com`：155
- `r.wdfl.co`：133
- `argoseyes.s3-accelerate.amazonaws.com`：129
- `analytics.google.com`：92
- `i.ytimg.com`：84
- `arcads.pages.dev`：68
- `help.arcads.ai`：60
- `js.stripe.com`：45
- `cdn.amplitude.com`：39
- `d3e54v103j8qbb.cloudfront.net`：37
- `data.arcads.ai`：35
- `cdnjs.cloudflare.com`：34
- `schema.org`：32

## 八、限制与口径

- 未登录/未点开的页面（如创建向导、生成任务页）其私有接口未抓到，记为 unknown。
- 静态命中的 API/路由为候选，实际以 `capture/network-*.json` 与 `capture/cdp-response-bodies.json` 为准。
- capture 已脱敏（Bearer/JWT/Cookie/token 键/邮箱/Clerk user_/sess_），业务 UUID 保留。
