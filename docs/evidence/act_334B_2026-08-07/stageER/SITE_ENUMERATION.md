# Stage ER — complete `era` / `REF` site enumeration, with a verdict on every line

Method: `grep -n '\bera\b|era\.|era\[|_era|era_|REF'` across `engine/rl_after/*.py` and
`engine/forward_valuation/*.py` in the worktree — **264 hits across 34 files** — then each hit
classified. A hit is a TRUE ERA-NORMALIZATION SITE only if it is (or feeds) the multiplicative
per-year rescale `a * REF / era.get(y, REF)`. Everything else is a name collision and was left alone.

Line numbers are pre-strip (the checkout at 4d435ea, after step 1's ladder revert).

---

## A. The table itself — REMOVED

| file:line | code | verdict |
|---|---|---|
| `_merged_recover.py:51-54` | `era={}` / `for Y in range(2009,2026):` / `if a: era[Y]=float(np.mean(a))` | **TRUE — the era table.** Mean season avg over all `>=6`-game seasons per year 2009-2025. REMOVED; replaced by a 7-line comment recording the owner ruling so it cannot be reintroduced by accident. |
| `_merged_recover.py:55` | `REF=float(np.mean(list(era.values())))` | **TRUE — the reference level.** The mean of the 17 yearly means. REMOVED. No symbol needed to be kept alive (see section D). |
| `_gate1.py:7-11` | a SECOND, independently-constructed copy of the same table + `eadj=lambda y,a:a*REF/era.get(y,REF)` | **TRUE — a duplicate era table.** Not found by looking at `_merged_recover` alone; it builds its own. REMOVED, `eadj` collapsed to the identity. |

## B. True normalization USE sites on the shipped value path — STRIPPED

| file:line | enclosing | code | verdict |
|---|---|---|---|
| `_merged_recover.py:899` | `_kpf_LD(p,Y)` | `ls=sorted((a*REF/era.get(y,REF) for y,a,gg in ...))` | **TRUE — stripped to `a`.** THE high-leverage site: the KPF "level demonstrated" (mean of the best two adjusted seasons in the window) feeds the W4 KPF credit regime. **All 28 board movers come from here.** |
| `_merged_recover.py:904` | `_kpf_LD(p,Y)` | `ls0=sorted((a*REF/era.get(y,REF) for ...))` | **TRUE — stripped to `a`.** The fork-v fallback branch of the same function (fires when injury exclusion leaves <2 healthy seasons). |
| `_merged_recover.py:1122` | `bestlvl(p,Y=2026)` | `s=[a*REF/era.get(y,REF) for y,a in ...]` | **TRUE — stripped to `a`.** Live on the value path (consumed by `_ruc_ceiling` at :1258 and the staleness/par ratio at :1836). Produced **0 movers of its own**: `bestlvl` is a MAX over seasons and a ~1.0 rescale rarely changes which season wins. |
| `_merged_recover.py:1795` | `_staleness_grade(p,Y,pos)` | `qv=(live[0]['avg']*REF/era.get(Y,REF))/max(MA.REPL...)` | **TRUE — stripped to `live[0]['avg']`.** The D8 graded-staleness quality axis. Narrow, mostly-saturated interpolation; **0 movers.** |

## C. True normalization use sites OFF the value path — stripped anyway

The owner ruling is "**NO era normalization may be applied to scoring anywhere**", so these were
stripped too even though none of them can move the board.

| file:line | verdict |
|---|---|
| `_merged_recover.py:2161` (`recent_ratio`) | **TRUE — stripped.** Sits at line 2161, **below** the `print("=== AFTER` marker at :2137. Every consumer execs `open('_merged_recover.py').read().split('print("=== AFTER')[0]`, so this tail only runs when the file is executed directly as a diagnostic. Off the value path, stripped for the invariant. |
| `s4_matrix_M1v7.py:94`, `s4_matrix_7147.py:43`, `s4_matrix_M1v7_blend.py:104`, `s4_matrix_M1v7_retainonly.py:82` | **TRUE — `adjavg` collapsed to `round(a,1)`.** This is the walk-forward book's `Ppath` (the displayed PRODUCTION column). A displayed score is still a score. |
| `_build_book_xlsx.py:9`, `_comb_book.py:10`, `_comb_recheck.py:9`, `_flags_support.py:8`, `_m1_ground.py:7`, `_p2b_derive.py:6`, `_p2b_divergence.py:6`, `_p2b_headtohead.py:6` | **TRUE — each `def adj(a,y)` collapsed to `return a`.** Diagnostic/report scripts that pull `era`/`REF` out of the exec'd engine globals. They would have `KeyError`d the moment the table left `_merged_recover.py`, so this was also required for them to run at all. |
| `_gate1_picksplit.py:19`, `_gate1_wf.py:25` | **TRUE — inline `a*REF/era.get(y,REF)` stripped to `a`.** Gate-1 walk-forward diagnostics. |
| `prototypes/staleness_graded_cap.py:56` | **TRUE, latent — stripped.** Found OUTSIDE the briefed grep scope (`engine/prototypes/`). Not code: a *string* of engine source that an unwired prototype would splice in. See section E. |

## D. Consumers that imported the symbols — all fixed at the consumer, none kept alive

The brief anticipated needing to keep `REF` defined-but-unused somewhere. **That was not necessary.**
Every importer of `era`/`REF` was a consumer whose only use was the normalization itself, so deleting
the import was strictly correct and left nothing dangling.

| file:line | was | now |
|---|---|---|
| `s4_matrix_M1v7.py:15` | `MA=g['MA'];ev=g['ev'];REF=g.get('REF',100);era=g['era'];delisted=g['delisted']` | `MA=g['MA'];ev=g['ev'];delisted=g['delisted']` |
| `s4_matrix_7147.py:5`, `s4_matrix_M1v7_blend.py:5`, `s4_matrix_M1v7_retainonly.py:5` | same pattern | same fix |
| `_build_book_xlsx.py:6`, `_comb_book.py:6`, `_comb_recheck.py:5`, `_flags_support.py:5`, `_m1_ground.py:5`, `_p2b_derive.py:5`, `_p2b_divergence.py:5`, `_p2b_headtohead.py:5`, `_keyfwd_decomp.py:5` | `...; era=g['era']; REF=g['REF']` | trailing `; era=...; REF=...` removed |
| `_gate1_picksplit.py:7`, `_gate1_wf.py:10` | `...; REF=ns['REF']; era=ns['era']` | trailing `; REF=...; era=...` removed |

Note `_keyfwd_decomp.py:5` imported `era`/`REF` and then **never used either** — a dead import. Removed.

The `.get('REF',100)` default in the four `s4_matrix*` files is what the brief flagged as possibly
needing a stub. It did not: with `adjavg` collapsed there is no reader left, so the whole binding went.
Had it been left in place it would have silently fallen back to `REF=100` against a missing `era` —
strictly worse than deleting it.

## E. Judgment call — `engine/prototypes/staleness_graded_cap.py`

Outside the briefed grep scope, but the final tree-wide invariant grep found it, so it is recorded here.

* The file is a **source-patching prototype**: it holds `OLD1/OLD2` anchor strings and `NEW1/NEW2`
  replacements, and `apply(src)` splices them into the engine source. Its header says
  *"WIRED NOWHERE — joins a candidate only on Luke's endorsement"* and *"NOT in BAKE CANDIDATE v2"*.
* `NEW2` contained `qv=(yrow[0]['avg']*REF/era.get(Y,REF))/...` — i.e. a **latent instruction to
  reintroduce era normalization**, which would additionally `NameError` now that the symbols are gone.
* **MEASURED BEFORE TOUCHING IT**: its `OLD1`/`OLD2` anchors already matched **0 times** against the
  engine at `ad50dad`, and **0 times** against the pre-strip `4d435ea` engine. It was *already* drift-dead
  before this stage. My change did not break it and cannot have moved anything.
* **Action taken (minimal):** stripped the era factor out of the `NEW2` string and added a note that the
  prototype's fitted `G_gapclass` tables were derived on the era-adjusted basis and would need
  re-deriving on the era-free basis before it could ever be endorsed. Nothing executable changed.

## F. NOT era — explicitly checked and LEFT ALONE

| pattern | where | why it stays |
|---|---|---|
| `AGE_REF` / `BASE_REF` | ~60 sites in `rl_model.py`, `_merged_recover.py`, `rl_export.py`, all of `engine/forward_valuation/*` | The engine's **age/season clock**, not a scale factor. `BASE_REF` = form-anchor year, `AGE_REF` = age-evaluation year. Nothing multiplicative, nothing per-year-mean. |
| `rl_model.py:1654` "backward-board **CONSERVATION NORMALISATION**" | `rl_model.py:1654-1665` | Confirmed by reading it: rescales each backward board `-N` by `(now-total / back-total)` over the SHARED ACTIVE SET so the board is conserved. A **whole-board conservation factor**, not a per-year era factor. Explicitly left, per the brief. |
| `rl_model.py:965` "the CURVE-TEACHING **normaliser**" | `peakval(p)` | Normalises an established teacher against the **establisher baseline** vs the entrant expectation. Per-player class baseline, not per-year. Left. |
| `_merged_recover.py:39` "the **NW normaliser** (w.sum)" | fsum determinism comment | Kernel arithmetic (Nadaraya-Watson weight sum). Left, per the brief. |
| `EXP_LOGREF` (`rl_model.py:862,868`) | expected-peak pick slope | Log-pick reference constant. Not era. |
| `SLIP_REF` `TILT_REF` `NBAD_REF` (`rl_model.py:1318,1326,1329`) | tilt/slip scalers | Fixed tuning constants. Not era. |
| `_ABS_L_REF` (`_merged_recover.py:708,729`) | absence haircut | Pinned mean pre-absence level (75.0). Not era. |
| `RUC_CEIL_REFPK` (`_merged_recover.py:1217`) | ruck-median slot | The pick index 72. Not era. |
| `_UC_VREFB` (`_merged_recover.py:454,478,2047,2063`) | Leg-B un-compress | Median captain-free price per position. Not era. |
| `WIDTH_REF` (`distribution_pricing.py:253`) | band widths | Per-age-bucket SD table. Not era. |
| `RL_V0SURF_REFIT` / "REFIT" / "REFUSE" / "REFRESHED" | many | Substring collisions with `REF`. Not era. |
| `rl_model.py:283` comment "*no era drift*" | history-pool lower bound | A comment **asserting** era-comparability — i.e. agreeing with the owner. Left verbatim. |
| `one_source_selftest.py:606` "*only the numbers below are era data*" | print text | Uses "era" in the ordinary-English sense. Left. |
| `conditional_prior.py:132` "referee-era refinement" | comment | Ordinary-English "era". Left. |
| ALL of `engine/forward_valuation/*.py` | 20 hits | **Zero era hits.** Every hit is `BASE_REF`/`AGE_REF`/`WIDTH_REF`. Nothing to strip; `fv` pin correctly did not move. |
| `s4_render_7147.py:32,109`, `s4_render_M1v7.py:77`, `s4_render_no2003.py:87` | xlsx title strings "era-adj PRODUCTION (P)" | **Labels, not arithmetic** — but they described the column the `s4_matrix` `adjavg` now leaves raw, so the wording was corrected to "PRODUCTION (P)" to keep the sheets truthful. No numeric change. |

## G. The invariant, proven

```
$ grep -rn "\*REF/era\|era\.get(\|era\[Y\]\|=g\['era'\]\|=ns\['era'\]" engine/ --include=*.py
engine/rl_after/_merged_recover.py:52:# An era[Y] table used to be built here ...
engine/rl_after/_merged_recover.py:53:# with REF = the mean of those years) and every career-score read was multiplied by REF/era.get(y,REF).
engine/rl_after/_merged_recover.py:57:# REF, and every a*REF/era.get(y,REF) site are gone; season averages are read RAW. Do not reintroduce.
engine/rl_after/_gate1.py:7:eadj=lambda y,a:a   # RAW season avg — this script's own era[Y]/REF table removed (...)
```

**Four hits remain and all four are comments** recording what was removed. Zero executable
`era.get` / `era[` / `era=` / `REF/era` anywhere in `engine/`. No score is scaled by any per-year
factor on the value path or off it.
