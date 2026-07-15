# RETURN — THE RE-ENTRY TRIO: store correction (item 108a), owner-ruled "proceed full trio, store-only"

- **Branch** `claude/reentry-trio-store-correction-4rzfl7` · base pin `1073f633` STRICT (ls-remote on
  `claude/rl-model-pin-assertion-sg5hxv` verified) · line `…→#89→improver→pin→this`. Engine UNTOUCHED
  (`fc7045d6`); config `c2d233ae` UNMOVED.
- **Store md5** `340a7a32 → b1fd0bce` (this chapter's ONE store write). **Board** `dc43d602 → 800d0399`
  (re-pinned + `.srcmd5` source `b1fd0bce`). **expected_boot** store+board re-pinned, engine_head
  UNCHANGED. **Book RE-SEALED** `2a77d834 → cf90c4f4` (engine head unchanged; store moved).
- **The correction (SSI — the SOURCE, not a copy):** Perez ND p35 → SSP 2025 · McAndrew MSD p12 → SSP
  2024 · Keane IRE → SSP 2022. Each: type=SSP + re-entry year + pick None + `_pickless` True + `_draft`
  SSP (register item 17 ii). Identity facts (stable_player_id, `_by`, scoring, positions) untouched.
- **AFFECTED_ROWS — 106 v-movers, net +30 num-SCAR (⚠ FLAG: ~15× the ruling's "~7 rows" estimate):**
  the entire ripple is **McAndrew** (isolation: Perez-only=0, Keane-only=0, McAndrew-only=106). The trio's
  OWN board values are UNCHANGED (Perez 13, McAndrew 1232, Keane 2155 — the engine's PRESENT_ID_OVERRIDES
  already SSP-prices them). **43 material (≥5%), ALL MSD; 63 non-material (<5%)** — 44 non-MSD (all
  hairline float ripple) + 19 small MSD; 33 of the 106 are |d|≤2 SCAR. Full list: `measurement/AFFECTED_ROWS.md`.
  Largest: Newcombe 4302→3975 (−327),
  Coe 97→258 (+161), Noble 2699→2554 (−145), Hall 2310→2168 (−142), D'Ambrosio 1755→1622 (−133), Durham
  1823→1694 (−129); largest lifts all low-pedestal MSD (Coe +166%, May +32%, Lewis +65%).
- **Mechanism (measured, not assumed):** McAndrew's MSD→SSP relabel moves **`PICKEQ['MSD']` 60 → 90** —
  the pickless PEDESTAL is pooled by type (`rl_model.py:727`); losing a strong performer flattens the MSD
  anchor. This is the **PEDESTAL** pool, which the item-11 "pool-neutral" read did not cover (that read
  only the L4 GBM *training* pool — MSD-excluded + frozen). Owner ruled 2026-07-15 to accept it.
- **value-flow (item 130):** NOT a young-strip and NOT a broad reprice — a single-cohort effect. By age:
  ≤22 **+189** (n=46) · 23–26 **−201** (n=49) · ≥27 **+42** (n=11). Board sum 729397 → 729427.
- **SHIP-GATES:** VERDICT **FAIL=3** (A2/A3/A12 — pre-existing, carried) · PASS=17 · PENDING=4 · STRUCK=1
  · FEATURE=1 — **identical to base; zero new fails**. A9 PASS (Ginnivan 2324 > Ward 2149) · A8 Berry
  3623 / Tsatas 1481 = 2.45× · B2 PASS (leakage 0.000) · **B3 book seal MATCHES `cf90c4f4`** · **B4 board
  byte-agree `800d0399`, export exit=0**. LOG + snapshot (`gates_fc7045d6.json`, store b1fd0bce) +
  report committed.
- **G-COHORT (regenerated this run — reported vs BOTH bounds):**
  - y4 **1.2926** — clears 1.30 (margin 0.0074) AND 1.335 (margin 0.0424) → clears **BOTH**
  - y5 **1.2995** — clears 1.30 (margin **0.0005**) AND 1.335 (margin 0.0355) → clears **BOTH** (tightest)
  - y6 **1.2445** — clears 1.30 (margin 0.0555) AND 1.335 (margin 0.0905) → clears **BOTH**
  All three clear the strict 1.30; the bounded 1.335 waiver is NOT needed. (Base was y5 1.2998; the trio
  nudged it to 1.2995 — slightly further from the line.)
- **PICK 1 = 3000** (board PVC[1]=3000; numéraire guard PASS on export). Store md5 moved
  `340a7a32 → b1fd0bce` (the chapter's one store write); all SSI stamps/pins updated;
  **correction-sticks canary (Guard 4) PASS** (+ Guards 1–3/F1/F2 + Guard 5 all PASS from fresh bootstrap).
- **FENCE honoured:** store · board+`.srcmd5` · `expected_boot` · `book_stable_seal` · gates snapshot ·
  session dir. NO engine pricing-code edits. Candidate — owner tag/main promote remain owner-only.
- **TIME:** band 30–60 min; actual longer (~ a full session) — the measurement→HALT→owner-ruling→full
  pipeline, plus a self-inflicted ship-gates detour (I had leaked `SGC_REPORT_DIR` into the gate-mode
  subprocess env, tripping the config-manifest gate-seam reject; fixed by unsetting it). Flag: >2× the band.

## Close (plain terms)
The three players who left the league and came back through the pre-season supplemental door are now
recorded that way in the one store that feeds everything — not just patched in live by a hard-coded engine
override. Two of them (Perez, Keane) change nothing on the board; they were already priced right. The third,
McAndrew, does something the original ruling didn't expect: because he was a strong mid-season-draft player,
taking him out of that small group makes the group look weaker, so the mid-season pedigree anchor drops and
every other mid-season player re-prices — the weak ones up, the strong ones down, 43 of them. That was the
owner's call, and he took it. Everything else holds: the cohort guard still passes with room (the tightest
ratio actually eased), the board still balances to pick-1 = 3000, the book re-seals, and all five integrity
guards are green. No engine code was touched.
