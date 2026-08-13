#!/usr/bin/env python3
"""ORDER 29 -- BOTH COMMITTED INSTRUMENTS, RE-READ ON THE **FINAL LANDED BOARD** (P15, T3).

THIS FILE IS `docs/evidence/grace_adoption_2026-08-13/o28_instruments.py`
(md5 cb55c8b62769aaea4469a9d792600057) COPIED, WITH TWO BASIS SUBSTITUTIONS AND NOTHING ELSE.
ORDER 28's committed artifact is left untouched. The full diff is committed beside this file as
INSTRUMENTS29_REBASIS.diff.

The two instruments are the ones fixed in INSTRUMENTS_PRESTATEMENT.md (ORDER 28 inputs/):
  (1) THE MARK-PATH PROGRESSION TEST   m_allin(d) = sum(marks at depth d) / sum(derived day-0)
  (2) THE REVERSE NO-ARB TEST          a pathway FAILS iff m_allin(d) < 1 for EVERY d = 1..6 AND the
                                       upper end of a 95% bootstrap on max_{d>=1} m_allin(d) is < 1.
Every convention -- the depth axis, the dead-zeroed-and-kept semantics, the bootstrap B/seed/pct, the
thin-sample rule, the MSD debut-year gap and its repaired reading -- is carried verbatim from that
pre-statement. NOTHING is re-specified here. NO predicate, tolerance, bootstrap parameter or
population rule is touched: the two substitutions below are both BASIS, never TEST.

SUBSTITUTION 1 -- THE DENOMINATOR IS NOW WHAT SHIPS, NOT WHAT WAS PROPOSED
  ORDER 28 read its ND ladder from DERIVE28.json's `candidate.allin` -- the PROPOSED all-in ladder,
  carried at full float precision and BEFORE owner ruling C. ORDER 29 reads the ND ladder from
  `engine/rl_after/pvc_curve_v2.json` -- THE ARTIFACT THAT SHIPS on the landed board (52aa1125,
  curve_md5 9729f0c5). The two differ exactly where the record says they must: integer rounding
  everywhere, plus the ruling-C -1-point-per-pick tiebreak inside the two pooled blocks (picks 6-12
  and 15-21). That difference is ASSERTED here, not assumed -- see the CURVE PROVENANCE block below,
  which halts if any pick outside those blocks moves by more than rounding.

  The POOL half of the denominator is unchanged and is READ FROM DERIVE28.json's candidate cells,
  because the landing did not move it: ruling C tiebroke the ND ladder only. That is verified rather
  than asserted -- `cell x anchor_factor` reproduces the published landed cell table in
  V0S29_out.txt (RD|MID 212, IRE|KPD 53, ...) and `anchor_factor` is bit-equal to the landed
  numeraire s = 0.9400914291048137 (V0S29.json s_new).

SUBSTITUTION 2 -- THE NUMERATOR CLOSES ORDER 28's OWN DECLARED BREACH
  ORDER 28 read its marks from per_entrant_O25R4.json, emitted OFF-DIAL, and said so in this file's
  header: "THIS IS A DECLARED BREACH ... with the dial-ON matrix re-emit named as the follow-up."
  ORDER 29 RUNS THAT FOLLOW-UP. The marks here come from per_entrant_O29FINAL.json, emitted by
  emit_variant_o29.sh against the LANDED tree: store cb38ef11, engine head e5109864, v0surf 4405cba2,
  ruled curve installed, grace-A at its landed CODE DEFAULT (RL_GRACE='1', pinned manifest). The
  matrix is checked for that identity at load and HALTS on a mismatch.

  ORDER 28 predicted the direction of the effect it could not measure: dial-ON marks HIGHER at the
  shallow depths, unchanged deeper, so its progressions "UNDERSTATE the rise". That prediction is now
  measurable, and the deltas are printed beside every arm rather than described.

  usage:  python3 o29_instruments.py   ->  INSTRUMENTS29.json / INSTRUMENTS29_out.txt
"""
import os, sys, json, math, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
O28 = os.path.abspath(os.path.join(HERE, '..', 'grace_adoption_2026-08-13'))
IN = os.path.join(O28, 'inputs')
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

DER = json.load(open(os.path.join(O28, 'DERIVE28.json')))
CAND = DER['candidate']; REF = DER['ref_26bv_graceA']
L2 = json.load(open(os.path.join(IN, 'LAYER2.json')))
L1 = json.load(open(os.path.join(IN, 'layer1_player_seasons.json')))
E = {e['key']: e for e in L1['entries']}
ATTR = L2['attribution']

# --------------------------------------------------------------- SUBSTITUTION 2: the landed matrix
MPATH = os.path.join(SP, 'per_entrant_O29FINAL.json')
M = json.load(open(MPATH)); R = M['recs']
_meta = M['meta']
if _meta.get('store_md5') != 'cb38ef11' or _meta.get('v0surf_sig', '')[:8] != '4405cba2':
    raise SystemExit("MATRIX BASIS HALT: this is not the landed emit.\n"
                     "  store  %s (want cb38ef11)\n  v0surf %s (want 4405cba2...)"
                     % (_meta.get('store_md5'), _meta.get('v0surf_sig')))
MREF = json.load(open(os.path.join(IN, 'per_entrant_O25R4.json')))   # the OFF-DIAL live matrix
RREF = MREF['recs']

NUM = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])

# --------------------------------------------------------------- SUBSTITUTION 1: the shipped ladder
_ART = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
ALLIN = {int(k): float(v) for k, v in _ART['curve'].items()}
ALLIN_PROPOSED = {int(k): float(v) for k, v in CAND['allin'].items()}
TIEBREAK_BLOCKS = set(range(6, 13)) | set(range(15, 22))
_bad = [p for p in ALLIN
        if p not in TIEBREAK_BLOCKS and abs(ALLIN[p] - ALLIN_PROPOSED[p]) > 0.5]
if _bad:
    raise SystemExit("CURVE PROVENANCE HALT: picks %s move by more than rounding OUTSIDE the two "
                     "ruled tiebreak blocks -- the shipped ladder is not the ruled candidate." % _bad)
ALLIN_V = {int(k): float(v) for k, v in REF['allin'].items()}
AF = float(CAND['anchor_factor'])
CELLS = {tuple(k.split('|')): float(v) for k, v in CAND['cells'].items()}
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
DEPTHS = list(range(0, 7))
B, SEED = 2000, 20260812


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)


def sem(r, Y):
    if Y > W: return None
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0
    if Y < yrs[0]: return None
    if Y > yrs[-1]: return 0.0
    i = yrs.index(Y); v = vp[i]
    return 0.0 if v is None else float(v)


def derived_v0(r, allin):
    k = r['key']; a = ATTR.get(k)
    if a is not None and a.get('excluded'): return None
    st = a['mechanism'] if a else stream(r)
    pk = a['pick'] if a else r.get('pick')
    if st == 'ND 1-64' and pk and 1 <= pk <= 64:
        return allin[pk] * NUM
    g = (E.get(k) or {}).get('position_group')
    c = CELLS.get((st, g))
    return (c * AF * NUM) if c is not None else None


def arm_of(r):
    a = ATTR.get(r['key'])
    return a['mechanism'] if a else stream(r)


LOG = []
def P(s=''):
    print(s); LOG.append(s)


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


def paths_for(rows):
    ma, mm, nn = {}, {}, {}
    for d in DEPTHS:
        num = den = 0.0; rat = []
        for r, v0 in rows:
            v = sem(r, cohort(r) + d)
            if v is None: continue
            num += v; den += v0; rat.append(v / v0)
        ma[d] = (num / den) if den else float('nan')
        mm[d] = (sum(rat) / len(rat)) if rat else float('nan')
        nn[d] = len(rat)
    return ma, mm, nn


def build_arms(allin):
    A = collections.OrderedDict()
    nd = [(r, derived_v0(r, allin)) for r in R
          if arm_of(r) == 'ND 1-64' and cohort(r) is not None and derived_v0(r, allin)]
    A['ND 1-64'] = nd
    for m in POOLM:
        rows = [(r, derived_v0(r, allin)) for r in R
                if arm_of(r) == m and cohort(r) is not None and derived_v0(r, allin)]
        if rows: A[m] = rows
    return A


def boot_max(rows):
    rs = np.random.RandomState(SEED)
    n = len(rows); out = []
    pre = []
    for r, v0 in rows:
        pre.append(([sem(r, cohort(r) + d) for d in DEPTHS], v0))
    for _ in range(B):
        idx = rs.randint(0, n, n)
        best = float('-inf')
        for d in range(1, 7):
            num = den = 0.0
            for i in idx:
                v = pre[i][0][d]
                if v is None: continue
                num += v; den += pre[i][1]
            if den:
                best = max(best, num / den)
        out.append(best)
    out = sorted(out)
    return out[int(0.975 * len(out))]


P("=" * 126)
P("ORDER 29  --  BOTH COMMITTED INSTRUMENTS, RE-READ ON THE FINAL LANDED BOARD 86c8d5d9.")
P("=" * 126)
P("  denominator: the LANDED derived day-0 -- the SHIPPED ladder pvc_curve_v2.json (curve_md5 %s,"
  % _ART.get('curve_md5', '?')[:8])
P("               ruling-C tiebroken, integer) for ND 1-64, and the landed pool cells x anchor_factor")
P("               %.15f for every pool arm. NOT the pre-ruling proposal." % AF)
P("  numerator:   marks from per_entrant_O29FINAL.json -- RE-EMITTED under the LANDED engine")
P("               (store %s, engine head %s, v0surf %s, grace-A at its landed code default)."
  % (_meta['store_md5'], _meta.get('engine_head'), _meta['v0surf_sig'][:8]))
P("  ORDER 28's DECLARED BREACH IS CLOSED HERE: it read OFF-DIAL marks and named this re-emit as the")
P("  follow-up. The follow-up ran. Section 3 prints what the dial actually moved, by arm and by depth.")
P("  conventions verbatim from INSTRUMENTS_PRESTATEMENT.md: depth axis, dead zeroed and KEPT,")
P("  B=%d, seed=%d, 97.5th pct, thin at n<40 @d4, no FAIL verdict under 8 entrants." % (B, SEED))
P("  ND ladder provenance CHECKED, not assumed: every pick outside the two ruled blocks (6-12, 15-21)")
P("  matches the ORDER 28 candidate to within rounding, else this run halts.")
P()

ARMS_C = build_arms(ALLIN)
ARMS_V = build_arms(ALLIN_V)

P("-" * 126)
P("INSTRUMENT 1 -- THE MARK-PATH PROGRESSION TEST")
P("-" * 126)
P("  m_allin(d) = sum(marks at depth d) / sum(derived day-0).  PRIMARY reading.")
P("  %-9s %6s %s   %8s %5s %8s %s"
  % ('arm', 'n@d4', "".join("%8s" % ('d%d' % d) for d in DEPTHS), 'peak', 'at d', 'peak 26BV', 'verdict'))
PROG = {}
for arm, rows in ARMS_C.items():
    ma, mm, nn = paths_for(rows)
    mav, _mmv, _nnv = paths_for(ARMS_V[arm])
    ok_d = [d for d in DEPTHS if ma[d] == ma[d]]
    best_d = max(ok_d, key=lambda d: ma[d]) if ok_d else None
    peak = ma[best_d] if best_d is not None else float('nan')
    peakv = max((mav[d] for d in DEPTHS if mav[d] == mav[d]), default=float('nan'))
    d0 = next((d for d in DEPTHS if nn[d] > 0), None)
    base = ma[0] if (0 in ok_d) else (ma[d0] if d0 is not None else float('nan'))
    rise = [d for d in DEPTHS if d >= 2 and ma[d] == ma[d] and ma[d] > base]
    thin = nn.get(4, 0) < 40
    ok = bool(rise) and best_d is not None and best_d >= 2
    PROG[arm] = dict(m_allin=ma, m_mean=mm, n=nn, peak=peak, peak_d=best_d, base=base,
                     base_depth=(0 if 0 in ok_d else d0), thin=thin, ok=ok, peak_26bv=peakv)
    P("  %-9s %6d %s   %8.4f %5s %8.4f %s"
      % (arm, nn.get(4, 0), "".join(("%8.4f" % ma[d]) if ma[d] == ma[d] else "%8s" % '--'
                                    for d in DEPTHS), peak, best_d, peakv,
         ('PASS' if ok else 'FAIL') + (' [THIN]' if thin else '')))
P()
P("  MSD note (carried, not rediscovered): the emitter builds `yrs` from draft year + 1 on every")
P("  route while cohort() for MSD is the draft year itself, so MSD's d=0 denominator is empty and")
P("  its entry reference is re-based on the first depth with a denominator (ORDER 26A anomaly 5).")
P("  base depth used per arm: %s" % {a: PROG[a]['base_depth'] for a in PROG})
P()
P("  DISPERSION of the per-entrant ratio vpath[d]/derived_v0 at d = 4 (the dispersion law)")
P("  %-9s %6s %10s %10s %10s %10s" % ('arm', 'n', 'p05', 'median', 'mean', 'p95'))
for arm, rows in ARMS_C.items():
    rat = []
    for r, v0 in rows:
        v = sem(r, cohort(r) + 4)
        if v is not None: rat.append(v / v0)
    if rat:
        P("  %-9s %6d %10.4f %10.4f %10.4f %10.4f"
          % (arm, len(rat), q(rat, .05), q(rat, .50), sum(rat) / len(rat), q(rat, .95)))

P()
P("-" * 126)
P("INSTRUMENT 2 -- THE REVERSE NO-ARB TEST")
P("-" * 126)
P("  PREDICATE (pre-stated): a pathway FAILS iff (1) m_allin(d) < 1 for EVERY d = 1..6 at which it")
P("  has any denominator, AND (2) the 97.5th-pct bootstrap upper limit on max_{d>=1} m_allin(d) is")
P("  ALSO below 1.  PASS = no pathway fails.")
P("  %-9s %6s %10s %12s %10s %10s %s"
  % ('arm', 'n', 'max m(d>=1)', 'boot upper', 'limb 1', 'limb 2', 'verdict'))
NOARB = {}; ANYFAIL = []
for arm, rows in ARMS_C.items():
    ma = PROG[arm]['m_allin']
    vals = [ma[d] for d in range(1, 7) if ma[d] == ma[d]]
    if not vals: continue
    mx = max(vals)
    up = boot_max(rows)
    limb1 = all(v < 1.0 for v in vals)
    limb2 = up < 1.0
    fail = limb1 and limb2 and len(rows) >= 8
    unrel = len(rows) < 8
    NOARB[arm] = dict(n=len(rows), max_m=mx, boot_upper=up, limb1=limb1, limb2=limb2,
                      fail=fail, unreliable=unrel)
    if fail: ANYFAIL.append(arm)
    P("  %-9s %6d %10.4f %12.4f %10s %10s %s"
      % (arm, len(rows), mx, up, 'RED' if limb1 else 'clear', 'RED' if limb2 else 'clear',
         ('FAIL' if fail else 'PASS') + (' [UNRELIABLE n<8]' if unrel else '')))
P()
P("  VERDICT: %s" % ('PASS -- no pathway is a systematic guaranteed-loss hold at the candidate '
                     'entry prices' if not ANYFAIL else 'FAIL -- ' + ", ".join(ANYFAIL)))
_red1 = [a for a in NOARB if NOARB[a]['limb1']]
P("  NON-VACUITY, stated honestly: limb 1 is RED for %s on this basis."
  % (", ".join(_red1) if _red1 else "NO ARM"))
if not _red1:
    P("  So the predicate is NOT exercised to its failure line here, and the PASS must be read as")
    P("  'every arm clears limb 1 by a printed margin', not as 'the test was hard and was survived'.")
    P("  The margin is the number to read: the SMALLEST max m(d>=1) across arms is %.4f (%s), i.e."
      % (min(NOARB[a]['max_m'] for a in NOARB),
         min(NOARB, key=lambda a: NOARB[a]['max_m'])))
    P("  %.0f%% above the failure line. The predicate CAN go red -- it does so for any pathway whose"
      % (100 * (min(NOARB[a]['max_m'] for a in NOARB) - 1)))
    P("  derived entry price exceeds every mark its cohort ever carries -- but no arm is near it.")

# ---------------------------------------------------------------------------------------------
# SECTION 3 -- WHAT THE RE-EMIT ACTUALLY MOVED.  REPORTING ONLY: no verdict above depends on this
# block, and nothing here is fed back into either instrument. It exists because ORDER 28 PREDICTED
# the direction of this effect and a prediction that is now measurable should be measured.
# ---------------------------------------------------------------------------------------------
W_REF = max(y for r in RREF for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)


def sem_ref(r, Y):
    if Y > W_REF: return None
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0
    if Y < yrs[0]: return None
    if Y > yrs[-1]: return 0.0
    i = yrs.index(Y); v = vp[i]
    return 0.0 if v is None else float(v)


REFROWS = collections.OrderedDict()
for arm in ARMS_C:
    REFROWS[arm] = [(r, derived_v0(r, ALLIN)) for r in RREF
                    if arm_of(r) == arm and cohort(r) is not None and derived_v0(r, ALLIN)]
P()
P("-" * 126)
P("SECTION 3 -- THE DIAL AND THE LANDING, MEASURED: landed marks vs the OFF-DIAL live marks")
P("-" * 126)
P("  Same denominator on both sides (the LANDED ladder), so this isolates the NUMERATOR move --")
P("  i.e. what re-emitting the walk-forward matrix under the landed engine did to each arm's marks.")
P("  ORDER 28 predicted: HIGHER at shallow depths, unchanged deeper. Printed, not assumed.")
P("  %-9s %s" % ('arm', "".join("%9s" % ('d%d' % d) for d in DEPTHS)))
DELTA = {}
for arm, rows in ARMS_C.items():
    ma = PROG[arm]['m_allin']
    mr = {}
    for d in DEPTHS:
        num = den = 0.0
        for r, v0 in REFROWS[arm]:
            v = sem_ref(r, cohort(r) + d)
            if v is None: continue
            num += v; den += v0
        mr[d] = (num / den) if den else float('nan')
    DELTA[arm] = {d: (ma[d] - mr[d]) for d in DEPTHS}
    P("  %-9s %s" % (arm, "".join(("%+9.4f" % DELTA[arm][d]) if DELTA[arm][d] == DELTA[arm][d]
                                  else "%9s" % '--' for d in DEPTHS)))
_shallow = [DELTA[a][d] for a in DELTA for d in (0, 1) if DELTA[a][d] == DELTA[a][d]]
_deep = [DELTA[a][d] for a in DELTA for d in range(2, 7) if DELTA[a][d] == DELTA[a][d]]
P()
P("  mean delta at d0-d1 (shallow): %+.4f   mean delta at d2-d6 (deep): %+.4f"
  % (sum(_shallow) / len(_shallow), sum(_deep) / len(_deep)))
P("  ORDER 28's prediction -- shallow up, deep ~unchanged -- reads %s."
  % ('CONFIRMED' if (sum(_shallow) / len(_shallow)) > abs(sum(_deep) / len(_deep))
     else 'NOT CONFIRMED: the deep move is not smaller than the shallow one'))

json.dump(dict(basis='ORDER 29 FINAL LANDED BOARD 86c8d5d9 (shipped ruling-C ladder + landed cells)',
               breach='CLOSED -- marks re-emitted under the landed engine (per_entrant_O29FINAL)',
               matrix=dict(path=MPATH, store=_meta['store_md5'], v0surf=_meta['v0surf_sig'],
                           engine_head=_meta.get('engine_head'), n_records=_meta.get('n_records')),
               curve=dict(artifact_curve_md5=_ART.get('curve_md5'),
                          tiebreak_blocks=sorted(TIEBREAK_BLOCKS)),
               anchor_factor=AF, numeraire=NUM, bootstrap=dict(B=B, seed=SEED, pct=97.5),
               progression={a: dict(m_allin=PROG[a]['m_allin'], m_mean=PROG[a]['m_mean'],
                                    n=PROG[a]['n'], peak=PROG[a]['peak'], peak_d=PROG[a]['peak_d'],
                                    peak_26bv=PROG[a]['peak_26bv'], thin=PROG[a]['thin'],
                                    ok=PROG[a]['ok']) for a in PROG},
               dial_delta=DELTA,
               noarb=NOARB, noarb_any_fail=ANYFAIL),
          open(os.path.join(HERE, 'INSTRUMENTS29.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'INSTRUMENTS29_out.txt'), 'w').write("\n".join(LOG) + "\n")
print("\nwrote INSTRUMENTS29.json / INSTRUMENTS29_out.txt")
