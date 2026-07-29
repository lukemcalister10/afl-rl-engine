# OPEN QUESTIONS — round 2, raised after the Q1–Q9 ruling set

Raised under issue #262 Addendum 1 (STOP-and-ask). Each item names the specific rows and the specific
question. **No value is written for a held row until the owner rules.** Everything not listed here
proceeds.

Measurements below were re-run by the execution supervisor against the sheet and the store directly,
not inherited.

---

## R2-1 — BLOCKING. Three players whose ruled per-season status contradicts their player-level position code

The Q5/Q6 table rules these three **non-key in their most recent / future seasons**, but their
`present_position` and `future_position` in both the store and the sheet are **key codes**. Present and
future position are what the board prices against, so the two cannot both stand.

| src | player | ruling (Q5/Q6) | store + sheet `present_position` | `future_position` | last season row |
|---|---|---|---|---|---|
| 1699 | Ryan Lester | KEY in 2024 and 2025; **non-key other years** — so 2026 is non-key | `KDEF` (→ KPD) | `KDEF` (→ KPD) | 2026 `DEF` |
| 1216 | Jake Lever | KEY up to and including 2025; **non-key 2026 onwards** | `KDEF` (→ KPD) | `KDEF` (→ KPD) | 2026 `DEF` |
| 727 | Jack Lukosius | key 2019, 2023, 2024, 2026; **not key in future seasons** | `KFWD` (→ KPF) | `KFWD` (→ KPF) | 2026 `FWD` |

**Question:** does the ruling also move these three players' `present_position` / `future_position` to
the general code — Lester → SD, Lever → SD, Lukosius → SF — or does the player-level modelling position
stay key and only the per-season rows change?

This lands in the stage-2 (owner-edits) half of the proof, so it moves values either way. Held.

**Not in conflict, checked and consistent** — no answer needed: Jai Serong (ruled non-key future,
`present`/`future` already `GDEF`), Reuben Ginbey (ruled key from future only, `present`/`future`
`KDEF` — consistent), Reef McInnes (ruled key whole career, `KDEF` — consistent), Dane Rampe, James
Sicily, Jordan Ridley, Josh Worrell, Jack Scrimshaw, Nick Haynes, Mason Wood, Jeremy Howe, Nick
Blakey, Mitch McGovern, Andy Otten, Ryan Maric.

---

## R2-2 — Name resolution: "Harry Himmelberg"

The sheet carries **two** Himmelbergs and neither is spelled "Harry":

| src | player | is_key | drafted | present | seasons |
|---|---|---|---|---|---|
| 1107 | **Harrison** Himmelberg | KEY | KFWD | GDEF | 11 (2016–2026) — carries the explicit `KEY FWD` 2016–21 / `GEN DEF` 2022–26 per-season rows |
| 1016 | **Elliott** Himmelberg | KEY | KFWD | KFWD | 7 (2018–2024), all `FWD` |

Reading the ruled rule *"when FWD eligible: KPF; when DEF eligible: SD"* against Harrison's own
per-season rows, they match exactly — so **Harry = Harrison** is near-certain. Under Addendum 1 it is
still confirmed rather than assumed.

**Question:** confirm Harry Himmelberg is src 1107, Harrison. On that reading **Elliott (src 1016) is
not named in the table and falls to the blanket rule** — all 7 of his FWD seasons become KPF. Confirm
that is intended.

---

## R2-3 — Q3 review rows, as requested. Count corrected: 16, not 13

The supervisor previously reported these as "9 key-flagged KDEF and 4 GFWD". The GFWD figure was the
`GFWD`-drafted-**and**-`GFWD`-present subset only; the full GFWD-drafted count is **7**. Total 16.

**None of the 16 appear in the Q5/Q6 ruling table — zero are resolved by it.** All 16 take DEF → SD
under the Q3 ruling unless amended.

### The 9 key-flagged, KDEF-drafted

| src | player | drafted | present | future | seasons |
|---|---|---|---|---|---|
| 1160 | Tom Keough | KDEF | KDEF | DEF → SD | 0 |
| 1429 | Lachlan Plowman | KDEF | GDEF | DEF → SD | 11 |
| 1727 | Alex Johnson | KDEF | KDEF | DEF → SD | 3 |
| 1850 | Sam Shaw | KDEF | KDEF | DEF → SD | 4 |
| 1851 | Benjamin Stratton | KDEF | KDEF | DEF → SD | 11 |
| 1874 | Dylan Grimes | KDEF | KDEF | DEF → SD | 15 |
| 1891 | Alex Silvagni | KDEF | KDEF | DEF → SD | 8 |
| 1914 | Simon White | KDEF | KDEF | DEF → SD | 8 |
| 2030 | Luke Delaney | KDEF | KDEF | DEF → SD | 6 |

Note the shape: eight of the nine are `KDEF` drafted **and** `KDEF` present, yet their future leg
already resolves to general defender through the engine's existing `DEF → GEN_DEF` alias. The rename
makes that visible as `SD`. Dylan Grimes (15 seasons) and Benjamin Stratton (11) are the largest
careers affected.

### The 7 GFWD-drafted

| src | player | drafted | present | future | seasons |
|---|---|---|---|---|---|
| 352 | Olli Hotton | GFWD | GFWD | DEF → SD | 0 |
| 585 | Isiah Winder | GFWD | GFWD | DEF → SD | 0 |
| 779 | Nick Hind | GFWD | GDEF | DEF → SD | 6 |
| 1412 | Alex Spina | GFWD | GFWD | DEF → SD | 0 |
| 1556 | Hayden Crozier | GFWD | GDEF | DEF → SD | 12 |
| 1558 | Murray Newman | GFWD | GFWD | DEF → SD | 2 |
| 1983 | Neville Jetta | GFWD | GDEF | DEF → SD | 13 |

Four of the seven are `GFWD` present with a `DEF` future — a forward whose future leg is a defender.
Flagged for the owner's eye; not held, since Q3 rules DEF → SD for all 136.

---

## R2-4 — Correction to the supervisor's own Q1 framing

The ruling adds *"Owens → KPF, Farrar → KPF, Laverde → KPD, McInnes → KPD"* to the edit set. Checked
against the store: **only Jy Farrar is an actual edit.**

| src | player | store `present_position` | sheet `present_position` | |
|---|---|---|---|---|
| 693 | Jy Farrar | `GDEF` | `KFWD` | **EDIT** → KPF |
| 455 | Mitchito Owens | `KFWD` | `KFWD` | no change (already KPF) |
| 1221 | Jayden Laverde | `KDEF` | `KDEF` | no change (already KPD) |
| 550 | Reef McInnes | `KDEF` | `KDEF` | no change (already KPD) |

The owner-edit set therefore remains 43 `present_position` + 12 `future_position` + 1
`alternate_position` + 2 `p_dual_stream`, of which Farrar is already one of the 43. No action needed —
recorded so the stage-2 mover attribution is not expected to show four rows where it will show one.

---

## CLEARED — verified, no question

- **Q4, unflagged rucks: zero.** No player drafted `RUC` lacks the `KEY` flag (0 of 219), and no player
  with present `RUC` who was not drafted `RUC` lacks it (0). Nothing for the owner to tidy.
- **Q8, DPP hierarchy: zero violations.** All 12 distinct season-position values across all 11,264
  season rows comply with FWD → DEF → RUCK → MID: `FWD/MID` (966), `DEF/MID` (381), `FWD/DEF` (298),
  `FWD/RUCK` (199), `DEF/RUCK` (24), `RUCK/MID` (6), plus the six single-value forms and Harrison
  Himmelberg's two explicit spellings.
- **Q9, bust defaults: zero applied**, as ruled. The 727 players with no scoring seasons have none in
  the store either, so there is no season row to attribute.
- **Precedence resolves the flag gap.** Ten of the 25 named players are not flagged `KEY` in the sheet
  — Blakey, Sicily, Ridley, Worrell, Scrimshaw, Melksham, Ginbey, Haynes, Howe, Langford. The owner's
  *"where this message and the sheet's flags disagree, this message wins"* governs; they take their
  ruled key seasons. Recorded, not asked.
