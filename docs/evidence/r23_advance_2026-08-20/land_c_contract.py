#!/usr/bin/env python3
"""ACT 1 (THE SHEET RE-CUT), LANDING STEP C — THE RELEASE CONTRACT, THROUGH ITS WRITERS OF RECORD.

ADAPTED from docs/evidence/d8_adoption_2026-08-20/land_c_contract.py. What is adapted: the
must-not-move / must-move assertions are re-pointed at THIS act's facts — engine_head must move OFF
3cfc4325 (the D8 head) because six pinned literals changed; config_sha256, rl_model, fv and store must
all be UNMOVED, since a pinned OWNER INPUT re-cut is not a manifest dial and writes no store.

TWO WRITERS, IN THE ORDER THE LANDING TAIL USED THEM:
  1. release_contract.restamp_dynamic(root, as_of_round=22, store, board, season_state)
     — the SAME call staged_apply.py:542 and ownership_store_apply.py:551 make, and the same call
       docs/evidence/landing_tail_2026-08-20/02c_release_contract_restamp.txt records. It re-pins
       identities.store + identities.board and refreshes season_metadata; it DELIBERATELY preserves
       the immutable engine/rl_model/fv/register/band identities, which is why step 2 exists.
       THE ROUND IS HELD AT 22 — no round is applied by this act.
  2. the repin_contract_bake_identities.py pattern (docs/evidence/landing_tail_2026-08-20/) — the
     bake-lane identities restamp_dynamic will not touch: config_sha256 / engine_head / rl_model / fv,
     each RE-MEASURED from the checkout by the tree's own definitions (config_manifest.manifest_hash,
     md5, fv_provenance.fv_identity) and asserted equal to the accepted manifest data/expected_boot.json
     BEFORE anything is written.

PREREG ASSERTIONS ENFORCED HERE:
  config_sha256  MUST BE UNMOVED  (the dial is not a manifest var — PREREG §2.2)
  rl_model / fv  MUST BE UNMOVED
  store          MUST BE UNMOVED
  engine_head    MUST MOVE to the recomputed value
  balanced_board_md5 + present_lens_baseline are NOT touched here — their writer of record is
  sibling_repin.py and they move by BUILD-AND-COMPARE in step D.
"""
import hashlib, importlib.util, json, os, sys

ROOT='/home/user/afl-rl-engine'
APPLY='--apply' in sys.argv
P=lambda *a: os.path.join(ROOT,*a)
sys.path.insert(0,ROOT); sys.path.insert(0,P('engine','rl_after'))
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

RCT=load('release_contract_r23', P('release_contract.py'))
import config_manifest as CM, fv_provenance as FV

boot=json.load(open(P('data','expected_boot.json')))
cp=P('data','release_contract.json')
raw=open(cp,'rb').read(); rc=json.loads(raw)
# ROUND-TRIP, with the ONE disclosed tolerance. The file's writer of record
# (release_contract.restamp_dynamic:402) emits indent=2 with NO trailing newline. The committed file
# currently carries ONE trailing newline, added by the D8 PRICING seat's restamp
# (docs/evidence/d8_ceiling_2026-08-20/d8_restamp.py:86-87). The D8 landing already dropped it; this
# act expects none and tolerates either. So the body round-trips exactly and the only byte in question is that newline,
# which the writer of record will drop when it rewrites the file. That is the writer's own format
# reasserting itself, not this seat reformatting anything — named here rather than silently absorbed.
_body=json.dumps(rc,indent=2).encode()
if raw!=_body and raw!=_body+b'\n':
    raise SystemExit('HALT: release_contract.json does not round-trip at indent=2; refusing to reformat it')
if raw==_body+b'\n':
    print('NOTE: the committed file carries one trailing newline (d8_restamp.py:87). The writer of '
          'record emits none; it will be dropped by restamp_dynamic. Body round-trips byte-exact.')
if rc['contract_sha256']!=RCT.contract_hash(rc):
    raise SystemExit('HALT: the contract seal is not self-consistent BEFORE this act')
print('contract seal self-consistent before the act: %s'%rc['contract_sha256'][:12])

BEFORE={'config_sha256':rc['config_sha256'],'as_of_round':rc['as_of_round'],
        'contract_sha256':rc['contract_sha256'],
        **{'identities.'+k:v for k,v in rc['identities'].items()}}

measured={'config':CM.manifest_hash(ROOT),
          'engine_head':md5(P('engine','rl_after','_merged_recover.py')),
          'rl_model':md5(P('engine','rl_after','rl_model.py')),
          'fv':FV.fv_identity(FV.checkout_fv_dir(ROOT))}
store_md5=md5(P('engine','rl_after','rl_model_data.json'))
board_md5=md5(P('data','rl_build','rl_app_data.json'))
print('\n-- MEASURED from the checkout, asserted against the accepted manifest --')
for k,v in measured.items():
    flag='== expected_boot' if boot.get(k)==v else '*** != expected_boot %s ***'%boot.get(k)
    print('  %-12s %s   %s'%(k,v,flag))
    if boot.get(k)!=v: raise SystemExit('HALT: manifest and tree disagree on %s'%k)
for k,v,exp in (('store',store_md5,boot['store']),('board',board_md5,boot['board'])):
    print('  %-12s %s   %s'%(k,v,'== expected_boot' if exp==v else '*** != %s ***'%exp))
    if exp!=v: raise SystemExit('HALT: manifest and tree disagree on %s'%k)

# PREREG §3.3 — the things that must not move
if measured['config']!='eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1':
    raise SystemExit('HALT: PREREG §3.3 — config_sha256 MOVED to %s. The injury sheet is a pinned OWNER '
                     'INPUT, not a manifest dial; data/model_config.json must be untouched.'%measured['config'])
if measured['rl_model']!='6fe7c4155866d80e8045bed2d3bf2802': raise SystemExit('HALT: PREREG §3.3 — rl_model moved')
if measured['fv']!='6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346': raise SystemExit('HALT: PREREG §3.3 — fv moved')
if store_md5!='cc02567f80bef39228f25854d121a766': raise SystemExit('HALT: PREREG §3.3 — store moved')
if measured['engine_head']=='3cfc4325aa323b7f26594cb2a202a976': raise SystemExit('HALT: engine_head did not move')
print('  PREREG §3.3: config_sha256 UNMOVED, rl_model UNMOVED, fv UNMOVED, store UNMOVED, engine_head MOVED. OK.')

ss=json.load(open(P('data','season_state.json')))
print('\n-- WRITER 1: release_contract.restamp_dynamic(root, as_of_round=22, store, board, season_state) --')
print('   (the round is HELD at 22; season_state read from data/season_state.json, not composed here)')
if not APPLY:
    print('   --dry-run: not called.')
else:
    seal=RCT.restamp_dynamic(ROOT, 22, store_md5, board_md5, ss)
    print('   restamp_dynamic returned seal %s'%seal[:12])
    rc=json.loads(open(cp,'rb').read())

print('\n-- WRITER 2: the bake-lane identities (repin_contract_bake_identities.py pattern) --')
FROZEN=('identities.balanced_board_md5','identities.band','identities.register','release_version',
        'present_lens_baseline','switch_posture','pvc_provenance','must_be_unset','held_checks',
        'f5_entrant_reconciliation','adopted','season_state_policy_id','_retired_checks')
def snap(c):
    return {k:(json.dumps(c['identities'].get(k.split('.')[1]),sort_keys=True) if k.startswith('identities.')
               else json.dumps(c.get(k),sort_keys=True)) for k in FROZEN}
fb=snap(rc)
for f,key in (('config_sha256','config'),):
    print('  contract %-24s %s -> %s'%(f, rc[f][:12], measured[key][:12]))
    rc[f]=measured[key]
for f in ('engine_head','rl_model','fv'):
    print('  contract identities.%-13s %s -> %s'%(f, str(rc['identities'][f])[:12], measured[f][:12]))
    rc['identities'][f]=measured[f]
old_seal=rc.pop('contract_sha256')
rc['contract_sha256']=RCT.contract_hash(rc)
print('  contract_sha256                  %s -> %s'%(old_seal[:12], rc['contract_sha256'][:12]))
fa=snap(rc)
mv=[k for k in fb if fb[k]!=fa[k]]
if mv: raise SystemExit('HALT: a field writer 2 must not touch moved: %s'%mv)
print('  frozen fields asserted unmoved: %d checked, 0 moved'%len(FROZEN))

if APPLY:
    tmp=cp+'.tmp_d8'
    with open(tmp,'w') as f: json.dump(rc,f,indent=2)
    os.replace(tmp,cp)
    rc2=json.load(open(cp))
    assert rc2['config_sha256']==measured['config']
    for f in ('engine_head','rl_model','fv'): assert rc2['identities'][f]==measured[f], '%s did not take'%f
    assert rc2['contract_sha256']==RCT.contract_hash(rc2), 'the seal must verify after the write'
    assert rc2['identities']['store']==boot['store'] and rc2['identities']['board']==boot['board']
    assert rc2['as_of_round']==22, 'the round must be HELD at 22'
    print('\nRE-STAMPED and re-read. The seal verifies; store/board pins name the live tree; round HELD at 22.')
    print('\n-- BEFORE -> AFTER --')
    AFTER={'config_sha256':rc2['config_sha256'],'as_of_round':rc2['as_of_round'],
           'contract_sha256':rc2['contract_sha256'],
           **{'identities.'+k:v for k,v in rc2['identities'].items()}}
    for k in sorted(set(BEFORE)|set(AFTER)):
        b,a=BEFORE.get(k),AFTER.get(k)
        print('  %-32s %-34s %s %s'%(k,str(b)[:32],'->' if b!=a else '==',str(a)[:32] if b!=a else 'UNMOVED'))
else:
    print('\n--dry-run: nothing written.')
