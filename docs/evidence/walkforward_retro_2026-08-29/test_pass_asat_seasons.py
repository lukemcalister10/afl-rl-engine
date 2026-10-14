#!/usr/bin/env python3
"""pass_asat_seasons.py / emit_asat_seasons.py — the DRY tests (no engine load).

Run:  python3 docs/evidence/walkforward_retro_2026-08-29/test_pass_asat_seasons.py   (exit 0 = all pass)

WHAT MATTERS HERE. The pass's failure mode is not crashing, it is pricing the wrong population or
leaving the store it priced subtly changed. So the assertions are about the ROSTER RULE on a small
synthetic MA.data (debut incl. MSD, _last_listed, retired-with-last-game-in-Y included, not-yet-
debuted excluded, the unplayed entry window, duplicate-key collapse) and about the REWIND / RESTORE
cycle (the engine sees the as-at world — flags cleared, scoring <= Y — and the rows come back
byte-exact, an absent _last_listed absent again, the scoring object restored by identity). A fake
ev() stands in for the engine and asserts what it was shown. The emitter is exercised on a temp tree
(its mirror-law refusal and its idempotence).
"""
import copy
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PA = _load('pass_asat_seasons')
EM = _load('emit_asat_seasons')

FAILS = []
N = [0]


def check(cond, msg):
    N[0] += 1
    if not cond:
        FAILS.append(msg)
        print('  FAIL  ' + msg)
    else:
        print('  ok    ' + msg)


def row(key, year, typ, scoring, retired=False, ll=None, pos='MID', pick=5):
    p = {'player': key.replace('-', ' ').title(), 'key': key, 'year': year, 'type': typ, 'pos': pos,
         'pick': pick, 'scoring': [{'year': y, 'games': g, 'avg': 70.0, 'pos': pos} for y, g in scoring],
         '_retired': retired}
    p['games'] = sum(g for _, g in scoring)
    if ll is not None:
        p['_last_listed'] = ll
    return p


# ---------------------------------------------------------------- the synthetic store
DATA = [
    row('a-active', 2023, 'ND', [(2024, 10), (2025, 12), (2026, 8)]),                  # active, debut 2024
    row('b-no-2025-games', 2024, 'ND', [(2026, 5)]),                                    # active, debut 2025, played only in 2026
    row('c-nov25-draftee', 2025, 'ND', []),                                             # active (unplayed prospect), debut 2026
    row('d-msd-2025', 2025, 'MSD', [(2025, 6), (2026, 9)]),                             # active MSD: debut 2025
    row('e-retired-last-2025', 2018, 'ND', [(2019, 20), (2024, 15), (2025, 11)], retired=True),
    row('f-retired-last-2024', 2016, 'ND', [(2017, 20), (2024, 3)], retired=True),
    row('g-delisted-ll-2025', 2019, 'RD', [(2020, 4), (2023, 2)], ll=2025),             # ground truth: listed through 2025
    row('h-delisted-ll-2024', 2020, 'ND', [(2024, 7)], ll=2024),
    row('i-unplayed-2023-nd', 2023, 'ND', [], retired=True),                            # debut 2024: window 2024-2025
    row('j-unplayed-2021-nd', 2021, 'ND', [], retired=True),                            # debut 2022: window 2022-2023
    row('k-msd-2026', 2026, 'MSD', [(2026, 4)]),                                        # debut 2026
    row('l-not-a-board-pos', 2020, 'ND', [(2024, 10), (2025, 10)], pos='XX'),
    row('a-active', 2019, 'RD', [(2020, 2)], retired=True),                             # a duplicate record of A, retired
    row('m-retired-ll-2025-no-games', 2015, 'ND', [(2016, 20), (2022, 10)], retired=True, ll=2025),
]
ACTIVE = {'a-active', 'b-no-2025-games', 'c-nov25-draftee', 'd-msd-2025', 'k-msd-2026', 'l-not-a-board-pos'}

print('(1) the roster rule')
check(PA.debut({'year': 2025, 'type': 'ND'}) == 2026 and PA.debut({'year': 2025, 'type': 'MSD'}) == 2025
      and PA.debut({'year': 2024, 'type': 'SSP'}) == 2025, 'debut = year+1, MSD = year')
r25 = PA.roster(DATA, 2025, ACTIVE)
r24 = PA.roster(DATA, 2024, ACTIVE)
k25 = {p['key']: why for p, why in r25}
k24 = {p['key']: why for p, why in r24}
check(k25.get('a-active') == 'played' and k24.get('a-active') == 'played', 'A: active, played both -> on both')
check(k25.get('b-no-2025-games') == 'active_now' and 'b-no-2025-games' not in k24,
      'B: debut 2025, no 2025 game, active now -> on 2025 (active now), off 2024 (not debuted)')
check('c-nov25-draftee' not in k25 and 'c-nov25-draftee' not in k24, 'C: Nov-2025 draftee (debut 2026) on neither')
check(k25.get('d-msd-2025') == 'played' and 'd-msd-2025' not in k24, 'D: MSD 2025 debuts in 2025 -> on 2025, off 2024')
check(k25.get('e-retired-last-2025') == 'played' and k24.get('e-retired-last-2025') == 'played',
      'E: retired, last game 2025 -> on 2025 AND 2024')
check('f-retired-last-2024' not in k25 and k24.get('f-retired-last-2024') == 'played',
      'F: retired, last game 2024 -> off 2025, on 2024')
check(k25.get('g-delisted-ll-2025') == 'listed' and k24.get('g-delisted-ll-2025') == 'listed',
      'G: _last_listed 2025, last game 2023 -> on both by ground truth')
check('h-delisted-ll-2024' not in k25 and k24.get('h-delisted-ll-2024') == 'played',
      'H: _last_listed 2024 -> off 2025, on 2024')
check(k25.get('i-unplayed-2023-nd') == 'entry_window' and k24.get('i-unplayed-2023-nd') == 'entry_window',
      'I: unplayed 2023 ND (debut 2024) -> on 2024 and 2025 (entry window)')
check('j-unplayed-2021-nd' not in k25 and 'j-unplayed-2021-nd' not in k24, 'J: unplayed 2021 ND -> window closed, on neither')
check('k-msd-2026' not in k25 and 'k-msd-2026' not in k24, 'K: MSD 2026 (debut 2026) on neither')
check('l-not-a-board-pos' not in k25 and 'l-not-a-board-pos' not in k24, 'L: a position the board does not value is excluded')
check(k25.get('m-retired-ll-2025-no-games') == 'listed' and k24.get('m-retired-ll-2025-no-games') == 'listed',
      'M: retired, no game since 2022, _last_listed 2025 -> on both (ground truth beats the games proxy)')
a_rows = [p for p, _ in r25 if p['key'] == 'a-active']
check(len(a_rows) == 1 and a_rows[0]['year'] == 2023, 'duplicate-key group collapses to ONE row, the active-now record')
check(len(r25) == 7 and len(r24) == 7, 'roster sizes: 2025=%d 2024=%d (expect 7/7: a b d e g i m / a e f g h i m)' % (len(r25), len(r24)))
# the unplayed window without a type restriction follows _on_board literally
check(PA.on_board_asat(row('x-ire', 2023, 'IRE', [], retired=True), 2024, set()) == 'entry_window',
      'the entry window is _on_board\'s rule: no draft-type restriction')
check(PA.on_board_asat(row('y', 2023, 'ND', [], retired=True), 2023, set()) is None, 'the window starts at debut, not draft year')

print('(2) rewind / restore, byte-exact, and what the engine is shown')
seen = []


def fake_ev(p, Y):
    # what the engine sees during pricing: the as-at world
    assert p['_retired'] is False and p.get('_last_listed') is None, 'flags not cleared for %s' % p['key']
    assert all(r['year'] <= Y for r in p['scoring']), 'scoring not rewound for %s' % p['key']
    assert p['games'] == sum(r['games'] for r in p['scoring']), 'games not recomputed for %s' % p['key']
    assert MA.BASE_REF == Y and MA.AGE_REF == Y and MA._LENS_FORM is None, 'clock not pinned to Y'
    seen.append((p['key'], Y, len(p['scoring'])))
    return 2.0 * (100 * len(p['scoring']) + (Y - 2000))     # F=2 below -> v = 100*n + (Y-2000)


MA = types.SimpleNamespace(data=DATA, BASE_REF=2026, AGE_REF=2026, _LENS_FORM=2026, _pe_clear=lambda: None)
G = {'_PL_F': 2.0, 'BASE_REF': 2026, 'AGE_REF': 2026, '_LENS_FORM': 2026}
NS = {'G': G, 'MA': MA, 'ev': fake_ev, 'T': lambda s: print('    T ' + s), 'repo': None}
before = [copy.deepcopy(p) for p in DATA]
before_ids = [id(p['scoring']) for p in DATA]
vals = PA.price_rows(NS, 2025, [p for p, _ in r25])
check(vals['a-active'] == 225 and vals['e-retired-last-2025'] == 325 and vals['i-unplayed-2023-nd'] == 25,
      'v = round(ev/F): A 2 seasons<=2025 -> 225; E 3 -> 325; I 0 -> 25')
check(all(p == q for p, q in zip(DATA, before)), 'every row byte-equal to its pre-rewind copy')
check(all(id(p['scoring']) == i for p, i in zip(DATA, before_ids)), 'every scoring list restored by identity')
check('_last_listed' not in DATA[0] and DATA[4]['_retired'] is True and DATA[6]['_last_listed'] == 2025,
      'absent _last_listed is absent again (not None); _retired / _last_listed values back')
check(DATA[1]['scoring'][0]['year'] == 2026 and DATA[1]['games'] == 5, 'a non-roster row rewound for peer purity is back too')
check(MA.BASE_REF == 2026 and MA.AGE_REF == 2026 and MA._LENS_FORM == 2026 and G['BASE_REF'] == 2026 and G['_LENS_FORM'] == 2026,
      'the clock globals (MA and G) are put back')
check(sorted(k for k, _, _ in seen) == sorted(k25), 'exactly the roster was priced, once each')

# the restore guard discriminates: a row that comes back changed HALTS by name
p = row('z', 2020, 'ND', [(2021, 3), (2026, 2)])
s = PA.rewind(p, 2025, clear_flags=True)
p['pick'] = 99
try:
    PA.restore(p, s)
    check(False, 'restore must HALT on a row that is not byte-exact')
except RuntimeError as e:
    check("'pick'" in str(e) and 'z' in str(e), 'restore HALTs and names the differing field: %s' % str(e)[:80])

print('(3) run(): the control gates the bank; the bank files carry the roster')
tmp = tempfile.mkdtemp(prefix='asat_')
try:
    os.makedirs(os.path.join(tmp, 'data', 'rl_build')); os.makedirs(os.path.join(tmp, 'engine', 'rl_after'))
    store_p = os.path.join(tmp, 'engine', 'rl_after', 'rl_model_data.json')
    json.dump(DATA, open(store_p, 'w'))
    live_rows = [p for p in DATA if p['key'] in ACTIVE and not PA.delisted_now(p) and p['pos'] in PA.GRP]
    # the fake engine's present value: 100*n_seasons + 26
    board = {'active': [{'key': p['key'], 'v': 100 * len(p['scoring']) + 26} for p in live_rows]}
    board_p = os.path.join(tmp, 'data', 'rl_build', 'rl_app_data.json')
    json.dump(board, open(board_p, 'w'))
    json.dump({'store': EM._md5(store_p), 'board': EM._md5(board_p)}, open(os.path.join(tmp, 'data', 'expected_boot.json'), 'w'))
    PA.OUT_DIR = os.path.join(tmp, 'bank')
    NS['repo'] = tmp
    cwd = os.getcwd(); os.chdir(tmp)       # no rl_model_data.json in cwd -> the repo store is used
    try:
        verdict = PA.run(NS)
    finally:
        os.chdir(cwd)
    check(verdict['control']['pass'] and verdict['control']['n'] == len(live_rows), 'control passes on the fake present')
    b25 = json.load(open(os.path.join(PA.OUT_DIR, 'values_asat_2025.json')))
    b24 = json.load(open(os.path.join(PA.OUT_DIR, 'values_asat_2024.json')))
    check(b25['season'] == 2025 and b25['n'] == 7 and set(b25['values']) == set(k25), 'values_asat_2025.json: season, n, keys')
    check(set(b25['retired_now']) == {'e-retired-last-2025', 'g-delisted-ll-2025', 'i-unplayed-2023-nd', 'm-retired-ll-2025-no-games'},
          'retired_now lists the rows that are retired or delisted TODAY')
    check(b24['values']['f-retired-last-2024'] == 224 and 'f-retired-last-2024' not in b25['values'],
          'F priced on the 2024 board (2 seasons -> 224) and absent from 2025')
    check(b25['store_md5'] == EM._md5(store_p) and b25['board_md5'] == EM._md5(board_p), 'bank stamped with store and board md5')
    check(all(p == q for p, q in zip(DATA, before)), 'after run(): the store rows are byte-equal to their copies')

    # a control that cannot reproduce the present HALTS before banking
    board['active'][0]['v'] += 1
    json.dump(board, open(board_p, 'w'))
    json.dump({'store': EM._md5(store_p), 'board': EM._md5(board_p)}, open(os.path.join(tmp, 'data', 'expected_boot.json'), 'w'))
    PA.OUT_DIR = os.path.join(tmp, 'bank2')
    os.chdir(tmp)
    try:
        PA.run(NS); check(False, 'a failed control must HALT')
    except RuntimeError as e:
        check('control failed' in str(e) and not os.path.exists(os.path.join(PA.OUT_DIR, 'values_asat_2025.json')),
              'failed control HALTs and banks nothing')
    finally:
        os.chdir(cwd)
    board['active'][0]['v'] -= 1
    json.dump(board, open(board_p, 'w'))

    print('(4) the emitter: mirror law, lens patch, idempotence')
    ui = os.path.join(tmp, 'ui', 'data'); os.makedirs(ui)
    bundle_p = os.path.join(ui, 'board_view_working.js')
    bundle = {'stamp': {'board_md5': EM._md5(board_p), 'store_md5': EM._md5(store_p)},
              'players': [{'key': p['key'], 'v': 1, 'lens': [7, 7, 1, 9, 9]} for p in live_rows]}
    open(bundle_p, 'w').write('// GENERATED\n// header\nwindow.__MATCHDAY_WORKING__ = ' + json.dumps(bundle, separators=(',', ':')) + ';\n')
    EM.BANK = lambda Y: os.path.join(tmp, 'bank', 'values_asat_%d.json' % Y)
    EM.BUNDLE, EM.BOARD, EM.STORE, EM.OUT = bundle_p, board_p, store_p, os.path.join(ui, 'asat_boards.js')
    EM.REPO = tmp
    EM.main([])
    head, w, tail = EM.load_bundle(bundle_p)
    byk = {r['key']: r for r in w['players']}
    check(head.startswith('// GENERATED\n// header\n') and tail == ';\n', 'bundle header and tail preserved')
    check(byk['a-active']['lens'] == [124, 225, 1, 9, 9], 'A: lens[0]=as-at 2024, lens[1]=as-at 2025, lens[2..4] untouched')
    check(byk['c-nov25-draftee']['lens'][0] is None and byk['c-nov25-draftee']['lens'][1] is None, 'C: null on both as-at boards')
    check(byk['b-no-2025-games']['lens'] == [None, 25, 1, 9, 9], 'B: null at -2, priced at -1')
    check(w['stamp']['asatLens']['seasons']['2025']['set'] == 3 and w['stamp']['asatLens']['seasons']['2025']['not_on_board'] == 2,
          'stamp.asatLens counts set / not-on-board (2025: 3 set, 2 null)')
    t = open(EM.OUT).read()
    ab = json.loads(t[t.index('{'):t.rindex('}') + 1])
    r25e = ab['seasons']['2025']['rows']
    check(ab['seasons']['2025']['n'] == 7 and r25e[0]['key'] == 'e-retired-last-2025' and r25e[0]['rank'] == 1 and r25e[0]['retired_now'],
          'asat_boards.js: the full 2025 roster incl. the retiree, ranked by v')
    check(ab['stamp']['board_md5'] == EM._md5(board_p) and ab['stamp']['store_md5'] == EM._md5(store_p), 'asat_boards.js stamped')
    first = open(bundle_p, 'rb').read() + open(EM.OUT, 'rb').read()
    EM.main([])
    check(first == open(bundle_p, 'rb').read() + open(EM.OUT, 'rb').read(), 'idempotent: a re-run writes the same bytes')
    # the mirror law: a bundle on another board is refused
    bundle['stamp']['board_md5'] = '0' * 32
    open(bundle_p, 'w').write('window.__MATCHDAY_WORKING__ = ' + json.dumps(bundle) + ';\n')
    try:
        EM.main([]); check(False, 'the emitter must refuse a bundle on another board')
    except SystemExit as e:
        check('mirror law' in str(e), 'mirror law: refused a bundle whose board is not the bank\'s')
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
if FAILS:
    print('FAILED %d of %d checks:' % (len(FAILS), N[0]))
    for f in FAILS:
        print('  - ' + f)
    sys.exit(1)
print('ALL %d CHECKS PASS — pass_asat_seasons.py roster rule + rewind/restore + run() gate; emit_asat_seasons.py mirror law + lens patch' % N[0])
