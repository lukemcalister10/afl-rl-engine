# LTI_REGISTER — 2026-07-02
_Luke-maintained ground truth: long-term-injury identifications and expected-return windows. The engine treats
entries here as GROUND TRUTH about availability, per the same rule as Luke's player reads._

## ⚠ CONTENT GAP — REGISTER ENTRIES ABSENT AT COMMIT
The D4 directive (ASK 6) says the supervisor supplies this file's entries; **no register content arrived with
the directive**. This commit establishes the file, schema, and guards so Luke/supervisor can fill rows directly;
the register is EMPTY until then. Flagged in the D4 return per the REQUIRED_INPUTS gap-report discipline —
nothing here is invented on Luke's behalf.

## Schema (one row per LTI identification)
| player (EXACT store name) | store key | club | injury | identified | expected return | season(s) written off | return-haircut note | Luke note |
|---|---|---|---|---|---|---|---|---|
| _(empty — supervisor supplies)_ | | | | | | | | |

## Guards (binding on any consumer of this file)
- **EXACT-name discipline** — the store's rename guard applies: the player commonly called "Max King" is
  **"Maxwell King"** in the store (Max King → Maxwell King rename guard, START_HERE §5); two Uwlands; 8 known
  name collisions — key rows by the `store key` column (`p['key']`), never by display name.
- Entries are Luke's ground truth: the engine may HAIRCUT for absence (cf. the existing `_b2hc` present-
  unavailability machinery) but never re-diagnoses an entry.
- A3 is evaluated PRE-LTI-layer (Luke, 02/07/2026, logged): any LTI overlay built from this register must not
  be the thing that passes A3.
