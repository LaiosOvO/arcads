# Arcads · 复刻工程骨架（抓包 + REA 驱动）

生成时间：2026-11-12 19:32

这份工程**不是拍脑袋写的**：路由、方法、入参、字段、响应样例全部来自
`docs/api-spec.json`（ego-browser CDP 实抓 + 递归收敛镜像），
代码层佐证来自 `analysis/rea-evidence/`（REA 静态分析证据包）。

## 结构

```
rebuild/
├── backend/            FastAPI。51 个路由家族 / 188 个端点 / 35 个真实响应 fixture
│   ├── app/main.py     路由注册 + CORS + /_meta/spec
│   ├── app/r_*.py      按家族分组的路由（每个端点一个 handler）
│   ├── app/fixtures/   抓包原文，原样回放
│   └── run.sh          venv + uvicorn :8000
└── frontend/           React 18 + Vite + TS + Tailwind + zustand + lucide-react
    └── src/pages/      6 个站点路由页 + 1 个接口浏览器
```

## 跑起来

```bash
cd backend && ./run.sh                       # http://127.0.0.1:8000
cd frontend && npm i && npm run dev          # http://127.0.0.1:5173 （已配 proxy 到 8000）
```

## 覆盖度（诚实口径）

| 维度 | 状态 |
|---|---|
| 端点清单（method + path + query 键） | ✅ 实证，见 `docs/api-spec.json` |
| 入参（请求体） | ✅ 有 postData 的即实证；无 body 的标 `untyped` |
| 响应（字段 + 样例） | ✅ 有落盘响应体的直接回放；无样本的显式 `_note` 标注 |
| 鉴权（Cookie/sessionid + msToken/a_bogus 签名） | ⚠️ 只做了结构说明，**未实现签名算法** |
| 真实生成/扣费/支付/导出 | ❌ 未抓（按纪律未提交生成与支付） |

## 下一步怎么并进来

1. 抓新的响应 → `build_api_docs.py` 重跑 → `api-spec.json` 更新 → 本工程重生成；
2. 需要真实业务逻辑时，把 `app/r_*.py` 里的 fixture 回放替换成写库/调上游；
3. 前端页面目前是「把真实响应渲染出来」的证据页，配色与布局需按 `bundle/css/` 里的原厂样式逐项对齐。
