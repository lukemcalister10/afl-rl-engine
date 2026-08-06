#!/usr/bin/env python3
"""#334 STAGE A pre-flight — INDEPENDENT RE-PARSE of the owner's corrected sheet.

Reproduces census.json's four headline numbers from the xlsx bytes, and additionally
emits the (key, season) list of ZERO-CONFIRMATIONS, which census.json carries only as a
count (177). That list is needed to make ADDENDUM 1's no-change assert non-vacuous:
"the zero-row players' training-cell count unchanged, as a number".

Matching is on (cohort year, type, pick) against the store, never on name — the two
distinct Will Hamills are the trap this rule exists for. Name is checked, not trusted.
"""
import json, sys, openpyxl

SHEET, STORE, CENSUS, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

store = json.load(open(STORE))
by_key = {r['key']: r for r in store}
idx = {}
for r in store:
    idx.setdefault((r.get('year'), r.get('type'), r.get('pick')), []).append(r)

ws = openpyxl.load_workbook(SHEET)['players']
rows = list(ws.iter_rows(min_row=8, values_only=True))

inserts, zeros, conflicts, unmatched, predraft = [], [], [], [], []
for row in rows:
    cohort, typ, pick, name, pos = row[0], row[1], row[2], row[3], row[4]
    if cohort is None or name is None:
        continue
    cand = idx.get((cohort, typ, pick), [])
    if len(cand) != 1:
        cand = [r for r in cand if r.get('player') == name] or cand
    if len(cand) != 1:
        unmatched.append((cohort, typ, pick, name)); continue
    rec = cand[0]
    have = {s['year'] for s in (rec.get('scoring') or [])}
    for season, gcell, acell in ((2005, row[5], row[6]), (2006, row[7], row[8])):
        if cohort == 2005 and season == 2005:
            predraft.append((rec['key'], season)); continue          # grey: pre-draft
        g = 0 if gcell in (None, '', 'pre-draft') else gcell
        if isinstance(g, str):
            predraft.append((rec['key'], season)); continue
        if season in have:
            # a store row already exists — the sheet may only confirm it
            existing = [s for s in rec['scoring'] if s['year'] == season][0]
            if int(g or 0) and int(g) != int(existing['games']):
                conflicts.append((rec['key'], season, int(g), existing['games']))
            continue
        if int(g or 0) > 0:
            inserts.append({'key': rec['key'], 'year': season,
                            'games': int(g), 'avg': round(float(acell), 1),
                            'pos_hint': pos})
        else:
            zeros.append((rec['key'], season))

census = json.load(open(CENSUS))
c_ins = sorted((i['key'], i['year'], i['games'], i['avg']) for i in census['inserts'])
m_ins = sorted((i['key'], i['year'], i['games'], i['avg']) for i in inserts)

print('RE-PARSE of %s' % SHEET)
print('  sheet data rows        %d' % len(rows))
print('  inserts   mine %3d   census %3d   IDENTICAL: %s'
      % (len(m_ins), len(c_ins), m_ins == c_ins))
print('  zero-confirmations     mine %3d   census %3d   MATCH: %s'
      % (len(zeros), census['zero_confirmations'], len(zeros) == census['zero_confirmations']))
print('  conflicts mine %d  census %d' % (len(conflicts), len(census['conflicts'])))
print('  unmatched names        %d   %s' % (len(unmatched), unmatched[:5]))
print('  pre-draft cells skipped %d' % len(predraft))
if m_ins != c_ins:
    only_m = [x for x in m_ins if x not in c_ins]; only_c = [x for x in c_ins if x not in m_ins]
    print('  ONLY MINE  ', only_m)
    print('  ONLY CENSUS', only_c)
json.dump({'inserts': inserts, 'zero_confirmations': sorted(zeros),
           'conflicts': conflicts, 'unmatched': unmatched},
          open(OUT, 'w'), indent=1)
print('  zero-confirmation (key,season) list written -> %s' % OUT)
ok = (m_ins == c_ins and len(zeros) == census['zero_confirmations']
      and not conflicts and not unmatched)
print('RE-PARSE %s' % ('REPRODUCES THE CENSUS' if ok else 'DOES NOT REPRODUCE — HALT'))
raise SystemExit(0 if ok else 1)
