#!/usr/bin/env python3
"""before_after.py — the "nothing else changed" falsifier, computed rather than eyeballed.

Parses the BOARD lines out of two full ship_gates_check runs and diffs every gate's CURRENT status.
The claim this act makes is that exactly two verdicts moved (A9 FAIL->STRUCK, B1 HALT->STRUCK) and
that no other gate moved in either direction — including the standing fails, which a careless strike
act could quietly tidy away.

  python3 docs/evidence/gate_strikes_2026-08-20/before_after.py BEFORE.txt AFTER.txt

Exit 0 only if the observed set of changes is EXACTLY the expected set.
"""
import re
import sys

# The board's own row format: "<gid> [DC] <control>| <previous>| <current> <detail>"
ROW = re.compile(r'^([A-D]\d+[a-d]?)\s+(?:\[DC\])?\s*([A-Z-]+|—)\s*\|\s*([A-Z-]+|—)\s*\|\s*([A-Z-]+)\s')

EXPECTED = {'A9': ('FAIL', 'STRUCK'), 'B1': ('HALT', 'STRUCK')}


def board(path):
    """-> {gid: current_status}. Only lines the board itself emitted as gate rows."""
    out = {}
    with open(path, encoding='utf-8', errors='replace') as f:
        for ln in f:
            m = ROW.match(ln)
            if m:
                out.setdefault(m.group(1), m.group(4))
    return out


def main(bp, ap):
    b, a = board(bp), board(ap)
    if not b or not a:
        print('before_after: FAIL — could not parse a board from %s' % (bp if not b else ap))
        return 1

    missing = sorted(set(b) - set(a))
    added = sorted(set(a) - set(b))
    changed = {g: (b[g], a[g]) for g in sorted(set(b) & set(a)) if b[g] != a[g]}

    print('gates parsed: BEFORE %d, AFTER %d' % (len(b), len(a)))
    print('\n%-6s %-10s %-10s %s' % ('gate', 'BEFORE', 'AFTER', ''))
    for g in sorted(set(b) | set(a), key=lambda x: (x[0], int(re.sub(r'\D', '', x) or 0), x)):
        bs, as_ = b.get(g, '—'), a.get(g, '—')
        mark = '   <- CHANGED' if bs != as_ else ''
        print('%-6s %-10s %-10s%s' % (g, bs, as_, mark))

    ok = True
    if missing or added:
        print('\nFAIL: the gate SET moved (missing %s / added %s) — a strike must not remove a gate'
              % (missing or 'none', added or 'none'))
        ok = False
    if changed != EXPECTED:
        print('\nFAIL: changed set %r != expected %r' % (changed, EXPECTED))
        ok = False
    else:
        print('\nchanged: exactly %s — and nothing else' %
              ', '.join('%s %s->%s' % (g, v[0], v[1]) for g, v in sorted(changed.items())))

    # The standing fails are named explicitly: this act is a ruling, not a sweep.
    swept = [g for g in ('A2', 'A3', 'A12') if a.get(g) != 'FAIL']
    if swept:
        print('FAIL: standing fail(s) %s no longer FAIL after the act — RULEBOOK PART 3 carries them '
              'AS RECORDED until Luke re-rules' % ', '.join('%s=%r' % (g, a.get(g)) for g in swept))
        ok = False
    else:
        print('standing fails A2/A3/A12 still FAIL, exactly as recorded (not swept)')

    print('\nbefore_after: %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
