# R106.7 FLOOR-HALF — findings for the owner's conversation

## 1. A/B chain — CLEAN (kill-switch)
`RL_FLEX=0` on the corrected store builds board **807e6551** — **matching the directive's expected value byte-for-byte**.
The whole §1b (projection + floor halves) and the item-284 guards are cleanly gated: FLEX=0 reproduces the
writes-only board exactly, no eligibility read leaks outside the flex gate. Dev-shell FLEX=1 reproduced the bake
board (9829d01a) — deterministic.

## 2. FINDING — non-DPP conservation ripple (FLEX-gated, rounding-level)
Of the 85 active board movers (ee70335a → 9829d01a):
- **32** are valid-DPP direct §1b moves (floor lifts: Petracca +74, Treloar +118, Yeo +116, Kelly +108, …).
- **4** are DPPs with no beneficial lower bar (jase-burgoyne etc.) that moved only via the ripple below.
- **49** are **genuine single-position** players (single MID / G-DEF / RUCK) that moved **±1 to ±4**.

Single-position players carry no §1b bar, so these 49 cannot move from §1b *directly*. They move through the
**Leg-B un-compress per-position conservation `C[pos]`** (the documented pool renorm): the floor-half lifts the
DPP production pool for MID / GEN_DEF / GEN_FWD / RUC, so `C[pos]` re-normalises those positions, nudging
players who sit near a numéraire rounding boundary by ±1. This is:
- **FLEX-gated** — none of it appears at RL_FLEX=0 (807e6551 matches the directive expected exactly);
- **the same interaction class the projection half already produced** on ee70335a (accepted at item 295);
- **rounding-level** — max single-position move is ±4, most ±1.

**Driscoll litmus HOLDS:** nathan-o-driscoll (100% MID, single-position) 894 → 894 unchanged; Bontempelli
3897 → 3897 unchanged. The directive's "single-position → NO §1b effect" holds for the named litmus rows;
the 49 rippled rows are a reported consequence of the pre-existing conservation layer, not new §1b leakage.

This is surfaced for the owner's call. It is not a G-COHORT breach (the sole hard halt). If the owner wants
single-position rows strictly invariant under §1b, that is a change to the Leg-B conservation (out of this
fence) — a separate decision.

## 3. item-284 — store is clean
The store scan finds **0** cross-class / present-not-in-set rows after the two owner corrections (both
corrections themselves removed present-not-in-set errors). The runtime registry is clean (only the selftest's
own fixtures self-flag). The four cross-class fixtures + the present-not-in-set synthetic all resolve
single-position (y0dpp_bar → None); a valid DPP still resolves its bar (verdict always produced).

## 4. Named rows (shipped numéraire board, base ee70335a → new 9829d01a)
| row | base | new | Δ | bar | note |
|---|---|---|---|---|---|
| Christian Petracca | 2881 | 2955 | +74 | GEN_FWD | floor binds; relay +29/+97 was pre-amendment |
| Colby McKercher | 3904 | 3824 | −80 | GEN_DEF | store fix: bar GEN_FWD→GEN_DEF; most of +105 off |
| Jake Lloyd | 100 | 104 | +4 | GEN_FWD | bar stays GEN_FWD, now legitimate; ≈ unchanged |
| Harry Sheezel | 7963 | 7964 | +1 | GEN_FWD | projection-leg; floor lifts low band nodes |
| Marcus Bontempelli | 3897 | 3897 | HOLD | — | single MID; no §1b bar |
| Nathan O'Driscoll (100% MID) | 894 | 894 | HOLD | — | single-position, NO §1b effect ✓ |

## 5. Ledgers (item-256 schema)
- MOVEMENT ledger: 85 active movers, 1150 total num-SCAR (all-mover table committed).
- value-up / rank-down FAILURE subset: **5** (the relay's was 115); tie-break = POSITIONAL rank. All are +1
  value moves whose positional rank slipped as larger DPP movers leapfrogged them.
