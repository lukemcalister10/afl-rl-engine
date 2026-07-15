# Form-conditioned aging — the one-page read (for the owner)

**Your question.** Gawn and Bontempelli haven't shown signs of dropping off — should we weigh that
demonstrated lack of decline against their age, which says they probably will? Put operationally: among
players 29–36 who are **flat-or-rising to date**, does decline actually arrive **slower** than for their age
group as a whole?

**The answer, plainly: no — being flat-or-rising to date buys essentially no slowdown.** In the committed
history, a player aged 30+ who has *not* declined yet still faces about a **coin-flip (≈50–54%)** chance of a
material drop in his demonstrated level the very next season, and a typical next-season change of **about −4
SuperCoach points**. The age cohort *as a whole* sits at almost exactly the same place (≈51%, −3 points). We
tried this eleven different ways — stricter and looser definitions of "not declining," of "a real drop," of
"a real season" — and in **every single one** the no-decline-yet group declined at least as fast as the
cohort, never slower. So the instinct "he hasn't dropped off, so he won't" is **not** supported by the data
at the group level: reversion dominates. Expected time to a first material drop for a flat-or-rising
30-year-old is only about **two seasons**, and only about **1 in 9** get through 30→33 without one.

**What this says about the engine.** The engine already prices a veteran's *remaining runway* (its age
multiplier eases them down ~0.73 at 30 toward ~0.55 at 37) and — the piece your question really targets — it
carries a 30+ player's recent *rise* forward at fraction **zero** (the "S_AGE 30+ zero"). This measurement,
now done **conditionally** for the first time, says that zero is **defensible even for the players who
haven't declined**: their rise does not persist as a class. The engine is **not** being unfair to
no-decline-yet veterans. **The numbers support leaving the 30+ age path as it is.**

**What this does NOT say — and where your instinct is right.** This is a statement about the **class
average, not about Gawn or Bontempelli individually.** All five names you'd point to are **right-censored**
— their 2026 season is only half-played, so the data cannot yet score their "next season." And two of them
are, *right now in their 2026 partials*, **beating the class expectation**: **Max Gawn** (~127, above his
demonstrated 126 and well above the class's −7) and **Isaac Heeney** (~124, above his demonstrated 109) are
persisting, not fading. **Bontempelli** (~119), **Tim English** (~99) and **Bailey Dale** (~99) are near or
a touch below expectation. A genuine persister tail **exists** — Gawn and Heeney are living in it — but you
cannot read any single man's future off the class curve, and the class curve is not why the engine values
these players: they get paid by **demonstrated production** as they keep producing, not by an age-based
forward bet.

**The decision the numbers support:** keep the 30+ forward-carry zero and the current age decline path — the
no-decline-yet cohort does not decline slower, so nothing here argues the engine is too harsh on veterans.

**The decision the numbers do NOT support:** (1) a blanket "flat-or-rising veterans are safe / decline
later" — no slowdown appears anywhere; (2) any individual verdict on Gawn/Bont/Heeney from this — they are
censored and currently outrunning the class; (3) a precise 33–36 age curve — that slice is thin (n≈12,
pooled). **No wiring is recommended; this is measurement only — the call is yours.**

*Basis: 2652-record committed store at base 9be07b8e (store b1fd0bce). Demonstrated level = the engine's own
recency-weighted level (validated against Heeney 109.5). Decline = a season-on-season drop beyond the
engine's own 3-point noise band. Both survivorship bounds (faders-who-left counted, and not) reported; the
truth sits between and the story holds either way. Full numbers in FINDING.md and the committed CSVs.*
