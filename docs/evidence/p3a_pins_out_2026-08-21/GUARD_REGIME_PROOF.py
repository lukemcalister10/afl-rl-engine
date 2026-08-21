#!/usr/bin/env python3
"""GUARD_REGIME_PROOF — PLAN_v6 3a: the pins left the engine and the guards did not move.

WHAT THIS PROVES, AND WHAT IT DOES NOT. The expensive half of 3a's assurance is the BOARD, and it is
not proved here: `tools/land lever` builds the board from this tree and asserts it is
b3e8da99bc7f632e5d1eebc732f9cf01 byte-exact, which is the standing falsifier of the whole act. What
IS proved here is the half a board build cannot show — that moving the values changed no guard's
FIRING REGIME and no guard's halt text:

  A. STRUCTURAL — the pin read happens INSIDE each dial's own branch. `_sheet_pins()` is called from
     exactly two places; the ORDER 41 call is lexically inside `if _O41_INJ:` and the ORDER 42 call is
     lexically inside `def _o42_state`. A build with the dial off therefore reads the declaration not
     at all, exactly as it read the literals not at all before. Checked on the AST, not by eye.

  B. TEXTUAL — every ORDER 41 and ORDER 42 halt message in the edited file is byte-identical to the
     pre-edit file's, and the pinned VALUES are byte-identical to the literals that were removed.
     Checked against `git show <pre-edit>:engine/rl_after/_merged_recover.py`.

  C. FUNCTIONAL — `_sheet_pins()` itself, lifted out of the module and exercised against a real
     temporary tree: a good declaration returns the three pinned facts; an ABSENT file, a MALFORMED
     file, a file with a missing key, and a file re-pointed at a different owner input each HALT
     fail-closed. A drifted md5/row/injured count is NOT tested here because the drift assertion is
     the ORDER 41/42 code that B proves byte-unchanged — it compares the sheet against whatever
     _sheet_pins() returns, and it cannot tell where the value came from.

Run:  python3 docs/evidence/p3a_pins_out_2026-08-21/GUARD_REGIME_PROOF.py [--pre <commit>]
Exit 0 = every check PASS. Any FAIL exits non-zero; there is no verdict-free path.
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.environ.get('RL_REPO') or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENGINE_REL = 'engine/rl_after/_merged_recover.py'
PIN_REL = 'data/sheet_pins.json'
SHEET_REL = 'docs/owner_annotations/SITTER_2026_v1.csv'

RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))
    print('%-6s %-52s %s' % ('PASS' if ok else '*FAIL*', name, detail))
    return bool(ok)


# --------------------------------------------------------------------------- A. STRUCTURAL (AST)
def enclosing_chain(tree, target_lineno):
    """The chain of enclosing statements around a line, outermost first."""
    chain = []

    def rec(node, path):
        for child in ast.iter_child_nodes(node):
            lo, hi = getattr(child, 'lineno', None), getattr(child, 'end_lineno', None)
            if lo is None or hi is None or not (lo <= target_lineno <= hi):
                continue
            rec(child, path + [child])
            if len(path) + 1 > len(chain):
                del chain[:]
                chain.extend(path + [child])

    rec(tree, [])
    return chain


def describe(node):
    if isinstance(node, ast.FunctionDef):
        return 'def %s' % node.name
    if isinstance(node, ast.If):
        return 'if %s' % ast.unparse(node.test)[:60]
    return type(node).__name__


def structural(src):
    tree = ast.parse(src)
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == '_sheet_pins':
            calls.append(node.lineno)
    calls = sorted(set(calls))
    check('A1 _sheet_pins() called from exactly two sites', len(calls) == 2, 'lines %s' % calls)
    if len(calls) != 2:
        return
    o41, o42 = calls[0], calls[1]
    c41 = [describe(n) for n in enclosing_chain(tree, o41)]
    c42 = [describe(n) for n in enclosing_chain(tree, o42)]
    check('A2 ORDER 41 read is inside `if _O41_INJ:`', 'if _O41_INJ' in c41,
          ' > '.join(c41[-3:]))
    check('A3 ORDER 42 read is inside `def _o42_state`', 'def _o42_state' in c42,
          ' > '.join(c42[-3:]))
    check('A4 ORDER 41 read precedes the ORDER 42 read in the file (halts FIRST)', o41 < o42,
          'line %d < line %d' % (o41, o42))
    top = {n.name for n in ast.walk(tree)
           if isinstance(n, ast.FunctionDef) and n.name == '_sheet_pins'}
    check('A5 _sheet_pins is defined once, at module level', top == {'_sheet_pins'}
          and sum(1 for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == '_sheet_pins') == 1)
    # No module-level literal survives: the six removed names must not be assigned outside a guard.
    stray = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                for nm in ast.walk(t):
                    if isinstance(nm, ast.Name) and nm.id in (
                            'O41_INJ_MD5', 'O41_INJ_ROWS', 'O41_INJ_Y',
                            '_SHEET_MD5', '_SHEET_ROWS', '_SHEET_Y'):
                        if isinstance(node.value, (ast.Constant,)):
                            stray.append((nm.id, node.lineno))
    check('A6 no pin LITERAL survives in the engine', not stray, str(stray) or 'none')


# ----------------------------------------------------------------------------- B. TEXTUAL (vs git)
HALT_RE = re.compile(r"'(ORDER 4[12] HALT:[^']*)'")


def textual(src, pre_src):
    now = HALT_RE.findall(src)
    was = HALT_RE.findall(pre_src)
    check('B1 ORDER 41/42 halt-message fragments byte-identical', now == was,
          '%d fragment(s), equal' % len(now) if now == was
          else 'now=%d was=%d' % (len(now), len(was)))
    lits = re.findall(r"O41_INJ_MD5\s*=\s*'([0-9a-f]{32})'|_SHEET_MD5\s*=\s*'([0-9a-f]{32})'", pre_src)
    old_md5 = sorted({a or b for a, b in lits})
    old_rows = sorted(set(re.findall(r"O41_INJ_ROWS\s*=\s*(\d+)|_SHEET_ROWS\s*=\s*(\d+)", pre_src)[0]
                          ) - {''})
    pins = json.load(open(os.path.join(ROOT, PIN_REL), encoding='utf-8'))
    check('B2 pinned md5 == the removed literal', old_md5 == [pins['sheet_md5']],
          '%s' % pins['sheet_md5'])
    check('B3 pinned rows == the removed literal', old_rows == [str(pins['sheet_rows'])],
          str(pins['sheet_rows']))
    old_y = sorted({x for pair in re.findall(r"O41_INJ_Y\s*=\s*(\d+)|_SHEET_Y\s*=\s*(\d+)", pre_src)
                    for x in pair} - {''})
    check('B4 pinned injured=Y == the removed literal', old_y == [str(pins['sheet_injured_y'])],
          str(pins['sheet_injured_y']))
    # And the declaration still describes the sheet that is actually in the tree.
    import csv
    import hashlib
    raw = open(os.path.join(ROOT, SHEET_REL), 'rb').read()
    rows = list(csv.DictReader(raw.decode('utf-8').splitlines()))
    ys = [r for r in rows if (r.get('injured') or '').strip().upper() == 'Y']
    check('B5 the declaration matches the sheet in the tree',
          hashlib.md5(raw).hexdigest() == pins['sheet_md5'] and len(rows) == pins['sheet_rows']
          and len(ys) == pins['sheet_injured_y'],
          'md5=%s rows=%d Y=%d' % (hashlib.md5(raw).hexdigest()[:12], len(rows), len(ys)))


# ------------------------------------------------------------------------------ C. FUNCTIONAL
LOADER_RE = re.compile(r"^_SHEET_PIN_REL=.*?^    return _po$", re.S | re.M)


def lift_loader(src):
    """Lift `_sheet_pins()` out of the module so it can be exercised without a board build."""
    m = LOADER_RE.search(src)
    if not m:
        return None
    ns = {'os': os}
    exec(compile(m.group(0), '<lifted _sheet_pins>', 'exec'), ns)
    return ns


def functional(src):
    ns = lift_loader(src)
    if not check('C0 _sheet_pins() lifted out of the module', ns is not None):
        return
    fn = ns['_sheet_pins']
    real = json.load(open(os.path.join(ROOT, PIN_REL), encoding='utf-8'))

    def run(tree_setup):
        ns['_SHEET_PIN_CACHE'][0] = None
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, 'data'))
            tree_setup(td)
            old = os.environ.get('RL_REPO')
            os.environ['RL_REPO'] = td
            try:
                return ('ok', fn())
            except SystemExit as e:
                return ('halt', str(e))
            finally:
                if old is None:
                    os.environ.pop('RL_REPO', None)
                else:
                    os.environ['RL_REPO'] = old

    def write(doc):
        return lambda td: open(os.path.join(td, PIN_REL), 'w', encoding='utf-8').write(
            json.dumps(doc, indent=2))

    kind, val = run(write(real))
    check('C1 a good declaration returns the three pinned facts',
          kind == 'ok' and val == (real['sheet_md5'], real['sheet_rows'], real['sheet_injured_y']),
          repr(val)[:70])

    kind, val = run(lambda td: None)
    check('C2 an ABSENT declaration HALTS fail-closed',
          kind == 'halt' and 'SHEET-PIN HALT' in val and 'ABSENT' in val, val[:70])

    kind, val = run(lambda td: open(os.path.join(td, PIN_REL), 'w').write('{not json'))
    check('C3 a MALFORMED declaration HALTS', kind == 'halt' and 'SHEET-PIN HALT' in val, val[:70])

    holed = {k: v for k, v in real.items() if k != 'sheet_md5'}
    kind, val = run(write(holed))
    check('C4 a declaration with a MISSING pin HALTS',
          kind == 'halt' and 'missing' in val, val[:70])

    repointed = dict(real, sheet_path='docs/owner_annotations/SOMETHING_ELSE.csv')
    kind, val = run(write(repointed))
    check('C5 a declaration RE-POINTED at another owner input HALTS',
          kind == 'halt' and 'will not be re-pointed' in val, val[:70])

    drifted = dict(real, sheet_md5='0' * 32)
    kind, val = run(write(drifted))
    check('C6 a DRIFTED md5 is returned to the guard, not swallowed here',
          kind == 'ok' and val[0] == '0' * 32,
          'the ORDER 41/42 compare (B1: byte-unchanged) is what halts on it')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pre', default=None,
                    help='the commit holding the PRE-EDIT engine file (default: the commit that '
                         'last changed it before HEAD)')
    a = ap.parse_args()
    src = open(os.path.join(ROOT, ENGINE_REL), encoding='utf-8').read()
    pre = a.pre
    if not pre:
        out = subprocess.run(['git', 'log', '-2', '--format=%H', '--', ENGINE_REL],
                             cwd=ROOT, stdout=subprocess.PIPE).stdout.decode().split()
        pre = out[1] if len(out) > 1 else 'HEAD~1'
    p = subprocess.run(['git', 'show', '%s:%s' % (pre, ENGINE_REL)], cwd=ROOT,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        print('cannot read the pre-edit engine file at %s: %s' % (pre, p.stderr.decode()[-200:]))
        return 2
    pre_src = p.stdout.decode('utf-8')

    print('GUARD REGIME PROOF — PLAN_v6 3a, the pins out of the engine')
    print('root       %s' % ROOT)
    print('pre-edit   %s' % pre)
    print('=' * 96)
    print('A. STRUCTURAL — the pin read is inside each dial\'s own branch')
    structural(src)
    print('')
    print('B. TEXTUAL — the halts and the values are byte-unchanged')
    textual(src, pre_src)
    print('')
    print('C. FUNCTIONAL — the loader itself, fail-closed in every direction')
    functional(src)
    print('=' * 96)
    bad = [n for n, ok, _ in RESULTS if not ok]
    print('%d check(s): %d PASS, %d FAIL' % (len(RESULTS), len(RESULTS) - len(bad), len(bad)))
    if bad:
        print('FAILED: %s' % ', '.join(bad))
        return 1
    print('VERDICT: PASS — the pins moved, the guards did not.')
    print('NOT PROVED HERE, PROVED BY THE LANDER: the built board is byte-identical '
          '(b3e8da99bc7f632e5d1eebc732f9cf01).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
