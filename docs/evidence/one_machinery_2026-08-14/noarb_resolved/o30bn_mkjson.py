import json, os
H = '/home/user/afl-rl-engine/.claude/worktrees/agent-a14698ead2bf8585d/docs/evidence/one_machinery_2026-08-14/noarb_resolved'
SIT = json.load(open('/home/user/afl-rl-engine/.claude/worktrees/agent-a14698ead2bf8585d/docs/evidence/landing_29_2026-08-13/noarb_sitter_preview/MARGINS_SIT.json'))
RC = json.load(open(H + '/ROWCONTROL_30BN.json'))
LC = json.load(open(H + '/LAWCHECK_30BN.json'))

live = {
    ('allarm', 'PRIMARY  cohorts 2005-2023'): dict(yr={0: 1.0, 1: .8077, 2: .9737, 3: 1.0703, 4: 1.1291, 5: 1.1096}, apprec=-.1923, margin=.3323, arb=False),
    ('allarm', 'MODERN   cohorts 2019-2023'): dict(yr={0: 1.0, 1: .8225, 2: .9256, 3: .9794, 4: .9772, 5: 1.0345}, apprec=-.1775, margin=.3175, arb=False),
    ('legacy338', 'ALL picks 1-64'): dict(yr={0: 1.0, 1: 1.0730}, apprec=.0730, margin=.0670, arb=False),
    ('legacy338', 'picks 1-20'): dict(yr={0: 1.0, 1: 1.1218}, apprec=.1218, margin=.0182, arb=False),
    ('legacy338', 'picks 21-64'): dict(yr={0: 1.0, 1: .9996}, apprec=-.0004, margin=.1404, arb=False),
}
sit = {(r['instrument'], r['window']): r for r in SIT['readings'] if r['variant'] == 'SITALL'}

readings = []
for (inst, win), lv in live.items():
    s = sit.get((inst, win.replace('  cohorts', '  cohorts')))
    if s is None:
        s = next((v for (i, w), v in sit.items() if i == inst and w.split()[0] == win.split()[0]), None)
    readings.append(dict(
        instrument=inst, window=win, basis='year-0 = landed entry law (29C convention)',
        charge=0.14,
        LIVE_88ce647f=dict(year_paths_pct_of_entry={str(k): round(100 * v, 1) for k, v in lv['yr'].items()},
                           apprec_0_1=lv['apprec'], margin_v14=lv['margin'],
                           verdict='ARB' if lv['arb'] else 'no arb'),
        SITTER_LAW_PREVIEW_SITALL=(None if s is None else dict(
            year_paths_pct_of_entry={k: round(100 * v, 1) for k, v in s['yr'].items()},
            apprec_0_1=s['apprec'], margin_v14=s['margin'],
            verdict='ARB' if s['arb'] else 'no arb')),
        RESOLVED_CANDIDATE=dict(status='HALTED',
                                reason='ORDER 29C emitter replication proof refuses the year-0 column '
                                       'on this branch (43 of 89). PRE-EXISTING: reproduced with the '
                                       '30B-N dial OFF. See STOP_STEP3_YEAR0_BASIS.md.')))

out = dict(
    order='30B-N', brief='#334 comment 5310246218', prereg='PREREG_30BN.md',
    greenlit=False, pre_numeraire=True,
    headline='RESOLVED COLUMN HALTED — the year-0 basis is an owner word, not a seat choice.',
    caveats=['PRE-NUMERAIRE: Step 6 re-pin has not run; read the MOVEMENT not the level',
             'POOL beta PROVISIONAL: pool v0 cells are Step 4; pool sitter fade forced to D=1.0 (NOT derived)',
             'RUCK-HEAD DEFECT OPEN',
             'T4 (the OBJECT) OPEN: these tables price the v0 object, not entry_anchor',
             'the 11-15 bridge lane is a DECLARED BRIDGE, not a measurement',
             'beta(g) is NOT monotone: it rises 2.5->10.5 games before falling; carried, not patched'],
    halt=dict(where='Step 3, emit_matrix_29c.py replication proof',
              reproduce_exactly=43, of=89,
              dial_on_result='HALT exit=1', dial_off_result='HALT exit=1, identical mismatch list',
              caused_by_this_order=False,
              cause='ORDER 30B Step-1 positional v0 re-fit, commit 860d370, moved pvc_curve_v2.json '
                    'after DAY0_29B_FINAL.json was published on board 36d5dfc7',
              population_move=dict(wired_entrants_moved=46, wired_entrants_total=89,
                                   mean_abs_move_pct=17.941, min_pct=-10.975, median_pct=0.340, max_pct=455.815),
              emit_population=dict(rows=2643, mean_v0_old=518.18, mean_v0_new=519.00,
                                   pooled_denominator_move_pct=0.158, rows_moved=1441,
                                   rows_moved_pct=54.5, p05_pct=-5.92, median_pct=0.00, p95_pct=13.51),
              options=['A: keep year-0 on the frozen 29C landed entry law (preserves the common '
                       'denominator; reintroduces the MIXED-BASIS defect 29C closed)',
                       'B: move year-0 to the current re-fitted v0 (internally coherent; the '
                       'denominator moves for 54.5% of rows so the RESOLVED column is no longer the '
                       'same measurement as LIVE and SITALL; requires re-pointing RL_DAY0_FINAL, the '
                       'guard that is currently refusing)']),
    controls=dict(P1_dial_off='9298203135202a0c707bb0977ba38c31',
                  P2_preview_lane='6a392bca7ad0dee04a6b4f037c758f65',
                  P4_resolved_board_twice='d3c65bc46cebb656914cacb34a693b77',
                  wiring_proof=LC,
                  row_control=dict(derived_total=RC['derived_total'], wired_total=RC['wired_total'],
                                   max_abs_delta=RC['max_abs_delta'], verdicts=RC['verdicts'],
                                   by_lane={k: dict(n=v['n'], maxabs=v['maxabs']) for k, v in RC['by_lane'].items()})),
    current_board_levels=dict(note='LEVEL reading, pre-numeraire; NOT a no-arb reading',
                              preview_weight_v0_nojoin=679874, weight_v0_joined=667260,
                              additive_v0_nojoin=755464, RESOLVED_additive_v0_joined=715229,
                              RESOLVED_additive_anchor_joined=715377,
                              wired_board_total=RC['wired_total'],
                              lanes=dict(sitter=[89, 17243], thin=[99, 35470], bridge=[44, 29578], deep=[572, 632937])),
    arbitrage_counts=dict(LIVE='0 of 5', SITALL='3 of 5', RESOLVED='not readable'),
    readings=readings,
    provenance=dict(store='cb38ef1171dcf20aae66ebf12682be0d',
                    pvc_curve_v2='06146b00daf2043487f58a8b9f842a1e (MOVED at 860d370 - the cause)',
                    rl_model='14000af2a46f7a3c4cdfde303f5a1aff',
                    v0surf='5dd34ca82735f5c8f021b1c7320df8f8',
                    matrix_live='per_entrant_O25R4.json 3c6ffcde',
                    matrix_historical_print='per_entrant_O29B.json ca24a49a',
                    matrix_landed_law='per_entrant_O29CFINAL.json 6db06e40',
                    noarb_table_338='0f8220351c64c56ccfa90c60edcdfa5f (byte-unmodified)',
                    emit_matrix_29c='0c3efa545832dd1131bd2b403588af29 (byte-unmodified; it refused)',
                    standing_emitter='bffde2f786be85037483e9f5f1563068'),
    discipline='No instrument modified. No literal re-pointed. No margin tuned. The refusal was '
               'reproduced with the dial OFF before it was reported.')
json.dump(out, open(H + '/NOARB_RESOLVED.json', 'w'), indent=1, sort_keys=True)
print('wrote NOARB_RESOLVED.json')
