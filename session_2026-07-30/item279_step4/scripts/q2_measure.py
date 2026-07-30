"""#279 step 4 — Q2 REHEARSAL MEASUREMENT: the three dual-position candidates for per-season par teaching.

Commissioned by the seam's word Q2 (2026-07-30): measure all three, each with group populations
before/after, which groups would empty, par-surface deltas, curve deltas. Present with a recommendation;
the OWNER rules before the execution word.

The three candidates are each grounded in an EXISTING engine law, not invented here:
  CURRENT : pos = MA.gfut(p) once per career          -- today's code, par_build.gather():50
  A PRIMARY: the primary component of the season's dual ('SF/MID' -> 'SF')
            -- futblend's own law: "The PRIMARY keys peak/curve/runway/key-premium"
  B LOWER  : the pair's LOWER replacement bar ('SF/MID' -> whichever of SF,MID has lower REPL)
            -- the eligibility-collapse law R105.1 / _collapse_elig, which the year-0 bar already applies
  C EXCLUDE: dual seasons do not teach the par at all

Nothing here is wired, adopted, or committed to the engine. Report-only.
"""
import os, sys, io, json, contextlib, collections, importlib.util
import numpy as np

OUT = sys.argv[1]
FV  = os.environ['RL_FV']

with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m

if FV not in sys.path: sys.path.insert(0, FV)
PB = _load('pb', os.path.join(FV, 'par_build.py'))
CP = PB.CP

GROUPS = PB.GROUPS
TEN_MAX = PB.TEN_MAX

# ---------------- the four keying rules ----------------
def key_current(p, r):
    return MA.gfut(p)

def _primary(s):
    return MA.GRP.get(s.split('/')[0])

def key_primary(p, r):
    return _primary(r['pos'])

def key_lower(p, r):
    s = r['pos']
    if '/' not in s: return MA.GRP.get(s)
    a, b = s.split('/', 1)
    ga, gb = MA.GRP.get(a), MA.GRP.get(b)
    if ga is None or gb is None: return ga or gb
    # LOWER replacement bar of the pair — the engine's own eligibility-collapse rule
    return gb if MA.REPL.get(gb, 1e9) < MA.REPL.get(ga, 1e9) else ga

def key_exclude(p, r):
    s = r['pos']
    if '/' in s: return None          # dual seasons do not teach
    return MA.GRP.get(s)

RULES = [('CURRENT_gfut', key_current), ('A_PRIMARY', key_primary),
         ('B_LOWER_REPL', key_lower), ('C_EXCLUDE_DUALS', key_exclude)]

# ---------------- gather(), parameterised by the keying rule ----------------
def gather_with(keyfn):
    """par_build.gather() with the observation key supplied. Everything else is carried verbatim:
    the same pool filter, the same tenure window, the same base-rate gate, the same _lvl_wt target."""
    pool = [p for p in MA.data if MA.GRP.get(p.get('pos'))
            and (p.get('pick') or p.get('_ft')) and PB.DRAFT_LO <= PB.draftyr(p) <= PB.DRAFT_HI]
    raw, dropped = [], 0
    for p in pool:
        pk = min(MA.effpk(p), CP.KMAX); d0 = PB.draftyr(p)
        for T in range(1, TEN_MAX + 1):
            Y = d0 + T; r = PB.season_row(p, Y); g = r['games'] if r else 0
            if g > 0:
                pos = keyfn(p, r)
                if pos is None:
                    dropped += 1
                    continue
                raw.append((pos, pk, T, Y, g, p))
    base = {}
    bycell = collections.defaultdict(list)
    for pos, pk, T, Y, g, p in raw: bycell[(pos, T)].append(g)
    for k, v in bycell.items(): base[k] = float(np.median(v))
    obs = []
    for pos, pk, T, Y, g, p in raw:
        if g >= PB.MIN_GAMES:
            obs.append((pos, np.log(pk), T, CP._lvl_wt(p, Y)))
    return obs, base, raw, dropped

# ---------------- run each rule ----------------
results = {}
fits = {}
for name, fn in RULES:
    obs, base, raw, dropped = gather_with(fn)
    by_group = collections.Counter(o[0] for o in obs)
    by_cell  = collections.Counter((o[0], int(o[2])) for o in obs)
    empty_groups = [g for g in GROUPS if by_group.get(g, 0) == 0]
    empty_cells  = [[g, T] for g in GROUPS for T in range(1, TEN_MAX + 1) if by_cell.get((g, T), 0) == 0]
    results[name] = {
        'obs_rows': len(obs), 'raw_rows': len(raw), 'dropped_unmappable': dropped,
        'by_group': {g: by_group.get(g, 0) for g in GROUPS},
        'EMPTY_GROUPS': empty_groups,
        'empty_cells_pos_x_tenure': empty_cells,
        'n_empty_cells': len(empty_cells),
    }
    # fit the par surface under this keying
    _orig = PB.gather
    PB.gather = (lambda _f=fn: (lambda: gather_with(_f)[:3][0:3]))()
    PB.gather = (lambda _f=fn: (lambda: tuple(gather_with(_f)[:3])))()
    try:
        F = PB.fit()
        fits[name] = F
        results[name]['fit'] = 'OK'
    except Exception as e:
        fits[name] = None
        results[name]['fit'] = 'RAISED %s: %s' % (type(e).__name__, e)
    finally:
        PB.gather = _orig

# ---------------- par-surface deltas vs CURRENT ----------------
EVAL_PICKS = PB.EVAL_PICKS
base_F = fits['CURRENT_gfut']
for name, _ in RULES:
    F = fits.get(name)
    if F is None or base_F is None: continue
    diffs, cells = [], {}
    for g in GROUPS:
        for pk in EVAL_PICKS:
            for T in (1, 3, 6):
                try:
                    a = PB.par_at(base_F, g, pk, T); b = PB.par_at(F, g, pk, T)
                except Exception:
                    continue
                if a == a and b == b:
                    diffs.append(b - a)
                    cells['%s|pick%d|T%d' % (g, pk, T)] = round(b - a, 3)
    if diffs:
        arr = np.array(diffs)
        results[name]['par_delta_vs_current'] = {
            'n_cells': len(diffs),
            'mean': round(float(arr.mean()), 4),
            'median': round(float(np.median(arr)), 4),
            'max_abs': round(float(np.abs(arr).max()), 4),
            'pct_cells_moved': round(100.0 * float((np.abs(arr) > 1e-9).mean()), 2),
        }
        results[name]['par_delta_sample'] = dict(sorted(cells.items(), key=lambda kv: -abs(kv[1]))[:12])

results['_meta'] = {
    'cohort': 'DRAFT %d-%d (par_build locked Decision A)' % (PB.DRAFT_LO, PB.DRAFT_HI),
    'note': 'par_build cohort window is 2003-2018 and is SEPARATE from the curve teaching class cut (<=2022). '
            'Not to be conflated.',
    'REPL': {k: v for k, v in MA.REPL.items()},
    'store_md5_expected': '6b9d00a7',
}
json.dump(results, open(OUT, 'w'), indent=1)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'empty_cells_pos_x_tenure'}
                  for k, v in results.items() if k != '_meta'}, indent=1))
