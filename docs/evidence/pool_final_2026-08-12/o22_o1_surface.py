#!/usr/bin/env python3
"""ORDER 22 -- THE O1 VARIANT SURFACE, so the owner rules on real board and instrument numbers.

O1 is the owner's signed override on the NATIONAL surface, board path only:
    KPP := pointwise max(KPP, nonKPP)
Whether it extends to an object derived on POOL data is HIS question, not the seat's. This file
produces the O1-ON surface from the O1-OFF one so both can be BUILT and READ, and prints exactly where
and by how much it binds -- on the whole-pool layer and on every pathway.

  usage: o22_o1_surface.py <surface_in.json> <surface_out.json>
"""
import sys, json

A, B = sys.argv[1], sys.argv[2]
S = json.load(open(A))
out = json.loads(json.dumps(S))
P = print
P("  O1: KPP := pointwise max(KPP, nonKPP).  Binding cells printed with their size.")
P("  %-10s %-4s %10s %10s %10s" % ('layer', 'd', 'KPP as-is', 'nonKPP', 'O1 wired'))
nb = 0
wp = out['whole_pool']
for i in range(6):
    a, b = wp['KPP'][i], wp['nonKPP'][i]
    if b > a + 1e-12:
        nb += 1
        P("  %-10s d%-3d %10.4f %10.4f %10.4f  <- BINDS (+%.4f)" % ('whole_pool', i + 1, a, b, b, b - a))
    wp['KPP'][i] = max(a, b)
per = {}
for pw, D in out['pathway'].items():
    k = 0
    for i in range(6):
        a, b = D['KPP'][i], D['nonKPP'][i]
        if b > a + 1e-12:
            k += 1; nb += 1
        D['KPP'][i] = max(a, b)
    per[pw] = k
P("  pathway layer, cells where O1 binds (of 6 each): %s" % per)
P("  TOTAL BINDING CELLS: %d of %d (whole pool 6 + 9 pathways x 6)" % (nb, 6 + 6 * len(out['pathway'])))
out['_ORDER22_O1'] = 'O1 APPLIED: KPP := pointwise max(KPP, nonKPP), whole-pool and every pathway.'
json.dump(out, open(B, 'w'), indent=1)
P("  wrote %s" % B)
