#!/usr/bin/env python3
"""Bound the guard-flip risk from the native-vs-SSE board delta: named anchors, sum, band shifts,
and the numeraire pick-1. Not the gate itself (that needs G-COHORT re-run on the SSE board) — a bound."""
import json, sys
a=json.load(open(sys.argv[1])); b=json.load(open(sys.argv[2]))
ma={r['key']:r for r in a['active']}; mb={r['key']:r for r in b['active']}
NAMED=['nick-daicos','marcus-bontempelli','harry-sheezel','max-gawn','harley-reid','josh-ward','darcy-moore','taylor-goad','josh-smillie','will-green']
print("NAMED ANCHORS (v native -> SSE):")
for k in NAMED:
    if k in ma and k in mb:
        va,vb=ma[k]['v'],mb[k]['v']
        print(f"  {k:22s} {va:>7} -> {vb:>7}  {'MOVED '+str(vb-va) if va!=vb else 'same'}")
sa=sum(r['v'] for r in a['active']); sb=sum(r['v'] for r in b['active'])
print(f"\nBOARD SUM native={sa} SSE={sb} delta={sb-sa} ({100*(sb-sa)/sa:+.4f}%)")
movers=[(k,ma[k]['v'],mb[k]['v']) for k in ma if k in mb and ma[k]['v']!=mb[k]['v']]
if movers:
    rel=[abs(vb-va)/max(abs(va),1) for _,va,vb in movers]
    print(f"movers={len(movers)} max_abs_delta={max(abs(vb-va) for _,va,vb in movers)} "
          f"max_rel={max(rel)*100:.3f}% mean_rel={sum(rel)/len(rel)*100:.4f}%")
# numeraire: pick-1 is a LOADED anchor; the panel is round(ev/1.0524). If daicos numeraire moves, numeraire drifts.
print("\nnumeraire check: pick-1=3000 is the LOADED _PVC0 anchor (pvc_curve_L1b.json), env-invariant by construction.")
