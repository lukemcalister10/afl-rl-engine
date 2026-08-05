#!/usr/bin/env python3
"""#306 L6 — THE BELIEF-MASS MEASUREMENT (rides on the separating run).

THE QUESTION, as the seam framed it (#306 comment 5186208519 clause 3):
  the channel-width measurement is a DERIVATIVE -- what moved under one change. It is not the MASS --
  how much of the basis's value LEVEL is model-shaped. This script measures what is actually
  measurable of that mass, and is explicit about the part that is not.

WHAT IS A TRUE MASS HERE
  Every curve-teaching row carries a provenance tag from harness_pvc.structural_values:
      concluded_realised  -- the career finished; value = evidence-weighted mean of its own value path
      completed           -- played-so-far + actuarial completion from >=20 concluded look-alikes
      prior_fallback_thin -- NO look-alike stratum exists; the value IS the model's estimate, wholesale
  The fallback class's share of total BASIS VALUE (not of row count) is a true mass: it is the portion
  of the teaching signal that is the model's opinion outright. The order's 5.931% is a COUNT share;
  this reports the VALUE share, which is the quantity the belief question actually asks about.

WHAT IS NOT MEASURABLE HERE, STATED PLAINLY
  Inside `concluded_realised` and `completed`, values come from the engine's ev() at each as-of year,
  and ev() blends a career's own record with the year-zero prior wherever that record is thin. That
  blend has NO no-prior counterfactual in this engine -- there is no mode that prices a career with the
  prior removed -- so the model-shaped FRACTION inside those rows CANNOT be measured, only bounded
  below by how far they move when the prior moves. This script reports that bound and names it a bound.
  Reporting it as the mass would be exactly the over-claim the seam's clause 3 warns against.

WHY THE SENSITIVITY IS NOW CLEAN
  The separating run established that the matrix is IDENTICAL under the old engine and the lens engine
  given the same loaded surface (9c4bca53 both ways, byte-for-byte). So the difference between the two
  matrices below is the SURFACE alone -- the surface+engine confound of the first measurement is
  dissolved, not merely bounded.

USAGE (from a dir holding the re-pinned harness as harness_pvc.py, under the pinned venv):
    python3 belief_mass.py <lens_surface_matrix.json> <old_surface_matrix.json>

READ-ONLY. Fits nothing, writes nothing.
"""
import sys, json
import harness_pvc as H

NEW, OLD = sys.argv[1], sys.argv[2]
mN, NDn = H.load_matrix(NEW)
mO, NDo = H.load_matrix(OLD)
rowsN = {r['key']: r for r in H.structural_values(NDn)[0]}
rowsO = {r['key']: r for r in H.structural_values(NDo)[0]}
common = set(rowsN) & set(rowsO)
CLASSES = ('concluded_realised', 'completed', 'prior_fallback_thin')

totN = sum(rowsN[k]['value'] for k in common)
totO = sum(rowsO[k]['value'] for k in common)

print("=== 1 · THE TRUE MASS -- share of total basis VALUE by provenance ===")
print("  (the order's 5.931%% is a share of ROW COUNT; this is the share of VALUE)")
print("  %-22s %6s %14s %10s   %14s %10s" % ("provenance", "rows", "value (lens)", "share", "value (old)", "share"))
for c in CLASSES:
    ks = [k for k in common if rowsN[k]['how'] == c]
    vN = sum(rowsN[k]['value'] for k in ks)
    vO = sum(rowsO[k]['value'] for k in ks)
    print("  %-22s %6d %14.1f %9.2f%%   %14.1f %9.2f%%"
          % (c, len(ks), vN, 100.0 * vN / totN, vO, 100.0 * vO / totO))
print("  %-22s %6d %14.1f %9.2f%%   %14.1f %9.2f%%" % ("TOTAL", len(common), totN, 100.0, totO, 100.0))

fbN = sum(rowsN[k]['value'] for k in common if rowsN[k]['how'] == 'prior_fallback_thin')
fbO = sum(rowsO[k]['value'] for k in common if rowsO[k]['how'] == 'prior_fallback_thin')
print()
print("  WHOLESALE-BELIEF MASS (value the model supplies outright, no career evidence behind it):")
print("     lens surface b540833b : %.1f of %.1f = **%.2f%%** of the teaching signal by value"
      % (fbN, totN, 100.0 * fbN / totN))
print("     old  surface fb9efdec : %.1f of %.1f = **%.2f%%**" % (fbO, totO, 100.0 * fbO / totO))
print("     against a COUNT share of 71/1197 = 5.931%% -- the value share is the quantity that matters")

print()
print("=== 2 · THE LOWER BOUND on prior-shaping inside evidence-backed rows ===")
print("  how far a class's value moves when ONLY the surface moves. A floor, not the mass.")
print("  %-22s %14s %14s %12s %10s" % ("provenance", "value (lens)", "value (old)", "delta", "delta %"))
for c in CLASSES:
    ks = [k for k in common if rowsN[k]['how'] == c]
    vN = sum(rowsN[k]['value'] for k in ks)
    vO = sum(rowsO[k]['value'] for k in ks)
    print("  %-22s %14.1f %14.1f %+12.1f %+9.2f%%"
          % (c, vN, vO, vN - vO, (100.0 * (vN - vO) / vO if vO else 0.0)))
print("  %-22s %14.1f %14.1f %+12.1f %+9.2f%%" % ("TOTAL", totN, totO, totN - totO, 100.0 * (totN - totO) / totO))

ev_ks = [k for k in common if rowsN[k]['how'] != 'prior_fallback_thin']
evN = sum(rowsN[k]['value'] for k in ev_ks)
evO = sum(rowsO[k]['value'] for k in ev_ks)
print()
print("  Evidence-backed rows only (concluded + completed, %d rows):" % len(ev_ks))
print("     level moved %.1f -> %.1f  = %+.2f%% on a surface change alone" % (evO, evN, 100.0 * (evN - evO) / evO))
print("     => AT LEAST %.2f%% of the evidence-backed level is prior-shaped. This is a FLOOR under one"
      % abs(100.0 * (evN - evO) / evO))
print("        particular surface perturbation, NOT the model-shaped fraction of the level.")

print()
print("=== 3 · WHAT THIS DOES AND DOES NOT SETTLE ===")
print("  SETTLES  : the wholesale-belief mass by value (section 1) -- a true share, exactly measured.")
print("  SETTLES  : that the engine contributes nothing -- the separating run proved the matrix")
print("             byte-identical under both engines at a fixed surface, so section 2 is surface-only.")
print("  DOES NOT : quantify the prior's share INSIDE concluded/completed values. That needs a no-prior")
print("             pricing mode the engine does not have. Section 2 is a floor and is labelled one.")
