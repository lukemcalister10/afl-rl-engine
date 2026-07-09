"""KPF REBALANCE (pre-bake) — one-engine-load board dump with KPF diagnostics.
ONE LOAD PER PROCESS (the engine's module-rebind pattern — cp._lvl_eff_orig capture at :72 —
makes a second in-process exec recurse; run_matrix.sh's one-load rule applies to boards too).
Guard 5 on entry. Usage: board_dump.py <out.json> [ENV=VAL ...]"""
import io, contextlib, json, os, sys
import numpy as np
HERE = '/home/user/afl-rl-engine'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('board_dump', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json')
out = sys.argv[1]
for kv in sys.argv[2:]:
    k, v = kv.split('=', 1); os.environ[k] = v
os.chdir('/home/claude/rl_workspace/rl_after')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; cp = g['cp']
rows = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if not p.get('key') or p.get('_retired'):
            continue
        try:
            v = g['ev'](p, 2026)
        except Exception:
            continue
        pos = MA.gfut(p); nq = g['_nqual'](p, 2026); a = cp._age_asof(p, 2026)
        Lc = g['_lvlcurr'](p, 2026) if nq > 0 else 0.0
        m = Lc - MA.REPL.get(pos, 0.0)
        rows[p['key']] = {'v': v, 'pos': pos, 'pick': p.get('pick'), 'nq': nq,
                          'age': round(a, 1) if a is not None else None,
                          'Lc': round(Lc, 1), 'm': round(m, 1), 'type': p.get('type')}
json.dump({'env': sys.argv[2:], 'rows': rows}, open(out, 'w'))
print(f'{out}: {len(rows)} rows')
