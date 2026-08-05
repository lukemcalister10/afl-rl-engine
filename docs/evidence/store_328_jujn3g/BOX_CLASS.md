# #328 STORE-ACT SEAT `jujn3g` — THE BOX-CLASS RECORD

Classified before any act, per the recorded recipe (N35, `docs/evidence/exec_306_u8ir65/ASSERT_LOG.md`
on `claude/exec-306-pass-2-u8ir65` at `9451fae`). **A host label classifies nothing; only reproduced
output bytes do.** This act contains a fit, so the classification is a gate, not a formality: a box that
fails it is restarted or swapped, never worked around.

## THE BOX

| | |
|---|---|
| model name | `Intel(R) Xeon(R) Processor @ 2.80GHz` · stepping 7 · AVX-512F present · 4 cores |
| boot | 2026-08-05 ~11:48 UTC (fresh container; `uptime` read 1 min on this seat's first command) |
| same label as | the rehearsal box (`u8ir65`), which is FIT-CLASS. **The label was not taken as the answer.** |
| different label from | the landing box (`648fai`, 2.10GHz stepping 2), which is **NOT** FIT-CLASS |

## THE ORDER OF ACTS

1. **Environment provisioned and re-read from the interpreter — pins 5/5 exact:** Python 3.12.3 ·
   numpy 2.4.4 · scipy 1.17.1 · scikit-learn 1.8.0 · openpyxl 3.1.5. Item-392 bundled OpenBLAS
   sha256 `05c9f9eb…` byte-exact, asserted by `bootstrap.sh`'s own fail-closed check.
   The landing seat's note holds here too: `setup_env.sh` (the venv route, `$HOME/rl_venv312`) is the
   one that works; the container's default `python3` is 3.11.
2. **`tools/preboot_assert.sh` as its own command** — PASS, no engine process live.
3. **`bootstrap.sh` with its exit code checked** — rc=0. Guard 5 PASS: store `81d24704` ·
   rl_model `3b011802` · fv `d920557e`, all == pinned. Engine head `15525b03` (the landed engine) ·
   cm_400 `34faa865` · q97m `cfdc7321` · register `652d83e8`.
4. **Tier-2 stamps regenerated** by the engine's own writer (`single_source.lock_tier2`):
   `peak_model_v4.pkl` `f305fe53` · `pvc_snapshot.json` `ade79790`, both == the landed pins.
5. **THE DECLARED LENS INPUT IS NOT ON LANDED MAIN — and the fit needs it.** The first fit attempt
   stopped on the engine's own refusal:

   ```
   v0 LENS BASIS MISSING: docs/evidence/exec_306_zlaarm/basis/structural_basis_279.json
     ... There is deliberately no fallback: fitting the lens from the surface's own prior is the
     barred, self-referential lineage.
   ```

   That path lives on `claude/exec-seat-306-afl-rl-zlaarm` and did not come across at the landing.
   Resolved through the route the refusal itself names, not around it: the basis was **regenerated
   from landed main by its own emitter**, whose two #279 sources are present here and match its pins
   byte-for-byte (`harness_pvc.py` `e0130cc2` · `per_entrant_279_vor.json` `77eba4d3`). It emitted
   **`25a72f85a96b865505123fb47597cea6` — byte-identical to the committed artifact**, which is also
   the value the L6 passes re-proved at every re-pin. Supplied to every run below via `RL_LENS_BASIS`,
   so the repository tree carries no borrowed evidence path. **Recorded as a gap in landed main:** a
   fit cannot be run from a clean checkout of `dab9657` without this input.
6. **FIT-PATH ASSERT (N35), on the landed substrate — the substrate this act actually runs on:**

   ```
   refit_v0surf.py --verify, landed main dab9657, adopted curve 01f27f02
     new md5  ebc3d3303a1956a8ec94b4e2c1497bdf
     pin      ebc3d3303a1956a8ec94b4e2c1497bdf
     VERIFY: refit REPRODUCES the committed pin.              99s
   ```

   **PASS. THIS BOX IS FIT-CLASS.** It reproduces the record's own converged surface from the fit
   path, so every fit figure below it is comparable to the record's.

| # | UTC | host | substrate | fit-path assert | verdict |
|---|---|---|---|---|---|
| 1 | 2026-08-05 ~11:56 | Xeon @ 2.80GHz · stepping 7 · up ~8 min | landed main `dab9657`, curve `01f27f02` | **PASS — `ebc3d330`** (99s) | **FIT-CLASS** |

## THE CLASSIFICATION RE-CONFIRMED TWICE MORE, WITHOUT BEING ASKED TO BE

Two later measurements are independent reproductions of a fit on this box, and both landed exactly:

- the lens basis re-emitted to `25a72f85`, the value the record carries (act 5 above);
- **the reversal check's control run reproduced the adopted ladder `01f27f02` byte-for-byte** from
  the closure's own pass-3 matrix (`REVERSAL_CHECK.md`). That run is the reason the step-4 halt can
  be read as a real basis move rather than an instrument or a box artefact.

## THE BAKE PRECONDITION, NAMED RATHER THAN ASSUMED

`refit_v0surf.py` states a clean-instance precondition in terms of the balanced board `06d8af60`, and
its own provenance log has recorded that precondition as **"NOT EVALUATED — unreachable since the
pricing split"** since item 271 stage B, pointing instead at "the job that ran it" for substitute
evidence. **This record is that substitute evidence**: the fit-path assert above, passed on the
substrate the bake ran on, minutes before it ran.
