#!/usr/bin/env python3
"""EMIT THE AS-AT SEASON BOARDS into the UI (owner ruling 2026-10-14) — derived UI data only.

Reads the banks pass_asat_seasons.py wrote (values_asat_2025.json = the -1 board, values_asat_2024.json
= the -2 board: every player LISTED at the end of that season, priced with that season as the base
year) and carries them into the UI the cheapest honest way:

  1. ui/data/board_view_working.js — for every CURRENT active row, `lens[1]` (-1) and `lens[0]` (-2)
     are set from the bank, and NULL when the player was not on that as-at board (a Nov-2025 draftee
     has no 2025 value; he was not on the list). `lens[2..4]` and every other field are untouched.
     The stamp gains `asatLens`, saying where the two columns now come from. The ONLY consumer of
     lens[0..2] is the player card (ui/app/card.js), whose line chart skips nulls and names the
     seasons the player was not on the board.
  2. ui/data/asat_boards.js (`window.__ASAT_BOARDS__`) — the FULL as-at rosters, retirees included:
     key, name, club (the store's afl_club where it carries one — the 804 current rows — else null,
     with the draft club beside it as the one club the store knows for a retiree), v, rank, and why
     the row is on that board. Stamped with the live board md5 and the store md5 it was built against.

WHAT THIS DOES NOT DO. The engine's rl_export still writes vM1/vM2 = ev(p,2025/2024) on the current
804 rows and the live board (data/rl_build/rl_app_data.json) is not touched; the owner sees the as-at
numbers in the UI before any engine change. The working bundle's `back` rows (the engine's old
retiree recall) are left as they are — the as-at retirees live in asat_boards.js.

THE MIRROR LAW (ui/app/ownership.js:25) APPLIES: the bank names the board and store it was priced
against; if either disagrees with the bundle this emitter is patching, or with the tree's live board
and store, the emission is REFUSED. A stale as-at column trusted while wrong is worse than none.

NOT A LANDING CARRIER (yet): ui/tools/extract_board_view.py regenerates the working bundle from the
board and will put the engine's vM1/vM2 back; re-run this emitter after it (the same discipline
emit_retro_series.py has in steps.py writer 4b, which the lander will inherit once the owner adopts
the as-at columns). Idempotent: a re-run writes the same bytes.

RUN:  python3 docs/evidence/walkforward_retro_2026-08-29/emit_asat_seasons.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SEASONS = (2025, 2024)                        # -1, -2  ->  lens[1], lens[0]
LENS_IDX = {2025: 1, 2024: 0}
BANK = lambda Y: os.path.join(HERE, 'values_asat_%d.json' % Y)
BUNDLE = os.path.join(REPO, 'ui', 'data', 'board_view_working.js')
BOARD = os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')
OUT = os.path.join(REPO, 'ui', 'data', 'asat_boards.js')
VAR = 'window.__MATCHDAY_WORKING__'


def _md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def load_bundle(path):
    """-> (header text before the assignment, the dict, the tail after the closing brace)."""
    t = open(path, encoding='utf-8').read()
    i = t.index(VAR)
    j = t.index('{', i)
    k = t.rindex('}') + 1
    return t[:j], json.loads(t[j:k]), t[k:]


def write_bundle(path, head, obj, tail):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(head)
        json.dump(obj, fh, ensure_ascii=False, separators=(',', ':'))   # the extractor's own serialisation
        fh.write(tail)


def main(argv=None):
    banks = {}
    for Y in SEASONS:
        if not os.path.exists(BANK(Y)):
            raise SystemExit('HALT: %s is not banked — run tools/harness docs/evidence/'
                             'walkforward_retro_2026-08-29/pass_asat_seasons.py first.' % os.path.basename(BANK(Y)))
        banks[Y] = json.load(open(BANK(Y)))
        if banks[Y].get('season') != Y:
            raise SystemExit('HALT: %s says season %r' % (BANK(Y), banks[Y].get('season')))

    # THE MIRROR LAW: one board, one store, named identically by the banks, the bundle and the tree.
    board_md5, store_md5 = _md5(BOARD), _md5(STORE)
    head, w, tail = load_bundle(BUNDLE)
    st = w.get('stamp') or {}
    ids = {'tree board': board_md5, 'tree store': store_md5,
           'bundle board': st.get('board_md5'), 'bundle store': st.get('store_md5')}
    for Y in SEASONS:
        ids['bank %d board' % Y] = banks[Y].get('board_md5')
        ids['bank %d store' % Y] = banks[Y].get('store_md5')
    if len(set(v for k, v in ids.items() if 'board' in k)) != 1 or len(set(v for k, v in ids.items() if 'store' in k)) != 1:
        raise SystemExit('HALT (mirror law): the as-at banks, the working bundle and the tree do not name '
                         'one board and one store — refusing to emit a stale as-at column.\n  ' +
                         '\n  '.join('%-18s %s' % (k, (v or 'None')[:8]) for k, v in sorted(ids.items())))

    # 1. the working bundle's backward lens columns, from the bank; null = not on that board
    stats = {}
    for Y in SEASONS:
        vals = banks[Y]['values']
        idx = LENS_IDX[Y]
        n_set = n_null = 0
        for r in w.get('players') or []:
            lens = list(r.get('lens') or [])
            while len(lens) < 5:
                lens.append(None)
            v = vals.get(r.get('key'))
            lens[idx] = int(v) if v is not None else None
            r['lens'] = lens
            n_set += v is not None
            n_null += v is None
        stats[str(Y)] = {'lens_index': idx, 'set': n_set, 'not_on_board': n_null,
                         'roster_n': banks[Y]['n'], 'retired_now': len(banks[Y].get('retired_now') or [])}
    w.setdefault('stamp', {})['asatLens'] = {
        'doc': 'lens[0] (-2) and lens[1] (-1) are the AS-AT boards (owner ruling 2026-10-14): every '
               'player listed at the end of 2024 / 2025, priced with that season as the base year, from '
               'docs/evidence/walkforward_retro_2026-08-29/values_asat_<Y>.json. null = not on that board. '
               'The live board\'s own vM1/vM2 (rl_export ev(p,2025/2024) on the current rows) are NOT '
               'these numbers; the full rosters incl. retirees are in ui/data/asat_boards.js.',
        'rule': banks[SEASONS[0]].get('rule'), 'seasons': stats, 'board_md5': board_md5, 'store_md5': store_md5,
        'generator': 'docs/evidence/walkforward_retro_2026-08-29/emit_asat_seasons.py'}
    write_bundle(BUNDLE, head, w, tail)
    for Y in SEASONS:
        s = stats[str(Y)]
        print('lens[%d] <- as-at %d: %d rows set, %d null (not on that board); roster %d incl. %d retired/delisted today'
              % (s['lens_index'], Y, s['set'], s['not_on_board'], s['roster_n'], s['retired_now']))

    # 2. the full as-at rosters, retirees included, names and clubs from the store (read-only)
    store = json.load(open(STORE))
    by_key = {}
    for p in store:
        if p.get('key') and p['key'] not in by_key:
            by_key[p['key']] = p
    live_keys = set(r.get('key') for r in (w.get('players') or []))
    seasons = {}
    for Y in SEASONS:
        b = banks[Y]
        retired = set(b.get('retired_now') or [])
        reasons = b.get('reasons') or {}
        order = sorted(b['values'].items(), key=lambda kv: (-kv[1], kv[0]))
        rows = []
        for i, (k, v) in enumerate(order):
            s = by_key.get(k) or {}
            rows.append({'key': k, 'name': s.get('player'), 'v': int(v), 'rank': i + 1,
                         'pos': s.get('drafted_position'), 'type': s.get('type'), 'year': s.get('year'),
                         # the store knows ONE current AFL club, on the 804 current rows; a retiree's row
                         # carries none, so his club is null and the draft club stands beside it, labelled.
                         'club': s.get('afl_club'), 'draft_club': s.get('_draft_club'),
                         'club_src': 'afl_club' if s.get('afl_club') else None,
                         'retired_now': k in retired, 'active_now': k in live_keys,
                         'why': reasons.get(k)})
        seasons[str(Y)] = {'season': Y, 'base_ref': Y, 'n': len(rows), 'lens_index': LENS_IDX[Y],
                           'n_retired_now': len(retired), 'n_active_now': sum(1 for r in rows if r['active_now']),
                           'rows': rows}
    out = {'stamp': {'board_md5': board_md5, 'store_md5': store_md5, 'rule': banks[SEASONS[0]].get('rule'),
                     'generator': 'docs/evidence/walkforward_retro_2026-08-29/emit_asat_seasons.py',
                     'source': ['docs/evidence/walkforward_retro_2026-08-29/values_asat_%d.json' % Y for Y in SEASONS],
                     'doc': 'The boards as they stood at the end of each season (owner ruling 2026-10-14), '
                            'retirees included, priced by the live engine with that season as the base year. '
                            'Derived UI data; the live board is untouched.'},
           'seasons': seasons}
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write('// GENERATED — the as-at season boards, from the banks named in stamp.source.\n')
        fh.write('// Do not hand-edit; regenerate via docs/evidence/walkforward_retro_2026-08-29/emit_asat_seasons.py.\n')
        fh.write('window.__ASAT_BOARDS__ = ')
        json.dump(out, fh, ensure_ascii=False, separators=(',', ':'))
        fh.write(';\n')
    print('wrote %s (%s) and %s (%s) against board %s store %s'
          % (os.path.relpath(BUNDLE, REPO), ', '.join('%s lens patched' % Y for Y in SEASONS),
             os.path.relpath(OUT, REPO), ', '.join('%s n=%d' % (Y, seasons[str(Y)]['n']) for Y in SEASONS),
             board_md5[:8], store_md5[:8]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
