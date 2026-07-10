# SPEC — POSITIONAL FLEXIBILITY PRICING — v1 · 2026-07-09 · FABLE seat (design only)

_Job: DIRECTIVE_flex_spec_fable_v1 (manifest tier 6). Written against manifest v4.3 · CONSTRAINTS v1.6 +
acceptance_v1_6.json (asserted, loaded) · DECISIONS v86. Base: session checkout `d4e8f6dc` = tag v2.6
(the engineering head; the repo `main` ref sits behind at `00d82dde`, a docs-upload line — the directive's
own pin "tag v2.6 = d4e8f6dc" names this head). Store md5 `e1b4d8bf` (boot-guard asserted). READ-ONLY
fence honored: nothing under `engine/`, `data/`, or any gate file is touched; every code fact below is
asserted by reading the v2.6 source, with file:line citations. This document DESIGNS; Opus implements
AFTER the dead-code strip lands (assumptions on that strip: §0.2)._

---

## 0. GROUND — what the spec stands on

### 0.1 The position representation at v2.6 (code-read facts)
- The store (`rl_model_data.json`, 2652 records) carries **three single-valued position columns**
  (`engine/rl_after/rl_model.py:5-20`): `drafted_position` → `p['pos']` (drives cohort curves),
  `present_position` → `_pos_now` (year-0 REPL bar via `bnow`, rl_model.py:40), `future_position` →
  `_futpos` (years-1+ REPL + peak/curve/runway via `gfut`, rl_model.py:41-44). In this build
  **future == present for every record**; there is NO eligibility field of any kind.
- **The weighted-leg machinery is alive but single-legged**: `futblend(p)` returns `[(gfut(p), 1.0)]`
  (rl_model.py:45) and `proj_from_peak` already consumes a `fut` list of (position, weight) pairs,
  netting REPL **per leg** inside the years-1+ term:
  `prod += sum(w*posval(base-REPL[gg]) for gg,w in fut)` (rl_model.py:317). A weighted future split is
  therefore a change to **what `futblend` returns**, not new pricing machinery.
- **REPL is per-position** (rl_model.py:261): MID 80.1 · GEN_DEF 78.3 · RUC 78.5 · KEY_DEF 68.4 ·
  GEN_FWD 70.9 · KEY_FWD 66.8. Largest bar gap between plausibly-flexible positions: **RUC↔KEY_FWD =
  11.7 SC pts** — the single biggest arbitrage flex pricing can open.
- **V0 start values are keyed by future position**: `_v0key(p)` includes `MA.gfut(p)`
  (`_merged_recover.py:672`) — a `future_position` re-designation on a zero-evidence young player moves
  his **entire V0 band start price**, not merely a REPL blend. This is the heaviest single consequence
  of Law 2 and is called out everywhere it matters below.
- **The L1c young credit keys its cell by `gfut(p)`** (`_merged_recover.py`, `_ycred_mult`:
  `_YC_TAB[...].get(MA.gfut(p))`) — an in-transition player already keys his FUTURE position's cell;
  the KEY_FWD cell carries the T3 ×0.92 trim.
- **No intra-season rounds axis exists on the board path.** Season progress appears only as the R14/24
  gate proration convention and the `_b2hc` present-unavailability haircut (a year-0-only, Now-board-only
  multiplier, rl_model.py:314,328). Rounds-remaining scaling (Law 1) therefore needs a **declared input**
  (§2.3).
- **The DPP-strip obituary stands** (BOARD_LAYERS_OBITUARY.md; evidence/dpp_strip/REPORT.md): the old
  `raw_multipos` probabilistic blend is deleted, each dual collapsed to its dominant leg (Marshall
  −$984, Petracca −$619, Bailey J. Williams −$687, Draper −$594 were the real-money swingmen; the
  median dual lost $1). Nothing here resurrects that machinery — this is a fresh design on the
  three-column representation, and the strip's own words anticipated it: "the seam is live."

### 0.2 Assumptions about the queued dead-code strip (+F17/F24)
The strip is queued BEFORE the flex build. This spec assumes:
1. The strip does **not** remove the three-column position model, `bnow`/`gfut`/`futblend`, or the
   `fut` weighted-sum loop in `proj_from_peak`/`_proj_w4`. **WARNING to the strip job:** with
   future==present on all 2652 records, `futblend` and the per-leg loop LOOK dead (a constant
   single-element list) — they are the live seam this entire spec builds on. If the strip folds them
   away, the flex build's first act is reinstating the seam; better that the strip declares them kept.
2. The strip does not alter the REPL table, `posval`, the L1c `gfut` keying, or `_v0key`.
3. Line numbers cited here may shift; the BUILD re-asserts every §0.1 fact against the post-strip head
   before pricing anything (cheap: grep-level assertions, same discipline as the boot guards).

---

## 1. THE OWNER'S LAW, MADE PRECISE (the spec's spine)

The owner's law has three parts. Each is restated below in machinery terms; where the owner's wording
admits more than one reading, the readings are presented as **symmetric options** (§4), never silently
picked.

### 1.1 LAW 1 — CURRENT DPP: value = MAX of eligible positions' values, scaled by rounds remaining

**Eligibility source.** A player carries an eligible-position set E(p) for the CURRENT season:
E(p) = {present_position} ∪ {alt eligibility, if any} (source and schema: §2.1/§2.2; Fork D governs
whose fact it is). Single-position players have |E(p)| = 1 and Law 1 is exactly inert for them.

**The MAX construction — precise, and one line long.** The engine's year-0 production term is
`posval(lev₀ + capt − REPL[bnow(p)]) · 21` (rl_model.py:315-316). The player's demonstrated level
`lev₀` is position-portable by the owner's law (his value at each eligible position = same level netted
against that position's replacement bar). Because `posval` is strictly increasing, the MAX over
eligible positions collapses to a **bar substitution**:

    MAX over g∈E(p) of posval(lev₀ + capt − REPL[g])  ==  posval(lev₀ + capt − min_{g∈E(p)} REPL[g])

i.e. **a flex player is priced against the LOWEST replacement bar among his eligible positions.** That
is the whole of Law 1's max construction. It lives INSIDE the single existing `posval` netting — it is
a substitution of the bar, never an additive layer, so replacement can never be double-counted (§3.1).

**Rounds-remaining scale.** Flex is worth more with more season left to exploit it. Define
ρ = rounds remaining fraction = clip((R_total − r_now) / R_total, 0, 1), from a single-sourced season
input (§2.3). The scale enters as a **bar interpolation** (keeping everything inside one `posval` call,
continuous in ρ, exactly zero at season end):

    bar_eff(p) = REPL[bnow(p)] − ρ · f · (REPL[bnow(p)] − min_{g∈E(p)} REPL[g])
    year-0 term: posval(lev₀ + capt − bar_eff(p)) · 21

with f = 1 under MAX-at-all-times, or f ∈ (0,1) under switching-friction (Fork B). The **flex premium**
(display + attribution object) is Δflex(p) = value with bar_eff − value with REPL[bnow] ≥ 0.

**Scope declaration (primary reading, challengeable).** Law 1 is a **year-0, Now-board object** — the
k==0 term only, guarded like `_b2hc` (`k==0 and BASE_REF==2026 and AGE_REF==2026`, rl_model.py:314).
Rationale: "rounds remaining" is inherently a current-season quantity, and the owner's Law 2 covers the
future through the 80/20 split — letting current eligibility also ride years 1+ would double-cover the
future position channel. The alternative reading (eligibility persists into the years-1+ MAX) is listed
as a ruling item (§6, R-6) but not recommended.

**What Law 1 does NOT touch:** peak age, curve, runway, key premium, L1c cell — all keyed by
`gfut` and untouched by current-season eligibility. The captaincy premium is level-based
(`capt_prem(lev)`) and rides along unchanged. Synths carry no eligibility and delegate byte-exact.

### 1.2 LAW 2 — FUTURE POSITIONS: a weighted split meeting 80/20 toward the future position

The store's `future_position` column is the owner's settled-future designation (today: == present for
everyone; the seam exists precisely so designations can differ). Where a designation differs from
present, the years-1+ leg becomes a **weighted two-leg split** toward the future position. The owner's
"meeting 80/20" admits distinct readings — presented as options for ruling (Fork A, with the full
pricing in §4.1):

- **What the 80/20 weights (three candidate depths):**
  - **R-A (REPL-legs only, minimal):** `futblend(p)` returns `[(future, 0.8), (present, 0.2)]` — the
    weights apply to the years-1+ replacement netting only (the existing per-leg loop, zero new
    machinery); peak age / curve / runway / L1c cell stay keyed on the dominant future leg (`gfut`).
  - **R-B (full projection blend):** years-1+ value = 0.8 · V(as-if future) + 0.2 · V(as-if present),
    where each V re-keys peak age, key premium, and runway. Two full passes; heavier; moves talls far
    more than R-A (their REPL gap is small but their peak/premium geometry differs).
  - Under EITHER reading, `_v0key`'s `gfut` term means a zero-evidence player's V0 re-keys to the
    future position outright (§3.2) — the 80/20 governs projection legs, not the V0 cell key, unless
    the owner rules the V0 key should blend too (not recommended: fractional cell keys break the D14
    same-boat identity assertions).
- **What "meeting" means (the weight path):**
  - **P-1 (constant):** 80/20 from designation until the year-roll collapses it (Law 3).
  - **P-2 (converging):** 80/20 at year 1, converging to 100/0 by year 2 or 3 — "meeting 80/20" read
    as the near-year landing point of a path, so a fully-transitioned player sheds the legacy leg.
  - **P-3 (season-ramped):** the split ramps toward 80/20 as the current season progresses (mirrors ρ),
    landing at 80/20 by season end. Listed for symmetry; couples Law 2 to the rounds axis.
- **Horizon:** whether the 20% present leg persists across the whole projection (P-1) or only its
  first year(s) (P-2). The year-roll (Law 3) bounds the question — under P-1 the split lives at most
  one season before the roll re-anchors it.

### 1.3 LAW 3 — YEAR-ROLL PROVISION

At the season roll (the board's year seam, when 2026 → 2027):
1. **present ← future**: the 2027 designation becomes the current position (`present_position`
   overwritten by `future_position` where they differ) — the owner's "2027 designations become current."
2. **future repopulates**: default **carry** (future ← new present, i.e. settled) unless the owner
   re-designates; alternative default (**re-curate**: future set null pending owner pass) is R-8. Under
   carry, a multi-season transition path (e.g. MID → wing → HBF over two years) is expressed by the
   owner re-designating at each roll — the machinery never invents a path.
3. **In-flight weights collapse**: the 80/20 split re-anchors on the new columns. A completed
   transition (future had differed; now rolled into present; new future == present) prices
   single-legged again. An owner re-designation at the roll re-opens a fresh 80/20 split.
4. **Eligibility expires**: `alt_position_current` (§2.1) is a season-scoped fact — nulled at roll,
   re-attested from the season's source (official list republishes / owner re-curates). ρ resets to 1.
5. **Forward boards must agree with the roll**: the ±1/±2 view already rolls the year-0 bar to `gfut`
   when AGE_REF > BASE_REF (the A2 note, rl_model.py:407). Flex joins that convention: on a +1 board
   the split has rolled exactly as (1)-(3) describe, and Law 1's ρ is 1.0 (a full season ahead) —
   BUT Law 1 on forward boards only binds if eligibility is assumed to persist, which it is not
   (item 4) — so Law 1 is zero on forward boards. Stated to keep vP1/vP2 well-defined.

---

## 2. REPRESENTATION & DATA (under the SINGLE_SOURCE_INVARIANT)

### 2.1 Schema: what suffices, what's new
- **Laws 2 and 3 need NO schema change.** The three columns carry them today; the strip report said
  exactly this ("a later transition model can populate future_position … with no schema change").
- **Law 1 needs eligibility** — one new field in the ONE store. Two shapes (owner ruling R-5):
  - **S-1 (recommended): `alt_position_current`** — nullable, SINGLE-VALUED, the player's one
    alternate eligible position this season. Preserves the single-valued-column discipline the strip
    established; matches the AFL DPP reality (dual status); E(p) = {present, alt}. A hypothetical
    triple-eligible player is representable by choosing the lowest-bar alt (which is all Law 1's MAX
    ever reads) — a documented, lossless-for-pricing reduction.
  - **S-2: `eligible_positions` list** — full generality, but re-introduces a list-shaped position
    field of the deleted `raw_multipos` SHAPE. If chosen, the lookalike tripwire (SSI guard 3) gains
    an assertion that no weights/probabilities ever attach to it (eligibility is a set, never a blend).
- **Values validate against the GRP group set** (MID/RUC/GEN_FWD/KEY_FWD/GEN_DEF/KEY_DEF, incl. raw
  aliases GFWD/KFWD/GDEF/KDEF/DEF, rl_model.py:36); unknown value ⇒ HALT (guard-family behavior).

### 2.2 How the data enters (SSI discipline)
- The register document (whichever source Fork D picks) is **provenance**; the store is the ONLY
  price-time source. The fold happens at the store-edit step through the one writable source, exactly
  as the 34 present-position calls and the LTI register precedent — **no side tables, no price-time
  file reads**. The self-test's correction-canary already proves store edits reach board + book;
  eligibility rides the same rail.
- **Migration:** all 2652 records get `alt_position_current: null` (and future stays == present). The
  null board is **byte-exact v2.6** by construction — the migration itself is a no-op re-price, which
  is the build's first gate (§5).
- **Guard impacts:** store md5 pin moves (Guard 5 / expected_boot re-pin at build, the standard bake
  step); B3 book seal and B4 non-mover parity re-stamp; SSI guards 1-4 unchanged in kind. The
  **standing `harvey-thomas` flag** (present disagreed with sole future leg at the strip; held at
  present, FLAGGED) should be resolved as a 35th owner call in the same store edit (§6, R-9).

### 2.3 The rounds input (new, single-sourced)
`season_round_now` (int) + `season_rounds_total` (int, 24) live in **`params.json`** — the engine's
existing versioned config (rl_model.py:4), aligning with the DECISIONS §24 one-versioned-config-file
direction — never hardcoded at use sites, never a second data file. ρ derives at load. Finals
treatment (do rounds 25+ count, and at what leverage) is Fork C's third fork.

---

## 3. INTERACTIONS — each with direction

### 3.1 Per-position replacement — no double-count, by construction
Law 1 substitutes the bar INSIDE the single year-0 `posval` netting; Law 2 weights legs each netted
against its own bar inside the one years-1+ loop (rl_model.py:316-317). Replacement is applied exactly
once per leg per path — the D3/3a lesson (netting once, never stacked) is honored structurally: there
is no additive "flex layer" anywhere, only bar/weight substitutions inside existing nettings.
**Direction: Δflex ≥ 0 always (a MAX over a set containing the status quo); the 80/20 split can move
either way (toward the future leg's bar/curve).**

### 3.2 V0 start values (D14 curve) — the heavyweight interaction
`_v0key` includes `gfut(p)` (`_merged_recover.py:672`): a `future_position` designation on a
zero/low-evidence player **re-keys his whole V0 cell** (position × draft-age × pick), a much larger
move than any 80/20 REPL blend — and it changes which position's V0 curve his start value is FIT
against, rippling that curve's other members (the strip's §PHASE-1 ripple, ~0.13% median, same
mechanism). **Direction: player moves to the destination position's start curve (sign depends on the
pair); curve co-members move at ripple magnitude.** The build must measure and attribute this
separately from the projection-leg split (two sub-effects of one lever; G-ATTR, §5). It also touches
the D14a/b same-boat assertions — identity now holds per (pos, draft-age, pick) with pos = the
DESIGNATED future position; two same-pick players with different designations lawfully differ. The
assertions need no code change, only this reading recorded.

### 3.3 G-MONO (pick curve) — untouched by construction, asserted anyway
The pick-value curve is built from synths through `pick_raw` → `proj_from_peak` with no eligibility
and no store keys (rl_model.py:438-442); synths delegate byte-exact (the same construction argument
as G-CONVEX's synth note). **Direction: zero motion on the PVC from Law 1/2 directly**; young flex
RE-pricing enters the board, not the curve. The smoothness harness still runs at build (young
designations could correlate with pick pockets on the BOARD's per-pick aggregates) — assert, don't
assume.

### 3.4 G-COHORT — denominator effect stated, and a book-convention flag
- Flex/future credit on **year-1/2 class members raises the year-1/2 class sums → raises the
  denominator → LOWERS the ratio (the safe direction)**; the same players carrying flex value into
  years 4-6 raises numerators → raises it. Net = incidence-dependent; measured at build; the fix
  direction doctrine (raise year-1, never cut young) is unchanged and un-threatened by an
  additive-only Law 1.
- **Book convention (must be declared at build):** G-COHORT is measured on the walk-forward book, and
  Law 1 is Now-board-only (BASE_REF==2026 guard) ⇒ **zero book effect** — the guard cannot move via
  Law 1. Law 2 designations are CURRENT-store facts: if the as-of matrix consumed them for historical
  years, a 2027 designation would color a player's pre-2026 as-of prices — a leak-shaped
  anachronism. **The build confines the split to evaluation years ≥ the designation's entry year**
  (designations carry an entry-year stamp in the store edit's provenance; the book applies the split
  only from that year). Cheap, and keeps the walk-forward book honest by construction.

### 3.5 L1c young credit — cell keying
The credit cell is keyed by `gfut(p)` — a designated MID→KEY_FWD transition youngster keys the
KEY_FWD cell **and picks up the T3 ×0.92 trim** (direction: slightly less credit than his MID
cellmates). Under R-A this stays as-is (declared, consistent: the dominant future leg keys everything
forward-looking). Under R-B only, an 80/20 blend of cell intensities becomes coherent (R-10, minor).
Never both.

### 3.6 Lenses — flagged, not solved (owner directive)
- **LENS discounts** (now .34 / bal .15 / fut .05, rl_model.py:277): Law 1 is a year-0 object ⇒
  near lens-invariant; Law 2 legs are discounted ⇒ the future-position designation matters more
  under the `fut` lens. Directions only; no lens work here.
- **±1/±2 boards:** §1.3(5) defines flex's roll behavior; Law 1 zero on forward boards (eligibility
  is season-scoped), Law 2 rides the rolled columns.
- **Contender/Balanced/Developing (queued chapter):** a Contender values current-season flex (ρ-scaled
  list coverage NOW) more than Developing; Developing values the future designation. **FLAG for the
  lens chapter: Δflex and the future-leg share are exported as separable components (§3.7) precisely
  so that chapter can tilt them per team context without re-opening this spec.**

### 3.7 Board display & attribution
One price stays law (the obituary's 3d). The export (rl_export.py:74 pattern, alongside `b2hc`/`cvx`)
gains DISPLAY knobs: `flexPrem` (Law 1 dollar delta at current ρ), `posNow` / `posFut` / `wFut`
(present, future, future-leg weight), `altPos` (eligibility). The board shows the one price; hover
attribution decomposes: base + flexPrem, and future-split share of the years-1+ leg. G-ATTR's LOO
harness gets the two sub-levers (§5).

---

## 4. DESIGN FORKS — symmetric owner options, priced, named players (keys verified in store `e1b4d8bf`)

### 4.1 FORK A — the 80/20 reading (Law 2)
| option | machinery | who moves, how |
|---|---|---|
| **R-A** REPL-legs-only, weight path P-1 (constant until roll) | `futblend` → `[(fut,.8),(now,.2)]`; ~3 tokens of change; peak/runway stay on `gfut` | `sam-darcy` (KFWD pk2/2021): a hypothetical KEY_DEF future designation moves his years-1+ bar by only 0.8·(66.8−68.4) = **−1.3 pts** (slightly HIGHER bar ⇒ small value dip) — tall-swing REPL gaps are small; his real money would move via V0/peak keying, which R-A leaves on the future leg |
| **R-B** full projection blend, P-1 | two projection passes, 0.8·V(fut) + 0.2·V(now); re-keys peak age/key premium per leg | same designation now also blends KEY_FWD vs KEY_DEF peak geometry and key premium — bigger, harder to attribute, ~2× projection cost |
| **P-2** converging path (with either) | weights [(fut, .8→1), (now, .2→0)] over 2-3 projection years | `jy-simpkin` (drafted GFWD, settled MID — the store's cleanest completed transition): P-2 is the path his transition WOULD have priced — 80/20 in the designation year, single-leg MID by +2 |
| **P-3** season-ramped to 80/20 | couples Law 2 to ρ | listed for symmetry; couples two axes the owner worded separately — flag as least-literal reading |

**Recommendation offered (challengeable): R-A + P-1** — minimal machinery, everything attributable,
the roll bounds the split's lifetime; escalate to R-B only if the owner wants tall-swing peak
geometry priced now.

### 4.2 FORK B — MAX-at-all-times vs switching friction (Law 1)
| option | machinery | priced consequence |
|---|---|---|
| **MAX-at-all-times** (f = 1) | bar substitution, full | `rowan-marshall` (RUC pk9/2016, the strip's max loser −$984): RUC+KEY_FWD eligibility prices his year-0 at bar 66.8 instead of 78.5 — **the full 11.7-pt gap × ρ**, re-opening most of the strip's deletion for every RUC/KFWD dual (`sam-draper`, `luke-jackson`, `tristan-xerri`, `bailey-williams-wc` class) whether or not they ever swing |
| **switching friction** (f ∈ (0,1), owner dial) | bar_eff interpolates a fraction of the gap | f = 0.5 halves Marshall's premium; keeps the option priced as an OPTION (exercise has cost: role disruption, form risk) rather than as already-exercised |
| **evidence-gated f** | f = share of current-season games actually played in the alt position (needs a per-season alt-games input — a data ask, flagged) | only demonstrated swingmen collect; purest but adds a data pipeline; can land later as a refinement of the dial |

The strip's own distribution is the decision data: **median dual's second leg was worth $1; the ~20
genuine swingmen carried $594-$984.** MAX-at-all-times re-inflates the whole class; friction
concentrates value on genuine swingmen. Symmetric; owner rules.

### 4.3 FORK C — rounds-remaining shape ρ (Law 1)
| option | form | at R12 of 24 (mid-season), Marshall-class full gap |
|---|---|---|
| **linear** | ρ = rem/24 | premium × 0.50 |
| **convex** | ρ = (rem/24)^γ, γ≈2 | premium × 0.25 — full-season flex worth disproportionately more (list-build leverage, finals runway) |
| **step** | in/out at a round cut | rejected-by-default: G-MONO-style cliff on the time axis; listed for symmetry |
Plus the finals sub-fork: `season_rounds_total` = 24 (H&A only) vs 24+finals-weighted. Linear is the
literal reading of "scaled by rounds remaining"; convex is the market reading. Owner rules.

### 4.4 FORK D — eligibility source (Law 1)
| option | character | precedent / risk |
|---|---|---|
| **official AFL DPP status** | objective, external, republishes each season | risk: fantasy-derived DPP lists are game-ised (positions granted for game balance, not football reality) — exactly the inference-vs-truth gap the owner rejected for injuries |
| **owner-curated register** (recommended) | LTI_REGISTER precedent verbatim: "human-maintained ground truth beats inference"; owner updates as reality changes | cost: maintenance; mitigated by season-scoped expiry (§1.3.4) — at most one curation pass per season plus in-season calls |
Either way the register document is provenance and the STORE is the price-time source (§2.2).

---

## 5. ACCEPTANCE SKETCH for the flex BUILD (not this spec)

- **Levers & G-ATTR:** family switch `RL_FLEX`, with sub-levers `RL_FLEX_NOW` (Law 1) and
  `RL_FLEX_FUT` (Law 2 split + V0 re-key) so each law's delta is separable per G-ATTR (BINDING on
  multi-lever builds). All-off ⇒ **byte-exact** current board (null eligibility + future==present makes
  the identity structural, same discipline as RL_YOUNG's exact-1.0 off-path). The V0-re-key and
  projection-split sub-effects of Law 2 are reported as separate attribution rows (§3.2).
- **Shape tests:** (i) Δflex ≥ 0 ∀p; (ii) Δflex monotone non-increasing in rounds elapsed at fixed
  level; (iii) Δflex ≡ 0 for null-eligibility players — and every null-eligibility, future==present
  player is **byte-identical** (B4-style non-mover parity INSIDE the candidate); (iv) PVC byte-check
  (synth delegation, §3.3) + the standard smoothness harness on the board aggregates; (v) continuity
  in ρ (no time-axis cliff unless the owner picks the step form); designation changes are discrete
  owner facts — declared events, like the 34, never smoothed.
- **Book:** Law 1 Now-board-only ⇒ book byte-unchanged by Law 1; Law 2 applies designation-entry-year
  gating in the as-of matrix (§3.4) — B3 re-seal, G-COHORT re-measured walk-forward with the class-sum
  construction and min(y1,y2) denominator asserted by code reading (per acceptance_v1_6).
- **Anchors that could move:** `max-gawn` / `kieren-briggs` (A-GAWN, BINDING) — both pure RUC today;
  if either is granted KFWD eligibility the "clearly above" ordering must hold and both prices are
  reported with flex attribution. `sam-darcy` (A-DARCY) — a KEY_DEF designation must not clip his
  ceiling; Law 1 is additive-only, R-A's −1.3-pt bar dip is the one negative channel — the build
  reports it in his (now four-locus) attribution. `willem-duursma` (A-DUUR) — year-1 member: any
  designation effect flows to the G-COHORT denominator, reported. A-PEAK/A-FADE untouched unless
  designated. Panel 10/10 on the candidate; frozen-suite full pass; guard behavior halt-not-warn
  throughout (G-DATA).

---

## 6. OWNER RULINGS REQUESTED (consolidated)

| # | question | options | spec's offered default (challengeable) |
|---|---|---|---|
| R-1 | 80/20 reading depth | R-A REPL-legs / R-B full blend | R-A |
| R-2 | weight path | P-1 constant / P-2 converging / P-3 season-ramped | P-1 |
| R-3 | MAX vs friction | f=1 / owner-dial f / evidence-gated f | owner-dial f (start 1.0, dialable) |
| R-4 | ρ shape + finals | linear / convex γ / step; R_total 24 vs finals-weighted | linear, R_total=24 |
| R-5 | eligibility schema | S-1 single `alt_position_current` / S-2 list | S-1 |
| R-6 | Law 1 scope | year-0 Now-board only / persists into years-1+ MAX | year-0 only |
| R-7 | eligibility source | official AFL DPP / owner-curated register | owner-curated (LTI precedent) |
| R-8 | roll default for `future_position` | carry (settled) / re-curate (null pending pass) | carry |
| R-9 | `harvey-thomas` standing flag | resolve as 35th call at the eligibility store edit | resolve |
| R-10 | L1c cell keying (ONLY if R-B) | keep `gfut` / blend intensities | keep `gfut` |

---

## 7. IN PLAIN TERMS (for Luke)

Right now every player on the board has exactly one position today and one settled future position —
and they're the same for everyone, so nobody is priced for versatility. Your law says two things
should change. First: a player who can genuinely cover two positions **this season** should be priced
at whichever of those positions makes him most valuable — and that bonus should shrink as the season
runs out, because flexibility you can't use anymore isn't worth anything. The nice discovery is that
the engine already prices everyone as "his level above what a free replacement gives you at his
position" — so "the max of his positions" just means netting him against the WEAKEST replacement bar
he's eligible for. One substitution, no new layers, impossible to double-count. Second: a player who's
**becoming** something else — your call, recorded per player — gets priced mostly as what he's
becoming (80%) with a foot (20%) still in what he is, and at the new year the future position simply
becomes his current one and everything re-anchors.

What I need from you before anyone builds: ten decisions, listed just above. The three that matter
most: **(1)** does a dual-position player get the full best-position price all the time, or a haircut
because actually switching him has a cost — this single choice decides whether the ruck/forward
swingmen (Rowan Marshall's the poster case) win back most of what the position clean-up took off them;
**(2)** does 80/20 apply just to the replacement-bar side of his future years (small, clean — my
recommendation) or to his whole projection including peak shape (bigger, mostly matters for talls like
Sam Darcy); **(3)** who says a player is dual-eligible — the AFL's official list, or your own register
like you keep for injuries. My recommendation on (3) is your register: the AFL's dual-position tags
are made for fantasy game balance, not football truth, and you already told us human-maintained ground
truth beats inference. One warning I've flagged for the clean-up job that runs before this build: the
wiring this design plugs into looks unused today (because everyone's future position equals their
present one) — it must not be swept out as dead code.

_No engine, store, or gate file was touched in this job. Spec only._
