# L5 — THE DIAL CENSUS AND THE DOCKET

**#290, 2026-07-31.** Substrate for every measured figure: **store `81d24704` · v0surf `84fb0cde` · γ 1.0 · curve `e69a3f38`.** Measurement-only leg — **no bake, no gate moved, nothing installed.** Every run behind `tools/preboot_assert.sh`.

## THE CENSUS — the gate is zero rows without a token

Denominator is **L0's own count: 187 canonical rows.** Reproduce with `python3 l5_census.py`; output committed verbatim as `L5_CENSUS.txt`, per-row detail as `l5_dispositions.json`.

```
canonical rows   187
dispositioned    187
WITHOUT A TOKEN    0     <- THE GATE: PASS
L0 UNCLEAR rows resolved: 16 of 16
```

| disposition | rows | of 187 |
|---|---|---|
| RULED-EXEMPT | 88 | 47.1% |
| REACHED-BY-L1 | 26 | 13.9% |
| REACHED-BY-L8 | 19 | 10.2% |
| RE-DERIVED | 16 | 8.6% |
| DOC-CORRECTED | 8 | 4.3% |
| RETIRED-FROM-LIVE | 8 | 4.3% |
| REACHED-BY-L4 / L6 / L7 | 6 / 6 / 5 | 9.1% |
| DEFERRED-TO-ADOPTION | 2 | 1.1% |
| REACHED-BY-L2 / L3 | 2 / 1 | 1.6% |

**L5-owned (the five tokens): 122 of 187 = 65.2%.** Owned by another leg: 65 = 34.8%.

**RULED-EXEMPT is split, because one word was hiding three situations** — a census whose largest bucket is ambiguous is not a census:

| | rows |
|---|---|
| already-ruled-current — the row already states the ruled basis | **47** |
| sealed history — the standing scope boundary; C.2 forbids re-stamping | **31** |
| exempt case by case — each carries its own evidence pointer | **10** |

**`REACHED-BY-Lx` is deliberately not one of the five tokens.** It records *which leg owns the row*, so a row is accounted for without L5 claiming work it did not do. Only the 122 are L5's dispositions.

### How the dispositions were made

Authored **per row**, in `l5_census.py`, each with an evidence pointer that can be argued with. The lanes' own class labels are used as **corroboration, never as the rule** — L0 established that mechanical rules over these lanes are untrustworthy (three defensible rules gave three different denominators).

**Two errors my own guard caught, recorded because the catch is the reusable part.** Rows 53 and 60 initially carried each other's evidence strings — a true-sounding label attached to the wrong object, hazard class 1, in my own census. And a leftover line dispositioned row 60 twice; the `assert r not in D` fired. Both fixed and re-verified by re-run, not by re-reading.

## ESCALATED BY NAME — 3

*"UNCLEAR is not a disposition — it resolves by derivation record or escalates by name."* All 16 UNCLEARs resolved; three rows are dispositioned **and** escalated, because a disposition that carries a gap is not a closed row.

| row | what | the gap |
|---|---|---|
| **29** | `MA.REPL` replacement bars | **the deriving script is absent from the repo.** The bars are carried forward, not regenerable — the same reachability class as the v0surf bytes, the ND matrix and the derivation lane. **Ask:** recover the script, or freeze the bars as bytes under the R-A pattern. |
| **9** | `bust_prior_table.json` | **no writer exists**, and the pinned `_fitted_note` claims one does. Ratified as a docket by R-D; correcting a pinned note is a landing act. |
| **34** | `cm_400.pkl` (band) | a fresh refit does not reproduce the shipped artifact, so it is not regenerable from the tree. Frozen as bytes under R-A — named so the freeze is not read as *resolved*. |

## THE I.2 HEADLINE, MEASURED RATHER THAN RESTATED

> *For every `RL_*` the manifest pins, the landing asserts `manifest value == code default` — or removes the default so the read fails loud.*

Run `python3 manifest_vs_default.py`; output committed as `MANIFEST_VS_DEFAULT.txt` / `.json`.

| | measured |
|---|---|
| **RL_\* pinned by the manifest — the denominator** | **55** |
| default sites found for those names | **98** |
| **AGREE** with the manifest | **86** |
| **DISAGREE** | **12** |
| pinned names with **no** code default (the stronger remedy already in place) | **0** |
| `RL_*` with a code default but **no manifest pin** | **13** |

**All 12 disagreements are outside the live path**, checked individually — session scripts, a stale fixture, and old bake shell scripts — **with one that deserves naming**:

`engine/rl_after/verify_anchors.py:8` carries `setdefault('RL_GAMMA','0.85')` and its docstring instructs `RL_GAMMA=0.85 … python3 ../verify_anchors.py`. It sits in the engine tree, so it *looks* live. Measured, it is not: **nothing imports or invokes it** (the only reference anywhere is a migration script's file list), and it is in **none** of the pinned identity sets — not `fv` (that hashes `engine/forward_valuation`), not `engine_head` (`_merged_recover.py`), not `rl_model`.

So it is the `:504` **shape without the `:504` danger** — stated that way deliberately, because overstating it would be the mirror of the error that made `:504` dangerous. The real hazard is human: a successor who runs it as its own docstring instructs would check a **VOR** engine against **SCAR** anchors and get a drift report to be misled by. **Disposition: DOC-CORRECTED at the landing.**

**The 13 unpinned-but-defaulted names** are outside I.2's wording but worth seeing, because nothing pins them at all. One is live engine code: `RL_DAMP_K` default `5.8` at `engine/rl_after/_merged_recover.py:186`.

**Reported, not fixed.** Writing the assertion or removing the defaults is a landing act.

## THE DOCKET, BY NAME

Carried from Addenda H.5 and I.2, plus this seat's:

| # | entry | state |
|---|---|---|
| 1 | **`rl_model.py:504`** — the engine's own γ default, and its general class | **measured above**: 55 pinned names, 12 disagreements, all off the live path; the assertion itself is a landing act |
| 2 | **bake-mode vs plain-mode basis divergence** — the board builds under the manifest, the gate runs under code defaults | the mechanism behind #1; invisible until the two disagree |
| 3 | **the unshared-namespace binding** — `rl_export.py:69` `g = MA.__dict__` vs `one_source_selftest.py:114`'s `_merged_recover` exec dict | not the F1 cause, but it cost two invalid probes |
| 4 | **the curve payload hash recipe** — `md5(json.dumps(curve, sort_keys=True))`, int ladder, written down nowhere; **mint the helper** | still unwritten in code |
| 5 | **the asymmetric identity-length convention** — 8-char stamp vs 32-char contract, one-sided `[:8]` at `one_source_selftest.py:527` | writing the full md5 into the stamp FAILS the check |
| 6 | **F1's hand-copied `ev()` call sequence is unnecessary** — all three modes agree | **hygiene only, never to make a red go away** (H.3 stands) |
| 7 | **the doc-only γ sites** — `par_build.py:11`, `par_redesign.py:13`, and now `verify_anchors.py:8` + its docstring | DOC-CORRECTED at the landing |
| 8 | **`bust_prior_table.json` has no writer**; its pinned `_fitted_note` says it does | R-D docket; landing act |
| 9 | **the derivation lane's pins are path-selected** by `import harness_pvc` | guarded loudly by `load_matrix`; the guard is all that stands between two same-named files |
| 10 | **the reachability class has fired four times** — v0surf bytes, the ND matrix, the derivation lane, and now `MA.REPL`'s absent script | the freeze law must cover the **instrument**, not only the input |

## COSTS

Census + docket: **measurement only, no engine act, no bake.** `l5_census.py` and `manifest_vs_default.py` each run in **under 2s**. Nothing installed, no pin re-stamped, no gate moved.
