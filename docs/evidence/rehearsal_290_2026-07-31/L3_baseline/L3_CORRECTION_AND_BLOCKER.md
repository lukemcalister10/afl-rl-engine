# L3 — a CORRECTION to my own baseline, and a BLOCKER on the watched number

**#290, L3, 2026-07-31.** Filed before proceeding, because L3 would otherwise be built on a wrong
premise of mine.

---

## 1 · CORRECTION — I conflated *teaching* the prior with *receiving* it

**What I filed** (comment 5141734922, §3): *"`build_cond_prior` trains on all 1,930 resolved careers,
so 1,572 (81.45%) currently teach a prior S-1 retires from them."*

**That framing is wrong.** S-1 says the prior is retired **from** concluded careers — it is about
**where the prior is APPLIED**, not about what teaches it. Training on concluded careers is not a
defect; it is the point. They are the resolved evidence the prior is learned from, and the same
concluded population supplies S-2's actuarial completion strata.

**Measured, on the L1-exit tree:**

| | |
|---|---|
| live board population (`MA.players`) | **804** |
| of those `_retired` | **0** |
| of those delisted (`_last_listed < 2026`) | **0** |
| **concluded careers on the live board** | **0** |

`_retired` / `_last_listed` are read in the engine only for **board eligibility**
(`rl_model.py:714-715`, `_merged_recover.py:1060`) — never for the prior's weight.
`distribution_pricing.shrunk_band` blends by `w = n/(n+k_shrink)` on **evidence density alone**.

**So the prior is never applied to a concluded career on the live board — S-1's application
requirement is structurally satisfied there.** The 1,572/358 split is a true and useful count of the
training population; it is **not** a count of an S-1 violation. Withdrawn as framed.

**Where S-1 actually bites** is where concluded careers *are* valued: the **curve-teaching**
population (the harness ND set, denominator 1,197). The step-4 harness already implements S-1/S-2
there correctly. So L3's real gap is narrower and different from what I filed:

> **S-1/S-2's structural completion exists only in a step-4 rehearsal *evidence script*
> (`harness_pvc_REPINNED.py`), not in the engine's own derivation path.** Carrying it across is
> L3's work. The ruled basis (N2: STRUCTURAL · class ≤2022 · par per-season) must live where the
> curve is derived, not only in a harness.

## 2 · BLOCKER — the watched number cannot be re-measured as things stand

L3 owes *"the thin-stratum fallback share with its denominator (baseline 5.931% = 71/1,197) — a
WATCHED NUMBER"*. It is produced by `harness_pvc_REPINNED.py`'s `structural_values()`
(`prior_fallback_thin` + `prior_fallback_no_written`, over `len(ND)`, with an assert that the three
provenance classes sum to the population). Re-running it is blocked twice over:

| the harness pins | value | the L1-exit substrate carries |
|---|---|---|
| `EXPECT_STORE` | `81d24704` | `81d24704` — **matches** |
| `EXPECT_V0SURF` | **`12d903336f6e`** | **`96d671c952c8`** — **does not match** |

`12d90333…` matches **neither** the L1-exit signature **nor** the pre-L1 one (`76498b5a…`). And:

> **No file carrying that identity exists anywhere in the tree.** The harness takes its ND matrix as
> `sys.argv[1]`; that matrix is **not committed**. `load_matrix()` asserts both identities on entry,
> so the harness cannot run here at all.

**Consequence:** the 5.931% = 71/1,197 baseline was measured on a substrate that is neither in the
tree nor reachable from it, and the WATCHED NUMBER has no committed input to be re-measured against.

## 3 · WHAT I HAVE NOT DONE, AND WHY

The obvious unblock is to re-emit the ND matrix on the L1-exit substrate and re-pin `EXPECT_V0SURF`.
**I have not done it.** `load_matrix()`'s pin is a gate, and editing a gate's expected value so that
it passes is precisely the H.3 trap this job has already paid for once — the last seat proposed
re-speccing F1 to trust what it checked, and the gate was right.

The lawful path, **proposed not performed**: re-emit the matrix through the declared emitter on the
L1-exit substrate, re-pin `EXPECT_STORE` / `EXPECT_V0SURF` / `EXPECT_N` as a **disclosed** act with
the old and new values both recorded, and re-measure the fallback share with its denominator. That
moves a pinned identity in a committed evidence harness, so it wants a word.

Until then the watched number stands as a **pre-L1 figure with a named substrate**, per the standing
rule that every such number names the surface it was measured on.

## 4 · UNAFFECTED

Bias-1's scoping (214 draft-year rows by design vs **64** genuine phantoms of 13,221 = 0.484%, plus
the separate tenure-offset limb over all 641 of the class's rows) is measured from
`build_cond_prior`'s own emission and does **not** depend on the harness. Both limbs remain L3's to
measure and present, nothing chosen silently.
