# `pick` SEMANTICS PER ENTRY MECHANISM — store schema note (added by the PICK-CORRECTIONS build, 2026-07-11)

The store's `pick` field means different things per `type`, and the engine consumes them differently. This
note prevents the next audit from re-deriving the mechanism→pick mapping. It documents behaviour; it changes
nothing. (Authority for the chaining CONTRACT is `SINGLE_SOURCE_INVARIANT.md` — the supervisor's pen; this is
a co-located reader's key for the store.)

| `type` | `_draft` | `pick` stored | pick CONSUMED by the engine (`effpk`) |
|---|---|---|---|
| `ND`  | National | official national-draft pick number | RAW national pick (`_eff = min(99, pick)`) |
| `PSD` | Pre-Season Draft | official pre-season-draft slot | CHAINED: `_eff = last_national_pick[year] + slot` — chains AFTER national, BEFORE rookie (owner ruling) |
| `RD`  | Rookie | official rookie-draft slot | CHAINED: `_eff = last_national_pick[year] + slot` |
| `MSD` | Mid-Season | mid-season draft slot | NEVER consumed; empirical pick-equivalent (≈60) is used instead |
| `SSP` | SSP | (pickless; `pick` may be null) | empirical pick-equivalent (≈94) |
| `IRE`/`UNR`/`PDA`/`PDN`/`PDS` | Post-Draft - … | pickless | empirical pick-equivalent (≈94 each) |

Key points:
- The chaining offset is the authoritative per-year LAST NATIONAL PICK (`national_draft_last_pick.json`),
  NOT the ND row count (the count is right only where the national sequence is gapless).
- Rookie/PSD `pick` should be the OFFICIAL draft slot. Historically the store held pass-dropped ORDINALS;
  the PICK-CORRECTIONS build corrected the web-verified rows and flagged the rest (see
  `session_2026-07-11/pick_corrections/out/store_corrections_ledger.json`). Rows carrying
  `_pick_source` have a web-verified official number; rows without it may still hold a legacy ordinal.
- MSD `pick` (mid-season slot) is intentionally never consumed — the empirical pick-equivalent prices it.
- Every chained rookie/PSD pick ≥ ~62 caps at `KMAX=70` / `min(99)` on the fitted surfaces, so per-row
  rookie/PSD numbering errors are near-$0 on the current board (they become live only if the caps are lifted).
