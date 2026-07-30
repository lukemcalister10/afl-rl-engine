# ITEM 271 — STAGE A HAND-BACK: the deferred 62 edits, applied and attributed

**Branch** `claude/issue-271-re-derivation-3b6jc6`, based on `main` `0b105d9`. **Nothing is adopted.**
The candidate is the branch (audit Correction 2); `main`'s board, UI bundles and release identities are
untouched by this work.

Every figure below was measured on this box, on the artifacts named. Every count names its denominator.

---

## IDENTITIES MOVED

| | before | after |
|---|---|---|
| store `engine/rl_after/rl_model_data.json` | `5d6e56d0` | `265f55d5` |
| `data/v0surf.pkl` | `4cfc0b99` | `19d085a2` |
| v0surf signature set | `8faa737b` · `b08a5a7e` | `85e57195` · `d071e743` |
| board `data/rl_build/rl_app_data.json` | `3d4e2e50` | `dca21c91` |
| `release_contract` `contract_sha256` | `85b027f3` | `348855fb` |

**Unmoved, and asserted so:** `rl_model` `293e21d6` · `engine_head` `404e8113` · `fv` `d10aa93e` ·
`bust_prior` `5942aa6a` · `q97m` `cfdc7321` · `register` `652d83e8`. Stage A changes **no engine source** —
it is a store edit plus the re-bake it forces.

---

## THE EDIT SET — 62 fields, 54 players, of 2,651 store rows

Re-derived from the ruled sources (the committed write-then-revert diff `3df3a85`→`99cd539`, plus
`OWNER_RULINGS_Q1_Q9.md` and #262 Addenda 2/3). The owner's sheet was not attached to the fire message, so
the committed sources govern, as ruled.

| field | edits |
|---|---|
| `present_position` | 45 |
| `future_position` | 14 |
| `p_dual_stream` | 2 |
| `alternate_position` | 1 |
| **total** | **62** across **54** distinct players |

This reconciles to the sealed record with nothing left over: 43 present + 12 future + 1 alternate as
submitted, plus the 2 intended `p_dual_stream` (Graham 70→90, Petracca 50→70) = 58 sheet; plus the 4 R2-1
overrides (Lester and Lukosius, present **and** future) = 62.

**Named checks, all PASS:** R2-1 Lester → SD/SD · R2-1 Lukosius → SF/SF · Q1 Farrar present → KPF ·
Q2 Graham 90 · Q2 Petracca 70. Addendum 2 Q1's other three named present-position changes — Owens, Laverde,
McInnes — contribute **zero** edits because `main` already carries the target values, exactly as Lever does
under R2-1.

**Isolation, measured:** the two stores differ in the 62 position fields and in **nothing else** — zero
other player-level field differences, zero players whose season rows differ, 2,651 rows both sides.

The manifest is committed at `EDIT_SET_62.json`.

---

## Q-E INSTRUMENT SET — all four arms, in the ruled order

### 1. Control arm (the ruling's addition) — PASS

Refit on the **unchanged** landed store, through the declared `RL_V0SURF_REFIT` lane, reproduced the landed
frozen pickle `4cfc0b99` **byte-identically**, with the frozen set `{8faa737b, b08a5a7e}` intact. Exit 0.

**And it can fail.** Flipping one non-edited player's `future_position` (Nick Daicos, MID→SF) in the
workspace store moved the signature `8faa737b` → `60288e97` and the pickle md5, exit 3. The workspace was
restored and re-asserted at `5d6e56d0` before proceeding.

This also answers, in the strongest terms available, the `refit_v0surf.py:17` precondition that has been
unreachable since the split: this box reproduces the committed surface exactly.

### 2. Baseline board reproduction — PASS

Rebuilt the board from the **baseline store + baseline surface** on this box: `3d4e2e50`, byte-exact against
the pin. Without this, every mover count below could have been a container artifact rather than an edit.

### 3. Reverse-map diagnostic — PASS, exactly

Reversing the 62 edits at payload level — each player's label put back to his pre-edit `gfut` at the point it
enters the fingerprint — reproduces the prior signature **`8faa737b`, exactly**. The equality is non-vacuous:
had the pick curve, the 37 gates, roster membership, an age or a pick moved, it would fail.

- roster rows in the fingerprint sample: **1,448** (the ND 1–64 count #225 stage 2 reached independently)
- edited players in that sample: **44** of 54
- **label movers in that sample: 10** — independently reproducing the seam audit's figure

The ten, with picks: adam-treloar (14) · archie-roberts (54) · chayce-jones (9) · jack-lukosius (2) ·
joel-hamling (41) · oliver-hollands (11) · oscar-adams (51) · ryan-lester (30) · touk-miller (29) ·
zeke-uwland (2).

### 4. Determinism, then the bake

Three repeated refits: byte-identical (`19d085a2` ×3). Baked through
`RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 … --bake`, pinned in the same commit. **No fallback restored, no
signature-function change, no widening of the frozen set** — the set still holds exactly two signatures.

### 5. Changed-cell inventory, attributed

| block | moved / total per surface |
|---|---|
| `c18` | 450 / 540 |
| `surfN` | 1,080 / 1,080 |
| `surfR` | **0 / 1,080** |
| `meta` | 9 / 48 |
| **per surface** | **1,539 / 2,748 (56.0%)** |
| both surfaces | 3,078 / 5,496 |

`c18` moved for 5 of 6 positions; **RUCK: 0 of 90**. `surfR` — the RUCK maturity surface — did not move at
all. That is the predicted signature of these ten movers, none of whom touch RUCK.

**The fit-sample counts are fully accounted for.** Predicted from the ten named movers versus measured in the
surface metadata:

| pos | predicted Δn | measured Δn |
|---|---|---|
| KPD | −1 | −1 (143→142) |
| KPF | 0 | 0 (169) |
| MID | −4 | −4 (413→409) |
| RUCK | 0 | 0 |
| SD | +2 | +2 (272→274) |
| SF | +3 | +3 (257→260) |
| **net** | **0** | **0** |

Every position matches and membership is conserved. There is no unexplained delta anywhere in the surface.

---

## THE BOARD — 535 movers of 804 active rows, every one attributed

Board `3d4e2e50` → `dca21c91`. Parity gate PASS (all 804 values == engine gated `ev()`, eps=0), numéraire
guard PASS (pick-1 = 3000), FUT-LABEL assertion PASS (90 dual rows). Reproduced four times independently:
bake mode, dev mode, and the canonical re-run.

- **VALUE movers: 535 of 804** active board rows
- **RANK movers: 681 of 804**
- **movers with no named cause: 0**

### The two channels, isolated by construction

Isolation used a **counterfactual surface** — the old surface cells filed under the moved signature, so the
board could be built with the edits applied and the surface held. It was written to scratch and passed via
`RL_V0SURF_PKL`; **it was never pinned and never written to `data/`**. Note that bake mode correctly
*refused* this override as an unknown model var; the counterfactual was therefore built in dev-shell mode,
after proving dev mode reproduces the bake-mode board `dca21c91` byte-identically on the same inputs.

| channel | movers | mechanism |
|---|---|---|
| A — the 62 edits, own row | 53 | the edited player's own bar/curve moved |
| A — the 62 edits, cohort | 382 | `gfut` cohort membership moved (below) |
| B — the stage-A re-bake | 100 | the refit V0 surface |
| **total** | **535** | union is exact; 0 unexplained, 0 cancelling |

53 of the 54 edited players moved. The one that did not is **Harvey Gallagher** (present SF→SD), whose value
holds at 138 — the bar change does not reach his rounded figure.

### Magnitudes

| group | n | mean Δ | median Δ | max abs Δ |
|---|---|---|---|---|
| edited players | 53 | +25.96 | +5 | 854 |
| non-edited | 482 | +4.34 | 0 | 351 |

The largest movers are dominated by edited rows: Touk Miller +854 (MID→SF), Jordan De Goey +597,
Jack Lukosius −559, Bradley Hill +510, Adam Treloar +507, Ryan Lester −440.

### FINDING — the third live `gfut`-keyed fit, and it is not on #225's map

The 382 non-edited movers are **not** the surface and **not** rounding. Bisecting the edit set by field class,
with the surface held in all runs:

| edits applied | movers | of which non-edited |
|---|---|---|
| `present_position` only (45) | 142 | 103 |
| `future_position` only (14) | **413** | **382** |
| `p_dual_stream` + `alternate_position` only (3) | 4 | 1 |
| all 62 together | 429 | 382 |

The `future_position` edits carry it, and `future_position` is exactly what moves `gfut`. The mechanism is
`engine/forward_valuation/par_build.py:45-50`, which builds the par surface **live from the roster, grouped
by `MA.gfut(p)`**. Moving 14 players between position groups moves those cohorts, which reprices everyone
in the affected groups — and leaves RUCK alone, which is what the board shows (0 of 55 RUCK rows moved).

**Why this matters beyond stage A:** #225's drafted-vs-played site map is scoped to
`engine/rl_after/rl_model.py` and does not mention `par_build.py`. This is not a defect on that map's axis —
`par_build` is already keyed on the played position, which is correct — but it **is** a third live
`gfut`-keyed fit on the value path, alongside the V0 surface and the in-engine fit that R3 holds out of the
bake. Any stage-B reasoning about what moves when the played axis moves must include it. Recorded here, not
acted on: stage A changes no code.

---

## SIBLING RE-PINS (Q-D: re-pinned to the branch's own identities, never deleted)

- `data/expected_boot.json` — `store`, `board`, `v0surf`
- `data/release_contract.json` — `held_candidates` **board** and **store** candidate sides re-stamped
  (`engine_head`, `rl_model`, `fv` candidates unmoved because the engine did not move); `contract_sha256`
  re-sealed. **All 5 declarations survive** — deletion is the adoption commit's act.
- `data/season_state.json` — `source_store_md5` re-derived; **every other derived value unchanged**
- `data/rl_build/rl_app_data.json.srcmd5` — regenerated by the build

**Verification:** Guard 5 PASS (`store 265f55d5 == pinned`, `rl_model`/`fv` == pinned) ·
`release_contract.py verify` PASS at `348855fb`.

---

## SCOPE HELD

No UI writes (R3-2) · no adoption · no engine source change · no method change · no shipped-artifact
regeneration on `main` · `sibling_repin` **not** run (its outputs include `ui/data/board_view_*.js`) ·
the frozen set never widened · no fallback restored.

## PROCESS NOTES

- `git fetch --unshallow` before any ancestry claim. Branch level with `origin/main` at `0b105d9` at start.
- Python 3.12.3 venv at `/home/user/venv312`, `--require-hashes --only-binary=:all:`; env-pin verified
  (numpy 2.4.4 cp312 + bundled OpenBLAS `05c9f9eb`, byte-exact). Pin not weakened. Built outside the repo so
  it cannot be committed.
- No parallel engine builds; every build sequential and single-threaded.
- **One self-caught error, recorded:** the first field-class bisect loop did not check exit codes, and the
  `future_position` run had HALTed at the signature gate (the held-surface pickle could not serve the moved
  signature), leaving the previous board in place. It was caught because two different stores reported an
  identical board. Re-run against the correct pickle. No result above rests on the bad run.
