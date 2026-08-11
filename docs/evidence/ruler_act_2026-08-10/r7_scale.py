"""Extract the engine's own season-pricing constants: SCALE, GAMMA, REPL, posval, capt_prem.
Loads rl_model.py in the act-branch engine workspace. READ-ONLY."""
import os, sys, io, json, contextlib, hashlib
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
WD = SP + "/rw"
sys.path.insert(0, "/home/claude/rl_vendor")
os.chdir(WD); sys.path.insert(0, ".")
print("store md5:", hashlib.md5(open(WD + "/rl_model_data.json", "rb").read()).hexdigest()[:8])
src = open("rl_model.py").read()
G = {"__name__": "_rl_scale"}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(src, G)
print("--- engine constants ---")
for k in ("SCALE", "GAMMA", "S_SH", "REPL", "LENS", "BOARD_FACTOR", "_P1",
          "LCAPT_BAR", "LCAPT_M", "LCAPT_W", "LCAPT_G", "LIVE_SEASON"):
    if k in G: print("  %-12s = %s" % (k, G[k]))
print("  PVC[1]       =", G["PVC"][1])
posval = G["posval"]; capt_prem = G["capt_prem"]; val = G["val"]
print("  posval(10)   =", posval(10.0), " capt_prem(110) =", capt_prem(110.0))
print("  val(1.0)     =", val(1.0), "   -> SCALE check")
# season kernel: value in board points of ONE season of (avg, games, bar)
SCALE = G["SCALE"]; REPL = G["REPL"]
def season_price(avg, games, bar):
    return SCALE * posval(avg + capt_prem(avg) - REPL[bar]) * games
print("--- sample season prices (board points) ---")
for (a, g, b) in [(100.0, 22, "MID"), (80.1, 22, "MID"), (60.0, 22, "MID"),
                  (110.0, 22, "MID"), (85.0, 22, "KPD"), (85.0, 11, "KPD")]:
    print("   avg=%5.1f games=%2d bar=%-4s -> %8.1f" % (a, g, b, season_price(a, g, b)))
json.dump(dict(SCALE=SCALE, GAMMA=G["GAMMA"], S_SH=G["S_SH"], REPL=REPL, LENS=G["LENS"],
               BOARD_FACTOR=G["BOARD_FACTOR"], P1=G["_P1"], PVC1=G["PVC"][1],
               LCAPT=dict(BAR=G["LCAPT_BAR"], M=G["LCAPT_M"], W=G["LCAPT_W"], G=G["LCAPT_G"])),
          open(SP + "/r7_scale.json", "w"), indent=1)
print("wrote", SP + "/r7_scale.json")
