"""
LTI / AVAILABILITY MECHANISM PROBE (READ-ONLY on engine/data) — evidence/lti/
Loads the BAKED engine (_merged_recover.py, md5 c47cb43d) exactly as run_panel.sh does,
then characterises how it treats injured / zero-games players. Prints MECHANISM decomposition,
not just prices. Magnitudes are state-labelled [BAKED c47cb43d].

Name-collision guard: every single-player line prints IDENTITY (player | cohort-year | pick | pos),
never surname alone. Two real "Max King"s etc. live in this register.

Run:
  cd /home/claude/rl_workspace/rl_after
  PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 \
  RL_PRIOR_TREES=400 PAR_RAMPS=22 PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor \
  python3 /home/user/afl-rl-engine/evidence/lti/probe_availability.py
"""
import io, contextlib, os
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    src = open('/home/claude/rl_workspace/rl_after/_merged_recover.py').read().split('print("=== AFTER')[0]
    exec(src, g)
MA = g['MA']; ev = g['ev']; cp = g['cp']; PR = g['PR']
nseas = g['nseas']; nseas_pro = g['nseas_pro']; delisted = g['delisted']
v0_start = g['v0_start']; sitout_ev = g['sitout_ev']; _prod_path = g['_prod_path']
_ev_click = g['_ev_click']; _m3_s = g['_m3_s']; _M3PIN = g['_M3PIN']
M3_FE = g['M3_FE']; M3_INPROG_Y = g['M3_INPROG_Y']

def ident(p):
    return f"{p['player'][:20]:20s} | coh{p.get('year')} | pk{MA.effpk(p):>3d} | {MA.gfut(p):8s}"

def g26(p):
    return next((r['games'] for r in p['scoring'] if r['year'] == 2026), 0)

def find(nm):
    c = [p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None

def decompose(p):
    """Return the mechanism trace for a single player."""
    if p is None:
        return None
    d = {}
    d['ident'] = ident(p)
    d['g2026'] = g26(p)
    d['ns_pro'] = nseas_pro(p, 2026)
    d['ns_raw'] = nseas(p, 2026)
    d['delisted'] = delisted(p)
    d['_b2hc'] = p.get('_b2hc', 0.0)
    d['ev'] = ev(p)
    # M3 clock-pin decomposition: click vs pinned eval
    s = _m3_s(p, 2026)
    d['m3_s'] = s
    d['m3_w'] = 1.0 - s * (1.0 - M3_FE) if s > 0 else 1.0
    _M3PIN['on'] = False
    d['ev_click'] = _ev_click(p, 2026)
    if s > 0 and M3_FE < 1.0 and not delisted(p):
        _M3PIN['on'] = True
        try:
            d['ev_pin'] = _ev_click(p, 2026)
        finally:
            _M3PIN['on'] = False
    else:
        d['ev_pin'] = d['ev_click']
    # counterfactual: force _b2hc=0 to isolate the haircut's contribution
    sav = p.get('_b2hc', 0.0)
    p['_b2hc'] = 0.0
    d['ev_no_b2hc'] = ev(p)
    p['_b2hc'] = sav
    # which ev branch fires
    if d['delisted']:
        d['branch'] = 'DELIST scrap (0.02*V0)'
    elif d['ns_pro'] == 0:
        d['branch'] = 'SIT-OUT (sitout_ev, ns_pro==0)'
    else:
        d['branch'] = 'NORMAL prod_path + staleness family'
    d['v0'] = v0_start(p)
    return d

def show(label, d):
    if d is None:
        print(f"  [{label}] NOT FOUND in store"); return
    print(f"  [{label}] {d['ident']}")
    print(f"        g2026={d['g2026']}  ns_pro={d['ns_pro']}  ns_raw={d['ns_raw']}  delisted={d['delisted']}  _b2hc={d['_b2hc']:.3f}")
    print(f"        branch = {d['branch']}")
    print(f"        V0_start={d['v0']:.0f}   ev(BAKED)={d['ev']}   ev_no_b2hc={d['ev_no_b2hc']}   -> b2hc costs {d['ev_no_b2hc']-d['ev']:+d}")
    print(f"        M3: s={d['m3_s']:.2f} w={d['m3_w']:.2f}  ev_click={d['ev_click']}  ev_pin={d['ev_pin']}  -> pin adds {d['ev_pin']-d['ev_click']:+d} at full weight")

print("="*78)
print("EXEMPLARS — the two observed behaviors (directive step 2)")
print("="*78)
for nm in ['Nic Martin', 'Connor Rozee', 'Tom Green']:
    show(nm, decompose(find(nm)))
    print()

print("="*78)
print("REGISTER RECONCILIATION by timing-class (directive step 3) — representative per class")
print("="*78)
# SECTION A representatives per timing class + a SECTION B (out, no haircut) representative
reps = [
    ('A/2025 (may return 2026)', 'Nic Martin'),
    ('A/2025 (may return 2026)', 'Jack Payne'),
    ('A/2026 (out till 2027)', 'Tom Green'),
    ('A/2026 (out till 2027)', 'Sam Darcy'),
    ('A/2026 pre-season (out till 2027)', 'Jesse Motlop'),
    ('A/2026 pre-season (out till 2027)', 'Jack Viney'),
    ('B/out-2026 no-haircut', 'Connor Rozee'),
    ('B/out-2026 no-haircut', 'Brody Mihocek'),
]
for cls, nm in reps:
    d = decompose(find(nm))
    if d is None:
        print(f"  [{cls}] {nm}: NOT FOUND"); continue
    print(f"  [{cls}]"); show(nm, d); print()
