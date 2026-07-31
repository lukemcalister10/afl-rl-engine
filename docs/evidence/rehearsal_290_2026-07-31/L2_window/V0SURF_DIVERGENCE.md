# FINDING — the L1-exit tree is not exactly reconstructible, and G-Y0 moves with the container

**#290, L2 seat, 2026-07-31.** Filed as evidence, not as prose. Every figure below was read from a
run in this container or from a committed artifact.

---

## 1 · WHAT HAPPENED

The seam ruled (2026-07-31) that any reconstruction of the L1-exit tree asserts, after the declared
71s refit lane:

```
md5(data/v0surf.pkl)            == e92e3885df24060aa90557ba20ba3612   (= expected_boot.v0surf)
git hash-object data/v0surf.pkl == a02818f…                           (the diff's target blob)
```

**The assert fired.** The lane, run exactly as declared, produced:

```
md5  84fb0cde29f36c1a91d440e63b753c3c      (want e92e3885df24060aa90557ba20ba3612)
blob 2f4c3859bd34629b3ba9849e2ea32eff2b52c346  (want a02818f…)
```

The assert is the reason this was caught rather than carried. Nothing here was inferred from prose.

---

## 2 · WHAT WAS MEASURED, IN ORDER

**(a) The lane is byte-deterministic in this container.** Two independent `--bake` runs, fresh
processes, produced **identical bytes** (`84fb0cde…` both times). So the divergence is
container-to-container, not run-to-run.

**(b) The config signature is IDENTICAL to the record's.** Both runs report shipped-config signature
`96d671c952c819fa64df0b5d1a402f1e` and the same frozen set of **2** surfaces
(`0589a2620e24e71a348988d27ab06154`, `96d671c952c819fa64df0b5d1a402f1e`) — byte-for-byte the same
lines the predecessor's `F_refit.txt` records. **The signature keys on `_PVC0` (the curve input), not
on the fitted output**, so equal signatures do not imply equal surfaces. The signature agreeing while
the bytes differ is the whole point.

**(c) `v0surf.pkl` is the SOLE differing input.** Proven field-level, not asserted:

| comparison | result |
|---|---|
| the 14 other patched files, my tree vs the committed `L1_amended_state.diff` | **byte-identical, all 14** |
| `data/expected_boot.json`, 37 keys, mine vs the record's intended L1-exit | **exactly 1 key differs: `v0surf`** |
| `session_2026-07-18/legf6/v0surf_refit_log.json` | differs only by my own two appended bake entries |

**(d) The gate set reproduces — except the acceptance number.** Full chain on the reconstructed tree:

```
bootstrap 0 · refit 66s · board 0 (120s) · book 0 (159s) · selftest 88s
selftest: 96 PASS / 1 FAIL          <- same tally as the record
```

Diffing my 97 check lines against the committed `selftest_L1_exit.txt` line-for-line:
**96 of 97 are character-identical.** Same store `81d24704`, same `rl_model 3b011802`, same
`fv 461c737b`, same contract `ca2f2e87…`, same curve payload `e69a3f38`, same `per_entrant 77eba4d3`,
F1 mismatches **0**, 804 active players, all six FROZEN-RULER checks green, sealed history untouched.

**The one line that differs is the acceptance gate:**

```
record : FAIL G-Y0 ceiling: live 19.869%
mine   : FAIL G-Y0 ceiling: live 13.919%
```

**5.950 percentage points, attributable to `v0surf.pkl` and nothing else** — because by (c) nothing
else differs.

**(e) G-Y0 = 13.919% is STABLE here, not noise.** An independent second board build + selftest on the
same tree reproduced **13.919%** and **96 PASS / 1 FAIL** exactly. So the figure is container-specific
and deterministic, not a wobble.

**(f) HOW FAR THE BOARD ACTUALLY MOVES.** Comparing the predecessor's committed
`f1_single_g10.json` against the same measurement re-run here (`f1_decide.py single`, γ=1.0, fresh
process). F1 reported `mismatches=0` in **both** containers, so each file equals its own board — this
is a board-to-board comparison, not a recompute artefact.

```
MOVERS: 173 of 804 (21.52%)     7 up / 166 down
median |delta| 10 | max |delta| 79 | median |rel| 8.732% | max |rel| 16.667%
total ev 798,003 -> 795,167  (-0.3554%)
```

**Where the movers sit is the evidence for the attribution** — generic BLAS drift would smear across
the whole board; this does not:

| decile (by the record's ev) | ev range | movers | max \|rel\| |
|---|---|---|---|
| 1 | 2,603–12,506 | **1 / 80** | 0.23% |
| 2 | 1,593–2,599 | 1 / 80 | 1.19% |
| 3 | 975–1,580 | 3 / 81 | 1.45% |
| 4–7 | 198–975 | 88 / 321 | ≤12.77% |
| **8–10** | **0–198** | **80 / 242** | **16.67%** |

**354 of the top 402 are byte-unchanged.** The highest-valued mover is `noah-mraz` at 4,277 → 4,267
(−0.23%), against a board top of 12,506 which does not move at all. The divergence is concentrated in
the low/no-production tail — which is the **V0 (year-zero) surface's own domain**, and G-Y0 is the
year-zero gap metric. One coherent story, measured rather than argued.

**(g) This box.** Intel Xeon @2.80GHz, `AVX512_SKX` / `AVX512_CLX` (6 AVX-512 feature flags), numpy
2.4.4 with the bundled OpenBLAS byte-pin `05c9f9eb` asserted green by `bootstrap.sh` — i.e. **the
pinned stack matched exactly and the surface still differs.** The pins are not the gap.

---

## 3 · WHY THIS IS THE ONE ARTIFACT IT SHOULD NOT HAVE BEEN

`refit_v0surf.py`'s own docstring records the defect the freeze exists to prevent:

> `_build_v0_curve()` used to RE-FIT the shipped V0 pick-curve surface … at every board/gate/panel
> import. numpy's OpenBLAS is DYNAMIC_ARCH, so **the same commit produced a slightly different
> surface per CPU on a mixed fleet — the whole board shifted coherently** (item 380).

The remedy was to compute it **once** and ship the frozen artifact. That remedy holds only while the
artifact travels. `L1_amended_state.diff` records `Binary files … differ` with **zero** `GIT binary
patch` sections, so the artifact did not travel — and a successor container re-fits its own, which is
the pre-item-380 behaviour reappearing inside the rehearsal chain.

**This is not a defect in the predecessor's L1 work.** L1 exits on its own terms and every identity it
moved reproduces here exactly. It is a gap in what the evidence chain carries.

---

## 4 · WHAT IT DOES AND DOES NOT AFFECT

**Does not affect L2's window comparison.** The L2 measurement runs a file-open audit hook over its own
process and records every path it touches: `v0surf.pkl` is **never read**. Both candidates are measured
on one substrate inside one container, so the A-vs-B comparison — which is what the window word turns
on — is independent of this divergence. Recorded in `l2_window_candidates.json` under
`portability_audit`.

**Does affect anything that quotes G-Y0 as a number.** The 19.869% waypoint in Addenda E–I and in
CURRENT_STATE v43 is a **container-specific** measurement, not a property of the tree. More seriously,
**acceptance 1 is `G-Y0 ≤ 2.000% at the converged fixed point`** and L6 measures G-Y0 every pass — so
the gate the whole job is steering toward is, today, container-dependent by ~6 points at L1.

---

## 5 · WHAT I DID NOT DO

I did not re-spec, relax, or work around any gate, and I am not proposing to. H.3's lesson is on the
record: the last seat proposed weakening a gate that was working, and the gate was right. This finding
is reported for the seam to rule on; I have taken no remedial act.

I also cannot say from here whether `e92e3885…` or `84fb0cde…` is the "right" surface. Neither is
privileged by anything I measured. That is the question, not the answer.

---

## 6 · REPRODUCTION

```
git apply --exclude=data/v0surf.pkl docs/evidence/rehearsal_290_2026-07-31/L1_amended/L1_amended_state.diff
python3 -c "import json;p='data/expected_boot.json';b=json.load(open(p));b['v0surf']='ce08c2d13ae7d9bd403c60cf58ea1660';open(p,'w').write(json.dumps(b,indent=2)+'\n')"
bash setup_env.sh && bash bootstrap.sh
cd /home/claude/rl_workspace/rl_after
RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --bake
md5sum $RL_REPO/data/v0surf.pkl        # assert == e92e3885df24060aa90557ba20ba3612
```

Every engine act above ran strictly serially behind `tools/preboot_assert.sh`, re-proven in this
container in both directions (PASS with none live; HALT naming both pids with two live; PASS again
after cleanup).
