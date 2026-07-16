# OWNER-ORDERED (2026-07-16): decompose each of the 37 young over-performer deltas to prove movement is
# 100% the pick channel — raw_ev (production) BYTE-IDENTICAL pre/post. Any row failing => HALT.
import json
off=json.load(open('board_off.json')); on=json.load(open('board_on.json'))
act=set(r['key'] for r in json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))['active'])
def good(d): return isinstance(d,dict) and 'error' not in d
# (0) GLOBAL production-frozen proof: raw_ev byte-identical for EVERY priced player, off vs on
allk=[k for k in off if good(off[k]) and good(on.get(k,{}))]
prod_moved=[k for k in allk if off[k]['rawev']!=on[k]['rawev']]
print(f"GLOBAL raw_ev byte-identity: {len(allk)-len(prod_moved)}/{len(allk)} identical; production MOVED on {len(prod_moved)} rows")
if prod_moved:
    print("  !! rows where production moved (unexpected coupling):", prod_moved[:20])
# (1) the 37 young over-performer cuts (age<=26, pormargin>0, num_on<num_off)
op=[k for k in allk if k in act and off[k]['age']<=26 and off[k].get('pormargin',0)>0 and on[k]['num']<off[k]['num']]
op.sort(key=lambda k:on[k]['num']-off[k]['num'])
print(f"\n=== 37-ROW DECOMPOSITION (young above-projection trims) — {len(op)} rows ===")
print(f"{'player':22}{'pos':7}{'pk':>3}{'rawev==':>8}{'iso_off':>9}{'iso_on':>9}{'isoR':>7}{'off':>6}{'on':>6}{'numR':>7}{'HALT?':>7}")
halts=[]
for k in op:
    o,n=off[k],on[k]
    rid = (o['rawev']==n['rawev'])
    isoR = float(n['iso'])/float(o['iso']) if float(o['iso'])!=0 else 0
    numR = n['num']/o['num'] if o['num'] else 0
    # 100% pick channel requires production byte-identical. numR vs isoR agreement is a secondary read
    # (downstream additive layers e.g. captaincy shift the ratio without moving production).
    halt = not rid
    if halt: halts.append(k)
    print(f"{o['player'][:21]:22}{o['pos']:7}{o['effpk']:>3}{('YES' if rid else 'NO!'):>8}"
          f"{float(o['iso']):>9.4f}{float(n['iso']):>9.4f}{isoR:>7.3f}{o['num']:>6}{n['num']:>6}{numR:>7.3f}{('HALT' if halt else 'ok'):>7}")
print(f"\nVERDICT: {len(op)} rows | production byte-identical on {len(op)-len(halts)}/{len(op)} "
      f"| {'*** HALT: '+str(len(halts))+' rows moved production ***' if halts else 'PASS — every delta is 100%% pick channel (raw_ev frozen)'}")
# sanity: show that for these rows the value ratio tracks iso where no downstream clamp/add binds
import statistics
clean=[k for k in op if off[k]['rawev']==on[k]['rawev']]
dev=[abs((on[k]['num']/off[k]['num']) - (float(on[k]['iso'])/float(off[k]['iso']))) for k in clean if off[k]['num']]
print(f"among production-frozen rows: median |numR - isoR| = {statistics.median(dev):.4f} "
      f"(0 => value ratio IS the iso ratio; >0 => an iso-independent additive downstream layer, still not production)")
outliers=sorted(clean,key=lambda k:abs((on[k]['num']/off[k]['num'])-(float(on[k]['iso'])/float(off[k]['iso']))),reverse=True)[:6]
print("largest numR-vs-isoR gaps (inspect for a downstream additive layer, NOT production):")
for k in outliers:
    o,n=off[k],on[k]
    print(f"  {o['player'][:22]:23} numR {n['num']/o['num']:.3f} isoR {float(n['iso'])/float(o['iso']):.3f} "
          f"pos {o['pos']} pk {o['effpk']} (raw_ev frozen: {o['rawev']==n['rawev']})")
