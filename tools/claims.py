#!/usr/bin/env python3
"""tools/claims.py — PROOF-CARRYING DELIVERABLES (PLAN_v6 1c): the claims schema and its checker.

    python3 tools/claims.py check  <claims.json> [--root DIR]     verify claims against the tree
    python3 tools/claims.py schema [ACT_TYPE]                     print the required slots
    python3 tools/claims.py selftest                              the negative control, asserted

WHAT THIS RETIRES (G4, named): supervisor RE-DERIVATION of gate-covered facts. Today a seat writes
"store b745002e, board 68be10c7, manifest 40/40, runner GREEN" in prose and a supervisor re-derives
every one of them by hand to find out whether it is true. Those are mechanical claims about a tree
that is sitting right there. A claims file makes them machine-checkable and the checker makes the
re-derivation one command. JUDGMENT REVIEW IS NOT RETIRED and is not touched: whether the act was
the right act, whether the movers look sane, whether the prereg was honest — none of that is here,
and none of it should be.

THE SCHEMA IS FIXED PER ACT TYPE. Fixed, because a free-form claims file is prose with brackets: a
seat under pressure writes down what went well, and the slot nobody filled is the one that mattered.
Three act types, because the estate has three shapes of act:

    lever-landing   an engine/exporter change lands: identities MOVE, and which ones move is the
                    claim. Requires the full identity set before and after, board counts, and the
                    landing gates.
    round-advance   scores are applied and the round advances: as_of_round moves, the store and
                    board move, the movers page is written.
    small-act       tooling, docs, process. NOTHING value-bearing moves, and the claim is exactly
                    that: a list of carriers asserted BYTE-UNMOVED. This is G1's standing falsifier
                    in claims form.

EVERY CLAIM IS RECOMPUTED, NEVER READ BACK. The checker does not compare the claims file to another
file the same seat wrote. It hashes the artifact, parses the JSON, counts the rows, runs the gate.
A checker that verified claims against a seat's own evidence file would certify nothing but the
seat's consistency with itself.

DAY-0 ACTIVATION STATE IS A REQUIRED SLOT ON EVERY LANDING, and the default is OFF. Anything this
act introduces that can be switched — a gate, a lever, a write path — is listed with its day-0
state, and a claim of `on` MUST name the owner word that activated it. A landing that introduces a
switch and says nothing about it is exactly how a write path ships armed.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

SCHEMA_VERSION = 1
ACT_TYPES = ('lever-landing', 'round-advance', 'small-act')

#: Top-level slots every claims file must fill, whatever the act type.
COMMON_SLOTS = ('schema_version', 'act_type', 'act', 'date', 'base_commit', 'owner_word',
                'claims', 'activation')

#: Claim kinds each act type MUST include at least one of. The point of the table is that a slot
#: nobody filled is visible, rather than absent.
REQUIRED_KINDS = {
    'lever-landing': ('file_md5', 'json_field', 'board_count', 'gate'),
    'round-advance': ('file_md5', 'json_field', 'board_count', 'gate'),
    'small-act': ('unmoved', 'gate'),
}


# ------------------------------------------------------------------------------------- primitives
def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _dig(doc, field):
    cur = doc
    for part in field.split('.'):
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


# ------------------------------------------------------------------------------------ claim kinds
def _c_file_md5(root, c):
    p = os.path.join(root, c['path'])
    if not os.path.exists(p):
        return False, 'file absent'
    got = _md5(p)
    return got == c['value'], 'md5 %s (claimed %s)' % (got, c['value'])


def _c_json_field(root, c):
    p = os.path.join(root, c['path'])
    if not os.path.exists(p):
        return False, 'file absent'
    try:
        got = _dig(json.load(open(p, encoding='utf-8')), c['field'])
    except (KeyError, IndexError, ValueError) as e:
        return False, 'field unreadable: %s' % e
    return got == c['value'], '%s = %r (claimed %r)' % (c['field'], got, c['value'])


def _c_unmoved(root, c):
    """The G1 claim: this carrier is byte-identical to what it was before the act.

    `value` is the PRE-ACT identity. The check is deliberately the same computation as file_md5 —
    the difference is what the claim MEANS, and it is worth its own kind because a reader scanning
    a small-act claims file must be able to see, in one column, that the act moved nothing.
    """
    return _c_file_md5(root, c)


def _c_board_count(root, c):
    """Row counts and value totals, recomputed from the board itself."""
    p = os.path.join(root, c.get('path', os.path.join('data', 'rl_build', 'rl_app_data.json')))
    if not os.path.exists(p):
        return False, 'board absent'
    board = json.load(open(p, encoding='utf-8'))
    rows = board.get(c['section'])
    if rows is None:
        return False, 'board has no section %r' % c['section']
    metric = c.get('metric', 'rows')
    got = len(rows) if metric == 'rows' else sum(r.get('v', 0) for r in rows)
    return got == c['value'], '%s.%s = %s (claimed %s)' % (c['section'], metric, got, c['value'])


def _c_gate(root, c):
    """Run the gate and read its verdict off the exit code. No verdict is ever taken on trust."""
    argv = c['argv']
    try:
        p = subprocess.run(argv, cwd=root, capture_output=True, text=True,
                           timeout=int(c.get('timeout_s', 900)),
                           env=dict(os.environ, RL_REPO=root))
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, 'gate could not be run: %s' % e
    want = str(c.get('expect', 'PASS')).upper()
    ok = (p.returncode == 0) if want in ('PASS', 'GREEN', '0') else (p.returncode != 0)
    out = (p.stdout or '') + (p.stderr or '')
    if ok and c.get('match') and c['match'] not in out:
        return False, 'exit %d as expected but %r absent from output' % (p.returncode, c['match'])
    return ok, 'exit %d (expected %s)' % (p.returncode, want)


KINDS = {'file_md5': _c_file_md5, 'json_field': _c_json_field, 'unmoved': _c_unmoved,
         'board_count': _c_board_count, 'gate': _c_gate}


# ---------------------------------------------------------------------------------- the validator
def validate_shape(doc):
    """Structural refusals — a malformed claims file is never 'mostly verified'."""
    bad = []
    for slot in COMMON_SLOTS:
        if slot not in doc:
            bad.append('missing required slot %r' % slot)
    if doc.get('schema_version') != SCHEMA_VERSION:
        bad.append('schema_version %r != %r' % (doc.get('schema_version'), SCHEMA_VERSION))
    at = doc.get('act_type')
    if at not in ACT_TYPES:
        bad.append('act_type %r is not one of %s' % (at, '/'.join(ACT_TYPES)))
        return bad
    claims = doc.get('claims') or []
    if not claims:
        bad.append('no claims — a claims file that claims nothing certifies nothing')
    kinds = {c.get('kind') for c in claims}
    for k in kinds:
        if k not in KINDS:
            bad.append('unknown claim kind %r' % k)
    for need in REQUIRED_KINDS[at]:
        if need not in kinds:
            bad.append('act type %r requires at least one %r claim and has none' % (at, need))

    # DAY-0 ACTIVATION. Present on every landing; OFF unless a named owner word says otherwise.
    act = doc.get('activation')
    if not isinstance(act, dict):
        bad.append('activation must be an object (use {} to state that this act introduces no switch)')
    else:
        for name, spec in act.items():
            if name.startswith('_'):
                continue          # `_doc` keys, the estate's convention for in-file documentation
            if not isinstance(spec, dict) or 'state' not in spec:
                bad.append('activation[%r] must name a state' % name)
                continue
            if str(spec['state']).lower() not in ('off', 'on'):
                bad.append('activation[%r].state %r is neither on nor off' % (name, spec['state']))
            elif str(spec['state']).lower() == 'on' and not spec.get('activated_by'):
                bad.append('activation[%r] claims ON and names no owner word that activated it — '
                           'day-0 state is OFF unless explicitly activated' % name)
    return bad


def check(doc, root):
    """-> (rows, shape_problems). rows = [(ok, kind, label, detail)]."""
    shape = validate_shape(doc)
    rows = []
    for c in (doc.get('claims') or []):
        fn = KINDS.get(c.get('kind'))
        label = c.get('label') or c.get('path') or c.get('name') or c.get('kind')
        if fn is None:
            rows.append((False, c.get('kind'), label, 'unknown claim kind'))
            continue
        try:
            ok, detail = fn(root, c)
        except Exception as e:                                   # noqa: BLE001 - deliberate
            ok, detail = False, '%s: %s' % (type(e).__name__, e)
        rows.append((ok, c['kind'], label, detail))
    return rows, shape


def render(doc, rows, shape, root):
    out = ['=' * 100,
           'CLAIMS CHECK — %s' % (doc.get('act') or '(unnamed act)'),
           '  act type   : %s' % doc.get('act_type'),
           '  date       : %s   base: %s' % (doc.get('date'), doc.get('base_commit')),
           '  owner word : %s' % (doc.get('owner_word') or '(none recorded)'),
           '  tree       : %s' % root,
           '=' * 100]
    switches = {k: v for k, v in (doc.get('activation') or {}).items()
                if not k.startswith('_')}
    for name, spec in sorted(switches.items()):
        out.append('  ACTIVATION  %-40s %s%s' % (name, spec.get('state'),
                                                 '  (by: %s)' % spec['activated_by']
                                                 if spec.get('activated_by') else ''))
    if not switches:
        out.append('  ACTIVATION  (none — this act introduces no switch)')
    out.append('')
    for ok, kind, label, detail in rows:
        out.append('  %-4s %-12s %-46s %s' % ('OK' if ok else 'FAIL', kind, label[:46], detail))
    bad = [r for r in rows if not r[0]]
    out.append('')
    for s in shape:
        out.append('  SHAPE FAIL   %s' % s)
    out.append('CLAIMS: %d of %d verified against the tree; %d shape problem(s)'
               % (len(rows) - len(bad), len(rows), len(shape)))
    out.append('VERDICT: %s' % ('GREEN — every claim recomputed and held'
                                if not bad and not shape else
                                'RED — the deliverable does not carry its own proof'))
    return '\n'.join(out)


# ---------------------------------------------------------------------------- the negative control
def selftest():
    """THE NEGATIVE CONTROL. A deliberately false claim MUST fail. Asserted, not assumed."""
    import tempfile
    ok_n = bad_n = 0

    def a(cond, msg):
        nonlocal ok_n, bad_n
        if cond:
            ok_n += 1
            print('  PASS  %s' % msg)
        else:
            bad_n += 1
            print('  FAIL  %s' % msg)

    tmp = tempfile.mkdtemp(prefix='claims_selftest_')
    os.makedirs(os.path.join(tmp, 'data'), exist_ok=True)
    open(os.path.join(tmp, 'f.txt'), 'w').write('hello\n')
    true_md5 = _md5(os.path.join(tmp, 'f.txt'))
    json.dump({'board': 'abc', 'n': 3}, open(os.path.join(tmp, 'data', 'x.json'), 'w'))
    json.dump({'active': [{'v': 1}, {'v': 2}]}, open(os.path.join(tmp, 'data', 'b.json'), 'w'))

    base = {'schema_version': SCHEMA_VERSION, 'act_type': 'small-act', 'act': 'selftest',
            'date': '2026-08-20', 'base_commit': 'deadbeef', 'owner_word': 'n/a',
            'activation': {}, 'claims': []}

    print('THE NEGATIVE CONTROL — a deliberately false claim must FAIL')

    doc = dict(base, claims=[{'kind': 'unmoved', 'path': 'f.txt', 'value': true_md5},
                             {'kind': 'gate', 'name': 'true', 'argv': [sys.executable, '-c', 'pass']}])
    rows, shape = check(doc, tmp)
    a(all(r[0] for r in rows) and not shape, 'CONTROL: a true claims file verifies GREEN')

    doc = dict(base, claims=[{'kind': 'unmoved', 'path': 'f.txt', 'value': '0' * 32},
                             {'kind': 'gate', 'name': 'true', 'argv': [sys.executable, '-c', 'pass']}])
    rows, _s = check(doc, tmp)
    a(not rows[0][0], 'a FALSE file hash fails (the flipped-hash control)')

    doc = dict(base, act_type='lever-landing',
               claims=[{'kind': 'json_field', 'path': 'data/x.json', 'field': 'board',
                        'value': 'NOT-abc'},
                       {'kind': 'file_md5', 'path': 'f.txt', 'value': true_md5},
                       {'kind': 'board_count', 'path': 'data/b.json', 'section': 'active',
                        'metric': 'rows', 'value': 2},
                       {'kind': 'gate', 'name': 'true', 'argv': [sys.executable, '-c', 'pass']}])
    rows, _s = check(doc, tmp)
    a(not rows[0][0], 'a FALSE identity field fails')

    doc['claims'][0]['value'] = 'abc'
    doc['claims'][2]['value'] = 99
    rows, _s = check(doc, tmp)
    a(not rows[2][0], 'a FALSE row count fails (recounted from the board, not read back)')

    doc['claims'][2]['value'] = 2
    doc['claims'][2]['metric'] = 'value'
    doc['claims'][2]['value'] = 3
    rows, _s = check(doc, tmp)
    a(rows[2][0], 'a TRUE value total holds (1 + 2 == 3)')
    doc['claims'][2]['value'] = 4
    rows, _s = check(doc, tmp)
    a(not rows[2][0], 'a FALSE value total fails')

    doc2 = dict(base, claims=[{'kind': 'unmoved', 'path': 'f.txt', 'value': true_md5},
                              {'kind': 'gate', 'name': 'fails', 'expect': 'PASS',
                               'argv': [sys.executable, '-c', 'import sys;sys.exit(1)']}])
    rows, _s = check(doc2, tmp)
    a(not rows[1][0], 'a gate claimed PASS that exits non-zero fails')

    a(bool(validate_shape(dict(base, activation={'score_write': {'state': 'on'}}))),
      'a switch claimed ON with no owner word is a SHAPE failure (day-0 state is OFF)')
    a(not validate_shape(dict(base, activation={'score_write': {'state': 'on',
                                                                'activated_by': 'owner word x'}},
                              claims=[{'kind': 'unmoved', 'path': 'f.txt', 'value': true_md5},
                                      {'kind': 'gate', 'name': 't',
                                       'argv': [sys.executable, '-c', 'pass']}])),
      'a switch claimed ON that NAMES its owner word is accepted')
    a(any('requires at least one' in s
          for s in validate_shape(dict(base, act_type='lever-landing',
                                       claims=[{'kind': 'gate', 'name': 't', 'argv': ['true']}]))),
      'a lever-landing missing its identity claims is a SHAPE failure (an unfilled slot is visible)')
    a(any('claims nothing' in s for s in validate_shape(dict(base, claims=[]))),
      'a claims file with no claims is refused')

    print('')
    print('CLAIMS SELF-TEST: %d PASS / %d FAIL' % (ok_n, bad_n))
    return 1 if bad_n else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('mode', choices=('check', 'schema', 'selftest'))
    ap.add_argument('claims', nargs='?')
    ap.add_argument('--root', default=os.environ.get('RL_REPO')
                    or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args(argv)

    if a.mode == 'selftest':
        return selftest()
    if a.mode == 'schema':
        at = a.claims or ''
        print('schema_version %d' % SCHEMA_VERSION)
        print('common slots  : %s' % ', '.join(COMMON_SLOTS))
        print('claim kinds   : %s' % ', '.join(sorted(KINDS)))
        for t in ([at] if at in ACT_TYPES else ACT_TYPES):
            print('%-14s: requires at least one of each — %s' % (t, ', '.join(REQUIRED_KINDS[t])))
        return 0

    if not a.claims:
        print('check needs a claims file')
        return 2
    doc = json.load(open(a.claims, encoding='utf-8'))
    root = os.path.abspath(a.root)
    rows, shape = check(doc, root)
    print(render(doc, rows, shape, root))
    return 0 if (all(r[0] for r in rows) and not shape) else 1


if __name__ == '__main__':
    sys.exit(main())
