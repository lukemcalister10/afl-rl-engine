# ORDER 27 — RULINGS INVENTORY (Phases 1–2)

Extracted from the register per `METHOD.md`. **190 ruling records.** Rulings are recorded as the register states them; nothing here adjudicates.

## Counts by triage class

| class | n |
|---|---|
| LIVE-STANDING | 91 |
| PROCESS-LAW | 44 |
| QUEUED | 34 |
| ONE-TIME-COMPLETED | 15 |
| SUPERSEDED | 6 |
| **total** | **190** |

## Counts by verification class (LIVE-STANDING + PROCESS-LAW only)

| class | n |
|---|---|
| ENFORCED | 73 |
| DELIVERED-UNGUARDED | 18 |
| NOT-REFLECTED | 3 |
| AMBIGUOUS-OR-CONFLICTING | 3 |
| UNVERIFIABLE-BY-CODE | 38 |

## The inventory

### R001 — numeraire
- **register location:** units BLK0008, SEG0921 · versions v17(2026-07-12), v511
- **ruling:** THE NUMÉRAIRE LAW (owner-ruled 2026-07-12: "Rebase, 3000 is it."): PICK 1 = 3000 IS THE NUMÉRAIRE … a NUMÉRAIRE ASSERT joins the export/bake checklist — any future board with pick-1 ≠ 3000 HALTS; future scale drift re-bases the CURRENCY to the anchor, never the anchor to the drift.
- **register's own status claim:** LAW; asserted at bake
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** one_source_selftest.py:431 check(_p0i[1]==3000); :551 curve artifact self-declares numeraire_pin1_3000; shipped board lensPicks[0].v == 3000 (data/rl_build/rl_app_data.json); manifest RL_PICK1=3000.

### R002 — curve/law-4
- **register location:** units SEG0921, SEG0910 · versions v511
- **ruling:** G-MONO AMENDED — LAW-10 ACT … Law 4 now reads: the NATIONAL pick curve covers picks 1–64 and is strictly decreasing across that domain, pick 1 = 3000 exactly; selections past 64 are not on the curve, they enter the pool and are valued by position, where order of selection carries no value.
- **register's own status claim:** RULEBOOK v2.1 + acceptance twin 2.1
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **supersession:** amends R104.9 (strict descent 1..79) — see R003
- **evidence / note:** docs/RULEBOOK.md law 4 v2.1; ingest_inputs monotonicity check scoped 1–64 (v582 ruling 1); one_source_selftest curve-artifact check r104_9_strict_descent; board picks 3000/2999/2874 descending.

### R003 — curve/strict-descent
- **register location:** units BLK0177, BLK0304 · versions item197, R104.9
- **ruling:** R104.9 — THE STRICT-DESCENT PVC GATE: the re-derived PVC must have EVERY pick 1 through 80 at least 1 point lower than the pick before it — curve(p+1) ≤ curve(p) − 1 for p = 1..79.
- **register's own status claim:** LEG-D HARD gate, acceptance v1.17
- **triage:** SUPERSEDED
- **supersession:** superseded on domain by R002
- **evidence / note:** Domain narrowed to 1–64 by Law 4 v2.1 (R002); the 65+ tail is no longer on the curve. Both stated; no winner picked.

### R004 — curve/closure
- **register location:** units SEG1355, SEG1359 · versions v572, v573
- **ruling:** L6 closes CONVERGED AT TOLERANCE — a pass moving no pick by more than 1 board point is converged … REVERSAL CONDITION: any future pass moving any pick by more than 1 point re-opens the closure and returns it to the owner.
- **register's own status claim:** closure ruled; re-closure ruled at v573 on the corrected store
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** The ±1 reversal condition is a process trigger carried in register prose and in act briefs (#334 step 3). No committed check re-derives the ladder and compares; it fires only when an act chooses to re-derive.

### R005 — curve/frozen-ruler
- **register location:** units SEG2398, SEG2489 · versions v691, v701
- **ruling:** the anchor (pick 1 = 3000 frozen ruler)
- **register's own status claim:** binding on ORDER 26B; the ×1.4200 anchor factor recorded as a measured constant
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Same site as R001. 26B honoured it (packet), and the numeraire route (through vs beside) is an OPEN owner decision.

### R006 — numeraire/pooled
- **register location:** units SEG2489 · versions v701
- **ruling:** the pooled-numeraire economy re-denominates picks AND PLAYERS from ONE measured head; s = RL_PICK1 / pooled_head_pre_scale; the E6 coherence halts exist so one side can never scale alone.
- **register's own status claim:** engine law; the seat's contrary claim WITHDRAWN
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** rl_model.py::_load_numeraire; E6 coherence halts. Owner-caught seat error corrected on the record.

### R007 — curve inputs / force majeure  ⚑FLAG
- **register location:** units SEG0996, SEG1006 · versions v533(2), v539 (#271 Addendum 2)
- **ruling:** EXCLUDE Paddy McCartin and Tom Boyd, every player in their drafts slid up one pick to cover — owner words verbatim: "those players were pick 1 KPF busts, so heavily bias the pool against them, however one retired early with depression, and another with concussion issues. It's a force majeure situation, so I am ruling that it shouldn't reflect on the KPF values." … AMENDED to WHOLE-DRAFT SLIDE (a natural pick 65 slides to 64, ENTERS the ND fit and leaves the pool for that year; slid effective picks computed BEFORE the ND/pool split; the store is never edited).
- **register's own status claim:** Discretionary, sealed; "the third ruling-as-prose failure this week" (v701)
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Honoured by hard-coded dicts in the offline instruments only: session_2026-07-29/item271/emit_matrix_271.py:53, docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py:83, and now 26B CFG.force_majeure. The LIVE ENGINE's own exclude-and-slide facility (rl_model.py:284-296 _pvc_exclude/_pvc_eff/_epk) does NOT carry them: store rows paddy-mccartin and thomas-boyd have no _pvc_exclude flag (probe_named_rows.py). ORDER 26B is the proof the class recurs.

### R008 — curve inputs / GWS concessions  ⚑FLAG
- **register location:** units SEG0996, SEG0997 · versions v533(1), v534(2)
- **ruling:** INCLUDE Jeremy Cameron, Dylan Shiel, Adam Treloar in the PVC going forward — GWS-concession entries … Cameron/Shiel/Treloar carry owner-assigned notional draft picks IN THE SHEET (where they would have gone if draft-eligible) — transcribe as given; v533's open detail is CLOSED.
- **register's own status claim:** sealed; open detail closed at v534
- **triage:** LIVE-STANDING · **verification:** NOT-REFLECTED
- **evidence / note:** The data half landed (store carries the notional ND-2011 picks: shiel 4, cameron 12, treloar 14). The machinery half did not: all three still carry _pvc_exclude=true in the landed store, and _pvc_exclude is precisely the flag that drops a row from the PICK-CURVE builders (rl_model.py:284-296) and from every curve-teaching population (emit_matrix_271.py:89 / emit_matrix_338.py:119 `eligible(p) … not p.get("_pvc_exclude")`).

### R009 — pool / ND65+ cap
- **register location:** units SEG1043, SEG2290 · versions #271 A22, v682/ORDER23
- **ruling:** THE ND-65+ CAP, a monotonicity PRICING law: ND-65+ prices equal-or-lower than the ruled curve's pick-64 value … AMENDED (v683): "Happy to amend the law… only historical ones… production determine their price now" — the min-against-curve[64] cap REMOVED.
- **register's own status claim:** amended by owner word at the pool landing
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **supersession:** amends the N43 cap limb
- **evidence / note:** one_source_selftest.py:660 asserts ND65+ prices at its DERIVED level and that the min-against-curve[64] cap is REMOVED; pvc_curve_v2.json carries signed_nd65_plus.

### R010 — pool / signed levels
- **register location:** units SEG1307 · versions v567 (N43)
- **ruling:** THE POOL-LEVEL SIGNATURE (N43): levels = the K=15 column — each division weighted n/(n+15) toward the pool-wide MEASURED aggregate, never the model prior; SIGNED LEVELS (VOR) per division.
- **register's own status claim:** signed; re-derived and re-signed at the 2026-08-12 pool update
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** pvc_curve_v2.json pool_levels (signed_flat + signed_rd_positional, ruling stamps _*_ruling_2026_08_12); one_source_selftest.py:627-700 asserts the fourteen levels verbatim, the currency factor, and the mirror.

### R011 — pool / day-0 pricing  ⚑FLAG
- **register location:** units SEG1366, SEG2430 · versions v574 (#326), v695
- **ruling:** the N43 signed levels price pool entrants AT ENTRY the way the pick curve prices national draftees — the entry anchor the year-zero floor and the thin-record blend read, fading as information arrives.
- **register's own status claim:** LANDED 2026-08-05 ("Keep as ruled. Land it."); v695 records it UNDER-DELIVERED
- **triage:** LIVE-STANDING · **verification:** NOT-REFLECTED
- **evidence / note:** The register's own ORDER 26A measurement: printed pool day-0 = 2.6498× the signed anchors (positional RUCK 1.315 → KPF 5.114). This seat verified the checkable half: one_source_selftest.py §(10) asserts the levels are carried, the currency, the anchor reach and the ND65+ amendment — but NO check asserts the ruled sentence itself (printed day-0 == the derived entry value). Searched: "day-0"/"day0"/entry_anchor equality asserts across one_source_selftest.py, ship_gates_check.py, _merged_recover.py.

### R012 — pool / two-layer architecture
- **register location:** units SEG2139, SEG2146 · versions v668, v669
- **ruling:** THE TWO-LAYER POOL ARCHITECTURE + THE RECONCILIATION LAW: "an individual v0 may differ from its pathway's all-inclusive value, but ACROSS ALL SELECTIONS a pathway's average v0 must be near-identical to its all-inclusive value — as ND v0s reconcile to the pick curve."
- **register's own status claim:** standing, owner-stated
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Reconciliation measured 2.21e-16 / 2.23e-16 at the ORDER 22/23 landing (v682/v683); the renormalisation guard is what reconciles shrinkage with the law.

### R013 — pool / same-derivation
- **register location:** units SEG2109, SEG2124 · versions v666, v667
- **ruling:** RULING 1 — SAME DERIVATION, NOT SCALING: pool entry values and pool v0s are DERIVED from historical career outcomes BY THE SAME METHOD THE ND PICK CURVE IS DERIVED BY.
- **register's own status claim:** standing
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Delivered by the pool repricing act (D1 amended derive-not-scale); no permanent assert binds a future act to it.

### R014 — pool / H cells
- **register location:** units SEG2234, SEG2244 · versions v676, v677
- **ruling:** D8 RULED — THE POOL-ONLY SITTER MULTIPLIER GOES: H_POOLSIT 0.804 and H_UNION 0.280 RETIRED (H_MATNONRD already 1.0 at the landing).
- **register's own status claim:** ruled; landed
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** _merged_recover.py:2190-2208 H_UNION/H_POOLSIT/H_MATNONRD all default 1.0, superseded values preserved as history in comments; data/model_config.json declares RL_H_UNION/RL_H_POOLSIT/RL_H_MATNONRD = 1.0 so gate/bake mode rejects drift.

### R015 — pool / separation
- **register location:** units SEG2244 · versions v677 (5255810874)
- **ruling:** THE SEPARATION LAW: "The ND and pool need to be entirely separated. Nothing here can impact ND pricing" — zero tolerance, ASSERTED not hoped.
- **register's own status claim:** ruled; asserted at the pool landings
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** ORDER 20/22/23 evidence: national v0_start 0 of 668 movers, target identical to 10 digits; _h_cut cells gated on p['_pool'] (_merged_recover.py:2209-2221) so no ND row can see them.

### R016 — pool / shrinkage
- **register location:** units SEG2244 · versions v677 (5260713967)
- **ruling:** K=15 UNIFORM ACROSS EVERY PATHWAY AT LAYER 1 ("K=15 was across the board, not PDS."), K=10 layer 2 unchanged.
- **register's own status claim:** superseding the PDS-only scope of 5253173347
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **supersession:** supersedes the PDS-only K scope
- **evidence / note:** pvc_curve_v2.json pool_levels['k']; ORDER 22 derived layer 1 at uniform K=15 with the renormalisation guard.

### R017 — era normalisation  ⚑FLAG
- **register location:** units SEG1479 · versions v598
- **ruling:** NO ERA NORMALIZATION (owner ruling, #334 Addendum 3): SuperCoach is scaled by construction (3,300 points per match) — scores are era-comparable … normalization is unnecessary AND misleading; it is REMOVED everywhere, a product law binding engine, teaching measures and instruments.
- **register's own status claim:** product law; recorded IN BREACH on main at v637; removed early in the composition build (v638/v658)
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** The live engine is clean: _merged_recover.py:53-57 records "every a*REF/era.get(y,REF) site are gone; season averages are read RAW. Do not reintroduce." No era.get site survives on the value path. BUT the only protection is that comment — no gate, selftest or lint asserts the absence, and the law was in breach on main for ~4 days after being ruled binding.

### R018 — year-zero surface / monotonicity
- **register location:** units SEG1572, SEG1580, SEG1634 · versions v613, v621 (1.1/1.2), v623
- **ruling:** R12 (2026-07-03, LUKE_RULINGS_LEDGER.md, owner verbatim): continuous V0 curve over pick, isotonic non-increasing, zero inversions, gate D14b … 1.1 RESTORE YES (isotonic MERGE per position×age profile) + 1.2 the surface-level never-rises scan.
- **register's own status claim:** BROKEN on the board 2026-08-05→08-10, RESTORED and wired
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** one_source_selftest.py:920-950 runs _v0_curve_assert() D14a/b/c on the STANDING GATED BUILD PATH and D14d scans the surface (rising_steps_1_64 and full grid must be 0); ci-guards.yml:93-97 runs one_source_selftest.py; ship_gates_check.py:716-761 keeps the hand-run superset. The comment at :925 names the process hole this closed.

### R019 — smoothness
- **register location:** units BLK0056 · versions item69 (R98.2)
- **ruling:** THE SMOOTHNESS LAW: A VALUATION MUST BE CONTINUOUS IN ITS INPUTS. No player's value may jump because a counter ticked over.
- **register's own status claim:** BINDING (L-SMOOTH in the acceptance twin)
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** acceptance twin gate L-SMOOTH, amended by owner word 2026-07-24 to "no UNDECLARED value discontinuities … a discontinuity is lawful only if registered before scoring with its step measured and reported as a margin".

### R020 — smoothness / waiver
- **register location:** units BLK0178 · versions item308
- **ruling:** THE WAIVER (owner verbatim, scope exact): "I understand round 24 to off season would not be a smooth transition, and violate a law. Waived." ⇒ the Smoothness Law is OWNER-WAIVED for ONE NAMED TRANSITION ONLY: the season-end evaporation of the current-season value component.
- **register's own status claim:** waived for one named transition; binding everywhere else
- **triage:** QUEUED
- **evidence / note:** The transition it waives (items 307/308 season-leverage design) is itself POST-v2.11 triggered and unbuilt.

### R021 — captaincy
- **register location:** units BLK0048, BLK0061 · versions item61, item73
- **ruling:** THE CAPTAINCY LAW: the captaincy credit is a PURE FUNCTION OF PROJECTED SCORING LEVEL, applied IDENTICALLY wherever a level is priced — the current season, every future season in a player's path, and every historical season in the walk-forward book; no player-specific exceptions.
- **register's own status claim:** RATIFIED; wired at the v2.10 bake
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** rl_model.py:658-678 _capt_ruled (softplus integral-of-P form, LCAPT_BAR/M/W/G pinned in-code, "no os.environ on a board-changing dial"); the rejected saturating curve is reachable only via RL_CAPT=0 as the byte-exact base proof.

### R022 — book parity
- **register location:** units BLK0050 · versions item63
- **ruling:** THE BOOK-PARITY LAW: the book and the board must be built by the SAME formula … Any change to the pricing formula REQUIRES a book rebuild and re-seal before any gate reads it.
- **register's own status claim:** LAW
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** G-BOOK gate + book_stable_seal.json; every landing since re-seals the book (F2 board==book parity in one_source_selftest.py:146).

### R023 — evidence weighting
- **register location:** units BLK0349, BLK0350 · versions item240 (R105.4), item241 (R105.5)
- **ruling:** R105.4 THE QUALIFYING LAW — WEIGHT, DON'T GATE ("I don't think we should wipe the data from the year — the games are still good information"); FORBIDDEN: any exclusion, floor, or phase gate. R105.5 L-RECENCY: an individual match's influence must always count for equal or more than matches from earlier seasons.
- **register's own status claim:** BINDING with a halt-not-warn self-test
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** one_source_selftest.py:276-340 — L-RECENCY monotonicity assert on the per-game weight (d in (0,1], non-increasing in years-back) AND an AST scan of rho_out's executable code for the forbidden tokens ('qualif','floor','exclud','exclus','phase','classif','interrupt','delist').

### R024 — pedigree residual
- **register location:** units BLK0130, BLK0125 · versions item141, item136
- **ruling:** TAIL RULED — (A) KEEP 0.11 … the pedigree residual FADES, NEVER VANISHES (R98.5); the plateau holds at the T5-scale 0.11.
- **register's own status claim:** CLOSED as measured law
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Wired as the evidence-weight tail constant; no named check asserts the floor is non-zero, and the pedigree machinery has since been re-taught several times (composition act ITEM A/C).

### R025 — age
- **register location:** units BLK0117, BLK0096 · versions item128, item108 R-SAGE-FADE
- **ruling:** S_AGE DISPOSITION RULED — (a) WIRE IT … the 29-tail carries its measured value and the fade reaches zero AT 30 — the 30+ zero STANDS.
- **register's own status claim:** wired on the improver line
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Wired at the v2.10 chapter; no standing assert re-measures it.

### R026 — symmetry
- **register location:** units BLK0096 · versions item108 R-SYMMETRY
- **ruling:** R-SYMMETRY (RULED): "Risers should have the same smoothing/ramping. And you should have to have the same drop for the engine to think you're declining as a rise for it to think you're rising."
- **register's own status claim:** ruled; wired by the improver build (L-SYMMETRY)
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** L-SYMMETRY named in CONSTRAINTS and honoured in later acts (v598-era movers "symmetric by L-SYMMETRY"); no permanent assert found.

### R027 — instrument / level law
- **register location:** units SEG1730 · versions v633
- **ruling:** THE LEVEL LAW (STANDING, top tier): the LEVEL of any delivery-based ruler (price vs realized careers) IS NOT EVIDENCE and is never presented as a finding … only CONTRASTS within the same ruler are evidence; any ASYMMETRIC level change (one rung, not all) is BARRED — it manufactures the pick-hoarding arbitrage the no-arb band exists to prevent.
- **register's own status claim:** STANDING, top tier; penned into CURRENT_STATE
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Verified against recent practice: the level law is cited and applied in v634 (decision 1 shape-reading), v636 (the 1.40 act dissolved as level-law-barred) and v645+ menus. Practice conforms.

### R028 — instrument / cohort book
- **register location:** units SEG1821 · versions v642
- **ruling:** THE COHORT-BOOK LAW (STANDING, top tier): cohort progression and no-arbitrage claims are presented ONLY on the historical cohort-book instrument … NEVER on live-board cross-sections, which serve mover attribution only; any figure offered for a sizing or adoption decision NAMES ITS INSTRUMENT.
- **register's own status claim:** STANDING, top tier
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Practice conforms after the ruling (v644-v658 tables are instrument-labelled; v651 extends it).

### R029 — instrument / all-arm cohort
- **register location:** units SEG1929 · versions v651
- **ruling:** THE ALL-ARM COHORT RULING (STANDING — instrument amendment to the cohort-book law): a cohort is ALL players drafted through mechanisms eligible to debut in the same year (ND+RD+SSP year Y + MSD year Y+1); cohort progression and no-arb are presented through THAT lens.
- **register's own status claim:** STANDING; the then-canonical population (ND 1-64, n=1197) did NOT satisfy it
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** ORDER 7 re-emitted the all-arm instrument; later acts (26A/26B) use all-arm and legacy side by side and label both.

### R030 — instrument / cohort membership
- **register location:** units SEG1611 · versions v611
- **ruling:** COHORT MEMBERSHIP IS BY YEAR-1 SEASON, NOT DRAFT-CALENDAR LABEL ("The 2025 cohort is 2025 ND, 2025 RD, 2025 pathways, SSP, 2026 MSD" + "we're not balancing the ND book, we're balancing the cohort book").
- **register's own status claim:** ALL owner-facing cohort tables follow this
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Applied from v616 onward (tables re-emitted under the cohort rule); consistent with BLK0005 item 13 (the engine's own _cycle_year implements the same cohort definition, rl_model.py:60).

### R031 — valuation principle
- **register location:** units SEG1968 · versions v655
- **ruling:** THE PLAY-QUALITY PRINCIPLE (STANDING): "we don't value players on whether they play, we value them on how they play … it doesn't make sense to add value to those guys unless we have data that they *play well*."
- **register's own status claim:** standing, top tier
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Delivered at ORDER 24B: the pool premium is quality-conditioned, M=(1-phi)*R + phi*(1+q*(U''-1)) with q=clip(current avg / par(pathway,depth),0,1) — the premium pays on HOW they play (v687).

### R032 — valuation principle
- **register location:** units SEG2062, SEG2076 · versions v662
- **ruling:** THE MEAN-PRESERVING SITTER SPLIT (STANDING design principle, owner-stated): a within-group differential on an entry price already calibrated to that group's realized returns must be REDISTRIBUTION — sitter penalty offset by non-sitter bonus — never a net charge.
- **register's own status claim:** standing; binds the D8 replacement
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** ORDER 21 derived the pool sit-out retention "MEAN-PRESERVING EXACTLY" (v681); U exact ×9 at the landing (v682).

### R033 — valuation principle
- **register location:** units SEG1675 · versions v627 (5237158452)
- **ruling:** THE YEAR-4-IS-NOT-A-TARGET LAW
- **register's own status claim:** standing
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Cited and applied at v664 (D3: the full outcome profile, year 4 one data point in context) and in the composition act's no-tuning-to-a-named-year discipline; no machine check.

### R034 — pool / evidence bar
- **register location:** units SEG1620 · versions v620 (5235555305)
- **ruling:** the owner's NO-BLANKET-REWARD law (any pool fix conditions on route+position, samples named, CI bar per cell)
- **register's own status claim:** standing
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Applied throughout the pool repricing act: no cut cell named without eff-n>=35 + CI clear of 1 (v608 F3-F15); H_MATNONRD retired to 1.0 because its CI contained 1.0.

### R035 — reference layer / survivorship
- **register location:** units SEG1377, SEG1457 · versions v576 (#336), v590
- **ruling:** THE SURVIVORSHIP DEFECT (#336, owner-named, the ABLETT INVERSION) … the owner's monotonicity law filed (a strictly worse career never produces a better-looking baseline) … RULED ADOPTED (amendment-3 form) on CORRECTNESS grounds.
- **register's own status claim:** ADOPTED; shipped in the composition bake
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** par_build.py carries the #336 layer; RL_336_XW default ON (par_build.py:464) and RL_336_PARSURV/RL_336_SURVLVL=0 declared in data/model_config.json.

### R036 — counterbalance / XW
- **register location:** units SEG1987, SEG2010 · versions v657, v658
- **ruling:** THE ADOPTION WORD — "H to 1, B to flat… build/bake/push live what we've agreed on… a line in the sand"; scope CONFIRMED by direct question: (a) XW IS INCLUDED in the bake … all experiment dials (V1–V5/V9/STACK) stay OFF.
- **register's own status claim:** shipped at v658
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** par_build.py:464 XW = os.environ.get('RL_336_XW','1') != '0' (ON, "RL_336_XW=0 is now the ABLATION rather than the default"); model_config.json RL_336_XW=1, RL_B_SHAPE=0, RL_AGE_DISC=0.

### R037 — discount ladder / V5
- **register location:** units SEG1805, SEG1933, SEG2433 · versions v640, v652, v696
- **ruling:** the owner's age-dynamic discount ladder (18:12 / 19:12.5 / … / 28+:16), his own design, wired as mode 5 … NEVER RATIFIED ON — it lost the sitting to XW by the owner's own adoption word, for the measured reason that the STACK was super-additive and arbitrage (v649).
- **register's own status claim:** PARKED with no resurfacing trigger (the named disease at v696)
- **triage:** QUEUED
- **evidence / note:** rl_model.py:828-832 AGE_DISC default 0 with the V5 ladder wired as RL_AGE_DISC_MODE=5; manifest declares RL_AGE_DISC=0. Parked state is faithfully implemented. Resurfacing is the owner's open decision.

### R038 — discount rate
- **register location:** units SEG1673, SEG1655 · versions v627, v626
- **ruling:** D5 DIAL = 14 ("for now. Can always change later") — the balanced-lens rate; LENS={now:0.34, bal:0.14, fut:0.05}.
- **register's own status claim:** live
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** rl_model.py:917 LENS bal = 0.14 under RL_DIAL14 (default ON); manifest RL_DIAL14=1.

### R039 — surprise-scaled trust
- **register location:** units SEG2005, SEG1498 · versions v603, v638
- **ruling:** THE RULED FORM (owner words): "4 games of sample, especially when it is so far from the projection, should not be trusted as much" — SURPRISE-SCALED evidence trust: shrink scales with the implied re-rate size, fades with games, zero at zero surprise, symmetric, continuous.
- **register's own status claim:** ruled; landed in the composition bake at dial 4.0
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** _merged_recover.py:2107 SUR_W=float(os.environ.get('RL_SUR_W','4.0')) with the ruled endpoints; :2127 applies it inside the lam ramp; manifest RL_SUR_W=4.0.

### R040 — named tolerance  ⚑FLAG
- **register location:** units SEG1707 · versions v631
- **ruling:** THE MRAZ TOLERANCE (owner verbatim): "The mraz tolerance (up to around 2k) was not set when he had zero games. It was set when he had four. A four game player should not be quadrupling or more in value off such a small sample."
- **register's own status claim:** the seat's delta-only re-basing REVERSED; level check stands at ~3.5x ladder
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Carried as a named check in act side-by-sides (the Mraz line); no permanent assert. Register also records the tolerance later widened to 3.5-3.8x acceptable fallout (5214443366) — see the ambiguity note in FLAGS.

### R041 — valuation basis
- **register location:** units SEG2301 · versions v683
- **ruling:** THE VALUATION-BASIS REVIEW is a STANDING POST-ACT ITEM … owner: "bad/illogical ways of determining value… after this is done, we need to review all of this" — landing proceeds on the incumbent convention because BOTH arms share it.
- **register's own status claim:** STANDING POST-ACT ITEM
- **triage:** QUEUED
- **evidence / note:** The workshop is queued behind D9; realised_full remains the incumbent basis on the live board.

### R042 — rederivation design
- **register location:** units SEG2390, SEG2394 · versions v690, v691
- **ruling:** FIX THE POOL STRUCTURE BEFORE THE BROAD VALUATION ACT … every historical player's career re-valued as PRODUCTION DELIVERED FROM THE DRAFT SLOT under today's pricing rules — future seasons discounted, each season's production valued at the REAL position played that season against the REPLACEMENT BAR — then the true all-in PVC and positional v0s derived from that data by the SAME METHOD today's board prices players.
- **register's own status claim:** ORDER 26A/26B; packet delivered, NOTHING LANDED
- **triage:** QUEUED
- **evidence / note:** PR #489 open unmerged; the landing is a later order on the owner's word.

### R043 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Replacement bars via the engine's own netting path (MA.REPL − REPL_DROP; effective {MID 77.1, SD 75.3, RUCK 75.5, KPD 65.4, SF 67.9, KPF 63.8}) — never hand-copied; pinned in evidence.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R044 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Discounting via the engine's own disc_factor() at live config = FLAT 14%/yr from acquisition (age ladders exist but are OFF); mature-agers discount from actual entry age.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R045 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Production-value function: today's engine's price for an established season of average X at position P — the exact live callable identified and pinned by the build.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R046 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Truncation at last listed season; below-bar seasons credit ZERO, never negative — no longevity penalty is possible.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R047 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Two uses of position: VALUE each season at the position PLAYED that season; ATTRIBUTE the career total to the ACQUISITION slot (ND: pick · pool: pathway × day-0 signed position).
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R048 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Anchor: pick 1 = 3000, frozen ruler.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R049 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** No era normalisation (3300/game since inception).
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R050 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Three-tier window: entries <=2014 clean fit core; 2015–2021 augmented (identity-gated projected tail, tail share disclosed); 2022+ walk-forward sensitivity ONLY.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R051 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** THE IDENTITY GATE, FIRST, MANDATORY: each of the panel player's six projected outcome careers through the scorer, WQ6-weighted, must equal his live board value within ±2%. Gate failure = STOP.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R052 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Games weighting: >=10 games = full season at its average; below, w = sqrt(games/10) default.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R053 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** THE TWO-LAYER DURABLE HARVEST: Layer 1 raw facts, assumption-free, committed as a pinned first-class dataset with its builder — kept beyond the exercise. Layer 2 valuation, all knobs in one config block.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R054 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** Thin-cell borrowing (pool): own cell → shrunk toward (pathway all-in × all-pool positional lens) → thin pathway all-in shrinks toward all-pool; K-shrinkage, every borrowed cell disclosed with n and borrowing share.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R055 — 26B ruling sheet
- **register location:** units SEG2438 · versions v697 (5269952564)
- **ruling:** The positional ND curve: all-in curve by pick + SMOOTH position relativities by pick band, reconciliation law binding: position-weighted average at each pick == the all-in curve value.
- **register's own status claim:** binding on ORDER 26B; nothing lands from the order
- **triage:** QUEUED
- **evidence / note:** Delivered inside the 26B packet on branch build/delivered-value (PR #489, unmerged). Becomes LIVE-STANDING only at the landing order.

### R056 — 26B / gate object
- **register location:** units SEG2472 · versions v699 (5270492281)
- **ruling:** THE GATE-OBJECT RULING — "Core, resume": the identity gate is RULED SATISFIED AT THE PRICING CORE (bit-exact 804/804); the four adjustment legs are player-STATE machinery deferred WHOLE to the consumption-rewire act; the landing assert's ruled form: PRINTED DAY-0 == DERIVED v0 × THE DISPLAY NUMERAIRE.
- **register's own status claim:** ruled
- **triage:** QUEUED
- **evidence / note:** The landing assert is specified but not yet built (the landing is a later order).

### R057 — 26B / consumption rewire
- **register location:** units SEG2453 · versions v697 (5269905525)
- **ruling:** the derived v0 eventually replaces EVERY draft-pedigree reference in valuation — 26B lands the object, a named CONSUMPTION-REWIRE act follows site-by-site with per-site asserts (the #326 lesson).
- **register's own status claim:** confirmed in full by the owner
- **triage:** QUEUED
- **evidence / note:** Named but not commissioned.

### R058 — 26B / correction
- **register location:** units SEG2494 · versions v702 (5274640130)
- **ruling:** CORRECTION ORDER 26B-C1: apply the ruled force-majeure slide exactly as amended; Layer-1 untouched; Layer-2 scores unchanged; re-run the derivations, comparisons and both instruments; publish the CORRECTION appendix.
- **register's own status claim:** COMPLETE AND SEAT-VERIFIED
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Delivered with a three-limb deriver assert proved non-vacuous; branch tip 18336fe, nothing merged.

### R059 — positional data
- **register location:** units SEG0994 · versions v531
- **ruling:** is_key: key/non-key is the league's overlay, applied as a BLANKET rule across every FWD/DEF season of a flagged player's career — "Harrison Himmelberg excepted, who I have categorised in the sheet accordingly".
- **register's own status claim:** sealed
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Applied at the #262 positional landing.

### R060 — positional data
- **register location:** units SEG0994 · versions v531
- **ruling:** blank cells: "all training seasons have positions assigned. Any bust who doesn't feature in the training data can have that season at [the drafted position]".
- **register's own status claim:** sealed
- **triage:** ONE-TIME-COMPLETED

### R061 — vocabulary
- **register location:** units SEG0993 · versions v530
- **ruling:** the vocabulary is REPLACED with new canonical names, not merged to a variant — K-FWD→KPF, K-DEF→KPD, G-DEF→SD, G-FWD→SF, MID→MID, RUC/RUCK→RUCK — so any un-migrated site fails visibly; the rename rides WITH the data landing, one migration.
- **register's own status claim:** RULED; landed
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Store vocabulary verified: every checked row uses KPF/KPD/SD/SF/MID/RUCK (probe_named_rows.py); one_source_selftest.py:235 asserts every future_position is in the vocab.

### R062 — process / data
- **register location:** units SEG0997 · versions v534(1)
- **ruling:** STOP-AND-ASK PROTOCOL, owner words: "if there are confusing aspects or inconsistencies or potential mistakes within the sheet I submit, we should rule on them. The agent should not guess or apply judgement as it is often wrong" — on any sheet ambiguity the seat stops that item, brings the owner the rows and the question, holds for the sealed ruling; never note-and-continue.
- **register's own status claim:** sealed
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Practice conforms: #262 raised nine questions before any edit (v535); the R22 ingest HALTED on the Bailey Williams ambiguity rather than guessing (v616).

### R063 — position fields  ⚑FLAG
- **register location:** units SEG0785, SEG0796, SEG0797 · versions v502, v503
- **ruling:** THE THREE-BUCKET RULE … the standing form is an ASSERTED INVARIANT — future_position == present_position for every player UNLESS he carries a declared blend or appears on a declared-exception list — which FAILS LOUDLY the moment an edit pass moves one field without its partner. Direction sealed: "future can follow present"; a forecast NEVER rewrites the fact.
- **register's own status claim:** "WHAT SURVIVES is the GATE (v502)" (v504/v505 re-stage withdrawn, D1 landed as staged)
- **triage:** LIVE-STANDING · **verification:** NOT-REFLECTED
- **evidence / note:** No such assert exists. Searched one_source_selftest.py, ship_gates_check.py and the engine for any present_position/future_position equality check: the selftest asserts vocabulary and at-most-one-alternate only (:223-246). Measured today (probe_v502.py): 341 store rows carry present != future and NONE of them carries a declared blend; 340 are retired, 13 sit on the back board, 1 on the active board (oskar-baker MID→SF).

### R064 — store / bars
- **register location:** units SEG1006, SEG1013 · versions v539, v541
- **ruling:** Q-A ruled: eligibility feeds the year-0 bar where a 2026 row exists (dual season → the pair's lower bar per the engine's existing law), fallback chain unchanged and counted.
- **register's own status claim:** ruled; adopted at #271
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** THE LOWER-BAR LAW in SPEC v1.4; §1b current-season DPP law live under RL_FLEX=1 (manifest).

### R065 — store / bar source
- **register location:** units SEG2502 · versions #271 Addendum 4
- **ruling:** the year-0 bar source is the store's ELIGIBILITIES COLUMN — the owner-maintained current-season record; §1b/y0dpp_bar RETIRED from year 0 by supersession.
- **register's own status claim:** sealed
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **supersession:** supersedes item 275 y0dpp_bar for the year-0 source
- **evidence / note:** Store carries `eligibilities` on every checked row.

### R066 — store / games convention
- **register location:** units SEG1355 · versions #323 Addendum 4
- **ruling:** THE UNUSED-SUBSTITUTE CONVENTION: an unused-sub appearance is NOT a game played; Bell 2021 stays 8 g @ 41.7 and Rockliff 2021 stays 1 g @ 25.0.
- **register's own status claim:** sealed; the fixture re-cut executed and seam-verified
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Landed as store bytes; no standing check re-asserts the convention on future ingests.

### R067 — store / derive rule
- **register location:** units SEG1359 · versions #328
- **ruling:** the NEW DERIVE-RULE GATE (career games == sum of season rows)
- **register's own status claim:** landed with the store act
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Shipped as a gate in the store act; fails the old store, passes the corrected one.

### R068 — store / dates of birth
- **register location:** units SEG1620, SEG1632 · versions v620, v622
- **ruling:** THE BIRTHDATES … FIX READY on one owner word … OWNER WORD "Authorise the refit." — 302/302 written clean, Kirkby 1986-02-04 + Looby 1987-09-02 applied as ruled.
- **register's own status claim:** landed (store 0dd6b4a0→d9a24282)
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Store rows now carry _by (verified on sampled rows).

### R069 — store / dob
- **register location:** units SEG1079 · versions #290 D-series
- **ruling:** Kirkby/Looby RULED YEAR-ONLY (owner word; days contested across sources; engine consumes _by only)
- **register's own status claim:** ruled
- **triage:** ONE-TIME-COMPLETED

### R070 — teaching population
- **register location:** units SEG1077 · versions #290 THE BUST RULING
- **ruling:** THE BUST RULING (owner verbatim: "Pre window careers do not count… that pick was a bust"): a pick prices what it bought FROM THERE; never-scored draftees teach as zero-outcome busts at full weight at the store-referenced pick; teach-as-zero becomes RULED behavior.
- **register's own status claim:** RULED behaviour
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Carried in every derivation since (busts at zero in every denominator; the n=1,197 convention).

### R071 — store / re-entry trio
- **register location:** units BLK0002 · versions item10(a)
- **ruling:** RE-ENTRY TRIO EXCEPTION — flynn-perez · lachlan-mcandrew · mark-keane are "known exceptions" to the §45 initial-entry law: record their LATER entry (SSP 2025/2024/2022).
- **register's own status claim:** RULED 2026-07-12, EXECUTION DEFERRED; executed store-only at item 145
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Verified landed: store now carries perez SSP 2025, mcandrew SSP 2024 (_by 2000), keane SSP 2022 (probe_named_rows.py).

### R072 — training pool / MSD
- **register location:** units BLK0003 · versions item11(a)
- **ruling:** DIRECTION RULED (owner-worded): "it's quite important that MSD is treated like SSP… It's its own pool. ND players shouldn't learn from it or it from ND players in any way that the SSP pool doesn't do for itself." RULED (a) — MSD excluded from the training pool, exact SSP parity; STANDING REVIEW TRIGGER: revisit toward (b) if the refit produces football-nonsense moves.
- **register's own status claim:** ruled; executed with the trio at item 145
- **triage:** SUPERSEDED
- **supersession:** superseded in mechanism by R073
- **evidence / note:** Superseded in mechanism by THE SPLIT (v514/#217, 2026-07-28): the ND/pool separation removes rookie and pathway rows from every national fit site outright, which subsumes the MSD-only exclusion. Both stated; no winner picked.

### R073 — engine split
- **register location:** units SEG0939, SEG0912 · versions v514, v512
- **ruling:** THE OWNER'S SPECIFICATION, verbatim: "It is essential to me that this new number we are deriving is ENTIRELY from scratch… If rookies that did well now no longer tack on to the ND, they CANNOT bleed value. ND pick 64 can only be valued based on outcomes of players that were DRAFTED IN THE ND."
- **register's own status claim:** THE MOST IMPORTANT ENTRY IN THIS CYCLE; landed at #217
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** rl_model.py:282-296 the ND/RD cohort definition + pool rows excluded at all five fit sites; #217 landed with the check OBSERVING each site's actual sampled rows.

### R074 — method fence
- **register location:** units SEG0948 · versions v515
- **ruling:** "We should be looking to replicate the old system for now, so however it handled 'low sample' positions like ruck — should be replicated. It is an apples for apples replication, except it is based off the new data entirely."
- **register's own status claim:** sealed for the re-derivation era
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Scope fence for #271; discharged at the 2026-07-30 adoption.

### R075 — scope fence
- **register location:** units SEG0952 · versions v516
- **ruling:** "Right now, we are doing apples for apples conversion of the new store and ND/RD/Pool split into the current system. Anything else would be redefining HOW we model or HOW we value, which is the job of the referee project which comes next, and 412."
- **register's own status claim:** sealed; in CURRENT_STATE Part B
- **triage:** SUPERSEDED
- **supersession:** superseded by R076
- **evidence / note:** Overtaken by the later ruled sequence (composition act → root act → RL_PVCFIT re-fit → referee, v628).

### R076 — roadmap
- **register location:** units SEG1677 · versions v628 (5238084682)
- **ruling:** "I would think the referee should happen after phase 5? Keep things truly separated so this engine enters the referee in as good a state as I can leave it, and then we look to optimise." — ROADMAP OF RECORD: composition sitting → build → checks → ROOT ACT → RL_PVCFIT pick re-fit → THEN the referee project (ITEM 410, frozen v1.0) → ITEM 412.
- **register's own status claim:** ROADMAP OF RECORD
- **triage:** QUEUED
- **evidence / note:** The root act and the referee are both unstarted.

### R077 — gate / G-COHORT
- **register location:** units BLK0367, BLK0368 · versions item258, item259
- **ruling:** THE COHORT GATE IS A HEALTH BAND, NOT A CEILING … "we want year 4-6 in a healthy range relative to year 1. 1.15-1.25 ideally, 1.08-1.33 stretch." … "Keep halt at 1.3, I will consider stretching either side of the guide but it needs to be a conversation about what the benefit and tradeoff is."
- **register's own status claim:** enforced band 1.08 floor – 1.30 cap, ideal 1.15–1.25
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** acceptance twin G-COHORT two_sided_band (1.08 report / 1.15–1.25 ideal / 1.30 sole hard halt); scored every run.

### R078 — gate / G-Y0
- **register location:** units BLK0294, SEG1031 · versions item184, #271 A12
- **ruling:** G-Y0 RATIFIED BINDING — POPULATION-LEVEL CONSTRUCTION ("over the wider sample, on average") … "Accept G-Y0 as ruled" — dated exception 2.929% ruled/3.035% guard vs 2% HARD, loud HELD, do-not-exceed ceiling 3.50% = hard FAIL.
- **register's own status claim:** BINDING; the dated exception retires AT ADOPTION
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** G-Y0 asserted by key in the acceptance twin; measured 0.033-0.035% at the 2026-08-05 closure (v572), i.e. inside the 2.000% bar with the exception no longer needed.

### R079 — gate / compression
- **register location:** units BLK0183, BLK0294 · versions item183(1), R104.3
- **ruling:** "Compression Acceptance: English - 1.75-1.8x Briggs as a minimum, but can be flexible on seeing a candidate if needed." → english_briggs_priced_ratio hard floor 1.75.
- **register's own status claim:** HARD; survives every later spec fold
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** acceptance twin E/B >= 1.75 HARD (retained explicitly through SPEC v1.4, item 310).

### R080 — gate / A-PAIRS
- **register location:** units BLK0030, BLK0375, BLK0134 · versions item43, item266, item135
- **ruling:** A-PAIRS bands owner-ruled: pair 2 (Harley Reid vs Bontempelli) PARITY re-banded ±10% → ±15%; pair 3 (Ryley Sanders vs Bontempelli) Bont ahead by 0–10%; A9 (Ginnivan > Ward) PARKED as EXPECTED-FAIL-BY-LAW.
- **register's own status claim:** in the acceptance twin standing_fails with source citations
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** acceptance twin standing_fails + audit_rule ("any FAIL not listed is a NEW DEFECT; every standing fail SCORED, never skipped").

### R081 — determinism / frozen fits
- **register location:** units BLK0064, BLK0091 · versions item76, item171
- **ruling:** OWNER RULING 2026-07-14: FREEZE. "Pin a platform" is NOT a symmetric option … cm_400 is FROZEN through the season (the q97m treatment). Refits happen ONLY as NAMED, kill-switched, owner-viewed events.
- **register's own status claim:** RATIFIED ("Ratifying the freeze postures"); re-affirmed 2026-08-12 ("Happy to keep the deferral.")
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** data/q97m.pkl + data/cm_400.pkl frozen and pinned; the q97m fit path deleted with an obituary; v0surf's silent refit fallback DELETED at #217 so an unknown signature HALTs (one_source_selftest.py:735-743 asserts "no SILENT refit of the year-zero surface").

### R082 — determinism / env pin
- **register location:** units BLK0262, BLK0264 · versions item392, item393
- **ruling:** ENV PIN ISSUED — OWNER RULED PIN-FIRST: hash-pin numpy/BLAS so np.interp stops diverging cross-build and EVERY container reproduces the board of record.
- **register's own status claim:** landed; the reproduction gate is the confidence anchor
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** bootstrap.sh:18-31 — an offline fail-closed check that HALTs if the running numpy is not the pinned build (numpy 2.4.4 + the pinned libscipy_openblas .so hash); requirements-lock.txt at the repo root.

### R083 — determinism / dispatch  ⚑FLAG
- **register location:** units BLK0219, BLK0266 · versions item349, item396
- **ruling:** STANDING: every bit-exact proof, gate, audit shard, and the bake itself runs with OPENBLAS_NUM_THREADS=1 … DISPATCH PIN ISSUED — OWNER RULED A ("A please. We need to move on"): PERMANENT INFRA — the pin + runtime-verified asserts land in bootstrap for EVERY future compute.
- **register's own status claim:** later RE-SEQUENCED to pre-go-live/post-bake (item ~400), owner authorization pending
- **triage:** QUEUED
- **evidence / note:** Partial today: OPENBLAS_NUM_THREADS=1 is set in live-scoring.yml, live-scoring-proofs.yml, tools/round_entry/weekly_update.sh and the ingestion apply paths — but NOT in ci-guards.yml or final-integration.yml, and the dispatch pin (NPY_DISABLE_CPU_FEATURES / OPENBLAS_CORETYPE) appears nowhere in bootstrap.sh or any workflow. Recorded as QUEUED because the register shows a deliberate owner-facing re-sequencing, not a silent drop.

### R084 — gate / G-COHORT basis
- **register location:** units BLK0014, BLK0026 · versions item52 (B1), item38
- **ruling:** THE B1 CONFORMANCE — "July 8 is correct — it's literally just the aggregated numbers on the walk-forward book. The average year-4 value. There's no need to rescale each class to 100."
- **register's own status claim:** THE JULY-8 CONSTRUCTION IS THE GATE; code conformed
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** cohort_gate_official.py deleted with an obituary; the frozen suite computes the July-8 construction; the indexed reading demoted to a labelled non-gating shape diagnostic.

### R085 — gate / release contract
- **register location:** units SEG0989 · versions v526
- **ruling:** Ruling 1, owner words: "For #1 I think the second makes sense" — the release-contract gate is to distinguish a DECLARED deliberately-held candidate from genuine drift; an undeclared mismatch still HALTs, proven able to fail both directions. Ruling 2: "agree on the proof jobs" — the six proof-* jobs come off every-push to a manual trigger.
- **register's own status claim:** landed at #251
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** release_contract.py + held_candidates declarations; .github/workflows/live-scoring-proofs.yml is manual-trigger.

### R086 — owner overrides
- **register location:** units BLK0014 · versions item24 / S1 findings
- **ruling:** FIX SET: (1) owner_overrides resolution HALTS (never []) when the file cannot be found in any non-dev mode; (2) a PRESENCE ASSERTION — every key listed in owner_overrides.json must carry its `ov` block on the exported board, else HALT; (4) RL_NO_OWNER_OVERRIDES out of INFRA_ALLOW for gate/bake modes.
- **register's own status claim:** folded into the bake build
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** engine/rl_after/owner_overrides.py:41-62 (HALT when the file is absent in a non-dev mode); rl_export.py:640 the POST-EXPORT PRESENCE ASSERTION. Verified live: will-brodie carries ov{factor 0.5, dispv 386, mark "OWNER OVERRIDE ×0.50"} on data/rl_build/rl_app_data.json against v=773.

### R087 — owner overrides doctrine
- **register location:** units BLK0157 · versions item167
- **ruling:** THE OVERRIDE DOCTRINE (owner verbatim): "On Gawn and Bontempelli I won't be providing an override because the reason they should be worth more is perceptible and visible in the stats available to us. The Will Brodie override was an exception where I had information the stats did not." ⇒ OWNER OVERRIDES = extra-statistical information ONLY.
- **register's own status claim:** DOCTRINE
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** data/owner_overrides.json carries exactly ONE row (will-brodie), with the arbitrary-by-acknowledgement provenance recorded in the file. No override has been added since.

### R088 — owner overrides / O1  ⚑FLAG
- **register location:** units SEG2281 · versions v682
- **ruling:** O1 OFF FOR THE POOL OBJECT ("My July override no longer stands. I trust that the data is correct so therefore my judgement is based on feelings, not fact… I should accept that, I think.")
- **register's own status claim:** as-built FINAL was already O1-OFF; the ND-side KPP floor question QUEUED
- **triage:** LIVE-STANDING · **verification:** AMBIGUOUS-OR-CONFLICTING
- **evidence / note:** The pool half is delivered. The register itself states the same ruling's reach into the NATIONAL surface's wired KPP floor "MOVES ND PRICES so it cannot ride this act (separation law) and is queued" — so an owner ruling of general form sits half-applied by design, with the other half unqueued to any named act.

### R089 — UI / movers
- **register location:** units SEG0908 · versions v510
- **ruling:** THE MOVERS TAB BECOMES A FROM/TO COMPARISON — two dropdowns over stored points … the board-identity chain, its integrity flag and the provenance bridge are REMOVED rather than loosened. ONE ASSERT REPLACES THE FIVE DELETED CHECKS: the newest stored column matches the live board.
- **register's own status claim:** landed at #208
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** ui/data/movers.js + the single newest-column assert.

### R090 — records
- **register location:** units SEG1034, SEG1035 · versions #271 A15, A16
- **ruling:** historical per-round reports are NEVER rewritten — each keeps its frozen era identity … AMENDED: out-of-round columns ARE model-change boundaries by round_movers' own design.
- **register's own status claim:** ruled; amended by owner word + owner-supplied precedent
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The out-of-round column registry (label owner-set verbatim); every landing since registers its own column.

### R091 — UI / Best-23
- **register location:** units BLK0288, SEG1040 · versions item178(3), #271 A19
- **ruling:** Best-23 = the value-maximal 23 fillable from the ELIGIBILITIES column, DPP-optimised, on ABSOLUTE BOARD VALUE (metric owner-corrected from "projected points"); "count honestly" REJECTED as displaying false information.
- **register's own status claim:** the ruled selector landed as #274's first item
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** A19 selector live (min-cost max-flow over ELIGIBILITIES, parity 17/17 at the landing); the backfill stopgap was declared-not-law and removed at #274.

### R092 — FHV
- **register location:** units SEG1043 · versions #270 FHV
- **ruling:** FHV DEFINITIONAL RULING (#270): Option A — expectation view, single constant ≈190; survivor-conditioned 250/528 REJECTED; per-window schedule = the one-word upgrade path.
- **register's own status claim:** first consumer #276's phantom; FHV=190 at render
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Landed in the #274 UI wave (over-free lens FHV=190 at render). No standing assert pins the constant.

### R093 — pick discounts
- **register location:** units BLK0183 · versions item183(3) / R104.5
- **ruling:** "2027 Pick Discount: 10% at balanced, 15% at contender, 5% at rebuilder." — the owner's OWN construction.
- **register's own status claim:** ruled; wired
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The posture triple 0.10/0.15/0.05 verified exact by the independent audit shard (BLK0242).

### R094 — posture lenses
- **register location:** units BLK0183, BLK0292 · versions item183(2), item182
- **ruling:** "Posture Presets - adopt sketch, agree balanced stays canonical." — balanced = canonical and the ONLY board that gates/bakes/seals.
- **register's own status claim:** ruled
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Leg E postures over the D5 dial family; the balanced board alone gates/bakes (RL_LEGE/RL_LEGF declared in the manifest).

### R095 — forward lens
- **register location:** units SEG0149, SEG0234 · versions v422, v443
- **ruling:** FORWARD-LENS RULING (owner words): "The projection view should always match the live/current board… the next time round scores go in after round 20, it should update." … "In a published working engine, the projection should match. So when new scores are added, the projection should follow. While we are working on it and overhauling it, there is obviously flexibility."
- **register's own status claim:** ratified with a BINDING EXPIRY at the next round advance
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The advance-repin sibling machinery (sibling_repin.py) regenerates the forward view inside the same atomic round transaction; the D2 merge discharged the deferral before R20.

### R096 — picks on the board
- **register location:** units BLK0005 · versions item12/13
- **ruling:** "picks are tradeable for the trade desk but should not be on the current board for ranking players. That is just a player ranking. It enters the future lens to represent the player it will become."
- **register's own status claim:** ASSUMPTION CONFIRMED
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The shipped board carries picks in separate arrays (lensPicks / phantomPicks), never in `active` (data/rl_build/rl_app_data.json).

### R097 — UI / design standard
- **register location:** units SEG1708, SEG1709 · versions v632
- **ruling:** "I'd love it if the interface looked like it'd been designed by the best UI designers and web developers in the world. Not like AI… every part of the information presentation… care and consideration" + THE BLINDNESS PROTOCOL (his own invention): a blind seat reviews the rendered app only.
- **register's own status claim:** both reviews landed; the mockup pick is PARKED on his word
- **triage:** QUEUED
- **evidence / note:** Recorded repeatedly in the register tail as "the mockup pick (parked)".

### R098 — process / status vocabulary
- **register location:** units SEG1767 · versions v637
- **ruling:** THE LIVE LAW (STANDING, top tier): ONE WORD — LIVE — meaning THE BYTES ARE ON MAIN IN THE ENGINE THAT BUILDS THE SHIPPED BOARD; every other status word is merely a ruling waiting to become live; NO AGENT REPORTS A RULING AS DONE unless it is LIVE with the implementing main-line site citable. THE RULED-BUT-NOT-LIVE LEDGER: every owner ruling that should change engine behaviour ENTERS the ledger when made and LEAVES only on a citable main-line implementation.
- **register's own status claim:** STANDING, top tier; ledger in CURRENT_STATE Part B
- **triage:** PROCESS-LAW · **verification:** ENFORCED
- **evidence / note:** docs/CURRENT_STATE.md:156 carries "THE RULED-BUT-NOT-LIVE LEDGER (standing; read at every pen and every sitting…)". The mechanism exists and is maintained.

### R099 — process / rulings-become-asserts
- **register location:** units SEG2430 · versions v695
- **ruling:** PROPOSED STANDING LAW (awaiting owner ratification): EVERY RULING LANDS WITH A NAMED PERMANENT ASSERT — the ruled behavior as a boot/build-time check on the actual board (the engine's own _v0_curve_assert is the model); an under-delivering landing or a later regression FAILS THE BUILD.
- **register's own status claim:** PROPOSED, awaiting the owner's formal yes
- **triage:** QUEUED
- **evidence / note:** One of the two "standing yes/nos" still open. First application already shipped in 26B-C1 (the three-limb deriver assert), so the pattern is proven; the law itself is unratified.

### R100 — process / open-decisions ledger  ⚑FLAG
- **register location:** units SEG2433 · versions v696
- **ruling:** PROPOSED FIX (second mechanism): AN OWNER-FACING OPEN-DECISIONS LEDGER — docs/OPEN_DECISIONS.md, one page, maintained by the pen: every parked owner decision, its measured menu, its blocking reason, and its resurfacing trigger; refreshed and RESTATED TO THE OWNER at every landing.
- **register's own status claim:** PROPOSED; V5 named as its first entry
- **triage:** QUEUED
- **evidence / note:** docs/OPEN_DECISIONS.md does not exist in the tree (checked). The parked items it would hold are currently held only in this register.

### R101 — process / directive review
- **register location:** units SEG2042 · versions v660 (5250590276)
- **ruling:** THE DIRECTIVE REVIEW RULE (STANDING): "For this one, I would like to review the directive before it is sent. The layer between you and subagents bypassing me has meant some errors have not been noticed before the damage is done." — DIRECTIVE DRAFTS ARE DELIVERED TO THE OWNER FOR REVIEW BEFORE THEY ARE TREATED AS ISSUED; the owner reads the DOCUMENT ITSELF, not a summary.
- **register's own status claim:** STANDING
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** First full pass completed at v662 (draft → owner read the document → four amendments → folded → issued). Practice conforms on the pool directive. Not evidenced for every later act.

### R102 — process / subagent visibility
- **register location:** units SEG1573 · versions v614 (5235093657)
- **ruling:** SUBAGENT VISIBILITY LAYER — every agent brief is POSTED ON #334 BEFORE LAUNCH; every agent appends one-line timestamped checkpoints to a progress file; the seat RELAYS checkpoints to the owner; the owner can say stop at any time; agents are read-only, findings return to the seat, the seat files them verbatim before interpretation.
- **register's own status claim:** NEW STANDING RULES
- **triage:** PROCESS-LAW · **verification:** ENFORCED
- **evidence / note:** Verified against #334: ORDER briefs 26A/26B/27 are all pre-posted before launch (comments 5269252799, 5269952564, 5274888553). This sweep's own brief is an instance.

### R103 — process / language
- **register location:** units SEG1571 · versions v612 (5235043061)
- **ruling:** ALL SEAT REPLIES TO THE OWNER USE ASD-STE100 SIMPLIFIED TECHNICAL ENGLISH from now on (cause: "so verbose and circular").
- **register's own status claim:** RULING
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Not verifiable from the repo; the register's own entries remain dense prose, which is a different surface from seat replies.

### R104 — process / language
- **register location:** units SEG1730 · versions v633
- **ruling:** PLAIN-LANGUAGE-UPFRONT LAW: every owner-facing explanation leads with problem/why/trade-off/options in plain terms — never simplification on request (third reminder = the ruling).
- **register's own status claim:** STANDING
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R105 — process / model allocation
- **register location:** units SEG1573 · versions v614
- **ruling:** Opus agents do ALL work not strictly necessary for Fable (reinforces the Opus-only subagent law; Fable = judgment/filings/verification only).
- **register's own status claim:** NEW STANDING RULES
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R106 — process / subagents
- **register location:** units SEG1074 · versions #290 SUBAGENT BOUNDARY LAW
- **ruling:** SUBAGENT BOUNDARY LAW (owner-endorsed): if it MEASURES the seam/seat may parallelize it with Opus subagents; if it WRITES it is a seat with an owner word; one writer per bake; no parallel engine builds; every subagent conclusion re-verified by re-run before it enters the record.
- **register's own status claim:** recorded
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Practice conforms in the recent record (read-only sweeps run in parallel; landings are single-writer).

### R107 — process / CI
- **register location:** units SEG0010, SEG0021 · versions v382, v384
- **ruling:** standing rule: CI may RUN and REPORT, CI NEVER COMMITS; registered workflows change only as deliberate reviewed work … role-exclusive carve-outs: no seat attests an owner word; no seat reviews its own operation; one pen on the durable list; seats sign as what they are.
- **register's own status claim:** standing
- **triage:** PROCESS-LAW · **verification:** ENFORCED
- **evidence / note:** No workflow in .github/workflows commits to the repo (checked: the five workflows run and report).

### R108 — process / attribution
- **register location:** units SEG0711, SEG0712 · versions v495
- **ruling:** A RULING'S CHANNEL IS NOT ITS AUTHOR — a seam ruling relayed by the owner remains a seam ruling and cites its register version; "owner word" is reserved for the owner's OWN decision, quoted or paraphrased with its channel and date.
- **register's own status claim:** NORM ADDED; restated with force at v506
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Later entries consistently label seam rulings vs owner words and cite comment ids.

### R109 — process / directives
- **register location:** units SEG0973 · versions v517
- **ruling:** DIRECTIVES NOW QUOTE THE OWNER VERBATIM AND STATE ACCEPTANCE AS A PROPERTY OF THE RESULT, PROVEN ABLE TO FAIL. A wrong edit can satisfy a line list; it cannot satisfy an outcome test.
- **register's own status claim:** STRUCTURAL FIX
- **triage:** PROCESS-LAW · **verification:** ENFORCED
- **evidence / note:** Verified in the directives on main: docs/directives/POOL_REPRICING_DIRECTIVE_2026-08-11.md and COMPOSITION_DIRECTIVE_2026-08-10.md both open with owner words verbatim and property-shaped acceptance.

### R110 — process / governing test
- **register location:** units SEG0889 · versions v508
- **ruling:** THE OWNER'S GOVERNING TEST, SEALED AND OVERRIDING: IS THIS A REASONABLE CHANCE OF STOPPING THE PROJECT FROM WORKING — not "can this be fixed". If it cannot plausibly stop the thing working it gets ONE LINE in the register and nothing else.
- **register's own status claim:** SEALED AND OVERRIDING
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Cited as the governing test in later dispositions (e.g. the movers directive pre-fire audit waiver, v510).

### R111 — process / evidence
- **register location:** units SEG1075 · versions v546 (N12)
- **ruling:** NEW STANDING RULE: A SEALED RECORD MAY ONLY CITE CONTENT REACHABLE FROM MAIN — evidence lands before or with the seal that cites it; no branch delete until the seam confirms nothing sealed-cited lives only there.
- **register's own status claim:** STANDING RULE
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Honoured in the recent record (evidence trees committed to main before the pens that cite them).

### R112 — process / retention
- **register location:** units SEG1058, SEG1065 · versions v543, v544
- **ruling:** NEW STANDING CONSTRAINT: nothing an OUTSTANDING OWNER READ depends on is deleted … "Do not delete anything I need for the referee read".
- **register's own status claim:** standing
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** docs/evidence trees are retention-protected and still present.

### R113 — process / seam economy
- **register location:** units SEG1086 · versions v547
- **ruling:** NEW SEAT LAW: THE SEAM VERIFIES DECIDING FIGURES; IT DOES NOT INGEST BULK — uploads, artifact dumps and row-level validation go to subagents returning verdicts + the deciding numbers for seam re-check.
- **register's own status claim:** owner-directed at rotation
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R114 — process / cost
- **register location:** units SEG1673 · versions v627 (5237381767)
- **ruling:** "machine time is my time" — governing-test accounting corrected; separate workspaces for parallel builds; deterministic lane only where it guards main; further speed/verification trades = owner's call.
- **register's own status claim:** owner words filed
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R115 — process / cost estimate
- **register location:** units SEG1047 · versions v541
- **ruling:** THE COST-ESTIMATE NORM — any request whose answer requires building artifacts that don't exist gets an explicit estimate + owner go-ahead BEFORE commissioning; general authorization is not specific authorization.
- **register's own status claim:** SEAT LAW, owner-endorsed
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R116 — process / estimates
- **register location:** units BLK0188, BLK0198 · versions item188
- **ruling:** every directive carries a CONCRETE wall-clock TIME ESTIMATE — a number band, as accurate as the supervisor can make it; "one session" is NOT an estimate.
- **register's own status claim:** STANDING RULE
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R117 — process / review lanes
- **register location:** units SEG1054, SEG1058 · versions v543
- **ruling:** OWNER WORD ON REVIEW LANES: Opus-subagent cold-screens of seam work standing-approved, and the seam MAY review its own work when the owner asks for a double-check; the implementer≠reviewer taint still governs seat work products and cold reviews.
- **register's own status claim:** carried in Part B seat law
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R118 — process / cold review
- **register location:** units SEG0331, SEG0473 · versions v459, v474
- **ruling:** a BASIC COLD REVIEW BEFORE THE VIEWING … one fresh bare cold seat, filed artifacts only, implementer ≠ reviewer ≠ supervisor; the landing word remains a SECOND owner word after the viewing.
- **register's own status claim:** ruled; discharged
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** The pattern recurs in every later act (pre-fire audit by a non-authoring session, e.g. v595).

### R119 — process / pen authority
- **register location:** units SEG0564, SEG0567 · versions v483
- **ruling:** PEN LANDING AUTHORITY RIGHTSIZED — OWNER WORD ("register pens should land without a per entry word") … CARVE-OUTS THAT SURVIVE: any write outside docs/; LAW-10 ACTS; RECORDING AN OWNER WORD; DIRECTIVES FIRING; LANDING TRANSACTIONS; tags, releases, score-arm and live pin movement. REVERSAL CONDITION, self-executing: any pen error reaching main RESTORES the per-entry word.
- **register's own status claim:** standing authority with a self-executing reversal
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R120 — process / delivery
- **register location:** units SEG1701, SEG1631 · versions v629, v623
- **ruling:** standing practice reaffirmed: the complete answer in the FINAL message, never mid-tool-chain (LONG ANSWERS GO BEFORE ANY TOOL WORK).
- **register's own status claim:** new seat law after two occurrences
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R121 — process / PRs
- **register location:** units SEG2244 · versions v677
- **ruling:** standing instruction added to every brief: even chores go via PR (after a commit reached main outside the PR flow, owned as a LAW BREACH).
- **register's own status claim:** standing instruction
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R122 — process / rotation
- **register location:** units SEG0126, SEG1092 · versions v415, v548
- **ruling:** STANDING ROTATION NORM: every seat self-reports context depth and recommends its own rotation at the next clean boundary; rotations are owner-initiated and err-toward-rotating governs. C3 ROTATION VIGILANCE: the seam raises its own rotation at ~500k clean boundaries.
- **register's own status claim:** standing; the 730k rotation is the recorded anti-pattern
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R123 — process / non-vacuity
- **register location:** units SEG0378, SEG0669 · versions v465, v492
- **ruling:** NON-VACUITY IS A STANDING REQUIREMENT of every assertion this house adds — a rejected input must raise and a valid one must pass; an unfalsifiable guard shipped to close a trust gap is the same defect in a new coat.
- **register's own status claim:** standing
- **triage:** PROCESS-LAW · **verification:** ENFORCED
- **evidence / note:** Practised in the recent record: the 26B-C1 deriver assert was "proved non-vacuous"; the ORDER 20B gates were shown capable of failing on the RL_V0_LENS=0 lane.

### R124 — process / hazard class
- **register location:** units SEG0646 · versions v490
- **ruling:** RULING — TRANSPORT AS A FILE, NEVER AS PASTED TEXT … NEW HAZARD CLASS NAMED: THE LOAD-BEARING INVISIBLE CHARACTER.
- **register's own status claim:** ruling + named hazard class
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R125 — process / identity
- **register location:** units SEG0829, BLK0378 · versions v505, item269
- **ruling:** STANDING RULE: identity resolution is by STABLE ID against the 804-scope ONLY; name-matching over the 2,652-row store is FORBIDDEN as an identity instrument. AN IDENTITY IS RESOLVED BY KEY, NEVER BY SUBSTRING.
- **register's own status claim:** STANDING RULE
- **triage:** PROCESS-LAW · **verification:** ENFORCED
- **evidence / note:** engine/rl_after/collision_sentry.json + the id_resolver key-join discipline; the F5 name-twins finding (v543) records join-by-key as the reason a count was right.

### R126 — round entry
- **register location:** units BLK0175, BLK0186 · versions item305, item311
- **ruling:** THE LAW, RESTATED: the tool exact-matches name→active-stable-ID at run time; any export name that does not cleanly resolve is a FLAGGED RESIDUE LINE for a one-tap owner confirm — NEVER a silent drop, NEVER attached to the wrong row, NEVER a new-row invention.
- **register's own status claim:** the item-305 frame carried verbatim as THE LAW
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** tools/round_entry + engine/rl_after/id_resolver.py; demonstrated live at the R22 ingest, which HALTED on the Bailey Williams ambiguity rather than guessing (v616).

### R127 — season dial
- **register location:** units BLK0167 · versions item297
- **ruling:** SEASON_PROG stays 0.58 through the v2.11 chapter; TRIGGER: post-bake, owner enters rounds and advances the dial himself (an owner dial, never a build's).
- **register's own status claim:** owner dial
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** data/season_state.json + the SEASON_PROG owner dial declared in the manifest; the R21/R22 applies advanced it by owner act.

### R128 — ingestion
- **register location:** units SEG0281, BLK0218 · versions v453, GO_LIVE
- **ruling:** live weekly ingestion remains the owner's deliberate FINAL SWITCH (his 2026-07-12 word: "I want adding weekly scores to be the last thing we start doing… But building provision for it can be now.").
- **register's own status claim:** provision built and merged; the switch is the owner's
- **triage:** SUPERSEDED
- **supersession:** overtaken by the go-live acts
- **evidence / note:** Superseded by events: the go-live store-write was subsequently built and the weekly lane is live (R20/R21/R22 applies landed). Recorded so no seat re-reads the old fence as current.

### R129 — parked work
- **register location:** units SEG0891 · versions v508
- **ruling:** PARKED BY OWNER RULING, do not start: Track D (five items, ALL in test harnesses), the conservation gate, the CI parallelisation, and further work on the state doc.
- **register's own status claim:** PARKED BY OWNER RULING
- **triage:** QUEUED
- **evidence / note:** Still parked; nothing in the recent record restarts them.

### R130 — parked work  ⚑FLAG
- **register location:** units SEG1633 · versions v623 (5235988984)
- **ruling:** "I am happy to park the rulings ledger for now." → 1.3 PARKED on his word (no deadline, on the parked list).
- **register's own status claim:** PARKED
- **triage:** QUEUED
- **evidence / note:** The owner's own law book LUKE_RULINGS_LEDGER.md (source of R12 and the R-numbered rulings) currently lives at docs/archive/pre-mvp-2026-07/process/LUKE_RULINGS_LEDGER.md — an archive path — while its laws are cited as binding (R12 at v613). Flagged at v623 ("the law book lives in a folder called archive"); parked by owner word.

### R131 — fade speed
- **register location:** units SEG2190, SEG2234 · versions v672, v676
- **ruling:** D9 RULED — FADE SPEED DEFERRED: the pool prior fades exactly as the ND prior does; the fade-speed question goes to its own act because the machinery is SHARED, so one later repair fixes both arms. THE PEDIGREE DEAD ZONE AND THE PRORATION ASYMMETRY TRAVEL WITH THE DEFERRAL.
- **register's own status claim:** ruled; the parked act
- **triage:** QUEUED
- **evidence / note:** Named as the next act after the pool landing, with ramm/liddy/visentini pre-registered as test names.

### R132 — defect candidate
- **register location:** units SEG2172 · versions v671
- **ruling:** NO RULING PAIRS THE TWO BARS — an unpaired asymmetry between mechanisms written at different times is a DEFECT CANDIDATE for the pre-adoption list, not a design (the pedigree bar reads raw games, LAM_SIT reads games AT PACE).
- **register's own status claim:** defect candidate; travels with the D9 deferral
- **triage:** QUEUED
- **evidence / note:** Neither measured for sign nor size.

### R133 — year-zero design
- **register location:** units SEG1252, SEG1258 · versions v561, v562
- **ruling:** OWNER LAWS, verbatim, standing law on every future seat: (LAW-INTERSECTIONS) the year-zero surface is a TRUE position × age × pick surface — per position/age the data draws a line along the pick axis, below the curve where the data says below, above where it says above, CROSSING FREELY; a position dial constant across picks is BARRED.
- **register's own status claim:** standing law on every future seat
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Honoured by the L-A lens construction (v565/v566) and re-verified at v585 ("LAW-INTERSECTIONS honoured (the one thing #306 got right)").

### R134 — year-zero design  ⚑FLAG
- **register location:** units SEG1583 · versions v613-era audit
- **ruling:** LAW-NO-HARD-BANDS: year-0 fit band-free
- **register's own status claim:** the year-0 fit is band-free BUT the production path still pools the seed-era hard band grid (rl_model.py bandof/MIX/BUST_BAND/basepk — long-standing, now NAMED)
- **triage:** LIVE-STANDING · **verification:** AMBIGUOUS-OR-CONFLICTING
- **evidence / note:** The register itself records the law satisfied on one path and breached on another, with the breach "long-standing, now NAMED" and no act commissioned to close it. Both readings stated; this seat picks no winner.

### R135 — year-zero design
- **register location:** units SEG1253 · versions v561 (N36)
- **ruling:** N36 THE OWNER'S DESIGN STEER (verbatim): year-zero = true worth at the draft moment; data-driven per-cell boosts/cuts; mature-age via the age cell; the average still equals the pick curve with POPULATION-WEIGHTED offsetting.
- **register's own status claim:** the steer extends N29 and changes no design line
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The N41 acceptance solves lam(pick) on the applied population's anchor-weighted composition — the population-weighted offsetting the steer requires.

### R136 — year-zero acceptance
- **register location:** units SEG1296 · versions v566 (N41)
- **ruling:** N41 RULING (owner word "Agree on acceptance test"): lam(pick) solves on the APPLIED population's anchor-weighted composition — the applied rows enter as COMPOSITION WEIGHTS ONLY; tolerance 0.005, B=2.00; still-failing => HALT, never iterate.
- **register's own status claim:** amends the approved design BY ADDENDUM on the constraint population only
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Implemented and accepted on the artifact (v566).

### R137 — determinism / fit path
- **register location:** units SEG1234, SEG1243 · versions v560 (N35)
- **ruling:** RULING N35 (THE FIT-PATH ASSERT): before ANY measurement act of this job, the box must reproduce the record's fit; FAIL -> no measurement act on that box; the assert goes STALE on any observed host migration or restart. A BOX IS CLASSIFIED BY OUTPUT BYTES, NEVER BY LABEL.
- **register's own status claim:** seam word, owner-reversible
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Practised repeatedly in the record ("Fifth same-day seam box re-classification preceded the figures").

### R138 — design / basis-as-inputs
- **register location:** units SEG1295 · versions v565 (N40a)
- **ruling:** IMPLEMENT, with BASIS-AS-INPUTS — the owner's live-and-breathe steer verbatim ("One change to one piece should [NOT] require an entire redesign and rebake. It should live and breathe") — the engine lens fit consumes the structural-values file and the anchor ladder as DECLARED INPUTS so bar changes propagate by re-run + re-pin, never code surgery.
- **register's own status claim:** ruled
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** THE RULED PATH STANDS (N40a) restated at v571: propagation by DELIBERATE RE-RUN + RE-PIN, never code surgery, never routing around an identity check.

### R139 — recipe / brandless
- **register location:** units SEG1349 · versions v571 (N45)
- **ruling:** N45 — THE RECIPE AUDIT: audit the CURRENT RUNNING CODE into a plain-English RECIPE … THE RECIPE IS BRANDLESS … THE FAILURE TEST, owner verbatim: "If our valuation and projection can't be done as a recipe, then we have already failed" — every unstatable item is a NAMED FINDING.
- **register's own status claim:** ordered; delivered as the #322 recipe
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Delivered and re-cut for Track B (v580).

### R140 — track B
- **register location:** units SEG1402 · versions v580
- **ruling:** TRACK B RE-CUT SIMPLE (owner word, superseding the v579 pack): "I don't want this track B new project to… be doomed before beginning by rules, regulations, laws, policies… This should be simple." … later clarified: "the simplicity was more about removing the layers of process… and have things update quickly" — the discipline is PROCESS-light, not model-simple.
- **register's own status claim:** delivered; the clarification recorded so v580 is never misread
- **triage:** ONE-TIME-COMPLETED
- **supersession:** clarified by the v596 owner words

### R141 — track B
- **register location:** units SEG1355 · versions #322 (5188203865)
- **ruling:** THE FROZEN MODELS WITHHELD from the blind-build package (owner word) — the builder fits its own models from the recipe alone, judged by OUTPUTS ONLY.
- **register's own status claim:** owner word
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The v580 two-file pack ships the store + the recipe only.

### R142 — process / vocabulary
- **register location:** units SEG1355 · versions #324 / plain vocabulary
- **ruling:** the standing rule that ALL NEW text uses plain words (after model content-filter false positives repeatedly blocked seat chats on the project's old metaphor vocabulary); identifiers, file names, the register and all evidence untouched.
- **register's own status claim:** owner-approved and landed (PR #324)
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R143 — anchors / Kako
- **register location:** units SEG0303, SEG1423 · versions v456, v583
- **ruling:** the Kako anchor: on the owner's word a seat types the round reading into KAKO_ANCHORS … RETIRED at R21 — the owner confirmed the store's R21 reading and retired rather than re-wind a clock that breaks every round; the 2025 completed-season anchor and the scope mechanism stand; SELFTEST EXPECTATION IS NOW 144 PASS / 0 FAIL.
- **register's own status claim:** retired by owner word
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Recorded so no seat reads a standing "145/0" note as current.

### R144 — overrides / catchup
- **register location:** units SEG1420, SEG0926 · versions v582, v512
- **ruling:** THE BAILEY WILLIAMS OVERRIDE IS ROUND-SCOPED TO R15–R19, NOT DELETED, via a new applies_to_rounds field and a scope check; the two players are disambiguated by owner word (West Coast 91→wc, Bulldogs 79→wb).
- **register's own status claim:** scoped rather than retired; seam-endorsed
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Store carries bailey-williams-wc (and the wb counterpart) as distinct keys; catchup_identity_overrides.json carries the round scope. Watch item recorded at v619: the R22 export REGRESSED the disambiguation.

### R145 — ownership sidecar
- **register location:** units SEG1049, SEG0969 · versions v542, v513
- **ruling:** ownership single-source directive (owner ruling: store=truth, sidecar=generated mirror, oracle unchanged) … TWO LANES: LIVE = AFFL ownership + pick holdings (an edit with no build, no bake, no board move); BATCHED = positions, which feed valuation. Positions must NEVER ride the live lane.
- **register's own status claim:** owner ruling; landed at #283
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** ui/data/ownership.js is a generated mirror; affl_team verified absent from the valuation path (v513 basis).

### R146 — store identity
- **register location:** units BLK0011 · versions item20(c)/(e)
- **ruling:** "rename club to draft club and keep. It might come in handy some time. Just don't want to cross wire it ever." + THE CSV ARCHIVE RULE: at import, stamp the CSV and move it to docs/inputs/archive/; the store becomes the SOLE carrier of every club, ID and eligibility.
- **register's own status claim:** ruled
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Store carries affl_team; docs/inputs holds the owner input files. No standing check asserts the archive/stamp step on a future import.

### R147 — conservation basis
- **register location:** units SEG1516, SEG1522 · versions v606
- **ruling:** CONSERVATION BASIS RULED: owner-facing cohort tables lead with the FULL COHORT (ND 1-64 + pool, classes 2004-2025 at reached years) — re-affirming his own #333 unified basis the stage tables had drifted from.
- **register's own status claim:** ruled
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Later reinforced by the cohort-book law (R028) and the all-arm ruling (R029).

### R148 — no-arb target
- **register location:** units SEG1475 · versions v594 (5210304078)
- **ruling:** "Let's go for 1.4. But I don't necessarily think it should be rigged to be 4 even steps. And it needs to be flexible - 2020 was a shocking draft. So their players should not be 'rigged' to improve by 40% to year 5 either."
- **register's own status claim:** THREE CLAUSES BOUND INTO STAGE B
- **triage:** SUPERSEDED
- **supersession:** dissolved into the root act (v638/v639)
- **evidence / note:** The 1.40 re-anchor act was DISSOLVED INTO THE ROOT ACT by owner word at v638/v639 (barred standalone by the YEAR-4 and LEVEL laws); the evidence rides the root act. The target itself is not withdrawn — it awaits the root act.

### R149 — no-arb / relocation
- **register location:** units SEG1506 · versions v604 (5213743952)
- **ruling:** THE RULING (owner verbatim): the 1.432 band-pass with yr1-to-peak risen 1.400→1.5068 is "a loophole to tick success… Year 1 players being worth less than their picks does not make sense" — the relocation reversal condition FIRED and the owner UPHELD it.
- **register's own status claim:** trigger (b) upheld; the act's shape rejected
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** The reversal condition is a named return-trigger in act directives; no permanent assert prevents a future act passing a band while relocating the shortfall.

### R150 — relativity guard
- **register location:** units SEG1804, SEG1734 · versions v640, v634
- **ruling:** THE RELATIVITY GUARD as a NEW HARD GATE: the side-by-side prints the book by career rung — (picks + year-0 + year-1) vs the peak-year rungs — before/after as ONE ratio, identically computed on both boards; ANY material movement against youth = TOP-OF-REPORT flag before adoption, never silently rebalanced.
- **register's own status claim:** ruled; FIRED at v640 and honoured
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** It fired as designed on the composition package (−4.90% against youth, flagged top-of-report, and the owner ruled the counterbalance). It is an act-level deliverable, not a committed check.

### R151 — counterbalance
- **register location:** units SEG1805 · versions v640 (5246868843)
- **ruling:** "I don't think we should pull it out. I think we should simply find the right way to factor into younger players the players they become as a cohort in year 4-5 so the ramp isn't as steep. Potentially starting by declining future seasons of 18-21 year olds at 13% and 26+ at 15%?"
- **register's own status claim:** #336 STAYS; the counterbalance = his age-dynamic discount PULLED FORWARD
- **triage:** SUPERSEDED
- **supersession:** the counterbalance choice superseded by v657
- **evidence / note:** The counterbalance chosen at the sitting was XW, not the discount (v652/v657); the discount reverted to parked (see R037). Both stated.

### R152 — grievance / goal  ⚑FLAG
- **register location:** units SEG2385, SEG2390 · versions v689, v690
- **ruling:** "pool prices are never higher than the day they are drafted. This makes no sense? You'd just sell them, there's no reason to ever hold… Neither have been meaningfully corrected, and a 5-10% movement when they were 2x too low is not progress." → FIX THIS BEFORE #2.
- **register's own status claim:** THE LANDING WORD WITHDRAWN, then restored with reasons (v693)
- **triage:** LIVE-STANDING · **verification:** AMBIGUOUS-OR-CONFLICTING
- **evidence / note:** The pool update v2 IS live (board 88ce647f…), but the register itself records the levels as PROVISIONAL, iterated on a meter the owner ruled "bad/illogical", and expected to move SUBSTANTIALLY DOWN at the 26B rederivation. The origin goal (the mark path) is explicitly NOT delivered by that landing.

### R153 — landing / override
- **register location:** units SEG2407 · versions v693 (5269252799)
- **ruling:** PR #477 MERGED ON THE OWNER'S RESTORED WORD (his reasoning verbatim: the finished-but-never-live failure mode — "we work on this, and it never ends up live, but I think because it's done it is" — plus "I'd like to have a better board while we wait"); the seat's hold recommendation OVERRIDDEN BY THE OWNER WITH REASONS.
- **register's own status claim:** live
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Board verified by content on origin/main at the time (v693).

### R154 — sitter premium
- **register location:** units SEG2320, SEG2326 · versions v684, v685
- **ruling:** "Liddy +897 is a ridiculous bug… He should be as close to no value as possible." + "It definitely shouldn't be giving players a 3x premium for playing, otherwise a player who plays well and early might become the #1 player in the game quickly!"
- **register's own status claim:** the fix built as ORDER 24/24B and landed in the pool update v2
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** M=(1-phi)*R+phi*U with phi the engine's own prorated participation bar (CURRENT state selects the multiplier, not career state), then quality-conditioned at 24B.

### R155 — sitter premium / quality
- **register location:** units SEG2353 · versions v687 (5266652914)
- **ruling:** the ORDER 24 premium was QUALITY-BLIND — "Surely the sign of playing is more than offset by the low pedigree and terrible scoring?" → AMEND-BEFORE-LANDING accepted; go word "Alright, fire."
- **register's own status claim:** amended and landed
- **triage:** ONE-TIME-COMPLETED
- **evidence / note:** Delivered as the q-conditioned premium (see R031).

### R156 — par fix
- **register location:** units SEG2265 · versions v680 (5261191193)
- **ruling:** "Yes, adopt. Please use opus 5 subagents where possible for the work here as always." — THE PAR FIX IS ADOPTED AND LANDED.
- **register's own status claim:** live board 1dbd1480 at that landing
- **triage:** ONE-TIME-COMPLETED

### R157 — frozen model / cm_400
- **register location:** units SEG2250 · versions v678 (5260931315 / 5261008724)
- **ruling:** the owner's deferral of the cm_400 retrain to "the next exercise after this is done"; re-put with the facts corrected and RE-AFFIRMED ("Happy to keep the deferral.").
- **register's own status claim:** deferral kept on corrected facts
- **triage:** QUEUED
- **evidence / note:** The static contamination (cm_400 trained ~45.36% on pool careers, baked inside every ND price) stands by owner choice, with its own later act.

### R158 — records
- **register location:** units SEG1362 · versions #326 records ruling
- **ruling:** RECORDS RULING: the release-transition register appends at ADOPTION only (its entry shape needs adoption-time identities + the owner's word).
- **register's own status claim:** ruled
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** data/release_lineage.json entries append at adoptions only.

### R159 — presentation
- **register location:** units SEG1374 · versions v576 PRESENTATION LAW
- **ruling:** THE PRESENTATION LAW: review material is CURRENT-BASIS or it does not ship; superseded views only as labeled baselines beside their current counterpart.
- **register's own status claim:** standing
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Applied in the later record (the pre-#326 pool table cost a review cycle and is named as the motivating case).

### R160 — presentation
- **register location:** units SEG1285 · versions v564
- **ruling:** twin rules recorded as binding: design audits check OWNER INTENT AND LAWS BEFORE MECHANICS (hazard 16), and EVERY PRESENTED NUMBER NAMES ITS QUANTITY in plain words.
- **register's own status claim:** binding; in the seam charter
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R161 — H design direction
- **register location:** units SEG1968, SEG1962 · versions v655, v654
- **ruling:** STANDING RULING — THE H DESIGN DIRECTION: a mature-pool discount, if the historical data supports one, belongs on the V0/PRIOR SIDE where a body of work overcomes it — NEVER as a flat multiplier on the finished production-led price.
- **register's own status claim:** STANDING RULING RECORDED
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** H retired to 1.0 across all three cells (see R014); the replacement (pool sit-out retention) is derived on pool history and applied mean-preservingly on the anchor side.

### R162 — prior vs end multiplier
- **register location:** units SEG1957 · versions v654
- **ruling:** owner words: "the main one is the 0.615 being multiplied at the END, not to the uncertainty. Pool v0 of mature non-rookie draft might make sense to be less given historical data, but it's there as a prior to be overcome by body of work/evidence".
- **register's own status claim:** the end-multiplier REJECTED; prior-side directed
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Same site as R161.

### R163 — pool isolation
- **register location:** units SEG2223 · versions v675 (5252409884)
- **ruling:** "this pool v0 would be the same method and principle as ND, but entirely separate. No leakage or sharing. So just like ND KPD pick 5 v0 doesn't double count KPD, RD KPD v0 wouldn't either?" — THE ISOLATION LAW: the live keys for a pool v0 are PATHWAY × POSITION × AGE.
- **register's own status claim:** owner challenged the seat and was right
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** entry_anchor(p) returns pool_level(p)*_PL_F*_b_factor(p) for pool rows and v0_start(p) for everyone else (_merged_recover.py:2014); _v0_curve_assert states a pool row "teaches no fit site, and IT NEVER READS THIS SURFACE AT ALL".

### R164 — year-zero restore
- **register location:** units SEG1616 · versions v621 (1.1)
- **ruling:** 1.1 RESTORE YES (method = the old law's isotonic MERGE per position×age profile — his "each position should have a 1-64 curve, their own ones" = the design, adopted).
- **register's own status claim:** landed as the G1 restore
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Same site as R018 (D14d rising steps 1–64 = 0; Grlj/Cumming inversion gone, both 2123.2).

### R165 — design principle
- **register location:** units SEG1622 · versions v622
- **ruling:** OWNER DESIGN PRINCIPLE: "you would think if we have decided that v0 is a thing, that v1 would then borrow from that prior, each year diminishingly so until production is the major lever in pricing".
- **register's own status claim:** seat reading recorded FOR THE COMPOSITION
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** The blend machinery exists (the anchor-vs-production games ramp); ITEM A extended it past ns==0. The pool anchor leg pointing at the age-aware prior is the part the register flags as load-bearing and sequencing-dependent.

### R166 — no cherry-picking
- **register location:** units SEG1653 · versions v624 (5236554831)
- **ruling:** NO-CHERRY-PICKING ANSWERED: ITEM I added — EVERY F-based verdict incl. audit 1's year-0 honesty verdicts RESTATED on the corrected ruler in one table (the sitting sees no number on the bent ruler).
- **register's own status claim:** ordered; delivered as ITEM I
- **triage:** ONE-TIME-COMPLETED

### R167 — ruler check
- **register location:** units SEG1634 · versions v623 (5236054423)
- **ruling:** owner words on the ruler check: the ruler is ASSUMED BENT — deliverable reframed as a TILT MAP ("zero chance the ruler is straight… where it's least straight?"); live careers ≥11 seasons ADMITTED (his rule); axes = ALL sizing axes not just position.
- **register's own status claim:** delivered as the year-4 ruler tilt map
- **triage:** ONE-TIME-COMPLETED

### R168 — measurement unit
- **register location:** units SEG1701 · versions v629
- **ruling:** F8 PLAYER UNIT: the bar counts players not player-seasons; one ruck cell passes rows/fails players = how the ambiguity was caught; fewer lawful cells, each more trustworthy; governs every cell reading from this act.
- **register's own status claim:** governs every cell reading
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Applied in the composition and pool acts; no committed check enforces the unit on a future instrument.

### R169 — anchors
- **register location:** units BLK0051 · versions item64
- **ruling:** THE RULING, GENERALISED: an anchor is a DIAGNOSTIC, not a TARGET. A wrong mechanism is not to be preserved because fixing it disturbs a read… No build may tune a lever to protect an anchor.
- **register's own status claim:** doctrine (same family as the standing ban on predicate-based nerfs)
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** Re-expressed later as "no component tuned to a named player's number" (v631) and the YEAR-4 law (R033).

### R170 — axis rule
- **register location:** units BLK0120, BLK0287 · versions item131, item177
- **ruling:** THE AXIS RULE (L-AXIS, RATIFIED BINDING): a mispricing between named players is cured on the axis where it lives; closing a two-player gap by moving a third population is a hand-edit wearing a rule's clothes. Carve-out: globally-motivated, globally-measured recalibrations are not "moving a third population"; owner-only, per-use, register-recorded waivers.
- **register's own status claim:** BINDING at CONSTRAINTS v1.17 PART 5
- **triage:** LIVE-STANDING · **verification:** DELIVERED-UNGUARDED
- **evidence / note:** Cited and applied in later dispositions (e.g. "the right fix is the YEAR-0 KPD surface, not a year-1 cut", v612); no machine check.

### R171 — conservation / sincerity
- **register location:** units BLK0365 · versions item256
- **ruling:** THREE OPERATIVE LAWS: (1) PER-POSITION CONSERVATION IS NOT OWNER LAW — positional pools may re-rate; unfunded value is permitted. (2) G-COHORT remains the binding relativity guard (age, not position). (3) THE SINCERITY LAW (standing): a success claim for a relative goal is judged in RELATIVE terms — a nominal rise that loses rank is a FAILURE and must be reported as one.
- **register's own status claim:** standing; folded to CONSTRAINTS as L-SINCERE
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** acceptance twin leg_b.value_flow (per-position conservation NOT law, unfunded permitted, sincerity two-artifact schema); sincerity ledgers with ranks shipped in every later act.

### R172 — young side
- **register location:** units BLK0119 · versions item130
- **ruling:** no net-strip of the young side (over-performers never cut); the protected quantity is EARNED/PRODUCTION value; the unearned pick prior dissolves in BOTH directions (R104.8 gloss).
- **register's own status claim:** ruled; the gloss ruled at item 190
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** acceptance twin value-flow checks + the standing pattern named at item 132 ("cutting is gate-safe under most checks and the young side holds the largest non-evidence value pool") with mechanical counters standing.

### R173 — process / cross-seat
- **register location:** units SEG1750 · versions v635
- **ruling:** NEW RULE recorded both sides: a process a seat did not start gets FLAGGED with ps evidence, killed only on the owning seat's word (or provably-orphaned AND blocking a ruled deliverable); own strays remain own to reap.
- **register's own status claim:** new rule
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R174 — process / parallel era
- **register location:** units SEG1720 · versions v632
- **ruling:** PARALLEL-ERA WORKING RULES, from two near-misses the same day: worktree separation for seat pens vs builds; never leave a fix-worktree on the build's branch.
- **register's own status claim:** recorded
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE
- **evidence / note:** This sweep runs in an isolated worktree, per the same rule.

### R175 — process / evidence order
- **register location:** units SEG1302 · versions v566
- **ruling:** Standing rule endorsed: EVIDENCE COMMITTED BEFORE ANY SUBSTRATE OPERATION; git stash remains barred on substrate files.
- **register's own status claim:** standing rule endorsed
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R176 — process / capture currency
- **register location:** units SEG1188 · versions #290 R-J
- **ruling:** R-J (THE CAPTURE-CURRENCY LAW): any act touching a product file refreshes the ruled capture IN THE SAME evidence commit — "I checked this before" is not a check.
- **register's own status claim:** seam law
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R177 — process / instruments
- **register location:** units SEG1142 · versions #290 THE GENERALISED FREEZE LAW
- **ruling:** THE GENERALISED FREEZE LAW: a pinned-input instrument's input is COMMITTED, or its emitter and substrate are both reachable from the tree.
- **register's own status claim:** law
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R178 — identity
- **register location:** units SEG1188 · versions #290 signature fact
- **ruling:** A SURFACE'S IDENTITY IS ITS FULL MD5; SIGNATURE-STABILITY IS NEVER BYTE-STABILITY.
- **register's own status claim:** ratified; joins the identity-by-key hazard family
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** Guard 5 pins the full md5; the v0surf frozen-signature check HALTs on an unknown signature (one_source_selftest.py:735-743).

### R179 — process / reconstruction
- **register location:** units SEG0106, SEG0542 · versions v410, v481
- **ruling:** RULING: reconstruction from derived artifacts is BARRED for the owner's edit canvas — the workbook baselines the ONE SOURCE's authored bytes or it does not exist … a reconstruction qualifies as the artifact of record only if it reproduces the committed candidate BYTE-EXACT, carries the no-op control, is LABELLED IN-FILE AS A RECONSTRUCTION, and is screened.
- **register's own status claim:** ruling
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R180 — process / acceptance vocabulary
- **register location:** units SEG0577, SEG0578 · versions v484
- **ruling:** NORM ADOPTED: "accepted" is TRUE of the PRESENT-LENS ORACLE and FALSE of the INTEGRATED RELEASE STATE — ORACLE SITES KEEP THE WORD, RELEASE-STATE SITES CANNOT … conforming a TRUE statement about the old world can silently MANUFACTURE AN UNTRUE CLAIM OF ACCEPTANCE, FINALITY OR OWNER APPROVAL about the new one.
- **register's own status claim:** NORM; added to the landing checklist as a STANDING PREDICATE
- **triage:** PROCESS-LAW · **verification:** UNVERIFIABLE-BY-CODE

### R181 — referee protocol
- **register location:** units SEG0092 · versions v407
- **ruling:** F4 GIVEN — REFEREE PROTOCOL FROZEN (owner word "F4 Frozen"): docs/referee/REFEREE_PROTOCOL.md v1.0 is FROZEN and is now the AUD-004 SPECIFICATION OF RECORD; immutable except by owner-worded, version-bumped amendment, next-round effective, full re-score, never proposable in the same round as a result it would reverse.
- **register's own status claim:** FROZEN
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** docs/referee/REFEREE_PROTOCOL.md present and frozen; the harness has never been built, so no round has scored against it.

### R182 — referee dials
- **register location:** units SEG0066, SEG0073 · versions v399 (Dial-8), v402 (Dial-9)
- **ruling:** DIAL-8 RULED (owner word "B - confirmation dispositive"): SELECTION IS EXPLORATORY, CONFIRMATION IS DISPOSITIVE. DIAL-9 RULED (owner word "Prospective"): PROSPECTIVE-DISPOSITIVE — the BINDING ongoing test is the future itself.
- **register's own status claim:** encoded in the frozen protocol
- **triage:** QUEUED
- **evidence / note:** Binding only once the referee harness exists and round 0 runs; the roadmap places the referee after the root act (R076).

### R183 — referee / method
- **register location:** units SEG0041, SEG0043, SEG0044 · versions v390, v391, v392
- **ruling:** OWNER PRIORITY SEALED: the goal is THE MOST ACCURATE MODEL of future performance across all lenses; procedure is minimized to what evidence requires — no over-engineering … the unit of admission is the MECHANISM CLASS, re-tuned fresh on training folds … admitted ingredients are RE-TUNED JOINTLY at every subsequent admission step.
- **register's own status claim:** SEALED
- **triage:** QUEUED
- **evidence / note:** Encoded in the frozen protocol; awaits the harness.

### R184 — entry-pathway structure
- **register location:** units SEG0211, SEG0216 · versions v438, v439
- **ruling:** OWNER READ SEALED — ENTRY-PATHWAY VALUATION STRUCTURE: (1) the PVC covers ND PICKS 1-64 ONLY; (2) SSP, MSD and rookie-draft pathway values are TRACKED INDIVIDUALLY; (3) ND 65+, post-draft academy/NGA, unregistered, Ireland and rookie-drafted players POOL into one shared-value bucket BY POSITION … the PUBLISHED pick scale is FIXED at 1-64 by product ruling; the curve within the fixed scale flattens onto the pool floor wherever measured decay lands.
- **register's own status claim:** sealed; implemented by THE SPLIT and #326
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **supersession:** refined by R010
- **evidence / note:** Superseded in detail by the per-division signed levels (R010) which give each pathway its own level rather than one shared bucket — an owner-ruled refinement, not a contradiction.

### R185 — architecture
- **register location:** units SEG0224, SEG0752 · versions v441, v499
- **ruling:** TWO-LAYER READ SEALED (owner words): "How well can we project future performance — the modelling. And how do we value performance — past, present and future — the pricing. Very separate." … POSITION PREDICTS, ELIGIBILITY PRICES: "The eligibility list is correct. I thought position was for modelling performance going forward… But eligibility was about assessing the value of that performance for a team."
- **register's own status claim:** SEALED
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The engine keys the year-0 bar on eligibilities (R065) and the years-1+ leg on future_position; §1b implements the current-season DPP pricing.

### R186 — item 412
- **register location:** units SEG0914 · versions v510
- **ruling:** ITEM 412 FOLD-BACK (owner-ruled): 412 is a read-only DESIGN seat … THE OWNER HAS ALREADY RULED THE POOL'S CONSTRUCTION, so that slice is IMPLEMENTATION and folds back into build work now. 412 RETAINS: the pricing validation design, curve family, era handling per R-ERA, observation-lane mechanics, the replacement bar re-keyed from position to eligibility, and the future-eligibility instrument that does not exist as a field.
- **register's own status claim:** owner-ruled
- **triage:** QUEUED
- **evidence / note:** ITEM 412 sits last on the roadmap of record (R076).

### R187 — incremental currency
- **register location:** units BLK0196, BLK0234 · versions item326/327, item364
- **ruling:** THE INCREMENTAL CURRENCY QUESTION: "Pick 60's value isn't pick 60. It's whatever pick 60 is worth over a free-to-replace list spot" … R RULED: a SINGLE FLAT SCALAR across the whole board, DERIVED not hand-set (R = the measured R_realized = 207), delivered as a VIEW (v−R) beside the gross curve; the PVC stays GROSS.
- **register's own status claim:** ruled; the v−R view first-class at the viewing
- **triage:** QUEUED
- **evidence / note:** The gross curve stands; the re-founding question (whether the board re-denominates) was explicitly left post-v2.11 and has not been re-opened. Adjacent to the ×1.4200 exchange-rate question now on the owner's desk (v701).

### R188 — lenses
- **register location:** units BLK0215, BLK0216 · versions item345, item346
- **ruling:** "The +1/2 lenses should include phantom draft picks to replace the value of declining players who exit the system." + "The -1/2 lenses should be easy to achieve as we have a record of all the players on a list in 2024/2025." → OWNER RULES OPTION B — the chapter extends: LEG F.
- **register's own status claim:** ruled; landed (Leg F)
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The shipped board carries phantomPicks (130 entries) and lensPicks; RL_LEGF declared in the manifest.

### R189 — conservation construction
- **register location:** units BLK0229 · versions item359
- **ruling:** OWNER RULES THE CONSERVATION CONSTRUCTION ("Rule it"): the FULL entrant side (~100 slots, real pick structure + mechanisms), ONE CARRIER — the POPULATION-measured decline rate carries ALL exit risk; the CONSERVATION GATES at ±5% both transitions, roster-matched (F4) and league-level (F5); survivor-only = diagnostic report, never a gate.
- **register's own status claim:** LAW at MEMO_LEGF v1.3
- **triage:** LIVE-STANDING · **verification:** ENFORCED
- **evidence / note:** The F5 league gate PASSES both transitions in the later record (v572 "F5 league gate PASS both transitions, F4 PASS").

### R190 — conservation gate
- **register location:** units SEG0880 · versions v508 conservation gate
- **ruling:** SEAM RULING on placement: inside the advance transaction, after the siblings stage and before COMMIT_BEGIN, in the same journalled rollback boundary — a conservation law that runs after commit reports a violation already published.
- **register's own status claim:** PARKED BY OWNER RULING (v508)
- **triage:** QUEUED
- **evidence / note:** On the parked list; not started.
