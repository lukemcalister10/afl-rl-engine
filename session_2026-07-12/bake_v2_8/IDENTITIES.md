# IDENTITIES — BAKED v2.8 · 2026-07-12 · branch claude/bake-v2-8-execution-5oyddf

The byte-identity of the baked v2.8 state. Every md5 below reproduces deterministically from the pinned
store on a clean bootstrap (verify-by-regeneration; never trust a filename — engine head 7a07e369 is
SHARED with v2.7, so the store + board + book-seal are the true disambiguators, per DECISIONS v93 §43).

| axis | md5 / identity | note |
|---|---|---|
| store | `04f38dad7c03ae2ba8d060ffdbdd1bdf` (`04f38dad`) | authoritative store, UNCHANGED from the pick-convention base c02499a3 |
| engine head | `7a07e369de93645bf900815de8328ac5` (`7a07e369`) | engine code untouched; L1 is data-only. SHARED with v2.7 |
| rl_model | `0c42d158cdb495376421ddb94e80f68f` | |
| band (cm_400) | `34faa8659cc8f19794f5cb9584fa19b2` (`34faa865`) | |
| register (LTI_REGISTER.md) | `652d83e87780e415a01a2de6d8b3cc57` (`652d83e8`) | R-REG=R2 pinned availability input |
| config | `69ead79b944d291bf8b06679e377f66d543da1061d197d2903ed85ba25c3bb8b` (`69ead79b`) | 40 model vars; RL_PVCFIT=0, RL_LTI_CLOCK=advance |
| board (rl_app_data.json) | `9ecbe0fa` | B4 byte-agree PASS (regen == shipped) |
| matrix (data/s4_matrix_baked_7a07e369.json) | file md5 `365e7a19` (id-keyed, non-deterministic by design) — **CERTIFIED identity = stable_sha256 `a19b3cb8`** | reproduces the sealed book; meta engine 7a07e369 / store 04f38dad / config 69ead79b / n=2649 |
| book-seal (stable_sha256) | `a19b3cb8b0f7eb75..` (`a19b3cb8`), n=2649 | B3 seal PASS (regen == committed seal) |
| ycred table | `daaf5e49` | L1 young-GDEF transition credit (GEN_DEF rows) |
| pick redenomination factor | `1.052440` (`1.0524`) | report-only; re-confirmed unchanged to 4dp |

## GATE VERDICT (reproduced byte-exact from clean bootstrap, 2026-07-12)
`VERDICT: FAIL=3  FEATURE=1  PASS=17  PENDING=4  STRUCK=1`
Reds **exactly {A2, A3, A12}** — the owner-ruled data-caused reds. A12 [DC] is a board test (Travaglia >
Moraes: 792 vs 1023) and stays red at 15% regardless of the read; the owner **WAIVED** the Travaglia read.
B1/B2/B3/B4/B6/D14a-c PASS · B5 FEATURE lowered=0 (raise-only) · panel 10/10 (re-pinned to board 9ecbe0fa).

## THREE NARROWEST MARGINS (class-sum convention, per the audit's note)
1. **G-COHORT y4 (BINDING, class-year-sum vs hard 1.30):** 128.6 vs 130 → **1.4 pts** — the binding
   no-arbitrage guard's narrowest; the GDEF credit lands mostly in the y1 denominator (margin WIDENS to
   8.6 pts at 12%). Class-sum walk-forward computation, asserted by code-reading (not in the automated
   ship_gates suite per CONSTRAINTS v1.6 G-COHORT).
2. **A10 Curnow decline (frozen suite, bar 0.50):** 0.55 vs 0.50 → **+0.05** — narrowest PASSING anchor
   (PROVISIONAL, data-caused; confirmed this run).
3. **A8 Berry ≥ 2× Tsatas (frozen suite):** 2.14× vs 2.00× → **+0.14×** (confirmed this run: Berry 2648,
   Tsatas 1240).

## RULING-CONFIG (asserted this run)
RL_PVCFIT=0 at all four layers (engine default · live env · export bake-guard present · guard-before-write)
+ RL_LTI_CLOCK=advance (engine default · env · manifest pin). ruling_config_check PASS.

## LINEAGE
`… → 4b08796c (BAKED v2.6) → 7a07e369 tag v2.7 (8f8c00b) → v2.8 (this bake head, engine 7a07e369 / store
04f38dad / board 9ecbe0fa / book-seal a19b3cb8)`. Tag push + main promote are **owner-only** — not done here.
