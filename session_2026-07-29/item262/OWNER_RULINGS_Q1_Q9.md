# OWNER RULINGS — ITEM 262, questions Q1–Q9

**Source:** owner message to the execution supervisor, 2026-07-29, in the executing chat.
**Status:** complete ruling set for Q1–Q9. Recorded verbatim as evidence before any edit was made.

**Precedence, owner's words:** *"This message is the complete ruling set — encode it as a committed
ruling table, verbatim, as evidence. My sheet stays as submitted; where this message and the sheet's
flags disagree, this message wins."*

The questions these answer were raised by the supervisor after surveying the owner's positional sheet
(`rl_model_data_editable_1.xlsx`, generated 2026-07-28 12:57:05, 2,651 player records / 11,264 scoring
records) against the store at `engine/rl_after/rl_model_data.json` (md5 `e3aaba772f339551cd223802ab115af7`).

---

## VERBATIM RULING TEXT

> Q1 — intended. I edited present/future/alternate position and dual-stream in the sheet deliberately.
> Land them. Prove the landing in two stages: the rename alone must show zero value and rank movers;
> then my edits applied, with every mover reported and attributed to the specific edited rows. The
> present-position changes below (Owens → KPF, Farrar → KPF, Laverde → KPD, McInnes → KPD) join that
> edit set.
>
> Q2 — real trades, wrong mechanism. The 16 `affl_team` changes are genuine trades since my last
> update. Apply them through the ownership sidecar's edit command (#232), not as store edits — and
> report whether the store's `affl_team` field is now legacy. The two `p_dual_stream` changes (Graham
> 70→90, Petracca 50→70) are intended.
>
> Q3 — DEF = SD for the 136, confirmed (the engine's existing alias made visible). Send me the 9
> key-flagged KDEF rows and the 4 GFWD rows for review, marking which are already resolved by the
> table below.
>
> Q4 — all ruckmen are key-position players. Any DPP season containing RUCK renders its FWD/DEF
> component key — KPF/RUCK or KPD/RUCK — regardless of the flag. SF/RUCK and SD/RUCK are not
> possible. Pure RUCK has no key variant. Report any unflagged rucks you find so I can tidy the
> profiles.
>
> Q5/Q6 — superseded by this per-season table. "KEY until year X" means up to and including X.
> Entries written as "when FWD/DEF eligible" apply off the season eligibility data, not year ranges:
>
> * Nick Blakey, Harry Himmelberg, Mitch McGovern — when FWD eligible: KPF; when DEF eligible: SD
> * Jayden Laverde — when FWD eligible: SF; when DEF eligible: KPD
> * James Sicily — KPD in 2020 and 2023–2025; non-key other seasons
> * Jordan Ridley — KPD 2022–2025; non-key other seasons
> * Josh Worrell — KPD 2024–2025; non-key other seasons
> * Jack Scrimshaw — KPD in 2025; non-key other seasons
> * Jake Melksham — KPF 2025–2026; non-key other seasons
> * Dane Rampe — KPD 2017–2024; non-key other seasons
> * Mitchito Owens — KPF in 2024 and 2026; non-key other seasons
> * Reuben Ginbey — no key eligibility to date; key from future seasons only
> * Mark Blicavs — KEY when DEF eligible
> * Nick Haynes — KEY up to and including 2017; non-key 2018 onwards
> * Mason Wood — KPF up to and including 2015; non-key 2016 onwards
> * Jeremy Howe — KPD 2020–2025; non-key before 2020 and from 2026
> * Kyle Langford — KPF in 2025 and 2026; non-key other seasons
> * Reef McInnes — KEY for his whole career
> * Ryan Lester — KEY in 2024 and 2025; non-key other years
> * Jack Lukosius — KEY up to and including 2019, in 2023 and 2024, and again in 2026; not key in
>   future seasons
> * Jai Serong — KEY up to and including 2026; non-key future seasons
> * Jake Lever — KEY up to and including 2025; non-key 2026 onwards
> * Andy Otten — KEY when DEF
> * Jy Farrar — KEY from 2025 onwards
> * Ryan Maric — drafted key, never played it: no key seasons
>
> Scope: every flagged player not named above gets the blanket rule (all FWD/DEF seasons key);
> unflagged and unlisted stays general.
>
> Q7 — confirmed: Himmelberg reads KPF / SD, now governed by his eligibility rule above.
>
> Q8 — order is semantic. The hierarchy is FWD → DEF → RUCK → MID, so your 6 RUCK/MID rows are
> already correct. Verify every DPP row complies with the hierarchy and report any that don't.
>
> Q9 — confirmed vacuous. No synthetic season rows for the 727; report 0 defaults applied. Busts
> count through their draft records at the curve fit, unchanged.
>
> Stop-and-ask still applies to anything new you hit. Proceed per the directive: branch, scripted
> transcription with the rename in the same pass, sibling re-pins including the held-candidate md5s,
> then PR and honest CI.

---

## PRIOR SEALED RULINGS THIS JOB ALSO EXECUTES

Carried from `docs/CURRENT_STATE.md` v26 and issue #262 + Addendum 1, restated here so the
transcription script has one source:

1. **Vocabulary is REPLACED, not merged:** `K-FWD`/`KFWD`/`KEY_FWD` → **KPF** · `K-DEF`/`KDEF`/`KEY_DEF`
   → **KPD** · `G-DEF`/`GDEF`/`GEN_DEF` → **SD** · `G-FWD`/`GFWD`/`GEN_FWD` → **SF** · `MID` → **MID** ·
   `RUC`/`RUCK` → **RUCK**. New names so any un-migrated site fails visibly instead of half-matching.
2. **The key overlay is a blanket rule** for flagged players not named in the Q5/Q6 table: every FWD
   season reads key forward, every DEF season reads key defender, across the whole career.
3. **Harrison Himmelberg is the named per-season exception** — his rows are categorised in the sheet
   itself (2016–2021 `KEY FWD`, 2022–2026 `GEN DEF`) and are transcribed as given.
4. **The bust default** — a bust absent from the training data falls to drafted position, explicitly
   marked, never a silent fallback. Ruled vacuous at Q9: 0 applied.
5. **No value re-derivation, no curve change, no valuation math change, no bar change.** The
   per-season bar re-measurement, the modelling-position wiring and the curve-input rulings
   (Cameron/Shiel/Treloar in; McCartin/Boyd out with drafts slid up one) belong to the re-derivation
   job that follows — none of them are this job's.
6. **Addendum 1 STOP-and-ask** stands for anything new: bring the owner the specific rows and the
   specific question, hold for the ruling, never guess.

---

## DERIVED DECISION TABLE

The machine-readable form the transcription script consumes is
`session_2026-07-29/item262/ruling_table.json`, generated from this document. Where the two differ,
**this document is the record and the JSON is wrong.**

### Season-position resolution order

For each scoring season of each player, in order:

1. If the sheet's season `Position` already carries an explicit key/general spelling (`KEY FWD`,
   `GEN DEF` — Harrison Himmelberg only), transcribe it as given → KPF / SD.
2. Split the season `Position` on `/` into components, preserving the sheet's order.
3. For each `FWD` or `DEF` component, decide key vs general:
   - **Q4 override first:** if any component of this season is `RUCK`, the FWD/DEF component is
     **key** (KPF / KPD) regardless of flag. SF/RUCK and SD/RUCK cannot occur.
   - else if the player is named in the Q5/Q6 table, apply that player's rule for this season year.
   - else if the player is flagged `KEY` in the sheet, key (blanket rule).
   - else general.
4. `MID` → `MID`. `RUCK` → `RUCK` (no key variant).
5. Re-join with `/` in the sheet's original order, which Q8 confirms is the semantic hierarchy
   FWD → DEF → RUCK → MID.

### Player-level position fields

`drafted_position`, `present_position`, `future_position`, `alternate_position` are mapped through the
vocabulary replacement only, with the store's existing `DEF` → `SD` alias made explicit per Q3
(`rl_model.py:67` `GRP` already maps `'DEF':'GEN_DEF'`). The owner's 43 present / 12 future / 1
alternate edits land as submitted per Q1.

### Open at time of writing

Three players whose ruled per-season key status contradicts their player-level position code, and the
Q3 review rows, are listed in `OPEN_QUESTIONS_ROUND2.md` in this directory and are **held pending owner
ruling** — no value is written for them until that ruling lands.
