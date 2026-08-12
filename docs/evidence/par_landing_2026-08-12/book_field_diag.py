import json, os, subprocess, collections
ROOT = '/home/user/afl-rl-engine/.claude/worktrees/agent-a6af0d68789879235'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o20c'
MAIN = json.loads(subprocess.run(['git', '-C', ROOT, 'show', 'origin/main:engine/rl_after/s4_matrix.json'],
                                 capture_output=True).stdout)
CTRL = json.load(open(os.path.join(SP, 'book_ctrl/s4_matrix.json')))

km, kc = set(MAIN), set(CTRL)
print("keys only in main   :", list(km - kc)[:6], "(n=%d)" % len(km - kc))
print("keys only in rebuild:", list(kc - km)[:6], "(n=%d)" % len(kc - km))

common = sorted(km & kc)
print("common keys:", len(common))
k = common[0]
print("\nsample key:", k)
a, b = MAIN[k], CTRL[k]
print(" fields main   :", sorted(a))
print(" fields rebuild:", sorted(b))
fielddiff = collections.Counter()
for k in common:
    for f in set(MAIN[k]) | set(CTRL[k]):
        if json.dumps(MAIN[k].get(f), sort_keys=True) != json.dumps(CTRL[k].get(f), sort_keys=True):
            fielddiff[f] += 1
print("\nper-field difference counts across %d common entries:" % len(common))
for f, n in fielddiff.most_common(15):
    print("   %-22s %d" % (f, n))
if fielddiff:
    f = fielddiff.most_common(1)[0][0]
    for k in common:
        if json.dumps(MAIN[k].get(f), sort_keys=True) != json.dumps(CTRL[k].get(f), sort_keys=True):
            print("\nexample field '%s' for key %s:\n  main    %s\n  rebuild %s"
                  % (f, k, str(MAIN[k].get(f))[:300], str(CTRL[k].get(f))[:300]))
            break
