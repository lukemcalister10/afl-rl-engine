"""JOB 5 — ACCEPTANCE HARNESS (DRAFT). Machine-checkable checks the NEW Leg-D curve must pass.
The SEAL is the supervisor's pen — this is a DRAFT that RUNS, not a ruling. To prove the checks are live
it runs the R104.9 strict-descent check against the CURRENTLY SHIPPED curve (engine/rl_after/pvc_curve_L1b.json)
and reports pass/fail with the offending picks (the flat top item 194 caught should surface here).
Writes out/job5_acceptance_draft.json (the harness spec) + out/job5_selftest_result.json (the live run).
"""
import json
ENG = '/home/user/afl-rl-engine/engine/rl_after'
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'
shipped = {int(k): v for k, v in json.load(open(ENG + '/pvc_curve_L1b.json'))['curve'].items()}

# ---- CHECK 1: R104.9 STRICT DESCENT — curve(p+1) <= curve(p) - 1 for p = 1..79 (no plateaus) ----
def check_strict_descent(curve, pmax=79, min_step=1):
    viol = []
    for p in range(1, pmax + 1):
        a, b = curve.get(p), curve.get(p + 1)
        if a is None or b is None: continue
        if not (b <= a - min_step):
            viol.append(dict(p=p, val_p=a, val_p1=b, gap=a - b,
                             kind=('PLATEAU' if a == b else 'ASCENT' if b > a else 'STEP<1')))
    return dict(rule="curve(p+1) <= curve(p) - 1 for p=1..79 (R104.9; item 197); no plateaus unless owner-ruled",
                passed=len(viol) == 0, n_violations=len(viol), violations=viol)

sd = check_strict_descent(shipped)

# ---- the harness DRAFT spec (statuses BINDING-in-substance but DRAFT until supervisor-sealed) ----
draft = {
 "_doc": "Leg-D acceptance harness DRAFT — assembled from ruled items; NOT sealed. Seal = supervisor's pen.",
 "_base": "legc-relay head 6306378, store 0efdc5d6 (values move under R106.7 — thresholds that depend on "
          "player values are left as CONSTRUCTIONS, not fitted numbers).",
 "checks": {
  "R104_9_strict_descent": {
     "source": "R104.9 owner-verbatim-in-substance (item 197); acceptance v1.20 leg_d_placeholders.pvc_strict_descent",
     "formal": "for p in 1..79: curve(p+1) <= curve(p) - 1  (strictly decreasing by >=1; NO plateaus, NO ascents)",
     "owner_ruled_exception": "a plateau is a violation UNLESS the owner rules a specific tie permissible",
     "machine_check": "check_strict_descent(curve) in this file; binds on the DERIVED curve at Leg D",
     "status": "BINDING (DRAFT harness)"},
  "G_Y0_population_identity": {
     "source": "R104.7; acceptance v1.20 leg_d_placeholders.g_y0_population + laws[G-Y0].identity_2026_07_14_CORRECTED",
     "construction": "comp-weighted (natural position-mix) mean V0 per pick band == derived PVC per band, "
                     "deviations netting to zero ON AVERAGE ACROSS MULTIPLE DRAFTS (not draft-by-draft). "
                     "V0 = value the day AFTER the draft (v0_start); PVC = value the day before. One day apart.",
     "population_law": "single class off the curve = a weak/strong class, NOT a breach; measure across drafts.",
     "tolerance": "TBD at the memo — audit #37: gate calibration intercept + slope + SIGNED residuals by pick "
                  "DECILE (not just the overall mean, which can cancel early-over/late-under). Construction here, "
                  "number is the supervisor/owner's.",
     "STALE_DO_NOT_APPLY": "acceptance laws[G-Y0].fix_direction ('raise_young_side...') is STALE — the 2026-07-13 "
                           "measurement came back V0 > PVC in every band (+19..+281). Re-derive the CURE, not the "
                           "numbers. Do NOT wire the recorded fix_direction into the harness.",
     "status": "BINDING population-level (DRAFT harness)"},
  "R104_5_posture_discounts": {
     "source": "R104.5 + audit #6; acceptance v1.20 leg_d_placeholders.posture_2027_discounts",
     "formal": "assert PICK_FUTURE_DISCOUNT == {balanced:0.10, contender:0.15, rebuilder:0.05} EXACTLY in every "
               "generated artifact; 2027 pick value = live_curve(band) * (1 - discount[posture])",
     "machine_check": "byte-exact equality on the three constants; fail on any drift",
     "status": "BINDING (DRAFT harness)"},
  "numeraire_pin": {
     "source": "standing law; spec §3 Leg D L7 rebase",
     "formal": "curve(1) == 3000 (RL_PICK1) after the L7 re-base",
     "status": "BINDING (DRAFT harness)"},
  "stamp_assert_not_stale": {
     "source": "spec §3 Leg D deliverables (the S5 stale-curve failure never repeats)",
     "formal": "the shipped curve artifact carries the store+engine md5 it was derived on; diff-vs-shipped is "
               "stamp-asserted",
     "status": "BINDING (DRAFT harness)"},
 },
 "explicitly_not_in_this_draft": [
   "the G-Y0 numeric tolerance (owner/supervisor's pen)",
   "any threshold that depends on live player values (they move under R106.7)",
   "circularity/survivorship CUT choice (Job 2/3 offer options; the memo decides nothing)",
 ],
}
json.dump(draft, open(BASE + '/out/job5_acceptance_draft.json', 'w'), indent=1)
json.dump(dict(_doc="Live run of the R104.9 check against the CURRENTLY SHIPPED curve (pvc_curve_L1b.json). "
                    "Demonstrates the harness runs and that the shipped curve is NOT yet R104.9-clean.",
               shipped_curve="engine/rl_after/pvc_curve_L1b.json",
               strict_descent=sd),
          open(BASE + '/out/job5_selftest_result.json', 'w'), indent=1)

print("=== JOB 5 acceptance harness DRAFT — live self-test ===")
print(f"R104.9 strict descent on the SHIPPED curve: passed={sd['passed']}  violations={sd['n_violations']}")
for v in sd['violations']:
    print(f"  pick {v['p']}->{v['p']+1}: {v['val_p']} -> {v['val_p1']}  ({v['kind']}, gap={v['gap']})")
print("wrote out/job5_acceptance_draft.json, out/job5_selftest_result.json")
