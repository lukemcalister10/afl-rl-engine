import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
s6=json.load(open(SP+"s6_rows.json"))
ND=[r for r in s6 if r['nd'] and 1<=r['pk']<=64 and 2004<=r['C']<=2022]
def f1(c):
    sp=sum(r['price'] for r in c); return (sum(r['F'] for r in c)/sp, len(c), sp)
print("leg ALL N   F1=%.4f rows=%d Sprice=%.0f" % f1(ND))
print("RUCK ALL N  F1=%.4f rows=%d Sprice=%.0f" % f1([r for r in ND if r['pos']=='RUCK']))
print("leg N<=4    F1=%.4f rows=%d" % f1([r for r in ND if r['N']<=4])[:2])
print("leg N>4     F1=%.4f rows=%d" % f1([r for r in ND if r['N']>4])[:2])
print("RUCK N>4    F1=%.4f rows=%d" % f1([r for r in ND if r['N']>4 and r['pos']=='RUCK'])[:2])
print()
print("per-N leg vs ruck F1:")
for N in range(1,13):
    a=[r for r in ND if r['N']==N]; b=[r for r in a if r['pos']=='RUCK']
    if not b: continue
    print("  N=%2d  leg %6.3f (n=%4d)   RUCK %6.3f (n=%3d)   ratio %.3f" % (N,f1(a)[0],len(a),f1(b)[0],len(b),f1(b)[0]/f1(a)[0]))
