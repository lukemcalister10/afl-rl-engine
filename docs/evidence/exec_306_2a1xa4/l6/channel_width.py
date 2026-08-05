#!/usr/bin/env python3
"""#306 L6 — MEASURE THE FEED-BACK CHANNEL'S ACTUAL WIDTH.

WHY THIS EXISTS
  The rotation order (#306 comment 5185851272) states the feed-back channel as "the 71 counted-fallback
  rows -- 71 of 1,197 (5.931%), the still-active careers with no >=20-concluded look-alike stratum, whose
  teaching value is the model's estimate", and instructs: confirm it against the recorded provenance
  before anything runs; if the channel is other than these rows, STOP AND FILE.

  The COUNT confirms exactly (825 concluded + 301 completed + 71 fallback = 1,197; share 5.931%).
  This script measures the thing the count cannot show: HOW MUCH of the curve-teaching population's
  structural value actually moves when the surface underneath it moves, and WHICH rows carry it.

THE MECHANISM IT TESTS
  emit_matrix_271.py builds each row's value path as
        Vpath = [ASOF[(id(p), y)] for y in yrs]      with   ASOF[(id(p), Y)] = ev(p, Y)
  i.e. the ENGINE's own valuation at each as-of year. harness_pvc.realised_full/realised_at then average
  that vpath under the evidence weights to produce the structural career value for every CONCLUDED row.
  ev() leans on the year-zero prior wherever a career's own evidence is thin -- so a moved surface can
  reach a concluded row's realised value without ever touching the counted-fallback path.

  If that is what happens, the channel is not the 71 rows, and a convergence verdict reasoned on the
  narrow-channel premise is reasoning about the wrong object.

USAGE (from a dir containing the re-pinned harness as harness_pvc.py, under the pinned venv):
    python3 channel_width.py <NEW_matrix.json> <OLD_matrix.json>

IT DOES NOT FIT, DECIDE, OR WRITE ANYTHING. Read-only on both matrices.

HONEST LIMIT OF THE COMPARISON, STATED RATHER THAN BURIED: the two matrices this was first run on
differ in BOTH the surface (fb9efdec -> b540833b) AND the engine (3c7b0c3c -> 15525b03, the lens).
It therefore measures the redesign's total effect on the teaching values, and does NOT by itself
attribute the movement between those two causes. The control that separates them is an emit on the
LENS engine carrying the OLD surface; it is named in the filing as the next measurement, not assumed.
"""
import sys, json
import harness_pvc as H

NEW, OLD = sys.argv[1], sys.argv[2]

mN, NDn = H.load_matrix(NEW)
mO, NDo = H.load_matrix(OLD)
rowsN = {r['key']: r for r in H.structural_values(NDn)[0]}
rowsO = {r['key']: r for r in H.structural_values(NDo)[0]}
recN = {r['key']: r for r in json.load(open(NEW))['recs']}
counts = H.structural_values(NDn)[1]
common = set(rowsN) & set(rowsO)


def d(k):
    return abs(rowsN[k]['value'] - rowsO[k]['value'])


def games(k):
    return sum(s['games'] for s in recN[k].get('seasons', []))


print("=== THE CHANNEL AS THE ORDER STATES IT -- the counted composition ===")
c = counts['counts']
print("  concluded_realised %d + completed %d + prior_fallback_thin %d = %d"
      % (c['concluded_realised'], c['completed'], c['prior_fallback_thin'], len(NDn)))
print("  fallback_rows %d | share %.3f%% | of_population %d"
      % (counts['fallback_rows'], counts['fallback_share_pct'], counts['of_population']))
print("  COUNT CONFIRMED:", counts['fallback_rows'] == 71 and counts['of_population'] == 1197)

print()
print("=== WHAT ACTUALLY MOVED -- by how the row is valued ===")
print("  %-20s %6s %7s %8s %10s %10s" % ("how", "rows", "moved", "moved%", "mean |d|", "max |d|"))
for how in ('concluded_realised', 'completed', 'prior_fallback_thin'):
    ks = [k for k in common if rowsN[k]['how'] == how]
    mv = [k for k in ks if d(k) > 1e-9]
    dd = [d(k) for k in mv]
    print("  %-20s %6d %7d %7.1f%% %10.2f %10.2f"
          % (how, len(ks), len(mv), 100.0 * len(mv) / len(ks),
             (sum(dd) / len(dd) if dd else 0.0), (max(dd) if dd else 0.0)))

print()
print("=== WHERE THE MOVEMENT SITS -- by career games ===")
print("  %-10s %6s %7s %10s %10s" % ("games", "rows", "moved", "mean |d|", "max |d|"))
for lo, hi in ((0, 0), (1, 5), (6, 20), (21, 50), (51, 100), (101, 10 ** 9)):
    ks = [k for k in common if lo <= games(k) <= hi]
    mv = [k for k in ks if d(k) > 1e-9]
    dd = [d(k) for k in mv]
    lab = "%d" % lo if lo == hi else ("%d-%d" % (lo, hi) if hi < 10 ** 9 else "%d+" % lo)
    print("  %-10s %6d %7d %10.2f %10.2f"
          % (lab, len(ks), len(mv), (sum(dd) / len(dd) if dd else 0.0), (max(dd) if dd else 0.0)))

tot = sum(d(k) for k in common)
fb = sum(d(k) for k in common if rowsN[k]['how'] == 'prior_fallback_thin')
print()
print("=== THE DECIDING FIGURE -- share of total movement carried by the 71 rows ===")
print("  total absolute movement over %d rows : %.1f" % (len(common), tot))
print("  carried by the 71 counted-fallback   : %.1f  = %.2f%%" % (fb, 100.0 * fb / tot))
print("  carried by the other %d rows        : %.1f  = %.2f%%"
      % (len(common) - 71, tot - fb, 100.0 * (tot - fb) / tot))
print()
print("  VERDICT:", "CHANNEL IS THE 71 ROWS" if (tot - fb) / tot < 0.01
      else "CHANNEL IS WIDER THAN THE 71 ROWS -- STOP AND FILE (per the rotation order)")
