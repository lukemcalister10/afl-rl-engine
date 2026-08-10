import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
D=json.load(open("/home/user/afl-rl-engine/data/rl_build/rl_app_data.json"))
print(type(D), list(D.keys())[:20] if isinstance(D,dict) else len(D))
if isinstance(D,dict):
    for k,v in D.items():
        print(" ", k, type(v), (len(v) if hasattr(v,'__len__') else ''))
