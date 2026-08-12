"""ORDER 20B TASK 4 — THE PAR SURFACE'S PER-CELL DIRECTION, ON THE RECORD.

For each named mover: his own par cells (position x pick x tenure 1..6), HEAD vs FIX, and the
decomposition of each cell's move into the two legs par_at is built from:

    par_at(pos, pick, T)  =  level_at(pos, pick)  +  ramp_shr[pos][T]
                             \_ THE PICK AXIS _/     \_ NO PICK AXIS _/

so "did this move come through the pick axis or not" is answered per cell rather than argued. Note
ramp_shr is re-anchored to 0 at T=1 (par_build.py:568), so for any TENURE-1 player the no-pick-axis
leg contributes EXACTLY ZERO by construction.

Also prints the whole level-only curve per position across pick 1..70, which is what settles whether a
shallow-pick move is a kernel reach from index 65 or a shift of the level surface as a whole.

Run: python3 par_cells.py <probe_HEAD> <probe_FIX> <out_prefix>
"""
import json, sys

H = json.load(open(sys.argv[1])); X = json.load(open(sys.argv[2])); PRE = sys.argv[3]
A, B = H['par_cells'], X['par_cells']
RA, RB = H['ramp_shr'], X['ramp_shr']
P = print
OUT = {}

MOVERS = [('Harry Dean', 'KPD', 3, 1), ('Angus Clarke', 'SD', 39, 2), ('Harvey Johnston', 'SD', 49, 3),
          ('James Leake', 'SD', 17, 3), ('Willem Duursma', 'MID', 1, 1), ('Will Hayes', 'SF', 56, 2),
          ('Luke Cleary', 'SD', 61, 5)]
GROUPS = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']

P("=" * 122)
P("ORDER 20B — THE PAR SURFACE PER-CELL, HEAD vs FIX   (instrument: engine_probe.py par_cells, PR.par_at)")
P("=" * 122)
P()
P("  ---- each mover's own cells, tenure 1..6 (value HEAD -> FIX) ----")
P("    %-17s %-5s %4s | %s" % ('name', 'pos', 'pick', ' '.join('%15s' % ('T%d' % T) for T in range(1, 7))))
for nm, pos, pk, _t in MOVERS:
    cells = ['%6.2f->%6.2f' % (A['%s|%d|%d' % (pos, pk, T)], B['%s|%d|%d' % (pos, pk, T)]) for T in range(1, 7)]
    P("    %-17s %-5s %4d | %s" % (nm, pos, pk, ' '.join('%15s' % c for c in cells)))
P()
P("    %-17s %-5s %4s | %s   <- PERCENT CHANGE" % ('name', 'pos', 'pick', ' '.join('%15s' % ('T%d' % T) for T in range(1, 7))))
for nm, pos, pk, _t in MOVERS:
    cells = ['%+.2f%%' % (100.0 * (B['%s|%d|%d' % (pos, pk, T)] / A['%s|%d|%d' % (pos, pk, T)] - 1)) for T in range(1, 7)]
    P("    %-17s %-5s %4d | %s" % (nm, pos, pk, ' '.join('%15s' % c for c in cells)))

P()
P("  ---- HIS OWN CELL (the tenure the engine reads for him), split into the two legs ----")
P("    %-17s %-5s %4s %3s | %9s %9s %9s | %9s %9s | %s"
  % ('name', 'pos', 'pick', 'T', 'par HEAD', 'par FIX', 'd par', 'd LEVEL', 'd RAMP', 'note'))
OUT['cells'] = {}
for nm, pos, pk, T in MOVERS:
    a = A['%s|%d|%d' % (pos, pk, T)]; b = B['%s|%d|%d' % (pos, pk, T)]
    ra = RA[pos][T]; rb = RB[pos][T]
    dL = (b - rb) - (a - ra); dR = rb - ra; dP = b - a
    note = 'T=1: ramp leg is 0 BY CONSTRUCTION' if T == 1 else ''
    P("    %-17s %-5s %4d %3d | %9.3f %9.3f %+9.3f | %+9.3f %+9.3f | %s"
      % (nm, pos, pk, T, a, b, dP, dL, dR, note))
    OUT['cells'][nm] = {'pos': pos, 'pick': pk, 'tenure': T, 'par_head': a, 'par_fix': b,
                        'd_par': dP, 'd_level': dL, 'd_ramp': dR,
                        'pct': 100.0 * (b - a) / a}

P()
P("  ---- ramp_shr[pos][T] — the NO-PICK-AXIS leg ----")
P("    %-6s | %s" % ('pos', ' '.join('%17s' % ('T%d' % T) for T in range(1, 7))))
for g in GROUPS:
    P("    %-6s | %s" % (g, ' '.join('%17s' % ('%6.3f->%6.3f' % (RA[g][T], RB[g][T])) for T in range(1, 7))))
OUT['ramp_shr'] = {g: {'head': RA[g], 'fix': RB[g]} for g in GROUPS}

P()
P("  ---- THE LEVEL-ONLY CURVE (par at T=1 minus ramp_shr[1]), percent change across pick ----")
P("       picks 65-70 are the POOL arm under the fix (MA.POOL_PICK=65, cp.KMAX=70)")
PK = [1, 2, 3, 5, 8, 10, 15, 17, 20, 25, 30, 35, 39, 45, 49, 53, 56, 60, 61, 64, 65, 70]
P("    %-6s %s" % ('pos', ' '.join('%7s' % ('pk%d' % p) for p in PK)))
OUT['level_curve_pct'] = {}
for g in GROUPS:
    row = []
    for pk in PK:
        a = A['%s|%d|1' % (g, pk)] - RA[g][1]; b = B['%s|%d|1' % (g, pk)] - RB[g][1]
        row.append(100.0 * (b - a) / a)
    OUT['level_curve_pct'][g] = dict(zip(map(str, PK), row))
    P("    %-6s %s" % (g, ' '.join('%+6.2f%%' % v for v in row)))

P()
P("  ---- SD picks 25-49 are ONE FLAT CELL: Clarke (39) and Johnston (49) read the SAME level ----")
for pk in (25, 30, 35, 39, 42, 45, 49):
    P("      SD pk%-3d level %8.4f -> %8.4f" % (pk, A['SD|%d|1' % pk] - RA['SD'][1], B['SD|%d|1' % pk] - RB['SD'][1]))

json.dump(OUT, open(PRE + '.json', 'w'), indent=1)
P()
P("  json -> %s.json" % PRE)
