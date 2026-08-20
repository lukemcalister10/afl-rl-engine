#!/usr/bin/env python3
"""verify_strikes.py — the structural half of this act, asserted rather than described.

Five things this act claims about the TREE (not about a run), each recomputed here:

  1. the scrapped workflow file is GONE;
  2. nothing in the tree still points at it as a live instrument — the one reader that named it
     (.github/workflows/live-scoring.yml) now records the retirement instead, and no workflow
     `uses:`/`needs:` it;
  3. ship_gates_check.py renders A9 and B1 through the SAME strike mechanism as A15 — i.e. a
     gate(...) call whose status literal is 'STRUCK', not a bypass, a skip, or a deleted leg;
  4. no B1 path can still HALT — a retired gate that can red the build on a bad input has not
     been retired;
  5. SHIP_GATES.md carries a written strike record for A9 and B1, each with the owner's date.

Run: python3 docs/evidence/gate_strikes_2026-08-20/verify_strikes.py    (exit 0 = PASS)
"""
import os
import re
import sys

ROOT = os.environ.get('RL_REPO') or os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

GONE = '.github/workflows/live-scoring-proofs.yml'
FAILS = []


def check(ok, label, detail=''):
    print('  %-4s %s%s' % ('PASS' if ok else 'FAIL', label, ('  — ' + detail) if detail else ''))
    if not ok:
        FAILS.append(label)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


print('verify_strikes — root %s' % ROOT)

# 1 -------------------------------------------------------------------------------- the file is gone
check(not os.path.exists(os.path.join(ROOT, GONE)),
      'the scrapped workflow is deleted', GONE)

# 2 ----------------------------------------------------------- no workflow still wires it in
wf_dir = os.path.join(ROOT, '.github', 'workflows')
live = read('.github/workflows/live-scoring.yml')
wired = []
for name in sorted(os.listdir(wf_dir)):
    body = read('.github/workflows/' + name)
    for ln in body.splitlines():
        s = ln.strip()
        # the artifact NAME 'live-scoring-proofs-light' in live-scoring.yml is not a wiring
        # of the deleted file; only a reference to the FILENAME is.
        if 'live-scoring-proofs.yml' in s and not s.startswith('#'):
            wired.append('%s: %s' % (name, s[:70]))
check(not wired, 'no workflow wires the deleted file (comments excepted)', '; '.join(wired) or 'clean')
LIVE_FLAT = re.sub(r'\s+', ' ', live)
check('SCRAPPED 2026-08-20' in live and 'live-scoring-proofs.yml` is DELETED' in live,
      'live-scoring.yml records the retirement where it used to point')
check('2a.3' in live and 'LANDER SELF-TEST' in live.upper(),
      'live-scoring.yml names the successor (PLAN_v6 2a.3 lander self-test)')

# 3 ------------------------------------------------- A9 / B1 struck by the A15 mechanism, not bypassed
src = read('ship_gates_check.py')
for gid in ('A15', 'A9', 'B1'):
    hits = re.findall(r"gate\(\s*'%s'\s*,\s*\w+\s*,\s*'([A-Z-]+)'" % gid, src)
    check(bool(hits) and all(h in ('STRUCK', 'INJECTED') for h in hits),
          '%s renders only through the strike mechanism' % gid,
          'statuses emitted: %s' % (sorted(set(hits)) or 'NONE'))

# the A15 line itself must be untouched: this act generalises a mechanism, it does not rewrite it
check("gate('A15', False, 'STRUCK', 'Luke 02/07/2026" in src,
      "A15's own strike line is byte-unchanged")

# 4 ---------------------------------------------------------------- no B1 path can still HALT
b1_halt = re.findall(r"gate\(\s*'B1'\s*,\s*\w+\s*,\s*'HALT'", src)
check(not b1_halt, 'no B1 path can still HALT', '%d HALT path(s) remain' % len(b1_halt))
# ... and A9 can no longer be scored by the comparison helper that used to FAIL it
check("cmp_gate('A9'" not in src, "A9 no longer runs through cmp_gate's pass/fail comparison")

# 5 -------------------------------------------------------------- the written record exists
sg = read('SHIP_GATES.md')
check('A9.  STRUCK (Luke, 20/08/2026)' in sg, 'SHIP_GATES.md records the A9 strike, dated')
check('B1. STRUCK (Luke, 20/08/2026)' in sg, 'SHIP_GATES.md records the B1 strike, dated')
# The words must survive line-wrapping in both carriers, so compare on whitespace-flattened text —
# a quote broken across a line is still the quote, and a quote that is NOT there is still not there.
def flat(t):
    return re.sub(r'\s+', ' ', t.replace('\n#', ' ').replace("' '", ''))
SG_FLAT, SRC_FLAT = flat(sg), flat(src)
A9_WORDS = ('Those player ordering assertions were retired and are outdated. Since they occurred, '
            'Ward has hit an excellent run of form.')
B1_WORDS = 'That cohort rail again was retired. Weeks ago.'
check(A9_WORDS in SG_FLAT and A9_WORDS in SRC_FLAT,
      "the owner's A9 words are carried verbatim in BOTH the record and the instrument",
      'SHIP_GATES.md=%s ship_gates_check.py=%s' % (A9_WORDS in SG_FLAT, A9_WORDS in SRC_FLAT))
check(B1_WORDS in SG_FLAT and B1_WORDS in SRC_FLAT,
      "the owner's B1 words are carried verbatim in BOTH the record and the instrument",
      'SHIP_GATES.md=%s ship_gates_check.py=%s' % (B1_WORDS in SG_FLAT, B1_WORDS in SRC_FLAT))

# the RULEBOOK is not edited by this act — P11 is appended to an UNSIGNED draft
am = read('docs/proposals/rulebook/AMENDMENT_1b_2026-08-20.md')
check('P11' in am and 'PROPOSED. NOT APPLIED' in am,
      'P11 is proposed in the unsigned draft, not applied to the RULEBOOK')
check('P11' not in read('docs/RULEBOOK.md'), 'docs/RULEBOOK.md carries no P11 (law 10(a) untouched)')

print('verify_strikes: %s (%d check(s) failed)' % ('FAIL' if FAILS else 'PASS', len(FAILS)))
sys.exit(1 if FAILS else 0)
