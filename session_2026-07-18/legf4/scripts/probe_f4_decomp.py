#!/usr/bin/env python3
# LEG F4 — DIAGNOSIS (READ-ONLY): decompose the mid/veteran (phi=0) forward-vs-backward asymmetry.
# Replicates rl_export's exact lens construction (v=ev(2026,None); vP1: _LENS_FORM=2026,ev(2027);
# vM1: _LENS_FORM=None,ev(2025)) then attributes the forward decline to mechanisms via in-memory
# neutralization (each restored). No board write, no file edit persisted.
import os, io, contextlib
from collections import defaultdict
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']; effpk = G['effpk']; GRP = G['GRP']
rl = MA  # rl_model module namespace (MA is rl_model imported into _merged_recover)

def lens_vals(pfilter=None):
    """Compute v, vP1, vM1 per player exactly as rl_export does."""
    out = []
    for p in players:
        if pfilter and not pfilter(p): continue
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
        v = ev(p, 2026)
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
        vM1 = ev(p, 2025)                       # backward: no form anchor (_LENS_FORM None)
        MA._LENS_FORM = 2026                      # forward: form-anchored (RL_LEGE default on)
        vP1 = ev(p, 2027)
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
        a = age(p)
        out.append(dict(key=p.get('key'), age=a, v=v, vP1=vP1, vM1=vM1,
                        coh=('developing' if (a or 99) <= 23 else 'mid' if a <= 27 else 'veteran')))
    return out

def report(rows, label):
    coh = defaultdict(lambda: [0, 0.0, 0.0, 0.0])
    for r in rows:
        c = coh[r['coh']]; c[0] += 1; c[1] += r['v'] or 0; c[2] += r['vP1'] or 0; c[3] += r['vM1'] or 0
    print("--- %s ---" % label)
    print("  %-11s %4s %9s %8s %8s   %8s" % ('cohort', 'n', 'now', 'fwd%', 'back%', 'fwd/back'))
    for c in ('developing', 'mid', 'veteran'):
        n, now, fwd, bak = coh[c]
        if not now: continue
        f = 100 * (fwd - now) / now; b = 100 * (now - bak) / bak
        print("  %-11s %4d %9.0f %+7.1f%% %+7.1f%%   %5.2fx" % (c, n, now, f, b, (f / b if b else 0)))
    # mid+vet combined
    mv = [0.0, 0.0, 0.0]
    for c in ('mid', 'veteran'):
        mv[0] += coh[c][1]; mv[1] += coh[c][2]; mv[2] += coh[c][3]
    f = 100 * (mv[1] - mv[0]) / mv[0]; b = 100 * (mv[0] - mv[2]) / mv[2]
    print("  %-11s      %9.0f %+7.1f%% %+7.1f%%   %5.2fx" % ('MID+VET', mv[0], f, b, (f / b if b else 0)))
    return f, b

print("=== BASELINE (F3 fixed board, RL_LEGF=1 RL_LEGE=1) ===")
base = lens_vals()
report(base, "baseline")

# --- MECH 1: neutralize _dev_advance (the forward age-curve level roll). Force identity so level_now==level_demo.
print("\n=== MECH 1: _dev_advance -> identity (no forward level roll) ===")
_orig_da = rl._dev_advance
rl._dev_advance = lambda L, p: L
MA._pe_clear()
m1 = lens_vals()
f1, b1 = report(m1, "dev_advance OFF")
rl._dev_advance = _orig_da
MA._pe_clear()

# --- MECH 2: neutralize the multi-year horizon DELTAS decline (frac flat past peak) on the FORWARD stream only.
#     frac(a,pa) returns DELTAS[a-pa]; flatten to <=1.0 cap at 1.0 for a>pa would change base board too, so
#     instead measure by pinning DELTAS decline to the k=0 value inside the forward projection is hard; skip —
#     dev_advance + horizon are entangled through cur. MECH1 already captures the level-roll; report note only.

# --- MECH 3: availability layers (RL_AVAIL present haircut / expgate). Measure via _avail_hc contribution.
print("\n=== MECH 3: availability (_avail_hc / RL_AVAIL present haircut) present-year share ===")
nhc = sum(1 for p in players if (p.get('_avail_hc', 0) or 0) > 0)
print("  players with _avail_hc>0: %d ; but present haircut applies at k==0 (BASE_REF==AGE_REF==2026) only —")
print("  forward vP1 has AGE_REF=2027 so the k==0 present-haircut branch is INERT forward (see _proj_w4:830).")

print("\n[baseline fwd/back and dev_advance-off fwd/back tell the level-roll share of the asymmetry]")
