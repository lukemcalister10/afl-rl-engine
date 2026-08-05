# NAMED FINDINGS — everything that could not be stated as a plain recipe rule, plus verified defects

each classified nobody-understands-it / shouldn't-exist / earns-its-complexity · 2026-08-05

Body text carries no code identifiers; every entry ends with a pointer into the verification appendix, which holds the code-level evidence.

---

## (a) The self-teaching loop (prediction F1)

**Statement.** The frozen start-value surface that prices every unproven player is taught from measured career values; those career values are produced by calling the engine's own valuation function season by season along each career; and that valuation leans on the year-zero estimate wherever a record is thin — through the pedigree term inside every early season's level, through the year-zero anchor inside every sit-out, staleness, floor and scrap rule, and directly through the counted fallback rows where a teaching stratum was too thin. The dependency, stated plainly: the surface learns from values that already contain its own previous generation.

**Corrections carried (ruled).** First, on the pedigree term's weight: the 0.11 figure is the fade factor's floor — the high-evidence asymptote — not a lower bound on the pedigree weight itself, which is the product of a qualifying gate and that fade: approximately zero at zero evidence, peaking at roughly 0.35–0.37 near one qualifying season, and settling at about 0.11 for established players. The echo of the prior is therefore largest exactly where the teaching evidence is thinnest. Second, the aggravator: the walk-forward emitter that produced the teaching values ran with the board-only pricing laws ACTIVE — against the engine's own stated design that teaching harnesses turn them off — so the teaching values were computed with the previous generation of the very surface being refit switched on.

**Classification:** nobody-understands-it. **Why it matters:** the direct self-reference is counted (the fallback share is stamped into the artifact), but the indirect echo — the prior's share inside a non-fallback taught value — is nowhere measured or bounded; no number in the system says how much of the flagship artifact is its own ancestor.

Evidence: verification appendix §4.2 (finding F1; steps 28–33), §2.2.

## (b) The prediction/valuation entanglement (prediction F2 · valuation F2)

**Statement.** No artifact anywhere in the chain is "expected per-season future output". The engine predicts a six-node band of forward-peak levels; every season-level expectation is reconstructed inside the pricing function from one number per node and converted to money in the same loop; the certainty/fade year-weights are simultaneously a belief statement (which future years are credible) and a payment statement (which are paid). The valuation module overwrites the prediction module's level estimator at import, and three pricing caps read the raw record directly, bypassing the band entirely. The list boundary in this recipe is a boundary in concept only.

**Classification:** earns-its-complexity. **Why it matters:** averaging prices over the outcome band instead of pricing the average is deliberate convexity — upside paid and collapse charged by construction — and that genuinely requires re-running the real chain per hypothetical level; a clean handover of per-season expectations would forfeit it. A rebuilder must not invent the missing boundary.

Evidence: verification appendix §4.2 (finding F2), §4.3 (finding F2).

## (c) The frozen, unstatable fitted artifacts

**(c-1) The two frozen forecasting ensembles (prediction F3).** The forward band and ceiling models are load-bearing — they ARE the forward-output expectation — yet unstatable: large boosted-tree ensembles whose committed bytes cannot be regenerated from their own inputs on the same machine. Inference deliberately feeds them a level feature computed by a different rule than the one they were trained on (a declared, permanent train/serve asymmetry); what a fixed ensemble does when one input's distribution shifts by design is not derivable from the code, only measurable. **Aggravator (ruled):** the band model carries a silent cold-cache retrain fallback — if its cached artifact file is missing, the build refits and rewrites the cache with no gate and no halt, producing a non-canonical model; the ceiling model, by contrast, halts. **Classification:** nobody-understands-it.

**(c-2) The start-value freeze (valuation F6, corrected).** "The start-value surface is frozen and loaded" is true only as a conjunction: the surface is rebuilt whenever its anchor curve mutates; the anchor curve mutates during import; so the freeze must pin every intermediate surface or it silently is not a freeze. **Correction carried:** the shipped frozen set holds exactly TWO configuration signatures, not the three the code's own commentary claims — two of the build's fitting calls see the same ladder and therefore share a signature; the freeze needs, and holds, two. An unknown signature halts the build rather than silently refitting. **Classification:** earns-its-complexity — the layered-revert design forces the intermediate rebuilds, and the halt makes staleness loud.

**Why it matters:** these artifacts are the model's core forward expectation and every new draftee's price; none of them can be re-derived from the recipe alone, and one of them can silently self-replace.

Evidence: verification appendix §4.2 (finding F3; step 13), §4.3 (finding F6; step 36).

## (d) The currency-anchor chain (prediction F4 · valuation F4)

**Statement.** The size of a board value point is defined as: "the 99th-percentile player of a retired valuation formula prices at 7,000", renormalized to the pick-1 = 3,000 numeraire by one board factor that divides by the head of an import-time curve fit that never ships and multiplies by the pick-curve derivation's published global head factor. A boot-loaded peak-projection model prices no player on the live path, yet still sizes every value unit, because the unit's definition runs through it. The rule can be transcribed but not justified from the code: the unit depends on machinery the owner ruled deleted, a frozen forest, and a legacy curve head — and the file's own history records that every previous prose description of this chain was measured false. Coherence today is maintained by loader halts, not by construction.

**Classification (ruled):** nobody-understands-it — the defining property is that the unit's definition cannot be justified from the code, only transcribed; the prediction audit's shouldn't-exist verdict is subsumed into this single classification by supervisor ruling (the categories admit exactly one class per finding). **Why it matters:** every number on the board is denominated in a unit whose definition survives only because guards force its pieces to agree.

Evidence: verification appendix §4.2 (finding F4), §4.3 (finding F4).

## (e) Uncommitted derivations and hand-set constants

**(e-1) The six pedigree-pole re-level constants (valuation F5, reclassified by ruling).** The six per-position multipliers that scale the pedigree pole — and hence every young player's price — DO have a documented derivation rule in the changelog (a trajectory-integrated pole over the development maturities divided by the two-season synthetic pole, with a robustness measurement and a passed hard gate). What is missing is a committed, re-runnable derivation script: no executing code in either audited tree can reproduce the six numbers. **Classification (ruled):** shouldn't-exist in its current unreproducible form — a frozen, documented calibration whose derivation code was never committed.

**(e-2) The hand-set staleness and mediocre-cap fractions.** The stalled-player cap's base fraction (25%), the played-but-never-near-par cap's larger base (45%), their per-year decline rates and the tall/ruck multipliers are hand-set constants whose provenance is a one-line comment; no derivation for them is runnable in the tree. Same family and classification as (e-1).

**Why it matters:** these constants directly price the young and the stalled; a rebuilder can copy them but never re-derive them.

Evidence: verification appendix §4.3 (finding F5), §4.2 (finding F6, constants clauses).

## (f) The dormant twin and the duplicate floor loop (valuation F3)

**Statement.** Two textually near-identical copies of load-bearing code exist: a superseded dormant twin of the level estimator, kept "in lock-step" by comment alone and never called; and a live parallel copy of the demonstrated-floor loop that must be edited "both or neither". Nothing executable enforces the lock-step; the tree's own comments queue the deletion/delegation as hygiene for a future build.

**Classification:** shouldn't-exist. **Why it matters:** a recipe rule must say which code produces the number; here correctness depends on a comment-enforced convention that future edits touch both copies.

Evidence: verification appendix §4.3 (finding F3).

## (f-bis) The price-space correction ladder (prediction F6, order corrected)

**Statement.** After the band is priced, the corrections act on the price in a fixed order that is itself part of the recipe — and nothing in the tree asserts that order. The verified execution order: the delist override pre-empts the entire ladder (it is the first gate, not the last rung); the un-compress output-proportionality step runs BEFORE the pedigree-pole pull; then the youth credit, the pick-order guard, first-evidence smoothing, the ruck ceiling, and the key-forward compress; the sit-out branch is evaluated and RETURNS before the staleness/mediocre caps ever run; then the staleness caps, the in-progress clock blend, and the start-value floor. (These three order facts correct the draft, which had the un-compress after the pole pull, the sit-out after the caps, and the delist override as the closing rung.) Caps applied after multiplicative credits bite differently than before them; the composed object is order-dependent even though each rung alone is a statable, owner-ruled rule.

**Classification:** earns-its-complexity — each rung is derived and ruled, and the order is the code; but a verifier and any rebuilder must treat the ORDER as part of the recipe, because nothing else records it.

Evidence: verification appendix §4.2 (finding F6).

## (g) Store data defects and rebuild traps

**(g-1) The stale derived counters — the #323 set (supervisor-confirmed).** The top-level career-games counter disagrees with the sum of season games on 569 of 2,651 records (548 under, 21 over), because the weekly merge updates only the season row while the live sample-size trust weight reads the top-level number. The has-current-season flag is stale-false on 27 records that do carry a current-season scoring row (a fallback test rescues them on today's board). Both findings are supervisor-confirmed by independent recount. Cross-reference: GitHub issue #323 carries the owner-worded store corrections — the derived career-games rule, the Leigh Brown removal with draft slide, the Bobby Hill 2019 season and 2023 average, and the counter reconciliations. **Classification:** shouldn't-exist. Evidence: §4.1 (findings 1, 2).

**(g-2) Pick numbering is the database's own universe (store finding 4, corrected).** Store selection numbers are a continuous per-year ordering under the owner's data law; the official published pick count is explicitly not the authority, so a rebuilder importing official draft results diverges. Correction carried: every per-stream per-year sequence in the shipped store is now gapless (maximum equals count in all years); the old gapped year-ends survive only in the last-national-pick side table, which consequently disagrees with the store's own last national ordinal in 4 of 23 years. **Classification:** earns-its-complexity (the ruled convention); the divergent side table itself: shouldn't-exist. Evidence: §4.1 (finding 4; item 31).

**(g-3) Two club fields on two axes (store finding 9).** One field is the real league club (display and name disambiguation); the other is the owner's keeper-league team holding the player (store-authoritative by ruling, read only by the movers report and the web join). Easy to conflate blind. **Classification:** earns-its-complexity. Evidence: §4.1 (finding 9).

**(g-4) The birth-year convention (store finding 11).** 302 records carry no birth year; the engine assumes age 18 at entry. Ages for those mostly long-retired players are a convention, not data — and the same convention silently shapes the historical training cohorts. **Classification:** earns-its-complexity (a declared fallback), noted because it leaks into training. Evidence: §4.1 (finding 11).

**(g-5) Two schemas in one list (store finding 12, corrected).** Six columns exist on exactly the 804 active records, plus the birth-date column on 848 records overlapping 46 retirees — seven newer columns in all, not eight as first drafted. The store is effectively a lean historical schema and a richer active-roster schema in one flat list, and nothing declares the structure. **Classification:** earns-its-complexity (the tiering is real and sensible), with the non-declaration flagged. Evidence: §4.1 (finding 12).

**(g-6) Name-key collisions (store finding 13, corrected).** The store's join keys are currently globally unique (2,651 of 2,651 distinct); the two same-named active players sit under distinct keys, and the recorded collision was a display-name artifact of the score feed's export. The live risk is name collisions in the weekly FEED, defended by the durable-ID resolver and a now-retired round-scoped override; the store-side dedup code is hypothetical defence-in-depth. **Classification:** earns-its-complexity. Evidence: §4.1 (finding 13).

**(g-7) The store is mutated in memory at load (store finding 14, verifier-strengthened).** The engine derives position/route/pool fields onto every record at import, and for four re-entry supplemental players the loader also rewrites the route, entry year and grouping (a broader mutation than first recorded). A field census taken through the engine after import will not match the file on disk — a rebuild trap. **Classification:** shouldn't-exist (as a trap; the derivation itself is ordinary). Evidence: §4.1 (finding 14).

## (h) The hygiene-note set

All entries here are one-line cleanups: real inconsistencies with no live defect path. Classification for the set: shouldn't-exist (hygiene grade).

**(h-1) The merged gamma note (valuation F1 downgraded by ruling; absorbs the refuted prediction F5).** The value-curve concavity dial's frozen-surface signature carries a contradictory 0.85 default beside a comment claiming it matches the engine's default of 1.0. Both are dead text: an import-time force-set to 1.0 always runs before any signature is computed (supervisor-verified), so the signature always signs the value the engine actually runs; there is no live misload path, and the once-alleged armed trap is impossible in-process. Roughly ten stale 0.85 pins also survive in auxiliary check scripts. A one-line cleanup each: fix the false comment, delete the dead default, update the stale pins. Evidence: §4.2 (finding F5 — refuted as a live defect), §4.3 (finding F1), §2.3 (step 6).

**(h-2)** A live pricing branch exists for the pre-season-draft route, which no record carries; the 8 known pre-season draftees are filed under the rookie route with a source note (store finding 5). Evidence: §4.1 (finding 5).

**(h-3)** A code comment says 90 players carry an alternate future stream; the data says 87 (store finding 7). Evidence: §4.1 (finding 7).

**(h-4)** The alternate-stream probability field is raggedly typed — mostly decimals, two whole numbers; the engine coerces harmlessly, a strict-schema rebuilder would trip (store finding 8). Evidence: §4.1 (finding 8).

**(h-5)** The concession-category and route-label fields carry free-text one-offs and one spelling variant; display-only (store finding 10). Evidence: §4.1 (finding 10).

**(h-6)** Five provenance columns are written and never read — the audit trail of the past pick renumbering. Corrections carried: the simplified stream code collapses five routes into its "OTHER" bucket (the mid-season and pre-season-supplemental routes keep their own codes), and the within-stream selection number is byte-identical to the main selection number on every row where either is present — fully redundant, not merely unread (store finding 6, corrected). Evidence: §4.1 (finding 6; item 29).

---

Dropped by ruling: store finding 3 ("the scoring system is never named") — REFUTED at verification and removed entirely.
