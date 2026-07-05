#!/usr/bin/env python3
# Mirror rl_export.py's EXACT setup (lines 1-30) in ONE process and check whether the priced players
# are in the _merged_recover namespace's _REAL set. If not, the _REAL-gated layers are dropped at export.
import os, io, contextlib
RA = os.path.dirname(os.path.abspath(__file__)) + '/../../engine/rl_after'
os.chdir(os.path.abspath(RA))

# rl_export.py line 6: exec rl_model.py into ns -> players
ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("rl_model.py").read().split("print('PVC:'")[0], ns)
players = ns['players']

# rl_export.py lines 22-26: exec _merged_recover.py into _ens -> _ev (this import builds its OWN _REAL)
_ens = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], _ens)
_ev = _ens['ev']; _REAL = _ens['_REAL']

em = [p for p in players if p['key'] == 'louis-emmett'][0]
n_in = sum(1 for p in players if id(p) in _REAL)
print("exported players total        :", len(players))
print("exported players with id in _REAL:", n_in, "(of %d)" % len(players))
print("id(louis-emmett) in _REAL     :", id(em) in _REAL)
with contextlib.redirect_stdout(io.StringIO()):
    v = _ev(em, 2026)
print("_ev(louis-emmett,2026) [export]:", v, " (853 = capped/true; ~1361 = cap dropped)")
