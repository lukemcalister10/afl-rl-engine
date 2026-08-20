# TEST LEDGER — baseline a8485f8 (pre-repair) vs HEAD (tail reconciled, apply halted)

| suite | a8485f8 baseline | HEAD | reading |
|---|---|---|---|
| ui/tools/ownership_store_apply.py verify | CRASH (incoherent base) | **PASS** all six read cb38ef11 | fixed |
| ui/tests/ownership_store_apply.test.py | CRASH | **28/28** | fixed |
| ui/tests/club_curve_provenance.test.py | 7/35 | **22/35** | +15; the 4 residual FAILs are the ONE curve-contract drift (the live CURVE DRIFT halt pre-empts three negative controls' own tamper halts; CASE1 prices 0 picks) |
| ui/tests/extract_seam.test.py | 42/42 | **42/42** | held |
| ui/tests/club_totals_parity.test.js | 17/17 | **17/17** | held |
| ui/tests/release_seam.test.js | 30/30 | **30/30** | held |
| ui/tests/counting_rule.test.js | 24/24 | **24/24** | held |
| ui/tests/adoption_gate.test.js | 3/3 | **3/3** | held |
| ui/tools/generate_movers_transition.py --check | OK | **OK** | mirror not stale |
| ui/tools/rebuild_movers_derived.py --check | OK | **OK** | derived blocks not stale |
| ui/tests/movers.test.js | 66/66 | 63/66 | 3 FAIL, ALL one cause: the movers bundle's newest stored point is the PRE-LANDING board 4b448a82 while the app now loads the landed a05fe951. That is the missing out-of-round column for THE LANDING — the same halted carrier as the lineage register (15_..._HALT_fork.txt), now visible because the UI finally loads the landed board. |
| ui/tests/ownership_sidecar.test.js | 35/35 | 21/35 | see below |
| ui/tests/ownership_single_source.test.js | 17/17 | 9/17 | see below |

## The two ownership suites, measured both ways

The ingest refused, so `ui/data/ownership.js` cannot be a correct mirror. Both available artifacts
were measured under the landed board_view:

| artifact shipped | ownership_sidecar | ownership_single_source |
|---|---|---|
| the ingest's HALTED mirror (shipped) | 21/35 | 9/17 |
| the pre-landing mirror retained instead | 22/35 | 16/17 |

**13 of the sidecar failures are IDENTICAL in both columns** — they are era-bound fixture cases that
fail on the landed board whichever mirror ships, and are not attributable to the choice. The choice
accounts for 1 sidecar case ("…and it is non-empty… — 0 entries") and 8 single_source cases, every
one of which asserts a property of a POPULATED mirror ("declares the store as its source of truth",
"names in full the store it was generated from", "nOverriding is 0 BY CONSTRUCTION", the two
NON-VACUITY divergence probes…). All 9 go green the moment the apply completes.

Neither artifact can show a wrong club: the halted mirror refuses outright, and the pre-landing
mirror fails the app's own pin check and degrades to the board's store-derived club (its suite's own
words: "a refused mirror degrades to the board's store-derived club — a degraded display, never a
wrong club"). The HALTED mirror was shipped because it is the ingest's own designed output and it
states the reason on its face rather than leaving a pre-landing overlay silently in place under a
landed board.
