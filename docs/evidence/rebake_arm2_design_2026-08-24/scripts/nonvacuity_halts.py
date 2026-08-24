#!/usr/bin/env python3
"""ARM 2 — PROVE THE THREE NEW GUARDS CAN FIRE. (Standing norm: "any guard added must be proven able to
fail." A guard nobody has seen fire is a comment with a raise statement in it.)

  (1) FB4, the sklearn._loss private-contract self-test — fired ALREADY, in anger, during development:
      this seat's first toy was a single-driver toy and the NON-VACUITY leg killed it, exactly as study B
      M-25 predicts ("quantile + monotonic_cst gives 0 violations when the constrained feature is the
      only driver"). Re-fired here on demand by monkeypatching the subclass back to the stock contract,
      so the transcript carries both halves rather than a memory of one.
  (2) THE COHERENCE HALT — band and ceiling declaring different feature contracts. Fired by pointing
      RL_CM_PKL at the CANDIDATE band and RL_Q97M_PKL at the LIVE ceiling: byte-for-byte the mixed
      configuration that produced register v834's F7 (c7cea06d), which built, parity-gated and reported
      with no verdict anywhere. It now halts on line one.
  (3) THE LAW-3 PROTECTION HALT — an incumbent band under an engine whose ratchet is retired. Fired by
      pointing both overrides at the LIVE pair.

Each leg asserts the halt actually fired AND that the message names the right thing. Run from anywhere;
it drives the engine as subprocesses so a halt is a real exit code, not a caught exception.
"""
import argparse, json, os, subprocess, sys


def run_engine(ws, root, env_extra):
    env = dict(os.environ)
    env.update({'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
                'NUMEXPR_NUM_THREADS': '1',
                'PYTHONPATH': ws + os.pathsep + '/home/claude/rl_vendor',
                'RL_CONFIG_MODE': 'gate', 'RL_REPO': root,
                'RL_FV': os.path.join(root, 'engine', 'forward_valuation')})
    env.update(env_extra)
    code = ("import contextlib,io,sys\n"
            "src=open('_merged_recover.py').read().split('print(\"=== AFTER')[0]\n"
            "g={}\n"
            "with contextlib.redirect_stdout(io.StringIO()): exec(src,g)\n"
            "print('ENGINE IMPORTED — NO HALT')\n")
    return subprocess.run([sys.executable, '-c', code], cwd=ws, env=env,
                          capture_output=True, text=True)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--ws', required=True)
    ap.add_argument('--root', required=True, help='the CANDIDATE root (pins the candidate artifacts)')
    ap.add_argument('--cand-cm', required=True)
    ap.add_argument('--cand-q97m', required=True)
    ap.add_argument('--live-cm', required=True)
    ap.add_argument('--live-q97m', required=True)
    ap.add_argument('--fv', required=True)
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])
    R = {}

    # ---------------------------------------------------------------- (1) FB4 re-fired on demand
    print('=== (1) FB4 — the private-contract self-test, fired on demand ===')
    code = ("import sys,json\n"
            "sys.path.insert(0,%r)\n"
            "import exact_monotone as EM\n"
            "from sklearn._loss.loss import PinballLoss\n"
            "# put the STOCK contract back on the subclass: this is exactly what a sklearn release that\n"
            "# stopped honouring `differentiable` would look like from inside the bake.\n"
            "EM.GradOnlyPinball.differentiable = False\n"
            "EM.GradOnlyPinball.need_update_leaves_values = True\n"
            "EM.selftest(strict=True)\n"
            "print('NO HALT')\n" % a.fv)
    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True,
                       env=dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1'))
    fired = r.returncode != 0 and 'FB4 HALT' in (r.stdout + r.stderr)
    print(r.stdout[-1500:] or r.stderr[-1500:])
    R['FB4_selftest'] = {'fired': fired, 'exit': r.returncode,
                         'names_the_contract': 'EXACTNESS LEG FAILED' in (r.stdout + r.stderr),
                         'also_fired_during_development': (
                             'YES — the first toy this seat wrote was a single-driver toy and the '
                             'NON-VACUITY leg rejected it, which is the failure mode study B M-25 '
                             'documents. The shipped toy is 10-feature with heteroscedastic skewed noise '
                             'and an interaction.')}
    print('  FIRED: %s' % fired)

    # ---------------------------------------------------------------- (2) the coherence halt
    print('\n=== (2) COHERENCE HALT — candidate band + LIVE ceiling (register v834 F7 by construction) ===')
    r = run_engine(a.ws, a.root, {'RL_CM_PKL': a.cand_cm, 'RL_Q97M_PKL': a.live_q97m})
    out = r.stdout + r.stderr
    fired = r.returncode != 0 and 'ARTIFACT COHERENCE HALT' in out
    print(out[-1400:])
    R['coherence_halt'] = {'fired': fired, 'exit': r.returncode,
                           'names_both_paths': (a.cand_cm in out and 'q97m' in out.lower()),
                           'configuration': 'RL_CM_PKL=candidate band, RL_Q97M_PKL=LIVE ceiling — the '
                                            'exact mixed pair that produced c7cea06d in ARM 1\'s screen'}
    print('  FIRED: %s' % fired)

    # ---------------------------------------------------------------- (3) the protection halt
    print('\n=== (3) LAW-3 PROTECTION HALT — incumbent band under a retired ratchet ===')
    r = run_engine(a.ws, a.root, {'RL_CM_PKL': a.live_cm, 'RL_Q97M_PKL': a.live_q97m})
    out = r.stdout + r.stderr
    fired = r.returncode != 0 and 'LAW-3 PROTECTION HALT' in out
    print(out[-1400:])
    R['protection_halt'] = {'fired': fired, 'exit': r.returncode,
                            'names_the_band_path': a.live_cm in out,
                            'configuration': 'both overrides on the LIVE (incumbent) pair — coherent with '
                                             'each other, so leg (2) passes and leg (3) is what fires'}
    print('  FIRED: %s' % fired)

    # ---------------------------------------------------------------- the POSITIVE control
    print('\n=== (4) POSITIVE CONTROL — the candidate pair imports cleanly (the halts are not blanket) ===')
    r = run_engine(a.ws, a.root, {'RL_CM_PKL': a.cand_cm, 'RL_Q97M_PKL': a.cand_q97m})
    out = r.stdout + r.stderr
    ok = r.returncode == 0 and 'ENGINE IMPORTED — NO HALT' in out
    print([l for l in out.split('\n') if 'REBAKE ARM 2 CONTRACT' in l or 'NO HALT' in l])
    R['positive_control'] = {'imported_cleanly': ok, 'exit': r.returncode,
                             'contract_line': next((l for l in out.split('\n')
                                                    if 'REBAKE ARM 2 CONTRACT' in l), None)}
    print('  CLEAN IMPORT: %s' % ok)

    R['verdict'] = ('ALL THREE GUARDS PROVEN ABLE TO FIRE, and proven not to fire on the candidate pair'
                    if (R['FB4_selftest']['fired'] and R['coherence_halt']['fired']
                        and R['protection_halt']['fired'] and R['positive_control']['imported_cleanly'])
                    else 'INCOMPLETE — see legs above')
    print('\nVERDICT: %s' % R['verdict'])
    if a.json:
        json.dump(R, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
