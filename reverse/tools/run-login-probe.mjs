/**
 * 登录态只读探测（ego-browser nodejs 模板，配置必须内联）。
 *
 * 由 capture_ctl.py login 生成：把 /*__LOGIN_CFG__*\/ null 替换为
 * {"out":"/abs/evidence/login-probe.json","sites":[{"name":"...","url":"..."}]}
 * 再用 `ego-browser nodejs < runner.mjs` 以 stdin 重定向执行。
 *
 * 纪律：
 *  - 只看不动手：只 goto + 读 innerText，不填表、不点登录、不提交。
 *  - 不继承 shell 环境变量 / cwd：所有路径写绝对路径。
 *  - 域名纠偏：以 page.url() 的真实落点为准，302 到别的域要记下来。
 */
import fs from "node:fs";

const CFG = {"out": "/Users/admin/Desktop/data/fde/marketing/product/arcads/reverse/evidence/login-probe.json", "spaceName": "login-probe", "sites": [{"name": "arcads", "url": "https://app.arcads.ai/dashboard"}]};
const OUT = CFG.out;

async function _task() {
  let t = null;
  try { t = await takeOverTaskSpace(CFG.spaceName || "login-probe"); } catch (e) {}
  if (!t) t = await taskSpace(CFG.spaceName || "login-probe");
  await new Promise((r) => setTimeout(r, 800));
  return t;
}

async function ensurePage(task, label) {
  const list = await task.pages();
  const existing = (list || []).find((p) => p && p.label === label);
  if (existing) return existing;
  for (let i = 0; i < 8; i++) {
    const np = await task.newPage();
    if (np && np.label === label) return np;
  }
  throw new Error(`page ${label} could not be created`);
}

const task = await _task();
const page = await ensurePage(task, "p1");
const results = [];

for (const site of CFG.sites) {
  let gotoError = "";
  try { await page.goto(site.url, { timeout: 60000 }); }
  catch (e) { gotoError = String(e && e.message || e); }
  try {
    await page.waitForFunction(
      () => document.body && document.body.innerText.length > 60,
      undefined, { timeout: 20000 });
  } catch (e) { /* 空壳 SPA 也算 unknown，不伪造 */ }

  const info = await page.evaluate(() => {
    const t = document.body ? document.body.innerText : "";
    return {
      href: location.href,
      title: document.title,
      textLen: t.length,
      needLogin: /登录|注册\/登录|立即登录|Sign in|Log in|Sign up/i.test(t),
      text: t.slice(0, 200).replace(/\n+/g, " | "),
    };
  });
  results.push({
    name: site.name,
    requestedUrl: site.url,
    finalUrl: info.href,
    redirected: new URL(info.href).hostname !== new URL(site.url).hostname,
    needLogin: info.needLogin,
    textLen: info.textLen,
    title: info.title,
    sample: info.text,
    gotoError,
    status: info.needLogin ? "NEED_LOGIN" : (info.textLen > 60 ? "LOGGED_IN_OR_PUBLIC" : "UNKNOWN"),
  });
  console.log(`${site.name}: ${results[results.length - 1].status} ${info.href}`);
}

fs.mkdirSync(OUT.slice(0, OUT.lastIndexOf("/")), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify({
  generatedBy: "probe_login.mjs",
  checkedAt: new Date().toISOString(),
  results,
  note: "needLogin=true 必须停下来让用户登录；不得自行造登录流程或猜验证码",
}, null, 2));
const blocked = results.filter((r) => r.needLogin || r.status === "UNKNOWN");
console.log(`login-probe: ${results.length - blocked.length}/${results.length} ready -> ${OUT}`);
process.exit(blocked.length ? 2 : 0);
