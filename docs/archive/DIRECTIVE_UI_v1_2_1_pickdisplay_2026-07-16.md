# DIRECTIVE — UI v1.2.1: HELD-PICKS DISPLAY FIX · 2026-07-16
### TIER 3 · ui/-FENCED · continues PR #99 (branch `claude/club-valuation-ui-v1-2-gdghtf`) in a FRESH
### Claude Code chat. The owner HOLDS the #99 merge until this lands; one viewing, one click.

## EFFORT: Low (display-only; three changes, no data or pricing logic). MODE: auto (PLAN first).
## TIME: 30–60 minutes wall-clock.
## BASE: branch `claude/club-valuation-ui-v1-2-gdghtf` at `2d00e3f` STRICT (a moved branch = HALT-AND-ASK).

## CONTEXT (register item 194 — read it): the owner flagged 2027 #2 (ex-Fremantle) priced 2,700 ==
2027 #1. VERIFIED NOT A UI BUG: the canonical engine curve has curve[1] == curve[2] == 3000 (flat
top); the ingest is faithful (3000 × 0.90 = 2,700) and every other screenshot row reconciles to the
curve exactly. THE CURVE is the defect and Leg D re-derives it (watch row filed). **CHANGE NO
PRICING. Values stay live-curve-faithful.**

## THE JOB (per-task commits + one screenshot each)
1. **SORT:** within the held-picks panel, order picks by VALUE DESC; tie-break band-low ASC, then
   year ASC. (Today's tie at 2,700 displays in ledger order — the owner read it as disorder.)
2. **TWO COLUMNS:** 2026 picks | 2027 picks, side by side, each value-sorted per (1).
3. **PER-YEAR TOTALS:** each column headed by its Σ (e.g. "2026: Σ 14,470 · 12 picks"); RETAIN the
   existing overall Σ + total pick count in the panel header.

## FENCE
IN: the held-picks panel component + its screenshot refresh. OUT (touch = HALT): ingest_inputs.py ·
any pricing/rounding · all other pages · docs/. RETURN ≤15 lines: head SHA · before/after screenshots
· confirm zero pricing deltas (byte-diff the data bundle — it must NOT change).
