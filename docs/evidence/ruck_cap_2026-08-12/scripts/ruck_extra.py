"""ORDER 20C — the two per-ruck readings engine_probe.py does not carry.

engine_probe.py is reused BYTE-IDENTICAL from ORDER 20B, so it is not edited to add fields. This
sibling emits, for every real RUCK row, the two quantities the classification's SUPPORTING reading
needs and nothing else:

  bestlvl(p,2026)   the era-normalized peak production the engine can price. `_ruc_ceiling` (:1216)
                    falls back to `RUC_PRIOR_CAP·_cap_basis·_ruc_head_v0` — i.e. the ruck cap becomes
                    his ev() ceiling — ONLY when this is <= 0.
  ruc_ceiling       `_ruc_ceiling(p,2026)` itself, the ev():2237 ceiling, so the ONE national channel
                    through which the cap can reach a board price is on the record per player.

Plus `_cap_basis`, `_ruc_head_v0` and the V0 ceiling, so the scaffold cap can be recomputed by hand.

Run: RL_REPO=<tree> OUT=<path.json> python3 ruck_extra.py
"""
import os, sys, io, json, contextlib

REPO = os.environ['RL_REPO']
OUT = os.environ.get('OUT', '/tmp/ruck_extra.json')
sys.path.insert(0, REPO + '/vendor')
os.chdir(REPO + '/engine/rl_after'); sys.path.insert(0, '.'); sys.path.insert(0, REPO)

_src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_o20c_ruck_extra'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, G)

MA = G['MA']; cp = G['cp']
_isreal = G['_isreal']; bestlvl = G['bestlvl']; _ruc_ceiling = G['_ruc_ceiling']
_cap_basis = G['_cap_basis']; _ruc_head_v0 = G['_ruc_head_v0']; RUC_PRIOR_CAP = G['RUC_PRIOR_CAP']
_v0_uncapped = G['_v0_uncapped']; _v0_raw = G['_v0_raw']; v0_start = G['v0_start']
_V0CURVE = G['_V0CURVE']; _v0key = G['_v0key']; _nqual = G['_nqual']

back = list(G.get('back_extra') or MA.__dict__.get('back_extra') or [])
ROWS = [('active', p) for p in MA.players] + [('back', p) for p in back]

rows = []
for src, p in ROWS:
    if not (_isreal(p) and MA.gfut(p) == 'RUCK'):
        continue
    r = {'set': src, 'key': p.get('key'), 'name': p.get('player'), 'ty': p.get('type'),
         'ep': MA.effpk(p), 'pool': bool(MA.is_pool(p))}
    def g(fn, *a):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                return float(fn(*a))
        except Exception:
            return None
    r['bestlvl26'] = g(bestlvl, p, 2026)
    r['ruc_ceiling26'] = g(_ruc_ceiling, p, 2026)
    r['cap_basis'] = g(_cap_basis, p)
    r['ruc_head_v0'] = g(_ruc_head_v0, p)
    r['v0_ceiling'] = (RUC_PRIOR_CAP * r['cap_basis'] * r['ruc_head_v0']
                       if None not in (r['cap_basis'], r['ruc_head_v0']) else None)
    r['v0_uncapped'] = g(_v0_uncapped, p)
    r['v0_raw'] = g(_v0_raw, p)
    r['v0_start'] = g(v0_start, p)
    # THE STRUCTURAL FACT THE CLASSIFICATION RESTS ON: is this row's v0_start served by the FROZEN D14
    # curve (cap can never reach it) or by the fallback to the CAPPED _v0_raw?
    r['in_v0curve'] = bool(_v0key(p) in _V0CURVE)
    try: r['nqual26'] = int(_nqual(p, 2026))
    except Exception: r['nqual26'] = None
    try: r['age26'] = float(cp._age_asof(p, 2026))
    except Exception: r['age26'] = None
    rows.append(r)

json.dump({'repo': REPO, 'RUC_PRIOR_CAP': RUC_PRIOR_CAP, 'rows': rows}, open(OUT, 'w'))
sys.stderr.write('RUCK_EXTRA OK %s rows=%d\n' % (OUT, len(rows)))
