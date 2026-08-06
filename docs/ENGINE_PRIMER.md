# ENGINE PRIMER — the meaning layer · v5 · authored 2026-08-04 (hi1an4); v5 at register v591 (2026-08-06): the #336 resolution (the band prices establishment risk in full; the adopted reference-layer form), the implemented tenure rule, and the two-lever hump framing added at the rotation

**WHAT THIS IS.** Every incoming seat reads this IN FULL, immediately after the charter and before
CURRENT_STATE. It carries what the process documents don't: what the engine is FOR, what each artifact
MEANS, the discoveries that changed how numbers must be read, and the name-traps that have burned seats.
It exists because a seam once verified every byte flawlessly while not knowing what the bytes meant, and
the owner spent an evening teaching it his own project back ("register v562–v563", 2026-08-04).

**WHAT IT IS NOT.** Not the record and not the law — a MAP. Where it disagrees with the register or a
primary document, the primary record wins and this file gets corrected. It is maintained by the supervisor
pen and changes only when MEANING changes: a new basis, a renamed quantity, a discovery that reinterprets
an artifact. Routine state lives in CURRENT_STATE; hashes and branch tips do not belong here.

---

## 1 · WHAT THE PROJECT IS

A player-valuation engine for the owner's AFL keeper league (AFFL). **It is a hobby project** — the
governing test in CURRENT_STATE Part A overrides every instinct to gold-plate. The product surfaces:

- **The board** — a priced list of players (~804 active), derived from the store by the engine. It is a
  MARKET price list: clubs trade against it.
- **The trade desk** — trades players and draft picks against board prices.
- **The clubs tab / public view** — display surfaces over the same numbers.
- **Draft picks are assets** with prices (the pick curve), tradeable like players.

**The one idea under all of it: a price is expected worth NOW.** It must already contain everything
predictable — a young player's price includes his probable future (probability-weighted, busts included),
so prices change on NEWS (risk resolving), never on schedule. If a class of player predictably appreciates,
its year-zero price is wrong (the owner's no-arbitrage test: "you'd just buy them in year 0 and hold").
**And prices are grounded in REALITY — measured careers — never in the model's beliefs about reality.**
That sentence is the moral of this project's hardest-won discovery (§4).

## 2 · THE CORE ARTIFACTS AND WHAT THEY MEAN

- **The store** — the single source of player data (careers, seasons, positions, eligibility, ownership).
  Everything derives from it; its md5 is pinned and asserted at build.
- **The engine** (`engine/rl_after/`, entry `_merged_recover.py` via `rl_export.py`) — turns the store into
  the board. Runs from a prepared workspace behind guards; CI runs and reports, never commits.
- **The pick curve** (`engine/rl_after/pvc_curve_v2.json` is the LADDER; `ui/release_pick_curve.json` is
  the release MANIFEST that stamps it, not a ladder — hashing it matches nothing) — what each national draft pick
  slot is worth, **picks 1–64 only; selections past 64 are NOT ON THE CURVE** (RULEBOOK law 4 v2.1 — they enter the pool, valued by position; matrices use 65 as the pool INDEX, §5). Identity = the N32
  string-keyed payload md5, never the file md5. **As of 2026-08-05 the ruled curve IS shipped-on-main**
  (the re-closure, owner word) — CURRENT_STATE carries the current payload identity.
- **The year-zero surface** (`data/v0surf.pkl`) — the value of a NEWLY DRAFTED player: the price at entry.
  The owner's definition is binding: *"the true worth of a player the moment they are drafted"* — career
  included, not year-one output. Rebuilt and LANDED (#306, 2026-08-05) as `ruled_curve(pick) × m(pos,
  age, pick)`, the lens `m` fit from measured careers. Its historical form was a model prior — see §4.
- **The frozen fitted set** (`peak_model_v4.pkl`, `q97m.pkl`, `cm_400.pkl`, the surface, the curve) —
  models fitted ONCE on a controlled machine and shipped as pinned artifacts, LOADED at build, never refit.
  Why: fits are machine-sensitive (§4, item 380) — the same code and data produce different bytes on
  different CPUs. A silent refit is a defect class, not a convenience.
- **Currencies (owner-corrected 2026-08-06):** γ is the SCAR-vs-VOR SHAPE knob on an internal valuation
  function — 0.85 = concave SCAR compression, 1.0 = linear VOR — **NOT a future-season discount, and NOT
  the shipped board's denomination in either era** (both eras' exporters price from the engine's own
  `ev()`). The shipped board is ONE currency for players AND picks: pick 1 = 3,000; the best player is
  ~4.04× pick 1 (4.041× on the round-21 board) (an earlier seam double-converted to 4.24×/2,851 and retracted it — #333). Never compare
  numbers across bases without saying so.
- **The walk-forward book** — season-by-season as-of values for every player-history, the evidence base
  behind career-value measures. "Concluded" vs "active" careers matter enormously — see §4.

## 3 · HOW VALUE FLOWS (one paragraph)

Store → engine builds the board: veterans priced from their measured careers (peak model, age curves);
draft picks priced by the pick curve; newly drafted and pool players priced by the year-zero surface;
guards assert every pinned identity on the way through (Guard 5, boot_guard, parity gate: board values ==
engine `ev()` at eps 0). The board ships as frozen bundles the UI reads. Nothing on the value path is
fitted at build time — everything is loaded from pins.

## 4 · THE DISCOVERIES THAT CHANGE HOW YOU READ NUMBERS (the "oh shit" ledger)

1. **The 1/4000th discovery (#279, 2026-07).** The then-adopted pick curve was advertised as
   evidence-weighted; measurement showed realized careers carried **0.0248% of its mass — one part in
   ~4,000** — the rest was the model's own prior, laundered in a loop: "Curve → surface → v0 → curve."
   Owner's words: *"what the model expected of someone like him is ridiculous to consider when we have the
   evidence of what he actually did."* Consequence: **model beliefs are BARRED as pricing inputs.** The
   #279 structural curve replaced the method; the #306 sibling order extended the same correction to the
   position/age lens. When you see any fitted number, your first question is: **what taught it — careers,
   or the model's opinion of careers?**
2. **Completion, not presumption.** 38% of the surface's teaching rows are STILL-ACTIVE careers. An
   unfinished career read as a finished answer drags every average toward wherever young players currently
   are. The ruled remedy (the structural method): concluded careers teach in full; active careers teach
   what they've played plus an **actuarial completion from concluded look-alikes** (busts' zero-remainders
   included); the model prior only as a counted fallback. Known wart: the completion back-tests **+4.7–8.4%
   optimistic** — reported beside results, never silently corrected.
3. **The anchor principle (N29) and the owner's product laws.** Year-zero values anchor to measured pick
   outcomes; position/age redistribute around the anchor and never inflate it. The laws (CURRENT_STATE
   Part A): intersections are the point — position effects VARY along the pick axis, crossing the curve
   freely; and **no hard bands anywhere, in models or in anything shown to the owner** — per-pick, smooth,
   locality-weighted, confidence-weighted, with no-data regions shown as no-data.
4. **Machines disagree about floating-point fits (item 380 → N35).** Identical code, data, and library
   bytes produced different fitted surfaces on different hosts — with identical CPU labels. Consequence:
   boxes are classified only by REPRODUCING OUTPUT BYTES (the fit-path assert), fits are frozen (§2), and
   the deterministic fit path was built and landed (#306): its surfaces reproduced on every fit-class
   box, and the VALUE path reproduced a board byte-identically on a different CPU architecture.
   Byte-identity is a tripwire, deliberately more sensitive than value-materiality (~1% worst per-chip).
5. **The bust exclusion.** Paddy McCartin and Tom Boyd (pick-1 KPF busts, force majeure) are excluded by
   owner ruling; every player in their drafts slides up one pick. If a KPF number looks bust-driven, check
   the exclusion applied before theorizing.
6. **The survivorship defect, the Ablett inversion, and the RESOLUTION (#336, ruled ADOPTED
   2026-08-06).** Parts of the engine sampled SURVIVORS ONLY: the load-time reference tables
   (`pkbest is not None`) and the par surface (60% of tenure cells never taught). Consequence: a
   mediocre career LOWERED the average while a zero-game bust VANISHED from it (Nathan Ablett's
   cell: survivor mean 61.0, bust-inclusive truth 32.1). **The owner's MONOTONICITY LAW binds all
   work: a strictly worse career must never produce a better-looking baseline.** The curve's own
   teaching basis was always clean (busts at 0). THE ADOPTED FORM (four measured cuts, two owner
   catches; the earlier "P(establishes)×level at expectation-shaped consumers" phrasing is
   SUPERSEDED): reference anchors read the bust-inclusive level of ESTABLISHERS (de-survivored,
   never survivor-at-tenure), with **NO probability discount at any anchor** — measured, the
   forward band's low quantiles already charge establishment failure IN FULL (d_band 0.7077 vs
   true class risk 0.7075); resolution is SMOOTH via the engine's own evidence fade (no six-game
   cliff); the v3.4 clamp is retired. It ships as part of #334 stage B; until then the form lives
   on branch `variant/336-bust-inclusive`. Two lessons that reinterpret numbers: an anchor-side
   probability discount is a DOUBLE CHARGE wherever the band prices the same risk; and "established"
   (any ≥6-game season) is resolved news — pricing a resolved player at his class prior violates
   the price-is-worth-NOW principle.
7. **The minimum-tenure rule and the era asymmetry (#338 — IMPLEMENTED 2026-08-06).** Historical
   players with no recorded seasons were valued as delisted-on-draft-day (a pick-21 worth 16 points
   at year 1) while current sitting-out players held the floor. The rule: assume ND picks 1–20
   listed ≥4 seasons, 21–40 ≥3, others ≥2; own data extends; known facts override; an evidence-less
   year inside tenure is a LISTED sitting-out year. Implemented in the book emitter (board
   untouched, proven byte-identical); the book of record and the no-arb lineage are re-emitted on
   it; era parity is EXACT — 460 pairs to four decimals in the BOOK lineage (register v584 P5, e.g. Simpson = Keeler = 243.0000); the no-arb sheets show the same pairs at per_entrant-lineage values (216), a different population — never conflate the two. Tenure-provisionality is lifted.
8. **The pool denominator rule (2026-08-06).** The walk-forward book's `v0` field for POOL rows still
   carries the SUPERSEDED old-surface belief (cleanup queued); pool tables denominate by the SIGNED
   ENTRY ANCHORS (#326 levels, ladder currency ×1.0524 into engine units). On that honest denominator
   the pool HUMPS like the draft (peak ≈141% at years 4–5 — the owner's cohort artifact page and its recompute carry the table; the ND ≈157% side is register v585) — the old "pool cliff" was superseded
   machinery measured against superseded prices.
9. **The hump is real, and it has exactly two levers (the #336 steering answer + the owner's
   framing, 2026-08-06).** Under FULLY honest pricing — busts counted, resolved players clean, no
   cliff, risk charged once — the cohort appreciation hump barely moves: 1.572 → 1.535 at year 4.
   The reference layer was never the lever. The owner's two-sided framing is the record: close the
   gap by making ESTABLISHED PLAYERS WORTH LESS (the untested doors: the proven-player near-year
   credits — up to +17%, ×2 for KPF — the demonstrated floors, the discount structure; the
   survivorship door is measured weak) or by making PICKS AND YEAR-0/1 WORTH MORE (re-teaching the
   curve on the corrected history). Both go OPEN to the #333 memo; stage B executes its choice.
   Never present either lever as pre-decided.
5.5. *(numbered 5.5 of record, deliberately out of sequence — it amends §1; cite by source numbering; renderers may renumber.)* **The measured-outcomes correction (2026-08-05, register v570).** The career-value measure that
   teaches the ruled curve and the lens is NOT raw scoring over replacement: the walk-forward path is
   built by calling the ENGINE'S OWN `ev()` as-of each season, and `ev()` leans on the year-zero
   estimate wherever a record is thin — every career's early seasons. Measured: a surface+engine change
   moved 475 of 825 fully-concluded careers' values; the 71 counted-fallback rows carry only 55.78% of
   total movement. §1's "never in the model's beliefs" OVERSTATES the implementation — read it as
   "taught by realized careers, valued through the engine." No raw-scores-over-bar measure has ever
   existed; the owner's standing requirement for one, and the recipe-audit order, are N45.

## 5 · THE NAME-TRAP GLOSSARY (each of these has burned someone)

- **"curve" in engine code usually means the year-zero SURFACE.** `_build_v0_curve`, `teaches_curve`,
  `incurve` are all about the surface fit. The pick curve is `_PVC0` / `pvc_curve_v2.json`, a pinned
  artifact the engine only reads.
- **`teaches_curve` / `incurve` flags** (matrices): the SURFACE fit population — drafts 2003–2025, ~38%
  active careers. The pick curve's teaching set is narrower and applied AT FIT TIME (the ruled curve:
  1,197 rows, draft classes 2004–2022, hard cut).
- **`in_hist`**: the engine's separate historical cohort (2003–2021) feeding in-engine fits. It fed
  neither pick curve.
- **`epk`** = slid effective pick (curve attribution). It is NOT "expected peak."
- **`v0` in a matrix row** = the surface's slot value — identical for every same-(pos, age, pick) player.
  It is a MODEL BELIEF, not that player's outcome. Ratios of `v0` to the curve measure the surface's
  shape, not reality's.
- **Pick 65** = the pool-index convention in matrices (`pick: 65` rows are pool entrants). No curve prices
  it; pool ENTRY pricing is the #326 signed per-division levels (N43), landed and adopted 2026-08-06.
- **Pathway/division tags** (owner-corrected TWICE — read them as the store means them, never expand
  from the acronym): `PD*` = **POST-DRAFT**, not pre-season — `PDA` post-draft academy · `PDN`
  post-draft next-gen · `PDS` post-draft scholarship. `UNR` = post-draft **UNREGISTERED** — a real
  recruiting pathway, NOT "untagged/unresolved" missing data. `IRE` = post-draft Ireland. `SSP` =
  supplemental selection period · `MSD` = mid-season draft · `RD` = rookie draft. Bid-matched academy
  and father-son taken WITH a pick are coded `ND` at that pick — `PD*` rows are the PICKLESS intake.
- **Positions** are KPD, KPF, MID, RUCK, SD, SF. `MATN`/`MATR` were mature-age tier keys in a voided
  design — not store positions.
- **A flag's name is not its semantics; a file's md5 is not a payload identity.** Trace what a flag
  actually feeds, and identify curves by the N32 string-keyed payload md5 (key TYPE is load-bearing:
  string-keyed and int-keyed dumps of the same ladder hash differently).
- **Which curve am I looking at?** As of 2026-08-05: shipped-on-main = the RULED curve, re-closed on the
  corrected store (the #271 and first-adopted ladders are history). Current identities live in
  CURRENT_STATE's merged-main block — check there, then verify by payload md5, never by filename.
- **Older names in the record.** Anything written before 2026-08-05 uses the earlier words for the same
  things: `substrate` = working state · `evidence substrate` = evidence base · `lane` = path · `capture` =
  snapshot · `sealed twin` = paired field · `digest` = summary · `seeded workspace` = prepared workspace.

## 6 · WHERE THE DEEP ANSWERS LIVE

- **The ruled curve's full basis and rulings:** `session_2026-07-30/item279/EVIDENCE.md` (+ `panel/
  harness_pvc.py` — `structural_values()` is the reusable machinery), branch
  `claude/pre-referee-baseline-shaping-4ql38z`. RETENTION-PROTECTED.
- **The held-constant method** (the superseded curve): issue #271 body + `session_2026-07-29/item271/
  derive_271.py`; #225's three comments for the function-for-function carriage.
- **The year-zero redesign:** LANDED 2026-08-05, ADOPTED 2026-08-06 — issue #306 body + its governing
  comments hold the owner's laws verbatim. "N-numbers" (N29, N32, N35, N43, N45 …) are the register's
  numbered standing rulings — look one up by grepping the register for its number; never read the
  register front to back.
- **The laws of record:** `RULEBOOK.md` (product laws) · `docs/directives/SEAT_CHARTER_seam.md` (this
  seat's law) · `docs/CURRENT_STATE.md` (live state + rulings summary) · the register (by pointer only).

## 7 · HOW TO USE THIS DOCUMENT

Read it before CURRENT_STATE. When you present ANY number, name its quantity in plain words — belief or
outcome, which basis, which curve, which denomination, which population and window (denominators always).
When a term surprises you, check §5 before reasoning. When the owner's memory disagrees with a derived
view, verify against the primary record before contradicting him — his memory has beaten derived views
repeatedly. And when he asks a casual question, treat it as load-bearing QC: four of his questions became
standing law in one evening.

**Self-test — if you cannot answer these from this document, re-read it:** What does the board price and
in what sense is it a market? What are the two curves and which one ships today? Why does pick 65 not
exist? What taught the old curve, and what fraction was reality? What is completion-not-presumption and
its known bias? Why are fitted artifacts frozen? What does `teaches_curve` actually flag? Why is a `v0`
ratio not an outcome measurement? What are the owner's two product laws?
