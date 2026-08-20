#!/usr/bin/env python3
"""ORDER Q — STEP 0, CHECK 0A. Does the supervisor's inferred pedigree leg equal the engine's own?

He inferred, per young row, from BOARD prices and the two charge factors:
    ped_P = (P_K - P_P) * fP / (fK - fP)
This reads the engine's ACTUAL legs on the ORDER P dial line and checks:
  1. the engine's own identity  price = rho*e + pi*pedigree + age_credit, M3 included
  2. whether the row has ONE charge factor at all (the M3 rows have two)
  3. the inference run against the true leg, on the rounded board prices he actually had
NO ENGINE ARITHMETIC IS CHANGED. The only instrumentation is a recorder on the blend site.
"""
import os, sys, json, math, hashlib, io, contextlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oq_lib as L

SP = L.SP
BP = {t: SP + '/op/bb_%s/rl_after/rl_app_data.json' % t for t in ('Kref', 'P')}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in BP}
print('BOARD PINS: Kref %s  P %s' % (MD5['Kref'][:8], MD5['P'][:8]))
assert MD5['Kref'].startswith('f3101883') and MD5['P'].startswith('374d4e44'), 'board pins wrong — HALT'
B = {t: {r['key']: r for r in json.load(open(BP[t]))['active']} for t in BP}
FNUM = json.load(open(L.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']

NS = L.load(RL_O37='1')
NS['_REC'] = L.install_recorder(NS)
import rl_model as MA
print('engine %s  store %s  players %d  numeraire %.4f'
      % (hashlib.md5(open(L.ROOT + '/engine/rl_after/_merged_recover.py', 'rb').read()).hexdigest()[:8],
         hashlib.md5(open(L.ROOT + '/engine/rl_after/rl_model_data.json', 'rb').read()).hexdigest()[:8],
         len(MA.players), FNUM))
EV = NS['ev']
raw = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        raw[p['key']] = EV(p, 2026)
bad = [k for k in raw if k in B['P'] and int(round(raw[k] / FNUM)) != B['P'][k]['v']]
print('IN-PROCESS BOARD REPRODUCTION vs 374d4e44: %d of %d rows disagree' % (len(bad), len(raw)))
assert not bad, 'the in-process engine does not reproduce the built board — HALT'

R = {}
for p in MA.players:
    a = L.assemble(NS, p, 2026)
    a.update(name=p.get('player'), pick=p.get('pick'), type=p.get('type'),
             pool=bool(p.get('_pool')), pos=MA.gfut(p),
             age=(2026 - int(p['_by'])) if p.get('_by') else None, raw=raw[p['key']])
    R[p['key']] = a

print('\n1. THE DECOMPOSITION, WITH M3 CARRIED')
d = [(k, abs(r['price'] - r['raw'])) for k, r in R.items() if r['price'] is not None]
print('   rows decomposed: %d of %d' % (len(d), len(R)))
print('   worst |decomposition - ev()|: %.3e' % max(x[1] for x in d))
print('   rows above 1e-9: %d' % sum(1 for _, x in d if x > 1e-9))
print('   rows the engine prices through TWO blend calls (the M3 clock pin): %d'
      % sum(1 for r in R.values() if r['m3']))

YOUNG = [r for r in R.values() if r['age'] is not None and r['age'] < 24 and (r['g_c'] > 0)
         and r['key'] in B['P'] and r['key'] in B['Kref'] and (r['type'] == 'ND' or r['pool'])
         and r['price'] is not None]
print('\n   young ND+pool rows, age<24, games>0: %d' % len(YOUNG))
SEL = [r for r in YOUNG if abs(r['f_K_eff'] - r['f_eff']) >= 0.02]
print('   with |fK - fP| >= 0.02 on the EFFECTIVE factor: %d   <- supervisor says 267' % len(SEL))
SEL1 = [r for r in YOUNG if abs(r['fK_c'] - r['f_c']) >= 0.02]
print('   with |fK - fP| >= 0.02 on the FULL-CLICK factor: %d' % len(SEL1))
print('   of the selected rows, how many are M3 two-call rows: %d of %d'
      % (sum(1 for r in SEL if r['m3']), len(SEL)))
m3sel = [r for r in SEL if r['m3']]
if m3sel:
    sp = max(abs(r['f_c'] - r['f_p']) for r in m3sel)
    print('   worst gap between a row\'s TWO ORDER P charge factors: %.4f' % sp)
    print('   worst gap between its two ORDER K factors:            %.4f'
          % max(abs(r['fK_c'] - r['fK_p']) for r in m3sel))

print('\n2. THE INFERENCE  ped_P = (P_K - P_P) * fP / (fK - fP)')
out = []
for r in SEL:
    k = r['key']
    PK, PP = B['Kref'][k]['v'], B['P'][k]['v']
    true_ped = r['ped_leg'] / FNUM
    exact_dP = (r['ped_leg_K'] - r['ped_leg']) / FNUM
    for tag, fP, fK in (('eff', r['f_eff'], r['f_K_eff']), ('click', r['f_c'], r['fK_c'])):
        pass
    dEff = r['f_K_eff'] - r['f_eff']
    inf = (PK - PP) * r['f_eff'] / dEff if dEff else None
    dClk = r['fK_c'] - r['f_c']
    infc = (PK - PP) * r['f_c'] / dClk if dClk else None
    out.append(dict(key=k, name=r['name'], pick=r['pick'], pool=r['pool'], age=r['age'],
                    g=r['g_c'], m3=r['m3'], fK=r['f_K_eff'], fP=r['f_eff'], fKc=r['fK_c'],
                    fPc=r['f_c'], PK=PK, PP=PP, dPb=PK - PP, dP_exact=exact_dP,
                    true_ped=true_ped, inf=inf, inf_click=infc,
                    v0=r['ped'] / NS['_PL_F'], s_P=r['s_P'],
                    prod=r['prod_leg'] / FNUM, credit=r['credit'] / FNUM,
                    pi_base=r['pi_base_eff']))
dd = [abs(x['dPb'] - x['dP_exact']) for x in out]
print('   (a) |board(P_K - P_P) - engine exact leg difference|: max %.4f mean %.4f  (pure board rounding: <=1.0)'
      % (max(dd), sum(dd) / len(dd)))
for tag, fld in (('EFFECTIVE (M3-correct)', 'inf'), ('FULL-CLICK only (what a single-factor read gives)', 'inf_click')):
    e = [abs(x[fld] - x['true_ped']) for x in out]
    ep = [100 * abs(x[fld] - x['true_ped']) / max(1e-9, x['true_ped']) for x in out]
    print('   (b) inference on the %s factor:' % tag)
    print('       |inferred - TRUE| points : max %8.1f  mean %6.2f  median %6.2f' % (max(e), sum(e) / len(e), sorted(e)[len(e) // 2]))
    print('       as %% of the true leg    : max %8.2f%% mean %6.2f%% median %6.2f%%' % (max(ep), sum(ep) / len(ep), sorted(ep)[len(ep) // 2]))
    print('       rows off by >2%% of the leg: %d of %d;  by >1 board point: %d of %d'
          % (sum(1 for z in ep if z > 2.0), len(ep), sum(1 for z in e if z > 1.0), len(e)))
print('\n   THE TEN WORST on the effective factor:')
for x in sorted(out, key=lambda z: -abs(z['inf'] - z['true_ped']))[:10]:
    print('     %-24s %-5s age %2d %5.0fg M3=%d fK %.4f fP %.4f  true %8.1f  inferred %8.1f  %+8.1f (%+7.2f%%)'
          % (x['name'][:24], x['pick'] if not x['pool'] else 'pool', x['age'], x['g'], x['m3'],
             x['fK'], x['fP'], x['true_ped'], x['inf'], x['inf'] - x['true_ped'],
             100 * (x['inf'] - x['true_ped']) / max(1e-9, x['true_ped'])))

json.dump(dict(meta=dict(boards={t: MD5[t][:8] for t in MD5}, F=FNUM, n=len(R),
                         n_young=len(YOUNG), n_sel=len(SEL), n_m3=sum(1 for r in R.values() if r['m3'])),
               sel=out, rows=list(R.values())), open(HERE + '/STEP0A_Q.json', 'w'), indent=1, default=str)
print('\nwrote STEP0A_Q.json')
