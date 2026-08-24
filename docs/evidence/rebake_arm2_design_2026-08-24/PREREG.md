# PREREG — REBAKE WEEK · ARM 2 · THE DESIGN ARM

**Filed BEFORE any engine or artifact edit (process law P9).** Charter: register v831 (all six rebake
decisions ruled, owner words verbatim), v833 (the binding handover), v834 (ARM 1 landed and verified).
Directive: `docs/directives/REBAKE_ARM2_DESIGN_2026-08-24.md`. Construction of record:
`docs/proposals/rebake_study_B/DESIGN_STUDY_B.md` §2.3, §2.6, §3.3, §4.2, §4.3, §5.1. Baseline tables:
`docs/proposals/rebake_study_A/REBAKE_DESIGN_STUDY.md` §5.1. Comparison:
`docs/proposals/REBAKE_COMPARISON_2026-08-21.md`.

**Branch base:** `rebake/arm1-store-alone` tip `4124fd6`. ARM 1's refit entry points, declared switches
(`RL_CM_PKL`, `RL_Q97M_PKL`, `RL_WS` in `INFRA_ALLOW`), the cm loader HALT, the in-repo stamp machinery
and the candidate-root pattern are REUSED, not reforked.

**No design decision is open.** Every construction below is owner-ruled at v831. This arm executes and
measures. Where the tree contradicts a line here, **the tree wins and the correction is named in the
hand-back** — never the reverse (P9, and the F5 incident it names).

---

## 0 · BASELINE, ESTABLISHED BEFORE THIS FILING

The seat's own isolated workspace (`/home/user/arm2_ws`, a copy of this worktree's `engine/rl_after` +
`engine/forward_valuation`; the shared `/home/claude/rl_workspace` is never written) reproduces the live
board **byte-exact** at `RL_CONFIG_MODE=gate`, single-thread BLAS, pinned venv `/root/rl_venv312`
(py 3.12.3 · numpy 2.4.4 · scipy 1.17.1 · sklearn 1.8.0):

    md5(rl_app_data.json) = 6fd0f7ded2b280d1a90962c299a152e3   == data/expected_boot.json 'board'

with `RL_CM_PKL` **and** `RL_Q97M_PKL` both bound to the in-repo live pickles — the ARM 1 reconciliation
lesson (v834): binding one and not the other silently prices on the out-of-repo live ceiling.

**One correction to the recipe, filed here rather than discovered later.** The board cannot be built
against this worktree's own `data/expected_boot.json`: ARM 1's in-repo stamp fix edited
`engine/forward_valuation/build_peak_model_v4.py`, and `fv_identity` hashes every `*.py` in that
directory, so the committed `fv` pin (`6e9a370e…`) no longer matches the tree (`47cbbfe6…`). ARM 1
declared that move and deliberately deferred the re-pin to the landing act (v834). The baseline above is
therefore taken in a **scratch root** built by ARM 1's own `make_candidate_root.py` with **no artifact
swaps** — the fv re-pin alone. The worktree's committed pins are byte-untouched.

---

## 1 · THE RULED CONSTRUCTION, READ FROM SOURCE

Line references are to this worktree at `4124fd6`.

### 1.1 The exact monotone constraint (v831 D1 — owner: "Exact it is.")

Study B §2.3, verbatim mechanism. `sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:962`
calls `_update_leaves_values` only when `self._loss.differentiable` is False, and that call overwrites
every leaf with the empirical quantile of its residuals — discarding the monotone bounds the grower just
enforced (`PinballLoss.differentiable = False`, `sklearn/_loss/loss.py:624`). The construction:

```python
from sklearn._loss.loss import PinballLoss
class GradOnlyPinball(PinballLoss):
    differentiable = True            # stops gradient_boosting.py calling _update_leaves_values
    need_update_leaves_values = False
```

on `HistGradientBoostingRegressor(loss=GradOnlyPinball(quantile=q), monotonic_cst=…)`.
`monotonic_cst[9] = +1` (level). **Zero negative level steps FROM THE FIT** is the claim; study B proved
0 in 1,004,720 twice, on two different fitted families (M-54, M-61).

**FB4 — the HALTing private-contract self-test.** `sklearn._loss` is a PRIVATE module. Before ANY fit,
the bake asserts the contract against the pinned library and **HALTs** if the internals moved. The
self-test is not a comment and not a version string compare: it (a) asserts `PinballLoss.differentiable
is False` and the subclass overrides it True; (b) asserts the gating call site still reads
`self._loss.differentiable`; (c) fits a two-feature toy where the stock construction demonstrably
violates and the subclass demonstrably does not, and asserts **exact** monotonicity on the subclass and
**non-exactness on the stock control** — so the self-test is proven able to fail in both directions
(the standing non-vacuity norm). A HALT here kills the bake.

### 1.2 Hyperparameters re-selected OUT OF SAMPLE (v831 D1 / study B §2.4, I-7)

The incumbent's settings measurably do not transfer: removing the leaf line search bounds every boosting
step (|gradient| ≤ 1, hessian ≡ 1). Study B's selected `lr=1.0, max_iter=800, max_depth=4,
min_samples_leaf=25` is **the prior, not the answer** — it was selected on a different design matrix
(plain `cp._lvl_eff`, not PAR-centred) and a different store.

**SELECTION RULE, DECLARED HERE, BEFORE THE RUN.** Lowest **mean walk-forward pinball** over three
rolling-origin splits by as-of year: train `YEAR <= T`, score `T+1 … T+3`, for `T ∈ {2014, 2017, 2020}`;
five quantiles `Q = [0.10,0.30,0.50,0.70,0.90]`, unweighted mean of the five, unweighted mean of the
three splits. **In-sample loss is reported and NEVER used to choose.** Ties break to the smaller
`max_iter`, then the smaller `learning_rate` (declared so a tie cannot be resolved after the fact).

**THE DESIGN MATRIX IS PAR-CENTRED** (`cp._lvl_eff = par_redesign.lvl_par`) — that is what the shipped
`cm_400` actually trains on (`par_redesign.retrain()`), and selecting on the plain feature would select
for a model the estate does not build. Study B selected on the plain feature; this is a declared
deviation from its numbers, with the reason.

**THE DECLARED GRID — every point will be reported, not just the winner.**

*Stage 1 (learning rate × iterations), at `max_depth=4, min_samples_leaf=25`:*

| | max_iter 400 | max_iter 800 | max_iter 1600 |
|---|---|---|---|
| **learning_rate 0.3** | ● | ● | ● |
| **learning_rate 0.6** | ● | ● | ● |
| **learning_rate 1.0** | ● | ● | ● |
| **learning_rate 1.5** | ● | ● | ● |

12 points. The grid is deliberately EXTENDED past study B's corner (lr 1.0 × 800) in both axes, because
M-58 records that its selection sat on its own grid edge.

*Stage 2 (capacity), one-at-a-time around the stage-1 winner:*
`max_depth ∈ {3, 4, 5}` × `min_samples_leaf ∈ {15, 25, 40}` — the 4 non-centre points of the cross
(depth 3/5 at leaf 25; leaf 15/40 at depth 4), 4 further points.

**INTERIOR-OPTIMUM CHECK (declared):** if the selected point sits on any grid edge, the grid is extended
one step in that direction and the extension reported. A boundary selection is disclosed as such.

*The incumbent `GradientBoostingRegressor` (400/4/0.05/25) is scored on the identical splits as the
comparison arm.*

### 1.3 The age hill (v831 D2 — the owner's peak challenge, on the record)

Study B §2.6. Raw `age` (index 10) is REMOVED and replaced by two derived features around a declared
peak `a*`:

```
u = max(0, a* − age)     # years short of peak      monotonic_cst = −1
v = max(0, age − a*)     # years past peak          monotonic_cst = −1
```

"Value falls the further you are from the peak, in either direction" becomes true **by construction**;
it contains law 6 (AGE FADES) as its right half and does not forbid the measured rise on its left half.
The design matrix becomes **12 features**: `oh[6] + [log(effpk), exposure, tenure, LEVEL, u, v]`. The
level index is UNMOVED at 9.

**`a*` IS SELECTED OUT OF SAMPLE, on the same rule, over a DECLARED GRID:**

    a* ∈ {20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0}

The grid includes **21, 22, 23, 24** as v831 requires; it includes the study's fitted response peak
(**~21.5**, M-57) and the owner's prior (**~23**, "I feel like the highest player value point is at year
5-6 — so age 23 or so on mean, not 21-22?"). **BOTH candidates' numbers will be reported side by side,
whichever wins**, with the mean age curve and its argmax at each.

**Three controls on the same splits, so the age choice is priced and not asserted:**
(i) raw age, no age constraint (the §1.2 selection); (ii) raw age + `monotonic_cst[age] = −1`;
(iii) `u/v` present but age unconstrained. Study B measured all four inside 0.19 % of each other and
concluded D2 is a guarantees question, not an accuracy one — that will be re-measured, not assumed.

**V4, the age-shape census:** 100 % of rows single-peaked (or monotone) in age on the selected model.

**RECORDED FOR THE OWNER (v831's own note, carried so the answer is not mistaken for his question):**
the owner's year-5-6 read most likely comes from the no-arb COHORT path (peak at year 5 ≈ age 23), which
is a COMPOSITION curve (survival × value) and NOT the same object as the band's CONDITIONAL age
response. The selection settles the band's `a*` by measurement; it does not overturn the cohort reading,
and the two will be reported as the two different objects they are.

### 1.4 Mild recency weighting (v831 D3 — owner: "Agree on recency weighting")

Study B M-60, **window-anchored** — the anchoring bug is the finding, not a footnote. Weight on training
row with as-of year `Y`, in a fit whose training window ends at `T`:

    w(Y) = 0.5 ** ((T − Y) / halflife)

anchored to **the end of the training window**, never to `YEAR.max()`. M-55's global anchor made a 6-year
half-life look 6 % worse than flat when the same idea, anchored properly, is a wash.

**DECLARED GRID (v831: 10–16y), selected on the same OOS rule:** `halflife ∈ {10, 12, 14, 16}` years,
plus **uniform (no weight)** as the control. Every point reported. At the final (production) fit the
anchor `T` is the training cap, 2026.

**Stated at the size of the effect, in advance (study B I-25):** this is worth about **0.18 %**. It is a
declared dial, not a derived constant, and it will not be presented as a significant improvement.

### 1.5 Scope (v831 D6 — owner: "Happy to rebake the ones you suggest")

`cm_400` + `q97m` + `peak_model_v4` (+ `pvc_snapshot`, which CO-EMITS with the peak-model build by
design; `rl_model.py:1234` loads it as the peak model's FROZEN train-time PVC feature). **`v0surf`
UNTOUCHED.** **`bust_prior_table`: the peak model trains on the FROZEN table** — the rederivation ruling
is with the owner (ARM 1's FA2 fired exactly where predicted: no producer exists in the repository).
The directive expects ONE cheap refit pass when the table and the final store are settled.

`q97m` gets the SAME exact construction and its OWN out-of-sample selection on the same declared grid at
`alpha = 0.97`, on its own `X/yy` (`_merged_recover.py:60-64`, MSD excluded). **T1 is applied to `cm_400`
only**, exactly as ARM 1 filed: T1 lives in `conditional_prior.build_cond_prior` and in no other
construction, and moving it into `q97m`'s row rule would be a training-row-rule change this arm has not
been ruled to make. The q97m-with-T1 reading stays a side measurement, as ARM 1 left it.

### 1.6 T1 applied, and attributed (v831)

As ARM 1: the `cm_400` candidate carries T1 automatically; a `--t1 off` variant is fitted for the
attribution board ONLY and is never the candidate. **T1's share of total absolute board movement will be
reported.** ARM 1 measured 37.86 % against a prereg prediction of < 15 % and filed the falsification
honestly; this arm carries no prediction about T1's share and simply reports it.

### 1.7 The ratchet retires (v831 D1; study B §4.3, §5.2; M-52)

**FORCED, not chosen.** `_o44_xs()` (`_merged_recover.py:488`) walks `estimators_` to read the step
surface's knots. `HistGradientBoostingRegressor` has no `estimators_`. **The read-site ratchet cannot
load against the new estimator.** That is the decisive cross-check of the whole comparison (F1), and it
means "new estimator + ratchet retained" is not a configuration that exists.

**THE MUST-MOVE PROOF, concretely (study B §4.3), all three boards measured:**

- **(a)** today's shipped board — incumbent forests, ratchet ON = `6fd0f7de`.
- **(b)** the rebaked exact-constrained forests **with the ratchet still on**, built in a SCRATCH engine
  copy whose `_o44_xs()` knot reader is generalised to the new estimator's own bin thresholds — four
  lines, in the evidence tree, NEVER in the shipped engine. This board exists only to be compared.
- **(c)** the rebaked forests with the ratchet **removed from the source** — the branch's engine, and
  the candidate board.

**The proof is `(b) == (c)`**, byte-exact, PLUS the per-row measured no-op: with the exact-constrained
artifacts loaded, the read-site ratchet finds **nothing to fix on any row** — `max` over the nested knot
family returns the row's own raw band, unchanged, on every board row. If (b) and (c) differ materially,
the ratchet was still doing work and the fit did not absorb it (FB3).

**`RL_O33_TAPEROFF` is a DIFFERENT KIND OF DIAL and is not conflated with it** (study B I-15). It is not
a patch on a fit defect; it is a value judgement the owner looked at and adopted ("Yes. I'm adopting.",
v798). It retires **only if** the rebaked ceiling re-derives `asc == 1`. That will be measured. **If it
does not re-derive, O33 STAYS and the finding comes back — it is not fixed in flight.**

---

## 2 · DECLARED SWITCHES — and the one this arm deliberately does NOT add

| name | site | default | status |
|---|---|---|---|
| `RL_ARM2_OUT` | `engine/forward_valuation/build_peak_model_v4.py`, the ONE resolver ARM 1 already built | **unset ⇒ the shipped output paths** | NEW. A path var, `INFRA_ALLOW` class, no `config_sha256` move. ARM 1's `RL_ARM1_OUT` resolver is generalised, not duplicated |
| `RL_CM_PKL`, `RL_Q97M_PKL`, `RL_WS` | as ARM 1 landed them | unchanged | REUSED, not re-declared |

**NO NEW MODEL-SEMANTICS SWITCH IS ADDED, AND THAT IS A DELIBERATE CHOICE WITH A REASON.** A design
switch would have to enter `data/model_config.json`, which moves `config_sha256`, which moves a LIVE pin
(`data/expected_boot.json 'config'`) — forbidden here. The alternative the estate already uses (a
code-default kill-switch outside the manifest, the `RL_O44_LVLMONO` / `RL_O33_TAPEROFF` family) cannot
carry this change either: the design moves the **feature dimension** (11 → 12) and the **estimator
class**, which are properties of the ARTIFACT, not of the environment. An env var that disagreed with
the loaded pickle would be a silent dimension mismatch.

**So the construction is carried BY THE ARTIFACT, which is strictly stronger than a switch.** Each
fitted estimator carries a `_rl_design_spec` dict (a*, feature layout, level index, constraint vector,
construction id, selected settings), which pickles with it and is asserted by Guard 5 exactly as the
pickle's md5 already is. **ONE site** reads it (`wire_redesign.build()`, which is already the one site
that loads the band and rebinds `cp._lvl_eff`) and binds the feature contract. **Two HALTs guard it, and
both will be proven able to fire:**

- **COHERENCE HALT** — the band's spec and the ceiling's spec must be identical (both absent, or equal).
  A candidate band against a live ceiling is exactly the mixed board ARM 1's screen produced (v834 F7);
  this makes that class of run impossible rather than merely visible.
- **PROTECTION HALT** — with the read-site ratchet retired, an engine that loads a band NOT declaring
  the exact-monotone contract is pricing law 3 with neither a fit guarantee nor a read-site repair. It
  HALTs, naming the artifact.

---

## 3 · WHAT WILL BE BUILT

1. `engine/forward_valuation/exact_monotone.py` — the construction of record in ONE place: the
   `GradOnlyPinball` subclass, the HALTing FB4 self-test, the estimator factory, the age-hill transform,
   the window-anchored weight, the design-spec schema. Imported by every fit site so the four-file
   hyperparameter duplication study B §4.1 names cannot recur.
2. `tools/rebake/refit_arm2_design.py` — ONE committed, versioned orchestrator (ARM 1's pattern),
   emitting `cm_400.candidate.pkl`, `q97m.candidate.pkl`, `peak_model_v4.candidate.pkl`,
   `pvc_snapshot.candidate.json` + a `training_stamp_<artifact>.json` **beside each**, every hash
   MEASURED from the artifact, never typed (P4).
3. `tools/rebake/select_arm2.py` — the out-of-sample selection, with the rule and every grid written
   into the script BEFORE the run, emitting the full tables.
4. Engine edits: `conditional_prior.py` (the design construction + the 12-feature bind),
   `_merged_recover.py` (`_feat_infer`, the two HALTs, the O44 retirement), `refit_q97m.py`,
   `_gate1_wf.py` + `_gate1_picksplit.py` (so B2 tests the construction under test, not the incumbent —
   study B §4.1's "all four places at once"), `build_peak_model_v4.py` (`RL_ARM2_OUT`).
5. A **candidate root** in scratch (ARM 1's `make_candidate_root.py`, reused byte-for-byte) so Guard 5
   runs HONESTLY against a coherent candidate world. The worktree's committed `data/expected_boot.json`
   is byte-untouched and will be shown so.
6. Boards: the candidate (c), the ratchet-on twin (b), the T1-off attribution board, and the live board
   (a) as filed.

---

## 4 · PREDICTIONS — numbered so each can be scored right or wrong

**The construction**

- **Q1.** The FB4 self-test PASSES on the pinned sklearn 1.8.0, and is proven able to FAIL (the stock
  `PinballLoss` control violates on the same toy). Falsifier: it cannot be made to fail ⇒ vacuous guard.
- **Q2.** **V3 at RAW reads ZERO** — 0 negative level steps over every board row at the declared grid,
  measured on the band straight off the forests with no ratchet anywhere. **This is the arm's whole
  point.** ARM 1's raw census read 25.49 % (live 23.05 %). Falsifier FB1: any negative step ⇒ the exact
  construction did not survive the real fit; kill the design and do NOT retire the ratchet.
- **Q3.** The read-site census also reads ZERO — trivially, because the ratchet is retired and the two
  censuses are then the same number. Reported so the pair is unambiguous.
- **Q4.** V3 on the FULL DESIGN (every training row, not just the 804 board rows) also reads zero,
  replicating study B M-54's 1,004,720-step result on this store and this feature bind.

**Selection**

- **Q5.** The selected hyperparameters will DIFFER from the incumbent's (400/4/0.05/25). Falsified if
  the incumbent's settings win the declared grid.
- **Q6.** The selected point will be an INTERIOR optimum of the extended grid. Falsified if it lands on
  an edge after the declared extension — which would be disclosed, not hidden.
- **Q7.** All four age arms will sit within **0.5 %** of each other on mean walk-forward pinball
  (study B measured 0.19 % on its own matrix). Falsified if the spread exceeds 0.5 %: that would make
  D2 an accuracy question after all, and it would be reported as such.
- **Q8.** The recency-weight gain over uniform will be **under 0.5 %** and positive at the selected
  half-life. Falsified either way and reported at the size of the effect.
- **Q9.** `a*` will be selected somewhere in 20–24. The owner's ~23 and the study's ~21.5 will BOTH be
  reported with their numbers regardless of which wins.

**Movement**

- **Q10.** vs LIVE `6fd0f7de`: **> 600 of 804 rows move** (ARM 1 alone moved 641 on the store, and this
  arm carries the store move plus the whole design).
- **Q11.** vs ARM 1's `02a554b5`: **> 400 of 804 rows move**. This is **the pure design diff, cleanly
  separated from staleness, and it is the owner's deciding table.** Falsified if under 400 — which would
  mean the design is nearly a no-op on price and would be the headline finding.
- **Q12.** Movement is two-directional on BOTH diffs: up-movers and down-movers each exceed 100.
- **Q13.** The design diff will move **young / thin-evidence rows** more than the store diff did,
  because the age hill and the exact constraint both bite hardest where the prior carries the price.
  ARM 1's store diff concentrated in MID-evidence rows (23–80 games, median 8.42 %), which this seat
  did NOT predict last time — so this prediction is made with low confidence and will be scored.

**Battery**

- **Q14.** B2 / B6 / G-Y0 all PASS on the candidate board, with the gate scripts running the CONSTRUCTION
  UNDER TEST. Falsifier: any of them fails.
- **Q15.** Pinball on study A §5.1's protocol beats **3.9788** (the PAR-centred zero point ARM 1 filed)
  and beats the incumbent on the same splits. Falsifier FB2: worse than the incumbent at any horizon
  after out-of-sample selection ⇒ the constraint is buying shape at a cost the data refuses; report and
  stop.
- **Q16.** The law-9 mint is non-zero. **Reported, not gated (v830).** No prediction on sign: ARM 1
  minted +0.865 %, and retiring a one-sided read-site operator could plausibly move it either way.
- **Q17.** P12 no-arb: **0 new breaches** on this arm's own candidate, taken on THIS arm and never
  inherited from ARM 1.
- **Q18.** Fit-twice: `cm_400` byte-identical on this box. `q97m` is expected to be ORDER-dependent —
  ARM 1 measured that its pickle md5 is not a function of the model (pickle memoisation), and the design
  arm does not fix it. Recorded honestly either way.
- **Q19.** The must-move proof: boards **(b) and (c) are byte-identical**, and the ratchet's per-row
  effect on the candidate artifacts is **exactly zero on every board row**. Falsifier FB3: any
  difference ⇒ the ratchet was still doing work; the retirement does not stand and comes back to the
  supervisor.
- **Q20.** `asc == 1` re-derives on the rebaked ceiling ⇒ O33 may retire. **Low confidence.** If it does
  not re-derive, O33 STAYS and the finding is reported (I-15).

**Byte-unmoved**

- **Q21.** `data/expected_boot.json`, `data/release_contract.json`, the live pickles,
  `/home/claude/cm_400.pkl` and `/home/claude/q97m.pkl` are byte-unmoved at the end of the arm, shown by
  measured md5s. The `fv` pin moves and is DECLARED (ARM 1 already moved it; this arm moves it further
  by editing `build_peak_model_v4.py` and `conditional_prior.py`). The re-pin is owed at the LANDING
  act and is deliberately not taken here.
- **Q22.** `config_sha256` is UNMOVED across every edit in this arm. Falsifier: any move ⇒ a
  model-semantics switch leaked into the manifest; revert and find another route.

---

## 5 · FALSIFIERS — results that stop this arm

- **FB1.** V3 returns any negative step on the constrained forests → the exact construction did not
  survive the real fit and the private-API dependency has moved. **Kill the design; do not retire the
  ratchet.** (Study B's own FB1, carried verbatim.)
- **FB2.** Walk-forward shows the rebake worse than the incumbent at any horizon after out-of-sample
  selection → **report and stop.**
- **FB3.** Board (c) does not reproduce board (b) → the must-move proof has failed.
- **FB4.** The `sklearn._loss` self-test fails → the private contract moved. **HALT the bake.**
- **FB5.** Movement concentrates in a population the diagnosis did NOT predict → the rebake is doing
  something other than what it claims. (Scored, not fatal; ARM 1's P4 already landed here.)
- **FA-carry.** ARM 1's structural falsifiers ride unchanged: any gate that cannot be RUN is reported
  UNMEASURED, never "assumed passing" (P5); any live pin, tag or release-contract move is an abort, not
  a footnote; a guard that cannot be shown able to fire is a vacuous guard.

---

## 6 · WHAT THIS ARM WILL NOT DO

No scope beyond v831 D6. **`v0surf` untouched.** `bust_prior_table` is NOT rederived — the peak model
trains on the FROZEN table, per the directive, pending the owner's ruling. No live-pin moves, no tags,
no rulebook edits, no `docs/register/` writes, no PRs, **no pushes** — the supervisor reviews, verifies
by re-running the deciding figures, and lands nothing without the owner's word. The live board moves
ONCE, at week's end, on his word, through `tools/land lever`.
