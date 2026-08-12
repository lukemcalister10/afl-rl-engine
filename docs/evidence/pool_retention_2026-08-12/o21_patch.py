#!/usr/bin/env python3
"""ORDER 21 -- THE STAGING PATCH. Applied to a SCRATCHPAD WORKTREE ONLY, before the identity
restamp, so every boot guard stays armed and the built board's engine identity records the patch.
THE CHECKOUT'S engine/rl_after/_merged_recover.py IS NEVER WRITTEN BY THIS SCRIPT.

  usage: o21_patch.py <worktree> <mode> <surface.json>

modes
  derived        THE STAGED CONFIGURATION. Both pool read sites replaced by the ONE derived object:
                   sitout_ev (ns==0, a SITTER by the derivation's own definition) -> R_derived(pathway,cls,tau)
                   _a_blend  (ns>=1, a NON-SITTER by that same definition)        -> U_pathway (the uplift)
  derived_sit    disclosed sensitivity: the derived R at sitout_ev ONLY; _a_blend keeps the national read.
  liftR          ORDER 19 VARIANT B, replicated on the adopted engine: R := 1.0 for pool rows at sitout_ev.
  liftRboth      ORDER 19's disclosed second-site sensitivity: R := 1.0 for pool rows at BOTH sites.

Everything is p.get('_pool')-gated. NATIONAL ROWS READ THE NATIONAL SURFACE AT BOTH SITES, UNTOUCHED.
"""
import sys, json, pathlib

wt, mode, surf_path = sys.argv[1], sys.argv[2], sys.argv[3]
f = pathlib.Path(wt + '/engine/rl_after/_merged_recover.py')
src = f.read_text()

SITE_SIT = "    R=_R_surf(_sitout_cls(MA.gfut(p)), MA.effpk(p), tau)     # D13 ASK3"
SITE_A = "    R=_R_surf(_sitout_cls(MA.gfut(p)),MA.effpk(p),tau)"
ANCHOR_DEF = "def _sitout_cls(pos): return 'RUCK' if pos=='RUCK' else ('KPP' if pos in ('KPF','KPD') else 'nonKPP')"

if mode in ('liftR', 'liftRboth'):
    NEW = ("    if p.get('_pool'): R=1.0                                 "
           "# ORDER 19 variant replication (MEASUREMENT ONLY, staged copy).\n")
    sites = [SITE_SIT] + ([SITE_A] if mode == 'liftRboth' else [])
    for OLD in reversed(sites):
        assert src.count(OLD) == 1, "anchor not unique (%r): %d" % (OLD[:40], src.count(OLD))
        i = src.index(OLD); j = src.index("\n", i) + 1
        src = src[:j] + NEW + src[j:]
    f.write_text(src)
    print("  PATCHED %d site(s): R := 1.0 for pool rows" % len(sites))
    sys.exit(0)

S = json.load(open(surf_path))
PATH = S['pathway']
WHOLE = S['whole_pool']
U = S['uplift']
U_ALL = S['mean_preserving']['ALL POOL']['U']

BLOCK = '''
# ===== ORDER 21 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL HISTORY (STAGED; NOT LANDED) ========
# Owner ruling, directive D8 (comment 5253173347): "the pool sitter on top penalty should go, and the
# pool index should be rederived in the same way the ND one is where possible not for pick 65, but for
# the pool" + "They're all part of the pool ... rookie draft pick 1 and 30 are the same" (NO PICK AXIS).
# Derivation: docs/evidence/pool_retention_2026-08-12/pool_retention_derive.py (the d13 ND method,
# departures D1-D7 declared in PREREG_ORDER21.md). H_POOLSIT / H_UNION are RETIRED to 1.0 alongside.
# THE ONE DERIVED OBJECT, AT BOTH READ SITES, BY CONSTRUCTION AND NOT BY ACCIDENT:
#   sitout_ev  fires iff ns==0  == a SITTER by the derivation's own definition  -> R_derived < 1
#   _a_blend   fires iff ns>=1  == a NON-SITTER by that same definition         -> U_pathway > 1
# The two engine sites partition the pool population on exactly the variable the derivation splits on,
# so the mean-preserving pair covers both. U>1 IS A LIFT and is intentional: the owner's D8 amendment
# requires the sitter differential to REDISTRIBUTE inside the pathway, never to be a net charge.
# EVERY SITE IS p.get('_pool')-GATED. National rows read the national surface unchanged at both sites.
_PR_PATH=__PATHSURF__
_PR_WHOLE=__WHOLE__
_PR_U=__UPLIFT__
_PR_U_ALL=__UALL__
def _pr_pathway(p):
    t=p.get('type')
    if t=='ND': return 'ND>64'
    return t if t in _PR_PATH else None
def _pr_R(p,tau):
    """the derived pool retention: pathway x class x depth, isotonic non-increasing, tau=0 -> 1.0"""
    cls=_sitout_cls(MA.gfut(p)); pw=_pr_pathway(p)
    dv=(_PR_PATH[pw][cls] if pw else _PR_WHOLE[cls])
    return float(np.interp(tau,[0,1,2,3,4,5,6],[1.0]+list(dv)))
def _pr_U(p):
    """the mean-preserving uplift the pathway's NON-sitters carry (entry-weighted mean == 1 exactly)"""
    pw=_pr_pathway(p)
    return float(_PR_U[pw] if pw else _PR_U_ALL)
# ===================================================================================================
'''
BLOCK = (BLOCK.replace('__PATHSURF__', json.dumps(PATH))
              .replace('__WHOLE__', json.dumps(WHOLE))
              .replace('__UPLIFT__', json.dumps(U))
              .replace('__UALL__', repr(float(U_ALL))))

assert src.count(ANCHOR_DEF) == 1, "definition anchor not unique"
i = src.index(ANCHOR_DEF); j = src.index("\n", i) + 1
src = src[:j] + BLOCK + src[j:]

nsite = 0
if mode == 'derived':
    assert src.count(SITE_A) == 1, "a_blend anchor not unique"
    i = src.index(SITE_A); j = src.index("\n", i) + 1
    src = src[:j] + ("    if p.get('_pool'): R=_pr_U(p)                            "
                     "# ORDER 21: the year-1+ arm is a NON-SITTER by definition -> the uplift.\n") + src[j:]
    nsite += 1

assert src.count(SITE_SIT) == 1, "sitout_ev anchor not unique"
i = src.index(SITE_SIT); j = src.index("\n", i) + 1
src = src[:j] + ("    if p.get('_pool'): R=_pr_R(p,tau)                        "
                 "# ORDER 21: the sit-out arm is a SITTER by definition -> the derived retention.\n") + src[j:]
nsite += 1

f.write_text(src)
print("  PATCHED mode=%s: derived pool surface injected, %d read site(s) rebound" % (mode, nsite))
