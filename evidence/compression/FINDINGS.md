# COMPRESSION / SPREAD QUANTIFICATION — FINDINGS

**State: all numbers `[BAKED c47cb43d]`** · READ-ONLY diagnostic · no engine change, no bake.

## STEP 0 — asserts (BLOCKING, passed)

- working head `389ac39` (v2.4 bake STEP 6). *(local `main` label still on seed `f4a4d34`; the baked head under measurement is 389ac39.)*
- engine `_merged_recover.py` md5 = **c47cb43d** ✔ (== required; bootstrap's "expect 8aed420a" is the pre-bake baseline)
- board `data/s4_matrix_baked_c47cb43d.json` — 2649 players ✔

## What was measured

Value field **V := `cur`** = the live keeper value the owner ranks on (Vpath[-1]; ≈ engine `ev()`, median diff 1 vs live recompute). `peakV = max(Vpath)` is the age-neutral valuation. Realised reference **R** = era-normalised production (engine's own `era`/`REF`, md5 c47cb43d): `recentP` (last-2 seasons), `peakP` (best season), `careerP` (season-sum). Primary population = **LIVE keeper board** (`retired_now==False`, n=794).

**Traps handled:** *value≠scoring* — value is a legitimate convex/keeper transform of production, so we measure RELATIVE spread + local rank-fidelity, not raw $. *Survivorship* — the realised reference uses a settled cohort with EVERY drafted player, busts at ~0 (never survivors-only). *State* — every figure labelled, populations printed.

---

## HEADLINE — the compression is LOCALISED, not uniform, and NOT a global-scale problem

Against a survivorship-aware realised reference, the value **scale** is not compressed — it is if anything **expanded**. Settled 2008–2016 ND cohort (n=647, 18% busts included at ~0):

| spread | realised `peakP` | engine `peakV` | realised/engine |
|---|---|---|---|
| p99/p50 | **1.86×** | **7.02×** | 0.26 |
| p99/p90 | 1.27× | 1.61× | 0.79 |
| spearman(peakP,peakV) | — | — | **0.882** |

The engine turns a 1.86× realised peak-production spread into a 7× value spread, and separates elite-from-good *more* than reality (p99/p90 1.61 vs 1.27). Rank agreement is strong. **=> Do NOT globally widen the scale.**

The compression the owner correctly perceives is **local**: value stops tracking production among **same-stage / aging elites**.

---

## 1. Distribution shape `[BAKED c47cb43d]` (LIVE board, V=cur)

| pop | n | p50 | p90 | p99 | p90/p50 | p99/p50 | p99/p90 (top-end) | topdec/nextdec |
|---|---|---|---|---|---|---|---|---|
| OVERALL | 794 | 368 | 2092 | 5058 | 5.68 | 13.73 | 2.42 | 2.07 |
| MID | 190 | 806 | 3449 | 5842 | 4.28 | 7.25 | 1.69 | 1.61 |
| RUC | 54 | 548 | 2074 | 6204 | 3.78 | 11.31 | 2.99 | 2.24 |
| KEY_FWD | 99 | 378 | 1508 | 3987 | 3.99 | 10.55 | 2.64 | 1.99 |
| GEN_FWD | 184 | 224 | 1244 | 2847 | 5.55 | 12.71 | 2.29 | 2.19 |
| KEY_DEF | 92 | 256 | 1518 | 2828 | 5.94 | 11.07 | 1.86 | 1.78 |
| GEN_DEF | 175 | 355 | 1686 | 3736 | 4.75 | 10.52 | 2.22 | 1.78 |

Overall spread is wide (p99/p50 ≈ 13.7×). MID is the flattest top-end (p99/p90 1.69, topdec/nextdec 1.61) — the elite MIDs sit closest together; RUC the widest (small-n, ceiling outliers).

## 2. Elite separation — actual $ gaps `[BAKED c47cb43d]`

**Petracca vs Bontempelli (owner flag):**
- Bontempelli `cur=3085`, recentP=**129**, peakV=6830 (pick4, 2013)
- Petracca `cur=3033`, recentP=**107**, peakV=5055 (pick2, 2014)
- **VALUE gap = $+52 (+1.7%)** while Bont **out-produces Petracca by +20%**. Production says Bont clearly ahead; `cur` has them tied. → sharpest confirmed compression.

**Elite KEY_FWD cluster vs next tier:**
| player | cur | recentP | peakV | pick / yr / nseas |
|---|---|---|---|---|
| Josh Treacy | 5156 | 93.7 | 5156 | 66 / 2020 / 6 |
| Sam Darcy | 3963 | 92.1 | 5231 | 2 / 2021 / 5 |
| Riley Thilthorpe | 3347 | 89.2 | 5223 | 2 / 2020 / 6 |
| Cooper Duff-Tytler | 1436 | 49.5 | 1436 | 4 / 2025 / **1** |
| Jonty Faull | 1134 | 38.9 | 1134 | 14 / 2024 / **2** |

- within-cluster spread **$1809 (1.54×)** on ~5% production spread; cluster-vs-next-tier **$1911 (2.33×)**.
- **This cluster is NOT compressed** — it is adequately/generously separated (value spreads them *more* than production). *Caveat: Duff-Tytler/Faull are on projection anchors (nseas 1–2), so cluster-vs-next-tier is projection-vs-realised, not like-for-like.*

**Top-8 clustering:** MID #1→#2 gap $307 (Sheezel 7076 / Daicos 6769), then ~$361/step down to #8 (4603) — young MID top is well-graded. KEY_FWD #1→#2 gap $1193.

## 3. The real locus — LOCAL rank-fidelity fails in the aging-elite regime

`spearman(recentP, cur)` within same-age bands (established, nseas≥4):

| career age | n | spearman | retention (cur/peakV) p10–p90 |
|---|---|---|---|
| 0–4 yr | 119 | 0.78 | 0.26–1.00 |
| 5–7 yr | 132 | 0.77 | 0.05–1.00 |
| 8–10 yr | 128 | 0.82 | 0.03–0.70 |
| 11–20 yr | 104 | **0.75** | 0.02–0.49 |

Aging elites (age 11–15, recentP≥100, n=15): production spread only **1.31×** but value spread **3.62×**, spearman 0.71 — and the scatter is driven by **retention (cur/peakV) swinging 0.21–0.83 with no production alignment**: the two *top* producers (Grundy 131 / Bont 129) retain only ~0.42–0.45, while lesser producers (Sinclair 117 @0.83, Dale 104 @0.65) retain far more. **The age/decay-retention term scrambles the production order — this is where value collapses production-justified gaps.**

## 4. Tail steepness `[BAKED c47cb43d]` — steep, not shallow

Fresh ND draftees (2023–26, ≤1 season, value=anchor=pick curve, n=61):

| pick~ | 1 | 3 | 5 | 10 | 20 | 30 | 40 | 60 |
|---|---|---|---|---|---|---|---|---|
| implied anchor | 2325 | 1952 | 1678 | 1518 | 810 | 584 | 376 | 143 |

**pick~1 vs pick~60 = 16.3×** (3019 → 185). The tail is **steep, not too shallow**. The only flattish stretch is **picks 1–10 (within ~1.5×)** — mild top-of-draft bunching — then a steep decline through the tail.

---

## VERDICT — UNIFORM vs LOCALISED: **LOCALISED**

| region | reads as | evidence |
|---|---|---|
| Aggregate scale / mid-tier | **not compressed — expanded** | value p99/p50 7.0× vs realised 1.9×; spearman 0.88 |
| **Aging elites (11–15 yr)** | **COMPRESSED — value decoupled from production** | Petracca≈Bont (+1.7% value / +20% prod); retention 0.21–0.83 unaligned; within-band spearman 0.71 |
| Young/mid establishing | fine | spearman 0.78–0.82, well-graded top-8 |
| Elite KEY_FWD cluster | not compressed (adequately separated) | 1.54× internal, 2.33× over next tier |
| Draft tail | steep (16.3×), fine | flattish only at picks 1–10 |

**Where the overhaul must act:** the **age/decay-retention transform for established/aging elites** — it collapses still-elite veterans into a common ~2.5–3.3k band and loses the production ordering (Petracca/Bont). It should **not** globally rescale the board (the aggregate scale already separates elites *more* than realised outcomes justify), and it should **not** widen the draft tail (already 16×).

## Reproduce

```
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 \
       RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22 \
       PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
python3 evidence/compression/build_dataset.py   # engine era/REF + board -> dataset.json
python3 evidence/compression/metrics.py         # shape, transfer, elite gaps, tail  -> metrics_report.txt
python3 evidence/compression/localise.py         # aggregate-vs-local, age control    -> localise_report.txt
```

Outputs committed: `dataset.json`, `era.json`, `metrics_out.json`, `metrics_report.txt`, `localise_report.txt`.
