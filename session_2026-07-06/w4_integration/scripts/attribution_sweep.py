"""W4 per-lever attribution: leave-one-out board sweeps (engine evaluations run SEQUENTIALLY — process rule #4).
Each config exec-loads the engine fresh in a subprocess and dumps ev() for every baked-board player.
Output: out/attr_<tag>.json per config + a merged attribution table."""
import subprocess, sys, os, json

WS = '/home/claude/rl_workspace/rl_after'
OUT = '/home/user/afl-rl-engine/session_2026-07-06/w4_integration/out'
ENV_BASE = dict(os.environ, PYTHONHASHSEED='0', RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25',
                RL_RECENCY_DECAY='0.72', RL_PRIOR_TREES='400', PAR_RAMPS='22',
                PYTHONPATH='/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor')

CONFIGS = [
    ('full', {}),
    ('no_ruc', {'RL_W4_RUC': '0'}),
    ('no_aging', {'RL_FORMDECL': '0'}),
    ('no_v7form', {'RL_V7FORM': '0'}),
    ('no_kpf', {'RL_KPFFIX': '0'}),
    ('no_fwdrecal', {'RL_FWDRECAL': '0'}),
    ('no_young', {'RL_YOUNG': '0'}),
    ('no_ovpx', {'RL_OVPX': '0'}),
]

SWEEP = r'''
import io, contextlib, json, sys
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']
baked = {r['key']: r['v'] for r in json.load(open('/home/claude/rl_build/rl_app_data.json'))['active']}
out = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        k = p.get('key')
        if k not in baked or p.get('_retired'):
            continue
        try:
            out[k] = float(ev(p, 2026))
        except Exception:
            out[k] = None
json.dump(out, open(sys.argv[1], 'w'))
print('done', len(out))
'''

for tag, envd in CONFIGS:
    dst = f'{OUT}/attr_{tag}.json'
    if os.path.exists(dst):
        print(f'{tag}: exists, skip'); continue
    env = dict(ENV_BASE); env.update(envd)
    r = subprocess.run([sys.executable, '-c', SWEEP, dst], cwd=WS, env=env,
                       capture_output=True, text=True, timeout=1800)
    print(tag, '->', r.stdout.strip().splitlines()[-1] if r.stdout.strip() else f'FAIL rc={r.returncode}: {r.stderr[-300:]}')
print('sweeps complete')
