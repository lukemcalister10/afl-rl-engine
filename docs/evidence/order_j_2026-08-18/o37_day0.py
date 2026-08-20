#!/usr/bin/env python3
"""ORDER J — the day-0 guard file, regenerated per board.

WHY IT IS REGENERATED, STATED BEFORE THE CODE. A day-0 price for a man who has never played IS his
entry value multiplied by the sitting discount. The owner-ruled tall/small factor is a change to
exactly that discount. So the printed day-0 of every wired sitter moves BY CONSTRUCTION the moment the
ruled factor is live, and the landing candidate's own day-0 file cannot match. What does NOT move is
`derived_v0`, the raw entry object the walk-forward matrix writes as year-0: bit-identical on 89 of 89
(o37_tall_disclose.py §7). Entry values are untouched; the matrix's year-0 column is untouched.

This is the same regeneration ORDER D's own pick-curve fade required when it landed, and the same one
ORDER I disclosed. It is DISCLOSED on the packet, not buried here.

ORDER A's generator verbatim; only the board path, the dial and the output name change.
Usage: J_TAG=<tag> J_DOSE=.. J_KAPPA=.. ... python3 o37_day0.py
"""
import os, sys, json, io, contextlib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o37'
TAG = os.environ.get('J_TAG', 'tall')
BOARDP = os.path.join(SP, 'bb_%s' % TAG, 'rl_after', 'rl_app_data.json')
OUTNAME = os.environ.get('J_DAY0_OUT', 'DAY0_J_%s.json' % TAG.upper())

os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_TALL='1',
                  RL_O36_LAM_S1=os.environ.get('J_DOSE', '0.0'),
                  RL_O36_KAPPA=os.environ.get('J_KAPPA', '0.24'),
                  RL_O36_GAMMA=os.environ.get('J_GU', '11.0'),
                  RL_O36_ETA=os.environ.get('J_ETA', '0.41'),
                  RL_O36_GAMMA_D=os.environ.get('J_GD', '14.0'),
                  RL_O36_LAMBDA=os.environ.get('J_REL', '1.08'),
                  PYTHONHASHSEED='0', RL_REPO=ROOT,
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
entry_derived = NSE['_entry29b_derived']; o31_D = NSE['o31_D']
BOARD_MD5 = hashlib.md5(open(BOARDP, 'rb').read()).hexdigest()
ROWS = {r['key']: r for r in json.load(open(BOARDP))['active']}
Y = MA.BASE_REF

out, mism = [], []
nND = nPOOL = 0
for p in MA.data:
    with contextlib.redirect_stdout(io.StringIO()):
        d0 = entry_derived(p, Y)
    if d0 is None:
        continue
    k = p.get('key') or MA.slug(p['player'])
    with contextlib.redirect_stdout(io.StringIO()):
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

DOC = dict(label='ORDER J — the day-0 reference regenerated on board %s (%s)' % (TAG, BOARD_MD5[:8]),
           board='ORDER J %s' % TAG, board_md5=BOARD_MD5,
           law='printed = round(day0_v0(p) * D(c_u)) — the ONE LAW at g=0, where rho(0)=0 and '
               'pi(0,c,s) == D(c) exactly',
           regeneration_reason='the owner-ruled tall/small factor changes the SITTER FADE, and a day-0 '
                               'sitter price IS the sitter fade; derived_v0 is bit-identical on 89 of 89',
           base_ref=Y, n_fresh_nd=nND, n_pool=nPOOL, n_wired=len(out),
           identity_all='%d of %d at tolerance 0' % (len(out) - len(mism), len(out)),
           mismatches=mism, rows=out)
json.dump(DOC, open(os.path.join(HERE, OUTNAME), 'w'), indent=1, sort_keys=True)
print('ORDER J PRINTED DAY-0 IDENTITY [%s]: %d of %d at tolerance 0 (ND %d, pool %d) on board %s'
      % (TAG, len(out) - len(mism), len(out), nND, nPOOL, BOARD_MD5[:12]))
if mism:
    print('MISMATCHES: %s' % mism[:10])
    sys.exit('ORDER J HALT: the printed day-0 identity does not hold on the written board.')
print('%s written.' % OUTNAME)
