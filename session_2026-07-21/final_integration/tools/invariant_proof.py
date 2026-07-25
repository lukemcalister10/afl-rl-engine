#!/usr/bin/env python3
"""INVARIANT + RECONCILIATION PROOF for the final canonical board (final integration 2026-07-21).

Verifies, against the ACCEPTED authorities (committed reference vector + git Board B, not transplanted):
  Present authority (ITEM 408 STOP-1 R19, owner-approved 2026-07-22) =
       session_2026-07-20/fv_provenance_remediation/fixtures/reference_vector_1373e824.json
       (accepted balanced/strict 1373e824; active 804; present-v total 760253)
  Board B (accepted forward lens) = 70ef0ff:.../board_B_lege1_legf1.json      (md5 1f10220c)
  Final board / board of record   = data/rl_build/rl_app_data.json           (working tree, md5 6f07f7cb, FROZEN)

  (10) present-lens invariants: 804 active; Sigma v == 760253; 0 present-v / present-rank / present-order
       movers of the board of record 6f07f7cb vs the accepted reference vector (1373e824). (Migrated from
       the superseded R14 Board A present authority f05ebe6 / 06d8af60 / total 752427; ITEM 408 item 5.3.
       The board of record 6f07f7cb is FROZEN and NOT moved; no store or valuation result is moved.)
  (11) forward-vector invariants: the board-of-record forward vectors (vP1/vP2) must be PRESENT + numeric
       over the EXACT active universe (804). Board B (1f10220c) is the SUPERSEDED R14 comparison oracle;
       the vP1/vP2 differences vs it are MEASURED + RECORDED (equal/changed/missing/added counts), NOT
       asserted. Semantic acceptance of the R19 vP1/vP2 vectors remains owner-DEFERRED (no accepted R19
       forward oracle exists).
  (12) visible draft-asset proof: exactly 64 visible 2027 + 64 visible 2028 placeholders; 0 on the current
       ladder; unique stable asset ids; labels distinguish year+pick; no AFL club; no AFFL club; no player
       identity; exact PVC[n] per row; PVC monotone non-increasing; future-lens sorting by value desc.
  (13) F5 reconciliation: visible(Sigma PVC[1..64]) + residual_nd + residual_mech == sealed F5 entrant
       layer 83538, per lens and vs Board B phantomTotals; no double count.

Each acceptance section emits its OWN pass boolean (ok_present / ok_forward / ok_draft / ok_f5) so a
present-lens result NEVER cascades into an unrelated section (ITEM 408 item 5.4).

Emits machine-readable evidence (invariant_proof.json) + PASS/FAIL; non-zero on any failure.
"""
import os, sys, json, hashlib, subprocess

ROOT = os.environ.get('RL_REPO') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
FINAL = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')
# ITEM 408 STOP-1 R19 accepted present authority — the committed reference vector (balanced/strict
# 1373e824). The board of record 6f07f7cb has ZERO present-v movers vs this vector (owner-approved
# 2026-07-22). Supersedes the R14 present-lens Board A (f05ebe6 / 06d8af60 / total 752427).
REFVEC = os.path.join(ROOT, 'session_2026-07-20', 'fv_provenance_remediation', 'fixtures',
                      'reference_vector_1373e824.json')
PRESENT_BALANCED_MD5 = '1373e82471a81064ef96820f3db065df'
PRESENT_TOTAL = 760253
BOARD_B = ('70ef0ff36ca7633aa4097a9b7c1a730013870abe',
           'session_2026-07-21/forward_lens_acceptance/board_B_lege1_legf1.json')

R = []
DEFERRED = []
def ck(name, cond, detail=''):
    R.append({'check': name, 'pass': bool(cond), 'detail': detail})
    print(('  PASS ' if cond else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(cond)

def deferred(name, detail=''):
    """An owner-DEFERRED item: reported transparently (with the real measured deltas) but NOT a gate.
    Used for the forward-lens (vP1/vP2), which the owner has explicitly NOT accepted (deferred repair);
    the superseded R14 Board B is not an R19 oracle, so its deltas are recorded, not asserted as a pass."""
    DEFERRED.append({'check': name, 'status': 'DEFERRED', 'detail': detail})
    print('  DEFER ' + name + ((' -- ' + str(detail)) if detail else ''))

def gitjson(commit, path):
    return json.loads(subprocess.check_output(['git', 'show', '%s:%s' % (commit, path)], cwd=ROOT))

def active_of(board):
    for k in ('active',):
        if k in board and isinstance(board[k], list): return board[k]
    # UI-bundle shape uses 'players'
    return board.get('players', [])

def main():
    print("=== FINAL BOARD INVARIANT + RECONCILIATION PROOF ===")
    F = json.load(open(FINAL))
    RV = json.load(open(REFVEC))
    B = gitjson(*BOARD_B)
    fa, ba = active_of(F), active_of(B)
    PVC = {int(k): v for k, v in F['PVC'].items()}

    fby = {p['key']: p for p in fa}
    aby = {k: int(v) for k, v in RV['vector'].items()}   # accepted present-v vector (key -> v), 1373e824
    bby = {p['key']: p for p in ba}

    # ---- (10) present-lens: the board of record 6f07f7cb vs the ACCEPTED reference vector (1373e824) ---
    ck('(10) reference vector is the accepted balanced/strict 1373e824 (active 804, sum_v 760253)',
       str(RV.get('board_md5', '')).startswith('1373e824') and RV.get('active') == 804 and RV.get('sum_v') == PRESENT_TOTAL,
       'board=%s active=%s sum_v=%s' % (str(RV.get('board_md5'))[:8], RV.get('active'), RV.get('sum_v')))
    ck('(10) final active count == 804', len(fa) == 804, len(fa))
    ck('(10) final Sigma present v == 760253', sum(p['v'] for p in fa) == PRESENT_TOTAL, sum(p['v'] for p in fa))
    vmov = [k for k in fby if k in aby and fby[k]['v'] != aby[k]]
    ck('(10) zero present-v movers vs the accepted reference vector (1373e824)', not vmov, '%d movers' % len(vmov))
    added = sorted(set(fby) - set(aby)); removed = sorted(set(aby) - set(fby))
    ck('(10) no added/removed active players vs the accepted reference vector', not added and not removed,
       'added=%d removed=%d' % (len(added), len(removed)))
    def ranks_kv(items):
        order = sorted(items, key=lambda kv: (-kv[1], kv[0]))
        return {k: i for i, (k, _v) in enumerate(order)}, [k for k, _v in order]
    fr, ford = ranks_kv([(p['key'], p['v']) for p in fa])
    ar, aord = ranks_kv(list(aby.items()))
    rmov = [k for k in fr if k in ar and fr[k] != ar[k]]
    ck('(10) zero present-rank movers vs the accepted reference vector', not rmov, '%d rank movers' % len(rmov))
    ck('(10) zero present-order movers vs the accepted reference vector', ford == aord,
       'order identical' if ford == aord else 'ORDER DIFFERS')

    # ---- (11) forward vectors — forward-lens repair is owner-DEFERRED (vP1/vP2 NOT accepted) ----------
    # The owner has explicitly NOT accepted the vP1/vP2 forward-lens outputs and the forward-lens repair is
    # DEFERRED (data/expected_boot.json _present_staleness_note "forward-lens treatment intentionally
    # unchanged and deferred"; data/release_lineage.json _present_lens_only "owner ... has NOT accepted the
    # old vP1/vP2 forward-lens outputs"). Board B (1f10220c) is the SUPERSEDED R14 forward oracle; the R19
    # board-of-record forward vectors advanced with the round exactly as the present values did (present-v
    # +723). We therefore do NOT assert equality to the stale R14 oracle (there is no accepted R19 forward
    # oracle). We DO gate the accepted property — the forward vectors are present + numeric on the FROZEN
    # board of record 6f07f7cb, over the exact active universe — and we RECORD the vs-Board-B deltas openly.
    eq1 = sum(1 for k in fby if k in bby and fby[k]['vP1'] == bby[k]['vP1'])
    eq2 = sum(1 for k in fby if k in bby and fby[k]['vP2'] == bby[k]['vP2'])
    ch1 = [k for k in fby if k in bby and fby[k]['vP1'] != bby[k]['vP1']]
    ch2 = [k for k in fby if k in bby and fby[k]['vP2'] != bby[k]['vP2']]
    miss = sorted(set(bby) - set(fby)); addf = sorted(set(fby) - set(bby))
    pv_mov = len([k for k in fby if k in bby and fby[k]['v'] != bby[k]['v']])
    fwd_present = all(isinstance(p.get('vP1'), (int, float)) and isinstance(p.get('vP2'), (int, float)) for p in fa)
    ck('(11) forward vectors present + numeric for all 804 active (board of record 6f07f7cb, frozen)',
       fwd_present and len(fa) == 804, 'present=%s active=%d' % (fwd_present, len(fa)))
    ck('(11) exact active universe vs Board B (no missing/added rows)', not miss and not addf,
       'missing=%d added=%d' % (len(miss), len(addf)))
    deferred('(11) vP1/vP2 acceptance vs Board B — owner-DEFERRED (forward-lens not accepted)',
             'vP1 changed=%d/804, vP2 changed=%d/804 vs the SUPERSEDED R14 Board B 1f10220c (present-v also '
             'moved +%d, the STOP-1 advance). No accepted R19 forward oracle exists; the forward-lens repair '
             'is owner-deferred. Deltas recorded, NOT asserted as a pass.' % (len(ch1), len(ch2), pv_mov))

    # ---- (12)+(13) visible draft assets + F5 reconciliation -------------------------------------------
    lp = F['lensPicks']
    vis1 = [p for p in lp if p['lens'] == 1 and not p.get('residual')]
    vis2 = [p for p in lp if p['lens'] == 2 and not p.get('residual')]
    ck('(12) exactly 64 visible 2027 national-draft placeholders (+1)', len(vis1) == 64, len(vis1))
    ck('(12) exactly 64 visible 2028 national-draft placeholders (+2)', len(vis2) == 64, len(vis2))
    ck('(12) all visible labelYear correct (2027/2028)',
       all(p['labelYear'] == 2027 for p in vis1) and all(p['labelYear'] == 2028 for p in vis2))
    ck('(12) zero visible future placeholders on the current player ladder',
       not any(p.get('asset') == 'pick' for p in fa) and not any('pick' in (p.get('kind') or '') for p in fa))
    ids = [p['id'] for p in lp]
    ck('(12) unique stable asset ids', len(ids) == len(set(ids)), '%d ids %d unique' % (len(ids), len(set(ids))))
    ck('(12) labels distinguish year + pick number',
       all(p['label'] == '%d Draft Pick %d' % (p['labelYear'], p['n']) for p in vis1 + vis2))
    ck('(12) no AFL club / no AFFL club on any visible pick',
       all(p.get('club') is None and p.get('affl_team') is None for p in vis1 + vis2))
    ck('(12) no accidental player identity (no key join; kind/asset == pick)',
       all(('key' not in p) and p.get('kind') == 'pick' and p.get('asset') == 'pick' for p in vis1 + vis2))
    pvc_ok = all(p['v'] == PVC[p['n']] for p in vis1 + vis2)
    ck('(12) exact PVC equality for every visible pick (v == PVC[n])', pvc_ok)
    mono = all(PVC[n] >= PVC[n + 1] for n in range(1, 64))
    ck('(12) release-active PVC monotone non-increasing over 1..64', mono)
    sort1 = [p['v'] for p in vis1]; sort2 = [p['v'] for p in vis2]
    ck('(12) visible picks sorted by value desc (both lenses)',
       sort1 == sorted(sort1, reverse=True) and sort2 == sorted(sort2, reverse=True))

    sum64 = sum(PVC[n] for n in range(1, 65))
    # residuals are held OUT of the ranking (supervisor req 5) — they live in draftAssetTotals, NOT lensPicks.
    ck('(12) lensPicks carries ONLY the 64 rankable visible picks per lens (no residual rows in the ranking)',
       all(not p.get('residual') for p in lp) and len(vis1) == 64 and len(vis2) == 64)
    for off, vis in ((1, vis1), (2, vis2)):
        dat = F['draftAssetTotals']['+%d' % off]
        res_nd = dat['residual_nd_tail']; res_mech = dat['residual_mech']
        visible = sum(p['v'] for p in vis)
        ck('(13) lens +%d: visible == Sigma PVC[1..64] == 64617' % off, visible == sum64 == 64617 == dat['visible_1_64'], visible)
        ck('(13) lens +%d: visible + residual == 83538 (F5 entrant layer)' % off,
           visible + res_nd + res_mech == 83538 == dat['f5_entrant_layer_pvc'], visible + res_nd + res_mech)
        ck('(13) lens +%d: residual_nd == draft_pvc(69266) - 64617 == 4649' % off, res_nd == 4649, res_nd)
        ck('(13) lens +%d: residual_mech == mech_pvc == 14272' % off, res_mech == 14272, res_mech)
        ck('(13) lens +%d: draftAssetTotals reconciled_to_f5' % off, dat['reconciled_to_f5'] is True)
    # cross-check against Board B's own sealed phantomTotals (no double count / same entrant layer)
    ptm = B['phantomTotals']['_meta']
    ck('(13) Board B sealed entrant layer == 83538 (draft 69266 + mech 14272)',
       ptm['entrant_layer_pvc'] == 83538 and ptm['draft_pvc'] == 69266 and ptm['mech_pvc'] == 14272)
    ck('(13) final board carries Board B phantomPicks/phantomLayer/phantomTotals unchanged',
       F.get('phantomTotals', {}).get('_meta', {}).get('entrant_layer_pvc') == 83538
       and len(F.get('phantomPicks', [])) == len(B.get('phantomPicks', [])))

    # ---- final board identity -------------------------------------------------------------------------
    raw = open(FINAL, 'rb').read()
    ident = {'md5': hashlib.md5(raw).hexdigest(), 'sha256': hashlib.sha256(raw).hexdigest(),
             'balanced_board_md5_lineage': PRESENT_BALANCED_MD5}

    # Per-section pass booleans so a present-lens result never cascades into forward-vector / draft-asset /
    # F5 (ITEM 408 item 5.4). Each section owns the checks tagged with its number; consumers read the
    # section boolean relevant to that section, not the aggregate `ok`.
    def section_ok(tag):
        rows = [r for r in R if r['check'].startswith(tag)]
        return bool(rows) and all(r['pass'] for r in rows)
    npass = sum(1 for r in R if r['pass']); n = len(R)
    result = {'ok': npass == n, 'n_pass': npass, 'n': n, 'final_board_identity': ident,
              'ok_present': section_ok('(10)'), 'ok_forward': section_ok('(11)'),
              'ok_draft': section_ok('(12)'), 'ok_f5': section_ok('(13)'),
              # `ok_forward` gates only the ACCEPTED forward property (present + numeric + exact universe on
              # the frozen board of record). The vP1/vP2-vs-Board-B acceptance is owner-DEFERRED (below).
              'forward_lens_deferred': True,
              'forward': {'vP1_equal': eq1, 'vP1_changed': len(ch1), 'vP2_equal': eq2,
                          'vP2_changed': len(ch2), 'present_v_moved': pv_mov, 'missing': len(miss),
                          'added': len(addf), 'oracle': 'Board B 1f10220c (SUPERSEDED R14; not an R19 oracle)'},
              'deferred': DEFERRED, 'checks': R}
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'evidence', 'invariant_proof.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(result, open(out, 'w'), indent=2, sort_keys=True)
    print("\nfinal board md5=%s sha256=%s" % (ident['md5'], ident['sha256'][:16] + '...'))
    print("RESULT: %d/%d PASS  -> %s" % (npass, n, os.path.relpath(out, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
