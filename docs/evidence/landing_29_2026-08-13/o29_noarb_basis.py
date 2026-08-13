import json
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/'
# The loader's own population filter, replicated READ-ONLY from
# harness_pvc_REPINNED_pass3.py::load_matrix (ND_LAST=64, YR_LO=2004, CLASS_CUT=2022).
f = lambda M: {r['key'] for r in M['recs'] if r.get('teaches_curve') and r.get('pick')
               and 1 <= r['pick'] <= 64 and 2004 <= r['year'] <= 2022}
out = {}
for lbl, p in [('LIVE (O25R4)', 'per_entrant_O25R4.json'),
               ('LANDED (O29FINAL)', 'per_entrant_O29FINAL.json')]:
    M = json.load(open(SP + p)); meta = M['meta']
    out[lbl] = (M, meta, f(M))
    print("%-18s store=%-10s v0surf=%-14s recs=%-5d ND-teaching(EXPECT_N)=%d"
          % (lbl, meta.get('store_md5'), meta.get('v0surf_sig', '')[:12],
             len(M['recs']), len(out[lbl][2])))
A = out['LIVE (O25R4)'][2]; B = out['LANDED (O29FINAL)'][2]
print("\nND teaching-population delta LANDED vs LIVE:  +%d entered  /  -%d left" % (len(B - A), len(A - B)))
print("  entered:", sorted(B - A))
print("  left   :", sorted(A - B))
print("\nmatrix meta keys:", sorted(out['LANDED (O29FINAL)'][1].keys()))
print("\nfull LANDED meta:")
for k, v in sorted(out['LANDED (O29FINAL)'][1].items()):
    print("   %-22s %s" % (k, str(v)[:110]))
