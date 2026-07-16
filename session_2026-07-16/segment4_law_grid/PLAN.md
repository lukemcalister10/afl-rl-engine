# PLAN / HALT RECORD — LEG B SEGMENT 4: THE v1.2 LAW + THE λ PRE-GATE

Build-session artifact (NOT a `docs/` pack doc — CORE: builds never author docs).
**Design of record (READ IN FULL, consumed):** `docs/MEMO_LEGB_functional_form_2026-07-16.md` **v1.2** (§2.1 ⟪v1.2⟫ WEIGHT-DON'T-GATE). This segment IMPLEMENTS the OWNER'S LAW verbatim; it does not redesign.
Directive: `docs/DIRECTIVE_LEGB_segment4_2026-07-16.md`. Deliverable set + fence: `docs/DIRECTIVE_LEGB_uncompress_2026-07-16.md`. Acceptance: `docs/acceptance_v1_19.json` (`leg_b.rho_construction`, `leg_b.lambda_pre_gate`). Rulings: register items 230/237/239/240/241.
**MODE: auto — SHORT PLAN commit first, then STOP.** This commit is the checkpoint artifact.

**⚠ OUTCOME: the λ PRE-GATE HALTS. λ_ρ(v1.2, d=0.5) = 0.8086 < 0.95. NOTHING beyond the ρ construction + its measurement is built (directive step 0). The owner rules at the checkpoint.**

---

## 0 — GUARDS / BASE PINS (verified, recorded)

- **Engine/code base — STRICT ✓**: `git ls-remote … claude/legb-segment3-v1-rewire-5jy7f3` = `243106b5c1ad4b00211813670fe33d6ae0057518` == pin `243106b`. Segment-3 scaffolding is DONE + prescreened (item 237).
- **Base reconciliation (SILENCE-IS-A-RED, owner ratifies at PROCEED):** the directive names the CODE base `segment3@243106b` ("CONTINUE this branch") and the docs base (memo v1.2 / acceptance v1.19); the harness mandates development on `claude/legb-segment4-v1-2-law-grid-2l4dhv`. The segment-3 CODE branch and the segment-4 DOCS branch had **empty file overlap** (code = engine/harness/data/session; docs = docs/ui/tools) and a shared merge-base `7a34429`. I resolved by **merging `segment3@243106b` into the segment-4 branch** (commit `1f38cd4`, `--no-ff`, conflict-free) — the union is exactly the landed state the directive describes (engine scaffolding + tools/ from #102 + ui/ + the verified docs). **The segment-3 remote head is UNTOUCHED at `243106b`.** If you want a different reconciliation (e.g. rebase the docs onto `243106b`), say so at PROCEED — nothing on `segment3` is disturbed.
- **Store / config — FENCE ✓ UNMOVED throughout**: store `b1fd0bced30baa838325814c39d43233` (== pin `b1fd0bce`), config `c2d233aec1041a2d24a66990a584f552d59b3902…` (== pin `c2d233ae`). This job never writes the store; `RL_UNCOMP`/`RL_UNCOMP_S` are declared kill-switch/dial (absent from `data/model_config.json`, not manifest dials). Workspace store md5 at measurement = `b1fd0bce`.

## 1 — PRE-VIEW SEAL MANIFEST (audit #16/#22/#45; recorded at the checkpoint, the OPEN RE-SEAL of items 230/240)

md5 **verified against my own fetch** — MATCHES the FEED seals:

| artifact | md5 (measured) | FEED-required | verdict |
|---|---|---|---|
| `docs/MEMO_LEGB_functional_form_2026-07-16.md` (v1.2) | `1ff0702af5146a6a5fe68adaf974a346` | `1ff0702a…` | ✓ |
| `docs/acceptance_v1_19.json` | `7a97717b8302c53f3937c238abf16794` | `7a97717b…` | ✓ |
| `docs/DIRECTIVE_LEGB_segment4_2026-07-16.md` | `9fd54d1d93604994563582ed341e4d12` | (brief) | recorded |
| `docs/DIRECTIVE_LEGB_uncompress_2026-07-16.md` | `0068a556a8067ba472b7faddc555c44a` | (brief) | recorded |

Any post-view mutation of the memo or acceptance JSON HALTS the ladder. This is the segment's pre-view seal.

## 2 — THE WEIGHT-FUNCTION DIFF (memo §2.1 ⟪v1.2⟫; directive step 1) — the ρ construction, verbatim

Two files, minimal, the map/captain/ramp/conservation scaffolding UNTOUCHED (item-237 prescreen stands):

- **`engine/rl_after/rl_model.py`** — DECLARED constant next to Δ=6.0:
  `UNCOMP_DECAY=0.5` (ρ games×recency decay d per year back; owner-tunable at seg-4).
- **`engine/rl_after/_merged_recover.py`** —
  - **DELETED** the `_qualifying(p,season)` predicate — a **never-shipped stub** (it only ever raised `NotImplementedError`; RL_UNCOMP stayed inert through seg-3, so it was never reached in any shipped/measured build). Replace, per directive step 1.
  - **REWROTE `rho_out(p,pos)`** to the LAW: over EVERY season with `games>0`, `u_s = games_s·UNCOMP_DECAY^(2026−year_s)`; `ρ_num = Σ u_s·(avg_s−REPL[pos]) / Σ u_s`; zero played seasons ⇒ `None` (caller w=0). **NO season exclusion, NO games floor, NO career-phase test** (acceptance-enforced `leg_b.rho_construction.forbidden`).
  - `RHO_DEN[pos]` (reference build, unchanged code) = **MEDIAN of this same `rho_out`** over the demonstrated-proven pop — numerator and denominator now share ONE law, exactly `leg_b.rho_construction.law`.
- **A/B invariant (unmeasured this commit, by the HALT rule):** RL_UNCOMP inert ⇒ the ρ axis is never evaluated ⇒ board `8d90c9ac` byte-exact. The map short-circuits before `rho_out`. (The full A/B re-prove is a POST-PROCEED step; not run — nothing beyond the construction is built.)

## 3 — THE λ PRE-GATE (directive step 0; `leg_b.lambda_pre_gate`) — **HALT**

Harness `rho_axis_v12.py` — the PINNED frozen `fit_beta` (log-log OLS + 1000-boot percentile CI, `np.random.default_rng(0)` fresh per fit) and the PINNED sample law (`measure.py::measure3` @ `2b76d37`: POP real/live/gfut∈REPL/age≥27; `o` = recent-2 games>0 avg above REPL; per-variant gate `o>0 ∧ rho>0 ∧ level_now>0`). Evidence: `LAMBDA_PREGATE.txt` / `.out`.

```
lambda[ floor10 (v1.1, games>=10)               vs o ] = 0.8957  CI=[0.7771,1.0085]  n=112  REPRO-OK
lambda[ floor6  (v1.1, games>=6)                vs o ] = 0.9942  CI=[0.9837,1.0001]  n=114  REPRO-OK
lambda[ v12_gxr (THE LAW: games×recency d=0.50) vs o ] = 0.8086  CI=[0.6800,0.9678]  n=112
CROSS-CHECK  rho_v12 (harness) == rho_out (shipped engine) : max|Δ|=0.000e+00 over n=112  IDENTICAL
λ PRE-GATE: λ_v12 = 0.8086  vs gate 0.95  ->  HALT
```

- **REPRODUCTION:** the harness reproduces the item-239 anchors byte-exact on this store (`floor6=0.9942 n=114`, `floor10=0.8957 n=112`) — the frozen `fit_beta` + store + o-construction are the pinned ones.
- **CROSS-CHECK:** the harness's `rho_v12` is **byte-identical to the shipped `rho_out`** (max|Δ|=0 over all 112 sampled players) — I measured THIS construction, not a proxy.
- **VERDICT:** `λ_ρ(v1.2, d=0.5) = 0.8086 < 0.95` ⇒ **HALT with the number** (`leg_b.lambda_pre_gate.rule`). The memo's *expectation* was 0.9923–0.9942 ("expected is not measured, hence the gate" — the gate fired).

## 4 — WHY IT MISSED + THE d LEVER (diagnostic — decision support, NOT a lever pulled). Evidence: `DSWEEP.txt`

`d` is the memo's explicitly **owner-tunable** checkpoint constant. The λ(d) curve (same pinned harness):

| construction | d=0.30 | d=0.40 | **d=0.50** | d=0.60 | d=0.72 |
|---|---|---|---|---|---|
| **all games>0 seasons (THE LAW)** | 0.8611 | 0.8317 | **0.8086** | 0.7190 | 0.7314 |
| recent-2 games>0 only (horizon-CAP) | 0.9720 | — | 0.9236 | — | 0.9083 |
| recent-3 games>0 only | — | — | 0.8230 | — | 0.8004 |

**No decay d ∈ [0.30, 0.72] clears λ≥0.95 for the law** (best 0.8611 at d=0.30). λ FALLS as d rises (more career mass ⇒ more compression). The gate is only approached by **capping the horizon to recent-2 seasons** — a *season exclusion*, which `leg_b.rho_construction.forbidden` **prohibits**.

**Root cause (plain):** `o` (what β must track) is recent-2 output. The v1.2 law weights the *whole career* by games×recency; an elite player's weighted career pulls DOWN toward mid-career levels, compressing the elite ρ-spread vs `o` (λ<1). The floor/qualifying measures got λ≈0.99 precisely because they looked only at recent-2 *qualifying* seasons (≈ `o`). **"Weight, don't gate" removes the recency-concentration that gave the axis its output-elasticity** — the very defect (low λ) v1.1 was built to cure re-enters through the full-history weighting. This is a genuine tension between the owner's data-preservation law and the β-repair mechanism, not a decay-tuning miss.

## 5 — THE OWNER DECISION (the checkpoint rules; I build nothing further until PROCEED)

The λ pre-gate is a HARD gate and it HALTS. Options are the OWNER'S to rule (I recommend none unilaterally — this is a law-vs-mechanism call above the build seat):
1. **Revise the law** so ρ stays output-elastic while honouring "don't gate" (e.g. a games×recency weighting whose *effective horizon* is recent-2 without excluding any season — a continuous recency kernel, not a hard cap). Requires a new memo block (redesign — out of this seat's fence).
2. **Accept a waiver** of the 0.95 gate at the measured 0.8086 (β headroom shrinks: `β_eff=(1−w)β_c+w·λ`, so saturated β caps well below 0.85 → the grid likely HALTs empty).
3. **HALT the chapter** here pending re-design.

## 6 — FENCE HONORED (what was NOT built — directive step 0 "NOTHING else built")

NOT run/built (all POST-PROCEED, and moot under the HALT): the A/B board re-prove · the s-grid {0.55–0.70} · `UNCOMP_S_DEFAULT` selection · the full item-206 RETURN (frozen-suite β · slope · English/Briggs · G-COHORT · census · SCAR ledger · mover report · value-flow · w-export · killswitch matrix · self-tests). STORE / docs/ / ui/ / acceptance / gates-guards / config / pick-curve — untouched.
