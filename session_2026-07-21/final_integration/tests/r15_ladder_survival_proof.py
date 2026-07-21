#!/usr/bin/env python3
"""DISPOSABLE ROUND-15 REGENERATION — the visible future-asset ladder SURVIVES a weekly update with NO
manual post-processing (final integration 2026-07-21, supervisor req 1.8).

Applies the owner's genuine Round-15 scores on a DISPOSABLE scratch copy of the accepted Round-14 state,
via the Track B updater (gate armed IN-PROCESS against the scratch ONLY — the real-store gate ships OFF).
The updater's board regeneration now runs the Option-A rl_export.py, so after canonical regeneration +
finalization the scratch board + UI bundles must carry the future-asset ladder AUTOMATICALLY. Asserts:
  - the regenerated scratch board reaches Round 15;
  - the visible ladder is present: exactly 64 picks per lens (2027 + 2028) at exact PVC;
  - the F5 reconciliation is exact (visible 64617 + residual 18921 = sealed 83538);
  - the regenerated scratch UI working bundle carries the ladder (no manual post-processing step);
  - NO canonical file (real store / board) changed; the real-store gate is OFF afterwards.

Run:  python3 session_2026-07-21/final_integration/tests/r15_ladder_survival_proof.py   (exit 0 = PASS)
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RA = os.path.join(ROOT, 'engine', 'rl_after'); ING = os.path.join(RA, 'ingestion')
WUH = os.path.join(ROOT, 'session_2026-07-20', 'weekly_updater_hardening')
CATCHUP = os.path.join(ROOT, 'session_2026-07-20', 'live_scoring_catchup')
FIX = os.path.join(CATCHUP, 'fixtures')
for p in (RA, ING, WUH, CATCHUP): sys.path.insert(0, p)

import round_catchup as RC        # noqa: E402
import failure_injection_proof as FI  # noqa: E402 (scratch + gate helpers)
import catchup_proof as CP        # noqa: E402 (install_ui helper)
import score_ingestor as SI       # noqa: E402

GEN = "2026-07-21T03:00:00Z"
R = []
def ck(name, ok, detail=''):
    R.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('  PASS ' if ok else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(ok)

def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None

def bundle_obj(path):
    s = open(path, encoding='utf-8').read()
    return json.loads(s[s.index('{'): s.rindex('}') + 1])

def main():
    print('=== DISPOSABLE R15 REGENERATION — future-asset ladder survival ===')
    real_store = os.path.join(RA, 'rl_model_data.json')
    real_board = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')
    store_before, board_before = md5(real_store), md5(real_board)

    scr = FI.make_scratch('r15ladder')
    CP.install_ui(scr)
    FI.arm()                                       # IN-PROCESS gate arm — scratch ONLY
    try:
        RC.RoundCatchup(scr, [(15, os.path.join(FIX, 'R15.csv'))]).run(approved=True, generated_at=GEN)
    finally:
        FI.disarm()

    scr_board = os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json')
    scr_workbundle = os.path.join(scr, 'ui', 'data', 'board_view_working.js')
    B = json.load(open(scr_board))

    # reached R15?
    vh = json.load(open(os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'value_history.json')))
    ck('scratch board regenerated through Round 15', 15 in vh.get('rounds', []), 'rounds=%s' % vh.get('rounds'))

    # ladder present in the regenerated scratch board (produced by the updater's rl_export — NO manual step)
    lp = B.get('lensPicks', [])
    v1 = [p for p in lp if p['lens'] == 1]; v2 = [p for p in lp if p['lens'] == 2]
    ck('regenerated board: exactly 64 visible 2027 picks', len(v1) == 64, len(v1))
    ck('regenerated board: exactly 64 visible 2028 picks', len(v2) == 64, len(v2))
    ck('regenerated board: picks labelled + PVC-valued (2027 Draft Pick 1 == PVC[1] 3000)',
       any(p.get('label') == '2027 Draft Pick 1' and p['v'] == 3000 for p in v1))
    dat = B.get('draftAssetTotals', {})
    for off in (1, 2):
        d = dat.get('+%d' % off, {})
        ck('regenerated board: +%d F5 reconciliation exact (64617+4649+14272=83538)' % off,
           d.get('visible_1_64') == 64617 and d.get('residual_nd_tail') == 4649 and
           d.get('residual_mech') == 14272 and d.get('f5_entrant_layer_pvc') == 83538 and d.get('reconciled_to_f5'))
    ck('regenerated board: F5 phantomTotals entrant layer still 83538',
       B.get('phantomTotals', {}).get('_meta', {}).get('entrant_layer_pvc') == 83538)

    # the ladder survives into the regenerated scratch UI bundle (no manual post-processing command)
    if os.path.exists(scr_workbundle):
        W = bundle_obj(scr_workbundle)
        wlp = W.get('lensPicks', [])
        ck('regenerated scratch UI bundle carries the 64-pick ladder (no manual post-processing)',
           len([p for p in wlp if p.get('lens') == 1]) == 64 and 'draftAssetTotals' in W)
    else:
        ck('regenerated scratch UI bundle present', False, 'missing %s' % scr_workbundle)

    # present-lens still 804 / Σv preserved on the R15 scratch (scores applied, no ladder-induced drift)
    ck('regenerated board: 804 active rows preserved', len(B['active']) == 804, len(B['active']))

    # NO canonical file changed; gate OFF afterwards
    ck('canonical store byte-identical (968de0c7 untouched)', md5(real_store) == store_before)
    ck('canonical board byte-identical (2ab73a6f untouched)', md5(real_board) == board_before)
    ck('real-store apply gate OFF after the scratch run', not SI._apply_enabled(),
       'APPLY_DEFAULT=%s INGEST_SCORE_APPLY=%s' % (SI.APPLY_DEFAULT, os.environ.get('INGEST_SCORE_APPLY')))

    npass = sum(1 for x in R if x['pass']); n = len(R)
    out = os.path.abspath(os.path.join(HERE, '..', 'evidence', 'r15_ladder_survival.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({'ok': npass == n, 'n_pass': npass, 'n': n,
               'scratch_board_md5': md5(scr_board), 'canonical_store_unchanged': md5(real_store) == store_before,
               'checks': R}, open(out, 'w'), indent=2)
    print('\nRESULT: %d/%d PASS  -> %s' % (npass, n, os.path.relpath(out, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
