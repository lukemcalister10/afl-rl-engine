# PLAN — FLEX SPEC LAW-2 REVISION → SPEC v1.1 · 2026-07-09 · FABLE seat (spec-only)

_Job: DIRECTIVE_flex_law2_revision_fable_v1 (manifest tier 6, auto mode — this PLAN is the first
committed artifact). Written against manifest v4.3 · DECISIONS v89 (§28 charter carried per the
directive's VERBATIM-INTENT statement; §34 = the ten rulings + probability source, quoted from v89
directly). Base: live `main` b303795 (fetched fresh this session; = merge of PR #52 with 2effba2 an
ancestor — matches DECISIONS §35's supervisor verification). Store `a2fbc9a0` (boot-guard asserted,
matches §35 canonical identities). READ-ONLY fence on engine/data honored; deliverable = SPEC v1.1._

## What this job does
Re-cut `SPEC_positional_flex_v1.md` (pinned 49a1435d, PR #50) into **SPEC v1.1**, the single document
the flex build will implement from:

1. **Re-found Law 2 on the ruled meaning (§28):** Law 2 prices PROBABILISTIC FUTURE ELIGIBILITY, not
   positional transition. One future position per player; that position may be a PROBABILITY BLEND of
   eligibility STREAMS (owner's JHF example: ~75% pure-MID + ~25% MID/G-FWD, the MAX law applying
   WITHIN the dual stream). "80/20 meet-toward" = probability weights across streams. The
   "phasing toward a destination position" framing dies everywhere, §7 plain-terms included.
2. **Fold the ten rulings as RULED (§34):** options sections collapse to decisions — probabilities
   OWNER-PROVIDED · R-1=A (Option B one line, future refinement, not offered) · R-3 pure MAX,
   friction-dial RETIRED, never-negative FLOOR kept as requirement + test · R-4 linear ρ, 24 rounds,
   no finals · R-5 hybrid schema · R-6 Law 1 year-0 only · R-7 owner-curated register · R-8 carry ·
   R-9 Harvey Thomas future=MID (p=1.0) · R-10 keep gfut.
3. **Update interactions + acceptance** to the ruled shape (L1c keying, walk-forward gating,
   build-order with the byte-exact-migration first gate), carrying v1's verified machinery findings
   (futblend substitution, per-leg REPL netting, params.json rounds input) unchanged where untouched.
4. **Supersede cleanly:** commit `SPEC_positional_flex_v1_1.md` in `session_2026-07-09/flex_spec/`
   with a header naming v1 SUPERSEDED, citing DECISIONS §28/§34. v1 is NOT edited; a byte-exact copy
   of v1 (from its pinned SHA) is carried into the same directory purely so the record and its
   supersession sit together on this branch (main does not yet carry PR #50).

## Verified this session (fresh fetch, live main b303795)
- `futblend(p)` → `[(gfut(p),1.0)]` at rl_model.py:45; per-leg weighted REPL netting
  `sum(w*posval(base-REPL[gg]) for gg,w in fut)` at rl_model.py:317 — the live seam, unchanged.
- REPL table rl_model.py:261: MID 80.1 · GEN_DEF 78.3 · RUC 78.5 · KEY_DEF 68.4 · GEN_FWD 70.9 ·
  KEY_FWD 66.8.
- Store `a2fbc9a0`, 2652 records; `jason-horne-francis` = MID in all three columns today (the JHF of
  the owner's example); `harvey-thomas` = GFWD in all three columns (the R-9 edit is still to ride
  the flex build's eligibility migration, as ruled).

## Out of scope (fence)
Any engine/data edit · re-opening ANY ruled question · new design forks (a genuine ruling
contradiction STOPS the job and is returned in one paragraph) · docs pack · bake/tag/main actions.

## Sequence
PLAN (this commit) → SPEC v1.1 + byte-exact v1 carry (second commit) → push → candidate PR → return.

Band 0.5–1.5 h, confirmed. BUILD-REPORTED until prescreen.
