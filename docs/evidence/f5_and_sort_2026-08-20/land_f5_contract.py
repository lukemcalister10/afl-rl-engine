#!/usr/bin/env python3
"""ACT A (THE F5 ROUNDING ACT), LANDING STEP B — THE RELEASE CONTRACT, THROUGH ITS WRITERS OF RECORD.

ADAPTED from docs/evidence/r23_advance_2026-08-20/land_c_contract.py (itself the D8 adaptation of the
landing tail's pattern). What is adapted: the must-move / must-not-move assertions are re-pointed at
THIS act's facts.

THE DIFFERENCE FROM EVERY PRIOR LANDING, STATED PLAINLY: **engine_head must NOT move.** This act edits
`engine/rl_after/rl_export.py`, the exporter, which no identity pin tracks. `engine_head` is
md5(_merged_recover.py) and the valuation engine is untouched — no player price moves, so the thing
that prices players must not move either. Prior landings asserted engine_head MOVED; this one asserts
the reverse, deliberately.

WRITERS, IN ORDER:
  1. release_contract.restamp_dynamic(root, as_of_round=23, store, board, season_state)
     — the SAME call staged_apply.py and ownership_store_apply.py make. Re-pins identities.store +
       identities.board and refreshes season_metadata. THE ROUND IS HELD AT 23: this act applies no
       round. store is UNMOVED (this act writes no store); only board moves.
  2. the bake-lane identities restamp_dynamic will not touch (config_sha256 / engine_head / rl_model /
     fv), each RE-MEASURED from the checkout by the tree's own definitions and asserted EQUAL to the
     accepted manifest before anything is written. Here that step is a pure NO-OP re-assertion — all
     four must already agree — which is exactly the outcome this act predicts.

WHAT IS NOT TOUCHED: balanced_board_md5 + present_lens_baseline (writer of record is sibling_repin.py;
this act does not rebuild the sibling and the balanced board does not move), and
f5_entrant_reconciliation — which names the RELEASED baseline layer 77611, a different era's numbers
under the adoption lane, NOT the current 56772/56773. It is asserted FROZEN here, because a seat
reading only the runbook's cost list might expect it to move with the declared layer. It must not.

Run:  python3 land_f5_contract.py            (dry run)
      python3 land_f5_contract.py --apply
"""
import hashlib, importlib.util, json, os, sys

ROOT = '/home/user/afl-rl-engine'
APPLY = '--apply' in sys.argv
P = lambda *a: os.path.join(ROOT, *a)
sys.path.insert(0, ROOT); sys.path.insert(0, P('engine', 'rl_after'))
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

RCT = load('release_contract_f5', P('release_contract.py'))
import config_manifest as CM, fv_provenance as FV

boot = json.load(open(P('data', 'expected_boot.json')))
cp = P('data', 'release_contract.json')
raw = open(cp, 'rb').read(); rc = json.loads(raw)
_body = json.dumps(rc, indent=2).encode()
if raw != _body and raw != _body + b'\n':
    raise SystemExit('HALT: release_contract.json does not round-trip at indent=2; refusing to reformat it')
if raw == _body + b'\n':
    print('NOTE: the committed file carries one trailing newline; the writer of record emits none.')
if rc['contract_sha256'] != RCT.contract_hash(rc):
    raise SystemExit('HALT: the contract seal is not self-consistent BEFORE this act')
print('contract seal self-consistent before the act: %s' % rc['contract_sha256'][:12])

BEFORE = {'config_sha256': rc['config_sha256'], 'as_of_round': rc['as_of_round'],
          'contract_sha256': rc['contract_sha256'],
          **{'identities.' + k: v for k, v in rc['identities'].items()}}

measured = {'config': CM.manifest_hash(ROOT),
            'engine_head': md5(P('engine', 'rl_after', '_merged_recover.py')),
            'rl_model': md5(P('engine', 'rl_after', 'rl_model.py')),
            'fv': FV.fv_identity(FV.checkout_fv_dir(ROOT))}
store_md5 = md5(P('engine', 'rl_after', 'rl_model_data.json'))
board_md5 = md5(P('data', 'rl_build', 'rl_app_data.json'))
print('\n-- MEASURED from the checkout, asserted against the accepted manifest --')
for k, v in measured.items():
    ok = boot.get(k) == v
    print('  %-12s %s   %s' % (k, v, '== expected_boot' if ok else '*** != %s ***' % boot.get(k)))
    if not ok: raise SystemExit('HALT: manifest and tree disagree on %s' % k)
for k, v, exp in (('store', store_md5, boot['store']), ('board', board_md5, boot['board'])):
    ok = exp == v
    print('  %-12s %s   %s' % (k, v, '== expected_boot' if ok else '*** != %s ***' % exp))
    if not ok: raise SystemExit('HALT: manifest and tree disagree on %s' % k)

# ---- THIS ACT'S must-not-move set ---------------------------------------------------------------
if measured['engine_head'] != '1867e953cf844d089ab1da68379b1742':
    raise SystemExit('HALT: engine_head MOVED. This act edits the EXPORTER, not the engine.')
if measured['config'] != 'eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1':
    raise SystemExit('HALT: config_sha256 moved — the F5 fix is not a manifest dial')
if measured['rl_model'] != '6fe7c4155866d80e8045bed2d3bf2802': raise SystemExit('HALT: rl_model moved')
if measured['fv'] != '6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346':
    raise SystemExit('HALT: fv moved')
if store_md5 != 'b745002eb0a0fbb1c34fa44f1ef708d6': raise SystemExit('HALT: the store moved')
if board_md5 == '7a3f4fe23207a29095e6d37408a4b727': raise SystemExit('HALT: the board did NOT move')
print('  config UNMOVED, engine_head UNMOVED, rl_model UNMOVED, fv UNMOVED, store UNMOVED, board MOVED. OK.')

ss = json.load(open(P('data', 'season_state.json')))
print('\n-- WRITER 1: release_contract.restamp_dynamic(root, as_of_round=23, store, board, season_state) --')
print('   (the round is HELD at 23; this act applies no round and writes no store)')
if not APPLY:
    print('   --dry-run: not called.')
else:
    seal = RCT.restamp_dynamic(ROOT, 23, store_md5, board_md5, ss)
    print('   restamp_dynamic returned seal %s' % seal[:12])
    rc = json.loads(open(cp, 'rb').read())

print('\n-- WRITER 2: the bake-lane identities (a NO-OP re-assertion for this act) --')
FROZEN = ('identities.balanced_board_md5', 'identities.band', 'identities.register', 'release_version',
          'present_lens_baseline', 'switch_posture', 'pvc_provenance', 'must_be_unset', 'held_checks',
          'f5_entrant_reconciliation', 'adopted', 'season_state_policy_id', '_retired_checks')
def snap(c):
    return {k: (json.dumps(c['identities'].get(k.split('.')[1]), sort_keys=True) if k.startswith('identities.')
                else json.dumps(c.get(k), sort_keys=True)) for k in FROZEN}
fb = snap(rc)
print('  contract config_sha256           %s -> %s' % (rc['config_sha256'][:12], measured['config'][:12]))
rc['config_sha256'] = measured['config']
for f in ('engine_head', 'rl_model', 'fv'):
    print('  contract identities.%-13s %s -> %s' % (f, str(rc['identities'][f])[:12], measured[f][:12]))
    rc['identities'][f] = measured[f]
old_seal = rc.pop('contract_sha256')
rc['contract_sha256'] = RCT.contract_hash(rc)
print('  contract_sha256                  %s -> %s' % (old_seal[:12], rc['contract_sha256'][:12]))
mv = [k for k in fb if fb[k] != snap(rc)[k]]
if mv: raise SystemExit('HALT: a field writer 2 must not touch moved: %s' % mv)
print('  frozen fields asserted unmoved: %d checked, 0 moved' % len(FROZEN))
print('  (f5_entrant_reconciliation.entrant_layer_pvc is among them and reads %s — the RELEASED'
      % (rc.get('f5_entrant_reconciliation') or {}).get('entrant_layer_pvc'))
print('   baseline under the adoption lane, a different era\'s number. It does NOT track the declared')
print('   layer and must NOT move to 56773.)')

if APPLY:
    tmp = cp + '.tmp_f5'
    with open(tmp, 'w') as f: json.dump(rc, f, indent=2)
    os.replace(tmp, cp)
    rc2 = json.load(open(cp))
    assert rc2['config_sha256'] == measured['config']
    for f in ('engine_head', 'rl_model', 'fv'): assert rc2['identities'][f] == measured[f], '%s did not take' % f
    assert rc2['contract_sha256'] == RCT.contract_hash(rc2), 'the seal must verify after the write'
    assert rc2['identities']['store'] == boot['store'] and rc2['identities']['board'] == boot['board']
    assert rc2['as_of_round'] == 23, 'the round must be HELD at 23'
    print('\nRE-STAMPED and re-read. The seal verifies; store/board pins name the live tree; round HELD at 23.')
    AFTER = {'config_sha256': rc2['config_sha256'], 'as_of_round': rc2['as_of_round'],
             'contract_sha256': rc2['contract_sha256'],
             **{'identities.' + k: v for k, v in rc2['identities'].items()}}
    print('\n-- BEFORE -> AFTER --')
    for k in sorted(set(BEFORE) | set(AFTER)):
        b, a = BEFORE.get(k), AFTER.get(k)
        print('  %-34s %-14s %s %s' % (k, str(b)[:12], '->' if b != a else '==', str(a)[:12] if b != a else ''))
else:
    print('\nDRY RUN — nothing written.')
