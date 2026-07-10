# SPEC — POSITIONAL FLEXIBILITY PRICING — v1.1 · 2026-07-09 · FABLE seat (design only)

**SUPERSEDES: `SPEC_positional_flex_v1.md` (pinned 49a1435d, PR #50).** v1 stands unedited as the
record of what was asked; THIS document is the single spec the flex build implements from. What
changed and why: **DECISIONS v89 §28** (the owner's Law-2 clarification) re-founds Law 2 — it prices
**probabilistic future eligibility, not positional transition** — and **DECISIONS v89 §34** rules all
ten of v1's open questions plus the probability source. v1's options sections collapse to decisions
here; v1's verified machinery findings carry forward unchanged where the rulings don't touch them.

_Job: DIRECTIVE_flex_law2_revision_fable_v1 (manifest tier 6). Written against manifest v4.3 ·
CONSTRAINTS v1.6 + acceptance_v1_6 · DECISIONS v89. Base: live `main` **b303795** (fetched fresh
2026-07-09; = merge of PR #52, 2effba2 an ancestor — matches §35's supervisor verification). Store
**a2fbc9a0** (boot-guard asserted; the post-correction canonical store, §35). Engine unchanged from
v2.6 across the store correction (md5 4b08796c); every §0 code fact below was RE-ASSERTED against
this live head this session. READ-ONLY fence honored: nothing under `engine/`, `data/`, or any gate
file is touched. This document DESIGNS; Opus implements AFTER the dead-code strip lands (§5.3)._

---

## 0. GROUND — what the spec stands on (re-verified at b303795)

### 0.1 The position representation (code-read facts, unchanged from v1 except the store identity)
- The store (`rl_model_data.json`, 2652 records, md5 a2fbc9a0) carries **three single-valued position
  columns**: `drafted_position` → `p['pos']` (cohort curves), `present_position` → `_pos_now` (year-0
  REPL bar via `bnow`, rl_model.py:40), `future_position` → `_futpos` (years-1+ REPL + peak/curve/
  runway via `gfut`, rl_model.py:41-44). Today **future == present for every record**; there is no
  eligibility field of any kind.
- **The weighted-leg machinery is alive but single-legged**: `futblend(p)` returns `[(gfut(p), 1.0)]`
  (rl_model.py:45) and `proj_from_peak` already nets REPL **per leg** inside the years-1+ term:
  `prod += sum(w*posval(base-REPL[gg]) for gg,w in fut)` (rl_model.py:317). The ruled Law 2 (§1.2) is
  a change to **what `futblend` returns** — the legs become the owner's probability streams — not new
  pricing machinery. (The dead-code-strip warning carries: this seam LOOKS dead with future==present
  everywhere; it must survive the strip. §5.3.)
- **REPL is per-position** (rl_model.py:261): MID 80.1 · GEN_DEF 78.3 · RUC 78.5 · KEY_DEF 68.4 ·
  GEN_FWD 70.9 · KEY_FWD 66.8. Largest bar gap between plausibly-flexible positions: RUC↔KEY_FWD =
  11.7 SC pts.
- **V0 start values are keyed by future position**: `_v0key(p)` includes `MA.gfut(p)`
  (`_merged_recover.py:672`) — a `future_position` edit on a zero-evidence young player moves his
  entire V0 band start price. Under the ruled Law 2 the key reads the **primary** future position
  (§1.2.4); probability weights never touch the key (no fractional cell keys — they would break the
  D14 same-boat identity assertions).
- **The L1c young credit keys its cell by `gfut(p)`** (`_merged_recover.py`, `_ycred_mult`) — RULED
  KEPT (R-10, §4): the primary future position keys the cell; the KEY_FWD cell carries the T3 ×0.92
  trim.
- **No intra-season rounds axis exists on the board path**; Law 1's ρ therefore needs the declared
  `params.json` input (§2.3, carried verbatim from v1).
- **The DPP-strip obituary stands.** Nothing here resurrects `raw_multipos`: the ruled design keeps
  single-valued primary columns plus at-most-one genuine alternate (R-5), with probabilities living
  ONLY on the future streams and coming ONLY from the owner (§2).
- **Store rows verified this session** (post-correction store a2fbc9a0): `jason-horne-francis` — the
  JHF of the owner's §28 example — is MID in all three columns today; `harvey-thomas` is GFWD in all
  three columns (the R-9 edit rides the flex build's eligibility migration, §2.4).

### 0.2 Assumptions about the queued dead-code strip
Carried verbatim from v1 §0.2, all three items — in particular: the strip must NOT fold away
`bnow`/`gfut`/`futblend` or the per-leg loop (the live seam this spec builds on), nor alter the REPL
table, `posval`, the L1c `gfut` keying, or `_v0key`. The BUILD re-asserts every §0.1 fact against the
post-strip head before pricing anything.

---

## 1. THE LAW AS RULED (the spec's spine — no open readings remain)

### 1.1 LAW 1 — CURRENT-SEASON DUAL ELIGIBILITY: pure MAX, scaled by rounds remaining

**RULED (R-3, owner-worded): "the one that 'adds' more counts."** A current-season dual-position
player is priced at whichever eligible position makes him more valuable — pure MAX, no haircut. The
friction-dial concept is **RETIRED** (superseded list, DECISIONS v89); no `f` parameter exists.

**Eligibility source — RULED (R-7): the owner-curated register** (LTI_REGISTER precedent:
human-maintained ground truth beats inference; official AFL DPP tags are game-ised). The register is
provenance; the store is the only price-time source (§2.2). E(p) = {present_position} ∪ {genuine
alternate, if any} (schema: §2.1). Single-position players: |E(p)| = 1, Law 1 exactly inert.

**The MAX construction (carried from v1 — verified machinery).** Because `posval` is strictly
increasing, MAX over eligible positions collapses to a **bar substitution** inside the one existing
year-0 netting:

    MAX over g∈E(p) of posval(lev₀ + capt − REPL[g])  ==  posval(lev₀ + capt − min_{g∈E(p)} REPL[g])

A flex player is priced against the LOWEST replacement bar among his eligible positions — a
substitution of the bar, never an additive layer, so replacement can never be double-counted (§3.1).

**Rounds-remaining scale — RULED (R-4): linear, 24 rounds, NO finals.**
ρ = clip((24 − r_now)/24, 0, 1) from the single-sourced `params.json` input (§2.3);
`season_rounds_total` = 24, home-and-away only. The scale enters as the bar interpolation:

    bar_eff(p) = REPL[bnow(p)] − ρ · (REPL[bnow(p)] − min_{g∈E(p)} REPL[g])
    year-0 term: posval(lev₀ + capt − bar_eff(p)) · 21

**The never-negative FLOOR — retained as a HARD REQUIREMENT + TEST (R-3).** Δflex(p) = value with
bar_eff − value with REPL[bnow] ≥ 0 for every player; a dual-eligible player is always ≥ his
single-position twin. Structural under the MAX (the eligible set contains the status quo), and
asserted anyway — build test, halt-not-warn (§5.1).

**Scope — RULED (R-6, owner-worded): "only this season."** Law 1 is a year-0, Now-board object — the
k==0 term only, guarded like `_b2hc` (k==0 and BASE_REF==2026 and AGE_REF==2026, rl_model.py:314).
Current-season eligibility NEVER rides years 1+; the future is covered entirely by Law 2's
owner-provided streams. Law 1 does not touch peak age, curve, runway, key premium, or the L1c cell;
captaincy rides along unchanged; synths carry no eligibility and delegate byte-exact.

### 1.2 LAW 2 — THE FUTURE POSITION: probabilistic future eligibility (the §28 re-foundation)

**RULED MEANING (DECISIONS §28/§34; owner-worded R-6): "future season value will be defined by the
future season positioning, which will be only one position, but that position could be a probability
blend."** Law 2 prices **PROBABILISTIC FUTURE ELIGIBILITY, not positional transition**. No player is
ever projected as dual-position in the future, and no player is "phasing toward a destination
position" — that framing (v1 §1.2/§1.3/§7) is dead. Each player has **ONE future position**, and that
one position may itself be a **probability blend of eligibility STREAMS**:

1. **A stream is a possible future eligibility state**: either a single position (pure-MID) or a
   dual-eligibility pairing (MID/G-FWD). The owner's example (§28, JHF = `jason-horne-francis`):
   **~75% pure-MID stream + ~25% MID/G-FWD stream**.
2. **Probabilities are OWNER-PROVIDED — RULED (owner-worded): "I will decide the splits; deriving is
   too hard."** No derived base rates, no engine inference, ever. His register carries the splits;
   they are **constant until he updates them** (R-2 is DISSOLVED — there is no "weight path"; the
   old P-1/P-2/P-3 fork is void because the weights are standing owner facts, not a schedule).
   v1's "80/20 meeting" language = probability weights across streams, nothing more.
3. **Within a dual stream, the MAX law applies** (§28: "the MAX law applying WITHIN the dual
   stream") — the same collapse as Law 1: the stream's replacement bar is the MINIMUM of the pair.
   bar(stream) = REPL[g] for a pure stream; min(REPL[g₁], REPL[g₂]) for a dual stream.
4. **RULED (R-1 = A): the projection is the SAME in both streams; only the replacement bar
   differs.** Level path, peak age, curve, runway, key premium, V0 key, L1c cell — all keyed once,
   by the **primary future position** (the blend's single position identity; JHF: MID), i.e. by
   `gfut(p)` exactly as today (R-10: gfut KEPT). The streams differ solely in the years-1+ REPL
   netting. _(Option B — per-stream projection re-keying — is noted in this one line as a possible
   future refinement; it is not offered.)_

**The machinery, exact.** `futblend(p)` returns the owner's streams as legs with per-stream bars:

    futblend(JHF) = [(MID, 0.75), (bar=min(REPL[MID], REPL[GEN_FWD]) → GEN_FWD, 0.25)]
    years-1+ term: 0.75·posval(base − 80.1) + 0.25·posval(base − 70.9)   — per rl_model.py:317, as-is

The existing per-leg loop consumes this unchanged; the 25% dual stream nets against a bar 9.2 pts
lower. **Floor, future channel:** the within-stream MAX makes every stream's bar ≤ the primary's bar,
so the blend value ≥ the pure-primary value — a player with a genuine alternate stream is never worth
less than his single-position twin. Same hard requirement + test as Law 1's floor (§5.1).

**A single-stream player (probability 1.0)** — including all 2652 records today, and `harvey-thomas`
after his R-9 edit — prices exactly as the current machinery does: one leg, weight 1.0.

### 1.3 LAW 3 — YEAR-ROLL PROVISION (re-cut in ruled terms: owner facts, not transitions)

At the season roll (2026 → 2027):
1. **present ← the owner's word**: the owner rolls the season; the new season's `present_position`
   (and current-season eligibility) is what his register says the player IS. Where his prior future
   designation was a blend, the roll is where he resolves it — the machinery never resolves a
   probability into a fact on its own.
2. **future carries — RULED (R-8): carry forward season to season until the owner overrides** at his
   season roll. No re-curate-to-null default; no invented paths. A standing blend (e.g. JHF's
   75/25) simply persists as the new season's future fact until he changes the numbers.
3. **No in-flight collapse**: there are no converging weights (R-2 dissolved), so nothing "completes."
   The only events are owner edits — discrete, declared, provenance-stamped (§3.4), like the 34
   present-position calls.
4. **Current eligibility expires**: season-scoped; nulled at roll, re-attested from the owner's
   register for the new season. ρ resets to 1.
5. **Forward boards**: the ±1/±2 view already rolls the year-0 bar to `gfut` when AGE_REF > BASE_REF
   (the A2 note, rl_model.py:407). Law 1 is ZERO on forward boards (eligibility is season-scoped,
   item 4); Law 2's streams ride the rolled columns unchanged. Stated to keep vP1/vP2 well-defined.

---

## 2. REPRESENTATION & DATA (under the SINGLE_SOURCE_INVARIANT)

### 2.1 Schema — RULED (R-5): hybrid
- **The owner's sheet keeps its easy comma-lists** (e.g. `MID, G-FWD` — his format, unchanged).
- **Ingest STRIPS auto-coverage**: K-FWD→G-FWD and K-DEF→G-DEF are implied coverages, removed before
  distillation (a listed K-FWD already covers G-FWD; the pair is not a genuine dual).
- **The engine stores the S-1 single-valued discipline: primary + AT-MOST-ONE genuine alternate.**
  Concretely (field names are build-level, the shape is ruled):
  - current season: `present_position` + nullable `alt_position_current` (Law 1's E(p));
  - future: `future_position` (the primary — keys gfut/V0/L1c/curve) + nullable
    `future_alt_position` (the dual stream's genuine alternate) + `future_alt_weight` (the owner's
    probability on the dual stream; JHF: GEN_FWD / 0.25). Absent alt ⇒ single stream, p = 1.0.
- **Non-collapsing rows are FLAGGED, never truncated**: a sheet row that still lists >1 genuine
  alternate after auto-coverage stripping HALTS to the owner for a call (guard-family behavior) —
  the engine never silently drops an eligibility.
- Values validate against the GRP group set (rl_model.py:36); unknown value ⇒ HALT.

### 2.2 How the data enters (SSI discipline — carried from v1)
The owner-curated register (R-7) is **provenance**; the store is the ONLY price-time source. The fold
happens at the store-edit step through the one writable source — no side tables, no price-time file
reads; the correction-canary already proves store edits reach board + book. Probability splits enter
the same way: owner numbers, in the register, folded to the store fields, constant until he updates.

### 2.3 The rounds input (carried verbatim from v1 — verified machinery)
`season_round_now` (int) + `season_rounds_total` (int, **= 24, RULED, no finals**) live in
`params.json` — the engine's existing versioned config (rl_model.py:4), never hardcoded at use
sites, never a second data file. ρ derives at load, linear (R-4).

### 2.4 Migration + the Harvey Thomas edit — RULED (R-9)
- **Migration**: all 2652 records get null current-alt and single-stream futures (weight 1.0). The
  migrated board is **byte-exact** the current corrected board (fd90472c) by construction — the
  build's FIRST GATE (§5.1).
- **RULED: `harvey-thomas`** — drafted G-FWD, G-FWD-eligible this season, settled **future position
  MID, probability 1.0** (single stream). The first real present≠future divergence — the gfut seam's
  first genuine use; his V0 cell re-keys GFWD→MID (§3.2). The edit rides the flex build's
  eligibility store migration (one store edit, owner-worded provenance) and closes the standing
  v2.5-strip flag.
- **Guard impacts**: store md5 pin moves (Guard 5 re-pin at build, standard bake step); B3 book
  re-seal; B4 non-mover parity re-stamp; SSI guards unchanged in kind.

---

## 3. INTERACTIONS — each with direction (updated to the ruled shape)

### 3.1 Per-position replacement — no double-count, by construction (carried)
Law 1 substitutes the bar INSIDE the single year-0 `posval` netting; Law 2 weights streams each
netted against its own stream-bar inside the one years-1+ loop (rl_model.py:316-317). Replacement is
applied exactly once per leg per path; there is no additive "flex layer" anywhere. **Direction:
Δflex ≥ 0 always (year-0); blend value ≥ pure-primary value always (years-1+; §1.2 floor). Under the
ruled meaning BOTH channels are non-negative** — v1's "the 80/20 split can move either way" is dead
with R-1=A + within-stream MAX: a stream's bar never exceeds the primary's bar.

### 3.2 V0 start values (D14 curve) — the heavyweight interaction, now single-keyed
`_v0key` includes `gfut(p)` = the **primary** future position. A primary designation on a
zero/low-evidence player re-keys his whole V0 cell (position × draft-age × pick) and re-fits that
curve (ripple ~0.13% median, the strip's mechanism). Probability weights NEVER touch the key (no
fractional cells; D14 same-boat identity holds per (pos, draft-age, pick) with pos = primary).
**First real case: harvey-thomas GFWD→MID (R-9).** The build measures and attributes the V0-re-key
effect separately from the stream-split effect (two sub-effects of one lever; G-ATTR, §5.1).

### 3.3 G-MONO (pick curve) — untouched by construction, asserted anyway (carried verbatim)
Synths carry no eligibility and single streams; `pick_raw` → `proj_from_peak` byte-delegates. Zero
motion on the PVC from Law 1/2 directly; the smoothness harness still runs at build on the board's
per-pick aggregates — assert, don't assume.

### 3.4 G-COHORT + the walk-forward gating rule (carried, re-worded to ruled terms)
- Denominator effect as v1: year-1/2 flex credit raises the class sums → lowers the ratio (safe
  direction); years-4-6 credit raises it; net incidence-dependent, measured at build. The fix-
  direction doctrine is unchanged and un-threatened (both channels additive-only, §3.1).
- **Book convention (BINDING at build)**: Law 1 is Now-board-only ⇒ zero book effect, structurally.
  Law 2 designations and probability splits are CURRENT owner facts: the as-of matrix must not let a
  2026 designation color pre-designation as-of prices (a leak-shaped anachronism). **Every owner
  eligibility/designation edit carries an entry-year stamp in the store edit's provenance; the book
  applies the stream blend only from that year forward.** Cheap; keeps the walk-forward book honest
  by construction.

### 3.5 L1c young credit — RULED (R-10): keep `gfut`
The credit cell keys by the primary future position, unchanged in code and in kind. A young player
whose primary is KEY_FWD keys the KEY_FWD cell and its T3 ×0.92 trim. v1's "blend of cell
intensities" sub-option existed only under R-1=B and dies with it.

### 3.6 Lenses — flagged, not solved (carried)
LENS discounts (now .34 / bal .15 / fut .05, rl_model.py:277): Law 1 near lens-invariant (year-0);
Law 2 streams are discounted ⇒ matter more under `fut`. ±1/±2: §1.3(5). Contender/Balanced/Developing
(queued chapter): Δflex and the stream-blend share export as separable components (§3.7) precisely so
that chapter can tilt them per team context without re-opening this spec.

### 3.7 Board display & attribution (carried, fields renamed to ruled shape)
One price stays law. The export gains DISPLAY knobs alongside `b2hc`/`cvx`: `flexPrem` (Law 1 dollar
delta at current ρ), `posNow`/`altPos` (present + current alternate), `posFut`/`futAlt`/`futAltW`
(primary, alternate stream position, owner probability). Hover attribution decomposes: base +
flexPrem; and the stream-blend share of the years-1+ leg. G-ATTR's LOO harness gets the two
sub-levers (§5.1).

---

## 4. THE TEN RULINGS — RECORD (DECISIONS v89 §34; nothing here is open)

| # | question (v1) | RULED | carried into |
|---|---|---|---|
| — | probability source | **OWNER-PROVIDED** ("I will decide the splits; deriving is too hard"); register carries them; constant until he updates | §1.2.2, §2.2 |
| R-1 | 80/20 reading depth | **A** — same projection both streams, only the replacement bar differs (Option B: one-line future refinement, not offered) | §1.2.4 |
| R-2 | weight path | **DISSOLVED** — weights are owner numbers, constant until updated; no path exists | §1.2.2, §1.3.3 |
| R-3 | MAX vs friction | **pure MAX** ("the one that 'adds' more counts"); friction-dial RETIRED; never-negative FLOOR retained as hard requirement + test (dual ≥ single-position twin) | §1.1, §5.1 |
| R-4 | ρ shape + finals | **linear, 24 rounds, NO finals** | §1.1, §2.3 |
| R-5 | eligibility schema | **hybrid** — sheet keeps comma-lists; ingest strips K-FWD→G-FWD / K-DEF→G-DEF auto-coverage; engine stores primary + at-most-one genuine alternate; non-collapsing rows FLAGGED | §2.1 |
| R-6 | Law 1 scope | **year-0 only** ("only this season; future season value will be defined by the future season positioning, which will be only one position, but that position could be a probability blend") | §1.1, §1.2 |
| R-7 | eligibility source | **owner-curated register** | §1.1, §2.2 |
| R-8 | roll default | **carry forward** until the owner overrides at his season roll | §1.3.2 |
| R-9 | harvey-thomas | **RULED: future MID, probability 1.0** — first real present≠future divergence; rides the eligibility migration | §2.4, §3.2 |
| R-10 | L1c cell keying | **keep gfut** (under R-1=A this was conditional anyway) | §3.5 |

---

## 5. ACCEPTANCE + BUILD ORDER for the flex BUILD (not this spec)

### 5.1 Acceptance (updated to the ruled shape)
- **Levers & G-ATTR**: family switch `RL_FLEX`; sub-levers `RL_FLEX_NOW` (Law 1) and `RL_FLEX_FUT`
  (stream blend + V0 re-key + the harvey-thomas row) — separable per G-ATTR (BINDING). All-off ⇒
  **byte-exact** the corrected current board (fd90472c): null eligibility + single-stream futures
  make the identity structural (RL_YOUNG's exact-1.0 off-path discipline). The V0-re-key and
  stream-split sub-effects report as separate attribution rows.
- **FIRST GATE — byte-exact migration**: the store migration alone (null alts, weight-1.0 streams,
  BEFORE the harvey-thomas edit) re-prices to a byte-identical board. Only after this gate passes
  does any pricing change land. (The harvey-thomas edit is then the first real mover, attributed.)
- **Shape tests** (halt-not-warn, G-DATA): (i) **FLOOR, both channels**: Δflex ≥ 0 ∀p AND blend
  value ≥ pure-primary value ∀p — every dual/blended player ≥ his single-position twin (the R-3
  requirement + test); (ii) Δflex monotone non-increasing in rounds elapsed at fixed level (linear ρ,
  no time-axis cliff); (iii) Δflex ≡ 0 and byte-identity for null-eligibility single-stream players
  (B4-style non-mover parity INSIDE the candidate); (iv) PVC byte-check (synth delegation) + the
  smoothness harness on board aggregates; (v) owner edits are discrete declared events — never
  smoothed.
- **Book**: Law 1 Now-board-only ⇒ book byte-unchanged by Law 1; Law 2 applies the entry-year gating
  (§3.4) in the as-of matrix — B3 re-seal, G-COHORT re-measured walk-forward with the class-sum
  construction and min(y1,y2) denominator asserted by code reading (acceptance_v1_6).
- **Anchors**: `max-gawn`/`kieren-briggs` (A-GAWN, BINDING — "clearly above" must hold under any
  granted eligibility, prices reported with flex attribution) · `sam-darcy` (A-DARCY — both channels
  now non-negative under the ruled shape, §3.1; his attribution reports any flex rows) ·
  `willem-duursma` (A-DUUR — G-COHORT denominator flow reported) · `harvey-thomas` (NEW: the R-9
  V0-re-key GFWD→MID, reported as its own attribution row) · A-PEAK/A-FADE untouched unless
  designated. Panel 10/10 on the candidate; frozen-suite full pass.

### 5.2 What carries from v1 UNVERIFIED-BY-RULING but VERIFIED-BY-CODE (unchanged)
The futblend substitution point (rl_model.py:45) · the per-leg REPL netting (rl_model.py:317) · the
`posval`-monotonicity MAX collapse · the `params.json` rounds input (rl_model.py:4) · the `_v0key`
gfut term (`_merged_recover.py:672`) · the `_b2hc`-style year-0 guard pattern (rl_model.py:314).

### 5.3 Build order (per DECISIONS v89 sequencing — BINDING)
1. The **dead-code strip** lands first, honoring §0.2 (the futblend seam and per-leg loop survive).
2. The **flex BUILD** (Opus seat) implements THIS spec: re-assert §0.1 against the post-strip head →
   store migration → **byte-exact first gate** → harvey-thomas edit (R-9) → Law 1 + Law 2 levers →
   full acceptance (§5.1) → candidate, BUILD-REPORTED until prescreen.
3. No bake/tag/main action belongs to this spec or that build's candidate.

---

## 6. IN PLAIN TERMS (for Luke)

Every player on the board has one position today and one settled future position, and right now
they're the same for everyone — so nobody is priced for versatility. Your rulings set exactly how
that changes, and nothing here is an open question anymore.

**This season:** a player you've marked as genuinely covering two positions counts at whichever one
adds more — your words, full value, no haircut — and that bonus shrinks in a straight line over the
24 home-and-away rounds, because flexibility you can't use anymore isn't worth anything. He can never
be worth LESS than an identical one-position player; that's wired in as a test the build must pass.

**The future:** nobody is "turning into" anything. A player has one future position — but you can say
that position is, for example, 75% "pure midfielder" and 25% "midfielder who can also swing forward."
Those numbers are yours alone: the engine never guesses them, and they stand until you change them.
In the 25% world, the swing counts at whichever of the two positions adds more — same max rule as
this season. The arithmetic then just averages the worlds by your probabilities. And because the
swing world can only ever add, a player with a genuine second string is never worth less than his
plain twin — same floor, same test.

**Your sheet stays easy:** keep writing comma-lists; the engine knows a key forward already covers
general forward and strips that automatically; if a row still has more than one real alternate after
that, it stops and asks you rather than guessing. **Harvey Thomas is settled** by your call: drafted
as a general forward, still forward-eligible this year, future = midfielder, full probability — the
first player whose future differs from his present, and his start-value pricing moves to the
midfield curve accordingly. **At each new season** your word rolls the positions: what you say he is
becomes current, and your future numbers carry until you change them.

The build that implements this waits for the code clean-up to land first, and its very first gate is
proving that adding the new empty fields changes nothing at all — byte-for-byte — before any real
pricing moves.

_No engine, store, or gate file was touched in this job. Spec only. v1 carried byte-exact alongside
as the record of what was asked; this v1.1 is what gets built._
