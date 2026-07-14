# A5 — 81e48293 REBUILT AT THE TAG'S OWN TREE (re-proved, not taken on trust)
# 2026-07-14 · pinned box (this session: Intel Xeon, SkylakeX/AVX512)

## METHOD
`git worktree add --detach <wt> 9f8ae76` (v2.9 tag) → `bash <wt>/bootstrap.sh` (seeds the workspace from the
TAG's own tree) → `RL_CONFIG_MODE=bake python3 rl_export.py` in the seeded workspace → md5 the built board.
The tag carries **no q97m pin** (`q97m: None` in its `expected_boot.json`), so q97m is **fitted at runtime**, as
the tag's construction requires — this is the genuine rebuild, not a reload of a committed artifact.

## BOOT IDENTITY (from the tag, asserted by the tag's Guard 5)
engine `2030e5df` · store `b0c39d78` · cm_400 `34faa865` · config `69ead79b` (40 model vars) · register `652d83e8`

## RESULT
- committed board file at the tag (`git show 9f8ae76:data/rl_build/rl_app_data.json | md5`) = **`81e48293`**
- **REBUILT board from the tag's source = `81e48293`** ✓ (expect `81e48293e4a47309567c47f392eda1fc`)
- NUMÉRAIRE GUARD: PASS — shipped pick-1 = 3000.

**A5 PASS. The board of record rebuilds byte-identical at the tag's own tree, on the pinned box.** Every number
in this project is measured against `81e48293`; it stands. (This also corroborates that the board of record is a
SkylakeX/AVX512 artifact: the same Intel box that natively builds `3dc19fbb` for the addef03 engine builds
`81e48293` for the v2.9 tag — both AVX512 kernels.)

## A1 (same box, current engine)
addef03 engine, native SkylakeX → `3dc19fbb`; `OPENBLAS_NUM_THREADS=1` → `3dc19fbb`; drift-to-Haswell
(`5546c120`) then restore → `3dc19fbb`. The board does not move on the pinned box.
