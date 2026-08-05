# CHANGES — corrected handover copy of `rl_model_data.json`

**Source (read-only, untouched):** `/tmp/claude-0/-home-user-afl-rl-engine/857170f9-1a0a-5fff-ab5e-32b13cff3f0e/scratchpad/wt-lens/engine/rl_after/rl_model_data.json`  
**Source md5:** `81d2470440a80f72afea4405e94338c5`  
**Output:** `/tmp/claude-0/-home-user-afl-rl-engine/857170f9-1a0a-5fff-ab5e-32b13cff3f0e/scratchpad/recipe_final/handover_store/rl_model_data.json`  
**Output md5:** `4b82c5b8a59fe1fc0bb483ffe21902ca`  
**Records:** 2651 in → 2650 out (−1, Leigh Brown removed)

Schema and per-record field order are preserved exactly: every output record was mutated
in place from its source record, never rebuilt, and a key-order assertion
(`list(out.keys()) == list(src.keys())`) passed for all 2650 records.

---

## Edit 1 — Remove Leigh Brown + 2008 National draft slide

### 1a. Record removed

| field | value |
|---|---|
| `player` | `Leigh Brown` |
| `key` | `leigh-brown` |
| `year` | `2008` |
| `pick` | `71` |
| `_draft` | `National` |
| `_draft_club` | `Collingwood` |
| `draft_stream` | `ND` |
| `stream_year` | `2008` |
| `stream_pick` | `71` |
| `games` | `65` |
| `_retired` | `True` |

Scoring rows dropped with the record: 2009: 20g/54.8 | 2010: 15g/74.5 | 2011: 20g/69.9

### 1b. Slide — `_draft=='National'` and `stream_year==2008`, pick > 71 → −1

**Affected records: 5**

| key | player | pick | stream_pick |
|---|---|---|---|
| `paul-cahill` | Paul Cahill | 72 → 71 | 72 → 71 |
| `shane-savage` | Shane Savage | 73 → 72 | 73 → 72 |
| `chris-hall` | Chris Hall | 74 → 73 | 74 → 73 |
| `caleb-tiller` | Caleb Tiller | 75 → 74 | 75 → 74 |
| `keiran-king` | Keiran King | 76 → 75 | 76 → 75 |

Class was 76 records, picks 1–76 contiguous with `pick == stream_pick` throughout.
After removal + slide: **75 records, picks 1–75 contiguous**, no gap at 71, no duplicates.

---

## Edit 2 — Tendai Mzungu (`tendai-mzungu`)

### 2a. Re-key (removes the 2016 rookie entry)

| field | before | after |
|---|---|---|
| `year` | `2016` | `2010` |
| `pick` | `12` | `78` |
| `_draft` | `Rookie` | `National` |
| `draft_stream` | `RD` | `ND` |
| `stream_year` | `2016` | `2010` |
| `stream_pick` | `12` | `78` |
| `_draft_club` | `GWS` | `Fremantle` |

> **OWNER REVIEW FLAG — `_draft_club` inferred from career start.** Source recorded
> `GWS`; set to `Fremantle` per owner instruction, inferred from where his career began.
> Not independently verified against a draft source.

Target slot **ND 2010 pick 78** was vacant: that class held 77 records, picks 1–77
contiguous, so pick 78 is a clean tail append — nothing displaced. Class is now 78,
picks 1–78 contiguous.

### 2b. Slide — `_draft=='Rookie'` and `stream_year==2016`, pick > 12 → −1

**Affected records: 22**

| key | player | pick | stream_pick |
|---|---|---|---|
| `jack-henry` | Jack Henry | 13 → 12 | 13 → 12 |
| `ben-ronke` | Ben Ronke | 14 → 13 | 14 → 13 |
| `nathan-mullenger-mchugh` | Nathan Mullenger-McHugh | 15 → 14 | 15 → 14 |
| `mitchell-hinge` | Mitchell Hinge | 16 → 15 | 16 → 15 |
| `luke-strnadica` | Luke Strnadica | 17 → 16 | 17 → 16 |
| `tim-smith` | Tim Smith | 18 → 17 | 18 → 17 |
| `brett-eddy` | Brett Eddy | 19 → 18 | 19 → 18 |
| `oscar-junker` | Oscar Junker | 20 → 19 | 20 → 19 |
| `drew-petrie` | Drew Petrie | 21 → 20 | 21 → 20 |
| `zach-guthrie` | Zach Guthrie | 22 → 21 | 22 → 21 |
| `robbie-fox` | Robbie Fox | 23 → 22 | 23 → 22 |
| `oscar-mcinerney` | Oscar McInerney | 24 → 23 | 24 → 23 |
| `liam-mackie` | Liam Mackie | 25 → 24 | 25 → 24 |
| `declan-keilty` | Declan Keilty | 26 → 25 | 26 → 25 |
| `jarrod-lienert` | Jarrod Lienert | 27 → 26 | 27 → 26 |
| `matthew-taylor` | Matthew Taylor | 28 → 27 | 28 → 27 |
| `ben-jarman` | Ben Jarman | 29 → 28 | 29 → 28 |
| `james-cousins` | James Cousins | 30 → 29 | 30 → 29 |
| `jamaine-jones` | Jamaine Jones | 31 → 30 | 31 → 30 |
| `max-lynch` | Max Lynch | 32 → 31 | 32 → 31 |
| `sam-simpson` | Sam Simpson | 33 → 32 | 33 → 32 |
| `toby-pink` | Toby Pink | 34 → 33 | 34 → 33 |

Class was 34 records, picks 1–34 contiguous. Mzungu (pick 12) left via re-key, so he is
not in the slide population. After: **33 records, picks 1–33 contiguous**.

### 2c. Scoring list replaced

**Before:** 2017: 4g/33.8 (MID)

**After** (pos `MID` on every row — taken from his existing 2017 row, per instruction):

| year | games | avg | pos |
|---|---|---|---|
| 2011 | 14 | 81.4 | MID |
| 2012 | 22 | 79.9 | MID |
| 2013 | 22 | 79.9 | MID |
| 2014 | 21 | 80.0 | MID |
| 2015 | 9 | 65.2 | MID |
| 2016 | 5 | 50.2 | MID |
| 2017 | 4 | 33.8 | MID |

Row-sum games = **97**. `_retired` is true, so no 2026 zero row (Edit 7) applies.

---

## Edit 3 — Tim Mohr (`tim-mohr`)

### 3a. Re-key

| field | before | after |
|---|---|---|
| `year` | `2018` | `2011` |
| `pick` | `19` | `81` |
| `_draft` | `Rookie` | `National` |
| `draft_stream` | `RD` | `ND` |
| `stream_year` | `2018` | `2011` |
| `stream_pick` | `19` | `81` |
| `_draft_club` | `Hawthorn` | `GWS` |

> **OWNER REVIEW FLAG — `_draft_club` inferred from career start.** Source recorded
> `Hawthorn`; set to `GWS` per owner instruction, inferred from where his career began.
> Not independently verified against a draft source.

Target slot **ND 2011 pick 81** was vacant: that class held 80 records, picks 1–80
contiguous, so pick 81 is a clean tail append. Class is now 81, picks 1–81 contiguous.

### 3b. Slide — `_draft=='Rookie'` and `stream_year==2018`, pick > 19 → −1

**Affected records: 0 — this rule was a no-op.**

The 2018 rookie class held exactly 19 records at picks 1–19, and Mohr *was* pick 19 —
the last selection. No pick in that class is greater than 19, so nothing slid. After
Mohr's re-key the class is 18 records at picks 1–18, still contiguous with no gap.
The rule was applied as written; it simply had no members. **No action needed, but
noted in case the owner expected movement here.**

### 3c. Scoring list replaced

**Before:** `[]` (empty — no scoring rows existed)

**After** (pos `KPD` on every row — his `present_position`, per instruction):

| year | games | avg | pos |
|---|---|---|---|
| 2012 | 13 | 65.9 | KPD |
| 2013 | 22 | 69.5 | KPD |
| 2014 | 8 | 72.4 | KPD |
| 2015 | 0 | 0.0 | KPD |
| 2016 | 2 | 31.5 | KPD |
| 2017 | 1 | 50.0 | KPD |
| 2018 | 2 | 56.0 | KPD |

Row-sum games = **48**, which equals his stored career total of 48 — his top-level
`games` value is therefore unchanged by Edit 8. `_retired` is true, so no 2026 zero row.

---

## Edit 4 — Bobby Hill (`bobby-hill`)

Key match: exactly one record contains `bobby-hill`.

| change | before | after |
|---|---|---|
| 2019 scoring row | *(absent)* | `{year: 2019, games: 7, avg: 56.4, pos: SF}` |
| 2023 `avg` | `56.1` | `57.1` |

The 2019 row was inserted in year order (it sorts ahead of his previous first row, 2020).
Its `pos` was not specified by the owner; `SF` was used — his `present_position`, and the
label on every other row of his list.

Final scoring: 2019:7g/56.4 | 2020:5g/59.4 | 2021:16g/49.4 | 2022:11g/40.3 | 2023:21g/57.1 | 2024:23g/62.7 | 2025:14g/56.1 | 2026:0g/0.0

He is `_retired: false` with no 2026 row in source, so Edit 7 also appended a 2026
zero row (0 games), which does not change his games total.

---

## Edit 5 — Stewart Crameri (`stewart-crameri`)

### Avg corrections

| year | avg before | avg after |
|---|---|---|
| 2010 | 52.6 | 52.7 |
| 2011 | 82.9 | 83.0 |
| 2012 | 77.8 | 78.5 |
| 2013 | 72.3 | 72.4 |
| 2014 | 68.2 | 68.0 |
| 2015 | 72.8 | 73.4 |

### New row

`{year: 2016, games: 0, avg: 0.0, pos: KPF}`, inserted in year order between 2015 and 2017.

> **Judgement call — `pos` label for the new 2016 row.** The instruction said "his existing
> pos label", but his rows do not carry one consistent label: 2010 is `KPD`, 2011 is `MID`,
> and 2012 onward are all `KPF`. `KPF` was used — his `present_position`, his `drafted_position`,
> and the label on every row from 2012 on, including the 2015 and 2017 rows that bracket the
> new one. Note his `future_position` is `SF`, which was *not* used.

Final scoring: 2010:3g/52.7 | 2011:20g/83.0 | 2012:18g/78.5 | 2013:16g/72.4 | 2014:22g/68.0 | 2015:17g/73.4 | 2016:0g/0.0 | 2017:2g/58.5 | 2018:4g/62.0

Row-sum games = **102**. `_retired` is true, so no 2026 zero row.

---

## Edit 6 — James Podsiadly (`james-podsiadly`)

| year | avg before | avg after |
|---|---|---|
| 2012 | 73.3 | 73.5 |
| 2014 | 69.3 | 69.4 |

No rows added or removed; games untouched at the row level.
Final scoring: 2010:17g/91.8 | 2011:20g/79.3 | 2012:17g/73.5 | 2013:20g/76.3 | 2014:21g/69.4

---

## Edit 7 — Blank-equals-zero 2026 rows

Rule: for every record with `_retired` falsy **and** no scoring row for 2026, append
`{year: 2026, avg: 0.0, games: 0, pos: <present_position>}`.

**Rows appended: 152**

Population arithmetic: 2,650 records → 804 with `_retired` falsy → 652 of those already
carried a 2026 row → **152 received one**. Every record in the file has an explicit
`true`/`false` `_retired` (no nulls or missing keys), so "falsy" resolves cleanly to `false`.
Every record has a non-null `present_position`, so no row got a null `pos`.

> **Not changed: `_has26`.** 152 records now have a 2026 scoring row while `_has26` still
> reads `false`. The owner rule specified the scoring-row append only, so the flag was left
> alone rather than silently re-derived. Note this flag is **already stale in the source**:
> 27 source records have `_has26` disagreeing with whether a 2026 row actually exists
> (including 1 retired record that carries a 2026 row). **Owner decision needed** on
> whether `_has26` should be recomputed during the rebuild.

<details><summary>All 152 keys that received a 2026 zero row</summary>

`oskar-taylor`, `lachlan-carmichael`, `mitchell-marsh`, `aidan-schubert`, `harley-barker`, `adam-sweid`  
`blake-thredgold`, `avery-thomas`, `sam-allen`, `thomas-matthews`, `tyan-prindable`, `hunter-holmes`  
`jevan-phillipou`, `koby-evans`, `tylah-williams`, `tobyn-murray`, `tai-hayes`, `koby-coulson`  
`hugo-mikunda`, `max-king-syd`, `archie-ludowyke`, `finnegan-davis`, `kye-fincher`, `zac-mccarthy`  
`matthew-leray`, `will-darcy`, `fred-rodriguez`, `riley-onley`, `leon-kickett`, `nick-driscoll`  
`kalani-white`, `noah-chamberlain`, `liam-hetherton`, `jai-saxena`, `ryda-luke`, `toby-whan`  
`jesse-mellor`, `oliver-griffin`, `harrison-coe`, `caleb-may`, `max-beattie`, `alex-van-wyk`  
`max-mapley`, `sid-draper`, `josh-smillie`, `jesse-dattoli`, `cody-angove`, `ned-bowman`  
`thomas-sims`, `james-barrat`, `charlie-nicholls`, `kayle-gerreyn`, `harry-o-farrell`, `ben-camporeale`  
`joel-cochran`, `lucca-grego`, `cooper-bell`, `jacob-molier`, `alex-dodson`, `lucas-camporeale`  
`riak-andrew`, `luke-urquhart`, `tyler-welsh`, `patrick-said`, `rhys-unwin`, `jaren-carr`  
`cody-anderson`, `lennox-hoffman`, `river-stevens`, `keighton-matofai-forbes`, `logan-smith`, `aiden-riddle`  
`harry-charleson`, `asher-eastham`, `joe-pike`, `eamonn-armstrong`, `cillian-burke`, `matt-duffy`  
`zak-evans`, `jacob-moss`, `jaime-uhr-henry`, `ricky-mentha`, `benny-barrett`, `jack-henderson`  
`zac-walker`, `noah-howes`, `mani-liddy`, `will-green`, `harry-demattia`, `oscar-ryan`  
`lance-collard`, `cooper-simpson`, `tew-jiath`, `clay-hall`, `ollie-murphy`, `luke-lloyd`  
`patrick-snell`, `reece-torrent`, `vigo-visentini`, `xavier-walsh`, `rob-monahan`, `nathan-wardius`  
`iliro-smit`, `luke-beecken`, `darcy-jones`, `harry-barnett`, `lewis-hayes`, `brayden-george`  
`jakob-ryan`, `hugh-davies`, `jed-adams`, `max-knobel`, `kaleb-smith`, `noah-long`  
`josh-draper`, `tyrell-dewar`, `robert-hansen`, `josh-sinn`, `toby-conway`, `jesse-motlop`  
`judson-clarke`, `jackson-archer`, `nicholas-martin`, `james-blanck`, `finlay-macrae`, `reef-mcinnes`  
`liam-mcmahon`, `tyler-brockman`, `henry-smith`, `tom-green`, `riley-garcia`, `max-king-stk`  
`sam-sturt`, `bobby-hill`, `lachlan-sholl`, `caleb-graham`, `paddy-dow`, `jack-payne`  
`bailey-banfield`, `sam-powell-pepper`, `elliot-himmelberg`, `tyson-stengle`, `tom-doedee`, `joshua-kelly`  
`jack-viney`, `jed-bews`, `ben-murphy`, `kobe-mcdonald`, `indy-cotton`, `oscar-berry`  
`patrick-carr`, `cillian-bourke`  

</details>

---

## Edit 8 — Derived career games

Rule: `games` = sum of scoring-row games **where** that sum ≥ the stored value, **or** the
record is one of the six fully-reconciled players. Otherwise the stored value is kept and
the record is listed under pending backfill.

**`games` rewritten on 553 records** (548 increased, 5 decreased).
**14 records kept their stored value** (pending backfill, below).
The remaining 2083 records already had `games` equal to their row sum — no write.

All 5 decreases are reconciled-six records, as intended:

| key | stored | row sum |
|---|---|---|
| `sam-de-koning` | 98 | **96** |
| `bobby-hill` | 102 | **97** |
| `tendai-mzungu` | 106 | **97** |
| `stewart-crameri` | 103 | **102** |
| `james-podsiadly` | 104 | **95** |

(Tim Mohr is the sixth reconciled record; his row sum of 48 already matched his stored 48.)

### PENDING BACKFILL — counters kept

14 records where the stored career total exceeds the scoring-row sum. Rows are incomplete
— predominantly retired or multi-stint careers whose early seasons are not in the store.
The stored counter was **kept** on each; the row sum is shown for the rebuild to reconcile.

| key | player | stored games | row-sum games | shortfall | retired |
|---|---|---|---|---|---|
| `jayden-post` | Jayden Post | 30 | 7 | 23 | True |
| `zach-tuohy` | Zach Tuohy | 288 | 268 | 20 | True |
| `luke-breust` | Luke Breust | 308 | 288 | 20 | True |
| `tom-hickey` | Tom Hickey | 151 | 144 | 7 | True |
| `tom-scully` | Tom Scully | 187 | 182 | 5 | True |
| `james-bell` | James Bell | 28 | 24 | 4 | True |
| `tom-de-koning` | Tom De Koning | 114 | 111 | 3 | False |
| `tom-lynch-1` | Tom Lynch | 243 | 240 | 3 | False |
| `tom-rockliff` | Tom Rockliff | 208 | 205 | 3 | True |
| `drew-petrie` | Drew Petrie | 16 | 14 | 2 | True |
| `declan-keilty` | Declan Keilty | 2 | 0 | 2 | True |
| `anton-tohill` | Anton Tohill | 1 | 0 | 1 | True |
| `wayde-skipper` | Wayde Skipper | 15 | 14 | 1 | True |
| `robin-nahas` | Robin Nahas | 117 | 116 | 1 | True |

---

## VERIFICATION

All figures below are computed from the finished output file, not from the build run.

### File-level

| check | expected | actual | |
|---|---|---|---|
| record count | 2,650 | 2,650 | PASS |
| output md5 | — | `4b82c5b8a59fe1fc0bb483ffe21902ca` | — |
| `leigh-brown` absent | yes | yes | PASS |
| duplicate keys | 0 | 0 | PASS |
| source file unmodified | yes | yes (md5 unchanged, read-only access) | PASS |

### Per-player games totals

| player | key | expected | actual | |
|---|---|---|---|---|
| Tendai Mzungu | `tendai-mzungu` | 97 | 97 | PASS |
| Tim Mohr | `tim-mohr` | 48 | 48 | PASS |
| Bobby Hill | `bobby-hill` | 97 | 97 | PASS |
| Stewart Crameri | `stewart-crameri` | 102 | 102 | PASS |
| James Podsiadly | `james-podsiadly` | 95 | 95 | PASS |
| Sam De Koning | `sam-de-koning` | 96 | 96 | PASS |

Each actual value above is both the record's top-level `games` **and** the sum of its
scoring rows — the two agree on all six.

### Slide / population counts

| assertion | expected | actual | |
|---|---|---|---|
| 2008 National slide (pick > 71) | 5 | 5 | PASS |
| 2016 Rookie slide (pick > 12) | 22 | 22 | PASS |
| 2018 Rookie slide (pick > 19) | 0 | 0 | PASS |
| 2026 zero rows appended | 152 | 152 | PASS |
| pending-backfill list length | 14 | 14 | PASS |

### Draft-class integrity (post-edit)

| class | records | picks | contiguous 1..n | `pick == stream_pick` |
|---|---|---|---|---|
| National 2008 | 75 | 1–75 | yes | all |
| Rookie 2016 | 33 | 1–33 | yes | all |
| Rookie 2018 | 18 | 1–18 | yes | all |
| National 2010 | 78 | 1–78 | yes | all |
| National 2011 | 81 | 1–81 | yes | all |

No gaps, no duplicate picks, and `stream_pick` mirrors `pick` on every record in every
touched class — including the two classes that received a re-keyed player.

### Field-level diff, source vs output — every difference accounted for

Comparison is per key, field by field, across all 2650 surviving records (plus the 1
removed record). **730 records differ from source; 777 individual field values changed.**

| field | changes | explained by |
|---|---|---|
| `games` | 553 | Edit 8 derive |
| `scoring` | 156 | Edit 7 (152) + Edits 2/3/5/6 on retired named players (4) |
| `pick` | 29 | Edit 1 slide (5) + Edit 2 slide (22) + re-keys (2) |
| `stream_pick` | 29 | same population as `pick` |
| `year` | 2 | re-keys: Mzungu, Mohr |
| `_draft` | 2 | re-keys: Mzungu, Mohr |
| `_draft_club` | 2 | re-keys: Mzungu, Mohr |
| `draft_stream` | 2 | re-keys: Mzungu, Mohr |
| `stream_year` | 2 | re-keys: Mzungu, Mohr |
| **total** | **777** | |

Note `bobby-hill`'s scoring change is counted inside Edit 7's 152 (he received both a
manual row edit and a 2026 zero row); the 4 additional `scoring` changes are the retired
named players Mzungu, Mohr, Crameri and Podsiadly, who are ineligible for a 2026 row.

**Closure check.** Let U be the union of: the 5 named players with content edits, the 27
slid records, the 152 zero-row records, and the 553 derive records.

| check | result |
|---|---|
| \|U\| | 730 |
| records differing from source | 730 |
| differing records **not** in U | 0 |
| records in U that did **not** change | 0 |
| records with a changed field **outside** its population's permitted field set | 0 |

The changed-record set is exactly U, and every changed field on every changed record falls
within the fields its rule is permitted to touch. **No record outside the named players and
the slide / zero-row / derive populations changed in any field.**

`sam-de-koning` appears in the reconciled six but has no content edit — only his `games`
counter was re-derived (98 → 96), so he sits in the derive population.

---

## OPEN ITEMS FOR OWNER REVIEW

1. **`_draft_club` inferred for both re-keyed players** (flagged per instruction).
   Mzungu `GWS` → `Fremantle`; Mohr `Hawthorn` → `GWS`. Inferred from career start,
   not verified against a draft record.
2. **`type` field left untouched on the re-keyed players.** Both still read `type: "RD"`
   while `draft_stream` is now `"ND"`. Elsewhere in the store `type` mirrors
   `draft_stream`. The owner rule enumerated seven fields and `type` was not among them,
   so it was left as-is rather than changed on inference. **Likely needs a decision.**
3. **`_has26` not re-derived** for the 152 records that gained a 2026 row (see Edit 7).
   The flag is already stale on 27 source records independently of this work.
4. **`pick_correction_note` retained verbatim** on Mzungu, Mohr, Crameri and Podsiadly.
   It cites "ITEM 411 Amendment 2" stream ordering, which these re-keys partly supersede
   for Mzungu and Mohr. Left unedited — no instruction covered it.
5. **2018 rookie slide was a no-op** (Edit 3b): Mohr was the final pick of a 19-pick
   class, so no pick exceeded 19. Confirm nothing else was expected to move.
6. **Crameri's new 2016 row `pos`** resolved to `KPF` from an inconsistent row history
   (2010 `KPD`, 2011 `MID`, 2012+ `KPF`). See Edit 5.
7. **Bobby Hill's new 2019 row `pos`** was unspecified; `SF` used (uniform across his rows).
8. **Pending backfill is 14 records** whose stored counters exceed their row sums by 1–23
   games. These counters were kept, so `games` and the scoring rows remain inconsistent
   for them by design until the rows are backfilled.

## Supervisor ruling (post-build, 2026-08-05)
Open item 2 RULED: `type` set to 'ND' on tendai-mzungu and tim-mohr — verified the engine's route classifier reads `type`, so the re-key is inert without it. File md5 after this fix: 813ed87473ea25dac62a450b5d87a6da. Role of this artifact: ACCEPTANCE FIXTURE for the #323 landing batch (the handover package itself is cut from landed main, owner-sequenced).

## Owner backfill of 2026-08-05 (in-channel sheets)
Jayden Post 2010 (7g, 36.7) · 2011 (8g, 47.8) · 2012 (8g, 53.6); Declan Keilty 2019 (2g, 37.5); Anton Tohill 2021 (1g, 39.0). All three derived sums now equal their stored counters exactly (30 / 2 / 1) — resolved and removed from the pending-backfill list. Remaining pending: the finals-convention ruling (9 records whose counter-vs-rows gap is exactly their finals games) and the two active feed-lag counters (resolve by derivation at the landing). File md5 after this edit: 0a4027f2f0e918c94035ee4c3c2703f6.
