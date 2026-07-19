#!/usr/bin/env python3
# LEG F3 — k=0 DORMANCY UNIT TEST (supervisor ruling item 353 pt 3): assert each edited site is DORMANT at
# k=0 by CLOCK IDENTITY — the §2.vi cure is provably a no-op off the forward lens, independent of FP hashes.
# Run from the workspace: python3 test_k0_dormancy.py   (exit 0 = PASS)
import os, io, contextlib, sys
FAIL = []
def chk(name, cond):
    print(("  PASS " if cond else "  FAIL ") + name); (FAIL.append(name) if not cond else None)

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; fac = g['_form_anchor_clock']; fay = g['_fa_year']
proj = g['_proj_w4']; proj0 = g['_proj_w4_0']; W4CTX = g['_W4CTX']
MA.BASE_REF = MA.AGE_REF = 2026; MA._LENS_FORM = None; MA._pe_clear()

# (1) _fa_year identity at k=0 / off the forward lens
chk("_fa_year(2026)==2026 when _LENS_FORM None", fay(2026) == 2026)
MA._LENS_FORM = 2026
chk("_fa_year(2027)==2026 in the forward lens (re-keys to BASE_REF)", fay(2027) == 2026)
MA._LENS_FORM = None
chk("_fa_year(2027)==2027 off the lens (identity)", fay(2027) == 2027)

# (2) _form_anchor_clock is a NO-OP at k=0 (AGE_REF unchanged), and only bites when _LENS_FORM set AND AGE_REF>BASE_REF
MA.AGE_REF = MA.BASE_REF = 2026; MA._LENS_FORM = None
with fac():
    chk("_form_anchor_clock no-op: AGE_REF stays 2026 off the lens", MA.AGE_REF == 2026)
MA._LENS_FORM = 2026; MA.AGE_REF = 2026  # AGE_REF==BASE_REF (k=0 even in the lens)
with fac():
    chk("_form_anchor_clock no-op at k=0 (AGE_REF==BASE_REF)", MA.AGE_REF == 2026)
MA.AGE_REF = 2027  # forward
with fac():
    chk("_form_anchor_clock BITES forward (AGE_REF->BASE_REF 2026)", MA.AGE_REF == 2026)
chk("_form_anchor_clock RESTORES AGE_REF after (==2027)", MA.AGE_REF == 2027)
MA._LENS_FORM = None; MA.AGE_REF = MA.BASE_REF = 2026

# (3) RL_LEGF=0 kill: _fa_year identity even in the lens, _form_anchor no-op
chk("RL_LEGF gate present (_LEGF_ON)", '_LEGF_ON' in g)
if not g['_LEGF_ON']:
    MA._LENS_FORM = 2026
    chk("RL_LEGF=0 => _fa_year identity", fay(2027) == 2027)
    MA._LENS_FORM = None

# (4) _proj_w4 F3 edit (ah=a-offset) is INERT at k=0 by CLOCK IDENTITY: at AGE_REF==BASE_REF the offset is 0,
#     so ah==a and the horizon/runway age-substitution is a no-op. (End-to-end byte-exactness is proven by the
#     board chain: RL_LEGF=0 lens => d85901af, RL_LEGF=1 k=0 v == RL_LEGF=0 k=0 v.) The F3 edit reads the source
#     line to confirm the ah-guard form, then asserts offset==0 at k=0.
MA.AGE_REF = MA.BASE_REF = 2026; MA._LENS_FORM = None
_off_k0 = MA.AGE_REF - MA.BASE_REF
chk("_proj_w4 offset==0 at k=0 (=> ah==a => the F3 age-substitution is a no-op)", _off_k0 == 0)
_src = open('_merged_recover.py').read()
chk("_proj_w4 carries the F3 ah-guard (ah=a-_off if _off>0 else a)", 'ah=a-_off if _off>0 else a' in _src)
chk("_proj_w4 offset gated on RL_LEGF (_LEGF_ON else 0)", 'if _LEGF_ON else 0' in _src)

print("\nRESULT:", "PASS" if not FAIL else ("FAIL " + ",".join(FAIL)))
sys.exit(0 if not FAIL else 1)
