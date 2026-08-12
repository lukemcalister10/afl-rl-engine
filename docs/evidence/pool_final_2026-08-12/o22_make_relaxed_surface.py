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

SECOND OWNER DIRECTION, same hour (#334 comment 5262213139), folded into THE SAME regeneration:
the class x depth cells gain n/(n+10) partial pooling toward the ALL-CLASS same-depth whole-pool cell.
The declared order of operations is written into substitution 3 below and printed by the run.

THIS FILE DOES NOT MODIFY ORDER 21's INSTRUMENT. `pool_retention_derive.py` is filed evidence of a
landed act. This file READS it, applies the textual substitutions listed in SUBS -- each printed with
its anchor so the change is auditable to the character -- writes the result to the SCRATCHPAD, and
runs the copy there. Nothing under docs/evidence/pool_retention_2026-08-12/ is written.

A FAULT THIS SEAT MADE AND FIXED, RECORDED RATHER THAN QUIETLY REPAIRED: the first version of this
file redirected the surface JSON but NOT the run transcript, and ORDER 21's committed
`pool_retention_derive_out.txt` was overwritten in the working tree. `git status` caught it, the file
was restored from HEAD (md5 501878a962b0baff9fbee3ff5a4f12c0), and substitution 2c now redirects the
transcript too.

CONTROLS: the relaxed surface's DEPTH-1 row is compared against ORDER 21's at every one of the 30
wired vectors and EVERY difference is printed. Amendment 1 alone cannot move depth 1 (index 0 is
never projected); AMENDMENT 2 CAN, because the class-axis shrink applies at every depth -- so a
depth-1 move is a reported consequence of the second ruling, not a control failure.

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
    # 1b -- AMENDMENT 2: the class-axis K=10 shrink, inserted between the kernel and the clip
    ("""for cls in CLASSES:
    raw, meta = [], []
    for dd in DEPTHS:
        m, bwd, en, n, thin = rsit_at(SIT[cls], dd)
        nm = NORM[(cls, dd)][0]
        R = m / nm if (nm == nm and nm > 0) else m
        R = float(min(max(R, 0.05), 1.0))
        raw.append(R)
        meta.append(dict(bwd=bwd, effn=round(en, 1), n_exact=sum(1 for c in SIT[cls] if c['d'] == dd),
                         thin=thin, norm=round(nm, 4), rsit=round(m, 4)))
    iso = isotonic_noninc(raw)""",
     """# ===== ORDER 22 AMENDMENT 2 -- owner direction 2026-08-12 (#334 comment 5262213139) ==============
# "O1 - potentially we apply the K thing again to the KPP cells if there isn't much of a sample? The
#  bigger the sample, the more it speaks to itself, the smaller the sample, the more it pulls towards
#  the pooled pool."
# The class x depth cell is partially pooled toward the ALL-CLASS same-depth whole-pool cell at K=10,
# the same within-group borrowing constant the pathway layer already uses (K_336 / K_338).
# THE ORDER OF OPERATIONS, DECLARED SO IT IS REPRODUCIBLE:
#   kernel-smooth raw (depth axis only)
#     -> class-axis K=10 shrink toward the all-class same-depth cell   [AMENDMENT 2]
#     -> clip [0.05, 1.0]                                              [unchanged -- a sitter is never
#                                                                       priced above his entry anchor]
#     -> NO isotonic step at depths >= 2                               [AMENDMENT 1]
#     -> pathway layer K=10 borrowing, now borrowing from the SHRUNK whole-pool class cells.
# The weight uses the RAW EXACT-DEPTH sit-out n, recomputed from the harvest, never transcribed.
K_CLASS = 10.0
NORM_ALL = {}
for dd in DEPTHS:
    _v = [wins(c['O'] / max(1e-9, c['Vanchor'])) for c in WC
          if c['d'] == dd and c['Vanchor'] == c['Vanchor'] and c['Vanchor'] > 0]
    NORM_ALL[dd] = (float(np.mean(_v)) if _v else float('nan'), len(_v))
ALLCELL, ALLMETA = {}, {}
for dd in DEPTHS:
    _m, _bwd, _en, _n, _thin = rsit_at(SITWC, dd)
    _nm = NORM_ALL[dd][0]
    ALLCELL[dd] = float(_m / _nm) if (_nm == _nm and _nm > 0) else float(_m)
    ALLMETA[dd] = dict(bwd=_bwd, effn=round(_en, 1), norm=round(_nm, 4), rsit=round(_m, 4),
                       n_exact=sum(1 for c in SITWC if c['d'] == dd))
CLASSSHRINK = []
for cls in CLASSES:
    raw, meta = [], []
    for dd in DEPTHS:
        m, bwd, en, n, thin = rsit_at(SIT[cls], dd)
        nm = NORM[(cls, dd)][0]
        R_own = m / nm if (nm == nm and nm > 0) else m
        n_ex = sum(1 for c in SIT[cls] if c['d'] == dd)
        w_cls = n_ex / (n_ex + K_CLASS)
        R = w_cls * R_own + (1.0 - w_cls) * ALLCELL[dd]
        R = float(min(max(R, 0.05), 1.0))
        CLASSSHRINK.append(dict(cls=cls, d=dd, n=n_ex, w=round(w_cls, 4), own=round(R_own, 4),
                                donor=round(ALLCELL[dd], 4), wired=round(R, 4)))
        raw.append(R)
        meta.append(dict(bwd=bwd, effn=round(en, 1), n_exact=n_ex,
                         thin=thin, norm=round(nm, 4), rsit=round(m, 4),
                         class_shrink_w=round(w_cls, 4), class_own=round(R_own, 4),
                         class_donor=round(ALLCELL[dd], 4)))
    iso = isotonic_noninc(raw)"""),
    # 1c -- disclose every shrunk class cell
    ("""P("  exact-depth sit-out cell counts (the derivation's own n, before the depth kernel):")""",
     """P("  ORDER 22 AMENDMENT 2 -- CLASS-AXIS K=%g SHRINKAGE TOWARD THE ALL-CLASS SAME-DEPTH CELL" % K_CLASS)
P("  (every cell disclosed: its own kernel value, the pooled donor, the weight, and what was wired)")
P("    all-class pooled cell by depth: %s"
  % "  ".join("d%d=%.4f (n=%d, bw=%.2f, effn=%.0f)"
              % (d, ALLCELL[d], ALLMETA[d]['n_exact'], ALLMETA[d]['bwd'], ALLMETA[d]['effn'])
              for d in DEPTHS))
P("    %-8s %-4s %7s %9s %10s %10s %10s" % ('class', 'd', 'n', 'w=n/(n+10)', 'own', 'donor', 'WIRED'))
for _r in CLASSSHRINK:
    P("    %-8s d%-3d %7d %9.4f %10.4f %10.4f %10.4f"
      % (_r['cls'], _r['d'], _r['n'], _r['w'], _r['own'], _r['donor'], _r['wired']))
P()
P("  exact-depth sit-out cell counts (the derivation's own n, before the depth kernel):")"""),
    # 1d -- carry the disclosure into the surface JSON
    ("    o1_floored_kpp=[round(x, 6) for x in kfl],",
     "    o1_floored_kpp=[round(x, 6) for x in kfl],\n"
     "    class_shrink=CLASSSHRINK, all_class_cell={str(d): ALLCELL[d] for d in DEPTHS},\n"
     "    all_class_meta={str(d): ALLMETA[d] for d in DEPTHS}, K_class=K_CLASS,\n"
     "    o22_amendments=['isotonic relaxed at depths >= 2 (5262159933)',\n"
     "                    'class-axis K=10 shrink toward the all-class same-depth cell (5262213139)'],"),
    # 2a -- the whole-pool assert
    ('assert all(viol(POOLSURF[cls]) == 0 for cls in CLASSES), "isotonic projection failed"',
     'P("  ORDER 22 AMENDMENT: the non-increasing law is RELAXED at depths >= 2 by owner ruling; "\n'
     '  "raw violations are now the WIRED values and are disclosed, not projected away.")'),
    # 2b -- the pathway assert
    ('assert all(viol(PATHSURF[pw][cls]) == 0 for pw in PATHS for cls in CLASSES), "pathway isotonic failed"',
     'P("  ORDER 22 AMENDMENT: pathway vectors carry their raw depth>=2 values (owner ruling).")'),
    # 2c -- THE OUTPUT TRANSCRIPT GOES TO THE SCRATCHPAD, NEVER OVER ORDER 21's FILED EVIDENCE.
    #       (Caught by `git status` on the first run: the script writes its transcript beside itself,
    #       and `HERE` points at the filed directory. Reported here rather than quietly fixed.)
    ("""with open(os.path.join(HERE, 'pool_retention_derive_out.txt'), 'w') as f:""",
     """with open(os.environ['RL_O22_TRANSCRIPT_OUT'], 'w') as f:"""),
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
           RL_O22_ORIG_HERE=os.path.dirname(SRC), RL_O22_ORIG_ROOT=ROOT,
           RL_O22_TRANSCRIPT_OUT=WORK + '/relaxed_derive_transcript.txt')
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
print("  DEPTH-1 vs ORDER 21: %d of %d wired vectors move." % (len(bad), 3 + 3 * len(OLD['pathway'])))
print("  Amendment 1 alone leaves depth 1 untouched (index 0 is never projected). AMENDMENT 2 DOES")
print("  MOVE IT -- the class-axis K=10 shrink applies at every depth including depth 1 -- so this is")
print("  a REPORTED CONSEQUENCE of the second ruling, not a control failure. Every move is printed:")
for b in bad:
    print("    %-10s %-7s  %.6f -> %.6f  (%+.2f%%)" % (b[0], b[1], b[2], b[3], 100.0*(b[3]/b[2]-1)))
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
