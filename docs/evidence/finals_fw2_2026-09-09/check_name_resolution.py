#!/usr/bin/env python3
"""EVERY NAME IN THE SCORE FILE LANDS ON EXACTLY ONE STORE ROW — asserted, not assumed.

Two files resolve the same 183 names and they resolve them DIFFERENTLY: the edit plan maps a CSV
name to a store KEY, and the report emitter maps a CSV name to a store DISPLAY NAME. Both are
correct and neither can be dropped — the plan runs against store rows, the emitter runs against the
shipped board bundle, which carries names and not keys.

Two maps of the same fact is exactly the drift the estate refuses everywhere else, so it is checked
instead: for every abbreviated name, the plan's key and the emitter's display name must land on THE
SAME STORE ROW. A name that reached the store under one key and is reported under another would
sail through both files and fail nothing until the report's reconciliation, at the end of a
landing, on a tree that has already moved.

No engine, no board, one second. Run it before the plan, not after.

    python3 docs/evidence/finals_fw2_2026-09-09/check_name_resolution.py
"""
import ast
import collections
import csv
import io
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')
SCORES = os.path.join(REPO, 'scores', 'FW2.csv')
PLAN_SRC = os.path.join(HERE, 'pass_finals_edit_plan.py')
EMIT_SRC = os.path.join(REPO, 'docs', 'evidence', 'fw2_report_2026-09-09', 'emit_fw2_report.py')


def _norm(s):
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower())


def _literal(path, name):
    """Read a dict literal out of a source file rather than importing it — the plan imports the
    engine at module scope and this check must stay engine-free."""
    src = io.open(path, encoding='utf-8').read()
    m = re.search(r'^\s*%s = (\{[^}]*\})' % name, src, re.S | re.M)
    if not m:
        raise SystemExit('HALT: %s carries no %s map' % (os.path.basename(path), name))
    return ast.literal_eval(re.sub(r'#[^\n]*', '', m.group(1)))


def main():
    rows = json.load(io.open(STORE, encoding='utf-8'))
    by_name = collections.defaultdict(list)
    for p in rows:
        by_name[_norm(p.get('player'))].append(p)
    by_key = {p['key']: p for p in rows if p.get('key')}

    plan_map = _literal(PLAN_SRC, 'OVERRIDE')          # csv name (lower) -> store key
    emit_map = _literal(EMIT_SRC, 'ALIASES')           # csv name        -> store display name
    emit_lower = {k.lower(): v for k, v in emit_map.items()}

    fails = []
    if set(plan_map) != set(emit_lower):
        fails.append('the two maps cover different names: plan %s vs emitter %s'
                     % (sorted(plan_map), sorted(emit_lower)))
    for csv_name, key in sorted(plan_map.items()):
        row_by_key = by_key.get(key)
        disp = emit_lower.get(csv_name)
        cands = [x for x in by_name[_norm(disp)] if not x.get('_retired')] if disp else []
        if row_by_key is None:
            fails.append('%r -> key %r is not a store row' % (csv_name, key))
        elif len(cands) != 1:
            fails.append('%r -> display %r resolves to %d rows' % (csv_name, disp, len(cands)))
        elif cands[0] is not row_by_key:
            fails.append('%r: the plan lands on %s and the emitter on %s — the same name reaching '
                         'the store and the report as two different players'
                         % (csv_name, row_by_key.get('key'), cands[0].get('key')))
        else:
            print('  [OK] %-16s -> %-22s %-20s (%s)'
                  % (csv_name, key, row_by_key.get('player'), row_by_key.get('afl_club')))

    listed, unresolved, ambiguous = 0, [], []
    with io.open(SCORES, encoding='utf-8') as fh:
        for row in csv.reader(fh):
            if not row or not row[0].strip() or row[0].strip().lower() == 'player':
                continue
            listed += 1
            nm = row[0].strip()
            if nm.lower() in plan_map:
                continue
            cands = [x for x in by_name[_norm(nm)] if not x.get('_retired')]
            if not cands:
                unresolved.append(nm)
            elif len(cands) > 1:
                ambiguous.append((nm, [c.get('key') for c in cands]))
    if unresolved:
        fails.append('%d name(s) match no store row: %s' % (len(unresolved), unresolved))
    if ambiguous:
        fails.append('%d name(s) are ambiguous and need an override: %s' % (len(ambiguous), ambiguous))

    print('  [OK] %d listed names, every one on exactly one non-retired store row' % listed)
    if fails:
        print('\n'.join('  [FAIL] ' + f for f in fails))
        raise SystemExit(1)
    print('NAME RESOLUTION: clean')


if __name__ == '__main__':
    main()
