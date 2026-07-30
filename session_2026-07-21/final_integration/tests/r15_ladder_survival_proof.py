#!/usr/bin/env python3
"""DISPOSABLE ROUND-15 REGENERATION — the visible future-asset ladder SURVIVES a weekly update with NO
manual post-processing (final integration 2026-07-21, supervisor req 1.8).

Applies the owner's genuine Round-15 scores on a DISPOSABLE scratch copy of the accepted Round-14 state,
via the Track B updater (gate armed IN-PROCESS against the scratch ONLY — the real-store gate ships OFF).
The updater's board regeneration now runs the Option-A rl_export.py, so after canonical regeneration +
finalization the scratch board + UI bundles must carry the future-asset ladder AUTOMATICALLY. Asserts:
  - the regenerated scratch board reaches Round 15;
  - the visible ladder is present: exactly 64 picks per lens (2027 + 2028) at exact PVC;
  - the F5 reconciliation is exact and INTERNALLY closed (visible + residual_nd + residual_mech ==
    f5_draft_pvc + f5_mech_pvc == the regenerated board's own sealed entrant layer);
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


def declare_replay_under_current_code(scr):
    """#274 mop-up — THE DECLARED CLAIM of this proof, made explicit.

    What this proof does, stated plainly: it REPLAYS R14-R19 HISTORY UNDER CURRENT CODE. The scratch is
    rewound to the accepted R14 baseline and the recorded rounds are re-applied, but the engine doing the
    applying is today's checkout. That was always true; it was never declared, and one assert silently
    assumed the opposite.

    THE ASSUMPTION THAT BROKE. `materialize_r14()` stamps the R14-era identities into the scratch manifest,
    including the R14-era `fv`. Guard 5 then resolves its pinned `fv` through `fv_provenance.repo_root()`,
    which walks up from the WORKSPACE copy (fv_provenance.py:34-40), so inside the scratch it reads the
    rewound R14 pin -- and compares it against the only forward_valuation in the tree, which is today's.
    While `fv` had not moved since R14 the two agreed by coincidence. The 30/7 rederivation moved it
    (6a9a520f -> d10aa93e) and Guard 5 began refusing, correctly: it exists to stop a silent stale import.

    THE RESTATEMENT. The historical stamp is asserted FIRST (so the rewind is still proven to have rewound)
    and recorded under `_fv_replay_note` as history, then the manifest's live `fv` pin is set to the
    CANONICAL checkout's pin -- the checkout the code actually comes from. Guard 5 keeps its full force: it
    still refuses any forward_valuation that is not the pinned one, only now the pin is the one the imported
    source is supposed to match. Nothing outside this throwaway scratch is touched; no committed record and
    no historical value is rewritten.

    Returns (historical_fv, canonical_fv).
    """
    mpath = os.path.join(scr, 'data', 'expected_boot.json')
    m = json.load(open(mpath))
    hist_fv = m.get('fv')
    canon_fv = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json'))).get('fv')

    # (1) the rewind really rewound: the scratch carries the HISTORICAL fv stamp, not today's.
    ck('scratch is rewound to the historical baseline (its fv stamp is history, not the current pin)',
       bool(hist_fv) and bool(canon_fv) and hist_fv != canon_fv,
       'scratch fv=%s vs canonical fv=%s' % (str(hist_fv)[:8], str(canon_fv)[:8]))

    m['_fv_replay_note'] = {
        'claim': 'R14-R19 history replayed under CURRENT code',
        'historical_fv_stamp': hist_fv,
        'replayed_under_fv': canon_fv,
        'why': ('the recorded rounds are historical; the engine replaying them is the current checkout, so '
                'Guard 5 is anchored to the canonical pin. The historical stamp is preserved here as '
                'history and is asserted above.'),
        'ruling': '#274 adoption mop-up act, owner word 2026-07-30',
    }
    m['fv'] = canon_fv
    with open(mpath, 'w') as f:
        json.dump(m, f, indent=2)

    # (2) the declared claim now holds: the pin the replay boots against IS the canonical one.
    ck('replay declares its claim: Guard 5 anchored to the canonical fv pin (%s)' % str(canon_fv)[:8],
       json.load(open(mpath)).get('fv') == canon_fv)
    # (3) and the history is still legible in the scratch, not overwritten out of existence.
    ck('the historical fv stamp is preserved as history in the scratch manifest',
       json.load(open(mpath)).get('_fv_replay_note', {}).get('historical_fv_stamp') == hist_fv)
    return hist_fv, canon_fv

def main():
    print('=== DISPOSABLE R15 REGENERATION — future-asset ladder survival ===')
    real_store = os.path.join(RA, 'rl_model_data.json')
    real_board = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')
    store_before, board_before = md5(real_store), md5(real_board)

    scr = FI.make_scratch('r15ladder')
    CP.install_ui(scr)
    declare_replay_under_current_code(scr)   # #274: declare the claim before the replay boots
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
    # #274 mop-up — RE-EXPRESSED against the regenerated board's OWN totals, not against an era's
    # magnitudes. These asserted 64617/4649/14272/83538, which were the released values when this proof was
    # written; the 30/7 rederivation moved them to 65925/2631/9055/77611. But this step's question is
    # "does a weekly regeneration PRESERVE the ladder and close F5?", and that is a property of the
    # regenerated board, not of any particular era's numbers. Pinning the era's magnitudes here made the
    # proof re-assert the release baseline as a side effect, so it went red on a legitimate re-derivation
    # while telling us nothing about ladder survival. It now closes the reconciliation internally — which
    # is the same form invariant_proof.py's PER-PUSH lane uses (see its two-lane header) — and the
    # released-magnitude question stays where it belongs, in that file's adoption lane.
    dat = B.get('draftAssetTotals', {})
    seal = B.get('phantomTotals', {}).get('_meta', {}).get('entrant_layer_pvc')
    for off in (1, 2):
        d = dat.get('+%d' % off, {})
        closes = (d.get('visible_1_64') is not None
                  and d['visible_1_64'] + d.get('residual_nd_tail', 0) + d.get('residual_mech', 0)
                      == d.get('f5_draft_pvc', 0) + d.get('f5_mech_pvc', 0)
                      == d.get('f5_entrant_layer_pvc')
                  and d.get('residual_nd_tail') == d.get('f5_draft_pvc', 0) - d['visible_1_64']
                  and d.get('residual_mech') == d.get('f5_mech_pvc')
                  and d.get('reconciled_to_f5'))
        ck('regenerated board: +%d F5 reconciliation closes internally (%s+%s+%s=%s)'
           % (off, d.get('visible_1_64'), d.get('residual_nd_tail'), d.get('residual_mech'),
              d.get('f5_entrant_layer_pvc')), closes)
    ck('regenerated board: draftAssetTotals and phantomTotals agree on the sealed entrant layer (%s)' % seal,
       seal is not None and all(dat.get('+%d' % o, {}).get('f5_entrant_layer_pvc') == seal for o in (1, 2)))

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
