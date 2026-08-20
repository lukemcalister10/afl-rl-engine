#!/usr/bin/env python3
"""ACT A (THE F5 ROUNDING ACT), LANDING STEP E — THE UI BUNDLES. BOTH WRITERS. THE THRICE-PROVEN TRAP.

CARRIED BYTE-FOR-BYTE IN LOGIC from docs/evidence/r23_advance_2026-08-20/land_e_ui.py. Only this
docstring differs. The script is parameterless — it reads the board pin, the round and every identity
from data/expected_boot.json and data/release_lineage.json — so there is nothing in it to re-point at
this act, and re-typing its assertions would only risk weakening them.

extract_board_view.py REGENERATES the bundle from the board and DROPS stamp.release; only
round_movers.inject_release_contract puts it back. Running the first without the second leaves the
html app with no release block — the failure this tree has now caught three times
(docs/evidence/landing_tail_2026-08-20/02a_*.txt, 28_reinject_release_contract.txt, and the D8
pricing seat's own d8_restamp.py §3 which runs them as a pair for exactly this reason).

MEASURED HERE, NOT ASSUMED: stamp.release was checked BEFORE this script ran and was ABSENT — the
sibling repin (step D) regenerates board_view through extract_board_view and had already dropped it.
So the trap was live in this very transaction, not hypothetical.

The invocation is the one docs/evidence/landing_tail_2026-08-20/02a_*.txt records and d8_restamp.py:91-99
carries: extract_board_view.py as a subprocess from the repo root, then
round_movers.inject_release_contract(bundle, root, as_of_round) with the round read from expected_boot.
"""
import hashlib, importlib.util, json, os, subprocess, sys
ROOT='/home/user/afl-rl-engine'
P=lambda *a: os.path.join(ROOT,*a)
BUNDLE=P('ui','data','board_view_working.js'); PUBLIC=P('ui','data','board_view_public.js')
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
def has_release(p):
    return '"release"' in open(p,encoding='utf-8').read()

boot=json.load(open(P('data','expected_boot.json')))
print('=== LANDING STEP E — BOTH UI WRITERS ===')
print('  board pin      : %s'%boot['board'])
print('  as_of_round    : %s'%boot['as_of_round'])
print()
print('BEFORE  working %s  release-block=%s'%(md5(BUNDLE), has_release(BUNDLE)))
print('BEFORE  public  %s  release-block=%s'%(md5(PUBLIC), has_release(PUBLIC)))
print()
print('--- WRITER 1/2: ui/tools/extract_board_view.py ---')
r=subprocess.run([sys.executable,P('ui','tools','extract_board_view.py')],cwd=ROOT,capture_output=True,text=True)
print(r.stdout.rstrip())
if r.returncode!=0:
    print(r.stderr[-2000:]); raise SystemExit('HALT: extract_board_view failed')
print('  working after writer 1: %s   release-block=%s   <-- DROPPED, as it always is'%(md5(BUNDLE),has_release(BUNDLE)))
print()
print('--- WRITER 2/2: round_movers.inject_release_contract(bundle, root, %s) ---'%boot['as_of_round'])
spec=importlib.util.spec_from_file_location('rm_f5',P('engine','rl_after','ingestion','round_movers.py'))
rm=importlib.util.module_from_spec(spec); sys.modules['rm_f5']=rm; spec.loader.exec_module(rm)
rel=rm.inject_release_contract(BUNDLE, ROOT, int(boot['as_of_round']))
print(json.dumps(rel,indent=2,sort_keys=True))
print()
print('AFTER   working %s  release-block=%s'%(md5(BUNDLE), has_release(BUNDLE)))
print('AFTER   public  %s  release-block=%s'%(md5(PUBLIC), has_release(PUBLIC)))
print()
print('--- THE EMBEDDED BOARD IDENTITY, READ BACK OUT OF THE HTML APP BUNDLE ---')
fails=[]
src=open(BUNDLE,encoding='utf-8').read()
st=json.loads(src[src.index('{'):src.rindex('};')+1])['stamp'] if False else None
import re
m=re.search(r'window\.__MATCHDAY_WORKING__\s*=\s*(\{.*)\n?', src, re.S)
obj=json.loads(m.group(1).rstrip().rstrip(';'))
st=obj['stamp']
for k,exp in (('board_md5',boot['board']),('board',boot['board']),('srcmd5',boot['board']),
              ('store_md5',boot['store']),('balanced_board_md5',boot['balanced_board_md5']),
              ('asOfRound',boot['as_of_round'])):
    ok = str(st.get(k))==str(exp)
    print('  stamp.%-20s %-34s %s'%(k,st.get(k),'OK' if ok else '*** != %s ***'%exp))
    if not ok: fails.append('stamp.'+k)
for k,exp in (('engine',boot['engine_head'][:8]),('store',boot['store'][:8]),('register',boot['register'][:8]),('config',boot['config'][:12])):
    ok = str(st.get(k))==exp
    print('  stamp.%-20s %-34s %s'%(k,st.get(k),'OK' if ok else '*** != %s ***'%exp))
    if not ok: fails.append('stamp.'+k)
print()
relb=st.get('release') or {}
lin=json.load(open(P('data','release_lineage.json')))
# stamp.release is assembled by round_movers.release_identity from TWO sources, and it says so in its
# own manifest_source field: 'data/expected_boot.json + data/release_lineage.json'. The identity pins
# come from expected_boot; balanced_board_md5 and release_version come from the LINEAGE file's
# top-level PRESENT-LENS BASELINE, which is a frozen historical anchor and MUST NEVER MOVE
# (append_landing_transition.py asserts exactly that before and after every append). So this field
# reading 06d8af60 while expected_boot.balanced_board_md5 reads the freshly-built sibling is CORRECT
# and pre-existing, not drift introduced here: the landing tail's own capture
# (02a_inject_release_contract.txt) shows 06d8af60 against an expected_boot of 72fe3a17. Asserted
# against its REAL source rather than the one it does not read.
EXPECT_REL={'board':boot['board'],'store':boot['store'],'engine_head':boot['engine_head'],
            'rl_model':boot['rl_model'],'fv':boot['fv'],'config':boot['config'],
            'register':boot['register'],'as_of_round':boot['as_of_round'],
            'balanced_board_md5':lin['balanced_board_md5'],'release_version':lin['release_version']}
SRC={'balanced_board_md5':'release_lineage (frozen present-lens baseline)',
     'release_version':'release_lineage (frozen present-lens baseline)'}
for k in ('board','store','engine_head','rl_model','fv','config','register','as_of_round',
          'balanced_board_md5','release_version'):
    exp=EXPECT_REL[k]; ok=str(relb.get(k))==str(exp)
    print('  stamp.release.%-20s %-34s %-4s %s'%(k,str(relb.get(k))[:34],'OK' if ok else '***FAIL***',
                                                 SRC.get(k,'expected_boot')))
    if not ok: fails.append('stamp.release.'+k)
print()
if fails: raise SystemExit('HALT: the UI bundle identity did not move: %s'%fails)
print("THE HTML APP'S EMBEDDED BOARD IDENTITY IS %s. Both writers ran; the release block is back."%boot['board'])
