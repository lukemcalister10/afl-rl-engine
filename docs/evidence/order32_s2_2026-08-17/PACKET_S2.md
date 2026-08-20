# PACKET S2 — ORDER 32: THE SITTER SPECTRUM SURFACE. FOR THE OWNER'S RULING.

**NOTHING WIRES.** This seat measured; it did not decide. Every credit, restoration, recency and
injury term below is a **WIRING PROPOSAL AWAITING RULING**. The candidate law as it stands — the
31-F fade row on `o31_cu`, with `o31_played_units` crediting a full season for any games > 0 —
remains exactly where ORDER 31-F left it.

**Read in this order:** this packet → `SPECTRUM_S2_out.txt` (every cell, every n, every dispersion)
→ `SPECTRUM_S2.json` (machine-readable) → `o32s2_spectrum.py` (the instrument) → `base_run/` (the
30A-2 instrument's own console and outputs from being run whole inside this act).

**Pre-registration:** `PREREG_S2.md`, committed at `772d4ab` **before** the harness existed in
runnable form. All 21 predictions scored in §8 — 14 held, 7 breached, every breach owned by number.
Determinism: two consecutive runs byte-identical (`SPECTRUM_S2.json` md5 `7443b25d`,
`SPECTRUM_S2_out.txt` md5 `dbcabb02`).

**No parallel methodology.** The committed 30A-2 instrument (`o30a2_recut.py`, md5 `fe6f436a`) was
exec'd **WHOLE** — the `o31_pool.py` / `o31f_rederive_fade.py` discipline — with one character-level
edit (its output directory re-pointed to `base_run/`), and its own population, listing basis (#338
minimum tenure, L-B outcome-blind floor), per-season decomposition and normaliser were harvested.
**Control S1: the rerun reproduces the committed 31-F fade row and every 31-F T4 cell to deviation
0.0 exactly.** Every number below is that instrument's estimator on new conditioning cells.

**Terms used throughout** (all carried from the ruled lineage):
- **depth N** — seasons since entry; seasons 1..N−1 are completed. **c** — the continuous clock,
  N + φ, φ = calendar_progress = 0.92. **c_u** — the *unplayed* clock the candidate fades on.
- **D** — remaining-career value ratio: `mean( (obs·share_from_N + tail) · DF(N−1) / v0 ) / RAW(1)`,
  the 30A-2 T4 estimand, L-B listed-conditional. RAW(1) = 0.995498 on the head-fixed surface.
  The pure-sitter row this act re-derived (= the wired 31-F row, control-exact):
  **D(2) 0.5583 · D(3) 0.2748 · D(4) 0.3973, flat from 4, log-linear between.**
- **full-cure level** — the pure row one season shallower: what a depth-N row would price at if its
  most recent season's sitting were fully cured. D above that level is more than a cure — it is
  production/selection value, and is flagged SATURATED, never inverted into a credit.
- **delivered season** — the engine's own bar: games ≥ 10 (× season fraction if in-progress) AND
  season avg ≥ the position's bar (`BARS`, the DV lane's own constants).
- **thin cell** — n < 10: published as a **BOUND**, never quoted as a law, never fed to a fit.

---

## 1. Q1 — THE CREDIT FUNCTION. What does playing g games cure?

Pattern cells: seasons 1..N−2 all gameless, then **g games in season N−1** — the pure "sat, then
played g" spectrum the owner asked for. Full dispersion per cell in the transcript; D and n here.

| depth (sat, then g) | g=0 | g=1 | g=2 | g=3-5 | g=6-10 | g=11+ |
|---|---|---|---|---|---|---|
| **2** (fresh, debut season g) — D | 0.5583 | 0.8771 | **1.1320** † | 0.8152 | **1.4232** † | **1.6350** † |
| n | 464 | 63 | 70 | 145 | 161 | 239 |
| **3** (sat 1yr, then g) — D | 0.2748 | **1.5849** † | 0.6771 | **1.3501** † | 0.7832 | **1.2932** † |
| n | 100 | 31 | 13 | 33 | 31 | 44 |
| **4** (sat 2yr, then g) — D | 0.3973 | — (n=0) | *0.3419* (n=5) | *0.5710* (n=6) | *0.2373* (n=7) | **1.3469** † (n=12) |
| n | 11 | 0 | 5 | 6 | 7 | 12 |

† = SATURATED: D at or above the full-cure level (above the pure row one season shallower).
*Italics* = thin, bound only. Standard errors of D are large in the played cells (0.13–0.56) and are
printed per cell in the transcript — this surface is **noisy**, and the packet says so before fitting
anything through it.

**The per-game spectrum at depth 2** (the owner's "0 to 1 isn't that different from 1 to 2"):

| g | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| D | 0.5583 | 0.8771 | 1.1320 | 0.7349 | 0.7753 | 0.9643 |
| n | 464 | 63 | 70 | 58 | 44 | 43 |
| step | — | **+0.319** | +0.255 | −0.397 | +0.040 | +0.189 |

The owner is **half right**: the 0→1 and 1→2 steps are comparable (+0.319 vs +0.255 — prereg S3
breached in the owner's direction and owned). But the sequence then *falls* at g=3 — the per-game
resolution is noise-limited beyond g≈2, and no smooth per-game story survives.

**The fitted credit family** (prereg-fixed): `u(g) = min(1, g/G*)` — the fraction of the season's
sitting accrual cured by g games. Fit on the non-thin, non-saturated cells, n-weighted, in D-space:

- **G\* = 1.5** — RMS 0.0919 (headline), **0.1653 over the g>0 cells alone** (the honest number:
  the two big g=0 anchors flatter the headline; disclosed in the transcript with per-cell residuals).
- **Identifiability profile** (RMS by G\*): 1 → 0.0969 · **1.5 → 0.0919** · 2 → 0.0976 · 3 → 0.1093 ·
  5 → 0.0964 · 8 → 0.1029 · 12 → 0.1284 · 16 → 0.1416. **G\* is weakly identified: anything in
  [1, 8] fits within ~0.011 RMS of the optimum; G\* ≥ 12 is clearly worse.**
- Prereg S6 predicted G\* ∈ [5,12] off the backbone's 6–10 hint, and its own falsifier band [3,16]
  **fired** (G\* = 1.5). Owned in §8. What the measurement actually says: **the 6–10 signature in the
  cumulative backbone is where D crosses pedigree parity (D=1), not where the cure saturates. The
  cure itself is front-loaded and saturates within a handful of games.**

**What is safe to say, and what is not.**
1. **Zero is different from any.** The g=0 cell sits far below every played cell at every depth, on
   ns of hundreds. The fade's 0-games row is solid.
2. **The first game does NOT cure a full season.** u(1) ≈ 0.67 under the fitted family (inversion of
   the depth-2 g=1 cell alone gives û(1) = 0.78 with a 1-SE band [0.26, 1.00]). The wired law's 1.00
   at g=1 is above the point estimate under every reading, **but the band reaches 1.00** — the
   measurement bounds the wired credit as *probably* too generous at g=1, it does not disprove it.
3. **By ~2 games the season is effectively cured** in remaining-value terms, and beyond that the
   played cells price *above* full cure (selection: a club that keeps giving games is telling you
   something). A credit function cannot and should not chase that — it caps at u=1 by construction.
4. The depth-3 g=1 cell (D=1.58, n=31, se 0.56) is the loudest survivorship artifact in the surface
   and is flagged SATURATED, not fed to the fit.

> **WIRING PROPOSAL P1 (awaiting ruling):** replace `o31_played_units`' any-games full credit with
> per-season credit `f_k · min(1, g_k / G*)`, **G\* ruled from [1.5, 8]** (measured optimum 1.5;
> the choice inside that band is an owner call the data cannot make). Any G\* in the band kills the
> one-game full-cure cliff while preserving day-0 prices exactly (u(0)=0).

---

## 2. THE TWO-WAY SURFACE — sitting depth × playing evidence

s = gameless seasons among 1..N−1; columns = total career games at observation. The owner's object,
published whole; Q1 and Q3 are cuts of it. (Depth 2 omitted here — it is the per-game table above.)

**Depth 3** (n listed 800):

| s \ games | 0 | 1-2 | 3-5 | 6-10 | 11-20 | 21+ |
|---|---|---|---|---|---|---|
| 0 | — | *0.0000* (n=1) | 0.8675 (22) | 0.6939 (64) | 0.9987 (138) | 1.7747 (282) |
| 1 | — | 0.9756 (63) | 1.0412 (48) | 0.7371 (33) | 1.1267 (43) | *1.4945* (6) |
| 2 | **0.2748** (100) | | | | | |

**Depth 4** (n listed 542):

| s \ games | 0 | 1-2 | 3-5 | 6-10 | 11-20 | 21+ |
|---|---|---|---|---|---|---|
| 0 | — | — | — | *0.3715* (11, CENSOR-3) | 0.5267 (36) | 1.7988 (333) |
| 1 | — | *0.7166* (2) | *5.3600* (6) | 1.4527 (22, CENSOR-3) | 0.9260 (30) | 1.5570 (49) |
| 2 | — | 0.9787 (10) | 1.1037 (11) | *0.2076* (8) | *1.2257* (9) | *1.2829* (4) |
| 3 | **0.3973** (11) | | | | | |

*Italics* thin (bound); CENSOR-3 = mean tail share > 0.375 (30A's unusability flag). The games axis
is **not** monotone inside any s row at depth 3–4 (prereg S20 held — violations at `3|s0|6-10`,
`3|s1|6-10`, `4|s1|11-20`); the s axis at fixed games IS consistently ordered where quotable
(more sitting, less value — e.g. depth-3 games 6-10: s=0 0.694 vs s=1 0.737 is flat, but the g=0
columns sit far below everything). The surface supports a **fade on unplayed time + a front-loaded
credit**, not a smooth two-dimensional law.

---

## 3. Q2 — RESTORATION. Does a delivered season end the fade?

R(k) = D(from k+1 on) of **previously-sat rows that then DELIVERED season k**, divided by the same
object for **never-sat rows that delivered season k**. R = 1 means full restoration of pedigree
persistence; R at the fade level (~0.4–0.6) means the fade is sticky.

| k (delivered season) | n sat / ctrl | D sat | D ctrl | **R(k)** |
|---|---|---|---|---|
| 2 | *6* / 114 | 1.5233 | 2.5438 | *0.599 — BOUND (thin)* |
| 3 | 19 / 144 | 1.7198 | 2.5794 | 0.667 |
| 4 | 22 / 129 | 3.3146 | 2.8616 | 1.158 |
| 5 | 30 / 107 | 3.8312 | 2.8971 | 1.322 |
| **POOLED k=2..5** | **77 (51 players) / 494 (237)** | 2.9828 | 2.7137 | **1.099** |

Under the weaker "substantial" bar (g ≥ 10, no avg test): pooled R = **0.979** on n = 248/1007 —
the same answer on three times the sample. Split by prior sitting: 1 prior sat year R = 1.124
(n=66); 2+ prior sat years R = *0.952 on n=11 — bound* (prereg S12 breached by one row: n=11 not
<10; treated as thin anyway, owned in §8).

**Reading, honestly.** Pooled restoration is **complete** — a previously-sat player who genuinely
delivers a season carries the same forward value as a never-sat player who delivered at the same
tenure (R ≈ 1.0 under both bars). The k-gradient (0.6–0.67 early, >1 late) says early-tenure
restoration may be partial and late-tenure cells carry survivorship; the pooled number breached my
own [0.75, 1.05] band at 1.099 (S10, owned) — but on the substantial bar, and on every reading, the
falsifier bands (<0.55 sticky, >1.15 artifact) **did not fire**. Named confirmation: this is exactly
the phoenix-gothard shape (sat 2024+2025, then 15 games at 68.8 — DELIVERED under the SF bar 67.9).

> **WIRING PROPOSAL P2 (awaiting ruling):** a DELIVERED season (the engine's own bar, the
> `o31_stall_run` predicate) **resets accrued c_u to 0** — the fade does not follow a player through
> genuine delivery. Measured basis: pooled R ≈ 1.0 both bars. The measurement does NOT support a
> reset for merely-played seasons (billy-wilson's 13 games at 73.5 misses the SD bar 75.3 — under P2
> his history keeps its games-proportional credit but is not wiped).

---

## 4. Q3 — ORDER/RECENCY. Does WHEN you sat matter?

At fixed total sitting s, split by whether the **most recent completed season** was gameless
("sitting now") or played ("playing now"):

| cell | n | D | median | games med (IQR) |
|---|---|---|---|---|
| depth 3, s=1, **playing now** (0,g) | 152 | **1.2083** | 0.2649 | 5 (2–12) |
| depth 3, s=1, **sitting now** (g,0) | 41 | **0.2320** | 0.0110 | 3 (2–5) |
| depth 4, s=1, playing now | 98 | 1.6707 | 0.5904 | 20 (10–28) |
| depth 4, s=1, sitting now | 11 | 0.5364 | 0.2108 | 11 (8–19) |
| depth 4, s=2, playing now | 30 | 0.7653 | 0.2364 | 9 (5–14) |
| depth 4, s=2, sitting now | 12 | 1.3993 (se **0.80**, median 0.08) | — | 4 (2–4) |

The owner's exact patterns at depth 4 (P = played, 0 = gameless, seasons 1/2/3):

| pattern | n | D | median |
|---|---|---|---|
| **P-0-0** (played, then sat two years) | *6* | ***0.0101*** | 0.0000 |
| 0-P-0 | *6* | *2.7885* | 1.0229 |
| **0-0-P** (sat two years, playing now) | 30 | **0.7653** | 0.2364 |

**The recency effect is the largest single contrast in this act** (prereg S13 held): at identical
total sitting, the row sitting *now* prices at 0.23 against 1.21 for the row playing *now* — a gap
of **0.98 in D**, far beyond anything the order-blind accrual clock can express. The owner's P-0-0
vs 0-0-P instinct is confirmed **directionally in the strongest terms** — played-then-went-dark is
near-worthless (D = 0.01, median exactly 0) while sat-then-emerged is alive at 0.77 — but the
P-0-0 cell is **six rows** and is published as a BOUND (prereg S14 breached on the 0-0-P side:
n=30, not thin — the asymmetry itself is the finding). Confound disclosed: the sitting-now cells
also carry fewer career games (med 3 vs 5 at depth 3), so part of the gap is the credit function,
not pure order — the two mechanisms cannot be fully separated at these n.

The depth-4 s=2 inversion (sitting-now mean 1.40 > playing-now 0.77) is a 12-row cell with se 0.80
and median 0.08 — one right-tail row drives it; reported, not smoothed, not believed.

> **WIRING PROPOSAL P3 (awaiting ruling):** recency matters and the current law under-expresses it.
> The mechanically smallest change consistent with this measurement: P1's credit **plus** P2's
> delivered-reset already produce most of the observed asymmetry (a currently-sitting row keeps
> accruing c_u while a currently-playing row earns credit each season). The seat recommends ruling
> P1+P2 first and re-measuring the residual order effect before wiring any explicit recency weight —
> the exact-pattern cells that would calibrate one are n=6.

---

## 5. Q4 — THE INJURY SPLIT. What can and cannot be known.

**Ground truth:** `LTI_REGISTER.md` (R-REG, pinned, owner-maintained; md5 `652d83e8`; 45 windows,
43 players). Its own timing semantics: designation `2025` = injured in his last 2025 *game* (he
played 2025), zero 2026 games so far; `2026_preseason` = full 2026 absence; `2026` = played 2026
then injured (truncated, not gameless). **No historical injury source exists anywhere in this repo**
— the store carries no injury field (verified by scan).

- **(a) The historical null, counted:** of **7,212** fitted-window sit-seasons (2004–2021 entrants,
  seasons ≤ 2025), the register resolves **0 = 0.00%**. **The injured-vs-unselected fade split is
  UNMEASURABLE on the fitted population. Every fade cell in the lineage POOLS the two causes.**
  This null is a result (prereg S15 held), and it is the honest answer to "measure the fade
  separately per cause": on this repo's data, no seat can — until a historical availability table
  exists.
- **(c) The live census (where the register IS ground truth):** 87 ND-entrant rows are gameless in
  2026 (an accruing sit season on the candidate clock). Register-marked **injured: 15 = 17.2%**;
  healthy-unselected: 72 = 82.8%. Injured keys listed in the transcript (jack-payne, toby-conway,
  reef-mcinnes, joshua-kelly, …). **None of the 8 named rows is in the register** — every named
  sitter is sitting healthy-unselected, on the owner's own curated record.
- **The mixture bound (illustrative, assumption-carrying — w borrowed from the live 17.2%):** if an
  injured year costs nothing (D_inj = 1.0), the true healthy-unselected depth-2 fade implied by the
  pooled 0.5583 is **0.4663**; if injury carries no distinct signal, 0.5583 stands. The pooled row
  is therefore at most ~0.09 too generous for a healthy-unselected sitter at that weight — the
  direction the owner suspects, bounded, not resolved.
- **The proxy, labelled as a proxy:** the register's own exemplar ("established → zero games" is the
  injury shape) makes Q3's played-then-sat cell the nearest observable cousin of injury sitting —
  and that cell prices at **0.01 (n=6, bound)**. Read carefully, this *cuts against* assuming
  injured sitting is harmless in history: historically, established-then-dark rows mostly never came
  back. It is a proxy on six rows, not a cause measurement, and the seat draws no law from it.

> **WIRING PROPOSAL P4 (awaiting ruling — a POLICY choice, not a measured one):** if the owner wants
> injured sit-seasons to accrue c_u at a reduced rate (e.g. the register's Section-A windows accrue
> at 0 while `status ≠ returned`), that is wireable **prospectively** off R-REG for 2025+ seasons
> only — the register cannot reach history, and the measurement can neither support nor refute the
> discount level. The seat's only evidence-based note is the proxy above, which warns against
> assuming injury sitting is costless.

---

## 6. NAMED ROWS THROUGH THE SURFACE — arithmetic on a packet, nothing wired

c = (2026−entry) + 0.92. WIRED = full-unit credit for any games (the defect). PROPOSED = P1 credit
at the measured G\* = 1.5 (illustrative point; the ruled G\* moves these smoothly). D on the 31-F
row. v0: 29B printed where it exists, else the landed positional entry-law cell (marked ^).

| player | pos | pick | entry | c | games | c_u wired | c_u prop | D wired | D prop | v0 | px wired | px prop |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| josh-smillie | MID | 7 | 2024 | 2.92 | none | 2.92 | 2.92 | 0.2908 | 0.2908 | 1617 | 470 | 470 |
| lachlan-carmichael | SD | 21 | 2025 | 1.92 | none | 1.92 | 1.92 | 0.5849 | 0.5849 | 761 | 445 | 445 |
| phoenix-gothard | SF | 12 | 2023 | 3.92 | 2026:15 | 3.00 | 3.00 | 0.2748 | 0.2748 | 976^ | 268 | 268 |
| billy-wilson | SD | 34 | 2023 | 3.92 | 2025:4, 2026:13 | 2.00 | 2.00 | 0.5583 | 0.5583 | 358^ | 200 | 200 |
| will-green | RUCK | 16 | 2023 | 3.92 | 2026:1 | 3.00 | 3.31 | 0.2748 | 0.3077 | 1076^ | 296 | 331 |
| william-mccabe | KPD | 19 | 2023 | 3.92 | 2026:4 | 3.00 | 3.00 | 0.2748 | 0.2748 | 647^ | 178 | 178 |
| charlie-edwards | MID | 21 | 2023 | 3.92 | 2026:2 | 3.00 | 3.00 | 0.2748 | 0.2748 | 923^ | 254 | 254 |
| alex-dodson | RUCK | 53 | 2024 | 2.92 | 2025:1 | 1.92 | 2.25 | 0.5849 | 0.4665 | 237^ | 139 | 111 |

**The cliff counterfactual** (the owner-caught defect, quantified): if a currently-gameless row
plays ONE game —

| player | D now | WIRED after 1 game | PROPOSED after 1 game |
|---|---|---|---|
| lachlan-carmichael | 0.5849 → 445 | **1.0000 (+71%) → 761** | 0.8363 (+43%) → 636 |
| josh-smillie | 0.2908 → 470 | **0.5583 (+92%) → 903** | 0.4492 (+54%) → 726 |

The wired law flips the whole in-progress fraction on one game; P1 grades it. Note **will-green**:
his single 2026 game moves his *proposed* price UP versus wired (296 → 331) — his deeper proposed
c_u (3.31) lands on the ruled depth-4 > depth-3 selection kink, which this act inherits unsmoothed
per the standing ruling. **alex-dodson** is the clean two-sided case: one game in 2025 bought a full
season's cure under the wired law (D 0.5849); under P1 it buys 0.67 of one (D 0.4665).

**Delivery check** (Q2 bar, in-progress threshold g ≥ 9.2): phoenix-gothard 15 g @ 68.8 vs SF bar
67.9 → **DELIVERED** (under P2 his c_u would reset to 0 and D → 1.0 — the restoration measurement
is what would license that). billy-wilson 13 g @ 73.5 vs SD bar 75.3 → **NOT delivered** (prereg
S18's Wilson clause said the packet would report it if the bar said otherwise: it does — he keeps
his games credit but no reset). will-green (76.0 avg on 1 game), mccabe, edwards: not delivered.

---

## 7. WHAT THE SEAT RECOMMENDS THE OWNER RULE ON

| # | proposal | measured basis | the seat's honesty note |
|---|---|---|---|
| P1 | per-season credit `f_k·min(1, g_k/G*)`, G\* ruled from **[1.5, 8]** | Q1: u(1)≈0.67–0.78, cure front-loaded, saturates within a few games | G\* weakly identified inside the band; the 1-SE band on û(1) touches 1.0; ANY choice in-band retires the cliff |
| P2 | a DELIVERED season resets c_u to 0 | Q2: pooled R = 1.099 (bar) / 0.979 (g≥10), no falsifier fired | early-tenure R is 0.6–0.67 on thin/moderate cells; late-tenure carries survivorship |
| P3 | no explicit recency weight YET; re-measure after P1+P2 | Q3: sitting-now 0.23 vs playing-now 1.21; P-0-0 at 0.01 | the exact-pattern calibration cells are n=6; P1+P2 already express most of the asymmetry |
| P4 | injured sit-seasons accrue at a ruled reduced rate, prospectively off R-REG | Q4: UNMEASURABLE historically (0 of 7,212); live injured share 17.2% | pure policy; the only evidence (a 6-row proxy) warns injury-sitting is not costless |

## 8. THE PREREG, SCORED — 14 HELD, 7 BREACHED, none dropped

| # | verdict | detail |
|---|---|---|
| S1 | **HELD** | rerun reproduces the 31-F fade row and T4 cells to deviation 0.0 |
| S2 | **HELD** | D(1)−D(0) = +0.319; D(1) = 0.877 ∈ [0.75, 1.05] |
| S3 | **BREACHED** | 1→2 step (+0.255) is comparable to 0→1 (+0.319), and g=3 falls −0.397 — **the owner's "0→1 isn't that different from 1→2" is supported**; my prediction of a dominant first game was wrong |
| S4 | **HELD** | n(g=1)=63, n(g=2)=70 |
| S5 | **HELD** | D(3, 6-10) = 0.783 ≥ 0.55 |
| S6 | **BREACHED — falsifier fired** | G\* = 1.5, outside [3,16]: the backbone's 6–10 hint is pedigree-parity crossing, not cure length; the family is kept with G\* presented as the [1.5, 8] identifiability band |
| S7 | **HELD** | both deep cells saturate at full cure (u = 1) |
| S8 | **BREACHED** | û(1) = 0.775, above my [0.10, 0.50] — the wired credit overstates less than I predicted; the 1-SE band [0.26, 1.00] even reaches the wired value |
| S9 | **HELD** | primary RMS 0.092 ≤ 0.12 (with the g>0-only RMS 0.165 disclosed beside it) |
| S10 | **BREACHED** | pooled R = 1.099, above [0.75, 1.05]; neither falsifier fired; substantial-bar R = 0.979 |
| S11 | **HELD** | pooled sat-delivered n = 77 |
| S12 | **BREACHED** | the 2+-prior-sat cell is n=11, one row over my <10 prediction; treated as thin regardless |
| S13 | **HELD** | sitting-now 0.2320 vs playing-now 1.2083, gap +0.976 ≥ 0.10 |
| S14 | **BREACHED** | P-0-0 is thin (n=6) but 0-0-P is n=30 — the *asymmetry* of the two populations is itself a finding I failed to predict |
| S15 | **HELD** | historical register resolution 0 of 7,212 = 0.00% |
| S16 | **HELD** | 0 named rows in the register |
| S17 | **HELD** | live injured share 17.2% ∈ [5%, 25%] |
| S18 | **HELD, one clause reported** | carmichael/gothard as predicted; billy-wilson NOT delivered (73.5 < SD bar 75.3) — the prereg's own report-clause covers it |
| S19 | **BREACHED** | the depth-4 g=0 cell has p25 = 0.027 (n=11, only 2 zeros) — the zero-spike thins at depth 4 in the listed population |
| S20 | **HELD** | the deep surface is not monotone on the games axis (3 violations listed) |
| S21 | **HELD** | writes only into this directory; two runs byte-identical |

**Scorer correction, disclosed:** the first executed run (console md5 `4c4664ba`) carried a
sign-inverted mechanical check for S13 — it printed BREACHED while the prereg's own words
(sitting-now BELOW playing-now by ≥ 0.10) plainly held on the same numbers. The scorer was corrected
(no estimator, cell or prediction text changed) and the act re-run; the committed outputs are the
corrected, deterministic pair. Both consoles' md5s are in the git history of this directory.

## 9. WHAT WOULD CHANGE THIS PACKET

- **A historical availability/injury table.** It would convert Q4 from a null into a measurement and
  would let Q1's credit be fitted per cause. The single biggest data improvement available.
- **A ruled G\*.** The identifiability band [1.5, 8] is a measurement fact; the point inside it is a
  ruling. The named-row prices under any candidate G\* are one line of arithmetic on this packet.
- **More seasons.** The exact-pattern recency cells (P-0-0) and the 2+-sat restoration cell are 6
  and 11 rows; they grow by one cohort per year and by nothing else.

---

*ORDER 32, seat S2. `land/order-29`. READ-ONLY: no engine file, no board, no store, no curve was
touched. **NOTHING WIRES UNTIL THE OWNER RULES.***
