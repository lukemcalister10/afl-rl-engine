"""TRUE WEIGHTS vs the VOID equal-weight reference — what the correct weighting changes. READ-ONLY."""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
T = json.load(open(SP + "/r33_owner_true.json"))
E = json.load(open(SP + "/r31_nodes.json"))
ORDER = ["willem-duursma", "zak-butters", "marcus-bontempelli"]
for k in ORDER:
    if k not in T or k not in E: continue
    t = {int(a): v for a, v in T[k]["cells"].items()}
    tot = sum(t.values())
    e = {int(a): float(v) for a, v in E[k]["mean"].items()}
    ages = sorted(set(t) | set(e))
    print()
    print("=" * 84)
    print("%s  — per-age share of current value: TRUE weights vs equal-weight reference" % k)
    print("  carriers: %s   (F = the node was carried by the demonstrated FLOOR, not the integral)"
          % " ".join(x[0] for x in T[k]["carried"]))
    print("=" * 84)
    print("  %-5s %12s %12s %10s" % ("age", "TRUE %", "equal-wt %", "delta pp"))
    worst = 0.0
    for a in ages:
        tv = 100 * t.get(a, 0.0) / tot; ev_ = 100 * e.get(a, 0.0)
        d = tv - ev_; worst = max(worst, abs(d))
        print("  %-5d %11.2f%% %11.2f%% %+9.2f" % (a, tv, ev_, d))
    print("  largest per-age shift: %.2f pp" % worst)
    a0 = int(round(float(T[k]["a_now"]))); cy0 = 2026 - int(T[k]["C"])
    tl = lambda N, m, s: 100 * sum(v for a, v in m.items() if (cy0 + (a - a0)) > N) / s
    print("  tail > career yr 11 :  TRUE %.1f%%   equal-wt %.1f%%"
          % (tl(11, t, tot), tl(11, e, 1.0)))
    print("  tail > career yr  7 :  TRUE %.1f%%   equal-wt %.1f%%"
          % (tl(7, t, tot), tl(7, e, 1.0)))
