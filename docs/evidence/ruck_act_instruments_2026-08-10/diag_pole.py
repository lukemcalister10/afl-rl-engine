import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
CF=json.load(open(SP+"ruck_cf_branch.json"))
IR={ (r['key'],r['Y']):r for r in json.load(open(SP+"ruck_instr_branch.json"))['rows'] }
keys=[('luke-jackson',2020),('brodie-grundy',2013),('sean-darcy',2017),('nicholas-naitanui',2009),('paddy-ryder',2006)]
for r in CF:
    k=(r['key'],r['Y'])
    if k not in keys: continue
    i=IR[k]
    print("%-20s Y=%d  e=%9.2f e_C=%9.2f  d_e=%+8.2f | price=%8.1f A=%8.1f C=%8.1f AC=%8.1f | raw_ev=%9.2f raw_pole=%9.2f iso=%.4f pole_w=%.4f po=%9.2f pr=%9.2f | cpv=%8.1f v0u=%8.1f" % (
      r['key'],r['Y'],r['e'],r['e_C'],r['e_C']-r['e'],r['price'],r['price_A'],r['price_C'],r['price_AC'],
      i['raw_ev'],i['raw_ev_pole'],i['iso_eff'],i['pole_w'],i['pole_po'],i['pole_pr'],i['cpv'],i['v0u']))
print()
neg=[r for r in CF if r['price_C']<r['price']-0.5]
print("rows where the pole CF LOWERS the price: %d of %d" % (len(neg),len(CF)))
import collections
c=collections.Counter(r['key'] for r in neg)
print(c.most_common(12))
