"""ORDER 26A -- THE BRIDGE. Read-only.

Reconciles the two "yr4/yr0" figures in the ORDER 25 packet to ZERO RESIDUAL:

    o25_derive.py yr4()            RD 1.379793   ALL POOL 1.338050   NATIONAL 1.554717
    noarb_table_allarm.py by-arm   RD 0.5090     (PRIMARY window, n=623)

Both are read off the SAME landed matrix per_entrant_O25R4.json. Neither instrument is
modified and neither is imported for its answer: both are RE-IMPLEMENTED here, verbatim
from their sources, so each bridge step can be toggled independently. The re-implementations
are CONTROL-CHECKED against the two instruments' own published outputs before any step is
taken -- if a control fails, nothing below it is readable.

    usage: python o26a_bridge.py <matrix.json> <out.json>
"""
import sys, json, os, hashlib, statistics, collections

MATRIX = sys.argv[1]
OUTJS = sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))

L = []
def P(s=''):
    print(s); L.append(s)

def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()

M = json.load(open(MATRIX))
R = M['recs']
meta = M['meta']

# ---------------------------------------------------------------------------------------
# THE TWO INSTRUMENTS' SHARED PRIMITIVES (identical source text in both files)
# ---------------------------------------------------------------------------------------
def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)

def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t

ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']

elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]

# WINDOW END -- both files derive it identically (max year with a non-null vpath entry)
W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

# ---------------------------------------------------------------------------------------
# THE ENTRY-PRICE OBJECTS. derive's anchor_of() reproduced verbatim from o25_derive.py.
# ---------------------------------------------------------------------------------------
_V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = _V2['pool_levels']
IN_FLAT = dict(CUR['signed_flat']); IN_RD = dict(CUR['signed_rd_positional'])
IN_ND65 = float(CUR['signed_nd65_plus']['measured_k15'])
PL_F = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])
LEVI = {k: int(float(v)) for k, v in IN_FLAT.items()}
LEVI['ND65+'] = int(IN_ND65)
for k, v in IN_RD.items(): LEVI['RD:' + k] = int(float(v))

def division(r):
    t = r.get('type')
    if t == 'RD': return 'RD:' + r['pos']
    if t == 'ND': return 'ND65+'
    return t

def anchor_of(r):
    if r.get('is_pool_engine'):
        d = division(r)
        if d in LEVI: return LEVI[d] * PL_F
    return float(r['v0'])

def v0_of(r):
    return float(r['v0'])

# ---------------------------------------------------------------------------------------
# THE TWO YEAR KEYS, kept textually distinct so H3 is MEASURED and not assumed
# ---------------------------------------------------------------------------------------
def ykey_derive(r):
    """o25_derive.py:yr4() -- Y = cohort(r) + 3"""
    return cohort(r) + 3

def ykey_allarm(r, N=4):
    """noarb_table_allarm.py:value_at() -- Y = cohort(r) + N - 1"""
    return cohort(r) + N - 1

# ---------------------------------------------------------------------------------------
# THE TWO ROW SEMANTICS
# ---------------------------------------------------------------------------------------
def sem_derive(r, Y):
    """o25_derive.py:yr4() branch structure, verbatim.
       returns (kind, value) ; kind 'skip' means the ENTRY LEAVES THE DENOMINATOR."""
    if Y > W: return ('skip_notyet', None)
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return ('zero_noyrs', 0.0)
    if Y < yrs[0]: return ('skip_pre', None)
    if Y > yrs[-1]: return ('zero_ended', 0.0)
    i = yrs.index(Y); v = vp[i]
    return ('zero_null', 0.0) if v is None else ('path', float(v))

def sem_allarm(r, Y):
    """noarb_table_allarm.py:value_at() + the `reached` filter, verbatim."""
    if Y > W: return ('skip_notyet', None)          # the `reached` filter drops it entirely
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return ('zero_ended', 0.0)
    if Y < yrs[0]: return ('skip_pre', None)        # 'pre' -> excluded from BOTH mean and mean_v0
    if Y > yrs[-1]: return ('zero_ended', 0.0)
    i = yrs.index(Y); v = vp[i]
    return ('zero_null', 0.0) if v is None else ('path', float(v))

# ---------------------------------------------------------------------------------------
# THE GENERIC READER -- every knob the bridge turns, in one place
# ---------------------------------------------------------------------------------------
def read(pop, ykey='derive', sem='derive', agg='sumsum', den='anchor', collect=False):
    YK = ykey_derive if ykey == 'derive' else ykey_allarm
    SM = sem_derive if sem == 'derive' else sem_allarm
    DN = anchor_of if den == 'anchor' else v0_of
    vals, dens, rows = [], [], []
    for r in pop:
        Y = YK(r)
        kind, v = SM(r, Y)
        if v is None:
            if collect: rows.append((r['key'], Y, kind, None, None))
            continue
        vals.append(v); dens.append(DN(r))
        if collect: rows.append((r['key'], Y, kind, v, DN(r)))
    if not vals: return (float('nan'), 0, rows)
    if agg == 'sumsum':
        d = sum(dens); ratio = (sum(vals) / d) if d else float('nan')
    else:
        m0 = statistics.mean(dens); ratio = (statistics.mean(vals) / m0) if m0 else float('nan')
    return (ratio, len(vals), rows)

# =======================================================================================
P("=" * 118)
P("ORDER 26A -- THE BRIDGE.  matrix=%s (%s)  store=%s  v0surf=%s  window_end=%d"
  % (os.path.basename(MATRIX), md5(MATRIX)[:8], meta['store_md5'][:8], meta['v0surf_sig'][:12], W))
P("=" * 118)
P("  eligible rows: %d of %d" % (len(elig), len(R)))
P("  _PL_F = %.4f   signed RD positional levels: %s"
  % (PL_F, "  ".join("%s %d" % (k, LEVI['RD:' + k]) for k in sorted(IN_RD))))
P()

# ---- the two populations -----------------------------------------------------------------
POP_DERIVE_RD = [r for r in elig if stream(r) == 'RD']
POP_ALLARM_RD = [r for r in elig if r['type'] == 'RD' and 2005 <= cohort(r) <= 2023]
POP_DERIVE_POOL = [r for r in elig if stream(r) in ORDER]
POP_DERIVE_ND = [r for r in elig if not r.get('is_pool_engine') and r.get('type') == 'ND'
                 and r.get('raw_pick') and 1 <= r['raw_pick'] <= 64]
POP_ALLARM_ND = [r for r in elig if r['type'] == 'ND' and 2005 <= cohort(r) <= 2023]

# =======================================================================================
P("-" * 118)
P("CONTROL 0 -- the re-implementations reproduce BOTH published instruments before any step")
P("-" * 118)
CTRL = {}
c_derive_rd, n1, _ = read(POP_DERIVE_RD, 'derive', 'derive', 'sumsum', 'anchor')
c_derive_pool, n2, _ = read(POP_DERIVE_POOL, 'derive', 'derive', 'sumsum', 'anchor')
c_derive_nd, n3, _ = read(POP_DERIVE_ND, 'derive', 'derive', 'sumsum', 'anchor')
c_allarm_rd, n4, _ = read(POP_ALLARM_RD, 'allarm', 'allarm', 'meanmean', 'v0')
c_allarm_nd, n5, _ = read(POP_ALLARM_ND, 'allarm', 'allarm', 'meanmean', 'v0')
for nm, got, want, tol in [('derive RD      ', c_derive_rd, 1.379793, 5e-7),
                           ('derive ALL POOL', c_derive_pool, 1.338050, 5e-7),
                           ('derive NATIONAL', c_derive_nd, 1.554717, 5e-7),
                           ('allarm RD      ', c_allarm_rd, 0.5090, 5e-5),
                           ('allarm ND      ', c_allarm_nd, 1.4803, 5e-5)]:
    ok = abs(got - want) <= tol
    P("  %s  reimplemented %.9f   published %.6f   %s" % (nm, got, want, 'PASS' if ok else '*** FAIL ***'))
    assert ok, "CONTROL FAILED for %s" % nm
    CTRL[nm.strip()] = dict(reimplemented=got, published=want)
P("  CONTROL PASS -- both instruments reproduced. Everything below is readable.")
P()

# =======================================================================================
# H3 MEASURED, NOT ASSUMED: the year keys, row by row
# =======================================================================================
P("-" * 118)
P("H3 -- YEAR INDEXING, MEASURED ROW BY ROW over all %d eligible rows" % len(elig))
P("-" * 118)
diffY = [(r['key'], ykey_derive(r), ykey_allarm(r)) for r in elig if ykey_derive(r) != ykey_allarm(r)]
P("  rows where derive's cohort+3 differs from allarm's cohort+N-1 at N=4 : %d" % len(diffY))
P("  both keys resolve to the SAME calendar year for every eligible row." if not diffY else
  "  DIFFERING ROWS: %s" % diffY[:10])
P()

# =======================================================================================
# THE RD BRIDGE -- one knob at a time, in the PRE-REGISTERED order
# =======================================================================================
P("=" * 118)
P("THE RD BRIDGE -- allarm 0.5090  ->  derive 1.379793.  Steps in the PRE-REGISTERED order.")
P("=" * 118)
STEPS = []
state = dict(pop='allarm', ykey='allarm', sem='allarm', agg='meanmean', den='v0')

def cur(st, collect=False):
    pop = POP_ALLARM_RD if st['pop'] == 'allarm' else POP_DERIVE_RD
    return read(pop, st['ykey'], st['sem'], st['agg'], st['den'], collect)

r0, n0, _ = cur(state)
P("  %-2s %-46s %12s %6s %12s" % ('#', 'state', 'reading', 'n_in', 'delta'))
P("  " + "-" * 92)
P("  %-2s %-46s %12.6f %6d %12s" % ('0', 'ALLARM AS PUBLISHED (pop/idx/sem/agg/den)', r0, n0, '--'))
STEPS.append(dict(step=0, name='allarm as published', knob=None, reading=r0, n=n0, delta=None,
                  cause='baseline'))

PLAN = [('P', 'pop',  'derive', 'POPULATION: cohort window 2005-2023 -> all eligible cohorts'),
        ('I', 'ykey', 'derive', 'YEAR INDEXING: N=4 (cohort+N-1) -> cohort+3'),
        ('S', 'sem',  'derive', 'SKIP/ZERO SEMANTICS: allarm branches -> derive branches'),
        ('A', 'agg',  'sumsum', 'AGGREGATION: mean/mean -> sum/sum'),
        ('D', 'den',  'anchor', "ENTRY-PRICE OBJECT: r['v0'] -> anchor_of(r) = signed level x _PL_F")]
prev = r0
for tag, knob, val, desc in PLAN:
    state[knob] = val
    rn, nn, _ = cur(state)
    P("  %-2s %-46s %12.6f %6d %+12.6f" % (tag, desc[:46], rn, nn, rn - prev))
    STEPS.append(dict(step=tag, name=desc, knob=knob, value=val, reading=rn, n=nn,
                      delta=rn - prev, cause=desc.split(':')[0]))
    prev = rn

TARGET = c_derive_rd
resid = prev - TARGET
P("  " + "-" * 92)
P("  %-2s %-46s %12.6f %6d %12s" % ('=', 'DERIVE AS PUBLISHED', TARGET, n1, ''))
P("  RESIDUAL (bridge end - derive reading) = %.3e   %s"
  % (resid, 'ZERO (< 1e-9)' if abs(resid) < 1e-9 else '*** UNEXPLAINED ***'))
P()

# =======================================================================================
# H1 -- THE SURVIVING ENTRY SHARE, measured on the derive population and derive semantics
# =======================================================================================
P("-" * 118)
P("H1 -- SURVIVOR BIAS THROUGH THE SKIP BRANCHES. The owner's numeric check: if the 1.38 is")
P("      survivors-over-their-own-entry, the SURVIVING ENTRY SHARE must be ~ 0.509/1.380 = 36.9%.")
P("-" * 118)
H1 = {}
for nm, pop, den in [('RD (derive pop, anchor den)', POP_DERIVE_RD, 'anchor'),
                     ('RD (derive pop, v0 den)', POP_DERIVE_RD, 'v0'),
                     ('ALL POOL (derive pop, anchor den)', POP_DERIVE_POOL, 'anchor'),
                     ('NATIONAL (derive pop, v0=anchor)', POP_DERIVE_ND, 'anchor')]:
    DN = anchor_of if den == 'anchor' else v0_of
    tot = sum(DN(r) for r in pop)
    kinds = collections.Counter()
    kept = alive = 0.0
    n_kept = n_alive = 0
    for r in pop:
        k, v = sem_derive(r, ykey_derive(r))
        kinds[k] += 1
        if v is not None:
            kept += DN(r); n_kept += 1
            if v > 0: alive += DN(r); n_alive += 1
    P("  %-34s  n=%4d  entry total %12s" % (nm, len(pop), format(round(tot), ',')))
    P("      branch census: %s" % dict(kinds))
    P("      entry KEPT in the denominator (not skipped) : %12s   share %6.2f%%  (n=%d)"
      % (format(round(kept), ','), 100.0 * kept / tot, n_kept))
    P("      entry of rows scoring a NON-ZERO mark        : %12s   share %6.2f%%  (n=%d)"
      % (format(round(alive), ','), 100.0 * alive / tot, n_alive))
    H1[nm] = dict(n=len(pop), entry_total=tot, entry_kept=kept, kept_share_pct=100.0 * kept / tot,
                  n_kept=n_kept, entry_nonzero=alive, nonzero_share_pct=100.0 * alive / tot,
                  n_nonzero=n_alive, branch_census=dict(kinds))
P()

# =======================================================================================
# H2 -- THE NUMERATORS, ROW BY ROW
# =======================================================================================
P("-" * 118)
P("H2 -- THE VALUE OBJECT. Are the two instruments reading the SAME number at the SAME year?")
P("-" * 118)
common = [r for r in POP_ALLARM_RD]
nd_ = na_ = 0; mismatch = []
for r in common:
    kd, vd = sem_derive(r, ykey_derive(r))
    ka, va = sem_allarm(r, ykey_allarm(r))
    if (vd is None) != (va is None) or (vd is not None and vd != va):
        mismatch.append((r['key'], kd, vd, ka, va))
P("  rows compared (allarm RD population, n=%d)" % len(common))
P("  numerator mismatches between the two instruments: %d" % len(mismatch))
if mismatch: P("    %s" % mismatch[:10])
P("  -> both read vpath[i] for the SAME calendar year; the NUMERATOR is byte-identical."
  if not mismatch else "  -> numerators DIFFER")
P()

json.dump(dict(matrix=os.path.basename(MATRIX), matrix_md5=md5(MATRIX), store=meta['store_md5'],
               window_end=W, PL_F=PL_F, levels_int=LEVI, controls=CTRL,
               h3_year_key_diff_rows=len(diffY), bridge=STEPS, residual=resid,
               derive_target=TARGET, h1=H1, h2_numerator_mismatches=len(mismatch),
               pops=dict(derive_RD=len(POP_DERIVE_RD), allarm_RD=len(POP_ALLARM_RD),
                         derive_POOL=len(POP_DERIVE_POOL), derive_ND=len(POP_DERIVE_ND),
                         allarm_ND=len(POP_ALLARM_ND))),
          open(OUTJS, 'w'), indent=1, default=float)
open(OUTJS.replace('.json', '_out.txt'), 'w').write('\n'.join(L) + '\n')
P("wrote %s" % OUTJS)
