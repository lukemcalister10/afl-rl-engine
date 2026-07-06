"""W4 pool probe: full active-board sweep vs baked — net pool delta, split by cohort (redistribution audit)."""
import io, contextlib, os, json
import numpy as np

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; cp = g['cp']; _nqual = g['_nqual']

baked = {r['key']: r['v'] for r in json.load(open('/home/claude/rl_build/rl_app_data.json'))['active']}
rows = []
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        k = p.get('key')
        if k not in baked or p.get('_retired'):
            continue
        try:
            v = float(ev(p, 2026))
        except Exception:
            continue
        a = cp._age_asof(p, 2026); n = _nqual(p, 2026)
        rows.append((p['player'], MA.gfut(p), a, n, baked[k], v))
tot0 = sum(r[4] for r in rows); tot1 = sum(r[5] for r in rows)
print(f"board pool ({len(rows)} matched): baked {tot0:,.0f} -> candidate {tot1:,.0f}  net {100*(tot1/tot0-1):+.2f}%")
def bucket(lab, sel):
    s = [r for r in rows if sel(r)]
    if not s: return
    b = sum(r[4] for r in s); c = sum(r[5] for r in s)
    print(f"  {lab:34s} n={len(s):4d}  {b:9,.0f} -> {c:9,.0f}  {100*(c/b-1):+.2f}%")
bucket('proven (nq>=4) age>=30', lambda r: r[3] >= 4 and r[2] >= 30)
bucket('proven (nq>=4) age 25-29', lambda r: r[3] >= 4 and 25 <= r[2] < 30)
bucket('proven (nq>=4) age <25', lambda r: r[3] >= 4 and r[2] < 25)
bucket('thin (nq<4) age <=22', lambda r: r[3] < 4 and r[2] <= 22)
bucket('thin (nq<4) age >22', lambda r: r[3] < 4 and r[2] > 22)
bucket('RUC (all)', lambda r: r[1] == 'RUC')
bucket('KEY_FWD (all)', lambda r: r[1] == 'KEY_FWD')
bucket('GEN_FWD (all)', lambda r: r[1] == 'GEN_FWD')
# biggest movers each way
rows.sort(key=lambda r: r[5] - r[4])
print("\nTOP -12 (funding):")
for r in rows[:12]: print(f"  {r[0][:24]:24s}{r[1]:8s} a{r[2]:.0f} nq{r[3]} {r[4]:6.0f} -> {r[5]:6.0f}  ({r[5]-r[4]:+.0f})")
print("TOP +12 (credited):")
for r in rows[-12:][::-1]: print(f"  {r[0][:24]:24s}{r[1]:8s} a{r[2]:.0f} nq{r[3]} {r[4]:6.0f} -> {r[5]:6.0f}  ({r[5]-r[4]:+.0f})")
nm = sum(1 for r in rows if abs(r[5]-r[4]) < 0.5)
print(f"\nnon-movers: {nm}/{len(rows)}")
json.dump([{'player':r[0],'pos':r[1],'age':r[2],'nq':r[3],'baked':r[4],'now':r[5]} for r in rows],
          open(os.environ.get('POOL_OUT','/tmp/pool_probe.json'),'w'))
