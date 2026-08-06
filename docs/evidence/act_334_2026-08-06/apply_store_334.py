#!/usr/bin/env python3
"""#334 STAGE A — THE STORE ACT. census.json + the Drummond ruling, applied verbatim.

Binding law, in the order it is applied:
  1  51 season inserts (census.json, byte-verbatim: year/games/avg).
     - row shape and field order {year, avg, games, pos}, matching every existing row;
     - avg written at the census 1-dp value verbatim, never re-rounded from a wider float;
     - pos = the player's EARLIEST EXISTING scoring row's pos; for the ten players with no
       rows at all, drafted_position. NEVER the sheet's present-day position hint
       (ADDENDUM 1 fault 6 — measured anachronisms: Ryder RUCK-hint vs KPD in 2007, etc.);
     - inserted at the correct position in the player's scoring list by year order.
  2  Career-games counters move with the inserts (ADDENDUM 1 fault 3 / #323 section 1):
     record['games'] == sum(row games) after the write, on all 2,650 records.
  3  NO rows for the 177 zero-confirmations (ADDENDUM 1, adopted ruling).
  4  Drummond (#334 comment 5199567533): year 2003->2004, pick 35->40, stream_year and
     stream_pick mirrors moved identically (ADDENDUM 1 fault 4); 2004 RD picks >=40 slide
     DOWN one; 2003 RD picks >35 slide UP one; mirrors move with pick.
  5  A per-row EXPECTED-DELTA table for every touched record (ADDENDUM 1 fault 5 — a blanket
     byte-identical claim is false for marcus-allan and martin-pask, which are BOTH slid and
     inserted). Every record not in the table is asserted byte-identical.
  All comparisons key on `key`, never on name (the two-Will-Hamill trap).

  python3 apply_store_334.py <repo> <census.json> <evidence_dir> [--apply]
"""
import copy, hashlib, json, os, sys

REPO, CENSUS, EVID = sys.argv[1], sys.argv[2], sys.argv[3]
APPLY = '--apply' in sys.argv
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')

NO_ROW_TEN = {'adam-iacobucci', 'ben-eckermann', 'ben-jolley', 'ben-schwarze', 'elijah-ware',
              'james-ezard', 'martin-pask', 'paul-thomas', 'ryan-willits', 'travis-baird'}

raw = open(STORE, 'rb').read()
before = json.loads(raw)
old_md5 = hashlib.md5(raw).hexdigest()

# --- the serializer proof, before anything is touched -------------------------------
if json.dumps(before).encode() != raw:
    raise SystemExit('HALT: the store does not round-trip byte-identically under '
                     'json.dumps(json.loads(x)) — a write here would reformat the file. '
                     '(This is the project\'s own SERIALIZER DRIFT check, '
                     'ui/tools/ownership_store_apply.py:215.)')
print('serializer proof   json.dumps(json.loads(store)) == store bytes   OK')
print('store on disk      %s   %d records' % (old_md5, len(before)))

keys = [r['key'] for r in before]
if len(set(keys)) != len(keys):
    raise SystemExit('HALT: duplicate keys in the store — every assert below keys on `key`')

after = copy.deepcopy(before)
by = {r['key']: r for r in after}
census = json.load(open(CENSUS))
inserts = census['inserts']

# ================================================================= 1 · THE 51 INSERTS
touched_ins, ins_log = set(), []
for i in inserts:
    rec = by[i['key']]
    rows = rec.setdefault('scoring', [])
    if any(s['year'] == i['year'] for s in rows):
        raise SystemExit('HALT: %s already carries a %d row — census said 0 conflicts'
                         % (i['key'], i['year']))
    if rows:
        pos = min(rows, key=lambda s: s['year'])['pos']
        pos_src = 'earliest existing row (%d)' % min(s['year'] for s in rows)
    else:
        if i['key'] not in NO_ROW_TEN:
            raise SystemExit('HALT: %s has no scoring rows but is not one of the ten named '
                             'no-row players — the pos rule does not cover it' % i['key'])
        pos = rec['drafted_position']
        pos_src = 'drafted_position'
    row = {'year': i['year'], 'avg': i['avg'], 'games': i['games'], 'pos': pos}
    rows.append(row)
    rows.sort(key=lambda s: s['year'])
    touched_ins.add(i['key'])
    ins_log.append({'key': i['key'], 'row': row, 'pos_source': pos_src,
                    'pos_hint_in_sheet_IGNORED': i.get('pos_hint'),
                    'hint_differs': i.get('pos_hint') != pos})
print('\n1  INSERTS  %d rows into %d players   (2005 %d · 2006 %d)'
      % (len(inserts), len(touched_ins),
         sum(1 for i in inserts if i['year'] == 2005),
         sum(1 for i in inserts if i['year'] == 2006)))
print('   pos from drafted_position (the ten no-row players): %d rows'
      % sum(1 for l in ins_log if l['pos_source'] == 'drafted_position'))
print('   sheet position HINT differs from the ruled pos on %d of %d rows — hint discarded'
      % (sum(1 for l in ins_log if l['hint_differs']), len(ins_log)))
print('   avg values byte-verbatim from census: %s'
      % all(by[i['key']]['scoring'][[s['year'] for s in by[i['key']]['scoring']].index(i['year'])]['avg']
            == i['avg'] for i in inserts))

# ============================================================ 2 · THE GAMES COUNTERS
games_log, total_added = [], 0
for k in sorted(touched_ins):
    rec, old = by[k], next(r for r in before if r['key'] == k)
    new_total = sum(s['games'] for s in rec['scoring'])
    games_log.append({'key': k, 'games_before': old['games'], 'games_after': new_total,
                      'delta': new_total - old['games']})
    total_added += new_total - old['games']
    rec['games'] = new_total
print('\n2  CAREER-GAMES COUNTERS  40 players, +%d games total (census sum %d)   MATCH: %s'
      % (total_added, sum(i['games'] for i in inserts),
         total_added == sum(i['games'] for i in inserts)))

# ================================================== 4 · DRUMMOND AND THE TWO SEQUENCES
def rd(recs, year):
    return sorted([r for r in recs if r.get('type') == 'RD' and r.get('year') == year],
                  key=lambda r: r['pick'])

pre03, pre04 = rd(after, 2003), rd(after, 2004)
print('\n4  DRUMMOND  before: 2003 RD n=%d picks %d..%d contiguous=%s · '
      '2004 RD n=%d picks %d..%d contiguous=%s'
      % (len(pre03), pre03[0]['pick'], pre03[-1]['pick'],
         [r['pick'] for r in pre03] == list(range(1, len(pre03) + 1)),
         len(pre04), pre04[0]['pick'], pre04[-1]['pick'],
         [r['pick'] for r in pre04] == list(range(1, len(pre04) + 1))))

dr = by['josh-drummond']
for f, want in (('year', 2003), ('pick', 35), ('stream_year', 2003), ('stream_pick', 35),
                ('type', 'RD')):
    if dr[f] != want:
        raise SystemExit('HALT: josh-drummond %s is %r, the ruling assumes %r' % (f, dr[f], want))
shaw = by['earl-shaw']; clarke = by['ed-clarke']
if not (shaw['year'] == 2004 and shaw['pick'] == 39 and clarke['year'] == 2004
        and clarke['pick'] == 40):
    raise SystemExit('HALT: the Shaw(39)/Clarke(40) anchor the owner named is not on the bytes')

slid = []
for r in pre04:                                   # 2004: picks >= 40 slide DOWN one
    if r['pick'] >= 40:
        slid.append({'key': r['key'], 'group': '2004 RD', 'pick_before': r['pick'],
                     'pick_after': r['pick'] + 1})
        r['pick'] += 1
        r['stream_pick'] = r['pick']
for r in pre03:                                   # 2003: picks > 35 slide UP one
    if r['pick'] > 35:
        slid.append({'key': r['key'], 'group': '2003 RD', 'pick_before': r['pick'],
                     'pick_after': r['pick'] - 1})
        r['pick'] -= 1
        r['stream_pick'] = r['pick']
dr['year'] = 2004; dr['pick'] = 40
dr['stream_year'] = 2004; dr['stream_pick'] = 40

post03, post04 = rd(after, 2003), rd(after, 2004)
c03 = [r['pick'] for r in post03] == list(range(1, 45))
c04 = [r['pick'] for r in post04] == list(range(1, 47))
print('   slid rows: %d (2004 RD %d down-one · 2003 RD %d up-one) + Drummond'
      % (len(slid), sum(1 for s in slid if s['group'] == '2004 RD'),
         sum(1 for s in slid if s['group'] == '2003 RD')))
print('   after: 2003 RD n=%d picks 1..%d contiguous=%s (want n=44) · '
      '2004 RD n=%d picks 1..%d contiguous=%s (want n=46)'
      % (len(post03), post03[-1]['pick'], c03, len(post04), post04[-1]['pick'], c04))
for g, recs, want in (('2003', post03, 44), ('2004', post04, 46)):
    picks = [r['pick'] for r in recs]
    if len(recs) != want or picks != list(range(1, want + 1)) or len(set(picks)) != len(picks):
        raise SystemExit('HALT: %s RD post-condition failed (n=%d picks=%s)'
                         % (g, len(recs), picks[:5]))
mirror_ok = all(r['stream_pick'] == r['pick'] and r['stream_year'] == r['year']
                for r in post03 + post04)
print('   stream_pick/stream_year mirrors track pick/year on every row of both groups: %s'
      % mirror_ok)
if not mirror_ok:
    raise SystemExit('HALT: a stream mirror did not move with its pick (ADDENDUM 1 fault 4)')
print('   drummond: year 2003->%d  pick 35->%d  stream_year->%d  stream_pick->%d  '
      'between earl-shaw %d and ed-clarke %d'
      % (dr['year'], dr['pick'], dr['stream_year'], dr['stream_pick'],
         by['earl-shaw']['pick'], by['ed-clarke']['pick']))

# ============================================ 5 · THE WHOLE-STORE EXPECTED-DELTA AUDIT
slid_keys = {s['key'] for s in slid}
expected = {}
for k in sorted(touched_ins | slid_keys | {'josh-drummond'}):
    fields = []
    if k in touched_ins:
        fields += ['scoring (+%d row%s)' % (sum(1 for i in inserts if i['key'] == k),
                                            's' if sum(1 for i in inserts if i['key'] == k) > 1 else ''),
                   'games']
    if k in slid_keys:
        fields += ['pick', 'stream_pick']
    if k == 'josh-drummond':
        fields += ['year', 'pick', 'stream_year', 'stream_pick']
    expected[k] = sorted(set(fields))

b_by = {r['key']: r for r in before}
actual, unexpected = {}, []
for k in sorted(b_by):
    o, n = b_by[k], by[k]
    if json.dumps(o) == json.dumps(n):
        continue
    moved = sorted([f for f in set(o) | set(n)
                    if json.dumps(o.get(f)) != json.dumps(n.get(f))])
    moved = ['scoring (+%d row%s)' % (len(n['scoring']) - len(o['scoring']),
                                      's' if len(n['scoring']) - len(o['scoring']) > 1 else '')
             if f == 'scoring' else f for f in moved]
    actual[k] = sorted(moved)
    if k not in expected:
        unexpected.append(k)
mismatched = sorted(k for k in set(expected) | set(actual)
                    if expected.get(k) != actual.get(k))
untouched_identical = sum(1 for k in b_by
                          if k not in expected and json.dumps(b_by[k]) == json.dumps(by[k]))
print('\n5  EXPECTED-DELTA AUDIT')
print('   records the act declares it touches      %d  '
      '(40 insert + %d slid + Drummond, union after the 2 both-slid-and-inserted)'
      % (len(expected), len(slid)))
print('   records that actually differ            %d' % len(actual))
print('   records differing but NOT declared      %d  %s' % (len(unexpected), unexpected))
print('   declared/actual field-set mismatches    %d  %s' % (len(mismatched), mismatched))
print('   every other record byte-identical       %d of %d  ASSERTED'
      % (untouched_identical, len(before) - len(expected)))
if unexpected or mismatched or untouched_identical != len(before) - len(expected):
    raise SystemExit('HALT: the whole-store diff does not match the declared expectation')

# ------------------------------------------------------------------ the written bytes
new_bytes = json.dumps(after).encode()
new_md5 = hashlib.md5(new_bytes).hexdigest()
if json.dumps(json.loads(new_bytes.decode())).encode() != new_bytes:
    raise SystemExit('HALT: the candidate bytes do not re-apply byte-identically')
print('\n   store md5  %s  ->  %s   (%d -> %d bytes, %d records unchanged in count)'
      % (old_md5, new_md5, len(raw), len(new_bytes), len(after)))

table = {'act': '#334 STAGE A', 'store_md5_before': old_md5, 'store_md5_after': new_md5,
         'records': len(after), 'inserts': ins_log, 'games_counters': games_log,
         'slid_rows': slid,
         'drummond': {'key': 'josh-drummond', 'year': [2003, 2004], 'pick': [35, 40],
                      'stream_year': [2003, 2004], 'stream_pick': [35, 40]},
         'expected_delta_by_key': expected, 'actual_delta_by_key': actual,
         'records_declared_touched': len(expected),
         'records_byte_identical': untouched_identical,
         'post_2003_RD_n': len(post03), 'post_2004_RD_n': len(post04)}
json.dump(table, open(os.path.join(EVID, 'expected_delta_table.json'), 'w'), indent=1)
print('   expected-delta table -> %s' % os.path.join(EVID, 'expected_delta_table.json'))

if not APPLY:
    open(os.path.join(EVID, 'store_candidate_334.json'), 'wb').write(new_bytes)
    print('\nDRY RUN — candidate written to evidence only, the live store is untouched.')
    raise SystemExit(0)
open(STORE, 'wb').write(new_bytes)
back = hashlib.md5(open(STORE, 'rb').read()).hexdigest()
assert back == new_md5, 'the write did not take'
print('\nWRITTEN — live store is now %s (re-read and asserted).' % back)
