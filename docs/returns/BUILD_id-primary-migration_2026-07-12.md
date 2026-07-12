# BUILD REPORT — ID-primary migration v1a — 2026-07-12 — TIER 2 — **BUILD-REPORTED / ESCALATED**

Branch: `claude/id-primary-migration-v1a-cv1uzl` · Base: main `626c83780f678c9204e1fcf80f43868b239dfc2f`
Effort: High · Mode: auto · Status: **HALTED at the guard boundary — Tier-1 ruling required before the store moves.**

## 0. BASE VERIFICATION (first act) — ALL PASS
- `git ls-remote` main == `626c8378…` (pinned) ✔ · not newer ✔
- tag `v2.8` == `9bd0cfdbf9…` ✔
- boot store `04f38dad` == `data/expected_boot.json` pin ✔ (Guard 5 green on entry)
- input `docs/inputs/authoritative_universe_v2.csv` md5 == `3e3f9f580cba5d62bd719075123501c6` ✔ (804 rows)
- Baseline `run_panel.sh` = **PASS 10/10** on the untouched store.

## 1. WHAT THIS BUILD DID
Measured the full migration against the v2.8 shipped board (9ecbe0fa) by regenerating the board
(`rl_export.py`) on baseline vs. migrated store and diffing every player's SCAR. Decomposed the
change into its four rule-classes to attribute every mover. Built the name→ID resolver. **The
source store was NOT modified** — the finding below is a guard-red that the directive routes to
Tier-1 ("ANY … unexpected mover → STOP, report, escalate to Tier 1. Do not self-amend anything").

## 2. THE CLEAN SCOPE (safe, surgical, exactly as intended)
Isolation (each class applied alone; identity-alone = 0 movers is also the determinism control):

| class | board movers | verdict |
|---|---|---|
| identity — `stable_player_id` + `affl_team` + `eligibilities` on 804 rows | **0** | inert; new fields, not read by `ev()` |
| DOB — `_by`/`_bd` import | **5** = exactly the named DOB rows | clean (age keys off `_by` only) |

- `stable_player_id` attaches to all 804 csv-matched rows; 0 duplicate ids; historical/unmatched
  rows untouched (no synthetic ids); `taylor-adams` correctly carries NO id (not in the csv).
- `eligibilities` imported to a NEW field — does NOT touch `drafted/present/future_position`
  (positional judgment preserved, per the current-season-DPP standing law).
- The 5 named DOB corrections reprice ONLY those 5 (old→new below), zero collateral.

## 3. THE FINDING — the two store-population changes detonate the board (THE ESCALATION)

| class | board movers | note |
|---|---|---|
| re-entry trio (perez/mcandrew/keane → pickless SSP) | **657** | up to ±25%; hits owner-watched players |
| taylor-adams retire (`_retired=True`) | **90** | adams removed (expected) + **89** unnamed ±1 SCAR |
| FULL migration (all classes) | **671** | 7 named movers + **664 unexpected refit ripple** |

**Root cause (code-read).** The board is a global equilibrium over the store population. Every
engine load recomputes population-dependent quantities BEFORE pricing:
`_merged_recover.py:9-12` builds `era`/`REF` (per-season league means) over the whole population,
and `:15-16` **fits a GradientBoostingRegressor calibration model at load-time on the pool
`debutyr<=2021 AND (pick or _ft)`**. Making perez + mcandrew pickless (`pick→None`) removes them
from that calibration pool → the fitted developmental model shifts → **every player re-prices a
little**. Marking adams retired re-solves a position-population statistic → 89 neighbours drift ±1.
Inert identity fields and single-row `_by` tweaks stay local (they don't change pool membership);
entry-class and retired-flag changes do not.

**The irony that makes this decision easy.** The re-entry ruling's INTENDED effect is nearly nil:
- `flynn-perez` **14 → 14** (NO CHANGE — production too low for pick capital to bind; the register's
  "perez will re-price" prediction does not hold on the board),
- `mark-keane` 1636 → 1648 (**+0.73%**),
- `lachlan-mcandrew` 1039 → 1191 (**+14.63%**, and that lift is dominated by his DOB correction,
  not the entry switch).
So the ruled change buys **~zero** intended movement on the named players while spraying a
**657-player collateral ripple** — including `jai-newcombe` −8.2% (an open owner investigation
row), `sam-durham` −7.1%, `john-noble` −5.7%, `massimo-d-ambrosio` −8.4%. Those reads would be
confounded by a change that was never about them.

**Decomposition — the detonator is one player: lachlan-mcandrew.** Applying each re-entry field
class alone (board movers vs. the v2.8 shipped board):

| re-entry variant applied | board movers | reading |
|---|---|---|
| `perezonly` (full re-entry, perez alone) | **7** | negligible; perez is a low-leverage pool row |
| `keaneonly` (full re-entry, keane alone) | **0** | keane is pickless already → never in the pool |
| `mcandrewonly` (full re-entry, mcandrew alone) | **653** | **the detonation** |
| `pickexit` (perez+mcandrew pickless, keep year) | 657 | pool-exit via the `pick` filter |
| `yearonly` (trio year→re-entry-year, keep pick/type) | 657 | pool-exit via the `debutyr>2021` filter |

Two independent take-aways: (1) the whole ripple is **mcandrew's** entry-switch — he is a productive
young ruck and a high-leverage row in the load-time calibration pool, so evicting him swings the
fitted model across the board; perez contributes 7, keane 0. (2) There is **no minimal re-entry
that stays in-fence and avoids it**: pickless (evicts via the `pick` filter) AND later-year (evicts
via the `debutyr>2021` filter) each trigger the same 657-row refit on their own.

## 4. WHY THIS IS A HALT, NOT A "just re-pin it"
G-DATA (BINDING) includes **board parity for non-movers** and **panel 10/10**. The full migration
moves the pinned panel itself (Daicos 8050→8039, Gawn 2538→2509, …) and 664 non-named players.
Re-pinning the panel + board to a detonated equilibrium would *hide* the ripple, not resolve it —
and "accept the ripple" vs "localize it" is an engine-architecture call, above Tier-2 and outside
this build's FENCE (which is OUT on "any valuation/guard/gate logic"). Per the directive I did not
self-amend: the store, board, and boot pin are **byte-unchanged**; the five guards + panel remain
green on the untouched source.

## 5. DECISION REQUIRED (Tier-1 / owner)
**On the re-entry trio (657-player ripple, ~zero intended benefit):**
- **(A) — recommended — DEFER the re-entry trio.** Ship the clean, surgical migration now
  (804 ids + `affl_team`/`eligibilities` + the 5 DOB corrections + adams retire), which is what the
  owner actually wanted the migration to deliver, and take the re-entry reclassification into the
  v2.9 lever build where a board-wide reprice is in-scope and can be ruled with the SSP-line and
  ruck-scarcity questions it interacts with. (Note: even deferring, adams-retire carries an 89-row
  ±1 ripple — see B.)
- **(B) localize it** — an engine change (OUT of this fence) to hold the load-time calibration pool
  membership stable across the reclassification, so perez/mcandrew move onto the pickless basis
  without the collateral refit. Requires a Tier-1 engine directive.
- **(C) accept the full 671-row reprice** as the true consequence, re-pin panel+board at this
  migration bake, and put the COMPLETE affected-row list (committed) in front of the owner. This is
  what the directive's Tier-2 deliverable literally asks for — but it abandons non-mover parity and
  confounds several open owner reads for ~zero intended benefit.

**On taylor-adams:** marking him `_retired=True` matches the store's existing 1847 retirees and is
the right non-live representation, but it carries an 89-row ±1 collateral ripple from a position
statistic. Same class of decision (accept the small ripple vs. localize).

## 6. NAMED-ROW LEDGER (old → new SCAR, full migration)
| row | old | new | delta | cause |
|---|---|---|---|---|
| riley-onley | 2 | 496 | +24700% | dob-age (_by 2000→2007) |
| fred-rodriguez | 3 | 522 | +17300% | dob-age (_by 2000→2007) |
| nick-driscoll | 5 | 571 | +11320% | dob-age (_by 2000→2007) |
| leon-kickett | 4 | 408 | +10100% | dob-age (_by 2000→2006) |
| lachlan-mcandrew | 1039 | 1191 | +14.63% | dob-age (_by 1999→2000) + entry-switch (MSD p12→SSP-2024) |
| mark-keane | 1636 | 1648 | +0.73% | entry-switch (IRE-2018→SSP-2022) |
| flynn-perez | 14 | 14 | 0.00% | entry-switch (ND-2019-p35→SSP-2025) — own value unchanged |
| taylor-adams | 75 | removed | — | retirement (mid-season; `_retired=True`) |
| luke-nankervis | 357 | 357 | 0.00% | NO-IMPORT (store PSD pick 2 stands; csv RD-1 ignored) ✔ |
| max-king-stk / -syd | — | — | separate | distinct ids; collision sentry stays GREEN ✔ |

The COMPLETE 671-row affected list (every mover, cause-attributed) is committed at
`docs/returns/id-migration/AFFECTED_ROWS.md` (+ `.csv`).

## 7. GUARD STATUS (on the untouched source — unchanged from v2.8)
The source store is byte-exact v2.8 (`md5 04f38dad` == `data/expected_boot.json` pin), so the whole
suite reproduces the v2.8 bake result:
- **Guard 5 (boot-store)** — PASS on entry (bootstrap + panel), store `04f38dad` == pin.
- **Panel** — **PASS 10/10** (Daicos 8050 … Green 588, byte-exact) WITH `id_resolver.py` present —
  proving the new module is guard-safe and pricing is untouched.
- **Guards 1-4 (read-only stamps / source-hash / lookalike tripwire / correction canary)** — run
  fresh on the byte-exact source; confirmatory (they passed at the v2.8 bake on this same store).
- **Collision sentry (two Max Kings)** — GREEN; the resolver returns distinct ids for
  `max-king-stk` / `max-king-syd` and never collapses them (a Sydney-side "Max King" is vetoed, not
  mis-attached).

Nothing was baked; the store, board (`9ecbe0fa`), and boot pin are byte-unchanged; no tag, no
promote, no merge, no PR opened. The only repo change is the new `engine/rl_after/id_resolver.py`
plus this report and the committed affected-row list.
