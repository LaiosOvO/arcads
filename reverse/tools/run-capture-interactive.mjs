/**
 * Arcads 增量取证 runner（独立输出，绝不覆盖 capture/ 的 132 路由全量证据）
 *
 * 目的（用户 21:04 授权：只读类受控交互 + 长连接/事件端点补齐）：
 *   A. 补 /api/relay/e —— Amplitude SDK 中继上报端点（ab_arcads_paid_funnel 漏斗 A/B 门控，
 *      visibilitychange 时 setTransport("beacon") + flush()）。因此：
 *        - 必须收集 type=Ping（beacon）与 Fetch/XHR，不能用原 runner 的 type 白名单；
 *        - 必须覆盖 onboarding 漏斗页；
 *        - 必须触发 flush（visibilitychange / pagehide）。
 *   B. 受控只读交互补 sample_body：只点击经过危险词白名单过滤的 button/[role=tab]/summary，
 *      不填表、不提交、不新建/删除/改名业务对象、不发消息、不点生成、不购买、不改账号设置。
 *
 * 纪律：所有数字只来自落盘证据；抓不到就写 unknown，不伪造响应体。
 * 运行：ego-browser nodejs < tools/run-capture-interactive.mjs
 */
const CFG = {
  spaceName: "login-probe",
  outDir: "/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse",
  outSub: "capture-interactive",
  routes: [
    { name: "onboarding-attribution", url: "https://app.arcads.ai/onboarding/attribution" },
    { name: "onboarding-intent", url: "https://app.arcads.ai/onboarding/intent" },
    { name: "onboarding-paywall", url: "https://app.arcads.ai/onboarding/paywall" },
    { name: "flow-library", url: "https://app.arcads.ai/flow/library" },
    { name: "public-home", url: "https://www.arcads.ai/" },
  ],
  settleMs: 9000,          // 等 Amplitude 自动 flush（默认 flushInterval 约 1s，留足余量）
  clickBudget: 5,          // 每页最多点击次数
};

const fs = await import("node:fs/promises");
const path = await import("node:path");
const crypto = await import("node:crypto");

const ROOT = path.join(CFG.outDir, CFG.outSub);
const BODIES = path.join(ROOT, "bodies");
await fs.mkdir(BODIES, { recursive: true });

// 危险词：任何带这些语义的控件一律不点（只读交互红线）
const DANGER = /create|new|delete|remove|save|submit|generate|buy|purchase|upgrade|pay|checkout|subscribe|invite|send|upload|confirm|logout|sign\s*out|start\s*trial|创建|新建|删除|移除|保存|提交|生成|购买|支付|订阅|邀请|发送|上传|确认|登出|退出|下一步|继续/i;

const task = await taskSpace(CFG.spaceName);
const page = task.page("p1");
await page.cdp("Network.enable", { maxTotalBufferSize: 800000000, maxResourceBufferSize: 60000000 });
console.log("SPACE=" + task.spaceId + " OUT=" + ROOT);

const allEvents = [];
const phases = [];
const bodies = [];
const seenBodyReq = new Set();

function safeName(s) {
  return String(s || "").replace(/[^A-Za-z0-9._-]/g, "_").slice(0, 120);
}

/** 收集 ego-browser 自上次调用以来的 CDP 事件，打上 phase 标签 */
async function drain(phase) {
  let ev = [];
  try { ev = await page.events(); } catch (e) { ev = []; }
  const tagged = (ev || []).map((e) => ({ phase, ...e }));
  allEvents.push(...tagged);
  phases.push({ phase, events: ev.length });
  return tagged;
}

/** 只对 arcads 主域的文本响应取 body；beacon/Ping 常见无体可读，如实记 error */
async function saveBodies(phase, ev) {
  let ok = 0, fail = 0;
  for (const e of ev) {
    if (e.method !== "Network.responseReceived") continue;
    const p = e.params || {}, r = p.response || {};
    const url = r.url || "";
    if (!/^https?:\/\//.test(url)) continue;
    let host = "";
    try { host = new URL(url).hostname.toLowerCase(); } catch (_) { continue; }
    if (!(host === "arcads.ai" || host.endsWith(".arcads.ai"))) continue;
    const mime = (r.mimeType || "").toLowerCase();
    if (!/json|text|javascript|html|xml/.test(mime)) continue;
    const rid = p.requestId;
    const key = rid + "|" + url;
    if (seenBodyReq.has(key)) continue;
    seenBodyReq.add(key);
    let rec = { phase, requestId: rid, url, status: r.status, mimeType: r.mimeType, type: p.type };
    try {
      const rb = await page.cdp("Network.getResponseBody", { requestId: rid });
      const buf = rb.base64Encoded ? Buffer.from(rb.body, "base64") : Buffer.from(rb.body, "utf8");
      const fp = path.join(BODIES, safeName(phase) + "__" + safeName(new URL(url).pathname) + "__" + crypto.createHash("sha1").update(url).digest("hex").slice(0, 8) + ".txt");
      await fs.writeFile(fp, buf);
      rec.local_path = fp;
      rec.bytes = buf.length;
      rec.sha256 = crypto.createHash("sha256").update(buf).digest("hex");
      bodies.push(rec);
      ok++;
    } catch (err) {
      rec.error = String((err && err.message) || err).slice(0, 200);
      bodies.push(rec);
      fail++;
    }
  }
  return { ok, fail };
}

for (const route of CFG.routes) {
  const phase = "goto:" + route.name;
  let gotoErr = null;
  try { await page.goto(route.url, { timeout: 60000 }); }
  catch (e) { gotoErr = String((e && e.message) || e).slice(0, 200); }
  try { await page.waitForLoadState("load", { timeout: 25000 }); } catch (_) {}
  try {
    await page.waitForFunction(() => document.body && document.body.innerText.length > 60, undefined, { timeout: 15000 });
  } catch (_) {}

  const landing = await page.evaluate(() => ({ href: location.href, title: document.title, textLen: (document.body?.innerText || "").length })).catch(() => ({}));
  let ev = await drain(phase);
  let b = await saveBodies(phase, ev);
  console.log(`ROUTE ${route.name} err=${gotoErr} href=${landing.href} events=${ev.length} bodies=${b.ok}/${b.fail}`);

  // ---- 受控只读交互：动态枚举 + 危险词过滤 + data-ego-ro 锚定 ----
  let candidates = [];
  try {
    candidates = await page.evaluate((budget) => {
      const bad = /create|new|delete|remove|save|submit|generate|buy|purchase|upgrade|pay|checkout|subscribe|invite|send|upload|confirm|logout|sign\s*out|start\s*trial|创建|新建|删除|移除|保存|提交|生成|购买|支付|订阅|邀请|发送|上传|确认|登出|退出|下一步|继续/i;
      const out = [];
      const els = Array.from(document.querySelectorAll('button,[role="tab"],summary,[data-testid]'));
      for (const el of els) {
        if (out.length >= budget) break;
        const t = (el.innerText || el.getAttribute("aria-label") || "").trim().replace(/\s+/g, " ");
        if (!t || t.length > 40 || bad.test(t)) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 4 || r.height < 4) continue;
        const idx = out.length;
        el.setAttribute("data-ego-ro", String(idx));
        out.push({ idx, tag: el.tagName, role: el.getAttribute("role"), text: t });
      }
      return out;
    }, CFG.clickBudget);
  } catch (e) { candidates = []; }

  const clicks = [];
  for (const c of candidates) {
    const cp = `click:${route.name}#${c.idx}`;
    let status = "ok";
    try {
      await page.click(`[data-ego-ro="${c.idx}"]`, { label: "readonly:" + c.text });
    } catch (e) { status = "fail:" + String((e && e.message) || e).slice(0, 100); }
    await new Promise((r) => setTimeout(r, 1200));
    const cev = await drain(cp);
    const cb = await saveBodies(cp, cev);
    clicks.push({ ...c, status, events: cev.length, bodies: cb.ok });
    console.log(`  CLICK #${c.idx} ${JSON.stringify(c.text)} ${status} events=${cev.length}`);
  }

  // ---- 触发 Amplitude flush：visibilitychange(hidden) + pagehide ----
  // 这是页面运行时观测钩子，不改业务对象、不提交表单；如实记入 trace。
  const flushPhase = `flush:${route.name}`;
  let flushInfo = null;
  try {
    flushInfo = await page.evaluate(() => {
      const before = document.visibilityState;
      try {
        Object.defineProperty(document, "visibilityState", { configurable: true, get: () => "hidden" });
        Object.defineProperty(document, "hidden", { configurable: true, get: () => true });
        document.dispatchEvent(new Event("visibilitychange"));
        window.dispatchEvent(new Event("pagehide"));
      } catch (e) { return { before, error: String(e && e.message || e) }; }
      return { before, dispatched: ["visibilitychange", "pagehide"], visibilityState: document.visibilityState };
    });
  } catch (e) { flushInfo = { error: String((e && e.message) || e).slice(0, 200) }; }

  await new Promise((r) => setTimeout(r, CFG.settleMs));
  const fev = await drain(flushPhase + ":settle");
  const fb = await saveBodies(flushPhase, fev);
  console.log(`  FLUSH ${JSON.stringify(flushInfo)} settleEvents=${fev.length} bodies=${fb.ok}/${fb.fail}`);

  await fs.writeFile(path.join(ROOT, `page-${route.name}.json`), JSON.stringify({
    route, gotoErr, landing, candidates, clicks, flushInfo, phases: phases.slice(-CFG.clickBudget - 3),
  }, null, 2), "utf8");
}

// ---- 汇总：requests（不过滤 type，保留 Ping/beacon）----
const requests = [];
const responses = [];
const loading = [];
for (const e of allEvents) {
  const p = e.params || {};
  if (e.method === "Network.requestWillBeSent") {
    const r = p.request || {};
    if (!r.url || !/^https?:\/\//.test(r.url)) continue;
    requests.push({
      phase: e.phase, requestId: p.requestId, url: r.url, method: r.method,
      type: p.type, postData: r.postData ? String(r.postData).slice(0, 20000) : null,
      headers: Object.fromEntries(Object.entries(r.headers || {}).filter(([k]) =>
        /^(content-type|accept|origin|referer|x-requested-with|x-client|x-app|x-version)$/i.test(k))),
    });
  } else if (e.method === "Network.responseReceived") {
    const r = p.response || {};
    if (!r.url || !/^https?:\/\//.test(r.url)) continue;
    responses.push({
      phase: e.phase, requestId: p.requestId, url: r.url, status: r.status,
      mimeType: r.mimeType, type: p.type, encodedDataLength: r.encodedDataLength || 0,
    });
  } else if (e.method === "Network.loadingFinished" || e.method === "Network.loadingFailed") {
    loading.push({ phase: e.phase, method: e.method, requestId: p.requestId, encodedDataLength: p.encodedDataLength, errorText: p.errorText });
  }
}

// relay 命中统计（不看 type，beacon 也算）
const relay = requests.filter((r) => /\/api\/relay\/e(\?|$)/.test(r.url));
const withBody = requests.filter((r) => r.postData);

await fs.writeFile(path.join(ROOT, "network-events.json"), JSON.stringify(allEvents, null, 2), "utf8");
await fs.writeFile(path.join(ROOT, "requests.json"), JSON.stringify(requests, null, 2), "utf8");
await fs.writeFile(path.join(ROOT, "responses.json"), JSON.stringify(responses, null, 2), "utf8");
await fs.writeFile(path.join(ROOT, "loading.json"), JSON.stringify(loading, null, 2), "utf8");
await fs.writeFile(path.join(ROOT, "response-bodies.json"), JSON.stringify(bodies, null, 2), "utf8");
await fs.writeFile(path.join(ROOT, "summary.json"), JSON.stringify({
  generatedAt: new Date().toISOString(),
  spaceName: CFG.spaceName,
  cfg: { routes: CFG.routes.map((r) => r.name), settleMs: CFG.settleMs, clickBudget: CFG.clickBudget },
  events: allEvents.length, requests: requests.length, responses: responses.length,
  requestsWithPostData: withBody.length,
  relayRequests: relay.length,
  relaySample: relay.slice(0, 3).map((r) => ({ phase: r.phase, method: r.method, type: r.type, url: r.url, bodyLen: (r.postData || "").length })),
  responseBodyRecords: bodies.length,
  responseBodiesOk: bodies.filter((b) => b.local_path).length,
  note: "独立增量取证；未覆盖 capture/ 既有全量证据。抓不到即 unknown，不伪造。",
}, null, 2), "utf8");

console.log(`TOTAL events=${allEvents.length} requests=${requests.length} responses=${responses.length} withPostData=${withBody.length}`);
console.log(`RELAY_HITS=${relay.length}`);
console.log("DONE interactive capture");
