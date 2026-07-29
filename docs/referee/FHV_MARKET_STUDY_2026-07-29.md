# FHV MARKET STUDY — what a free list-spot actually converts into (report-only)

Register item #270 first deliverable ("referee opening question — FREE-HIT VALUE ... report-only market study first").
Read-only measurement; no repo file was touched; every figure below is the output of a python pass over the two stores named next.

**Provenance correction (seam, 2026-07-29):** this study was computed on a working tree that a stale ref had left at
the PRE-#262 artifact pair (store `e3aaba77`, board `750446d7`) — a seam-side checkout slip, found and disclosed the
same day. The seam re-ran the headline measurements on the LANDED pair (store `5d6e56d0`, board `3d4e2e50`) and every
figure re-checked is **identical**: free-mechanism n=389 (52/106/231), whole-cohort median 0 / mean 178, survivors
149 (median 240 / mean 466), ≥528 = 33 (8%), top values newcombe 4180 / uwland 3782 / martin 3484. This is expected,
not lucky: #262 was proven value-neutral (board byte-identical modulo relabel) and touched no stream/value fields —
but it is stated because it was measured, not assumed. Position-vocabulary strings do not appear in this report, so
no era-relabel applies to its text.

**Sources**
- Player store: `/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json` — 2,651 records, unique `key`s.
- Current board: `/home/user/afl-rl-engine/data/rl_build/rl_app_data.json` — per-player value field is `v` inside the
  `active` list (n=804). A separate `back` list (n=198) carries departed players at residual display values
  (median v=12); `_retired=False` in the store matches the 804 `active` exactly, `_retired=True` records that appear
  at all appear only in `back`. "On the current board" below = **in `active`**; `back` membership is reported separately
  and counted as 0 in whole-cohort views.
- Constants under comparison: **150** (owner's illustrative guess), **250** (clubs-tab phantom placeholder),
  **528** (`pool_value` in `/home/user/afl-rl-engine/engine/rl_after/pvc_curve_v2.json`).

**Scale of `v`** (so the constants have context): numeraire pin is ND pick 1 = 3000 (`pvc_curve_v2.json` `pin`, and
`phantomPicks[0].v = 3000` in the app data). The adopted curve runs PVC[1]=3000 ... PVC[50]=589 ... PVC[64]=530;
`pool_value = 528` is, per the artifact's own note, "the pre-split artifact's own value at index 65". Across the 804
active board values (med 453, mean 960): **150 sits at the 22nd percentile, 250 at the 32nd, 528 at the 54th.**

**Field-semantics findings established before measuring** (each verified by direct counts):
- `draft_stream` ∈ {ND 1569, RD 693, OTHER 231, MSD 106, SSP 52}; `type` refines OTHER into
  IRE ("Post-Draft - Ireland", 57), UNR ("Post-Draft - Unregistered", 59), PDA ("Post-Draft - Academy", 51),
  PDN ("Post-Draft - Next Gen", 43), PDS ("Post-Draft - Scholarship", 21). **OTHER is not PSD** — it is the
  pre-listing category-signing family.
- PSD (pre-season draft) exists in the store only as **8 rows** stamped `_pick_source = "pre-season-draft-official"`,
  currently typed RD, all `stream_pick = 1`, years 2003–2021 (most recent: luke-nankervis 2021). Per
  `pick_semantics_schema.md` (owner data law), redrafted/recycled players are excluded from the store — and PSD
  selections are overwhelmingly redrafts — so **the PSD window is structurally near-invisible here**.
- Cohort-year conventions, measured from (first scoring year − `stream_year`) among entrants who played:
  MSD mode = 0 (the mid-season draft of season Y, debut that season: 51/74); SSP mode = +1 (34/43) — i.e.
  **SSP `stream_year` Y = signed for season Y+1**, so "the 2026 SSP cohort" = `stream_year` 2025; ND/RD mode = +1;
  OTHER mode = +2 (41/100 at +2, 34 at +1) — post-draft signings often debut late.
- `games` field is a mixed-vintage snapshot (equals sum of scoring rows for 2082/2651, equals pre-2026 sum for
  2007/2651, matches neither for the rest); `scoring` rows are used as the authority. Career games =
  Σ scoring.games, falling back to `games` for the 3 records (tim-mohr, anton-tohill, declan-keilty) that have
  games>0 but no scoring rows. 2026 is in progress (`BASE_YEAR` 2026, `SEASON_PROG` 0.83), so all 2026 figures are
  partial-season.
- 3 of 52 SSP records (mark-keane, flynn-perez, lachlan-mcandrew) carry scoring **before** their SSP year — prior
  stints folded into an "initial entry" row; their career stats include the pre-entry seasons.

---

## 1. COHORT ENUMERATION

Counts by `draft_stream` × `stream_year` (denominator = 2,651 store records):

| stream | n | stream_year breakdown |
|---|---|---|
| **SSP** | 52 | 2018:9 · 2019:4 · 2020:6 · 2021:5 · 2022:7 · 2023:4 · 2024:8 · 2025:9 (signed-for seasons 2019–2026) |
| **MSD** | 106 | 2019:9 · 2021:20 · 2022:15 · 2023:11 · 2024:17 · 2025:16 · 2026:18 (no 2020 mid-season draft) |
| **OTHER** | 231 | 2003–2025; recent years 2019:9 · 2020:9 · 2021:9 · 2022:17 · 2023:10 · 2024:13 · 2025:14 |
| **RD** | 693 | 2003–2025; 2019:14 · 2020:12 · 2021:10 · 2022:12 · 2023:9 · 2024:9 · 2025:6 |
| (ND) | 1569 | 2003–2025 (context only) |

OTHER sub-classification (from `type` / `_draft`, not assumed): IRE 57 (2003–2025, a steady trickle),
PDA 51 (2009–2025), PDN 43 (2016–2025), PDS 21 (**2007–2011 only — a defunct scholarship scheme**), UNR 59 (2007–2025).

Named window cohorts used below:
- **2026 SSP cohort** = SSP `stream_year` 2025, n=9. **2025 SSP cohort** = sy2024, n=8.
- **2026 MSD cohort** = MSD 2026, n=18. **2025 MSD cohort** = MSD 2025, n=16.
- **Most recent PSD-like cohort**: not distinguishable as a cohort — only the 8 stamped pick-1 PSD rows exist
  (singletons, 2003–2021); reported as a remnant in §2.

`stream_pick` coverage: ND 1569/1569, RD 693/693, MSD 106/106; **SSP 0/52 and OTHER 0/231 are pickless** —
order analysis (§3) is therefore possible for MSD (and RD as corroboration) only.

## 2. REALISED OUTCOMES PER COHORT (survivor-honest)

Conventions: "ever played" = career games > 0. Career avg = games-weighted mean of scoring `avg`, 0 for
never-established. "First season" = the first scoring row at/after the entry season (entry season = stream_year for
MSD, stream_year+1 otherwise); it is reported only for the n that have one (denominator shown). Board v: survivors =
cohort members in `active`; whole-cohort = v with absent/never-established at 0.

### Stream totals (all years)

| cohort | n | ever played | career games (zeros incl) min/med/mean/max | career avg (zeros) med/mean | career avg (played-only) n, med | on board | surv v med/mean/max | back page | whole-cohort v med/mean |
|---|---|---|---|---|---|---|---|---|---|
| SSP 2018–25 | 52 | 43/52 (83%) | 0 / 10 / 25.0 / 106 | 48.3 / 42.9 | n=43, 51.6 | 28/52 | 200 / 448 / 3484 | 10/52 | **8 / 241** |
| MSD 2019–26 | 106 | 74/106 (70%) | 0 / 6 / 16.9 / 156 | 40.3 / 35.2 | n=74, 49.9 | 63/106 | 248 / 611 / 4180 | 20/106 | **39.5 / 363** |
| OTHER 2003–25 | 231 | 102/231 (44%) | 0 / 0 / 19.8 / 310 | 0 / 22.5 | n=102, 50.3 | 58/231 | 202 / 317 / 3782 | 21/231 | **0 / 79.5** |
| RD 2003–25 | 693 | 377/693 (54%) | 0 / 2 / 38.3 / 337 | 34.0 / 32.2 | n=377, 59.8 | 66/693 | 416 / 751 / 6029 | 37/693 | **0 / 71.6** |

**Read this table's whole-cohort `v` with care — it is cohort-age-dominated, not a quality ranking** (owner-caught
2026-07-29). The all-years denominators span up to 23 entry years, and every retired/delisted member counts 0
regardless of career quality: RD's 373 pre-2011 entrants averaged 40.6 career games each — 188 played, 66 reached
100 games, 22 reached 200 (Eddie Betts 337, Luke Breust 288, Kieren Jack 234 at a 112 peak average) — and every one
contributes 0 to the 71.6 whole-cohort mean **because they are retired**, exactly as sold shares show $0 in a current
portfolio. RD's 2019–25 entrants run 330–368 — right alongside the MSD. MSD (2019–) and SSP
(2018–) look stronger here partly because their cohorts are young enough to still be listed. Cross-stream
comparison is only meaningful on the mature-window rows in §4, where entry age is held comparable — and RD is
context only throughout: no RD row feeds the free-hit conclusions or the three-constant comparison.

First-season-after-entry production (separate from career): SSP 43/52 debuted — fs games med 9, fs avg med 48.9;
MSD 74/106 — fs games med 4, fs avg med 48.0; OTHER 101/231 — fs games med 4, fs avg med 44.0; RD 375/693 —
fs games med 6, fs avg med 52.6. The free tier's typical debut season is **4–9 games at an average in the mid-40s**.

### The named window cohorts

| cohort | n | ever played | career games med | career avg (played) med | first-season games med / avg med | on board | surv v min/med/mean/max | whole-cohort v med/mean | ≥150 | ≥250 | ≥528 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SSP for-2026 (sy2025) | 9 | 9/9 | 9 | 46.9 | 7 / 47.6 | 9/9 | 10 / 95 / 196 / 437 | 95 / 196 | 4/9 | 4/9 | 0/9 |
| SSP for-2025 (sy2024) | 8 | 8/8 | 11.5 | 47.7 | 9.5 / 44.1 | 6/8 | 6 / 101 / 359 / 1400 | 49.5 / 269 | 2/8 | 2/8 | 2/8 |
| MSD 2026 | 18 | 12/18 | 2 | 58.5 | 4.5 / 58.5 | 18/18 | 29 / 238.5 / 334.5 / 920 | 238.5 / 334.5 | 14/18 | 8/18 | 6/18 |
| MSD 2025 | 16 | 14/16 | 10 | 50.3 | 4.5 / 45.0 | 15/16 | 10 / 197 / 393 / 2090 | 196 / 368 | 9/16 | 6/16 | 2/16 |
| MSD 2024 | 17 | 13/17 | 10 | 48.1 | 6 / 48.1 | 12/17 | 19 / 275 / 599 / 2823 | 162 / 423 | 9/17 | 7/17 | 3/17 |

Caveat on the two 2026 cohorts: everyone is (SSP sy2025) or almost everyone is (MSD 2026) still on the board because
there has been no delisting window yet, and their v is dominated by the engine's own entry pricing rather than
realised careers (6/18 MSD-2026 players have not yet played a game but carry v 52–586). Their whole-cohort ≈
survivors-only equality is a cohort-age artifact, not evidence against the survivor effect.

### Per-year board-value drift (whole-cohort vz vs survivors, absent=0)

SSP by signing year: sy2018 n=9: vz med 0 / mean 83 (3 on board); sy2019 n=4: **0/4 ever played**, vz 0/0;
sy2020 n=6: 43/103; sy2021 n=5: 0/697 (one survivor: nicholas-martin v=3484); sy2022 n=7: 286/535;
sy2023 n=4: 0.5/9.5; sy2024 n=8: 49.5/269; sy2025 n=9: 95/196.

MSD by year: 2019 n=9: vz med 0 / mean 238 (1 survivor: john-noble v=2143); 2021 n=20: 0/659 (8 on board, med 1584 —
the newcombe/durham/moyle/turner year); 2022 n=15: 0/148; 2023 n=11: 0/166; 2024 n=17: 162/423; 2025 n=16: 196/368;
2026 n=18: 238.5/334.5. Pattern: the **median falls to 0 within 2–4 years of entry** for every cohort old enough to
have been through delistings; the mean is carried by 1–3 outliers per cohort.

### OTHER by sub-type

| sub-type | n | ever played | on board | surv v med/mean/max | whole-cohort v med/mean |
|---|---|---|---|---|---|
| IRE (Ireland) | 57 | 23/57 (40%) | 14/57 | 131.5 / 149 / 347 | 0 / 36.6 |
| PDA (Academy) | 51 | 31/51 (61%) | 15/51 | 262 / 568 / 3782 | 0 / 167 |
| PDN (Next Gen) | 43 | 17/43 (40%) | 16/43 | 248 / 308 / 723 | 0 / 115 |
| PDS (Scholarship, 2007–11) | 21 | 7/21 (33%) | 0/21 | — | 0 / 0 |
| UNR (Unregistered) | 59 | 24/59 (41%) | 13/59 | 119 / 218 / 608 | 0 / 48 |

### PSD remnant (8 stamped pick-1 rows, 2003–2021)

All 8 played (careers 44–337 games, career avg med 75.6 — rockliff 100.8, betts 71.9 across 337 games, etc.);
1/8 on today's board (luke-nankervis, v=457). These are **pick-1 PSD selections of never-previously-listed players**
— a doubly-selected remnant (best slot, and the rare non-redraft), not a window tier. They demonstrate the store's
PSD blindness, not PSD value.

## 3. ORDER STRUCTURE (does taken-order predict realised value?)

Only MSD carries an order field among the free windows (SSP/OTHER pickless; store MSD slots run 1–n per year with no
gaps because redrafts are excluded).

**MSD 2025 per pick (most recent complete MSD cohort, n=16)** — career games / career avg / current v:

| pk | player | g | cAvg | v | | pk | player | g | cAvg | v |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | tom-mccarthy | 28 | 91.9 | 1594 | | 9 | cooper-trembath | 22 | 65.5 | 2090 |
| 2 | zac-banch | 8 | 33.6 | 42 | | 10 | ewan-mackinlay | 15 | 54.8 | 45 |
| 3 | harrison-ramm | 3 | 21.0 | 388 | | 11 | zac-walker | 0 | 0 | 280 |
| 4 | flynn-young | 11 | 40.2 | 10 | | 12 | lachlan-blakiston | 28 | 51.9 | 19 |
| 5 | michael-sellwood | 18 | 61.4 | 197 | | 13 | caleb-lewis | 2 | 12.5 | 205 |
| 6 | archie-may | 17 | 51.0 | 471 | | 14 | noah-howes | 0 | 0 | 306 |
| 7 | roan-steele | 20 | 49.7 | 22 | | 15 | mani-liddy | 9 | 51.1 | 30 |
| 8 | jacob-newton | 5 | 26.8 | 195 | | 16 | oskar-smartt | 4 | 24.8 | 0 (departed) |

Banded, MSD pooled 2019–2025 (n=88):

| picks | n | ever played | games med/mean | v(zeros) med/mean | share ≥528 |
|---|---|---|---|---|---|
| 1–5 | 30 | 22/30 (73%) | 9.5 / 19.2 | 0 / 496 | 6/30 |
| 6–10 | 29 | 20/29 (69%) | 11 / 23.3 | 22 / 409 | 6/29 |
| 11–20 | 29 | 20/29 (69%) | 4 / 16.8 | 19 / 198 | 3/29 |

Within-cohort Spearman rho (pick vs outcome): 2021 +0.08/−0.07 (games/v), 2022 −0.21/−0.46, 2023 −0.02/−0.12,
2024 −0.11/+0.14, 2025 −0.37/−0.30, 2026 −0.20/−0.22; pooled 2021–26 with picks normalised within year
(n=97): **rho(pick, games) = −0.12, rho(pick, current v) = −0.15**.

Finding: **taken-order carries only a weak signal** — a mild early-pick advantage visible in the pooled means
(1–5 vs 11–20: mean vz 496 vs 198; ≥528 share 20% vs 10%) but inconsistent year to year, sign-flipping, and absent
in the medians (0/22/19). The engine's existing choice to never consume MSD pick order and to declare "order of
selection carrying no value" for the pool (`pvc_curve_v2.json` split note; MSD priced at a single pick-equivalent)
is consistent with this measurement. Corroboration from the rookie tail: RD 2015–2022 (n=154) banded by slot shows
mean vz 327/98/68 (slots 1–10/11–20/21+) with all medians 0 and rho(slot, v) = −0.14 — order matters a little at the
mean, nowhere near a curve.

## 4. THE THREE-CONSTANT COMPARISON — 150 vs 250 vs 528

Where the constants live: 528 is committed (`pool_value`, `engine/rl_after/pvc_curve_v2.json`; effectively the
adopted curve's own index-65 value — PVC[64] = 530). 250 was **not found as a literal in the checked-in clubs-tab
code** (grepped `ui/app/*.js`, `club_totals.js`, build scripts); it exists in the register only inside the #270
filing ("250/528/FHV reconciliation") — the current clubs tab prices future slots off the PVC phantom layer
(pick 1 = 3000 ... mechanisms at pick-equivalent 90/92 per `phantomTotals._meta.pickeq`). 150 is the owner's
illustrative guess (not in code).

Side-by-side: survivors-only (the overstating view) vs whole-cohort-with-zeros (the honest view), plus the share of
each cohort clearing each constant **today**:

| cohort | n | SURVIVORS n | surv v med / mean | WHOLE v med / mean | ≥150 | ≥250 | ≥528 |
|---|---|---|---|---|---|---|---|
| **Mature** (entry ≥3 seasons ago) | | | | | | | |
| SSP sy2018–22 (seasons 19–23) | 31 | 11 | 377 / 782 | **0 / 277** | 8/31 (26%) | 8/31 (26%) | 4/31 (13%) |
| MSD 2019–23 | 55 | 18 | 657 / 1077 | **0 / 352** | 13/55 (24%) | 10/55 (18%) | 10/55 (18%) |
| OTHER 2015–22 | 100 | 20 | 187 / 487 | **0 / 97** | 11/100 (11%) | 9/100 (9%) | 5/100 (5%) |
| RD 2015–22 (context) | 154 | 37 | 388 / 880 | **0 / 211** | 29/154 (19%) | 25/154 (16%) | 14/154 (9%) |
| **Still-maturing** | | | | | | | |
| SSP sy2023–25 | 21 | 17 | 89 / 233 | 37 / 189 | 6/21 (29%) | 6/21 (29%) | 2/21 (10%) |
| MSD 2024–26 | 51 | 45 | 229 / 425 | 197 / 375 | 32/51 (63%) | 21/51 (41%) | 11/51 (22%) |
| **Combined free mechanisms (SSP+MSD+OTHER)** | | | | | | | |
| all years | 389 | 149 | 240 / 466 | **0 / 178** | 97/389 (25%) | 70/389 (18%) | 33/389 (8%) |
| mature 2015–23 | 200 | 57 | 240 / 676 | **0 / 193** | 35/200 (18%) | 28/200 (14%) | 19/200 (10%) |

The survivor effect, quantified: for every mature window the survivors-only mean is **2–3x** the whole-cohort mean
(SSP 782 vs 277; MSD 1077 vs 352; OTHER 487 vs 97; combined mature 676 vs 193), and survivors-only medians
(187–657) sit against whole-cohort medians of **0**. The currently-listed free-mechanism pool (n=149, v med 240,
mean 466; 32/149 have still never played) is precisely the survivor set — any constant read off currently-listed
pool players inherits this overstatement.

What the evidence says qualitatively about each constant (no pricing formula proposed — pricing is a later
project's job):

- **528** clears only 8% of all free-mechanism entrants ever (33/389), 10% of the mature set, and 13–18% of even
  the two strongest windows (SSP/MSD mature). It equals the 54th percentile of the whole active board and is
  numerically the fitted curve's own tail (PVC[64]=530) — it reads as the value of a **surviving, established**
  pool player, i.e. exactly the survivor-conditioned number this study exists to expose, and overstates the
  whole-cohort mean of the best window (MSD mature, 352) by ~50% and the combined mature mean (193) by ~2.7x.
  The register's own earlier supplement points the same way ("SSP pedestal at 92 vs ~51 delivered (n=24, thin)",
  OPEN_ITEMS_REGISTER item 1).
- **250** ≈ the median of today's surviving free-mechanism players (240) and ≈ the whole-cohort **mean** of the
  strongest recent windows (SSP for-2025 269; MSD 2024–26 375, but that figure is prior-heavy) — defensible only
  as a survivors-median or as a mean that leans on the MSD window; it is ~4–5 units above nothing in median terms
  (mature medians are 0) and only 14–18% of mature entrants clear it today.
- **150** is the only constant *below* every window's whole-cohort mean (mature: SSP 277, MSD 352, OTHER 97 —
  OTHER alone undershoots it) yet still above the whole-cohort median of every mature cohort (0). On the
  expectation (mean) view the free tier is worth more than 150 for SSP/MSD but less than 150 for the OTHER family;
  on the typical-outcome (median) view even 150 is generous.
- The comparison is dominated by **which statistic you mean**: the tier is a lottery — means are carried by a
  handful of hits (newcombe 4180, bodhi-uwland 3782, nicholas-martin 3484, max-hall 2823 head the entire
  389-entrant class) while the modal outcome is delisting at ~0 within 2–4 years. Whole-cohort means land
  roughly between 150 and 375 by window; whole-cohort medians land at 0–240 depending only on cohort age.
  Between the three constants: 528 is a survivors' number; 250 straddles (survivor-median / strong-window mean);
  150 is a below-mean, above-median floor. The owner's hypothesis — that the free tier is much weaker than
  currently-listed pool players suggest — is **supported**: the listed-survivor view (med 240 / mean 466) runs
  2–3x the honest whole-cohort view (med 0 / mean 178–193).

## 5. DATA LIMITS (what the store cannot see)

1. **Available-but-untaken players do not exist in the store.** One row per player at initial entry only; nobody who
   nominated for / was eligible at a window and went unpicked is recorded. Every denominator above is
   "players actually taken", so the option value of the *choice set* at each window is unmeasurable here.
2. **Redrafts are excluded by owner data law** (`pick_semantics_schema.md`: "Players previously listed are excluded
   when redrafted, and only their initial entry is recorded"). Windows whose real traffic is heavily recycled
   players are therefore undercounted subsets: PSD collapses to 8 first-entry rows (2003–2021, all pick 1) and the
   MSD/SSP cohorts here are first-entry intakes only — a club's typical MSD/SSP acquisition of a previously-listed
   player is invisible, and its FHV contribution is unmeasured.
3. **Delistings that never re-entered leave no value trail.** Departed players either sit on the `back` page
   (198, residual v med 12 — recent exits) or vanish from the board entirely; this study counts both as 0. The 0
   is a club-value statement, not a career statement, and pre-`back`-page exit dates are not stored (only 13
   records carry `_last_listed`).
4. **Recent-cohort board values are the engine's own priors** (circularity): all 9 SSP-for-2026 and 18/18 MSD-2026
   entrants are on the board, 6 of the MSD-2026 without a senior game yet carrying v 52–586 — those v's descend
   from the very pedestal/pool constants under review, so 2025–26 cohorts cannot arbitrate between the constants.
5. **Small n everywhere in the free tier**: SSP years are n=4–9, MSD years n=9–20; single players (newcombe,
   martin, uwland) move cohort means by hundreds of units. The 2019 SSP class (n=4) never played a game; the 2021
   MSD class alone contributes 4 of the top-8 free-tier survivors.
6. **2026 is a partial season** (`SEASON_PROG` 0.83); all 2026 games/averages and hence current v are in-flight.
7. Minor store frictions handled explicitly: `games` is a mixed-vintage snapshot (scoring rows used as authority;
   3 records have games with no scoring rows); 3 SSP rows carry pre-entry scoring (prior stints folded in);
   16 records have scoring but `games`=0; one RD career avg is negative (−14.0, real scoring row).

---
*Method note: all statistics computed with python over the two JSON stores; distributions reported as
n / min / median / mean / max; "whole-cohort" always counts never-established and off-board members at 0;
no engine code executed, no repo file modified.*
