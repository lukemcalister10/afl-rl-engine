"""Shared engine loader (READ-ONLY). Single exec-load per process (START_HERE §2).

GATE MODE: config_manifest.enforce('gate') clears ambient model env and loads
data/model_config.json -- this is what the shipped board/book gate runs do
(docs/evidence/g1_never_rises_2026-08-10/gate_run.sh: RL_CONFIG_MODE=gate).
Notably it sets RL_GAMMA=1.0 (the manifest value), NOT the 0.85 in START_HERE §2.
"""
import io, contextlib, os, sys
ROOT = '/home/user/afl-rl-engine'
RA = os.path.join(ROOT, 'engine', 'rl_after')
os.environ.setdefault('PYTHONHASHSEED', '0')
os.environ['RL_REPO'] = ROOT
os.environ['RL_FV'] = os.path.join(ROOT, 'engine', 'forward_valuation')
os.environ['RL_CONFIG_MODE'] = 'gate'
for p in (RA, os.path.join(ROOT, 'engine', 'forward_valuation'),
          os.path.join(ROOT, 'vendor'), ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)
import config_manifest as _CFG
_CFG.enforce('gate')


def load():
    cwd = os.getcwd()
    os.chdir(RA)
    try:
        g = {}
        src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, '_merged_recover.py', 'exec'), g)
        return g
    finally:
        os.chdir(cwd)
