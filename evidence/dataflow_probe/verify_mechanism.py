#!/usr/bin/env python3
# Verify the dual-namespace _REAL bug in rl_export.py: the players it prices are exec'd from rl_model.py
# in a DIFFERENT namespace than the _merged_recover.py that builds _REAL, so id(p) in _REAL is False and
# every _REAL-gated layer (ruck cap / v7 age-taper / floor) is dropped at export.
# Run from engine/rl_after with the panel env (see probe.sh wrapper).
import os, io, contextlib, json
RA = os.path.dirname(os.path.abspath(__file__)) + '/../../engine/rl_after'
RA = os.path.abspath(RA); os.chdir(RA)

# (A) SINGLE-NAMESPACE engine (the panel/true path): ev() sees id(p) in _REAL -> layers apply.
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA, ev, _REAL = g['MA'], g['ev'], g['_REAL']
em_true = [p for p in MA.data if p['key'] == 'louis-emmett'][0]
print("(A) SINGLE-NS true engine:")
print("    id(emmett) in _REAL      :", id(em_true) in _REAL)
print("    ev(emmett,2026) [capped] :", ev(em_true, 2026))
daic_true = [p for p in MA.data if p['key'] == 'nick-daicos'][0]
print("    ev(daicos,2026)          :", ev(daic_true, 2026))

# (B) DUAL-NAMESPACE (exact rl_export.py pattern): players from a SEPARATE rl_model exec.
ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('rl_model.py').read().split("print('PVC:'")[0], ns)
players = ns['players']
ens = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], ens)
_ev = ens['ev']; _REAL2 = ens['_REAL']
em_exp = [p for p in players if p['key'] == 'louis-emmett'][0]
daic_exp = [p for p in players if p['key'] == 'nick-daicos'][0]
print("(B) DUAL-NS export path:")
print("    id(emmett_ns) in _REAL   :", id(em_exp) in _REAL2, "  <- export players are FOREIGN objects")
print("    _ev(emmett_ns,2026)      :", _ev(em_exp, 2026), " <- cap DROPPED")
print("    _ev(daicos_ns,2026)      :", _ev(daic_exp, 2026), " <- v7 layer DROPPED")

# (C) shipped board values
B = json.load(open('../../data/rl_build/rl_app_data.json'))
sv = {r['key']: r['v'] for r in B['active']}
print("(C) shipped board 'v': emmett=%s  daicos=%s" % (sv['louis-emmett'], sv['nick-daicos']))
print("    => board matches DUAL-NS (buggy) path, NOT the true single-NS engine")
