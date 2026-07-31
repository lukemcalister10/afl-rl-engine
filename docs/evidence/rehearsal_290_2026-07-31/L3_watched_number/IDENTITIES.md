# L3 — the watched number, unblocked. Identities beside the input, as ruled.

**#290 L3, 2026-07-31.** Seam ruling: one disclosed act. **The freeze law generalised — a
pinned-input instrument's input is COMMITTED, or its emitter and substrate are both reachable from
the tree.** This directory is that input.

## THE COMMITTED INPUT

| | |
|---|---|
| file | `nd_matrix_ruled.json` |
| **md5** | **`a216e6e647ffbbdb992bfcb9d397fb52`** |
| size | 3,241,153 bytes · 2,646 recs |
| **`meta.store_md5`** | **`81d24704`** — the ruled substrate |
| **`meta.v0surf_sig`** | **`96d671c952c819fa64df0b5d1a402f1e`** |
| `meta.v0surf_frozen` | `True` |
| emitter | `session_2026-07-29/item271/emit_matrix_271.py`, the declared one, **179s** |
| substrate | reconstructed L1-exit tree · store `81d24704` · frozen v0surf **`84fb0cde`** |

## THE RE-EMIT WAS NOT AN IN-PLACE WRITE

The declared emitter writes to `session_2026-07-29/item271/out/per_entrant_271.json`, which is live
at md5 **`2f8b4bd4`** and is **provenance-cited** by `engine/rl_after/pvc_curve_v2.json`
(`derived_from`, `per_entrant_path`). It is also one half of the never-conflate `per_entrant` pair
the runbook names. So the act ran **backup → emit → capture → restore**, and the restore is **proven
by md5, not assumed**:

```
pre-emit   2f8b4bd4df55217f19c716f68e310b40
post-emit  a216e6e647ffbbdb992bfcb9d397fb52   <- captured here as nd_matrix_ruled.json
restored   2f8b4bd4df55217f19c716f68e310b40   git status clean
```

A first attempt was killed by a 2-minute foreground timeout. The artifact was checked **before
anything else** and was intact at `2f8b4bd4` with no engine process alive — the kill landed before
any write. The retry ran in background with capture-and-restore in the same script so a kill could
not strand the tree half-written.

## THE RE-PIN — full chain, old and new recorded

```
EXPECT_V0SURF  'b781ed253bff' -> '0c75bb6d829d' -> '12d903336f6e' -> '96d671c952c8'
                |____________ step-4 container era ____________|      ruled substrate
EXPECT_STORE   '81d24704' -> '81d24704'   UNCHANGED
EXPECT_N       1197 -> 1197               RE-MEASURED, never assumed
```

`12d903336f6e` was **never documented** — the harness was born carrying it (first committed at
`f4c096f` / `592c7a2`, the step-4 STOP run; seam attribution from git). Both container-era moves
happened inside the step-4 container and neither the matrix nor the surface travelled, so
`12d903336f6e` matches nothing reachable from the tree. **Second instance of the v0surf-bytes class.**

**A fact the ruling's framing did not yet carry:** the *committed* `per_entrant_271.json`
(`2f8b4bd4`) declares `store 265f55d5` and `v0surf_sig 85e57195189b`. It satisfies **neither** pin
either. So this harness has **never had a committed input that could pass its own asserts** until now.

## EXPECT_N — RE-MEASURED, with its filter

The harness's own filter, applied to the re-emitted matrix:

| step | count |
|---|---|
| `teaches_curve` | 1,444 |
| + `pick` present, `1 ≤ pick ≤ 64` | 1,444 |
| + `2004 ≤ year ≤ 2022` (the class cut) | **1,197** |

**Delta vs the step-4-container pin: +0.** And the **key set is identical** to the old matrix's under
the same filter — **0 added, 0 dropped**. The teaching population did not move under the substrate
flip, which is what one would want: ND membership is a function of store/type/pick/year, not of the
surface. Recorded as a re-measurement, not as a confirmation of an assumption.

## THE WATCHED NUMBER — re-measured, with its denominator

```
counts: concluded_realised 825 | completed 301 | prior_fallback_thin 71
        (prior_fallback_no_written = 0)
fallback_rows 71 | of_population 1197 | fallback_share_pct 5.931
```

| | step-4 container figure | re-measured on the ruled substrate | delta |
|---|---|---|---|
| **fallback share** | **5.931% = 71/1,197** | **5.931% = 71/1,197** | **0.000 pp** |

**5.931% = 71/1,197 stands as the step-4-container figure with its substrate now named; the
re-measure becomes the current watched number, and the two agree exactly.** No material shift, so no
finding to report beyond the agreement itself. The harness's own assert that the three provenance
classes sum to the population (825 + 301 + 71 = 1,197) passed.

Also measured on this run: `never_established` true on **265 of 1,197**; mean structural value
**871.3**; folds k=5 seed=20260730 fingerprint `66d46e0103ce`, sizes 240/240/239/239/239.

**S-1/S-2 shown live in these counts:** 825 concluded careers valued at **realised full weight with
the prior retired**; 301 actives **completed actuarially** from the concluded strata; 71 falling back
to the prior, **counted, never silent** — 68.9% / 25.1% / 5.9% of 1,197.

## ASSERT NON-VACUITY AT THE RE-PIN — both directions

Full transcript in `ASSERT_BOTH_DIRECTIONS.txt`. All three identity asserts fire independently and
name the offending value:

| direction | result |
|---|---|
| ruled matrix | **PASS, exit 0** (and clean under `-W error::SyntaxWarning`) |
| wrong store (the committed pre-split matrix) | **FIRES** — `matrix store 265f55d5 != committed identity 81d24704` |
| doctored `v0surf_sig` | **FIRES** — `matrix v0surf deadbeefdead != expected 96d671c952c8` |
| one teaching row removed | **FIRES** — `ND population 1196 != expected 1197` |
