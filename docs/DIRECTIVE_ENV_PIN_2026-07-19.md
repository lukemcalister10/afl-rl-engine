# DIRECTIVE — ENV PIN · NUMPY/BLAS DETERMINISM · seat 14 · 2026-07-19
### The ROOT fix for item 391: the value-path amplifier is np.interp, which diverges ≥1e-8 across
### DIFFERENT numpy/BLAS BUILDS (CPU kernel was ruled out), flipping the board RANK-UNSAFELY on a
### minority of containers because NOTHING in the repo pins the environment. Pin it so EVERY container
### reproduces the board of record 06d8af60. Owner ruled PIN-FIRST, 2026-07-19; owner authorised
### trimming non-essential procedure — see SCOPE. The reproduction GATE is NOT trimmable.

## ★ THE ONE GATE THAT DOES NOT MOVE ★
Not "done" until the balanced board reproduces `06d8af60` byte-exact on ≥2 GENUINELY-DIFFERENT
containers under the pin. THIS build proves container #1 + the mechanism; the follow-on viewing render
(fresh container, pinned) is container #2. If EITHER diverges, the pin is insufficient → HALT + report.
This is the check F6 skipped. Do not shortcut it, do not simulate it with forced-coretype-on-clean.

## THE JOB (PLAN FIRST — the PLAN is commit #1)
1. DIAGNOSE the exact env delta that makes np.interp diverge: capture THIS container's numpy version +
   build (`np.show_config()`, `numpy.__config__`), BLAS vendor/build, and the wheel hash. Determine
   whether the divergence rides in the numpy WHEEL (version/compile) or the bundled BLAS. Name it.
2. PIN it: commit a hash-pinned dependency lock (numpy== + exact wheel hash; whatever pins the BLAS
   build) + a one-command bootstrap that installs the pinned env at build start. Prefer the SMALLEST
   pin that works (a hash-pinned numpy wheel); escalate to a full container/image pin ONLY if the
   wheel pin does not neutralise the divergence.
3. MECHANISM PROOF (in-container): show the pin neutralises the divergence — reproduce a diverging
   result WITHOUT the pin (a different numpy build, or an interp perturbation ≥ the ~1e-12 threshold
   from item 391), then show that WITH the pin the balanced board holds `06d8af60`. If you cannot
   reproduce ANY divergence to test against, SAY SO explicitly — do not claim a fix you could not
   challenge.
4. CONFIRM the pinned balanced board (`RL_LEGE=0 RL_LEGF=0`, threads=1, PYTHONHASHSEED=0, v0surf LOAD)
   = `06d8af60` byte-exact, 5/5.
5. VALUE-NEUTRAL: k=0 row-diff vs the standard clean board = 0 rows; identity ×4 configs
   (1f10220c/06d8af60/d85901af/9829d01a); store 968de0c7 · curve 56dd7a7b · q97m cfdc7321 · v0surf
   3af2b725 UNTOUCHED. (Pinning to the STANDARD build changes no value BY CONSTRUCTION — confirm it.)

## GIT ENTRY: base = F6 head `540b62f3c1600178aabc56f2dd1ab59c68460b2b` (PR #121) STRICT, HALT on
mismatch; stack on #121. Branch parent = the F6 head. THREADS=1.
## EFFORT: High (the diagnosis + the pin-actually-fixes-it proof is the risk, not the LOC). Why not
Medium: a Medium-grade "looks pinned" check is the F6 failure mode. MODE: auto, PLAN first. TIME: ~2–4 h
(fast if a wheel pin fixes it; longer if it must go to a container pin; flag >2×/<½× per S3).
## FENCE: IN = the dependency lock + the bootstrap + session_2026-07-19/envpin/ proofs (+ the single
engine touchpoint IF one is needed to load the pin). HARD-OUT: the store, curve, q97m, v0surf.pkl,
rl_model.py, and every board VALUE — this changes the ENV, never a value. HALT on any value move.
## EXIT (RETURN ≤25 lines): the env delta named + the pin + the MECHANISM PROOF + `06d8af60` confirmed
+ k=0 / identity ×4 + untouched stamps; branch · head SHA · PR stacked on #121. SILENCE IS A RED ·
halt-not-warn. If the wheel pin does NOT hold `06d8af60` against the divergence test → HALT + report
(we pin deeper); do NOT ship a pin you could not prove.

## SCOPE / TRIMMED PROCEDURE (owner-authorised, this leg only — logged so no later seat reads a silent skip):
- NO separate cold audit for this env-pin: it moves NO player value (pins to the already-correct
  standard build); the reproduction GATE above IS its proof. Tier-1-LITE by construction.
- The 2nd-container leg of the GATE = the follow-on viewing render on the pinned env — no extra run.
- NOT trimmed: the reproduction GATE; and the owner's viewing + sealed-reads + written bake word before
  the v2.11 bake (the chapter ships real value — the owner's decision, never procedure).
