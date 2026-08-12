"""ORDER 20C — the board-build MUTATOR that stages ORDER 20's fix into a build tree.

Run by `build_board_o20b.sh <out> <this file>` as `python3 mut_fix.py <TREEDIR>`, after the tree is
copied and BEFORE the identity restamp, so the built board's engine identity records the fix.

It copies the SAME two files ORDER 20B staged, from the SAME source: `$SP/tree_FIX`, which
`stage_trees.sh` filled by `git show build/nd-pool-separation:<file>`. Nothing else is touched, so a
board built with this mutator differs from the base board only by ORDER 20's two files.

No environment input: this mutator does one thing. (`RC_*` dials live in build_board_rc.sh, and are
deliberately NOT `RL_`/`PAR_`-prefixed so config_manifest's reject scan never sees them.)
"""
import sys, shutil, hashlib, os

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
FIX = os.environ.get('RC_FIXTREE', SP + '/tree_FIX')
WT = sys.argv[1]
FILES = ['engine/forward_valuation/par_build.py', 'engine/forward_valuation/par_redesign.py']

md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
for f in FILES:
    src, dst = os.path.join(FIX, f), os.path.join(WT, f)
    assert os.path.exists(src), 'missing staged fix file: ' + src
    before = md5(dst)
    shutil.copyfile(src, dst)
    print('  MUT fix: %s  %s -> %s' % (f.split('/')[-1], before[:8], md5(dst)[:8]))
