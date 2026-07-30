"""Install a derived curve into the worktree's adopted-curve artifact — the ONE disclosed pin edit
of the convergence lane. Updates curve, pool_value and the file's own curve_md5 so the artifact stays
self-consistent. Optionally also re-points the superseded L1b artifact (the ambiguous channel)."""
import json,sys,hashlib
derived,target,pool = sys.argv[1],sys.argv[2],float(sys.argv[3])
also_l1b = (len(sys.argv)>4 and sys.argv[4]=='--also-l1b')
ci=json.load(open(derived))['curve']['integer']
assert len(ci)==64, "expected 64 points, got %d"%len(ci)
assert ci[0]==3000, "numeraire broken: pin(1)=%s"%ci[0]
bad=[k for k in range(1,64) if ci[k-1]<=ci[k]]
assert not bad, "strict descent violated at %s"%bad[:5]
curve={str(k):int(ci[k-1]) for k in range(1,65)}
d=json.load(open(target))
d['curve']=curve
d['pool_value']=int(round(pool))
d['curve_md5']=hashlib.md5(json.dumps(curve,sort_keys=True).encode()).hexdigest()[:8]
json.dump(d,open(target,'w'),indent=1)
print("installed -> %s  payload %s  ladder %d  pool %d"%(target,d['curve_md5'],sum(ci),d['pool_value']))
if also_l1b:
    p=target.replace('pvc_curve_v2.json','pvc_curve_L1b.json')
    l=json.load(open(p))
    # L1b is the SUPERSEDED artifact: it carries no 'pool_value' field and holds its pool level as a
    # CURVE ENTRY at the pool index (its domain is the declared legacy 1-99 exception). Writing a bare
    # 1-64 curve strips that entry and _split_ladder HALTS on the missing pool level — which is itself
    # proof the artifact is really loaded and validated at import. Preserve the entry.
    lc=dict(curve); lc[str(65)]=int(round(pool))
    l['curve']=lc
    if 'pool_value' in l: l['pool_value']=int(round(pool))
    json.dump(l,open(p,'w'),indent=1)
    print("  also re-pointed L1b (pool level preserved as curve entry 65)")
