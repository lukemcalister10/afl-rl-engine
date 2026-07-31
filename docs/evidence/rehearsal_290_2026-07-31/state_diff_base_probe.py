#!/usr/bin/env python3
"""STATE-DIFF BASE PROBE — #290, 2026-07-31.

THE CLAUSE THIS SERVES (standing law, v553): **a state diff names its base commit beside itself.**

WHY A PROBE RATHER THAN PROSE. A state diff carries, per file, an `index <pre>..<post>` line naming
the blob it was cut against. That is enough to test a candidate base WITHOUT applying anything —
and, unlike `git apply --check`, it does not care whether the diff carries its binary payload.

WHAT IT CAN AND CANNOT DO — stated because overstating it is the failure mode:

  * It returns the SET of commits whose trees match every pre-image blob. That set is an INTERVAL,
    not a point: any commit that did not touch the diff's targets is indistinguishable from any
    other. Measured on this tree: L3_T1_state.diff admits **6** commits; L1_amended_state.diff
    admits **25**.
  * So the probe NARROWS; it never RECOVERS. The base must be RECORDED when the diff is generated.
    That is the whole argument for the clause, and this script is the proof of it rather than the
    escape from it.

NON-VACUITY. The probe must be able to reject. It rejects on two distinct grounds, both exercised
in the committed run beside this file: a pre-image MISMATCH (the target exists and its blob differs
— e.g. `harness_pvc_REPINNED.py` at `af12049` and later, where the re-pin already landed) and an
ABSENT target (the path does not exist in that tree — e.g. the same file at `origin/main`, where
the step-4 pack never travelled). A probe that reported every commit as admissible would be
hazard class 5 and is worth nothing.

USAGE
  python3 state_diff_base_probe.py --diff <path> [--tip <rev>] [--limit N] [--show-all]
"""
import argparse
import re
import subprocess
import sys


def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def preimages(path):
    """{target path: pre-image blob prefix} — first `index` line per file section."""
    cur, pre = None, {}
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('diff --git a/'):
                cur = line[len('diff --git a/'):].split(' b/')[0]
            elif line.startswith('index ') and cur:
                m = re.match(r'index ([0-9a-f]+)\.\.([0-9a-f]+)', line)
                if m and cur not in pre:
                    pre[cur] = m.group(1)
    return pre


def score(commit, pre):
    """(match, mismatch, absent) for one candidate commit."""
    match = mismatch = absent = 0
    for f, h in pre.items():
        blob = sh('git', 'rev-parse', '%s:%s' % (commit, f))
        if blob is None:
            absent += 1
        elif blob.startswith(h):
            match += 1
        else:
            mismatch += 1
    return match, mismatch, absent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--diff', required=True)
    ap.add_argument('--tip', default='HEAD', help='walk first-parent from here')
    ap.add_argument('--limit', type=int, default=0, help='0 = the whole line')
    ap.add_argument('--show-all', action='store_true', help='print rejects too')
    a = ap.parse_args()

    pre = preimages(a.diff)
    if not pre:
        print('HALT: no `index` lines found — not a git diff, or generated without them')
        return 2
    commits = (sh('git', 'rev-list', '--first-parent', a.tip) or '').split('\n')
    if a.limit:
        commits = commits[:a.limit]

    n = len(pre)
    admissible = []
    print('diff        : %s' % a.diff)
    print('targets     : %d' % n)
    print('scanned     : %d commits, first-parent from %s' % (len(commits), a.tip))
    print()
    for c in commits:
        m, x, ab = score(c, pre)
        ok = (m == n)
        if ok:
            admissible.append(c)
        if ok or a.show_all:
            print('  %s  %2d/%d match · %d mismatch · %d absent  %s  %s'
                  % (c[:7], m, n, x, ab, 'ADMISSIBLE' if ok else 'reject    ',
                     (sh('git', 'log', '-1', '--format=%s', c) or '')[:52]))
    print()
    print('ADMISSIBLE SET: %d of %d scanned' % (len(admissible), len(commits)))
    if admissible:
        print('  newest %s   oldest %s' % (admissible[0][:7], admissible[-1][:7]))
        print()
        print('  This is an INTERVAL. The probe narrows; it does not recover.')
        print('  The base of record comes from the generating act, recorded beside the diff.')
    else:
        print('  NONE — the diff was not cut against any commit on this line.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
