# P0 / A1 — THE FOUR HASHES, PRINTED AND REBUILT (not the word "matches")

**Box: AVX512 (avx512f/bw/cd/dq/vl), OpenBLAS DYNAMIC_ARCH → Haswell (AVX2) kernel, numpy dispatch
AVX512_ICL/SPR. On this box `refit_q97m.py --verify` REPRODUCES the frozen pin `cfdc7321` — i.e. this box
is the bake-box analog.**

| leg | artifact | expected (pin) | REBUILT md5 | verdict |
|---|---|---|---|---|
| A | working-head board | `3dc19fbbf920958affe7c6a2be9697d2` | **`3dc19fbbf920958affe7c6a2be9697d2`** | ✅ byte-identical |
| A | working-head book (B3 stable seal) | `d371a27c…871bc44f` (n=2649) | **`d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f`** (n=2649) | ✅ byte-identical |
| B | **tag board of record** | `81e48293…` | **`81e48293e4a47309567c47f392eda1fc`** | ✅ byte-identical |
| B | **the tag's book** (B3 stable seal) | `c7825f1b…4323` (n=2649) | **`c7825f1b3c1dc122e16e3a11c1cd530b29599551eea935c39bc908f6b19a4323`** (n=2649) | ✅ byte-identical |

## Construction — IN FULL (every pin booted on, every override, any guard bypassed)

### Leg A — working-head board `3dc19fbb` and book `d371a27c`
- **Branch/tree:** `claude/q97m-freeze-determinism-s9v8ky` @ `f14710d` (== directive BASE; sits on `ed13177`/PR#74).
- **Pins booted on (all native to this branch, Guard 5 PASS, NOTHING overridden, NO bypass):**
  store `340a7a32` · board `3dc19fbb` · engine_head `2334f570` · config `c2d233ae` · band `34faa865` ·
  q97m `cfdc7321` (LOADED, not fitted) · register `652d83e8`.
- **Board cmd:** `cd /home/claude/rl_workspace/rl_after && RL_REPO=<repo> RL_CONFIG_MODE=gate python3 rl_export.py` → md5 `rl_app_data.json`.
- **Book cmd:** `S4_MATRIX=<tmp> RL_CONFIG_MODE=gate python3 s4_matrix_M1v7.py` → B3 stable_sha256 over the id(p)-keyed book re-keyed by (player,type,year,pick). (Raw xlsx bytes are non-deterministic by design — item 78; the seal is the hash.)
- Book meta confirms: engine_head `2334f570`, store `340a7a32`, config `c2d233ae`. The sealed baseline
  (`book_stable_seal.json`) carries head `2030e5df` but content sha `d371a27c` — the regen MATCHES it (P5).

### Leg B — tag board of record `81e48293` and the tag's book (⚠ the last return was SILENT on this leg)
- **Tree:** a fresh git worktree at **tag `9f8ae76` (v2.9)** — `git worktree add --detach /tmp/tag_v29 9f8ae76`.
- **Pins booted on (the TAG's OWN pins, via the tag's own `bootstrap.sh`; Guard 5 PASS on the tag tree; NO bypass, NO false halt):**
  store `b0c39d78` · board `81e48293` · engine_head `2030e5df` · config `69ead79b` · band `34faa865`.
  **`q97m` pin is ABSENT at the tag** — the tag engine (`2030e5df`) FITS q97m at runtime (there is no frozen
  pickle at the tag). On this box that runtime fit == `cfdc7321` (verified), so it reproduces `81e48293`.
- **Why this is NOT the item-86 false-halt trap:** the four-pin false alarm arises only when the TAG's STORE
  is run against THIS branch's pins. Here the tag tree is booted on the tag's OWN `expected_boot.json`
  (store/board/config/engine all self-consistent), so Guard 5 passes cleanly — **no guard was disabled.**
- **Board cmd:** `RL_REPO=/tmp/tag_v29 RL_CONFIG_MODE=gate python3 rl_export.py` (tag config 69ead79b).
- **Result:** TAG BOARD md5 `81e48293e4a47309567c47f392eda1fc` == the board of record. **The chapter's
  board of record is rebuildable, from source, on this box. A1 is now VERIFIED, not claimed.**
- **Cleanup:** worktree removed; my branch re-bootstrapped (workspace restored to store `340a7a32`, engine `2334f570`).

### The "both configs" re-proof of #74 board-neutrality
Leg A built board `3dc19fbb` at config `c2d233ae`; Leg B built board `81e48293` at config `69ead79b`.
Per the item-20 note these two boards differ ONLY by the store (bramble +1: `81e48293`→`3dc19fbb` is the
store move `b0c39d78`→`340a7a32`, engine/config UNCHANGED). The book seal's own `sealed_by` records the
config move `69ead79b`→`c2d233ae` as **content-identical** (`d371a27c` byte-identical; "the 7 newly-pinned
model vars all == engine defaults"). That is the by-product re-proof that #74's config change is board- and
book-neutral. (A direct single-store two-config A/B was not run to avoid editing the tag worktree's pins;
the store-isolation above + the sealed-content identity establish neutrality without it.)

## Raw logs (committed)
`legA_workinghead_board.txt` · `legB_tag_board.txt` (full build log incl. tag bootstrap + hashes) ·
`boardA_native.json`/`boardB_sse.json` (P3) · `build_tag_legB.sh`, `build_board.sh` (exact commands).
