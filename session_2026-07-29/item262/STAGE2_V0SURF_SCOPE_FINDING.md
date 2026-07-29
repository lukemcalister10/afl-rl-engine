# FINDING — stage 2's position edits move the V0 pick-curve surface. STOP, per R2-3.

**No re-bake taken.** Owner ruling R2-3: *"Any non-reproduction at the diagnostic, or any cell
difference at the comparison however small: STOP and report — nothing pins on an unexplained delta."*

The delta here is *explained* in mechanism but its **consequence exceeds the landing's stated scope**,
which is why it stops rather than proceeds.

---

## What happened

Stage 2 applied cleanly to the store. The board build then HALTed at v0surf again — but this halt is
**a different kind from stage 1's**.

| | stage 1 (rename) | stage 2 (owner edits) |
|---|---|---|
| why the signature moved | the label *spelling* changed | the **roster composition** changed |
| reverse-map reproduces frozen? | **yes, exactly** | **no — and cannot** |
| surface cells differing | **0 of 5,496** | **1,539 of 5,496** |
| magnitude | none | material — e.g. `c18.MID[7]` 2423.0 → 2623.8, ~8% |

Stage 1's signature move was cosmetic. Stage 2's is real.

## Why

`_v0surf_sig` hashes `str(MA.gfut(p))` per roster row, and `gfut()` is
`future_position or present_position` (`rl_model.py:45`). The owner's deliberate edits changed
`gfut()` for **14 players**, and **10 of them sit inside the V0 national-curve sample** (type ND,
pick ≤ 64):

| player | pick | gfut before → after |
|---|---|---|
| Zeke Uwland | 2 | MID → SD |
| Jack Lukosius | 2 | KPF → SF *(R2-1 override)* |
| Chayce Jones | 9 | MID → SD |
| Oliver Hollands | 11 | SD → MID |
| Adam Treloar | 14 | MID → SF |
| Touk Miller | 29 | MID → SF |
| Ryan Lester | 30 | KPD → SD *(R2-1 override)* |
| Joel Hamling | 41 | KPD → KPF |
| Oscar Adams | 51 | SD → KPD |
| Archie Roberts | 54 | MID → SD |

The other four are outside the sample and have no effect on the surface: Max Hall (MSD), Bailey
Banfield (RD), Tyrell Dewar (PDN, pickless), Zachary Williams (PDA, pickless).

Ten roster rows changing bucket — several at the top of the curve, two at pick 2 — is enough to
refit the surface materially.

## Why this stops rather than proceeds

Two clauses of the directive are now in tension, and only the owner can resolve it.

1. **Scope fence, issue #262:** *"No value re-derivation. No curve change. No valuation math change.
   No bar change."* The V0 pick-curve surface **is a curve input**. Re-baking it is a curve change.

2. **Owner ruling Q1:** *"then my edits applied, with every mover reported and attributed to the
   specific edited rows."* If the surface refits, board values move for players **nobody edited** —
   the surface is fitted over the whole cohort and prices everyone. Those movers cannot be attributed
   to specific edited rows, because they have no edited row behind them.

So re-baking would both breach the scope fence and make the promised attribution impossible.

## The options, none taken

1. **Re-bake and widen the mover report.** Accept that stage-2 movers come in two buckets — *direct*
   (the edited players) and *surface-refit* (everyone else, via the refitted V0 curve) — and report
   them separately. Honest, but it is a curve change inside a landing that forbids one.

2. **Defer stage 2's position edits to the re-derivation job.** Land stage 1 alone — it is proven,
   zero movers, and it is the part that has to happen exactly once with the rename. The 43+12+1+2
   sheet edits and the 4 R2-1 overrides then ride with the re-derivation, which refits everything
   anyway and where a moved curve is expected rather than forbidden. **The per-season eligibility
   data can still land now**, since it has no reader yet and moves nothing.

3. **Hold the surface at the stage-1 freeze.** Mechanically unavailable without either widening the
   frozen set or changing the signature function — both explicitly forbidden. Recorded so it is not
   proposed later as if it were open.

**Recommendation: option 2.** It keeps the scope fence intact, keeps the zero-movers proof meaningful,
lands the two things that genuinely belong to this job (the vocabulary replacement and the per-season
data), and hands the position edits to the job whose whole purpose is re-deriving value. Option 1 is
defensible if the owner wants the edits live now and accepts a curve move inside this landing — but
that is his call, not a supervisor's.

## State of the tree at this finding

Stage 2's **store write is applied and committed** so the work is not lost, but the tree is
**deliberately inconsistent and must not merge as it stands**:

- store `e4580f07` → `265f55d5`, `expected_boot.store` re-pinned to match
- the committed **board is still stage 1's** `3d4e2e50`, built from store `e4580f07`
- so `data/rl_build/rl_app_data.json.srcmd5` names a source the store no longer is

That inconsistency is the honest record of where this stopped. Resolving it means either completing
stage 2 (option 1) or reverting the stage-2 store write (option 2) — both are one step once the owner
rules.

### Stage 2's store content, verified

| | |
|---|---|
| player-level edits | 62 = 58 from the sheet (43 `present_position`, 12 `future_position`, 1 `alternate_position`, 2 `p_dual_stream`) + 4 R2-1 overrides (Lester, Lukosius) |
| fields changed outside those four | **none** |
| per-season eligibility written | **11,264 of 11,264** — full coverage, all 1,924 scoring players |
| existing season fields moved | **0** (`year`, `avg`, `games` untouched) |
| season values outside the six codes | **none** |
| bust defaults applied | **0**, as ruled vacuous at Q9 |
| resolution path | general 4,803 · plain 3,599 · blanket overlay 2,419 · Q4-ruck 223 · Q5/Q6 table 209 · sheet-explicit 11 |

`affl_team` was **not** touched — Q2 routes those 16 trades through the #232 sidecar.

Spot-checked against the ruling table and correct in every case: Harrison Himmelberg's 11 explicit
rows transcribe as given (KPF ×6, SD ×5); Elliott takes the blanket overlay (KPF ×7); Laverde is
SF when FWD and KPD when DEF; Lever is KPD 2015–2025 and SD in 2026; Lukosius keys only in 2019,
2023, 2024, 2026; Blakey takes his ruled treatment despite an unflagged sheet row; Ginbey has no key
season.
