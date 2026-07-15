# PLAN — RE-ENTRY TRIO store correction (item 108a) · 2026-07-15

**Base pin (STRICT):** rl_model-pin head `1073f6336ba492316f3921776dc44f41d3ecbefb`
(`claude/rl-model-pin-assertion-sg5hxv`, ls-remote verified). Branch re-rooted onto it; the register
docs live on main and reconcile at promotion (item 142 caveat). Base green: engine `fc7045d6`, store
`340a7a32`, board `dc43d602`, config `c2d233ae`.

**Ruling:** record the LATER (SSP re-entry) entry onto the ONE authored store (SSI: change THE SOURCE)
for the three "known exceptions" to the §45 initial-entry law. Fields per item 17(ii): type=SSP +
re-entry year + pick None (+ `_pickless` True, `_draft` SSP to mirror a native SSP record).

| player | before | after |
|---|---|---|
| Flynn Perez | ND p35 (2019) | SSP 2025, pick None |
| Lachlan McAndrew | MSD p12 (2021) | SSP 2024, pick None |
| Mark Keane | IRE (2018) | SSP 2022, pick None |

**Owner ruling (2026-07-15):** after the HALT report showed the measured effect (106 movers, all
McAndrew via `PICKEQ['MSD']` 60→90; Perez/Keane 0), the owner ruled **"proceed full trio, store-only."**
The MSD-pedestal reprice rides as the accepted mechanical consequence. Engine stays UNTOUCHED (no guard
added to hold McAndrew out of the pickless pedestal — that was option C, declined).

**Fence:** store (`rl_model_data.json`) · board + `.srcmd5` · `data/expected_boot.json` ·
`data/book_stable_seal.json` (re-seal) · gates snapshot · `session_2026-07-15/reentry_trio/`.
NO engine pricing-code edits.

**Steps:**
1. Edit source store (3 rows). Store `340a7a32 → b1fd0bce`.
2. Re-pin `expected_boot` store + `_reentry_trio_note`; bootstrap (Guard 5 green vs new pin).
3. Rebuild board (RL_CONFIG_MODE=bake). Board `dc43d602 → 800d0399`. Copy board + `.srcmd5` to
   `data/rl_build/` + shipped; re-pin `expected_boot` board (engine_head UNCHANGED).
4. Re-seal the walk-forward book (engine unchanged, store moved → MSD rows move in the book).
5. Five guards from a fresh bootstrap: 1–3 + F1/F2 (`one_source_selftest.py`), 4 correction-canary
   (`guard_correction_canary.py`, sentinel josh-ward), 5 boot-store (`boot_guard.py`).
6. Ship gates (`ship_gates_check.py`) → LOG + snapshot + report committed. G-COHORT y4/y5/y6 vs BOTH
   1.30 and 1.335. PICK 1 = 3000.
7. AFFECTED_ROWS (done), VALUE_FLOW, RETURN. Commit + push + PR.
