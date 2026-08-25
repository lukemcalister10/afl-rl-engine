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

**C2 — the kill-switch proof's mechanics restated.** Gate mode also rejects DIVERGENT overrides,
so falsifier §5.1 cannot pass `RL_O45=0` in the environment. The proof instead emits against a
manifest that DECLARES `RL_O45='0'` (coherently restamped via `set_o45_manifest.py`), then the
manifest is restored to the landing posture `'1'`. The emitted board embeds no config identity
(verified: no config/engine hash in `rl_app_data.json`), so byte-equality with `543bf900` is
still the falsifier. The board of record's landed posture is the `'1'` manifest.
