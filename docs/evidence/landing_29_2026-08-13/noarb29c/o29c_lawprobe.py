"""ORDER 29C — THE LANDED-ENTRY-LAW PROBE. Measurement only; writes no store, fits nothing.

WHAT THIS IS FOR. ORDER 29C re-bases the cohort no-arb instruments' YEAR-0 column from the frozen
fitted surface (`emit_matrix_338.py:252` writes `v0 = v0_start(p)`) onto the LANDED ENTRY LAW that
commit `13cbebb` wired into `ev()`. This probe does three things, all of them BEFORE the emit and
BEFORE any instrument is run, so that `PREREG_29C.md` can table its per-arm predictions from
measured artifact values rather than from guesses:

  1. REPLICATES the landed law's arithmetic as a standalone function `landed_v0_board(p)` and PROVES
     the replication against the board's own printed day-0 numbers -- the 89 rows of
     DAY0_29B_FINAL.json, board 36d5dfc7, `printed` vs `int(round(landed_v0_board(p)))`, TOLERANCE 0.
  2. Walks the STANDING EMITTER'S OWN POPULATION (same eligibility, same dedup, same force-majeure
     exclusion) and reports, per arm: n, the OLD basis year-0 mean (`v0_start`, engine currency) and
     the LANDED-LAW year-0 mean (board currency x _PL_F, engine currency), plus the count of rows the
     law cannot map.
  3. Reports the ladder-vs-surface comparison for the in-curve ND population, which is the only
     quantity `PREREG_29C` (c) can honestly predict a direction from.

WHAT THE LAW IS, quoted from `_merged_recover.py` (the ORDER 29B block) rather than paraphrased:
    day0_v0(p):  p['_pool']                      -> float(MA.pool_v0_of(p))      # pathway|gfut cell
                 type ND and 1 <= pick <= 64      -> float(posv[MA.gfut(p)][pick])
                 otherwise                        -> None
    ev(day-0 entrant, Y) = day0_v0(p) * _PL_F   (BOARD -> ENGINE currency; the numeraire s is ALREADY
                                                 inside both published objects)
    printed = int(round(ev / _F))  and  _F == _PL_F, so  printed == int(round(day0_v0(p))).

THE POSITION KEY IS AS-OF-INVARIANT, and that is why this re-basis is well defined for a historical
entrant. `MA.gfut(p)` reads `p['_futpos']` (the settled future position) or `_pos_present(p)` =
`GRP[p['_pos_now']] or GRP[p['pos']]` -- all three are STORE COLUMNS, never scoring-derived. The
walk-forward truncates `p['scoring']`; it does not touch those columns. So the law's day-0 position
for a 2004 entrant is the same object it is for a 2025 entrant, read from the same field, and no
day-0 position has to be reconstructed or borrowed. This is measured below (`gfut_source` census),
not asserted.

READ-ONLY on the engine and on the store.
"""
import os, sys, io, contextlib, json, hashlib, statistics
from collections import Counter, defaultdict

REPO = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
WORKDIR = os.environ.get('RL_WORKDIR', '/home/claude/rl_workspace/rl_after')
VENDOR = os.environ.get('RL_VENDOR', REPO + '/vendor')
sys.path.insert(0, VENDOR)
os.chdir(WORKDIR)
sys.path.insert(0, '.')
OUT = os.environ.get('RL_OUT', os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT, exist_ok=True)
DAY0 = os.environ['RL_DAY0_FINAL']          # docs/.../DAY0_29B_FINAL.json — the board's own printed day-0

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_noarb29c_probe'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; ev = G['ev']; delisted = G['delisted']; v0_start = G['v0_start']
META = G['_V0CURVE_META']; _PL_F = G['_PL_F']; _isreal = G['_isreal']
_V2J = G['_V2J']

STORE_MD5 = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()[:8]
ENGINE_HEAD = hashlib.md5(open('_merged_recover.py', 'rb').read()).hexdigest()[:8]
ART_MD5 = hashlib.md5(open('pvc_curve_v2.json', 'rb').read()).hexdigest()[:8]

# ---- THE LAW, replicated from the artifact exactly as the 29B block reads it -----------------------
_POSV = {g: {int(k): float(v) for k, v in d.items()} for g, d in _V2J['nd_v0']['posv'].items()}
_PV0 = _V2J['pool_v0']
_AF = float(_PV0['anchor_factor'])
_CURVE = {int(k): float(v) for k, v in _V2J['curve'].items()}

def landed_v0_board(p):
    """The row's OWN derived day-0 v0 in BOARD currency, by the ORDER 29B law. None => not an entrant
    object under the law, exactly as `day0_v0` returns None and the legacy chain keeps the row."""
    if p.get('_pool'):
        return float(MA.pool_v0_of(p))
    _pk = p.get('pick')
    if p.get('type') == 'ND' and _pk and 1 <= int(_pk) <= MA.ND_CURVE_LAST:
        _row = _POSV.get(MA.gfut(p))
        if _row is None:
            return None                       # position the artifact does not publish — counted, never defaulted
        return float(_row[int(_pk)])
    return None

def landed_v0_engine(p):
    b = landed_v0_board(p)
    return None if b is None else b * _PL_F

# ---- 1. THE REPLICATION PROOF, against the board's own printed day-0 numbers -----------------------
d0 = json.load(open(DAY0))
by_key = {p.get('key'): p for p in MA.data}
rep_ok = rep_bad = 0; rep_mis = []
for row in d0['rows']:
    p = by_key.get(row['key'])
    if p is None:
        rep_bad += 1; rep_mis.append((row['key'], 'NOT IN STORE', None, None)); continue
    mine_board = landed_v0_board(p)
    mine_print = None if mine_board is None else int(round(mine_board))
    if mine_print == row['printed'] and mine_board is not None \
       and abs(mine_board - row['derived_v0']) == 0.0:
        rep_ok += 1
    else:
        rep_bad += 1
        rep_mis.append((row['key'], row['printed'], mine_print, mine_board))
print("REPLICATION vs board %s: %d of %d EXACT (tolerance 0, on BOTH printed int AND the unrounded "
      "derived_v0)" % (d0['board_md5'][:8], rep_ok, len(d0['rows'])))
if rep_mis:
    print("  MISMATCHES: %s" % rep_mis[:10])

# ---- 2. THE STANDING EMITTER'S POPULATION, rebuilt identically ------------------------------------
FORCE_MAJEURE = {'thomas-boyd': 2013, 'paddy-mccartin': 2014}
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p) and p.get('key') not in FORCE_MAJEURE]
best = {}
for p in players:
    k = (p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))
    if k not in best or len(p['scoring']) > len(best[k]['scoring']): best[k] = p
players = list(best.values())
players = [p for p in players if p.get('year') is not None]
print("population: %d records (the standing emitter's own eligibility + dedup + force-majeure cut)"
      % len(players))

# gfut source census — the evidence that no day-0 position has to be reconstructed
src_ct = Counter('_futpos' if p.get('_futpos') else ('_pos_now' if p.get('_pos_now') else 'pos')
                 for p in players)
print("gfut source census (ALL store columns, none scoring-derived, so as-of invariant): %s"
      % dict(src_ct))

rows = []
unmappable = []
for p in players:
    b = landed_v0_board(p)
    if b is None:
        unmappable.append(dict(key=p.get('key'), player=p.get('player'), type=p.get('type'),
                               pick=p.get('pick'), pickless=bool(p.get('_pickless')),
                               pool=bool(p.get('_pool')), pos=MA.gfut(p)))
    rows.append(dict(key=p.get('key'), type=p.get('type'), year=p.get('year'),
                     pool=bool(p.get('_pool')), pick=p.get('pick'), pos=MA.gfut(p),
                     old_v0=round(v0_start(p), 1),
                     new_v0=(None if b is None else round(b * _PL_F, 1)),
                     new_v0_board=(None if b is None else b)))
print("UNMAPPABLE under the landed law: %d of %d" % (len(unmappable), len(rows)))
if unmappable:
    print("  by type: %s" % Counter(u['type'] for u in unmappable).most_common())
    print("  first 15: %s" % [(u['key'], u['type'], u['pick'], u['pickless']) for u in unmappable[:15]])

def arm_of(r):
    if r['type'] == 'ND' and not r['pool']: return 'ND 1-64'
    if r['type'] == 'ND': return 'ND>64'
    return r['type']

by_arm = defaultdict(list)
for r in rows: by_arm[arm_of(r)].append(r)
arm_tab = []
print()
print("PER-ARM YEAR-0 MEANS — OLD BASIS (v0_start, the frozen surface) vs LANDED LAW")
print("  %-8s %6s %12s %12s %8s %8s" % ("arm", "n", "old mean v0", "new mean v0", "ratio", "unmap"))
for a in sorted(by_arm, key=lambda x: -len(by_arm[x])):
    rs = by_arm[a]
    o = [r['old_v0'] for r in rs]
    n = [r['new_v0'] for r in rs if r['new_v0'] is not None]
    um = sum(1 for r in rs if r['new_v0'] is None)
    mo = statistics.mean(o) if o else float('nan')
    mn = statistics.mean(n) if n else float('nan')
    arm_tab.append(dict(arm=a, n=len(rs), old_mean_v0=round(mo, 2), new_mean_v0=round(mn, 2),
                        ratio=(round(mo / mn, 4) if n and mn else None), unmappable=um,
                        old_median=round(statistics.median(o), 2) if o else None,
                        new_median=round(statistics.median(n), 2) if n else None))
    print("  %-8s %6d %12.2f %12.2f %8s %8d"
          % (a, len(rs), mo, mn, ("%.3f" % (mo / mn)) if n and mn else "n/a", um))

# ---- 3. LADDER vs SURFACE on the in-curve ND population (the ONLY honest input to prereg (c)) -----
nd = [r for r in rows if r['type'] == 'ND' and not r['pool'] and r['new_v0'] is not None]
rel = [(r['new_v0_board'] / (_CURVE[int(r['pick'])] or 1.0)) for r in nd if r['pick']]
print()
print("ND in-curve: n=%d  landed/old mean ratio %.4f  median %.4f"
      % (len(nd),
         statistics.mean([r['old_v0'] for r in nd]) / statistics.mean([r['new_v0'] for r in nd]),
         statistics.median([r['old_v0'] for r in nd]) / statistics.median([r['new_v0'] for r in nd])))
print("ND positional relativity posv[g][pick]/curve[pick] over the in-curve ND rows: "
      "min %.4f max %.4f mean %.4f  (== 1.0 on %d rows)"
      % (min(rel), max(rel), statistics.mean(rel), sum(1 for x in rel if x == 1.0)))

n_zero = sum(1 for r in rows if r['new_v0'] == 0)
n_zero_old = sum(1 for r in rows if r['old_v0'] == 0)
print("year-0 == 0 rows: LANDED LAW %d   OLD BASIS %d   (the all-arm instrument excludes v0 <= 0, so a "
      "zero is a POPULATION change and is counted here rather than discovered later)" % (n_zero, n_zero_old))
if n_zero:
    print("  zero-v0 rows under the law: %s"
          % [(r['key'], r['type'], r['pos'], r['pick']) for r in rows if r['new_v0'] == 0][:20])

# THE PER-ROW MAP: written so PREREG_29C can table EXACT predicted denominators from committed inputs
# (the 29B matrix + this artifact) rather than approximations. Keyed exactly as the matrix records are.
json.dump({'%s|%s|%s' % (r['key'], r['type'], r['year']): r['new_v0'] for r in rows},
          open(os.path.join(OUT, 'LANDED_V0_29C.json'), 'w'), indent=0)

json.dump(dict(meta=dict(store=STORE_MD5, engine_head=ENGINE_HEAD, artifact=ART_MD5,
                         PL_F=_PL_F, anchor_factor=_AF, board_probed=d0['board_md5'],
                         v0surf_sig=META.get('_v0surf_sig'),
                         v0surf_frozen=bool(META.get('_v0surf_frozen'))),
               replication=dict(ok=rep_ok, bad=rep_bad, n=len(d0['rows']), mismatches=rep_mis),
               population=len(rows), unmappable=unmappable,
               gfut_source_census=dict(src_ct), by_arm=arm_tab,
               n_zero_new_v0=n_zero, n_zero_old_v0=n_zero_old,
               nd_relativity=dict(n=len(rel), min=min(rel), max=max(rel),
                                  mean=statistics.mean(rel),
                                  n_equal_1=sum(1 for x in rel if x == 1.0))),
          open(os.path.join(OUT, 'LAWPROBE_29C.json'), 'w'), indent=1)
print()
print("store=%s engine=%s artifact=%s _PL_F=%.6f anchor_factor=%.16f"
      % (STORE_MD5, ENGINE_HEAD, ART_MD5, _PL_F, _AF))
print("wrote %s" % os.path.join(OUT, 'LAWPROBE_29C.json'))
