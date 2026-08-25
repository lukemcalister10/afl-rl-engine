# PREREG ORDER 45 — THE POSITION-SCALED SAFETY NET (RL_O45)

**Seat:** the post-compaction landing seat. **Date:** 2026-08-25.
**Engine base:** arm-2 head `53ce2fb7` (`/home/user/arm2_norec/root_final/engine/rl_after/_merged_recover.py`; live main is `3af8c1f7` — the flip commit carries both this head and the lever to main).
**Board base (kill-switch-off board):** `543bf900` — the adopted candidate (D1, owner verbatim 2026-08-25: *"Yes, adopt the new model"*).
**Board of record (unmoved until the landing):** `82fcd8bb`.

**This document is committed BEFORE the lever edit (process law P9). Every number in §4 is a
prediction filed in advance from `docs/evidence/seam_fix_search_2026-08-25/NET_PREDICTION.json`,
reproduced by this seat from the filed script in the filed world before this prereg was written
(screen by re-running). Nothing in §4 is a result.**

---

## 1 · THE RULED WORDS THIS BUILD EXECUTES

- **D1** (v852): *"Yes, adopt the new model"* — board 543bf900 adopts.
- **D2** (v853): *"Scaled on the safety net"* — the POSITION-SCALED ramp.
- **D3** (v853): *"Exclude mature agers"* — entry-age ≥22 rows are out of the net.

The net is a SHIELD (`max(0, cf − v)`): it can only raise, exactly like the shipped ORDER D7
parity guard ("the shield is not a charge"). Its one-directionality is owner-ruled and declared
here, not discovered later; the claims note will carry it.

## 2 · WHAT IS BEING BUILT

A final `ev()` wrap — **ORDER 45 (RL_O45)** — installed immediately after the ORDER D7 parity
guard in `_merged_recover.py`, following the file's standing kill-switch pattern:
`RL_O45` default `'1'`; `RL_O45=0` ⇒ the wrapper is never installed ⇒ board `543bf900` byte-exact.

**Scope (a row is in scope iff ALL hold, at Y=2026 only):**
- not `_retired`;
- no banked level: no season with ≥6 games;
- ≥1 career game (`gtot ≥ 1`);
- tenure 1–4, entry-year convention: `ten = 2026 − year + 1`;
- entry age < 22: `year − _by < 22`; a scoped row with missing `_by` HALTS (no silent pass).

**The lift:** `v_new = round(v + λ(c) · max(0, cf − v))` — add-then-round (the audit's blocker-1
convention: at λ=1 the new value EQUALS the counterfactual exactly).
- `c` = games-weighted cameo average over seasons ≤ 2026;
- `pos = MA.gfut(p)` — gfut RETURNS the group; `REPL` is keyed by it; an unresolved group HALTS
  (never a silent MID default). The display `grp` column is NOT consulted (seven gfut-vs-display
  sightings stand: dodson, leake, edwards, mccabe, whitlock, nairn, dalton);
- knots `(40, 45) × s`, `s = (REPL[pos] − 3)/77.1` (MID normalizer; MID s = 1 exactly);
- `λ = smoothstep(3t² − 2t³)` between the scaled knots, 0 at/below, 1 at/above — continuous,
  no cliff (law 3 declared satisfied by construction);
- `cf` = the row's own engine price with scoring stripped: in-process `p['scoring'] = []` →
  inner `ev` → restore in `finally`. The probe is NON-DESTRUCTIVE BY ASSERTION (the D7-F6
  pattern): after restore, the inner `ev` is re-run and must equal `v` exactly, else HALT.
  The "48 sitters validated" claim of v854 traces to prose only and is treated as UNFILED;
  THIS assert, running on every lifted row at every emit, is its replacement;
- the pick re-denomination factor is READ from `engine/rl_after/pick_redenomination.json`
  (`factor`, the certified carrier) wherever the lever needs it — never hardcoded.

**Recursion:** none — `cf` is computed through the pre-45 inner `ev` (`__inner`), and a stripped
row has 0 games so it could not re-enter scope even through the wrapped symbol.

**Walk-forward safety:** the wrap acts at `Y == 2026` only; years-1+ matrices formed from
`ev(p, Y > 2026)` cannot be reached by it (the D7 convention).

## 3 · THE KILL SWITCH (spec.py slots)

- `kill_switch.name` = ORDER 45 — the position-scaled safety net
- `kill_switch.env` = `RL_O45`
- `kill_switch.board_with_switch_off` = `543bf900` (NOT the board of record; `board_before` for
  the landing is `82fcd8bb`, and `board_after` is the WITH-NET board md5 minted at the emit in §5).

## 4 · PREDICTIONS (filed before the edit)

**Exactly 11 movers** vs board `543bf900`, total **+923**, every other row byte-identical:

| player | pos (gfut) | tenure | cameo c | 543bf900 | predicted | lift | λ |
|---|---|---|---|---:|---:|---:|---|
| James Leake | SD | 4 | 48.1 | 168 | 421 | +253 | 1.0 exact |
| Taylor Goad | RUCK | 4 | 43.5 | 441 | 667 | +226 | 0.958 partial |
| Will Green | RUCK | 4 | 62.7 | 468 | 678 | +210 | 1.0 exact |
| Charlie Edwards | MID | 4 | 47.5 | 289 | 404 | +115 | 1.0 exact |
| Vigo Visentini | RUCK | 4 | 67.2 | 173 | 211 | +38 | 1.0 exact |
| Lachlan Smith | RUCK | 4 | 53.0 | 150 | 186 | +36 | 1.0 exact |
| Zane Zakostelsky | KPD | 4 | 49.0 | 143 | 171 | +28 | 1.0 exact |
| Oscar Ryan | SD | 4 | 88.0 | 185 | 193 | +8 | 1.0 exact |
| Tom Anastasopoulos | SF | 4 | 42.2 | 77 | 84 | +7 | 1.0 exact |
| Cooper Simpson | SD | 4 | 39.6 | 86 | 87 | +1 | 0.033 partial |
| Wil Parker | SD | 4 | 40.0 | 36 | 37 | +1 | 0.096 partial |

- **The structural fact (v856, for the dry-run too):** after D3 the net is a TENURE-4-ONLY
  instrument — every tenure-1–3 non-mature in-scope row has λ = 0 (largest cameo among them,
  patterson 35.6, sits below the SD lower knot 39.07).
- **Mature-agers excluded by D3** (would otherwise move): johnson +82, jepson +74, henderson
  +21, podhajski +6 — candidate-world pre-D3 = 15 movers, +1,105.
- **No mover is a day-0 row** (measured) ⇒ `day0_rebase = OFF`.
- Pool moves **+923 (+0.13%)** on the owner's explicit D2/D3 words; the movement is a
  redistribution *toward* the counterfactual each row's own engine price defines, and the
  full mover ledger above is the conservation statement (the leg-b ledger remains UNMEASURED
  per PART 3, as it is for every current release).

**DECLARED KNIFE-EDGE (the george-stevens class, v856):** the lever returns an integer at the
`ev()` scale; the exporter's own re-denomination rounding then applies. For the eight λ=1-exact
rows the lever returns the counterfactual integer itself, so the board value is IDENTICAL to the
prediction by construction. For the three partial-λ rows (goad, simpson, parker) double rounding
can in principle land ±1 from the single-rounded prediction. Falsifier bands, accordingly:
λ=1 rows must match EXACTLY; partial rows within ±1 (any ±1 case is disclosed and reconciled
before the dry-run, not waved through).

## 5 · FALSIFIERS AND SEQUENCE (each one reds the act if it fails)

1. **Kill-switch proof:** `RL_O45=0` emit ⇒ `rl_app_data.json` md5 == `543bf900` byte-exact.
2. **The with-net emit:** `RL_O45=1` (default) ⇒ exactly the 11 movers of §4, within the
   declared bands; ZERO other movers; the with-net md5 becomes `board_after`.
3. **Self-test proven able to fail:** the mover-comparison self-test is first run against a
   deliberately corrupted expectation and must FAIL; then against §4 and must PASS.
4. **Non-destructive probe:** the in-lever D7-F6-style restore assert HALTS on any drift —
   silence is a red.
5. **P12 — the priced-arm reading:** the no-arb class reading + level census + pinball run ON
   THE WITH-NET BOARD (not on 543bf900, not on a sibling), via the filed battery recipe with
   `$EV` re-pointed at a durable checkout of `rebake/arm2-design` and `RL_DAY0_FINAL`
   regenerated for the with-net board (predicted unchanged from `DAY0_FINAL_FINAL.json`, since
   no mover is a day-0 row — the regeneration is run anyway and must agree).
6. **B3 book-seal rerun** on an idle box (twice timed out on a loaded one; the timeout is a
   carried red until this rerun lands its verdict).
7. **Law 11:** this is a value-moving release — machine-generated claims note (`tools/claims.py`)
   + ONE blind independent review BEFORE the owner's word; this seat's own screens do not exempt it.
8. **The landing:** dry-run one-screen movers to the owner (stating the tenure-4-only fact) →
   HIS GO → flip commit (arm-2 engine head + band/ceiling/peak/table/pvc + lever to main,
   `coherent_base` = that commit's parent — the Graham pattern) → ONE landing through
   `tools/land lever`. `board_before = 82fcd8bb`; identity moves per v856's pre-filled slots;
   store `fb640ca0` UNMOVED.

Corrections to this prereg, if any are forced by the tree, are made AGAINST the tree with the
error named (P9), never the tree against the prereg.

---

## 7 · THE LAW-11 BLIND REVIEW IS ABSORBED (verdict: BLOCKED pending these corrections; the
## reviewer independently reproduced every hash, the full board diff — exactly 10 movers +922,
## zero strays — the knife-edge arithmetic, all nine identity moves, and the P9 commit ordering.
## Every finding below is a correction to what this act SAYS, plus one code fix; none moves the
## board. Where §1-§6 conflict with this section, THIS SECTION SUPERSEDES.)

**R-FIX (the one code change) — the synthetic-row halt.** The first ship-gates run CRASHED on the
lever's own D3 halt: gates price KEYLESS synthetic probe rows, and one with 1-5 games and no `_by`
reached the halt. Fixed: a keyless row has no store identity, D3 cannot be evaluated, the net does
not apply — base price stands; a REAL (keyed) row missing `_by` still halts. Engine head moves
**572b823e → e215caece9e43a5eb3ab47340dbab7fa** (supersedes C1's value); candidate boot re-pinned;
BOTH emits re-proven on the fixed head (prediction: the with-net board returns byte-identical
`3167cba6` — the fix touches only keyless rows) and ship-gates rerun in flight.

**R-FIX2 — the reviewer's second pass (verdict CONDITIONAL) is absorbed; three findings, all
addressed BEFORE the re-proof ran.** (NEW-1) The keyless-probe guard was nested inside the `_by`
branch — a keyless probe that grows a `_by` would have slipped past it into the full net (no such
builder exists today, measured; the B6 probe's own comment documents exactly this field-drift).
MOVED to a top-level scope test beside `_retired`: a keyless row gets the base price whatever
other fields it carries. Engine head moves **e215caec → d84031cff312818a158855f2dd223cc1** (the
FLIP head; supersedes R-FIX's value); boot re-pinned; the full re-proof (both emits + self-tests
+ ship-gates) runs on THIS head, with the same byte-identical-board prediction. (NEW-2) B6's
games-ramp gate probes with a KEYLESS synthetic — so after the guard it measures the BASE ramp
and is STRUCTURALLY BLIND to the net's ≥6-games boundary step; recorded IN THE INSTRUMENT per
P11 (ship_gates_check.py, the B6 header), and stated here: NO instrument in the suite covers the
net's boundary step — R2's declaration is the only cover, and it is load-bearing. (NEW-3) the
emit script could strand the candidate root COHERENTLY sealed in the net-OFF posture on any
mid-script failure (it was in exactly that state when the reviewer measured it); a `trap` now
restores the `'1'` posture on every exit path, and the PRE-FLIP CHECK IS MANDATORY: manifest
`RL_O45='1'`, config `29fdfd1e1447…`, before the flip commit is cut.

**R-FIX3 — the reviewer's interim third pass: the FLIP SET GAINS THREE COMPANION FILES (was a
BLOCKER), and the executing emit script is filed.** (NEW-4) A full tracked-file diff (this seat
re-measured; the C4 sweep had scoped to engine/ and data/ and missed them) finds three more
candidate-side files, each BYTE-IDENTICAL to `rebake/arm2-design` and differing from main:
**`boot_guard.py`** (368a6787 — Guard 5's `_resolve_cm_load` mirror, which the flip-set member
`wire_redesign.py` documents MUST move in lock-step with its new `cm_load_path()`, on pain of
re-opening the register-item-91 hole), **`config_manifest.py`** (41f043a2 — its INFRA_ALLOW
learns `RL_CM_PKL`/`RL_Q97M_PKL`; without it the landed main REJECTS the filed emit recipe and
`board_after` could not be re-derived on the tree that claims it — the C1 failure mode), and
**`refit_q97m.py`** (4ff515e1 — the provenance script of the MOVED identity q97m). ALL THREE
ENTER THE DECLARED FLIP SET; C4/R7's "nothing else differs" is corrected a second time, and the
honest statement is now: the flip set = C4's list + ship_gates_check.py (NEW-2) + these three;
`gates_snapshots/gates_53ce2fb7.json` remains the one EXCLUDED difference (R7). The widened
INFRA_ALLOW surface is **THREE variables, not two** (reviewer NEW-6, AST-parsed from both files):
`RL_CM_PKL` and `RL_Q97M_PKL` (pickle paths — they name WHERE artifacts load from, and Guard 5/
the manifest pin WHAT loads) plus **`RL_WS`**, which is NOT a pickle path: it is the refit
tooling's workspace root (`config_inventory.py` classifies it "refit_q97m workspace (bake tool
only)"), read by ZERO board-path modules and set by NO filed recipe — it is admitted solely
because dropping it would break `config_manifest.py`'s byte-identity with `rebake/arm2-design`,
and an accurate declaration is cheaper than a divergent file. Also for the record: six GENERATED
docs indexes (STATE.md, register/incident INDEX/LATEST/index.json) differ only because the
candidate root is a stale seed of an older main commit — they are DELIBERATELY NOT CARRIED
(carrying them would revert main's registers); the flip set is an enumerated allowlist, and
nobody should later "complete" it with these. (NEW-5) the R-FIX2 trap went into the EXECUTING emit script but the filed
evidence copy lacked it — the executing copy (with trap, 2548 bytes) is now filed over the stale
one; the recipe on the record is the recipe that runs.

**R-FIX4 (reviewer NEW-7) — the emit recipe's ANNOUNCE GUARDS were structurally broken, and the
record is corrected.** rl_export execs the engine inside a discarded StringIO, so no module-level
print (ORDER D7's included — measured 0 in every emit log) can ever reach the logs. The ON-leg
announce grep was therefore a GUARANTEED false RED (it fired in BOTH chains — the first chain's
exit-4 was mis-read by this seat as a one-off and the instrument left unfixed; this seat had even
diagnosed the swallowed prints and corrected its conclusion without correcting the guard), and
the OFF-leg mirror was a VACUOUS pass that could never have caught a wrapper installing with the
dial off. BOTH RETIRED from the recipe; installation is now proven by what the boards say: the
OFF board byte-equals `543bf900` (verified by `cmp`, reviewer-verified), the ON board differs
from it and equals the predicted `3167cba6` with the self-test binding it to the filed movers.
THE HONEST RESTATEMENT OF C3 AND THE RE-PROOF: falsifier 1's conclusion rests on its board-byte
leg ALONE (which holds, twice, on both heads); falsifier 2's board leg is GREEN on the final head
`d84031cf` — the reviewer's own full recursive diff reconfirmed exactly 10 movers +922 with zero
strays, vP1 +618 / vP2 +648, both self-test legs correct — while its announce leg RED'd in both
chains and is void, never having tested anything. The filed evidence copy of the recipe is
updated in the same commit as this note.

**R-FIX5 (the review's FINAL CONDITION, filed before the owner is asked) — FALSIFIER 6 (§5.6, the
B3 rerun) IS NOT DISCHARGED, and its carried-red record is CORRECTED under P7.** The rerun ran on
a fully idle box and timed out again — at the instrument's OWN internal 1800s ceiling, with the
matrix computing healthily (~24 CPU-min, watched live by the reviewer). §5.6's hypothesis
("timed out twice on a loaded box" — implying an idle rerun resolves it) is **FALSIFIED**: the
cause is the check's ceiling, not machine load. Under P7 a red is carried only while failing THE
RECORDED WAY; the record is hereby re-presented in its true form: **B3 fails by instrument
ceiling (1800s < its own workload at current scale), on any box, board-independent — and it has
never sealed ANY candidate this cycle, including the already-adopted 543bf900**, so it does not
discriminate between the net and the rebake the owner already ruled. An un-capped measurement run
of the matrix is in flight for the record; the certifying fix (ceiling raise and/or the load-once
harness making the matrix a minutes job) rides the next act, and the landing choice — carry the
re-presented red tonight, or hold ~90 min for a raised-ceiling full rerun — is the OWNER'S,
stated on the dry-run page in exactly these terms. ALSO from the final pass, queued non-gating
for act two (NEW-8): B5's floor-saves report now mislabels the net's lifts as floor saves (leake
"+266 saved" is ORDER 45's lift, arithmetic confirmed by the reviewer) — the same
instrument-presentation class as B6/o33; a P11 scope note is owed in B5. The review's closing
principle, adopted for the amendment draft: **A GUARD IS PROVEN ABLE TO FIRE BEFORE IT IS
TRUSTED** (falsifier 3, run against a deliberately corrupted expectation, is the model — five
instrument defects tonight, every one a check measuring the wrong thing and reporting a confident
verdict anyway).

**R1 (was a BLOCKER) — the "tenure-4-only instrument" claim of §4/v856 is RETRACTED.** Measured by
the reviewer and confirmed: the OUTCOME is tenure-4-only (all 10 movers), but the INSTRUMENT is
not — **19 tenure-1-3 non-mature in-scope rows carry λ > 0 (12 at λ = 1.0 exactly**, mraz/francou/
dattoli/grego/banfield/dalton/murray/ough/nairn/peucker/ludowyke/howes); they do not move today
only because each one's counterfactual sits at or below its price (cf ≤ v). The net is ARMED on
them: a future refit or store change can move them with no further ruling. The §4 "patterson"
rationale compared every position against the SD knot and is void. THE DRY-RUN STATES THE TRUE
FACT; the act-spec column label drops "tenure-4-only".

**R2 (was a BLOCKER) — law 3's declared-or-red rule: the SCOPE-BOUNDARY STEPS are hereby DECLARED
with measured margins.** The smoothstep is continuous in cameo average, but the scope edges are
steps: crossing the banked-level boundary (any season ≥6 games) zeroes the lift. Measured steps at
that boundary for the landed movers: **leake −253 (his largest season is 5 games — ONE game from
the boundary), anastasopoulos −7, parker −1** (both also at 5); tenure-out-of-4 and entry-age-≥22
edges likewise zero the lift (the latter is D3, the owner's own word). These are the ruled scope's
own edges (D2/D3 define them), now registered before scoring per the law's threshold row, and they
appear on the dry-run page.

**R3 — the forward-lens ledger, previously omitted.** The board's +1/+2 lens columns inherit the
lift through the LEG F3 floor (`round(φ(games)·v)`): measured **now +922 · +1 lens +618 · +2 lens
+648** (lensConservation totals move identically; vM1/vM2 zero movers). §2's walk-forward-safety
claim is true of `ev(p, Y>2026)` but NOT of the board's lens columns; the full three-line ledger is
the conservation statement and goes on the dry-run page.

**R4 — "≥1 career game" DEFINED.** The scope test is the sum of games over the row's SEASON
SCORING RECORDS (year ≤ 2026) — the field the lever, the prediction, and the packet the owner
ruled on all use. It is NOT the store's flat `games` display field, which is stale on ~500 rows
(will-green: field 0, seasons sum 3 — verified against the raw store). The stale-field
reconciliation is QUEUED as data hygiene for act two.

**R5 — the counterfactual's honest name.** `cf` is the row's price with its season scoring records
stripped and every other field (including the `games` tally read by the peak-blend at
rl_model.py:1275) retained — a scoring-stripped price, NOT literally "the price had he never
played". The prediction was built with the identical strip, so the lever prices exactly what the
owner ruled on; the §2 description is corrected, and no validation of cf beyond the three
hand-checked movers and the D7-F6 restore assert is claimed.

**R6 — C3's "identical by construction" for λ=1 rows is RETRACTED.** Those rows carry the same
double-rounding exposure as the partial rows (`round(round(CF)/F)` vs `round(CF/F)`); all eight
matched in fact, not by construction. The self-test's exact band stood and stands.

**R7 — C4's "nothing else differs" corrected.** One additional tracked-path file differs:
`data/gates_snapshots/gates_53ce2fb7.json` (a candidate-world snapshot for the superseded
intermediate head). It is EXCLUDED from the flip set — the landing machinery writes its own gates
snapshot.

**R8 — the one-directionality is put IN WORDS for the owner's GO.** Law 5 says "no
one-directional levers"; this net lifts only. The packet the owner ruled on presented it as
exactly that (a safety net lifting toward cf), so his D2 word covers the design he saw — but the
waiver is his to give in words, so the dry-run page carries an explicit line and the claims note
carries the declaration. Whether shields become a standing rulebook exception (the D7 precedent)
is queued for an owner word — rulebook changes are law 10(a).

**R9 — the hardcoded 2026.** The wrap tests `Y == 2026` literally (the D7 convention); at the
season rollover it goes inert silently. Carried class, queued for act two (wire to the declared
LIVE_SEASON constant or add a rollover checklist assert).

**R10-R12 (nits, corrected on the record):** goad λ is 0.963 (0.958 was a transcription slip);
the pre-D3 reconciliation reads 923 + 183 = 1,106 (not 1,105); predict_net.py §4 numbers carry its
hardcoded F/normalizer (the LEVER derives both — the reviewer verified); the lever's "active" test
is `_retired` only, narrower than the engine's `delisted()` (zero exposure today, measured).

## 6 · P9 CORRECTIONS FILED AGAINST THE TREE (same day, before any result was read)

**C1 — the identity `config` MOVES; v856's pre-filled slot list (and §5.8's "identity moves per
v856") had it UNMOVED, and that was wrong.** The gate-mode config manifest rejects any RL_* dial
not declared in `data/model_config.json` (measured: the first emit attempt HALTED on
`UNKNOWN model override RL_O45='0'`). Declaring the kill-switch is therefore part of the lever
build, exactly as the manifest's own doc requires ("amend the manifest at a bake in the same
commit that re-stamps config_sha256 + expected_boot.json"). Consequences, all now predictions:
- `model_config.json` gains `vars.RL_O45 = '1'` (+ a var_note) → config hash moves
  `eed19a75f775…` → **`29fdfd1e1447…`** (85 vars; `config_manifest.py check` PASS in the
  candidate root);
- `expected_boot.json` `config` and `engine_head` re-pin (engine head `53ce2fb7` →
  **`572b823e`**, the lever-carrying head — this is the head the flip commit takes to main);
- `release_contract.json` `config_sha256` moves and the contract re-seals via its own
  `contract_hash` (the landing preflight asserts self-consistency, tools/landing/steps.py:1133).

**C3 — the knife-edge fired, on one row, and is reconciled (filed AFTER the emits; results, not
predictions).** Falsifier 1 GREEN: the declared-`'0'` manifest emit byte-reproduced `543bf900`
exactly. Falsifier 2: the with-net board is **`3167cba643a6b16e5ef5d904d8957fcd`** — this md5 is
`board_after`. It moves **10 rows, +922** vs the predicted 11/+923: every λ=1 row matches
EXACTLY, goad (λ .963) and parker (λ .096) match exactly, and **cooper-simpson (λ .0309,
predicted 86→87) did not move** — the §4-declared double-rounding knife-edge, PROVEN by
measurement (PROBE_KNIFE_out.txt): inner V=90, CF=127.038, X=V+λ(CF−V)=91.1440 → the lever's
`round(X)`=91 at the ev scale → the exporter's re-denomination `round(91/1.0524)`=**86**, while
the prediction's single-rounded `round(X/1.0524)`=87; exactly one rounding boundary separates
the paths, and the other two partial-λ rows agree on both paths. The landed convention is the
engine's (the lever sits at the one law, as v854/v856 specify); the deviation is within the
declared ±1 band and is carried to the dry-run page as a named line, not silently. Falsifier 3
GREEN: the self-test FAILS on a corrupted expectation (leake +1) and PASSES on the real one with
the cooper-simpson deviation DISCLOSED (SELFTEST_*_out.txt).

**C4 — the identity `fv` MOVES too; v856's slot list was wrong on it as well.** Measured: the
candidate root's `engine/forward_valuation` differs from main in `build_peak_model_v4.py`,
`conditional_prior.py`, and a NEW `exact_monotone.py` — each byte-identical to
`rebake/arm2-design` (the exact-monotone design that retired ORDER 44 into the fit). fv identity
moves `6e9a370e` → `123a8155` (the candidate build's own log said so; v856 carried "fv unmoved"
anyway). The COMPLETE flip set, measured by full-tree diff of the candidate root against main
(pycache excluded): engine/forward_valuation {build_peak_model_v4.py, conditional_prior.py,
+exact_monotone.py} · engine/rl_after {_merged_recover.py (arm-2 head + the O45 lever),
_gate1_picksplit.py, _gate1_wf.py, wire_redesign.py, bust_prior_table.json, peak_model_v4.pkl
(+.srcmd5), pvc_snapshot.json (+.srcmd5)} · data {cm_400.pkl, q97m.pkl, model_config.json,
expected_boot.json, release_contract.json} — every rl_after/fv code file verified byte-identical
to `rebake/arm2-design` except `_merged_recover.py`, whose only delta beyond the branch is the
ORDER 45 block. Nothing else differs; the board itself is written by the landing machinery, not
the flip commit.

**C2 — the kill-switch proof's mechanics restated.** Gate mode also rejects DIVERGENT overrides,
so falsifier §5.1 cannot pass `RL_O45=0` in the environment. The proof instead emits against a
manifest that DECLARES `RL_O45='0'` (coherently restamped via `set_o45_manifest.py`), then the
manifest is restored to the landing posture `'1'`. The emitted board embeds no config identity
(verified: no config/engine hash in `rl_app_data.json`), so byte-equality with `543bf900` is
still the falsifier. The board of record's landed posture is the `'1'` manifest.
