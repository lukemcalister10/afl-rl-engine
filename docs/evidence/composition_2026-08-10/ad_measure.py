"""THE AGE-DYNAMIC DISCOUNT — the measurement the owner ordered. READ-ONLY.

Per pair: the relativity guard re-read (the headline), the young/peak books ex-picks, the board
total, the Mraz line in LADDER currency, and both year-1 landings.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from engine_load import load

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
REPO = "/home/user/afl-rl-engine"
g = load(); MA = g['MA']; Y = 2026
PL_F = g['_PL_F']; CURVE35 = float(g['_PVC0'][35])
byk = {p['key']: p for p in MA.data if p.get('key')}

bd = lambda p: {r['key']: r for r in json.load(open(p))['active']}
MAIN = bd(REPO + "/data/rl_build/rl_app_data.json")

# membership FROZEN on the pre-act board, exactly as pre-registered
YOUNG, PEAK = set(), set()
for k in MAIN:
    p = byk.get(k)
    if not p: continue
    try: r = Y - MA.debut(p) + 1
    except Exception: continue
    if r <= 1: YOUNG.add(k)
    elif r in (4, 5, 6): PEAK.add(k)

def picks(b):
    for kk in ('picks', 'pick_values', 'PICKS'):
        v = b.get(kk)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            for f in ('v', 'value', 'val'):
                if f in v[0]: return sum(float(x[f]) for x in v)
    return 0.0

PT = picks(json.load(open(REPO + "/data/rl_build/rl_app_data.json")))
s = lambda d, S: sum(d[k]['v'] for k in S if k in d)

VARIANTS = [
    ("main (pre-act)",        REPO + "/data/rl_build/rl_app_data.json"),
    ("FULL (no AD)",          SP + "/bd_FULL.json"),
    ("AD 12.5 / 15.5",        SP + "/bd_AD_125_155.json"),
    ("AD 13 / 15  (ordered)", SP + "/bd_FULL_AD.json"),
    ("AD 13.5 / 14.5",        SP + "/bd_AD_135_145.json"),
    ("AD 12 / 16",            SP + "/bd_AD_12_16.json"),
]

print("""
================================================================================================================
READ THE ENVELOPE COLUMNS AS AN ENVELOPE, NOT AS A TARGET.
The owner's acceptance envelope is peak ~= 140% of year-0 and ~= 130% of year-1. It is a frame for JUDGING a
composed result, and NO COMPONENT MAY BE TUNED TO IT. That is the dissolved-1.40-act lesson: the moment a
ratio becomes an objective, every dial starts serving the ratio instead of the evidence, and the number stops
meaning anything. Nothing in this act is sized against these columns; they are reported so the owner can see
where the package sits relative to his frame.
================================================================================================================""")
print("=" * 112)
print("THE AGE-DYNAMIC DISCOUNT — GUARD TABLE PER PAIR")
print("  RELATIVITY = (picks + young players) / peak players, membership frozen on the pre-act board")
print("=" * 112)
print(" %-22s %10s %10s %11s %9s %9s %11s" %
      ("variant", "YOUNG", "PEAK", "RELATIVITY", "vs main", "recovered", "board total"))
base_r = None; full_r = None
rows = []
for lab, path in VARIANTS:
    if not os.path.exists(path):
        print(" %-22s  (board absent)" % lab); continue
    d = bd(path)
    yv = s(d, YOUNG) + PT; pv = s(d, PEAK)
    r = yv / pv
    tot = sum(x['v'] for x in d.values())
    if base_r is None: base_r = r
    if lab.startswith("FULL"): full_r = r
    gap = r - base_r
    rec = ""
    if full_r is not None and lab.startswith("AD"):
        short = base_r - full_r
        rec = "%.1f%%" % (100.0 * (r - full_r) / short) if short else "n/a"
    print(" %-22s %10.0f %10.0f %11.6f %9s %9s %11d"
          % (lab, yv, pv, r, "%+.3fpp" % (gap * 100), rec, tot))
    rows.append((lab, d, r, yv, pv, tot))

print("\n=== YOUNG / PEAK PLAYER BOOKS, EX-PICKS (the pick block is constant at %.0f) ===" % PT)
print(" %-22s %12s %10s %12s %10s" % ("variant", "young", "vs main", "peak", "vs main"))
m_y = s(MAIN, YOUNG); m_p = s(MAIN, PEAK)
for lab, d, r, yv, pv, tot in rows:
    y = s(d, YOUNG); pk = s(d, PEAK)
    print(" %-22s %12d %9.1f%% %12d %9.1f%%" % (lab, y, 100 * (y / m_y - 1), pk, 100 * (pk / m_p - 1)))

print("\n=== THE MRAZ LINE, IN LADDER CURRENCY (pick-35 = %.1f; ruled band 2-3x) ===" % CURVE35)
print(" %-22s %8s %12s   %s" % ("variant", "board", "x pick-35", "verdict"))
for lab, d, r, yv, pv, tot in rows:
    v = d.get('noah-mraz', {}).get('v')
    if v is None: continue
    lr = v * PL_F / CURVE35
    print(" %-22s %8d %12.3f   %s" % (lab, v, lr, "INSIDE 2-3x" if 2.0 <= lr <= 3.0 else
                                      ("above 3x" if lr > 3.0 else "below 2x")))

# ---- the gradient: what pair would fully recover? ----
print("\n=== THE GRADIENT (INFORMATION, NOT A RECOMMENDATION — the sizing word is the owner's) ===")
pts = []
for lab, d, r, yv, pv, tot in rows:
    if lab.startswith("AD"):
        import re
        nums = re.findall(r"[\d.]+", lab)
        if len(nums) >= 2:
            spread = float(nums[1]) - float(nums[0])
            pts.append((spread, r))
if len(pts) >= 2 and full_r is not None:
    pts.sort()
    xs = np.array([x for x, _ in pts]); ys = np.array([y for _, y in pts])
    sl, ic = np.polyfit(xs, ys, 1)
    need = (base_r - ic) / sl if sl else float('nan')
    print("  RELATIVITY is close to linear in the LO-HI spread over the range tested:")
    for x, y in pts: print("     spread %.3f -> %.6f" % (x, y))
    print("  fitted slope %.6f RELATIVITY per percentage-point of spread." % sl)
    print("  Extrapolated, full recovery of the breach would need a spread of about %.1f points" % need)
    print("  around the 14%% centre - i.e. rates of roughly %.0f%% and %.0f%%." % (14 - need / 2, 14 + need / 2))
    print("""
  THE HONEST READING OF THAT NUMBER: it is outside any defensible range, and the linear fit has no
  business being extrapolated three times past its data. The finding is not "use a spread of 11" -
  it is that THE AGE-DYNAMIC DISCOUNT, AT ANY SIZE THE OWNER WOULD PLAUSIBLY SIGN, DOES NOT CLOSE
  THE RELATIVITY BREACH. The widest pair measured (12/16) recovers about a third of it. If the
  breach is to be closed, it needs a different instrument or a decision about #336 itself, which
  is the item that opened it.""")

# ---- the acceptance-envelope ratios ----------------------------------------------------------
# DEFINITIONS, stated once and held identical across every variant (consistency matters more than
# the particular choice):
#   YEAR-0 per player = mean entry_anchor over the board's ND in-curve rows, converted to BOARD
#                       currency (entry_anchor is engine currency; board = engine / _PL_F)
#   YEAR-1 per player = mean board price over rung-1 players
#   PEAK   per player = mean board price over rung 4-6 players
ea = g['entry_anchor']
NDIC = [k for k in MAIN if byk.get(k) is not None and byk[k].get('type') == 'ND'
        and not MA.is_pool(byk[k])]
Y0 = float(np.mean([float(ea(byk[k])) / PL_F for k in NDIC])) if NDIC else float('nan')
R1 = set(k for k in MAIN if byk.get(k) is not None
         and (lambda r: r == 1)(Y - MA.debut(byk[k]) + 1 if byk.get(k) else 0))
print("\n=== THE ACCEPTANCE ENVELOPE (peak ~140% of year-0, ~130% of year-1) — A FRAME, NOT A TARGET ===")
print("  year-0 per player = mean entry_anchor over %d ND in-curve rows, in board ccy = %.1f" % (len(NDIC), Y0))
print(" %-22s %11s %11s %13s %13s" % ("variant", "yr-1/player", "peak/player", "peak/year-0", "peak/year-1"))
for lab, d, r, yv, pv, tot in rows:
    r1v = [d[k]['v'] for k in R1 if k in d]
    pkv = [d[k]['v'] for k in PEAK if k in d]
    if not r1v or not pkv: continue
    m1 = float(np.mean(r1v)); mp = float(np.mean(pkv))
    print(" %-22s %11.0f %11.0f %12.1f%% %12.1f%%" % (lab, m1, mp, 100 * mp / Y0, 100 * mp / m1))
print("  envelope: 140% and 130%. Distance from it is information for the owner's sitting; no dial")
print("  in this act was sized against these two numbers.")
