# MEASUREMENTS LEDGER — Wave-1a "confirm-with-a-number" items on the HONEST board

**Job:** Wave-1a measurements build. READ-ONLY on the engine (no re-fit, no engine/source edit).
Writes only this ledger. Independent of Wave-0b.

## Preamble — the honest base (asserted before any measurement)

- **Base:** `origin/main` @ `7bc5726` by name (the honest v2.5 board; "Refresh doc pack post-v2.5").
- **HEAD SHA:** `7bc5726f64a23edf472676118d2e7ecc90c8c333`.
- **Store assert:** `engine/rl_after/rl_model_data.json` md5 = `e1b4d8bf` == pinned `e1b4d8bf` (baked-v2.5-2026-07-05). **PASS.**
- **Engine:** `_merged_recover.py` md5 = `efea88e5` (workspace `/home/claude/rl_workspace/rl_after`). Panel re-run **10/10 PASS**
  (Daicos 7002 · Bontempelli 3084 · Sheezel 7151 · Gawn 2112 · Reid 3549 · Ward 1650 · Moore 198 · Goad 723 · Smillie 974 · Green 536).
- **Inputs read:** DECISIONS **v70** (`docs/DECISIONS_v70_2026-07-06.md` — the latest DECISIONS in-repo; the task's "v74" is ahead of
  the repo, so v70 is the authoritative decided state used here) · OVERHAUL_SPEC_v1 §6 measurement list
  (`docs/OVERHAUL_SPEC_v1.md` on `claude/fable-synthesis-overhaul-spec-pgfula`).
- **Confirms:** no engine re-fit · no engine/source edit · `main` NOT promoted · only this ledger written.

## Scope decision (spec list cross-checked vs DECISIONS v70)

The confirm-with-a-number list is OVERHAUL_SPEC_v1 §6. Cross-checked against DECISIONS v70; **dropped as dead** (stripped
feature — do not measure): **OV-6 DPP forward-eligibility** (store carries 0 `_fut`/`_futpos`; DECISIONS v70 §LOCKED) and the
**phantom sub-item** of the OV-5 bundle (phantoms scrubbed at v2.5, calibration lift sacrificed — DECISIONS v70 §LOCKED).

---

## RESULT TABLE

| # | item | tag | measured number (labelled) | n | method / provenance |
|---|------|-----|----------------------------|---|---------------------|
| **F7** | games ≠ Σscoring | **UNBLOCKED** | **349 records disagree** (was 377 @ c47cb43d); **329 are a systematic −1 off-by-one** (the actionable class) | 1909 records w/ scoring | direct store recount, e1b4d8bf |
| **F26** | staleness cliff | **UNBLOCKED** | **+103.1%** ns-bar cliff (426→865); was **+102%** @ c47cb43d — cliff persists | synthetic careers | `cliff_demo` re-run on efea88e5 |
| **Pedigree-floor** | B5 floor incidence | **UNBLOCKED** | **53 floor-saves, +1296 aggregate lift**; lift strongly pedigree-ordered (pk1-10 = 490 = 38% of all lift on 21% of pop) | 590 in-scope ND | engine B5 floor, e1b4d8bf |
| **KPF** | elite-KPF elasticity + spread | **UNBLOCKED** | KEY_FWD **spread-ratio 6.09** (val 9.63/prod 1.58) vs MID 4.25; elite-KPF **24.71× value on 1.36× production**; **DISTINCT from OV-2 locus** (0 KPF in recentP≥100 locus; 15/18 elite-KPF young/prime) | 69 est. KFWD / 18 elite | EVID2 method on dataset.json [BAKED efea88e5] |
| **OV-5 census** | store re-cut, 2004 window | **UNBLOCKED** | 2652 records · 1571 ND-with-pick · **decided cohort (2004–18) n=1069** · **RUC decided = 64** (re-stamps ≈41) · **missing `_by` = 302** (re-stamps 175) · RD 693 · pathway 388 | full store | store profiling, e1b4d8bf |
| **M1** | SUSTAINED follow-through | **NEEDS-A-METHOD-CALL** | magnitude HELD ($15,726 withheld / 34 sustained); follow-through verdict blocked on protocol | 46 hits | needs cohort-qualification + censoring ruling |
| **F11** | band feature-skew | **NEEDS-A-METHOD-CALL** | — | — | needs train-feature matrix + distance metric + cohort/mask ruling |
| **F25** | per-club proration delta | **BLOCKED** | — | — | no fixture/per-club schedule data in repo |
| **(injury)** | return-from-injury %s | **BLOCKED** | — | — | must be net of the un-derived OV-1 aging curve |

**5 UNBLOCKED · 2 NEEDS-A-METHOD-CALL · 2 BLOCKED.** (5 unblocked is within the expected band — no >2×/<½× flag.)

---

## MEASURED ITEMS (detail)

### F7 — career `games` vs Σ(scoring-row games) [UNBLOCKED]

**Finding restated:** two sources of truth for career games. Cold review counted **377** disagreements @ `c47cb43d`;
v2.5 fixed an off-by-one class — *whether the class is closed is what we re-measure.*

**Method:** for every store record carrying scoring rows (n=1909), compare top-level `games` to the sum of scoring-row
`games`. Pure read on store `e1b4d8bf`. No smoothing (this is a count, not a distribution over an axis).

**Result — NOT closed. 349 records still disagree**, in three classes:

| class | n | what it is | actionable? |
|---|---|---|---|
| **−1 off-by-one** | **329** | row-sum is exactly 1 **more** than stated career games; spans debut 2011–2025; ND 257 · MSD 20 · RD 33 · others 19 | **YES — the genuine dual-source bug** |
| coverage gap | 18 | `games` **exceeds** row-sum (scoring rows start after debut for older/recruit players; e.g. Zach Tuohy 288 vs Σ268, Luke Breust 308 vs Σ288) | legitimate — pre-2005/pre-coverage seasons, not a bug |
| pathway anomaly | 2 | non-standard pathway rows (Jesse Joyce PDA: Σ182 vs games 64; Josh Worrell −2) | data-hygiene, isolated |

**Named examples (−1 class):** `levi-ashcroft` (games 40, Σ 41) · `murphy-reid` (36 / 37) · `harvey-langford` (35 / 36).

**Verdict:** the F7 dual-source disagreement is **OPEN on v2.5** — 329 records carry a clean 1-game off-by-one. Per the spec
disposition, this triggers "derive top-level games at load (single source) + store-lint assert." **Provenance:** store `e1b4d8bf`.

### F26 — staleness qualification cliff [UNBLOCKED]

**Finding restated:** hard re-pricing cliffs in the staleness/ns family. Headline @ `c47cb43d`: a MID pick-8 career of
(5,5,5,5) games → **433**, vs (6,6,5,5) games → **875** = **+102%** for one extra qualifying season. v2.5 shifted the
coordinates +7 but did **not** touch the staleness family — so we re-stamp the magnitude on `efea88e5`.

**Method:** re-ran the cold-review `cliff_demo` construction against the current engine (synthetic near-identical careers
straddling the `ns` qualification bar; `mk()` aligned to the engine's own `synth()` schema — the "coordinate re-check" the
spec flags as mechanical). Synthetic careers are not in `_REAL`, so the B5 floor/v7 overlay correctly do not apply — the
price is the raw staleness branch, exactly what F26 targets. `ev(p, 2026)`, engine `efea88e5`.

**Result (re-stamped `[efea88e5]`):**

| career (MID pk8, drafted 2022) | ns | ev | step |
|---|---|---|---|
| (5,5,5,5) @55 | 1* | **426** | — |
| (6,6,5,5) @55 | 2 | **865** | **+103.1%** |
| (6,6,6,5) @55 | 3 | 819 | −5.3% |

**Verdict:** cliff **CONFIRMED, +103.1%** on the honest board (was +102% @ c47cb43d — essentially unchanged; v2.5 left the
`ns` counter alone). The companion mediocre-`pr`=0.55 boundary is *not* a sharp cliff at these parameters (steps ±5%);
the +102% headline is the `ns`-bar cliff, and it reproduces. Fix rides Wave 3/4 (fractional `ns` credit), guarded by G-NEW-4.
**Provenance:** engine `efea88e5`, store `e1b4d8bf`.

### Pedigree-floor — B5 floor-saves + incidence by pick pedigree [UNBLOCKED]

**Finding restated:** re-print the floor-saves list + B5 floor incidence by pick pedigree, and assert (or refute) the
claimed **ordering defect**. *Measured BEFORE any P7c floor re-base, so the read informs the re-run rather than being
churned away* (per the spec's explicit sequencing note).

**Method:** the B5 floor is wired in the current engine as
`ev(p,Y) = max(ev_prefloor(p,Y), floor_frac(Y−draftyr) · v0_start(p))`, scope = real ND, not retired/pickless/delisted.
Detected floor-binding (prefloor < floor) per player; bucketed by effective pick (pedigree tiers). Read-only, engine
`efea88e5`. Buckets are diagnostic slices, not derivation bins (statistics rule); the underlying `FLOOR_YRS` schedule is a
signed 6-knot curve, so per-pedigree is the natural reporting axis.

**Result — 53 floor-saves, aggregate lift +1296** (compare pre-v2.5 prototype @ `644d1254`: 51 saves / +1287 — re-stamped
UP slightly on the honest board):

| pedigree | n | binds | incidence % | aggregate lift | median lift |
|---|---|---|---|---|---|
| pk 1–10 | 122 | 10 | 8.2 | **490** | 39.5 |
| pk 11–20 | 114 | 11 | 9.6 | 319 | 29.0 |
| pk 21–30 | 98 | 11 | 11.2 | 156 | 12.0 |
| pk 31–40 | 71 | 5 | 7.0 | 72 | 14.0 |
| pk 41–60 | 141 | 10 | 7.1 | 131 | 12.0 |
| pk 61+ | 44 | 6 | 13.6 | 128 | 16.0 |

**Top saves (key · pick · prefloor→floored · lift):** `paddy-dow` 3 · 13→112 · **+99** · `stephen-coniglio` 3 · 23→112 ·
**+89** · `chayce-jones` 9 · 9→83 · **+74** · `steele-sidebottom` 11 · 3→74 · **+71** · `jaeger-o-meara` 1 · 61→125 · **+64**.

**Ordering assertion — CONFIRMED (as measured, defect-vs-design is an owner read):** incidence is roughly **flat** across
pedigree (7–14%, no monotone), but the **dollar lift is strongly pedigree-ordered** — pk1-10 alone absorbs **490 of 1296
(38%) of all floor lift while being 21% of the population**; median lift falls 39.5 → ~12 from early to mid pedigree. This
is *by construction* — the floor is `frac · v0_start`, and `v0_start` rises with pedigree, so a high-pedigree bust is
floored to a higher number than a low-pedigree bust at the same schedule year. Whether that pedigree-ordering is the
intended "sunk draft capital" behaviour or a **defect** is exactly the owner call the flag anticipates; the *measurement*
(lift monotone in pedigree, incidence flat) is unambiguous and is presented for that ruling. **Provenance:** engine
`efea88e5`, store `e1b4d8bf`, pre-P7c-re-base.

### KPF — elite key-forward transfer elasticity + spread [UNBLOCKED]

**Finding restated:** cut EVID2's value↔production elasticity + spread on the KEY_FWD cell; decide whether it **merges into
OV-2** (KPF inside the aging-elite locus) or is a **distinct** young/prime signal.

**Method:** EVID2 method (value `V:=cur`, production `recentP` = era-normalised last-2-season, from `dataset.json`
[BAKED efea88e5], built from `data/s4_matrix_baked_efea88e5.json` on `main`). Population = LIVE, established (`nseas≥3`,
`recentP>0`). Spread = value p99/p50 ÷ production p99/p50. Elasticity = `dlnV/dlnR`, reported **both** as a global ln-ln OLS
slope **and kernel-smoothed local elasticity** (Gaussian kernel, bandwidth 0.35 in ln-recentP, sampled at production
quantiles — the "finest resolution + smoothing" discipline, not a single wide bin). Elite slice declared as `recentP ≥ p75`
of the established KEY_FWD cell (pooling stated; n=18 is thin — treat as a probe).

**Result — KEY_FWD cell (n=69):**
- spearman(recentP, cur) = **0.582** (weaker than MID's 0.679 — value orders key forwards by production *less* faithfully).
- **spread-ratio = 6.09** (value p99/p50 = 9.63 on production p99/p50 = 1.58) vs **MID reference = 4.25** — KEY_FWD value is
  ~**1.4× more decoupled** from production than MID.
- kernel-smoothed local elasticity dlnV/dlnR rises 1.75 → 3.97 across recentP p25→p90 (steepens with production).

**Result — elite-KPF slice (recentP ≥ p75 = 68.7, n=18):** **value-spread 24.71× on production-spread 1.36×** — the same
decoupling signature as the OV-2 aging-elite locus (3.35× on 1.26×) but **more extreme**. Retention (cur/peakV) is NOT
production-aligned: `josh-treacy` 93.5 → ret 1.00 (cur 5312) vs `jack-gunston` 89.9 → ret 0.16 (cur 928) vs `taylor-walker`
68.7 → ret 0.04 (cur 215). *(Note: the 24.71× max/min is driven by the age tail — Treacy 5312 vs Walker 215; the cell-wide
p99/p50 = 9.63 is the robust figure. n=18 elite is thin, pooled deliberately.)*

**MERGE-VS-DISTINCT VERDICT — DISTINCT (does NOT merge into OV-2):**
- **0 key forwards** fall inside the OV-2 aging-elite locus (age 11–15 **and** recentP≥100) — KEY_FWD production tops out at
  ~93, so the locus's recentP≥100 threshold (a MID-scale cut) **excludes key forwards by construction**.
- **15 of 18 elite-KPF are young/prime (age ≤ 10)** — Treacy(5), Darcy(4), Thilthorpe(5), Cadman(3), Morris(2), Owens(4)…
  The elite-KPF decoupling is driven by **age crossing a lower, position-specific elite band**, spanning young(4–5) vs
  aging(16–18) key forwards at the same ~70–90 production.

**Consequence (for the OV-2 builder, not decided here):** OV-2's locus is defined on a MID-centric `recentP≥100` threshold
that misses key forwards entirely. The KPF decoupling is real and *more* severe (spread-ratio 6.09 cell-wide; 24.71×/1.36×
elite) but lives in a different cell — so it is a **distinct item**, or equivalently OV-2's conditioned-decline fit must be
made **position-relative** rather than absolute-production. **Provenance:** `dataset.json` [BAKED efea88e5] on
`claude/evidence-pack-v2-5-o4wcib`, derived from `data/s4_matrix_baked_efea88e5.json` on `main`.

### OV-5 census — store re-cut on `e1b4d8bf`, 2004 window [UNBLOCKED]

**Finding restated:** every count in PVC spec §2c.2/§5 was profiled on `644d1254`; v2.5 scrubbed phantoms and fixed games,
so the counts move — re-cut before fitting, on the corrected **2004-draft** window (primary-fit-eligible iff draft year ≥ 2004).

**Method:** direct store profiling on `e1b4d8bf`. Decided cohort = ND-with-pick, draft year ∈ [2004, 2018]. Pure read.

**Result:**

| census field | v2.5 (`e1b4d8bf`) | prior (`644d1254`) | note |
|---|---|---|---|
| total records | **2652** | 2656 | phantom scrub net −4 |
| ND records / ND-with-pick | 1571 / **1571** | — / 1572 | every ND now carries a pick |
| RD records | 693 | 693 | unchanged |
| pathway records (non-ND, non-RD) | **388** | 391 | PDN 43·PDA 51·SSP 49·MSD 107·IRE 58·UNR 59·PDS 21 |
| **missing `_by` (birth year)** | **302** | 175 (spec) / 302 (review) | **re-stamps to 302** on the honest board |
| **decided cohort (2004–18 ND-w-pick)** | **1069** | — | window is 2004–18 (corrected), not 2006–18 |
| reference-only (draft < 2004) | 61 (all 2003) | — | never in fit; 2003 = era context only |

**Decided-cohort cell counts (2004–18):** by present_position — MID 311 · GFWD 218 · GDEF 153 · KFWD 132 · KDEF 122 ·
DEF 69 · **RUC 64**; by drafted_position — MID 327 · GFWD 222 · GDEF 132 · KFWD 139 · KDEF 116 · DEF 69 · RUC 64.
**RUC decided = 64** re-stamps the spec's "RUC n≈41" — still thin (the standing pool-the-RUC-shape rule holds), but larger
than the old census.

**Coverage-verify rider (P1's "verify 2005-season-complete + no-other-reason"):** 125 entries are 2004/2005 drafts; **29**
have a first scoring row later than draft+2 (e.g. `tom-williams`, `john-meesen`, `angus-monfries`, `lynden-dunn`) — these
must be eyeballed/printed rather than silently included, per the owner's verification rider. (Flagged, not resolved here.)

**At-draft-position integrity (post-34-reassignments):** `drafted_position` populated for all 2652 records; `drafted ≠
present` for **98** (natural career position moves). All **34** present-position reassignments have `drafted == present`
(expected — they are recent draftees), and **none** of the 34 appear among the 98 drafted≠present divergences — consistent
with the reassignment touching `present_position` only. *(A strict byte-level "untouched" assertion needs the
pre-reassignment snapshot, which is a Wave-0b/evidence artifact; the honest-board consistency check passes.)* **Provenance:**
store `e1b4d8bf`; reassignment list `evidence/f1f2_rewire/the_34_reassignments.json`.

---

## NEEDS-A-METHOD-CALL (measurable, but a genuine method decision is undecided — returned for the owner/supervisor)

### M1 — SUSTAINED-breakout follow-through test [NEEDS-A-METHOD-CALL]

- **What we HOLD (already stamped `[BAKED efea88e5]`):** the M1 up-branch hits **46 players** (34 SUSTAINED, 12 SPIKE),
  withholding **214.49 level pts / $15,726** (sustained share $10,802) at `S_M1=0.46`. Exemplars keyed:
  `sam-berry` pick29 cohort2021 ($932) · `kysaiah-pickett` pick12 cohort2020 ($740). This magnitude is a solved measurement.
- **What is BLOCKED on a method call:** the *new* measurement the spec asks for is the **out-of-sample follow-through** —
  "for historical M1-hit seasons, did SUSTAINED breakouts realise their full (uncredited) level in Y+1/Y+2?" That verdict
  needs three decisions this job must **not** guess: (1) which **historical** cohorts qualify as M1-hits (re-run the
  classifier as-of each past Y, with the leakage protocol); (2) how to **censor** 2024–2026 hits that have no complete
  Y+1/Y+2 yet; (3) the definition of "realise their full level" (threshold on realised vs withheld). Straight measurement
  is impossible until these are ruled — flagged per the judgment guard.

### F11 — band feature-skew report [NEEDS-A-METHOD-CALL]

- **What the spec asks:** train-feature vs inference-feature distribution distance per cohort, plus band-output drift on the
  non-flat population.
- **Why it is a method call (not straight measurement):** the band is a fitted pickle (`cm_400.pkl`); the honest board does
  not carry the **training feature matrix** as a diffable object, and the report needs three undecided rulings — the exact
  **feature set** to compare, the **distance metric** (KS / population-stability-index / Wasserstein), and the **cohort
  partition** + the "non-flat population" mask. Measurable once the training-feature record is located/produced and the
  metric+partition are ruled; not guessable here.

---

## BLOCKED

### F25 — per-club rounds-played deltas at the 2026 cuts [BLOCKED — no data]

The store's scoring rows carry only `{year, avg, games}` — there is **no per-round or per-club fixture/bye schedule** in the
repo. Measuring "per-club rounds-played deltas at the 2026 cuts → implied s/fE shift" requires each club's completed-rounds
count at the snapshot date, which cannot be derived from player game totals alone (a missed game ≠ a bye). A crude proxy
(per-club 2026 games spread) would not isolate the bye-schedule effect and would itself need a method ruling. **Blocker:
external AFL fixture / per-club schedule data, absent from the honest board.**

### Return-from-injury %s [BLOCKED — known, task-specified]

**Confirmed blocked as briefed.** The return-from-injury percentages must be measured **net of the re-derived aging curve**
(OV-1): the return outcome has to be read against the counterfactual ordinary-aging trajectory, or injury-return decay and
ordinary age decay are inseparable. The re-derived aging curve **does not exist yet** (it is OV-1 / Wave-3 derivation work).
**Defer to the derivation phase.** No other coupling-blocked item beyond this one surfaced; the only *other* blocked item is
F25 (data-blocked, above), which is independent.

---

## PLAIN TERMS (league-manager read)

**Numbers we now hold (measured on the honest board, store `e1b4d8bf`):**
1. **The games count still forks for 329 players** — the top-level career-games number is one short of the season-by-season
   sum for 329 players (out of 377 the review first flagged; the bake fixed ~28). It's a tidy off-by-one; the fix is to
   compute career games from one source at load.
2. **The "one more good season" jump is still huge and real: +103%.** A young mid who logs a 6-game season instead of a
   5-game one leaps from ~$426 to ~$865 for that single game crossing the qualification bar. Basically unchanged from before
   the bake (+102%). This is the cliff the fractional-credit fix targets.
3. **The price floor rescues 53 players for +$1,296 total, and it leans hard toward high draft picks** — a top-10-pick bust
   gets floored to a much bigger number than a late-pick bust (top-10 picks soak up 38% of all the floor money while being a
   fifth of the players). Whether that's right ("we paid a lot for him") or wrong is your call — the measurement is on the table.
4. **Key forwards are priced looser to their output than midfielders, and it's a separate problem from the aging-stars one.**
   Value is ~1.4× more spread-out-per-unit-of-production for key forwards, and among the elite key forwards the gap is
   extreme (Josh Treacy at $5,312 vs Jack Gunston at $928 for almost identical recent output — one is 24, one is 34). The
   aging-stars fix (OV-2) would MISS them, because it's defined on a production level key forwards never reach. So key
   forwards need their own fix (or the aging fix rewritten position-by-position).
5. **The draft-pick census is re-counted on the clean board, on the corrected 2004-draft window:** 2,652 players · 1,069 in
   the decision-usable cohort · 64 rucks (up from the old ~41 but still thin — keep pooling them) · 302 players missing a
   birth year (more than the old 175 — needs backfilling before age-resolved fits) · 29 old-draft entries that need a manual
   "is the early data actually complete" check before they go in.

**What we still can't get yet, and why:**
- **The injured-players return rates** — genuinely blocked. You can only measure "how much does a player lose coming back
  from a missed year" once we've rebuilt the normal age curve to subtract off; that curve is later derivation work. Deferred,
  as briefed.
- **The bye-round proration effect (F25)** — blocked on data: we don't have each club's fixture in the repo, so we can't
  measure how uneven bye timing shifts the part-season readings.

**Needs a decision from you before it can be measured:**
- **Did breakout players actually sustain their jump? (M1)** — we hold the dollar figure being withheld ($15,726), but
  proving whether the model is under-crediting real breakouts needs you to rule how to score "did it stick" and how to treat
  recent players who don't have two more seasons yet.
- **The band feature-skew report (F11)** — measurable once we decide which features to compare and with what yardstick; the
  raw training data isn't sitting on the board in a form we can diff.

---

*READ-ONLY measurements job. No engine re-fit, no engine/source edit, `main` not promoted. This ledger is the only artifact
written. All figures labelled with board/engine/store provenance; thin samples (elite-KPF n=18, decided-RUC n=64) pooled and
declared. Thresholds and slice definitions here are diagnostic, not derivation bins.*
