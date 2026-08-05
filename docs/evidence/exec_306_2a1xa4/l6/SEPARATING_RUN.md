# #306 L6 — THE SEPARATING RUN · **THE ENGINE CONTRIBUTES EXACTLY NOTHING. THE EFFECT IS ALL SURFACE.**

**Seat `2a1xa4`, 2026-08-05.** Act 1 of the two ordered acts
([#306 comment 5186820918](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5186820918)),
run before the pass-1 install per the sequencing amendment. Bake held; EXECUTION word withheld; nothing landed.

---

## 1 · THE RESULT — byte-identity, which is a stronger answer than an attribution

Emitted one matrix with the **old surface `fb9efdec` installed under the lens engine `15525b03`**:

```
separating emit  (old surface fb9efdec · LENS engine 15525b03)  ->  9c4bca53b738452739c353d94fe99928
#290 committed   (old surface fb9efdec · OLD  engine 3c7b0c3c)  ->  9c4bca53b738452739c353d94fe99928
cmp: no difference · 3,241,031 bytes both
```

**The two are byte-identical.** At a fixed surface, the lens engine and the pre-lens engine produce the
same matrix down to the byte.

**Therefore the engine's contribution to the teaching values is exactly zero, and 100% of the movement
measured at the pass-0 verdict is the surface.** The confound the earlier filing carried as a caption is
not merely bounded — it is **dissolved**. Every figure in the channel decomposition is a surface effect,
cleanly isolated.

**Why, from the mechanism** (so this reads as explicable rather than lucky): the surface is frozen and
**loaded**, never fitted at board/matrix build — `v0surf_frozen: true`. The lens changes how the surface
is **fit** (`RL_V0_LENS` gates the fit path in `_merged_recover.py`). The matrix emit never exercises the
fit path, so at a fixed surface the two engines are the same compute. That is exactly what N16's freeze
was built to achieve, observed working.

**Consequence for the record:** the caption required by ruling 4 on every use of the pass-0 channel
numbers — *"surface and engine moved together; total effect, attributes nothing"* — **is now discharged
and should be replaced** with: *the engine contributes zero; these are surface effects, isolated by the
separating run.*

## 2 · THE BELIEF-MASS MEASUREMENT — the seam's clause-3 question, answered

The channel decomposition was a **derivative** (what moved). This is the **mass** (how much of the level
is the model's opinion). Both matrices below differ only in surface, per §1.

### The true mass — share of total basis VALUE by provenance
The order's 5.931% is a share of **row count**; the belief question asks about **value**.

| provenance | rows | value (lens `b540833b`) | share | value (old `fb9efdec`) | share |
|---|---|---|---|---|---|
| `concluded_realised` | 825 | 562,107.5 | 54.74% | 566,723.0 | 54.63% |
| `completed` | 301 | 401,347.9 | 39.08% | 402,811.6 | 38.83% |
| **`prior_fallback_thin`** | **71** | **63,422.6** | **6.18%** | **67,884.9** | **6.54%** |
| TOTAL | 1,197 | 1,026,878.0 | 100.00% | 1,037,419.5 | 100.00% |

**The wholesale-belief mass is 6.18% of the teaching signal by value** (6.54% under the old surface) —
value the model supplies outright, with no career evidence behind it. Close to, and slightly above, the
5.931% count share.

### The lower bound on prior-shaping inside evidence-backed rows

| provenance | lens | old | delta | delta % |
|---|---|---|---|---|
| `concluded_realised` | 562,107.5 | 566,723.0 | −4,615.5 | **−0.81%** |
| `completed` | 401,347.9 | 402,811.6 | −1,463.7 | **−0.36%** |
| `prior_fallback_thin` | 63,422.6 | 67,884.9 | −4,462.3 | **−6.57%** |
| TOTAL | 1,026,878.0 | 1,037,419.5 | −10,541.4 | **−1.02%** |

Evidence-backed rows (concluded + completed, 1,126 rows) moved **−0.63%** on a surface change alone.
**That is a FLOOR on how prior-shaped their level is — under one particular surface perturbation — and it
is not the model-shaped fraction of the level.** Quantifying that fraction needs a no-prior pricing mode
the engine does not have; saying more than this would be the over-claim clause 3 warns against.

### The plain answer to the question asked
**The basis is not materially belief-driven.** About **6% of the teaching signal by value** is the model's
opinion outright; the other ~94% is evidence-backed, and that evidence-backed level shifts by well under
one percent when the prior underneath it moves substantially.

**This does not retract the channel finding and does not soften it.** Both hold, and they measure
different things: 44.22% of total **absolute movement** flows outside the 71 counted rows — the channel is
genuinely wide, the narrow story is still wrong — while in **level** terms that outside movement is small
(−0.63%). Wide channel, modest mass. Naming both is the point; either alone misleads.

## 3 · DISCIPLINE — backup → swap → emit → capture → restore, all proven

| act | proof |
|---|---|
| backup | `v0surf.pkl` `b540833b` · `expected_boot.json` `28666b18` · `per_entrant_271.json` `2f8b4bd4` |
| surface source | the **committed** frozen artifact `…/L6_convergence/pass0_surface/v0surf.pkl`, verified `fb9efdec` with its `IDENTITY.json` |
| re-pin | `expected_boot.v0surf` → `fb9efdec`, **surgical string replace, no reformat**; occurrence count checked **before** touching (exactly 1, at the `v0surf` key; `fb9efdec` absent) |
| Guard 5 | PASS on engine `15525b03`, store `81d24704` |
| emit | 187s |
| **F-C binding** | installed surface at emit = `fb9efdec…` = `expected_boot.v0surf`. **The emitted sig is `96d671c952c8` — identical to the lens emit's.** Only the full md5 distinguishes the two matrices; the signature cannot. F-C earning its keep, concretely. |
| restore | all three restored and re-hashed: `b540833b` / `28666b18` / `2f8b4bd4` |
| round trip | substrate minus the authorised re-pin re-hashes to **`2b7640be`**, before and after |

**N35:** the container restarted a **fourth** time before this act; re-classified in full — `fb9efdec`
reproduced in 74s (entry 4) — before the emit. No figure produced on a stale classification.

## 4 · REPRODUCING

```
python3 belief_mass.py   l6/pass0_lens_matrix.json  l6/sep_oldsurface_matrix.json
python3 channel_width.py l6/pass0_lens_matrix.json  l6/sep_oldsurface_matrix.json
cmp l6/sep_oldsurface_matrix.json <#290>/L6_convergence/pass0_matrix.json    # byte-identical
```
Instruments and outputs committed beside the matrices, with `sep_matrix_identity.json` carrying the
identity block and the F-C binding.
