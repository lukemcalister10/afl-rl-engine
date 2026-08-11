import pickle, glob, os
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
cands = ["/home/claude/v0surf.pkl", SP + "/repoM/data/v0surf.pkl", SP + "/repoB/data/v0surf.pkl"]
cands += sorted(glob.glob(SP + "/v0surf*.pkl"))
for c in cands:
    if not os.path.exists(c): print("missing:", c); continue
    try:
        d = pickle.load(open(c, "rb"))
        ks = list(d.keys()) if isinstance(d, dict) else ["<not a dict>"]
        print("%-70s %s" % (os.path.relpath(c, SP), ks))
    except Exception as e:
        print("%-70s ERROR %s" % (c, e))
