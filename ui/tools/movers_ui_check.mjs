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
  // wait for the app to build its nav (poll for the Movers tab) — robust under CPU load
  for (let i = 0; i < 60; i++) {
    const r = await cmd('Runtime.evaluate', { expression: "!!Array.from(document.querySelectorAll('.tabs button')).find(b=>b.textContent.trim()==='Movers')", returnByValue: true });
    if (r.result && r.result.result && r.result.result.value === true) break;
    await sleep(200);
  }
  await sleep(300);

  const evalJson = async (expr) => {
    const r = await cmd('Runtime.evaluate', { expression: `JSON.stringify((function(){${expr}})())`, returnByValue: true, awaitPromise: true });
    if (r.result && r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
    return JSON.parse(r.result.result.value);
  };

  // ---- the in-page acceptance suite ---------------------------------------------------------
  // The SHIPPED production bundle carries the OWNER-AUTHORISED R15-R19 history (ITEM 408 Items 6-7,
  // Option A), bridged to the current accepted release by the owner-approved provenance transition
  // (window.__MATCHDAY_TRANSITION__, from ui/data/movers_transition.js). We (a) prove the shipped bundle
  // BRIDGES + renders under the current app (and fails closed without the transition), then (b) inject a
  // synthetic same-lineage bundle anchored to the LOADED working board to exercise + screenshot the
  // populated view directly (state 'ok', no transition needed since it is chained to the loaded app).
  const res = await evalJson(`
    const out = {};
    const MD = window.MD;
    out.md_present = !!MD && !!MD.movers;
    const navBtns = Array.from(document.querySelectorAll('.tabs button'));
    const moversBtn = navBtns.find(b => b.textContent.trim() === 'Movers');
    out.nav_has_movers = !!moversBtn;
    moversBtn && moversBtn.click();
    out.view_is_movers = MD.state.view === 'movers';
    out.has_masthead = !!document.querySelector('#root .app .mast');

    // (A) SHIPPED bundle is the OWNER-AUTHORISED R15-R19 history, BRIDGED to the current release by the
    // owner-approved provenance transition -> the table renders (not empty, not an alarm); it FAILS
    // CLOSED without the transition.
    const shipped = window.__MATCHDAY_MOVERS__;
    out.shipped_rounds = (shipped && shipped.rounds) || [];
    const _st = (window.__MATCHDAY_WORKING__ || {}).stamp || {};
    const _rel = _st.release || null;
    const shippedApp = {
      board: (_rel && _rel.board) || _st.srcmd5 || _st.board, store: (_rel && _rel.store) || _st.store_md5 || _st.store,
      balanced_board_md5: (_rel && _rel.balanced_board_md5) || _st.balanced_board_md5,
      release_version: (_rel && _rel.release_version) || _st.releaseVersion || _st.tag,
      engine_head: (_rel && _rel.engine_head) || _st.engine, register: (_rel && _rel.register) || _st.register,
      as_of_round: (_rel && _rel.as_of_round != null) ? _rel.as_of_round : _st.asOfRound, release: _rel };
    out.shipped_lineage = MD.movers.core.lineage(shipped, shippedApp, window.__MATCHDAY_TRANSITION__);
    out.shipped_bridged = !!(out.shipped_lineage && out.shipped_lineage.ok && out.shipped_lineage.state === 'bridged');
    out.shipped_table_shown = !!document.querySelector('.movertable');
    out.shipped_not_empty = !document.querySelector('#root .app .moversempty');
    out.shipped_not_alarm = !document.querySelector('#root .app .failclosed');
    out.shipped_failclosed_without_transition = !MD.movers.core.lineage(shipped, shippedApp, null).ok;

    // (B) simulate the post-R19 state: ADD a release contract to the loaded app's stamp (WITHOUT
    // changing srcmd5 — the app's board ring-fence stays intact) and inject a synthetic bundle whose
    // FULL release identity chains to the REAL loaded board. The lineage passes precisely because the
    // latest report board/store == the loaded app's actual board/store.
    function pad(s){ s=String(s); while(s.length<32) s+='0'; return s.slice(0,32); }
    const FIX = { release_version:'v2.11-present-lens-baseline', balanced_board_md5:pad('06d8af60'), engine_head:pad('40f43772'),
      rl_model:pad('a5fd3d7d'), fv:pad('de4c7ec3'), config:pad('c2d233ae'), register:pad('652d83e8') };
    const appBoard = window.__MATCHDAY_WORKING__.stamp.srcmd5;                  // the REAL loaded board (ring-fenced)
    const appStore = window.__MATCHDAY_WORKING__.stamp.store || pad('s19');
    const boards = ['base','r15b','r16b','r17b','r18b'].map(pad); boards.push(appBoard);
    const stores = ['s14','s15','s16','s17','s18'].map(pad); stores.push(appStore);
    function mkRel(rn, board, store){ return Object.assign({}, FIX, {board:board, store:store, as_of_round:rn}); }
    // add the full release contract to the loaded stamp (no srcmd5 change -> board ring-fence intact)
    window.__MATCHDAY_WORKING__.stamp.release = mkRel(19, appBoard, appStore);
    function players(rn){
      const arr=[];
      for(let i=0;i<120;i++){
        const dnp = (i%3===0);
        const dv = dnp ? (i%2? -3 : 2) : (60 - i);
        arr.push({key:'p'+i, name:'Player '+i, affl_team:(i%2?'North Melbourne Kangaroos':'Collingwood Magpies'),
          club:(i%2?'West Coast':'Western Bulldogs'), pos:(i%3===0?'Ruck':(i%2?'Mid':'Def')),
          played:!dnp, dnp:dnp, score: dnp? null : 50+(i%80),
          prev_value:800+i, cur_value:800+i+dv, value_change:dv, value_change_pct: Math.round(dv/(800+i)*1000)/10,
          prev_rank: i+2, cur_rank: i+1, rank_change: 1, prev_pos_rank: 3, cur_pos_rank: 2, pos_rank_change: 1});
      }
      return arr;
    }
    function views(pl){
      const risers = pl.filter(p=>p.value_change>0).sort((a,b)=>b.value_change-a.value_change).map(p=>p.key).slice(0,50);
      const fallers = pl.filter(p=>p.value_change<0).sort((a,b)=>a.value_change-b.value_change).map(p=>p.key).slice(0,50);
      return {value_risers:risers, value_fallers:fallers, rank_risers:pl.map(p=>p.key).slice(0,50), rank_fallers:pl.map(p=>p.key).slice(0,50),
        played_count: pl.filter(p=>p.played).length, dnp_count: pl.filter(p=>p.dnp).length};
    }
    function rep(rn, idx){
      const pl = players(rn);
      return {kind:'weekly_movers_report', submitted_round:rn, previous_round:rn-1,
        board_md5_before:boards[idx], board_md5_after:boards[idx+1],
        source_store_md5_before:stores[idx], source_store_md5_after:stores[idx+1],
        release_identity:mkRel(rn, boards[idx+1], stores[idx+1]), player_count:pl.length,
        integrity:{players_unique:true, coverage_full:true, board_after_matches_committed:true},
        views:views(pl), players:pl};
    }
    const reports={}; const rounds=[15,16,17,18,19];
    rounds.forEach((rn,idx)=>{ reports[String(rn)] = rep(rn, idx); });
    window.__MATCHDAY_MOVERS__ = {kind:'matchday_movers_bundle', rounds:rounds, reports:reports,
      baseline:{as_of_round:14, board:boards[0], store:stores[0], release_identity:mkRel(14, boards[0], stores[0])},
      integrity:{board_chain_ok:true, baseline_anchor_ok:true, overwrite_conflict_last_write:false, rounds:rounds}};
    const appNow = {board:appBoard, store:appStore, release:mkRel(19, appBoard, appStore)};
    out.lineage = MD.movers.core.lineage(window.__MATCHDAY_MOVERS__, appNow);
    MD.state.round = null; MD.state.view='value_risers'; MD.state.club=null; MD.state.pos=null; MD.state.status=null; MD.state.sort=null;
    MD.go('movers');

    out.in_app_shell = !!document.querySelector('#root .app .movertable');
    const activeMovers = Array.from(document.querySelectorAll('.tabs button.on')).some(b => b.textContent.trim()==='Movers');
    out.active_tab_styled = activeMovers;
    const rsel = document.querySelector('.moversbar select');
    out.round_options = rsel ? Array.from(rsel.options).map(o => o.value) : [];
    out.summary_cards = document.querySelectorAll('.movercards .movercard').length;
    out.mover_rows = document.querySelectorAll('.moverrow').length;
    const rep0 = rsel ? window.__MATCHDAY_MOVERS__.reports[rsel.value] : null;
    const wantTop = rep0 ? MD.movers.core.viewRows(rep0, 'value_risers', {})[0].key : null;
    out.default_top_matches_core = !!(document.querySelector('.moverrow') && document.querySelector('.moverrow').getAttribute('data-key') === wantTop);
    out.release_shown = !!Array.from(document.querySelectorAll('.moversmeta .lbl')).find(e=>e.textContent.trim()==='release');
    const allBtn0 = Array.from(document.querySelectorAll('.moversbar .seg button')).find(b => b.textContent.trim() === 'All players');
    allBtn0 && allBtn0.click();
    out.dnp_rows = document.querySelectorAll('.moverrow.dnp').length;
    const risersBtn = Array.from(document.querySelectorAll('.moversbar .seg button')).find(b => b.textContent.trim() === 'Value risers');
    risersBtn && risersBtn.click();
    const dnpBtn = Array.from(document.querySelectorAll('.moversfilters .seg button')).find(b => b.textContent.trim()==='DNP');
    dnpBtn && dnpBtn.click();
    const afterFilter = Array.from(document.querySelectorAll('.moverrow'));
    out.dnp_filter_all_dnp = afterFilter.length > 0 && afterFilter.every(r => r.classList.contains('dnp'));
    const allBtn = Array.from(document.querySelectorAll('.moversfilters .seg button')).find(b => b.textContent.trim()==='All');
    allBtn && allBtn.click();
    const firstRow = document.querySelector('.moverrow');
    const linkedKey = firstRow ? firstRow.getAttribute('data-key') : null;
    firstRow && firstRow.click();
    out.row_links_to_card = !!(firstRow && MD.state.view === 'card' && MD.state.cardKey === linkedKey);
    MD.go('movers');
    const srcs = Array.from(document.scripts).map(s => (s.src||'') + ' ' + (s.textContent||'').slice(0,0));
    out.no_framework = !srcs.some(s => /react|vue|angular|svelte|jquery|preact|ember/i.test(s));
    // fail-closed on malformed movers data (duplicate keys in an otherwise on-lineage report)
    const saved = window.__MATCHDAY_MOVERS__;
    window.__MATCHDAY_MOVERS__ = { kind:'matchday_movers_bundle', rounds:[15], baseline:{board:boards[0], store:stores[0], release_identity:mkRel(14, boards[0], stores[0])}, integrity:{board_chain_ok:true,baseline_anchor_ok:true}, reports:{ '15': { kind:'weekly_movers_report', board_md5_before:boards[0], board_md5_after:appBoard, source_store_md5_before:stores[0], source_store_md5_after:appStore, previous_round:14, submitted_round:15, release_identity:mkRel(15, appBoard, appStore), players:[{key:'a'},{key:'a'}] } } };
    MD.go('movers');
    out.failclosed_on_bad = !!document.querySelector('#root .app .failclosed');
    // fail-closed on an OUT-OF-LINEAGE bundle (the coherent bundle loaded against a DIFFERENT app board)
    window.__MATCHDAY_MOVERS__ = saved;
    MD.movers._state.round = null;
    out.failclosed_out_of_lineage = !MD.movers.core.lineage(saved, {board:pad('WRONGBOARD'), store:appStore, release:mkRel(19, pad('WRONGBOARD'), appStore)}).ok;
    MD.go('movers');
    // Board view still renders (no regression)
    MD.go('board');
    out.board_still_ok = !!document.querySelector('#root .app .rows, #root .app .row');
    MD.go('movers');
    return out;
  `);

  const checks = [
    ['MD.movers present', res.md_present],
    ['Movers is a native nav tab', res.nav_has_movers],
    ['clicking Movers sets the movers view', res.view_is_movers],
    ['SHIPPED production bundle carries the owner-authorised R15-R19 history', Array.isArray(res.shipped_rounds) && res.shipped_rounds.join(',') === '15,16,17,18,19'],
    ['shipped bundle BRIDGES under the owner-approved transition (state=bridged, table renders, not empty/alarm)', res.shipped_bridged && res.shipped_table_shown && res.shipped_not_empty && res.shipped_not_alarm],
    ['shipped bundle FAILS CLOSED without the provenance transition', res.shipped_failclosed_without_transition],
    ['synthetic bundle passes lineage when anchored to the loaded app', res.lineage && res.lineage.ok && res.lineage.state === 'ok'],
    ['Movers renders inside the existing app shell', res.in_app_shell && res.has_masthead],
    ['active nav tab uses existing styling', res.active_tab_styled],
    ['round selector offers R15-R19', JSON.stringify(res.round_options) === JSON.stringify(['15','16','17','18','19'])],
    ['four summary cards render', res.summary_cards === 4],
    ['complete movers table has rows', res.mover_rows > 0],
    ['release identity (derived) shown in the meta strip', res.release_shown],
    ['DNP players are visible', res.dnp_rows > 0],
    ['default order matches deterministic core', res.default_top_matches_core],
    ['DNP filter shows only DNP rows', res.dnp_filter_all_dnp],
    ['row links into the existing player card', res.row_links_to_card],
    ['no new frontend framework introduced', res.no_framework],
    ['malformed movers data fails closed', res.failclosed_on_bad],
    ['out-of-lineage bundle fails closed', res.failclosed_out_of_lineage],
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

  // the honest EMPTY state (what a fresh baseline app renders BEFORE any finalized round, using a
  // SYNTHETIC empty bundle): reset BOTH the loaded app release and the empty bundle baseline to a
  // coherent R14 baseline (as_of_round 14). This exercises the empty-state RENDERING; it does NOT assert
  // the shipped production bundle is empty (it is not — it carries the owner-authorised R15-R19 history).
  await cmd('Runtime.evaluate', { expression:
    "(function(){var pad=function(s){s=String(s);while(s.length<32)s+='0';return s.slice(0,32);};" +
    "var base=pad('baseline'),st=pad('basestore');" +
    "var rel={release_version:'v2.11-rc',balanced_board_md5:pad('06d8af60'),engine_head:pad('40f43772'),rl_model:pad('a5fd3d7d'),fv:pad('de4c7ec3'),config:pad('c2d233ae'),register:pad('652d83e8'),board:base,store:st,as_of_round:14};" +
    "window.__MATCHDAY_WORKING__.stamp.srcmd5=base; window.__MATCHDAY_WORKING__.stamp.release=rel;" +
    "window.__MATCHDAY_MOVERS__={kind:'matchday_movers_bundle',rounds:[],reports:{},baseline:{as_of_round:14,board:base,store:st,release_identity:rel},integrity:{board_chain_ok:true,baseline_anchor_ok:true}};" +
    "window.MD && MD.go && MD.go('movers');})();" });
  await sleep(300);
  await shot(1280, path.join(SHOTS, 'movers_empty.png'), false);

  console.log(rc === 0 ? 'MOVERS UI CHECK: ALL PASS' : 'MOVERS UI CHECK: FAIL');
} catch (e) {
  console.error('movers_ui_check error:', e && e.message || e); rc = 1;
} finally {
  try { ws && ws.close(); } catch {}
  proc.kill('SIGKILL');
  process.exit(rc);
}
