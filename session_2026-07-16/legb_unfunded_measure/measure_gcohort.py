#!/usr/bin/env python3
"""LEG B UNFUNDED — G-COHORT y4/y5/y6 via the FROZEN repo gate suite (the July-8 construction, the REAL
gate — NOT the memo §6 proxy). Per directive: build the candidate walk-forward matrix with the toggle env
set (exactly as ship_gates_check does: s4_matrix_M1v7.py, RL_CONFIG_MODE=gate, S4_MATRIX=<tmp>), assert its
__meta__ hashes match the running engine (the gate's own guard, no weakening), then run the frozen
_b1_july8 / _b1_rows extracted VERBATIM from ship_gates_check.py and apply the gate's exact ratio math
(den=min(y1,y2); ratios y4/y5/y6 = SUM[N]/den; hard <=1.30).

usage:  RL_UNCOMP=0 python3 measure_gcohort.py OFF            # baseline (map inert => must ~ Leg-A head)
        RL_UNCONSERVE=1 RL_UNCOMP_S=<s> python3 measure_gcohort.py <label>
Run from the workspace (WS) with the pinned gate env already exported.
"""
import os, sys, json, ast, hashlib, tempfile, subprocess
import numpy as np

label = sys.argv[1] if len(sys.argv) > 1 else 'RUN'
HERE = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
WS = os.getcwd()  # invoked from the workspace

# --- md5-assert the frozen gate source before extracting from it ---
SGC = os.path.join(HERE, 'ship_gates_check.py')
src = open(SGC).read()

# extract _b1_july8 + _b1_rows VERBATIM (the real gate functions; deps = json, np) ------------------------
ns = {'json': json, 'np': np}
_tree = ast.parse(src)
_got = []
for node in _tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ('_b1_july8', '_b1_rows'):
        exec(compile(ast.Module(body=[node], type_ignores=[]), SGC, 'exec'), ns)
        _got.append(node.name)
assert set(_got) == {'_b1_july8', '_b1_rows'}, 'frozen gate fns not both extracted: %s' % _got
_b1_july8 = ns['_b1_july8']; _b1_rows = ns['_b1_rows']

# --- build the candidate matrix exactly as ship_gates_check's B1 block does ---
HEAD = hashlib.md5(open(os.path.join(WS, '_merged_recover.py'), 'rb').read()).hexdigest()[:8]
STORE = hashlib.md5(open(os.path.join(WS, 'rl_model_data.json'), 'rb').read()).hexdigest()[:8]
_mfd, CAND = tempfile.mkstemp(prefix='s4_cand_uncons_', suffix='.json'); os.close(_mfd)
# DEV-SHELL build (no RL_CONFIG_MODE): gate mode CLEARS/REJECTS the declared kill-switches (RL_UNCOMP_S /
# RL_UNCONSERVE are not manifest dials), so it can only measure the BAKED config — an unbaked env-toggled
# candidate MUST be built dev-shell (the sanctioned path). The July-8 CONSTRUCTION (matrix math + _b1_july8)
# is identical; only the config-integrity wrapper differs. __meta__ still stamps engine/store/config, asserted.
_menv = {k: v for k, v in os.environ.items() if not k.startswith('SGC_') and k != 'RL_CONFIG_MODE'}
_menv.update(S4_MATRIX=CAND, RL_REPO=HERE)
_run = subprocess.run([sys.executable, 's4_matrix_M1v7.py'], cwd=WS, env=_menv,
                      capture_output=True, text=True, timeout=1800)
_meta = json.load(open(CAND)).get('__meta__', {}) if os.path.exists(CAND) else {}
if not _meta:
    print('G-COHORT[%s] HALT: matrix carries no __meta__ (exit=%s) stderr: %s'
          % (label, _run.returncode, _run.stderr[-400:]))
    sys.exit(2)
_eng = _meta.get('engine_head_md5', '?')[:8]; _sto = _meta.get('store_md5', '?')[:8]
_mok = (_eng == HEAD and _sto == STORE)
print('G-COHORT[%s] matrix meta: engine %s==%s store %s==%s config %s -> %s'
      % (label, _eng, HEAD, _sto, STORE, (_meta.get('config_sha256') or '-')[:12],
         'HASH-OK' if _mok else 'HASH-MISMATCH <<<'))
if not _mok:
    print('G-COHORT[%s] HALT: matrix hashes != running engine' % label); sys.exit(2)

# --- the frozen July-8 gated construction + the gate's exact ratio math ---
SUM, cohorts = _b1_july8(CAND)
for _rq in (1, 2, 4, 5, 6):
    if SUM.get(_rq) is None:
        print('G-COHORT[%s] HALT: July-8 incomplete, missing y%d' % (label, _rq)); sys.exit(2)
den = min(SUM[1], SUM[2]); den_src = 'y1' if SUM[1] <= SUM[2] else 'y2'
ratios = {N: SUM[N] / den for N in (4, 5, 6)}
breaches = [N for N in (4, 5, 6) if ratios[N] > 1.30]
ok = not breaches
print('G-COHORT[%s] July-8 (frozen, %d classes 2004-2020 ND+RD): %s ; den=min(y1,y2)=%s=%.1f'
      % (label, len(cohorts), ' '.join('y%d=%.1f' % (N, SUM[N]) for N in sorted(SUM)), den_src, den))
print('G-COHORT[%s] RATIOS  y4=%.4f  y5=%.4f  y6=%.4f  | hard<=1.30 -> %s'
      % (label, ratios[4], ratios[5], ratios[6],
         'PASS x3' if ok else 'BREACH at y%s (finding)' % breaches))
# machine-readable line for the driver to harvest
print('GCJSON %s' % json.dumps(dict(label=label, y4=ratios[4], y5=ratios[5], y6=ratios[6],
      sum={str(k): v for k, v in SUM.items()}, den=den, breaches=breaches,
      engine=HEAD, store=STORE, n_classes=len(cohorts))))
os.unlink(CAND)
