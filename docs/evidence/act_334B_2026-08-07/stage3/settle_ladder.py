"""334 stage B / stage 3 STEP 1+2 — the SETTLED LADDER and the NUMERAIRE.

  base_ef(p)          = the era-free BASE re-taught by base_reteach.py (harness currency == ladder
                        currency; identity mapping, see the memo)
  f(p)                = the stage-2 era-free per-pick re-anchor, read from the committed evidence table
  g                   = f(1) = the re-anchor's drift AT THE NUMERAIRE ANCHOR
  ladder(p)           = round( base_ef(p) * f(p) / g )      -> ladder(1) == 3000 exactly
  numeraire block     : published_pin 3000 UNCHANGED
                        pooled_head_pre_scale H_new = H_old * g
                        s_new = s_old / g = 3000 / H_new    (E6 coherence exact by construction)

The single global factor 1/g is the exporter's own instruction, verbatim from the NUMERAIRE HALT:
"re-base the CURRENCY to the anchor (L7 / the scale drift), never the anchor to the drift."
Applying it to BOTH sides (ladder and the numeraire block's s) is the E6 two-sided law in
rl_model._load_numeraire.  ZERO engine change.
"""
import os, json, hashlib, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/claude/seamcheck_landing'
EV = os.path.join(REPO, 'docs/evidence/act_334B_2026-08-07')

BASE = json.load(open(os.path.join(HERE, 'base_reteach.json')))
base_ef = BASE['D_338_336layer_free']['ladder']
assert len(base_ef) == 64 and base_ef[0] == 3000

RA = json.load(open(os.path.join(EV, 'stage2_erafree/per_pick_reanchor.json')))
rows = {int(r['pick']): r for r in RA['rows']}
f = [float(rows[p]['f']) for p in range(1, 65)]
g = f[0]
print('f(1) = g = %.12f   f(64) = %.12f   f max/min = %.6f' % (g, f[63], max(f) / min(f)))

exact = [base_ef[i] * f[i] / g for i in range(64)]
lad = [int(round(x)) for x in exact]
print('exact head %.9f -> %d   exact tail %.6f -> %d' % (exact[0], lad[0], exact[63], lad[63]))
assert lad[0] == 3000, lad[0]

# ---- monotone non-increasing on the EXACT product ----
viol_exact = [p for p in range(2, 65) if exact[p - 1] > exact[p - 2] + 1e-12]
print('monotone non-increasing on the EXACT product: %s'
      % ('PASS (no isotonic projection needed)' if not viol_exact else 'VIOLATIONS at %s' % viol_exact))

# ---- strict integer descent, minimal integer repairs, each reported ----
repairs = []
for i in range(1, 64):
    if lad[i] >= lad[i - 1]:
        new = lad[i - 1] - 1
        repairs.append((i + 1, lad[i], new, exact[i]))
        lad[i] = new
print('strict integer descent repairs: %d' % len(repairs))
for pk, old, new, ex in repairs:
    print('   pick %2d  rounded %d -> %d  (exact product %.6f; collision with pick %d)'
          % (pk, old, new, ex, pk - 1))
assert all(lad[i] < lad[i - 1] for i in range(1, 64)), 'strict descent still violated'
assert lad[0] == 3000

payload = hashlib.md5(json.dumps({str(i + 1): lad[i] for i in range(64)}, sort_keys=True).encode()).hexdigest()
print('SETTLED LADDER payload md5 %s   total %d' % (payload, sum(lad)))
print('ladder[1,2,3,10,20,40,64] = %s' % [lad[k - 1] for k in (1, 2, 3, 10, 20, 40, 64)])

# ---- the numeraire arithmetic ----
CUR = json.load(open(os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')))
H_old = float(CUR['numeraire']['pooled_head_pre_scale']); s_old = float(CUR['numeraire']['s'])
pin = float(CUR['numeraire']['published_pin'])
H_new = H_old * g
s_new = pin / H_new
print()
print('NUMERAIRE  published_pin %.1f (UNCHANGED)' % pin)
print('  pooled_head_pre_scale  %.4f  ->  %.10f   (x g)' % (H_old, H_new))
print('  s                      %.16f -> %.16f   (/ g)' % (s_old, s_new))
print('  coherence  pin/H_new - s_new = %.3e   (must be <= 1e-9)' % abs(pin / H_new - s_new))
print('  s_new / s_old = %.12f = 1/g = %.12f' % (s_new / s_old, 1.0 / g))

# ---- the per-pick candidate table ----
SH = BASE['_shipped']['ladder']
print()
print('%4s %8s %8s %10s %10s %8s %8s' % ('pick', 'shipped', 'base_ef', 'f', 'exact', 'settled', 'vs_ship'))
for p in range(1, 65):
    print('%4d %8d %8d %10.6f %10.3f %8d %8d'
          % (p, SH[p - 1], base_ef[p - 1], f[p - 1], exact[p - 1], lad[p - 1], lad[p - 1] - SH[p - 1]))

json.dump({'base_ef': base_ef, 'f': f, 'g': g, 'exact': exact, 'ladder': lad,
           'payload': payload, 'total': int(sum(lad)), 'repairs': repairs,
           'numeraire': {'published_pin': pin, 'H_old': H_old, 'H_new': H_new,
                         's_old': s_old, 's_new': s_new},
           'monotone_exact_violations': viol_exact},
          open(os.path.join(HERE, 'settled_ladder.json'), 'w'), indent=1, sort_keys=True)
print('\nwrote settled_ladder.json')
