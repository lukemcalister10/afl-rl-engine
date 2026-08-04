#!/usr/bin/env python3
"""#306 §3 — WHERE THE YEAR-ZERO GAP LIVES, made re-runnable.  (Charter D2 / seam condition 1.)

THE QUESTION
  N16's first spec word is "tail constrained by construction".  This measures whether the tail is
  in fact where the year-zero residual sits on the HALT substrate, so the directive's first limb
  rests on a number taken here rather than on the era's baseline diagnostic map.

READ THIS BEFORE QUOTING ANY NUMBER BELOW
  **This is the FIT population** — the matrix's own `teaches_curve` rows at picks 1-64 — and it is
  NOT the G-Y0 gate's population.  The gate runs inside `one_source_selftest.py` over its own
  ~1,326-row set and prints its own figure every run.  The overall numbers here land near the gated
  ones and are NOT them.  The SHAPE across bands is what this script is for; a figure from here must
  never be presented as a gated G-Y0.

THE METHOD
  For each pass, the gap is computed against THE CURVE THAT WAS INSTALLED AT THAT PASS — the pairing
  is fixed in PAIRS below and asserted by md5, because comparing a matrix against the wrong pass's
  curve would produce a plausible, wrong table.  Per band:

      gap% = 100 * SUM(v0 - curve[pick]) / SUM(curve[pick])     over teaching rows in the band

  Passes 2 and 4 installed the SAME curve, so their rows are the repeat control: any band difference
  between them is path memory, not signal.

INPUTS ARE COMMITTED AND ASSERTED BY md5.  Read-only: no engine act, no bake.

    python3 tail_gap_by_band.py
"""
import json, hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)

# pass -> (matrix, matrix md5, curve artifact installed AT that pass, its md5, payload)
PAIRS = [
    (2, 'pass2_matrix.json', '43169abba833851a95ade398b2018a63',
        'pass1_derived_curve2.json', '31eb9a3e243e2e2807fb6bb5f3751848', 'ca662051'),
    (3, 'pass3_matrix.json', '760032aa09d339a620250438dc56ba16',
        'pass2_derived_curve3.json', '7baa781892f3f864d2bc4cdfa896279c', 'b0bda532'),
    (4, 'pass4_matrix.json', '85d2a04b3fc40fd509796bbc8e75b3fb',
        'pass3_derived_curve4.json', '9c0a3fd95612ce647a73d05d633b36ae', 'ca662051'),
]
BANDS = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def pinned(name, want):
    p = os.path.join(D, name)
    got = md5(p)
    if got != want:
        raise SystemExit('HALT: %s is %s, pinned %s — an input moved.' % (name, got, want))
    return p


def payload_of(ladder):
    """The recipe, re-proved here rather than assumed: STRING keys (the recipe string-sorts them),
    default separators, int(round(v)) values.  An int-keyed dict hashes to something else entirely —
    L5 docket 11."""
    curve = {str(i + 1): int(round(v)) for i, v in enumerate(ladder)}
    return hashlib.md5(json.dumps(curve, sort_keys=True).encode()).hexdigest()[:8], curve


def main():
    rows, table = [], {}
    for n, mf, mh, cf, ch, want_pay in PAIRS:
        recs = [r for r in json.load(open(pinned(mf, mh)))['recs']
                if r.get('teaches_curve') and r.get('v0') is not None
                and r.get('pick') and 1 <= r['pick'] <= 64]
        ladder = json.load(open(pinned(cf, ch)))['ladders']['ruled_pooled_numeraire']
        pay, curve = payload_of(ladder)
        if pay != want_pay:
            raise SystemExit('HALT: %s derives payload %s, expected %s' % (cf, pay, want_pay))
        num = sum(r['v0'] - curve[str(r['pick'])] for r in recs)
        den = sum(curve[str(r['pick'])] for r in recs)
        cells = {}
        for lo, hi in BANDS:
            sub = [r for r in recs if lo <= r['pick'] <= hi]
            nn = sum(r['v0'] - curve[str(r['pick'])] for r in sub)
            dd = sum(curve[str(r['pick'])] for r in sub)
            cells['%d-%d' % (lo, hi)] = {'gap_pct': round(100.0 * nn / dd, 4) if dd else None,
                                         'rows': len(sub)}
        table[n] = {'installed_payload': pay, 'rows': len(recs),
                    'overall_gap_pct': round(100.0 * num / den, 4), 'by_band': cells}
        rows.append((n, pay, table[n]['overall_gap_pct'], [cells['%d-%d' % b]['gap_pct'] for b in BANDS]))

    assert table[2]['installed_payload'] == table[4]['installed_payload'], \
        'passes 2 and 4 must share an installed curve — they are the repeat control'
    swing = {b: round(table[3]['by_band'][b]['gap_pct'] - table[2]['by_band'][b]['gap_pct'], 4)
             for b in table[2]['by_band']}
    repeat = {b: round(table[4]['by_band'][b]['gap_pct'] - table[2]['by_band'][b]['gap_pct'], 6)
              for b in table[2]['by_band']}

    out = {'what': 'the year-zero gap by pick band on the L6 halt substrate, per pass',
           'POPULATION_WARNING': ("FIT population (teaches_curve rows, picks 1-64) — NOT the G-Y0 "
                                  "gate's ~1,326-row population. Never quote a figure from here as "
                                  "a gated G-Y0."),
           'formula': '100 * SUM(v0 - curve[pick]) / SUM(curve[pick]) over the band',
           'per_pass': table,
           'cycle_amplitude_pp_pass3_minus_pass2': swing,
           'repeat_control_pp_pass4_minus_pass2': repeat,
           'reading': ('The gap is a TAIL phenomenon: picks 46-64 sit far above the curve while '
                       'picks 1-10 sit below it. The cycle moves every band by ~2pp and the tail '
                       'most. The repeat control (same installed curve, different history) is flat '
                       'to ~0.001pp, so none of the band structure is path memory.')}
    p = os.path.join(HERE, 'tail_gap_by_band.json')
    json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
    open(p, 'a').write('\n')

    print(out['POPULATION_WARNING'] + '\n')
    print('%-6s %-10s %-9s %s' % ('pass', 'curve', 'overall', ' '.join('%9s' % ('%d-%d' % b) for b in BANDS)))
    for n, pay, ov, cells in rows:
        print('%-6d %-10s %+8.3f%% %s' % (n, pay, ov, ' '.join('%+8.2f%%' % c for c in cells)))
    print('\ncycle amplitude, pass 3 - pass 2 (pp): ' + ' · '.join('%s %+.2f' % (b, v) for b, v in swing.items()))
    print('repeat control, pass 4 - pass 2 (pp):  ' + ' · '.join('%s %+.4f' % (b, v) for b, v in repeat.items()))
    print('\nwrote', os.path.relpath(p, D))


if __name__ == '__main__':
    main()
