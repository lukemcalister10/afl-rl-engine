# DIRECTIVE CALC PROGRESS — build seat computation agent
Started 2026-08-10. READ-ONLY. Repo /home/user/afl-rl-engine @ 37bad1a.

## Input verification
- [x] board data/rl_build/rl_app_data.json md5 = 4b448a821f54180182637983f7a26a9d — MATCHES frozen.
- [x] store: NOT at data/rl_players_store.json (does not exist). Located as
      engine/rl_after/rl_model_data.json md5 = d9a24282357cf3083b1640466e3ecd83 — matches
      expected prefix d9a24282. Corroborated by
      docs/evidence/dob_write_2026-08-10/md5_before_after.txt (artifact named explicitly)
      and docs/evidence/g1_never_rises_2026-08-10/summary.json base.store.
- [x] engine engine/rl_after/rl_model.py (1469 lines)
- [x] draft docs/directives/DRAFT_composition_directive_2026-08-10.md — READ
- [!] stage-5 evidence dir docs/evidence/act_334B_2026-08-07/stage5/ DOES NOT EXIST.
      The described file (dict {meta,recs}, recs with key/player/pos/type/pick/year/v0/vpath)
      is docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json
      md5 5fb617d09cd8341d9f36b90a1827e2e5, n_records 2645, meta.store_md5 37ced3ce
      (i.e. emitted on a PRE-DOB/PRE-G1 store — flag for discrepancies).
- [x] board total after G1 = 761,574 (delta -13 from 761,587) per g1 summary.json.

## TODO
- [ ] find par surface in rl_model.py
- [ ] find year-1+ ND ceiling/cap object (ruling 3.8)
- [ ] find v0 surface / entry anchor
- [ ] TASK 1 rows
- [ ] TASK 2 magnitudes table
- [ ] TASK 3 conservation sums

## Engine reproduction (2026-08-10)
- Engine LOADS and runs. Pinned venv /root/rl_venv312 (py3.12.3, numpy 2.4.4, sklearn 1.8.0).
- MUST run under config_manifest.enforce('gate') -> RL_GAMMA=1.0 (manifest), NOT the 0.85 in
  START_HERE §2. Only gate mode reproduces the frozen v0surf signature
  6ef67f07db98258786189a6316ce24f9 (the one in data/v0surf.pkl and in the G1 summary).
  Dev-shell 0.85 HALTS on the v0surf frozen-signature guard (sig e68e2f7f...).
- Board GAMMA field == 1.0, confirming the shipped board is the gate-mode build.
- Board sum(active.v) = 761,574 EXACT match to the filed board total.
- Currency: ev() engine currency; board v = ev / 1.0524 (_PL_F). Verified on Mraz 3741/3555.
- Loader: scratchpad/engine_load.py

## Objects located (file:line)
- par surface (LIVE value path): par_at(F,pos,pick,T) engine/forward_valuation/par_build.py:255
  exposed PR.par_at engine/forward_valuation/par_redesign.py:68; consumers _par_prior
  engine/rl_after/_merged_recover.py:306-308 and local `par` at :1925.
- par surface (rl_model.py's own): expected_c(g,pk,s) engine/rl_after/rl_model.py:370 on
  expected() :221 ("below-par" :1104, "position+experience bar" :1094). Both readings computed.
- draft-age integer: _ageR  _merged_recover.py:1271 ; age->tenure bridge eff_ten :309-311.
- entry anchor: entry_anchor() :1761-1765 -> v0_start() :1737-1741 (D14 V0*(pos,draft-age,pick)).
- current expectation e: ev(p,Y) :1895-1937.
- cap candidates: entry_anchor (chosen, from the w=0 identity); R_SURF :1104-1125 + sitout_ev
  :1847-1852; RUC_PRIOR_CAP :1138 / _ruc_ceiling :1195-1201; staleness/mediocre :1929-1936.
  NO object in the engine is literally "the year-1+ ND ceiling" -- see DISCREPANCIES.

## Results
- Landing re-run (current matrix): mean ev/entry_anchor over ND in-curve class 2025, n=58 = 1.0194
  (filed 1.0248). played-only n=34 = 1.2742. sum/sum = 1.0842.
- mean w over year-1 cohort: 0.2271 (all 58) / 0.3873 (played only).
- Board total sum(active.v) = 761,574. Sigma entry_anchor board ccy = 581,904.5 (804 rows).
- Scripts: engine_load.py, item_c_rows.py, cohort_landing.py, sums.py, par_alt.py,
  find_rows.py, find_rows2.py, sig_debug.py, probe_board.py
- STATUS: TASK 1/2/3 complete. No repo file touched. Nothing committed, pushed or posted.
