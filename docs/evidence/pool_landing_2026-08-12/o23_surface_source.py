#!/usr/bin/env python3
"""ORDER 23 -- WIRE THE DERIVED RETENTION SURFACE AS A **SOURCE**, NOT A DIAL.

  usage: o23_surface_source.py <tree> <surface.json>

Run AFTER docs/evidence/pool_final_2026-08-12/o21_patch.py (which is CARRIED VERBATIM and is what
inlines the surface's numbers into engine/rl_after/_merged_recover.py). This script does the two
things that turn that staging mechanism into a landed one:

  1. COMMITS THE SURFACE ITSELF as engine/rl_after/pool_retention_surface.json -- the signed data
     artifact it now is, sitting beside pvc_curve_v2.json, which is where this repo keeps signed
     numbers that the engine reads.
  2. REWRITES THE INJECTED BLOCK'S HEADER so it names that artifact, its md5, and the derivation
     provenance -- so a reader of the engine never has to guess where the literals came from, and a
     drift between the artifact and the inlined literals is a one-command check rather than a hunt.

The literals stay inlined. That is deliberate: it is the mechanism every measuring act since ORDER 21
has used, so the landed engine is byte-for-byte the engine that was measured, and no new file-read
path is introduced into the board build on the day the numbers land.
"""
import sys, json, pathlib, hashlib

TREE, SURF = sys.argv[1], sys.argv[2]

blob = pathlib.Path(SURF).read_bytes()
dst = pathlib.Path(TREE + '/engine/rl_after/pool_retention_surface.json')
dst.write_bytes(blob)
SMD5 = hashlib.md5(blob).hexdigest()

S = json.load(open(SURF))
npath = len(S['pathway'])
ncls = len(S['whole_pool'])

f = pathlib.Path(TREE + '/engine/rl_after/_merged_recover.py')
src = f.read_text()

OLD = "# ===== ORDER 21 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL HISTORY (STAGED; NOT LANDED) ========\n"
NEW = (
    "# ===== #334 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL HISTORY. LANDED BY ORDER 23. ============\n"
    "# THE SOURCE OF THESE NUMBERS IS A COMMITTED SIGNED DATA ARTIFACT -- not a dial, not a constant a\n"
    "# seat typed, and not something a rebuild can quietly re-fit:\n"
    "#     engine/rl_after/pool_retention_surface.json   md5 %s\n"
    "#     %d pathway surfaces x %d classes x 6 depths, plus the mean-preserving uplift U per pathway.\n"
    "# DERIVATION PROVENANCE: docs/evidence/pool_retention_2026-08-12/pool_retention_derive.py (ORDER 21,\n"
    "# the d13 ND method with departures D1-D7 pre-registered), as amended by ORDER 22's\n"
    "# o22_make_relaxed_surface.py under two owner rulings of 2026-08-12 -- the isotonic constraint\n"
    "# RELAXED at depths >= 2 (comment 5262159933) and a class-axis K=10 shrinkage toward the all-class\n"
    "# same-depth cell (comment 5262213139) -- with U re-derived, entry-weighted and mean-preserving to\n"
    "# 1.0000000000 exactly, at ORDER 23's final levels. Verification: docs/evidence/pool_landing_2026-08-12/.\n"
    "# The literals below are that artifact inlined by docs/evidence/pool_final_2026-08-12/o21_patch.py,\n"
    "# which is the mechanism every measuring act since ORDER 21 has used; ORDER 23 makes it permanent, so\n"
    "# the landed engine is byte-for-byte the engine the packet's numbers were measured on.\n"
    % (SMD5, npath, ncls))
assert src.count(OLD) == 1, "the ORDER 21 block header is not where it was (%d)" % src.count(OLD)
src = src.replace(OLD, NEW)
f.write_text(src)
print("  [S] retention surface WIRED AS SOURCE: engine/rl_after/pool_retention_surface.json md5 %s" % SMD5)
print("      _merged_recover.py md5 -> %s" % hashlib.md5(f.read_bytes()).hexdigest())
