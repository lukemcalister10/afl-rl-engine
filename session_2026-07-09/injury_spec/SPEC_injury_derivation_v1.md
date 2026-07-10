# CHAPTER-3 INJURY/AVAILABILITY — DERIVATION SPEC v1 · 2026-07-09 · FABLE seat
### Job: DIRECTIVE_injury_spec_fable_v1 (manifest tier 6). This is a SPEC — read-only job; Opus
### implements. Base main SHA read on entry: `d4e8f6dc580eccc9bbb3413d324d64ce26bf6b1b` (= tag v2.6).
### Feed asserted: `acceptance_v1_6.json` (loaded as JSON and asserted — guards/anchors cited by ID) ·
### CONSTRAINTS v1.6 · DECISIONS v86 · LTI_REGISTER 2026-07-02 (repo copy, header stamps read:
### machinery lookup RESOLVED-ABSENT, not re-queued · A3 evaluated PRE-LTI-layer · the engine may
### haircut for absence but never re-diagnoses a register entry).
### Inherited decided facts: NO LTI machinery exists (design fresh) · store md5 `e1b4d8bf` (verified
### against `engine/rl_after/rl_model_data.json`) · L1c live at w=0.9 · A3 standing data-caused red ·
### A-DARCY availability attribution becomes real here · KPFFIX↔injury priced here.
### Constraint IDs referenced, never restated: G-COHORT · G-MONO · G-FLOOR (B5) · G-PEAK (B1) ·
### G-CONVEX · G-DATA · G-ATTR · A-DARCY · A-FADE · A3 (gate legend).

---

## §0 · WHAT THE ENGINE HAS TODAY (verified, paths cited — the ground the design stands on)

1. **The ONE store** `engine/rl_after/rl_model_data.json` (md5 `e1b4d8bf` == pin): 2652 players, keyed
   by `key` (slug convention), per-season `scoring` rows `{year, avg, games}`, seasons 2005–2026, 2026
   partial (`_has26`). **No injury/availability field exists in the schema.**
2. **The only availability logic** is `_b2hc` (`rl_model.py:792–803`): a transient, age-banded
   (<27→0.088 · 27–29→0.039 · 30+→0), present-component-only haircut, **inferred** from the store's own
   0-games-in-2026 signal for established players once `SEASON_PROG>1/3`. It is explicitly a stopgap
   ("next build's return data supersedes it"). No return-season haircut anywhere; no register consumer.
3. **Season progress** is one hardcoded constant `SEASON_PROG=0.58` (`rl_model.py:583`, mirrored
   `_merged_recover.py:32`, `conditional_prior.py`). The store has season aggregates only — **no
   per-round data, no live calendar**. In-progress 2026 evidence is judged against prorated bars via
   `fE` (`_merged_recover.py:34–36`) and the concave within-season penalty `τ' = (R/24)^1.5`
   (`_merged_recover.py:809`). The partial-season "gross-up" reading of 2026 games at `rl_model.py:770`
   (`/SEASON_PROG`) is the single most dangerous line for this chapter — see §3.
4. **L1c young credit** (`_merged_recover.py:468–526`, w=0.9): fade-clock keyed on **career games
   played** g, `φ(g)=(1−g/G0)²`, G0=46 — "NEVER career-year" (code comment `:469`). An injured season
   adds ~0 games, so the clock already *implicitly pauses* — fork (i) prices whether that stays.
5. **Sit-out/games-ramp** (`_merged_recover.py:549–607`, applied `:808–820`): V0 held through
   pre-season; retention surface `R_SURF` (class × log-pick × depth, isotonic); evidence blend λ with
   structural endpoints λ(0)=0, λ(bar)=1 (no cliff at graduation); D14 KPP floor. This is the existing
   zero-games-this-season path and the natural seam for the nerf.
6. **Calendar fix state**: M2 exposure-clock proration LANDED (f=0.545); M3 proportional tenure/age
   clock DERIVED-NOT-WIRED (queued). The partial-season games-completion hypothesis was **FALSIFIED**
   (2026-07-01 phase-1 build) — games are priced as they stand; Rozee's 2026 is his real 2 games.
7. **KPFFIX** (`_merged_recover.py:315–412, 843–862`): compresses the loose residual above demonstrated
   output; demonstrated level `LD` = mean of the **top-2 high-games seasons within Y−3..Y**
   (`_kpf_LD`, `:355`); young/speculative (nqual<4 or age<24) never touched by the reward leg.
8. **A3 gate** (`ship_gates_check.py:142–147`): `E(rozee,2026)/E(rozee,2025) ≥ 0.75` — threshold
   already amended 0.80→0.75 data-caused (`:138–141`, SHIP_GATES.md §A3); currently RED (~0.71–0.73).
   Register stamp: **A3 is evaluated PRE-LTI-layer** — this chapter's overlay must not be what passes it.
9. **study-v2** (INJURY_RETURN_STUDY_v2, DECISIONS v75 §14–18): its *numbers do not carry* (netted
   against the old aging curve on a changed engine). What carries: two hypotheses (young LTI = forfeited
   growth year, not ceiling dent; recovery is age-dependent and heterogeneous) and one binding rule —
   **measure net of aging or it double-counts**. The statistics doctrine ("CORE rule 7" in the
   directive) is the standing finest-resolution rule (KICKOFF_PROMPT.md:53): finest resolution the
   sample supports, kernel/local smoothing on continuous axes, pooling declared — no wide-bin single
   numbers. Convention: adaptive-bandwidth Nadaraya-Watson, local eff-n ≥ 35.

**Derivation sample verified to exist** (computed read-only on the store, walk-forward-safe cases):
**184** gap-season return cases (≥5 games in year Y, zero in Y+1, played Y+2, Y+2 ≤ 2024). Raw
return-vs-prior output ratio, age-banded medians: **≤22: 1.03 · 23–26: 1.00 · 27–29: 0.87 · 30+: 0.64**
(n = 45/65/25/7). Read: the raw "haircut" is mostly *aging in disguise* — precisely the double-count
study-v2's rule forbids. A further **513** same-shape cases never returned (confounded with delisting —
attrition, not injury; see §4.4). Position counts (MID 36 · KDEF 34 · GFWD 33 · KFWD 24 · RUC 22 ·
GDEF 18 · DEF 17) — too thin for position-resolved cells; pooling mandatory and declared (§4.2).

---

## §1 · THE OWNER'S TWO-PART SHAPE, MADE PRECISE (the spec's spine)

> Part 1 — **CURRENT-SEASON NERF**: an injured player's current-season value is reduced, scaled by
> season progress: out in round 2 costs more of the season than out in round 20.
> Part 2 — **RETURN-FROM-INJURY PRICING**: derived FRESH per study-v2, **net of new aging** — the
> return-season haircut must not re-charge the aging the player did while out.

Design principle that falls out of the engine survey: **Part 1 is not a new multiplier — it is telling
the machinery the truth about the season.** The engine already prices partial seasons (fE bars, τ',
games-ramp, M2). What it does not know is that a register player's 2026 is *over*. Part 1 therefore
enters as **availability-aware season state**, not as a stacked haircut — which is what keeps it from
double-counting τ'/M2 and keeps G-ATTR attribution clean. Part 2 is the only genuinely *new priced
quantity*, and it is derived, not asserted.

---

## §2 · THE REGISTER AS A VERSIONED ENGINE INPUT

### §2.1 Schema (the owed `key` column delivered — every key VERIFIED against store `e1b4d8bf`; zero guesses)

One row per **injury window** (repeat-LTI players get two rows). Proposed columns:

`key · player · section (A|B) · window_id (1,2,…) · designation (2025 | 2026_preseason | 2026) ·
status (out_until_2027 | may_return_2026 | returned) · returned_year (blank until real) · notes`

The three timing designations map to engine semantics as:

| designation | engine reading of 2026 | return season |
|---|---|---|
| `2025` | zero 2026 games **so far**; return during 2026 possible — governed by fork (iii) | 2026 if returns, else 2027 |
| `2026_preseason` | full-season absence; nil 2026 production; season lost fraction L=1 | 2027 |
| `2026` | 2026 truncated at store games-so-far — those games are FINAL (no gross-up); L = 1 − g₂₀₂₆/G_FULL | 2027 |

Section B rows carry the same **availability** semantics (nil remaining-2026 production) with the
return-season haircut **structurally zero** — not a haircut of size 0, an untouched path, so B4
non-mover parity and A-FADE attribution stay clean.

**The verified key table** (this table ships inside the register file; three names required
disambiguation — the register's name-collision guard earning its keep):

Section A: jack-payne · matt-carroll · jesse-motlop · harry-o-farrell · jamie-elliott ·
reef-mcinnes (windows 1+2) · oscar-steene · brayden-fiorini · lewis-hayes (windows 1+2) ·
**nicholas-martin** (register "Nic Martin") · toby-conway · tom-green · **joshua-kelly** (register
"Josh Kelly" — the GWS 2013 pick-2; `will-kelly`/`tim-kelly` etc. rejected on cohort) · darcy-jones ·
nathan-wardius · jai-culley · jack-viney · andy-moniz-wakefield · jackson-archer · blake-thredgold ·
ollie-lord · esava-ratugolea · josh-sinn · josh-gibcus · judson-clarke · sam-flanders ·
liam-hetherton · **max-king-syd** (register "Maxwell King") · noah-long · jacob-newton ·
deven-robertson · sam-darcy.
Section B: archie-may · harley-barker · brody-mihocek · toby-pink · mani-liddy · ewan-mackinlay ·
connor-rozee · jonty-faull · joel-amartey · noah-chamberlain · harry-edwards.

**Collision evidence (why the key column is non-negotiable):** the store holds `max-king-syd`
(Sydney, pick 49, 2025) and `max-king-stk` (St Kilda, pick 4, 2018) — and they share the **identical
DOB 2007-01-09**. Name+DOB is non-discriminating; only the store key separates them. A third,
`max-king-1` (Maximus King, retired), also exists. This is the toby-briggs lesson in live data.

### §2.2 Validation: report, never re-diagnose

A build-time validator (halt-not-warn on structural errors, report-only on content) checks:
- every `key` exists in the store, exactly once (unknown key → HALT — a mis-keyed haircut is worse
  than none);
- designation-vs-store consistency as **report-only diagnostics** — e.g. `toby-conway` is designated
  "2025" but his last store games are 2024; `oscar-steene` has no 2025 row. Per the register stamp the
  engine **never re-diagnoses**: anomalies are listed in the build report for Luke's next register
  edit, and the register row governs as written.
- repeat-window ordering (window 2 postdates window 1).

### §2.3 Owner workflow

Luke edits the register file (markdown table as today, or the same table as CSV — implementer's
choice, but ONE format); no inference layer ever writes to it. Each edit is a commit; the engine
consumes the committed file at build. Post-edit, the validator's diagnostic table comes back to Luke
in the build report.

### §2.4 SSI compliance — where the register lives (recommendation + priced alternative)

**Recommended: R2 — pinned sidecar input.** The register stays its own file (owner-authored ground
truth, distinct provenance from the scraped store), added to the input pin set exactly as the store
is: md5 pinned in `data/expected_boot.json`, asserted by Guard 5 (`boot_guard.py`) on entry, seeded by
`bootstrap.sh`, a row in `REQUIRED_INPUTS.md`, lookalike tripwire extended to `LTI_REGISTER*` in the
source dir (Guard 3 analogue), and the register md5 **stamped into every derived artifact** (board,
book, gate report, boot identity) alongside the store stamp. SSI is honoured in its operational sense:
one source **per datum** — availability facts have exactly one home, and it is Luke's file.
- *Why not R1 (fold fields into the store)*: it would put owner-authored rows inside a scraped file —
  Luke would hand-edit the one store the whole engine boots on, every register touch would move the
  pinned store md5 (a bake-grade event for a curation edit), and a scraper refresh could silently
  clobber his rows. R1 is cleaner on paper (guards 1–4 apply for free) and is the fallback if the
  owner dislikes a second authored file — priced consequence: register updates become store bakes.
- Either way: **the register is versioned input, the derived availability multipliers are derived
  data** — they appear in exports stamped with both md5s, never hand-edited (Guard 1 discipline).

*Requested owner ruling R-REG: ratify R2 (sidecar + pins) or direct R1 (fold into store).*

---

## §3 · PART 1 — CURRENT-SEASON NERF (design)

### §3.1 The progress measure

The engine's only season clock is `SEASON_PROG` (0.58 today, hand-set). The nerf needs a **per-player
effective season state**, not a new global clock:

- For every non-register player: unchanged — partial 2026, progress `SEASON_PROG`, existing fE/τ'/M2
  treatment.
- For register players out for the remainder of 2026 (designation `2026_preseason`, `2026`, and all
  Section B): the player's 2026 is **complete at g₂₀₂₆ games**. Define per-player
  `fE_p = 1.0` (his season is over) versus the global `fE = SEASON_PROG`, and lost-season fraction
  `L_p = 1 − min(g₂₀₂₆ / G_FULL, 1)` with **G_FULL = the season-length constant the games-ramp already
  uses** (the τ' denominator, 24 — one constant, asserted equal at build, never a second hardcode).
- Designation `2025` names: governed by fork (iii) — until ruled, they sit in the existing 0-games
  sit-out path unchanged.

This gives the owner's scaling for free and continuously: injured after 2 games ⇒ L≈0.92 of the season
lost; after 20 games ⇒ L≈0.17 — no bins, no cliff (G-MONO-compatible by construction).

### §3.2 What the nerf actually touches (and the danger spots it must defuse)

1. **Kill the gross-up** (`rl_model.py:770`): a register name's 2026 production must never be read
   "at pace" (`games/SEASON_PROG`) — he will play no more. His 2026 row is judged as a *final* season
   of g games. This is the mechanical heart of the nerf: out-in-round-2 leaves 2 final games (thin,
   heavily τ'-discounted evidence + a nearly-whole lost season), out-in-round-20 leaves a near-full
   final season.
2. **Do not double-charge τ'/λ/M2**: with `fE_p = 1.0`, the within-season penalty τ' and the λ
   evidence blend re-evaluate on final-games footing — they already price thin evidence. The nerf adds
   **no second multiplier** on the evidence path. The *only* new present-season factor is the
   **lost-production term**: the player's 2026-relevant production contribution is scaled by
   (1 − L_p) where the engine consumes 2026 output as current-value evidence. Attribution reports
   `avail_nerf` = (board value with availability state) − (board value without), per player (G-ATTR).
3. **`_b2hc` is superseded, not stacked** (its own docstring says so): for register names the layer
   replaces `_b2hc` (register beats inference); for non-register players `_b2hc` dies entirely —
   RECOMMENDED, because a curated register plus an inference stopgap firing on the same signal is a
   double-count waiting to happen. If any true LTI is missing from the register, the fix is a register
   row, not a resurrected inference. *(Requested owner ruling R-B2HC: retire `_b2hc` at this chapter,
   register-only availability.)*
4. **Section B — nil production, no haircut, structurally**: Section B names get the season state
   (final games, no gross-up, lost-production term) and **nothing else** — no return-season arm, no
   L1c/KPFFIX window interaction. Their 2027+ expectation must equal a same-evidence never-injured
   counterfactual (asserted in §6.3).
5. **V0/G-FLOOR**: the nerf acts on production evidence and season state only — it never lowers the V0
   scaffold or the ramp's retention floor. A zero-games first-year register name (Thredgold,
   Hetherton, Barker, Chamberlain, Wardius…) prices exactly as today's sit-out machinery prices him
   (V0 · R_SURF · λ), THEN the return-season arm (if Section A) applies per §4. Never-crater holds.

### §3.3 Register fields that drive it

`designation` + `section` (which arm applies) · store `scoring[2026].games` (the truncation point —
the register never carries game counts; the store stays the single source of production) · `status`
(fork iii) · `window_id` (repeat handling, fork ii).

---

## §4 · PART 2 — RETURN-FROM-INJURY PRICING (derived fresh; the derivation spec)

### §4.1 Case definition (walk-forward, leak-free)

From the store's scoring histories, all seasons ≤ the evaluation cut:
- **Full-gap case**: ≥5 games in season Y, zero games in Y+1, ≥1 game in Y+2. (The 184-case sample.)
- **Long-gap variant**: zero games in Y+1 and Y+2, return Y+3 (prices multi-year absence — thin;
  pooled with full-gap via a gap-length covariate, declared).
- **Late-truncation case** (maps to designation "2026"): ≥10 games in Y, ≤4 in Y+1 (season cut short),
  return Y+2 — supplementary cell for players whose injury season kept a stub of games.
Historical windows carry no injury labels — a gap season may be suspension/omission/delisting-return.
Accepted and declared: the measured haircut prices *absence*, which is the treatment the register
applies. Walk-forward discipline: any table consumed at eval year T is built from data ≤ T (the L1c
`ycred_table` pattern, asserted by CODE READING per the G-COHORT basis doctrine).

### §4.2 The measured quantity — net of new aging (the study-v2 binding rule, operationalised)

For each case, the haircut is measured against the **aged counterfactual**, not the pre-injury self:

`h = 1 − actual(Y+2) / E_aged(Y+2)` where `E_aged(Y+2)` = the re-derived aging/level curve's
expectation for a player of that age, position class, and pre-injury demonstrated level, had he
simply aged from Y to Y+2 without the absence.

The raw age-banded medians (≤22: 1.03 · 23–26: 1.00 · 27–29: 0.87 · 30+: 0.64) demonstrate why: naive
`actual/prior` would ship an aging curve wearing an injury costume, and the M2/M3 clock levers plus
the fade lever already own aging — charging it again violates the study-v2 rule and double-counts
against A-FADE attribution. **Expected finding, stated up front: the net-of-aging residual haircut is
likely small, possibly ≈0 for young players** (consistent with study-v2's forfeited-growth-year
hypothesis: the young player's cost is the lost development clock — priced by Part 1 and fork (i) —
not a ceiling dent). A near-zero derived haircut is a legitimate result, not a failed derivation
(the A-DARCY acceptance note's "absence is a finding" doctrine applies to magnitudes too).
**Coupling declared**: E_aged must come from the re-derived aging curve (the queued PVC/aging
re-derivation, WAVE-3) — this derivation is sequenced AFTER or WITH it, never against the old curve
(that is exactly how study-v2's numbers died).

### §4.3 Cells and smoothing (finest-resolution rule, honestly applied to n=184)

- **Continuous axes**: age at return (kernel: adaptive-bandwidth Nadaraya-Watson, local eff-n ≥ 35 —
  the engine's standing convention) × pre-injury demonstrated level (the KPFFIX `LD` construction
  reused, so "demonstrated level" means one thing engine-wide).
- **Pooled and declared**: position pooled to at most the sit-out machinery's three classes
  (RUC / KPP / nonKPP) — position-resolved cells at n=17–36 per position cannot honestly support the
  finest-resolution rule; gap length enters as a covariate, not a cell split.
- **Output**: a smooth surface `h(age, LD_class…)` reported with local eff-n alongside every quoted
  value; RAW gradient plots in the build report — **no wide-bin single numbers** anywhere in the
  shipped table.
- **Application**: the haircut multiplies the **return-season expected production component only**
  (2027 for the out-until-2027 names; the return season generally), decaying to zero by the following
  season — one season's uncertainty, not a permanent scar. It applies AFTER KPFFIX (so the KPF's
  demonstrated-output split is computed on un-haircut history — fork (v) governs the window) and is
  exported as its own attribution column `lti_return_hc` (G-ATTR).

### §4.4 What this arm does NOT price (declared limits)

- **Never-return risk**: 513 historical same-shape cases never returned — but that pool is dominated
  by delistings, not medical fate, and the register names are all listed players Luke asserts will
  return. No mortality term is priced; fork (iii)'s probabilistic option is the only place a return
  probability could enter, and only for the six "may return 2026" names.
- **Severity**: the register carries timing, not diagnosis. One haircut surface for all Section A
  windows; Luke's Section A/B split IS the severity knob, by design (human ground truth over inference).

---

## §5 · DESIGN FORKS — SYMMETRIC OWNER OPTIONS, PRICED

### Fork (i) — does an injured youngster's L1c fade-clock pause while out?
The clock counts **career games** (never career-year, per the code's own comment), so absence already
pauses it implicitly.
- **(a) Status quo — games-clock, implicit pause. RECOMMENDED.** Sam Darcy (46-game clock; ~23 career
  games… his credit φ stays high through 2027): keeps his young-credit runway intact when he returns —
  exactly the forfeited-growth-year hypothesis; his lost year costs him Part 1's nerf, not his
  ceiling. Same for Jai Culley, Jacob Newton, the 2025-draft Section A names. Zero implementation; one
  diagnostic (report credit-age in calendar years for register names).
- **(b) Advance the clock by expected games during LTI windows**: Darcy's credit fades ~a full season
  despite zero new evidence — his 2027 board value drops with no data against him; violates the
  evidence-quantity rationale the owner accepted for L1c, and clips A-DARCY's ceiling through the
  availability locus (the thing A-DARCY forbids).
- **(c) Explicit pause + calendar cap (credit expires k years after draft regardless)**: protects
  against a perpetual-youth edge case (a player injured for 3 straight years stays "young" at 25),
  costs a new constant with no derivation basis today.
- *Consequence table*: (a) Darcy/Culley/Newton hold ceiling; (b) all three fade blind; (c) = (a) for
  every current register name (none is near a sane cap), differs only hypothetically.
- **Recommendation: (a)**, with (c)'s cap noted as a dormant guard to derive only if a real case
  appears.

### Fork (ii) — repeat-LTI treatment (Reef McInnes, Lewis Hayes — two windows each)
- **(a) Independent windows. RECOMMENDED.** Each return is priced by the same derived surface; no
  memory. McInnes (3 games in 2025 between windows) and Hayes (1 game in 2025) both re-enter 2027 as
  ordinary returners at their demonstrated level — which for both is already so thin that the sit-out
  machinery, not the haircut, dominates their price.
- **(b) Compounding (second window within k years draws a durability-deepened haircut)**: the
  historical repeat-case sample is a handful — a compounding multiplier would be an underived prior,
  which is the exact thing this engine's doctrine forbids shipping. Priced consequence: McInnes/Hayes
  drop further on an asserted (not measured) number.
- **Recommendation: (a)** + a report-only `repeat_lti` flag on their rows so the owner can rule on
  sight if the board price looks wrong (OWNER-ON-SIGHT is the existing pattern for exactly this).

### Fork (iii) — the six "may return 2026" names (Payne, O'Farrell, Nicholas Martin, Conway, Jones, Clarke)
- **(a) Owner-flagged binary, default OUT-for-2026. RECOMMENDED.** The register's whole thesis is
  human ground truth beats inference: Luke flips `status` to `returned` (with `returned_year`) the day
  it happens; until then the engine treats the name as out-for-remainder (nerf per §3) with return
  season 2026-if-flagged else 2027. Nicholas Martin (16g @ 97.8 in 2025, the exemplar): priced today
  as full-2026 lost + return-2027 haircut; the moment Luke flips him, 2026-return pricing applies. One
  register edit, no probability machinery.
- **(b) Probabilistic return (expected value over return/no-return)**: needs a return probability —
  the honest base rate from the store is confounded by delisting attrition (§4.4), so p would be
  asserted, not derived; and it prices every one of the six at a value NO world realises (neither the
  returned world nor the out world), which the board's trade-currency use case punishes.
- **(c) Binary, default IN (optimistic)**: prices Payne/Martin near-full and craters the day they're
  ruled out — the wrong direction to be wrong in, and inconsistent with Luke's "MAY return".
- **Recommendation: (a)** — conservative default, one-field owner workflow, no underived numbers.

### Fork (iv) — interaction ordering vs SITOUT_RETAIN/games-ramp · calendar fix · cliff blend (register cross-thread flag 2, discharged)
- **(a) Nerf enters as season state at the proration seam (per §3). RECOMMENDED.** Ordering (matches
  the engine's existing pipeline):
  `raw pricing → L1c (games-clock, fork i) → V0 → M2 (landed) [/M3 when wired] → sit-out/games-ramp
  reading availability-aware fE_p/L_p → KPFFIX (window per fork v) → return-season haircut
  (lti_return_hc) → PVC (pick side, untouched)`.
  Compatibility declared: **games-ramp** — register zero-games names flow through the existing V0 ·
  R_SURF · λ path untouched (no second penalty; the nerf only stops the gross-up and prices lost
  production); **calendar fix** — M2/M3 keep owning clock proration; the falsified games-completion
  ruling is honoured (nobody's season is "completed"; Rozee stays 2 games permanently); **cliff
  blend** — L_p is continuous in g₂₀₂₆ and the λ endpoints are unchanged, so the continuity law holds
  across the played↔sat seam and the proposed cliff-only-blend (still PROPOSED state) composes
  independently.
- **(b) Standalone post-hoc availability multiplier** (one factor at the end of the chain): simpler to
  implement and attribute, but it stacks on top of τ'/λ which already discount the same thin season —
  a structural double-count needing an offsetting fudge. Priced consequence: every "2026"-designation
  name (Fiorini 2g, Lord 1g, Gibcus 1g…) gets hit twice or needs a hand-tuned unwind.
- **Recommendation: (a).**

### Fork (v) — KPFFIX ↔ injury: the demonstrated-output window
`LD` = top-2 high-games seasons in Y−3..Y. One nuked season is already survivable by construction; two
absences inside the window collapse LD toward the loose slice and the KPF loses demonstrated-backed
retention for reasons that aren't form.
- **(a) Exclude register-flagged nuked seasons from top-2 selection, extending the window back
  year-for-year, capped at +2. RECOMMENDED.** Jamie Elliott (GFWD but KPF-adjacent machinery
  illustrates: window 2024–2027 in the 2027 build would otherwise hold 2026=11g-injured +
  2027=absent): keeps his 2025 (25g @ 76.8) demonstrated season alive on return. Sam Darcy: his 2026
  (6g) is excluded, LD stands on 2025 (17g @ 95.7) + 2024 — his KPF-speculative locus can't be clipped
  by the availability locus (A-DARCY's rule enforced by construction). Cap +2 so LD never rests on
  ancient form; when the extended window still holds <2 healthy seasons, fall back to (b) and REPORT
  it.
- **(b) Status quo — injured seasons count against the window**: no code, but an injured KPF is
  silently re-classed as speculative — a second, hidden injury penalty routed through KPFFIX;
  contradicts G-ATTR separability (the availability cost would surface in the KPF column).
- **(c) Freeze LD at its pre-injury value through the window**: cleanest for the player but lets a
  40-year-old's LD survive indefinitely via repeat windows; needs the same cap as (a) anyway.
- **Recommendation: (a)** — with the fallback-and-report rule.

---

## §6 · ACCEPTANCE SKETCH FOR THE CHAPTER-3 BUILD

### §6.1 A3 / Rozee (standing data-caused red; this chapter's resolution)
Facts: threshold already amended 0.80→0.75 [DC]; measured ~0.71–0.73; his 2026 is 2 games
**permanently**; the register stamp binds — **A3 is evaluated PRE-LTI-layer**, so nothing this chapter
builds may be the thing that passes it. The ratio is structural: it cannot go green by any authorised
means while the 2026 row is final. Resolution options for the owner (R-A3):
- **(α) UPHOLD the red as permanent-DC. RECOMMENDED.** A3 stays in the suite exactly as frozen,
  annotated `[DC-PERMANENT: register connor-rozee out-remainder-2026]`; every gate report carries the
  annotation so a knife-edge red reads as the recorded world, not a regression. What the board says
  all year: Rozee prices at his 2025-established level, minus Part 1's lost-2026 production, with
  **no return haircut** (Section B) and an unimpaired 2027 expectation — i.e. a top-8-pick-grade
  asset having a nil year, not a faded one. A-FADE unaffected (his decline lever never fires;
  attribution shows availability, not fade).
- **(β) Amend A3 to a per-game basis** (2026 avg 80.0 / 2025 avg 105.0 = 0.762 ≥ 0.75 — would go
  green): keeps a live gate but changes what A3 measures at the exact moment its red is inconvenient —
  the frozen-suite discipline exists to forbid this pattern; requires an explicit owner amendment
  under the DATA-CAUSED triage if wanted.
- **(γ) Retire A3, replace with the §6.3 shape test**: loses the one named-player tripwire on thin
  seasons; not recommended while the machinery it guards is being built.

### §6.2 A-DARCY availability attribution (becomes real at this chapter)
His board row's attribution must state, per locus: `young_convexity_ceiling` — untouched (fork i-a
holds his clock) · `kpf_speculative` — untouched (young/speculative exemption + fork v-a keeps LD on
healthy seasons) · `availability_layer` — now REAL: `avail_nerf` = lost-2026 production (6 final
games, L≈0.75) and `lti_return_hc` = the derived 2027 return haircut at his age/level cell — **stated
even if the derived value is ≈0** (per §4.2 the young cell plausibly nets to ~zero; absence/zero is a
reported finding, not a failure — acceptance JSON A-DARCY note honoured). Direction stays UP overall
or the build explains which locus moved him down. `_b2hc` no longer appears (superseded per §3.2.3).

### §6.3 Nerf shape test (the "no-expected-dip" analogue)
On a synthetic established player swept over injury round r = 0(pre-season)…G_FULL:
- board value **monotone non-decreasing in r** (later injury costs less season) — no inversion, no bin
  cliff anywhere on the sweep (G-MONO discipline applied to the new axis);
- continuous at r=0 (pre-season designation vs round-1 injury differ infinitesimally, not by a step);
- continuous at the healthy boundary (r=G_FULL ⇒ nerf ≡ 0 ⇒ byte-parity with the no-register world);
- **Section B counterfactual**: a Section B player's post-2026 expectation equals a same-evidence
  never-injured counterfactual exactly (no-haircut assertion, automated);
- **B4 parity**: every non-register player is value-identical with the layer on vs off (the layer
  touches register keys only — this is the chapter's cheapest, strongest guard).

### §6.4 Guard interactions (directions stated, per the FENCE)
- **G-COHORT**: eight register names are 2025-draft year-1s (Newton, Thredgold, Hetherton, May,
  Mackinlay, Liddy, Chamberlain, Barker). The nerf lowers their 2026-evidence contribution → the
  year-1/year-2 **class sums fall → the denominator falls → the ratio RISES → toward breach**. The
  build must re-measure G-COHORT walk-forward with the layer on (code-reading basis, as always). If it
  tips, the remediation doctrine binds: identify the mechanism (likely: lost-season production is a
  *availability* fact, not a *value-of-the-class* fact — candidate rectification is measuring the
  cohort sums on availability-adjusted expected production rather than nerfed realised production) —
  never a blanket young lift, never cutting survivors.
- **G-FLOOR**: §3.2.5 — the layer never touches V0/scaffold; zero-games rookies price via the
  existing ramp. Assert unchanged V0 curve in the build.
- **G-PEAK / A-PEAK**: Butters/Holmes are not register names → B4 parity covers them; the layer
  cannot move them by construction. Untouched, asserted.
- **G-ATTR**: three separable columns ship or the build fails acceptance: `avail_nerf`,
  `lti_return_hc`, `avail_clock_note` (fork i/v dispositions per player).
- **G-DATA/Guard 5**: register md5 joins the boot pin set (§2.4); halt-not-warn.
- **G-CONVEX (advisory)**: scored as CA-5 diagnostics; fork (i-a) is the convexity-preserving choice
  for young register names.

---

## §7 · IN PLAIN TERMS (for Luke)

Your injury list becomes a real, versioned input the engine reads every build — your word is final,
the engine never second-guesses a row, and every name is pinned to its exact store identity (we
caught that the two Max Kings share a birthday — only the store key tells them apart, which is why
the key column now ships in the file).

The build does two things. **First**, anyone you've listed as done for 2026 has their season closed
out at the games they actually played — a bloke hurt in round 2 loses nearly the whole year's worth,
one hurt in round 20 loses a sliver, on a smooth slide with no steps. Nobody gets credited for games
they'll never play. Your Section B names get exactly this and nothing more — no comeback penalty.
**Second**, for the long-term injured, the comeback season gets a measured discount — measured from
every "played, missed a whole year, came back" case in the data (184 of them), and measured *after*
stripping out normal aging, because the old study's mistake was charging blokes twice for getting
older. Fair warning: for young players that measured discount may come out near zero — the data says
a young player's real cost is the lost year itself, not a dent in what he becomes, and if that's the
answer we'll say so rather than invent a number.

Rozee: his gate stays red and we recommend you simply record it as the known fact it is — he's priced
as a star having a nil year, full value expected back in 2027. Darcy: nothing in this layer touches
his ceiling — his lost year costs him the year, not the future, and the build must show you that in
black and white. Five decisions are yours to make (§8) — each comes with our recommendation and what
every option does to named players.

---

## §8 · OWNER RULINGS REQUESTED (consolidated)

| # | ruling | recommendation |
|---|---|---|
| R-REG | register placement: R2 pinned sidecar vs R1 fold-into-store (§2.4) | R2 |
| R-B2HC | retire `_b2hc` inference at this chapter; register-only availability (§3.2.3) | retire |
| R-i | L1c clock during LTI: implicit pause (games-clock) vs advance vs pause+cap (§5.i) | (a) status quo |
| R-ii | repeat-LTI: independent windows vs compounding (§5.ii) | (a) independent + on-sight flag |
| R-iii | "may return 2026": owner-flagged binary (default out) vs probabilistic vs default-in (§5.iii) | (a) binary, default out |
| R-iv | nerf insertion: season-state at proration seam vs standalone multiplier (§5.iv) | (a) season-state |
| R-v | KPFFIX LD window: exclude-and-extend (cap +2) vs count-against vs freeze (§5.v) | (a) exclude-and-extend |
| R-A3 | A3 resolution: uphold permanent-DC vs per-game amendment vs retire (§6.1) | (α) uphold |

Constraint discipline: nothing above amends any frozen gate or constraint text — A3 options are
presented FOR an owner ruling under the DATA-CAUSED triage; G-COHORT/G-FLOOR/G-PEAK/G-ATTR are
referenced by ID and bind the implementing build as written in CONSTRAINTS v1.6.
