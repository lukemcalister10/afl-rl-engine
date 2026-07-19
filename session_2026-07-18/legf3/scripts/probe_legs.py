#!/usr/bin/env python3
# LEG F3 — leg-level decomposition (READ-ONLY). Pin which valuation leg drops forward.
import os, io, contextlib
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']; effpk = G['effpk']; GRP = G['GRP']; peak_est = G['peak_est']
raw_ev = g['raw_ev']; iso_eff = g['iso_eff']; prod_path = g['_prod_path']; v0start = g['v0_start']
v0raw = g['_v0_raw']; ycred = g['_ycred_mult']; devadv = G['_dev_advance']; leveldemo = G['level_demo']; levelnow = G['level_now']
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

def setstate(Y, form):
    MA._LENS_FORM = form; MA.AGE_REF = Y; MA.BASE_REF = form if form is not None else Y; MA._pe_clear()
def clearstate():
    MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

names = ['Jagga Smith', 'Xavier Lindsay', 'Taj Hotton', 'Sam Lalor', 'Zeke Uwland', 'Daniel Curtin', 'Nate Caddy', 'Jed Walter']
print("%-16s %4s %3s | %7s %7s %7s | %6s %6s | %6s %6s | %6s %6s | %6s" %
      ("name","age","pk","ev26","ev27","V0","rev26","rev27","iso26","iso27","Ldem","Ladv","pe"))
for nm in names:
    p = next((pp for pp in players if nm.lower() in (pp.get('player') or '').lower()), None)
    if not p: continue
    clearstate()
    ev26 = ev(p, 2026); r26 = raw_ev(p, 2026); i26 = iso_eff(p, 2026); pp26 = prod_path(p, 2026)
    V0 = v0start(p); Ldem = leveldemo(p); pe = peak_est(p)
    setstate(2027, 2026)
    ev27 = ev(p, 2027); r27 = raw_ev(p, 2027); i27 = iso_eff(p, 2027); pp27 = prod_path(p, 2027); Ladv = levelnow(p)
    clearstate()
    print("%-16s %4s %3s | %7.0f %7.0f %7.0f | %6.0f %6.0f | %6.3f %6.3f | %6.1f %6.1f | %6.1f" %
          (nm[:16], age(p), effpk(p), ev26, ev27, V0, r26, r27, i26, i27, Ldem or -1, Ladv or -1, pe or -1))
print("\nlegend: rev=raw_ev(production anchor incl young-credit), iso=iso_eff, Ldem=level_demo(2026), Ladv=level_now(2027 adv), pe=peak_est")
print("If rev27<<rev26 -> the production anchor itself collapses forward (proj_from_peak/dev_advance).")
print("If rev27~=rev26 but ev27<<ev26 -> a floor/staleness gate drops the pedigree at k>=1.")
