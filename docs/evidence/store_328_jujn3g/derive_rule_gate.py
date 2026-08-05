#!/usr/bin/env python3
"""#328 STEP 1 — THE DERIVE-RULE GATE (Addendum 1 item 3, from pre-fire audit fault 3).

#323 section 1 is the owner's first word in the batch: career games becomes a DERIVED SUM —
"a computed total cannot go stale ... the weekly feed keeps updating rows only." The rule is
read live: rl_model.py:493 takes the top-level counter straight into the own-form trust weight
(w = clamp(games/130.0, 0.30, 0.85)), which #323 says moves 181 records.

The batch installs a store in which the rule holds. Nothing until now asserted that it does, and
nothing would have noticed the next weekly feed re-introducing the drift the rule exists to prevent.
This is that assert. It runs at install, on the bytes about to be written.

  python3 derive_rule_gate.py <store.json>            # assert; non-zero exit on any mismatch
  python3 derive_rule_gate.py <store.json> --tamper N # perturb N counters in memory first, to
                                                      # demonstrate the gate is able to fail

Uniform, no special cases: every record carries a games key and a scoring list with games on
every row (checked here, not assumed), and the counter must equal the sum of the row games.
"""
import json, sys


def check(records):
    """Return (mismatches, structural_faults). Both empty means the rule holds."""
    mismatches, structural = [], []
    for rec in records:
        key = rec.get('key')
        if 'games' not in rec or rec.get('games') is None:
            structural.append((key, 'no games counter'))
            continue
        rows = rec.get('scoring')
        if not isinstance(rows, list):
            structural.append((key, 'no scoring list'))
            continue
        if any('games' not in r or r.get('games') is None for r in rows):
            structural.append((key, 'a season row carries no games'))
            continue
        total = sum(r['games'] for r in rows)
        if rec['games'] != total:
            mismatches.append((key, rec['games'], total))
    return mismatches, structural


def main(argv):
    path = argv[1]
    records = json.load(open(path))
    tamper = 0
    if '--tamper' in argv:
        tamper = int(argv[argv.index('--tamper') + 1])
        for rec in records[:tamper]:
            rec['games'] = (rec.get('games') or 0) + 1

    mismatches, structural = check(records)
    print('derive-rule gate: %d records read from %s%s'
          % (len(records), path, '  [%d counters TAMPERED]' % tamper if tamper else ''))
    print('  structural faults (missing counter / rows / row games): %d' % len(structural))
    print('  counter != sum(season row games): %d' % len(mismatches))
    for key, got, want in mismatches[:10]:
        print('    %-28s counter %s  rows sum %s' % (key, got, want))
    if mismatches or structural:
        raise SystemExit('DERIVE-RULE GATE FAILS — the store does not satisfy #323 section 1.')
    print('DERIVE-RULE GATE PASS — every counter equals its own season-row sum.')


if __name__ == '__main__':
    main(sys.argv)
