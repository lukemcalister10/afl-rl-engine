# ORDER 33 — SEAT W3 PACKET: does time-in-system add growth signal at fixed age?

**Seat:** W3 (measurement only, read-only). **Date:** 2026-08-17. **Store:** `cb38ef11`,
2,650 players, 11,340 played season rows. **Prereg:** `PREREG_W3.md` (pushed before any
result). Seed 33, cluster bootstrap by player, B=1000. Full tables in
`MEASURE_W3_out.txt`, `SENS_W3_out.txt`, `ASYM_W3_out.txt`; table build in `w3_build.py`
(ORDER 32 S1 conventions reused).

## 1. VERDICT

**The hypothesis is not supported by the store's history — and pooled across ages it runs
the other way.** Your claim (2026-08-17): at the same age and same games/average, a
first-year player (Hall-Kahan, Murdock) has more improvement ahead than a four-year
veteran. Measured on every player-season 2005–2025 with an observable next season:

- **Pooled (ages 18–30):** first-or-second-season players improve **2.1 points LESS**
  next season than same-age, same-position, same-output veterans (95% CI −3.2 to −1.1).
  Robust to full-season-only samples, a games control, and a 3-year horizon.
- **In your key population (age 23+):** the effect is a **null with a negative lean**:
  −1.0 [−2.5, +0.4]. Prereg falsifier **F2 fires**: exposure adds nothing measurable at
  fixed age — and certainly not the positive premium the claim predicts.
- **The "19-year-old over Hall-Kahan, obviously" half is confirmed emphatically** — the
  longitudinal age curve is large (+8 points of expected next-season growth at 19 vs +2
  at 23, §3). Age really is the primary variable. The secondary variable you proposed
  does not show up with the sign you expect.
- One genuine exposure signal DOES exist, with the opposite meaning: at fixed age and
  output, **more career games predicts MORE subsequent improvement** (+2.0 points per 50
  career games, CI +1.5 to +2.6, and +2.0 at 23+ alone). Accumulated games are a quality
  /durability credential, not spent-upside. That is S3's selection channel, not a
  newcomer growth bonus (§8).

**Implication for the engine: the age-only keying of growth stands as measured.** Wiring
an exposure bonus for mature first-years would move values in the wrong direction.

## 2. SAMPLE

Season rows with games ≥ 6·u, ages 18–30, 2005–2025 (so Y+1 observable): **n = 7,823**
(1,516 players). With a real next season (games ≥ 6·u): **n = 6,373** (81.5%). No next
season at all: 7.9%; thin next season: 10.6% — both handled as outcomes (§6).
Exposure measures at end of season Y: **career games** (X1), **played-season index**
(X2; FIRST2 = first or second season), **listed tenure** (X3, from the entry-year field).
Key-cell inventory: age ≥ 23 in first/second season = 333 rows (243 players; RD 145,
ND 123, MSD 19, SSP 16, UNR 14, IRE 6, PDx 10) — thin but workable pooled; individual
age × band cells are NOT workable and are bounded honestly in §5.

## 3. THE LONGITUDINAL AGE CURVE (the adjustment reference — and your claim's first half)

Mean next-season change d1 = avg(Y+1) − avg(Y), conditional on a real next season:

| age | TALL | SMALL |
|---|---|---|
| 18–19 | +6.6 (n75) | +8.4 (n334) |
| 20 | +4.9 | +6.0 |
| 21 | +5.2 | +4.2 |
| 22 | +2.7 | +2.2 |
| 23 | +2.8 | +2.1 |
| 24 | +1.6 | −0.2 |
| 25 | +0.7 | −0.1 |
| 26 | −0.1 | −1.7 |
| 27+ | −1.9 | −2.7 |

Within-cell sd is 11–14 points everywhere: every effect in this packet is small against
individual-season noise. All later analysis is on **dA** = d1 minus this curve's cell
mean, so "improvement" always means *relative to age-peers of the same class*.

## 4. THE POOLED TEST (M1/M3): exposure at fixed age × position × output

dA regressed on exposure + age dummies + position + avg-vs-bar + output-band dummies;
cluster bootstrap by player. Your claim predicts negative career-games/season-index
coefficients and a positive FIRST2 coefficient. Measured:

| exposure variable | coefficient | 95% CI | claim predicts |
|---|---|---|---|
| career games / 50 | **+2.34** | +1.83, +2.85 * | negative |
| played-season index | **+0.44** | +0.23, +0.64 * | negative |
| FIRST2 (1st/2nd season) | **−2.14** | −3.17, −1.12 * | positive |
| listed tenure (X3) | +0.05 | −0.16, +0.26 | negative |

Shape (M3, season-index dummies vs 5+ baseline): season 1 **−3.8***, season 2 **−2.0***,
season 3 −0.2, season 4 −1.5*. The deficit is concentrated in the first two seasons —
the *adaptation* shape exists, but as a **debit**, not the credit your claim expects:
a player's first-two-season output, at fixed level, is the *least* likely to kick on.
Listed tenure (which counts rookie-list years without games) carries nothing; the
information is in games actually played.

## 5. THE KEY CELLS (age 23+), bounded honestly

Controlled regression on 23+ only: FIRST2 = **−1.01 [−2.50, +0.38]** (n=3,911; 238
first-year rows; identical at games ≥ 10u and with a games control). Season-index
dummies at 23+: −1.6, −1.3, −0.3, −2.0 — no positive anywhere. Per prereg **F1 fails,
F2 fires**; the age-band interaction (S-D) shows the pooled deficit is driven by ages
18–22 (−2.9*) with 23+ at −1.1 [−2.6, +0.4].

**The one number that superficially supports the claim, and why it doesn't:** the raw
pooled-23+ cell contrast is LOW-exposure +1.42 vs HIGH −0.21 dA (diff +1.62 [+0.11,
+3.17]). That contrast does not control current output: 46% of mature first-year rows
sit more than 10 points under the bar (vs 21% of veteran rows), and that band
mean-reverts upward for everyone (+6 to +7). Inside output bands the advantage
disappears or reverses (age-23 examples: TALL B1 −11.5 vs +0.6 favors veterans; SMALL B1
+3.9 vs −1.9 favors first-years, n=16; SMALL B3 −13.3 vs −3.1 favors veterans). Cell sds
are 8–18 points on n of 5–20: **no individual age × class × band cell at 23+ can
support a claim in either direction**, and four of them are formally UNSUPPORTED (n<5),
including the age-26+ above-bar first-year cells that Murdock and McAndrew actually
occupy. What the data CAN support is the pooled 23+ read: between −2.5 and +0.4 points,
centered at −1. Full cell grid (5 age bands × 2 classes × 4 bands × both groups, with
exits) in `MEASURE_W3_out.txt` §M2.

## 6. SURVIVORSHIP, HANDLED EXPLICITLY

- Raw, mature first-years exit faster (12.9% no-next-season vs 8.4% for 23+ veterans) —
  but that is again output composition. At fixed age × output the exit LPM on FIRST2 is
  **+0.3pp [−1.8, +2.4]: first-years do not exit faster than same-output veterans.**
- The unconditional reading (exit counts as failure): P(improve AND survive) is
  **−7.3pp [−10.8, −3.6]** for FIRST2 at fixed age/output. So the conditional deficit is
  not an artifact of who survives — the unconditional view is worse, not better (prereg
  F3 does not rescue the claim; it deepens the null).
- 3-year horizon (best of Y+1..Y+3): FIRST2 **−2.19 [−3.46, −0.91]** on age-adjusted
  change and −2.9pp on having any qualifying later season. The deficit is not a
  one-season blip that later catch-up repays.

## 7. MECHANISM — what the deficit is and is not (post-hoc probes, disclosed)

- **Not short-season measurement noise:** unchanged at games ≥ 10u only and with a
  current-games control (S-A, S-B).
- **Not pure track-record shrinkage:** shrinkage predicts first-years fall back above
  the bar but bounce equally below it; measured pooled it is symmetric (−2.1 below,
  −2.2 above). At 23+ there is a mild shrinkage-shaped asymmetry (−0.6 below, −1.8
  above) but CIs are wide (`ASYM_W3_out.txt`).
- **Selection is not removable:** who GETS a mature debut (and who accumulates 100 games
  by 26) is chosen by clubs, not randomized. The career-games credential (+2/50 games)
  in particular should be read as "clubs kept picking him" quality signal. No regression
  here can turn these into causal effects; they are the correct *actuarial* read for
  valuation, which prices players as selected, not counterfactually.

## 8. WIRING — AWAITING RULING (measurement seat proposes, does not change)

- **W3-P0 (recommended): change nothing.** The growth projection's age-only keying is
  consistent with measurement; the proposed exposure bonus has the wrong sign in the
  data. A null honored is cheaper than a channel wired backwards.
- **W3-P1 (only if the deficit is to be priced): a small early-career growth debit, not
  a credit** — growth(age) × (1 − h(season_index)) with h ≈ 0.15–0.25 of a sd-scaled
  ~2-point haircut in played seasons 1–2, 0 from season 3, capped so it never exceeds
  the measured CI. Direction is opposite to the owner's intuition and the 23+ CI
  includes zero — flagged accordingly.
- **No-double-counting boundary (binding on any ruling):** S3's channel pays career
  games as SELECTION at fixed output — bust-risk resolution, the odds you keep getting
  picked. This seat's career-games finding prices remaining GROWTH at fixed age — how
  the level itself moves next year. If S3's channel is wired, the +2.0/50-games growth
  credential here must NOT be wired as well without a joint fit: the two coefficients
  were measured separately on overlapping information and would double-pay the same
  games. Any W3-P1 haircut keyed on season index must likewise be netted against
  whatever S3 already charges first-year rows for unresolved bust risk.

## 9. NAMED ROWS (2026 in progress, u = 0.92; comparators by prereg rule)

| player | 2026 season | career G | season idx | comparator (same age/POS, ≥4 seasons) |
|---|---|---|---|---|
| milan-murdock (SSP, SF, 26) | 17g @ 70.1 | 17 | 1 | toby-bedford, 16g @ 70.5, 99 career G |
| hugo-hall-kahan (MSD, SD, 23) | 9g @ 73.0 | 9 | 1 | matthew-roberts, 17g @ 73.3, 65 career G |
| lachlan-mcandrew (SSP, RUCK, 26) | 20g @ 87.3 | 22 | 2 | bailey-williams-wc, 16g @ 90.4, 104 career G |

What the measurement says about each pair, at fixed age and output:

- **Murdock vs Bedford:** the claim would price Murdock's upside above Bedford's. The
  data gives no support — the pooled read docks first-years ~2 points, the 23+ read ~1
  (CI includes 0), and the career-games credential favors Bedford (+2/50 games ⇒ ~+3 on
  his 99 vs Murdock's 17). His exact cell (26+, SMALL, just-above-bar, first-year) is
  n=4 — UNSUPPORTED, so the honest statement is: *nothing measured here justifies
  projecting Murdock above Bedford; the point estimates run the other way.*
- **Hall-Kahan vs Roberts:** Hall-Kahan's exact cell (23, SMALL, just-under-bar,
  1st/2nd season) is the single owner-direction cell in the grid: +3.9 vs −1.9 (n=16 vs
  81, sd 15). It does not survive pooling and its neighbours reverse; on the supported
  23+ read the two project the same to within ±2.5, with Roberts holding the 65-game
  credential and the 17-vs-9-game season. Backing Hall-Kahan OVER Roberts is a
  taste call the data does not fund in either direction.
- **McAndrew vs Williams:** high-band short-career rows at 23+ fall back slightly MORE
  than veterans (B3 LOW dA −5.8 vs HIGH −4.0), and his 87.3 sits 12 above the RUCK bar
  in an age band where the curve is already flat-to-negative. The measurement warns
  against reading his 2026 as a launch pad rather than a peak; n is thin (15 pooled-23+
  first-year B3 rows) and is bounded as such.
- The age curve half of your sentence is the half that pays: the 19-year-old over
  Hall-Kahan is worth ~+6 points/year of expected growth. Hall-Kahan over a same-output
  26-year-old veteran is likewise mostly an AGE call (+2.1 vs −1.7 on the curve) — the
  engine already pays that, and needs no time-in-system term to do it.

## 10. HONESTY LEDGER

- **This is a null-plus-reversal result and is reported as such.** F1 failed; F2 fired
  on the key population; the pooled all-ages sign is significantly opposite the claim.
- All effects (±2 points) are an order of magnitude smaller than individual next-season
  sd (~12.6). This channel, whichever way it pointed, was never going to move one
  player's projection much; it matters only in aggregate.
- Thin cells are named UNSUPPORTED, never averaged into a story; the mature first-year
  population is 243 players total across 21 seasons — per-cell claims at 26+ are out of
  reach of this store, full stop.
- Post-hoc probes (games control, asymmetry, age-band interaction) are labeled as such;
  everything else was prereg'd first (`PREREG_W3.md`, pushed before the first run).
- Selection into mature debuts is not removable (§7); readings are actuarial, not causal.
- 2026 rows never enter the estimation sample; named-row readings are in-progress.
- Deterministic: seed 33, thread pins, store md5 `cb38ef11` printed in every output.
