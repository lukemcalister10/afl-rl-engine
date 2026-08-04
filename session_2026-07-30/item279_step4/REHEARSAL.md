# #279 STEP 4 — REHEARSAL EVIDENCE (pre-execution). Nothing shipped, nothing adopted.

Runbook: #279 comment 5133237818. Seam audit PASS with three words: #279 comment 5133276813.
Rehearsal run 2026-07-30 in a detached scratch worktree off `95f13c3` (= `origin/main`), full history.
Environment: pinned venv 3.12.3 / numpy 2.4.4 / scipy 1.17.1 / scikit-learn 1.8.0 / openpyxl 3.1.5;
`bootstrap.sh` ENV PIN reports numpy 2.4.4 + bundled OpenBLAS `05c9f9eb` byte-exact to the pin.

**The product edits E1–E5 are NOT applied to this branch.** They live in the scratch worktree and are
recorded here as `out/E1-E5_proposed.diff` for the bounded hands to author, per the roles law.

---

## Phase 0 — the before-picture (`out/phase0_baseline.json`, `out/selftest_baseline_full.txt`)

| | |
|---|---|
| store | `6b9d00a75ca88122c42da9189739916b` |
| `data/v0surf.pkl` | md5 `ce08c2d13ae7d9bd403c60cf58ea1660`, keys `b781ed253bff…`, `d071e74348b3…` |
| `expected_boot.json` `v0surf` | `ce08c2d13ae7d9bd403c60cf58ea1660` — matches the pickle exactly |
| `pvc_curve_v2.json` | curve_md5 `08ea9375`, pool_value 299 |
| `ui/release_pick_curve.json` | md5 `11adecc85a24040e1a7fab193c3a0884`, pool_value 299 |
| FROZEN-RULER pin | `11adecc85a24040e1a7fab193c3a0884` — matches the mirror (C5 closed, re-confirmed) |
| **G-Y0 baseline** | **3.035%, n=1,326 over 64 picks** — held under the dated exception, ceiling 3.500% |
| selftest | **PASSED — 99 checks, 0 fail** |

**Cost measured** (the runbook promised to measure rather than guess): `rl_export.py` 119s ·
`s4_matrix_M1v7.py` 171s · `one_source_selftest.py` 95s → **385s for a full baseline cycle**. A signature
probe under the declared refit lane is ~70s. The Q2 four-way par measurement is 36s.

---

## Q2 — the three dual-position candidates (`out/q2_dual_position_candidates.json`)

Each candidate is grounded in an existing engine law, not invented: **A PRIMARY** is `futblend`'s own rule
("The PRIMARY keys peak/curve/runway/key-premium"); **B LOWER-REPL** is the eligibility-collapse law
(R105.1 / `_collapse_elig`); **C EXCLUDE** drops dual seasons from teaching.

| rule | obs rows | raw rows | dropped | MID | SD | SF | KPD | KPF | RUCK | empty groups |
|---|---|---|---|---|---|---|---|---|---|---|
| CURRENT (`gfut`) | 4,215 | 5,556 | 0 | 1,260 | 971 | 896 | 463 | 387 | 238 | none |
| **A PRIMARY** | 4,215 | 5,556 | 0 | 1,211 | 793 | 1,052 | 448 | 506 | 205 | none |
| **B LOWER-REPL** | 4,215 | 5,556 | 0 | 1,211 | 793 | 1,052 | 448 | 506 | 205 | none |
| **C EXCLUDE** | 3,568 | 4,735 | 821 | 1,211 | 682 | 660 | 438 | 372 | 205 | none |

par-surface delta vs CURRENT over 162 cells (6 groups × 9 picks × 3 tenures):
A and B **mean +0.9237, median +0.8571, max |Δ| 8.100**; C **mean +0.4035, median +0.5012, max |Δ| 9.826**.

**Three findings.**

1. **A and B are the same rule on this data.** They disagree on exactly **2 of 1,874** dual rows — the two
   `SF/KPD` seasons — and neither reaches par_build's 2003–2018 cohort, so the fitted par surface is
   identical. Every other dual form has its primary component as the lower-REPL member. **The owner's
   choice is two-way, not three-way.**
2. **No candidate starves a group.** The loud halt is insurance, not a live blocker (G4 fires it on
   synthetic input, as expected).
3. **The population shift is the owner's predicted direction, measured:** SF +156 and KPF +119, against
   SD −178, MID −49, RUCK −33. Aging midfielders' prime seasons stop refiling under their destination
   forward cells — which is the Joe Berry ripple the par ruling exists to cut.

**Seam recommendation for the owner's word: A PRIMARY.** It is the minimal reading of "the position
recorded for that season", it keeps all 11,264 season rows teaching, it matches the engine's own
"primary keys the surface" law, and it is empirically identical to B. C discards 821 raw rows (14.8% of
the teaching population) to avoid a question the other two answer.

*Caveat stated plainly:* the curve-delta leg of Q2 is **bake-gated behind P3** and is not measured here.
The par-surface delta above is measured; its propagation to the ladder is not.

---

## The gates, fired in anger

| gate | result | evidence |
|---|---|---|
| **G1** γ-flip moves the signature | **PASS** — γ=0.85 → `5ae00319…`, γ=1.0 → `93b4a680…` | `out/G1_G3_signature_probes.txt` |
| **G1 negative control** non-gate var | **PASS** — `RL_RUCK_TAX=0.99` leaves the signature unchanged | same |
| **G2** dead-key HALT | **PASS, fired in anger** — a normal build halts naming signature `5ae00319…` and both dead keys | `out/G2_deadkey_halt.txt` |
| **G3** RL_PICK1 transitivity | **FALSIFIED — see below** | `out/G3_surface_vs_signature.txt` |
| **G4** par loud halt | **PASS both directions, two cases** | `out/G4_par_loud_halt.txt` |
| **G5** s-invariance instrument | **PASS (non-vacuous)**; full binding bake-gated | `out/G5_s_invariance_instrument.txt` |
| **G6** harness identity pins | **PASS — all four assertions fire** | inline below |

**G2, verbatim:** `v0surf FROZEN-SIGNATURE HALT: this build's config signature
5ae003199ab0077ea93c928ec01b84f4 is NOT in data/v0surf.pkl (frozen: b781ed253bff…, d071e74348b3…)`.
Word 3's obligation 2 is discharged: the dead-config rebuild halts by design, loudly, naming the signature.

**G4, verbatim (single starved group):** edited code raises
`par_build HALT: no on-park observations for position group(s) KPF.` with the cohort window, the gate, the
dual rule, `gather()`'s raw and gated counts, and the per-group counts. The **unmodified** code on the
identical input raises `IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed`
— naming nothing. Also proven with all six groups starved.

**G5:** on the committed ladder, a single application of s preserves 12 of 12 pick-to-player relativities;
a deliberate double application moves **all 12** by ×1.022822 (= 1/s). The instrument passes the correct
case and fails the named failure mode.

**G6:** honest load passes at n=1,197 (store `6b9d00a7`, v0surf `b781ed253bff`). Doctored inputs each fire:
wrong store md5 · wrong v0surf sig · population 1,183 ≠ 1,197 · emptied population
(`EMPTY ND teaching population — loader refuses to return nothing`).

---

## THREE FINDINGS THE RUNBOOK DID NOT NAME

### F1 — G3 is falsified. `RL_PICK1` is NOT captured by the signature, and it moves the surface.

My read-back and the runbook both asserted `RL_PICK1` was "transitively captured via the pvc entries".
**Measured, it is not.** Holding γ=0.85 and flipping `RL_PICK1` 3000 → 3500:

| | signature | surface `c18` | surface `surfN` | `_PVC0` head |
|---|---|---|---|---|
| RL_PICK1=3000 | `5ae00319…` | `eddccddbee8a4436` | `a6e2fe368cacdc8b` | 3000, 2767, 2693, 571 |
| RL_PICK1=3500 | `5ae00319…` **same** | `6cb62db45f4d1a93` **moved** | `1f45ba1a61447cfc` **moved** | 3000, 2767, 2693, 571 **same** |

The fitted surface moves; the signature does not. `_PVC0` is sourced from the pinned adopted-curve
artifact (pin(1)=3000 by construction), so `RL_PICK1` never reaches the signature's `pvc` leg. **This is a
second live blind spot of exactly the class item 4 exists to close**, and it is the seam's call whether
`RL_PICK1` joins `_V0SURF_GATES` alongside `RL_GAMMA` in this job or is docketed. The seam's instinct to
demand this as a measurement rather than accept it as reasoning is what caught it.

### F2 — the whole-economy rescale is currently ONE-SIDED, which is load-bearing for item 7.

Measured at `rl_model` load (`out/G3b_scale_mechanism.txt`):

| RL_PICK1 | SCALE | PVC[1] | PVC[64] |
|---|---|---|---|
| 3000 | 4.719196 | 3000 | 571 |
| 3500 | **5.505729** (×1.16667) | **3000** (unchanged) | **571** (unchanged) |

`BOARD_FACTOR` does rescale `PVC` at `rl_model.py:867`, but the adopted-curve swap (RL_PVC2 / L1b)
subsequently overwrites the pick side with the pinned artifact — so the net effect of `RL_PICK1` is to
scale **players only**. Nothing is wrong in the shipped board (RL_PICK1 is 3000 and the artifact is pinned
at 3000, so the two agree). But **item 7 cannot be discharged by re-anchoring `BOARD_FACTOR` alone**: that
would move the player side while the pick side stayed on the old artifact — the one-sided twin of the
double-scaling failure mode the ruling names. The candidate curve must be installed at the new unit *and*
`BOARD_FACTOR` re-anchored consistently, with G5's invariance bound to the full pipeline, not to
`rl_model` load. The comment at `rl_model.py:862–864` ("the WHOLE board (picks + players) scales to it")
is net-stale under the shipped config — the same make-the-prose-say-what-the-code-does class as E4.

### F3 — two PRODUCT identity pins move under the edit set, and neither was in the runbook.

Guard 5 halted the bootstrap on the first attempt — correctly. `data/expected_boot.json` carries:

- **`fv`** — a canonical tree hash over every `*.py` in `engine/forward_valuation`; E1, E3 and E5 all touch
  that tree. `d10aa93e977a16a7…` → `28cfe2e63b44b508…`
- **`engine_head`** — md5 of `_merged_recover.py`; E2 and E4 touch it.
  `404e811353281843b065b3d75768bec0` → `5ba32e5de6a97e6f1d0910572a365aad`

Both re-pinned **surgically** (regex on the two pin lines only; file length unchanged at 20,888 chars;
a full JSON diff confirms exactly two keys changed). These are disclosed pin edits of the same class as the
v0surf re-pin, and they belong in the runbook's edit table. After re-pinning, bootstrap is green.

---

## What remains, and why

Bake-gated behind **P3** (no store-identity pin until the seam relays #283's landed store md5): the declared
refit, the curve re-derivation, attribution channels C and D, the G-Y0 re-derivation, the pool/MSD/SSP
levels under the propagated design, the ruck-cap bite check, item 10's picks 60–64 cohort measurement,
G5 bound to the full pipeline, and the Q2 curve-delta leg.

**CI:** not run at the tip in this rehearsal; the scratch baseline selftest is green at 99 checks. Posture
otherwise inherited from `f60af6c`. Nothing here touches the shipped board or any release identity.
