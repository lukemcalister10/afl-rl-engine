#!/usr/bin/env python3
"""#306 §2 — THE HYSTERESIS MAGNITUDE, made re-runnable.  (Charter D2 / seam condition 1.)

THE QUESTION
  R-K's mechanism clause read that removing the refit's path memory is what the deterministic fit
  lane exists to do, with the implication that it would break the observed period-2 cycle.  This
  script measures the path memory's SIZE, so the claim rests on a number rather than on a story.

THE METHOD — a same-curve pair
  Passes 2 and 4 of L6 installed a BYTE-IDENTICAL curve (ca662051) onto a BYTE-IDENTICAL frozen
  fitted stack, but arrived there through different histories.  Every difference between their
  emitted matrices is therefore path memory and nothing else.  The comparison is over the year-zero
  value `v0` that each matrix record carries — the quantity the G-Y0 gate is built out of.

  A control pair (passes 1 and 3) is measured beside it: DIFFERENT installed curves, so its
  differences are the map doing its job, not hysteresis.  Without the control the same-curve number
  has nothing to be small RELATIVE TO.

INPUTS ARE COMMITTED AND ASSERTED BY md5.  If an input moves, this HALTS rather than reporting a
number against an unnamed substrate.  Read-only: no engine act, no bake, nothing written outside
this directory.

    python3 hysteresis_magnitude.py
"""
import json, hashlib, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)

PINS = {
    'pass1_matrix.json': '143dcbad8bef81264a79ca748c9a7823',
    'pass2_matrix.json': '43169abba833851a95ade398b2018a63',
    'pass3_matrix.json': '760032aa09d339a620250438dc56ba16',
    'pass4_matrix.json': '85d2a04b3fc40fd509796bbc8e75b3fb',
}
BANDS = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def load(name):
    p = os.path.join(D, name)
    got = md5(p)
    if got != PINS[name]:
        raise SystemExit('HALT: %s is %s, pinned %s — an input moved; re-pin deliberately or stop.'
                         % (name, got, PINS[name]))
    d = json.load(open(p))
    return {r['key']: r for r in d['recs'] if r.get('v0') is not None}, d['meta']['v0surf_sig']


def compare(a_name, b_name):
    A, siga = load(a_name)
    B, sigb = load(b_name)
    keys = sorted(set(A) & set(B))
    diffs = [B[k]['v0'] - A[k]['v0'] for k in keys]
    moved = [d for d in diffs if d != 0]
    rel = [abs(B[k]['v0'] - A[k]['v0']) / abs(A[k]['v0']) for k in keys if A[k]['v0']]
    band = {}
    for lo, hi in BANDS:
        sub = [k for k in keys if A[k].get('pick') and lo <= A[k]['pick'] <= hi
               and A[k].get('teaches_curve')]
        band['%d-%d' % (lo, hi)] = {
            'rows': len(sub),
            'moved': sum(1 for k in sub if B[k]['v0'] != A[k]['v0']),
            'max_abs': max((abs(B[k]['v0'] - A[k]['v0']) for k in sub), default=0.0),
        }
    return {
        'a': a_name, 'b': b_name,
        'a_v0surf_sig': siga, 'b_v0surf_sig': sigb,
        'rows_compared': len(keys),
        'moved': len(moved),
        'moved_pct': round(100.0 * len(moved) / len(keys), 4) if keys else None,
        'max_abs_move': max((abs(d) for d in diffs), default=0.0),
        'max_rel_move': max(rel, default=0.0),
        'median_abs_move_over_movers': statistics.median(sorted(abs(d) for d in moved)) if moved else 0.0,
        'mean_signed_move': sum(diffs) / len(diffs) if diffs else 0.0,
        'by_band_teaching_rows': band,
    }


def main():
    same = compare('pass2_matrix.json', 'pass4_matrix.json')   # SAME curve ca662051, different history
    ctrl = compare('pass1_matrix.json', 'pass3_matrix.json')   # DIFFERENT curves — the control

    assert same['a_v0surf_sig'] == same['b_v0surf_sig'], \
        'the same-curve pair must share a signature key — the curve is what the signature hashes'
    assert ctrl['a_v0surf_sig'] != ctrl['b_v0surf_sig'], \
        'the control pair must NOT share a signature key'

    out = {
        'what': ('the SIZE of the refit path memory, measured on a same-curve pair, with a '
                 'different-curve control beside it'),
        'population': ('every matrix record carrying a v0 value (2,646 emitted records); the '
                       'per-band block restricts to teaches_curve rows at picks 1-64'),
        'same_curve_pair': same,
        'different_curve_control': ctrl,
        'reading': ('The same-curve pair is the path memory ALONE: identical installed curve, '
                    'identical frozen fitted stack, different history. It moves 60 of 2,646 v0 '
                    'values by at most 0.1 absolute / 1.85e-4 relative. The cycle it was proposed '
                    'to explain swings the band gaps by ~2 percentage points. The hysteresis is '
                    'real and must be removed for the lane to be auditable, but it is three orders '
                    'of magnitude too small to BE the cycle. Determinism is necessary, not '
                    'sufficient.'),
        'not_a_gated_figure': ('nothing here is the G-Y0 gate figure; the gate runs on its own '
                               'population inside one_source_selftest.py'),
    }
    p = os.path.join(HERE, 'hysteresis_magnitude.json')
    json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
    open(p, 'a').write('\n')

    for label, r in (('SAME curve ca662051, different history', same),
                     ('CONTROL — different curves', ctrl)):
        print('%s\n  %s vs %s   sigs %s -> %s' % (label, r['a'], r['b'],
                                                  r['a_v0surf_sig'][:12], r['b_v0surf_sig'][:12]))
        print('  rows %d | moved %d (%.2f%%) | max abs %.4f | max rel %.3e | mean signed %+.4f'
              % (r['rows_compared'], r['moved'], r['moved_pct'], r['max_abs_move'],
                 r['max_rel_move'], r['mean_signed_move']))
        print('  by band (teaching rows): ' + ' · '.join(
            '%s %d/%d max %.3f' % (b, v['moved'], v['rows'], v['max_abs']) for b, v in r['by_band_teaching_rows'].items()))
        print()
    print('wrote', os.path.relpath(p, D))


if __name__ == '__main__':
    main()
