"""ORDER 25 (carried from ORDER 20C) — install the re-sealed book (built in a scratchpad copy, never in the checkout).

Guards: the book being installed must be the one built against the LANDED board, its builder's own
parity gate must have passed, and the srcmd5 must be self-consistent and still name the unmoved store.
"""
import hashlib, os, shutil, json

ROOT = '/home/user/afl-rl-engine/.claude/worktrees/agent-ae867318eb00a513e'
SRC = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o25/book'
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

log = open(os.path.join(SRC, 'book_build.log')).read()
assert 'BOOK PARITY GATE PASS' in log, "the builder's own parity gate did not pass — refusing to install"

newbook = os.path.join(SRC, 's4_matrix.json')
sm = json.load(open(os.path.join(SRC, 's4_matrix.json.srcmd5')))
assert sm['own_md5'] == md5(newbook), "srcmd5 own_md5 does not match the book it describes"
assert sm['source_md5'] == 'd9a24282357cf3083b1640466e3ecd83', "srcmd5 names a moved store — HALT"

for rel, src in (('engine/rl_after/s4_matrix.json', newbook),
                 ('engine/rl_after/s4_matrix.json.srcmd5', os.path.join(SRC, 's4_matrix.json.srcmd5'))):
    p = os.path.join(ROOT, rel)
    old = md5(p)
    tail_nl = open(p, 'rb').read().endswith(b'\n')
    shutil.copyfile(src, p)
    # keep the checkout's own trailing-newline convention for the sidecar
    b = open(p, 'rb').read()
    if not tail_nl and b.endswith(b'\n'):
        open(p, 'wb').write(b.rstrip(b'\n'))
    elif tail_nl and not b.endswith(b'\n'):
        open(p, 'ab').write(b'\n')
    print("%-42s %s -> %s" % (rel, old, md5(p)))
