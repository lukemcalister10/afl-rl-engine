"""ORDER 20 — THE POOL PERTURBATION MUTATOR.

Run as:  python3 perturb_pool.py <TREEDIR>          (env RL_O20_PERTURB names the perturbation)

Rewrites `engine/rl_after/pvc_curve_v2.json`'s `pool_levels` block IN THE STAGED TREE ONLY. The pool
levels are THE pool price primitive: `rl_model.pool_level()` reads this block verbatim (rl_model.py:
1419-1425) and it is the only owner-signed input that sets what a pool entrant is worth. Perturbing
it is therefore the sharpest possible statement of "a pool price changed, and nothing else did".

The national side of the artifact — `curve` (the 1-64 pick curve), `pool_value`, `pin`, `numeraire` —
is NOT touched by any perturbation, with ONE declared exception noted at ND65PLUS below.

Perturbations (RL_O20_PERTURB):
  x1.5        every signed pool level x 1.5     (a large, uniform lift)
  x0.5        every signed pool level x 0.5     (a large, uniform cut)
  x3.0        every signed pool level x 3.0     (an absurd lift — the law says zero at ANY size)
  tilt        RD:* x 2.0, everything else x 0.6 (a RESHAPE that changes the pool's internal mix)
  rd_only     RD:* x 2.5, every other division untouched (one division moves, alone)
  flat100     every signed pool level := 100    (destroys the level structure entirely)
"""
import json, os, sys, pathlib

TREE = sys.argv[1]
NAME = os.environ.get('RL_O20_PERTURB', 'x1.5')

f = pathlib.Path(TREE) / 'engine/rl_after/pvc_curve_v2.json'
J = json.loads(f.read_text())
PL = J['pool_levels']

before = {'signed_flat': dict(PL['signed_flat']),
          'signed_rd_positional': dict(PL['signed_rd_positional']),
          'measured_k15': PL['signed_nd65_plus']['measured_k15']}


def scale_flat(fn):
    for k in PL['signed_flat']:
        PL['signed_flat'][k] = fn(float(PL['signed_flat'][k]))


def scale_rd(fn):
    for k in PL['signed_rd_positional']:
        PL['signed_rd_positional'][k] = fn(float(PL['signed_rd_positional'][k]))


def scale_nd65(fn):
    # ND65+ is `min(measured_k15, curve[cap_pick])` (rl_model.py:1423-1424). Scaling measured_k15 UP
    # would be absorbed by the min() against the NATIONAL curve and the perturbation would silently
    # not happen; scaling it DOWN moves it. Both directions are applied here and the resolved level is
    # printed, so a perturbation that the min() ate is VISIBLE rather than a false pass.
    PL['signed_nd65_plus']['measured_k15'] = fn(float(PL['signed_nd65_plus']['measured_k15']))


if NAME == 'x1.5':
    scale_flat(lambda v: v * 1.5); scale_rd(lambda v: v * 1.5); scale_nd65(lambda v: v * 1.5)
elif NAME == 'x0.5':
    scale_flat(lambda v: v * 0.5); scale_rd(lambda v: v * 0.5); scale_nd65(lambda v: v * 0.5)
elif NAME == 'x3.0':
    scale_flat(lambda v: v * 3.0); scale_rd(lambda v: v * 3.0); scale_nd65(lambda v: v * 3.0)
elif NAME == 'tilt':
    scale_flat(lambda v: v * 0.6); scale_rd(lambda v: v * 2.0); scale_nd65(lambda v: v * 0.6)
elif NAME == 'rd_only':
    scale_rd(lambda v: v * 2.5)
elif NAME == 'flat100':
    scale_flat(lambda v: 100.0); scale_rd(lambda v: 100.0); scale_nd65(lambda v: 100.0)
elif NAME == 'none':
    pass
else:
    raise SystemExit('unknown perturbation %r' % NAME)

f.write_text(json.dumps(J, indent=1) + "\n")
print('  PERTURB %s: signed_flat %s -> %s' % (
    NAME,
    {k: int(float(v)) for k, v in list(before['signed_flat'].items())[:4]},
    {k: int(float(v)) for k, v in list(PL['signed_flat'].items())[:4]}))
print('           signed_rd_positional %s -> %s' % (
    {k: int(float(v)) for k, v in list(before['signed_rd_positional'].items())[:3]},
    {k: int(float(v)) for k, v in list(PL['signed_rd_positional'].items())[:3]}))
print('           nd65 measured_k15 %s -> %s' % (before['measured_k15'],
                                                 PL['signed_nd65_plus']['measured_k15']))
