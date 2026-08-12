#!/usr/bin/env python3
"""ORDER 24 -- STAGE A DIALLED RETENTION SURFACE INTO A BUILD WORKTREE.

Sibling of docs/evidence/pool_landing_2026-08-12/o23_surface_source.py, but for a branch where the
surface is ALREADY LANDED as engine literals: instead of injecting a block, this REPLACES the four
literal assignments in the staged worktree's `_merged_recover.py` and rewrites the source artifact
beside them, so the built board's engine identity records exactly the surface that produced it.

THE CHECKOUT IS NEVER WRITTEN -- this only ever edits the throwaway worktree it is handed.

  usage: o24_stage_surface.py <worktree> <surface.json>
"""
import sys, json, pathlib, hashlib, re

wt, surf_path = sys.argv[1], sys.argv[2]
S = json.load(open(surf_path))
alpha = S.get('_ORDER24_alpha')
assert alpha is not None, "surface carries no _ORDER24_alpha -- refusing to stage an unlabelled surface"

f = pathlib.Path(wt + '/engine/rl_after/_merged_recover.py')
src = f.read_text()

REPL = [('_PR_PATH=', json.dumps(S['pathway'])),
        ('_PR_WHOLE=', json.dumps(S['whole_pool'])),
        ('_PR_U=', json.dumps(S['uplift'])),
        ('_PR_U_ALL=', repr(float(S['mean_preserving']['ALL POOL']['U'])))]
# ORDER 24B: the par table travels with the surface, so the built board's engine identity records
# exactly the par that produced it. A surface with no `par` block stages nothing new and the engine's
# committed par literals stand -- so an ORDER 24 alpha surface still stages correctly.
if 'par' in S:
    REPL += [('_PR_PAR=', json.dumps(S['par'])),
             ('_PR_PAR_ALL=', json.dumps(S['par_all']))]
for key, val in REPL:
    pat = re.compile(r'^' + re.escape(key) + r'.*$', re.M)
    n = len(pat.findall(src))
    assert n == 1, "anchor %r is not unique in the staged engine (%d matches)" % (key, n)
    src = pat.sub(lambda _m: key + val, src, count=1)

# the source artifact beside the literals, and the md5 the block header quotes
art = pathlib.Path(wt + '/engine/rl_after/pool_retention_surface.json')
art.write_text(json.dumps(S, indent=1, default=float))
newmd5 = hashlib.md5(art.read_bytes()).hexdigest()
src = re.sub(r'(engine/rl_after/pool_retention_surface\.json\s+md5 )[0-9a-f]{32}',
             lambda m: m.group(1) + newmd5, src, count=1)
f.write_text(src)
print("  STAGED surface alpha=%s  U'=%s" % (alpha, {k: round(v, 6) for k, v in S['uplift'].items()}))
print("  surface artifact md5 -> %s" % newmd5)
