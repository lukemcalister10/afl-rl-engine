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

**Superseded by ADDENDUM A below — read that table, not this one.**

| word | leg | state |
|---|---|---|
| the par teaching-window / 2003-censoring word | **L2 — HALT point** | candidates measured and presented at rehearsal; **narrowed to one limb** by THE BUST RULING |
| Kirkby + Looby DOB (one word each) | courier | seam recommends **YEAR-ONLY**; other 300 rows cleared |
| the EXECUTION word | before any landing bake | follows a seam-verified rehearsal hand-back |
| adoption word · FHV word (three sites) · five SCAR→VOR relabels | L8 / adoption | owner's separate act |
| trade-desk pick-split fix timing | UI lane | live defect today, pre-dates this job |

---

# ADDENDUM A — post-audit updates (seam relay, 2026-07-31, issuecomment-5138572658)

The runbook PASSED as filed. Three items post-date it and are carried here rather than by editing the body
in place (a directive is amended by addendum, never edited — v461).

### A.1 — The L2 HALT is CONFIRMED, with a scope allowance

**L3 never starts before the owner's window word.** Confirmed by the seam. **Allowed during the window:**
non-training preparation — code, harness, probes. **Not allowed:** anything that teaches, fits, or retrains
on a treatment the owner has not chosen. So L3's `conditional_prior` edits may be *written and probed*
against both treatments; nothing is *fitted* until the word lands.

### A.2 — THE COURIER IS FULLY CLEARED, 302 of 302

**Kirkby and Looby are RULED YEAR-ONLY** — the seam's recommendation is now the ruling. So:

| batch | rows | write |
|---|---|---|
| sheet 1 (played/scored) + supplement (never scored) + the 2 internationals | **300** | full date — `_by` **and** `_bd` |
| Ruory Kirkby · Tim Looby | **2** | **`_by` only** (1986 / 1987) — year-only is a first-class store state; `_bd` deliberately absent |
| **total** | **302 of 302** | zero unlisted, zero pending |

**Provenance is recorded per row.** The two year-only rows carry their dissent in the courier record: the
day-level conflict (Kirkby `30 Mar 1986` vs `1986-04-02`; Looby `02 Apr 1987` vs `1987-02-04`, a genuine
upstream transposition) is preserved as provenance, not resolved by silent choice. The years are undisputed
in every source, and year precision is what the age features consume.

**Consequence for L4's age-source census:** the census token set already distinguishes **REAL-DATE (`_bd`)**
from **REAL-YEAR (`_by`)**, so the 2 year-only rows land as REAL-YEAR, not FALLBACK. Post-courier the
expected census on the training population is **FALLBACK → 0** for these 302 (300 REAL-DATE + 2 REAL-YEAR),
and the leg HALTs if the fallback count does not fall by exactly the number of rows written.

**No change to the courier act's shape:** one atomic exact-byte write, join by `stable_player_id`, all pins
enumerated, #283-pattern lane.

### A.3 — The trade-desk word is DISCHARGED; #292 is a parallel seat

The trade-desk pick-split defect (picks 66–80 priced at 0, pick 65 as an ordinal — vs `RULEBOOK v2.1` law 4,
which `ingest_inputs.price_pick` implements correctly) **leaves this runbook's scope**. It is **#292**, fired
as a parallel UI seat. L8's queue drops it.

**Line pointers re-measured for the incoming seat** — the inventory's cite (lane C C8: `:63, :78, :86`;
INDEX: `:23,66`) has drifted. Measured at this tip: **`pickVal` at `:21`** (`pvc[String(n)] ?? 0` — the
`?? 0` is the defect), **the `for (let n = 1; n <= 80 …)` type-ahead loop at `:66`**, and the user-facing
`1–80` strings at **`:81`** (placeholder) and **`:89`** (no-match), with a third at `:141` in a comment.
Measured against the shipped bundle, `board_view_working.js` `pvc` has exactly **65 keys**, so 66–80 price
at 0 and 65 prices at the pool as though it were an ordinal.

**Coordination note, since two seats now touch adjacent surfaces:** #292 works `ui/app/trade.js`; this job
touches `ui/data/` bundles, `ui/release_pick_curve.json`, `ui/app/config.js` (FHV) and
`ui/tests/ui_222_items.test.mjs` at adoption. The overlap is the **rendered pick prices** — #292 fixes how
the desk *reads* the ladder; this job changes *what the ladder is*. They must not land a shared file in the
same window; if #292 lands first, this job's adoption re-denominates underneath a desk that is by then
reading the ladder correctly, which is the better order.

### A.4 — WORDS OUTSTANDING (replaces §8's table)

| word | leg | state |
|---|---|---|
| **the L2 window word** | **L2 — HALT point** | candidates measured and presented at the halt; narrowed to one limb by THE BUST RULING |
| **the EXECUTION word** | before any landing bake | follows this rehearsal's seam-verified hand-back |
| **the adoption set** — adoption word · FHV word (three sites) · the five SCAR→VOR relabels | L8 / adoption | owner's separate act |

Discharged since filing: the two DOB words (A.2) · the trade-desk timing word (A.3).

### A.5 — REHEARSAL POSTURE

Released to rehearse L0–L8: **unbakeable throughout** (no landing bake, no pin moved on this branch's
product files, no adoption), **every gate fired in anger**, the **L2 candidates measured and presented at
the halt**, **cost measured per leg**. Hand back for seam verification; the EXECUTION word follows.

---

# ADDENDUM B — REHEARSAL FINDINGS (L0 complete · L1 BLOCKED). The runbook is amended by these.

Rehearsal run in a scratch clone (full history, `git fetch --unshallow` — hazard class 6 cleared),
workspace seeded from the scratch tree, gates fired in anger. **L1 as filed is NOT EXECUTABLE.** Four
defects, each reproduced at source, and one self-caught process violation.

## B.0 — Costs measured (this container, cp312 pinned stack)

| act | measured |
|---|---|
| `setup_env.sh` (idempotent re-prove) | ~1s |
| `bootstrap.sh` + Guard 5 | **1.6s** |
| `rl_export.py` (board build, `RL_CONFIG_MODE=bake`) | **132s** |
| `s4_matrix_M1v7.py` (book build) | **179s** |
| board + book together | **311s** (the record's "385s/cycle" is the right order; 311s is this container's) |
| `one_source_selftest.py` — baseline, PASS | **103s** |
| `one_source_selftest.py` — Guard-5-fail path | **143s** (a failing gate costs MORE than a passing one) |
| `ruling_config_check.py` · `config_manifest.py check` | <1s each |
| `guard_correction_canary.py` | **>8 min, did not finish** — it does a full rebuild with an edited store |

**A full L1 cycle is therefore ~7–9 minutes** (bootstrap + board + book + selftest), before the canary.
L6's convergence is N of these; at 3 passes that is ~25 minutes of pure compute, plus the refit.

## B.1 — L0 IS DONE, and its denominator is **187**

Acceptance 2's denominator: **187 canonical rows**, from 209 lane rows (A 62 · B **53** · C 94) less 22
merged away across **21 adjudicated cross-lane merge sets**. Artifacts:
`out/l0_rows_raw.json` · `out/l0_canonical_adjudicated.json`, with the merge table and the deliberate
NON-merges published so each call can be argued with.

**THE DEDUP IS NOT MECHANIZABLE — the runbook under-costed L0.** Three defensible mechanical rules gave
three different denominators (130 merging on file; 207 merging on file+field; 6 vs 16 cross-lane candidates
depending only on the file-detection rule). The lanes use incompatible row granularity — A is one dial per
row, B one file-block per row, C one pin/field per row — so no regex resolves them. The cross-lane merges
were adjudicated **by hand**. L0 is not "estimated hours, measurement-parallel"; it is careful seat work.

**Lane B's count defect, resolved by derivation record.** Lane B has **53 table rows** (8+10+20+11+4), not
the 47 its header and the INDEX claim. Its STALE-ROOTED count is **22 rows**, not 19: the enumeration's 22
tokens and my extraction agree **exactly**, and the prose's "20 distinct artifacts" reconciles as 22 − 2
merges (A1+A2 both `pvc_curve_v2.json`; C1+C2 both the board). So **19 is simply wrong; 22 rows / 20
artifacts is right.** Lane A reproduces exactly (62 rows, all five class counts). Lane C reproduces at 94
rows; its RC count reads 37 against an enumerated 36 because **A9 is dual-class** (RC for board+store,
EXPECTED-TO-MOVE for curve identity) and lane C, unlike lanes A and B, does not document its dual-class
handling.

**The `pvc_fit_candidate` conflict, resolved.** Lane A row 11 says NOT-LIVE; lane B A5 says SR. Verified at
source: `RL_PVCFIT='0'` in the manifest, the engine default resolves to 0 under owner ruling R3, and
`rl_export.py` carries an active R3 BAKE GUARD refusing to write a bakeable board with the fit on. **Lane A
is right for the live-pricing question**; lane B classified by basis without weighting liveness. Disposition
**RETIRED-FROM-LIVE**, not RE-DERIVED. **14 further conflicts** are listed in the artifact for resolution.

## B.2 — DEFECT 1 (blocking): L1(a) moves FIVE identities, not four

**Six of the seven γ sites live in `engine/forward_valuation/`, and `expected_boot.fv` is a hash of that
source set.** Proven in isolation on an otherwise untouched tree:

```
pinned fv                    : d10aa93e977a16a7
fv identity, tree untouched  : d10aa93e977a16a7  MATCH
fv identity, ONE gamma token : 4b8875a6533d1dea  DRIFT
```

A **single-character** γ edit moves the fv pin, and `bootstrap.sh`/Guard 5 then **refuse to boot** ("never
boot on an unverified forward_valuation"). Addendum 3's dependent set — `expected_boot` · `release_contract`
· `release_lineage` · `finalization_state` — enumerates the **config_sha** carriers correctly but misses
that the γ edit independently moves a **different** pin. **L1(a)'s same-commit set is the config_sha four
PLUS `expected_boot.fv`.** Reproduced end-to-end: bootstrap exit=1, Guard 5 HALT.

## B.3 — DEFECT 2 (blocking): the config_sha re-stamp is a FIELD-level act, not a file-level one

A file-level re-stamp of the four dependents **corrupts sealed history.** Measured occurrences of
`45b207c0` at HEAD:

| file | occurrences | what they are |
|---|---|---|
| `expected_boot.json` | 1 — `.config` | **live pin; moves** |
| `release_contract.json` | 1 — `.config_sha256` | **live pin; moves** |
| `release_lineage.json` | **4** — `release_transition.source/destination.config`, `register[1].source/destination.config` | **all historical citations; must NOT move.** A `source.config` records what the config *was*; re-stamping it claims a past transition happened under γ=1.0. The lawful act is a **new** register entry, not a re-stamp. |
| `finalization_state.json` | **6** — `rounds.15…20.release_identity.config` | **rounds 15–19 are sealed production history; must NOT move.** Only the round-20 tail is live, and Addendum 3 routes that to L5 — so **nothing in this file moves at L1.** |

I performed the naive replace, saw it move all ten, and reverted. **The "five-artifact one-commit re-stamp"
is really two fields re-stamped, one file needing a different act (an appended lineage entry), and one file
that does not move at L1 at all.**

## B.4 — DEFECT 3 (blocking): the curve install cannot be separated from the v0surf refit

L1(b) installs the curve; the runbook puts the v0surf refit at L6. **The engine will not boot in between.**
Reproduced: with the curve moved, the selftest HALTs —

```
FAIL GUARD 5: checkout v0surf ce08c2d1 != pinned 84378086 … the FROZEN artifact and its pin are out of sync
              v0surf LOAD-PATH MISMATCH … never boot on an unverified LOADED artifact
```

This is lane A's N1 blocker, live: `_v0surf_sig` hashes `_PVC0` itself, so any curve move invalidates the
frozen signature. Lane A already says *"the re-bake must ride in the same commit"*; the runbook did not
carry that into its leg order. **The v0surf refit is part of L1(b), not L6.** L6 keeps only the
curve↔surface **convergence iteration**.

## B.5 — DEFECT 4: the step-4 E1–E6 diff is not leg-separable, and installs the wrong curve for L1(b)

The built diff applies cleanly at the current tip (every text patch; only the binary `v0surf.pkl`
placeholder fails). But:

1. **It installs the CONVERGED payload `fd9e8b63` (ladder 54,354, s=0.99997), not the stop-point
   `e69a3f38`** that Addendum 3 names as L1(b)'s working substrate. That is the wrong direction: the
   step-4 converged curve was converged against the **un-re-derived** player stack, which L1–L5 are about to
   change. Verified from the artifact: `ruled_curve_final_279.json` carries `factor_s 0.977688`, payload
   `e69a3f38`, **ladder sum 54,722.0 exactly**, head `3000, 2999, 2886, 2453, 1892`, pick 64 = 221.
2. **It leaves `pool_value` at 299, `stamp.statistic` at `"SCAR"`, and `stamp.store_md5` at `265f55d5`** —
   so the FROZEN-RULER set and the pool triplet are untouched. L1(b)'s enumerated same-commit set is real
   additional work the diff does not contain.
3. **It spans four legs**: E1 touches `build_peak_model_v4.py` (L4), E3 installs the per-season par with
   `PAR_DUAL_RULE='primary'` (L2), E5 corrects two docstrings (L5), alongside L1(b)/(c). Under the
   one-column-per-landed-change law it **must be split before any of it lands**.

## B.6 — PROCESS: I violated the one-writer law, and the workspace makes it easy

`/home/claude/rl_workspace` is a **single shared mutable workspace**. I backgrounded the baseline
`guard_correction_canary.py` — which does a full rebuild **with a deliberately edited store** — and then
re-seeded that same workspace for L1. Both runs are therefore **VOID** and are recorded as void, not as
results. This is N10's *"one writer per bake; no parallel engine builds, ever"*, and the design gives no
interlock: nothing warned me. **Amendment: every engine act in this job runs serially, and the runbook's
standing per-leg gate gains a precondition — assert no other engine process is live before seeding.**

## B.7 — Smaller corrections

- **Two** documentation-only γ sites, not one: `par_build.py:18` and **`par_redesign.py:13`** (both `Run:`
  lines). Line numbers drift once E1–E6 applies.
- `distribution_pricing.py`'s setdefault is at **:28** (Addendum 3 cites :27).
- Baseline G-Y0 confirmed live at **3.035%** against ceiling 3.500%, HELD against the 2.000% hard bar —
  the selftest prints it every run, and it PASSES today.

## B.8 — WHAT IS NOT REHEARSED, and why

**L2–L8 are not rehearsed.** They cannot be, honestly: every one of them runs on the flipped substrate, and
**L1 does not currently produce a bootable engine**. Rehearsing L2+ on a tree that halts at Guard 5 would
measure nothing. The blocking order is: amend L1 per B.2–B.5 → re-rehearse L1 to a green boot → then L2's
two window candidates → the halt.

Also outstanding: `guard_correction_canary.py` needs a **serial** baseline run (>8 min), and the four CI
workflows have not been exercised in this container.

---

# ADDENDUM C — THE L1 AMENDMENT. Supersedes §4's L1 and L6 leg text. (Seam GO, 2026-07-31; audits this before re-rehearsal.)

Amends, never edits in place (v461). Folds Addendum B's defects B.2–B.5 plus B.6's process rule. **§4's L1
and the v0surf clause of L6 are superseded by this addendum; everything else in §4 stands.**

## C.0 — A REFINEMENT TO DEFECT 1, in fairness to the step-4 work

Addendum B said the fv pin was missed. Precisely: **the step-4 E1–E6 diff already re-pins it** — its
`expected_boot.json` hunk moves `fv` `d10aa93e`→`28cfe2e6` alongside `engine_head`, `rl_model` and `v0surf`.
The mechanism was known to the *diff*. What omits it is the **directive text** (Addendum 3's dependent set)
and **my runbook** — so an executor following the prose rather than the diff halts at Guard 5, which is what
happened in rehearsal. My additional γ edits moved fv again (`c604f4fd`) past the diff's own re-pin, and
nothing re-stamped it. The defect is real; the fix is well-precedented. Recorded so the step-4 seat is not
credited with an omission that is the text's.

## C.1 — THE COMPLETE L1 IDENTITY SET (hazard class 7: what READS the field, and what STAMPS it)

`release_contract.identities` **mirrors eight `expected_boot` fields byte-for-byte** — measured: `board`,
`balanced_board_md5`, `store`, `engine_head`, `rl_model`, `fv`, `register`, `band`. **Every pin that moves in
`expected_boot` must move in `release_contract.identities` in the same commit.** This is the two-axis
sibling set the standing hazard names, and neither Addendum 3 nor my §4 enumerated it.

| identity | moves at | why |
|---|---|---|
| `model_config.json` `vars.RL_GAMMA` + `config_sha256` | L1(a) | the source of the flip |
| `expected_boot.config` | L1(a) | config_sha carrier |
| `release_contract.config_sha256` | L1(a) | config_sha carrier |
| **`expected_boot.fv`** + **`release_contract.identities.fv`** | **L1(a)** | six of the seven γ sites are in `engine/forward_valuation`; `fv` hashes that source set — **one character moves it** |
| `expected_boot.v0surf` | **L1(b)** | the re-bake (C.3) |
| `expected_boot.engine_head` + `…identities.engine_head` | L1(b)/(c) | `_merged_recover.py` (E2/E4) and `rl_model.py` (E6) change |
| `expected_boot.rl_model` + `…identities.rl_model` | L1(c) | `rl_model.py` changes |
| `release_contract.pvc_provenance` + `contract_sha256` | L1(b) | the curve declaration |
| `release_lineage.json` | **NOT AT L1** — see C.2 | |
| `finalization_state.json` | **NOT AT L1 AT ALL** — see C.2 | |
| `expected_boot.board` / `band` / `q97m` / `peak_model` / `pvc_snapshot` / `bust_prior` | later legs | board at L8; the fitted pins at L4 |

**L1(a) acceptance additions:** `RL_PICK1` provably unmoved at all seven sites **and** in `model_config`
(byte-diff scoped to the γ tokens); and **`fv` re-pinned to the post-edit value in the same commit**, proven
by a clean `bootstrap.sh` exit 0.

## C.2 — SEALED HISTORY: what must NOT be re-stamped, and the act that replaces it

Measured occurrence map of `45b207c0` — **1 + 1 + 4 + 6**:

- `expected_boot.json` `.config` — **1, live, moves.**
- `release_contract.json` `.config_sha256` — **1, live, moves.**
- `release_lineage.json` — **4**, all in `release_transition.source/destination.config` and
  `release_transition_register[1].source/destination.config`. **None moves.** A `source.config` records what
  the config *was*; re-stamping it asserts a past transition happened under γ=1.0.
  **REPLACEMENT ACT:** a **new** `release_transition_register` entry, appended, in the register's own
  existing shape (source identity set → destination identity set + owner word + `column_id`). It is authored
  at **L7**, not L1, because the destination identities do not exist until the landing head. L1 leaves the
  file untouched.
- `finalization_state.json` — **6**, `rounds.15…20.release_identity.config`. **None moves at L1.** Rounds
  15–19 are sealed production history. The round-20 tail is live but Addendum 3 routes it to **L5** as the
  live-tail-vs-sealed-history boundary call, and `movers_R20.json`'s twin stale pins ride with it there.

**Standing rule this establishes:** a config/identity re-stamp is a **FIELD-level** act, enumerated by JSON
path. A file-level string replace is forbidden in this job. The L1 acceptance includes a diff review proving
the ten historical occurrences are **unchanged**.

## C.3 — L1(b) REWRITTEN: the curve installs WITH its v0surf re-bake, in one commit

`data/v0surf.pkl` is **load-or-HALT** and **curve-keyed** — `_v0surf_sig` hashes `_PVC0` itself — so a curve
move invalidates the frozen signature and the engine will not boot. Reproduced in rehearsal. Lane A's N1
says the re-bake must ride in the same commit; §4 wrongly deferred it to L6.

**L1(b), in order:**
1. **Install the STOP-POINT curve `e69a3f38`** as working substrate — **not** the converged `fd9e8b63`.
   Verified from `ruled_curve_final_279.json`: `factor_s` **0.977688**, **ladder Σ(1..64) = 54,722.0
   exactly**, head `3000, 2999, 2886, 2453, 1892`, pick 64 = **221**. (The step-4 diff installs
   `fd9e8b63` — ladder 54,354, pick 64 = 215 — which was converged against the **un-re-derived** player
   stack that L1–L5 are about to change. Installing it would bake in a fixed point of the old world.)
2. Curve artifact fields, all moving together: `curve` (1..64) · `curve_md5` · the **numeraire block**
   carrying `s = 0.977688` · `pool_value` · `stamp.statistic` **SCAR → VOR** · `stamp.store_md5`
   `265f55d5` → **`81d24704`** · `stamp.per_entrant_md5` `2f8b4bd4` → the stop-point input
   (`session_2026-07-30/item279/out/per_entrant_279_vor.json`, md5 **`77eba4d3`** — measured; it is the VOR
   arm, not the SCAR arm `db8c934c`, and the two must never be conflated).
   **`pool_value` installs the stop-point level as declared WORKING SUBSTRATE and is re-measured at L6**
   (seam word on D2). It is not a landing figure and is labelled so in the artifact.
3. **THE v0surf RE-BAKE, same commit:**
   `RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 python3 session_2026-07-18/legf6/scripts/refit_v0surf.py --bake`
   — **all THREE signature states frozen** (import-time, post-`RL_PVCADOPT` L1b-transient, post-`RL_PVC2`),
   or the L1b pass fits live again; that exact defect is recorded at `refit_v0surf.py:56-60`. Then re-pin
   `expected_boot.v0surf`.
4. **E2** (the two-key v0surf signature, `_merged_recover.py`, seam word F1) lands here — it is the
   signature machinery the re-bake depends on.
5. **FROZEN-RULER same-commit set:** `one_source_selftest.py` `_contract_md5` (`:490`),
   `_curve_source_store` (`:499`), `_per_entrant_md5` (`:500`) · `ui/release_pick_curve.json` payload md5,
   file md5, `pool_value`, `per_entrant_md5`, `_doc` rewrite · `release_contract.pvc_provenance` +
   `contract_sha256`. The `:497-498` *"must NOT move"* comment is **OVERRIDDEN BY THIS AUTHORITY**.
6. **E4** (the `draftval` tracks-the-adopted-curve comment correction) rides here as disclosed prose.

**L1(b) acceptance:** `bootstrap.sh` exit 0 and the selftest reaching its checks rather than halting on
Guard 5 — i.e. **a green boot is L1's exit condition**, which §4 never stated.

## C.4 — L6 REDUCED

L6 keeps **only** the curve↔surface **convergence iteration** with G-Y0 measured each pass, and the L6
**re-measurement of POOL / MSD / SSP at the converged fixed point**. The v0surf refit machinery moves to
L1(b); if a later convergence pass moves the curve again, the refit is re-run **as part of that pass**, by
the same same-commit rule.

## C.5 — THE E1–E6 SPLIT, by leg (the diff is not leg-separable as shipped)

All six E-numbers are present in the step-4 diff and it spans four legs. **It must be split before any part
lands** (one column per landed change):

| E | file(s) | what | leg |
|---|---|---|---|
| **E1** | `build_peak_model_v4.py` | hard-assign → `setdefault` for `RL_GAMMA`/`RL_PICK1` | **L1(a)** — this is what lets the γ flip take effect at all; the hard assign would silently overwrite 1.0 back to 0.85 and bake SCAR. *The build's other fixes — `range(1,100)`, the two broken reads, the copy-back — stay at L4.* |
| **E2** | `_merged_recover.py` | two keys join the v0surf signature (seam word F1) | **L1(b)** |
| **E3** | `par_build.py` | per-season par keying + `PAR_DUAL_RULE='primary'` + the loud empty-group HALT | **L2** |
| **E4** | `_merged_recover.py` | `draftval` tracks-the-adopted-curve comment correction | **L1(b)** (disclosed prose) |
| **E5** | `par_build.py`, `par_redesign.py` | two docstrings that falsely claimed "STANDALONE / nothing wired into the engine" when both are on the value path | **L5** DOC-CORRECTED |
| **E6** | `rl_model.py` | `BOARD_FACTOR = (_P1/PVC[1]) × s`, the two-sided re-anchor (seam word F3) | **L1(c)** |

**E3 carries a measured fact worth keeping:** `'primary'` and `'lower'` disagree on exactly **2 of 1,874**
dual rows (both `SF/KPD`), and neither reaches the cohort — so the two rules produce a **byte-identical** par
surface at this cohort. Q2 PRIMARY is ruled regardless; this is why the ruling is cheap here.

## C.6 — THE SERIAL-ENGINE RULE (B.6) and the preboot assert

`/home/claude/rl_workspace` is a **single shared mutable workspace with no interlock**, and
`guard_correction_canary.py` rebuilds through it **with a deliberately edited store**. Two engine acts
cannot overlap.

**Rule.** Every engine act in this job — `bootstrap.sh`, `rl_export.py`, `s4_matrix_M1v7.py`,
`one_source_selftest.py`, `guard_correction_canary.py`, `refit_v0surf.py`, `build_peak_model_v4.py`,
`run_panel.sh` — runs **strictly serially**. No backgrounding, no parallel engine builds, ever (N10).

**Preboot assert, added to every leg's precondition block** — run before seeding the workspace:

```
pgrep -f 'rl_export|s4_matrix|one_source_selftest|guard_correction_canary|refit_v0surf|build_peak_model|run_panel' \
  && { echo "HALT: an engine process is live; the workspace is single-writer"; exit 1; }
```

**Interlock proposed** (cheap, and the standing test says price a guard's upkeep before adding it — this one
is ~5 lines and prevents a whole class of void runs): `bootstrap.sh` writes `/home/claude/.rl_workspace.lock`
carrying its pid and the seeding checkout path; every engine entry point asserts the lock names the tree it
is about to read. **Not added unilaterally — offered for the seam's call**, since it touches a shared script.

**Both rehearsal runs of 2026-07-31 remain VOID** and are cited as void, never as measurements.

## C.7 — COST LINES

| act | measured / estimated |
|---|---|
| Addendum C drafting (docs-only) | ~1 seat-hour, no compute |
| **amended L1 cycle** — bootstrap + board + book + selftest | **~7–9 min compute** per attempt (measured components: 1.6s + 132s + 179s + 103s) |
| **+ the v0surf re-bake now inside L1(b)** | **UNMEASURED** — `refit_v0surf.py --bake` has not been run in this container; it is the first new cost the amendment introduces |
| serial canary baseline (still owed) | **>8 min**, unfinished at the void run |
| L1 attempts expected before green | ≥2 (the identity set is wide; the first attempt prices the second) |

## C.8 — WHAT ADDENDUM C DOES **NOT** CHANGE

The acceptance set (§6) · the courier act (§5, cleared 302/302 per Addendum A) · the L2 HALT and its single
censoring limb · L3–L5 and L7–L8 as filed · the rehearsal posture: **unbakeable, nothing lands, the L2
window word and the EXECUTION word remain the owner's.**

---

# ADDENDUM D — erratum + the two audit conditions. (Seam audit of C: PASS WITH TWO CONDITIONS, 2026-07-31.)

Filed as a block, never in-place (v461). Addendum C stands as filed except where amended here.

## D.1 — ERRATUM (prose only, no act changes)

Addendum C.3 gives the stop-point curve's head as `3000, 2999, 2886, 2453, 1892`. **Position 5 is wrong.**
Re-read from the committed artifact:

| curve | head[1..5] | pick 64 |
|---|---|---|
| **stop-point `e69a3f38`** (L1(b)'s install) | `3000, 2999, 2886, 2453, ` **`1931`** | **221** |
| converged `fd9e8b63` (NOT installed) | `3000, 2999, 2864, 2425, ` `1892` | 215 |

**`1892` is the converged curve's value**, transcribed into the stop-point row — the two curves differ at
positions 3, 4 and 5, and I carried one of them across. Everything C.3 *does* is unaffected: the install is
still `e69a3f38`, `factor_s` 0.977688, **Σ(1..64) = 54,722.0**, pick 64 = 221. Recorded because a head
string is exactly the kind of literal a later sweep would pin.

## D.2 — CONDITION 1 (accepted): the lineage entry re-homes to L8/adoption

C.2 put the appended `release_transition_register` entry at **L7**. The seam is right that this is too early:
a register entry's `destination` requires `board`, `balanced_board_md5`, `release_version` **and
`owner_approved`** — three identities and **an owner word** that exist only at **L8/adoption**.

**Amended:** the appended lineage entry is authored at **L8/adoption**, not L7. **`release_lineage.json` is
untouched at L1 AND at L7.** Its four historical `config` citations never move at any leg. This also means
the entry cannot be pre-drafted with placeholders — an entry whose `owner_approved` is not yet true must not
exist in the file at all.

## D.3 — CONDITION 2 (accepted and discharged): the preboot assert was vacuous; it is now a script, proven both ways

C.6's inline `pgrep -f` **self-matched its own invoking shell and fired with zero engine processes** —
seam-reproduced, and I reproduced it too. Worse, the obvious bracket fix (`rl_ex[p]ort|…`) **also fires**,
because the caller's command line still contains the unbracketed literal for `pgrep -f` to find. An assert
that always fires is hazard class 5 (vacuity) wearing a safety costume: it cannot pass, so in practice it
gets ignored, which is worse than not having it.

**Replaced by `tools/preboot_assert.sh`** — a file, so the pattern never appears in the caller's command
line; it additionally excludes its own pid, its parent, any `pgrep`, and anything named `preboot_assert`.

**Non-vacuity proven in both directions, as the condition requires:**

```
DIRECTION 1 (zero engine processes)     -> "preboot assert PASS"                     exit 0
DIRECTION 2 (two engine-named processes)-> "PREBOOT HALT: an engine process is live" exit 1
                                            + it NAMES the pids and command lines
DIRECTION 1 again, after cleanup        -> "preboot assert PASS"                     exit 0
```

**Every leg's precondition block now reads `bash tools/preboot_assert.sh || exit 1` before seeding the
workspace.** This is the one non-docs file the runbook adds, and it exists because the condition asked for
a script rather than an inline pattern.

## D.4 — SEAM RULINGS RECORDED

- **NO lockfile.** The serial rule plus the fixed assert suffice. My C.6 offer is withdrawn.
  **Reversal condition, as ruled:** a second overlap violation *despite a working assert* re-opens it.
- **The unmeasured `refit_v0surf.py --bake` cost is accepted flagged**, and **its measured line is
  MANDATORY in the next hand-back.**
- C's B.2–B.5 resolutions and the E1 re-homing are confirmed at source by the seam; they stand as filed.

## D.5 — COST LINE

| act | measured |
|---|---|
| Addendum D + the assert script, with both non-vacuity directions proven | ~20 min, negligible compute |

---

# ADDENDUM E — L1 RE-REHEARSAL RESULT. Build lane GREEN; selftest 95 PASS / 2 FAIL; L1 does NOT yet exit.

Filed as a block (v461). One coherent tree, full gate set run against that final state, strictly serial,
preboot assert before every seeding. **Both remaining reds are named and neither is the pair that was
predicted.**

## E.1 — MEASURED COSTS (the `--bake` line is here, as required)

| act | measured |
|---|---|
| `bootstrap.sh` + Guard 5 | **1s** |
| **`refit_v0surf.py --bake`** (the mandatory line) | **71s** (73s on the earlier, discarded pre-E2 run) |
| `rl_export.py` board | **131s** |
| `s4_matrix_M1v7.py` book | **178s** |
| `one_source_selftest.py` | **99–101s** |
| **full L1 chain** (bootstrap→refit→re-seed→board→book→selftest) | **480s ≈ 8 min** |
| `guard_correction_canary.py` (faithful serial baseline) | **595s**, **PASS** |
| ci-guards-equivalent total | **~17 min** |

The `--bake` refit is **far cheaper than feared — 71s**, and the lane **re-pins `expected_boot.v0surf`
itself**, so that pin is not manual work.

## E.2 — WHAT IS GREEN

- **Boot:** `bootstrap.sh` exit 0. Guard 5 passes with `fv` re-pinned `d10aa93e → 461c737b`.
- **Build lane:** board exit 0 (131s), book exit 0 (178s). **No frozen-signature HALT.**
- **All six FROZEN-RULER checks PASS**, including `curve payload md5=e69a3f38 == contract`,
  `stamp store=81d24704 == contract`, `per_entrant=77eba4d3`.
- **Sealed history untouched throughout:** `release_lineage.json` and `finalization_state.json` clean at
  every step — all ten historical `config` occurrences unmoved.
- **`RL_PICK1` unmoved** at all seven γ sites and in the manifest.
- **Independent corroboration:** applying E2/E4/E6 separately produced `engine_head 3c7b0c3c` and
  `rl_model feb4ca0e` — **byte-identical to the step-4 diff's own `expected_boot` hunk**.

## E.3 — THE TWO REMAINING REDS (and why neither is the predicted pair)

The ruled exit condition allowed "only the two declared expected reds (the FROZEN-RULER
candidate-vs-shipped pair)". **That prediction was wrong, and in the good direction:** the FROZEN-RULER pair
was expected to diverge because the pins would *not* move. L1 moves them in-commit, so **all six
FROZEN-RULER checks go GREEN.** Two different reds remain:

1. **F1 numéraire display parity — 666 mismatches.** `board v == round(engine ev / 1.0524)` fails because
   `pick_redenomination.json` still carries the **old-basis 1.0524** while SCALE has moved. This is
   **outstanding L1(c) work**, not a defect. Measured input for the re-base: **SCALE = 4.613902** under the
   amended substrate (the 1.0524 was `4.68336 / 4.45`). **The denominator of the new ratio is a decision, not
   a measurement** — whether the "baked" reference stays 4.45 or becomes the pre-flip SCALE — so I have not
   invented one. L1(c) also owes the three hard-coded fallbacks.
2. **G-Y0 ceiling: live 19.869% vs the 3.500% do-not-exceed.** See E.4.

## E.4 — G-Y0 UNDER THE SUBSTRATE FLIP: 3.035% → 19.869%

| state | G-Y0 |
|---|---|
| baseline (shipped SCAR curve, γ=0.85) | **3.035%** |
| step-4 propagation, converged curve, no player re-derivation | 11.224% |
| **amended L1** (stop-point curve · γ=1.0 · v0surf refit) | **19.869%** |

**This is the expected direction and it is not a failure of L1.** L1 flips the *substrate* only; the player
stack is still SCAR-taught, so moving the pick side to VOR opens the gap further. It is the same phenomenon
the G-Y0 stop measured, now larger because γ propagated as well. **L2–L5 exist to close it.** The number is
recorded as the amended-L1 waypoint, **not** as a landing figure (nothing between L1 and L6 is).

## E.5 — FINDINGS THAT AMEND C AND D

1. **C.3's "all THREE signature states" is an OVER-COUNT — it is TWO.** The refit freezes 2 and states they
   are "every surface this build fits"; the build then completes with **no fit and no HALT**, which is the
   proof. Corrected by measurement, not by accepting the tool's self-report.
2. **C.3 under-specified the numeraire block.** E6 requires **three** keys —`pooled_head_pre_scale`, `s`,
   `published_pin` — bound by `published_pin / pooled_head_pre_scale == s` to **1e-9**, plus
   `published_pin == RL_PICK1`. C.3 named only `s`. My hand-written block halted, **naming the missing key** —
   the assertion working exactly as designed.
3. **OPEN QUESTION, needs a word: which is authoritative, the measured head or the published `s`?**
   Lane C records `s = 3000/3068.4647`; the artifact publishes `s = 0.977688` (6 dp). Using the measured head
   with the rounded `s` gives a **~4e-7** disagreement that **exceeds E6's 1e-9 and HALTS**. Back-deriving the
   head from the rounded `s` (what I did, `H = 3068.4635589268`) satisfies coherence exactly but **misstates
   the measured head by ~0.0011**. The head is the physically meaningful quantity, so full-precision `s`
   looks right — **but that is a call about what the artifact means, not a mechanical fix.**
4. **The curve payload hash recipe is written down NOWHERE.** It is
   `md5(json.dumps(curve, sort_keys=True))` — *string*-sorted keys, default separators — reverse-engineered
   by reproducing the shipped `08ea9375`, then confirmed to reproduce `e69a3f38`. **No helper computes it;
   every consumer only compares stored fields.** I minted a wrong-serialization pin (`0bbbb9ff`) and wrote it
   into three selftest literals, the contract mirror and `pvc_provenance` before catching it — a true hash of
   the wrong bytes, hazard class 1. **L5 disposition owed: name the convention in code.**
5. **An undocumented ASYMMETRIC identity-length convention.** `pvc_curve_v2.stamp.store_md5` is an **8-char
   prefix**; `release_pick_curve.curve_source_store_md5` is the **full 32**; `one_source_selftest.py:527`
   compares them with a **one-sided `[:8]`**. Writing the full md5 into the stamp (the natural act) FAILS the
   check. **L5 disposition owed.**
6. **The refit must follow E2.** E2 changes the v0surf signature function, so a refit run before it is
   discarded work (cost me 73s). **Ordering constraint inside L1(b).**
7. **The int convention is load-bearing on identity:** `int(round(v))` reproduces `e69a3f38`; `float(v)`
   gives `c2321957`. This strengthens the `:930`/`:931` int-cast question framed for L6 — the cast is not
   cosmetic.

## E.6 — L1 DOES NOT EXIT YET. What remains

**Outstanding L1(c):** re-base `pick_redenomination.json` (needs the denominator decision) + its three
hard-coded fallbacks + `rl_model.py:940`'s "SCALE stays frozen" override + `rl_export.py:581`'s
`105000/_F` disposition. Then re-run board + selftest and confirm F1 returns to green.

**Then** the exit condition is met on one coherent tree, and L2's two window candidates can be measured.

---

# ADDENDUM F — the ruled numeraire applied; and a RETRACTION of my own red-1 framing.

## F.1 — The numeraire primitive, as ruled (C.3 refinement)

**The measured head is primitive** (seam ruling 2026-07-31). The artifact now carries:

```
pooled_head_pre_scale = 3068.4647              <- the lane-C MEASURED value, exactly
s                     = 0.9776876364261254     <- DERIVED from it, full precision
published_pin         = 3000.0                 == RL_PICK1
E6 coherence |published_pin/H - s| = 0.000e+00   (tolerance 1e-9)
```

Coherence is exact **by construction**, not by tolerance — the point of making the head primitive. The
6dp `0.977688` in the register and in the shaping artifact's own `factor_s` field is the **rounded
presentation of this same s**, never the stored primitive. My back-derivation is reversed. Reversal
condition: one owner word.

**E6's block requirement, filed as the C.3 refinement:** three keys — `pooled_head_pre_scale`, `s`,
`published_pin` — bound by `published_pin / pooled_head_pre_scale == s` to 1e-9, plus
`published_pin == RL_PICK1`. C.3 named only `s`.

## F.2 — TWO-VS-THREE SIGNATURE STATES: filed as TWO, on a second independent proof

The chain under the ruled numeraire **built with NO refit re-run** (board 125s exit 0, book 191s exit 0, no
frozen-signature HALT). The curve *values* were unchanged and only the numeraire block moved, so this
confirms `_v0surf_sig` is keyed on the curve **values**, not on the artifact. Together with the earlier
"surfaces frozen: 2 → build performs no fit", **C.3's "three signature states" is over-counted and the
answer is TWO**, established twice, neither time by the tool's self-report.

## F.3 — RETRACTION: red 1 was NOT a "numéraire denominator decision". I mis-framed it.

I reported F1's 666 mismatches as needing an owner word on the numéraire denominator. **That was wrong, and
the word was rightly not spent.**

**F1 is INVARIANT to the value of the factor.** Both sides divide by the *same* `_F` read from the *same*
file — `rl_export.py:177` `_nb = lambda x: int(round(x/_F))` writes the board, and
`one_source_selftest.py:66` `_num` applies the identical transform to the recomputed ev. So
`board[k] != _num(gated[k])` reduces to `ev_export[k] != ev_selftest[k]` **for any `_F` whatsoever**.
Re-basing the factor cannot move this check by a single row.

**Confirmed empirically:** the 6dp-`s` run and the full-precision-`s` run produced **identical mismatches —
666 rows, same values** — exactly as F-invariance predicts.

**What F1 is actually reporting** (harry-sheezel, worked):

```
board v written by rl_export = 11883   => the ev the EXPORT saw      = 12505.7
ev the SELFTEST recomputed   = 10371   (raw, pre-divisor)
disagreement                 = 1.2058x  (20.6%)
```

`ev()` is **order/state-dependent** — the selftest says so in its own comment (*"replicate the export's
as-of sequence"*) and calls `ev(p,2026); ev(p,2024); ev(p,2025); ev(p,2027); ev(p,2028)` in that order to
reproduce it. At baseline the replication matches for all 804. **Under the amended substrate it diverges
for 666 of 804, by up to ~20%.** So either the substrate flip made `ev()`'s hidden state materially
order-sensitive, or E6 changed the export's effective sequence.

**This is a real finding, not outstanding paperwork**, and it is the sharpest thing the L1 rehearsal
produced: a parity gate whose correctness depends on hand-replicating a call order, over a function with
order-dependent state, on a stack about to be re-derived leg by leg. **It needs diagnosis before L1(c) is
written, and it may be a defect rather than a re-base.** Docketed.

**What L1(c) still legitimately owes** (unchanged, and separate from F1): the display factor IS stale
against the moved SCALE (measured **4.613902**) for *display* purposes, plus its three hard-coded
fallbacks, the `rl_model.py:940` override, and `rl_export.py:581`'s `105000/_F` disposition.

## F.4 — STATE AT THIS ADDENDUM

Selftest **95 PASS / 2 FAIL**: F1 (F.3, docketed for diagnosis) and G-Y0 **19.869%** (the substrate-flip
waypoint, unchanged by the numeraire refinement to 3dp, as expected from a ~4e-7 relative move in `s`).
All six FROZEN-RULER checks green. Sealed history untouched. Chain 434s.

---

# ADDENDUM G — F1 diagnosis: two candidates eliminated, one test INVALIDATED, one structural cause found.

## G.1 — ELIMINATED, proven: the numéraire factor

F1 is **invariant to `_F`**. `rl_export.py:177` and `one_source_selftest.py:66` divide by the same `_F` from
the same file, so the check reduces to `ev_export != ev_selftest` for any factor. Demonstrated twice: the
6dp-`s` and full-precision-`s` runs produced **identical mismatches, 666 rows at identical values**.
Corroborated independently by the seam (no baked `4.45` anywhere in engine, contract, boot, book builder or
step-4 evidence). **The denominator question is dissolved; it was mine and it was wrong.**

## G.2 — ELIMINATED: iteration source

`rl_export.py:114` iterates `players = g['players']`; the selftest iterates `MA.players`. Same engine list,
same order. Not the cause.

## G.3 — **MY `_LENS_FORM` TEST WAS INVALID. The hypothesis is OPEN, not falsified.**

I patched a selftest copy to set `g['_LENS_FORM']=2026` around the 2027/2028 calls, got the identical 666
mismatches, and reported the hypothesis falsified. **That conclusion does not stand**, because the two
harnesses bind `g` to **different namespaces**:

| harness | binding | namespace |
|---|---|---|
| `rl_export.py:69` | `g = _ens['MA'].__dict__` | **`rl_model`'s** module dict |
| `one_source_selftest.py:114` | `MA=g['MA']; ev=g['ev']` | the dict **`_merged_recover.py` was `exec`'d into** |

So the export writes `_LENS_FORM` into `rl_model`'s namespace, and my probe wrote it into the
`_merged_recover` exec namespace. **The probe set the flag somewhere the export does not**, which is why it
changed nothing. A null result from a probe that never applied the treatment is **not** evidence of no
effect — hazard class 5 wearing the other hat. The hypothesis returns to OPEN and must be re-tested against
the correct namespace.

**Recorded as my second self-falsification of this rehearsal** (after the D7 characterisation), and as the
reason the standing law says re-run rather than reason.

## G.4 — THE STRUCTURAL FINDING (candidate cause, needs confirmation)

**The two harnesses do not share an engine-state namespace.** The export mutates `rl_model.__dict__`
(`_LENS_FORM`, and at `:212` `BASE_REF`/`AGE_REF`/`_pe_clear()`); the selftest's replication runs against the
`_merged_recover` exec dict. Any per-player state the export sets or clears in *its* `g` is therefore not
necessarily the state the replication sees.

That is a coherent mechanism for "matches all 804 at baseline, diverges on 666 under a new substrate": the
namespaces agree on values only while the state that differs between them happens not to bite. **It also
means the gate's whole replication strategy is built on an assumption it never asserts.**

## G.5 — DISPOSITION PROPOSED for L1(c) (with its non-vacuity demonstration)

**Fix the GATE, not the engine** — and stop re-deriving what the export already publishes. `rl_export.py:178`
already keeps `_raw2026` — its own comment says it is retained *"for the order/ratio verification and the
numéraire parity gate"*. The authoritative pre-rebase 2026 ev **already exists**; F1 re-computes it through a
stateful function instead of consuming it.

Proposed: the export publishes `_raw2026` alongside the board; F1 asserts `board[k] == _num(raw2026[k])` and
additionally that the published raw set covers the active set key-for-key. That removes the hand-copied call
sequence, the namespace assumption, and the order-dependence in one act.

**Non-vacuity demonstration required either way:** doctor one published raw value and prove F1 fires naming
that key; doctor the board and prove it fires naming that key. A parity gate that cannot fail on either side
is not a parity gate.

**Not implemented — proposed.** It changes a shipped gate's contract, so it wants the seam's word before it
is written.

## G.6 — STATE

L1 remains **95 PASS / 2 FAIL**, unchanged: F1 (this addendum) and G-Y0 19.869% (waypoint). L1 does not
exit. L2's candidates stay behind it. Costs this pass: probe runs 69s / 71s / 103s, all serial, all
recorded — including the two invalid ones.

---

# ADDENDUM H — F1 SOLVED. An EIGHTH γ site. **L1 EXITS: 96 PASS / 1 FAIL (the accepted G-Y0 waypoint).**

## H.1 — The deciding measurement, and its verdict

Fresh processes, order-clean, three modes, each in its own process:

| mode | mismatches vs the board |
|---|---|
| `single` — `ev(p,2026)` only, no replayed sequence | **666** |
| `replay_selftest` — the gate as written | **666** |
| `replay_export` — with `MA._LENS_FORM` toggled where it is actually read | **666** |
| **agreement between all three modes (raw ev)** | **0 differences** |

So: **`ev()` is NOT order-dependent** here, `_LENS_FORM` has **no effect** on the 2026 value, and the
replication is **not** the defect. The `_LENS_FORM` hypothesis is now properly retired — by a valid test
this time, against `MA`, where `getattr(MA,'_LENS_FORM',None)` actually reads it.

**But the answer is neither branch of the decision rule.** One more measurement decided it:

| recompute | mismatches |
|---|---|
| at the engine's γ default (how the gate runs today) | **666 of 804** |
| at **γ=1.0** (how the bake-mode board was built) | **0 of 804** |

## H.2 — THE CAUSE: an EIGHTH γ site — `rl_model.py:504`, the engine's OWN default

```python
GAMMA = float(os.environ.get('RL_GAMMA','0.85'))   # 0.85=SCAR(concave); 1.0=VOR(linear)
```

The board is built under `RL_CONFIG_MODE=bake`, which loads `model_config.json` → γ=1.0. The selftest runs
**plainly** (`python3 one_source_selftest.py`, no bake mode, no env — `ci-guards.yml:97`), so it resolves γ
from this line → **0.85**. At baseline manifest and default agreed (both 0.85) and F1 passed. Under L1 the
manifest moved and **the default did not**, so the gate recomputed the whole board at SCAR while the board
was VOR.

**This site is in neither Addendum 3's seven, nor my runbook's, nor Addendum C's.** It is the most
consequential of them: **every consumer that does not run in bake/gate mode silently prices at SCAR.** The
seven sites are `setdefault`s in the *forward-valuation* modules and `run_panel.sh`; this is the *engine's*
own default and it governs everything else.

**Fixed:** `'0.85'` → `'1.0'`, `RL_PICK1` refs unmoved, `expected_boot.rl_model` re-stamped
`feb4ca0e → 3b011802` with its `identities` mirror. `engine_head` unchanged (`_merged_recover.py` untouched).

## H.3 — **G.5 IS WITHDRAWN.** The gate was right.

My proposal to re-spec F1 to consume the export's published `_raw2026` would have made F1 pass **while
leaving every non-bake consumer silently on SCAR**. The gate was not broken; it was **correctly detecting a
real basis inconsistency**, exactly as designed. The seam's decision rule — *"do not re-spec the gate to
trust it"* — is what kept this from being papered over, and the right answer turned out to be outside both
of its branches.

**This is the third thing I got wrong this rehearsal, and the most important**: I proposed weakening a gate
that was working.

## H.4 — L1 EXITS

```
bootstrap exit 0 · refit through the declared lane · board exit 0 · book exit 0
selftest: 96 PASS / 1 FAIL
  the single FAIL = G-Y0 19.869% vs the 3.500% ceiling — the ACCEPTED WAYPOINT
  (the 2.000% bar judges the CONVERGED FIXED POINT at L6, not L1)
```

All six FROZEN-RULER checks green · F1 green · F2 green · Guard 5 green · sealed history untouched across
every run of this rehearsal.

**The "two declared expected reds" prediction was wrong in both directions:** the FROZEN-RULER pair went
green (L1 moves those pins in-commit), and the reds that did appear were F1 (a real, now-fixed defect) and
G-Y0 (the accepted waypoint).

## H.5 — L5 DOCKET ENTRIES, by name

1. **`rl_model.py:504` — the engine's own γ default**, and the general class: *a manifest value and a code
   default that must agree, with nothing asserting that they do*. The re-derivation should assert
   manifest-vs-default equality for every `RL_*` the manifest pins, or the next flip repeats this.
2. **Bake-mode vs plain-mode basis divergence:** the board builds under the manifest, the gate runs under
   code defaults. That asymmetry is invisible until the two disagree.
3. **The unshared-namespace binding** (`rl_export.py:69` `g = MA.__dict__` vs `one_source_selftest.py:114`
   `g` = the `_merged_recover` exec dict) — **not** the cause here, but a live footgun that cost two invalid
   probes.
4. **The curve payload hash recipe** — unwritten anywhere; mint the helper (Addendum E.5 finding 4).
5. **The asymmetric identity-length convention** — 8-char stamp vs 32-char contract, one-sided `[:8]`
   (Addendum E.5 finding 5).
6. `ev()`'s hand-copied call sequence in F1 is **unnecessary** — all three modes agree — so the gate can be
   simplified, but **only** as hygiene, never as a way to make a red go away.

## H.6 — COSTS

| act | measured |
|---|---|
| deciding measurement, 3 modes × own process | 80s + 102s + 104s |
| γ=1.0 confirmation run | 82s |
| selftest after the fix | 112s |
| **cumulative L1 rehearsal** | ~6 full chains + 8 probe runs, all serial |

---

# ADDENDUM I — the two closing rulings, and the seat boundary.

## I.1 — The eighth γ site joins L1(a) formally, and its lesson is HAZARD 7 ON A NEW AXIS

`rl_model.py:504` is now part of **L1(a)'s enumerated set**: eight sites, not seven.

**The lesson generalises, and it is hazard class 7 (two-axis sibling sets) on an axis nobody had named:**

> The seven sites **SET** the value (`setdefault` / `export`). `:504` **READS** it, with a fallback.
> A census that enumerates only the writers misses the reader whose default silently disagrees.

**Every future census in this job enumerates BOTH axes** — what sets a value, and what reads it with a
default of its own. The existing hazard-7 formulation ("what READS the changed field *and* what STAMPS the
moved identity") is the identity version of the same shape; this is the *configuration* version.

## I.2 — L5 DOCKET HEADLINE, generalised as ruled

> **For every `RL_*` the manifest pins, the landing asserts `manifest value == code default` — or removes
> the default so the read fails loud.**

A code default that silently disagrees with the manifest is a basis fork that only appears when the two
diverge, i.e. exactly at a re-derivation. Both remedies are acceptable; the assertion is cheaper, the
removal is stronger.

## I.3 — G.5 stays withdrawn

F1 remains **as specified**. It was right.

## I.4 — CONTAINER STATE AT ROTATION

- **Committed:** the runbook (Addenda A–I), `tools/preboot_assert.sh`, and all evidence under
  `docs/evidence/rehearsal_290_2026-07-31/` — including L0's canonical-list artifacts and scripts, and
  `L1_amended/` carrying the full L1-exit tree diff (`L1_amended_state.diff`, which includes the `:504`
  move), the exit selftest, the faithful canary baseline, the refit log, `f1_decide.py`, and all four
  deciding-measurement JSONs.
- **NOT committed, and declared:** the scratch clone at
  `<scratchpad>/rehearsal/repo` holds the L1-exit tree as **17 uncommitted working-tree changes**. It is
  **captured in full** by `L1_amended_state.diff`. The clone itself is **ephemeral and void on container
  reclaim** — nothing in it is a record.
- **Declared VOID, never results:** the two overlapping engine runs of 2026-07-31 (the backgrounded canary
  and the L1 selftest that shared the workspace), and the two invalid `_LENS_FORM` probes (wrong namespace).
  All four are cited as void in Addenda B and G.
- `/home/claude/rl_workspace` and `/home/claude/rl_build` hold build products of the L1-exit tree. They are
  **regenerable by `bootstrap.sh` + the chain** and are not a record.
