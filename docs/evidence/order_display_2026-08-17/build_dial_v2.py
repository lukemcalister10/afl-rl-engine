#!/usr/bin/env python3
"""DISPLAY SEAT (issue #334, ORDER 32 S6/S7 + ORDER 33 W6) -- build LOTTERY_DIAL_V2.html.

READ-ONLY.  No engine import, no law constant, no board, no emit is touched.  This script reads two
committed artefacts and writes ONE self-contained HTML file:

  in : docs/evidence/order32_s6_2026-08-17/S6_FAN_EMIT.json    (the S6 emit, 804 active rows)
  in : docs/evidence/order32_s7_2026-08-17/CELLFANS_S7.json    (the S7 measured outcome fans)
  out: docs/evidence/order_display_2026-08-17/LOTTERY_DIAL_V2.html

WHAT CHANGED vs S6_LOTTERY_DIAL.html (display only -- every number below already existed in the two
committed inputs; nothing is recomputed from the engine):

 1. The sixth scenario column is relabelled "Price if ceiling lands".  It is
    sp[5] = anchor_pts + rho * six_phat[5] -- TODAY'S BOARD PRICE re-weighted onto the top scenario,
    with (1-rho) of it still sitting on the pedigree leg.  It was headed "S6 q97", which the owner
    read as a career ceiling.  The (r) marks on rows whose tapered ceiling prices below scenario
    five are kept exactly as they were.
 2. Two career-value columns are added, so the like-for-like comparison is on the page:
      * "his ceiling, career value" = six_raw[5], the engine's own career value AT the top scenario
        (this is the 3,883 for nick-madden that the ~1,388 price was mistaken for);
      * "measured ceiling" = the realized q97 career delivered value of the row's own S7 cell
        (ND rows: pick band x position; pool rows: pathway arm), i.e. what the top 3% of players who
        came in the same way actually went on to deliver.  BOUND(max) cells print the bound marker
        and n, never a naked number; n < 8 cells fall back to the band's all-positions row and say so.
 3. A plain-language explainer box distinguishing the two ceilings.
 4. The lambda = 0 == board assertion badge, every pre-existing column and every sort are untouched.
"""
import os, json, math, hashlib, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
S6 = os.path.join(ROOT, 'docs/evidence/order32_s6_2026-08-17/S6_FAN_EMIT.json')
S7 = os.path.join(ROOT, 'docs/evidence/order32_s7_2026-08-17/CELLFANS_S7.json')

md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
EMIT = json.load(open(S6))
CELL = json.load(open(S7))
R = EMIT['rows']; WQ6 = EMIT['law']['WQ6']; V = EMIT['validation']

def dot(w, x): return sum(a * b for a, b in zip(w, x))

# ---------------------------------------------------------------- S7 cell mapping
BANDS = [(1, 10, '1-10'), (11, 20, '11-20'), (21, 30, '21-30'), (31, 40, '31-40'), (41, 64, '41-64')]
ARMNAME = {'RD': 'rookie draft', 'MSD': 'mid-season draft', 'SSP': 'supplemental selection period',
           'PDA': 'post-draft academy', 'PDN': 'post-draft next-gen', 'PDS': 'post-draft scholarship',
           'UNR': 'post-draft unregistered', 'IRE': 'post-draft Ireland'}

def band_of(pick):
    for lo, hi, k in BANDS:
        if lo <= pick <= hi:
            return k, False
    return '41-64', True          # picks 65+ : beyond the measured band, flagged

def cell_for(r):
    """Return (label, note, cellobj, flags) for one active row.  flags: beyond / pooled."""
    if r['pathway'] == 'ND':
        b, beyond = band_of(int(r['pick']))
        key = '%s|%s' % (b, r['pos'])
        c = CELL['nd'][key]
        pooled = c.get('status') != 'resolved'          # n < 8 : no fan published for that cell
        if pooled:
            thin_n = c['n']
            c = CELL['nd']['%s|ALL' % b]
            label = 'national draft %s &middot; all positions' % b
            note = ('his own %s %s cell has only n=%d careers in it -- too thin to publish a 97th '
                    'percentile, so the band\u2019s all-positions row is shown instead') % (b, r['pos'], thin_n)
        else:
            label = 'national draft %s &middot; %s' % (b, r['pos'])
            note = ''
        if beyond:
            note = (note + ' ' if note else '') + ('he was pick %d; the measured history stops at pick 64, '
                                                   'so the 41-64 band is the nearest cell there is') % int(r['pick'])
        return label, note, c, {'beyond': beyond, 'pooled': pooled}
    arm = r['pathway']
    c = CELL['pool'][arm]
    label = '%s &middot; %s (all positions)' % (arm, ARMNAME.get(arm, arm))
    return label, '', c, {'beyond': False, 'pooled': False}

def q97_of(c):
    """(value, bound, n, n_zero, median) -- never returns nan; bound=1 means BOUND(max)."""
    n = int(c.get('n') or 0)
    nz = int(c.get('n_zero') or 0)
    med = c.get('median')
    lv = c.get('levels')
    if not lv or 'q97' not in lv:
        return None, 1, n, nz, med
    q = lv['q97']
    v = q.get('value')
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None, 1, n, nz, med
    return float(v), (0 if q.get('resolved') and not q.get('flag') else 1), n, nz, med

# ---------------------------------------------------------------- rows
PAGE = []
NBOUND = NPOOLED = NBEYOND = 0
for r in R:
    rho, anc, sixp = r['rho'], r['anchor_pts'], r['six_phat']
    sp = [anc + rho * x for x in sixp]
    d = abs(dot(WQ6, sp) - r['cand'])
    assert d < 1e-6, ('scenario prices do not average to the printed price', r['key'], d)
    label, note, c, fl = cell_for(r)
    q97, bound, n, nz, med = q97_of(c)
    assert not (q97 is None and bound == 0)
    NBOUND += bound; NPOOLED += fl['pooled']; NBEYOND += fl['beyond']
    PAGE.append([
        r['name'], r['pathway'] or '?', r['pos'] or '?', int(r['games'] or 0), int(r['cand']),
        round(rho, 6),
        sp,                                        # 6  scenario prices, board points (full precision)
        [round(x, 1) for x in r['six_raw']],       # 7  the raw per-scenario career values
        [round(x, 2) for x in r['b6']],            # 8  the six band levels
        (round(r['spread_ratio_6_1'], 3) if r['spread_ratio_6_1'] is not None else None),
        (round(r['spread_span_over_med'], 3) if r['spread_span_over_med'] is not None else None),
        (round(100 * r['top_scenario_share_of_Phat'], 2) if r['top_scenario_share_of_Phat'] is not None else None),
        (round(100 * r['weighted_cv'], 2) if r['weighted_cv'] is not None else None),
        round(r['m_downstream'], 6),
        1 if r['fan_carries_price'] else 0,
        1 if r['q97_below_band5'] else 0,
        (round(q97, 1) if q97 is not None else None),   # 16 measured cell q97 (career delivered value)
        bound,                                          # 17 1 = BOUND(max) / unresolved
        n,                                              # 18 careers in the cell
        nz,                                             # 19 of which delivered ~zero
        (round(med, 1) if med is not None else None),   # 20 the cell's median career
        label,                                          # 21 which cell
        note,                                           # 22 why, when it is not his own cell
    ])

TOT = sum(int(r['cand']) for r in R)
ratios = sorted(r['spread_ratio_6_1'] for r in R if r['rho'] >= 0.3 and r['spread_ratio_6_1'])
STATS = {'n': len(R), 'total': TOT, 'lowrho': sum(1 for r in R if r['rho'] < 0.3),
         'nofan': V['n_rows_fan_cannot_carry_price'], 'flat': V['n_fan_flat'],
         'inv': V['n_q97_below_band5'], 'bound': NBOUND, 'pooled': NPOOLED, 'beyond': NBEYOND,
         'med_ratio': round(statistics.median(ratios), 3), 'n_ratio': len(ratios)}

DATA = json.dumps({'wq6': WQ6, 'rows': PAGE, 'stats': STATS}, separators=(',', ':'))

HTML = """<!doctype html>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Lottery Dial v2 &middot; two ceilings, kept apart</title>
<style>
:root{
  --pitch:#0a0c10; --card:#12151c; --card-2:#181c25; --card-3:#1e2431; --edge:#232936; --edge-2:#2f3747;
  --text:#f2f5f9; --dim:#8b95a6; --faint:#525c6d; --ghost:#39414f;
  --volt:#c8f04a; --volt-soft:rgba(200,240,74,.12);
  --sky:#6cc6f5; --sky-soft:rgba(108,198,245,.10);
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
.app{max-width:1560px;margin:0 auto;padding:0 18px 80px}
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
.box.fix{border-color:var(--sky);border-left:4px solid var(--sky);background:var(--sky-soft)}
.box.fix h2{color:var(--sky)}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px 26px;margin:12px 0 4px}
.two .c{border:1px solid var(--edge-2);background:var(--card);padding:12px 14px}
.two .c .h{font-family:var(--cond);font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--sky)}
.two .c .h.m{color:var(--volt)}
.two .c .u{font-family:var(--mono);font-size:10.5px;color:var(--faint);margin:3px 0 7px;letter-spacing:.04em}
.two .c p{margin:0;color:var(--dim);font-size:12.5px}
.eg{margin-top:12px;border-left:2px solid var(--sky);padding:8px 0 8px 12px;color:var(--dim);font-size:12.5px}
.eg b{color:var(--text)}
.eg .n{font-family:var(--mono);color:var(--text)}
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
table{border-collapse:collapse;width:100%;min-width:1560px}
th{position:sticky;top:0;z-index:2;background:var(--card-2);border-bottom:1px solid var(--edge-2);
  font-family:var(--cond);font-weight:700;font-size:10px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--dim);padding:9px 8px;text-align:right;cursor:pointer;user-select:none;white-space:nowrap}
th:hover{color:var(--volt)}
th.l{text-align:left}
th.on{color:var(--volt);background:var(--card-3)}
th.car{color:var(--sky)}
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
.car{color:var(--sky)}
.meas{color:var(--text)}
.cn{color:var(--faint);font-size:10.5px}
.bnd{color:var(--warn)}
.grey{color:var(--ghost)!important}
.up{color:var(--up)} .dn{color:var(--dn)} .zero{color:var(--faint)}
.mv{font-size:11px}
.sep{border-left:1px solid var(--edge-2)}
footer{margin-top:22px;color:var(--faint);font-size:11px;font-family:var(--mono);line-height:1.9}
</style>

<div class="banner">Order 32 &middot; seats S6 + S7 &middot; display prototype &mdash; the sealed pricing law is UNCHANGED. &lambda; is a lens over an emit, not a re-price.</div>

<div class="app">
<header>
  <div class="brand">Lottery<b>Dial</b> v2<span class="sub">the six-scenario fan behind one printed price &mdash; and what careers like his actually delivered</span></div>
  <div class="spacer"></div>
  <div class="stamp">
    board <b>fe6be9d6</b> &middot; store <b>cb38ef11</b> &middot; engine <b>14000af2</b> &middot; pvc <b>78ad9842</b><span class="badge">RL_O31</span><span class="badge" id="vbadge">checking</span><br>
    __N__ active rows &middot; board total <b>__TOT__</b> pts &middot; candidate build (ORDER 31-F, tag f2on) &middot; emitted __WHEN__<br>
    measured cells: S7 outcome fans <b>__S7MD5__</b>
  </div>
</header>

<div class="box fix">
  <h2>Two different &ldquo;ceilings&rdquo; &mdash; and the page used to show only one of them</h2>
  <p style="margin:0 0 6px">The column that used to be headed <b>&ldquo;S6 q97&rdquo;</b> was read as a career ceiling. It never was one.
  It is a <b>price today</b>. Three separate numbers now sit on each row, and they answer three different questions.</p>
  <div class="two">
    <div class="c">
      <div class="h">1 &middot; Price if ceiling lands</div>
      <div class="u">board points &mdash; an auction price, right now</div>
      <p>What he would be <b>worth on the board</b> if his best band level is the one that turns up. It is
      today&rsquo;s price with all the weight moved onto the top scenario &mdash; and for a young player most of that
      price is still <b>pedigree</b>, which does not move with the scenario at all. That is why the number stays
      close to his printed price. <b>It is not the size of a career.</b></p>
    </div>
    <div class="c">
      <div class="h">2 &middot; His ceiling, as career value</div>
      <div class="u">board points of delivered career &mdash; the engine&rsquo;s own number</div>
      <p>The <b>same</b> top scenario, but written out as the whole career the engine reckons that level would
      deliver. This is the number to hold up against history &mdash; not the price. On most young rows it is two to
      four times the price in column 1, because a price is not a career.</p>
    </div>
    <div class="c">
      <div class="h m">3 &middot; Measured ceiling</div>
      <div class="u">board points of delivered career &mdash; measured, not modelled</div>
      <p><b>What the top 3% of players like him went on to deliver.</b> Real finished careers, from the same
      entry route: same pick band and position for national-draft players, same pathway arm for the pickless
      ones. No model in it at all. The number of careers it is measured from is printed beside it &mdash; when
      that count is small the page prints a <b>bound</b> (&ge;) instead of pretending to a percentile.</p>
    </div>
  </div>
  <div class="eg">
    <b>The row that caught this.</b> <b>Nick Madden</b> reads <span class="n">__MADPRICE__</span> in column 1.
    That is his <i>price if the ceiling lands</i>, and roughly two thirds of it is pedigree that the scenario never
    touches. His ceiling written as a <i>career</i> is <span class="n">__MADCAREER__</span> (column 2), and the top 3% of
    <span class="n">__MADCELL__</span> entrants actually delivered <span class="n">__MADMEAS__</span> (column 3,
    from __MADN__ finished careers). Comparing the <span class="n">__MADPRICE__</span> against career outcomes in the
    thousands was comparing a price to a career &mdash; the page was at fault, not the reader.
  </div>
  <p style="margin:10px 0 0;color:var(--dim)">Two honesties about column 3. It is <b>unconditional</b>: it knows the route he came in
  by, not how he is playing now &mdash; a player already getting games at a good level is not the median of his own
  entry cell. And the two career columns are the same <b>scale</b> (board points of delivered career) but not the same
  <b>ruler</b>: one is the engine&rsquo;s scenario valuation, the other a measured career total. Read the gap between them
  as a rough bearing, not a decimal.</p>
</div>

<div class="box warn">
  <h2>Read this before you move the dial</h2>
  <p style="margin:0 0 9px"><b>The fan covers the PRODUCTION leg only.</b> Under the one law a price is
  <code>rho(g) &times; P&#770; + [D(c_u)(1&minus;rho) + &Phi;&beta;rho] &times; v0</code>. The six scenarios live entirely inside
  <code>P&#770;</code>. The <b>v0 (pedigree) leg has its own variance and it is not in this emit</b> &mdash; the measured
  ceiling column is the closest thing to it on this page, and it is a population fan, not this player&rsquo;s.</p>
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
  <p style="margin:0">(3) <b>The ceiling is not always the top scenario.</b> The sixth scenario is built on the frozen q97
  ceiling, but the v7 age-taper pulls it back toward the band median &mdash; so on <b>__INV__ of __N__ rows</b> it prices
  <i>below</i> scenario five. Those rows are marked <span style="color:var(--warn)">&#9660;</span> in the
  &ldquo;price if ceiling lands&rdquo; column, and on them pushing &lambda; positive is <b>not</b> the same as betting on the
  best case: past a point it walks the price back down. Read the six numbers, not the dial's direction.</p>
</div>

<div class="box">
  <h2>What the columns mean</h2>
  <div class="defs">
    <div><div class="t">The six scenarios</div><div class="d">The engine never prices a player at one projected level.
      <code>b6</code> builds six of them &mdash; five conditional-prior band quantiles plus a frozen ceiling (<b>q97</b>) as
      the sixth &mdash; and the board price is a fixed-weight average across all six.</div></div>
    <div><div class="t">S1 &hellip; S5, and &ldquo;price if ceiling lands&rdquo;</div><div class="d">What this player would be worth
      <b>on the board</b> if that scenario were the one that lands. S1 = the floor band; the sixth is the frozen-ceiling
      scenario. The printed price is exactly the weighted average of these six numbers.</div></div>
    <div><div class="t">His ceiling, career value</div><div class="d">The engine's own career value at that same top
      scenario &mdash; the whole career, not the auction price of it. This is the number that belongs beside the measured
      column; the price never did.</div></div>
    <div><div class="t">Measured ceiling</div><div class="d">Realized <b>q97 career delivered value</b> of his own entry
      cell: what the top 3% of players who came in the same way actually delivered. <span class="bnd">&ge;</span> means the
      cell is too thin to resolve a 97th percentile and the sample maximum is shown as a <b>bound</b>; the count of
      finished careers is printed beside every value. Hover the cell for which cell it is.</div></div>
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
  <th data-k="s5" title="today's price re-weighted onto the top scenario -- a PRICE, not a career">Price if ceiling lands</th>
  <th class="sep car" data-k="cvv" title="the engine's own career value at that same top scenario">His ceiling, career value</th>
  <th class="car" data-k="mc" title="realized q97 career delivered value of his own entry cell -- measured, not modelled">Measured ceiling &middot; top 3% like him</th>
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
//             16 measured cell q97 17 bound 18 cell n 19 cell n_zero 20 cell median 21 cell label 22 cell note
const NAME=0,PATH=1,POS=2,G=3,CAND=4,RHO=5,SP=6,SIX=7,BB=8,RATIO=9,SPAN=10,TSH=11,CV=12,MM=13,FAN=14,INV=15,
      MQ=16,MBND=17,MN=18,MNZ=19,MMED=20,MLAB=21,MNOTE=22;

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
  cvv:i=>ROWS[i][SIX][5], mc:i=>ROWS[i][MQ],
  ratio:i=>ROWS[i][RATIO], span:i=>ROWS[i][SPAN], tsh:i=>ROWS[i][TSH], cv:i=>ROWS[i][CV]};
const TXTK={nm:1,pa:1,po:1};

function fmt(x){return x===null||x===undefined?'\\u2014':Math.round(x).toLocaleString();}
function f2(x,n){return x===null||x===undefined?'\\u2014':x.toFixed(n);}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');}

// The measured cell NEVER prints a naked number it has not earned:
//   resolved  ->  value  + "n <count>"
//   bound     ->  ">= value *" + "n <count>"   (sample max, not a percentile)
//   missing   ->  "no measured cell" + "n <count>"
function measCell(r){
  const v=r[MQ], n=r[MN];
  const tip=esc(r[MLAB].replace(/&middot;/g,'\\u00b7').replace(/&rsquo;/g,"'")+' \\u00b7 '+n+' finished careers, '
    +r[MNZ]+' of them delivered ~0 \\u00b7 median career '+(r[MMED]===null?'\\u2014':Math.round(r[MMED]).toLocaleString())
    +(r[MBND]?' \\u00b7 BOUND(max): n is too small to resolve a 97th percentile, the sample maximum is shown as a bound':'')
    +(r[MNOTE]?' \\u00b7 '+r[MNOTE].replace(/&rsquo;/g,"'"):''));
  if(v===null||v===undefined)
    return '<td class="meas" title="'+tip+'"><span class="bnd">no measured cell</span> <span class="cn">n '+n+'</span></td>';
  const val=(r[MBND]?'<span class="bnd">\\u2265 </span>':'')+fmt(v)+(r[MBND]?'<span class="bnd">*</span>':'');
  return '<td class="meas" title="'+tip+'">'+val+' <span class="cn">n '+n+'</span></td>';
}

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
      +'<td class="sep car">'+fmt(r[SIX][5])+'</td>'
      +measCell(r)
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
  'ORDER 32 seats S6 + S7 &middot; display layer only &middot; emitted from board fe6be9d6 (ORDER 31-F candidate, tag f2on, total '
  +ST.total.toLocaleString()+') under RL_O31=1 &middot; scenario prices: docs/evidence/order32_s6_2026-08-17/S6_FAN_EMIT.json &middot; '
  +'measured cells: docs/evidence/order32_s7_2026-08-17/CELLFANS_S7.json &middot; builder: '
  +'docs/evidence/order_display_2026-08-17/build_dial_v2.py<br>'
  +'READ-ONLY: no engine file, law constant, no-arb instrument, board or emit was modified. WQ6 stays sealed at '
  +'[0.18&times;5, 0.10] normalised in the engine &mdash; &lambda; renormalises weights in this page only. The relabel and the '
  +'two career columns are DISPLAY changes: every number was already in the two committed inputs.<br>'
  +'Measured-ceiling coverage: '+ST.bound+' of '+ST.n+' rows sit in a cell whose q97 does not resolve (printed as a '
  +'&ge; bound with n, never as a percentile) &middot; '+ST.pooled+' rows fall back to their band\\u2019s all-positions cell '
  +'(own cell n &lt; 8) &middot; '+ST.beyond+' rows were picked beyond 64, where the measured history stops.<br>'
  +'Validation carried by the emit: dot(WQ6, six_raw) reproduces price6() to __DEVP6__ &middot; '
  +'dot(WQ6, six_phat) reproduces P&#770; to __DEVPHAT__ (rel __DEVPHATREL__) &middot; '
  +'price(&lambda;=0) reproduces the printed board price to __DEVANCHOR__ on all __N__ rows.';

reprice();
document.querySelector('#t th[data-k=rk]').classList.add('on');
</script>
"""

# ---------------------------------------------------------------- madden, for the explainer box
MAD = [p for p in PAGE if p[0].lower().startswith('nick madden')]
assert len(MAD) == 1, 'nick-madden row not found exactly once'
m = MAD[0]
madcell = m[21].replace('&middot;', '\u00b7')
madmeas = ('\u2265 %s*' % '{:,}'.format(int(round(m[16])))) if m[17] else '{:,}'.format(int(round(m[16])))

SUBS = {
 '__DATA__': DATA,
 '__N__': str(STATS['n']),
 '__TOT__': '{:,}'.format(STATS['total']),
 '__WHEN__': EMIT['generated_utc'],
 '__S7MD5__': md5(S7)[:8],
 '__LOWRHO__': str(STATS['lowrho']),
 '__NOFAN__': str(STATS['nofan']),
 '__FLAT__': str(STATS['flat']),
 '__INV__': str(STATS['inv']),
 '__MADPRICE__': '{:,}'.format(int(round(m[6][5]))),
 '__MADCAREER__': '{:,}'.format(int(round(m[7][5]))),
 '__MADCELL__': madcell,
 '__MADMEAS__': madmeas,
 '__MADN__': str(m[18]),
 '__DEVP6__': '%.3e' % V['max_dev_dot_WQ6_six_raw_vs_price6'],
 '__DEVPHAT__': '%.3e' % V['max_dev_dot_WQ6_six_phat_vs_Phat'],
 '__DEVPHATREL__': '%.3e' % V['max_rel_dev_dot_WQ6_six_phat_vs_Phat'],
 '__DEVANCHOR__': '%.3e' % V['max_dev_price_at_lambda0_vs_printed'],
}
for k, v in SUBS.items():
    HTML = HTML.replace(k, v)
for k in SUBS:
    assert k not in HTML, 'unsubstituted placeholder %s' % k

OUTP = os.path.join(HERE, 'LOTTERY_DIAL_V2.html')
open(OUTP, 'w').write(HTML)
print('WROTE %s  (%s, %.1f KB)' % (OUTP, md5(OUTP), os.path.getsize(OUTP) / 1024.0))
print('  inputs: S6_FAN_EMIT.json %s  CELLFANS_S7.json %s' % (md5(S6)[:8], md5(S7)[:8]))
print('  rows %d  total %s  bound-q97 cells %d  pooled-fallback %d  pick>64 %d'
      % (STATS['n'], '{:,}'.format(STATS['total']), STATS['bound'], STATS['pooled'], STATS['beyond']))
print('  nick-madden: price-if-ceiling-lands %s | his ceiling as career value %s | measured %s (%s, n=%d)'
      % (SUBS['__MADPRICE__'], SUBS['__MADCAREER__'], SUBS['__MADMEAS__'], madcell, m[18]))
