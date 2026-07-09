# BEFORE / AFTER — Chapter-3 injury build exemplars — 2026-07-09
### Board value ev(2026). "baked v2.6" = the pre-chapter board (head 4b08796c, git b303795, WITH _b2hc).
### "strip" = _b2hc retired, RL_AVAIL off (layer-off baseline). "candidate" = RL_AVAIL + RL_LTI_RETURN on.
### The whole movement is confined to register names + their KPFFIX interactions; every non-register player
### is byte-identical (non-mover parity — proven separately: nonmover_parity.txt).

| player | key | baked v2.6 | strip (b2hc off, layer off) | candidate (layer on) | net vs baked | attribution |
|---|---|---|---|---|---|---|
| Connor Rozee | connor-rozee | 3019 | 3019 | _TBD_ | _ | Section B: avail_nerf (nil 2026, L=0.91); NO return haircut. Feeds A3 (DATA-CAUSED red, R-A3 uphold) |
| Sam Darcy | sam-darcy | 4470 | 4470 | _TBD_ | _ | A-DARCY: avail_nerf only (6 final 2026 g, L=0.73); lti_return_hc=0 (young, shipped zero); ceiling + KPF loci byte-identical |
| Nic Martin | nicholas-martin | 3266 | 3516 | _TBD_ | _ | _b2hc strip +250 (removed inference), then register avail_nerf; may_return_2026 default OUT |
| Tom Green | tom-green | 4885 | 5222 | _TBD_ | _ | _b2hc strip +337, then register avail_nerf (L=1.0, out whole 2026) |
| Reef McInnes | reef-mcinnes | 76 | 76 | _TBD_ | _ | repeat-LTI (2 windows, independent); floored — availability barely moves him |
| Lewis Hayes | lewis-hayes | 360 | 360 | _TBD_ | _ | repeat-LTI (2 windows, independent) |
| Nick Daicos | nick-daicos | 7626 | 7626 | 7626 | 0 | non-register — byte-identical (parity witness) |
| Marcus Bontempelli | marcus-bontempelli | 3524 | 3524 | 3524 | 0 | non-register — byte-identical (parity witness) |
| Max Gawn | max-gawn | 2413 | 2413 | 2413 | 0 | non-register — byte-identical (parity witness) |

## _b2hc retirement parity note
The `_b2hc` inference fired on exactly {nicholas-martin, tom-green} on store a2fbc9a0 — BOTH register names.
Retiring it moves ONLY those two (up, by the removed haircut: Nic Martin 3266→3516, Tom Green 4885→5222),
then the register layer re-prices them. No non-register player carried _b2hc, so the strip is register-only.
