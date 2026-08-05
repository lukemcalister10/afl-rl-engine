# #306 seat `u8ir65` — THE BOX-CLASS ASSERT LOG

Appended to, never edited in place. N35: the fit-path assert is mandatory before any fit figure, and it
stales on any observed restart or host migration. A host label classifies nothing — only reproduced
output bytes do (hazard class 15).

| # | UTC | host (`model name` · stepping · uptime at entry) | substrate | fit-path `fb9efdec` (N35) | verdict |
|---|---|---|---|---|---|
| 1 | 2026-08-05 04:29 | `Intel(R) Xeon(R) Processor @ 2.80GHz` · stepping 7 · **up 0 min at session start (boot 04:18:42 UTC)** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (55s) | **FIT-CLASS** |

## Entry 1 — the arrival assert

`uptime` read **0 min** on the first command of this seat, so both asserts were stale on arrival and no fit
figure would have been trustworthy until the box was classified. Boot established from `/proc/uptime` as
**04:18:42 UTC**; the fit assert ran at **04:29**, after the boot, so the classification covers every figure
below it.

**Order of acts, per N35 and R-H:**

1. **Substrate proven first, by round trip.** The pure pass-0 capture `13b71c26934d8a5b62c4f3ac1fa22137`
   applied to the recorded base and `git diff --binary -- . ':(exclude)docs/'` regenerated it
   **byte-identically**. Taken before anything ran, so the restore check used afterwards is itself valid.
   `data/v0surf.pkl` `fb9efdec4d669d389fe3beef2bca3092`.
2. **Environment provisioned and re-read from the interpreter** — pins **5/5 exact**
   (Python 3.12.3 · numpy 2.4.4 · scipy 1.17.1 · scikit-learn 1.8.0 · openpyxl 3.1.5); item-392 bundled
   OpenBLAS **sha256 `05c9f9eb…` byte-exact** (`libscipy_openblas64_-32a4b2a6.so`). Recorded because it
   cost a minute: the pin is a **sha256**, and an md5 of the same file (`92d36f8f…`) is not a mismatch,
   it is the wrong instrument.
3. **`preboot_assert.sh` as its own command** — PASS, no engine process live.
4. **`bootstrap.sh` with its exit code checked** — rc=0. Guard 5 **PASS**: store `81d24704` == pinned ·
   rl_model `3b011802` == pinned · fv `d920557e` == pinned. cm_400 `34faa865` · q97m `cfdc7321` ·
   register `652d83e8` · engine head `3c7b0c3c` (the OLD engine, correct for the pure pass-0 substrate).
5. **The two untracked tier-2 stamps regenerated per N33**, by calling the engine's own writer
   `single_source.stamp_tier2_frozen` — a pure function of the artifact's own bytes. No peak rebuild
   (R-A forbids it on a travelling substrate).

   ```
   peak_model_v4.pkl.srcmd5     d14f0f126a3e7682318745c80e346ea2   == N33's expectation
   pvc_snapshot.json.srcmd5     aaccad1c9908e262c15fd7addfe79f50   == N33's expectation
   ```

6. **FIT-PATH ASSERT (N35), the ruled first act:**

   ```
   refit_v0surf.py --verify, pure pass-0 substrate, installed curve e69a3f38
     new md5  fb9efdec4d669d389fe3beef2bca3092
     pin      fb9efdec4d669d389fe3beef2bca3092
     VERIFY: refit REPRODUCES the committed pin.          55s
   ```

   **PASS. This box is FIT-CLASS.** It reproduces the record's own fit, so comparisons against the
   record's figures are valid from here. Same CPU label as the seam's box, which **fails** this assert
   (`969dba06`) — hazard class 15 from both directions, exactly as the record says.

7. **Substrate round trip proven again after the assert** — `13b71c26` byte-identical, so `--verify`
   is confirmed to have written nothing.

## THE OPERATING TREE — a reconstruction finding a successor should not have to rediscover

The live capture's `.BASE` names **`472c39d` on `claude/exec-seat-306-afl-rl-zlaarm`**. That base carries
**39 non-docs files the `2a1xa4` evidence branch does not** — the #279 panel machinery
(`session_2026-07-30/item279/panel/`, `item279_step4/scripts/` including `harness_pvc_REPINNED.py`) and
`tools/preboot_assert.sh`. Applying the capture to the evidence branch tree **fails** on the first missing
file. The operating tree is therefore **zlaarm's non-docs content + the `2a1xa4` docs tree**, and the
committed instruments assume it (`run_pass.sh` hardcodes the repo root; `install_pass1.py` reads the
derived curve out of `docs/evidence/exec_306_2a1xa4/l6/`).

Reconstructed here without a commit: the 39 paths were checked out into **index and worktree** from
`472c39d`, which makes the index equal `472c39d`'s non-docs tree exactly, so
`git diff --binary -- . ':(exclude)docs/'` is measured against the base the captures were cut against.
**Both round trips are exact, which is the proof that this reconstruction is the right one** — a wrong
base cannot reproduce a capture byte-identically.

## THE NINE CAPTURES — all re-hashed from their carriers, all match

| # | md5 | carrier |
|---|---|---|
| 1 | `13b71c26` | `7e9d7f9` (d7bnaa) — pure pass-0, the N35 assert substrate |
| 2 | `02e248dc` | `472c39d` (zlaarm) |
| 3 | `8650c060` | `472c39d` |
| 4 | `59ef1940` | `472c39d` |
| 5 | `e9508660` | `472c39d` |
| 6 | `efaf67d6` | `472c39d` |
| 7 | `2b7640be` | `472c39d` |
| 8 | `ebaca58e` | `489587b` (2a1xa4) — pass 1 as first installed, defective pin, retained as record |
| 9 | **`bc1001f9`** | `489587b` — **THE LIVE SUBSTRATE**, applied and round-trip proven here |

## Entry 2 — the pre-closure re-classification

The container **restarted** between the pass-3 filing and the closure install: `uptime` read **1 min**,
boot established from `/proc/uptime` as **05:48:26 UTC**. Entry 1's classification (boot 04:18:42) went
stale at that moment, and the closure act contains a **C.3 refit** — a fit act — so no part of it was
permitted to proceed on a stale classification.

Re-classified in full, in the ruled order: live substrate round-tripped to `692b12ff` first (proving the
restart cost nothing) → pure pass-0 capture `13b71c26` restored and round-trip proven → pins **5/5 exact**,
OpenBLAS **sha256 `05c9f9eb` byte-exact** → `preboot_assert.sh` as its own command → `bootstrap.sh`
**rc=0**, Guard 5 PASS → tier-2 stamps regenerated to `d14f0f12` / `aaccad1c` → **FIT-PATH ASSERT PASS,
`fb9efdec4d669d389fe3beef2bca3092`, 76s** → round trip to `13b71c26` again → live substrate restored to
`692b12ff` and proven before the install.

| # | UTC | host (`model name` · stepping · uptime at entry) | substrate | fit-path `fb9efdec` (N35) | verdict |
|---|---|---|---|---|---|
| 2 | 2026-08-05 05:52 | `Intel(R) Xeon(R) Processor @ 2.80GHz` · stepping 7 · **up 1 min (container restarted; boot 05:48:26 UTC)** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (76s) | **FIT-CLASS, re-classified** |

**Two classifications, two reproductions of `fb9efdec`** — 55s / 76s. Every closure figure post-dates
entry 2. On this environment `uptime` has now moved under this seat once; the outgoing seat saw it move
five times in a day. It is not a formality.

## CORRECTION TO THE CAPTURES TABLE ABOVE — appended, not edited in place

The table headed "THE NINE CAPTURES" was true when written (arrival). **Twelve captures now stand,
none overwritten.** Added since, all on this branch under `docs/evidence/exec_306_u8ir65/`:

| # | md5 | what it is |
|---|---|---|
| 10 | `e6bc7e9d` | `L6_pass2_state.diff` — pass 2 (curve `b61c01b0`, surface `69571649`) |
| 11 | `692b12ff` | `L6_pass3_state.diff` — pass 3, **the BOUND-EXHAUSTED state** the HALT was measured on |
| 12 | **`96cb79b2`** | `L6_closure_state.diff` — **THE LIVE SUBSTRATE**, the adopted curve `01f27f02` + surface `ebc3d330` |

Each carries a `.BASE` annotation written at generation. The nine-row table above is left standing as
the arrival record rather than rewritten, per this file's own discipline.
