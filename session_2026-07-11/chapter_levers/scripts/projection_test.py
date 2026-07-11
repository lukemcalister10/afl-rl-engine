"""ACCEPTANCE — THE PROJECTION TEST (owner's test, directive 2026-07-11): project the levered board
6-7 years forward and report the future top-end positional mix. Young GDEFs vanishing = FAIL,
regardless of guards.

METHOD (declared; read-only, board JSON + the engine's OWN exported aging lens — no engine load):
  proj_H(p) = v_now * DELTAS[clip(age + H - PEAK_AGE[gf])] / DELTAS[clip(age - PEAK_AGE[gf])]
using the board's exported PEAK_AGE (per position) and DELTAS (years-from-peak value fractions,
-8..+14 — the engine's own aging curve). Players projected past DELTAS[+14] or age 34+ are treated
as RETIRED (excluded) — today's veterans age out of the projected top end exactly as the owner's
"project the DB forward" framing implies. The projector deliberately does NOT re-inflate anyone's
value beyond the board's own age curve: every position rides the same lens, so the POSITIONAL MIX of
the projected top end is an apples-to-apples read of what the board believes matures. Run on BOTH the
base candidate board (8f3675f3) and the LEVERED board (9ecbe0fa) — the delta shows what the L1
transition credit does to the projected defender top end.
Usage: python3 projection_test.py <base_board.json> <levered_board.json>
"""
import json, sys

base_p, lev_p = sys.argv[1], sys.argv[2]
OUT = '/home/user/afl-rl-engine/session_2026-07-11/chapter_levers/out/projection_test.json'
res = {'doc': __doc__}

def project(board_path, H):
    b = json.load(open(board_path))
    D = {int(k): v for k, v in b['DELTAS'].items()}
    PA = b['PEAK_AGE']
    rows = []
    for p in b['active']:
        age, gf = p['age'], p['gf']
        if age + H >= 34: continue
        k0 = max(-8, min(14, age - PA[gf])); k1 = age + H - PA[gf]
        if k1 > 14: continue
        k1 = max(-8, k1)
        rows.append(dict(key=p['key'], gf=gf, age_then=age + H, cg=p['cg'],
                         v_now=p['v'], v_proj=round(p['v'] * D[k1] / D[k0])))
    rows.sort(key=lambda r: -r['v_proj'])
    return rows

for H in (6, 7):
    for tag, path in (('base', base_p), ('levered', lev_p)):
        rows = project(path, H)
        for N in (20, 50):
            mix = {}
            for r in rows[:N]: mix[r['gf']] = mix.get(r['gf'], 0) + 1
            res[f'H{H}/{tag}/top{N}_mix'] = mix
        res[f'H{H}/{tag}/gdef_in_top50'] = [(r['key'], r['v_proj'], r['age_then'], ('young-now' if r['cg'] < 46 else 'estab-now'))
                                            for r in rows[:50] if r['gf'] == 'GEN_DEF']
        if tag == 'levered':
            res[f'H{H}/levered/top20'] = [(r['key'], r['gf'], r['v_proj'], r['age_then']) for r in rows[:20]]

# verdict: young-now GDEFs must be PRESENT in the projected top-50 on the levered board at both horizons
young_gdef = {H: [k for k, v, a, tag in res[f'H{H}/levered/gdef_in_top50'] if tag == 'young-now'] for H in (6, 7)}
res['verdict'] = ('PASS — young-now GDEFs present in the projected top-50 at both horizons: %s' % young_gdef) \
    if all(young_gdef.values()) else ('FAIL — young GDEFs vanish from the projected top end: %s' % young_gdef)
json.dump(res, open(OUT, 'w'), indent=1)

for H in (6, 7):
    print(f'--- horizon +{H} (board year {2026+H}) ---')
    for tag in ('base', 'levered'):
        print(f'  {tag:8s} top20 mix: {res[f"H{H}/{tag}/top20_mix"]}   top50 mix: {res[f"H{H}/{tag}/top50_mix"]}')
    print(f'  GDEFs in levered top-50: {res[f"H{H}/levered/gdef_in_top50"]}')
print('\nVERDICT:', res['verdict'])
print('wrote', OUT)
