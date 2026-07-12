# `pick` SEMANTICS PER ENTRY MECHANISM — store schema note (PICK-CONVENTION REMEDIATION, 2026-07-11)

The store's `pick` field means different things per `type`, and the engine consumes them differently. This
note prevents the next audit from re-deriving the mechanism→pick mapping. It documents behaviour; it changes
nothing. (Authority for the chaining CONTRACT is `SINGLE_SOURCE_INVARIANT.md` — the supervisor's pen; this is
a co-located reader's key for the store.)

## OWNER DATA LAW (ground truth, owner-stated 2026-07-11) — the store's numbering convention

Store `pick` numbers are **DATABASE-UNIVERSE ordinals, not AFL official numbering.** They are the position of
a player within *this database's* draft universe, which deliberately differs from the real-world number:

> **"Players previously listed are excluded when redrafted, and only their initial entry is recorded."**

One row per player, at their **initial** entry; redrafts/recycled players never consume numbering. Because
recycled players ahead of a pick are excluded, a store ordinal is deliberately LOWER than the AFL-official
number (e.g. Josh Treacy's rookie ordinal is **5**, not his real-world 7 — players ahead of him were recycled
redrafts). This is intentional and correct; it is **not** a data error.

Consequences (binding on every build):

- The store IS the authority. **No build may "correct" store pick numbers against external / AFL-official
  sources without an explicit owner ruling.** (The 2026-07-11 correction build's "renumber to real-world"
  pass — 190 rookie renumbers + the 2010→77 chain override — violated this law and was REVERTED by the
  pick-convention remediation.)
- The rookie draft **chains onto the end of the national draft** in the database universe: first rookie pick
  of year Y = `last_national_pick[Y] + 1` (e.g. ND ends pick 54 ⇒ RD pick 1 = 55). PSD chains after national,
  before rookie. Both sides are counted in the DATABASE's universe.
- `last_national_pick[Y]` = the database's own national END = the store's **MAX National ordinal** for year Y
  (`national_draft_last_pick.json`), NOT the ND row count and NOT the real-world selection count. Count==max
  for 21/23 gapless years; where they differ (2010, 2011) the gaps are excluded/redrafted players and the
  MAX is the collision-free end.

## `pick` per `type`

| `type` | `_draft` | `pick` stored | pick CONSUMED by the engine (`effpk`) |
|---|---|---|---|
| `ND`  | National | database-universe national ordinal (initial-entry, redrafts excluded) | RAW national pick (`_eff = min(99, pick)`) |
| `PSD` | Pre-Season Draft | database-universe pre-season-draft slot | CHAINED: `_eff = last_national_pick[year] + slot` — chains AFTER national, BEFORE rookie (owner ruling) |
| `RD`  | Rookie | database-universe rookie slot (redrafts excluded ⇒ deliberately below real-world) | CHAINED: `_eff = last_national_pick[year] + slot` |
| `MSD` | Mid-Season | mid-season draft slot | NEVER consumed; empirical pick-equivalent (≈60) is used instead |
| `SSP` | SSP | (pickless; `pick` may be null) | empirical pick-equivalent (≈94) |
| `IRE`/`UNR`/`PDA`/`PDN`/`PDS` | Post-Draft - … | pickless | empirical pick-equivalent (≈94 each) |

Key points:

- The chaining offset is the authoritative per-year LAST NATIONAL PICK (`national_draft_last_pick.json`) =
  the store's own MAX National ordinal — the database's ND end (owner data law above), NOT the ND row count.
- Rookie/PSD/ND `pick` is the **database-universe ordinal**, which deliberately differs from the AFL-official
  number by the count of excluded (recycled/redrafted) players ahead of it. A store ordinal that does not
  match an external source is expected, not suspect.
- `_pick_source` stamps now mark ONLY the 8 web-verified **Pre-Season Draft split** rows (`type=PSD`): those
  rows were re-classified out of `Rookie` (a genuine `type` correction), and the stamp records the
  reclassification evidence. Rookie/national `pick` numbers carry NO such stamp — they are database ordinals
  and are not verified against external numbering by design.
- MSD `pick` (mid-season slot) is intentionally never consumed — the empirical pick-equivalent prices it.
- Every chained rookie/PSD pick ≥ ~62 caps at `KMAX=70` / `min(99)` on the fitted surfaces, so per-row
  rookie/PSD numbering differences are near-$0 on the current board (they become live only if the caps are
  lifted).
