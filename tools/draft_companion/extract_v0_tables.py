#!/usr/bin/env python3
"""tools/draft_companion/extract_v0_tables.py — the v0 tables the draft companion app reads. READ-ONLY.

Loads the engine once (the same day-0 load ui/tools/gen_v0_sidecar.py uses) and writes
tools/draft_companion/v0_tables.json:

  national[POS][AGE] = [v0 at pick 1 .. 64]   the frozen year-zero pick surface, _V0CURVE_META['_star'] —
                                              the exact function that prices every national draftee's v0
  pool_nd65          = v0 of a national pick past the curve (65+), the ND65+ signed level x board factor
  rookie[POS]        = rookie-draft v0, the positional RD level x board factor
  pathways[CODE]     = UNR / IRE / PDN (Next Gen) / PDA (Academy), flat signed level x board factor
  free_agents        = active board players with AFFL team "Free Agents" (name, club, positions, value)

Draft age, as the engine computes it for a draftee of draft year Y: max(Y - birth year, 18) (rl_model._age_at,
then _ageR). Pathway levels are flat across age (RL_B_SHAPE=0, owner ruling "B to flat").

PROOF before writing: for every active national-draft player on the board, the surface value at his
(future position, draft age, pick) must equal his published v0 in ui/data_aux/v0.js; for every active pool
entrant, level x board factor must equal his published v0; and the age rule must equal the engine's _ageR on
synthetic draftees. Any mismatch halts and nothing is written.

Run:  PATH=$HOME/rl_venv312/bin:$PATH python3 tools/draft_companion/extract_v0_tables.py
"""
import json, os, sys, hashlib, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'tools', 'draft_companion', 'v0_tables.json')
DRAFT_YEAR = 2026
POS = ['MID', 'SF', 'KPF', 'SD', 'KPD', 'RUCK']
AGES = list(range(18, 31))


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def main():
    sys.path.insert(0, os.path.join(ROOT, 'ui', 'tools'))
    import gen_v0_sidecar as G
    MA, ns = G.load_engine()
    star = ns['_V0CURVE_META']['_star']
    PL_F = float(ns['_PL_F'])
    LV = dict(MA._POOL_LEVELS)
    last = int(MA.ND_CURVE_LAST)

    # ---- the tables
    national = {p: {str(a): [round(float(star(p, a, k)), 1) for k in range(1, last + 1)] for a in AGES} for p in POS}
    rookie = {p: round(LV['RD:' + p] * PL_F, 1) for p in POS}
    pathways = {c: round(LV[c] * PL_F, 1) for c in ('UNR', 'IRE', 'PDN', 'PDA')}
    pool_nd65 = round(LV['ND65+'] * PL_F, 1)

    # ---- proofs against the published v0 sidecar
    sraw = open(os.path.join(ROOT, 'ui', 'data_aux', 'v0.js'), encoding='utf-8').read()
    side = json.loads(sraw[sraw.index('{', sraw.index('__V0__')):sraw.rindex('}') + 1])['byKey']
    board = json.load(open(os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')))
    active = {p['key'] for p in board['active']}
    bad, n_nat, n_pool = [], 0, 0
    for p in MA.data:
        k = p.get('key')
        if k not in active or k not in side or side[k].get('v0') is None:
            continue
        pub = side[k]['v0']
        if p.get('_pool') or MA.is_pool(p):
            got = int(round(float(MA.pool_level(p)) * PL_F)); n_pool += 1
        else:
            got = int(round(float(star(MA.gfut(p), int(ns['_ageR'](p)), p.get('pick'))))); n_nat += 1
        if got != pub:
            bad.append((k, pub, got))
    # the age rule on synthetic draftees of the draft year
    age_bad = []
    for by in range(1990, 2011):
        q = {'player': 'synthetic %d' % by, 'key': 'synthetic-%d' % by, 'year': DRAFT_YEAR, 'type': 'ND',
             'pick': 10, '_by': by, 'future_position': 'MID', 'scoring': [], 'games': 0}
        want = max(DRAFT_YEAR - by, 18)
        try:
            got = int(ns['_ageR'](q))
        except Exception as e:                                  # noqa: BLE001
            got = 'error %s' % e
        if got != want:
            age_bad.append((by, want, got))
    if bad or age_bad:
        print('PROOF FAILED — nothing written.')
        print('  v0 mismatches (key, published, recomputed):', bad[:20], '... total', len(bad))
        print('  age-rule mismatches (birth year, rule, engine):', age_bad)
        sys.exit(1)

    # ---- free agents on the live board (for the live AFFL draft tab)
    bv = open(os.path.join(ROOT, 'ui', 'data', 'board_view_working.js'), encoding='utf-8').read()
    bvo = json.loads(bv[bv.index('{', bv.index('=')):bv.rindex('}') + 1])
    fas = []
    for p in bvo['players']:
        if (p.get('affl_team') or '') == 'Free Agents':
            fas.append({'key': p.get('key'), 'name': p.get('name'), 'afl_club': p.get('afl_club'),
                        'pos': p.get('pos'), 'elig': p.get('elig'), 'v': p.get('v'), 'age': p.get('age')})
    fas.sort(key=lambda r: -(r['v'] or 0))
    store = json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')))
    affl = sorted({r['affl_team'] for r in store if r.get('affl_team') and r['affl_team'] != 'Free Agents'})
    afl = sorted({r['afl_club'] for r in store if r.get('afl_club') and not r.get('_retired')})

    boot = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
    doc = {
        'meta': {'generated': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                 'generator': 'tools/draft_companion/extract_v0_tables.py',
                 'board': boot.get('board'), 'store': boot.get('store'), 'engine_head': boot.get('engine_head'),
                 'draft_year': DRAFT_YEAR, 'board_factor': PL_F, 'curve_last_pick': last,
                 'age_rule': 'draft age = max(draft year - birth year, 18); surface clamps 16..30',
                 'proof': {'national_rows_matched': n_nat, 'pool_rows_matched': n_pool, 'age_rule_years': 21}},
        'positions': POS, 'ages': AGES,
        'national': national, 'pool_nd65': pool_nd65, 'rookie': rookie, 'pathways': pathways,
        'levels_ladder': {'ND65+': LV['ND65+'], 'UNR': LV['UNR'], 'IRE': LV['IRE'], 'PDN': LV['PDN'], 'PDA': LV['PDA'],
                          **{'RD:' + p: LV['RD:' + p] for p in POS}},
        'affl_clubs': affl, 'afl_clubs': afl, 'free_agents': fas,
    }
    json.dump(doc, open(OUT, 'w'), indent=1)
    print('PROOF OK: %d national + %d pool active players reproduce their published v0; age rule == engine on 21 '
          'birth years.' % (n_nat, n_pool))
    print('wrote', os.path.relpath(OUT, ROOT), '| pick 1 MID age 18 = %s, SF = %s | rookie MID %s | pool %s | %d free agents'
          % (national['MID']['18'][0], national['SF']['18'][0], rookie['MID'], pool_nd65, len(fas)))


if __name__ == '__main__':
    main()
