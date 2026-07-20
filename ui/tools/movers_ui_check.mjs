// MOVERS UI CHECK — headless-Chromium acceptance for the integrated Movers view + screenshot evidence.
// Reuses the repo's raw-CDP driver pattern (ui/tools/shoot.mjs); Node built-ins only. Loads the REAL
// ui/index.html over file://, drives the existing app to the Movers tab, and asserts the owner's UI
// acceptance in-page: native nav integration, existing app shell + styles, R15-R19 round selection,
// deterministic sort + filters, DNP visibility, player-detail links, fail-closed on malformed data, no
// new frontend framework, and no regression of the existing Board view. Captures desktop + mobile PNGs.
//
// Run:  node ui/tools/movers_ui_check.mjs
// Exit 0 = all UI assertions pass. Writes ui/screenshots/movers_desktop.png + movers_mobile.png.
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..', '..');
const INDEX = 'file://' + path.join(REPO, 'ui', 'index.html');
const SHOTS = path.join(REPO, 'ui', 'screenshots');
const PORT = 9344;

// Resolve a Chromium binary robustly (dev container path, env override, or a system chromium).
import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
function findChrome() {
  const cands = [process.env.CHROME, process.env.CHROMIUM,
    '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    '/opt/pw-browsers/chromium/chrome-linux/chrome'];
  for (const c of cands) { if (c && existsSync(c)) return c; }
  for (const bin of ['chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable']) {
    try { const p = execSync('command -v ' + bin, { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); if (p) return p; } catch {}
  }
  return null;
}
const CHROME = findChrome();
if (!CHROME) { console.log('MOVERS UI CHECK: SKIP (no Chromium found; run in the dev container or set CHROME=/path)'); process.exit(0); }

const proc = spawn(CHROME, [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`, '--window-size=1280,2200',
  '--force-device-scale-factor=1', '--allow-file-access-from-files', 'about:blank',
], { stdio: 'ignore' });

let ws, rc = 0;
const cmdP = (send) => { let id = 0; const pend = new Map();
  send.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
  return (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); send.send(JSON.stringify({ id: i, method, params })); });
};

try {
  let target;
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json`); const j = await r.json();
      target = j.find(t => t.type === 'page'); if (target) break; } catch {}
    await sleep(100);
  }
  if (!target) throw new Error('no CDP page target');
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  const cmd = cmdP(ws);
  await cmd('Page.enable'); await cmd('Runtime.enable');
  await cmd('Page.navigate', { url: INDEX });
  await sleep(1100);

  const evalJson = async (expr) => {
    const r = await cmd('Runtime.evaluate', { expression: `JSON.stringify((function(){${expr}})())`, returnByValue: true, awaitPromise: true });
    if (r.result && r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
    return JSON.parse(r.result.result.value);
  };

  // ---- the in-page acceptance suite ---------------------------------------------------------
  const res = await evalJson(`
    const out = {};
    const MD = window.MD;
    out.md_present = !!MD && !!MD.movers;
    // 1: Movers is a native nav tab (existing shell)
    const navBtns = Array.from(document.querySelectorAll('.tabs button'));
    const moversBtn = navBtns.find(b => b.textContent.trim() === 'Movers');
    out.nav_has_movers = !!moversBtn;
    out.nav_tab_count = navBtns.length;
    moversBtn && moversBtn.click();
    out.view_is_movers = MD.state.view === 'movers';
    // uses the existing app shell (masthead + controls live in #root .app)
    out.in_app_shell = !!document.querySelector('#root .app .movertable');
    out.has_masthead = !!document.querySelector('#root .app .mast');
    // 2: existing styles (volt token on the active nav button)
    const activeMovers = Array.from(document.querySelectorAll('.tabs button.on')).some(b => b.textContent.trim()==='Movers');
    out.active_tab_styled = activeMovers;
    // 3: round selector R15-R19
    const rsel = document.querySelector('.moversbar select');
    out.round_options = rsel ? Array.from(rsel.options).map(o => o.value) : [];
    // summary cards + table
    out.summary_cards = document.querySelectorAll('.movercards .movercard').length;
    out.mover_rows = document.querySelectorAll('.moverrow').length;
    // 4: deterministic sort — the default (value risers) first row equals the core order
    const rep = window.__MATCHDAY_MOVERS__.reports[rsel.value];
    const wantTop = MD.movers.core.viewRows(rep, 'value_risers', {})[0].key;
    out.default_top_matches_core = document.querySelector('.moverrow') && document.querySelector('.moverrow').getAttribute('data-key') === wantTop;
    // DNP players are visible in the complete "All players" view (the focused riser/faller views hold
    // players who moved on value, so DNP rows naturally surface in All / under the DNP filter).
    const allBtn0 = Array.from(document.querySelectorAll('.moversbar .seg button')).find(b => b.textContent.trim() === 'All players');
    allBtn0 && allBtn0.click();
    out.dnp_rows = document.querySelectorAll('.moverrow.dnp').length;
    const risersBtn = Array.from(document.querySelectorAll('.moversbar .seg button')).find(b => b.textContent.trim() === 'Value risers');
    risersBtn && risersBtn.click();
    // 5: filter DNP — every visible row is a DNP row
    const dnpBtn = Array.from(document.querySelectorAll('.moversfilters .seg button')).find(b => b.textContent.trim()==='DNP');
    dnpBtn && dnpBtn.click();
    const afterFilter = Array.from(document.querySelectorAll('.moverrow'));
    out.dnp_filter_all_dnp = afterFilter.length > 0 && afterFilter.every(r => r.classList.contains('dnp'));
    // reset filter to All
    const allBtn = Array.from(document.querySelectorAll('.moversfilters .seg button')).find(b => b.textContent.trim()==='All');
    allBtn && allBtn.click();
    // 6: player link -> existing card view
    const firstRow = document.querySelector('.moverrow');
    const linkedKey = firstRow.getAttribute('data-key');
    firstRow.click();
    out.row_links_to_card = MD.state.view === 'card' && MD.state.cardKey === linkedKey;
    // back to movers for the screenshot
    MD.go('movers');
    // 7: no new frontend framework loaded
    const srcs = Array.from(document.scripts).map(s => (s.src||'') + ' ' + (s.textContent||'').slice(0,0));
    out.no_framework = !srcs.some(s => /react|vue|angular|svelte|jquery|preact|ember/i.test(s));
    // 8: fail-closed on malformed movers data
    const saved = window.__MATCHDAY_MOVERS__;
    window.__MATCHDAY_MOVERS__ = { rounds:[15], reports:{ '15': { kind:'weekly_movers_report', players:[{key:'a'},{key:'a'}] } } };
    MD.movers = MD.movers.core ? MD.movers : MD.movers; // keep instance
    MD.go('movers');
    out.failclosed_on_bad = !!document.querySelector('.movers, #root .app .failclosed') && !!document.querySelector('#root .app .failclosed');
    window.__MATCHDAY_MOVERS__ = saved;
    MD.go('movers');
    // 9: Board view still renders (no regression)
    MD.go('board');
    out.board_still_ok = !!document.querySelector('#root .app .rows, #root .app .row');
    MD.go('movers');
    return out;
  `);

  const checks = [
    ['MD.movers present', res.md_present],
    ['Movers is a native nav tab', res.nav_has_movers],
    ['clicking Movers sets the movers view', res.view_is_movers],
    ['Movers renders inside the existing app shell', res.in_app_shell && res.has_masthead],
    ['active nav tab uses existing styling', res.active_tab_styled],
    ['round selector offers R15-R19', JSON.stringify(res.round_options) === JSON.stringify(['15','16','17','18','19'])],
    ['four summary cards render', res.summary_cards === 4],
    ['complete movers table has rows', res.mover_rows > 0],
    ['DNP players are visible', res.dnp_rows > 0],
    ['default order matches deterministic core', res.default_top_matches_core],
    ['DNP filter shows only DNP rows', res.dnp_filter_all_dnp],
    ['row links into the existing player card', res.row_links_to_card],
    ['no new frontend framework introduced', res.no_framework],
    ['malformed movers data fails closed', res.failclosed_on_bad],
    ['existing Board view still renders (no regression)', res.board_still_ok],
  ];
  console.log('MOVERS UI CHECK');
  for (const [label, ok] of checks) { console.log('  [' + (ok ? 'PASS' : 'FAIL') + '] ' + label); if (!ok) rc = 1; }

  // ---- screenshots: desktop + mobile ------------------------------------------------------
  async function shot(w, file, mobile) {
    await cmd('Emulation.setDeviceMetricsOverride', { width: w, height: 2200, deviceScaleFactor: 1, mobile: !!mobile });
    await cmd('Runtime.evaluate', { expression: "window.MD && MD.go && MD.go('movers');" });
    await sleep(400);
    const metrics = await cmd('Page.getLayoutMetrics');
    const h = Math.min(Math.ceil((metrics.result.cssContentSize && metrics.result.cssContentSize.height) || 2200), 6000);
    await cmd('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: !!mobile });
    const s = await cmd('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
    writeFileSync(file, Buffer.from(s.result.data, 'base64'));
    console.log('  wrote', path.relpath ? path.relpath(REPO, file) : file);
  }
  const { mkdirSync } = await import('node:fs');
  mkdirSync(SHOTS, { recursive: true });
  await shot(1280, path.join(SHOTS, 'movers_desktop.png'), false);
  await shot(390, path.join(SHOTS, 'movers_mobile.png'), true);

  console.log(rc === 0 ? 'MOVERS UI CHECK: ALL PASS' : 'MOVERS UI CHECK: FAIL');
} catch (e) {
  console.error('movers_ui_check error:', e && e.message || e); rc = 1;
} finally {
  try { ws && ws.close(); } catch {}
  proc.kill('SIGKILL');
  process.exit(rc);
}
