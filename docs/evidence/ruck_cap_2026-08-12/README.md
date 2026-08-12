# ORDER 20C — THE 12-RUCK CAP TABLE

> **Measurement only.** Nothing is wired, no shipped default is changed, no board is promoted,
> `data/expected_boot.json` in the checkout is not restamped. Branch `build/ruck-cap-table`, cut from
> `origin/main` `591d082`. Pre-registration `PREREG_RUCK_CAP.md`, committed at `d2c8af3`
> **before any measurement was run**.

**THE OWNER'S QUESTION, VERBATIM**

> "can you give me a list of the 12 players, what their rating was before this act, what it's going to
> be afterwards, and what it would be without the ruck cap?"

**PINS ASSERTED AT ENTRY AND EXIT — ALL THREE UNMOVED**

| pin | value | entry | exit |
|---|---|---|---|
| board `engine/rl_after/rl_app_data.json` | `94f1fec59f99c59d5890d5975c79fa9b` | ✓ | ✓ |
| store `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` | ✓ | ✓ |
| instrument `noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` | ✓ | ✓ |

Also unmoved in the checkout: `data/v0surf.pkl` `fbc5b393…`, `data/expected_boot.json` `d48f9a07…`,
`data/model_config.json` `efe922cb…`. Every build ran in a **scratchpad copy**; the checkout was never
written to outside `docs/evidence/ruck_cap_2026-08-12/`.

---

## THE HEADLINE, BEFORE THE TABLE

**Lifting the ruck cap does not move a single one of the 12 national rucks it binds on.** Not one.
Their board price is identical to the digit under the fix and under the fix-with-no-cap.

That is not a null result; it is the answer to the question ORDER 20B's P9 breach raised. The cap's
national binding set doubling from 6 to 12 is a change in a **latent scaffold quantity**, not in a
price. Board-path `v0_start` returns the **frozen D14 curve** for every national ND row
(`_merged_recover.py:1756-1759`), so the cap — which is applied inside `_v0_raw` (`:1219`, `:1247`) —
never reaches the number the board consumes. All 12 read `in_v0curve = True`.

Across the **whole board** the cap is worth **+102 on 748,894 (+0.0136%)**, on **17 of 1002 rows**,
**every one of them a pool ruck**, and **13 of those 17 are delisted players' 2%-of-`v0_start` scrap
remnants** (`:2230`) worth +74 between them. Excluding the scrap, lifting the cap moves the live board
by **+28**, of which **+31 is one player, Liam Reidy** — and three live rows go *down* by 1.

---

## TABLE 1 — THE 12 NATIONAL RUCKS (`_ruc_prior_cap` binding under the FIX engine)

Three board values, read out of three **built boards**, never re-derived.
BEFORE = the live board `94f1fec5` (HEAD engine, shipped defaults).
AFTER = the ORDER 20 par-separation fix, board `1dbd1480` (reproduced exactly).
NO-CAP = the fix with `RL_RUC_PRIOR_CAP=99`, board `48c23615`.

| player | eff pick | age | career games | **BEFORE** | **AFTER** | **NO-CAP** | Δ fix | Δ cap | `_v0_uncapped` HEAD → FIX | ceiling | binding | classification |
|---|--:|--:|--:|--:|--:|--:|--:|--:|---|--:|---|---|
| Tom De Koning | 30 | 27 | 113 | 1830 | 1830 | **1830** | +0 | **0** | 1114.5 → 1130.3 | 928.2 | already on HEAD | PRODUCTION-LED |
| Mitchell Edwards | 32 | 21 | 16 | 2411 | 2439 | **2439** | +28 | **0** | 984.3 → 996.6 | 865.2 | already on HEAD | PRODUCTION-LED |
| Max Gawn | 33 | 35 | 268 | 3336 | 3336 | **3336** | +0 | **0** | 1066.4 → 1079.8 | 834.4 | already on HEAD | PRODUCTION-LED |
| Samson Ryan | 42 | 26 | 29 | 296 | 302 | **302** | +6 | **0** | 599.4 → 794.5 | 681.8 | **NEWLY** | PRODUCTION-LED |
| Lachlan Smith | 47 | 21 | 2 | 399 | 399 | **399** | +0 | **0** | 423.6 → 572.5 | 546.0 | **NEWLY** | PRODUCTION-LED |
| Rhys Stanley | 47 | 36 | 230 | 28 | 28 | **28** | +0 | **0** | 438.4 → 592.5 | 546.0 | **NEWLY** | PRODUCTION-LED |
| Callum Jamieson | 48 | 26 | 17 | 10 | 10 | **10** | +0 | **0** | 588.8 → 784.9 | 522.2 | already on HEAD | PRODUCTION-LED |
| Darcy Cameron | 48 | 31 | 140 | 1669 | 1669 | **1669** | +0 | **0** | 551.4 → 747.9 | 522.2 | already on HEAD | PRODUCTION-LED |
| Marc Pittonet | 50 | 30 | 98 | 466 | 466 | **466** | +0 | **0** | 389.1 → 521.8 | 484.4 | **NEWLY** | PRODUCTION-LED |
| Jacob Molier | 52 | 20 | 0 | 283 | 283 | **283** | +0 | **0** | 354.1 → 474.5 | 457.8 | **NEWLY** | PRODUCTION-LED |
| Alex Dodson | 53 | 20 | 1 | 274 | 274 | **274** | +0 | **0** | 395.7 → 524.2 | 443.8 | **NEWLY** | PRODUCTION-LED |
| Dante Visentini | 56 | 23 | 27 | 1268 | 1274 | **1274** | +6 | **0** | 431.8 → 564.7 | 403.2 | already on HEAD | PRODUCTION-LED |
| **TOTAL (12)** | | | | **12270** | **12310** | **12310** | **+40** | **0** | | | 6 newly / 6 already | 12 production-led |

**The six already binding under HEAD**, which ORDER 20B did not name, are **Tom De Koning, Mitchell
Edwards, Max Gawn, Callum Jamieson, Darcy Cameron, Dante Visentini** — disjoint from the six it did.

**The ceiling moved on 0 of 12 rows.** `RUC_PRIOR_CAP · _cap_basis · _ruc_head_v0` is par-independent;
what the fix moved is `_v0_uncapped`, which rose through a stationary ceiling. Re-taken here, agreeing
with ORDER 20B on all 71 ruck rows (0 of 71 ceilings moved).

### the mechanism, per player (reported, NOT used to classify)

| player | `bestlvl(2026)` | nqual | in `_V0CURVE` | `v0_start` HEAD → FIX | ev() ceiling |
|---|--:|--:|---|---|--:|
| Tom De Koning | 101.50 | 6 | True | 952.8 → 952.8 | 5399.7 |
| Mitchell Edwards | 53.30 | 1 | True | 904.7 → 904.7 | 1040.1 |
| Max Gawn | 139.90 | 13 | True | 877.4 → 877.4 | 14387.4 |
| Samson Ryan | 54.20 | 1 | True | 735.2 → 735.2 | 1050.8 |
| Lachlan Smith | **0.00** | 0 | True | 579.7 → 579.7 | **546.0** |
| Rhys Stanley | 98.50 | 13 | True | 579.7 → 579.7 | 5017.0 |
| Callum Jamieson | 45.70 | 0 | True | 559.8 → 559.8 | 943.5 |
| Darcy Cameron | 109.70 | 7 | True | 565.6 → 565.6 | 6974.9 |
| Marc Pittonet | 88.80 | 5 | True | 513.3 → 513.3 | 3468.6 |
| Jacob Molier | **0.00** | 0 | True | 483.6 → 483.6 | **457.8** |
| Alex Dodson | **0.00** | 0 | True | 467.8 → 467.8 | **443.8** |
| Dante Visentini | 55.50 | 1 | True | 420.9 → 420.9 | 1100.5 |

Two facts read off this table:

1. **`v0_start` is byte-identical HEAD → FIX on all 12** — the arm-split fix does not move national
   board-consumed v0, exactly as ORDER 20B measured (0 of 668).
2. **Three of the 12 have no qualified production at all** (Smith, Molier, Dodson: `bestlvl = 0`), and
   for them `_ruc_ceiling` (`:1216`) falls back to the prior cap, so the cap **is** their `ev()`
   ceiling — 546.0, 457.8, 443.8. Even so their price does not move, because the ceiling binds only
   when `_cpv < e ≤ _v0_uncapped`, and their production leg sits **below** the ceiling. The cap is
   armed on them and never fires.

---

## HOW THE CLASSIFICATION WAS MADE

Fixed in the pre-registration, before any board was built, and applied mechanically:

- **PRIOR-DOMINATED** — his NO-CAP board value **differs** from his AFTER board value. The cap is
  load-bearing on his price.
- **PRODUCTION-LED** — his NO-CAP board value is **identical**. The cap binds only on the latent V0
  scaffold `_v0_raw`, which the board does not read for him.

It is a **measured** criterion — the difference of two built boards — not a narrative one, and it is
deliberately the one thing the owner needs to read the table correctly: **a binding cap and a cap that
moves a price are different things**, and on the national arm every one of the 12 is the first kind.

`bestlvl`, `nqual` and `in_v0curve` are printed as the *mechanism* and are never used to classify.

---

## TABLE 2 — THE 40 POOL RUCKS (headline rows; full table in `out/RUCK_CAP_TABLE.txt`)

The pool arm is where the cap is live, because pool rows are **absent** from `_V0CURVE` (`in_v0curve =
False` on all 40) and `v0_start` therefore falls back to the **capped** `_v0_raw`.

**17 of 40 are PRIOR-DOMINATED; 23 are PRODUCTION-LED.** Pool binding grew 34 → 40 under the fix.

| player | age | games | BEFORE | AFTER | NO-CAP | Δ cap | classification | channel |
|---|--:|--:|--:|--:|--:|--:|---|---|
| Liam Reidy | 26 | 7 | 328 | 291 | **322** | **+31** | PRIOR-DOMINATED | live sit-out blend |
| Coen Livingstone | 21 | 0 | 3 | 3 | **14** | +11 | PRIOR-DOMINATED | delisted scrap |
| Ivan Soldo | 30 | 66 | 3 | 3 | **14** | +11 | PRIOR-DOMINATED | delisted scrap |
| Sam Naismith | 34 | 33 | 8 | 8 | **17** | +9 | PRIOR-DOMINATED | delisted scrap |
| Tom Campbell | 35 | 58 | 8 | 8 | **17** | +9 | PRIOR-DOMINATED | delisted scrap |
| Will Verrall | 22 | 0 | 8 | 8 | **15** | +7 | PRIOR-DOMINATED | delisted scrap |
| Cameron Owen | 22 | 0 | 8 | 8 | **15** | +7 | PRIOR-DOMINATED | delisted scrap |
| Clay Tucker | 22 | 0 | 8 | 8 | **14** | +6 | PRIOR-DOMINATED | delisted scrap |
| Kaelen Bradtke | 25 | 0 | 7 | 7 | **12** | +5 | PRIOR-DOMINATED | delisted scrap |
| Flynn Riley | 22 | 1 | 232 | 233 | **232** | **−1** | PRIOR-DOMINATED | live sit-out blend |
| Alex Van Wyk | 22 | 1 | 233 | 233 | **232** | **−1** | PRIOR-DOMINATED | live sit-out blend |
| Vigo Visentini | 21 | 3 | 167 | 168 | **167** | **−1** | PRIOR-DOMINATED | live sit-out blend |
| *(5 more scrap rows: Joe Furphy +3, Darryl McDowell-White +2, Oscar McInerney +2, Brynn Teakle +1, Kieran Strachan +1)* | | | | | | | | |
| **the 23 PRODUCTION-LED**, incl. Tristan Xerri 7800, Ned Moyle 2285, Jordon Sweet 2285, Rowan Marshall 2027, Nick Madden 1766, Lloyd Meek 1300, Sam Draper 1107, Reilly O'Brien 985, Jarrod Witts 139 | | | | | | **0** | PRODUCTION-LED | — |
| **TOTAL (40)** | | | **23319** | **23476** | **23578** | **+102** | 17 prior / 23 production | |

**Every big pool ruck is production-led.** Xerri, Marshall, Sweet, Moyle, Madden, Meek, Draper,
O'Brien — the cap binds on all of their scaffolds and moves none of their prices. The entire +102 sits
on delisted remnants (+74) and four thin-record live rows (+28).

---

## TWO SURPRISES

### 1. Three live pool rucks go **DOWN** when the cap is lifted

Lifting a `min()` clamp should never lower a price. Flynn Riley 233→232, Alex Van Wyk 233→232, Vigo
Visentini 168→167. This is decomposed in `out/FALLER_DECOMP.txt` (`scripts/faller_diag.py`, the
engine's own functions on the engine's own player objects), and it is **not** rounding — it is the
**surprise damper** in `sitout_ev` (`:1968`):

```
Flynn Riley   cap=1.4   e_full = 407.39 (ceiling binds)   surprise 1.6674   lam 0.011743   blend 244.752 -> ev 245 -> v 233
Flynn Riley   cap=99    e_full = 536.29 (no bind)         surprise 2.5532   lam 0.002684   blend 243.608 -> ev 244 -> v 232
```

`lam = lam_ramp ** (1 + surprise)`, and `surprise = SUR_W·|log(e_full/anchor)|·(unresolved share)`.
Uncapping raises his production claim from 407 to 536, which the engine reads as a **larger unearned
re-rate**, so it collapses the weight `lam` on the production leg from 0.0117 to 0.0027 and leans the
blend further onto the entry anchor (242.82). The anchor is *below* the blended price, so the price
falls. This is the design behaving as specified — the blend is deliberately non-monotone in the
production claim for a thin record — but the owner should know that **for a pool ruck with almost no
games at pace, a higher prior can lower his price.** The control row proves the sign flips with
evidence: Liam Reidy has `lam_ramp = 0.6406` (games at pace), his damper barely bites, and the higher
claim wins: +31.

### 2. 13 of the 17 movers are delisted players

`ev = round(0.02 · v0_start)` for a delisted row (`:2230`). The cap sits directly on `v0_start` for
pool rows, so uncapping roughly doubles the **scrap remnant** — Coen Livingstone 3→14, Ivan Soldo
3→14, Sam Naismith 8→17. These are not keeper prices; they are the delisted remnant. Reported so the
+102 is not read as +102 of live board value. It is **+74 of scrap and +28 of live**.

---

## PREDICTION LEDGER

| # | prediction | outcome |
|---|---|---|
| P1 | HEAD board rebuilds to `94f1fec5…` | **TRUE** — exact |
| P2 | FIX board rebuilds to `1dbd1480…` | **TRUE** — exact |
| P3 | gate-mode `RL_RUC_PRIOR_CAP=99` HALTs on the frozen-v0surf signature | **TRUE** — signature `2dff9ca1…` not in the pickle; the engine died rather than re-fit |
| P4 | the D14 surface is cap-independent under the shipped lens | **TRUE** — refit@1.4 reproduces the committed pin `fbc5b393…`; refit@99 pairs value-for-value to both frozen entries |
| P5 | the dev lane + merged pickle at cap 1.4 still gives `1dbd1480…` | **TRUE** — exact |
| P6 | ≥ 8 of the 12 national rucks show a cap delta of exactly zero | **TRUE, and stronger — 12 of 12** |
| P7 | at most 4 national rucks move on cap lift | **TRUE — 0 moved** |
| P8 | ≥ 25 of the 40 binding pool rucks move | **BREACHED — 17 of 40** |
| P9 | board total NO-CAP ≥ FIX, strictly | **TRUE — +102** (but see Surprise 1: three individual rows fall; the prediction was about the total and did not anticipate row-level non-monotonicity) |
| P10 | zero NON-ruck rows move | **TRUE — 0 of 1002** |
| P11 | the ceiling moves on 0 of 71 ruck rows HEAD→FIX | **TRUE — 0 of 71** |
| P12 | the six already-binding are not ORDER 20B's six | **TRUE** — De Koning, Edwards, Gawn, Jamieson, Cameron, Visentini |

**P8 BREACHED, owned.** I predicted the pool arm would move broadly because pool `v0_start` reads the
capped `_v0_raw`. It does — but 23 of the 40 are established producers whose price is set by the
production path with `v0_start` entering only as a floor and a blend weight that a real record has
already faded out. The reasoning behind P8 confused "the cap reaches his `v0_start`" with "the cap
reaches his price". That is the same confusion the classification exists to expose, and I made it in
my own pre-registration.

**One self-inflicted error, corrected before filing.** The first run of `ruck_cap_table.py` reported
**17 phantom NON-RUCK movers** and printed `*** P10 BREACHED ***`. The board writes `fut` as a share
vector `[['RUCK', 1.0]]`, not a string, and my comparison against `'RUCK'` failed on all 17. The
check now tests membership of the **engine's own** n=71 real-RUCK set from `engine_probe.py` and only
prints the `fut` label; P10 holds cleanly. The bug is recorded rather than quietly fixed.

---

## HOW THE CAP WAS NEUTRALISED, AND THE PROOF THAT THE DIAL IS READ

`RUC_PRIOR_CAP = float(os.environ.get('RL_RUC_PRIOR_CAP','1.4'))` — `_merged_recover.py:1157`. It is
both a live env dial and a `data/model_config.json` manifest var.

**The dial is demonstrably read.** `RL_RUC_PRIOR_CAP` is a member of `_V0SURF_GATES` (`:1323`), which
feeds `_v0surf_sig`. Moving it to 99 in gate mode produced signature `2dff9ca182110c050c4e4f72a21d2aed`,
which is not in `data/v0surf.pkl`, and the build **HALTed** (`:1416`) rather than silently re-fitting.
That halt is the proof: a dial the engine did not read could not have changed the signature.

Neutralising it therefore took four declared steps, each measured rather than asserted:

1. **The frozen surface is cap-independent** — `scripts/v0surf_fit_one.py` drives the *committed*
   refit entry point (`session_2026-07-18/legf6/scripts/refit_v0surf.py`, imported) once at cap 1.4 and
   once at cap 99, one process each. `--verify` at cap 1.4 reproduces the committed pin
   `fbc5b39387b2b135284a2e157f46c810` exactly on this box.
2. **`scripts/v0surf_merge.py`** pairs the cap-99 surfaces to the cap-1.4 surfaces **by value** and
   requires exact equality. Both pair, value-for-value:
   `2dff9ca1… ≡ 6ef67f07…` and `49d0f5ed… ≡ 41af7326…`. A single differing float would have HALTed.
3. It then writes a merged pickle = the **original frozen entries** plus **those same objects re-keyed**
   under the cap-99 signatures. The no-cap board reads the *shipped* surfaces, not the refit's arrays.
4. **The lane is proved inert before it is used**: `build_board_rc.sh` at the shipped cap 1.4 with the
   merged pickle reproduces `1dbd1480a34c7823f330273211cbb76a` byte-for-byte — the gate-mode FIX board.
   Only then was the cap-99 board built.

The one cost: the no-cap arm runs **dev-shell** (no `RL_CONFIG_MODE`) rather than gate mode, because
`config_manifest.enforce` rejects `RL_V0SURF_PKL` — it is not a manifest var and must not become one in
a measurement. Step 4 is what pays for that: the same lane, same pickle, shipped cap, identical board.

---

## THE FOUR BOARDS

| board | md5 | how |
|---|---|---|
| BEFORE (HEAD, gate) | `94f1fec59f99c59d5890d5975c79fa9b` | `run_board.sh HEAD_gate` |
| AFTER (FIX, gate) | `1dbd1480a34c7823f330273211cbb76a` | `run_board.sh FIX_gate` |
| lane control (FIX, dev, merged pickle, cap 1.4) | `1dbd1480a34c7823f330273211cbb76a` | `run_board.sh FIX_dev` |
| **NO-CAP (FIX, dev, merged pickle, cap 99)** | **`48c23615376bdab34d618de5c6083fbe`** | `run_board.sh FIX_dev_cap99` |

Cross-check: `engine_probe.py` run at cap 99 (`run_probe_nocap.sh`) reproduces the no-cap board's
per-row values independently — the same **17** rows move, with the same deltas.

---

## REPRODUCTION

```bash
export PATH="/root/rl_venv312/bin:$PATH"
cd <this worktree>
D=docs/evidence/ruck_cap_2026-08-12/scripts
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad

bash $D/stage_trees.sh                 # HEAD + FIX scratchpad copies (checkout untouched)
bash $D/stage_lens_basis.sh            # the one declared input the refit lane needs
bash $D/run_board.sh HEAD_gate         # -> 94f1fec5…   (~2m)
bash $D/run_board.sh FIX_gate          # -> 1dbd1480…   (~2m)
bash $D/run_board.sh FIX_gate_cap99    # -> HALT (P3; expected, exit 1)
bash $D/run_refit_verify.sh FIX 1.4    # -> refit REPRODUCES the pin  (~2.5m)
bash $D/run_capkeys.sh                 # two refits + the merge       (~5m)
bash $D/run_board.sh FIX_dev           # -> 1dbd1480…  (lane control) (~2m)
bash $D/run_board.sh FIX_dev_cap99     # -> 48c23615…  (the arm)      (~2m)
bash $D/run_probe.sh HEAD $SP/probe_HEAD.json          # ~1.5m
bash $D/run_probe.sh FIX  $SP/probe_FIX.json           # ~1.5m
bash $D/run_probe_nocap.sh $SP/probe_FIX_nocap.json    # ~1.5m
bash $D/run_extra.sh HEAD $SP/extra_HEAD.json          # ~1.2m
bash $D/run_extra.sh FIX  $SP/extra_FIX.json           # ~1.2m
bash $D/run_faller.sh > docs/evidence/ruck_cap_2026-08-12/out/FALLER_DECOMP.txt
python3 $D/ruck_cap_table.py $SP docs/evidence/ruck_cap_2026-08-12/out/RUCK_CAP_TABLE
```

**Reused from ORDER 20B, byte-identical** (`docs/evidence/par_adoption_2026-08-12/scripts/`):
`stage_trees.sh`, `build_board_o20b.sh`, `engine_probe.py`, `run_probe.sh`. Everything else is a thin
adapter or a reader, and `build_board_rc.sh` states its four-line diff from `build_board_o20b.sh` in
its own header.

## OUTPUTS

| file | what |
|---|---|
| `out/RUCK_CAP_TABLE.txt` | both tables in full, board totals, every mover, the cross-checks |
| `out/RUCK_CAP_TABLE.json` | the same, machine-readable |
| `out/FALLER_DECOMP.txt` | the term-by-term decomposition of the three rows that fall |

## WHAT THIS DOES NOT SETTLE

Whether the cap should be **re-derived** alongside the par fix. This packet answers only what the owner
asked — the three numbers per player — and it says the national half of ORDER 20B's P9 breach has **no
price consequence at all** at today's board. It does not say the scaffold is fine: `_v0_uncapped` still
rises through a stationary ceiling on 12 national rucks, and if a future bake ever re-fits the D14
surface from `_v0_raw` (the `RL_V0_LENS=0` lane, or a re-bake through the declared refit), that latent
cut becomes a live one. That is a decision, and it is the owner's.
