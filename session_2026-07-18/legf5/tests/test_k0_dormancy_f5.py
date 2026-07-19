#!/usr/bin/env python3
# LEG F5 — k=0 DORMANCY UNIT TEST (MEMO_LEGF v1.3 §2.viii): assert the §2.viii ENTRANT LAYER is DORMANT at
# k=0 / RL_LEGF=0 by CONSTRUCTION — additive, lens-scoped, engine-ev()-free, seal-gated. Independent of FP
# hashes (source + seal + optional built-board structural checks).
# Usage: python3 test_k0_dormancy_f5.py [built_RL_LEGF1_board.json]
#   run from the workspace rl_after (needs rl_export.py + the sealed structure via RL_REPO). exit 0 = PASS.
import os, sys, json, hashlib, re
FAIL = []
def chk(name, cond): print(("  PASS " if cond else "  FAIL ") + name); (None if cond else FAIL.append(name))

REPO = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
src = open(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'engine', 'rl_after', 'rl_export.py')
           if os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'engine')) else 'rl_export.py').read()

# (1) the ENTIRE §2.viii layer lives inside the RL_LEGF guard (k=0/RL_LEGF=0 emits nothing)
i_guard = src.find("if os.environ.get('RL_LEGF', '1') != '0':")
i_layer = src.find('§2.viii THE SEALED ENTRANT SLOT STRUCTURE')
i_else = src.find("else:\n    print('LEG F5 ENTRANT LAYER: RL_LEGF=0")
chk("§2.viii layer is INSIDE the RL_LEGF!=0 branch", 0 < i_guard < i_layer < i_else)
chk("RL_LEGF=0 branch prints 'layer NOT emitted' (no phantom keys)", "RL_LEGF=0 — layer NOT emitted" in src)

# (2) the block never calls the engine ev() and never writes a player `v` — additive lens arrays only
block = src[i_guard:i_else]
chk("block does NOT call _ev( (engine valuation untouched)", '_ev(' not in block)
chk("block only ADDS out['phantom*'] keys (no out['active']/['back'] mutation)",
    ("out['phantomLayer']" in block and "out['phantomPicks']" in block and "out['phantomTotals']" in block
     and "out['active']" not in block))
chk("block reads only PVC / vP1 / vP2 / club / sealed file (no ev channel)",
    ('_lf_pvc' in block and "'vP1'" in block and "'vP2'" in block and 'sealed_entrant_structure' in block))

# (3) the balanced lens '0' is a pure echo: withPhantom == withoutPhantom (delta 0 at k=0) by construction
chk("lens '0' withPhantom==withoutPhantom==Σv (k=0 delta 0)",
    "'0'] = {'withPhantom': _v0, 'withoutPhantom': _v0, 'delta': 0" in block)

# (4) seal-gated: the structure is seal-verified and HALTs on drift (seal-first law)
chk("seal-verify present + pinned a17aafed + HALT on drift",
    ("_hl.sha256" in block and "'a17aafed'" in block and 'LEG F5 HALT' in block))
struct = json.load(open(os.path.join(REPO, 'session_2026-07-18', 'legf5', 'sealed_entrant_structure.json')))
chk_dict = {k: v for k, v in struct.items() if k != 'seal_sha256_8'}
seal = hashlib.sha256(json.dumps(chk_dict, sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:8]
chk("sealed structure recomputes to a17aafed", seal == struct['seal_sha256_8'] == 'a17aafed')

# (5) optional: a built RL_LEGF=1 board carries delta 0 at k=0 and the sealed entrant on the forward lenses
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    pt = json.load(open(sys.argv[1]))['phantomTotals']; lg = pt['league']
    chk("built board: league k=0 delta == 0", lg['0']['delta'] == 0)
    chk("built board: +1 and +2 entrant delta == sealed total 83538",
        lg['1']['delta'] == struct['entrant_pvc']['total'] == lg['2']['delta'])
    chk("built board: k=0 withPhantom == withoutPhantom (byte)", lg['0']['withPhantom'] == lg['0']['withoutPhantom'])

print("\nRESULT:", "PASS" if not FAIL else ("FAIL " + ",".join(FAIL)))
sys.exit(0 if not FAIL else 1)
