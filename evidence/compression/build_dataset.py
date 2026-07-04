#!/usr/bin/env python3
"""
build_dataset.py  [BAKED c47cb43d]  READ-ONLY

Extracts a clean per-player table from the baked board
  data/s4_matrix_baked_c47cb43d.json
and attaches era-normalised production, pulling the engine's own `era`/`REF`
constants (frozen engine md5 c47cb43d) so the realised-outcome reference is
built on the SAME era scale the engine uses. No engine mutation, no bake.

Value field
-----------
The board carries the engine valuation trajectory per player:
  Vpath[]  engine value by season   -> anchor = Vpath[0] (entry), cur = Vpath[-1] (now)
  Ppath[]  production (fantasy avg) by season, same index as yrs[]
We take the engine value V := `cur` (the live keeper value the owner ranks on),
and peakV := max(Vpath). Production R is era-normalised Ppath.

Output: dataset.json  (list of records) + era.json
"""
import io, contextlib, json, os, sys

BOARD = '/home/user/afl-rl-engine/data/s4_matrix_baked_c47cb43d.json'
OUT   = os.path.join(os.path.dirname(__file__), 'dataset.json')
ERAJS = os.path.join(os.path.dirname(__file__), 'era.json')

# --- pull era / REF from the frozen engine (read-only) -----------------------
sys.path.insert(0, '/home/claude/rl_vendor')
os.chdir('/home/claude/rl_workspace/rl_after')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
era = {int(k): float(v) for k, v in g['era'].items()}
REF = float(g['REF'])
ENGINE_MD5 = None
import hashlib
ENGINE_MD5 = hashlib.md5(open('_merged_recover.py', 'rb').read()).hexdigest()[:8]
assert ENGINE_MD5 == 'c47cb43d', f"engine md5 {ENGINE_MD5} != c47cb43d"

def era_norm(avg, year):
    """era-normalise a season avg to the engine's REF scale."""
    e = era.get(int(year), REF)
    return avg * REF / e if e else avg

# --- read board --------------------------------------------------------------
board = json.load(open(BOARD))
recs = []
for oid, r in board.items():
    yrs   = r.get('yrs') or []
    Vpath = r.get('Vpath') or []
    Ppath = r.get('Ppath') or []
    # era-normalise every season's production
    Pn = [era_norm(p, y) for p, y in zip(Ppath, yrs)]
    peakV = max(Vpath) if Vpath else r.get('cur', 0)
    peakP = max(Pn) if Pn else 0.0
    # recent production = mean of era-normalised last-2 seasons that were real
    recentP = (sum(Pn[-2:]) / len(Pn[-2:])) if Pn else 0.0
    # career output proxy = sum of era-normalised season avgs (season-weighted realised production)
    careerP = float(sum(Pn))
    nseas = len(Pn)
    recs.append(dict(
        player=r['player'], cpos=r.get('cpos'), pos=r.get('pos'),
        pick=r.get('pick'), pickless=r.get('pickless'), year=r.get('year'),
        type=r.get('type'), draftval=r.get('draftval'),
        cur=r.get('cur'), anchor=r.get('anchor'), peakV=peakV,
        peakP=round(peakP, 2), recentP=round(recentP, 2), careerP=round(careerP, 2),
        lastP=round(Pn[-1], 2) if Pn else 0.0,
        nseas=nseas, retired_now=r.get('retired_now'), incurve=r.get('incurve'),
        sat_out_yr1=r.get('sat_out_yr1'),
    ))

json.dump(recs, open(OUT, 'w'))
json.dump({'era': era, 'REF': REF, 'engine_md5': ENGINE_MD5}, open(ERAJS, 'w'), indent=1)
print(f"[BAKED c47cb43d] engine md5={ENGINE_MD5}  players={len(recs)}  era yrs={min(era)}..{max(era)} REF={REF:.1f}")
print(f"wrote {OUT}  and {ERAJS}")
