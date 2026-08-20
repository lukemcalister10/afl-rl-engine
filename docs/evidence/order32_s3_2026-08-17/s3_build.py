#!/usr/bin/env python3
"""ORDER 32 SEAT S3 — dataset builder. READ-ONLY: reads Layer 1 + LAYER2 (validation only) + store.

Replicates the Layer-2 season scorer in pure python (constants read from LAYER2.json::cfg and
rl_model.py's published rules), VALIDATES it against LAYER2.json::base[key].obs under the flat-14
discount (gate: <=1e-6 rel err on >=99% of careers), then emits one row per focal player-season
(k=1..3, entry 2004-2021, played seasons only) with outcomes Y1/Y5/Yrc and controls.

Outputs (evidence dir): DATASET_S3.json, VALIDATE_S3.txt
"""
import os, sys, json, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
IN = os.path.join(ROOT, 'docs/evidence/grace_adoption_2026-08-13/inputs')

L1 = json.load(open(os.path.join(IN, 'layer1_player_seasons.json')))
L2 = json.load(open(os.path.join(IN, 'LAYER2.json')))
STORE = json.load(open(os.path.join(ROOT, 'engine/rl_after/rl_model_data.json')))
CFG = L2['cfg']

SCALE = float(CFG['scale'])            # 1.4398232006949683
BARS = {k: float(v) for k, v in CFG['bars'].items()}
S_SH = float(CFG['s_sh'])              # 3.0
DISC = 1.0 + float(CFG['disc_rate'])   # 1.14 flat
# capt_prem — the ruled L-CAPTAIN curve, constants verbatim from engine/rl_after/rl_model.py
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00

def softplus(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt_prem(lev):
    c = LCAPT_G * LCAPT_W * (softplus((lev - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0.0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def w_sqrt(g): return min(1.0, math.sqrt(max(0.0, g) / 10.0))

# ---- the engine's season-bar rule (rl_model.py::_fit_bar 99-104), replicated with its own maps ----
GRP = {'MID': 'MID', 'RUCK': 'RUCK', 'SF': 'SF', 'KPF': 'KPF', 'SD': 'SD', 'KPD': 'KPD'}
REPL = {'MID': 80.1, 'SD': 78.3, 'RUCK': 78.5, 'KPD': 68.4, 'SF': 70.9, 'KPF': 66.8}
def collapse_elig(elig):
    if not elig: return set()
    s = {GRP.get(t.strip().upper()) for t in str(elig).split(',') if t.strip()}
    s.discard(None)
    if 'KPF' in s: s.discard('SF')
    if 'KPD' in s: s.discard('SD')
    return s

BYKEY = {}
for p in STORE:
    kk = p.get('key')
    if kk and kk not in BYKEY: BYKEY[kk] = p

def decl_bar(p):
    es = collapse_elig(p.get('eligibilities'))
    if es: return min(es, key=lambda g: REPL[g])
    pn = GRP.get(p.get('present_position')) or GRP.get(p.get('drafted_position'))
    return pn

def season_bar_group(pos_label, p):
    if pos_label:
        es = collapse_elig(str(pos_label).replace('/', ','))
        if es: return min(es, key=lambda g: REPL[g]), 'row'
    if p is not None:
        g = decl_bar(p)
        if g: return g, 'decl_fallback'
    return None, 'unresolved'

def season_pts(avg, games, pos):
    """UNDISCOUNTED delivered board points for one season."""
    x = avg + capt_prem(avg) - BARS[pos]
    return SCALE * posval(x) * 21.0 * w_sqrt(games)

# ==================================================================================================
# VALIDATION GATE — reproduce LAYER2 base[key].obs (flat-14 discounted to acquisition)
# ==================================================================================================
E = {e['key']: e for e in L1['entries']}
SEAS = collections.defaultdict(list)
for s in L1['player_seasons']:
    SEAS[s['key']].append(s)
for k in SEAS: SEAS[k].sort(key=lambda x: x['year'])

rep = []
nok = nbad = 0
bad_names = []
for key, e in E.items():
    ey = e['entry_year']; ea = e['entry_age']
    if ea is None: ea = e['entry_age_fallback_if_null']
    tot = 0.0
    p = BYKEY.get(key)
    for s in SEAS.get(key, []):
        pos, how = season_bar_group(s['position_played'], p)
        if pos is None or pos not in BARS: continue
        kk = (s['year'] - ey) if ey is not None else 0
        d = DISC ** kk if kk > 0 else 1.0
        tot += season_pts(s['avg'], s['games'], pos) / d
    ref = L2['base'].get(key, {}).get('obs')
    if ref is None: continue
    denom = max(1.0, abs(ref))
    if abs(tot - ref) / denom <= 1e-6: nok += 1
    else:
        nbad += 1
        if len(bad_names) < 25: bad_names.append((key, ref, tot))
gate_pass = nok / max(1, nok + nbad) >= 0.99
with open(os.path.join(HERE, 'VALIDATE_S3.txt'), 'w') as f:
    f.write('VALIDATION GATE — replica season scorer vs LAYER2 base.obs (flat-14 to acquisition)\n')
    f.write('careers ok %d  bad %d  frac_ok %.6f  gate(>=0.99) %s\n' % (nok, nbad, nok / max(1, nok + nbad), 'PASS' if gate_pass else 'FAIL'))
    for b in bad_names: f.write('  MISMATCH %s ref %.6f mine %.6f\n' % b)
print('validation ok %d bad %d -> %s' % (nok, nbad, 'PASS' if gate_pass else 'FAIL'))
if not gate_pass: sys.exit('GATE FAILED — stopping per prereg §3')

# ==================================================================================================
# ATTRIBUTION — force-majeure slide, verbatim rule from o26b_layer2.py::attribute
# ==================================================================================================
FM_KEYS = {'thomas-boyd', 'paddy-mccartin'}
FM_YEARS = {2013, 2014}
def attribute(e):
    key, ty, yr, pk = e['key'], e['type'], e['entry_year'], e['pick']
    if key in FM_KEYS: return None
    slid = False
    if ty == 'ND' and yr in FM_YEARS and pk:
        pk = pk - 1; slid = True
    mech = e['mechanism']
    if ty == 'ND':
        mech = 'ND 1-64' if (pk and 1 <= pk <= 64) else 'ND>64'
    return dict(mechanism=mech, pick=pk, slid=slid)

def band(mech, pick):
    if mech == 'ND 1-64':
        for lo, hi in ((1, 10), (11, 20), (21, 30), (31, 40), (41, 64)):
            if lo <= pick <= hi: return 'ND%d-%d' % (lo, hi)
    if mech == 'ND>64': return 'ND>64'
    return mech   # each pool pathway its own cell

# ==================================================================================================
# FOCAL ROWS
# ==================================================================================================
rows = []
cnt = collections.Counter()
for key, e in E.items():
    ey = e['entry_year']
    if ey is None or not (2004 <= ey <= 2021): cnt['excl_window'] += 1; continue
    at = attribute(e)
    if at is None: cnt['excl_force_majeure'] += 1; continue
    ea = e['entry_age']
    if ea is None: ea = e['entry_age_fallback_if_null']
    p = BYKEY.get(key)
    seasons = SEAS.get(key, [])
    by_year = {int(s['year']): s for s in seasons}
    # per-season resolved (pos, pts, surplus) map — 2026 rows kept for outcome exclusion logic only
    res = {}
    for s in seasons:
        pos, how = season_bar_group(s['position_played'], p)
        if pos is None or pos not in BARS: cnt['season_no_bar'] += 1; continue
        res[int(s['year'])] = dict(games=float(s['games']), avg=float(s['avg']), pos=pos,
                                   surplus=float(s['avg']) - BARS[pos],
                                   pts=season_pts(s['avg'], s['games'], pos))
    for kfoc in (1, 2, 3):
        fy = ey + kfoc
        r = res.get(fy)
        if r is None: cnt['focal_k%d_noplay' % kfoc] += 1; continue
        if fy >= 2026: cnt['focal_in_progress_2026'] += 1; continue
        prior_g = sum(res[y]['games'] for y in res if y < fy)
        # outcomes
        y1 = None
        if fy <= 2024:
            y1 = res.get(fy + 1, {}).get('pts', 0.0)
        y5 = None; g5 = None; s5w = None
        if fy <= 2020:
            y5 = sum(res.get(fy + j, {}).get('pts', 0.0) for j in range(1, 6))
            g5 = sum(res.get(fy + j, {}).get('games', 0.0) for j in range(1, 6))
            num = sum(res.get(fy + j, {}).get('surplus', 0.0) * res.get(fy + j, {}).get('games', 0.0)
                      for j in range(1, 6))
            s5w = (num / g5) if g5 and g5 > 0 else None
            # flat-14 discounted-to-focal variant
            y5d = sum(res.get(fy + j, {}).get('pts', 0.0) / (DISC ** j) for j in range(1, 6))
        else:
            y5d = None
        yrc = None
        if e['retired']:
            yrc = sum(v['pts'] for y, v in res.items() if y > fy)
        rows.append(dict(
            key=key, k=kfoc, focal_year=fy, entry_year=ey, entry_age=ea, age=None if ea is None else ea + kfoc,
            mech=at['mechanism'], pick=at['pick'], band=band(at['mechanism'], at['pick']),
            pos=r['pos'], games=r['games'], avg=r['avg'], surplus=r['surplus'], focal_pts=r['pts'],
            prior_games=prior_g, draft_club=e.get('draft_club'), retired=bool(e['retired']),
            y1=y1, y5=y5, y5d=y5d, g5=g5, s5w=s5w, yrc=yrc))

out = dict(_doc=dict(built_by='docs/evidence/order32_s3_2026-08-17/s3_build.py',
                     prereg='PREREG_S3.md (committed 096a339, before results)',
                     validation='VALIDATE_S3.txt — gate PASS required before this file exists',
                     units='delivered board points, UNDISCOUNTED unless suffixed d (flat-14 to focal)',
                     exclusions=dict(cnt)),
           rows=rows)
json.dump(out, open(os.path.join(HERE, 'DATASET_S3.json'), 'w'))
print('rows %d' % len(rows))
print(json.dumps(dict(cnt), indent=1))
kc = collections.Counter(r['k'] for r in rows)
print('by k:', dict(kc))
print('k=1 with y5:', sum(1 for r in rows if r['k'] == 1 and r['y5'] is not None))
