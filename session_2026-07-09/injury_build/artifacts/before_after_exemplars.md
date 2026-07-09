# BEFORE / AFTER — Chapter-3 injury build exemplars — 2026-07-09
### Board value ev(2026). "baked v2.6" = the pre-chapter board (head 4b08796c, git b303795, WITH _b2hc).
### "strip" = _b2hc retired, RL_AVAIL off (layer-off baseline). "candidate" = RL_AVAIL + RL_LTI_RETURN on
### (values from the candidate board; gate-mode shipped board is byte-equal within ≤1 on a couple of rows).
### The whole movement is confined to register names + their KPFFIX interactions; every non-register player
### is byte-identical (non-mover parity — proven separately: nonmover_parity.txt, 0 non-register movers).

| player | key | baked v2.6 | strip (b2hc off, layer off) | candidate (layer on) | net vs baked | attribution |
|---|---|---|---|---|---|---|
| Connor Rozee | connor-rozee | 3019 | 3019 | 2271 | −748 | Section B: avail_nerf (nil 2026, L=0.91); NO return haircut. Feeds A3 (DATA-CAUSED red, R-A3 uphold) |
| Sam Darcy | sam-darcy | 4470 | 4470 | 3825 | −645 | A-DARCY: avail_nerf only (6 final 2026 g, L=0.73); **lti_return_hc=0 (young, shipped zero); young-convexity ceiling + KPF-speculative loci byte-identical (fork-v kept LD on healthy 2024/2025)** |
| Nic Martin | nicholas-martin | 3266 | 3516 | 2809 | −457 | _b2hc strip +250 (removed inference), then register avail_nerf (L=1.0); may_return_2026 default OUT (R-iii) |
| Tom Green | tom-green | 4885 | 5222 | 4165 | −720 | _b2hc strip +337 (removed inference), then register avail_nerf (L=1.0, out whole 2026) |
| Reef McInnes | reef-mcinnes | 76 | 76 | 76 | 0 | repeat-LTI (2 independent windows, fork-ii); at floor — availability doesn't move him; report-only repeat_lti flag |
| Lewis Hayes | lewis-hayes | 360 | 360 | 358 | −2 | repeat-LTI (2 independent windows, fork-ii); report-only repeat_lti flag |
| Nick Daicos | nick-daicos | 7626 | 7626 | 7626 | 0 | non-register — byte-identical (parity witness) |
| Marcus Bontempelli | marcus-bontempelli | 3524 | 3524 | 3524 | 0 | non-register — byte-identical (parity witness) |
| Max Gawn | max-gawn | 2413 | 2413 | 2413 | 0 | non-register — byte-identical (parity witness) |

## A-DARCY triple-locus (mandatory attribution)
- **young_convexity_ceiling** — UNTOUCHED (fork-i-a holds his games-clock; the layer never clips the ceiling).
- **kpf_speculative** — UNTOUCHED (young/speculative exemption + fork-v-a keeps his LD on healthy 2024/2025).
- **availability_layer** — REAL and the ONLY mover: `avail_nerf` = −645 (his 6 final 2026 games, L≈0.73);
  `lti_return_hc` = **0 (young cell nets to ~zero — shipped zero per the A-DARCY "absence is a finding" doctrine)**.
- Direction: DOWN vs baked, entirely via the availability locus (lost 2026). **Owner-on-sight** — the ceiling
  is demonstrably unclipped; this is the injury priced, not a fade.

## _b2hc retirement parity note
`_b2hc` fired on exactly {nicholas-martin, tom-green} on store a2fbc9a0 — BOTH register names. Retiring it
moves ONLY those two UP by the removed haircut (Nic Martin 3266→3516, Tom Green 4885→5222); the register
layer then re-prices them. No non-register player carried _b2hc → the strip is register-only. Non-register
parity holds across the whole chain: baked → [b2hc strip] → [RL_AVAIL on] → candidate.
