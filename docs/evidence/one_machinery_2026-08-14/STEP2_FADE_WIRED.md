# STEP 2 — THE RULED SITTER FADE, WIRED. The stop is resolved; sitting is priced.

**ORDER 30B build seat · `land/order-29` · 2026-08-14 · resumes from `STOP_STEP2_FADE_RULER.md`.**

## 1. THE RULING THIS WIRES

Owner, #334 comment `5292534855` — **AS MEASURED, FLAT DEEP END**. It answers all three questions the
stop asked, and it amends one earlier ruling:

| stop question | ruling |
|---|---|
| **Q1 — which numbers** | the **R1 re-derived** row. The measurement travels with its ruler. |
| **Q2 — the deep end** | **the measured n=11 cell, HELD FLAT from depth 4 out.** Nothing extrapolates. |
| **Q3 — monotonicity** | **NOT required.** The depth-4 kink is SELECTION and is kept and disclosed. |

Owner's words on the kink: *"players who last on a list that long without production may well do so for
good reason - whereas those who are no good are likely to be delisted before then."* The depth-3 → depth-4
cell count falls **100 → 11** — that is the year-3→4 delist wave, and what survives it is selected.

**RULING 2 IS AMENDED (RETIRED) FOR THIS LAW.** "Extrapolate the fitted decay past year 4" had no coherent
meaning once the decay fitted through depths 2–3 read **0.1176** at year 4 against a measured cell of
**0.3460** — 2.94× apart — because it was being extrapolated *through* a selection kink. The deep end holds
flat instead.

## 2. WHAT IS IN THE ENGINE

`engine/rl_after/_merged_recover.py`, block **ORDER 30B STEP 2**, immediately after the ORDER 29B block.

```
D(1) = 1.0000                     entry — no discount
D(2) = 0.5501935857356868         n = 464
D(3) = 0.26278629823610156        n = 100
D(4) = 0.3460004697526451         n =  11   <- ABOVE D(3): selection, kept, NOT smoothed
D(c) = 0.3460004697526451         FLAT for every c >= 4
```

- **clock** `c(p,Y) = (Y − entry_year(p)) + fE(Y,p)` — continuous, in season fractions. `fE` is the engine's
  **own** `_fEy(Y,p)`: `calendar_progress = 0.92` from `data/season_state.json` for the in-progress season,
  `1.0` for a completed one (and `1.0` for an LTI out-for-the-remainder name, whose season *is* complete at
  his real games). **One clock convention in the engine, not a second one.**
- **interpolation** log-linear in `D`: `D(c) = D(N)^(1−f)·D(N+1)^f`. `c ≤ 1 ⇒ D = 1.0`.
- **MSD** (owner ruling 5): the first season IS season 1, so the MSD clock runs one season ahead of the
  `entry_year + 1` debut convention every other route uses. Wired in `fade30b_clock`; it bites at Step 4.
- **population at this step: ND in-curve only** (`type ND`, pick 1–64) — the exact population the law was
  derived on. **Pool rows are deliberately NOT faded here**; their fade is derived by the same construction
  on their own pathway values at Step 4. Wiring ND-derived numbers onto pool rows would be the
  pathway-specific-machinery mistake this order exists to end, in reverse.

**DECLARED, because packet 2 never had to say it.** Packet 2 quoted its named rows at `NOW = 2026` only.
The generalisation to an as-of year `Y` is the same expression with the same `fE`, so the 24-year as-of
matrix and the board read one law rather than two.

## 3. WHAT IT SUPERSEDES

**ORDER 29B's flat hold** — "a zero-evidence row prints its derived v0, full stop" — and its games-as-of
predicate **as a price law**. The predicate itself survives unchanged as the **population test** (who is a
sitter at `Y`). 29B's printed-day-0 identity is **restated, not dropped**:

> `printed == round(v0 × D(c))`, tolerance 0 — and at `c ≤ 1` (`D == 1`) it reduces to 29B's own equality.

The assert now reads the engine's `_entry30b_price` predicate, so board and engine cannot drift apart.
**Measured on the written board: 89 of 89, tolerance 0.**

## 4. `los_decay` RETIRES FROM THE LIVE PATH — MEASURED, NOT ASSERTED

`los_decay(p)` is called in exactly two places:

| site | what it is | on a printed price? |
|---|---|---|
| `rl_model.py:1748` | the LEGACY `rl_model.value()` chain | **NO** — the board's `ev()` never calls `value()` |
| `rl_export.py:332` | the `losd` field of the UI bundle | **NO** — a display field, not a price |

So it was not reachable from a printed price before this act and is not after it. It is **kept in code as
the declared fallback** — the existing convention for every superseded law in this engine
(`RL_PVC2`/`RL_EVW`/`RL_ISOFADE`/`RL_ENTRY29B` all keep their old leg) — behind this block's declared
kill-switch.

## 5. THE KILL-SWITCH

`RL_ONEMACH=0` makes the whole block inert. **Measured: board `84c9ea16f8ac5ac45e4e2359a718e7d2`
byte-exact** — the Step-1 board, i.e. the 29B flat hold restored exactly. Declared kill-switch, not a
manifest dial (`config_sha256` UNMOVED).

## 6. THE READING

| | |
|---|---|
| board | `84c9ea16f8ac5ac45e4e2359a718e7d2` → **`9298203135202a0c707bb0977ba38c31`** |
| total | 718,019 → **706,672** (−11,347, −1.58 %) |
| movers | **46 of 804 — every one `cg == 0`, every one ND in-curve.** Zero pool movers, zero rows with evidence. |
| printed-day-0 | **89 of 89, tolerance 0**, under the restated identity |

**THE THREE RULED NAMED ROWS REPRODUCE THE OWNER'S DISCLOSED NUMBERS EXACTLY:**

| row | entry | pos/pick | c | v0 (Step-1) | D(c) | old print | **new print** | ruling said |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `josh-smillie` | 2024 ND | MID 7 | 2.92 | 1688.81 | 0.2788 | 1689 | **471** | ~471 |
| `harry-demattia` | 2023 ND | MID 25 | 3.92 | 890.60 | 0.3384 | 891 | **301** | ~301 |
| `max-knobel` | 2022 ND | RUCK 42 | 4.92 | 830.54 | 0.3460 | 831 | **287** | ~287 |

`max-knobel` is the row the flat deep end decides: 287 on the ruled law, against 49 had the fitted decay
been extrapolated and 138 on the old constants. The owner's ruling is the reason he is 287.

Evidence: `MOVERS_S2.json`, `MOVERS_S2_out.txt`.

---

*Nothing was tuned after seeing the reading. The constants are the ruling's, copied at full precision from
`FADE30B_DRIFT.json`.*
