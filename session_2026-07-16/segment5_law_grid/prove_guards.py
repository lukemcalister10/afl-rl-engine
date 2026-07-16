#!/usr/bin/env python3
"""Dev-shell PROOF that the two suite-wired guards (L-RECENCY R105.5 + ρ forbidden-list R105.4) PASS against
the flipped engine (UNCOMP_DECAY=0.25). Mirrors the one_source_selftest.py block byte-for-byte in logic;
run in the workspace with the edited engine seeded. Exits non-zero if any guard fails."""
import io, os, contextlib, ast
HERE = os.path.dirname(os.path.abspath(__file__))
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']
import json
store = json.load(open('rl_model_data.json'))
FAIL = []
def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond: FAIL.append(msg)
def hp(*p): return os.path.join(os.getcwd(), *p)

_rho_out = g['rho_out']; _d = float(MA.UNCOMP_DECAY)
print("UNCOMP_DECAY in the seeded engine = %.4f" % _d)
_bs = sorted({2026 - x['year'] for p in store for x in (p.get('scoring') or []) if (x.get('games',0) or 0) > 0})
check(0.0 < _d <= 1.0, "L-RECENCY: decay d in (0,1] (d=%.4f)" % _d)
check(len(_bs) >= 2, "L-RECENCY: store spans >=2 distinct years-back (range %d..%d)" % (_bs[0], _bs[-1]))
_wpg = [_d**_b for _b in _bs]
check(all(_wpg[i] >= _wpg[i+1]-1e-15 for i in range(len(_wpg)-1)),
      "L-RECENCY: declared kernel d^yearsback non-increasing over %d..%d" % (_bs[0], _bs[-1]))
_pos = sorted(MA.REPL)[0]; _repl = MA.REPL[_pos]; _A, _B = 10.0, 20.0
_rec = []; _probe_ok = True
for _b in [b for b in _bs if b >= 1]:
    _synth = {'scoring':[{'year':2026,'games':1,'avg':_repl+_A},{'year':2026-_b,'games':1,'avg':_repl+_B}]}
    _r = _rho_out(_synth, _pos)
    if _r is None or not (_A < _r < _B): _probe_ok = False; break
    _rec.append((_b, (_r-_A)/(_B-_r)))
check(_probe_ok and len(_rec) >= 1, "L-RECENCY: engine rho_out evaluates the 2-season synthetic across the range")
if _probe_ok and _rec:
    check(all(w > 0.0 for _, w in _rec), "L-RECENCY: engine per-game weight POSITIVE every years-back")
    check(all(_rec[i][1] >= _rec[i+1][1]-1e-12 for i in range(len(_rec)-1)),
          "L-RECENCY: engine rho_out per-game weight NON-INCREASING in years-back")
    check(all(abs(w - _d**b) <= 1e-9 + 1e-6*(_d**b) for b, w in _rec),
          "L-RECENCY: recovered weight == d^yearsback exactly (games-independent)")
    print("   recovered kernel (yearsback: weight): " + ", ".join("%d:%.6g" % (b, w) for b, w in _rec[:8]) + (" ..." if len(_rec) > 8 else ""))

_rho_fn = next((n for n in ast.walk(ast.parse(open(hp('_merged_recover.py')).read()))
                if isinstance(n, ast.FunctionDef) and n.name == 'rho_out'), None)
check(_rho_fn is not None, "R105.4: rho_out present in the engine source")
if _rho_fn is not None:
    _fb = _rho_fn.body
    if _fb and isinstance(_fb[0], ast.Expr) and isinstance(getattr(_fb[0], 'value', None), ast.Constant) and isinstance(_fb[0].value.value, str):
        _fb = _fb[1:]
    _mod = ast.Module(body=list(_fb), type_ignores=[])
    _bad_floor = []
    for _n in ast.walk(_mod):
        if isinstance(_n, ast.Compare):
            _dump = ast.dump(_n)
            if 'games' in _dump or '_gm' in _dump:
                for _c in ast.walk(_n):
                    if isinstance(_c, ast.Constant) and isinstance(_c.value, (int, float)) and _c.value not in (0, 0.0):
                        _bad_floor.append((ast.dump(_n), _c.value))
    check(not _bad_floor, "R105.4: rho_out compares games only to 0 — NO games floor (offenders=%s)" % (_bad_floor[:2]))
    _forb = ('qualif','floor','exclud','exclus','phase','classif','interrupt','delist')
    _idents = set(); _strs = []
    for _n in ast.walk(_mod):
        if isinstance(_n, ast.Name): _idents.add(_n.id.lower())
        if isinstance(_n, ast.Attribute): _idents.add(_n.attr.lower())
        if isinstance(_n, ast.Constant) and isinstance(_n.value, str): _strs.append(_n.value.lower())
    _hit = sorted({t for t in _forb if any(t in i for i in _idents) or any(t in s for s in _strs)})
    check(not _hit, "R105.4: rho_out executable code carries no forbidden token (offenders=%s)" % _hit)

import sys
print("\n" + ("GUARD PROOF FAILED: %d" % len(FAIL) if FAIL else "GUARD PROOF PASSED: L-RECENCY + ρ forbidden-list hold at d=0.25"))
sys.exit(1 if FAIL else 0)
