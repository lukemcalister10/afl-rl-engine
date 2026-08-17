/* DISPLAY SEAT -- headless verification of LOTTERY_DIAL_V2.html (node + a DOM shim, same route S6 took).
 *
 * Loads the page's own <script>, runs it against a minimal DOM, and asserts:
 *   V1  the page's own lambda = 0 == board badge goes green, and the deviation it reports is 0
 *   V2  at lambda = 0 the board total is the printed 666,913 and 0 of 804 rows move rank
 *   V3  every column header sorts, both directions, without throwing, keeping all 804 rows
 *   V4  the NEW measured-ceiling column sorts NUMERICALLY (monotone in the underlying value,
 *       nulls last), as does the new career-value column
 *   V5  nick-madden's row shows the corrected pairing (price / his ceiling as career / measured cell)
 *   V6  no rendered cell anywhere prints NaN, undefined or null -- thin cells print a bound and n
 *   V7  the sixth scenario column is relabelled, and the (r) markers still sit on exactly the rows
 *       whose tapered ceiling prices below scenario five
 *   V8  the dial still moves (lambda = +1.2 / -1.2 reproduce the S6 README totals) and reset returns
 *   V9  the page is self-contained: no external asset reference of any kind
 *
 * Usage: node docs/evidence/order_display_2026-08-17/verify_dial_v2.js
 */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');

const HERE = __dirname;
const FILE = path.join(HERE, 'LOTTERY_DIAL_V2.html');
const html = fs.readFileSync(FILE, 'utf8');

let fails = 0, checks = 0;
function ok(name, cond, detail) {
  checks++;
  if (!cond) { fails++; console.log('  FAIL  ' + name + (detail ? '   ' + detail : '')); }
  else console.log('  ok    ' + name + (detail ? '   ' + detail : ''));
}

/* ------------------------------------------------------------------ DOM shim */
function El(tag) {
  this.tagName = tag; this._cls = new Set(); this.dataset = {}; this._h = []; this.children = [];
  this.value = ''; this._text = ''; this._html = ''; this.attrs = {};
}
El.prototype = {
  get className() { return [...this._cls].join(' '); },
  set className(v) { this._cls = new Set(String(v).split(/\s+/).filter(Boolean)); },
  get classList() {
    const s = this._cls;
    return { add: (...c) => c.forEach(x => s.add(x)), remove: (...c) => c.forEach(x => s.delete(x)),
             toggle: (c, on) => { if (on === undefined) { s.has(c) ? s.delete(c) : s.add(c); } else { on ? s.add(c) : s.delete(c); } },
             contains: c => s.has(c) };
  },
  get textContent() { return this._text; },
  set textContent(v) { this._text = String(v); },
  get innerHTML() { return this._html; },
  set innerHTML(v) { this._html = String(v); },
  addEventListener(ev, fn) { (this._h[ev] = this._h[ev] || []).push(fn); },
  fire(ev, e) { (this._h[ev] || []).forEach(fn => fn.call(this, e || { target: this })); },
  appendChild(c) { this.children.push(c); return c; },
  insertAdjacentHTML(_pos, h) { this._html += h; },
  querySelector() { return null; },          // only used for the .ar arrow, which we do not model
  querySelectorAll() { return []; },
  getAttribute(k) { return this.attrs[k]; },
};

const byId = {};
for (const id of ['vbadge', 'lamv', 'wtxt', 'tot', 'moved', 'riser', 'faller', 'wbars', 'tb',
                  'shown', 'q', 'fpath', 'fpos', 'fmov', 'lam', 'reset', 'foot']) byId[id] = new El('div');

/* the real <th> list, read out of the page so the shim cannot drift from the markup */
const thead = html.slice(html.indexOf('<thead>'), html.indexOf('</thead>'));
const THS = [...thead.matchAll(/<th\b([^>]*)>([\s\S]*?)<\/th>/g)].map(m => {
  const el = new El('th');
  const k = /data-k="([^"]+)"/.exec(m[1]);
  el.dataset.k = k ? k[1] : '';
  el.label = m[2].trim();
  const t = /title="([^"]*)"/.exec(m[1]); el.attrs.title = t ? t[1] : '';
  return el;
});

const document = {
  getElementById: id => byId[id] || (byId[id] = new El('div')),
  querySelectorAll: sel => (sel === '#t th' ? THS : []),
  querySelector: sel => {
    const m = /#t th\[data-k=([^\]]+)\]/.exec(sel);
    if (m) return THS.find(t => t.dataset.k === m[1].replace(/["']/g, '')) || new El('th');
    return new El('div');
  },
  createElement: t => new El(t),
};

/* ------------------------------------------------------------------ run the page's script */
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (scripts.length !== 1) { console.log('EXPECTED exactly one inline <script>, found ' + scripts.length); process.exit(1); }
const src = scripts[0] + `
;globalThis.__T = { ROWS, WQ6, ST, KEY, pricesAt, wts, render, dot,
  get lam(){return lam;}, setLam(v){ lam=v; reprice(); },
  get PX(){return PX;}, get BRANK(){return BRANK;}, get RANK(){return RANK;},
  get sortKey(){return sortKey;}, get sortDir(){return sortDir;},
  IDX: {NAME:0,PATH:1,POS:2,G:3,CAND:4,RHO:5,SP:6,SIX:7,BB:8,RATIO:9,SPAN:10,TSH:11,CV:12,MM:13,FAN:14,INV:15,
        MQ:16,MBND:17,MN:18,MNZ:19,MMED:20,MLAB:21,MNOTE:22} };
`;
const ctx = vm.createContext({ document, console, Math, JSON, Number, String, Array, Set, Object, Infinity, isNaN, parseFloat, parseInt });
try { vm.runInContext(src, ctx, { filename: 'LOTTERY_DIAL_V2.inline.js' }); }
catch (e) { console.log('PAGE SCRIPT THREW ON LOAD: ' + e.stack); process.exit(1); }
const T = ctx.__T, I = T.IDX, ROWS = T.ROWS;
console.log('page script loaded: ' + ROWS.length + ' rows\n');

/* helpers over the rendered table */
function rowsOut() { return byId.tb.innerHTML.split('</tr>').filter(s => s.indexOf('<tr>') >= 0); }
function tds(tr) { return [...tr.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map(m => m[1]); }
function nameOf(tr) { const m = /class="l nm">([^<]*)</.exec(tr); return m ? m[1] : null; }
const nameIdx = new Map(ROWS.map((r, i) => [r[I.NAME], i]));

/* ------------------------------------------------------------------ V1 anchor badge */
console.log('V1  lambda=0 identity badge');
ok('badge is green (class ok)', byId.vbadge.className.indexOf('ok') >= 0, byId.vbadge.className);
ok('badge text asserts the identity', /=0/.test(byId.vbadge.textContent) && /board/.test(byId.vbadge.textContent),
   JSON.stringify(byId.vbadge.textContent));
let worst = 0;
for (const r of ROWS) worst = Math.max(worst, Math.abs(T.dot(T.WQ6, r[I.SP]) - r[I.CAND]));
ok('max |dot(WQ6, scenario prices) - printed price| is float-exact (< 5e-4, the page\'s own bound)',
   worst < 5e-4, 'worst=' + worst.toExponential(3) + ' (~2 ulp, the renormalising multiply)');

/* ------------------------------------------------------------------ V2 board at lambda = 0 */
console.log('\nV2  the board at lambda = 0');
ok('board total reads 666,913', byId.tot.textContent === '666,913', byId.tot.textContent);
ok('0 rows move rank', byId.moved.textContent === '0 of ' + ROWS.length, byId.moved.textContent);
ok('all rows rendered', rowsOut().length === ROWS.length, rowsOut().length + ' rows');
ok('weights are WQ6 (18/18/18/18/18/10)', byId.wtxt.textContent === '18.0% / 18.0% / 18.0% / 18.0% / 18.0% / 10.0%',
   byId.wtxt.textContent);

/* ------------------------------------------------------------------ V3/V4 sorting */
console.log('\nV3  every header sorts, both directions');
const TXT = { nm: 1, pa: 1, po: 1 };
function checkSorted(k, dir) {
  const out = rowsOut();
  if (out.length !== ROWS.length) return 'row count ' + out.length;
  const idx = out.map(nameOf).map(n => nameIdx.get(n));
  if (idx.some(x => x === undefined)) return 'unknown player name in output';
  const kf = T.KEY[k];
  for (let j = 1; j < idx.length; j++) {
    let x = kf(idx[j - 1]), y = kf(idx[j]);
    if (TXT[k]) { if (dir * String(x).localeCompare(String(y)) > 0) return 'text order broken at ' + j; continue; }
    if (x === null || x === undefined) x = -Infinity;
    if (y === null || y === undefined) y = -Infinity;
    if (dir === 1 ? y > x : y < x) return 'numeric order broken at ' + j + ': ' + x + ' then ' + y;
  }
  return null;
}
for (const th of THS) {
  const k = th.dataset.k;
  let bad = null, dirs = [];
  // the page toggles direction when the SAME header is clicked again, so read the direction it
  // actually adopted rather than assuming one -- and require that both directions were exercised
  try {
    th.fire('click'); dirs.push(T.sortDir); bad = checkSorted(k, T.sortDir);
    th.fire('click'); dirs.push(T.sortDir); bad = bad || checkSorted(k, T.sortDir);
  } catch (e) { bad = 'threw: ' + e.message; }
  if (!bad && !(dirs.indexOf(1) >= 0 && dirs.indexOf(-1) >= 0)) bad = 'only one direction exercised';
  ok('sort ' + k.padEnd(6) + ' (' + th.label.replace(/&[a-z]+;/g, '').replace(/<[^>]*>/g, '').trim() + ')', !bad, bad || 'both directions');
  if (T.sortDir !== 1) th.fire('click');   // leave it at dir=+1 for the next header
}

console.log('\nV4  the new columns sort numerically');
for (const k of ['mc', 'cvv']) {
  const th = THS.find(t => t.dataset.k === k);
  th.fire('click');
  const idx = rowsOut().map(nameOf).map(n => nameIdx.get(n));
  const vals = idx.map(i => T.KEY[k](i));
  let mono = true;
  for (let j = 1; j < vals.length; j++) {
    const a = vals[j - 1] === null ? -Infinity : vals[j - 1], b = vals[j] === null ? -Infinity : vals[j];
    if (b > a) { mono = false; break; }
  }
  const top = idx.slice(0, 3).map(i => ROWS[i][I.NAME] + ' ' + Math.round(T.KEY[k](i)));
  ok(k + ' descends numerically over all ' + vals.length + ' rows', mono, 'top: ' + top.join(' | '));
  th.fire('click'); th.fire('click');
  // a string sort would have put "9,..." above "10,..." -- assert the max really is the max
  ok(k + ' top value is the true maximum', Math.abs(Math.max(...ROWS.map((r, i) => T.KEY[k](i) === null ? -Infinity : T.KEY[k](i))) - vals[0]) < 1e-9);
}

/* ------------------------------------------------------------------ V5 madden */
console.log('\nV5  nick-madden shows the corrected pairing');
THS.find(t => t.dataset.k === 'rk').fire('click');   // back to rank order
const mi = nameIdx.get('Nick Madden');
ok('nick-madden is on the board', mi !== undefined);
const mrow = rowsOut().find(tr => nameOf(tr) === 'Nick Madden');
const mt = tds(mrow);
// column layout: 0 # 1 name 2 path 3 pos 4 G 5 rho 6 board 7 price 8 delta 9 rankd 10..15 S1..S6 16 career 17 measured
const price6 = mt[15].replace(/<[^>]*>/g, '').trim();
const career = mt[16].replace(/<[^>]*>/g, '').trim();
const meas = mt[17].replace(/<[^>]*>/g, '').trim();
ok('"price if ceiling lands" cell = 1,388', price6.replace(/\s+/g, '') === '1,388', JSON.stringify(price6));
ok('"his ceiling, career value" cell = 3,883', career === '3,883', JSON.stringify(career));
ok('"measured ceiling" cell carries value + n', /1,543/.test(meas) && /n\s*38/.test(meas), JSON.stringify(meas));
ok('measured cell names his PDA cell in the tooltip', /PDA/.test(mrow) && /post-draft academy/.test(mrow));
ok('the three numbers are distinct (price != career != measured)',
   price6 !== career && career !== meas.split(' ')[0]);
ok('his cell is resolved, so no bound marker', ROWS[mi][I.MBND] === 0 && meas.indexOf('≥') < 0);

/* ------------------------------------------------------------------ V6 no naked nan anywhere */
console.log('\nV6  no NaN / undefined / null printed, on any row, in any sort');
let dirty = [];
for (const th of THS) {
  th.fire('click');
  const body = byId.tb.innerHTML;
  for (const bad of ['NaN', 'undefined', 'null'])
    if (body.indexOf(bad) >= 0) dirty.push(th.dataset.k + ':' + bad);
  th.fire('click');
}
ok('table body is clean under every sort', dirty.length === 0, dirty.join(','));
THS.find(t => t.dataset.k === 'rk').fire('click');
const allRows = rowsOut();
let nBound = 0, nNoCell = 0, nWithN = 0;
for (const tr of allRows) {
  const c = tds(tr)[17];
  if (/≥/.test(c)) nBound++;
  if (/no measured cell/.test(c)) nNoCell++;
  if (/n\s*\d+/.test(c)) nWithN++;
}
ok('every measured cell prints its n', nWithN === allRows.length, nWithN + '/' + allRows.length);
ok('bound cells print the >= marker', nBound === ROWS.filter(r => r[I.MBND] === 1).length,
   nBound + ' bound cells (' + (100 * nBound / allRows.length).toFixed(1) + '% of rows)');
ok('no row is left without a cell', nNoCell === 0, nNoCell + '');

/* ------------------------------------------------------------------ V7 relabel + markers */
console.log('\nV7  the relabel, and the inversion markers');
const th5 = THS.find(t => t.dataset.k === 's5');
ok('sixth scenario header reads "price if ceiling lands"', /price if ceiling lands/i.test(th5.label), th5.label);
ok('header no longer says "q97"', !/q97/i.test(th5.label), th5.label);
ok('its tooltip says it is a price, not a career', /PRICE/.test(th5.attrs.title), th5.attrs.title);
const thc = THS.find(t => t.dataset.k === 'cvv'), thm = THS.find(t => t.dataset.k === 'mc');
ok('career-value header present', /career value/i.test(thc.label), thc.label);
ok('measured header is plain-language', /top 3%/i.test(thm.label), thm.label);
let markRows = 0, markMismatch = 0;
for (const tr of allRows) {
  const i = nameIdx.get(nameOf(tr)), has = /▼/.test(tds(tr)[15]);
  if (has) markRows++;
  if (has !== (ROWS[i][I.INV] === 1)) markMismatch++;
}
ok('markers sit on exactly the tapered-inversion rows', markMismatch === 0 && markRows === ROWS.filter(r => r[I.INV] === 1).length,
   markRows + ' marked, ' + markMismatch + ' mismatches');
ok('that count is the emit\'s 341', markRows === 341, markRows + '');

/* ------------------------------------------------------------------ V8 the dial still works */
console.log('\nV8  the dial still moves, and reset returns to the board');
T.setLam(1.2);
const totUp = byId.tot.textContent, movedUp = byId.moved.textContent;
ok('lambda=+1.2 total is the S6 README\'s 947,934', totUp === '947,934', totUp);
T.setLam(-1.2);
ok('lambda=-1.2 total is the S6 README\'s 458,634', byId.tot.textContent === '458,634', byId.tot.textContent);
byId.reset.fire('click');
ok('reset returns the board total exactly', byId.tot.textContent === '666,913', byId.tot.textContent);
ok('reset returns 0 rank moves', byId.moved.textContent === '0 of ' + ROWS.length, byId.moved.textContent);
ok('the dial actually moved rows at +1.2', /of 804/.test(movedUp) && parseInt(movedUp) > 0, movedUp);

/* filters still work */
byId.q.value = 'madden'; T.render();
ok('name filter works', rowsOut().length === 1 && nameOf(rowsOut()[0]) === 'Nick Madden');
byId.q.value = ''; byId.fpath.value = 'PDA'; T.render();
ok('pathway filter works', rowsOut().length === ROWS.filter(r => r[I.PATH] === 'PDA').length, rowsOut().length + ' PDA rows');
byId.fpath.value = ''; T.render();
ok('filters clear back to all rows', rowsOut().length === ROWS.length);

/* ------------------------------------------------------------------ V9 self-contained */
console.log('\nV9  self-contained');
const ext = [...html.matchAll(/(?:src|href)\s*=\s*"([^"]*)"/g)].map(m => m[1])
  .filter(u => !/^#/.test(u));
ok('no external src/href', ext.length === 0, ext.join(','));
ok('no url() asset reference', !/url\(/.test(html));
ok('no fetch / XHR / import', !/\bfetch\(|XMLHttpRequest|importScripts|import\s*\(/.test(html));

console.log('\n' + (fails ? 'FAILED ' + fails + ' of ' + checks : 'ALL ' + checks + ' CHECKS PASSED'));
process.exit(fails ? 1 : 0);
