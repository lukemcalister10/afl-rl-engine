# SPEC 3 — RYAN / MOORE DOWN-MOVE PERSISTENCE (BODY-OF-WORK INERTIA) — v2.9 spec · 2026-07-12
### Register item 7 (OPEN_ITEMS v8) · TIER-3 spec (design only) · FABLE
### Owner reads: luke-ryan 1698 "a bit high" (30yo GDEF) · dylan-moore 1500 "a bit low"
### (137-game body of work slashed off ONE poor season). The DOWN-side mirror of the riser
### question — paired BY CONSTRUCTION with the age-persistence machinery (banked branch
### `claude/age-persistence-curve-research-l7hinr` @ 394cd16) so the two cannot ship
### contradictory curves.

## 0 — SUBJECTS AS THE BOARD CARRIES THEM (verified this session, board 9ecbe0fa)
**luke-ryan** — GEN_DEF, ND 2016 pick 65, born 1996 (30), 190 games, ev **1698**.
Line: … 98.7(24g) → 109.5(23) → 116.6(23) → 94.1(24) → 92.3(12, in-progress).
**dylan-moore** — MID drafted, priced GFWD, ND 2017 pick 66, born 1999 (26-27), 137 games, ev **1500**.
Line: 94.6(22g) → 91.0(23) → 96.5(25) → 87.5(26) → 71.3(12, in-progress).
Both are established (nqual≥4) and ride the DOWN-BRANCH of the level core. Both 2026 "poor
seasons" are IN-PROGRESS at 12 games — on-pace, so the M3 blend gives them NO pin protection
(s=0 at ≥11 games): the down-move is priced as if demonstrated.

## 1 — WHAT THE ENGINE ALREADY BELIEVES ABOUT DOWN-MOVES (the incumbent, read from code)
The down-branch (`_coreM1`, `_lvl_eff_core`) is NOT a flat rule; it already encodes a measured
position: drop = L_old − L_current(recency-weighted, LDECAY GEN 0.35 / MID+RUC 0.225 / KEY 0.40);
drop ≤ 3 holds; the shed phases in over drop 3→8 toward **Lc × _agemult2(age, lcr)** where:
- `_agemult(age)`: 0.92@20 → 0.85@25 → 0.79@28 → 0.73@30 → 0.55@37 — derived 2026-06-30 from
  realized forward output of established decliners ("recovery ~0 beyond ~3 SC drop").
- `_fbump(age, lcr)` (PR #45, folded at W4): an UP-ONLY recovery credit in level-above-replacement
  (lcr) — measured r = fwd(Y+1..Y+3)/Lc over 2369 established-decliner player-seasons, mean r
  rising 0.11 → 0.90 across lcr; a still-elite 30yo shed multiplies ≈0.73+0.08…0.14 rather than 0.73.
So the incumbent doctrine is: **down-moves persist almost fully, softened only by age × current
elite-ness.** The owner's Moore read asserts a THIRD axis — body of work (137 games) — should buy
mean-reversion the current surface doesn't price. The owner's Ryan read asserts the OPPOSITE sign
at 30: the shed should bite HARDER than _fbump lets it. One measurement must answer both; that
opposition is exactly why this is measure-first, not fix-first.

## 2 — THE PAIRING CONSTRAINT (the reason this spec exists now)
The UP-side is mid-flight: flat S_M1 = 0.46 shipped; candidate s(age) = 0.86@22 → 0.49@25 →
0.27@27 → 0.03@29 (crosses 0.46 at 25.3), adoption A/B/C gated on the walk-forward G-COHORT
re-measure (register: v2.9 batch; butters −1.0%-vs-2% margin noted). If v2.9 adopts s(age) for
up-moves and separately re-derives down-move behavior on a different extraction, the board ships
two independently-fitted opinions about the same object — how much a season-level shock at age a
carries forward. REQUIREMENTS, binding on the v2.9 build:
- **One extraction, one book, both signs.** The down-side measurement MUST be produced by the same
  script lineage, population definitions, kernel discipline (h=2.0 baseline, eff-n≥35 nodes),
  leak-free cut (events Y≤2022) and cluster-bootstrap convention as l7hinr's s(age). Publish ONE
  joint table on one age grid: s_up(age) (fraction of up-gap persisting) and s_dn(age | bow, lcr)
  (fraction of down-gap persisting = 1 − recovery).
- **Coherence checks (reported, not gated):** (i) both curves bracket the unconditional age trend —
  E[Δlevel | shock] blended over shock signs must reproduce the plain aging curve the store shows;
  (ii) where the axes overlap, s_dn must reconcile with the PR #45 r-surface (its 2369-season
  population is the incumbent evidence — replicate it on its own axes FIRST, then extend; a new
  surface that cannot reproduce the old one on the old axes is a basis bug until explained);
  (iii) no age may price BOTH signs as ~fully transient (that claims age-a seasons carry no
  information) or both as ~fully permanent (that claims age-a level is a random walk with the
  variance of one season) without the joint table saying so out loud to the owner.
- **One ruling session.** The A/B/C up-side options and the down-side finding go to the owner
  TOGETHER (the register already sequences both into the v2.9 batch with the age machinery).

## 3 — MEASUREMENT DESIGN
Estimand family, established players (nqual ≥ 4 at event):
- **Event:** completed season Y with games ≥ 12 (G_ADQ convention) and season level at least D
  below the established level L_old (computed as `_lvl_eff_orig` at Y−1 — the engine's own object,
  so findings map 1:1 onto dials). Primary D = 8 (where the shipped shed saturates); grid D ∈
  {5, 8, 12, 16} reported (the drop 3→8 onset band is itself under test).
- **Outcome:** r = games-weighted forward level (Y+1..Y+3, engine ruler) expressed BOTH ways:
  r_old = fwd/L_old (recovery toward the body of work) and r_cur = fwd/Lc (the PR #45 convention)
  — publishing both denominators is what lets the owner see "mean-reversion" and "persistence" as
  the same number read from two ends.
- **Axes:** age at Y × body-of-work at Y — bow measured two declared ways: career games, and
  n-seasons-within-5-of-L_old (a 137-game career of one good year is not Moore's case; separate
  them) — × lcr (keep the incumbent's axis so the extension is nested).
- **The body-of-work question, precisely:** after conditioning on age × lcr (the shipped surface),
  do the bow slices separate? Moore's cell (age 26-27, bow 130+, one sub-level season) vs the same
  age × lcr at bow ≤ 80. Ryan's cell (age 30, high lcr, TWO consecutive sub-peak seasons) is a
  different event class — single-season events vs sustained-decline events (2+ consecutive) are
  extracted as SEPARATE event types; the owner's two reads live in different cells of the same table.
- **Washout convention:** washout-INCLUSIVE (exits/delists = zero forward), matching the incumbent
  derivation — and additionally report the survivor-only column so the owner sees how much of
  "persistence" is list mortality (for a 30yo the delist hazard IS the persistence mechanism).

## 4 — EXACT DATA CUTS
- Store 04f38dad basis (re-pin at fire time). Events: seasons 2004–2022 (outcomes complete by
  2025; leak-free vs the 2026 board). WALK-FORWARD BASIS (named): every model-side quantity at Y
  (L_old, Lc, lcr, nqual) computed from data ≤ Y only; asserted by CODE READING of the extraction
  script (G-COHORT basis rule; no numeric fingerprints).
- Positions pooled primary (the l7hinr result: interactions unsupported except sustained-at-22);
  KEY/RUC cell SHOWN (late-maturing check; thinnest — declared), GDEF cell shown (Ryan's), GFWD
  cell shown (Moore's) — shown-not-decided, one pooled curve unless bands separate (both eff-n≥12,
  the l7hinr support standard).
- Expected n: the incumbent found 2369 established-decliner player-seasons at drop>3 — slicing by
  bow × event-type will thin fast. Thin-slice doctrine: pool to eff-n ≥ 35 per kernel node,
  DECLARE every pool; the finest supported resolution governs, smoothed (kernel), never a fitted
  step at a bow threshold.
- Level basis: lcr per position-of-record IN season Y (Moore's MID→GFWD flip moves his REPL bar
  9.2 pts — see confound 4).
- Both lenses where value-denominated (the estimand itself is in level space — lens-free; the
  who-moves sim below is dual-lens).

## 5 — TEST DESIGN
- Kernel-smoothed r over (age × bow) at fixed lcr bands; cluster bootstrap by player (B=1000).
  "bow adds signal" = bow slices' bands separate at fixed age × lcr (support standard as above).
  NO pre-registered statistical acceptance gate (doctrine: statistics inform; owner reads + hard
  guards accept).
- Incumbent replication FIRST (the r vs lcr curve on the PR #45 axes must reproduce within bands)
  — this is the basis assertion that the new extraction measures the same universe.
- **Who-moves sim (read-only, on the candidate surface):** if the measurement supports a
  bow-conditioned shed target, sim the full board (the l7hinr sim pattern: named movers, biggest
  20, anchor deltas, dual-lens) — the owner rules on names, not curves. Ryan and Moore are re-stated
  from their cells with their in-progress-season caveat attached.
- Named acceptance contacts computed in the sim: A-PEAK (butters/holmes — the up-side candidate
  already sits at −1.0% of the 2% tolerance; a down-side change must report the JOINT effect),
  A-FADE (coniglio/blicavs/guthrie at-scrap-flat satisfies; the decline lever must remain folded),
  A-BONT (30yo — any softening of old-age sheds grazes his ≥+10% BINDING anchor from the other
  side: it must not LIFT him via reduced shed either, direction-checked), G-COHORT walk-forward
  re-measure MANDATORY before any adoption (bow credit lifts year-4-6 survivors = numerator —
  adverse direction, same gate the up-side adoption already carries).

## 6 — EXPECTED CONFOUNDS
1. **In-progress 2026 events are not events.** Both subjects' flagged seasons are 12-game partials;
   within-season recovery is invisible to a season-grain extraction. The extraction uses COMPLETED
   seasons only; the subjects are then PRICED off the measured surface through the live M3/
   SEASON_PROG machinery — the spec measures the curve, not the two names' partials. Declared to
   the owner explicitly: Moore's 71.3 may be half a poor season, and the read may resolve itself
   by round 24.
2. **Selection into the event (injury-in-season).** A poor season with ≥12 games can still be a
   carried-injury season — indistinguishable in-store. Pooled and declared; the LTI register has
   no history (R2 input covers current absences).
3. **Role/position changes** (Moore MID→GFWD): level shifts from role, not ability. Control: lcr
   on position-of-record per season; flag event-seasons with a recorded position flip and show the
   with/without-flip slices.
4. **Delist-timing endogeneity:** clubs delist AFTER poor seasons — forward zeros concentrate in
   exactly the cells under test. That is genuine keeper-value loss (washout-inclusive is the right
   primary) but the survivor column must be shown or "persistence" conflates output decline with
   list decisions.
5. **Era drift & scoring inflation:** levels computed vs season-REPL; class-year clustering
   absorbed by the bootstrap.
6. **Mean-reversion by construction:** a season selected for being ≥D below level regresses toward
   the mean mechanically under noise even with no real signal. Control: the null band — apply the
   identical event filter to a permutation/synthetic-noise baseline (season-level noise at the
   store's observed within-player variance) and report r against THAT null, not against 1.0. This
   is the single most likely way a naive "body-of-work mean-reversion" finding would be fake.
7. **bow correlates with age and lcr by construction** (you don't reach 137 games young or bad) —
   the nested design (bow tested WITHIN age × lcr cells) is the control; where cells thin out, the
   pooling declaration says so rather than letting the correlation masquerade as signal.

## 7 — REFUTATION CLAUSE (owner doctrine §49)
Symmetric, and the two reads can lose independently:
- **Moore side refuted** if, at age 26-27 × high bow × one-poor-season, r_old's band sits at/below
  the incumbent surface's implied forward (no bow effect beyond age × lcr): then 1500 is
  measured-honest, "a bit low" closes, and bow is filed as a non-mechanism (the l7hinr precedent:
  the two names that started the up-side question were both refuted while the machinery finding
  stood).
- **Ryan side refuted** if, at age 30 × high lcr × sustained-decline, r_cur's band sits AT the
  _fbump-credited level (the still-elite 30yo really does hold ~0.81–0.87 of current): then 1698
  is measured-honest and "a bit high" closes.
- Both reads can also WIN in the same table (bow effect real at 26 AND high-lcr credit too generous
  under the sustained-decline event type at 30) — the event-type split is what makes that outcome
  expressible.

## 8 — IMPLICATIONS (mandatory)
- **This is the second half of the persistence machinery.** Whatever v2.9 rules on s(age) for
  up-moves, this measurement either completes a coherent two-sided persistence model (one
  extraction, one table, one ruling) or — if bow adds nothing and the incumbent replicates — it
  formally closes the down-side as already-measured, which is itself the pairing guarantee the
  register asked for ("so the two don't ship contradictory curves").
- **If bow is real at Moore's cell:** the fix is a shed-target term (recovery toward a
  body-of-work-weighted level), fitted and smoothed on the measured surface — a mechanism, not a
  "veteran multiplier"; blanket multipliers stay forbidden. Movers will concentrate in established
  26-29yo one-bad-year names — the sim's named list goes to the owner with the A-PEAK joint margin
  stated first (it is already the narrowest number in the batch at −1.0%/2%).
- **If the Ryan side is real:** _fbump's up-only credit gets an event-type condition (sustained
  decline ≠ one-season dip) — again surface-shaped, not name-shaped. Direction is A-FADE-friendly
  and G-COHORT-friendly (sheds the old-survivor numerator down) but A-BONT/A-GAWN must be
  direction-checked in the sim (both are 30+ anchors).
- **Sequencing:** runs beside (not after) the up-side G-COHORT re-measure; both surfaces go to the
  same v2.9 ruling session with the joint table. The FLEX build and PVC adoption are independent
  of this lever; no ordering constraint beyond the shared ruling session.
- **Cost of not running it:** v2.9 would adopt an age-conditioned UP-side while the DOWN-side keeps
  a differently-derived 2026-06-30 surface — two curves, two bases, one object; and the owner's
  two named reads (opposite signs on the same branch) would stay unadjudicated anecdotes.
