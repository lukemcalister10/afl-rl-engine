/* SMOKE THE STANDALONE BUNDLE — does the single downloadable file actually work?
   The bundler proves every referenced file was inlined. It cannot prove the page RUNS: an app that
   throws on load still bundles perfectly. So this opens the built file over file:// in headless
   Chromium, visits every tab, and fails on a console error, a page exception, an empty view, or a
   missing fact the owner asked for by name.
   Node 22 built-ins only (global WebSocket + fetch), same CDP plumbing as shoot.mjs. Reads only.
   Run:  node ui/tools/standalone_smoke.mjs [path-to-valueboard.html] */
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const FILE = path.resolve(process.argv[2] || 'valueboard.html');
const PORT = 9345;
if (!existsSync(FILE)) { console.error('no such file: ' + FILE); process.exit(1); }

let fails = 0, n = 0;
const ok = (cond, label, extra) => { n++; if (cond) console.log('  [PASS] ' + label);
  else { fails++; console.log('  [FAIL] ' + label + (extra ? '  ' + extra : '')); } };

const proc = spawn(CHROME, ['--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`, '--window-size=1400,2400', 'about:blank'], { stdio: 'ignore' });

let ws;
try {
  let target;
  for (let i = 0; i < 80; i++) {
    try { const j = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
      target = j.find(t => t.type === 'page'); if (target) break; } catch {}
    await sleep(100);
  }
  if (!target) throw new Error('no CDP page target');
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

  let id = 0; const pend = new Map();
  const consoleErrors = [], pageErrors = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); return; }
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error')
      consoleErrors.push((m.params.args || []).map(a => a.value ?? a.description ?? '?').join(' '));
    if (m.method === 'Runtime.exceptionThrown')
      pageErrors.push(m.params.exceptionDetails?.exception?.description
                      || m.params.exceptionDetails?.text || 'exception');
  };
  const cmd = (method, params = {}) => new Promise((res) => {
    const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const evalJs = async (expr) => {
    const r = await cmd('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.result?.exceptionDetails) return { __throw: r.result.exceptionDetails.exception?.description };
    return r.result?.result?.value;
  };

  await cmd('Page.enable'); await cmd('Runtime.enable');
  await cmd('Page.navigate', { url: 'file://' + FILE });
  await sleep(2500);

  console.log('STANDALONE SMOKE — ' + FILE + '\n  ' + '-'.repeat(70));

  /* (1) it loaded at all */
  ok(await evalJs('!!(window.MD && window.MD.state)'), 'the app booted (window.MD is live)');
  ok((await evalJs('document.getElementById("root") && document.getElementById("root").children.length')) > 0,
     'the app rendered into #root');
  ok(await evalJs('!!(window.MD && MD.seam && MD.seam.working && MD.seam.working.players.length > 0)'),
     'the board seam carries players', String(await evalJs('(window.MD&&MD.seam&&MD.seam.working&&MD.seam.working.players.length)||0')));

  /* (2) no network reach — a standalone file that fetches is not standalone */
  ok(await evalJs('performance.getEntriesByType("resource").filter(function(r){return !/^data:/.test(r.name);}).length === 0'),
     'the page fetched NOTHING over the network (no external resource)',
     JSON.stringify(await evalJs('performance.getEntriesByType("resource").map(function(r){return r.name;}).slice(0,3)')));

  /* (3) every tab renders without throwing and puts something on screen */
  const tabs = await evalJs('JSON.stringify(MD.TABS.map(function(t){return t[0];}))');
  for (const view of JSON.parse(tabs || '[]')) {
    const before = pageErrors.length + consoleErrors.length;
    await evalJs(`MD.go(${JSON.stringify(view)});`);
    await sleep(600);
    const chars = await evalJs('(document.getElementById("root")||{}).innerText ? document.getElementById("root").innerText.length : 0');
    // The trade desk is EMPTY until two sides are picked, and an empty desk is the correct render —
    // so it is held to carrying its own furniture, not to a word count that would only be satisfied
    // by putting something on screen that is not there.
    const wants = view === "trade" ? 250 : 400;
    ok(chars > wants && pageErrors.length + consoleErrors.length === before,
       `tab "${view}" renders clean`, `${chars} chars`);
  }

  /* (4) the facts the owner asked for BY NAME — the movers list runs to FW1 and Dean's week is there */
  await evalJs('MD.go("movers");');
  await sleep(600);
  const bundle = 'window.__MATCHDAY_MOVERS__';
  ok(await evalJs(`${bundle}.points.some(function(p){return p.id==="retro-r25" && /Finals Week 1/.test(p.label);})`),
     'the movers list carries FINALS WEEK 1 as its own point');
  ok(await evalJs(`${bundle}.points.filter(function(p){return p.kind==="retro";}).map(function(p){return p.after_round;}).join(",")==="14,15,16,17,18,19,20,21,22,23,24,25"`),
     'the retrospective runs R14 through FW1 with no gap');
  const dean = await evalJs(`(function(){var v=${bundle}.values;for(var k in v){if(/harry-dean/.test(k))return JSON.stringify({r14:v[k].byPoint["retro-r14"].v,r24:v[k].byPoint["retro-r24"].v,fw1:v[k].byPoint["retro-r25"].v});}return null;})()`);
  ok(dean === '{"r14":2660,"r24":2769,"fw1":2992}', 'Harry Dean reads R14 2660 -> R24 2769 -> FW1 2992', String(dean));
  const live = await evalJs('(function(){var p=MD.seam.working.players;for(var i=0;i<p.length;i++)if(p[i].key==="harry-dean")return p[i].v;return null;})()');
  ok(Number(live) === 2992, 'and the LIVE board agrees with the FW1 point', String(live));
  ok(await evalJs(`(${bundle}.reports["25"]||{}).views.played_count===92 && ${bundle}.reports["25"].views.dnp_count===712`),
     'the FW1 weekly report is present: 92 played, 712 DNP');

  /* (5) the default comparison the app opens on is the newest one-round pair, both ends current model */
  const pair = await evalJs('JSON.stringify(MD.movers._state ? {from:MD.movers._state.from,to:MD.movers._state.to} : null)');
  ok(/"to":"retro-r25"/.test(String(pair)), 'the Movers tab OPENS on the pair ending at FW1', String(pair));
  ok(/Finals Week 1/.test(String(await evalJs('document.getElementById("root").innerText'))),
     '…and the rendered tab says "Finals Week 1" on screen');

  /* (6) a player card opens and carries a value history */
  await evalJs('MD.go("card","harry-dean");');
  await sleep(600);
  const cardTxt = await evalJs('document.getElementById("root").innerText');
  ok(/harry dean/i.test(String(cardTxt)), 'the player card opens on Harry Dean');
  ok(/2,?992/.test(String(cardTxt)), '…and shows his current value 2992 on the card');
  ok(/finals week 1/i.test(String(cardTxt)), '…and his card NAMES the week "Finals Week 1", not "Round 25"');
  ok(!/round\s*25/i.test(String(cardTxt)), '…and says "Round 25" nowhere — that round is on no fixture');
  ok(/\b99\b/.test(String(cardTxt)), "…and carries his Finals Week 1 score of 99");

  /* (7) nothing threw anywhere along the way */
  ok(pageErrors.length === 0, 'no uncaught exception on any tab', pageErrors.slice(0, 2).join(' | '));
  ok(consoleErrors.length === 0, 'no console error on any tab', consoleErrors.slice(0, 2).join(' | '));

  console.log('  ' + '-'.repeat(70));
  console.log(fails ? `STANDALONE SMOKE: ${fails} FAIL / ${n}` : `STANDALONE SMOKE: ALL ${n} PASS`);
} finally {
  try { ws && ws.close(); } catch {}
  proc.kill('SIGKILL');
}
process.exit(fails ? 1 : 0);
