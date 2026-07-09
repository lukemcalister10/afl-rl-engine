# PLAN — POSITIONAL-FLEX SPEC (FABLE seat, spec-only) — 2026-07-09

**Directive:** DIRECTIVE_flex_spec_fable_v1 (manifest tier 6). Mode auto ⇒ this PLAN is the first
committed artifact. **Read-only fence on engine/data honored for this chat's lifetime — the deliverable
is ONE design document; no engine, store, or gate file is touched.**

**Base cited on entry:** session checkout at `d4e8f6dc` = tag **v2.6** (the engineering head; the repo's
`main` ref sits behind it at `00d82dde`, a docs-upload line — the directive's own pin "tag v2.6 = d4e8f6dc"
confirms d4e8f6dc is the intended base). Store md5 `e1b4d8bf` confirmed by the session-start boot guard.
**Time band 1.5–3 h: confirmed.**

## Ground already established (by code/doc reading at v2.6)
1. **Position model (post-DPP-strip):** store carries three single-valued columns —
   `drafted_position` (cohort curves, `p['pos']`), `present_position` (year-0 REPL bar, `bnow`),
   `future_position` (years-1+ REPL + peak/curve/runway, `gfut`). `futblend(p)` returns
   `[(gfut(p), 1.0)]` — the live single-leg seam (`rl_model.py:5-45`); in this build future==present
   for all 2652 records. The old `raw_multipos` probabilistic blend is DELETED (obituary stands).
2. **Weighted-leg machinery survives:** `proj_from_peak` already consumes a `fut` list of
   `(position, weight)` pairs and nets REPL per leg (`rl_model.py:317`) — an 80/20 split is a
   change to what `futblend` returns, not new pricing machinery.
3. **REPL is per-position** (`rl_model.py:261`): MID 80.1 · GDEF 78.3 · RUC 78.5 · KDEF 68.4 ·
   GFWD 70.9 · KFWD 66.8 — the RUC↔KFWD bar gap (11.7) is the largest flex arbitrage in the table.
4. **L1c young credit keys its cell by `gfut(p)`** (`_merged_recover.py`, `_ycred_mult`) — an
   in-transition player already keys his FUTURE position cell; KEY_FWD carries the ×0.92 T3 trim.
5. **No intra-season rounds axis exists** on the board path (season progress appears only as the
   R14/24 gate proration and the `_b2hc` present haircut) — rounds-remaining needs a declared input.
6. **F17/F24 / dead-code strip:** not present in this repo snapshot (HANDOVER items) — the spec will
   state its assumptions about the strip explicitly, including the risk that the single-element
   `fut` loop and `futblend` seam LOOK dead (future==present everywhere) and must survive the strip.

## Steps
1. ✅ Research (above).
2. Commit this PLAN.
3. Write `SPEC_positional_flex_v1.md` covering the full FENCE: the owner's three-part law made
   precise (current-DPP MAX × rounds-remaining · future-position 80/20 readings as owner options ·
   year-roll mechanics); representation/SSI (schema delta for eligibility); interactions with
   direction (REPL no-double-count, G-MONO, G-COHORT, L1c keying, lenses, display); symmetric forks
   with named store players (keys verified against `e1b4d8bf`); acceptance sketch (RL_FLEX lever,
   G-ATTR separability, shape tests, anchors at risk); plain-language close.
4. Commit spec → push `claude/new-session-yftulk` → candidate PR (BUILD-REPORTED until prescreen).
5. Return ≤30 lines: branch · head SHA · PR # · time vs band · owner rulings requested.
