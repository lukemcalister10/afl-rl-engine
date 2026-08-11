import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
r=json.load(open(SP+"s6_rows.json"))
print("s6_rows type:", type(r))
if isinstance(r, dict):
    print("keys:", list(r.keys())[:20])
    for k in list(r.keys())[:3]:
        print(k, type(r[k]))
    rows = r.get('rows', None)
else:
    rows = r
print("nrows:", len(rows))
print("row0:", json.dumps(rows[0], indent=1)[:1500])
ks=set()
for x in rows: ks|=set(x.keys())
print("all keys:", sorted(ks))
pe=json.load(open(SP+"per_entrant_338_stage5.json"))
print("pe keys:", list(pe.keys()))
print("meta:", json.dumps(pe['meta'], indent=1)[:2000])
print("nrecs:", len(pe['recs']))
print("rec0:", json.dumps(pe['recs'][0], indent=1)[:1500])
ks=set()
for x in pe['recs']: ks|=set(x.keys())
print("rec keys:", sorted(ks))
