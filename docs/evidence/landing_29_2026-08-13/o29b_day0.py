#!/usr/bin/env python3
"""ORDER 29B -- STEP 4: THE PRINTED-DAY-0 ASSERT. THE P12 HARNESS, RE-POINTED AS DECLARED.

THIS IS o29_day0.py's POPULATION AND STRUCTURE. Exactly one thing moves, and PREREG_29B section 0.3
declared it before any wiring was written: the COMPARAND. ORDER 29's harness compared the printed
day-0 to `curve[pick]` -- the POSITION-BLIND all-in ladder -- because that was the only day-0 number
anything could be compared to when nothing consumed the positional object. ORDER 29B consumes the
positional object, so the comparand is the ROW'S OWN derived v0:

    ND in-curve entrant  ->  nd_v0.posv[gfut][pick]
    pool entrant         ->  pool_v0.cells['<pathway>|<position>']

BOTH READINGS ARE PRINTED, ALWAYS. The legacy position-blind reading is NOT dropped -- it is reported
beside the new one on every run, so the re-point is a NUMBER a reader can check rather than a sentence
he has to trust. PREREG_29B P29B-3 predicts the legacy reading stays 0 of 46 in both directions,
because relat_g(p) != 1 at essentially every (position, pick); the reconciliation
SUM_g share_g(p)*posv_g(p) = curve(p) is a POPULATION identity, never a per-row one.

CURRENCY. Both day-0 objects are published ALREADY ANCHORED (posv is built on the SHIPPED ladder, which
is raw x s; the cells carry x anchor_factor == s), so the numeraire is inside them and the printed
board value is round(derived v0) exactly. Tolerance: 0. See PREREG_29B section 0.2.

  usage: python3 o29b_day0.py <board.json> [label] [--assert]
         --assert  => exit non-zero unless the identity is N of N on the wired population
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BOARD = sys.argv[1] if len(sys.argv) > 1 else ROOT + '/engine/rl_after/rl_app_data.json'
LABEL = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else os.path.basename(BOARD)
HARD = '--assert' in sys.argv

LOG = []
def P(s=''):
    print(s); LOG.append(s)

b = json.load(open(BOARD))
art = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
curve = {int(k): int(v) for k, v in art['curve'].items()}
NUM = art['numeraire']
POSV = art['nd_v0']['posv']
CELLS = art['pool_v0']['cells']
SIGN = art['pool_v0'].get('cell_signature') or {}

P("=" * 118)
P("ORDER 29B  --  STEP 4 / P12 RE-POINTED: THE PRINTED-DAY-0 ASSERT      [%s]" % LABEL)
P("=" * 118)
P()
P("  board            %s   md5 %s" % (os.path.basename(BOARD), hashlib.md5(open(BOARD, 'rb').read()).hexdigest()))
P("  artifact         curve_md5 %s   unsigned_cells %s" % (art['curve_md5'], art['pool_v0']['unsigned_cells']))
P("  numeraire        s %.16f   head %.10f   pin %.1f"
  % (NUM['s'], NUM['pooled_head_pre_scale'], NUM['published_pin']))

rows = b['active']

# ---- THE POPULATION. o29_day0.py:36-37 verbatim for the ND half; the pool half is the same
#      cg==0 predicate on the rows the ND clause does not reach.
fresh = [r for r in rows if (r.get('cg') or 0) == 0 and r.get('ty') == 'ND'
         and r.get('pk') and 1 <= int(r['pk']) <= 64]
zero = [r for r in rows if (r.get('cg') or 0) == 0]
pool = [r for r in zero if r not in fresh]
assert fresh, 'no fresh entrants found — the assert would be vacuous'

def cell_of(r):
    ty = r.get('ty')
    path = 'RD' if ty == 'RD' else ('ND>64' if ty == 'ND' else ty)
    return '%s|%s' % (path, r['gf'])

def derived(r):
    """The row's OWN derived day-0 v0, board currency."""
    if r in fresh: return float(POSV[r['gf']][str(int(r['pk']))])
    return CELLS.get(cell_of(r))

P()
P("  POPULATION (P12's own definition, o29_day0.py:36-37, unchanged):")
P("     fresh ND entrants (cg==0, ty ND, pick 1..64)   %d" % len(fresh))
P("     pool entrants     (cg==0, everything else)     %d" % len(pool))
P("     wired population                               %d" % len(zero))

# ================================================================= READING 1: THE NEW IDENTITY
P()
P("  READING 1 -- THE IDENTITY THIS ACT DELIVERS:  printed == round(derived v0 x numeraire)")
P("  %-28s %-5s %6s %10s %14s %10s" % ('row', 'pos', 'pick', 'printed', 'derived v0', 'diff'))
nd_ok = nd_bad = 0; badrows = []
for r in sorted(fresh, key=lambda x: int(x['pk'])):
    d = derived(r); pr = r['v']; ok = (pr == int(round(d)))
    if ok: nd_ok += 1
    else: nd_bad += 1; badrows.append((r['key'], pr, d))
    P("  %-28s %-5s %6d %10d %14.4f %10d %s"
      % (r['key'], r['gf'], int(r['pk']), pr, d, pr - int(round(d)), '' if ok else '   *** MISMATCH ***'))
P()
P("  %-28s %-5s %6s %10s %14s %10s" % ('row', 'pathway', 'pos', 'printed', 'derived v0', 'diff'))
pl_ok = pl_bad = 0
for r in sorted(pool, key=lambda x: (cell_of(x), x['key'])):
    c = cell_of(r); d = derived(r); pr = r['v']
    if d is None:
        pl_bad += 1; badrows.append((r['key'], pr, None))
        P("  %-28s %-8s %-4s %10d %14s" % (r['key'], c, r['gf'], pr, 'UNSIGNED')); continue
    ok = (pr == int(round(d)))
    if ok: pl_ok += 1
    else: pl_bad += 1; badrows.append((r['key'], pr, d))
    P("  %-28s %-8s %-4s %10d %14.4f %10d %s%s"
      % (r['key'], c, r['gf'], pr, d, pr - int(round(d)),
         '[BORROWED] ' if SIGN.get(c) == 'borrowed' else '', '' if ok else '*** MISMATCH ***'))

P()
P("  " + "=" * 108)
P("  IDENTITY, ND FRESH ENTRANTS (the P12 population)      %d of %d" % (nd_ok, len(fresh)))
P("  IDENTITY, POOL ENTRANTS                               %d of %d" % (pl_ok, len(pool)))
P("  IDENTITY, WIRED POPULATION                            %d of %d" % (nd_ok + pl_ok, len(zero)))
P("  TOLERANCE 0 -- an exact integer equality, not a band. Mismatches: %d" % len(badrows))
P("  " + "=" * 108)

# ================================================================= READING 2: THE LEGACY, KEPT VISIBLE
P()
P("  READING 2 -- THE LEGACY POSITION-BLIND READING, KEPT VISIBLE (PREREG_29B P29B-3).")
P("  ORDER 29's harness compared printed to curve[pick]. That comparison is NOT the identity this act")
P("  delivers and is NOT expected to hold; it is printed so the declared re-point is auditable.")
legacy_ok = [r for r in fresh if r['v'] == curve[int(r['pk'])]]
ratios = [r['v'] / float(curve[int(r['pk'])]) for r in fresh if curve[int(r['pk'])]]
P("     printed == curve[pick] exactly:  %d of %d" % (len(legacy_ok), len(fresh)))
P("     ratio printed/all-in ladder:     min %.4f   max %.4f   mean %.4f"
  % (min(ratios), max(ratios), sum(ratios) / len(ratios)))
P("     (ORDER 29 measured on the ENTRY board: 0 of 46, min 0.3166 max 0.9037 mean 0.5274)")

# ---- the positional relativity IS the whole difference between the two readings, stated as a number
rel = [(r['key'], int(r['pk']), r['gf'], derived(r) / float(curve[int(r['pk'])])) for r in fresh
       if curve[int(r['pk'])]]
_r = [x[3] for x in rel]
P()
P("     WHY THE TWO READINGS CANNOT BOTH BE 46 of 46: posv/curve = relat_g(pick), measured over these")
P("     46 rows at min %.4f  max %.4f  mean %.4f. It is 1.0 on %d of 46 rows."
  % (min(_r), max(_r), sum(_r) / len(_r), sum(1 for x in _r if abs(x - 1.0) < 1e-12)))

# ================================================================= E6, re-asserted unchanged
P()
P("  E6 COHERENCE, re-asserted on the artifact the board was built from (o29_day0.py:79-84 verbatim):")
P("     published_pin / pooled_head_pre_scale = %.16f" % (NUM['published_pin'] / NUM['pooled_head_pre_scale']))
P("     published s                           = %.16f" % NUM['s'])
P("     |difference|                          = %.3e   (_load_numeraire HALTs above 1e-9)"
  % abs(NUM['published_pin'] / NUM['pooled_head_pre_scale'] - NUM['s']))
assert abs(NUM['published_pin'] / NUM['pooled_head_pre_scale'] - NUM['s']) < 1e-9

tag = LABEL.replace('/', '_')
open(HERE + '/DAY0_29B_%s_out.txt' % tag, 'w').write("\n".join(LOG) + "\n")
json.dump({'label': LABEL, 'board': os.path.basename(BOARD),
           'board_md5': hashlib.md5(open(BOARD, 'rb').read()).hexdigest(),
           'n_fresh_nd': len(fresh), 'n_pool': len(pool), 'n_wired': len(zero),
           'identity_nd': nd_ok, 'identity_pool': pl_ok, 'identity_all': nd_ok + pl_ok,
           'mismatches': [{'key': k, 'printed': p, 'derived': d} for k, p, d in badrows],
           'legacy_positionblind_ok': len(legacy_ok),
           'legacy_ratio': {'min': min(ratios), 'max': max(ratios), 'mean': sum(ratios) / len(ratios)},
           'relat_over_population': {'min': min(_r), 'max': max(_r), 'mean': sum(_r) / len(_r)},
           'rows': [{'key': r['key'], 'ty': r.get('ty'), 'pos': r['gf'], 'pick': r.get('pk'),
                     'cell': (None if r in fresh else cell_of(r)),
                     'printed': r['v'], 'derived_v0': derived(r)} for r in zero]},
          open(HERE + '/DAY0_29B_%s.json' % tag, 'w'), indent=1)

if HARD and (nd_ok + pl_ok) != len(zero):
    raise SystemExit('ORDER 29B PRINTED-DAY-0 IDENTITY FAILED: %d of %d' % (nd_ok + pl_ok, len(zero)))
