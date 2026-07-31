#!/usr/bin/env python3
"""L5 — THE DIAL CENSUS. #290, 2026-07-31.

THE GATE THIS SERVES (runbook L5): **zero rows of L0's canonical list left without a token.**
The denominator is L0's own count — 187 canonical rows — so "zero silent drops" is provable
rather than asserted.

HOW A ROW IS DISPOSITIONED. Exactly one of:

  * REACHED-BY-Lx   — another leg owns it. NOT an L5 token: it records WHICH leg, so the row is
                      accounted for without L5 claiming work it did not do.
  * one of the five widened L5 tokens, for rows no other leg reaches:
      RE-DERIVED · RETIRED-FROM-LIVE · RULED-EXEMPT · DOC-CORRECTED · DEFERRED-TO-ADOPTION

**UNCLEAR IS NOT A DISPOSITION** (lane B's own instruction). Every row the lanes left UNCLEAR
either resolves here by derivation record, or ESCALATES BY NAME into the escalations list.

WHY THE RULES ARE WRITTEN OUT PER ROW RATHER THAN INFERRED. L0 established that mechanical rules
over these lanes are not trustworthy: three defensible rules gave three different denominators,
and the cross-lane merges had to be hand-adjudicated. The lanes' own class labels are used here as
CORROBORATION, never as the rule — every disposition below is authored, and every one carries an
evidence pointer that can be argued with.
"""
import json, collections, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
L0 = os.path.join(HERE, '..', 'l0_canonical_adjudicated.json')

# ---------------------------------------------------------------------------------------------
# THE DISPOSITION TABLE. key = canonical row number (L0's own 1..187 ordering).
# value = (disposition, evidence pointer)
# ---------------------------------------------------------------------------------------------
D = {}


def put(rows, disp, ev):
    for r in rows:
        assert r not in D, 'row %d dispositioned twice' % r
        D[r] = (disp, ev)


# ---- REACHED BY L1 — the substrate flip: gamma, the ruled curve, E6 scale, the v0surf re-bake --
put([1, 2, 22, 23, 24, 28, 45, 46, 51],
    'REACHED-BY-L1', 'L1(a)/(b)/(c) + Addendum C.1-C.3; captured in L3_T1_state.diff (base 79ee8e5)')
put([15, 16, 17, 21, 78, 118, 119, 121, 122, 148, 149, 150, 151, 99],
    'REACHED-BY-L1', 'the FROZEN-RULER same-commit set + config_sha carriers, Addendum C.1/C.3')
put([75], 'REACHED-BY-L1', 'expected_boot is the boot identity manifest; C.1 moves it field-level')
put([27], 'REACHED-BY-L1', 'the hard pick-1 numeraire assertion — N14, the ruled numeraire primitive')

# ---- REACHED BY L2 — the par spine -----------------------------------------------------------
put([32, 33], 'REACHED-BY-L2', 'E3 per-season par keying + PAR_DUAL_RULE=primary; window word A')

# ---- REACHED BY L3 — the prior stack under S-1/S-2, and T1 -----------------------------------
put([39], 'REACHED-BY-L3', 'conditional_prior dials; T1 applied (N17) + the S-1/S-2 carry')

# ---- REACHED BY L4 — the retrains, the census, the stamps ------------------------------------
put([34], 'REACHED-BY-L4', 'cm_400: refit measured, NOT installed; frozen as bytes under R-A')
put([35], 'REACHED-BY-L4', 'q97m: --verify run (diverges); refit is BAKE-ONLY; frozen under R-A')
put([36], 'REACHED-BY-L4', 'peak_model_v4 retrained b763f59e -> f305fe53; frozen under R-A')
put([3], 'REACHED-BY-L4', 'pvc_snapshot co-emitted with the peak model 735d2dec -> ade79790')
put([9], 'REACHED-BY-L4', 'bust_prior_table: NO WRITER EXISTS — R-D docket, correcting the pinned '
                          '_fitted_note is a landing act')

# ---- REACHED BY L6 — convergence and the level re-measurement --------------------------------
put([69, 120], 'REACHED-BY-L6', 'POOL/MSD/SSP re-measured at the converged fixed point (seam word on D2)')
put([156, 157, 160], 'REACHED-BY-L6', 'G-Y0 is judged at the converged fixed point; the 2.000% bar')

# ---- REACHED BY L7 — gates and seals ----------------------------------------------------------
put([13, 19, 106], 'REACHED-BY-L7', 'F5 real assertion + its fail-closed sibling set; '
                                    'sealed_entrant_structure re-measured')
put([18], 'REACHED-BY-L7', 'the G-Y0 dated-exception ceiling_pct 3.50 is RETIRED at L7')
put([67], 'REACHED-BY-L7', 'forward_lens ForwardAuthorityError sites ride the F5 seal')

# ---- REACHED BY L8 / adoption — the owner's separate act -------------------------------------
put([73, 74, 102, 103, 104, 105, 107, 108, 109, 110, 126, 162, 167],
    'REACHED-BY-L8', 'the candidate board + the adoption set (adoption word · FHV word · relabels)')
put([127, 128], 'REACHED-BY-L8', 'FHV rationale + upgrade path ride the FHV word at adoption')
put([131, 132], 'REACHED-BY-L8', 'the five rendered SCAR->VOR relabels are the owner\'s separate act')

# ---- HISTORICAL-SEALED — the standing scope boundary ------------------------------------------
# Runbook scope, carried and not re-opened: "live pricing inputs re-derive; sealed historical
# records (lineage, round history, evidence trees) stay history." That is an owner-level scope
# word already on the record, so the token is RULED-EXEMPT and the evidence is the boundary itself.
SEALED = [54, 70, 77, 80, 81, 82, 83, 84, 85, 86, 90, 92, 95, 96, 97, 98, 100, 114, 115, 117,
          124, 125, 147, 159, 163, 172, 174, 175, 176, 179, 181]
put(SEALED, 'RULED-EXEMPT', 'sealed history — runbook scope boundary; C.2 forbids re-stamping it')
put([20], 'RULED-EXEMPT', 'present_lens_baseline is a sealed baseline; re-stamping it would assert '
                          'a past lens that did not hold')

# ---- THE LIVE-TAIL / SEALED-HISTORY BOUNDARY CALL — L5\'s own, per Addendum 3 + D4 -------------
put([88], 'DEFERRED-TO-ADOPTION', 'finalization_state: rounds 15-19 are sealed and NEVER move (C.2); '
                                  'the round-20 TAIL is live and its destination identities do not '
                                  'exist until the landing head — so the tail moves at adoption, not here')
put([89], 'DEFERRED-TO-ADOPTION', 'movers_R20 twin stale pins ride WITH the round-20 tail (D4): the '
                                  'config_sha re-stamp moves the hash but not those pins')

# ---- THE NAMED L5 DIALS — the rows no other leg reaches ---------------------------------------
put([25], 'RETIRED-FROM-LIVE', 'CE remnant: ALPHA=0.6 + legacy _ce(). alpha=1.0 is RULED (N6); the '
                               'CE aggregator is not on the ruled value path')
put([26], 'RETIRED-FROM-LIVE', 'CE remnant: PVC_ALPHA_LO/HI=0.6,0.8 + _alpha_pvc() — same ruling, '
                               'alpha=1.0 throughout')
put([29], 'RE-DERIVED', 'MA.REPL replacement bars move with the retrained band/peak substrate. '
                        'NAMED GAP: the deriving script is absent from the repo (lane A) — the bars '
                        'are carried, not regenerable. Escalated below.')
put([30], 'RE-DERIVED', 'EXP_PEAK_BASE / EXP_RETAIN / EXP_PICK_SLOPE floors sit on the value path and '
                        'move with the flipped substrate')
put([47], 'RE-DERIVED', 'RUC_PRIOR_CAP=1.4 + _ruc_prior_cap/_ruc_ceil — the ruck-cap bite check folds here')
put([48], 'RE-DERIVED', 'RUC_CEIL_REFPK=72 with RUC_CEIL_HEAD=0.80 — same cap family')
put([49], 'RE-DERIVED', 'R_SURF sit-out retention surface — value path')
put([50], 'RE-DERIVED', 'LAM_SIT — value path, same family as R_SURF')
put([60], 'RE-DERIVED', '_ABS_EFF absence age-effect curve + _ABS_L_REF=75.0 — value path')
put([61], 'RE-DERIVED', 'decliner-shed calibration LDECAY_G / FLAT_TOL_G')
put([64], 'RE-DERIVED', 'the W4 dial block — W4_CRED/KPFUP/FADE/OVPX/KPFSH')
put([65], 'RE-DERIVED', '_natcv / _natcv34 / PICKEQ / MECH_STATS')
put([56], 'RULED-EXEMPT', '_LSYM_SEAL r_pop/s are a SEAL over a sealed population, not a live dial')
put([11], 'RE-DERIVED', 'lti_return_table.json (store a2fbc9a0) — availability input, re-derives with '
                        'the store')

# ---- DOCUMENTATION-ONLY ROWS -------------------------------------------------------------------
put([136, 137, 138, 144, 145, 166, 186],
    'DOC-CORRECTED', 'prose/comment only: stale board narrative, name-uniqueness premise, history-card '
                     'scope note, dead constant + stale comment, extractor docstring, parity docstring, '
                     'workflow prose. Corrected in the landing set; no behaviour attached.')
put([135], 'DOC-CORRECTED', 'numeraire prose — restated to N14 (measured head primitive)')

# ---- NOT-LIVE ROWS -----------------------------------------------------------------------------
put([4], 'RETIRED-FROM-LIVE', 'pvc_fit_candidate: RL_PVCFIT=0 in the manifest, engine default 0 under '
                              'ruling R3, and rl_export carries an active R3 BAKE GUARD (L0 resolved '
                              'the lane A/B conflict this way)')
put([40], 'RETIRED-FROM-LIVE', 'par_redesign.BASE_RATE — not on the live path')
put([41], 'RETIRED-FROM-LIVE', 'par_redesign BETA_POS/MULT/TILT_CAP/WIDE — not on the live path')
put([42], 'RETIRED-FROM-LIVE', 'build_cohort_book.py — not on the live path')
put([59], 'RETIRED-FROM-LIVE', 'the retired saturating captain curve CAPT_GAIN/EXP/CAP')
put([68], 'RETIRED-FROM-LIVE', 'establishment-P surface pgrid.build — not on the live path')

# ---- RULED-CURRENT ROWS THAT NEED NO MOVE ------------------------------------------------------
CURRENT = [5, 12, 14, 37, 43, 44, 52, 53, 57, 58, 66, 76, 79, 93, 94, 101, 111, 112, 113, 116,
           134, 139, 140, 141, 142, 143, 146, 152, 153, 154, 155, 158, 161, 164, 165, 168, 169, 170,
           171, 177, 178, 180, 182, 183, 184, 185, 187]
CURRENT = [r for r in CURRENT if r not in D]
put(CURRENT, 'RULED-EXEMPT', 'ALREADY-RULED-CURRENT: RULED-CURRENT at L0 and unmoved by any leg — the '
                             'row already states the ruled basis, so there is nothing to re-derive')

# ---- THE UNCLEARS THAT RESOLVE HERE -------------------------------------------------------------
put([6], 'RULED-EXEMPT', 'national_draft_last_pick: a structural domain fact (ND_CURVE_LAST=64), not a '
                         'dial; the split law row 66 carries it')
put([7], 'RULED-EXEMPT', 'rl_passmark: a passmark table read at import, unchanged by the substrate flip')
put([8], 'RULED-EXEMPT', 'params.json: engine parameters superseded by the config manifest, which the '
                         'L1 flip re-stamps')
put([10], 'RE-DERIVED', 'ycred_table — credential table on the value path, moves with the substrate')
put([31], 'RE-DERIVED', 'BETA_POS / ICPT_POS position intercepts — value path')
put([38], 'RE-DERIVED', 'REPL_DROP_PTS=3 (RL_REPL_DROP) rides MA.REPL, row 29')
put([55], 'RE-DERIVED', 'the live LENS posture dials move with the flipped value path')
put([62], 'RULED-EXEMPT', 'evidence-weight pins _EVW_R=0.11 etc are the blend weights the par surface '
                          'is read through — pinned by ruling, not re-derived here')
put([63], 'RE-DERIVED', '_L3_AY s(age) persistence + _SAGE29_VAL — age curve on the value path')
put([129], 'RULED-EXEMPT', 'delta-base default — a UI display default, no pricing basis attached')
put([130], 'RULED-EXEMPT', 'owner anchor manifest — owner-set anchors, not a derived dial')
put([173], 'RULED-EXEMPT', 'monotonicity tamper constant — a test fixture constant whose job is to '
                           'break monotonicity deliberately; it must NOT track the curve')

# ---- REMAINING ROWS ------------------------------------------------------------------------------
put([71], 'REACHED-BY-L6', 'the walk-forward book/matrix rebuilds on the converged substrate')
put([72], 'REACHED-BY-L8', 'export attribution sidecar is the mover-attribution channel set')
put([87], 'REACHED-BY-L4', 'sibling_repin sidecar resolves via this rebuild — its first lawful sibling build')
put([91], 'RULED-EXEMPT', 'value history baseline — sealed history')
put([123], 'REACHED-BY-L1', 'contract self-description moves with pvc_provenance + contract_sha256')
put([133], 'REACHED-BY-L8', 'trade-desk pick domain — #292 landed the fix; the ladder itself moves at adoption')


# ---------------------------------------------------------------------------------------------
# ESCALATIONS BY NAME. A disposition that carries a gap is not a closed row — lane B's instruction
# is "resolve by derivation record, or ESCALATE BY NAME". These are dispositioned AND escalated.
# ---------------------------------------------------------------------------------------------
ESCALATIONS = [
 {'row': 29, 'what': 'MA.REPL replacement bars',
  'gap': 'the deriving script is ABSENT from the repo (lane A). The bars are carried forward, not '
         'regenerable. Same class as the three reachability failures already on the record '
         '(v0surf bytes, the ND matrix, the derivation lane).',
  'ask': 'either the deriving script is recovered and committed, or the bars are frozen as bytes '
         'with provenance under the R-A pattern.'},
 {'row': 9, 'what': 'bust_prior_table.json',
  'gap': 'NO WRITER EXISTS anywhere in the tree, and the pinned expected_boot._fitted_note claims '
         'build_peak_model_v4.py regenerates it at a bake. Measured: that file READS it at line 16 '
         'and never writes it.',
  'ask': 'correcting a pinned note is a LANDING act — ratified as a docket by R-D, carried here.'},
 {'row': 34, 'what': 'cm_400.pkl (the band)',
  'gap': 'a fresh refit does not reproduce the shipped artifact (3c568d86 vs 9804bc48, like-for-like) '
         'so the shipped band is not regenerable from the tree; frozen as bytes under R-A.',
  'ask': 'no action at L5 — the freeze is the remedy; naming it so it is not read as resolved.'},
]


def main():
    rows = json.load(open(L0))['rows']
    n = len(rows)
    missing = [i for i in range(1, n + 1) if i not in D]
    out = []
    for i, r in enumerate(rows, 1):
        disp, ev = D.get(i, ('** NO TOKEN **', ''))
        out.append({'row': i, 'key': r['key'], 'lanes': r.get('lanes'),
                    'l0_classes': sorted(r.get('classes', {})),
                    'disposition': disp, 'evidence': ev})
    tally = collections.Counter(o['disposition'] for o in out)
    print('L5 DIAL CENSUS — denominator is L0\'s own count')
    print('  canonical rows : %d' % n)
    print('  dispositioned  : %d' % (n - len(missing)))
    print('  WITHOUT A TOKEN: %d   %s' % (len(missing), missing if missing else '<- the gate'))
    print()
    for k, v in sorted(tally.items(), key=lambda kv: (-kv[1], kv[0])):
        print('   %-22s %3d   %5.1f%%' % (k, v, 100.0 * v / n))
    # RULED-EXEMPT is the widest token and would hide two different things behind one word.
    # Split it, because a census whose largest bucket is ambiguous is not a census.
    ex_current = sum(1 for o in out if o['disposition'] == 'RULED-EXEMPT'
                     and o['evidence'].startswith('ALREADY-RULED-CURRENT'))
    ex_sealed = sum(1 for o in out if o['disposition'] == 'RULED-EXEMPT'
                    and o['evidence'].startswith('sealed history'))
    ex_other = tally['RULED-EXEMPT'] - ex_current - ex_sealed
    print()
    print('  RULED-EXEMPT splits — the token is one word for three situations:')
    print('     already-ruled-current  %3d   (the row already states the ruled basis)' % ex_current)
    print('     sealed history         %3d   (the standing scope boundary; C.2 forbids re-stamping)' % ex_sealed)
    print('     exempt, case by case   %3d   (each carries its own evidence pointer)' % ex_other)
    l5 = sum(v for k, v in tally.items() if not k.startswith('REACHED-BY'))
    print()
    print('  L5-OWNED (the five tokens)   : %d of %d = %.1f%%' % (l5, n, 100.0 * l5 / n))
    print('  owned by another leg         : %d of %d = %.1f%%' % (n - l5, n, 100.0 * (n - l5) / n))
    print()
    print('  ESCALATED BY NAME            : %d' % len(ESCALATIONS))
    for e in ESCALATIONS:
        print('     row %-4d %s' % (e['row'], e['what']))
    unresolved = [o for o in out if 'UNCLEAR' in o['l0_classes'] and o['disposition'].startswith('**')]
    print('  L0 UNCLEAR rows resolved     : %d of %d' %
          (sum(1 for o in out if 'UNCLEAR' in o['l0_classes']) - len(unresolved),
           sum(1 for o in out if 'UNCLEAR' in o['l0_classes'])))
    json.dump(out, open(os.path.join(HERE, 'l5_dispositions.json'), 'w'), indent=1)
    assert not missing, 'GATE FAILS: %d rows carry no token: %s' % (len(missing), missing)
    print('\n  GATE: zero rows without a token — PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
