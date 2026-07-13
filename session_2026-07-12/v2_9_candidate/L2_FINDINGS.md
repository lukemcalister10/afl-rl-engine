# L2 — DIAL 14 + the prior-cap-gone PROOF · result: HALT (assert-order unmet) · 2026-07-12

## The dial, confirmed + the method correction
The discount dial is **`LENS['bal']`** (`rl_model.py:301`; `d=LENS[lens]`, `*21/((1+d)**k)`), board
ships the 'bal' lens. **Correct reproduction requires patching the dial BEFORE import so the board
regenerates with `SCALE` re-anchored to the 99th percentile** (`rl_model.py:457`,
`SCALE=7000/ref**GAMMA`) — exactly the sweep's "engine md5 restored per arm" method. Verified: at
0.13 the full-regen board reproduces `SWEEP_DISCOUNT.md` **to the number** — emmett **913**, gawn
**2463**, bont **3630** (sweep: 913 / 2463 / 3630).

⚠️ **Superseded:** the first probe `out/l2_dial.json` mutated `LENS` in-process WITHOUT the SCALE
re-anchor and showed emmett *rising* (1178→1479) — WRONG SIGN, method error. Kept only as the
counter-example; `l2_measure.py` (dial patched pre-import) is the correct harness.

## The assert-order proof (directive L2: "prove it, don't assume it")
Claim under test (ruling pack D5 / synthesis §1): *the young-ruck prior-cap artifact — louis-emmett
−22% at ≤13% — is removed by L1(b) full adoption, so the dial may drop.*

| arm (dial 0.13) | emmett | gawn | bont | youth≤21 mean |
|---|---|---|---|---|
| base `_PVC0` (frozen) | **913** | 2463 | 3630 | 933 |
| **+ L1(b) adopted `_PVC0`** | **913** | 2463 | 3630 | 937 |

**RESULT — NOT PROVEN (refuted).** L1(b) as implemented (the `sim_option_b` `_PVC0` swap + V0/RUC
rebuild) leaves emmett at **913** — the artifact is **unchanged**. At the L1 dial (0.15) emmett was
already unmoved by adoption (1178→1178): he is **not among the 24 young-RUC movers** option (b)
lifts (knobel/barnett/conway are; emmett is not — his pick-27 cap basis barely changes between the
frozen and derived curves). So "option (b) removes the mechanism" does **not** hold for emmett under
this adoption.

## Consequence for L2
Per the directive's assert order — *"the prior-cap artifact machinery must be GONE (via L1(b)) before
the dial moves — prove it, don't assume it"* — the proof **fails**, so **L2 HALTS**: do not move the
dial on the premise that adoption cleared emmett's cap. Two separable facts for the ladder:
- **DIAL 14 (0.14) itself is above the ≤13% artifact zone** (the sweep's emmett drop concentrates at
  ≤13%; at 14% it is milder). So dial 14 *may* still be rulable on its own merits (the sweep proved
  15→12 breaks no guard, G-COHORT y4 margin widens 1.4→8.6). But that is a **discount ruling on its
  own**, NOT "the cap is gone" — the directive coupled them, and the coupling is refuted.
- **Removing emmett's cap artifact needs a DIFFERENT mechanism than L1(b)** — e.g. lifting/retiring
  `RUC_PRIOR_CAP` for young rucks, or a fuller adoption that raises his specific cap basis. That is
  an unruled engine change → owner/supervisor word.

## Status
Dial mechanism VERIFIED (reproduces the sweep exactly). Prior-cap-gone proof RUN and **refuted** →
L2 held. This is the "prove it, don't assume it" gate doing its job: the combined "adopt-(b)-then-
drop-the-dial-because-the-cap-is-gone" construction does not survive contact with the engine.
