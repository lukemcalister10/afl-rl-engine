# 334 stage B / ERA REMOVAL (stage ER)

**The owner's law, in one line:** SuperCoach scores are era-comparable BY CONSTRUCTION — every match
assigns 3,300 points — so no era normalization may be applied to scoring anywhere in this engine.

The shipped engine carried an `era[Y]` table (mean season average over `>=6`-game seasons per year
2009-2025, with `REF` = the mean of those years) built at the top of
`engine/rl_after/_merged_recover.py`, and multiplied career scores by `REF / era.get(year, REF)` at
five sites. Reconstructed from the pinned store, that multiplier ran **0.95885 to 1.05495** — a 9.6%
per-year rescale applied to every score the engine read. It is now gone. Season averages are read RAW.

## What is in this directory

| file | what it is |
|---|---|
| `SITE_ENUMERATION.md` | Every `era`/`REF` hit across `engine/rl_after/*.py` and `engine/forward_valuation/*.py` (264 hits, 34 files), each with a verdict: true era-normalization site, name collision, or judgment call. Includes the proof of the invariant. |
| `STRIP_DIFF.txt` | The strip: per-file added/removed counts plus the complete diff of all 21 touched sources. |
| `SELFTEST_REPOINTS.md` | The re-point enumeration — **empty**, plus why, plus every gate result. |
| `board_delta.txt` | The board delta vs the stage-1 board: movers, totals, ratio, mean relative move, the complete mover list, the age-bucket breakdown, and the reconstructed era table. |
| `selftest_full_output.txt` | Full 228-line `one_source_selftest.py` transcript. |
| `PINS.md` | Pins old -> new, the stamping order, and one pre-existing inconsistency repaired. |

## Why the stage-2 ladder was reverted

Stage 2 (`4d435ea`) re-taught the pick ladder `engine/rl_after/pvc_curve_v2.json` from a per-pick
re-anchor derived off the stage-1 matrix. **That entire derivation was taught on the era-adjusted
basis** — every score that fed the re-anchor had the `REF/era` multiplier on it. The owner ruling
supersedes the basis the ladder was fitted to, so the ladder is not merely stale, it is *wrong at the
root*: keeping it would carry the era distortion forward inside a fitted artifact even after the
multiplier itself was deleted from the code.

Step 1 of this stage therefore restored it:

```
git checkout ad50dad -- engine/rl_after/pvc_curve_v2.json
```

Confirmed back at the shipped payload: `md5({str(pick): int(round(v))} over the curve object,
json.dumps sort_keys) = df766dff94657940e2a892e91da5a6e2`, matching the filed control.
*(Note: the control was described as an "N32" payload; the `curve` object in fact carries 64 picks
(keys 1-64). The md5 over all 64 is exactly the specified `df766dff...`, so the revert is confirmed
against the filed value — only the label was off.)*

**The ladder now needs re-deriving on the era-free basis.** That is not this stage's job, and the
commit message says so.

**This makes the board delta clean.** Because the ladder is back at stage-1 values, the delta in
`board_delta.txt` is the *pure* era-removal effect: nothing else differs between the two boards.

## The result

* Board `de5110bb` -> `f94e0778`. **28 movers of 804 (3.48%). Every single one is a cut. Not one lift.**
* **Every mover is a key-position forward.** The one high-leverage site was `_kpf_LD()` — the KPF
  "level demonstrated" that feeds the W4 KPF credit regime.
* Board total `733440` -> `732696`, ratio **0.998986**. Mean |relative move| 0.0792% across the board,
  2.2743% across the movers.
* Monotone in age: `<=22` ratio 0.999960 (1 mover), `23-26` 0.998700 (10), `>=27` 0.998135 (17).
  Young players have little qualifying history for the multiplier to have acted on.
* All gates pass. The self-test needed **zero** re-points.

## How to re-run

```bash
export PATH=/root/rl_venv312/bin:$PATH
git worktree add /home/claude/stageER_landing landing/334-stage-b

# 1. seed the workspace from the checkout (Guard 5 asserts store/rl_model/fv on entry)
RL_VENDOR=/home/claude/stageER_landing/vendor bash /home/claude/stageER_landing/bootstrap.sh

# 2. canonical env for every build step below
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export RL_CONFIG_MODE=gate
export RL_REPO=/home/claude/stageER_landing
export RL_FV=/home/claude/stageER_landing/engine/forward_valuation

cd /home/claude/rl_workspace/rl_after
rm -f rl_app_data.json
python3 rl_export.py            # PARITY GATE must pass; board md5 -> f94e0778f8ab49e81bba8658f1c14a4d
python3 s4_matrix_M1v7.py       # BOOK<->BOARD PARITY GATE must pass
python3 one_source_selftest.py  # must exit 0; 146 PASS, 0 FAIL
```

To re-verify the invariant at any time:

```bash
grep -rn "\*REF/era\|era\.get(\|era\[Y\]\|=g\['era'\]\|=ns\['era'\]" engine/ --include=*.py
```

Four hits, **all four comments** recording what was removed. Zero executable per-year scaling.

## Scope notes

* `data/v0surf.pkl` is untouched. The v0surf config signature is made of the pick curve, the roster,
  and the `_V0SURF_GATES` env keys — **no engine source hash participates** — so the strip could not
  and did not disturb the freeze. It loaded frozen; no refit, declared or silent.
* `rl_model.py` and all of `engine/forward_valuation/` were not edited (no era in either), so those
  pins did not move.
* One file outside the briefed grep scope was touched: `engine/prototypes/staleness_graded_cap.py`,
  an unwired source-patching prototype that held a latent era multiplier inside a replacement string.
  Its splice anchors were measured **already dead** against both `ad50dad` and `4d435ea` before it was
  touched. See `SITE_ENUMERATION.md` section E.
