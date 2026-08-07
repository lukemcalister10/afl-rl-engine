"""STAGE 6 TEACHING MEASUREMENT — the conditioned development residual on the ESTABLISHED leg.

READ-ONLY.  Teaching source: the FROZEN baseline walk-forward matrix
docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json (md5 b564b12e),
the same matrix the stage-6 cross-section (issue #334 comment 5215260604) measured.  Never re-emitted
for teaching (directive 5217307894 section 2, "taught ONCE, frozen").

POPULATION.  Every (player, evaluation year Y) the engine routes through the ns>=1 arm of ev() —
i.e. nseas_pro(p,Y) >= 1, the ESTABLISHED leg.  Addendum 1 (5217452004) pools the year-1, year-2 and
year-3 evaluation rows so the fade is ENDOGENOUS to the surface rather than decreed.

STATISTIC.  F = mean_k [ v(Y+k) / 1.0939**k ], k = 1..4, busts / out-of-window = 0, read off the
FROZEN matrix vpath; price = the same matrix's own walk-forward price at Y.  F' = F / price.
F' > 1 = under-priced.  The estimand named by Addendum 1 is the VALUE-WEIGHTED aggregate
sum(F)/sum(price); the MEDIAN F' is pre-registered alongside it and printed at every rung.

MECHANISM STATE captured per row, all of it engine-native and all of it recomputable at build time
from the record to date (the recalculation law — nothing here is stored on a player):
  tau     the engine's continuous round-driven clock  max(0,Y-debutyr) + fE**1.5
  cls     the engine's three position classes, _sitout_cls(gfut) -> RUCK / KPP / nonKPP
  pos     gfut, for the KPD/KPF split that the KPP class collapses (sub-dial, Addendum 1 F11)
  pk      MA.effpk
  gcum    CUMULATIVE career games through Y   (the recalculation law axis)
  pr      bestlvl(p,Y)/max(1,par) — the DEMONSTRATED-LEVEL statistic ev() already computes at the
          site, continuous, no thresholds (terciles are REPORTING knots only)
  age     draft age (None => the correction is identically zero, Addendum 1 F13; rows enumerated)
"""
import os, sys, io, contextlib, json, hashlib
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_s6_measure'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G['MA']; cp = G['cp']; PR = G['PR']
delisted = G['delisted']; nseas_pro = G['nseas_pro']; bestlvl = G['bestlvl']
v0_start = G['v0_start']; entry_anchor = G['entry_anchor']
_sitout_cls = G['_sitout_cls']; _fEy = G['_fEy']; _prod_path = G['_prod_path']
_fa_year = G['_fa_year']; _form_anchor_clock = G['_form_anchor_clock']

MATRIX = os.environ.get('RL_MATRIX',
    REPO + '/docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json')
MMD5 = hashlib.md5(open(MATRIX, 'rb').read()).hexdigest()
assert MMD5 == 'b564b12e533119f49c2c6bb0c92a5d91', 'teaching matrix md5 mismatch: ' + MMD5
MX = json.load(open(MATRIX))
RECS = {(r['key'], r['type'], r['year']): r for r in MX['recs']}

DISC = 1.0939
KMAX = int(os.environ.get('RL_KMAX', '4'))
YR_LO, YR_HI = 2004, 2022          # teaching window: a class must have outcomes to teach from
FORCE_MAJEURE = {'thomas-boyd', 'paddy-mccartin'}

def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p) and p.get('key') not in FORCE_MAJEURE]

def _min_tenure(p):
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = MA.effpk(p)
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2
def _debut_year(p):
    C = p.get('year')
    if C is None: return None
    return C if p.get('type') == 'MSD' else C + 1
def _listed_through(p, lastscore):
    LL = p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d = _debut_year(p)
    return max((d + _min_tenure(p) - 1) if d is not None else 0, lastscore)

ROWS = []
for Y in range(2004, 2027):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], p.get('_retired'), p.get('_last_listed'))
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        eff_last = _listed_through(p, lastscore)
        p['_retired'] = False
        p['_last_listed'] = eff_last if (eff_last is not None and eff_last < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    for p in players:
        C = p.get('year')
        if C is None or C > Y or not (YR_LO <= C <= YR_HI): continue
        try:
            if delisted(p): continue
            if nseas_pro(p, Y) < 1: continue          # the ESTABLISHED leg — the ns>=1 arm of ev()
            fe = _fEy(Y, p)
            tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
            pos = MA.gfut(p); cls = _sitout_cls(pos); pk = int(MA.effpk(p))
            gcum = sum(x['games'] for x in p['scoring'] if x['year'] <= Y)
            with _form_anchor_clock(): el = PR.tenure(p, _fa_year(Y))
            par = PR.par_at_p(p, pos, min(MA.effpk(p), cp.KMAX), min(max(el, 1), 6), _fa_year(Y))
            pr = bestlvl(p, Y) / max(1, par)
            with contextlib.redirect_stdout(io.StringIO()):
                e = _prod_path(p, Y)
            age = cp._age_asof(p, C) if hasattr(cp, '_age_asof') else None
        except Exception:
            continue
        ROWS.append(dict(key=p.get('key'), typ=p.get('type'), C=C, Y=Y, N=Y - C,
                         tau=float(tau), cls=cls, pos=pos, pk=pk, gcum=float(gcum),
                         pr=float(pr), el=float(el), e=float(e),
                         A=float(entry_anchor(p)), v0=float(v0_start(p))))
    for p in players:
        if id(p) in saved: p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

def rec_for(key, C):
    for t in ('ND', 'MSD', 'RD', 'PDA', 'PDN', 'PDS', 'SSP', 'UNR', 'IRE'):
        if (key, t, C) in RECS: return RECS[(key, t, C)]
    return None

kept = []
for r in ROWS:
    rec = rec_for(r['key'], r['C'])
    if rec is None: continue
    vmap = {y: (float(v) if v is not None else 0.0) for y, v in zip(rec['yrs'], rec['vpath'])}
    price = vmap.get(r['Y'])
    if not price or price <= 0: continue
    ks = [k for k in range(1, KMAX + 1) if r['Y'] + k <= 2026]
    if not ks: continue          # the cross-section's own convention: partial windows kept, busts = 0
    F = float(np.mean([vmap.get(r['Y'] + k, 0.0) / (DISC ** k) for k in ks]))
    kept.append(dict(r, price=float(price), F=F, nk=len(ks),
                     age=(rec.get('age_draft') if rec.get('age_draft') is not None else None),
                     nd=bool(rec.get('type', r['typ']) == 'ND' and not rec.get('pickless')),
                     is_pool=bool(rec.get('is_pool'))))

print("established-leg rows scanned = %d ; with complete %d-year realized window = %d"
      % (len(ROWS), KMAX, len(kept)))
json.dump(kept, open(os.environ.get('RL_OUT', '.') + '/s6_rows.json', 'w'))
print("teaching matrix md5 = %s" % MMD5)

def agg(rows):
    if not rows: return None
    sp = sum(x['price'] for x in rows); sf = sum(x['F'] for x in rows)
    med = float(np.median([x['F'] / x['price'] for x in rows]))
    return dict(n=len(rows), agg=(sf / sp if sp > 0 else float('nan')), med=med,
                mean=float(np.mean([x['F'] / x['price'] for x in rows])))
def show(name, rows):
    a = agg(rows)
    if a: print("%-34s %6d  agg %8.4f   median %8.4f   mean %8.4f"
                % (name, a['n'], a['agg'], a['med'], a['mean']))

# THE TEACHING POPULATION.  The cross-section of record (5215260604) measured the ND 1-64 leg; the
# pool routes are stage 7's own directive (5217529020) and their own measurement (5217499636) reads the
# pool established leg HONEST.  The pick taper below zeroes the correction past pick ~52, so the pool
# index (effpk 65) takes zero BY CONSTRUCTION — no separate population fence is needed or used.
ND = [x for x in kept if x['nd'] and 1 <= x['pk'] <= 64]
print("\n== ND 1-64 (the teaching population) ==")
for NN in (1, 2, 3, 4, 5, 6):
    show("evaluation year %d" % NN, [x for x in ND if x['N'] == NN])
print("\n== whole established leg incl. pool (reporting only) ==")
for NN in (1, 2, 3):
    show("evaluation year %d" % NN, [x for x in kept if x['N'] == NN])
print()
kept_all = kept; kept = ND
y1 = [x for x in kept if x['N'] == 1]
show("YEAR-1 ESTABLISHED (the leg)", y1)
for lo, hi, nm in [(1, 10, "pick 1-10"), (1, 20, "pick 1-20"), (21, 40, "pick 21-40"),
                   (41, 64, "pick 41-64"), (65, 999, "pool")]:
    show("  yr1 " + nm, [x for x in y1 if lo <= x['pk'] <= hi])
for c in ('nonKPP', 'KPP', 'RUCK'):
    show("  yr1 cls " + c, [x for x in y1 if x['cls'] == c])
for pz in ('MID', 'SF', 'SD', 'KPF', 'KPD', 'RUCK'):
    show("  yr1 pos " + pz, [x for x in y1 if x['pos'] == pz])
prs = sorted(x['pr'] for x in y1)
t1, t2 = prs[len(prs) // 3], prs[2 * len(prs) // 3]
print("  demonstrated-level (pr) tercile knots: %.4f / %.4f" % (t1, t2))
show("  yr1 pr low tercile", [x for x in y1 if x['pr'] < t1])
show("  yr1 pr mid tercile", [x for x in y1 if t1 <= x['pr'] < t2])
show("  yr1 pr top tercile", [x for x in y1 if x['pr'] >= t2])
med_pr = float(np.median(prs))
show("  yr1 pick1-20 x above-median pr", [x for x in y1 if x['pk'] <= 20 and x['pr'] >= med_pr])
show("  yr1 pick1-20 x below-median pr", [x for x in y1 if x['pk'] <= 20 and x['pr'] < med_pr])
show("  yr1 pick1-10 x top tercile pr", [x for x in y1 if x['pk'] <= 10 and x['pr'] >= t2])
for lo, hi, nm in [(0, 5, "gcum 0-5"), (6, 9, "gcum 6-9"), (10, 15, "gcum 10-15"),
                   (16, 22, "gcum 16-22"), (23, 99, "gcum 23+")]:
    show("  yr1 " + nm, [x for x in y1 if lo <= x['gcum'] <= hi])
show("  yr1 draft age <=18", [x for x in y1 if x['age'] is not None and x['age'] <= 18])
show("  yr1 draft age 19-20", [x for x in y1 if x['age'] is not None and 19 <= x['age'] <= 20])
show("  yr1 draft age 21+", [x for x in y1 if x['age'] is not None and x['age'] >= 21])
show("  yr1 draft age UNKNOWN", [x for x in y1 if x['age'] is None])
