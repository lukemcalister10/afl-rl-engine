#!/usr/bin/env python3
"""ARM 2 — BUILD THE "RATCHET STILL ON" ENGINE, for must-move board (b). SCRATCH ONLY.

WHAT THIS PRODUCES AND WHY IT MUST NOT BE THE SHIPPED ENGINE
  Study B section 4.3 requires three boards to close the must-move proof:
      (a) the shipped board                       — incumbent forests, ratchet ON
      (b) the rebaked forests, ratchet STILL ON   — THIS ENGINE
      (c) the rebaked forests, ratchet REMOVED    — the branch's engine, the candidate
  and the proof is that (b) and (c) agree. Board (b) cannot be built by the branch's engine, which has
  the block deleted, and it cannot be built by the OLD engine either, because _o44_xs() walks estimators_
  and the design estimator has none (M-52, and this seat reproduced the AttributeError in anger).

  So (b) needs one thing that exists nowhere else: the shipped ratchet, with its knot reader generalised
  to the new estimator's own bin thresholds. That generalisation is FOUR LINES, and it lives HERE, in the
  evidence tree, and is written into a SCRATCH copy of the engine that is never committed and never
  loaded by anything but this proof. Putting it in the shipped engine would be precisely the road the
  comparison paper's F1 rejected: "keeping any read-site smoother through the estimator swap means
  rewriting it against the new estimator's OWN private internals" — a larger, less testable internal-API
  dependency than the four-line loss subclass, and one nobody would need once the fit is exact.

  The restored block is taken from GIT (the branch base 4124fd6), not retyped, so board (b) is built by
  the ratchet the estate actually shipped and not by this seat's recollection of it.

Usage: make_ratchet_engine.py --src <branch _merged_recover.py> --out <scratch _merged_recover.py>
       [--base 4124fd6]
"""
import argparse, os, subprocess, sys

GENERALISED = '''def _o44_xs():
    """THE EXACT KNOTS OF THE STEP SURFACE — GENERALISED FOR THE MUST-MOVE PROOF ONLY (rebake ARM 2).

    The shipped body walked `_m.estimators_`, which HistGradientBoostingRegressor does not have (study B
    M-52; reproduced as a live AttributeError by scripts/mustmove_ratchet.py). The walk below is the exact
    analogue for the new estimator: a boosting round's predictor carries a `nodes` record array with
    feature_idx / num_threshold / is_leaf, so the split thresholds on the level feature are read the same
    way tree_.threshold[tree_.feature == LVL] read them. Everything else in this file is the SHIPPED
    ORDER 44 block, restored verbatim from git.

    THIS FILE IS SCRATCH. It exists to build must-move board (b) and for nothing else."""
    _k=(id(cm),id(q97m))
    _x=_O44_XS.get(_k)
    if _x is None:
        _s=set()
        for _m in [cm[_q] for _q in cp.Q]+[q97m]:
            if hasattr(_m,'estimators_'):
                for _e in np.asarray(_m.estimators_).ravel():
                    _t=_e.tree_; _s.update(float(_v) for _v in _t.threshold[_t.feature==_O44_LVL])
            else:
                for _rnd in _m._predictors:
                    for _pr in _rnd:
                        _nd=_pr.nodes; _sel=(~_nd['is_leaf'].astype(bool))&(_nd['feature_idx']==_O44_LVL)
                        _s.update(float(_v) for _v in _nd['num_threshold'][_sel])
        _x=np.concatenate([[_O44_LO],np.array(sorted(_s),dtype=float)+_O44_EPS,[_O44_HI]])
        _x=np.unique(_x[(_x>=_O44_LO)&(_x<=_O44_HI)])
        _O44_XS[_k]=_x
    return _x
'''


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--base', default='4124fd6')
    ap.add_argument('--repo', default=os.environ.get('RL_REPO', '.'))
    a = ap.parse_args(argv[1:])

    old = subprocess.run(['git', '-C', a.repo, 'show',
                          '%s:engine/rl_after/_merged_recover.py' % a.base],
                         capture_output=True, text=True, check=True).stdout

    # the SHIPPED block, lifted from git: header -> just before def _b6_core
    s = old.index('# ==== ORDER 44 — THE LEVEL-AXIS BAND MONOTONISER (RL_O44_LVLMONO')
    e = old.index('def _b6_core(p,Y):', s)
    block = old[s:e]
    assert block.count('def _o44_xs():') == 1 and block.count('def _o44_band(') == 1

    # swap in the generalised knot reader (the ONLY change to the shipped block)
    ks = block.index('def _o44_xs():')
    ke = block.index('def _o44_rows6(F):')
    block = block[:ks] + GENERALISED + block[ke:]

    src = open(a.src).read()
    # put the block back where the retirement note stands
    s2 = src.index('# ==== ORDER 44 — THE LEVEL-AXIS BAND MONOTONISER — RETIRED INTO THE FIT')
    e2 = src.index('def _b6_core(p,Y):', s2)
    src = src[:s2] + ('# SCRATCH ENGINE — must-move board (b). The ORDER 44 block below is RESTORED FROM\n'
                      '# GIT (%s) with ONLY its knot reader generalised to the new estimator. NEVER COMMITTED.\n'
                      % a.base) + block + src[e2:]

    # restore _b6_core's dispatch
    note = ('    # ORDER 44 RETIRED (above): the two lines below are the band, unmediated. They were the\n'
            '    # `dial OFF` path and they are now the only path — _b6_core is byte-identical to what\n'
            '    # RL_O44_LVLMONO=0 always produced, on forests that no longer need the repair.\n')
    assert src.count(note) == 1
    src = src.replace(note, '    if _O44 and not _O44_SUSPEND[0]:\n'
                            '        with contextlib.redirect_stdout(io.StringIO()): return _o44_band(p,Y)\n')

    # the production-hook conservation line (raw variants never execute it; restored for fidelity)
    hook = ("    # ORDER 44 LAW-9 LEG RETIRED with its dial: the +conserve variants were never the shipped\n"
            "    # default (RAW/unconserved was, under the owner's recorded waiver v830), and the\n"
            "    # renormalisation had nothing left to renormalise once the ratchet was gone.\n")
    assert src.count(hook) == 1
    src = src.replace(hook, '    if _O44_CONSERVE: pr*=_O44_C.get(MA.gfut(p),1.0)\n')

    with open(a.out, 'w') as f:
        f.write(src)
    import hashlib
    print('scratch ratchet engine -> %s  md5=%s' % (a.out, hashlib.md5(src.encode()).hexdigest()))
    print('  ORDER 44 restored from %s; knot reader generalised (4 lines); everything else verbatim.' % a.base)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
