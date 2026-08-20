import json, math
ROOT = "/home/user/afl-rl-engine/.claude/worktrees/agent-ac6abd0494353e85f"
J = json.load(open(ROOT + "/engine/rl_after/pvc_curve_v2.json"))
posv = {g: {int(k): float(v) for k, v in d.items()} for g, d in J['nd_v0']['posv'].items()}
PHI = 0.92
ROWS = [('josh-smillie', 'MID', 7, 2.92), ('harry-demattia', 'MID', 25, 3.92), ('max-knobel', 'RUCK', 42, 4.92)]

def mk(tab, deep):
    """tab: {depth: D}. deep: callable for c beyond the last tabled depth."""
    def D(c):
        if c <= 1: return 1.0
        lo = int(math.floor(c)); f = c - lo
        def at(n):
            if n in tab: return tab[n]
            return deep(n)
        a, b = at(lo), at(lo + 1)
        return a ** (1 - f) * b ** f
    return D

def decay(d2, d3):
    a = -math.log(d2); b = math.log(-math.log(d3) / a) / math.log(2.0)
    return lambda n: math.exp(-a * (n - 1) ** b)

OPTS = {
 'A ruled constants':      ({1: 1.0, 2: 0.5684, 3: 0.3600, 4: 0.3073}, decay(0.5684, 0.3600)),
 'B R1 + measured d4':     ({1: 1.0, 2: 0.5502, 3: 0.2628, 4: 0.3460}, decay(0.5502, 0.2628)),
 'C R1 + fitted from d4':  ({1: 1.0, 2: 0.5502, 3: 0.2628},            decay(0.5502, 0.2628)),
}
print("%-22s %6s %6s %10s | %s" % ("row", "pos", "pick", "v0(30B)", "  ".join("%-22s" % k for k in OPTS)))
for key, g, pk, c in ROWS:
    v0 = posv[g][pk]
    cells = []
    for name, (tab, dp) in OPTS.items():
        D = mk(tab, dp)
        cells.append("D=%.4f -> %6.0f   " % (D(c), v0 * D(c)))
    print("%-22s %6s %6d %10.2f | %s" % (key, g, pk, v0, "".join(cells)))
