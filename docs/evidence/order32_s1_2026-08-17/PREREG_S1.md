# PREREG — ORDER 32 SEAT S1: AGE-REFERENCED BARS FOR THE STALL GATE

**Filed BEFORE any result is computed.** Everything below this line was written from schema
inspection only (field names, field coverage, vocabulary values, the season-state fraction, and the
already-established facts quoted in the seat brief). No distribution, no cell mean, no
classification rate, no construction value existed when this file was committed. Results computed
before this file's push are void by house law.

Seat: S1 (measurement, READ-ONLY — no engine code, no board, no law is touched).
Program brief: issue #334 comment 5311991190. Branch: `land/order-29` at store `cb38ef11`
(tree `53f7433`).

---

## 1. THE QUESTION

The ORDER 31-F candidate's stall gate (`engine/rl_after/_merged_recover.py::o31_stall_run`,
~line 3319) counts a played season as a stall season when

```
games < 10 x season-fraction   OR   season avg < _O30BP_BARS[gfut(p)]
```

with `_O30BP_BARS` = the owner's Ruling-1 replacement bars: KPD 65.4, KPF 63.8, MID 77.1,
RUCK 75.5, SD 75.3, SF 67.9 — position-level and AGE-BLIND. Established consequence (measured by a
prior seat, not re-derived here): 94% of played rows with 1–50 career games are stall-flagged;
median price cost 8.5%, p90 37%. A 19-year-old KPD averaging 59.7 (harry-dean, pick 3) reads as a
staller; the owner considers that a solid season for that age.

The question this seat answers: **should the GATE's avg bar be age-referenced, and if so at what
values, per age x position — judged by whether the bar separates seasons that presage delivered
careers from seasons that presage washouts.**

One structural fact, stated up front because it bounds everything: the avg bar only BINDS on a
season that already passes the games test (games >= 10 x season-fraction). A season below the games
bar is stall-flagged on games alone and NO avg-bar construction can change that. This seat will
report what share of young flags are avg-only flags — that share is the maximum the re-reference
can relieve.

## 2. DATA AND DEFINITIONS (all fixed before computation)

- **Store**: `engine/rl_after/rl_model_data.json` on this tree — 2,650 players, per-player
  `scoring` arrays `{year, games, avg, pos}`, seasons 2005–2026. 2026 is in progress at
  calendar_progress 0.92 (`data/season_state.json`), so the gate's live games test for 2026 is
  games >= 9.2.
- **AGE** = season year − `_by` (birth year; present on all 2,650 rows). This is the owner's own
  convention — it reads harry-dean's 2026 as his age-19 season (2026−2007). `_bd` (exact birth
  date) exists on only 1,150 rows, so the year-difference convention is used uniformly; the
  ~half-year within-cohort spread this ignores is disclosed, not corrected.
- **POS** = the player's `future_position` (the store's `_futpos`; one of the six groups). This is
  the gate's OWN bar key (`gfut(p)`), so over/under-bar classification here reproduces the gate
  exactly. Sensitivity cut: the season row's own `pos` primary label (first token of e.g. `SF/MID`).
- **FULL SEASON** (a season the avg bar can bind on): games >= 10 for completed years; for 2026,
  games >= 10 x 0.92 = 9.2 — exactly the gate's own games test. Justification: below it the bar is
  irrelevant (see §1). Distribution tables are also shown at games >= 6 as sensitivity; the
  predictive analysis uses the gate's own >= 10 definition.
- **FITTED WINDOW** for every predictive number: season years **2005–2021** — every fitted season
  has >= 5 subsequent seasons observable (2022–2026). Sensitivity: extend to 2022. Seasons
  2023–2026 appear in distribution tables (which need no follow-through) and in the named-row
  application, never in a fitted predictive cell.
- **OUTCOME 1 — DELIVERED-LATER (binary)**, per season (player, Y): there exists a later season
  y > Y with games >= 10 AND avg >= flat bar(POS). The FLAT Ruling-1 bar stays the outcome
  criterion by design: it is the owner's ruled mature replacement level, and the question under
  test is only whether the gate misreads YOUNG seasons against it — not whether the mature bar is
  right.
- **OUTCOME 2 — SDV (continuous)**, per season (player, Y): subsequent delivered value
  = Σ over later seasons y > Y of games x max(0, avg − flat bar(POS)). v0-language surplus points,
  the same language as the delivered-value lane. (2026 games counted raw, not grossed up —
  disclosed conservatism, small at 0.92.)
- **Career windows — the #338 basis** (`docs/evidence/noarb_338_2026-08-06/README.md`, rule commit
  `30996f8`): a drafted player is listed for a minimum tenure (4 seasons ND picks 1–20, 3 for
  ND 21–40, 2 otherwise) whether or not the DB kept numbers. Consequence adopted here: a season row
  followed by listed years with no scoring is followed by LISTED years of zero delivery — not
  missing data; and a career that ended (delisted, retired) is a FINAL outcome, not truncation.
  Because every fitted season has >= 5 observable subsequent years and the store's scoring gaps
  inside tenure are zero-games years for outcome purposes either way (they deliver nothing),
  the #338 rule changes no fitted cell's population — it changes only the READING of
  never-delivered careers (final, not censored). This will be stated in the packet, and any named
  row where the distinction binds will be called out.
- **WASHOUT**: a fitted season whose player never posts a delivered season afterwards
  (Outcome 1 = 0). An active player who has not delivered by 2026 despite >= 5 years is counted a
  washout for his fitted seasons; count of such still-active non-deliverers disclosed.
- **Age cells**: ages 18, 19, 20, 21, 22, 23, and 24+ pooled ("mature"). Under-18 seasons (if any
  exist) fold into 18 and are counted. The mature reference band for construction anchoring is
  **24–28** (full seasons, 2005–2025 completed years — the reference needs no follow-through so it
  may use the full store).

## 3. THE CONSTRUCTIONS (designed now, values computed after push)

- **C0 — the current flat bar** (baseline): bar(a, POS) = flat for all a.
- **C1 — age-quantile-matched**: find q*(POS) = the quantile at which the flat bar sits within the
  mature (24–28) full-season avg distribution for POS. Then bar(a, POS) = the q*(POS)-quantile of
  the age-a x POS full-season avg distribution. "The same strictness at every age."
- **C2 — equal false-flag anchoring**: bar(a, POS) set so that the under-bar rate among fitted
  seasons of EVENTUAL DELIVERERS at age a equals the mature (24+) under-bar rate among eventual
  deliverers under the flat bar. "A young season on a delivered career is flagged no more often
  than a mature one."
- **C3 — development-curve offset**: Δ(a, class) = mean mature full-season avg − mean age-a
  full-season avg, with class = TALL {KPD, KPF, RUCK} vs SMALL {MID, SD, SF} pooled (thin-cell
  robust); Δ floored at 0 and required non-increasing in age (pool-adjacent-violators if needed,
  disclosed). bar(a, POS) = flat(POS) − Δ(a, class).
- **CAP LAW (design constraint, binding on all constructions)**: bar(a, POS) <= flat(POS) always.
  This order's scope is to relieve false flags on the young; no currently-passing season may become
  flagged. The milan-murdock guard (mature, Φ=1.00, above-bar) is therefore structural, and the
  packet will still verify it row-by-row for the named ten.
- Per-cell n and dispersion published for every cell of every construction; cells with n < 15 are
  marked THIN and never silently smoothed — where a position-level cell is thin the class-pooled
  value is used and the substitution is printed in the table.

## 4. WHAT WILL BE MEASURED (the tables the packet must contain)

1. Season-count census: seasons by age x POS, at games >= 1, >= 6, >= 10 (the gate's own bar-live
   set), plus the avg-only vs games-only flag decomposition for career-games 1–50 rows.
2. Full-season avg distributions per age x POS: n, mean, sd, p10/25/50/75/90, share under flat bar.
3. Predictive tables (fitted window), per age band x POS (class-pooled where thin): among
   OVER-bar and UNDER-bar full seasons under C0/C1/C2/C3 — n, share DELIVERED-LATER, median and
   mean SDV; misclassification both ways: eventual-deliverer seasons flagged (false flags) and
   washout seasons passed (misses); relative risk of washout given under-bar.
4. The recommended construction's full bar table (value per age x POS with n and dispersion per
   cell), before/after flag rates on the current 2026 board's young rows, and the named ten:
   harry-dean, kye-annand, cooper-duff-tytler, alix-tauru, jordan-croft, jedd-busslinger,
   ethan-read, isaac-kako, nick-madden, milan-murdock — each with their seasons, gate reading
   before/after (games test, avg test, stall run s).
5. The coupling note (§5 of the brief): `_O30BP_BARS` also defines the v0-language production
   reference (the two retained par denominators re-referenced to the effective positional bars).
   Re-referencing the GATE only = a new, separate object consumed by `o31_stall_run` alone; the
   packet names the coupling and the risk of a silent ripple if the shared object were edited
   in place. (No engine edit is made by this seat either way.)

## 5. PREDICTIONS (falsifiable, committed now)

- **P1**: mean full-season avg at ages 18–19 sits 8–20 points below the mature (24–28) mean in
  both classes, with the TALL gap at the larger end.
- **P2**: the flat bar sits between the 35th and 65th percentile of mature full seasons for every
  position, but at or above the 75th percentile of age-18–19 full seasons for the TALL positions.
- **P3**: the false-flag rate (eventual-deliverer full seasons read under-bar) under the flat bar
  at ages 18–20 is at least 2x the mature rate.
- **P4**: the flat bar separates worse when young: relative risk of washout given under-bar at ages
  18–20 is materially lower than at 24+ (young under-bar seasons are much more often on delivered
  careers than mature under-bar seasons).
- **P5**: at least one age-referenced construction cuts young eventual-deliverer false flags by
  >= one-third while raising the washouts-passed share by less than the false-flag cut (in
  percentage points).
- **P6**: under the recommended construction harry-dean's 2026 (KPD, 59.7, 17 games) passes the
  avg test; milan-murdock's reading is unchanged (cap law).
- **P7 (structural, verifiable without fitting)**: a material share — predicted > half — of the
  established 94% young-row flag rate is games-test flags that NO bar construction can relieve;
  the packet will report the avg-only share exactly.

## 6. FALSIFIERS (what would kill the recommendation, committed now)

- **F1**: if n(age 18–19 x POS, full seasons) < 15 for a position, a position-level bar at that
  age is UNSUPPORTED for that cell; only the class-pooled construction may be recommended there,
  and the packet says so cell by cell.
- **F2**: if the flat bar's under-bar young seasons predict washout about as strongly as mature
  ones (relative risk within 20% of the mature RR), the age re-reference is NOT supported; the
  seat recommends keeping the flat bar and says so.
- **F3**: if no construction cuts young deliverer false flags without passing >10 percentage
  points more true washouts, the seat recommends none.
- **F4**: if the avg-only flag share among young flagged rows is small (< 20%), the bar
  re-reference is second-order for the constituency and the packet must lead with that, whatever
  the construction tables show.

## 7. EXCLUSIONS AND THRESHOLDS, NAMED ONCE

- Seasons 2026 never enter a fitted predictive cell (in progress). Fitted window 2005–2021.
- Gameless seasons never enter the season table (the gate skips them; they are D(c_u)'s channel).
- No era normalization (owner ruling: scores are era-comparable by construction; read raw).
- No winsorisation anywhere; distributions reported by quantiles instead.
- Dual-position season labels: bar key = future_position (the gate's key), sensitivity by season
  primary label.
- Thin-cell law: n < 15 = THIN, printed, class-pooled substitute used, never silent smoothing.

*Committed and pushed before any measurement script was run. — Seat S1, 2026-08-17.*
