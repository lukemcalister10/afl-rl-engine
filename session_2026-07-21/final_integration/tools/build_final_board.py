#!/usr/bin/env python3
"""DETERMINISTIC FINAL-BOARD BUILDER (final integration 2026-07-21).

Produces data/rl_build/rl_app_data.json — the final canonical round-14 board under the owner-approved
posture RL_PVC2=1 / RL_LEGE=1 / RL_LEGF=1 — from the accepted, frozen forward-lens Board B, plus the
owner-facing visible future-draft asset ladder (2027/2028 Draft Pick 1-64) reconciled EXACTLY to the
sealed F5 entrant layer. No engine ev() is run and no player v / vP1 / vP2 is altered.

METHOD (why this is correct without re-running the engine):
  * Board B (RL_LEGE=1/RL_LEGF=1, md5 1f10220c) is the accepted forward-lens board. It preserves the
    present lens exactly (804 active, Σv=752427, 0 movers vs Board A 06d8af60) and carries the
    owner-approved forward vectors (vP1/vP2) and the sealed F5 entrant layer (phantomPicks/phantomLayer/
    phantomTotals; draft 69266 + mech 14272 = 83538). It is read here from the diagnostic commit
    70ef0ff (PR #131) via `git show` — NOT transplanted into the integration branch.
  * The F5 §2.viii layer is, by construction, a pure additive presentation over PVC + vP1/vP2 + club +
    the sealed structure (engine ev() untouched, k=0 phantom=NONE). So the visible draft-asset ladder is
    reproduced deterministically here from the accepted board + the release-active PVC.

VISIBLE LADDER (owner-facing, per +1/+2 lens) — reconciled to F5:
  - 2027/2028 "Draft Pick n" for n in 1..64, each valued at the EXACT release-active PVC[n];
  - two labelled residual aggregate rows so the visible + residual = the sealed F5 entrant layer:
      (i)  national-draft deep tail (chained RD/PSD effpk 65-82 + partial occupancy) = draft_pvc - Σ PVC[1..64]
      (ii) non-national-draft entry mechanisms (MSD/SSP/rookie/pre-season/international) = mech_pvc
  Each row carries a stable machine-readable asset id, no AFL club, no AFFL club, kind/asset "pick".

Run: RL_REPO=/path python3 build_final_board.py            # writes the board; prints md5 + reconciliation
     python3 build_final_board.py --dry                    # prints reconciliation only, writes nothing
"""
import os, sys, json, hashlib, subprocess

ROOT = os.environ.get('RL_REPO') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
BOARD_B_COMMIT = '70ef0ff36ca7633aa4097a9b7c1a730013870abe'
BOARD_B_PATH = 'session_2026-07-21/forward_lens_acceptance/board_B_lege1_legf1.json'
BOARD_B_MD5 = '1f10220c341679903b79a319f554672c'
OUT = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')

PRESENT_SUM = 752427
ACTIVE_N = 804
F5_ENTRANT = 83538
F5_DRAFT = 69266
F5_MECH = 14272
VISIBLE_HI = 64


def load_board_b():
    raw = subprocess.check_output(['git', 'show', '%s:%s' % (BOARD_B_COMMIT, BOARD_B_PATH)], cwd=ROOT)
    md5 = hashlib.md5(raw).hexdigest()
    if md5 != BOARD_B_MD5:
        raise SystemExit("Board B md5 %s != pinned %s (frozen diagnostic drift)" % (md5, BOARD_B_MD5))
    return json.loads(raw)


def build(dry=False):
    B = load_board_b()
    PVC = {int(k): v for k, v in B['PVC'].items()}
    active = B['active']
    assert len(active) == ACTIVE_N, "active %d != %d" % (len(active), ACTIVE_N)
    assert sum(p['v'] for p in active) == PRESENT_SUM, "present sum drift"
    assert PVC[1] == 3000, "numeraire drift"
    pt_meta = B['phantomTotals']['_meta']
    assert pt_meta['entrant_layer_pvc'] == F5_ENTRANT and pt_meta['draft_pvc'] == F5_DRAFT \
        and pt_meta['mech_pvc'] == F5_MECH, "F5 sealed totals drift"

    sum_pvc_64 = sum(PVC[n] for n in range(1, VISIBLE_HI + 1))          # 64617
    residual_nd = F5_DRAFT - sum_pvc_64                                 # 4649 (deep tail + partial occupancy)
    residual_mech = F5_MECH                                            # 14272
    residual_total = residual_nd + residual_mech                       # 18921
    assert sum_pvc_64 + residual_total == F5_ENTRANT, "reconciliation != F5 entrant layer"

    sum_vP1 = sum(p['vP1'] for p in active)
    sum_vP2 = sum(p['vP2'] for p in active)

    lens_picks = []
    draft_asset_totals = {}
    for off, vfield, sum_vP in ((1, 'vP1', sum_vP1), (2, 'vP2', sum_vP2)):
        ly = 2026 + off
        for n in range(1, VISIBLE_HI + 1):
            lens_picks.append({
                'lens': off, 'labelYear': ly, 'n': n, 'v': PVC[n],
                'label': '%d Draft Pick %d' % (ly, n),
                'id': 'draft-pick:%d:%d' % (ly, n),
                'kind': 'pick', 'asset': 'pick', 'assetType': 'future_national_draft_pick',
                'club': None, 'affl_team': None, 'phantom': True, 'residual': False,
            })
        lens_picks.append({
            'lens': off, 'labelYear': ly, 'n': None, 'v': residual_nd,
            'label': '%d National draft — deep tail (picks 65+) & partial occupancy' % ly,
            'id': 'draft-residual-nd:%d' % ly,
            'kind': 'pick', 'asset': 'pick', 'assetType': 'future_national_draft_residual',
            'club': None, 'affl_team': None, 'phantom': True, 'residual': True,
        })
        lens_picks.append({
            'lens': off, 'labelYear': ly, 'n': None, 'v': residual_mech,
            'label': '%d Non-national-draft entry (MSD / SSP / rookie / pre-season / international)' % ly,
            'id': 'entrant-residual-mech:%d' % ly,
            'kind': 'pick', 'asset': 'pick', 'assetType': 'future_nonND_entrant_residual',
            'club': None, 'affl_team': None, 'phantom': True, 'residual': True,
        })
        draft_asset_totals['+%d' % off] = {
            'lensYear': ly, 'nVisiblePicks': VISIBLE_HI, 'nResidualRows': 2,
            'visible_1_64': sum_pvc_64, 'residual_nd_tail': residual_nd, 'residual_mech': residual_mech,
            'residual_total': residual_total, 'total': sum_pvc_64 + residual_total,
            'f5_entrant_layer_pvc': F5_ENTRANT, 'f5_draft_pvc': F5_DRAFT, 'f5_mech_pvc': F5_MECH,
            'reconciled_to_f5': (sum_pvc_64 + residual_total == F5_ENTRANT),
            'players_sum': sum_vP,
        }
    draft_asset_totals['_meta'] = {
        'basis': 'owner-facing visible future-draft asset ladder; picks 1-64 at exact release-active PVC[n]; '
                 'labelled residual aggregates carry the deep national-draft tail + non-ND entry mechanisms',
        'reconciliation': 'visible(Sigma PVC[1..64]) + residual_nd(draft_pvc - Sigma PVC[1..64]) + residual_mech'
                          ' == F5 sealed entrant layer 83538 (seal a17aafed); no value added on top of F5',
        'no_double_count': 'draftAssets is a face-value RE-PRESENTATION of the same F5 draft; phantomPicks '
                           '(occupancy) and draftAssets are never summed together; club-held real picks are '
                           'a separate owned-asset namespace (club_valuation), not the anonymous entrant layer',
        'report_only': True,
    }

    # recompute lensConservation consistently with the new visible ladder (report-only)
    lc = B.get('lensConservation', {})
    for off, sum_vP in ((1, sum_vP1), (2, sum_vP2)):
        key = '+%d' % off
        node = dict(lc.get(key, {}))
        node.update({'lensYear': 2026 + off, 'nPlayers': ACTIVE_N, 'nPicks': VISIBLE_HI, 'nResidual': 2,
                     'players': sum_vP, 'picksVisible': sum_pvc_64, 'residual': residual_total,
                     'picks': F5_ENTRANT, 'entrantLayer': F5_ENTRANT, 'total': sum_vP + F5_ENTRANT})
        lc[key] = node
    lc.setdefault('_meta', {})
    lc['_meta'].update({'entrant_reconciled': True, 'entrant_layer_pvc': F5_ENTRANT,
                        'note': 'picks side = the F5 sealed entrant layer (83538) shown visibly as 64 draft '
                                'picks + 2 residual aggregates; player side = Sigma vP over 804 active'})

    B['lensPicks'] = lens_picks
    B['draftAssetTotals'] = draft_asset_totals
    B['lensConservation'] = lc

    recon = {
        'active': len(active), 'present_sum': sum(p['v'] for p in active),
        'sum_vP1': sum_vP1, 'sum_vP2': sum_vP2,
        'visible_1_64': sum_pvc_64, 'residual_nd_tail': residual_nd, 'residual_mech': residual_mech,
        'visible_plus_residual': sum_pvc_64 + residual_total, 'f5_entrant_layer': F5_ENTRANT,
        'reconciled': (sum_pvc_64 + residual_total == F5_ENTRANT),
        'n_lens_picks': len(lens_picks),
    }
    if dry:
        print(json.dumps(recon, indent=2)); return recon, None

    payload = json.dumps(B, sort_keys=True)          # engine writer format: json.dump(out, f, sort_keys=True)
    with open(OUT, 'w') as f:
        f.write(payload)
    md5 = hashlib.md5(payload.encode()).hexdigest()
    recon['final_board_md5'] = md5
    recon['final_board_sha256'] = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps(recon, indent=2))
    print("WROTE %s  md5=%s" % (os.path.relpath(OUT, ROOT), md5))
    return recon, md5


if __name__ == '__main__':
    build(dry='--dry' in sys.argv[1:])
