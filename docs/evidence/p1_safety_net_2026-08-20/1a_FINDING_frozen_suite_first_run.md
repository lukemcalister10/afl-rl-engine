# FINDING — the frozen acceptance suite ran end-to-end for the first time, and it is not all green

**Raised by P1 1a. Not caused by P1. Presented, not repaired, and NOT put in the ruled-red ledger:
nobody has ruled on it, and a red nobody has presented is a FAIL, not a RULED-RED.**

Repairing `ship_gates_check.py:49` did what the record said it would: the frozen acceptance suite
(SHIP_GATES.md, frozen ref `764a0d91`) executed **every gate in the A / B / D families** against the
live head for the first time since it was bricked. Full output:
`1a_ship_gates_FIRST_FULL_RUN.txt`. Three-column rule (Luke, binding D10):
**CONTROL `7a07e369` · PREVIOUS `efea88e5` · CURRENT `1867e953`**.

## What the run confirms

| leg | verdict | why it matters |
|---|---|---|
| Guard 5 pre-flight | **PASS** | store `b745002e` == pin · rl_model `6fe7c415` == pin · fv `6e9a370e` checkout **and** loaded-path. The exact blocker is gone. |
| config manifest, gate mode | **LOADED** `eed19a75f775` | 84 model vars pinned, ambient cleared — the RL_GAMMA self-brick is genuinely repaired |
| **B4** | **PASS** | the suite **rebuilt the board from the checkout** and got `68be10c7` against shipped `68be10c7`. An independent byte-agree re-derivation of today's board of record. |
| **B3** | **PASS** | the book stable seal regenerated this run **matches the sealed baseline** `9f46aba3…`, 2650 players, sealed head `1867e953` |
| B2, B6, D14a–d, A1, A4–A8, A10, A11 | PASS | |
| B5 | FEATURE | 15 floor-saves, aggregate lift +4575; lowered 0, moved-outside-scope 0 |
| A13 / A14 | PENDING | PVC stage not run — by design |
| A15 | STRUCK | Luke 02/07/2026 |

## TWO REDS THAT ARE NEW AT THE CURRENT HEAD

Both are marked `<- MOVED` by the suite's own three-column comparison: they PASSED at CONTROL and at
PREVIOUS, and do not pass at CURRENT.

**A9 — FAIL.** `Ginnivan > Ward: 2198 vs 2837`. Passed at `7a07e369` and `efea88e5`.

**B1 — HALT.** The July-8 cohort construction. Raw class-year sums, unweighted across 17 classes:
`y1=62073.9 y2=68070.9 y3=78013.9 y4=88527.6 y5=89498.0 y6=86685.1 y7=79201.6`; denominator
`min(y1,y2)=y1`; ratios `y4=1.4262 · y5=1.4418 · y6=1.3965` against a **hard bar of 1.30** →
**BREACH at y[4,5,6], HALT**. Certified against engine `1867e953`, store `b745002e`, config
`eed19a75f775`. Passed at `7a07e369` and `efea88e5`.

## THREE REDS THAT ARE NOT NEW

**A2, A3, A12 — FAIL at all three columns.** These are the standing fails the RULEBOOK already
carries by name (PART 3: *"Standing-fails and named-row waivers from v1.21 (A2, A3, A12, A-PAIRS-3,
the earned-2-row waiver) carry forward AS RECORDED until Luke re-rules"*), and A2 in particular
ships red by explicit ruling (*"we can look at Curtis down the line"*). They are recorded, not new.

## Attribution, stated plainly

**Nothing in Package 1 can have caused A9 or B1.** P1 touched no engine file, no exporter, no store,
no data file and no dial; the G1 identity check before and after this package is byte-identical on
every value-bearing artifact, and the suite's own B4 leg rebuilt the board of record byte-exact from
the tree it graded. The suite has simply not been runnable while the head moved from `efea88e5` to
`1867e953`, and this is the first look.

**This is PLAN_v6 process law P5 firing in anger** — *a gate's name is not coverage*. The frozen
suite was named in the bake checklist as the bar throughout the period in which these two legs went
red, and it did not execute one gate.

## What is owed, and by whom

- **A9 and B1 are model verdicts, not tooling.** They are not P1's to repair and not P1's to rule.
- They are **NOT** entered in `acceptance/ruled_red.json`. The ledger requires a fork already
  presented in writing; this document is the presentation, and the ruling is the owner's.
- `ship_gates_check.py` is wired into no workflow and into no runner check, so nothing in the
  estate is currently red *because* of this. That is itself the finding underneath the finding.
- The suite wrote its normal gate snapshot for this head — `data/gates_snapshots/gates_1867e953.json`,
  the first for `1867e953` — under its own binding reporting rules (Luke, D10). It is committed as
  the record of the run. The out-of-fence report write to `/tmp` was **refused** by the rev143
  fence, exactly as designed.
