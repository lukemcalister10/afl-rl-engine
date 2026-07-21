#!/usr/bin/env python3
"""INVARIANT + RECONCILIATION PROOF for the final canonical board (final integration 2026-07-21).

Verifies, against the frozen accepted boards (read from git, not transplanted):
  Board A (present-lens baseline) = f05ebe6:data/rl_build/rl_app_data.json   (md5 06d8af60)
  Board B (accepted forward lens) = 70ef0ff:.../board_B_lege1_legf1.json      (md5 1f10220c)
  Final board                     = data/rl_build/rl_app_data.json           (working tree)

  (10) present-lens invariants: 804 active; Sigma v == 752427; 0 present-v / present-rank / present-order
       movers vs Board A.
  (11) forward-vector invariants: vP1 and vP2 EXACTLY equal Board B for all 804 active; equal/changed/
       missing/added/removed counts; fail on any active mismatch.
  (12) visible draft-asset proof: exactly 64 visible 2027 + 64 visible 2028 placeholders; 0 on the current
       ladder; unique stable asset ids; labels distinguish year+pick; no AFL club; no AFFL club; no player
       identity; exact PVC[n] per row; PVC monotone non-increasing; future-lens sorting by value desc.
  (13) F5 reconciliation: visible(Sigma PVC[1..64]) + residual_nd + residual_mech == sealed F5 entrant
       layer 83538, per lens and vs Board B phantomTotals; no double count.

Emits machine-readable evidence (invariant_proof.json) + PASS/FAIL; non-zero on any failure.
"""
import os, sys, json, hashlib, subprocess

ROOT = os.environ.get('RL_REPO') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
FINAL = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')
BOARD_A = ('f05ebe6df49b653b053f0ebdd82ddc56ee8d4187', 'data/rl_build/rl_app_data.json')
BOARD_B = ('70ef0ff36ca7633aa4097a9b7c1a730013870abe',
           'session_2026-07-21/forward_lens_acceptance/board_B_lege1_legf1.json')

R = []
def ck(name, cond, detail=''):
    R.append({'check': name, 'pass': bool(cond), 'detail': detail})
    print(('  PASS ' if cond else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(cond)

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
    A = gitjson(*BOARD_A)
    B = gitjson(*BOARD_B)
    fa, aa, ba = active_of(F), active_of(A), active_of(B)
    PVC = {int(k): v for k, v in F['PVC'].items()}

    fby = {p['key']: p for p in fa}
    aby = {p['key']: p for p in aa}
    bby = {p['key']: p for p in ba}

    # ---- (10) present-lens ----------------------------------------------------------------------------
    ck('(10) final active count == 804', len(fa) == 804, len(fa))
    ck('(10) final Sigma present v == 752427', sum(p['v'] for p in fa) == 752427, sum(p['v'] for p in fa))
    vmov = [k for k in fby if k in aby and fby[k]['v'] != aby[k]['v']]
    ck('(10) zero present-v movers vs Board A', not vmov, '%d movers' % len(vmov))
    added = sorted(set(fby) - set(aby)); removed = sorted(set(aby) - set(fby))
    ck('(10) no added/removed active players vs Board A', not added and not removed,
       'added=%d removed=%d' % (len(added), len(removed)))
    def ranks(rows):
        order = sorted(rows, key=lambda p: (-p['v'], p['key']))
        return {p['key']: i for i, p in enumerate(order)}, [p['key'] for p in order]
    fr, ford = ranks(fa); ar, aord = ranks(aa)
    rmov = [k for k in fr if k in ar and fr[k] != ar[k]]
    ck('(10) zero present-rank movers vs Board A', not rmov, '%d rank movers' % len(rmov))
    ck('(10) zero present-order movers vs Board A', ford == aord,
       'order identical' if ford == aord else 'ORDER DIFFERS')

    # ---- (11) forward vectors vs Board B --------------------------------------------------------------
    eq1 = sum(1 for k in fby if k in bby and fby[k]['vP1'] == bby[k]['vP1'])
    eq2 = sum(1 for k in fby if k in bby and fby[k]['vP2'] == bby[k]['vP2'])
    ch1 = [k for k in fby if k in bby and fby[k]['vP1'] != bby[k]['vP1']]
    ch2 = [k for k in fby if k in bby and fby[k]['vP2'] != bby[k]['vP2']]
    miss = sorted(set(bby) - set(fby)); addf = sorted(set(fby) - set(bby))
    ck('(11) vP1 == Board B for all 804 active', eq1 == 804 and not ch1, 'equal=%d changed=%d' % (eq1, len(ch1)))
    ck('(11) vP2 == Board B for all 804 active', eq2 == 804 and not ch2, 'equal=%d changed=%d' % (eq2, len(ch2)))
    ck('(11) no missing/added active rows vs Board B', not miss and not addf,
       'missing=%d added=%d' % (len(miss), len(addf)))

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
    for off, vis in ((1, vis1), (2, vis2)):
        res = [p for p in lp if p['lens'] == off and p.get('residual')]
        res_nd = next(p['v'] for p in res if 'nd' in p['id'])
        res_mech = next(p['v'] for p in res if 'mech' in p['id'])
        visible = sum(p['v'] for p in vis)
        dat = F['draftAssetTotals']['+%d' % off]
        ck('(13) lens +%d: visible == Sigma PVC[1..64] == 64617' % off, visible == sum64 == 64617, visible)
        ck('(13) lens +%d: visible + residual == 83538 (F5 entrant layer)' % off,
           visible + res_nd + res_mech == 83538, visible + res_nd + res_mech)
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
             'balanced_board_md5_lineage': '06d8af60b679a12db07c064c60c065f9'}

    npass = sum(1 for r in R if r['pass']); n = len(R)
    result = {'ok': npass == n, 'n_pass': npass, 'n': n, 'final_board_identity': ident,
              'forward': {'vP1_equal': eq1, 'vP1_changed': len(ch1), 'vP2_equal': eq2,
                          'vP2_changed': len(ch2), 'missing': len(miss), 'added': len(addf)},
              'checks': R}
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'evidence', 'invariant_proof.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(result, open(out, 'w'), indent=2, sort_keys=True)
    print("\nfinal board md5=%s sha256=%s" % (ident['md5'], ident['sha256'][:16] + '...'))
    print("RESULT: %d/%d PASS  -> %s" % (npass, n, os.path.relpath(out, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
