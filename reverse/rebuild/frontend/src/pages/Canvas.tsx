import { useEffect, useState } from "react";
import { callApi } from "../api";
import type { Endpoint } from "../types";

const EPS: Endpoint[] = [
  { method: "POST", path: "/api/biz/v1/asset/create_v2", calls: 1, query_keys: [], has_sample: true },
  { method: "POST", path: "/api/web/v1/tcc/get_config", calls: 1, query_keys: [], has_sample: true },
];

export default function Canvas() {
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
      <h1 className="text-lg font-semibold text-slate-100">画布编辑器</h1>
      <p className="mt-1 text-sm text-slate-400">自由画布 + 素材 + Agent 对话（真实路由 /project?projectId=&canvasId=）</p>
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
