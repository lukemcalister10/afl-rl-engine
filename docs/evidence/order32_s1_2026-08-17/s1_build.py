#!/usr/bin/env python
# ORDER 32 SEAT S1 — STEP 1: the season table.
# READ-ONLY: reads the store and season state, writes SEASON_TABLE.json + CENSUS_S1.txt into the
# evidence dir. No engine file is imported or touched (the gate's constants and tests are
# transcribed and cited; transcription checked against the source lines in the packet).
#
# Definitions per PREREG_S1.md (committed & pushed before this script ran):
#   AGE   = season year - _by  (owner convention: harry-dean 2026 -> 19)
#   POS   = future_position (the gate's own bar key gfut)
#   FULL  = games >= 10 (completed yrs) / >= 10*0.92 (2026)
#   OUTCOME1 delivered-later: any later season games>=10 & avg >= flat bar(POS)
#   OUTCOME2 SDV: sum over later seasons games*max(0, avg - flat bar(POS))
import json, os, hashlib, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STORE = os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')
OUT = os.path.dirname(os.path.abspath(__file__))

BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}  # _O30BP_BARS (Ruling 1)
SS = json.load(open(os.path.join(ROOT, 'data', 'season_state.json')))
FE26 = float(SS['calendar_progress'])          # 0.92 — the gate's _fEy(2026) for non-register rows
INPROG = int(SS['inprog_year'])                # 2026

d = json.load(open(STORE))
md5 = hashlib.md5(open(STORE, 'rb').read()).hexdigest()

rows = []
n_nofut = 0
for p in d:
    pos = p.get('future_position')
    if pos not in BARS:
        if any((x.get('games') or 0) > 0 for x in (p.get('scoring') or [])):
            n_nofut += 1
        continue
    by = p.get('_by')
    sc = sorted((p.get('scoring') or []), key=lambda r: r['year'])
    played = [x for x in sc if (x.get('games') or 0) > 0]
    for x in played:
        Y = x['year']; g = float(x['games']); a = float(x['avg'] or 0.0)
        age = Y - by
        u = FE26 if Y == INPROG else 1.0
        full = g >= 10.0 * u
        # subsequent-career outcomes (later seasons only, y > Y)
        later = [z for z in played if z['year'] > Y]
        delivered_later = any(float(z['games']) >= 10.0 * (FE26 if z['year'] == INPROG else 1.0)
                              and float(z['avg'] or 0.0) >= BARS[pos] for z in later)
        sdv = sum(float(z['games']) * max(0.0, float(z['avg'] or 0.0) - BARS[pos]) for z in later)
        rows.append(dict(key=p['key'], year=Y, age=age, pos=pos, games=g, avg=a,
                         season_pos=(x.get('pos') or pos).split('/')[0],
                         u=u, full=full, under_flat=a < BARS[pos],
                         delivered_later=delivered_later, sdv=round(sdv, 1),
                         n_later=len(later), last_played=played[-1]['year'],
                         retired=bool(p.get('_retired')), typ=p.get('type'), pick=p.get('pick')))

json.dump(dict(meta=dict(store_md5=md5, n_players=len(d), n_season_rows=len(rows),
                         fe26=FE26, bars=BARS, built='2026-08-17 ORDER32 S1 step1',
                         n_played_players_no_futpos_group=n_nofut),
               rows=rows),
          open(os.path.join(OUT, 'SEASON_TABLE.json'), 'w'))

# ---- census ----
L = []
P = L.append
P('ORDER 32 S1 STEP 1 CENSUS — store %s, %d players, %d played season rows' % (md5[:8], len(d), len(rows)))
P('played players excluded for future_position outside the six groups: %d' % n_nofut)
yrs = sorted(set(r['year'] for r in rows))
P('season years: %d..%d' % (yrs[0], yrs[-1]))
ages = collections.Counter(r['age'] for r in rows)
P('age range of played seasons: %d..%d' % (min(ages), max(ages)))

def band(age): return str(age) if 18 <= age <= 23 else ('<=17' if age < 18 else '24+')
ABANDS = ['<=17', '18', '19', '20', '21', '22', '23', '24+']
POSL = ['KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF']

for thr_name, cond in [('games>=1', lambda r: True),
                       ('games>=6', lambda r: r['games'] >= 6 * r['u']),
                       ('FULL (gate games test, >=10u)', lambda r: r['full'])]:
    P('')
    P('SEASONS BY AGE x POS — %s' % thr_name)
    P('%-6s' % 'age' + ''.join('%7s' % g for g in POSL) + '%8s' % 'ALL')
    for ab in ABANDS:
        cnt = {g: 0 for g in POSL}; tot = 0
        for r in rows:
            if band(r['age']) == ab and cond(r):
                cnt[r['pos']] += 1; tot += 1
        P('%-6s' % ab + ''.join('%7d' % cnt[g] for g in POSL) + '%8d' % tot)

# flag decomposition for the young-constituency claim: career games 1-50 at each season row's moment
P('')
P('FLAG DECOMPOSITION (the P7 check) — played 2026 rows, career games 1-50 as of 2026, gate reading:')
P('  (a season is stall-flagged when games<10u OR avg<flat bar; only avg-only flags are bar-relievable)')
cg = {}
for p in d:
    cg[p.get('key')] = sum(float(x.get('games') or 0) for x in (p.get('scoring') or []))
n_g = n_a = n_b = n_pass = 0
for r in rows:
    if r['year'] != INPROG: continue
    if not (1 <= cg.get(r['key'], 0) <= 50): continue
    gfail = not r['full']; afail = r['under_flat']
    if gfail and afail: n_b += 1
    elif gfail: n_g += 1
    elif afail: n_a += 1
    else: n_pass += 1
tot = n_g + n_a + n_b + n_pass
P('  n=%d 2026 played rows with career games 1-50: games-only fail %d, avg-only fail %d, both fail %d, pass %d'
  % (tot, n_g, n_a, n_b, n_pass))
P('  flagged %d (%.0f%%); of flagged, avg-only (bar-relievable this year) %d (%.0f%% of flagged)'
  % (tot - n_pass, 100.0 * (tot - n_pass) / max(tot, 1), n_a, 100.0 * n_a / max(tot - n_pass, 1)))
P('  NOTE: the established 94%% figure counts the standing stall RUN over all seasons; this table is')
P('  the 2026 season reading only — the packet reconciles the two.')

open(os.path.join(OUT, 'CENSUS_S1.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
