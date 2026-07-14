# D2 RE-CUT — RETURN

- **branch** `claude/absence-value-forms-lpfm11` · **head** `<filled at commit>` · **PR** `<candidate, at return>`
- **board of record** `9f8ae76` (v2.9): store **`b0c39d78`** · board `81e48293` · engine `2030e5df`. Guard 5 PASS.
- Prior D2 reproduced to the number (−3.42 SC; 14,698 controls; 109 absence players). Tier 3, read-only. **No lever proposed.**

**R1 — additive or multiplicative?** Raw effect-vs-level slope −0.274 pts/SC — but that is **mean-reversion**: the
continuous control shows the identical −0.272/SC. Absence-specific slope = **−0.060/SC, 95%CI [−0.146,+0.030]**
(spans 0). Additive predicts 0 (dist .060); multiplicative predicts −0.063 (dist **.003**). Point estimate sits ON
the multiplicative line; both inside CI (undistinguished). **⇒ data favours MULTIPLICATIVE (percent-of-level) over
additive; a flat point haircut is the worst spec** (convex `ev` craters low-avg value). Relative amplifies (young −5.6%, prime −0.5%).

**R2 — the smooth age curve (no bins).** It IS a U: developmental trough **age 22–23 ≈ −5.7**, shallow prime
plateau **27–28 ≈ −3.3 (least, NOT zero)**, steep aging decline **−5(30) → −7(31) → −9…−12(32–34)**. The 3-bin cut
destroyed it — "18–24=−4.94" lumped data-free 18–19 (declared unsupported) with the trough; "prime pure
availability" is false (adj −3.3, CI clear of 0). Figure `fig_r2_agecurve.svg`; thin slices (<20, 32–34) pooled+declared.

**R3 — what the recency decay already charges.** It **UNDER-charges** almost everywhere: docks only −1.7 lvl-pts vs
−3.6…−4.9 owed, **worst for the young** (−0.67 charged where ≈−5 owed), error closing with age (slope −0.472/yr,
CI[−0.780,−0.153]). Charge shape is **INVERTED** from the truth and TRANSIENT (fades in ~2 seasons). The directive's
"over-charging prime" guess is **REFUTED** — prime under-charged too. SCAR convex-skewed: **Jamarra −315** (197→512).

**R4 — the four phantom boards (1 game each).** avg=0: 15 movers, ΣΔ **−675** (bites wrong). REPL / **candidate
(pre+effect)** / null (pre): **all indistinguishable**, ΣΔ +23/+17/+15, ~11 movers — **at one game "data-implied" =
"costs nothing."** Surgical: A-anchors inert. The knob is **WEIGHT**: candidate at g=1/5/10/18 → ΣΔ +17/−637/−1133/−1248.
**Jamarra rises under all four** (his problem is the cameo, item 6, not the absence). Owner's board to read.

**R5 — LTI register (two regimes).** Holds 43 injury *windows* (designation/status/section), keyed by ID, **no game
counts**. Read by `RL_AVAIL` into the **VALUE/availability channel, NOT the level**: present haircut `_avail_hc=L` +
return haircut (Section-A, young-exempt) + fork-v nuking the injured season out of KPF selection (protective). **No
absence charge enters `_lvlcurr`.** Forward+injury-only: historical gaps get none of it (only 1/109 overlap; Jamarra
`_avail_hc=0`). A cause-conditioned phantom avg would need a NEW field (avg) + a cause it only has going forward.

**In plain terms.** An absence costs the most to a 22–23-year-old and again to a player past 30, and least in the
prime — a smooth U, not three flat bands, once you subtract the ordinary drift-toward-average that happens to
everyone. The engine already charges for a missed year through recency decay, but in the wrong shape: almost nothing
for the young, where the loss is biggest, and it fades within a season. The owner's phantom-game fix works — but one
game is far too light to say anything; it only speaks with a season's weight behind it, and the honest average to
give it is the player's own level minus the measured penalty. Candidate PR only — no bake, no tag, no merge.
