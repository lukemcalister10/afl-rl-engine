#!/usr/bin/env python3
"""verify_v3.py — the v3 amendment act, asserted rather than described.

    python3 docs/evidence/rulebook_v3_2026-08-20/verify_v3.py        exit 0 = PASS

Six assertions, each one a thing a reader would otherwise have to take on trust:

  V1  PART 1 numbers TWELVE laws, contiguous, and the RULEBOOK declares that count itself.
  V2  PART 4 numbers ELEVEN process laws, P1..P11, contiguous.
  V3  Laws 1-10 are BYTE-IDENTICAL to their v2.1 text (the amendment touched 11, added 12, and
      nothing else in PART 1). Compared against the base commit, not against a copy in this file.
  V4  NOTHING DIED WITH THE TWIN: every threshold payload the removed docs/acceptance_v2_0.json
      carried is present in RULEBOOK PART 3. Read out of the base commit's twin, not hardcoded.
  V5  THE TWIN IS GONE and so is its regenerator.
  V6  THE NEGATIVE CONTROL: put a derived laws view back at that path and the lint REDS on R5 and
      R6. A rule that has never been seen to fail has not been tested. The probe writes into a
      TEMPORARY TREE, never into the repo (ruled_red.json _probe_contract: a probe must never
      write to the tree it measures).
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = '68a3a50'
ROOT = os.environ.get('RL_REPO') or subprocess.run(
    ['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
RB = os.path.join(ROOT, 'docs', 'RULEBOOK.md')

fails = []


def check(ok, name, detail):
    print('  %-4s %-28s %s' % ('PASS' if ok else 'FAIL', name, detail))
    if not ok:
        fails.append(name)


def base_blob(path):
    p = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASE, path)],
                       capture_output=True)
    return p.stdout.decode('utf-8') if p.returncode == 0 else None


sys.path.insert(0, os.path.join(ROOT, 'tools'))
import rulebook_lint as RL                                                       # noqa: E402

text = open(RB, encoding='utf-8').read()
laws, numbers, unparsed = RL.parse_rulebook(text)
pids, pnums = RL.parse_process_laws(text)

print('verify_v3 — docs/evidence/rulebook_v3_2026-08-20')

# V1
check(len(laws) == 12 and numbers == list(range(1, 13)) and not unparsed
      and RL.declared_count(text) == 12,
      'V1 twelve laws', 'PART 1 numbers %d (%s), declared %s'
      % (len(laws), '1..%d' % len(numbers), RL.declared_count(text)))

# V2
check(len(pids) == 11 and pnums == list(range(1, 12)),
      'V2 eleven process laws', 'PART 4 numbers %d, P1..P%d' % (len(pids), len(pnums)))

# V3 — laws 1-10 byte-identical to v2.1
old = base_blob('docs/RULEBOOK.md') or ''


def part1_lines(t):
    out, inside = [], False
    for ln in t.splitlines():
        if ln.startswith('## PART 1'):
            inside = True
            continue
        if inside and ln.startswith('## '):
            break
        if inside:
            out.append(ln)
    return out


def upto_law(lines, n):
    """The PART 1 block from law 1 up to (not including) law n."""
    out = []
    for ln in lines:
        m = re.match(r'^\s*(\d+)\.\s', ln)
        if m and int(m.group(1)) >= n:
            break
        out.append(ln)
    return '\n'.join(out).strip('\n')


check(upto_law(part1_lines(old), 11) == upto_law(part1_lines(text), 11),
      'V3 laws 1-10 unchanged', 'byte-identical to %s' % BASE)

# V4 — every threshold the twin carried survives in PART 3
twin = json.loads(base_blob('docs/acceptance_v2_0.json') or '{}')
part3 = text.split('## PART 3')[1].split('## PART 4')[0] if '## PART 3' in text else ''
missing = []
for law in twin.get('laws', []):
    for key, val in law.items():
        if key in ('id', 'status', 'check', 'note'):
            continue
        # the numeric/None payloads: pick1_equals 3000, band_scar 200, max_pct 2.0, max 1.3, ...
        needles = [str(val), str(val).rstrip('0').rstrip('.')]
        if not any(n and n in part3 for n in needles):
            missing.append('%s.%s=%s' % (law.get('id'), key, val))
check(not missing, 'V4 thresholds survived',
      '%d twin laws scanned, %d threshold payload(s) absent from PART 3: %s'
      % (len(twin.get('laws', [])), len(missing), missing or '-'))

# V5
gone = [p for p in ('docs/acceptance_v2_0.json', 'tools/rulebook_twin.py')
        if not os.path.exists(os.path.join(ROOT, p))]
check(len(gone) == 2, 'V5 twin + regenerator gone', 'absent: %s' % ', '.join(gone))

# V6 — the negative control, in a temporary tree
tmp = tempfile.mkdtemp(prefix='verify_v3_')
try:
    os.makedirs(os.path.join(tmp, 'docs'))
    os.makedirs(os.path.join(tmp, 'tools'))
    shutil.copy(RB, os.path.join(tmp, 'docs', 'RULEBOOK.md'))
    with open(os.path.join(tmp, 'docs', 'acceptance_v2_0.json'), 'w', encoding='utf-8') as fh:
        json.dump({'regenerated_from': 'RULEBOOK.md v3', 'laws': [{'id': 'G-MONO'}]}, fh)
    f, _n = RL.lint(tmp)
    reds = ' '.join(f)
    check(len(f) == 2 and 'R5 TWIN ABSENCE' in reds and 'R6 NO DERIVED VIEW' in reds,
          'V6 negative control', 'a replanted twin reds %d rule(s): %s'
          % (len(f), ', '.join(x.split(':')[0] for x in f) or 'none — THE RULE IS ASLEEP'))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print('verify_v3: %s (%d fail)' % ('PASS' if not fails else 'FAIL', len(fails)))
sys.exit(1 if fails else 0)
