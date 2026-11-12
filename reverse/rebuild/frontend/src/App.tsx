import { NavLink, Routes, Route, Navigate } from "react-router-dom";
import { Sparkles, Clapperboard, Megaphone, Terminal, LayoutGrid, Film } from "lucide-react";
import Home from "./pages/Home";
import Novel from "./pages/Novel";
import Interactive from "./pages/Interactive";
import Marketing from "./pages/Marketing";
import Cli from "./pages/Cli";
import Canvas from "./pages/Canvas";
import ApiExplorer from "./pages/ApiExplorer";

const NAV = [
  { to: "/home", label: "创作", icon: Sparkles },
  { to: "/novel/list", label: "短剧 Agent", icon: Clapperboard },
  { to: "/novel/interactive/list", label: "互动剧", icon: Film },
  { to: "/marketing-agent", label: "营销 Agent", icon: Megaphone },
  { to: "/cli", label: "CLI / API", icon: Terminal },
  { to: "/project", label: "画布", icon: LayoutGrid },
  { to: "/api", label: "接口浏览器", icon: LayoutGrid },
];

export default function App() {
  return (
    <div className="flex h-full">
      <aside className="w-60 shrink-0 border-r border-line bg-panel p-3">
        <div className="px-2 py-3 text-sm font-semibold tracking-wide text-slate-100">小云雀 · 复刻</div>
        <nav className="mt-2 space-y-1">
          {NAV.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to}
              className={({ isActive }) =>
                `flex items-center gap-2 rounded-md px-2 py-2 text-sm ${isActive ? "bg-brand/15 text-brand" : "text-slate-400 hover:bg-white/5"}`}>
              <Icon size={16} /> {label}
            </NavLink>
          ))}
        </nav>
        <p className="mt-6 px-2 text-[11px] leading-relaxed text-slate-500">
          路由与接口来自抓包实证；字段未实证处标注 untyped，不做臆造。
        </p>
      </aside>
      <main className="min-w-0 flex-1 overflow-auto p-5">
        <Routes>
          <Route path="/" element={<Navigate to="/home" replace />} />
          <Route path="/home" element={<Home />} />
          <Route path="/novel/list" element={<Novel />} />
          <Route path="/novel/interactive/list" element={<Interactive />} />
          <Route path="/marketing-agent" element={<Marketing />} />
          <Route path="/cli" element={<Cli />} />
          <Route path="/project" element={<Canvas />} />
          <Route path="/api" element={<ApiExplorer />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </div>
  );
}
