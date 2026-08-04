#!/usr/bin/env python3
"""#306 L-B — THE DETERMINISTIC FIT LANE.  The PASSING direction, earned.

THE ACCEPTANCE (#306 §4 L-B, verbatim)
    "Same-curve double-fit from ANY starting state -> byte-identical surface."
  Fit the same curve from at least three MATERIALLY DIFFERENT starting states -- a fresh state with
  no surface present, the state after fitting one curve, and a state as far from it as the record
  supplies -- in FRESH PROCESSES, and compare FULL md5, never the signature key (N22: the signature
  SELECTS, the md5 GOVERNS; that distinction is exactly how the pass-0/pass-1 surfaces shared a key
  with different bytes).

THE FAILING DIRECTION IS ALREADY DISCHARGED and is NOT re-run here: the recorded cross-container
pair (5939fa35 x5 on the off-class box vs fb9efdec x3 on two fit-class boxes, both 2026-08-04) is
today's lane demonstrably producing different bytes under identical declared inputs. Ruled at N35 §3.

WHY THE NEW LANE SHOULD PASS, STATED BEFORE IT IS RUN so the test can genuinely fail:
  the anchored lens fit reads the basis artifact, the anchor ladder, and the roster's COMPOSITION.
  It never reads the surface it is replacing -- that is the structural difference from the old lane,
  whose refit inherited state from the surface on disk. If any starting state changes the output
  bytes, L-B has NOT been achieved and this HALTs rather than reporting a pass.

Each state runs in a FRESH PROCESS (the engine builds and caches the surface at import).
Read-only with respect to the record: the substrate is restored and round-trip verified by the
caller. This script installs surfaces into the working tree and MUST be run under that discipline.

    python3 lb_determinism.py
"""
import hashlib, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
L6 = os.path.join(REPO, 'docs/evidence/rehearsal_290_2026-07-31/L6_convergence')
SURF = os.path.join(REPO, 'data/v0surf.pkl')
REFIT = os.path.join(REPO, 'session_2026-07-18/legf6/scripts/refit_v0surf.py')

# materially different starting states, in the directive's own terms
STATES = [
    ('no surface present', None),
    ('fb9efdec — pass-0, the state after fitting the ruled curve', os.path.join(L6, 'pass0_surface/v0surf.pkl')),
    ('84fb0cde — the L3-L5 record surface, pre-catch-up', os.path.join(REPO, 'docs/evidence/rehearsal_290_2026-07-31/v0surf_frozen_2026-07-31/v0surf.pkl')),
    ('31e7f00b — the halt surface, fitted at a DIFFERENT curve (ca662051)', os.path.join(L6, 'pass4_surface/v0surf.pkl')),
    ('2d7dab64 — the other cycle limb, as far as the record supplies', os.path.join(L6, 'pass3_surface/v0surf.pkl')),
]


def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def main():
    keep = md5(SURF) if os.path.exists(SURF) else None
    backup = os.path.join(HERE, '.v0surf.keep')
    if keep: shutil.copy2(SURF, backup)
    env = dict(os.environ)
    env['RL_V0SURF_REFIT'] = '1'; env['RL_V0_LENS'] = '1'
    results = []
    try:
        for label, src in STATES:
            if src is None:
                if os.path.exists(SURF): os.remove(SURF)
                start = 'ABSENT'
            else:
                shutil.copy2(src, SURF); start = md5(SURF)[:8]
            p = subprocess.run([sys.executable, REFIT, '--verify'], capture_output=True, text=True,
                               cwd='/home/claude/rl_workspace/rl_after', env=env)
            out = p.stdout + p.stderr
            got = None
            for tok in out.split():
                if len(tok) == 32 and all(c in '0123456789abcdef' for c in tok):
                    got = tok; break
            results.append({'state': label, 'starting_surface': start, 'output_md5': got,
                            'rc': p.returncode, 'note': None if got else out.strip()[-400:]})
            print('  %-62s start %-8s -> %s' % (label[:62], start, got or 'NO OUTPUT (see JSON)'))
    finally:
        if keep: shutil.copy2(backup, SURF); os.remove(backup)
        elif os.path.exists(SURF): os.remove(SURF)

    outs = [r['output_md5'] for r in results if r['output_md5']]
    agree = len(set(outs)) == 1 and len(outs) == len(STATES)
    verdict = {'states_run': len(STATES), 'states_producing_a_surface': len(outs),
               'distinct_outputs': sorted(set(outs)), 'BYTE_IDENTICAL_FROM_EVERY_STATE': agree,
               'L_B_PASSING_DIRECTION': 'PASS' if agree else 'FAIL — HALT'}
    doc = {'what': 'L-B acceptance: same-curve fit from materially different starting states',
           'compared_on': 'FULL md5 of the fitted surface payload (N22), never the signature key',
           'failing_direction': 'already discharged by the recorded cross-container pair (N35 §3); '
                                'deliberately not re-run here',
           'substrate_surface_restored_to': keep, 'results': results, 'verdict': verdict}
    with open(os.path.join(HERE, 'lb_determinism.json'), 'w') as f:
        json.dump(doc, f, indent=1, sort_keys=True); f.write('\n')
    print('\n  distinct outputs: %s' % (verdict['distinct_outputs'] or 'none'))
    print('  L-B PASSING DIRECTION: %s' % verdict['L_B_PASSING_DIRECTION'])
    print('\nwrote lb_determinism.json')
    return 0 if agree else 3


if __name__ == '__main__':
    sys.exit(main())
