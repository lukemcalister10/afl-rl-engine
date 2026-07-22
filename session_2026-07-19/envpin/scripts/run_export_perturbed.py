#!/usr/bin/env python3
# MECHANISM-PROOF harness (env-pin, 2026-07-19). Runs rl_export.py in the current workspace after
# monkeypatching numpy.interp to add a relative perturbation of magnitude RL_INTERP_PERTURB to every
# interp output. This simulates the last-ULP output difference a DIFFERENT numpy WHEEL (a different
# compile of compiled_base.c's interp routine) would produce for identical inputs — the exact cross-build
# amplifier item 391 named. EPS=0 == the pinned wheel (no perturbation).
#
# The engine calls np.interp as a module-attribute (`np.interp(...)`) at call time, so patching
# numpy.interp before rl_export imports the engine reaches every one of the 25+ call sites.
#
# RL_INTERP_MODE:
#   coherent   (default) — out = r*(1+EPS): every interp output biased the SAME direction. This is the
#              worst-case, order-preserving-in-magnitude model item 391 used ("interp @1e-8 -> Sv-96").
#   incoherent — out = r*(1 +/- EPS) with per-element sign from mantissa parity (ULP jitter model).
#
# After the build it also prints Sv (sum of displayed v) and Sheezel v, so sub-md5 movement is visible.
import os, sys, io, json, hashlib
import numpy as np

EPS = float(os.environ.get("RL_INTERP_PERTURB", "0") or "0")
MODE = os.environ.get("RL_INTERP_MODE", "coherent")
_orig_interp = np.interp

def _perturbed_interp(x, xp, fp, *a, **kw):
    r = _orig_interp(x, xp, fp, *a, **kw)
    if EPS == 0.0:
        return r
    arr = np.asarray(r, dtype=np.float64)
    if MODE == "incoherent":
        bits = arr.view(np.int64)
        sign = np.where((bits & 1) == 0, 1.0, -1.0)
    else:
        sign = 1.0
    out = arr * (1.0 + EPS * sign)
    if np.ndim(r) == 0:
        return np.float64(out)
    return out

if EPS != 0.0:
    np.interp = _perturbed_interp
    sys.stderr.write(f"[perturb] numpy.interp patched EPS={EPS:g} mode={MODE}\n")

src = open("rl_export.py").read()
g = {"__name__": "__main__", "__file__": "rl_export.py"}
exec(compile(src, "rl_export.py", "exec"), g)

# report board md5 + Sv + Sheezel from the freshly written rl_app_data.json
try:
    raw = open("rl_app_data.json", "rb").read()
    md5 = hashlib.md5(raw).hexdigest()[:8]
    d = json.loads(raw)
    rows = d if isinstance(d, list) else d.get("players") or d.get("board") or next((v for v in d.values() if isinstance(v, list)), [])
    def gv(p): return p.get("v", p.get("_v"))
    sv = sum(int(gv(p)) for p in rows if isinstance(p, dict) and gv(p) is not None)
    sh = next((int(gv(p)) for p in rows if isinstance(p, dict) and "sheezel" in str(p.get("player", p.get("name",""))).lower()), None)
    sys.stderr.write(f"[result] md5={md5} Sv={sv} Sheezel={sh}\n")
except Exception as e:
    sys.stderr.write(f"[result] post-parse failed: {e}\n")
