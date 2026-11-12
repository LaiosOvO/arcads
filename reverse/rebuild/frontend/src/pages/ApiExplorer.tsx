import { useEffect, useMemo, useState } from "react";
import { ENDPOINTS, FAMILIES } from "../types";

export default function ApiExplorer() {
  const [q, setQ] = useState("");
  const list = useMemo(
    () => ENDPOINTS.filter((e) => (e.path + e.method).toLowerCase().includes(q.toLowerCase())),
    [q]
  );
  return (
    <section>
      <h1 className="text-lg font-semibold text-slate-100">接口浏览器</h1>
      <p className="mt-1 text-sm text-slate-400">
        共 {ENDPOINTS.length} 个端点 / {Object.keys(FAMILIES).length} 个家族，全部来自抓包实证。
      </p>
      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="过滤 path 或 method…"
        className="mt-3 w-72 rounded-md border border-line bg-panel px-3 py-2 text-sm outline-none focus:border-brand" />
      <div className="mt-3 flex flex-wrap gap-2">
        {Object.entries(FAMILIES).map(([k, v]) => (
          <span key={k} className="rounded bg-white/5 px-2 py-1 text-[11px] text-slate-400">
            {k} · {v}
          </span>
        ))}
      </div>
      <ul className="mt-4 divide-y divide-line overflow-hidden rounded-lg border border-line">
        {list.map((e) => (
          <li key={e.method + e.path} className="flex items-center gap-3 bg-panel px-3 py-2 text-xs">
            <span className="w-14 shrink-0 rounded bg-brand/15 px-1.5 py-0.5 text-center text-brand">{e.method}</span>
            <code className="flex-1 truncate text-slate-300">{e.path}</code>
            <span className="text-slate-500">{e.calls} 次</span>
            <span className={e.has_sample ? "text-ok" : "text-warn"}>{e.has_sample ? "有响应样本" : "未实证"}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
