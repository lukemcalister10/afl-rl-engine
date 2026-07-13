"""Shared measurement harness — TAGGED BOARD (store b0c39d78 / board 81e48293).

Run with env.sh sourced (WS_TAG + RL_* set). Exec's the engine source once and exposes:
  MA, cp, ev, F, players(), find(nm), board_val(p)  + walk-forward accessors.
Import as:  import harness as H
capt monkeypatch:  H.set_capt(gain, exp, cap)  /  H.capt_off()  /  H.capt_default()
"""
import io, contextlib, os, sys, copy
import numpy as np

WS = os.environ["WS_TAG"]
os.chdir(WS)
if WS not in sys.path: sys.path.insert(0, WS)

_src = open("_merged_recover.py").read().split('print("=== AFTER')[0]
G = {"__name__": "_mr_harness"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, G)

MA = G["MA"]; cp = G["cp"]; ev = G["ev"]; PR = G["PR"]
_nqual = G["_nqual"]; _fbump = G["_fbump"]; _agemult = G["_agemult"]; _agemult2 = G["_agemult2"]
F = 1.0524  # L7 numeraire divisor (baked 2026-07-13)

# capt constants live in rl_model (MA) module globals; capt_prem reads them at call time
_CAPT0 = dict(gain=MA.CAPT_GAIN, exp=MA.CAPT_EXP, cap=MA.CAPT_CAP, thresh=MA.CAPT_THRESH)

def set_capt(gain=None, exp=None, cap=None):
    if gain is not None: MA.CAPT_GAIN = gain
    if exp  is not None: MA.CAPT_EXP  = exp
    if cap  is not None: MA.CAPT_CAP  = cap
def capt_off():     MA.CAPT_GAIN = 0.0
def capt_default(): MA.CAPT_GAIN, MA.CAPT_EXP, MA.CAPT_CAP = _CAPT0["gain"], _CAPT0["exp"], _CAPT0["cap"]

def players():
    return [p for p in MA.data if MA.GRP.get(p.get("pos"))]
def find(nm):
    c = [p for p in MA.data if nm.lower() in p["player"].lower() and MA.GRP.get(p.get("pos"))]
    return c[0] if c else None
def board_val(p, Y=2026):
    return int(round(ev(p, Y) / F))
def ln_level(p, Y=2026):
    """the captaincy-line level: current weighted level cp._lvl_eff (what capt_prem is fed near k=0)."""
    return cp._lvl_eff(p, Y)

# ---- walk-forward accessors ----
def debutyr(p): return cp.debutyr(p)
def draft_year(p): return p.get("year")
def scoring(p): return sorted(p["scoring"], key=lambda x: x["year"])
def cum_games(p, Y): return sum(x.get("games", 0) for x in p["scoring"] if x["year"] <= Y)

def value_asof(p, t):
    """walk-forward: price p at Yt = draft_year+t with scoring truncated <= Yt (July-8 cohort machinery)."""
    D = draft_year(p); Yt = D + t; q = copy.deepcopy(p)
    q["scoring"] = [x for x in q["scoring"] if x["year"] <= Yt]; q["_pos_now"] = None; q["_fut"] = []
    MA.BASE_REF = MA.AGE_REF = Yt; MA._pe_clear()
    if cum_games(p, Yt) == 0 and t >= 3: return 0.0
    with contextlib.redirect_stdout(io.StringIO()): return float(ev(q, Yt))

if __name__ == "__main__":
    # smoke test: reproduce the tagged numeraire panel
    for nm, exp in [("Nick Daicos", 7667), ("Marcus Bontempelli", 3482), ("Max Gawn", 2393),
                    ("Harley Reid", 3594), ("Darcy Moore", 197)]:
        p = find(nm); v = board_val(p)
        print(f"  {nm:22s} board={v:<7d} expect={exp:<6d} {'OK' if v == exp else 'MISMATCH'}")
    print("  store md5 fields loaded; capt0:", _CAPT0)
