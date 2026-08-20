# H3 REPAIR — RESULT. The five falsifiers, measured.

**Seat:** H3 repair + R23 advance (build seat), register **v792** · **Date:** 2026-08-20
**Base:** `origin/main` @ `702e25d` · store `cc02567f` · board `a05fe951` · `as_of_round=22`
**Prereg:** `PREREG_H3_REPAIR.md`, committed **before** the edit (commit `9ac8fed`).
**Diagnosis:** `H3_DIAGNOSIS.md` (register v792, adjudicated REAL).

---

## 1. The fix as it landed

**`engine/rl_after/rl_export.py:210`** — one statement, inserted at the top of the value loop's
per-player iteration, before the first value-forming `ev()` call (`:211`, formerly `:191`):

```python
    for _p in players:
        g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()      # <- :210, THE FIX
        _r = _ev(_p, 2026); _raw2026[_p['key']] = _r; _p['_v'] = _nb(_r)
```

That is byte-for-byte the repair `H3_DIAGNOSIS.md` §6 names as option 1. No expression, constant,
threshold or law was touched. `rl_export.py` `5dca63ec` → `<new>`; the rest of the diff is the comment
block that states the defect, the measurement, and what is deliberately left undone.

**Not done, by prereg:** the in-`ev()` structural cure (make `ev(p,Y)` pin its own clock before any
evaluation). Referred to the modernisation programme.

## 2. The falsifiers

| id | falsifier | measured | verdict |
|---|---|---|---|
| **F1** | canonical board **byte-identical** `a05fe951` (the mask made it clean; the fix must be a no-op there) | canonical build `rc=0`, board **`a05fe951f78482c70520480e184c80ec`** — byte-exact, twice | **PASS** |
| **F2** | corrected balanced vector == board of record on **804/804**, Σ 664,949 | **804/804 identical**, Σ **664,949** = 664,949, keysets equal | **PASS** |
| **F3** | determinism ×2, both postures | canonical `a05fe951` ×2 · balanced `72fe3a176953fce36239d7b81c3cd492` ×2, Σv 664,949 ×2 | **PASS** |
| **F4** | sibling parity gate 96 fails → 0 | before: `EXPORT<->ENGINE PARITY GATE FAILED for 96/804 players`, `rc=1`. after: **`PARITY GATE PASS: all 804`**, `rc=0` | **PASS** |
| **F5** | `nick-daicos` (`players[0]`, the previously-clean row) unchanged | board of record **9944** · balanced pre-fix **9944** · balanced post-fix **9944** | **PASS** |

Method: the accepted disposable FV builder (`sibling_repin._run_sibling_build` →
`test_fv_provenance._run_build`) under `tools/build_lock.sh`, `PYTHONHASHSEED=0`, all BLAS thread
counts pinned to 1. Nothing was written under the repo by any measurement. Staging trees deleted after
each run.

## 3. The priced movement (disclosed in the prereg, now measured)

Balanced/strict sibling, pre-fix → post-fix:

* **96 rows move, every one of them UP** — the same 96 the diagnosis named. The moved set is
  **exactly** `H3_96_rows.csv`'s 96 keys, and the per-row (before, after) pair agrees with the
  diagnosis on **96/96**.
* Board total **662,177 → 664,949** = **+2,772 (+0.419 %)**. Range **+0.39 % … +9.65 %**.
* 708 rows unmoved, `nick-daicos` among them.
* The post-fix balanced vector **is** the canonical board of record's vector, 804/804.

### Top 20 by absolute movement

| # | key | balanced before | after (= board of record) | delta | % |
|---|---|---:|---:|---:|---:|
| 1 | `harry-sheezel` | 10310 | 10433 | +123 | +1.19% |
| 2 | `aaron-cadman` | 1667 | 1781 | +114 | +6.84% |
| 3 | `will-ashcroft` | 6494 | 6607 | +113 | +1.74% |
| 4 | `bailey-humphrey` | 2213 | 2303 | +90 | +4.07% |
| 5 | `jaspa-fletcher` | 2368 | 2456 | +88 | +3.72% |
| 6 | `george-wardlaw` | 2868 | 2954 | +86 | +3.00% |
| 7 | `cameron-mackenzie` | 1865 | 1942 | +77 | +4.13% |
| 8 | `mattaes-phillipou` | 1838 | 1915 | +77 | +4.19% |
| 9 | `reuben-ginbey` | 2074 | 2144 | +70 | +3.38% |
| 10 | `nick-madden` | 996 | 1064 | +68 | +6.83% |
| 11 | `seth-campbell` | 862 | 928 | +66 | +7.66% |
| 12 | `joshua-weddle` | 1373 | 1437 | +64 | +4.66% |
| 13 | `oliver-hollands` | 1435 | 1498 | +63 | +4.39% |
| 14 | `mitchito-owens` | 1818 | 1880 | +62 | +3.41% |
| 15 | `sam-darcy` | 5016 | 5076 | +60 | +1.20% |
| 16 | `jacob-van-rooyen` | 1660 | 1719 | +59 | +3.55% |
| 17 | `jye-amiss` | 1342 | 1399 | +57 | +4.25% |
| 18 | `mac-andrew` | 3694 | 3750 | +56 | +1.52% |
| 19 | `nasiah-wanganeen-milera` | 8593 | 8644 | +51 | +0.59% |
| 20 | `ryan-maric` | 1238 | 1289 | +51 | +4.12% |

Largest by percentage: `cooper-harvey` 311 → 341 (+9.65 %), `seth-campbell` +7.66 %,
`aaron-cadman` +6.84 %, `nick-madden` +6.83 %, `steely-green` 36 → 38 (+5.56 %).

Full 96-row table with draft year / type / pick / games: **`H3_96_rows.csv`** (unchanged — this build
reproduced it).

---

## 4. F1 FIRED ONCE, ON A WIDER VARIANT, AND THE VARIANT WAS REVERTED

Reported in full because it is the one place this act had to be pulled back.

The prereg declared **two** inserted re-pins: (a) the players loop, and (b) the `back_extra` loop
(`:243-246`), which sits inside the same `:189-221` value block, is board-visible
(`back=[player_rec(p) …]`, `rl_export.py:359`), and was expected to carry the same residue on its
first row.

**(a)+(b) was built and F1 fired.** The canonical board came out `b507446e5a603957f5cba3ba01cc9c2c`,
not `a05fe951`. Diffed against the board of record:

* **active rows: 0 of 804 differ** — byte-identical, `v` and every other field.
* **`back`: 26 of 198 rows differ**, all down (e.g. `charlie-dean` 41 → 39, `jacob-bauer` 29 → 27,
  `tyler-sellers` 21 → 20), plus `lensConservation` which aggregates over them.

So the back-history rows carry a residue of their own — and a larger one than predicted. Entering that
loop the ambient clock is `BASE_REF=2026` but **`AGE_REF=2028`** (the players loop's last forward
call), and these rows evidently do not traverse the `_b6_core`/`price6` re-pin that would correct it,
which is why *26* rows move rather than only the first.

**(b) was reverted.** H3's ruling is about the `BASE_REF` residue on the **active** value loop; the
diagnosis measured `AGE_REF` residue **inert for those rows** and adjudicated nothing about the
back-history basis; and curing it **moves the canonical board of record**, which is a valuation act no
owner word covers. F1 exists precisely to catch an act widening past its warrant, and it did. The
reverted state is recorded in a comment at `rl_export.py:239-248` so the finding is not lost, and it
is logged below rather than carried.

### NEW FINDING, HALTED AND REFERRED — the `back_extra` AGE_REF residue

* **What:** the 198 board-visible back-history rows are priced with `AGE_REF` left at 2028 by the
  preceding forward calls; 26 of them price differently from a present-pinned basis.
* **Status:** **not repaired.** It moves `a05fe951`. Needs an owner ruling of its own, and belongs
  with the in-`ev()` structural cure (`H3_DIAGNOSIS.md` §6 q2/q3) in the modernisation programme.
* **Does it block anything?** No. It is pre-existing, identical in both postures, and the F1 gate is
  satisfied by the board as it stands.

---

## 5. What this discharges, and what it does not

* **H3 is repaired.** The sibling parity gate is green; the balanced/strict board can be built.
* **The corrected basis is the board of record's own basis** — the strongest form the evidence could
  have taken, and the one the diagnosis predicted: 804/804, Σ 664,949.
* Downstream, `balanced_board_md5` moves to `72fe3a17…`, with
  `release_contract.present_lens_baseline` and its seal, the reference/forward vectors, the
  forward-lens oracle, both board-view bundles and `sibling_repin_state.json`. That movement is the
  sibling repin act, recorded in `H3_SIBLING_REPIN.md`.
* **Part 2 (the v790 sheet re-cut and the R23 advance) was withdrawn by the supervisor mid-flight**,
  on the owner's re-sequencing: the ceiling fix is to land before the R23 ingestion so the R22→R23
  movers are measured under the same conditions. It was not abandoned by this seat and nothing of it
  was begun — the owner's R23 file was never read, `scores/R23.csv` was never created, and
  `SITTER_2026_v1.csv` and the ORDER 42 pins are untouched.
