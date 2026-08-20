#!/usr/bin/env python3
"""ORDER 44 — DAY0_SFXBASE.json: THE DAY-0 REFERENCE, REGENERATED ON THE LIVE R23 BOARD 68be10c7.

docs/evidence/candidate_31f/o31f_day0.py carried with FOUR declared changes and nothing else:

  (1) THE BOARD IS THE TRACKED LIVE BOARD, NOT A BUILT ONE. BOARDP is
      engine/rl_after/rl_app_data.json in this worktree — md5 68be10c79d0ee096455754e084bcf757, the
      shipped board, asserted below. No build is run by this file.
  (2) The legacy per-var env block (RL_GAMMA / RL_PICK1 / RL_RUCK_TAX / RL_RECENCY_DECAY /
      RL_PRIOR_TREES / PAR_RAMPS) is DROPPED. Those were that seat's shell defaults; the bake made
      the dial stack the shipped default and this file must read the SHIPPED expression, so it
      carries exactly the env run_emit_SFX.sh carries (RL_O31/RL_O32 + the path vars + the five
      thread pins). If dropping them changed a value the identity assert below would fail; it does
      not, and that is the proof rather than the claim.
  (3) the output filename (DAY0_SFXBASE.json) and the labels.
  (4) RL_O44_LVLMONO IS NOT SET. This file generates the reference on the OFF expression, on purpose:
      the reference must be the LIVE board's own day-0 law, and the candidates are then measured
      AGAINST it by the emitter's own fail-closed guard.

WHY THIS FILE EXISTS AT ALL — A FINDING, NOT HOUSEKEEPING.

  The standing day-0 reference is docs/evidence/final_candidate_2026-08-19/DAY0_CP.json (board
  a05fe951, pre-R23). Pointed at it, THIS SEAT'S DIAL-UNSET EMIT ON THE LIVE R23 TREE READ
  24 OF 89 AND FAILED CLOSED (EMIT_SFXBASE_STALEREF_out.txt, kept). That is NOT ORDER 44: the dial
  was unset. The R23 advance moved the unplayed clock c_u, so the sitter fade D(c_u) moved, so the
  printed day-0 price moved on 65 rows — by construction, exactly as ORDER D and ORDER K had to
  regenerate when they moved the fade. THE R23 ADVANCE DID NOT REGENERATE THE REFERENCE, so the
  ORDER 31-F replication guard fails closed for ANY emit on the R23 board. Filed as a finding of
  this seat, reported in the packet, NOT smoothed and NOT fixed here beyond what this act needs.

  The regenerated file is THIS SEAT'S, scoped to THIS ACT: it is the base the two candidate emits are
  measured against, so that "did ORDER 44 move a day-0 price?" is answered at tolerance 0 against a
  reference built on the same clock. It supersedes nothing on the record and re-pins nothing.

READ-ONLY on the engine and on the store.
"""
import os, sys, json, io, contextlib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('SFX_WT', os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
BOARDP = os.path.join(ROOT, 'engine', 'rl_after', 'rl_app_data.json')
LIVE = '68be10c79d0ee096455754e084bcf757'
OUTP = os.environ.get('SFX_DAY0_OUT', os.path.join(HERE, 'DAY0_SFXBASE.json'))

os.environ.update(RL_O31='1', RL_O32='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
os.environ.pop('RL_CONFIG_MODE', None)
os.environ.pop('RL_BUILD_LOCK_HELD', None)          # the thrice-burned rule: never ship an RL_ tooling var into the engine
assert os.environ.get('RL_O44_LVLMONO') in (None, ''), 'the reference is generated on the OFF expression'

BOARD_MD5 = hashlib.md5(open(BOARDP, 'rb').read()).hexdigest()
assert BOARD_MD5 == LIVE, 'BOARDP is not the live board: %s' % BOARD_MD5

sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
entry_derived = NSE['_entry29b_derived']; o31_D = NSE['o31_D']
ENGINE_HEAD = hashlib.md5(open(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py'), 'rb').read()).hexdigest()
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
    if p.get('_pool'):
        nPOOL += 1
    else:
        nND += 1
    out.append(dict(key=k, ty=p.get('type'), pos=MA.gfut(p), pick=p.get('pick'),
                    cell=('%s|%s' % (p.get('type'), MA.gfut(p))) if p.get('_pool') else None,
                    printed=int(printed) if printed is not None else None,
                    derived_v0=float(d0), fade_D=D, day0_price=price))

PRIOR = json.load(open(os.path.join(ROOT, 'docs/evidence/final_candidate_2026-08-19/DAY0_CP.json')))
pk = {r['key']: r for r in PRIOR['rows']}
now = {r['key']: r for r in out}
added = sorted(set(now) - set(pk)); dropped = sorted(set(pk) - set(now))
moved = sorted(k for k in set(now) & set(pk) if now[k]['printed'] != pk[k]['printed'])
v0_moved = sorted(k for k in set(now) & set(pk) if abs(now[k]['derived_v0'] - pk[k]['derived_v0']) != 0.0)

DOC = dict(label='ORDER 44 — the day-0 reference regenerated on THE LIVE R23 BOARD 68be10c7 (dial OFF)',
           authority='PREREG_STAIRCASE.md section 7 (the day-0 check rides every priced delivery); '
                     'regenerated because DAY0_CP.json (board a05fe951, pre-R23) reads 24 of 89 on the '
                     'R23 board with the dial UNSET — a finding about the R23 advance, not about ORDER 44',
           law='printed = round(day0_v0(p) * D(c_u)) — the ONE LAW at g=0, where rho(0)=0 and pi(0,c,s) == D(c) exactly',
           board='THE LIVE BOARD (dial unset)', board_md5=BOARD_MD5, engine_head=ENGINE_HEAD,
           store_md5=hashlib.md5(open(os.path.join(ROOT, 'engine/rl_after/rl_model_data.json'), 'rb').read()).hexdigest(),
           base_ref=Y, n_wired=len(out), n_fresh_nd=nND, n_pool=nPOOL,
           identity_all='%d of %d at tolerance 0' % (len(out) - len(mism), len(out)),
           mismatches=mism,
           supersedes='NOTHING ON THE RECORD. This file is this act\'s own base reference; DAY0_CP.json '
                      'stands unaltered and un-repointed on the record.',
           vs_DAY0_CP=dict(prior_board=PRIOR['board_md5'], n_prior=len(PRIOR['rows']),
                           population_added=added, population_dropped=dropped,
                           printed_moved=len(moved), printed_moved_keys=moved,
                           derived_v0_moved=len(v0_moved), derived_v0_moved_keys=v0_moved),
           rows=sorted(out, key=lambda r: r['key']))
open(OUTP, 'w').write(json.dumps(DOC, indent=1, sort_keys=True))

print('=== ORDER 44 — DAY-0 REFERENCE REGENERATED ON THE LIVE BOARD ===')
print('  board      %s   (live pin %s)' % (BOARD_MD5, LIVE))
print('  engine     %s   (the EDITED tree, dial OFF)' % ENGINE_HEAD)
print('  BASE_REF   %s' % Y)
print('  wired      %d   (fresh ND %d + pool %d)' % (len(out), nND, nPOOL))
print('  identity   %s' % DOC['identity_all'])
if mism:
    print('  *** MISMATCHES *** %s' % mism[:10])
print()
print('=== AGAINST THE STANDING (PRE-R23) REFERENCE DAY0_CP.json %s ===' % PRIOR['board_md5'][:8])
print('  population  added %d %s   dropped %d %s' % (len(added), added or '', len(dropped), dropped or ''))
print('  printed day-0 prices MOVED on %d of %d rows  (the R23 clock advance moving D(c_u))' % (len(moved), len(pk)))
print('  derived_v0 (the raw entry object) moved on %d rows' % len(v0_moved))
print('  -> this is why the standing reference reads 24 of 89 on the R23 board with the DIAL UNSET.')
print('     IT IS NOT ORDER 44. Reported as a finding of the R23 advance.')
print()
print('  written: %s  (%s)' % (OUTP, hashlib.md5(open(OUTP, 'rb').read()).hexdigest()[:12]))
