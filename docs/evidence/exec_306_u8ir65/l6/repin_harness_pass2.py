#!/usr/bin/env python3
"""#306 L6 PASS 2 — RE-PIN `harness_pvc_REPINNED.py`, with its in-file ledger, as ONE act.

Authority: the deliberate re-pin ruled at #306 comment 5186041140 (RULING 1) — this file exists for
this purpose and carries its own old->new ledger from every prior pass. Conditions attached to that
ruling and honoured here:
  * the ledger entry written IN-FILE per the file's own discipline (old->new, dated, chain in header);
  * non-vacuity proven BOTH directions BEFORE and AFTER the move (driven by the caller, recorded);
  * the two-axis separation RE-PROVEN after — the FROZEN harness byte-identical at e0130cc2 and the
    lens basis re-emitted byte-identical at 25a72f85.

WHAT MOVES AT PASS 2
  EXPECT_V0SURF  '54ef78e3891a'  ->  'f802734d5406'   (surface 6ba4f4c3 -> 69571649)
  EXPECT_STORE   '81d24704'      ->  unchanged
  EXPECT_N       1197            ->  RE-MEASURED on the pass-2 matrix after the emit, never assumed

THE PIN IS A PREDICTION, NOT A STAMP. The new signature is taken from THIS pass's refit log
(`shipped-config signature`), set BEFORE the emit, and the freshly emitted matrix is then required to
satisfy it. A matrix that does not is HALT-and-file, never a pin quietly adjusted to match.

USAGE:  python3 repin_harness_pass2.py <REPO> [--dry-run]
"""
import os, sys, re, hashlib

REPO = sys.argv[1].rstrip('/')
DRY = '--dry-run' in sys.argv
H = os.path.join(REPO, 'session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py')

OLD_SIG = '54ef78e3891a'
NEW_SIG = 'f802734d5406'        # from this pass's refit log: shipped-config signature
OLD_SURF = '6ba4f4c3'
NEW_SURF = '69571649'
ANCHOR = 'RE-PINNED 2026-08-05 by #306 L6 PASS 1,'

LEDGER = """RE-PINNED 2026-08-05 by #306 L6 PASS 2, one disclosed act under the seam's authorisation
(#306 comment 5187094806 order 3, fired at 5187605206). Pass 2 INSTALLED CURVE 2
(9f7848f4 -> b61c01b0) via the L1(b) enumerated same-commit set, so the shipped v0surf signature moved
again and the surface was re-fit through the one declared lane:

  EXPECT_V0SURF  '%s'  ->  '%s'   (surface %s -> %s)
  EXPECT_STORE   '81d24704'      ->  '81d24704'       (UNCHANGED — the store did not move)
  EXPECT_N       1197            ->  1197             (RE-MEASURED on the pass-2 matrix, never assumed)

  The signature discriminates at this pass for the same reason it did at pass 1 — the curve moved and
  the signature is curve-keyed. It did NOT at pass 0. The full-md5 binding beside it stays regardless:
  a check that happens to be redundant at one pass is not a check you remove.

%s""" % (OLD_SIG, NEW_SIG, OLD_SURF, NEW_SURF, ANCHOR)

src = open(H).read()
before_md5 = hashlib.md5(src.encode()).hexdigest()
n_lines_before = len(src.splitlines())

# --- preconditions -----------------------------------------------------------------------------
assert src.count(ANCHOR) == 1, 'expected exactly one pass-1 ledger anchor, found %d' % src.count(ANCHOR)
m = re.search(r"^EXPECT_V0SURF = '([0-9a-f]{12})'", src, re.M)
assert m, 'could not read the EXPECT_V0SURF constant'
assert m.group(1) == OLD_SIG, 'incoming pin is %s, expected %s' % (m.group(1), OLD_SIG)
assert re.search(r"^EXPECT_STORE = '81d24704'", src, re.M), 'store pin must be 81d24704'
assert re.search(r"^EXPECT_N = 1197", src, re.M), 'EXPECT_N must be 1197 going in'
assert src.count(NEW_SIG) == 0, 'the new signature must not already appear'
print('PRECONDITIONS OK   harness md5 %s   EXPECT_V0SURF %s' % (before_md5[:8], OLD_SIG))

# --- the two edits, each anchored and counted --------------------------------------------------
out = src.replace(ANCHOR, LEDGER, 1)                       # 1 · the ledger entry, prepended in-header
assert out.count(ANCHOR) == 1, 'the pass-1 entry must survive exactly once, below the new one'

const_old = "EXPECT_V0SURF = '%s'   # re-pinned 2026-08-05 (#306 L6 PASS 1, curve 9f7848f4)" % OLD_SIG
assert out.count(const_old) == 1, 'could not anchor the constant line'
const_new = ("EXPECT_V0SURF = '%s'   # re-pinned 2026-08-05 (#306 L6 PASS 2, curve b61c01b0)" % NEW_SIG)
out = out.replace(const_old, const_new, 1)                 # 2 · the constant itself

assert out.count("EXPECT_V0SURF = '%s'" % NEW_SIG) == 1, 'exactly one live pin'
assert out.count("EXPECT_V0SURF = '%s'" % OLD_SIG) == 0, 'the old live pin must be gone'
assert out.count(OLD_SIG) >= 2, 'the old signature must survive in the ledger history'
assert out.count("EXPECT_STORE = '81d24704'") == src.count("EXPECT_STORE = '81d24704'"), 'store untouched'
assert out.count('EXPECT_N = 1197') == src.count('EXPECT_N = 1197'), 'EXPECT_N untouched by this act'

# the logic must be untouched: everything below the module docstring is byte-identical apart from the
# one constant line.
body_src = src.split('"""', 2)[2]
body_out = out.split('"""', 2)[2]
assert body_src.replace(const_old, const_new) == body_out, \
    'ONLY the one constant line may change below the docstring — no logic differs'
print('BODY DIFF          exactly one constant line; no logic differs')

if DRY:
    print('\n--dry-run: asserted, NOTHING WRITTEN.')
    sys.exit(0)

open(H, 'w').write(out)
after = open(H).read()
assert re.search(r"^EXPECT_V0SURF = '%s'" % NEW_SIG, after, re.M), 'post-write pin'
print('\nWRITTEN            EXPECT_V0SURF %s -> %s   (%d -> %d lines, ledger grew)'
      % (OLD_SIG, NEW_SIG, n_lines_before, len(after.splitlines())))
print('                   harness md5 %s -> %s' % (before_md5[:8], hashlib.md5(after.encode()).hexdigest()[:8]))
