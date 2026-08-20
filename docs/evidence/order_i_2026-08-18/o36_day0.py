#!/usr/bin/env python3
"""ORDER I -- DAY0_I_FINAL.json: A DISCLOSED RE-BASE OF THE DAY-0 GUARD, AND WHY IT WAS NEEDED.

THE FINDING, STATED BEFORE THE CODE. Running the emit against the landing candidate's own day-0 file
HALTED: 0 of 89 wired entrants reproduced the printed day-0. The cause is Lever 3. A day-0 price for a
row that has never played IS `v0 x D(c_u)` -- the sitter fade -- and Order H's tall/small factor is a
change to exactly that fade. So it moves the printed day-0 of every wired SITTER by construction.

WHAT DID NOT MOVE, AND THIS IS THE DISTINCTION THAT MATTERS: `derived_v0`, the raw entry object the
emitter writes as year-0, is byte-identical on all 89 rows at tolerance 0. oskar-taylor's is
903.8014284605089 on the landing candidate and 903.8014284605089 here. V0 is untouched. What moved is
what the board CHARGES a sitter today, which is the sitter fade doing its job.

This is the same re-base ORDER D required when its own pick-curve fade landed, and it is reported as a
GATE RESULT in PACKET_I.md, not buried here. Everything else in the file is ORDER A's generator
verbatim; only the board path, the dial and the output name change.
"""

import os, sys, json, io, contextlib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o36'
BOARDP = os.path.join(SP, 'bb_full', 'rl_after', 'rl_app_data.json')

os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_LAM_S1='0.25', RL_O36_TALL='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
day0_v0 = NSE['day0_v0']; entry_derived = NSE['_entry29b_derived']; o31_D = NSE['o31_D']
BOARD_MD5 = hashlib.md5(open(BOARDP, 'rb').read()).hexdigest()
ROWS = {r['key']: r for r in json.load(open(BOARDP))['active']}
Y = MA.BASE_REF

out, mism = [], []
nND = nPOOL = 0
for p in MA.data:
    d0 = entry_derived(p, Y)
    if d0 is None:
        continue
    k = p.get('key') or MA.slug(p['player'])
    D = float(o31_D(p, Y))
    price = float(d0) * D
    printed = ROWS[k]['v'] if k in ROWS else None
    if printed is None or int(round(price)) != int(printed):
        mism.append((k, printed, price))
    if p.get('_pool'): nPOOL += 1
    else: nND += 1
    out.append(dict(key=k, ty=p.get('type'), pos=MA.gfut(p), pick=p.get('pick'),
                    cell=('%s|%s' % (p.get('type'), MA.gfut(p))) if p.get('_pool') else None,
                    printed=int(printed) if printed is not None else None,
                    derived_v0=float(d0), fade_D=D, day0_price=price))

DOC = dict(label='ORDER A / CANDIDATE 32 -- the candidate\'s own printed day-0 prices',
           board='ORDER 31-F candidate', board_md5=BOARD_MD5,
           law='printed = round(day0_v0(p) * D(c_u)) -- the ONE LAW at g=0, where rho(0)=0 and '
               'pi(0,c,s) == D(c) exactly',
           entry_year_note='at a row\'s OWN entry year the fade clock c_u <= 1 so D == 1 and the day-0 '
                           'price IS day0_v0(p); the fade below is the value at Y=%d for rows that '
                           'entered earlier and have never played' % Y,
           base_ref=Y, n_fresh_nd=nND, n_pool=nPOOL, n_wired=len(out),
           identity_all='%d of %d at tolerance 0' % (len(out) - len(mism), len(out)),
           mismatches=mism, rows=out)
json.dump(DOC, open(os.path.join(HERE, 'DAY0_I_FINAL.json'), 'w'), indent=1, sort_keys=True)
print('ORDER I PRINTED DAY-0 IDENTITY: %d of %d at tolerance 0 (ND %d, pool %d) on board %s'
      % (len(out) - len(mism), len(out), nND, nPOOL, BOARD_MD5))
if mism:
    print('MISMATCHES: %s' % mism[:10])
    sys.exit('ORDER I HALT: the printed day-0 identity does not hold on the written board.')
print('DAY0_I_FINAL.json written.')
