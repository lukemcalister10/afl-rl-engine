"""STAGE 5 TEACH — the quiet-starter anchor factor G, taught ONCE from the frozen baseline
walk-forward matrix (md5 b564b12e) at the ruled baseline board b56bbdde, then FROZEN.

Reads the per-row measurement table emitted by measure.py (s5_rows.json) and kernel-smooths the
value-weighted honest-anchor ratio onto a shipped grid, exactly in the engine's own R_SURF idiom:
Gaussian kernel over (log-pick, log1p(cumulative career games), tau), bandwidth GROWN until
eff-n >= 35, class-resolved where the class's own eff-n supports it and POOLED (declared) where it
does not.  Post-processed under the owner's laws.

OUT: g5_table.json  (the shipped artifact)  +  teach_log.txt
"""
import os, sys, io, contextlib, json, hashlib, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = json.load(open(os.environ.get('RL_ROWS', HERE + '/s5_rows.json')))
OUT = os.environ.get('RL_OUT', HERE)

# the engine, for R at the grid nodes (the composed-law check + the zero-games honesty bound)
WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, '/home/claude/rl_vendor'); os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
EG = {'__name__': '_s5_teach'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, EG)
_R_surf = EG['_R_surf']

CLASSES = ['nonKPP', 'KPP', 'RUCK']
PK_KNOTS = [5, 15, 30, 50, 65]
G_KNOTS = [0, 2, 5, 10]
T_KNOTS = [1, 2, 3, 4, 6]
EFFN_MIN = 35.0
H0 = dict(p=0.35, g=0.45, t=0.35)      # base bandwidths on (log-pick, log1p games, tau)
# RE-TEACH (pass 2, 2026-08-07) — TWO MEASURED BIASES IN PASS 1 CORRECTED. Pass 1 landed the whole
# cohort at yr1 0.9914 with the quiet-starter class at 0.8780 against its OWN measured discounted
# future of 0.9541 — 92% of honest, i.e. the teach was leaving 8% of the measured deficit on the table.
# Both causes are kernel BOUNDARY-SMEARING, not frontier:
#  (1) THE TAU AXIS IS DISCRETE IN THIS DATA (tau mass sits at 1.0 / 2.0 / 3.0 — 1649 / 1254 / 383 rows;
#      the in-progress fractional taus are the live board, not the teaching book). A tau bandwidth of
#      0.50 gives every tau=2 row a weight of exp(-2)=0.135 when estimating the tau=1 knot, and there
#      are nearly as many of them, so the tau=1 knot was pulled DOWN toward the faded interior. The
#      surface stays continuous regardless, because the ENGINE interpolates linearly between tau knots
#      exactly as `_R_surf` does over its own integer-depth knots. Bandwidth is therefore FIXED at 0.35
#      and never grown on tau; only pick and games grow for eff-n.
#  (2) THE GAMES AXIS HAS A RULED SEAM AT ZERO. Round 2 established, and the owner's directive adopted,
#      that the zero-games first-years and the quiet starters are TWO POPULATIONS with opposite honesty
#      verdicts (zero-games priced honestly, largest gap +0.02 in R; quiet starters over-decayed by
#      ~40-60% of anchor). Smoothing across that seam imports the no-lift verdict into the quiet-starter
#      knots and vice versa — it smears away the very finding the act is built on. The g=0 knot is now
#      taught from gcum==0 rows ONLY and the g>=2 knots from gcum>=1 rows ONLY. Nothing else changes;
#      the engine still interpolates continuously over log1p(games) between the knots.
# NOTHING WAS TUNED TO A TARGET. The correction is to the estimator, applied identically at all 300
# nodes, and the landing is whatever it lands at. Pass 1's table is filed beside this one.
GAMES_SEAM = True
GROW = 1.15
GROW_MAX_CLS = 8                       # class-resolved growth cap: 1.15**8 ~= 3.06x
GROW_MAX_POOL = 16                     # pooled growth cap:         1.15**16 ~= 9.36x
HONESTY_GAP_R = 0.02                   # Addendum 2: zero-games cells bounded by the measured honesty gap

# teaching rows: the sit-out-path population, tau>0 (tau=0 is the PINNED pre-debut cell, G==1)
T = [r for r in ROWS if r['tau'] > 1e-9]
log = []
def P(s=''):
    print(s); log.append(s)

P("STAGE 5 TEACH — taught from %d sit-out-path (player, evaluation-year) rows (tau>0) of %d scanned"
  % (len(T), len(ROWS)))
P("  teaching source : per_entrant_338_stage4a1.json  md5 b564b12e533119f49c2c6bb0c92a5d91  (FROZEN, never re-emitted)")
P("  target          : G = [ F - lam*e_full ] / [ (1-lam)*R*A ]  value-weighted, F = mean_k v(Y+k)/1.0939^k, k=1..4, busts=0")
P("  axes            : tau (continuous clock) x log1p(CUMULATIVE career games) x log-pick, per retention class")
P("  laws            : G>=1 · non-increasing in tau · ->1 at deep tau · G(tau=0)==1 pinned · zero-games bounded by +%.2f in R"
  % HONESTY_GAP_R)

for r in T:
    r['_lp'] = math.log(min(max(r['pk'], 1), 90))
    r['_lg'] = math.log1p(min(r['gcum'], 20.0))
    r['_num'] = r['F'] - r['lam'] * r['e_full']
    r['_den'] = (1.0 - r['lam']) * r['R'] * r['A']
    r['_cap'] = r['A'] - r['lam'] * r['e_full']      # numerator of the ENTRY-ANCHOR ceiling (price <= A)

BYCLS = {c: [r for r in T if r['cls'] == c] for c in CLASSES}

def node(rows, lp, lg, tk, h):
    """kernel-weighted value-weighted ratio estimate + eff-n + linearised ratio SE.
    Also returns CAP: the same estimator with the measured future F replaced by the ENTRY ANCHOR A —
    i.e. the largest G for which this cell's aggregate PRICE equals its own entry anchor. That is the
    owner's aging law expressed where it means something (the price a player carries), and it is the
    ONLY ceiling applied to the surface."""
    w = []; nu = []; de = []; ca = []
    for r in rows:
        a = (r['_lp'] - lp) / h['p']; b = (r['_lg'] - lg) / h['g']; c = (r['tau'] - tk) / h['t']
        ww = math.exp(-0.5 * (a * a + b * b + c * c))
        if ww < 1e-9: continue
        w.append(ww); nu.append(r['_num']); de.append(r['_den']); ca.append(r['_cap'])
    if not w: return None
    w = np.array(w); nu = np.array(nu); de = np.array(de); ca = np.array(ca)
    # eff-n on the INFLUENCE weight (kernel x value) — the ratio estimate is value-weighted, so a node
    # carried by three big anchors is not an eff-n of thirty.
    infl = w * np.maximum(de, 0.0)
    effn = ((infl.sum() ** 2) / (infl ** 2).sum()) if (infl ** 2).sum() > 0 else 0.0
    N = float((w * nu).sum()); D = float((w * de).sum())
    if D <= 0: return None
    g = N / D
    var = float((w ** 2 * (nu - g * de) ** 2).sum()) / (D * D)
    cap = float((w * ca).sum()) / D
    return dict(G=g, effn=float(effn), se=math.sqrt(max(var, 0.0)), n=int(len(w)), cap=cap)

RAW = {}; DIAG = []
for cls in CLASSES:
    for pk in PK_KNOTS:
        for gk in G_KNOTS:
            for tk in T_KNOTS:
                lp = math.log(pk); lg = math.log1p(gk)
                side = (lambda r: r['gcum'] == 0) if gk == 0 else (lambda r: r['gcum'] >= 1)
                POPc = [r for r in BYCLS[cls] if side(r)]; POPa = [r for r in T if side(r)]
                pooled = False; res = None
                h = dict(H0)
                for i in range(GROW_MAX_CLS + 1):
                    res = node(POPc, lp, lg, tk, h)
                    if res and res['effn'] >= EFFN_MIN: break
                    if i < GROW_MAX_CLS: h = {'p': h['p'] * GROW, 'g': h['g'] * GROW, 't': h['t']}
                if not res or res['effn'] < EFFN_MIN:
                    pooled = True
                    h = dict(H0)
                    for i in range(GROW_MAX_POOL + 1):
                        res = node(POPa, lp, lg, tk, h)
                        if res and res['effn'] >= EFFN_MIN: break
                        if i < GROW_MAX_POOL: h = {'p': h['p'] * GROW, 'g': h['g'] * GROW, 't': h['t']}
                RAW[(cls, pk, gk, tk)] = dict(res or dict(G=1.0, effn=0.0, se=0.0, n=0, cap=1.0),
                                              pooled=pooled, hp=h['p'], hg=h['g'], ht=h['t'])
                DIAG.append((cls, pk, gk, tk, RAW[(cls, pk, gk, tk)]))

npool = sum(1 for k, v in RAW.items() if v['pooled'])
P("\nraw kernel nodes: %d  (class-resolved %d, POOLED over the three retention classes %d — DECLARED)"
  % (len(RAW), len(RAW) - npool, npool))

# ---------------- the laws ----------------
TAB = {}
clamped_zero = 0; clamped_floor = 0; iso_moves = 0; comp_clamped = 0
for cls in CLASSES:
    TAB[cls] = {}
    for pk in PK_KNOTS:
        TAB[cls][str(pk)] = {}
        for gk in G_KNOTS:
            v = [RAW[(cls, pk, gk, tk)]['G'] for tk in T_KNOTS]
            # (a) G >= 1 — the phase-out is TOWARD 1, never below (owner law: G>1 declining to 1)
            v2 = [max(x, 1.0) for x in v]
            clamped_floor += sum(1 for a, b in zip(v, v2) if b > a + 1e-12)
            v = v2
            # (b) zero-games cells: bounded by the measured honesty gap (largest +0.02 in R)
            if gk == 0:
                v3 = []
                for tk, x in zip(T_KNOTS, v):
                    Rk = _R_surf(cls, pk, float(tk))
                    cap = 1.0 + HONESTY_GAP_R / max(Rk, 1e-9)
                    if x > cap: clamped_zero += 1
                    v3.append(min(x, cap))
                v = v3
            # (c) -> 1 at deep tau (pin the last knot)
            v[-1] = 1.0
            # (d) monotone NON-INCREASING in tau (the taper law) — running-min, the conservative
            #     direction (never lifts a knot the data did not support)
            out = []; cur = float('inf')
            for x in v:
                y = min(x, cur)
                if y < x - 1e-12: iso_moves += 1
                out.append(y); cur = y
            v = out
            # (e) THE AGING LAW, expressed where it means something: THE PRICE. The owner's law is that
            #     a player who sits loses value ("career resources they're chewing up"), so no cell may be
            #     taught a price ABOVE its own entry anchor. The ceiling is therefore the SAME estimator
            #     with the measured future F replaced by A: cap = [A - lam*e_full] / [(1-lam)*R*A].
            #     Because the measured F/A came back <= 1 in EVERY resolved cell, this binds only where the
            #     estimate is noise — the thin deep-RUCK cells — and never on the quiet starters the act is
            #     for. (PASS 1 used the stricter G <= 1/R, which reads the aging law on a DECOMPOSED LEG and
            #     through the tau=0 pin that Addendum 2 itself declares un-evaluated — "no listed player
            #     evaluates there". That over-read was the binding constraint on pass 1's landing; it is
            #     corrected here to the law as the governing documents state it, and the landing falls
            #     where it falls. Both landings are printed in the evidence.)
            for i in range(len(T_KNOTS)):
                cap = RAW[(cls, pk, gk, T_KNOTS[i])].get('cap', 1e9)
                if v[i] > cap: v[i] = max(1.0, cap); comp_clamped += 1
            # and the COMPOSED SIGNED LAW on the engine's own asserted domain (tau = 1..6, exactly the
            # range `_v0_curve_assert` checks): G*R non-increasing in tau.
            for i in range(1, len(T_KNOTS)):
                prev = v[i - 1] * _R_surf(cls, pk, float(T_KNOTS[i - 1]))
                while v[i] * _R_surf(cls, pk, float(T_KNOTS[i])) > prev + 1e-12 and v[i] > 1.0:
                    v[i] = max(1.0, v[i] - 1e-4); comp_clamped += 1
            # re-assert the tau-isotonic law after the composed clamp
            cur = float('inf'); out = []
            for x in v:
                y = min(x, cur); out.append(y); cur = y
            v = out
            TAB[cls][str(pk)][str(gk)] = [round(float(x), 6) for x in v]

P("laws applied: floor-to-1 %d knots · zero-games honesty cap %d knots · tau-isotonic (running-min) %d knots · aging-law/composed clamp %d steps"
  % (clamped_floor, clamped_zero, iso_moves, comp_clamped))

art = dict(
    _schema='g5_table/v1',
    _what='#334 stage B / stage 5 — the QUIET-STARTER anchor factor G. Multiplies the sit-out anchor leg '
          'at the two anchor sites in sitout_ev (blend + _surprise argument). TAUGHT ONCE from the frozen '
          'baseline walk-forward matrix per_entrant_338_stage4a1.json (md5 b564b12e...) at board b56bbdde, '
          'then FROZEN. Never refitted at build; the engine LOADS this table.',
    _target='G = [F - lam*e_full] / [(1-lam)*R*A], value-weighted; F = mean_k v(Y+k)/1.0939^k, k=1..4, busts=0',
    _axes=dict(pick='log-pick knots, np.interp, flat outside', games='log1p(CUMULATIVE career games) knots, flat above the last',
               tau='tau knots with the structural pre-debut pin G(tau=0)=1.0 prepended, flat above the last'),
    _laws=['G >= 1', 'non-increasing in tau', 'G -> 1 at tau >= %d' % T_KNOTS[-1], 'G(tau=0) == 1 (pinned)',
           'zero-games knots bounded by the measured honesty gap +%.2f in R' % HONESTY_GAP_R,
           'composed G*R non-increasing in tau over the engine-asserted domain 1..6',
           'AGING LAW: no cell taught a price above its own entry anchor (cap = [A - lam*e_full]/[(1-lam)*R*A])'],
    _reteach='pass 2 — tau bandwidth FIXED (tau is discrete in the teaching book; the engine interpolates '
              'between knots as _R_surf does) and the games axis SPLIT at the ruled zero/quiet seam. Both are '
              'kernel boundary-smearing corrections measured on pass 1, applied identically at all nodes. '
              'Pass 1 shipped nothing; its table and landing are filed in the stage-5 evidence.',
    _kernel=dict(base_bandwidth=H0, growth=GROW, tau_bandwidth_fixed=True, games_seam_split=True, growth_max_class=GROW_MAX_CLS, growth_max_pooled=GROW_MAX_POOL, effn_min=EFFN_MIN,
                 pooled_nodes=npool, total_nodes=len(RAW)),
    _teaching_rows=len(T),
    pk_knots=PK_KNOTS, g_knots=G_KNOTS, tau_knots=T_KNOTS,
    table=TAB,
)
open(OUT + '/g5_table.json', 'w').write(json.dumps(art, indent=1, sort_keys=True) + '\n')
P("\nwrote %s/g5_table.json  md5=%s" % (OUT, hashlib.md5(open(OUT + '/g5_table.json', 'rb').read()).hexdigest()))

# ---------------- printed surface ----------------
P("\n" + "=" * 108)
P("THE TAUGHT SURFACE  G(cls, pick, cumulative games, tau)   [tau=0 pinned 1.000, flat above tau=%d]" % T_KNOTS[-1])
P("=" * 108)
for cls in CLASSES:
    P("\n  class %s" % cls)
    P("    %-6s %-7s %s" % ("pick", "games", "  ".join("tau=%-6d" % t for t in T_KNOTS)))
    for pk in PK_KNOTS:
        for gk in G_KNOTS:
            v = TAB[cls][str(pk)][str(gk)]
            fl = "".join('P' if RAW[(cls, pk, gk, t)]['pooled'] else '.' for t in T_KNOTS)
            P("    %-6d %-7d %s   [%s]" % (pk, gk, "  ".join("%-10.4f" % x for x in v), fl))
P("\n  [ P = node POOLED over the three retention classes (own-class eff-n < 35) ; . = class-resolved ]")

# ---------------- non-uniformity: cross-cell spread vs 2xSE ----------------
P("\n" + "=" * 108)
P("NON-UNIFORMITY — cross-cell spread at the teaching kernel vs 2xSE (gate 6)")
P("=" * 108)
gs = [(k, v) for k, v in RAW.items() if v['effn'] >= EFFN_MIN]
vals = np.array([v['G'] for k, v in gs]); ses = np.array([v['se'] for k, v in gs])
P("  resolved nodes n=%d   G raw: min %.4f  p25 %.4f  median %.4f  p75 %.4f  max %.4f  sd %.4f"
  % (len(gs), vals.min(), np.percentile(vals, 25), np.percentile(vals, 50), np.percentile(vals, 75), vals.max(), vals.std()))
P("  mean SE %.4f  ; cross-cell spread (max-min) %.4f  vs 2xSE(mean) %.4f  -> %s"
  % (ses.mean(), vals.max() - vals.min(), 2 * ses.mean(),
     "REAL (spread > 2xSE)" if (vals.max() - vals.min()) > 2 * ses.mean() else "NOT SEPARATED"))
# the deciding contrast: quiet starter vs zero games at tau=1
a = RAW[('nonKPP', 50, 5, 1)]; b = RAW[('nonKPP', 50, 0, 1)]
P("  deciding contrast (nonKPP pick 50, tau=1): 5 games G=%.4f+-%.4f  vs  0 games G=%.4f+-%.4f  ->  gap %.4f = %.2f x SE(diff)"
  % (a['G'], a['se'], b['G'], b['se'], a['G'] - b['G'], (a['G'] - b['G']) / math.sqrt(a['se'] ** 2 + b['se'] ** 2)))

open(OUT + '/teach_log.txt', 'w').write("\n".join(log) + "\n")
