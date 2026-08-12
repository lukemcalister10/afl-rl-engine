"""Assert the scratchpad copy carries the landed pins, so the book is sealed against the right board."""
import sys, os, json, hashlib
WT = sys.argv[1]
sys.path.insert(0, WT)
os.environ['RL_REPO'] = WT
import fv_provenance as F
e = json.load(open(os.path.join(WT, 'data/expected_boot.json')))
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
checks = [
    ('board(rl_build)', md5(os.path.join(WT, 'data/rl_build/rl_app_data.json')), e['board']),
    ('board(working)', md5(os.path.join(WT, 'engine/rl_after/rl_app_data.json')), e['board']),
    ('store', md5(os.path.join(WT, 'engine/rl_after/rl_model_data.json')), e['store']),
    ('fv', F.fv_identity(os.path.join(WT, 'engine/forward_valuation')), e['fv']),
]
bad = [c for c in checks if c[1] != c[2]]
for n, g, x in checks:
    print("   %-18s %s %s" % (n, g[:16], "OK" if g == x else "*** != %s ***" % x[:16]))
assert e['board'] == '665311ca72576df6ff0bbf6dfd007739', "copy does not carry ORDER 23's landed board"
sys.exit(1 if bad else 0)
