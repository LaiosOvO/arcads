import { useEffect, useState } from "react";
import { callApi } from "../api";
import type { Endpoint } from "../types";

const EPS: Endpoint[] = [
  { method: "POST", path: "/commerce/v1/benefits/user_credit", calls: 1, query_keys: [], has_sample: true },
  { method: "POST", path: "/api/biz/v1/agent/get_available_model_list", calls: 1, query_keys: [], has_sample: true },
  { method: "POST", path: "/commerce/v1/subscription/price_list", calls: 1, query_keys: [], has_sample: true },
];

export default function Home() {
  const [out, setOut] = useState<Record<string, unknown>>({});
  useEffect(() => {
    (async () => {
      const next: Record<string, unknown> = {};
      for (const ep of EPS) {
        try { next[ep.path] = await callApi(ep); } catch (e) { next[ep.path] = String(e); }
      }
      setOut(next);
    })();
  }, []);
  return (
    <section>
      <h1 className="text-lg font-semibold text-slate-100">创作首页</h1>
      <p className="mt-1 text-sm text-slate-400">Agent 入口、模型选择、积分、会员弹窗（真实路由 /home）</p>
      <div className="mt-4 space-y-3">
        {EPS.map((ep) => (
          <div key={ep.path} className="rounded-lg border border-line bg-panel p-3">
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <span className="rounded bg-brand/15 px-1.5 py-0.5 text-brand">{ep.method}</span>
              <code>{ep.path}</code>
            </div>
            <pre className="mt-2 max-h-56 overflow-auto rounded bg-black/30 p-2 text-[11px] leading-relaxed text-slate-300">
{JSON.stringify(out[ep.path] ?? "loading…", null, 1).slice(0, 4000)}
            </pre>
          </div>
        ))}
      </div>
    </section>
  );
}
