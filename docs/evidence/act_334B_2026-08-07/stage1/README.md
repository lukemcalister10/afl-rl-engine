# 334 stage B / stage 1 — the adopted #336 reference layer, landed

Stage 1 of the four-stage act: take the **adopted** bust-inclusive reference layer off the
experiment branch and land it on a real landing branch, with its identity pins re-stamped and its
board rebuilt and verified. Four engine files come from `variant/336-bust-inclusive` @ `3bbc688`
(amendment 3) — `par_build.py`, `par_redesign.py`, `_merged_recover.py`, `rl_model.py`; nothing
else moved. The branch point is `origin/main` @ `f8fe836`, which has never touched those four
files, so the take is clean (verified, zero intervening commits on all four paths).

**EXPECTATION CONTROL: MATCHED.** The board built here is
`de5110bb57a04d9b24e9c761241e54c7` — byte-exact to the prior scratch build of this configuration.
PARITY GATE PASS (804/804, eps=0), BOOK PARITY GATE PASS, self-test 144 PASS / 0 FAIL. The board
delta vs the shipped board also reproduces the #336 amendment-3 evidence exactly (565 movers,
ΣΔ −26282, ratio 0.965406, identical top-5 cuts and lifts) — see `stage1_delta.txt`.

Pins re-stamped: `rl_model`, `engine_head`, `fv`, `board` — every one recomputed from the checkout
by the guard's own rule, all four independently reproducing the #336 identities. `store`, `v0surf`
and `balanced_board_md5` are untouched; the year-zero surface is **held**. See `PINS.md`, which
also discloses the `board` pin as an addition beyond the three the checklist named.

**Caveat carried from #336:** the reference layer is bust-inclusive but the year-zero surface is
still the shipped survivors-basis fit — the joint re-derivation is the rest of stage B. The two
reds that steer it are unchanged: the hump does not fall (1.535 vs 1.572) and the relocation is
not gone (yr1-to-peak 1.503 vs the shipped 1.394/1.400).

## Re-run

```
export PATH="/root/rl_venv312/bin:$PATH"
git checkout landing/334-stage-b
RL_VENDOR=/home/user/afl-rl-engine/vendor bash /home/user/afl-rl-engine/bootstrap.sh   # Guard 5 must PASS
cd /home/claude/rl_workspace/rl_after && rm -f rl_app_data.json
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor RL_CONFIG_MODE=gate \
  RL_REPO=/home/user/afl-rl-engine RL_FV=/home/user/afl-rl-engine/engine/forward_valuation \
  python3 rl_export.py                     # -> de5110bb57a04d9b24e9c761241e54c7
python3 s4_matrix_M1v7.py && python3 one_source_selftest.py
```

This is a **candidate on a branch**. Nothing was pushed to `main`, no tag, no PR.
