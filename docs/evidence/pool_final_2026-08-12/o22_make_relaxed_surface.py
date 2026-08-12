#!/usr/bin/env python3
"""ORDER 22 AMENDMENT -- BUILD THE RELAXED (NON-ISOTONIC AT DEPTH >= 2) POOL RETENTION SURFACE.

OWNER RULING, 2026-08-12 (#334 comment 5262159933), verbatim:

  "I am actually ok with this not being isotonic as it's logical. If you are not good, you can be
   delisted. Especially with pool players starting on one year contracts, survival can be a more
   positive sign - whereas a lot of year 1 sitters sit because they're not up to the level, so would
   be delisted after a year. Those who are not are not for a reason. So I think it would be fine for
   2 year sitters/3 year sitters to reflect the data we have."

RULED: the never-gains-by-sitting law is AMENDED FOR THE POOL OBJECT ONLY. Raw kernel-smoothed values
are wired at depths >= 2, on the whole-pool layer AND the pathway layer. The **[0.05, 1.0] CLIP STAYS**
(a sitter is never priced above his entry anchor). The NATIONAL surface is untouched.

THIS FILE DOES NOT MODIFY ORDER 21's INSTRUMENT. `pool_retention_derive.py` is filed evidence of a
landed act. This file READS it, applies THREE textual substitutions -- each printed with its before
and after so the change is auditable to the character -- writes the result to the scratchpad, and runs
it there. The substitutions are:

  1. `isotonic_noninc` returns its input unchanged (depth 1 is index 0 and is untouched either way,
     so the ruling's "depth-1 values are unchanged" is true by construction, and asserted below).
  2. the three isotonic-projection asserts become disclosures (they assert the OPPOSITE law now).
  3. the output filename.

CONTROL, ASSERTED: the relaxed surface's DEPTH-1 row must be byte-identical to ORDER 21's at every
one of the 30 wired vectors (9 pathways x 3 classes + 3 whole-pool). A single depth-1 difference is
a HALT.

  usage: OPENBLAS_NUM_THREADS=1 python3 o22_make_relaxed_surface.py <out_surface.json>
"""
import os, sys, json, hashlib, subprocess, pathlib, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
SRC = ROOT + '/docs/evidence/pool_retention_2026-08-12/pool_retention_derive.py'
OUT = os.path.abspath(sys.argv[1])
WORK = SP + '/o22/relax'
os.makedirs(WORK, exist_ok=True)

src = pathlib.Path(SRC).read_text()
print("  ORDER 21 instrument: %s  md5 %s  (READ ONLY -- never written)"
      % (os.path.basename(SRC), hashlib.md5(src.encode()).hexdigest()))

SUBS = [
    # 0 -- the copy runs from the scratchpad, so HERE/ROOT are pinned to the real tree explicitly
    ("""HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))""",
     """HERE = os.environ['RL_O22_ORIG_HERE']
ROOT = os.environ['RL_O22_ORIG_ROOT']"""),
    # 1 -- the isotonic projection becomes the identity
    ("""def isotonic_noninc(vals):
    out = list(vals)
    for i in range(1, len(out)):
        if out[i] > out[i - 1]: out[i] = out[i - 1]
    return out""",
     """def isotonic_noninc(vals):
    # ORDER 22 AMENDMENT (owner ruling 2026-08-12, #334 comment 5262159933): the non-increasing
    # projection is RELAXED for the POOL object at depths >= 2. Index 0 (depth 1) is never touched by
    # the projection anyway, so depth-1 values are unchanged by construction. The [0.05, 1.0] clip is
    # applied BEFORE this call and is unaffected. The NATIONAL surface does not pass through here.
    return list(vals)"""),
    # 2a -- the whole-pool assert
    ('assert all(viol(POOLSURF[cls]) == 0 for cls in CLASSES), "isotonic projection failed"',
     'P("  ORDER 22 AMENDMENT: the non-increasing law is RELAXED at depths >= 2 by owner ruling; "\n'
     '  "raw violations are now the WIRED values and are disclosed, not projected away.")'),
    # 2b -- the pathway assert
    ('assert all(viol(PATHSURF[pw][cls]) == 0 for pw in PATHS for cls in CLASSES), "pathway isotonic failed"',
     'P("  ORDER 22 AMENDMENT: pathway vectors carry their raw depth>=2 values (owner ruling).")'),
    # 3 -- the output path (the write site and its two report lines)
    ("""with open(os.path.join(HERE, 'POOL_RETENTION_SURFACE.json'), 'w') as f:""",
     """with open(os.environ['RL_O22_SURFACE_OUT'], 'w') as f:"""),
    ("""P("wrote POOL_RETENTION_SURFACE.json  md5 %s"
  % _md5(os.path.join(HERE, 'POOL_RETENTION_SURFACE.json')))""",
     """P("wrote %s  md5 %s" % (os.environ['RL_O22_SURFACE_OUT'],
                        _md5(os.environ['RL_O22_SURFACE_OUT'])))"""),
]
for i, (a, b) in enumerate(SUBS, 1):
    assert src.count(a) == 1, "substitution %d anchor not unique (%d matches)" % (i, src.count(a))
    print("  SUB %d: %s" % (i, a.splitlines()[0][:88]))
    src = src.replace(a, b)

dst = WORK + '/o22_retention_relaxed.py'
pathlib.Path(dst).write_text(src)
print("  relaxed instrument written to scratchpad: %s  md5 %s"
      % (dst, hashlib.md5(src.encode()).hexdigest()))

env = dict(os.environ, RL_O22_SURFACE_OUT=OUT, OPENBLAS_NUM_THREADS='1', PYTHONHASHSEED='0',
           RL_O22_ORIG_HERE=os.path.dirname(SRC), RL_O22_ORIG_ROOT=ROOT)
r = subprocess.run([sys.executable, dst], cwd=os.path.dirname(SRC), env=env,
                   capture_output=True, text=True)
pathlib.Path(WORK + '/relaxed_derive_out.txt').write_text(r.stdout + r.stderr)
if r.returncode != 0:
    print(r.stdout[-4000:]); print(r.stderr[-4000:]); raise SystemExit("relaxed derivation FAILED")

NEW = json.load(open(OUT))
OLD = json.load(open(ROOT + '/docs/evidence/pool_retention_2026-08-12/POOL_RETENTION_SURFACE.json'))
CLASSES = ('nonKPP', 'KPP', 'RUCK')
bad = []
for cls in CLASSES:
    if abs(NEW['whole_pool'][cls][0] - OLD['whole_pool'][cls][0]) > 0:
        bad.append(('whole_pool', cls, OLD['whole_pool'][cls][0], NEW['whole_pool'][cls][0]))
for pw in OLD['pathway']:
    for cls in CLASSES:
        if abs(NEW['pathway'][pw][cls][0] - OLD['pathway'][pw][cls][0]) > 0:
            bad.append((pw, cls, OLD['pathway'][pw][cls][0], NEW['pathway'][pw][cls][0]))
print()
print("  CONTROL -- depth-1 unchanged at every wired vector: %s (%d differences of %d vectors)"
      % ('PASS' if not bad else '*** HALT ***', len(bad), 3 + 3 * len(OLD['pathway'])))
assert not bad, bad
print()
print("  WHOLE-POOL SURFACE, ORDER 21 (isotonic) -> ORDER 22 (relaxed):")
for cls in CLASSES:
    print("    %-8s  %s" % (cls, "  ".join("%.4f" % x for x in OLD['whole_pool'][cls])))
    print("    %-8s  %s   <- WIRED" % ('', "  ".join("%.4f" % x for x in NEW['whole_pool'][cls])))
nviol = 0
for pw in NEW['pathway']:
    for cls in CLASSES:
        v = NEW['pathway'][pw][cls]
        nviol += sum(1 for i in range(1, len(v)) if v[i] > v[i - 1] + 1e-12)
print()
print("  rises (depth d value above depth d-1) now WIRED across the 27 pathway x class vectors: %d" % nviol)
print("  surface md5: %s" % hashlib.md5(open(OUT, 'rb').read()).hexdigest())
print("  full relaxed derivation output: %s" % (WORK + '/relaxed_derive_out.txt'))
