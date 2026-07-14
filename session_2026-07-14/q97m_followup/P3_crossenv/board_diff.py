#!/usr/bin/env python3
"""Compare two rl_app_data.json board builds over the 804 active players (key='key', value='v')."""
import json, sys
a=json.load(open(sys.argv[1])); b=json.load(open(sys.argv[2]))
ra=a['active']; rb=b['active']
ma={r['key']:r['v'] for r in ra}; mb={r['key']:r['v'] for r in rb}
common=[k for k in ma if k in mb]
movers=[(k,ma[k],mb[k],mb[k]-ma[k]) for k in common if ma[k]!=mb[k]]
print(f"active players A={len(ra)} B={len(rb)} common-keyed={len(common)}")
print(f"SUM A={sum(ma.values())} SUM B={sum(mb.values())}")
print(f"MOVERS (v differs): {len(movers)} of {len(common)}")
if movers:
    deltas=[t[3] for t in movers]
    print(f"  delta range: min={min(deltas):+} max={max(deltas):+} sum={sum(deltas):+}")
    import collections
    hist=collections.Counter(abs(dd) for _,_,_,dd in movers)
    print("  |delta| histogram:", dict(sorted(hist.items())))
    print("  largest movers by |delta|:")
    for k,va,vb,dd in sorted(movers,key=lambda t:-abs(t[3]))[:25]:
        print(f"    {str(k)[:30]:30s} {va:>7} -> {vb:>7}  (delta {dd:+})")
else:
    print("  VALUE-IDENTICAL across the two environments (0 of 804 move)")
