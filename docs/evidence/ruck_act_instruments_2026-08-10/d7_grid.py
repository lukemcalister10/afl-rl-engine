"""Recover the pick-neutral ruck production->$ ceiling curve empirically from the instrumented rows.
   ceiling = RUC_CEIL_HEAD(0.80) * grid(bestlvl) * head_mult   ->  grid = ceiling / 0.80 / head_mult
   (only rows with qualified production, bestlvl>0, carry the production ceiling)."""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
BR = json.load(open(SP + "ruck_instr_branch.json"))
pts = {}
for r in BR['rows']:
    if r['no_production']: continue
    g = r['cpv'] / 0.80 / r['head_mult']
    pts.setdefault(round(r['bestlvl'], 1), g)
print("BRANCH (act) ceiling grid, recovered:   meta grid_lo=%.1f grid_hi=%.1f refpk=%s"
      % (BR['meta']['ruccei_meta']['grid_lo'], BR['meta']['ruccei_meta']['grid_hi'], BR['meta']['ruccei_meta']['refpk']))
ks = sorted(pts)
for k in ks[::max(1, len(ks) // 30)]:
    print("   peak season avg %6.1f -> standardized ruck price %9.1f   (ceiling at head 0.80 = %8.1f)" % (k, pts[k], 0.8 * pts[k]))
flat = [k for k in ks if abs(pts[k] - BR['meta']['ruccei_meta']['grid_lo']) < 1e-6]
print("   FLAT AT THE GRID FLOOR up to peak season avg = %.1f  (n=%d distinct levels)" % (max(flat) if flat else 0, len(flat)))
print()
MN = json.load(open(SP + "ruck_instr_main.json"))
pts2 = {}
for r in MN['rows']:
    if r['pos'] != 'RUCK' or r.get('no_production'): continue
    pts2.setdefault(round(r['bestlvl'], 1), r['cpv'] / 0.80 / r['head_mult'])
print("MAIN (live) ceiling grid, recovered:    meta grid_lo=%.1f grid_hi=%.1f"
      % (MN['meta']['ruccei_meta']['grid_lo'], MN['meta']['ruccei_meta']['grid_hi']))
ks2 = sorted(pts2)
for k in ks2[::max(1, len(ks2) // 20)]:
    print("   peak season avg %6.1f -> standardized ruck price %9.1f   (ceiling at head 0.80 = %8.1f)" % (k, pts2[k], 0.8 * pts2[k]))
flat2 = [k for k in ks2 if abs(pts2[k] - MN['meta']['ruccei_meta']['grid_lo']) < 1e-6]
print("   FLAT AT THE GRID FLOOR up to peak season avg = %.1f" % (max(flat2) if flat2 else 0))
print()
print("HEAD MULTIPLIER (smooth young-ruck headroom) as seen on the leg rows:")
seen = {}
for r in BR['rows']:
    seen.setdefault((r['pk'] <= 3, r['pk']), r['head_mult'])
for r in sorted(BR['rows'], key=lambda z: z['pk'])[:1]:
    pass
hm = {}
for r in BR['rows']:
    hm.setdefault((r['pk'], int(r['age_asof']) if r['age_asof'] is not None else -1), r['head_mult'])
for k in sorted(hm)[:0]:
    pass
print("   examples: " + ", ".join("pk%d age%d -> %.4f" % (a, b, hm[(a, b)]) for a, b in sorted(hm)[:12]))
