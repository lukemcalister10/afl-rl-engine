#!/usr/bin/env python3
"""THE SITTER-LAW PREVIEW TRANSFORM — exactly as run in-session 2026-08-14 (see README.md).

Applies the packet-2 candidate sitter discount to every zero-games-as-of-that-year cell of the
ORDER 29C landed-law matrix. PREVIEW ONLY: nothing wires; the owner's ruling governs adoption.

usage: sitter_preview_transform.py <per_entrant_O29CFINAL.json> <outdir>
Emits per_entrant_SITND.json (ND rows only) and per_entrant_SITALL.json (+ provisional pool fade).
"""
import json, copy, sys, os

D_ND = {2: 0.5684, 3: 0.3600}          # packet-2 listed-conditional candidate; >=4 held at the bound
ND_FLOOR = 0.3073                       # the depth-4 bound, held flat (deep-end rule = an owner word)
D_POOL = {2: 0.624, 3: 0.380}           # PROVISIONAL: the landed pool psi-surface values, pending 30B
POOL_FLOOR = 0.380

def disc(table, depth, floor):
    return table.get(depth, floor)

def transform(recs, include_pool):
    rows = cells = 0
    for r in recs:
        v0 = r.get('v0')
        if not v0 or v0 <= 0:
            continue
        pool = r.get('is_pool')
        if pool and not include_pool:
            continue
        tab, flo = (D_POOL, POOL_FLOOR) if pool else (D_ND, ND_FLOOR)
        gb = r.get('games_by') or {}
        vp = r.get('vpath') or []
        moved = False
        for i, mark in enumerate(vp):
            if mark is None:
                continue
            N = i + 1
            if gb.get(str(N)) == 0:
                newv = v0 * disc(tab, N + 1, flo)
                if abs(newv - mark) > 1e-9:
                    vp[i] = newv; cells += 1; moved = True
        if moved:
            rows += 1
    return rows, cells

def main():
    src, outdir = sys.argv[1], sys.argv[2]
    base = json.load(open(src))
    for name, incpool in (('SITND', False), ('SITALL', True)):
        d = copy.deepcopy(base)
        rows, cells = transform(d['recs'], incpool)
        d['meta']['sitter_preview'] = name
        out = os.path.join(outdir, f'per_entrant_{name}.json')
        json.dump(d, open(out, 'w'))
        print(name, 'rows changed', rows, 'cells moved', cells, '->', out)

if __name__ == '__main__':
    main()
