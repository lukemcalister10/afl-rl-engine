# D2 RE-CUT — What is an absence worth? (relative · smooth in age · vs what the engine already charges)

**Tier 3, READ-ONLY.** Board of record **`9f8ae76`** (v2.9 tag): store **`b0c39d78`** · board `81e48293` ·
engine `2030e5df` · config `69ead79b` · register `652d83e8`. Guard 5 PASS (store md5 asserted == `b0c39d78`).
Every figure below is on `b0c39d78`. Deep-copies / temporary function patches only — nothing written to
store/engine/board/gates/docs/pricing/λ/trust-basis. **No lever proposed. The owner rules.**

**What carries forward (verified, reproduced to the number):** the age-controlled diff-in-diff against
**14,698** continuous transitions is sound and reproduces exactly — overall **−3.42 SC [−4.84,−1.95]**,
young 18–24 −4.94, prime 25–28 −1.07 (CI spans 0), 109 established-base absence players, 0 explicit
`games==0` rows (absence = a year-gap). The construction stands. R1/R2/R3 re-cut it; R4/R5 answer the
lever question the prior D2 never asked.

---

## R1 — ADDITIVE or MULTIPLICATIVE? (form of the effect vs pre-absence level)

Regress the per-event effect (`Δavg − age-expected Δavg`) on the pre-absence level.

| form | test | slope | 95% CI | flat? |
|---|---|---|---|---|
| additive | effect(**points**) ~ level | **−0.274 /SC** | [−0.356,−0.187] | **NO** |
| multiplicative | effect(**percent**) ~ level | **−0.329 %pt/SC** | [−0.443,−0.219] | **NO** |

Both look non-flat — but **the raw slope is mean-reversion, not absence.** The continuous control group
(no absence) shows the **identical** level-slope of Δavg: **−0.272 /SC [−0.284,−0.260]**. Netting it:

- **Absence-specific level slope = returner − control = −0.060 /SC, 95% CI [−0.146, +0.030] — spans zero.**
- Additive predicts slope **0** (dist 0.060, INSIDE CI). Multiplicative predicts slope = mean/level =
  −4.76/75 = **−0.063** (dist **0.003**, INSIDE CI). **The point estimate sits essentially ON the
  multiplicative prediction; both forms are inside the CI — the data cannot statistically separate them.**

**STATE WHICH:** once mean-reversion is removed the effect is **flat in neither by a wide margin, but the
point estimate is multiplicative, not additive** (−0.060 ≈ the −0.063 a percent-charge predicts, vs 0 for a
flat-points charge). Combined with the value-side reason the directive names — `ev(level)` is convex at the
replacement bar, so a flat point haircut craters low-average players' SCAR through the floor — **the data
supports a MULTIPLICATIVE (percent-of-level) form over additive.** A flat point penalty is the worst spec.
(Also confirmed: relative AMPLIFIES the age gradient — young −5.6% vs prime −0.5% in percent, vs −4.94/−1.07
in points; and the mean-reversion-adjusted effect is *larger*: overall −4.76, young −6.0, prime −2.4,
older −5.6 — see R2.)

## R2 — THE SMOOTH AGE CURVE (CORE rule 7; no bins) — **it IS a U, and the 3-bin cut destroyed it**

Gaussian local-linear kernel smoother (bandwidth 2.5 yr, declared) of the effect on age, 18→34, bootstrap
95% ribbon. **Figure: `fig_r2_agecurve.svg`.** Mean-reversion-adjusted curve (primary):

| age | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| effect | −2.5 | −4.5 | −5.6 | **−5.7** | −5.3 | −4.5 | −3.7 | −3.3 | −3.3 | −3.9 | −5.1 | −7.1 |

**Shape:** a **developmental trough at age 22–23 (≈ −5.7)** → shallow **prime plateau at 27–28 (least
penalty, ≈ −3.3)** → **steep aging decline into the 30s** (−5 at 30, −7 at 31, and −9…−12 at 32–34). It is a
U (asymmetric). **The three-bin cut hid all of it:** "18–24 = −4.94" lumped a **data-free 18–19** (raw n≈0 —
kernel extrapolation, DECLARED unsupported, shaded on the figure) with the 22–24 trough; "prime 25–28 =
−1.07, pure availability" is really "27–28 is *least* penalised," and even there the adjusted penalty is
−3.3 (CI excludes 0) — **prime is NOT inert**; "29+ = −3.32" hid a −4→−12 age ramp. **Owner was right: age
18 ≠ age 24.** Thin slices pooled + declared per rule 7: age <20 (no data) and 32–34 (raw n 1,1 — pooled
into the 30+ decline, ribbon huge).

## R3 — WHAT THE RECENCY DECAY ALREADY CHARGES — **it UNDER-charges, worst for the young; wrong shape**

The engine has no absence lever, but a year-gap ages a player's demonstrated seasons via `ld^(Y−yr)`
(ld = 0.40 KEY / 0.35 GEN / 0.225 MR — steep). Isolating that charge (remove the gap → contiguous record →
re-price) across all 109 gap players, evaluated at the return year, vs the R2 truth:

| age band | recency charge | truth [adj] | error | truth [age-only] | error |
|---|---|---|---|---|---|
| 18–22 (dev trough) | **−0.67** | −5.58 | **+4.91 UNDER** | −4.42 | +3.75 UNDER |
| 23–24 | −0.77 | −5.42 | +4.65 UNDER | −4.24 | +3.48 UNDER |
| 25–28 prime | −2.41 | −4.39 | +1.99 UNDER | −3.08 | +0.67 UNDER |
| 29+ older | −3.47 | −4.26 | +0.79 UNDER | −2.52 | −0.95 OVER |

**The engine UNDER-charges absence at almost every age** (docks only −1.7 level pts vs −3.6…−4.9 owed), and
**the shortfall is age-shaped: worst for the young** (charges −0.67 where ≈ −5 is owed) and closes with age
— **error-vs-age slope −0.472 /yr, 95% CI [−0.780,−0.153]** (clear of 0). **The charge shape is INVERTED
from the truth:** decay is smallest for the young (short records, fast decay) exactly where the true
developmental loss is largest. **The directive's specific guess — "over-charging prime" — is REFUTED:** prime
is under-charged too (by 0.7–2.0); only the oldest band under the age-only truth shows a whiff of over-charge
(−0.95). Because the decay is TRANSIENT (steep ld ⇒ the gap's cost decays away within ~2 seasons once a
player re-establishes — median board-year charge −0.15), it also cannot express the young's PERSISTENT
developmental loss. **SCAR note:** the charge is convex-skewed — near zero for most, but **Jamarra −315 SCAR**
(197 → 512 if the gap's extra decay is removed): the convex floor amplifies exactly the near-replacement case.

## R4 — THE FOUR PHANTOM BOARDS (owner-proposed; TEST, do not wire) — **1 game is too light to matter**

One phantom `games=1` row per missed season; re-price the affected board. Weight of a 1-game row =
ld¹ ≈ 0.40 (KEY) against ~18 for a real season.

| phantom avg | movers (≥1 SCAR) | ΣΔ board | Jamarra | young cohort Σ |
|---|---|---|---|---|
| **1. avg = 0** | 15 | **−675** | 197→224 | −3.5% |
| **2. avg = REPL bar** | 12 | +23 | 197→226 | +0.1% |
| **3. avg = pre+effect (candidate)** | 11 | +17 | 197→216 | +0.1% |
| **4. avg = pre (null)** | 11 | +15 | 197→221 | +0.1% |

**Options 2, 3 and 4 are indistinguishable** (ΣΔ +15…+23, ~11 movers) — **at one game the phantom can't
express the −4.9 truth, and "data-implied" reads the same as "absence costs nothing."** Only avg=0 bites, and
it bites the wrong way (a zero is an outlier dragging through the convex floor). **The phantom IS surgical** —
the A-anchors (Bontempelli 3664, Gawn 2518, Daicos 8069, Sheezel 8204, H.Reid 3782) are inert; only
gap-players move. **The real knob is WEIGHT, not the average** — carrying the candidate avg at g games:
g=1 → ΣΔ +17 (Jamarra +19); **g=5 → −637 (+73); g=10 → −1133 (+138); g=18 → −1248 (+220)**. At weight the
candidate (option 3) and the null (option 4) finally diverge — the candidate charges the measured truth, the
null charges nothing. **Jamarra RISES under every option** (his lowness is the 3-game cameo, register item 6,
not the absence — a data-implied 2025 dilutes the cameo). **This is the owner's board to read:** at one game
his fourth option and the data-candidate agree that an absence is worth ≈ nothing; to make an absence worth
the measured −4.9 the phantom needs a season's WEIGHT.

## R5 — HISTORICAL vs FUTURE ABSENCES: TWO REGIMES (report, do not design)

**What the LTI register holds** (`LTI_REGISTER.md`, pinned R-REG=R2, md5 `652d83e8` asserted by Guard 5):
43 rows (32 Section-A + 11 Section-B), one per injury *window*, keyed by store ID (Max-King collision guard).
Columns key/section/window_id/**designation** (`2025` / `2026_preseason` / `2026`) / **status**
(`may_return_2026` / `out_until_2027` / `returned`). **It carries NO game counts and NO averages, by design**
("the store stays the single source of production").

**What reads it — and is it in the LEVEL?** The `RL_AVAIL` layer (default ON; `lti_register.py` →
`_merged_recover.py:1035`) reads it into the **VALUE / availability channel, NOT the demonstrated level.**
Concretely it sets: a **present-season lost-production haircut** `_avail_hc = L` (L=1 full-season,
L=1−g/G_FULL mid-season) applied to the forward production projection at k=0; a **return-season haircut**
`_lti_ret_hc` at the return year (Section-A only; **young/speculative `nqual<4` ship ZERO**; board-only, decays
next season); and a season-fraction override `_fEy`. The **one** place it touches the level is protective —
fork-v **nukes** the injured season out of the KPF top-2 selection so the level rests on healthy seasons.
**Plainly: the LTI layer docks forward value and shields the level from injury contamination; it puts NO
absence charge into `_lvlcurr`.** Historical mid-career gaps (the R1–R4 population) get **none** of this — they
flow only through the recency decay of R3. Empirically the two regimes are near-disjoint: **only 1 of the 109
historical-gap players (jamie-elliott) is also an LTI register name; Jamarra is not** (`_avail_hc=0` — his
2025 is charged by decay alone).

**What a cause-conditioned phantom average would need from it:** the register supplies **cause+timing forward
only** (injury window, designation, return status) — enough to place a phantom in the right season and stop at
return. It does **not** supply (a) a game count or average (deliberately excluded — a phantom avg would be a
NEW field), or (b) any cause for a HISTORICAL gap (the store can't say why 2025 is missing; the register is
forward-only and injury-only — suspension / non-selection are not distinguished). **An ACL is registered and
handled forward; a form-omission historical gap is invisible to cause.** A cause-conditioned phantom is
therefore a forward-only, register-scoped construct; historical phantoms cannot be cause-conditioned. **Scope
noted; nothing built.**

---

## In plain terms

An absence is worth **more the more you had to lose and the younger you are** — but not in the way the old
three-bin table said. Once you strip out ordinary bounce-back (good and bad years both drift toward average
whether or not you miss time), the true cost is a smooth **U in age**: it bites hardest on a 22–23-year-old
losing a developmental year, eases through the late-20s, and bites again as players age past 30. The engine
already charges *something* for a missed year — the recency decay quietly ages your last good season — but it
charges the **wrong shape**: almost nothing for the young (where the real loss is biggest) and it fades within
a season or two, when the young player's loss is permanent. The owner's phantom-game idea works, but **one
game is far too light to carry the message** — at one game "the data says it's worth −5 points" and "it's
worth nothing" price the same; the lever only comes alive with a full season's weight behind it, and when it
does, the honest average to give the phantom is the player's own level minus the measured penalty.
