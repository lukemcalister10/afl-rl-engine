"""
FULL-REGISTER RECONCILIATION (READ-ONLY) — evidence/lti/
For every player in LTI_REGISTER_2026-07-02.md, resolve the store row by IDENTITY
(name -> exact/alias match; print coh/pick/pos, never surname alone) and report which
engine BRANCH fires and the availability-relevant mechanism signals. MECHANISM, not $ audit.
"""
import io, contextlib
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    src = open('/home/claude/rl_workspace/rl_after/_merged_recover.py').read().split('print("=== AFTER')[0]
    exec(src, g)
MA = g['MA']; ev = g['ev']; cp = g['cp']; PR = g['PR']
nseas_pro = g['nseas_pro']; delisted = g['delisted']; v0_start = g['v0_start']
_ev_click = g['_ev_click']; _m3_s = g['_m3_s']; _M3PIN = g['_M3PIN']; M3_FE = g['M3_FE']

# name -> store name aliases (collision-guarded: Max King -> Maxwell King per START_HERE §5)
ALIAS = {'Nic Martin': 'Nicholas Martin', 'Max King': 'Maxwell King'}

def resolve(nm):
    nm = ALIAS.get(nm, nm)
    exact = [p for p in MA.data if p['player'].lower() == nm.lower() and MA.GRP.get(p.get('pos'))]
    if exact:
        return exact
    return [p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]

def g26(p):
    return next((r['games'] for r in p['scoring'] if r['year'] == 2026), None)  # None = no row

def branch(p):
    if delisted(p):
        return 'DELIST-scrap'
    if nseas_pro(p, 2026) == 0:
        return 'SIT-OUT'
    return 'NORMAL'

def m3bump(p):
    s = _m3_s(p, 2026)
    _M3PIN['on'] = False; c = _ev_click(p, 2026)
    if s > 0 and M3_FE < 1.0 and not delisted(p):
        _M3PIN['on'] = True
        try: pin = _ev_click(p, 2026)
        finally: _M3PIN['on'] = False
    else:
        pin = c
    return c, pin

SECTION_A = {  # player: timing-class
 'Jack Payne':'2025','Matt Carroll':'2026','Jesse Motlop':'2026pre','Harry O\'Farrell':'2025',
 'Jamie Elliott':'2026','Reef McInnes':'2025+2026','Oscar Steene':'2026','Brayden Fiorini':'2026',
 'Lewis Hayes':'2025+2026','Nic Martin':'2025','Toby Conway':'2025','Tom Green':'2026',
 'Josh Kelly':'2026pre','Darcy Jones':'2025','Nathan Wardius':'2026pre','Jai Culley':'2026',
 'Jack Viney':'2026pre','Andy Moniz-Wakefield':'2026','Jackson Archer':'2026pre','Blake Thredgold':'2026pre',
 'Ollie Lord':'2026','Esava Ratugolea':'2026','Josh Sinn':'2026pre','Josh Gibcus':'2026',
 'Judson Clarke':'2025','Sam Flanders':'2026','Liam Hetherton':'2026pre','Max King':'2026pre',
 'Noah Long':'2026pre','Jacob Newton':'2026','Deven Robertson':'2026','Sam Darcy':'2026'}
SECTION_B = ['Archie May','Harley Barker','Brody Mihocek','Toby Pink','Mani Liddy','Ewan Mackinlay',
             'Connor Rozee','Jonty Faull','Joel Amartey','Noah Chamberlain','Harry Edwards']

from collections import Counter
brn = Counter(); missing = []
print(f"{'REGISTER NAME':22s}{'cls':9s}{'IDENTITY (store)':40s}{'g26':>4s}{'nsP':>4s}{'dl':>3s}{'b2hc':>6s}{'branch':>13s}{'ev':>6s}{'click':>6s}{'pin':>6s}")
def emit(nm, cls):
    ps = resolve(nm)
    if not ps:
        missing.append(nm); print(f"{nm[:21]:22s}{cls:9s}{'-- NOT IN STORE --':40s}"); return
    p = ps[0]
    ident = f"coh{p.get('year')} pk{p.get('pick')} {MA.gfut(p):8s}{'(2+dup)' if len(ps)>1 else ''}"
    b = branch(p); brn[b] += 1
    c, pin = m3bump(p)
    gg = g26(p); gs = '-' if gg is None else str(gg)
    print(f"{nm[:21]:22s}{cls:9s}{ident:40s}{gs:>4s}{nseas_pro(p,2026):>4d}{'Y' if delisted(p) else '-':>3s}{p.get('_b2hc',0.0):>6.3f}{b:>13s}{ev(p):>6d}{c:>6d}{pin:>6d}")

print("=== SECTION A (LTI — deserve return-season haircut) ===")
for nm, cls in SECTION_A.items():
    emit(nm, cls)
print("\n=== SECTION B (out 2026, no haircut per register) ===")
for nm in SECTION_B:
    emit(nm, 'B-out')
print("\n=== BRANCH DISTRIBUTION ===", dict(brn))
print("MISSING FROM STORE:", missing)
