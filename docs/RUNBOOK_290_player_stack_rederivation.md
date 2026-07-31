# RUNBOOK — #290, THE PLAYER-STACK RE-DERIVATION

**Authority.** #290 body + Addenda 1–5 + THE BUST RULING (issuecomment-5138401971), as re-sequenced by
**Addendum 3** (which supersedes the body's §"The work" and §"Acceptance" in full). Seam pre-fire audit:
issuecomment-5138041889. Seat's delta read-back: issuecomment-5138348303. Seam read-back audit and the two
blocking words: issuecomment-5138413464.

**Standing.** The FIRE word is on record. This runbook is written for seam audit; **nothing lands before the
EXECUTION word**, which follows a seam-verified rehearsal hand-back. Every leg below is written to be
executed in scratch first, every gate fired in anger, cost measured — and the hand-back reports what this
document got wrong.

**Scope boundary (carried, not re-opened).** Live pricing inputs re-derive; sealed historical records
(lineage, round history, evidence trees) stay history.

---

## 0 · STATE AT FILING — every precondition by content id

Measured in this container, stdlib-only or by `md5sum`, not read from a manifest.

| identity | value | how established |
|---|---|---|
| branch | `claude/seam-relay-step4-fp78jm` | created from `origin/main` |
| base | `c49ed30` (= `origin/main`, the v545 pen) | `git rev-parse` |
| store | `81d2470440a80f72afea4405e94338c5` | `md5sum engine/rl_after/rl_model_data.json` |
| board of record | `f2df6e0a…` | `data/expected_boot.json` `board` |
| engine head | `404e8113` · rl_model `7349a1e4` · fv `d10aa93e` | Guard 5 at bootstrap |
| band (`cm_400`) | `34faa865` · q97m `cfdc7321` · register `652d83e8` | Guard 5 at bootstrap |
| config_sha256 | `45b207c0…` | `data/model_config.json` |
| shipped curve | payload `08ea9375` · file `6506d8b1` · pool 299 · Σ(1..64) **65,925** | re-summed from the artifact |
| step-4 evidence | 31 files, tree `e339b1e9…`, carried from `592c7a2` | tree-hash identity, §1 below |

### The three curve states — every carried figure is labelled with one of these

Addendum 3's L0 iteration-labelling requirement. Measured from `out/propagation_fixed_point.json`.

| state | ladder total | `s` | payload | status |
|---|---|---|---|---|
| step-3 ruled design — **the stop-point** | 54,722 | 0.977688 | `e69a3f38` | L1(b) **working substrate** |
| step-4 iteration 1 | 54,506 | 0.975872 | `7cfca117` | transient, evidence only |
| step-4 iteration 2 — **converged** | **54,354** | **0.999968** | **`fd9e8b63`** | the fixed point step 4 reached |

Consequences, carried into every leg:

- The **whole consistency inventory** was written against the stop-point. Lane C's headline *"−17.0% move in
  the pick unit … the magnitude that drives most of the table"* is the **stop-point** figure; at the
  converged ladder it is **−17.6%** (54,354 / 65,925 = 0.8245). L0 restates it once.
- **POOL 234.3 [206.4, 262.3] / MSD 296.4 / SSP 333.4 are STOP-POINT figures** (step-3 panel
  `session_2026-07-30/item279/panel/levels_pool_msd_ssp.py`). The converged artifact carries **no pool
  level**. Per the seam's word on D2, **L6 re-measures all three at the converged fixed point** before any
  of them is installed or worded off. They are not targets until then.
- Between L1 and L6 the tree carries a curve identity that is **neither shipped nor final**. No measurement
  taken in that window is recorded as a landing figure.

### Environment — provisioned and proven (D6 discharged)

| pin | got | want |
|---|---|---|
| python | 3.12.3 | 3.12.3 |
| numpy | 2.4.4 | 2.4.4 |
| scipy | 1.17.1 | 1.17.1 |
| scikit-learn | 1.8.0 | 1.8.0 |
| openpyxl | 3.1.5 | 3.1.5 |

`bash setup_env.sh` → venv at `$HOME/rl_venv312`, **outside the repo tree**. Pins re-verified by an
independent re-run, not the script's own PASS line: **5/5 exact**. `sys.version_info[:2]==(3,12)` asserted
before any engine import. `bash bootstrap.sh` then seeds `/home/claude/rl_workspace` and passes **Guard 5**
(store · rl_model · fv · cm_400 · q97m · register all == pinned), plus the numpy+OpenBLAS byte-pin check
(item 392). Neither act writes inside the repo — verified `git status` clean after both.

**Activation preamble for every act in this runbook:**

```
export RL_VENV=/root/rl_venv312
export PATH="$RL_VENV/bin:$PATH"
bash setup_env.sh          # idempotent; re-proves the pins
bash bootstrap.sh          # idempotent; Guard 5 on entry
```

---

## 1 · WHAT IS ALREADY DONE (released acts, discharged before this runbook)

**(a) Provision + pin proof** — above. **(b) The D1 evidence pick** — the 31-file step-4 pack cherry-picked
forward onto this branch (`2314c9d` → `ff51827` → `f4c096f`), authorship preserved by the pick. Content
proof: the `session_2026-07-30/item279_step4` tree hash is **`e339b1e96c5b29289666dc23a8971e4890d7c76f` on
both sides**, 31 files each, **0 blob differences**, and the whole diff versus `origin/main` is **31 files /
3,108 insertions / 0 paths outside the evidence directory**. The old branch
`claude/step-4-execution-supervisor-g4edkc` is **untouched at `592c7a2`** (re-verified after the push). This
discharges the retention exposure the seam named: sealed-record-cited evidence was living on a deletable ref.

---

## 2 · A CORRECTION TO MY OWN D7 — issued before it can mislead a leg

My read-back said `build_peak_model_v4.py` *"writes to nowhere in this repo."* Literally true, **materially
misleading**, and the seam accepted D7 as stated — so I correct it here rather than let L4 inherit it.

`/home/claude/rl_workspace/` is **not a dead workstation path**. It is the engine's normal absolute-path
layout, created by `bootstrap.sh:39-43`, which copies `engine/rl_after` and `engine/forward_valuation` into
it; the four gating workflows all create `/home/claude` and run `bootstrap.sh` before anything else. So the
build's **output** paths are live, and the real L4 fix is *not* "rewrite the absolute paths".

Measured, the genuinely broken reads are exactly **two**:

| build reads | reality | disposition |
|---|---|---|
| `…/rl_workspace/forward_valuation/dob_corrected.json` | **untracked anywhere in the repo**, so bootstrap never copies it | **RETIRED as an input class** (Addendum 1) — DOBs come from store `_by`/`_bd` |
| `…/rl_workspace/forward_valuation/bust_prior_table.json` | file lives at `engine/rl_after/bust_prior_table.json`, so bootstrap copies it to `…/rl_workspace/**rl_after**/` | **wrong subdirectory** — a one-token path fix (Addendum 1 item 4 is exactly right) |

And one act the read-back missed entirely: the build writes `peak_model_v4.pkl` / `pvc_snapshot.json` /
`bust_prior_table.json` into the **workspace**, so **L4 needs an explicit copy-back into the repo** with an
identity proof on each artifact. That step is written into L4 below.

Everything else in D7 stands and reproduces: the `:8` hard assign of both vars, the `:38`
`np.log(MA.PVC[ep])` substrate dependency, and the `range(1,100)` snapshot loop against a 65-key live PVC
(**KeyError at 66, guaranteed**). L4 remains a **first lawful in-repo build**, so its cost is unmeasured.

---

## 3 · THE RULINGS THIS RUNBOOK EXECUTES UNDER

- **The five #279 rulings** — VOR γ=1.0 · structural completion / class cut ≤2022 / per-season par teaching ·
  control fitter · pooled numeraire · α=1.0. Plus **Q2 PRIMARY**, words **F1/F3**, the corrected **E6**
  two-sided mechanism, **Q1** overwrite-with-logged-history, the **exact-byte courier law**, and the
  **repin sweep law** (outgoing AND incoming literal).
- **S-1 (owner, verbatim):** *"a concluded career votes at FULL evidence weight; the model prior is retired
  from it entirely. The prior may only stand in for the unwritten share of an active career."*
- **S-2:** completion over presumption — actives' unwritten remainders completed actuarially from concluded
  look-alikes, busts' zero-remainders included; the prior survives **only** as an explicit COUNTED
  thin-stratum fallback (a WATCHED NUMBER with its denominator: **5.931% = 71/1,197** at the last build,
  identical at both step-4 iterations — a stable instrument).
- **THE BUST RULING (owner, 2026-07-31).** *"A pick prices what the pick bought FROM THERE."* A draftee —
  including a mature-age redraft — with no scored career after the store-referenced pick is a
  **zero-outcome bust at full weight**; pre-window careers do not count. Three consequences this runbook
  obeys: **(1)** the existing teach-as-zero treatment of never-scored draft rows is now **RULED behaviour —
  no code change, no external data source, no exclusions**; **(2)** Addendum 5's never-scored split (the
  ≥17 with real pre-window games) is **REPORT-ONLY context at L0, not a decision input**; **(3)** the
  censoring word **narrows back to Addendum 2's single limb** — how the 2003 class's *scored* careers handle
  the unobservable 2004 season.
- **N10, the subagent boundary law.** If it MEASURES, fan out. If it WRITES, it is a seat act. **One writer
  per bake; no parallel engine builds, ever.** Every subagent conclusion enters the record only after the
  supervisor re-verifies it **by re-run**. REASONING IS NOT EVIDENCE.

---

## 4 · THE LEGS

Each leg: **preconditions (by content id) → acts in order → measurements → gates → rollback → cost.**

Standing rollback for every leg, stated once: this branch is not main, and **nothing reaches main without
the EXECUTION word plus the housing lane (branch → PR → rebase-merge)**. Per-leg rollback below is therefore
about the *working tree and the workspace*, not about main. `git reset --hard <leg's parent>` plus a
re-run of `bootstrap.sh` restores any leg's entry state exactly, because bootstrap re-seeds the workspace
from the checkout and Guard 5 asserts it.

Standing gate for every leg, stated once: **Guard 5 on entry** (via `bootstrap.sh`) and **`git status` clean
of anything the leg did not intend**. A leg that moves a file it did not declare HALTs.

---

### L0 — BEFORE-PICTURE + THE CANONICAL ROW LIST

**Preconditions.** Base `c49ed30`; store `81d24704`; the evidence pack present at tree `e339b1e9…`; the
three inventory lane reports at `docs/evidence/consistency_inventory_2026-07-31/`.

**Acts, in order.**
1. Pin the tip **by content** (tree id, not branch name) and record it as L0's opening identity.
2. Emit **THE CANONICAL DEDUPED ROW LIST** from lanes A (62 rows) + B (47) + C (94), each row given a
   stable id and a live **disposition column**. Resolve the two known count defects by derivation record:
   lane B's STALE-ROOTED count (the header says 19, the row enumeration lists 22 tokens, the prose names 20
   distinct artifacts) and the `pvc_fit_candidate` classification conflict (lane A row 11 **NOT-LIVE** vs
   lane B A5 **SR**). **Acceptance 2's denominator is this list's own count** — that is what makes "zero
   silent drops" provable rather than asserted.
3. Baseline every identity in §0 and record the **three curve states** table verbatim, with lane C's −17.0%
   restated as −17.6% at the converged ladder.
4. Enumerate the **three** live `1.0524` sites (D3): `one_source_selftest.py:65`, `s4_matrix_M1v7.py:129`,
   `guard_correction_canary.py:112` — plus `rl_export.py:132` recorded as **clean (fails loud, no
   fallback)** and `rl_export.py:581`'s `105000/_F` ground-truth literal recorded as needing a named
   disposition.
5. **Design the F5 REAL assertion.** Today's is vacuous (hazard class 5): `residual_nd_tail` is *defined* as
   `f5_draft_pvc − ΣPVC[1..64]`, so `reconciled: true` survives any ladder. The replacement must be an
   equality that a wrong ladder can break, and it ships with a **non-vacuity demonstration** (a deliberately
   wrong ladder must make it fail).
6. **Report-only (BUST RULING consequence 2):** record Addendum 5's never-scored context — the ≥17 rows with
   real pre-window senior games that the store cannot see (`games` derives from scoring rows; across all 588
   pick-carrying zero-scoring rows only 2 have store `games`>0), and the 67-of-186 first-season-later signal.
   **Context, not a decision input.**

**Measurements.** The list's row count (the denominator); per-lane dedup overlap; the two count-defect
resolutions with their evidence; the −17.6% restatement.

**Gates.** No engine gate — L0 is docs/evidence only. The gate is structural: the diff touches **only**
`docs/evidence/` and `docs/`, and the row list's count is reproducible from the three lane reports by a
re-run.

**Rollback.** Docs-only; `git reset --hard c49ed30`.

**Cost.** Measurement-parallel (subagent fan-out over three lane reports, supervisor re-verifies by re-run).
No bake. Estimated hours, not seat-days.

---

### L1 — THE SUBSTRATE FLIP (γ + curve + scale) · ONE COORDINATED LANDING

**This leg lands as one commit or not at all.** The config_sha re-stamp moves five artifacts together.

**Preconditions.** L0 landed; Guard 5 green; the stop-point curve payload `e69a3f38` available from the
shaping branch `claude/pre-referee-baseline-shaping-4ql38z` (unmerged by design — its engine-side landing is
exactly this act).

#### L1(a) — γ = 1.0

**Acts.** `data/model_config.json` `vars.RL_GAMMA` `"0.85"` → `"1.0"` → recompute `config_sha256` → re-stamp
the **four** measured dependents: `data/expected_boot.json`, `data/release_contract.json`,
`data/release_lineage.json`, `engine/rl_after/ingestion/finalization_state.json`. The
`.weekly_txn/*/manifest.json` (6) and `movers_R15..R20.json` (6) carry the same hash and are **SEALED
HISTORY — they do NOT re-stamp**. Then the **seven** γ pin sites, as disclosed edits:

```
engine/forward_valuation/build_peak_model_v4.py:8   (hard assign)
engine/forward_valuation/distribution_pricing.py:28 (setdefault)   [Addendum 3 cites :27; measured at :28]
engine/forward_valuation/conditional_prior.py:40    (setdefault)
engine/forward_valuation/dist_redesign.py:24        (setdefault)
engine/forward_valuation/par_build.py:21            (setdefault)
engine/forward_valuation/build_cohort_book.py:5     (setdefault)
run_panel.sh:26                                     (export)
```

**Measurements / gates.** `config_manifest.py check` green. **D8's proof, mandatory:** every one of the
seven sites sets `RL_PICK1='3000'` on the same line as `RL_GAMMA`, and `RL_PICK1` is **RULED-CURRENT**. The
byte-diff of this act must be **scoped to the γ tokens only**, and a post-edit grep must show
**`RL_PICK1=3000` unmoved at all seven sites plus `model_config.json`** — proven, not asserted. `par_build.py:11`
carries `RL_GAMMA=0.85` in a docstring `Run:` line — an eighth, **documentation-only** site: DOC-CORRECTED at L5,
**not** here, so the executable diff stays clean.

#### L1(b) — the ruled curve artifact installs (working substrate)

**Acts.** Install payload `e69a3f38` with its numeraire block. The **FROZEN-RULER same-commit set**, enumerated:

- `one_source_selftest.py` — `_contract_md5` (`:490`), `_curve_source_store` (`:499`), `_per_entrant_md5` (`:500`)
- `ui/release_pick_curve.json` — payload md5, file md5, `pool_value`, `per_entrant_md5`, and the `_doc` rewrite
- `data/release_contract.json` — `pvc_provenance` + `contract_sha256`

The comment at `one_source_selftest.py:497-498` — *"nothing was re-derived, so those two pins must NOT
move"* — is **OVERRIDDEN BY THIS AUTHORITY**. It is true of the #274 pool re-stamp it describes and false of
this act, and it is the first thing an adoption commit reads.

**The two per_entrant files are never conflated.** `one_source_selftest.py:500` pins **`2f8b4bd4`** =
`session_2026-07-29/item271/out/per_entrant_271.json` (the curve's derivation input — this moves).
`sibling_repin.py:102` freezes **`40d7da7c`** = `session_2026-07-17/legd_derivation/out/per_entrant.json`
(a byte-freeze whose values are never read — this does **not** move). Both md5s re-verified on disk.

#### L1(c) — E6's two-sided SCALE

**Acts.** Install the rehearsal-built two-sided re-anchor (`BOARD_FACTOR = (_P1/PVC[1]) × s`; no-op control
at `s=1.0` proven `= 3000/4441` exactly). Re-base `pick_redenomination.json`'s `factor` and, **in the same
act**, its **three** hard-coded fallbacks (D3). Override `rl_model.py:940`'s *"SCALE stays frozen"* — same
dead-premise class as the FROZEN-RULER comment. Give `rl_export.py:581`'s `105000/_F` its named disposition.

**Gates for L1 as a whole.** `one_source_selftest.py` · `config_manifest.py check` · `ruling_config_check.py`
· Guard 5. **Expected reds are declared in advance, not discovered:** the two FROZEN-RULER
candidate-vs-shipped fails are the known candidate/shipped divergence (the release mirror re-stamps only at
adoption). Anything else red HALTs the leg.

**Rollback.** Single commit → `git revert` or `reset --hard` to L0's head; `bootstrap.sh` re-seeds the
workspace from the restored checkout and Guard 5 re-asserts.

**Cost.** One bake cycle minimum (385s/cycle per the record — **not my measurement**; re-measured at
rehearsal). The five-artifact re-stamp is mechanical; the risk is atomicity, not time.

---

### L2 — THE PAR SPINE (before the prior, because `cm` trains on `lvl_par`)

**Preconditions.** L1 landed; γ=1.0 live; the ruled curve installed as substrate.

**Acts.** Build per-season keying (`rl_model.py` already carries `_fit_bar(p,Y)` at `:99-105`;
`par_build.gather()` never adopted it — the cleanest single fix in the lane, and it moves lane-A rows 19,
20, 21, 34 and 39 together) + the ruled PRIMARY dual rule. Re-derive the structural gate (today a flat
`MIN_GAMES >= 6g`) and the teaching window (today `DRAFT_LO, DRAFT_HI = 2003, 2018`, i.e. every axis
pre-dates the rulings).

**Measurements — both treatments, presented, not chosen.** Per THE BUST RULING consequence 3, the censoring
word is **one limb only**: censor-aware-2003-inclusive **vs** a uniform 2004+ window. For each: cell
populations, gate classifications, surface deltas. Measured context: store scoring spans **2005–2026 with
zero 2004 rows**; **65** rows of the 2003 draft class carry scoring; tenure anchoring is already
draft-year-based (`conditional_prior.py:51`), so a 2003 draftee's 2005 season already reads as tenure 2 and
nothing imputes zeros.

**THE OWNER WORDS THE WINDOW. I measure both; I do not choose.** This is a **HALT point** — L3 does not
start until the word lands.

**Gates.** `par_build` loud-halt probe (G4, already built at step 4) · Guard 5 · selftest.

**Rollback.** `par_build.py` / `par_redesign.py` revert; no artifact is re-pinned until the word lands.

**Cost.** Two measurement passes (one per candidate) + presentation. No bake until the word.

---

### L3 — THE PRIOR STACK under S-1 / S-2

**Preconditions.** L2's window word landed; par spine rebuilt.

**Acts.** Re-derive `conditional_prior` under S-1 and S-2. The prior is **RETIRED from concluded careers
entirely** — real store markers per #279 C1, and the store carries them (**measured: `_retired` on 1,847
rows, `_last_listed` on 13**). Actives' unwritten remainders complete actuarially from concluded
look-alikes; busts' zero-remainders included **at full weight per THE BUST RULING**. Land Addendum 2's
**bias-1 fix here** (`conditional_prior.py:105-115`): the exposure clock counts 2004 as exposed for the 2003
class while games cannot include it, so play rates read low and base-rate-relative gates can misclassify.
Addendum 3 moved this from Addendum 2's Leg-3/Leg-1 assignment to L3; the correction is carried.

**Measurements.** The thin-stratum fallback share **with its denominator** (baseline 5.931% = 71/1,197) —
a WATCHED NUMBER. The concluded/active split with counts. The exposure-clock delta on the 2003 class.

**Gates.** Selftest · Guard 5 · the fallback share reported with denominator (a bare percentage is a HALT).

**Rollback.** `conditional_prior.py` revert; `cm_400.pkl` is not retrained until L4, so L3 is reversible
without touching a pickle.

**Cost.** One bake cycle + the prior rebuild.

---

### L4 — THE MODEL RETRAINS, on ground that has already moved

**Preconditions.** L1–L3 landed; γ=1.0, ruled curve, ruled par, ruled prior all live. **This is a FIRST
LAWFUL IN-REPO BUILD, not a re-run** — cost unmeasured until rehearsal.

**Acts, in order.**
1. Fix the **`range(1,100)`** snapshot loop to the post-split domain (**1..64 + pool index 65**; the live
   `MA.PVC` has exactly 65 keys — KeyError at 66 today, reproduced).
2. Fix the **two broken reads** per §2: `dob_corrected.json` **retired as an input class** (DOBs from store
   `_by`/`_bd`); `bust_prior_table.json` path corrected from `…/forward_valuation/` to `…/rl_after/`.
   **Do not "fix" the workspace output paths — they are the bootstrap layout and are correct.**
3. Retrain **peak / `cm_400` / `q97m`** on the flipped substrate. `pvc_snapshot.json` re-derives as a
   **PAIR** with `peak_model_v4.pkl` in one act — the co-emit doctrine is the build's own law
   (*"co-generated so they can never drift apart"*), and the anti-skew rule forbids re-pointing the snapshot
   alone. `bust_prior_table.json` regenerates here at the bake per `expected_boot._fitted_note`.
4. Apply Addendum 2's **bias-2** correction: career-total teaching quantities (completions, forward-realised
   targets) understate 2003-class careers by the missing 2004 season.
5. **COPY BACK** each rebuilt artifact from `/home/claude/rl_workspace/…` into the repo, with an md5 identity
   proof per artifact, and re-pin `expected_boot`: `peak_model` · `pvc_snapshot` · `bust_prior` · `band` · `q97m`.
6. **TRAINING-STORE STAMPS, mandatory** on every retrained artifact — closing the no-stamp gap for good
   (today `cm_400`, `q97m`, `peak_model_v4`, `pvc_snapshot`, `bust_prior_table` are pinned by md5 and
   **none records the store or curve it was trained on**).

**THE AGE-SOURCE CENSUS (Addendum 4 — a hard L4 acceptance).** The retrain seal publishes every training row
classified **REAL-DATE (`_bd`) / REAL-YEAR (`_by`) / FALLBACK / EXCLUDED**, totals summing to the training
population as the denominator. Baseline measured on store `81d24704`:

| class | count |
|---|---|
| store rows | 2,651 |
| `_by` present (REAL-YEAR) | 2,349 — of which **848** carry `_bd` (REAL-DATE; `_bd` is an exact subset of `_by`, 848/848) |
| missing `_by` (FALLBACK today) | **302** |

The fallback count becomes a **WATCHED NUMBER** beside the prior-fallback share. This is what makes silent
defaulting arithmetically impossible: today, never-played rows were never *excluded* — they trained with the
fallback age `18.0 + years-since-debut`, an included-with-a-guessed-age distortion frozen inside the current
peak model. It dies here. **Busts are counted in the census** (BUST RULING consequence 4) — the census
counts *age provenance*, not outcome.

**Gates.** Guard 5 · selftest · `config_manifest.py check` · the census totals summing to the denominator
(a census that does not sum HALTs) · every retrained artifact carrying its training-store stamp.

**Rollback.** The pickles are the risk. Each retrain writes to the workspace first; the copy-back into the
repo is the committing act, so rollback is "do not copy back" before the commit, and `git revert` of the
single L4 commit plus `bootstrap.sh` re-seed afterwards.

**Cost.** **UNMEASURED — first lawful build.** Priced at rehearsal, not before. `RL_PRIOR_TREES=400` and the
GBR path are the expensive parts.

---

### L5 — THE DIAL CENSUS

**Preconditions.** L1 landed (so the substrate is ruled). Runs **concurrently with L3/L4** as a
measurement-only census — subagent fan-out, **one writer**, every conclusion re-verified by my re-run.

**Acts.** Disposition **by name** every lane-A row no other leg reaches: the CE remnants (`ALPHA=0.6`/`_ce`,
`PVC_ALPHA_LO/HI`) · `MA.REPL` (v3.3 + a hand dial; deriving script absent from the repo) · the `EXP_*`
floors · `RUC_PRIOR_CAP` / `RUC_CEIL_REFPK` (the ruck-cap bite check folds here) · `R_SURF` · `LAM_SIT` ·
the W4 dial block · `_ABS_EFF` · decliner-shed · `_natcv`/`PICKEQ`/`MECH_STATS` · `lti_return_table.json`
(store `a2fbc9a0`) · `_LSYM_SEAL` · the `finalization_state` round-20 tail (the live-tail-vs-sealed-history
boundary call — and per D4, `movers_R20.json`'s twin stale pins ride with it, since the config_sha re-stamp
moves the hash but **not** those pins) · the 12 documentation-only stale rows, including `par_build.py:11`
from L1(a).

**Token set (widened).** RE-DERIVED · RETIRED-FROM-LIVE · RULED-EXEMPT (owner word) · DOC-CORRECTED ·
DEFERRED-TO-ADOPTION. **UNCLEAR is not a disposition** — it resolves by derivation record or **escalates by
name**, per lane B's own instruction.

**Measurements.** Every disposition carries its evidence pointer. Count against L0's canonical list.

**Gates.** Structural: zero rows of L0's list left without a token.

**Rollback.** Docs + disclosed dial edits; per-row revert.

**Cost.** Parallel measurement; the writer serialises.

---

### L6 — v0surf REFIT, THEN CONVERGENCE

**Preconditions.** L1–L5 landed.

**Acts.**
1. **The v0surf refit through the one declared lane** (`RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 refit_v0surf.py
   --bake`), with the **three-signature reality** named: `_build_v0_curve` runs at import, then again
   post-`RL_PVCADOPT` (the L1b transient) and post-`RL_PVC2`. **All three states must freeze**, or the L1b
   pass fits live again — the exact defect `refit_v0surf.py:56-60` records having already happened once.
   `data/v0surf.pkl` is **load-or-HALT** and curve-keyed (`_v0surf_sig` hashes `_PVC0` itself), so this
   rides in the **same commit** as the curve move with `expected_boot.v0surf` re-pinned.
2. **CONVERGENCE.** Curve ↔ surface iteration to a fixed point. **G-Y0 measured every pass.** Step 4's
   evidence is the prior: the curve reached its own fixed point (s 0.975872 → 0.999968) while G-Y0 **diverged**
   3.035% → 8.353% → 11.224%. That divergence was measured against the *unre-derived* player stack; L1–L5
   exist to change it. **It may still fail — see the acceptance.**
3. **RE-MEASURE THE LEVELS at the converged fixed point** (D2, seam-worded): POOL / MSD / SSP. The
   stop-point values 234.3 / 296.4 / 333.4 are **not** carried forward as targets. Note the MSD/SSP ordering
   inverts versus the schedule live in `ui/app/config.js:54` — so nothing is worded off the old schedule.

**Measurements.** G-Y0 per pass with its denominator; the ladder and `s` per pass; the converged payload;
the three levels with confidence intervals; the fallback share re-checked.

**Gates.** Guard 5 · selftest · G-Y0 · the v0surf frozen-signature HALT proven **able to fire** (a stale
store md5 or v0surf sig must halt — re-proven, as at step 4's G6).

**Rollback.** The v0surf re-bake is the irreversible-feeling act; it is not — the pickle is regenerated from
the lane, and the prior signature set is recoverable from the committed artifact. Revert the L6 commit and
re-run the lane at the prior curve.

**Cost.** N bake cycles, N unknown until the iteration runs. **The dominant cost of the job.**

---

### L7 — GATES AND SEALS

**Preconditions.** L6 converged (or HOLD declared).

**Acts.** Re-seal **F5 with L0's real assertion** at the new totals — **and its fail-closed sibling set in
the SAME landing**: `forward_lens.py`'s `ForwardAuthorityError` sites (it fails closed the moment the F5
seal moves, via `f5_seal_of` / `F5_SEALED_INPUT_REL`), `rl_export.py:657-666`, the `release_contract` block,
the `board_view` mirrors. Re-measure `sealed_entrant_structure` on the current store (its every stamped
identity is superseded: store `968de0c7`, curve payload `89c14729` **pre-split**, board `06d8af60`, PICKEQ
90/92 both > 64). **RETIRE the G-Y0 dated-exception record** — `ceiling_pct 3.50` is a live DO-NOT-EXCEED
bar read by `one_source_selftest.py:577-581`, measured on a curve that no longer exists; leaving it past
adoption is the exact failure the entry was written to prevent. Edit the attributed-column sentinels
(`ui_222_items.test.mjs:123,138`; `ui/app/history.js:12` prose) **per landed column** — the named cost.

**Measurements.** Each re-sealed gate's new value **plus a non-vacuity demonstration** (proven able to fail).

**Gates.** All four gating workflows: `ci-guards` · `final-integration` · `fv-provenance` · `live-scoring`.
`live-scoring-proofs` is dispatch-only and its disposition is **stated in the seal**.

**Rollback.** Seal values are recorded pre-change; revert restores them. The `forward_lens` coupling means
F5 and its siblings revert together or not at all.

**Cost.** One full CI pass + the seal re-measurements.

---

### L8 — THE CANDIDATE BOARD

**Preconditions.** L7 green; acceptance evaluated.

**Acts.** Build the candidate board **beside** shipped. Every mover attributed through the widened channel
set (store-lag + each ruled change + each re-derived leg). **A mover with no named cause HALTs and reports**
(#271's deliverable law). One column per landed change (#279's body). **Adoption remains the owner's
separate act.** Queued behind his word: the **FHV re-denomination** (a two-file, three-site edit —
`ui/app/config.js:56` plus `ui_222_items.test.mjs:369` and `:389`), the **five rendered SCAR→VOR relabels**
(`trade.js:157,160,163,200`; `board.js:117`), and the **trade-desk pick-split fix** (live defect today:
picks 66–80 price at 0 and pick 65 as an ordinal — pre-dates all of this).

**Measurements.** The full mover set with attribution; the unattributed count (**must be zero**).

**Gates.** The HALT-and-report law itself.

**Rollback.** The candidate board is built beside shipped and adopts nothing; rollback is deletion.

**Cost.** One board build + the attribution decomposition.

---

## 5 · THE DOB COURIER ACT

**Standing:** cleared by the seam for **300 of 302 rows**; **2 rows (Ruory Kirkby, Tim Looby) await one
owner word each.** Not on the critical path to rehearsal.

**Verification state (Addendum 5, seam-run).** The 186 (played/scored): **186/186 verified, zero
discrepancies**, day-exact against AFL Tables, namesake hazards resolved by club/era index; 94 carry a third
source. The 114 (never scored): **112 verified**, 111/114 with genuinely independent confirmation (all 114
sheet values match Draftguru character-exact, so Draftguru is treated as the sheet's *source*, not an
independent check); **2 with day-level conflicts, year agreed in both** — Kirkby (`30 Mar 1986` vs
`1986-04-02`) and Looby (`02 Apr 1987` vs `1987-02-04`, a genuine upstream day/month transposition). The 2
internationals: seam-verified (Ó hAilpín 1985-08-24 · Begley 1986-08-31). **Seam recommendation on the two:
YEAR-ONLY** — `_by` without `_bd`, a first-class store state; the years 1986/1987 are undisputed in every
source, and year precision is what the age features consume. The owner's proposed corrections match no
published source found and land only with his word and stated provenance.

**Where it slots.**

1. **Before the courier — at rehearsal.** L4's lane dry-runs at *current* coverage with the census emitted
   and counted (2,349 / 848 / 302 against the training denominator). This proves the census instrument works
   and prices the gap **before any data arrives**.
2. **The courier act.** Both batches land as **ONE atomic, exact-byte act** through the #283-pattern lane:
   overlay → validate → all pins enumerated → atomic commit. Per the owner's word the birth data is
   *"incorporated and written to the store, not separated as an addendum."* **Join by `stable_player_id`,
   never by name** — which is why D5's name-form divergence (store `Aisake O'hAilpin` vs Addendum 4's
   `Aisake Ó hAilpín`) is already immune, as the seam confirmed. Discrepancies from the cross-check **return
   to the owner by name with sources; his values are never altered without his word.**
3. **Sheet-label correction of record (Addendum 5):** both supplements' *"Played games: no"* column meant
   *"no scored seasons."* The store write is unaffected — birth dates are birth dates.
4. **After the courier.** The store md5 **moves**, so every store-pinned identity re-stamps in that same act
   and L4's **final** bake runs on the couriered store with the census re-emitted. **The census is the proof
   the courier worked:** the FALLBACK count must fall by **exactly** the number of rows written, or the leg
   HALTs.
5. **Window-word interaction.** If the uniform-2004+ window wins, **95 of the 302** become moot — measured:
   53 of the 186 plus 42 of the 114 are the 2003 class. So the window word is worth collecting **before** the
   courier lands, not after. (2004/2005 priority: 133 names of sheet 1 — 61 + 72.)

---

## 6 · ACCEPTANCE (Addendum 3, restated — each able to fail)

1. **PASS = G-Y0 ≤ 2.000% at the converged fixed point. Anything else = HOLD** — residual attributed and
   presented; **a HOLD BLOCKS landing and adoption** until the owner rules. Two distinct outcomes; the gate
   can genuinely fail.
2. Every row of **L0's canonical list** carries a disposition from the widened token set; **zero silent
   drops**; the denominator is the list's own count.
3. The closing sweep runs on the **NAMED pair list**, both literals (outgoing AND incoming):
   `08ea9375`→final payload · `265f55d5`→`81d24704` · `2f8b4bd4`→new · 299→the re-measured pool ·
   65,925→new totals · ceiling 3.5 retirement · 190 at adoption · 0.85→1.0. It proves no live
   **literal-carrier** reads a superseded basis; the **UNSTAMPED** inputs are covered by the mandatory
   training-store stamps. The sweep proves what sweeps can prove; stamps prove the rest.
4. Every retrained artifact **stamped**; every re-sealed gate **proven able to fail**.
5. **REHEARSAL NORM IN FULL** — this runbook, end-to-end scratch rehearsal, every gate fired in anger, cost
   measured — before the EXECUTION word.
6. All four gating workflows green on the landing head; `live-scoring-proofs`' dispatch-only disposition
   stated in the seal.

---

## 7 · HAZARDS CARRIED

The standing block — cp312 via `RL_VENV` (now provisioned and proven) · unshallow · `env -i` whitelist ·
**every count names its denominator** · never present an unread number · seal by content — **plus**:

- The **config_sha five-artifact re-stamp moves as one commit or not at all.**
- The **two `per_entrant` files must never be conflated** (`2f8b4bd4` the curve input; `40d7da7c` the
  byte-freeze).
- `sibling_repin` resolves via this rebuild — **its first lawful sibling build**.
- **Reasoning is not evidence.** The two self-falsifications of 2026-07-30 (the seam's word-3 mechanism; the
  seat's `RL_PICK1` transitivity) and the shared no-op `BOARD_FACTOR` misread are the cautionary tales — the
  rehearsal-validation clause caught all three. **§2 of this document is a fourth instance, caught by
  re-running rather than re-reading.**
- **Named hazard class 5 (vacuity)** is live in this job twice: the F5 reconciliation today, and any gate
  re-sealed without a non-vacuity demonstration.

---

## 8 · WORDS OUTSTANDING

| word | leg | state |
|---|---|---|
| the par teaching-window / 2003-censoring word | **L2 — HALT point** | candidates measured and presented at rehearsal; **narrowed to one limb** by THE BUST RULING |
| Kirkby + Looby DOB (one word each) | courier | seam recommends **YEAR-ONLY**; other 300 rows cleared |
| the EXECUTION word | before any landing bake | follows a seam-verified rehearsal hand-back |
| adoption word · FHV word (three sites) · five SCAR→VOR relabels | L8 / adoption | owner's separate act |
| trade-desk pick-split fix timing | UI lane | live defect today, pre-dates this job |
