# LANDING VERIFICATION — ORDER 23, THE POOL UPDATE

Branch `land/pool-update`, cut from `origin/main` `27d9484`. Issue #334, owner rulings filed at
comment **5262928754** (2026-08-12). Pre-registration `PREREG_ORDER23.md`, committed at `7d6043d`
**before any board was built or any level measured on this branch**.

**NOT MERGED. Branch + PR + STOP. Only the owner's word merges.**

---

# 1. THE HEADLINE, IN FOUR NUMBERS

| | |
|---|---|
| **the landed board** | **`665311ca72576df6ff0bbf6dfd007739`** — 746,043 → **753,837** (+7,794, **+1.045%**), **117 rows moved**, 96 up, 21 down |
| **the target, re-measured fresh arm-split, every round** | **`0.9900060981`** — one distinct value across all five rounds |
| **the pool aggregate** | ORDER 22, capped: **1.038853** → ORDER 23, uncapped: **0.999535** |
| **ND 1-64** | **620,877 → 620,877**, rows moved **0**, national `v0` delta **0 EXACTLY** |

---

# 2. TASK 1 — THE FINAL ITERATION, ALL NINE PATHWAYS REPRICEABLE

## 2.1 THE FINAL LEVELS, AND THE DELTA VS THE PACKET

The owner has not seen these numbers. **Every level here is the outcome of the derivation, not a
ratio of an old price** — at the fixed point the level that produced the matrix has washed out.

| division | live (N43 signed) | ORDER 22 packet | **ORDER 23 FINAL** | Δ vs packet | % |
|---|---:|---:|---:|---:|---:|
| SSP | 252.8 | 320 | **315** | −5 | **−1.56%** |
| MSD | 286.8 | 379 | **374** | −5 | **−1.32%** |
| IRE | 133.4 | 107 | **106** | −1 | **−0.93%** |
| PDA | 194.3 | 191 | **188** | −3 | **−1.57%** |
| PDN | 123.0 | 97 | **96** | −1 | **−1.03%** |
| PDS | 145.0 | 57 | **56** | −1 | **−1.75%** |
| UNR | 103.7 | 66 | **66** | 0 | **0.00%** |
| RD MID | 294.8 | 289 | **289** | 0 | **0.00%** |
| RD SD | 246.9 | 246 | **245** | −1 | **−0.41%** |
| RD SF | 231.5 | 217 | **217** | 0 | **0.00%** |
| RD KPD | 300.3 | 370 | **370** | 0 | **0.00%** |
| RD KPF | 216.0 | 209 | **209** | 0 | **0.00%** |
| RD RUCK | 282.5 | 258 | **259** | **+1** | **+0.39%** |
| **ND>64** | **185 (capped; 266.1 stored)** | **274 wanted, BLOCKED at 185** | **298 — UNCAPPED AND PRICED** | **+113 vs what shipped** | **+61.1%** |

**Read this table as the owner asked it to be read.** Outside ND>64 the whole re-run moves the book
by at most **1.75%**, and every one of those moves is the same effect: uncapping ND>64 raises the
pool's total entry price, which drops the whole-pool aggregate the K=15 shrinkage borrows from
(1.0389 → ≈1.000), which pulls every pathway's shrunk λ down by `(1−w)×0.038` — **−0.08% at RD's
w=0.979, −1.6% at PDS's w=0.583**. It is one cause, not thirteen.

**ND>64 does not land on the packet's 274.** At 274 the pathway still returned **+3.6%** above
target, because raising its level raises its own realised value too — the `_ruc_prior_cap` puts
**6 of its 9 rucks on the cap** at 298 where **0 of 9** were on it at 185, and a bound row's `v0` is
exactly `1.400 × the signed level`. Two more rounds carried it to **298**, where it returns
**0.999416** of target.

**THE FIXED POINT IS EXACT, and this is the cleanest statement of convergence available.** Applying
the update rule to the final levels returns the final levels — all **fourteen** of them:

    SSP 314.80→315 · MSD 373.87→374 · IRE 105.74→106 · PDA 187.95→188 · PDN 95.87→96 · PDS 55.87→56
    UNR 65.70→66 · MID 288.89→289 · SD 245.37→245 · SF 216.62→217 · KPD 370.21→370 · KPF 208.54→209
    RUCK 258.88→259 · ND65+ 297.83→298

## 2.2 CONVERGENCE

**Declared tolerance: 1.0% relative on every pathway's shrunk λ. Declared cap: 8 further rounds.
Four were run. All nine pathways were inside tolerance from round G2 onward.**

| pathway | F1 (packet) | G1 | G2 | G3 | **G4 = FINAL** | \|λ−1\| |
|---|---:|---:|---:|---:|---:|---:|
| RD | 1.000254 | 0.999428 | 0.999761 | 0.999784 | **0.999773** | 0.023% |
| SSP | 1.000626 | 0.991512 | 0.995305 | 1.003345 | **0.999358** | 0.064% |
| MSD | 0.999618 | 0.992285 | 0.996023 | 1.001558 | **0.999642** | 0.036% |
| IRE | 0.998832 | 0.991791 | 0.997458 | 0.997701 | **0.997586** | 0.241% |
| PDA | 0.998344 | 0.990388 | 0.996316 | 0.999883 | **0.999758** | 0.024% |
| PDN | 1.001999 | 0.993291 | 0.998479 | 0.998782 | **0.998638** | 0.136% |
| PDS | 1.004861 | 0.990785 | 0.997403 | 0.997890 | **0.997660** | 0.234% |
| UNR | 1.003481 | 0.996634 | 0.995374 | 0.995613 | **0.995499** | 0.450% |
| **ND>64** | **1.479714** | 1.068397 | 1.001906 | 0.999491 | **0.999430** | **0.057%** |
| **ALL POOL (raw)** | **1.038853** | 1.005070 | 0.998919 | 1.000089 | **0.999535** | 0.047% |

**And the RAW λ is now inside 1% on all nine too — worst 0.553% (UNR)**, which ORDER 22 could not
achieve on a single thin pathway. The packet proved the raw residual was **an identity**, not slack:
`raw = (shrunk − (1−w)·pool_agg)/w`, so every pathway's raw λ is pinned by the pool aggregate, and the
pool aggregate was held above 1 by the one blocked pathway. **Remove the block and the identity
collapses to nothing.** Predicted-vs-measured raw λ at the final round agrees to **≤1.11e-16** on all
nine. And the two aggregates that ORDER 22 measured 4.2 percentage points apart are now the same
number to three decimals:

| | ORDER 22 (capped) | **ORDER 23 (uncapped)** |
|---|---:|---:|
| pool aggregate INCLUDING ND>64 | 1.038853 | **0.999535** |
| pool aggregate EXCLUDING ND>64 | 0.996912 | **0.999552** |

The three quantisation-limited pathways are declared rather than polished: at **UNR 66** one integer
step is **1.52%**, at **PDS 56** it is **1.79%**, at **IRE 106** it is **0.94%**. Their residuals
(0.45% / 0.23% / 0.24%) are all **smaller than one step of the storage the engine has**, so they
cannot be closed further without changing how levels are stored.

## 2.3 THE OTHER MEASUREMENTS AT THE FIXED POINT

- **Reconciliation** (entry-weighted in BOTH layers, tolerance 1e-9 relative): **worst residual
  2.23e-16** across all nine pathways. Six read exactly 0.00e+00.
- **Layer 2**: **13 of 54** cells reach n≥20 and derive on their own outcomes — the same split the
  packet pre-registered (RD 6, ND>64 3, MSD 2, IRE 1, UNR 1). Thin cells borrow the whole-pool
  positional shape at K=10; the unsampled remainder is its own residual group; every pathway is
  renormalised after borrowing.
- **U, mean-preserving**: pathways whose post-redistribution entry-weighted mean is not exactly
  **1.0000000000**: **0**. (RD 1.206327 · ND>64 1.368670 · IRE 1.337969 · UNR 1.504054 ·
  PDA 1.614437 · PDS 1.415978 · MSD 3.095901 · PDN 2.095600 · SSP 1.200096 · ALL POOL 1.252214.)
- **Both headline metrics, neither a target**: at the fixed point every pathway's career profile sits
  on the target while year-4/year-0 does not — MSD reads **0.871** at year four against a career
  profile of **0.990**, UNR reads **2.410**. **YEAR 4 IS NOT A TARGET** and nothing here aimed at it.

---

# 3. THE CONTROLS — RUN FIRST, ALL PASSED

| control | result |
|---|---|
| **C1** the **unmodified** landing tree rebuilds the live board | **`1dbd1480a34c7823f330273211cbb76a` BYTE-IDENTICAL** — had this failed the act would have HALTED here |
| **C2** ORDER 22's own staged recipe, re-run from this branch | **`21055b901312f76a8f0b17d362932130` BYTE-IDENTICAL** to the packet's FINAL board |
| **C3** ORDER 21's VARIANT A (H retirement only) | **`452623adeb9aaed115d883dbe6b0239c` BYTE-IDENTICAL** |
| **C4** `harness_armsplit(split=False)` reproduces the pinned harness | value-for-value on all eligible rows, asserted inside every derivation round |
| **C5** the landed tree's board == task-1's final staged board | **`665311ca…` BYTE-IDENTICAL**, and reproduced on a **second independent build** |

**C2 matters more than it looks.** It says this seat's staging apparatus reproduces the previous
seat's published board exactly, so the deltas in §2.1 are a measurement of the owner's amendment and
not of a changed harness.

---

# 4. THE BOARD, REBUILT DETERMINISTICALLY

The landed board was built from this branch with **`nopatch nolevels` and no manifest override at
all** — shipped defaults only, because the defaults *are* the configuration now:

```
  ref: HEAD -> 1c11205
  engine_head: 72e40e94  curve_artifact: 07b7109f
  OK 665311ca72576df6ff0bbf6dfd007739  -> board_LANDED.json
  (rebuilt) OK 665311ca72576df6ff0bbf6dfd007739  -> board_LANDED2.json
```

| board | md5 | total | Δ vs LIVE | % | moved | up | down |
|---|---|---:|---:|---:|---:|---:|---:|
| LIVE | `1dbd1480a34c7823f330273211cbb76a` | 746,043 | — | — | — | — | — |
| lever 1 — H retirement only | `452623adeb9aaed115d883dbe6b0239c` | 748,355 | +2,312 | +0.310% | 48 | 48 | 0 |
| lever 2 — + the derived retention | `b5741109af73706b9616ff5ab93eba55` | 751,679 | +5,636 | +0.755% | 82 | 74 | 8 |
| **lever 3 — + the repricing (LANDED)** | **`665311ca72576df6ff0bbf6dfd007739`** | **753,837** | **+7,794** | **+1.045%** | **117** | **96** | **21** |

**Lever totals across every moved row: H retirement +2,303 · retention +3,308 · repricing +2,183.**
**The act's headline change is still the smallest of its three levers** — the packet's finding,
unchanged by the amendment. Uncapping ND>64 grows the repricing lever from **+1,989 to +2,158**
board-wide (+169), and every point of that growth is the ND>64 pathway; the retention lever remains
the largest single cause of the board move.

## By pathway

| pathway | rows | moved | LIVE | H only | + retention | **LANDED** | **Δ** | **%** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **ND 1-64** | **561** | **0** | **620,877** | **620,877** | **620,877** | **620,877** | **0** | **+0.000%** |
| RD | 66 | 22 | 45,874 | 46,148 | 46,304 | 46,237 | +363 | +0.791% |
| MSD | 63 | 34 | 36,089 | 36,962 | 39,404 | 41,483 | **+5,394** | **+14.946%** |
| **ND>64** | 28 | **13** | 18,828 | 18,887 | 18,945 | **19,273** | **+445** | **+2.364%** |
| SSP | 28 | 14 | 11,535 | 12,237 | 12,240 | 12,546 | +1,011 | +8.765% |
| PDA | 15 | 5 | 8,103 | 8,159 | 8,263 | 8,249 | +146 | +1.802% |
| PDN | 16 | 10 | 2,729 | 2,906 | 3,325 | 3,142 | +413 | +15.134% |
| IRE | 14 | 10 | 712 | 803 | 950 | 823 | +111 | +15.590% |
| **UNR** | 13 | 9 | 1,296 | 1,376 | 1,371 | **1,207** | **−89** | **−6.867%** |

ND>64 moved **4** rows for **+117** under the packet's capped configuration. Uncapped it moves **13**
rows for **+445** — still a small pathway on the live board, which is exactly the owner's stated
ground for amending the law (*"it's not going to impact many players anymore, only historical ones"*).

---

# 5. THE SEPARATION ASSERTIONS — ASSERTED AND PRINTED

| check | result |
|---|---|
| **ND 1-64 board rows moved**, every lever and the landed board | **0** |
| ANY non-pool board row moved, every lever | **0** |
| **ND 1-64 board value**, LIVE and LANDED | **620,877 → 620,877** |
| **national records repriced on ANY year of the 24-year walk-forward** (1,443 records) | **0** |
| **national records whose `v0` moved**, SHIP vs FINAL | **0 — EXACTLY zero, not merely small** |
| the calibration target across all five rounds | **0.9900060981 at every round — 1 distinct value** |

**1,134 records reprice on the walk-forward under the final configuration and every single one is a
pool record.** The instrument is plainly sensitive; the national arm does not move by one float bit.

`_ruc_prior_cap`, checked because it is the only route by which a signed pool level reaches
`v0_start` at all: it binds on **127 of 140** pool ruck rows. A bound row's `v0` is exactly
`1.400 × the signed level`, before and after (`flynn-riley`: level 286 → 374, v0 400.4 → 523.6).

---

# 6. THE INSTRUMENTS — 15 READINGS, EVERY MARGIN BESIDE THE 14% CHARGE

`margin vs 14% = 14% − (year-0 → year-1 appreciation)`. **A negative margin is an arbitrage.**

## All-arm DECIDING instrument (`noarb_table_allarm.py`)

| window | variant | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | apprec 0→1 | **margin vs 14%** | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PRIMARY n=2212 | SHIP | 1.0000 | 0.7767 | 0.9581 | 1.0608 | 1.1231 | 1.1047 | −22.33% | **+36.33%** | no arb |
| PRIMARY | ORDER 22 FINAL | 1.0000 | 0.7988 | 0.9672 | 1.0671 | 1.1300 | 1.1104 | −20.12% | **+34.12%** | no arb |
| PRIMARY | **ORDER 23 LANDED** | 1.0000 | **0.8028** | 0.9694 | 1.0675 | 1.1299 | 1.1100 | −19.72% | **+33.72%** | **no arb** |
| MODERN n=540 | SHIP | 1.0000 | 0.8007 | 0.9084 | 0.9717 | 0.9734 | 1.0309 | −19.93% | **+33.93%** | no arb |
| MODERN | ORDER 22 FINAL | 1.0000 | 0.8180 | 0.9184 | 0.9752 | 0.9788 | 1.0362 | −18.20% | **+32.20%** | no arb |
| MODERN | **ORDER 23 LANDED** | 1.0000 | **0.8202** | 0.9194 | 0.9754 | 0.9788 | 1.0361 | −17.98% | **+31.98%** | **no arb** |

## Legacy retained instrument (`noarb_table_338.py`, UNMODIFIED — md5 computed at run)

| group | SHIP | ORDER 22 | **ORDER 23** | apprec 0→1 | **margin vs 14%** | verdict |
|---|---:|---:|---:|---:|---:|---|
| ALL picks 1-64 | 1.0730 | 1.0730 | **1.0730** | +7.30% | **+6.70% → +6.70%** | no arb |
| picks 1-20 | 1.1218 | 1.1218 | **1.1218** | +12.18% | **+1.82% → +1.82%** | no arb |
| picks 21-64 | 0.9994 | 0.9995 | **0.9996** | −0.04% | **+14.06% → +14.04%** | no arb |

> **ARBITRAGES OPENED BY THE LANDED CONFIGURATION: 0 of 15 readings.** The legacy 1-64 aggregate does
> not move at all (**0.00 points**). The picks 21-64 slice moves by **0.02 points**, and
> `separation_check.py` named the single row responsible back in ORDER 21: **`daniel-butler`**, a POOL
> row admitted to a population selected by *stored* pick number — the documented crosser, not a
> national reprice.

**Instrument md5s are COMPUTED at run and never hardcoded:** `noarb_table_338.py`
`0f8220351c64c56ccfa90c60edcdfa5f`, `noarb_table_allarm.py` `3f9124de638d5ed30792dbdffef591b8`,
`harness_pvc_REPINNED_pass3.py` `f2c81da18e02e8a6003ce011c4b8ada3`, `harness_armsplit.py`
`5c68354979de09de743fe89c7e00776e` — each asserted equal to `origin/main`'s own copy.

---

# 7. THE PINS RESTAMPED — THE MOVED SET ASSERTED BEFORE WRITING

`o23_restamp.py` enumerates every non-note key of `data/expected_boot.json`, prints moved and unmoved
alike, and **asserts the moved set is exactly `{board, config, engine_head, rl_model}`** before it
will write.

| key | from | to |
|---|---|---|
| `board` | `1dbd1480a34c7823f330273211cbb76a` | `665311ca72576df6ff0bbf6dfd007739` |
| `config` | `cd38fb00…` | `bf012105…` (H_POOLSIT / H_UNION → 1.0) |
| `engine_head` | `a8071af4dd86b7d8d3d9d916ae75f787` | `72e40e945bc06bdb6f3bf94fc8ef89c9` |
| `rl_model` | `de7ce41659adeda756f4fd1a2caaf172` | `e5eb5e4405c09eebef45a9db89f014bc` |

**Unmoved, printed key by key:** `store` (`d9a24282…`), **`fv` (`2621b56a…` — no
`engine/forward_valuation` source is touched)**, `band`, `q97m`, `v0surf`, `peak_model`,
`pvc_snapshot`, `bust_prior`, `register`, `balanced_board_md5`, `as_of_round`, `release_version`,
`register_note`, `tag`.

Three further identity carriers move in the same commit, per the ORDER 9 / ORDER 20C precedent:
`data/rl_build/rl_app_data.json` and `engine/rl_after/rl_app_data.json` (the landed board),
`engine/rl_after/rl_app_data.json.srcmd5` (`own_md5`), and
`engine/rl_after/rl_app_data.provenance.json` (`config_manifest_identity`, `rl_model_md5`; its
`fv_identity` is asserted UNCHANGED).

**BOOT GUARD ON THE LANDED TREE: PASS**, both halves (`boot_guard_landed.txt`) — forward-valuation
provenance (checkout + loaded-path) and `assert_boot` over store / register / config / board /
`rl_model` / the five fitted artifacts / the three load-path resolutions.

---

# 8. THE UNTOUCHED ARTIFACTS — ASSERTED AS NUMBERS, NOT CLAIMED

Every value computed from the file on disk at exit and compared against `origin/main`'s own copy
(`untouched_artifacts.txt`). **`SCOPE GUARDS: ALL HELD.`**

| artifact | verdict |
|---|---|
| **store** `engine/rl_after/rl_model_data.json` `d9a24282…` | UNMOVED |
| **pickles** `v0surf` · `q97m` · `peak_model_v4` | UNMOVED — **no pickle was regenerated** |
| `pvc_snapshot.json` · `bust_prior_table.json` | UNMOVED |
| **band pickle** `/home/claude/cm_400.pkl` `34faa865…` | == its pin, never written |
| **both instruments + both harnesses** | UNMOVED |
| `o21_patch.py` (the carried patcher) `b2c01de9…` | UNMOVED — carried, never modified |
| `pool_retention_derive.py` (ORDER 21) `6df38acb…` | UNMOVED — read, never written |
| `LTI_REGISTER.md` · `season_state.json` · `rl_export.py` | UNMOVED |

**The national side of the curve artifact did not move.** `pvc_curve_v2.json`'s `curve`, `curve_md5`,
`pool_value`, `domain`, `split`, `numeraire_pin1_3000`, `r104_9_strict_descent`, `stamp`, `source`,
`derived_from`, `pin` and `construction` are byte-identical to `origin/main`. **The only top-level key
that moved is `pool_levels`** — asserted, not asserted-about.

**The sitter lever is asserted MOVED**, which is the inverse of ORDER 20C's guard because this is the
act that owns it: manifest `RL_H_POOLSIT` = `1.0` and `RL_H_UNION` = `1.0`, the engine's own code
defaults = `1.0`, `H_MATNONRD` untouched at 1.0, the `RL_ITEM_H` kill-switch untouched, and the
composed `_h_cut` cell logic untouched.

---

# 9. THE N43 RE-SIGNATURE, AND THE SELF-TEST

The packet's **flag (d)**: `one_source_selftest.py` carries the levels as literals and checks the
artifact against them, *"so that an edited level would agree with itself and pass"*. **Adoption
requires the owner's signature in code, by design.** This act re-signs them, keeps the selftest's
structure, and **strengthens** the one law it had to change: the ND65+ check now asserts the
retirement as well as the value — the live `cap_against_curve_pick` key must be **GONE** and the
dated historical key must be **present**, so a silent restoration of the cap goes red.

Run on the landed tree (`selftest_landed.txt`), section (10) is fully green, including:

```
  PASS #326/ORDER23 ND65+ prices at its DERIVED level 298.0; the min-against-curve[64] cap is
       REMOVED (owner ruling 2026-08-12) and preserved only as dated history
  PASS #326 the engine's resolved pool levels == the signed table (ND65+ = 298.0 DERIVED,
       curve[64]=185 NOT applied -> 298)
  PASS #326 ui/release_pick_curve.json mirrors the artifact's pool_levels verbatim
  PASS #326 currency end-to-end (ND65+): Sam Switkowski ships at 15 == floor_frac(9)=0.05 x signed
       level 298 x ITEM B age factor = 15
```

**The whole self-test ends `SELF-TEST FAILED: 2 check(s)` — and both are PRE-EXISTING and are not
this act's.** A CONTROL RUN ON `origin/main` FAILS THE SAME TWO AND NO OTHERS
(`selftest_origin_main_control.txt`):

```
  - GUARD 1: rl_app_data.json is read-only (mode 644)
  - GUARD 1: s4_matrix.json is read-only (mode 644)
```

Those are file-mode checks about a bake-time `chmod`, which a plain git checkout does not reproduce.
**Landed tree: 2 failures. origin/main: the same 2 failures. Net new failures from this act: 0.**

---

# 10. THE BOOK RE-SEALED (isolated commit)

| book | vs live board `1dbd1480` | vs landed board `665311ca` |
|---|---:|---:|
| as committed on `origin/main` | **0** mismatches | **117** mismatches |
| re-sealed on the landed tree | — | **0** mismatches |

Rebuilt by `engine/rl_after/s4_matrix_M1v7.py` in a **scratchpad copy** of the landed tree (the
checkout is never built in), after asserting that copy carried the landed board, the unmoved store
and the unmoved `fv`. The builder's own gate passed in the same run: `BOOK PARITY GATE PASS: all 802
shared board players' present value == round(book cur / 1.0524)`.

`s4_matrix.json`'s md5 carries no identity information — its top-level keys are Python `id()` values —
so it is non-byte-reproducible by construction, is deliberately not pinned, and the boot guard does
not assert it (ORDER 20C's finding, carried).

---

# 11. THE MOVERS LEDGER

`docs/ledgers/POOL_UPDATE_MOVERS_2026-08-12.md` + `.json` — **117 rows**, every one named,
before → after → delta → pct, **with the three-lever decomposition on every row** (not only on the
35 movers ≥50 points the order requires it for). **The lever-sum identity — H + retention +
repricing == total delta — is asserted on all 117 rows at write time; the writer halts otherwise.**

The five largest, with their attribution:

| player | pathway | pos | LIVE | H only | + retention | **LANDED** | **Δ** | lever H | lever retention | lever repricing |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mani Liddy | MSD | MID | 128 | 128 | 785 | **1025** | **+897** | 0 | +657 | +240 |
| Nicholas Martin | SSP | SF | 2822 | 3509 | 3518 | **3520** | **+698** | +687 | +9 | +2 |
| Robert Hansen | MSD | SF | 80 | 80 | 509 | **650** | **+570** | 0 | +429 | +141 |
| Flynn Young | MSD | SF | 128 | 128 | 386 | **502** | **+374** | 0 | +258 | +116 |
| James Blanck | MSD | KPD | 60 | 60 | 333 | **431** | **+371** | 0 | +273 | +98 |

**The finding the packet reported survives the amendment: the biggest movers are all MSD, and their
moves are dominated by the RETENTION lever, not the repricing.** The two largest ND>64 movers are
**Aidan Johnson** (KPF, 80 → 200, of which **+76 is the repricing**) and **Logan Smith** (RUCK,
91 → 185, **+70 repricing**) — the uncapping showing up as the owner would expect it to, on a handful
of rows.

**Declared, not reconciled away:** the ledger's lever columns sum to +2,303 / +3,308 / +2,183 while
the board-wide lever deltas are +2,312 / +3,324 / +2,158. The columns are summed over rows that move
in the LANDED board, and **two rows move under an intermediate lever and land back on exactly their
live value**, so they carry no total delta and are not ledger rows: **`jacob-moss`** (36 → 45 → 57 →
**36**) and **`jayden-nguyen`** (452 → 452 → 456 → **452**). They account for the entire +9 gap in the
H column. Named here rather than smoothed.

---

# 12. PRE-REGISTRATION SCORING — 25 PREDICTIONS

| # | prediction | measured | result |
|---|---|---|---|
| C1 | unmodified tree reproduces `1dbd1480` | byte-identical | ✓ |
| C2 | ORDER 22's recipe reproduces `21055b90` | byte-identical | ✓ |
| C3 | armsplit `split=False` control passes every round | asserted, every round | ✓ |
| C4 | landed board == task-1 final board, and reproduces | `665311ca` twice | ✓ |
| I1 | converges on all nine within 4 further rounds | **all nine inside 1.0% from round 2 of 4** | ✓ |
| I2 | target identical to the last digit at every round | `0.9900060981`, 1 distinct value | ✓ |
| I3 | ND>64 final level above 274, in [270, 305] | **298** | ✓ |
| I4 | every other level moves DOWN, by ≤2.0% | magnitude held (worst **1.75%**); **direction BREACHED** — 7 down, 5 unchanged, and **RD:RUCK 258 → 259, +0.39%** | **BREACH** — the shrinkage pull is a *net* effect and RUCK's own cell λ pushed back harder than the aggregate pulled. Owned; the prediction was too strong in a direction I had no need to claim. |
| I5 | RD positional levels move ≤1 integer unit | SD −1, RUCK +1, four unchanged | ✓ |
| I6 | pool aggregate λ within 0.5% of 1.000 | **0.999535** (0.047%) | ✓ |
| I7 | raw λ within 1.0% on all nine | worst **0.553%** (UNR) | ✓ |
| I8 | reconciliation worst residual ≤1e-9, in fact <1e-12 | **2.23e-16** | ✓ |
| I9 | U mean-preserving, 0 pathways off | **0** | ✓ |
| S1 | ND 1-64 board rows moved = 0 | 0, every lever | ✓ |
| S2 | ND 1-64 board value 620,877 unchanged | 620,877 → 620,877 | ✓ |
| S3 | national records repriced on the walk-forward = 0 | 0 | ✓ |
| S4 | national `v0` delta = 0 EXACTLY | 0 | ✓ |
| S5 | any non-pool board row moved = 0 | 0 | ✓ |
| B1 | landed total above the packet's 753,668 | **753,837** | ✓ |
| B2 | rows moved in (109, 160) | **117** | ✓ |
| B3 | ND>64 board value rises by more than +117 | **+445** | ✓ |
| L1 | one ledger row per mover, decomposition, columns sum | 117 rows, decomposition on all, identity asserted | ✓ |
| P1 | pins moved == exactly {board, config, engine_head, rl_model}; `fv` does not move | exactly that, asserted before writing | ✓ |
| P2 | store unmoved, no pickle regenerated | asserted by computed md5 against `origin/main` | ✓ |
| P3 | boot guard passes on the landed tree | PASS, both halves | ✓ |
| P4 | F2 parity >0 → 0, isolated commit | 117 → 0 | ✓ |
| P5 | instruments untouched, md5 computed not hardcoded | UNMOVED, computed | ✓ |
| A1 | 0 of 20 readings open an arbitrage | **0 arbitrages — but 15 readings, not 20** | **PARTIAL** — I ran the three configurations this act is about (SHIP, ORDER 22 FINAL, ORDER 23 LANDED); the packet's 20 included variants (ORDER 21 staged, O1-on) that are not this landing. The substance held; the count did not. |
| A2 | legacy 1-64 margin moves ≤0.05 points | **0.00** points | ✓ |
| N1 | N43 re-signed, structure kept, ND65+ check rewritten | done, and the check strengthened to assert the retirement | ✓ |

**SCORE: 27 held, 1 breached (I4), 1 partial (A1).** The breach is a direction claim I did not need to
make and did not measure before making; it is listed as a breach, not re-labelled as a discovery.

---

# 13. WHAT REMAINS THE OWNER'S, AND IS CARRIED UNRESOLVED

The packet handed back eight items. **Two of them are closed by this act** — the ND65+ cap (d2) by the
owner's amendment, and the N43 re-signature (d4) by this landing. **Six are carried, untouched:**

1. **The denominator (d1).** The largest question in the packet. Both bases are still printed on every
   table this act produced (`basis=ANCHOR` drives; `basis=V0` printed beside it).
2. **Layer-2 structure for the eight non-RD pathways (d3).** Their derived positional cells are real,
   computed and printed in `DERIVE_FINAL_O23_out.txt` — and un-installable without new structure in
   the signed table. **Only RD is wirable, 691 of the 1,200 pool entrants.**
3. **Owner override O1** — OFF, per the standing ruling. Not re-measured here.
4. **RUCK depth-1 = 1.000 on the clip ceiling** — survived, unchanged, flagged not smoothed.
5. **PDA charged more than the shipped read** (derived mean R 0.3856 vs today's composed 0.4077).
6. **The age adjustment (D7).** RD earns one on playing quality (t = 2.45); nothing is wired.

And two things this act flags on its own account:

7. **THE DRAFT-BOUNDARY TENSION IS NOW REAL, AND THE OWNER ACCEPTED IT IN ADVANCE.** ND65+ ships at
   **298** while the national curve's pick 64 is **185**. A post-64 selection now prices above pick 64.
   The owner ruled the grounds (the pathway is essentially historical) and queued the tension for the
   pick-curve re-derivation. It is recorded in the artifact and in `rl_model.py` so the re-derivation
   inherits it rather than rediscovering it.
8. **A pre-existing wart, flagged so it is not mistaken for this act's work.**
   `data/rl_build/rl_app_data.json.srcmd5` carries `own_md5: 4b448a82…` — a board from before the
   ORDER 9 bake. It was already stale on `origin/main`, is read by no guard, and correcting it is not
   this lever. Its sibling `engine/rl_after/rl_app_data.json.srcmd5` **is** current and **is**
   restamped here. (ORDER 20C flagged the same thing and also left it.)

---

# 14. REPRODUCE

    export PATH="/root/rl_venv312/bin:$PATH"
    E=docs/evidence/pool_landing_2026-08-12 ; E22=docs/evidence/pool_final_2026-08-12
    bash $E22/build_board_o22.sh <out> nopatch nolevels                      # -> 665311ca on this branch
    bash $E/o23_iterate.sh G3 G4 G2                                          # one round of the iteration
    python3 $E/o23_derive.py <matrix> $E/FINAL_LEVELS_O23.json <out> FINAL
    python3 $E/o23_trajectory.py $E/ITERATION_O23.json F1 G1 G2 G3 G4
    python3 $E/o23_consequence.py $E/CONSEQUENCE_O23.json
    python3 $E/o23_separation_ruck.py <ship> <final> $E/FINAL_LEVELS_O23.json <out>
    bash    $E22/run_noarb_o22.sh <ship> SHIP <final> FINAL23
    python3 $E22/o22_margins.py $E/NOARB_MARGINS_O23.json SHIP FINAL FINAL23
    python3 $E/o23_untouched.py ; python3 $E/o23_bootcheck.py ; python3 $E/o23_f2check.py

**Landing, applied by the SAME scripts the measurement used — which is why the landed board and the
measured board are the same object:**

    python3 $E22/o21_patch.py          <tree> derived $E/FINAL_SURFACE_O23.json
    python3 $E/o23_surface_source.py   <tree>         $E/FINAL_SURFACE_O23.json
    python3 $E/o23_stage.py            <tree>         $E/FINAL_LEVELS_O23.json
    python3 $E/o23_land_config.py      <tree>
    python3 $E/o23_restamp.py          <tree> <board_LANDED.json>

---

_Generated by [Claude Code](https://claude.ai/code)_
