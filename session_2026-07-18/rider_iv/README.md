# Rider (iv) — the replacement-adjusted view · seat 13 · 2026-07-18

**REPORT-ONLY · read-only Tier-3 · DO-NOT-MERGE.** The fourth adopted ladder-viewing rider (R107.6),
computed read-only against the frozen five-migration lineage. Nothing gates, nothing merges, no value
moves. Findings for the owner's central open read (items 325/332/342), **not verdicts** — the reading
is the owner's at the ladder. Runs parallel to the Leg-E writer (disjoint files).

> **Axes note (the law, verbatim).** production bars and list-space R are orthogonal (R107.7); v2.11
> bakes GROSS either way; making v-R the traded currency is the named post-v2.11 chapter, on the
> owner's word.

## Provenance — asserted at load in `scripts/common_riv.py`, HALT-on-mismatch (silence is a red)
| input | stamp | how asserted |
|---|---|---|
| git entry (five-migration head) | `a90052add8570c014626196cc2e3e13eece02548` | `ls-remote` (FIRST_COMMANDS_PROOF.txt) + `rev-parse` in loader |
| store base | md5 `968de0c7` | md5 of `a90052a:engine/rl_after/rl_model_data.json` == curve stamp block |
| curve **payload** | md5 `89c14729` | md5 of the sorted `curve` dict of `pvc_curve_v2.json` |
| curve file | md5 `56dd7a7b` | md5 of the whole `pvc_curve_v2.json` blob |
| per_entrant | md5 `40d7da7c` | md5 of `a90052a:session_2026-07-17/legd_derivation/out/per_entrant.json` |
| R-inputs | git object | `a90052a:session_2026-07-18/five_migration/out/rider_R_inputs.json` (pick-equivalents) |
| rider-(iii) grade | PR #110 | `03cecdec:.../rider_iii_uncertainty.json` (overlaid on the deep-tail premium) |

All frozen inputs are **byte-identical** at `a90052a` and the riders-(i)-(iii) base pin `e4177c2`; this
rider reuses the riders-(i)-(iii) machinery (loader / realised-outcome convention / log-pick
adaptive-bandwidth smoother, eff-n>=35, no decile bands). No HARD-OUT file was written (engine, store,
`pvc_curve_v2.json`, `docs/`, the five-migration branch).

## Artifacts → what they answer → stamps
| artifact | job | content |
|---|---|---|
| `PLAN.md` | — | method per job + derived fence |
| `scripts/common_riv.py` | S1 | loader (stamps asserted, HALT-on-mismatch); R method; smoother; grade loader |
| `scripts/build_r_candidates.py` | 1+2 | the three R candidates + cohort-bootstrap uncertainty (seed 20260718) |
| `scripts/build_view.py` | 3 | GROSS vs v-R full board; p1/p60 & p1/p90 ratio table; deep-tail premium + grade overlay |
| `scripts/svgplot.py` | — | dependency-free SVG helper (copied from riders-i-iii) |
| `out/r_candidates.{json,md}` | 1+2 | R_curve / R_realized / R_owner, per-mechanism + pooled, bands + grades |
| `out/the_view.{json,md}` | 3 | the view tables + ratios + deep-tail premium |
| `out/view_fullboard.svg` | 3 | GROSS beside the three v-R curves, picks 1-99 |
| `out/view_deeptail_premium.svg` | 3 | v-R past ~p50 with rider-(iii) grade (right-scaled) overlaid |

## The three R candidates (findings, symmetric — no verdict)
| candidate | value | grade |
|---|---:|---|
| **R_curve** (v2 curve @ pick-eq 90/92) | **471** | rider-(iii) uncertainty 39.8% @pk90 (~2.2x the 17.4% top) |
| **R_realized** (era-matched, evidence-weighted, busts full weight, no cutoff) | **207** [16/84: 184–229] | bootstrap rel-SD ~11% pooled; 23–34% per mechanism (thin) |
| **R_owner** (item 332, reference line only) | **220** | asserted, not measured |

- **Circularity note is TESTED, not assumed** — and **refuted** under this construction: every
  mechanism entrant has `incurve=False` (0/389 in the curve's `load_pool`); pk86-94 is anchored by
  real-pick RD+ND, so R_curve is **not** self-referential on pickless outcomes.
- Era-matching cross-read: ND realised at pk88-94 = 248, which with R_realized (207) **brackets**
  R_owner (220) — all three far below the v2 list value (471).

## Thin-sample declaration (on every artifact)
MSD 44/17 played, SSP 31/16 (engine cohort); IRE/UNR/PDA/PDN/PDS 5–12 played. The per-mechanism and
pooled R_realized are **bands, not points**.

## Reproduce
`bash session_2026-07-18/rider_iv/run_all.sh` → `RIDER_IV_COMPLETE` (deterministic, bootstrap seed
20260718; re-run reproduces the committed outputs byte-for-byte).
