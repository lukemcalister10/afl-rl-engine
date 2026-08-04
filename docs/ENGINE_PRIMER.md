# ENGINE PRIMER — the meaning layer · v1 · authored 2026-08-04 by the outgoing seam (hi1an4), owner-directed

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
  the board. Runs from a seeded workspace behind guards; CI runs and reports, never commits.
- **The pick curve** (`pvc_curve_v2.json` / `ui/release_pick_curve.json`) — what each national draft pick
  slot is worth, **picks 1–64 only; pick 65 does not exist** (RULEBOOK law 4). Identity = the N32
  string-keyed payload md5, never the file md5. **Two curves exist as of 2026-08-04** — see §5's census
  and CURRENT_STATE for which is shipped vs ruled.
- **The year-zero surface** (`data/v0surf.pkl`) — the value of a NEWLY DRAFTED player: the price at entry.
  The owner's definition is binding: *"the true worth of a player the moment they are drafted"* — career
  included, not year-one output. Under redesign (#306) to `ruled_curve(pick) × m(pos, age, pick)`, the lens
  `m` fit from measured careers (the sibling order). Its historical form was a model prior — see §4.
- **The frozen fitted set** (`peak_model_v4.pkl`, `q97m.pkl`, `cm_400.pkl`, the surface, the curve) —
  models fitted ONCE on a controlled machine and shipped as pinned artifacts, LOADED at build, never refit.
  Why: fits are machine-sensitive (§4, item 380) — the same code and data produce different bytes on
  different CPUs. A silent refit is a defect class, not a convenience.
- **Currencies:** values are denominated in a replacement-relative unit; γ is the discount knob. The ruled
  curve is **VOR-denominated (γ=1.0)**; a γ=0.85 pricing variant exists in the record. Never compare
  numbers across denominations without saying so.
- **The walk-forward book** — season-by-season as-of values for every player-history, the evidence substrate
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
   #279 structural curve replaced the method; the #306 sibling order extended the same surgery to the
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
   a deterministic fit lane is being built (#306 L-B). Byte-identity is a tripwire, deliberately more
   sensitive than value-materiality (~1% worst observed per-chip effect).
5. **The bust exclusion.** Paddy McCartin and Tom Boyd (pick-1 KPF busts, force majeure) are excluded by
   owner ruling; every player in their drafts slides up one pick. If a KPF number looks bust-driven, check
   the exclusion applied before theorizing.

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
  it; pool pricing is its own fenced decision (#207 / N37).
- **Positions** are KPD, KPF, MID, RUCK, SD, SF. `MATN`/`MATR` were mature-age tier keys in a voided
  design — not store positions.
- **A flag's name is not its semantics; a file's md5 is not a payload identity.** Trace what a flag
  actually feeds, and identify curves by the N32 string-keyed payload md5 (key TYPE is load-bearing:
  string-keyed and int-keyed dumps of the same ladder hash differently).
- **Which curve am I looking at?** As of writing: shipped-on-main = the superseded #271 ladder; the
  rehearsal anchor = the #279 ruled ladder (classes 2004–2022, pick 64 = 221). Current identities live in
  CURRENT_STATE's census table — check there, then verify by payload md5, never by filename.

## 6 · WHERE THE DEEP ANSWERS LIVE

- **The ruled curve's full basis and rulings:** `session_2026-07-30/item279/EVIDENCE.md` (+ `panel/
  harness_pvc.py` — `structural_values()` is the reusable machinery), branch
  `claude/pre-referee-baseline-shaping-4ql38z`. RETENTION-PROTECTED.
- **The held-constant method** (the superseded curve): issue #271 body + `session_2026-07-29/item271/
  derive_271.py`; #225's three comments for the function-for-function carriage.
- **The year-zero redesign in flight:** issue #306 — body + the governing comment set (CURRENT_STATE names
  the ids). The owner's laws and steers are quoted verbatim there.
- **The laws of record:** `RULEBOOK.md` (product laws) · `docs/directives/SEAT_CHARTER_seam.md` (this
  seat's law) · `docs/CURRENT_STATE.md` (live state + rulings digest) · the register (by pointer only).

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
