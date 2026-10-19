#!/usr/bin/env python3
"""ORDER 26B-V -- THE GRACE-YEARS VARIANTS.  **MEASUREMENT ONLY. NOT RULED.**

Owner order #334 comment 5275831956 (2026-08-13). Delivers the FOUR-WAY MENU the owner asked for --
flat-14 (the operative C2 basis) / V5 / grace-A / grace-B -- with the full downstream re-derivation
under each: the loclin curve, the pre-anchor head, the anchor factor and premium, the positional
relativities, the pool ladders and pathway ND-pick equivalents, and the pooled derived-vs-printed and
derived-vs-anchor aggregates. Plus the HITS TABLE (the pick-1 cohort, per player) and the named rows.

Everything is identical to the operative C2 basis except the discount ladder: the loclin estimator,
the force-majeure slide and its asserts, window tiers, games weighting, K=15, bars, positions, tails.

The k-mapping and the two readings are fixed in PRESTATEMENT_26BV.md, committed and pushed BEFORE this
file existed. Reading O is primary; Reading L and the grace-0 diagnostic are reported beside it.

NOTHING LANDS. No board is built, no engine byte moves. The board-side twin -- a dial-gated grace
parameter inside rl_model.py::disc_factor -- is the follow-up act IF the owner likes what he sees, and
AT LANDING the identity gate forces both sides to move together (see PRESTATEMENT_26BV.md §4).

  usage:  python3 o26b_variants.py   ->  VARIANTS.json / VARIANTS_out.txt
"""
import os, sys, json, math, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
HARN_DIR = os.path.join(ROOT, 'docs', 'evidence', 'composition_2026-08-10', 'noarb')
sys.path.insert(0, HARN_DIR); sys.path.insert(0, HERE)
import harness_pvc_REPINNED_pass3 as HP
import o26b_loclin as LL

L2 = json.load(open(os.path.join(HERE, 'LAYER2.json')))
D0 = json.load(open(os.path.join(HERE, 'DERIVE.json')))
L1 = json.load(open(os.path.join(ROOT, 'data/delivered_value/layer1_player_seasons.json')))
E = {e['key']: e for e in L1['entries']}
ATTR = L2['attribution']; FM = L2['force_majeure']; GRACE = L2['grace_cfg']
MATRIX = os.path.join(HERE, 'per_entrant_O25R4.json')
if not os.path.exists(MATRIX):
    MATRIX = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/per_entrant_O25R4.json'
M = json.load(open(MATRIX)); R = M['recs']
NUM = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])
PVC = {int(k): float(v) for k, v in json.load(open(ROOT + '/engine/rl_after/rl_app_data.json'))['PVC'].items()}

PICKS = list(range(1, 65))
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
K_SHRINK = int(D0['pool']['K']); PIN1 = 3000.0
BANDS = HP.RANGES
HEADP = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 64]

# ---- the entry-price objects, verbatim from o26a_bridge.py (as o26b_compare.py carries them) ----
_V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = _V2['pool_levels']
LEVI = {k: int(float(v)) for k, v in dict(CUR['signed_flat']).items()}
LEVI['ND65+'] = int(float(CUR['signed_nd65_plus']['measured_k15']))
for k, v in dict(CUR['signed_rd_positional']).items(): LEVI['RD:' + k] = int(float(v))


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def anchor_of(r):
    if r.get('is_pool_engine'):
        d = ('RD:' + r['pos']) if r.get('type') == 'RD' else ('ND65+' if r.get('type') == 'ND'
                                                              else r.get('type'))
        if d in LEVI: return LEVI[d] * NUM
    return float(r['v0'])


def arm_of(r):
    a = ATTR.get(r['key'])
    return a['mechanism'] if a else None


POOLROWS_M = [r for r in R if arm_of(r) in POOLM and (r.get('v0') or 0) > 0 and cohort(r) is not None]
NDROWS_M = [r for r in R if arm_of(r) == 'ND 1-64' and (r.get('v0') or 0) > 0]

LOG = []
def P(s=''):
    print(s); LOG.append(s)


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


# ==================================================================================================
# THE FULL DOWNSTREAM RE-DERIVATION, PARAMETRIC IN THE SCORING
# ==================================================================================================
def derive(SC):
    """Everything downstream of a Layer-2 scoring, on the operative C2 basis."""
    nd = [dict(key=k, pick=ATTR[k]['pick'], value=SC[k]['total'], pos=E[k]['position_group'])
          for k in L2['fit_nd_keys']]
    # 26B-C1 asserts, still armed under every variant
    assert not (set(FM['excluded_keys']) & set(L2['fit_nd_keys'])), "26B-C1 (a) breached"
    raw, effn, dg = LL.kernel_loclin(nd, PICKS, HP.NMIN, HP.HMIN, HP.HMAX)   # 26B-C2 estimator
    head = raw[0]; af = PIN1 / head
    allin = {p: raw[i] * af for i, p in enumerate(PICKS)}
    # positional relativities + the Ruling-13 reconciliation assert
    share, rawpos = {}, {}
    posrows = {g: [r for r in nd if r['pos'] == g] for g in POSN}
    for g in POSN:
        ind = [dict(key=r['key'], pick=r['pick'], value=(1.0 if r['pos'] == g else 0.0)) for r in nd]
        s, _ = HP.kernel_raw(ind, PICKS)
        share[g] = {p: s[i] for i, p in enumerate(PICKS)}
    for p in PICKS:
        t = sum(share[g][p] for g in POSN)
        for g in POSN: share[g][p] = share[g][p] / t if t else 0.0
    for g in POSN:
        nm = min(HP.NMIN, max(8.0, len(posrows[g]) / 4.0))
        v, _e, _d = LL.kernel_loclin(posrows[g], PICKS, nm, HP.HMIN, HP.HMAX)
        rawpos[g] = {p: v[i] for i, p in enumerate(PICKS)}
    posv = {g: {} for g in POSN}
    for p in PICKS:
        nrm = sum(share[g][p] * rawpos[g][p] for g in POSN)
        for g in POSN:
            posv[g][p] = allin[p] * rawpos[g][p] / nrm if nrm else allin[p]
    recon = max(abs(sum(share[g][p] * posv[g][p] for g in POSN) / allin[p] - 1.0) for p in PICKS)
    assert recon < 1e-12, "RULING 13 RECONCILIATION BREACHED under a variant: %.3e" % recon
    bands = {}
    for lo, hi in BANDS:
        ps = [p for p in PICKS if lo <= p <= hi]
        a = sum(allin[p] for p in ps) / len(ps)
        bands['%d-%d' % (lo, hi)] = {g: (sum(posv[g][p] for p in ps) / len(ps)) / a for g in POSN}
    # pool ladders
    pool = [dict(key=k, mech=ATTR[k]['mechanism'], pos=E[k]['position_group'], value=SC[k]['total'])
            for k in L2['fit_pool_keys']]
    ap = sum(r['value'] for r in pool) / len(pool)
    lens = {}
    for g in POSN:
        sub = [r for r in pool if r['pos'] == g]
        lens[g] = (sum(r['value'] for r in sub) / len(sub) / ap) if sub and ap else 1.0
    path = {}
    for m in POOLM:
        sub = [r for r in pool if r['mech'] == m]
        n = len(sub); a = (sum(r['value'] for r in sub) / n) if n else 0.0
        w = n / float(n + K_SHRINK)
        path[m] = dict(n=n, raw=a, shrunk=w * a + (1 - w) * ap)
    cells = {}
    for m in POOLM:
        for g in POSN:
            sub = [r for r in pool if r['mech'] == m and r['pos'] == g]
            n = len(sub); w = n / float(n + K_SHRINK)
            own = (sum(r['value'] for r in sub) / n) if n else 0.0
            cells[(m, g)] = w * own + (1 - w) * path[m]['shrunk'] * lens[g]

    def nd_equiv(v):
        a = v * af
        if a >= allin[1]: return '<1'
        for p in PICKS:
            if allin[p] <= a: return str(p)
        return '>64'

    # pooled derived vs printed vs anchor
    def dv0(r):
        a = ATTR.get(r['key'])
        if a is None or a.get('excluded'): return None
        if a['mechanism'] == 'ND 1-64' and a['pick'] and 1 <= a['pick'] <= 64:
            return allin[a['pick']] * NUM
        c = cells.get((a['mechanism'], (E.get(r['key']) or {}).get('position_group')))
        return (c * af * NUM) if c is not None else None

    cmp_ = []
    for r in POOLROWS_M:
        d = dv0(r)
        if d is None: continue
        cmp_.append((arm_of(r), (E.get(r['key']) or {}).get('position_group'), d, float(r['v0']),
                     anchor_of(r)))
    agg_prn = sum(c[2] for c in cmp_) / sum(c[3] for c in cmp_)
    agg_anc = sum(c[2] for c in cmp_) / sum(c[4] for c in cmp_)
    bypos = {}
    for g in POSN:
        sub = [c for c in cmp_ if c[1] == g]
        if sub:
            bypos[g] = dict(n=len(sub), der_prn=q([c[2] / c[3] for c in sub], .5),
                            der_anch=q([c[2] / c[4] for c in sub], .5))
    bypath = {}
    for m in POOLM:
        sub = [c for c in cmp_ if c[0] == m]
        if sub:
            bypath[m] = dict(n=len(sub), derived=sum(c[2] for c in sub) / len(sub),
                             der_prn=q([c[2] / c[3] for c in sub], .5),
                             der_anch=q([c[2] / c[4] for c in sub], .5))
    return dict(head=head, anchor_factor=af, premium=af - 1.0, allin=allin, raw_curve=raw,
                bands=bands, recon=recon, pathways=path, all_pool=ap, lens=lens,
                nd_equiv={m: nd_equiv(path[m]['shrunk']) for m in POOLM},
                anchored_path={m: path[m]['shrunk'] * af for m in POOLM},
                cells={'%s|%s' % k: v for k, v in cells.items()},
                agg_der_prn=agg_prn, agg_der_anch=agg_anc, n_cmp=len(cmp_),
                by_pos=bypos, by_path=bypath,
                nd_mean=sum(r['value'] for r in nd) / len(nd),
                derived_v0={r['key']: dv0(r) for r in POOLROWS_M + NDROWS_M if dv0(r) is not None})


# ARM STATUS -- carried on the face of every table, never in a footnote.
STATUS = collections.OrderedDict([
    ('flat-14', 'OPERATIVE -- the live config and the basis of every 26B conclusion'),
    ('V5 [OFF]', 'RULED OFF 2026-08-13. OWNER: "don\'t worry about V5 for now - the XW change '
                 'addressed the issue and V5 on top would impact the live board a bit too much I '
                 'think." Kept in the menu as MEASURED CONTEXT only; it is not a live option.'),
    ('grace-A', 'NOT RULED -- live variant, measurement only'),
    ('grace-B', 'NOT RULED -- live variant, measurement only'),
])
ARMS = collections.OrderedDict([
    ('flat-14', L2['base']), ('V5 [OFF]', L2['v5']),
    ('grace-A', L2['grace_a']), ('grace-B', L2['grace_b'])])
EXTRA = collections.OrderedDict([
    ('grace-A (L)', L2['grace_a_readingL']), ('grace-B (L)', L2['grace_b_readingL']),
    ('grace-0 (diag)', L2['grace_zero'])])
DER = {k: derive(v) for k, v in ARMS.items()}
DERX = {k: derive(v) for k, v in EXTRA.items()}

# ==================================================================================================
P("=" * 122)
P("ORDER 26B-V  --  THE GRACE-YEARS VARIANTS.   **MEASUREMENT ONLY.  NOT RULED.**")
P("=" * 122)
P("  flat-14 on the C2 basis remains the OPERATIVE derivation. These are labelled Layer-2 re-runs.")
P("  order: #334 comment 5275831956.  forms and predictions: PRESTATEMENT_26BV.md (pushed first).")
P("  mechanism: %s" % GRACE['mechanism'])
P("  k-mapping: %s" % GRACE['k_convention'])
P("  READING O (PRIMARY):   %s" % GRACE['reading_O'])
P("  READING L (secondary): %s" % GRACE['reading_L'])
P("  everything else identical to C2: %s" % GRACE['everything_else'])
P()
P("  LANDING CONSTRAINT, recorded before the numbers: %s" % GRACE['landing_constraint'])
P()
P("-" * 122)
P("ARM STATUS -- carried on the face of the menu, not in a footnote")
P("-" * 122)
for a, s in STATUS.items():
    P("  %-10s %s" % (a, s))
P()

P("-" * 122)
P("1.  THE FOUR-WAY MENU")
P("-" * 122)
P("  %-26s %14s %14s %14s %14s" % ('metric', *ARMS.keys()))
P("  %-26s %14.1f %14.1f %14.1f %14.1f"
  % ('PRE-ANCHOR HEAD (pick 1)', *[DER[a]['head'] for a in ARMS]))
P("  %-26s %14.4f %14.4f %14.4f %14.4f"
  % ('ANCHOR FACTOR', *[DER[a]['anchor_factor'] for a in ARMS]))
P("  %-26s %13.1f%% %13.1f%% %13.1f%% %13.1f%%"
  % ('PICK-vs-PLAYER PREMIUM', *[100 * DER[a]['premium'] for a in ARMS]))
P("  %-26s %14.1f %14.1f %14.1f %14.1f"
  % ('ND cohort mean', *[DER[a]['nd_mean'] for a in ARMS]))
P("  %-26s %14.4f %14.4f %14.4f %14.4f"
  % ('pooled derived/printed', *[DER[a]['agg_der_prn'] for a in ARMS]))
P("  %-26s %14.4f %14.4f %14.4f %14.4f"
  % ('pooled derived/ANCHOR', *[DER[a]['agg_der_anch'] for a in ARMS]))
P("  %-26s %14.3e %14.3e %14.3e %14.3e"
  % ('reconciliation (assert)', *[DER[a]['recon'] for a in ARMS]))
P()
P("  THE ANCHORED CURVE (all four pinned at pick 1 = 3000, so this is SHAPE only)")
P("  %-14s %s" % ('pick', "".join("%8d" % p for p in HEADP)))
for a in ARMS:
    P("  %-14s %s" % (a, "".join("%8.0f" % DER[a]['allin'][p] for p in HEADP)))
P("  %-14s %s" % ('today PVC', "".join("%8.0f" % PVC[p] for p in HEADP)))
P()
for a in list(ARMS)[1:]:
    mx = max(abs(DER[a]['allin'][p] / DER['flat-14']['allin'][p] - 1) for p in PICKS)
    P("  max |%s / flat-14 - 1| across picks 1-64 (post-anchor SHAPE): %.4f (%.2f%%)"
      % (a, mx, 100 * mx))
P()
P("  PATHWAY ND-PICK EQUIVALENTS  (the '>64' threshold is each variant's own pick-64 value)")
P("  %-7s %10s %10s %10s %10s   %8s %8s %8s %8s" %
  ('path', *[a + ' v' for a in ARMS], *['eq ' + a[:5] for a in ARMS]))
for m in sorted(POOLM, key=lambda x: -DER['flat-14']['anchored_path'][x]):
    P("  %-7s %10.0f %10.0f %10.0f %10.0f   %8s %8s %8s %8s"
      % (m, *[DER[a]['anchored_path'][m] for a in ARMS], *[DER[a]['nd_equiv'][m] for a in ARMS]))
P("  pick-64 value: " + "  ".join("%s %.0f" % (a, DER[a]['allin'][64]) for a in ARMS))
P()
P("  POOLED derived/printed and derived/ANCHOR, BY DAY-0 POSITION (medians)")
P("  %-6s %s" % ('pos', "".join("%12s" % a for a in ARMS)))
for g in POSN:
    P("  %-6s %s" % (g + ' p', "".join("%12.4f" % DER[a]['by_pos'][g]['der_prn'] for a in ARMS)))
    P("  %-6s %s" % (g + ' a', "".join("%12.4f" % DER[a]['by_pos'][g]['der_anch'] for a in ARMS)))
P()
P("  BY PATHWAY, derived/ANCHOR (median) -- who gains and who loses under grace")
P("  %-7s %s   %s" % ('path', "".join("%12s" % a for a in ARMS), 'A/flat  B/flat'))
for m in POOLM:
    if m not in DER['flat-14']['by_path']: continue
    f = DER['flat-14']['by_path'][m]['der_anch']
    P("  %-7s %s   %6.3f  %6.3f"
      % (m, "".join("%12.4f" % DER[a]['by_path'][m]['der_anch'] for a in ARMS),
         DER['grace-A']['by_path'][m]['der_anch'] / f, DER['grace-B']['by_path'][m]['der_anch'] / f))

# ---- READING L and the grace-0 diagnostic -------------------------------------------------------
P()
P("-" * 122)
P("2.  READING L vs READING O, AND THE grace-0 DIAGNOSTIC  (the conflation, as a number)")
P("-" * 122)
P("  The order's formula (1.14)^-max(0, j-1-G) gives EVERY entrant one free year at G=0, which")
P("  collides with the owner's own 'Not mature age players'. Reading O honours both constraints;")
P("  Reading L is the formula taken literally. grace-0 isolates the universal shift alone.")
P("  %-16s %12s %12s %12s %12s %12s" %
  ('arm', 'head', 'factor', 'premium', 'der/anchor', 'der/printed'))
for a, d in list(DER.items()) + list(DERX.items()):
    P("  %-16s %12.1f %12.4f %11.1f%% %12.4f %12.4f"
      % (a, d['head'], d['anchor_factor'], 100 * d['premium'], d['agg_der_anch'], d['agg_der_prn']))
P()
P("  READING-CHOICE SENSITIVITY (L/O):  head %.4f / %.4f   pooled der/anchor %.4f / %.4f"
  % (DERX['grace-A (L)']['head'] / DER['grace-A']['head'],
     DERX['grace-B (L)']['head'] / DER['grace-B']['head'],
     DERX['grace-A (L)']['agg_der_anch'] / DER['grace-A']['agg_der_anch'],
     DERX['grace-B (L)']['agg_der_anch'] / DER['grace-B']['agg_der_anch']))

# ---- THE HITS TABLE -----------------------------------------------------------------------------
P()
P("-" * 122)
P("3.  THE HITS TABLE -- THE PICK-1 COHORT, PER PLAYER  (the owner's specific ask)")
P("-" * 122)
P("  entries 2004-2021 attributed to slid pick 1, after the force-majeure exclusion (26B-C1).")
P("  %-24s %6s %6s %11s %11s %11s %8s %8s" %
  ('key', 'entry', 'age', 'flat-14', 'grace-A', 'grace-B', 'A/flat', 'B/flat'))
P1 = sorted([k for k in L2['fit_nd_keys'] if ATTR[k]['pick'] == 1],
            key=lambda k: -L2['base'][k]['total'])
HITS = {}
for k in P1:
    b = L2['base'][k]['total']; a = L2['grace_a'][k]['total']; c = L2['grace_b'][k]['total']
    ea = E[k]['entry_age'] or E[k]['entry_age_fallback_if_null']
    HITS[k] = dict(entry=E[k]['entry_year'], age=ea, flat=b, gA=a, gB=c,
                   nat=ATTR[k]['natural_pick'], slid=ATTR[k]['slid'], nseasons=E[k]['n_season_rows'])
    P("  %-24s %6s %6s %11.1f %11.1f %11.1f %8s %8s"
      % (k, E[k]['entry_year'], ea, b, a, c,
         ("%.4f" % (a / b)) if b > 0 else '  --  ', ("%.4f" % (c / b)) if b > 0 else '  --  '))
_mean = lambda xs: sum(xs) / len(xs)
for lbl, arm in (('flat-14', 'base'), ('grace-A', 'grace_a'), ('grace-B', 'grace_b')):
    vs = [L2[arm][k]['total'] for k in P1]
    P("  %-24s cohort mean %10.1f   top %10.1f   top/mean %6.3f   zeros %d of %d"
      % (lbl, _mean(vs), max(vs), max(vs) / _mean(vs), sum(1 for v in vs if v <= 0), len(vs)))
_long = [k for k in P1 if E[k]['n_season_rows'] >= 8 and L2['base'][k]['total'] > 0]
_short = [k for k in P1 if E[k]['n_season_rows'] <= 2 and L2['base'][k]['total'] > 0]
P("  LONG careers (>=8 seasons, n=%d):  A/flat %.4f   B/flat %.4f"
  % (len(_long), _mean([L2['grace_a'][k]['total'] / L2['base'][k]['total'] for k in _long]),
     _mean([L2['grace_b'][k]['total'] / L2['base'][k]['total'] for k in _long])))
if _short:
    P("  SHORT careers (<=2 seasons, n=%d): A/flat %.4f   B/flat %.4f"
      % (len(_short), _mean([L2['grace_a'][k]['total'] / L2['base'][k]['total'] for k in _short]),
         _mean([L2['grace_b'][k]['total'] / L2['base'][k]['total'] for k in _short])))
P("  AND THE BUSTS: every zero stays exactly zero under every ladder -- a career with no above-bar")
P("  season scores 0 whatever the discount, so grace cannot move a bust by construction.")

# ---- NAMED ROWS ---------------------------------------------------------------------------------
P()
P("-" * 122)
P("4.  THE NAMED ROWS UNDER EACH VARIANT")
P("-" * 122)
NAMED = ['willem-duursma', 'callum-moore', 'harrison-ramm', 'vigo-visentini', 'jai-newcombe']
P("  %-18s %-7s %5s %11s %11s %11s   %11s %11s %11s" %
  ('key', 'path', 'age', 'deliv f14', 'deliv gA', 'deliv gB', 'v0 f14', 'v0 gA', 'v0 gB'))
NAMEDOUT = {}
for k in NAMED:
    e = E[k]; ea = e['entry_age'] or e['entry_age_fallback_if_null']
    d = [L2[a][k]['total'] for a in ('base', 'grace_a', 'grace_b')]
    v = [DER[a]['derived_v0'].get(k) for a in ARMS]
    v = [v[0], v[2], v[3]]
    NAMEDOUT[k] = dict(age=ea, mech=ATTR[k]['mechanism'], deliv=d, v0=v)
    P("  %-18s %-7s %5s %11.1f %11.1f %11.1f   %11s %11s %11s"
      % (k, ATTR[k]['mechanism'], ea, d[0], d[1], d[2],
         *["%.1f" % x if x else 'n/a' for x in v]))

OUT = dict(status='MEASUREMENT ONLY -- grace-A and grace-B NOT RULED; V5 RULED OFF 2026-08-13',
           arm_status=STATUS, grace_cfg=GRACE,
           menu={a: {kk: DER[a][kk] for kk in
                     ('head', 'anchor_factor', 'premium', 'allin', 'bands', 'recon', 'pathways',
                      'nd_equiv', 'anchored_path', 'agg_der_prn', 'agg_der_anch', 'by_pos',
                      'by_path', 'nd_mean', 'all_pool', 'cells')} for a in ARMS},
           reading_L={a: {kk: DERX[a][kk] for kk in
                          ('head', 'anchor_factor', 'premium', 'agg_der_prn', 'agg_der_anch')}
                      for a in DERX},
           hits=HITS, named=NAMEDOUT, pvc=PVC)
json.dump(OUT, open(os.path.join(HERE, 'VARIANTS.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'VARIANTS_out.txt'), 'w').write("\n".join(LOG) + "\n")
print("\nwrote VARIANTS.json / VARIANTS_out.txt")
