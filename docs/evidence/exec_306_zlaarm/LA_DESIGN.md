# #306 L-A — THE TAIL, CONSTRAINED BY CONSTRUCTION · THE DESIGN, MEASURED · **AND ONE SCOPE COLLISION FOR THE SEAM**

**2026-08-04, the #306 cold execution seat `zlaarm`.** Filed for the seam's audit — §4 makes the construction
this job's to design and the seam's to audit. Both R-H gates green on this fit-class box (`ASSERT_LOG.md`
entry 3). Every figure re-runnable from `measurements/`. **No engine act, no bake, nothing landed.**

---

## 1 · THE DEFECT, NAMED STRUCTURALLY — not "the tail is too high", but *why it can be*

`_build_v0_curve` (`engine/rl_after/_merged_recover.py:1340`) fits `_v0_raw` — the model's own year-zero
estimate — by adaptive-bandwidth kernel regression over **log(recorded pick)**, then projects isotonic
non-increasing. **It never references the pick curve.** The curve reaches the surface only through
`_v0surf_sig`, the *config signature* — a hash used to select a frozen artifact. It is not an input to the
value at any point.

**So `pick` enters the surface directly, as a free regressor.** The surface is therefore at liberty to sit
wherever the model's estimates sit, and in the tail — where evidence thins and the kernel bandwidth grows to
`hmax` — it does. Measured (`lens_shape.py`, installed curve `e69a3f38`, pass-0 substrate, 1,444 teaching
rows):

| m = v0 / curve[pick] | 1–10 | 11–20 | 21–30 | 31–45 | **46–64** | overall |
|---|---|---|---|---|---|---|
| **band aggregate** | 0.939 | 0.990 | 1.024 | 1.189 | **1.653** | **1.076** |
| row p10 … p90 | 0.36…1.31 | 0.53…1.32 | 0.71…1.26 | 0.78…1.68 | **0.99…2.45** | — |

**The lens is monotone in pick depth.** Under N29 the lens is supposed to be the *positional/age* view of an
anchor; a lens that climbs 0.94 → 1.65 with depth is not modulating around the anchor, **it is re-shaping
it**. That is the defect stated as a property of the construction rather than as a symptom of the number.

The legitimate lens is real and large and must survive: **by position** KPF 0.517 … KPD 1.423 (2.75×);
**by draft age** 16: 1.242 … 26: 0.541.

## 2 · THE CONSTRUCTION

```
v0*(pos, age, pick)  =  anchor(pick)  ×  m(pos, age)
```

| limb | what makes it structural |
|---|---|
| **`anchor(pick)`** — the installed pick curve | **`pick` enters the surface through the anchor and through nothing else.** The surface cannot leave the curve's shape because it has no other channel through which to do so. This is the single change that makes N29's *"the pick curve is the skeleton the surface cannot leave"* a fact about the artifact rather than an aspiration. |
| **`m(pos, age)`** — the lens | a function of **position and draft age only**. Pick is not an argument. A pick-depth drift is therefore **not representable**, which is what "constrained by construction" has to mean. |
| **bounded** | `m = B^t`, `t ∈ [−1, 1]` ⇒ `m ∈ [1/B, B]` **identically**. No clip is applied to a finished surface; an out-of-band surface cannot be built. |
| **aggregate-neutral** | the neutrality scalar is solved **inside the estimator**, against `Σ anchor·m = Σ anchor` over the fit population. Where the bound binds, **the bound wins** and neutrality holds to a stated tolerance — N30's wording exactly. |

**Design constants, fixed here and stated in the artifact's own record per N30:** `B = 2.00` (m ∈ [0.50, 2.00])
· aggregate tolerance **0.5%** · cells = position × age-group {≤17, 18, 19–20, 21+}, minimum 25 rows, thin
cells pooled to the position's all-age cell (17 cells on this substrate).

## 3 · WHAT IT DOES — both directions, as §4 requirement 3 demands

`anchored_construction_sim.py`. **A design simulation on committed rows, not an acceptance run** — the engine
fits `m` from `_v0_raw`; acceptance is measured on the artifact. Nothing here is a gated G-Y0.

| band | rows | **before** | **after** | move |
|---|---|---|---|---|
| 1–10 | 229 | −6.10% | **+0.80%** | +6.89 pp |
| 11–20 | 228 | −1.03% | **−0.35%** | +0.68 pp |
| 21–30 | 230 | +2.37% | **−0.78%** | −3.14 pp |
| 31–45 | 345 | +18.90% | **+0.47%** | −18.43 pp |
| **46–64** | 412 | **+65.28%** | **−1.78%** | **−67.06 pp** |

**The tail collapses from +65% to −1.8%, and the head does not open a gap** — it moves *toward* neutral,
−6.10% → +0.80%. Requirement 3 names the failure mode explicitly (*"a construction that fixes +64% at 46–64
while opening a gap at 1–10 has moved the problem, not solved it"*); this construction does not exhibit it,
and the table is reported at every band in both directions rather than only where it flatters.

## 4 · N30 (ACCEPTANCE 7) — both limbs, each demonstrated fail-capable

| limb | result |
|---|---|
| **aggregate-neutral to a stated tolerance** | achieved **1.00000000**, `\|1−ratio\| = 0.0e+00`, against a 0.5% tolerance. It is exact because it is solved, not fitted-and-hoped. |
| **no band exceeds its stated bound** | the bound **BINDS**, at `KPF\|18` and `KPF\|na` (both pinned to 0.500). A constraint that binds on real data is demonstrably able to fire — this is N30's non-vacuity, shown rather than asserted. |

**Born failing, as N30 requires:** on today's artifact the same two limbs read **+7.64% aggregate** and
**+65.28% at 46–64**. The acceptance fails today and passes under the construction — measured both ways.

**A design question the seam should rule rather than inherit:** `B = 2.00` binds on KPF, i.e. it pulls key
forward pricing *up* toward the anchor. That may be the intended constraint or it may be the bound set too
tight for a position the data genuinely prices at ~0.5×. I have not widened it to make the bind disappear —
that would be choosing the bound to avoid a result.

## 5 · §4 REQUIREMENT 4 — the bust inversion, CHECKED and NOT depended on

| | never played | played | inverted |
|---|---|---|---|
| today, this substrate | 387.1 (n=166) | 302.2 (n=347) | **yes**, ratio 1.28 |
| under the construction (lens only) | mean m 1.0076 | mean m 0.9578 | ratio **1.052** |

**Within a cell the inversion becomes structurally impossible** — two pool entrants in the same
(position, age) cell take the same anchor and the same lens, and games played is not an input to either. What
survives is a 5.2% across-cell residual, down from 28%. The construction is **checked against** the inversion
and **does not depend on** it.

*Stated precisely:* these are not the directive's figures (618.3, n=297 / 553.1, n=429). That cut is defined
differently; mine is `is_pool` rows at `age_draft ≥ 19` on the pass-0 matrix. **The direction reproduces; the
magnitudes are a different population and are not quoted as the same number.**

---

# 6 · THE SCOPE COLLISION — §4 REQUIREMENT 2 CANNOT HOLD WITH THE POOL LEVEL FENCED OUT

Requirement 2 asks that *"the pool sits **below** the last national band"* hold **by construction, provably**.
Measured on this substrate, it cannot — and the reason is arithmetic, not design.

```
curve[64]                                   221
implied anchor(65), by the curve's own slope 212.35
worst-case pool value at B = 2.00           424.70     >  221
guaranteed below curve[64] for EVERY m  iff  B <= 1.0407
today's pool mean v0                        435.63     (83.78% of pool rows sit above curve[64])
```

**`B ≤ 1.0407` would crush the legitimate lens.** The measured positional spread alone runs 0.517 → 1.423; a
bound of 1.04 forbids the entire positional and age structure the surface exists to express. There is no `B`
that both carries the real lens and guarantees pool coherence.

**And the alternative route collides with the fence.** Making the pool coherent means bringing it from ~435
to ≤ 221 — a **~50% move in the pool's level**. §4 fences the pool's *level* out explicitly (ITEM 412 / #207
stage-2, the owner's call), while requirement 2 asks for a coherence that cannot be reached without moving
it.

**So two lines of the directive cannot both be satisfied**, and this is a ruling, not a seat's choice. Three
routes, with what each costs:

| | route | consequence |
|---|---|---|
| **A** | **Pool gets its own bound** `B_pool ≤ curve[64]/anchor(65)`, national lens keeps `B = 2.00` | coherence becomes structural and provable; **but it moves the pool level ~50%**, which is #207's to rule |
| **B** | **Requirement 2 is narrowed** to *within-national coherence*, pool coherence deferred to #207 stage-2 | keeps the fence intact; the incoherent-pool state the gate itself flags **persists**, named as UNRESOLVED |
| **C** | Pool anchored at a level #207 supplies, then bounded like everything else | correct in principle; **blocks L-A on an owner decision that is not scheduled** |

**I recommend B for this job and A for #207** — L-A delivers the national tail constraint now, which is where
the +65% actually lives, and the pool's coherence travels to the stage where its level is already the
question. **I have not chosen. L-A's other four requirements are complete and do not depend on this.**

---

## 7 · WHAT IS NOT IN THIS DESIGN

- **No engine change has been made.** `_build_v0_curve` is untouched; the substrate is byte-identical to
  `13b71c26` (round-trip proven). Implementation follows the seam's audit, not precedes it.
- **No predicted G-Y0.** Acceptance 4 binds: the number is re-measured on the artifact or it is not stated.
  The §3 table is a design simulation on committed rows and is labelled so in the script, its JSON, and here.
- **No gate re-spec'd**, no tolerance moved, no definition of converged touched.
- **The pool's level is not set**, and nothing here proposes one.

**HOLDING for the seam's audit of the construction and its ruling on the §6 collision.** L-B follows on the
same substrate; its failing direction is already discharged by the recorded cross-container pair (N35 §3).

**Nothing lands; the EXECUTION word remains WITHHELD.**
