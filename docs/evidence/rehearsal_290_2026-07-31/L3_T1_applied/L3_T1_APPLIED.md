# L3 — T1 APPLIED. Gates green. Watched number invariant.

**#290 L3, 2026-07-31.** Owner treatment word: **T1**. Applied, verified, gated.

## THE WORD, AND WHAT WENT IN

T1 = each tenure cell taught only by classes **observable** at that tenure; **no fabricated zeros**;
**no relabel**. Implemented in `conditional_prior.build_cond_prior`: a training row is skipped when
`d0 < Y < first_observable_season()`. `first_observable_season()` is **derived from the store**
(measured 2005), never hardcoded, so it stays true if coverage changes. The **draft-year row
(`Y == d0`) is KEPT** — a real zero by design, not a fabricated one. Limb 2 (the tenure re-anchor)
was measured and **NOT taken**: tenure keeps its true elapsed-time meaning.

**Residual, recorded as a named referee-era refinement** (seam): the cumulative features
`_exposure` and `_lvl_eff` still integrate across the unobservable span. T1 removes the fabricated
rows, not that residual.

## VERIFIED EXACT AGAINST THE MEASUREMENT

| | |
|---|---|
| training rows | **13,157** (T0 13,221 − **64**) |
| rows dropped | **64** — all draft class **2003**, all season **2004** |
| draft-year rows dropped | **0**, by construction (`d0 < Y`) |
| bands vs the measured T1 | **0 mismatches of 804**, max diff 0 |

The applied word **is** the treatment that was measured — not a re-implementation of it.

## THE C.1 IDENTITY HAZARD FIRED, AS AT L1

One line in `engine/forward_valuation/conditional_prior.py` moved the fv identity and Guard 5
refused to boot. Re-pinned in **both** carriers in the same act (the 8/8 mirror):

```
expected_boot.fv            461c737b… -> 95277b76…
release_contract.identities.fv  461c737b… -> 95277b76…
```

**Field-level, proven:** `expected_boot` differs from the committed L1-exit intent in exactly **two**
keys (`fv`, `v0surf` — both intended); `release_contract` in exactly **one** field
(`.identities.fv`). **Sealed history untouched:** the ten historical `45b207c0` occurrences unmoved —
`release_lineage.json` 4|4|4, `finalization_state.json` 6|6|6. The five changed lines carrying that
hash are only the live carriers C.2 says must move.

## GATES

```
bootstrap 0 · board 0 (114s) · book 0 (145s) · selftest 76s
selftest: 96 PASS / 1 FAIL — the single fail is G-Y0 13.919%, the accepted waypoint
```

| | |
|---|---|
| board `rl_app_data.json` | `1432f5e4…` → **`92e397bd…`** — the board MOVED |
| **G-Y0** | **13.919% → 13.919% — UNCHANGED** |

**Both facts matter and they are not in tension.** T1 moves the pedigree prior, which feeds player
valuation, so the board moves. G-Y0 measures the year-zero pick-curve residual, governed by the
frozen v0 surface and the curve — which T1 does not touch. **So T1 buys nothing toward the 2.000%
acceptance bar.** That closure remains L6's convergence job, and a green gate here must not be read
as progress toward it.

## THE WATCHED NUMBER — re-measured on the T1 substrate, not assumed

The matrix was **re-emitted through the declared emitter on the T1 substrate** (165s, same
backup → emit → capture → restore, restore proven by md5, `git` clean).

| | |
|---|---|
| T1 matrix md5 | **`a216e6e647ffbbdb992bfcb9d397fb52`** — **byte-identical to the pre-T1 ruled matrix** |
| fallback share | **5.931% = 71/1,197** |
| counts | `concluded_realised 825 · completed 301 · prior_fallback_thin 71` |
| **delta vs pre-T1** | **0.000 pp** |

**T1 leaves the ND matrix byte-identical**, and the mechanism is worth stating: the matrix carries
structural fields (`teaches_curve`, `pick`, `year`, `pos`, `vpath`, `v0`, `retired_now`) derived from
realised career paths and the pick curve — **not** from the conditional prior. The 71 fallback rows
read `r['v0']`, the year-0 **structural** value, not the pedigree band. So the watched number is
**invariant to T1 by construction**, and the re-measure confirms it rather than assuming it.

## THE STATE DIFF CARRIES ITS BINARY — the v0surf lesson applied

`L3_T1_state.diff` is generated with **`git diff --binary`** and contains **1 `GIT binary patch`
section** for `data/v0surf.pkl`. `L1_amended_state.diff` contained **zero**, and that single omission
is what produced the entire v0surf divergence episode. **Proven to round-trip:** applied to a clean
checkout of `HEAD`, it reproduces `data/v0surf.pkl` at **`84fb0cde29f36c1a91d440e63b753c3c`** —
byte-exact to the ruled frozen surface — with T1 present and `expected_boot.fv` at `95277b76`.
18 files, 142,345 bytes.

## TWO MISTAKES OF MINE, BOTH CAUGHT BY MEASURING

1. **The first re-pin rewrote the JSON wholesale** (`json.dumps(indent=2)`), reformatting all 37
   lines of `expected_boot.json` instead of one field — a **C.2 violation**, since a config/identity
   re-stamp is a field-level act. Caught by diffing the result rather than trusting "I changed one
   field". Redone byte-surgically (literal replace, one occurrence asserted per file).
2. **Reverting it, I ran `git checkout --` on files whose L1 state was uncommitted working-tree
   content**, discarding the L1 patches. Fully recovered by re-applying the committed
   `L1_amended_state.diff` — which is exactly the property the freeze law exists to guarantee, paying
   out on the same day it was ruled.

Neither reached a commit. Both are recorded because the recovery, not the slip, is the reusable part.

## WHAT L3 STILL OWES

**Carrying S-1/S-2's structural completion into the derivation path.** Measured position: the logic
lives in `harness_pvc_REPINNED.py:110-152` — an *evidence script* — and its input is now committed
beside it. The engine loads a **frozen** curve; the derivation itself happens in the session scripts,
so "the derivation path" is where L6's convergence will re-derive the curve. **Not attempted here**:
it is a structural move at the end of a long seat, and this seat has already produced two self-caught
slips today. Scoped and handed back rather than rushed.
