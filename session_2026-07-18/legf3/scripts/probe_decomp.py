#!/usr/bin/env python3
# LEG F3 — decomposition probe (READ-ONLY; mirrors rl_export's ev sequence).
# Reproduces the item-352 cohort finding on THIS container and decomposes the forward
# pedigree strip per named young high-pick row. No board write; no engine mutation persisted.
import os, io, contextlib, json, statistics as st
from collections import defaultdict
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']
GRP = G['GRP']; age = G['age']; effpk = G['effpk']; level_now = G['level_now']; peak_est = G['peak_est']
v0raw = g.get('_v0_raw'); ycred = g.get('_ycred_mult'); ycgames = g.get('_ycred_games'); raw_ev = g.get('raw_ev')
nqual = g.get('_nqual')
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

def val_at(p, Y, form):
    MA._LENS_FORM = form
    try:
        return ev(p, Y)
    finally:
        MA._LENS_FORM = None
        MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

def games_asof(p, Y):
    d0 = MA.__dict__.get('cp') and None
    try:
        return ycgames(p, Y)
    except Exception:
        return sum(x.get('games', 0) for x in p['scoring'] if x['year'] <= Y)

rows = []
for p in players:
    v   = val_at(p, 2026, None)
    vP1 = val_at(p, 2027, 2026)
    vP2 = val_at(p, 2028, 2026)
    vM1 = val_at(p, 2025, None)
    a = age(p)
    rows.append(dict(key=p.get('key'), name=p.get('player'), pos=GRP.get(p.get('pos')),
                     age=a, pk=effpk(p), type=p.get('type'),
                     g=games_asof(p, 2026),
                     v=v, vP1=vP1, vP2=vP2, vM1=vM1))

def cohort(a):
    if a is None: return 'unknown'
    if a <= 23: return 'developing(<=23)'
    if a <= 27: return 'mid(24-27)'
    return 'veteran(>=28)'

coh = defaultdict(lambda: dict(n=0, now=0.0, fwd=0.0))
for r in rows:
    c = cohort(r['age']); coh[c]['n'] += 1; coh[c]['now'] += r['v'] or 0; coh[c]['fwd'] += r['vP1'] or 0

Sv  = sum(r['v'] or 0 for r in rows); SvP1 = sum(r['vP1'] or 0 for r in rows)
SvP2 = sum(r['vP2'] or 0 for r in rows); SvM1 = sum(r['vM1'] or 0 for r in rows)
print("=== CONTAINER-RELATIVE TOTALS (raw ev units; numeraire /F cancels in ratios) ===")
print("n=%d  Sv=%.0f  SvP1=%.0f (%.1f%%)  SvP2=%.0f  SvM1=%.0f (back %.1f%%)" %
      (len(rows), Sv, SvP1, 100*(SvP1/Sv-1), SvP2, SvM1, 100*(Sv/SvM1-1)))
print("\n=== JOB2 COHORT DECOMPOSITION now->+1 (the inverted gradient) ===")
for c in ('developing(<=23)', 'mid(24-27)', 'veteran(>=28)'):
    x = coh[c]; d = x['fwd'] - x['now']
    print("  %-18s n=%3d  now=%9.0f  +1=%9.0f  d=%+9.0f  mean=%+7.1f  %+6.1f%%" %
          (c, x['n'], x['now'], x['fwd'], d, d/x['n'], 100*d/x['now']))

# focused decomposition — young high-pick low-games rows
print("\n=== JOB3 PEDIGREE STRIP — young<=23, pick<=20, games<=40 ===")
young_hp = [r for r in rows if (r['age'] or 99) <= 23 and (r['pk'] or 999) <= 20 and (r['g'] or 0) <= 40]
young_hp.sort(key=lambda r: (r['v'] or 0) - (r['vP1'] or 0), reverse=True)
Syhp = sum(r['v'] for r in young_hp); Syhp1 = sum(r['vP1'] for r in young_hp)
print("  n=%d  now=%.0f  +1=%.0f  lost=%.0f (%.1f%%)" % (len(young_hp), Syhp, Syhp1, Syhp-Syhp1, 100*(Syhp-Syhp1)/Syhp))
print("  %-22s %3s %3s %4s %8s %8s %8s   V0     yc26  yc27  pe26  pe27" % ('name','age','pk','g','v','vP1','lost'))
for r in young_hp[:14]:
    p = next(pp for pp in players if pp.get('key') == r['key'])
    V0 = v0raw(p) if v0raw else float('nan')
    MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear(); yc26 = ycred(p, 2026) if ycred else 1; pe26 = peak_est(p)
    MA._LENS_FORM = 2026; MA.BASE_REF = 2026; MA.AGE_REF = 2027; MA._pe_clear()
    yc27 = ycred(p, 2027) if ycred else 1; pe27 = peak_est(p)
    MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    print("  %-22s %3s %3s %4s %8.0f %8.0f %8.0f  %6.0f %5.3f %5.3f %5.1f %5.1f" %
          (r['name'][:22], r['age'], r['pk'], r['g'], r['v'], r['vP1'], r['v']-r['vP1'], V0, yc26, yc27, pe26, pe27))

json.dump(rows, open(os.environ.get('PROBE_OUT', '/tmp/probe_rows.json'), 'w'))
print("\n[wrote rows ->", os.environ.get('PROBE_OUT', '/tmp/probe_rows.json'), "]")
