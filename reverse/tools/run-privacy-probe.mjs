/**
 * 只读诊断：确认为何 /api/relay/e 无事件上报（不修改任何 opt-out / 隐私设置）。
 * 运行：ego-browser nodejs < tools/run-privacy-probe.mjs
 */
const fs = await import("node:fs");
const OUT = "/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/capture-interactive/privacy-state.json";

const task = await taskSpace("login-probe");
const page = task.page("p1");
let gotoErr = null;
try { await page.goto("https://app.arcads.ai/onboarding/attribution", { timeout: 60000 }); }
catch (e) { gotoErr = String((e && e.message) || e).slice(0, 200); }
try { await page.waitForLoadState("load", { timeout: 25000 }); } catch (_) {}
await new Promise((r) => setTimeout(r, 6000));

let info = {};
try {
  info = await page.evaluate(() => {
    const out = { href: location.href };
    try { out.doNotTrack = navigator.doNotTrack ?? null; } catch (e) { out.doNotTrack = "err"; }
    try { out.globalPrivacyControl = navigator.globalPrivacyControl ?? null; } catch (e) { out.globalPrivacyControl = "err"; }
    try {
      out.cookieNames = document.cookie.split(";").map((s) => s.trim().split("=")[0]).filter(Boolean);
    } catch (e) { out.cookieNames = ["err"]; }
    try {
      const ls = {};
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        const v = String(localStorage.getItem(k) || "");
        if (/opt|track|consent|privacy|amplitude|amp_|ab_|nonce/i.test(k + " " + v.slice(0, 120))) {
          ls[k] = v.slice(0, 200);
        }
      }
      out.localStorageKeys = Object.keys(localStorage);
      out.localStorageMatches = ls;
    } catch (e) { out.localStorageKeys = ["err"]; }
    try {
      out.amplitudeGlobals = Object.keys(window).filter((k) => /amplitude|ampl|gtm|datalayer/i.test(k)).slice(0, 30);
    } catch (e) { out.amplitudeGlobals = ["err"]; }
    try {
      out.analyticsScripts = Array.from(document.querySelectorAll("script[src]"))
        .map((s) => s.src).filter((u) => /amplitude|relay|analytics/i.test(u)).slice(0, 30);
    } catch (e) { out.analyticsScripts = ["err"]; }
    return out;
  });
} catch (e) { info = { evalErr: String((e && e.message) || e).slice(0, 300) }; }

fs.writeFileSync(OUT, JSON.stringify({
  generatedAt: new Date().toISOString(),
  gotoErr,
  note: "只读诊断；未修改 cookie/localStorage/账号设置。用于解释 /api/relay/e 抓不到事件上报的原因。",
  ...info,
}, null, 2), "utf8");
console.log("PRIVACY_PROBE", JSON.stringify(info).slice(0, 1200));
console.log("DONE " + OUT);
