#!/usr/bin/env python3
"""tools/draft_companion/build_page.py — writes draft_night.html from template.html.

Injects: v0_tables.json (engine tables, from extract_v0_tables.py), the free agents read off the shipped working
bundle (AFFL team "Free Agents", plus the owner's AFFL delistings in affl_delisted.json), the prospect list and
state flags (prospects/, the owner's 2026-11-19 handover). No engine load: re-run after any landing."""
import base64, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
data = json.load(open(os.path.join(HERE, 'v0_tables.json')))

bv = open(os.path.join(ROOT, 'ui', 'data', 'board_view_working.js'), encoding='utf-8').read()
bvo = json.loads(bv[bv.index('{', bv.index('=')):bv.rindex('}') + 1])
dl = set(json.load(open(os.path.join(HERE, 'affl_delisted.json')))['keys'])
# the AFL club comes from the store: the board carries the club it was BUILT with, so an ownership-courier club
# change (identity only, no board build) would otherwise show the old club until the next board build.
club_of = {r['key']: r.get('afl_club') for r in json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')))}
seen, fas = set(), []
for p in bvo['players']:
    if (p.get('affl_team') or '') == 'Free Agents' or p.get('key') in dl:
        seen.add(p.get('key'))
        fas.append({'key': p.get('key'), 'name': p.get('name'), 'afl_club': club_of.get(p.get('key')) or p.get('afl_club'), 'pos': p.get('pos'),
                    'elig': p.get('elig'), 'v': p.get('v'), 'age': p.get('age'),
                    'was': p.get('affl_team') if p.get('key') in dl else None})
missing = sorted(dl - seen)
assert not missing, 'AFFL delistings not on the active board: %s' % missing
fas.sort(key=lambda r: -(r['v'] or 0))
data['free_agents'] = fas

pr = json.load(open(os.path.join(HERE, 'prospects', 'players.json')))['players']
data['prospects'] = [{'id': p['playerId'], 'name': p['name'], 'dob': p.get('birthDate') or '', 'pos': p.get('position') or '',
                      'state': p.get('stateCode') or '', 'stateName': p.get('state') or '', 'rank': p.get('kemenyRank'),
                      'h': p.get('heightCm'),
                      'links': [{'club': l['club'], 'type': l['type']} for l in p.get('clubLinks') or []],
                      'badges': [{'code': b['code'], 'label': b['label'], 'club': b['club']} for b in p.get('displayedBadges') or []]}
                     for p in pr]
flags = {}
for code in ('SA', 'WA', 'VM', 'VC', 'AL'):
    b = open(os.path.join(HERE, 'prospects', 'state-flags', code.lower() + '.png'), 'rb').read()
    assert b[:8] == b'\x89PNG\r\n\x1a\n'
    flags[code] = 'data:image/png;base64,' + base64.b64encode(b).decode()
data['flags'] = flags

tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
js = lambda o: json.dumps(o, separators=(',', ':')).replace('</', '<\\/')
assert tpl.count('/*__DATA__*/') == 1 and tpl.count('/*__SEED__*/') == 1
page = tpl.replace('/*__DATA__*/', js(data))

# 1. the claude.ai artifact: entries live in the artifact's database, so no board is baked in
out = os.path.join(HERE, 'draft_night.html')
open(out, 'w', encoding='utf-8').write(page.replace('/*__SEED__*/', 'null'))
print('wrote draft_night.html (%d bytes): %d free agents (%d AFFL delistings), %d prospects'
      % (os.path.getsize(out), len(fas), len(dl), len(data['prospects'])))

# 2. the standalone file: opens in any browser, saves in that browser, starts from board_snapshot.json.
#    The artifact host wraps its page in a document skeleton; a standalone file carries its own.
snap = json.load(open(os.path.join(HERE, 'board_snapshot.json')))
seed = {'standalone': True, 'taken': snap.get('taken'), 'slots': snap.get('slots', {}), 'fa': snap.get('fa', {})}
head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}img{max-width:100%}'
        '[hidden]{display:none!important}</style></head><body>')
sa = os.path.join(HERE, 'draft_night_standalone.html')
open(sa, 'w', encoding='utf-8').write(head + page.replace('/*__SEED__*/', js(seed)) + '</body></html>\n')
print('wrote draft_night_standalone.html (%d bytes): board snapshot %s, %d entries'
      % (os.path.getsize(sa), seed['taken'], sum(1 for s in seed['slots'].values() if s.get('name'))))
