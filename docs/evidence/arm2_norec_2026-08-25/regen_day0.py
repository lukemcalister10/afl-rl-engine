#!/usr/bin/env python3
"""DAY-0 FINAL regeneration for the NOREC candidate (the 31-F emitter's RL_DAY0_FINAL input).

WHY: the emitter's default day-0 file is STALE (board fe6be9d6, 89 rows; the fade clock and board
have moved) — the register's queued repair, hit live. The guard's PURPOSE is to prove the emitter's
arithmetic against THE BOARD'S OWN PUBLISHED day-0 prices, so the regeneration takes `printed`
FROM THE CANDIDATE BOARD (independent of the emitter) and `derived_v0` from the engine's own v0
artifact through the accessor CARRIED from the filed emitter (run-time slice, md5 printed — the
arm2_noarb_class carry pattern). The identity printed == round(derived_v0 * D) is ASSERTED here
against the published board; any failure HALTS (it would be real incoherence, not staleness)."""
import contextlib, hashlib, io, json, os, sys

os.environ.setdefault('RL_CONFIG_MODE', 'gate')
REPO = os.environ['RL_REPO']
sys.path.insert(0, REPO)
import config_manifest
config_manifest.enforce('gate')
G = {'__name__': '_day0_regen'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
MA = G['MA']

EMITTER = os.path.join(REPO, 'docs/evidence/candidate_31f/emit_matrix_31f.py')
src = open(EMITTER).read()
lines = src.splitlines(True)
def carve(startpat, endpat):
    i = next(n for n, l in enumerate(lines) if startpat in l)
    j = next(n for n, l in enumerate(lines[i:], i) if endpat in l)
    return ''.join(lines[i:j + 1])
slice1 = carve("_PL_F = G['_PL_F']", "_POSV = {")            # _PL_F/_V2J/_POSV setup
def carve_to_next_def(startpat, nextpat):
    i = next(n for n, l in enumerate(lines) if startpat in l)
    j = next(n for n, l in enumerate(lines[i+1:], i+1) if nextpat in l)
    return ''.join(lines[i:j])
slice2 = carve_to_next_def('def _landed_v0_board', 'def _landed_v0_engine')  # the WHOLE accessor, verbatim
print('carried emitter md5:', hashlib.md5(src.encode()).hexdigest()[:12])
print('slice1 md5:', hashlib.md5(slice1.encode()).hexdigest()[:12],
      '| slice2 md5:', hashlib.md5(slice2.encode()).hexdigest()[:12])
NS = {'G': G, 'MA': MA}
exec(slice1, NS)
exec(slice2, NS)
_landed_v0_board = NS['_landed_v0_board']
o31_D = G['o31_D']
e29b = G['_entry29b_derived']

board_path = sys.argv[1]
out_path = sys.argv[2]
board = json.load(open(board_path))
bv = {r['key']: r['v'] for r in board['active']}
bmd5 = hashlib.md5(open(board_path, 'rb').read()).hexdigest()

rows, bad = [], []
for p in MA.data:
    if e29b(p, MA.BASE_REF) is None:
        continue
    mb = _landed_v0_board(p)
    if mb is None:
        bad.append((p.get('key'), 'no landed v0')); continue
    pr = int(round(mb * float(o31_D(p, MA.BASE_REF))))
    pub = bv.get(p.get('key'))
    if pub != pr:
        bad.append((p.get('key'), 'identity fails: computed %s vs published %s' % (pr, pub))); continue
    rows.append({'key': p.get('key'), 'printed': pub, 'derived_v0': mb})
if bad:
    raise SystemExit('DAY0 REGEN HALT: %d rows fail the published-board identity: %s' % (len(bad), bad[:6]))
out = {'base_ref': MA.BASE_REF, 'board': 'NOREC candidate (recency-less arm 2)',
       'board_md5': bmd5, 'label': 'regenerated day-0 final for the NOREC candidate board',
       'entry_year_note': 'printed taken FROM the published board; identity round(derived_v0*D)==printed asserted here',
       'identity_all': '%d of %d at tolerance 0' % (len(rows), len(rows)),
       'rows': rows}
json.dump(out, open(out_path, 'w'), indent=1)
print('wrote %s: %d rows, board %s, identity all-pass' % (out_path, len(rows), bmd5[:8]))
