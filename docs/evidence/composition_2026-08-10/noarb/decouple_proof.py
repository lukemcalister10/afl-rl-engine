"""PROOF that the ramp de-couple (RL_A_GSAT) leaves sitout_ev BYTE-UNCHANGED.

The spec names one trap: sitout_ev and _a_share read the SAME LAM_SIT ramp for two different jobs, so
an edit that re-points "the ramp" moves the whole sit-out population as a side effect. This proves the
edit did not, two independent ways.

  STATIC  every textual occurrence of the dial is located and shown to sit inside _a_share (or its
          comment block) and nowhere else -- in particular not inside sitout_ev.
  DYNAMIC sitout_ev is evaluated over the WHOLE real population x an as-of year set x an e_full grid,
          and the full result vector is hashed. The hash is printed. Run the file twice, once with
          RL_A_GSAT=0 and once with RL_A_GSAT=18, and the two hashes must be identical.
          _a_share is hashed the same way in the same pass, and those two hashes must DIFFER -- so the
          proof is non-vacuous: it can tell "the dial did nothing anywhere" apart from "the dial did
          something, but not here".

  usage:  RL_A_GSAT=<v> OPENBLAS_NUM_THREADS=1 python decouple_proof.py
          (gate mode requires the manifest value to match the environment; use probe_arm.sh's pattern)
"""
import sys, os, io, re, json, hashlib, contextlib
sys.path.insert(0, '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10')

SRC = '/home/user/afl-rl-engine/engine/rl_after/_merged_recover.py'
lines = open(SRC).read().split('\n')
hits = [(i+1, l) for i, l in enumerate(lines) if '_A_GSAT' in l or 'RL_A_GSAT' in l]
print("=== STATIC: every occurrence of the dial in _merged_recover.py ===")
# locate the enclosing def for each hit
def enclosing_def(n):
    # a statement at column 0 is MODULE SCOPE, whatever def precedes it in the file
    if lines[n-1][:1] not in (' ', '\t'): return '<module scope>'
    for j in range(n-1, -1, -1):
        m = re.match(r'^def (\w+)', lines[j])
        if m: return m.group(1)
    return '<module scope>'
for n, l in hits:
    print(f"  :{n:5}  in {enclosing_def(n):12}  {l.strip()[:90]}")
bad = [ (n, enclosing_def(n)) for n, l in hits
        if not l.lstrip().startswith('#') and enclosing_def(n) not in ('_a_share', '<module scope>') ]
print("  READS OUTSIDE _a_share (must be empty):", bad)
sit0 = next(i for i, l in enumerate(lines) if l.startswith('def sitout_ev'))
sit1 = next(i for i in range(sit0+1, len(lines)) if lines[i].startswith('def ') or lines[i].startswith('# ====='))
print("  sitout_ev body :%d-%d contains the dial:" % (sit0+1, sit1),
      any('A_GSAT' in l for l in lines[sit0:sit1]))
print("  sitout_ev body lam line:", next(l.strip() for l in lines[sit0:sit1] if 'lam=' in l)[:110])

import engine_load
g = engine_load.load()
MA = g['MA']; sitout_ev = g['sitout_ev']; _a_share = g['_a_share']
print("\n=== DYNAMIC: RL_A_GSAT =", os.environ.get('RL_A_GSAT', '<unset>'), " _A_GSAT =", g['_A_GSAT'], "===")

def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = sorted([p for p in MA.data if eligible(p)], key=lambda p: (p.get('key') or '', p.get('year') or 0))
YEARS = (2022, 2025, 2026)
EF = (250.0, 3000.0)
hs, ha = hashlib.md5(), hashlib.md5()
ns = na = 0
for p in players:
    for Y in YEARS:
        for e in EF:
            try:
                with contextlib.redirect_stdout(io.StringIO()): v = sitout_ev(p, Y, e)
                hs.update(('%s|%d|%.1f|%.12g\n' % (p.get('key'), Y, e, v)).encode()); ns += 1
            except Exception as ex:
                hs.update(('%s|%d|%.1f|ERR%s\n' % (p.get('key'), Y, e, type(ex).__name__)).encode())
        try:
            with contextlib.redirect_stdout(io.StringIO()): a = _a_share(p, Y)
            ha.update(('%s|%d|%.12g\n' % (p.get('key'), Y, a)).encode()); na += 1
        except Exception as ex:
            ha.update(('%s|%d|ERR%s\n' % (p.get('key'), Y, type(ex).__name__)).encode())
print(f"  players {len(players)}  x years {len(YEARS)}  x e_full {len(EF)}")
print(f"  sitout_ev  evaluations {ns}   MD5 {hs.hexdigest()}")
print(f"  _a_share   evaluations {na}   MD5 {ha.hexdigest()}")
print("  VERDICT INPUT: sitout_ev md5 must MATCH across the two dial settings;"
      " _a_share md5 must DIFFER (non-vacuity).")
