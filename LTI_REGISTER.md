# LTI & AVAILABILITY REGISTER — Luke's ground-truth data — KEYED SIDECAR v1 · 2026-07-09
### The curated register the engine consumes as a PINNED INPUT (R-REG=R2, DECISIONS §33). Human-maintained
### ground truth beats inference for injury detection. Owner edits this file; the engine only READS it and
### never re-diagnoses a row (report-only on store anomalies). Supersedes the un-keyed
### `LTI_REGISTER_2026-07-02.md` (retired at this commit; its body is folded here verbatim WITH the owed
### `key` column — 43/43 keys VERIFIED against store `a2fbc9a0`, 2026-07-09; zero guesses). Body-of-record
### unchanged from the 2026-07-02 capture (turn 43, Luke verbatim intent).
###
### TIMING DESIGNATIONS (Luke's definitions):
### · `2025`          = injured in his last game of 2025; hasn't played since; MAY return during 2026.
### · `2026_preseason`= injured before the 2026 season started; will not play until 2027.
### · `2026`          = injured in his most recently recorded 2026 game; will not play until 2027.
###
### ENGINE READING (spec §2.1): `2025` → zero 2026 games so far, return-during-2026 possible (fork iii,
### R-iii = owner-flagged binary, DEFAULT OUT until `status` is flipped to `returned`); `2026_preseason` →
### full-season absence, L=1; `2026` → 2026 truncated at store games-so-far, those games FINAL (no gross-up),
### L = 1 − g₂₀₂₆/G_FULL. Section B = same availability semantics, return-season haircut STRUCTURALLY ZERO.
###
### NAME GUARD: "Maxwell King" is the disambiguated name (two real players named Max King; the store holds
### `max-king-syd` (Sydney, pick 49, 2025) and `max-king-stk` (St Kilda, pick 4, 2018) sharing the identical
### DOB 2007-01-09 — only the store key separates them; a third `max-king-1` (retired) also exists). Key by
### ID, never name. The collision sentry (one_source_selftest.py) pins the pair permanently.
###
### SCHEMA: one row per INJURY WINDOW (repeat-LTI players get two rows). Columns:
### `key | player | section | window_id | designation | status | returned_year | notes`
### · status ∈ {out_until_2027, may_return_2026, returned}; returned_year blank until a real return.
### · The engine consumes `key`, `section`, `window_id`, `designation`, `status`. Game counts are NEVER
###   carried here — the store stays the single source of production (spec §3.3).

| key | player | section | window_id | designation | status | returned_year | notes |
|---|---|---|---|---|---|---|---|
| jack-payne | Jack Payne | A | 1 | 2025 | may_return_2026 |  | may return 2026 |
| matt-carroll | Matt Carroll | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| jesse-motlop | Jesse Motlop | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027 |
| harry-o-farrell | Harry O'Farrell | A | 1 | 2025 | may_return_2026 |  | may return 2026 |
| jamie-elliott | Jamie Elliott | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| reef-mcinnes | Reef McInnes | A | 1 | 2025 | out_until_2027 |  | repeat LTI — window 1 (fork ii: independent windows) |
| reef-mcinnes | Reef McInnes | A | 2 | 2026 | out_until_2027 |  | repeat LTI — window 2; report-only repeat_lti on-sight flag |
| oscar-steene | Oscar Steene | A | 1 | 2026 | out_until_2027 |  | out until 2027; store anomaly: no 2025 row (report-only, register governs) |
| brayden-fiorini | Brayden Fiorini | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| lewis-hayes | Lewis Hayes | A | 1 | 2025 | out_until_2027 |  | repeat LTI — window 1 (fork ii: independent windows) |
| lewis-hayes | Lewis Hayes | A | 2 | 2026 | out_until_2027 |  | repeat LTI — window 2; report-only repeat_lti on-sight flag |
| nicholas-martin | Nic Martin | A | 1 | 2025 | may_return_2026 |  | Luke's exemplar obvious case (established → zero games) |
| toby-conway | Toby Conway | A | 1 | 2025 | may_return_2026 |  | may return 2026; store anomaly: last store games 2024 (report-only, register governs) |
| tom-green | Tom Green | A | 1 | 2026 | out_until_2027 |  | Luke's exemplar obvious case |
| joshua-kelly | Josh Kelly | A | 1 | 2026_preseason | out_until_2027 |  | GWS 2013 pick-2 (will-kelly/tim-kelly rejected on cohort); out until 2027 |
| darcy-jones | Darcy Jones | A | 1 | 2025 | may_return_2026 |  | may return 2026 |
| nathan-wardius | Nathan Wardius | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027; first-year (no store scoring row) |
| jai-culley | Jai Culley | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| jack-viney | Jack Viney | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027 |
| andy-moniz-wakefield | Andy Moniz-Wakefield | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| jackson-archer | Jackson Archer | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027 |
| blake-thredgold | Blake Thredgold | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027; first-year (no store scoring row) |
| ollie-lord | Ollie Lord | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| esava-ratugolea | Esava Ratugolea | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| josh-sinn | Josh Sinn | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027 |
| josh-gibcus | Josh Gibcus | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| judson-clarke | Judson Clarke | A | 1 | 2025 | may_return_2026 |  | may return 2026 |
| sam-flanders | Sam Flanders | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| liam-hetherton | Liam Hetherton | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027; first-year (no store scoring row) |
| max-king-syd | Maxwell King | A | 1 | 2026_preseason | out_until_2027 |  | name-collision guard applies (max-king-syd, Sydney pick 49); first-year |
| noah-long | Noah Long | A | 1 | 2026_preseason | out_until_2027 |  | out until 2027 |
| jacob-newton | Jacob Newton | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| deven-robertson | Deven Robertson | A | 1 | 2026 | out_until_2027 |  | out until 2027 |
| sam-darcy | Sam Darcy | A | 1 | 2026 | out_until_2027 |  | out until 2027; A-DARCY anchor — no availability locus may clip his ceiling |
| archie-may | Archie May | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |
| harley-barker | Harley Barker | B | 1 | 2026_preseason | out_until_2027 |  | remainder of 2026; no return haircut; first-year |
| brody-mihocek | Brody Mihocek | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |
| toby-pink | Toby Pink | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |
| mani-liddy | Mani Liddy | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |
| ewan-mackinlay | Ewan Mackinlay | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |
| connor-rozee | Connor Rozee | B | 1 | 2026 | out_until_2027 |  | out for remainder of 2026; feeds A3 (DATA-CAUSED red, R-A3 uphold); no return haircut |
| jonty-faull | Jonty Faull | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |
| joel-amartey | Joel Amartey | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |
| noah-chamberlain | Noah Chamberlain | B | 1 | 2026_preseason | out_until_2027 |  | remainder of 2026; no return haircut; first-year |
| harry-edwards | Harry Edwards | B | 1 | 2026 | out_until_2027 |  | remainder of 2026; no return haircut |

## CROSS-THREAD FLAGS (supervisor, carried from the 2026-07-02 capture)
1. **Connor Rozee is out for the rest of 2026** — his 2026 stays at his real 2 games permanently; A3
   (2026 ≥ 75% of 2025) is a permanent DATA-CAUSED red (R-A3 = uphold), evaluated PRE-LTI-layer.
2. Register declared compatible with the calendar fix (M2/M3 own clock proration; nobody's season is
   "completed"), the games-ramp/SITOUT_RETAIN (register zero-games names flow the existing V0·R_SURF·λ
   path untouched), and the cliff blend (L_p continuous in g₂₀₂₆; λ endpoints unchanged). See spec §5.iv.
3. LTI machinery verified ABSENT 2026-07-08 (built fresh at this chapter; not re-queued).
