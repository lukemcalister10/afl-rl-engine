# FROZEN v0surf — the ruled substrate for L3–L8 and the landing

**Seam ruling, owner-directed, 2026-07-31: NO refit. Freeze the surface in hand.**
This file is that freeze's provenance record. The artifact is committed beside it as `v0surf.pkl`.

---

## THE ARTIFACT

| | |
|---|---|
| path when live | `data/v0surf.pkl` |
| **md5** | **`84fb0cde29f36c1a91d440e63b753c3c`** |
| **git blob** | **`2f4c3859bd34629b3ba9849e2ea32eff2b52c346`** |
| size | 49,758 bytes |
| shipped-config signature | `96d671c952c819fa64df0b5d1a402f1e` |
| surfaces frozen | **2** — `0589a2620e24e71a348988d27ab06154` and `96d671c952c819fa64df0b5d1a402f1e` (shipped) |
| status | **RULED SUBSTRATE.** L3–L8, L6's convergence measurement, and the landing all run on this. `expected_boot.v0surf` re-stamps to this md5 inside the C.1 identity set. |

## THE LANE THAT PRODUCED IT

```
RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 \
python3 session_2026-07-18/legf6/scripts/refit_v0surf.py --bake
```
run from `/home/claude/rl_workspace/rl_after` with `RL_REPO` set to the reconstructed L1-exit tree,
strictly serial behind `tools/preboot_assert.sh`. Cost **66s**; a second independent bake produced
**byte-identical** output (65s), so the lane is deterministic *on a fixed machine*.

## PRIOR IDENTITIES — both, as required

| identity | md5 | what it is |
|---|---|---|
| **prior pin, in-tree before the bake** | `ce08c2d13ae7d9bd403c60cf58ea1660` | the committed `data/v0surf.pkl` at `c49ed30` / main / `3cccb9d` — the pre-L1 frozen surface |
| **the record's L1-exit identity** | `e92e3885df24060aa90557ba20ba3612` | what the predecessor's container produced; **never committed as bytes** — `L1_amended_state.diff` carries only `Binary files … differ` |
| **this freeze** | `84fb0cde29f36c1a91d440e63b753c3c` | produced here, now committed as bytes so it never has to be regenerated again |

## THE MACHINE IT WAS FITTED ON — **host 1**

| | |
|---|---|
| CPU | `Intel(R) Xeon(R) Processor @ 2.80GHz` |
| numpy AVX-512 dispatch tiers | `AVX512_SKX`, `AVX512_CLX` (Skylake-SP / Cascade-Lake class) |
| python | 3.12.3 |
| numpy | 2.4.4, bundled OpenBLAS byte-pin `05c9f9eb` (item 392, asserted green by `bootstrap.sh`) |
| scipy / sklearn / openpyxl | 1.17.1 / 1.8.0 / 3.1.5 — 5/5 pins independently re-verified |
| threading | `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`, `PYTHONHASHSEED=0` |

**MID-SESSION HOST CHANGE — recorded because it changes what "container CPU" means here.**
After every measurement in the L2 filing was taken, and before this freeze was committed, the
container migrated hosts. Detected by `/proc/uptime` reading 97s with the working disk intact.

| | host 1 — fitted the artifact | host 2 — current |
|---|---|---|
| CPU | Xeon @2.80GHz | Xeon @2.10GHz, family 6 **model 207** stepping 2 |
| numpy AVX-512 tiers | SKX, CLX | SKX, CLX, **CNL, ICL, SPR** |

Host 2 exposes a **strictly newer OpenBLAS DYNAMIC_ARCH dispatch tier**. Every figure in the L2
filing — the two candidates, the 173-of-804 board move, G-Y0 13.919%, the two byte-identical
selftest runs — was measured on **host 1**, before the migration. The artifact was fitted on host 1.

This is why the provenance names the host explicitly rather than saying "this container": within one
session the container was two machines.

**AND THE ACCIDENT PAID FOR ITSELF — see `CROSS_MACHINE_ASSERT.txt`.** Re-running host 1's exact
state on host 2 with this surface **loaded** (never refitted) produced a **byte-identical board
(`1432f5e4…`) and a byte-identical 97-line selftest (`8d769d42…`)**, G-Y0 13.919% both, and the whole
L2 window measurement reproduced identically. So:

- the engine's **compute** path is cross-CPU deterministic to the byte once the surface is supplied;
- the **only** cross-machine sensitivity in the chain is in **fitting** v0surf — the act this freeze
  removes;
- **the ruling is validated by measurement**: with these bytes committed, L3–L8, L6's convergence and
  the landing are reproducible on any machine. The gap was never the engine; it was that the artifact
  was not carried.

## STANDING CONSEQUENCE (ruling item 3)

**Every future G-Y0 statement names the surface md5 it was measured on.** The three known values:

| G-Y0 | surface | machine |
|---|---|---|
| 3.035% | pre-L1 shipped surface `ce08c2d1`, γ=0.85 | the record's baseline |
| **19.869%** | `e92e3885` | the predecessor's container |
| **13.919%** | **`84fb0cde` — this freeze** | host 1 |

19.869% and 13.919% are **container-bound waypoints**, not properties of the tree. No gate moves.

## WHAT IS NOT DONE HERE (ruling item 2)

No deterministic-lane work. The year-zero fit's redesign — better-conditioned tail, deterministic
lane, cross-machine byte-assert — is triggered by **L6's converged G-Y0** against the 2.000% law:
fail → the redesign fires immediately as the remedy; pass → it rides the referee era's reopening.
The L6 hand-back must state the converged G-Y0 against that trigger explicitly. The seam pens the
register item.
