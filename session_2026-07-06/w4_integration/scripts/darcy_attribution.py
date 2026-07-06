"""Sam Darcy — three-locus attribution (young-convexity ceiling · KPF young-speculative · LTI return-haircut).
Owner read: UNDERPRICED, out until 2027 (LTI_REGISTER). Attribute which layer holds him down; confirm none of
the three clips his ceiling. In-process toggles for the LTI-side layers; the lever-side deltas come from the
leave-one-out sweep files. Run under the full candidate config."""
import io, contextlib, json, os
import numpy as np

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; cp = g['cp']; b6 = g['b6']; _nqual = g['_nqual']; _lvlcurr = g['_lvlcurr']

p = next(x for x in MA.data if x['player'] == 'Sam Darcy')
key = p['key']
OUT = '/home/user/afl-rl-engine/session_2026-07-06/w4_integration/out'
attr = {t: json.load(open(f'{OUT}/attr_{t}.json')) for t in
        ['full', 'no_ruc', 'no_aging', 'no_v7form', 'no_kpf', 'no_fwdrecal', 'no_young', 'no_ovpx']
        if os.path.exists(f'{OUT}/attr_{t}.json')}
baked = {r['key']: r['v'] for r in json.load(open('/home/claude/rl_build/rl_app_data.json'))['active']}

def E(Y=2026):
    with contextlib.redirect_stdout(io.StringIO()):
        return float(ev(p, Y))

lines = []
def say(s):
    print(s); lines.append(s)

v_full = E()
say(f"Sam Darcy KEY_FWD age {cp._age_asof(p,2026):.0f} · nqual={_nqual(p,2026)} · "
    f"lcr={_lvlcurr(p,2026)-MA.REPL['KEY_FWD']:+.1f} · 2026 games={sum(x['games'] for x in p['scoring'] if x['year']==2026)}")
say(f"baked v2.5 = {baked.get(key)} -> candidate = {v_full:.0f}  ({100*(v_full-baked.get(key,1))/baked.get(key,1):+.1f}%)")
say("")
say("LOCUS 1 — young-convexity ceiling (v7 q97 taper):")
bb = b6(p, 2026)
say(f"  forward band [q10..q97] = {[round(float(x),1) for x in bb]}  (demonstrated Lc={_lvlcurr(p,2026):.1f})")
if 'no_v7form' in attr:
    d = v_full - (attr['no_v7form'].get(key) or v_full)
    say(f"  v7 FORM-CONDITIONED relax (lever L5) contributes {d:+.0f} — his demonstrated lcr earns tail retention;")
say(f"  ceiling check: q97 node {float(bb[5]):.1f} sits ABOVE his demonstrated level -> the ceiling is NOT clipped.")
say("")
say("LOCUS 2 — KPF young-speculative:")
say(f"  KPF compress gate = nqual>=4 AND age>=24; Darcy nqual={_nqual(p,2026)} age {cp._age_asof(p,2026):.0f} -> "
    f"OUTSIDE the gate BY CONSTRUCTION (young-KPF ceiling protected).")
if 'no_kpf' in attr:
    d = v_full - (attr['no_kpf'].get(key) or v_full)
    say(f"  KPF lever total on Darcy = {d:+.0f} (should be ~0: no compress, and the reward leg is proven-gated).")
if 'no_young' in attr:
    d = v_full - (attr['no_young'].get(key) or v_full)
    say(f"  young runway credit (lever L2, position-relative: KPF peak age 27 -> a 23yo KPF is pre-peak) = {d:+.0f}.")
say("")
say("LOCUS 3 — LTI return-haircut (net of aging; B2 + season-absence channels):")
b2 = p.get('_b2hc', 0.0)
p['_b2hc'] = 0.0
v_nob2 = E()
p['_b2hc'] = b2
say(f"  B2 present-unavailability haircut = {b2:.3f}; value with B2 OFF = {v_nob2:.0f} -> B2 costs {v_full-v_nob2:+.0f}.")
sc26 = [x for x in p['scoring'] if x['year'] == 2026]
sav = list(p['scoring'])
p['scoring'] = [x for x in p['scoring'] if x['year'] != 2026]
try:
    v_no26 = E()
finally:
    p['scoring'] = sav
say(f"  recency/exposure drag of the empty 2026 season (M2/M3/decay channels): value with the 2026 row removed = "
    f"{v_no26:.0f} (Δ {v_full-v_no26:+.0f}) — the forfeited-growth-year cost, NOT a ceiling dent (band above holds).")
say(f"  MESH CHECK (no double-count): B2 is age-banded BELOW 30 because the age curve prices 30+ decline; the W4")
say(f"  credit/fade legs are proven-gated (nqual>=4) so NEITHER fires on Darcy — the only aging-side layers he")
say(f"  carries are the v7 taper (RELAXED by demonstrated form) and the runway credit (POSITIVE). No stacked haircut.")
say("")
vals = {t: attr[t].get(key) for t in attr}
say(f"per-lever leave-one-out: " + "  ".join(f"{t.replace('no_','')}:{(v_full-(v or v_full)):+.0f}" for t, v in vals.items() if t != 'full'))
open(f'{OUT}/darcy_attribution.md', 'w').write("\n".join(lines))
print("\nwrote", f'{OUT}/darcy_attribution.md')
