"""#334 stage B / STAGE 5 — THE CONSISTENCY PASS (owner-authorized, #334 comment 5217293177).

ONE NAMED SOLVER CORRECTION. Nothing else moves: same teaching source (the FROZEN baseline matrix
b564b12e), same target (each cell's own measured discounted future F), same axes, same knots, same
kernel and bandwidths, same pooling rule, same pins (G(tau=0) == 1, tau=6 -> 1), same laws.

WHAT WAS WRONG (this seat's own MEMO.md section 4, filed with the STOP report):

    G was solved for the anchor leg at the FROZEN lam:

        G = [ F - lam*e_full ] / [ (1-lam)*R*A ]                        (the frozen-lam solve)

    But installing G MOVES lam. The directive requires G to enter `_surprise`'s anchor argument, and
    `_surprise` reads s = |log(e_full/anchor)|. Lift the anchor and s moves, the evidence exponent moves,
    lam moves, and the realised price is NOT the F the cell was solved for. Measured consequence: the
    quiet-starter class landed at 93.5% of its own measured future and the whole cohort missed the 1.00
    floor at 0.9945.

WHAT THIS PASS DOES. It solves for the G whose INSTALLED effect prices the cell at F — the trust-weight
feedback is inside the solve. For a teaching row i with cell factor g:

    a_i(g)   = g * R_i * A_i                                            the lifted anchor leg
    s_i(g)   = |log(e_i / a_i(g))|                                      the surprise, RE-READ at a_i(g)
    u_i      = 1 - rho(gp_i)/rho(6)                                     the unresolved share (fixed)
    x_i(g)   = xb_i + SUR_W * s_i(g) * u_i                              xb_i = 1 + PED_BAR*(1-q_i)
    lam_i(g) = lam0_i ** x_i(g)
    P_i(g)   = (1 - lam_i(g)) * a_i(g) + lam_i(g) * e_i                 THE INSTALLED PRICE

and finds the g solving the kernel- and value-weighted cell equation

    SUM_i w_i * P_i(g)  =  SUM_i w_i * F_i .

P_i is continuous and NON-DECREASING in g on g >= 1 (raise the anchor and either s grows, the bar rises,
lam falls and more weight lands on the now-higher anchor; or s shrinks, lam rises and more weight lands
on e_i which is above the anchor in that branch — both directions push the price up), so the aggregate
is monotone and bisection is safe and unique. Verified numerically at every node before the root is
taken; a non-monotone node would HALT rather than return a root.

xb_i is RECOVERED from the frozen-lam measurement, not re-derived:
    xb_i = log(lam_i)/log(lam0_i) - SUR_W * s_i(1) * u_i
so this pass consumes exactly the same per-row measurement file the published teach consumed. Rows with
lam0 in {0, 1} are handled in closed form (lam is pinned there and no exponent exists).

THE AGING LAW is unchanged and is now expressible in the same currency as the target: the cap is the g
that prices the cell at its own ENTRY ANCHOR, solved by the identical root-finder with F replaced by A.

OUT: g5_table_LANDED.json + consistency_log.txt. The frozen-lam table (g5_table.json, md5 1dc66750...)
is LEFT IN PLACE as part of the STOP record.
"""
import os, sys, io, contextlib, json, hashlib, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = json.load(open(os.environ.get('RL_ROWS', HERE + '/s5_rows.json')))
OUT = os.environ.get('RL_OUT', HERE)

WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, '/home/claude/rl_vendor'); os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
EG = {'__name__': '_s5_cons'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, EG)
_R_surf = EG['_R_surf']; _rho_res = EG['_rho_res']; _RHO_SIT_BAR = EG['_RHO_SIT_BAR']
SUR_W = EG['SUR_W']; LAM_SIT = EG['LAM_SIT']

CLASSES = ['nonKPP', 'KPP', 'RUCK']
PK_KNOTS = [5, 15, 30, 50, 65]
G_KNOTS = [0, 2, 5, 10]
T_KNOTS = [1, 2, 3, 4, 6]
EFFN_MIN = 35.0
H0 = dict(p=0.35, g=0.45, t=0.35)
GROW = 1.15
GROW_MAX_CLS = 8
GROW_MAX_POOL = 16
HONESTY_GAP_R = 0.02
GMAX = 12.0                    # the bracket's upper end; the aging cap almost always binds first

T = [r for r in ROWS if r['tau'] > 1e-9]
log = []
def P(s=''):
    print(s); log.append(s)

P("STAGE 5 CONSISTENCY PASS — the fixed-point solve on the installed lam response")
P("  teaching source : per_entrant_338_stage4a1.json  md5 b564b12e533119f49c2c6bb0c92a5d91  (FROZEN, unchanged)")
P("  target          : UNCHANGED — each cell's own measured discounted future F = mean_k v(Y+k)/1.0939^k, k=1..4, busts=0")
P("  solve           : find g with SUM w*P_i(g) = SUM w*F_i, P_i the INSTALLED price incl. the surprise re-read")
P("  rows            : %d sit-out-path rows with tau>0 (identical to the published teach)" % len(T))
P("  engine dials read: SUR_W=%.4g  PED_BAR=%.4g  (both UNMOVED by this pass)" % (SUR_W, EG['PED_BAR']))

# ---- per-row solver inputs, recovered from the SAME measurement file ----
BAD = 0
for r in T:
    r['_lp'] = math.log(min(max(r['pk'], 1), 90))
    r['_lg'] = math.log1p(min(r['gcum'], 20.0))
    gp = r['gp']
    r['_lam0'] = float(np.interp(gp, [0, 1, 2, 3, 4, 5, 6], LAM_SIT))
    r['_u'] = 1.0 - _rho_res(gp) / _RHO_SIT_BAR
    anch1 = r['R'] * r['A']
    s1 = abs(math.log(r['e_full'] / anch1)) if (r['e_full'] > 0 and anch1 > 0) else 0.0
    if 0.0 < r['_lam0'] < 1.0 and r['lam'] > 0:
        r['_xb'] = math.log(r['lam']) / math.log(r['_lam0']) - SUR_W * s1 * r['_u']
    else:
        r['_xb'] = None                      # lam is pinned at 0 or 1; no exponent exists
    # self-check: the recovered parameters must reproduce the measured lam and price at g=1
    if r['_xb'] is not None:
        lam_chk = r['_lam0'] ** (r['_xb'] + SUR_W * s1 * r['_u'])
        if abs(lam_chk - r['lam']) > 1e-9: BAD += 1
P("  parameter recovery self-check: %d of %d rows fail to reproduce their own measured lam  (must be 0)"
  % (BAD, len(T)))
assert BAD == 0, "parameter recovery is not exact — the solve would be measuring a different engine"


def price(r, g):
    """The INSTALLED price of row r under cell factor g — the engine's own expression."""
    a = g * r['R'] * r['A']
    l0 = r['_lam0']
    if l0 <= 0.0: return a                                   # lam == 0: pure anchor leg
    if l0 >= 1.0: return r['e_full']                         # lam == 1: anchor drops out (the 6-game bar)
    s = abs(math.log(r['e_full'] / a)) if (r['e_full'] > 0 and a > 0) else 0.0
    lam = l0 ** (r['_xb'] + SUR_W * s * r['_u'])
    return (1.0 - lam) * a + lam * r['e_full']


def node(rows, lp, lg, tk, h):
    w = []; sub = []
    for r in rows:
        a = (r['_lp'] - lp) / h['p']; b = (r['_lg'] - lg) / h['g']; c = (r['tau'] - tk) / h['t']
        ww = math.exp(-0.5 * (a * a + b * b + c * c))
        if ww < 1e-9: continue
        w.append(ww); sub.append(r)
    if not w: return None
    w = np.array(w)
    de = np.array([(1.0 - r['lam']) * r['R'] * r['A'] for r in sub])
    infl = w * np.maximum(de, 0.0)
    effn = ((infl.sum() ** 2) / (infl ** 2).sum()) if (infl ** 2).sum() > 0 else 0.0
    return dict(w=w, rows=sub, effn=float(effn), n=len(sub))


def solve(nd, target_key):
    """Bisect for the g whose INSTALLED aggregate price hits the target. target_key: 'F' or 'A'."""
    w = nd['w']; rows = nd['rows']
    tgt = float(sum(wi * (r['F'] if target_key == 'F' else r['A']) for wi, r in zip(w, rows)))
    def agg(g): return float(sum(wi * price(r, g) for wi, r in zip(w, rows)))
    lo, hi = 1.0, GMAX
    a_lo, a_hi = agg(lo), agg(hi)
    # monotonicity check on a coarse grid — a non-monotone node HALTS rather than returning a root
    grid = [agg(1.0 + i * (GMAX - 1.0) / 12.0) for i in range(13)]
    if any(grid[i + 1] < grid[i] - 1e-6 * max(abs(grid[i]), 1.0) for i in range(12)):
        raise SystemExit('HALT: aggregate installed price is NOT monotone in g at a node — bisection is unsafe')
    if a_lo >= tgt: return 1.0, 'at-or-below-floor'
    if a_hi <= tgt: return GMAX, 'bracket-exhausted'
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if agg(mid) < tgt: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi), 'solved'


BYCLS = {c: [r for r in T if r['cls'] == c] for c in CLASSES}
RAW = {}
nonmono = 0
for cls in CLASSES:
    for pk in PK_KNOTS:
        for gk in G_KNOTS:
            for tk in T_KNOTS:
                lp = math.log(pk); lg = math.log1p(gk)
                side = (lambda r: r['gcum'] == 0) if gk == 0 else (lambda r: r['gcum'] >= 1)
                POPc = [r for r in BYCLS[cls] if side(r)]; POPa = [r for r in T if side(r)]
                pooled = False; nd = None
                h = dict(H0)
                for i in range(GROW_MAX_CLS + 1):
                    nd = node(POPc, lp, lg, tk, h)
                    if nd and nd['effn'] >= EFFN_MIN: break
                    if i < GROW_MAX_CLS: h = {'p': h['p'] * GROW, 'g': h['g'] * GROW, 't': h['t']}
                if not nd or nd['effn'] < EFFN_MIN:
                    pooled = True
                    h = dict(H0)
                    for i in range(GROW_MAX_POOL + 1):
                        nd = node(POPa, lp, lg, tk, h)
                        if nd and nd['effn'] >= EFFN_MIN: break
                        if i < GROW_MAX_POOL: h = {'p': h['p'] * GROW, 'g': h['g'] * GROW, 't': h['t']}
                if not nd:
                    RAW[(cls, pk, gk, tk)] = dict(G=1.0, cap=1.0, effn=0.0, n=0, pooled=pooled, how='empty')
                    continue
                g_f, how = solve(nd, 'F')
                g_a, _ = solve(nd, 'A')
                RAW[(cls, pk, gk, tk)] = dict(G=g_f, cap=g_a, effn=nd['effn'], n=nd['n'],
                                              pooled=pooled, how=how, hp=h['p'], hg=h['g'], ht=h['t'])

npool = sum(1 for v in RAW.values() if v['pooled'])
P("\nsolved %d nodes: class-resolved %d, POOLED over the three retention classes %d — DECLARED"
  % (len(RAW), len(RAW) - npool, npool))
P("  bracket-exhausted nodes (target above the g<=%.0f reach): %d"
  % (GMAX, sum(1 for v in RAW.values() if v.get('how') == 'bracket-exhausted')))

# ---------------- the laws, verbatim from the published teach ----------------
TAB = {}
c_floor = c_zero = c_iso = c_age = c_comp = 0
for cls in CLASSES:
    TAB[cls] = {}
    for pk in PK_KNOTS:
        TAB[cls][str(pk)] = {}
        for gk in G_KNOTS:
            v = [RAW[(cls, pk, gk, tk)]['G'] for tk in T_KNOTS]
            v2 = [max(x, 1.0) for x in v]
            c_floor += sum(1 for a, b in zip(v, v2) if b > a + 1e-12); v = v2
            if gk == 0:
                v3 = []
                for tk, x in zip(T_KNOTS, v):
                    cap = 1.0 + HONESTY_GAP_R / max(_R_surf(cls, pk, float(tk)), 1e-9)
                    if x > cap: c_zero += 1
                    v3.append(min(x, cap))
                v = v3
            # THE AGING LAW, in the same currency as the target: no cell priced above its entry anchor.
            # RL_G5_NOCAP=1 lifts it — a DIAGNOSTIC ONLY, never shipped, used to price what the law costs
            # so the owner can rule on a number instead of a principle. See CONSISTENCY_PASS.md.
            if os.environ.get('RL_G5_NOCAP') != '1':
                for i in range(len(T_KNOTS)):
                    cap = RAW[(cls, pk, gk, T_KNOTS[i])]['cap']
                    if v[i] > cap: v[i] = max(1.0, cap); c_age += 1
            v[-1] = 1.0                                        # -> 1 at the deep knot
            out = []; cur = float('inf')
            for x in v:
                y = min(x, cur)
                if y < x - 1e-12: c_iso += 1
                out.append(y); cur = y
            v = out
            for i in range(1, len(T_KNOTS)):                   # composed G*R non-increasing, tau 1..6
                prev = v[i - 1] * _R_surf(cls, pk, float(T_KNOTS[i - 1]))
                while v[i] * _R_surf(cls, pk, float(T_KNOTS[i])) > prev + 1e-12 and v[i] > 1.0:
                    v[i] = max(1.0, v[i] - 1e-4); c_comp += 1
            cur = float('inf'); out = []
            for x in v:
                y = min(x, cur); out.append(y); cur = y
            TAB[cls][str(pk)][str(gk)] = [round(float(x), 6) for x in out]

P("laws applied: floor-to-1 %d · zero-games honesty cap %d · AGING (price<=entry anchor) %d · tau-isotonic %d · composed %d"
  % (c_floor, c_zero, c_age, c_iso, c_comp))

art = dict(
    _schema='g5_table/v1',
    _what='#334 stage B / stage 5 — the QUIET-STARTER anchor factor G, CONSISTENCY PASS (owner-authorized, '
          '#334 comment 5217293177). Multiplies the sit-out anchor leg at the two anchor sites in sitout_ev. '
          'TAUGHT ONCE from the frozen baseline walk-forward matrix per_entrant_338_stage4a1.json '
          '(md5 b564b12e...) at board b56bbdde, then FROZEN. The engine LOADS this table; it never fits it.',
    _target='SUM w*P_i(g) = SUM w*F_i, where P_i(g) is the INSTALLED price (the surprise statistic re-reads '
            'the lifted anchor, so the trust-weight feedback is inside the solve). F = mean_k v(Y+k)/1.0939^k, '
            'k=1..4, busts=0. Supersedes the frozen-lam solve of the first pass (md5 1dc66750a51d04eb9b35b33685960feb).',
    _axes=dict(pick='log-pick knots, np.interp, flat outside',
               games='log1p(CUMULATIVE career games) knots, flat above the last',
               tau='tau knots with the structural pre-debut pin G(tau=0)=1.0 prepended, flat above the last'),
    _laws=['G >= 1', 'non-increasing in tau', 'G -> 1 at tau >= %d' % T_KNOTS[-1], 'G(tau=0) == 1 (pinned)',
           'zero-games knots bounded by the measured honesty gap +%.2f in R' % HONESTY_GAP_R,
           'AGING LAW: no cell taught an INSTALLED price above its own entry anchor',
           'composed G*R non-increasing in tau over the engine-asserted domain 1..6'],
    _kernel=dict(base_bandwidth=H0, growth=GROW, tau_bandwidth_fixed=True, games_seam_split=True,
                 growth_max_class=GROW_MAX_CLS, growth_max_pooled=GROW_MAX_POOL, effn_min=EFFN_MIN,
                 pooled_nodes=npool, total_nodes=len(RAW)),
    _teaching_rows=len(T),
    pk_knots=PK_KNOTS, g_knots=G_KNOTS, tau_knots=T_KNOTS,
    table=TAB,
)
open(OUT + ('/g5_table_NOCAP_DIAGNOSTIC.json' if os.environ.get('RL_G5_NOCAP')=='1' else '/g5_table_LANDED.json'), 'w').write(json.dumps(art, indent=1, sort_keys=True) + '\n')
_fn = OUT + ('/g5_table_NOCAP_DIAGNOSTIC.json' if os.environ.get('RL_G5_NOCAP')=='1' else '/g5_table_LANDED.json')
NEWMD5 = hashlib.md5(open(_fn, 'rb').read()).hexdigest()
P("\nwrote %s  md5=%s" % (_fn, NEWMD5))

# ---------------- printed surface + the before/after against the frozen-lam pass ----------------
OLD = json.load(open(HERE + '/g5_table.json'))['table']
P("\n" + "=" * 116)
P("THE SOLVED SURFACE  G(cls, pick, cumulative games, tau)   [frozen-lam pass in brackets]")
P("=" * 116)
dmax = 0.0
for cls in CLASSES:
    P("\n  class %s" % cls)
    P("    %-6s %-7s %s" % ("pick", "games", "  ".join("tau=%-14d" % t for t in T_KNOTS)))
    for pk in PK_KNOTS:
        for gk in G_KNOTS:
            v = TAB[cls][str(pk)][str(gk)]; o = OLD[cls][str(pk)][str(gk)]
            dmax = max(dmax, max(abs(a - b) for a, b in zip(v, o)))
            fl = "".join('P' if RAW[(cls, pk, gk, t)]['pooled'] else '.' for t in T_KNOTS)
            P("    %-6d %-7d %s   [%s]"
              % (pk, gk, "  ".join("%.4f (%.4f)" % (a, b) for a, b in zip(v, o)), fl))
P("\n  [ P = node POOLED over the three retention classes (own-class eff-n < 35) ; . = class-resolved ]")
P("  largest single-knot move from the frozen-lam pass: %.6f" % dmax)
P("  max G anywhere on the shipped surface: %.6f"
  % max(max(max(vv) for vv in byg.values()) for byp in TAB.values() for byg in byp.values()))
open(OUT + '/consistency_log.txt', 'w').write("\n".join(log) + "\n")
