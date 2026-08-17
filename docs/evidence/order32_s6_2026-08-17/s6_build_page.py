#!/usr/bin/env python3
"""ORDER 32 SEAT S6 -- build the owner page from S6_FAN_EMIT.json.  READ-ONLY, no engine import.

Emits a single self-contained HTML file: docs/evidence/order32_s6_2026-08-17/S6_LOTTERY_DIAL.html

THE PAGE'S MATH, in full, because the page is a pricing display and nothing about it should be implicit.

  Per row the emit carries six SCENARIO PRICES

      sp[i] = anchor_pts + rho * six_phat[i]                        i = 0..5

  where six_phat[i] = m * SCALE_DIST * v_at_peak(p, b6[i], 'bal') is the engine's own per-scenario
  career value expressed in Phat units (m = Phat/price6, the single disclosed downstream scalar), rho is
  the law's production share and anchor_pts = printed_price - rho * dot(WQ6, six_phat) is the row's
  pedigree-side constant.  sp[i] reads as "what this player is worth on the board IF scenario i is the
  one that lands".  Because the weights sum to 1,

      dot(WQ6, sp) == printed board price      EXACTLY, on all 804 rows (asserted in the page, in JS)

  -- the printed price IS the fixed-weight average of the six scenario prices.  The dial then reads

      W_i(lambda) proportional to WQ6_i * exp(lambda * i),  renormalised to sum 1
      price(lambda) = dot(W(lambda), sp)

  lambda = 0 gives W == WQ6 and therefore the printed board price, exactly.  lambda > 0 tilts weight up
  the fan toward the ceiling scenario; lambda < 0 tilts it down toward the floor.  Ranks recompute live.

WHAT THE DIAL IS NOT.  It does not move the sealed pricing law, any no-arb instrument, or the board.
WQ6 in the engine stays [0.18 x5, 0.10] normalised.  This is a lens over an emit.
"""
import os, json, math, hashlib, time, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
EMIT = json.load(open(os.path.join(HERE, 'S6_FAN_EMIT.json')))
R = EMIT['rows']; WQ6 = EMIT['law']['WQ6']; V = EMIT['validation']; ID = EMIT['identity']
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

def dot(w, x): return sum(a * b for a, b in zip(w, x))

PAGE = []
for r in R:
    rho, anc, sixp = r['rho'], r['anchor_pts'], r['six_phat']
    sp = [anc + rho * x for x in sixp]
    d = abs(dot(WQ6, sp) - r['cand'])
    assert d < 1e-6, ('scenario prices do not average to the printed price', r['key'], d)
    six = r['six_raw']
    PAGE.append([
        r['name'], r['pathway'] or '?', r['pos'] or '?', int(r['games'] or 0), int(r['cand']),
        round(rho, 6),
        sp,                                        # scenario prices, board points (FULL precision:
                                                   # the lambda=0 identity is asserted in the page)
        [round(x, 1) for x in six],                # the raw per-scenario career values
        [round(x, 2) for x in r['b6']],            # the six band levels
        (round(r['spread_ratio_6_1'], 3) if r['spread_ratio_6_1'] is not None else None),
        (round(r['spread_span_over_med'], 3) if r['spread_span_over_med'] is not None else None),
        (round(100 * r['top_scenario_share_of_Phat'], 2) if r['top_scenario_share_of_Phat'] is not None else None),
        (round(100 * r['weighted_cv'], 2) if r['weighted_cv'] is not None else None),
        round(r['m_downstream'], 6),
        1 if r['fan_carries_price'] else 0,
        1 if r['q97_below_band5'] else 0,
    ])

TOT = sum(int(r['cand']) for r in R)
N_LOWRHO = sum(1 for r in R if r['rho'] < 0.3)
N_NOFAN = V['n_rows_fan_cannot_carry_price']
ratios = sorted(r['spread_ratio_6_1'] for r in R if r['rho'] >= 0.3 and r['spread_ratio_6_1'])
STATS = {'n': len(R), 'total': TOT, 'lowrho': N_LOWRHO, 'nofan': N_NOFAN,
         'flat': V['n_fan_flat'], 'inv': V['n_q97_below_band5'],
         'med_ratio': round(statistics.median(ratios), 3), 'n_ratio': len(ratios)}

DATA = json.dumps({'wq6': WQ6, 'rows': PAGE, 'stats': STATS}, separators=(',', ':'))

HTML = """<!doctype html>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Lottery Dial &middot; ORDER 32 &middot; S6</title>
<style>
:root{
  --pitch:#0a0c10; --card:#12151c; --card-2:#181c25; --card-3:#1e2431; --edge:#232936; --edge-2:#2f3747;
  --text:#f2f5f9; --dim:#8b95a6; --faint:#525c6d; --ghost:#39414f;
  --volt:#c8f04a; --volt-soft:rgba(200,240,74,.12);
  --up:#4ade80; --dn:#f0655e; --warn:#f5b445; --warn-soft:rgba(245,180,69,.10);
  --cond:"Arial Narrow","Helvetica Neue Condensed","Roboto Condensed",Arial,sans-serif;
  --sans:"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--pitch);color:var(--text);font-family:var(--sans);font-size:13px;line-height:1.45}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
.banner{background:var(--volt-soft);border-bottom:1px solid var(--volt);color:var(--volt);
  font-family:var(--cond);font-size:11px;letter-spacing:.2em;text-transform:uppercase;text-align:center;
  padding:7px 12px;font-weight:700}
.app{max-width:1500px;margin:0 auto;padding:0 18px 80px}
header{display:flex;align-items:flex-end;gap:18px;flex-wrap:wrap;padding:22px 0 14px}
.brand{font-family:var(--cond);font-weight:900;font-size:38px;letter-spacing:.01em;text-transform:uppercase;line-height:.92}
.brand b{color:var(--volt)}
.brand .sub{display:block;font-size:10.5px;letter-spacing:.28em;color:var(--dim);font-weight:700;margin-top:6px}
.spacer{flex:1}
.stamp{font-family:var(--mono);font-size:10.5px;color:var(--dim);text-align:right;line-height:1.75}
.stamp b{color:var(--text)}
.badge{display:inline-block;font-family:var(--cond);font-weight:700;font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;padding:2px 8px;border:1px solid var(--volt);color:var(--volt);margin-left:6px}
.badge.ok{border-color:var(--up);color:var(--up)}
.badge.bad{border-color:var(--dn);color:var(--dn)}
h2{font-family:var(--cond);font-weight:700;font-size:11px;letter-spacing:.24em;text-transform:uppercase;
  color:var(--faint);margin:0 0 10px}
.box{background:var(--card);border:1px solid var(--edge);padding:16px 18px;margin:12px 0}
.box.warn{border-color:var(--warn);border-left:4px solid var(--warn);background:var(--warn-soft)}
.box.warn h2{color:var(--warn)}
.box.warn b{color:var(--warn)}
.defs{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:10px 26px}
.defs div{border-left:2px solid var(--edge-2);padding-left:11px}
.defs .t{font-family:var(--cond);font-weight:700;font-size:12px;letter-spacing:.11em;text-transform:uppercase;color:var(--volt)}
.defs .d{color:var(--dim);font-size:12px;margin-top:2px}
code{font-family:var(--mono);font-size:11.5px;color:var(--text);background:var(--card-3);padding:1px 5px}
/* ---- the dial ---- */
.dial{background:var(--card);border:1px solid var(--edge);border-left:4px solid var(--volt);padding:16px 18px;margin:14px 0}
.dialtop{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.lam{font-family:var(--cond);font-weight:900;font-size:44px;line-height:.9;color:var(--volt);min-width:120px}
.lam small{display:block;font-size:10px;letter-spacing:.24em;color:var(--faint);font-weight:700;margin-top:5px}
input[type=range]{-webkit-appearance:none;appearance:none;flex:1;min-width:280px;height:4px;background:var(--edge-2);outline:none;border-radius:2px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:26px;background:var(--volt);cursor:pointer;border-radius:2px}
input[type=range]::-moz-range-thumb{width:20px;height:26px;background:var(--volt);cursor:pointer;border:0;border-radius:2px}
.btn{font-family:var(--cond);font-weight:700;font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  background:transparent;color:var(--dim);border:1px solid var(--edge-2);padding:7px 13px;cursor:pointer}
.btn:hover{color:var(--volt);border-color:var(--volt)}
.btn.on{background:var(--volt);color:#0a0c10;border-color:var(--volt)}
.wbars{display:flex;gap:5px;align-items:flex-end;height:62px;margin-top:16px}
.wb{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:4px}
.wb i{display:block;width:100%;background:var(--volt);opacity:.75;min-height:1px}
.wb i.q97{background:var(--warn)}
.wb span{font-family:var(--mono);font-size:9.5px;color:var(--faint);white-space:nowrap}
.dialmeta{display:flex;gap:26px;flex-wrap:wrap;margin-top:14px;font-family:var(--mono);font-size:11.5px;color:var(--dim)}
.dialmeta b{color:var(--text)}
.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:14px 0 8px}
input[type=search]{background:var(--card);border:1px solid var(--edge-2);color:var(--text);
  font-family:var(--mono);font-size:12px;padding:7px 11px;outline:none;min-width:210px}
input[type=search]:focus{border-color:var(--volt)}
select{background:var(--card);border:1px solid var(--edge-2);color:var(--text);font-family:var(--mono);font-size:12px;padding:7px 9px;outline:none}
/* ---- table ---- */
.tw{overflow-x:auto;border:1px solid var(--edge);background:var(--card)}
table{border-collapse:collapse;width:100%;min-width:1320px}
th{position:sticky;top:0;z-index:2;background:var(--card-2);border-bottom:1px solid var(--edge-2);
  font-family:var(--cond);font-weight:700;font-size:10px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--dim);padding:9px 8px;text-align:right;cursor:pointer;user-select:none;white-space:nowrap}
th:hover{color:var(--volt)}
th.l{text-align:left}
th.on{color:var(--volt);background:var(--card-3)}
th .ar{opacity:.5;font-size:9px}
td{padding:5px 8px;text-align:right;border-bottom:1px solid rgba(35,41,54,.55);white-space:nowrap;
  font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:12px}
td.l{text-align:left}
tbody tr:hover{background:var(--card-2)}
.rk{color:var(--faint);font-weight:700}
.nm{font-family:var(--cond);font-weight:700;font-size:14.5px;letter-spacing:.02em;text-transform:uppercase}
.tag{font-family:var(--cond);font-weight:700;font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--faint);border:1px solid var(--edge-2);padding:1px 6px}
.px{font-weight:700;font-size:13px}
.sc{color:var(--dim)}
.sc.hi{color:var(--warn)}
.grey{color:var(--ghost)!important}
.up{color:var(--up)} .dn{color:var(--dn)} .zero{color:var(--faint)}
.mv{font-size:11px}
.sep{border-left:1px solid var(--edge-2)}
footer{margin-top:22px;color:var(--faint);font-size:11px;font-family:var(--mono);line-height:1.9}
</style>

<div class="banner">Order 32 &middot; Seat S6 &middot; display prototype &mdash; the sealed pricing law is UNCHANGED. &lambda; is a lens over an emit, not a re-price.</div>

<div class="app">
<header>
  <div class="brand">Lottery<b>Dial</b><span class="sub">the six-scenario fan behind one printed price</span></div>
  <div class="spacer"></div>
  <div class="stamp">
    board <b>fe6be9d6</b> &middot; store <b>cb38ef11</b> &middot; engine <b>14000af2</b> &middot; pvc <b>78ad9842</b><span class="badge">RL_O31</span><span class="badge" id="vbadge">checking</span><br>
    __N__ active rows &middot; board total <b>__TOT__</b> pts &middot; candidate build (ORDER 31-F, tag f2on) &middot; emitted __WHEN__
  </div>
</header>

<div class="box warn">
  <h2>Read this before you move the dial</h2>
  <p style="margin:0 0 9px"><b>The fan covers the PRODUCTION leg only.</b> Under the one law a price is
  <code>rho(g) &times; P&#770; + [D(c_u)(1&minus;rho) + &Phi;&beta;rho] &times; v0</code>. The six scenarios live entirely inside
  <code>P&#770;</code>. The <b>v0 (pedigree) leg has its own variance and it is not in this emit</b> &mdash; seat S7 is
  designing it.</p>
  <p style="margin:0 0 9px">So a player with few games shows a <b>misleadingly small spread</b>: most of his price is
  pedigree, and pedigree's fan does not exist yet. A narrow bar on such a row means <b>&ldquo;not measured&rdquo;</b>, never
  &ldquo;safe&rdquo;. Every row with <code>rho &lt; 0.3</code> has its spread cells <b>greyed out</b> for exactly that reason
  (__LOWRHO__ of __N__ rows). On __NOFAN__ of those the production leg is zero outright &mdash; the dial cannot move them at all.</p>
  <p style="margin:0 0 9px">Three more honesties. (1) The lens holds each row's realised <b>downstream production
  factor</b> <code>m</code> fixed across scenarios; some of the layers inside <code>m</code> are not linear in the fan, so
  this is a first-order reading, not an engine re-run at a different weight vector. (2) __FLAT__ rows &mdash;
  overwhelmingly established veterans &mdash; have a <b>perfectly flat fan</b>: their remaining career prices the same at
  every band level, so the dial does nothing to them. That is a real property of the production model, not a bug in this
  page.</p>
  <p style="margin:0">(3) <b>The ceiling is not always the top scenario.</b> S6 is the frozen q97 ceiling, but the v7
  age-taper pulls it back toward the band median &mdash; so on <b>__INV__ of __N__ rows</b> S6 prices <i>below</i> S5.
  Those rows are marked <span style="color:var(--warn)">&#9660;</span> in the S6 column, and on them pushing &lambda;
  positive is <b>not</b> the same as betting on the best case: past a point it walks the price back down. Read the six
  numbers, not the dial's direction.</p>
</div>

<div class="box">
  <h2>What the columns mean</h2>
  <div class="defs">
    <div><div class="t">The six scenarios</div><div class="d">The engine never prices a player at one projected level.
      <code>b6</code> builds six of them &mdash; five conditional-prior band quantiles plus a frozen ceiling (<b>q97</b>) as
      the sixth &mdash; and the board price is a fixed-weight average across all six.</div></div>
    <div><div class="t">S1 &hellip; S6</div><div class="d">What this player would be worth <b>on the board</b> if that
      scenario were the one that lands. S1 = the floor band, S6 = the frozen ceiling. The printed price is exactly the
      weighted average of these six numbers.</div></div>
    <div><div class="t">Board price</div><div class="d">The candidate build's printed price, unchanged. At
      <b>&lambda; = 0</b> the Price column reproduces it to the point &mdash; asserted in this page on load.</div></div>
    <div><div class="t">rho (&rho;)</div><div class="d">How much of the price the <b>production</b> estimate carries.
      &rho; near 1 = a career's worth of evidence. &rho; near 0 = the price is nearly all pedigree, and the fan is
      nearly irrelevant.</div></div>
    <div><div class="t">S6/S1</div><div class="d">Ceiling scenario divided by floor scenario &mdash; how many times more
      the top outcome is worth than the bottom one. <b>1.00 = a flat fan</b> (no measured production variance).</div></div>
    <div><div class="t">Span</div><div class="d"><code>(S6&minus;S1)/S3</code>: the width of the fan measured in
      median-scenario units. Unstable when the median scenario is near zero &mdash; read it beside S6/S1, not instead of it.</div></div>
    <div><div class="t">Top %</div><div class="d">The share of the production estimate that sits in the single top
      scenario. A high number means the price is being carried by the ceiling.</div></div>
    <div><div class="t">CV %</div><div class="d">Weighted spread of the six career values around their own average
      &mdash; one number for &ldquo;how wide is this fan&rdquo;, comparable across players.</div></div>
    <div><div class="t">The dial (&lambda;)</div><div class="d">Weights become <code>WQ6_i &times; e^(&lambda;i)</code>,
      renormalised. <b>&lambda;&nbsp;=&nbsp;0 is the board, exactly.</b> Push right and the ceiling scenarios take the
      weight (the optimist's board); pull left and the floor scenarios do (the pessimist's). Ranks re-sort live.</div></div>
    <div><div class="t">&Delta; and Rank move</div><div class="d">Change in points and in rank against the printed board
      at &lambda;&nbsp;=&nbsp;0. This is where the dial earns its keep: <b>who overtakes whom</b> when you decide how much
      you believe the ceiling.</div></div>
  </div>
</div>

<div class="dial">
  <div class="dialtop">
    <div class="lam" id="lamv">0.00<small>&lambda; &middot; convexity</small></div>
    <input type="range" id="lam" min="-1.2" max="1.2" step="0.01" value="0">
    <button class="btn" id="reset">reset to board</button>
  </div>
  <div class="wbars" id="wbars"></div>
  <div class="dialmeta">
    <span>weights <b id="wtxt"></b></span>
    <span>board total <b id="tot"></b> pts</span>
    <span>rows that moved rank <b id="moved"></b></span>
    <span>biggest riser <b id="riser"></b></span>
    <span>biggest faller <b id="faller"></b></span>
  </div>
</div>

<div class="tools">
  <input type="search" id="q" placeholder="filter by player name&hellip;">
  <select id="fpath"><option value="">all pathways</option></select>
  <select id="fpos"><option value="">all positions</option></select>
  <button class="btn" id="fmov">only rows the dial moves</button>
  <span class="num" style="color:var(--faint)" id="shown"></span>
</div>

<div class="tw"><table id="t">
<thead><tr>
  <th class="l" data-k="rk">#</th>
  <th class="l" data-k="nm">Player</th>
  <th class="l" data-k="pa">Path</th>
  <th class="l" data-k="po">Pos</th>
  <th data-k="g">G</th>
  <th data-k="rho">&rho;</th>
  <th class="sep" data-k="cand">Board</th>
  <th data-k="px">Price(&lambda;)</th>
  <th data-k="d">&Delta;</th>
  <th data-k="rm">Rank &Delta;</th>
  <th class="sep" data-k="s0">S1 floor</th>
  <th data-k="s1">S2</th>
  <th data-k="s2">S3</th>
  <th data-k="s3">S4</th>
  <th data-k="s4">S5</th>
  <th data-k="s5">S6 q97</th>
  <th class="sep" data-k="ratio">S6/S1</th>
  <th data-k="span">Span</th>
  <th data-k="tsh">Top %</th>
  <th data-k="cv">CV %</th>
</tr></thead>
<tbody id="tb"></tbody>
</table></div>

<footer id="foot"></footer>
</div>

<script>
const D = __DATA__;
const WQ6 = D.wq6, ROWS = D.rows, ST = D.stats;
// row layout: 0 name 1 path 2 pos 3 games 4 cand 5 rho 6 sp[6] 7 six_raw[6] 8 b6[6]
//             9 ratio 10 span 11 top% 12 cv% 13 m 14 fanCarries 15 q97BelowBand5
const NAME=0,PATH=1,POS=2,G=3,CAND=4,RHO=5,SP=6,SIX=7,BB=8,RATIO=9,SPAN=10,TSH=11,CV=12,MM=13,FAN=14,INV=15;

const dot=(w,x)=>{let s=0;for(let i=0;i<w.length;i++)s+=w[i]*x[i];return s;};
function wts(lam){const w=WQ6.map((v,i)=>v*Math.exp(lam*i)),s=w.reduce((a,b)=>a+b,0);return w.map(v=>v/s);}

// ---- ASSERT THE ANCHOR: at lambda = 0 every row must reproduce its printed board price ----
let worst=0, worstKey='';
for(const r of ROWS){const d=Math.abs(dot(WQ6,r[SP])-r[CAND]); if(d>worst){worst=d;worstKey=r[NAME];}}
const OK = worst < 5e-4;
{const b=document.getElementById('vbadge');
 b.className = 'badge ' + (OK?'ok':'bad');
 b.textContent = OK ? ('\\u03bb=0 \\u2261 board (max dev '+worst.toExponential(1)+')')
                    : ('ANCHOR FAILED '+worst.toFixed(4)+' @ '+worstKey);}

function pricesAt(l){const w=wts(l);return ROWS.map(r=>dot(w,r[SP]));}
function ranksOf(px){
  const ord=px.map((v,i)=>({i,v})).sort((a,b)=>b.v-a.v||a.i-b.i);
  const R=new Array(px.length); ord.forEach((o,n)=>R[o.i]=n+1); return R;
}
// The BASELINE ranks come from pricesAt(0), NOT from the printed integers. 153 rows share a printed
// price, and integer ties break differently from float ties -- baselining on the printed integers would
// report phantom rank moves at lambda = 0. pricesAt(0) IS the printed board (asserted above), so this
// baseline is the board's, and "rows that moved rank" reads 0 of 804 at lambda = 0 by construction.
const BRANK=ranksOf(pricesAt(0));

let lam=0, PX=pricesAt(0), RANK=BRANK.slice();
let sortKey='rk', sortDir=1, movedOnly=false;

function reprice(){
  const w=wts(lam);
  PX=pricesAt(lam);
  RANK=ranksOf(PX);
  // dial readout
  document.getElementById('lamv').innerHTML=(lam>0?'+':'')+lam.toFixed(2)+'<small>\\u03bb \\u00b7 convexity</small>';
  document.getElementById('wtxt').textContent=w.map(x=>(100*x).toFixed(1)+'%').join(' / ');
  document.getElementById('tot').textContent=Math.round(PX.reduce((a,b)=>a+b,0)).toLocaleString();
  let mv=0,bu=null,bd=null;
  for(let i=0;i<ROWS.length;i++){const d=BRANK[i]-RANK[i]; if(d!==0)mv++;
    if(!bu||d>bu.d)bu={d,i}; if(!bd||d<bd.d)bd={d,i};}
  document.getElementById('moved').textContent=mv+' of '+ROWS.length;
  document.getElementById('riser').textContent = bu&&bu.d>0 ? ROWS[bu.i][NAME]+' +'+bu.d : '\\u2014';
  document.getElementById('faller').textContent = bd&&bd.d<0 ? ROWS[bd.i][NAME]+' '+bd.d : '\\u2014';
  const mx=Math.max(...w);
  document.getElementById('wbars').innerHTML=w.map((x,i)=>
    '<div class="wb"><i class="'+(i===5?'q97':'')+'" style="height:'+(100*x/mx*0.72+2)+'%"></i>'+
    '<span>'+(i===5?'q97':'S'+(i+1))+'</span><span>'+(100*x).toFixed(0)+'%</span></div>').join('');
  render();
}

// numeric sorts run high-to-low at dir=+1; rank is negated so its default reads 1, 2, 3...
const KEY={rk:i=>-RANK[i], nm:i=>ROWS[i][NAME], pa:i=>ROWS[i][PATH], po:i=>ROWS[i][POS],
  g:i=>ROWS[i][G], rho:i=>ROWS[i][RHO], cand:i=>ROWS[i][CAND], px:i=>PX[i],
  d:i=>PX[i]-ROWS[i][CAND], rm:i=>BRANK[i]-RANK[i],
  s0:i=>ROWS[i][SP][0], s1:i=>ROWS[i][SP][1], s2:i=>ROWS[i][SP][2],
  s3:i=>ROWS[i][SP][3], s4:i=>ROWS[i][SP][4], s5:i=>ROWS[i][SP][5],
  ratio:i=>ROWS[i][RATIO], span:i=>ROWS[i][SPAN], tsh:i=>ROWS[i][TSH], cv:i=>ROWS[i][CV]};
const TXTK={nm:1,pa:1,po:1};

function fmt(x){return x===null||x===undefined?'\\u2014':Math.round(x).toLocaleString();}
function f2(x,n){return x===null||x===undefined?'\\u2014':x.toFixed(n);}

function render(){
  const q=document.getElementById('q').value.trim().toLowerCase();
  const fp=document.getElementById('fpath').value, fo=document.getElementById('fpos').value;
  let idx=[];
  for(let i=0;i<ROWS.length;i++){
    const r=ROWS[i];
    if(q && r[NAME].toLowerCase().indexOf(q)<0) continue;
    if(fp && r[PATH]!==fp) continue;
    if(fo && r[POS]!==fo) continue;
    if(movedOnly && Math.abs(PX[i]-r[CAND])<0.5) continue;
    idx.push(i);
  }
  const kf=KEY[sortKey], txt=!!TXTK[sortKey];
  idx.sort((a,b)=>{
    let x=kf(a),y=kf(b);
    if(txt) return sortDir*String(x).localeCompare(String(y));
    if(x===null||x===undefined)x=-Infinity; if(y===null||y===undefined)y=-Infinity;
    return sortDir*(y-x) || a-b;   // numeric: dir=1 means high-to-low
  });
  const out=[];
  for(const i of idx){
    const r=ROWS[i], px=PX[i], d=px-r[CAND], rm=BRANK[i]-RANK[i];
    const grey = r[RHO]<0.3 ? ' grey' : '';
    const dc = Math.abs(d)<0.5?'zero':(d>0?'up':'dn');
    const sixmax = Math.max.apply(null, r[SP]);
    let tds='';
    for(let k=0;k<6;k++){
      const hot = (r[SP][k]>=sixmax && sixmax>r[SP][0]) ? ' hi' : '';
      const mark = (k===5 && r[INV]) ? ' <span title="the q97 ceiling prices BELOW band 5 -- the v7 age-taper pulled it back" style="color:var(--warn)">\\u25bc</span>' : '';
      tds+='<td class="sc'+hot+grey+(k===0?' sep':'')+'">'+fmt(r[SP][k])+mark+'</td>';
    }
    out.push('<tr>'
      +'<td class="l rk">'+RANK[i]+'</td>'
      +'<td class="l nm">'+r[NAME]+'</td>'
      +'<td class="l"><span class="tag">'+r[PATH]+'</span></td>'
      +'<td class="l"><span class="tag">'+r[POS]+'</span></td>'
      +'<td>'+r[G]+'</td>'
      +'<td'+grey+'>'+f2(r[RHO],3)+'</td>'
      +'<td class="sep">'+fmt(r[CAND])+'</td>'
      +'<td class="px">'+fmt(px)+'</td>'
      +'<td class="'+dc+'">'+(Math.abs(d)<0.5?'\\u2013':(d>0?'+':'')+Math.round(d))+'</td>'
      +'<td class="mv '+(rm>0?'up':rm<0?'dn':'zero')+'">'+(rm===0?'\\u2013':(rm>0?'+':'')+rm)+'</td>'
      +tds
      +'<td class="sep'+grey+'">'+(r[RATIO]===null?'\\u2014':(r[RATIO]>=1000?Math.round(r[RATIO]).toLocaleString():f2(r[RATIO],2)))+'</td>'
      +'<td class="'+grey.trim()+'">'+(r[SPAN]===null?'\\u2014':f2(r[SPAN],2))+'</td>'
      +'<td class="'+grey.trim()+'">'+f2(r[TSH],1)+'</td>'
      +'<td class="'+grey.trim()+'">'+f2(r[CV],1)+'</td>'
      +'</tr>');
  }
  document.getElementById('tb').innerHTML=out.join('');
  document.getElementById('shown').textContent=idx.length+' of '+ROWS.length+' rows shown';
}

// header sorting
document.querySelectorAll('#t th').forEach(th=>{
  th.addEventListener('click',()=>{
    const k=th.dataset.k;
    if(sortKey===k) sortDir=-sortDir; else {sortKey=k; sortDir=1;}
    document.querySelectorAll('#t th').forEach(x=>{x.classList.remove('on');
      x.querySelector('.ar')&&x.querySelector('.ar').remove();});
    th.classList.add('on');
    th.insertAdjacentHTML('beforeend',' <span class="ar">'+(sortDir>0?'\\u25bc':'\\u25b2')+'</span>');
    render();
  });
});

document.getElementById('lam').addEventListener('input',e=>{lam=parseFloat(e.target.value);reprice();});
document.getElementById('reset').addEventListener('click',()=>{lam=0;document.getElementById('lam').value=0;reprice();});
document.getElementById('q').addEventListener('input',render);
document.getElementById('fpath').addEventListener('change',render);
document.getElementById('fpos').addEventListener('change',render);
document.getElementById('fmov').addEventListener('click',e=>{movedOnly=!movedOnly;
  e.target.classList.toggle('on',movedOnly);render();});

// filter option lists
for(const [sel,ix] of [['fpath',PATH],['fpos',POS]]){
  const vals=[...new Set(ROWS.map(r=>r[ix]))].sort();
  const el=document.getElementById(sel);
  vals.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;el.appendChild(o);});
}
document.getElementById('foot').innerHTML =
  'ORDER 32 seat S6 &middot; emitted from board fe6be9d6 (ORDER 31-F candidate, tag f2on, total '
  +ST.total.toLocaleString()+') under RL_O31=1 &middot; source: docs/evidence/order32_s6_2026-08-17/'
  +'{s6_emit_fan.py, S6_FAN_EMIT.json, s6_build_page.py}<br>'
  +'READ-ONLY: no engine file, law constant, no-arb instrument or board was modified. WQ6 stays sealed at '
  +'[0.18&times;5, 0.10] normalised in the engine &mdash; &lambda; renormalises weights in this page only.<br>'
  +'Validation carried by the emit: dot(WQ6, six_raw) reproduces price6() to __DEVP6__ &middot; '
  +'dot(WQ6, six_phat) reproduces P&#770; to __DEVPHAT__ (rel __DEVPHATREL__) &middot; '
  +'price(&lambda;=0) reproduces the printed board price to __DEVANCHOR__ on all __N__ rows.';

reprice();
document.querySelector('#t th[data-k=rk]').classList.add('on');
</script>
"""

SUBS = {
 '__DATA__': DATA,
 '__N__': str(STATS['n']),
 '__TOT__': '{:,}'.format(STATS['total']),
 '__WHEN__': EMIT['generated_utc'],
 '__LOWRHO__': str(STATS['lowrho']),
 '__NOFAN__': str(STATS['nofan']),
 '__FLAT__': str(STATS['flat']),
 '__INV__': str(STATS['inv']),
 '__DEVP6__': '%.3e' % V['max_dev_dot_WQ6_six_raw_vs_price6'],
 '__DEVPHAT__': '%.3e' % V['max_dev_dot_WQ6_six_phat_vs_Phat'],
 '__DEVPHATREL__': '%.3e' % V['max_rel_dev_dot_WQ6_six_phat_vs_Phat'],
 '__DEVANCHOR__': '%.3e' % V['max_dev_price_at_lambda0_vs_printed'],
}
for k, v in SUBS.items():
    HTML = HTML.replace(k, v)
assert '__' not in HTML.replace('__', '', 0) or True
for k in SUBS:
    assert k not in HTML, 'unsubstituted placeholder %s' % k

OUTP = os.path.join(HERE, 'S6_LOTTERY_DIAL.html')
open(OUTP, 'w').write(HTML)
print('WROTE %s  (%s, %.1f KB)' % (OUTP, md5(OUTP), os.path.getsize(OUTP) / 1024.0))
print('  rows %d  total %s  low-rho(greyed) %d  no-production-leg %d  flat fans %d  q97-below-band5 %d'
      % (STATS['n'], '{:,}'.format(STATS['total']), STATS['lowrho'], STATS['nofan'],
         STATS['flat'], STATS['inv']))
print('  median S6/S1 over the %d rows with rho>=0.3: %.3f' % (STATS['n_ratio'], STATS['med_ratio']))
