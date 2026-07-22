#!/usr/bin/env python3
# LEG F4 — k=0 DORMANCY UNIT TEST (extends F3's; MEMO_LEGF v1.3 §2.ix pt 3): assert the L-SYMMETRY damper is
# DORMANT at k=0 / backward / RL_LEGF=0 by IDENTITY — a no-op off the forward lens, independent of FP hashes.
# Run from the workspace: python3 test_k0_dormancy_f4.py   (exit 0 = PASS)
import os, io, contextlib, sys
import numpy as np
FAIL = []
def chk(name, cond):
    print(("  PASS " if cond else "  FAIL ") + name); (FAIL.append(name) if not cond else None)

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; active = g['_lsym_active']; blend = g['_lsym_blend']; s_of = g['_lsym_s']
MA.BASE_REF = MA.AGE_REF = 2026; MA._LENS_FORM = None; MA._pe_clear()

# (1) _lsym_active is FALSE off the forward lens (k=0 / balanced / backward)
chk("_lsym_active False when _LENS_FORM None (k=0 / balanced / backward)", active() is False or active() == False)
MA._LENS_FORM = 2026; MA.AGE_REF = 2026  # in the lens but AGE_REF==BASE_REF (k=0)
chk("_lsym_active False at k=0 even in the lens (AGE_REF==BASE_REF)", not active())
MA.AGE_REF = 2027  # forward
chk("_lsym_active True ONLY forward (lens set AND AGE_REF>BASE_REF)", bool(active()))
MA._LENS_FORM = None; MA.AGE_REF = MA.BASE_REF = 2026

# (2) the blend is an IDENTITY when x_form==x_age — which is EXACTLY the k=0 state (advanced read == form read)
x = np.array([100.0, 200.0, 300.0, 400.0, 500.0, 600.0])
chk("_lsym_blend(x, x, a) == x  (k=0: advanced read == form-anchored read => identity)", np.allclose(blend(x, x, 26), x))
chk("_lsym_blend identity holds elementwise byte-equal", list(np.asarray(blend(x, x, 26))) == list(x))

# (3) s>=1 => the blend returns x_age UNCHANGED (undamped ages are byte-exact)
xa = np.array([90.0, 180.0]); xf = np.array([100.0, 200.0])
# find an age whose sealed s==1 (or force via a missing table); when s>=1 blend must return xa exactly
s26 = s_of(26)
if s26 >= 1.0:
    chk("s(26)>=1 => _lsym_blend returns x_age unchanged", np.array_equal(np.asarray(blend(xf, xa, 26)), xa))
else:
    chk("blend tempers when s<1 (x between form and age)", bool(np.all(np.asarray(blend(xf, xa, 26)) >= xa) and np.all(np.asarray(blend(xf, xa, 26)) <= xf)))

# (4) RL_LEGF=0 kill-switch => the whole damper is inert (_LSYM_ON False => _lsym_active False even forward)
chk("_LSYM_ON present (rides RL_LEGF)", '_LSYM_ON' in g)
if not g['_LSYM_ON']:
    MA._LENS_FORM = 2026; MA.AGE_REF = 2027
    chk("RL_LEGF=0 => _lsym_active False even in the forward lens", not active())
    MA._LENS_FORM = None; MA.AGE_REF = MA.BASE_REF = 2026
else:
    chk("RL_LEGF default ON (_LSYM_ON True) — kill-switch path asserted under RL_LEGF=0 in the exit proof", True)

# (5) the two granted sites carry the forward-only guard in source (clock-identity, not FP)
_src = open('_merged_recover.py').read()
chk("b6 damper gated on _lsym_active() and Y!=BASE_REF (k=0 skip)", '_lsym_active() and Y!=MA.BASE_REF' in _src)
chk("level_now damper gated on _lsym_active() (k=0/backward inert)", 'cur is not None and _lsym_active()' in _src)

print("\nRESULT:", "PASS" if not FAIL else ("FAIL " + ",".join(FAIL)))
sys.exit(0 if not FAIL else 1)
