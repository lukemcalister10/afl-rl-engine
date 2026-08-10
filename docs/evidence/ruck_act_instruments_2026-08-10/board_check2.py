import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
D=json.load(open("/home/user/afl-rl-engine/data/rl_build/rl_app_data.json"))
A=D['active']
print("active n=%d" % len(A))
print(json.dumps(A[0], indent=1)[:1200])
IN=json.load(open(SP+"ruck_instr_main.json"))
er={r['key']:r for r in IN['rows']}
F=IN['meta']['pl_factor']
# match on key if present
k0=A[0]
keys=set(er)
have=[a for a in A if a.get('key') in keys]
print("matched by key: %d of %d" % (len(have), len(A)))
import statistics
rats=[]
for a in have[:2000]:
    r=er[a['key']]
    v=a.get('value') or a.get('v') or a.get('price')
    if v: rats.append(r['price']/float(v))
print("engine/board ratio: n=%d median=%.6f min=%.6f max=%.6f" % (len(rats), statistics.median(rats), min(rats), max(rats)))
