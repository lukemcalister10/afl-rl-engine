# #334 REHEARSAL SEAT — THE BOX-CLASS RECORD. Classification **NOT ACHIEVABLE** on this substrate.

Attempted before any act, per N35 and the recorded recipe. **A host label classifies nothing; only
reproduced output bytes do.** Stage B contains a fit, so this is a gate, not a formality.

## THE BOX

| | |
|---|---|
| model name | `Intel(R) Xeon(R) Processor @ 2.80GHz` · 4 cores |
| uptime at first command | ~28 min (no restart observed during the seat) |
| same label as | the #328 `jujn3g` box, which was FIT-CLASS. **The label was not taken as the answer.** |
| env pins | Python **3.12.3** · numpy **2.4.4** · scipy **1.17.1** · scikit-learn **1.8.0** · openpyxl **3.1.5** — 5/5 exact |
| OpenBLAS | item-392 bundled sha256 `05c9f9eb…` byte-exact, asserted by `bootstrap.sh`'s own fail-closed check |

## THE ORDER OF ACTS

1. A **pristine worktree at landed main `da9aa70`** was cut for the classification, so the pre-fix
   substrate is the real one and not a reconstruction: store `f1e8c9fe`, curve payload `df766dff`,
   surface pin `d594dc034e86935b370c49b240a18370`.
2. `tools/preboot_assert.sh` as its own command — **PASS**, no engine process live.
3. `bootstrap.sh` with its exit code checked — **rc=0**. Guard 5 PASS: store `f1e8c9fe` ·
   rl_model `33f94073` · fv `d920557e`, all == pinned. engine `9f258a3b` · q97m `cfdc7321` ·
   register `652d83e8` · cm_400 `34faa865`.
4. Declared lens basis present on landed main (`docs/evidence/exec_306_zlaarm/basis/`), so no
   `RL_LENS_BASIS` override was needed — the #328 gap is closed on this tree.
5. **FIT-PATH ASSERT (N35) — DID NOT RUN.**

   ```
   RL_V0SURF_REFIT=1 refit_v0surf.py --verify, pristine da9aa70, curve df766dff
   AssertionError at _merged_recover.py:1909
     #326 HALT: the year-zero surface was NOT loaded from the freeze
     (signature af556bdca53dee20d4f73e0ae25a8127, refit declared='1').
   rc=1, 88s
   ```

   **VERDICT: UNCLASSIFIABLE ON THIS SUBSTRATE — not "fails", not "passes".** The refit path is
   barred by an unconditional module-scope assert landed by #326:

   ```python
   _v0surf_frozen = (_frozen is not None and os.environ.get('RL_V0SURF_REFIT') != '1')
   assert _V0CURVE_META.get('_v0surf_frozen') is True, '#326 HALT: ...'
   ```

   `RL_V0SURF_REFIT=1` is the only way to fit and it forces the flag False, so the assert always
   fires. #326 used exactly this as its own non-vacuity RED evidence
   (`docs/evidence/act_326_2026-08-06/gate7_nosilentrefit_RED.txt` — same line, same message), so
   the bar is deliberate and documented; what is new is that it also bars the *declared* bake lane,
   which is the lane every future surface re-bake must use. **Recorded as a substrate finding on
   landed main, not worked around.** No env was unset, no assert was edited, no fit was forced.

## WHAT THIS BOX **DID** PROVE — DETERMINISM-CLASS

Two reproductions, both byte-exact, both on the value path:

| # | run | result |
|---|---|---|
| 1 | full build from the pristine `da9aa70` checkout, single-thread, gate mode | board **`864b6726a4612b0d8afe57f230421514`** — **the landed pin, byte-exact** |
| 2 | full build on the corrected store `f1e7f20c`, run twice | **`827fb1fdfefe60c7c2c9026212d3992d`** both times |

So every Stage-A figure in `ACT.md` is comparable to the record's, and the 154-mover result is a real
basis move rather than a box artefact. What is *not* established is fit-class, and therefore no
number that would come out of a surface fit is reported anywhere in this rehearsal.

## THE PRECONDITION, NAMED RATHER THAN ASSUMED

`refit_v0surf.py` states a clean-instance precondition in terms of the balanced board `06d8af60`,
recorded as "NOT EVALUATED — unreachable since the pricing split" since item 271. Run 1 above is the
substitute evidence of the same kind #328's record used — except that here it stands alone, because
the fit-path assert it was meant to accompany could not be executed.
