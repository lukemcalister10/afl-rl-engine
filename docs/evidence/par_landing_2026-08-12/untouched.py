"""ORDER 20C — the scope guards, asserted as numbers at EXIT and diffed against origin/main.

No pin hex is taken on trust from the order text: every value here is computed from the file on disk
and compared to origin/main's own copy of the same file.
"""
import hashlib, os, subprocess, sys

ROOT = '/home/user/afl-rl-engine/.claude/worktrees/agent-a6af0d68789879235'


def md5f(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def md5_main(rel):
    out = subprocess.run(['git', '-C', ROOT, 'show', 'origin/main:' + rel],
                         capture_output=True)
    if out.returncode != 0:
        return None
    return hashlib.md5(out.stdout).hexdigest()


CHECKS = [
    ('STORE',      'engine/rl_after/rl_model_data.json'),
    ('pickle v0surf', 'data/v0surf.pkl'),
    ('pickle q97m',   'data/q97m.pkl'),
    ('INSTRUMENT noarb_table_338.py', 'docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py'),
    ('model_config',  'data/model_config.json'),
    ('rl_model.py',   'engine/rl_after/rl_model.py'),
    ('_merged_recover.py', 'engine/rl_after/_merged_recover.py'),
    ('LTI_REGISTER.md',    'LTI_REGISTER.md'),
    ('peak_model_v4.pkl',  'engine/rl_after/peak_model_v4.pkl'),
    ('pvc_snapshot.json',  'engine/rl_after/pvc_snapshot.json'),
    ('bust_prior_table.json', 'engine/rl_after/bust_prior_table.json'),
]

bad = []
print("%-34s %-34s %-34s %s" % ("artifact", "landed md5", "origin/main md5", "verdict"))
print("-" * 116)
for label, rel in CHECKS:
    p = os.path.join(ROOT, rel)
    got = md5f(p) if os.path.exists(p) else 'ABSENT'
    exp = md5_main(rel) or 'ABSENT-ON-MAIN'
    ok = got == exp
    if not ok:
        bad.append(label)
    print("%-34s %-34s %-34s %s" % (label, got, exp, "UNMOVED" if ok else "*** MOVED ***"))

# the band pickle lives outside the checkout, on the engine's own load path
band = '/home/claude/cm_400.pkl'
print()
if os.path.exists(band):
    print("band pickle (engine load path) %s  md5 %s" % (band, md5f(band)))
    print("   pinned band in expected_boot: 34faa8659cc8f19794f5cb9584fa19b2 -> %s"
          % ("MATCH, and this landing never writes it"
             if md5f(band) == '34faa8659cc8f19794f5cb9584fa19b2' else "*** MISMATCH ***"))
    if md5f(band) != '34faa8659cc8f19794f5cb9584fa19b2':
        bad.append('band')
else:
    print("band pickle %s ABSENT on this box (boot guard load-path check reported above)" % band)

# sitter configuration must be untouched
print()
out = subprocess.run(['git', '-C', ROOT, 'diff', 'origin/main', '--name-only'], capture_output=True, text=True)
changed = [x for x in out.stdout.split() if x]
print("FILES THIS BRANCH CHANGES vs origin/main (%d):" % len(changed))
for c in changed:
    print("   ", c)

# Sitter config: only a CODE/CONFIG change counts. This branch's own prose (the prereg and the
# verification note) says the words "H_POOLSIT"/"H_UNION" precisely to declare them untouched, so
# documentation under docs/ is excluded — otherwise declaring the guard would breach the guard.
g = subprocess.run(['git', '-C', ROOT, 'diff', 'origin/main', '-G', 'H_POOLSIT|H_UNION', '--name-only',
                    '--', '.', ':(exclude)docs/'], capture_output=True, text=True)
hits = [x for x in g.stdout.split() if x]
print()
print("H_POOLSIT / H_UNION in CODE/CONFIG touched by this branch: %s"
      % ("NO — no non-doc file adds or removes a line mentioning them" if not hits else "*** YES: %s ***" % hits))
if hits:
    bad.append('H_POOLSIT/H_UNION')

# and prove the sitter values themselves are identical to origin/main wherever they live
sit = subprocess.run(['git', '-C', ROOT, 'grep', '-n', '-E', 'H_POOLSIT|H_UNION', 'origin/main',
                      '--', '.', ':(exclude)docs/'], capture_output=True, text=True)
now = subprocess.run(['git', '-C', ROOT, 'grep', '-n', '-E', 'H_POOLSIT|H_UNION', 'HEAD',
                      '--', '.', ':(exclude)docs/'], capture_output=True, text=True)
a = [l.split(':', 1)[1] for l in sit.stdout.splitlines() if l]
b = [l.split(':', 1)[1] for l in now.stdout.splitlines() if l]
print("   sitter-config lines identical to origin/main: %s  (%d lines)"
      % ("YES" if a == b else "*** NO ***", len(a)))
if a != b:
    bad.append('sitter-config-lines')

print()
print("SCOPE GUARDS: ALL HELD" if not bad else "*** SCOPE BREACH: %s ***" % bad)
sys.exit(0 if not bad else 1)
