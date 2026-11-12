// 所有请求都打本地后端（vite 已配 proxy）。后端回的是抓包实证的响应体。
import type { Endpoint } from "./types";

const BASE = "";

export async function callApi(ep: Endpoint, body?: unknown): Promise<unknown> {
  const init: RequestInit = { method: ep.method, headers: { "content-type": "application/json" } };
  if (body && ep.method !== "GET") init.body = JSON.stringify(body);
  const res = await fetch(BASE + ep.path, init);
  const text = await res.text();
  try { return JSON.parse(text); } catch { return text.slice(0, 400); }
}

export async function fetchSpec(): Promise<{ endpoints: Endpoint[] }> {
  const res = await fetch("/_meta/spec");
  if (!res.ok) return { endpoints: [] };
  return res.json();
}
