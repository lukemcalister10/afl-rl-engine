# MEMO — LEG B FUNCTIONAL FORM · v1.0 · 2026-07-16 · seat 9 (Fable) · EXTRA
### The design decisions, made BEFORE any build (spec §3 Leg B; R104.10's pre-sim obligation
### discharged in §6). Consumed: the Leg-A landed state (engine a83c9f6d · board 8d90c9ac · store
### b1fd0bce · config c2d233aec104) · the GPT audit clusters (ii)/(iii) (item 199) · rev144 §3's
### decision list. Every number in §6 is a supervisor re-run in a bootstrapped sandbox off the
### frozen July-8 construction (`ship_gates_check._b1_july8`, re-implemented verbatim and verified
### against the committed gate snapshot); candidate-map numbers are DECLARED FINDINGS (S4) — the
### frozen suite measures the real candidate. Pre-view hash discipline (audit #45): this memo and
### acceptance v1.17 are hashed at the directive; any post-view mutation HALTS the ladder.

## §1 — THE DEFECT (restated in one breath)
The output→price map is concave at the top: proven-27+ elasticity β = 0.683, β = 0.364 at the peak —
elite output ratios do not carry into price ratios (English/Briggs was 1.56× pre-Leg-A against an
output relationship the owner reads as ≥ 1.75×). The same compression runs down the age bands: the
≤22 slope is 0.111 (the Reid constraint — it must RISE).

## §2 — DECISION (a): THE FUNCTIONAL FAMILY — the OUTPUT-ANCHORED EVIDENCE BLEND
For a player-year with demonstrated above-replacement level ρ (his level ÷ the positional reference
level, BOTH from the engine's smoothed level machinery — §2.1) and evidence weight E (the v2.10
`_ev_qual` family, τ = 1.1 — the SAME family Leg A's fade rides):

**v′ = v^(1−w) · (V_ref · ρ^κ)^w,  w = s·E**, with s the ONE strength dial and κ = 1 (the β-target
exponent; κ stays 1 — the dial is s). In log-space this is a straight blend of the current price
toward the output-proportional price. Achieved top elasticity is exactly **β_eff = (1−w)·β_c + w**,
so with β_c = 0.683 measured, **β ≥ 0.85 requires saturated w ≥ 0.527 ⇒ s ≥ ~0.53** (the build
measures with the frozen estimator; this algebra is the design target, not the verdict).

REJECTED, with the pre-sim evidence (§6 table B):
- **Price-exponent stretch** (power-law on v, two-sided around a pivot): the top tail is unbounded —
  unconserved it explodes G-COHORT (y5 1.32 → 1.71 at the mildest setting); conserved per-cell it is
  ratio-neutral and traps the denominator; conserved per-position the elite tail eats the whole
  budget (den −17% to −55%). Dead in every conservation regime.
- **Piecewise-linear in log-space above a fitted knot**: the blend achieves the same top behaviour
  with NO knot — a knot is a manufactured discontinuity the audit (#28) and L-SMOOTH then have to
  police. Rejected on smoothness economy.
- **Isotonic re-fit under a convexity floor**: least parametric, least auditable, step-function
  L-SMOOTH risk, no natural Reid extension. Rejected.

### §2.1 — BINDING SUB-DECISION: ρ is the SMOOTHED LEVEL, never single-season points
Pre-sim finding: with single-season output, injured-season cells are crushed (Docherty-class
markdowns of −40..−60% at moderate s). ρ consumes the engine's demonstrated-level machinery
(`level_demo`/`level_now` family — multi-season, injury-filtered), so an LTI year does not read as
output collapse. The directive enumerates the exact feed.
### §2.2 — Smooth onset at the replacement bar
w ramps to zero continuously over a declared width above the bar (one parameter, stated in the
directive) — no cliff between sub-bar and above-bar players (audit #28). No age gates anywhere:
responsiveness is continuous in evidence (audit #29 — no birthday cliffs by construction).

## §3 — DECISION (b): CONSERVATION — PRODUCTION-SIDE LOAD-TIME CALIBRATION, PER POSITION, ACROSS ALL YEAR-DEPTHS
- **Population**: per position, across the whole evidence/age range — NEVER per-(pos, year-depth)
  cell. The pre-sim proves cell-level conservation makes the gate arithmetic a tautology (ratios
  frozen at the breach) — the path under 1.30 REQUIRES value to flow across year-depths.
- **Side**: the renormalisation applies to the PRODUCTION-side term only; pedigree pedestals and
  iso premiums are nominal. A global all-value scale would inflate unearned pick priors and walk the
  census gauge (audit #15) — refused.
- **L-AXIS**: one diagnosed axis — the compression. Donors = sub-elite proven the flat top
  relatively over-priced; recipients = the elite the flat top under-priced + young over-performers
  (the Reid side). No unrelated population finances anything (audit #9).
- **The ledger**: the build ships a whole-system SCAR ledger (players + held picks + every derived
  adjustment) reconciling to zero unexplained residual at a predeclared absolute AND relative
  tolerance (audit #10/#40); the mechanism is an explicit budget transfer VISIBLE in the ledger,
  implemented as the load-time calibration renorm.

## §4 — DECISION (c): THE REID EXTENSION — SAME MAP, EVERY VALUATION SITE, PER-YEAR EVIDENCE
The map wraps the above-replacement production→SCAR conversion at the raw_ev/posval site family
(the Leg-A `iso_eff` site precedent — the directive enumerates the sites exactly as Leg A's did).
Current-year and projected-year legs each carry the E of the year being valued. The ≤22 slope rises
because a young demonstrated over-performer carries real w > 0 the moment evidence exists — no
special young mechanism, no second map. Kill-switch **RL_UNCOMP**: OFF ⇒ the Leg-A head byte-exact
(the A/B identity the ladder asserts).

## §5 — DECISION (d): THE ACCEPTANCE MAPPING (→ acceptance v1.17; audit cluster (ii) folded)
1. **G-COHORT**: frozen July-8 construction, hard ≤ 1.30, scored on **y4 AND y5 AND y6** — the
   pre-sim finds **y4 = 1.3017 is ALSO over at the Leg-A head** (base 1.2960; Leg A pushed it over),
   not only y5 = 1.3160. A committed row-level fixture makes build and audit byte-comparable (#17).
2. **β (proven-27+)**: point ≥ 0.85 with CI ∋ 1.0, under a FROZEN estimator, sample, weighting and
   CI method, with a max CI width / min effective n so imprecision cannot pass it (#13).
3. **≤22 slope**: a minimum effect size, not bare direction (#12) — PROPOSED ≥ 0.15 with the CI
   clear of 0.111 (owner-tunable at the directive).
4. **English/Briggs ≥ 1.75 hard** (R104.3), measured with the captain lift IN (spec §d).
5. **Per-young-player earned-component gate at FINAL SCAR** (#8/#26/#41): no young player's earned
   component falls, measured after ALL composition — the R104.8 decomposition condition carried
   forward from Leg A's prescreen.
6. **Census-v2**: the global gauge ≤ +15,612 AND predeclared cell-level gates by age/evidence/
   position/draft-band (#15) — the conservation design in §3 keeps pick priors nominal by
   construction; the cells verify it.
7. **L-SMOOTH**: a numeric threshold predeclared (#18) + boundary probes at the bar onset and
   evidence knots-that-aren't (#28/#29).
8. **Kill-switch regeneration matrix** (#19/#42): RL_UNCOMP × RL_ISOFADE combinations regenerate
   from the authored store and hash-compare vs runtime-switched output.
9. **Watch rows with exact minimum deltas** (#14); **A4 Reid (rank 40→44, value held 3,650,
   expected-recovery)** is revisited HERE — the acceptance carries his row.
10. **Pre-view hashes** (#16/#22/#45): this memo + the acceptance JSON hashed in the directive
    before any candidate metric is rendered; mutation = HALT.
11. **Leg-C re-measure** (#20): every Leg-B acceptance statistic re-runs after Leg C lands on the
    candidate line; material drift is a ladder stop, not a footnote.

## §6 — THE G-COHORT PRE-SIM (the R104.10 obligation) — **VERDICT: A CREDIBLE PATH UNDER 1.30 EXISTS**
All figures: supervisor re-run, frozen July-8 construction re-implemented verbatim from
`ship_gates_check.py::_b1_july8` on freshly built walk-forward matrices (meta asserted: engine
a83c9f6d · store b1fd0bce · config c2d233aec104). Candidate-map rows are FINDINGS (S4): the proxy
uses single-season Ppath, a coarse E(N), and an all-value renorm — its known biases are stated below.

**A. Baselines (independently re-derived; the build's claims are now re-run facts):**
| head | y4 | y5 | y6 |
|---|---|---|---|
| v2.10-exact (RL_ISOFADE=0, dev-shell) | 1.2960 | **1.3057** | 1.2544 |
| Leg-A head (gate-mode matrix) | **1.3017** | **1.3160** | 1.2664 |
Leg-A attribution: +0.0057 / +0.0103 / +0.0120 — y5 matches item 198 exactly; **y4 crossed at Leg A**.

**B. The rejected price-exponent family** (why it is dead): unconserved γ=1.3 ⇒ y5 = 1.71;
per-cell-conserved ⇒ y5 pinned ~1.32-1.33 at every γ (denominator trapped); per-position-conserved ⇒
den −17%..−55% (elite tail eats the budget), y5 1.58-3.7.

**C. The decided family** (output-anchored blend, per-position conservation, VOR-form out-ratio):
| s | y4 | y5 | y6 | den vs base |
|---|---|---|---|---|
| 0.40 | 1.147 | 1.193 | 1.150 | +7.1% |
| 0.55 | 1.100 | 1.154 | 1.113 | +9.3% |
| 0.70 | 1.061 | 1.119 | 1.080 | +11.3% |
At the β-motivated setting s ≈ 0.55, all three year-depths clear 1.30 with ≥ 0.14 of margin.
**Known proxy biases, declared:** (i) the den lift is OVERSTATED where the proxy renorm touches
pedigree value (the real design renormalises production-side only — §3); (ii) markdown severities
are OVERSTATED by single-season output (cured by §2.1); (iii) E(N) is career-year, not the engine's
qualifying-season weight. None of the three plausibly consumes a 0.14+ margin; the frozen suite
measures the real candidate at the prescreen regardless.
**⇒ The waiver question does NOT return to the owner. Leg B may proceed to directive.**

## §7 — DECISION (e): INTERACTIONS
- **Captain curve**: the map sits pre-captain in composition; English/Briggs is measured with the
  lift in (no coupling term; the kill-switch matrix proves separability).
- **L-SMOOTH**: smooth by construction (§2.2 onset ramp; no knots); the census instrument re-runs.
- **Census gauge**: production-side conservation leaves the unearned accounting nominal; Leg A's iso
  fade is upstream and separable (RL_ISOFADE × RL_UNCOMP in the regeneration matrix).
- **Leg C**: §5.11's re-measure closes the calibrated-to-a-pre-C-population hole (#20).

## §8 — THE RISK THE OWNER SHOULD SEE AT THE VIEWING (plainly)
The board's biggest movement will be DOWN on sub-elite proven players whose price rode the flat top
(the pre-sim's donor side; the flattery-census names overlap — Wanganeen-Milera moves in the proxy).
This is the ruled direction (the pick prior and flat-top excess dissolve both ways — R104.8's gloss),
but the SEVERITY is the s dial and the §2.1 level-feed, and the guardrails are the named reads,
A-PAIRS, the earned-component gate (§5.5), and his sealed reads at the viewing rung. The directive
will carry a donor-side mover report as a first-class deliverable.

## §9 — WHAT FOLLOWS THIS MEMO (the ruled sequence)
Spec v1.2 fold (audit cluster (i): text ↔ ruled state; pre-view hashing adopted) → acceptance v1.17
JSON (§5's entries, machine-readable, + G-Y0's population placeholder for Leg D) → the Leg-B
directive (sites enumerated · the s dial's measurement plan · wall-clock estimate per item 188).
