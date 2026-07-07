"""Collect the final deliverable data: board_final.json (full board rows), anchors_final.json,
book_cohort_rows.json, build_meta.json, pvc_v34_baseline.json. Run under the FULL candidate config
(after the final board+book exist)."""
import io, contextlib, json, os, hashlib
import numpy as np

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; cp = g['cp']; _nqual = g['_nqual']; _lvlcurr = g['_lvlcurr']
OUT = '/home/user/afl-rl-engine/session_2026-07-06/w4_integration/out'
baked = {r['key']: r['v'] for r in json.load(open('/home/user/afl-rl-engine/session_2026-07-06/w4_integration/out/baked_board_full.json'))['active']}  # TRUE baked v2.5 board (git 00d82dd) — /home/claude/rl_build now holds the CANDIDATE (B4 basis)

rows = []
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        k = p.get('key')
        if k not in baked or p.get('_retired'):
            continue
        try:
            v = float(ev(p, 2026))
        except Exception:
            continue
        rows.append({'key': k, 'player': p['player'], 'pos': MA.gfut(p), 'age': cp._age_asof(p, 2026),
                     'nq': _nqual(p, 2026), 'pick': p.get('pick'), 'baked': baked[k], 'now': v})
json.dump(rows, open(f'{OUT}/board_final.json', 'w'))
tot0 = sum(r['baked'] for r in rows); tot1 = sum(r['now'] for r in rows)
movers = sum(1 for r in rows if abs(r['now'] - r['baked']) >= 1)
meta = {'head': hashlib.md5(open('_merged_recover.py', 'rb').read()).hexdigest()[:8],
        'pool_delta': f"{100*(tot1/tot0-1):+.2f}%", 'n_players': len(rows), 'n_movers': movers}
json.dump(meta, open(f'{OUT}/build_meta.json', 'w'), indent=1)

ANCH = {
 'Willem Duursma': ('young gun — runway credit', 'year-1 cohort lifted under the no-arbitrage bound'),
 'Zak Butters': ('peak cohort (4-6) survivor', 'HELD (not crushed) — margin credit, no fade (elite)'),
 'Max Holmes': ('peak cohort (4-6) survivor', 'HELD (not crushed) — margin credit, no fade (elite)'),
 'Marcus Bontempelli': ('elite veteran (target >= +10%)', '120+ avg permanent captain, no decline — certainty credit on the present margin + captaincy'),
 'Max Gawn': ('elite veteran (must clear Briggs)', '+48 above REPL + captaincy; forward-years no longer level him with a low-80s ruck'),
 'Kieren Briggs': ('runway-pair reference', 'low-80s barely above REPL — moderate far-years now carry washout risk'),
 'Jeremy Cameron': ('elite KPF (up)', 'KPF above-REPL margin reward + v7 form relax'),
 'Sam Darcy': ('KPF young — owner read UNDERPRICED', 'three-locus: young ceiling kept, KPF compress never touches him, LTI channels attributed'),
 'Stephen Coniglio': ('fader', 'still at scrap level (small +Δ = lifted V0 floor basis only)'),
 'Taylor Adams': ('fader', 'unchanged'),
 'Mark Blicavs': ('fader', 'unchanged'),
 'Zach Guthrie': ('fader', 'unchanged'),
 'Nick Daicos': ('panel/proven young elite', 'margin credit (form-conditioned, age-blind)'),
 'Harry Sheezel': ('panel/proven young elite', 'margin credit'),
 'Harley Reid': ('panel yr-3 pedigree', 'small young credit'),
 'Taylor Goad': ('panel sat-out young ruck', 'smooth young-ruck headroom (no pick cliff) + young credit'),
 'Will Green': ('panel sat-out young ruck', 'smooth young-ruck headroom + young credit'),
 'Josh Smillie': ('panel sat-out mid', 'young credit via V0'),
 'Sam Walsh': ('#45 aging mover', 'aging decline form-conditioned + margin credit'),
 'Louis Emmett': ('#44 ruck anchor', 'production-honest ceiling (owner band 650-800) + young headroom'),
}
anch = {}
with contextlib.redirect_stdout(io.StringIO()):
    for nm, (role, read) in ANCH.items():
        p = next((x for x in MA.data if x['player'] == nm and MA.GRP.get(x.get('pos'))), None)
        if p is None:
            continue
        v = float(ev(p, 2026)); b = baked.get(p.get('key'))
        anch[nm] = {'role': role, 'read': read, 'baked': b, 'now': round(v),
                    'dpct': (f"{100*(v-b)/b:+.1f}%" if b else '—')}
json.dump(anch, open(f'{OUT}/anchors_final.json', 'w'), indent=1)

mat_p = os.environ.get('W4_MATRIX', f'{OUT}/s4_matrix_final.json')
if os.path.exists(mat_p):
    mat = json.load(open(mat_p))
    S = {}
    for v in mat.values():
        C = int(v['year'])
        if not v['incurve'] or not (2004 <= C <= 2020):
            continue
        for i, _y in enumerate(v['yrs']):
            N = i + 1
            if N > 7:
                break
            S[(C, N)] = S.get((C, N), 0.0) + float(v['Vpath'][i] or 0.0)
    cohorts = sorted({c for c, _ in S})
    R = {str(C): {str(N): round(100.0 * S[(C, N)] / max(S[(C, 1)], 1e-9)) for N in range(1, 8) if (C, N) in S}
         for C in cohorts}
    json.dump(R, open(f'{OUT}/book_cohort_rows.json', 'w'), indent=1)
print('final outputs written:', meta)
