# #306 LANDING SEAT `648fai` — THE BOX-CLASS RECORD (N35)

Classified before any act, per the recorded recipe (`docs/evidence/exec_306_u8ir65/ASSERT_LOG.md`
on branch `claude/exec-306-pass-2-u8ir65` at `9451fae`). A host label classifies nothing; only
reproduced output bytes do.

## THE BOX

| | |
|---|---|
| model name | `Intel(R) Xeon(R) Processor @ 2.10GHz` · stepping 2 · AVX-512F present · 4 cores |
| boot | 2026-08-05 09:30:34 UTC (fresh container; `uptime` 0 min at seat start) |
| rehearsal box, for comparison | `Intel(R) Xeon(R) Processor @ 2.80GHz` · stepping 7 (seat `u8ir65`) |

**This is a different architecture from the one the whole rehearsal ran on.** That matters twice
below, in opposite directions.

## THE ORDER OF ACTS, AS RECORDED

1. **Operating tree reconstructed and proven by round trip.** `472c39d` (branch
   `claude/exec-seat-306-afl-rl-zlaarm`) non-docs content + the `2a1xa4` / `u8ir65` docs trees, exactly
   as the `u8ir65` assert log names it. The 39 non-docs paths were taken into index and worktree so the
   index equals `472c39d`'s non-docs tree, which is the base the captures were cut against.
2. **Pure pass-0 capture `13b71c26` applied, and `git diff --binary -- . ':(exclude)docs/'`
   regenerated it byte-identically.** A wrong base cannot reproduce a capture byte-for-byte, so this is
   the proof the reconstruction is the right one. `data/v0surf.pkl` read `fb9efdec`.
3. **Environment provisioned and re-read from the interpreter — pins 5/5 exact:** Python 3.12.3 ·
   numpy 2.4.4 · scipy 1.17.1 · scikit-learn 1.8.0 · openpyxl 3.1.5. Item-392 bundled OpenBLAS
   sha256 `05c9f9eb…` byte-exact (`libscipy_openblas64_-32a4b2a6.so`). Note for a successor: the repo
   default `python3` here is 3.11 and `bootstrap_env.sh` cannot install into this container's managed
   system interpreter — `setup_env.sh` (the venv route, `$HOME/rl_venv312`) is the one that works, and
   it satisfies the same pin.
4. **`tools/preboot_assert.sh` as its own command** — PASS, no engine process live.
5. **`bootstrap.sh` with its exit code checked** — rc=0. Guard 5 PASS: store `81d24704` · rl_model
   `3b011802` · fv `d920557e`, all == pinned. Engine head `3c7b0c3c` (the old engine, correct for the
   pure pass-0 substrate) · cm_400 `34faa865` · q97m `cfdc7321` · register `652d83e8`.
6. **Tier-2 stamps regenerated per N33** by the engine's own writer (`single_source.lock_tier2`):
   `peak_model_v4.pkl.srcmd5` `d14f0f12` · `pvc_snapshot.json.srcmd5` `aaccad1c`, both == N33's
   expectation.
7. **FIT-PATH ASSERT (N35), on the pure pass-0 substrate, installed curve `e69a3f38`:**

   ```
   refit_v0surf.py --verify
     new md5  32b6d1e5c03c802093efb7e5369cb8e9
     pin      fb9efdec4d669d389fe3beef2bca3092
     VERIFY: refit DIVERGES from the committed pin.            42s
   ```

   **NOT FIT-CLASS.** A third value now stands on the record beside the rehearsal box's `fb9efdec`
   and the seam box's `969dba06` — hazard class 15, from a third direction.
8. **Substrate round trip proven again after the assert** — `13b71c26` byte-identical, so `--verify`
   is confirmed to have written nothing.

| # | UTC | host | substrate | fit-path `fb9efdec` (N35) | verdict |
|---|---|---|---|---|---|
| 1 | 2026-08-05 ~09:40 | Xeon @ 2.10GHz · stepping 2 · up 0 min (boot 09:30:34 UTC) | pure pass-0, `13b71c26` | **DIVERGES — `32b6d1e5`** (42s) | **NOT FIT-CLASS** |

## WHAT THAT PERMITS, AND WHAT IT FORBIDS

**Forbidden here:** any fit act. No refit, no bake of a surface, no fit figure. N35 is not a
formality and this box would produce a surface no other box could reproduce.

**Not forbidden, and this is the point:** the landing contains no fit act. The converged surface
ships as **bytes** (`ebc3d330`), loaded and never fitted — which is precisely what the freeze exists
for. So the landing proceeded, and every figure below it was re-measured here rather than carried
over.

## THE CROSS-MACHINE LEG, NOW MEASURED IN BOTH DIRECTIONS

`#306` L-C asked for a cross-machine byte-assert and the record has carried it as **UNMEASURED for
want of a second architecture** (owner ruling 2026-07-22, recorded in `ci-guards.yml`). A second
architecture arrived by itself. What it measured:

| | result |
|---|---|
| the v0surf **FIT**, cross-machine | **DIVERGES** — `fb9efdec` there, `32b6d1e5` here. Item 380 exactly; the reason the surface is frozen. |
| the **compute path** with the surface supplied, cross-machine | **BYTE-IDENTICAL** — board `46ebfb37` here == `46ebfb37` on the rehearsal box, and `46ebfb37` again on a second build here. |
| the gates on this box | selftest **97 PASS / 0 FAIL** · G-Y0 **0.033%** ≤ 2.000% HARD (n=1326) · F5 reconciliation MATCH 62726 at seal `ed5b7fcc` · F5 league + F4 roster both PASS |
| the L8 attribution on this box | 804 common · 601 movers · curve 322 / lens 255 / pool 24 · sums `+1339` / `-466` / `+81` — identical to the rehearsal figures |

This is not a substitute for the assert L-C asks to be **wired into the lane**; that remains owed.
It is, however, the first time the record's central claim — *the compute path is cross-CPU
byte-deterministic once the surface is supplied* — has been measured on two genuinely different
architectures rather than one box under forced kernels. It holds.
