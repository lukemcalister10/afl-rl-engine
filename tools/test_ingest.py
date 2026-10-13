#!/usr/bin/env python3
"""tools/ingest — the holes Phase 0.5 closed (2026-10-13), measured without a landing or a build.

Run:  python3 tools/test_ingest.py       (exit 0 = all pass)

  * a failed app rebuild, smoke test or push STOPS the command with a non-zero exit whose last line
    says the week is landed and committed and names the command to re-run. Before: printed, exit 0.
  * the column id is the WEEK's alone (fw3-finals-week-3-2026) and the spec's date and label are
    the FIRST inputs commit's, so a re-run on a later day regenerates a byte-identical spec and makes
    no second inputs commit. Before: today's day/month in the id, the label and the date.
  * the new id shape still resolves through round_movers.FINALS_COLUMN_PREFIXES and
    finals_report.feed_round_of, which key on the `fw3-` prefix.
"""
import contextlib
import datetime
import io
import os
import shutil
import subprocess
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import ingest as ING                                          # noqa: E402

fails = 0
n = 0


def ok(cond, label):
    global fails, n
    n += 1
    print(('  [PASS] ' if cond else '  [FAIL] ') + label)
    if not cond:
        fails += 1


def fake_subprocess(returncodes):
    """A subprocess stand-in whose run() returns the given exit codes in order, recording argv."""
    calls = []
    codes = list(returncodes)

    def run(argv, **kw):
        calls.append(list(argv))
        rc = codes.pop(0) if codes else 0
        return subprocess.CompletedProcess(argv, rc, stdout='out line\n', stderr='err line\n')
    return types.SimpleNamespace(run=run, calls=calls)


def stops(fn):
    """-> (SystemExit code or None, everything printed)."""
    buf = io.StringIO()
    code = None
    with contextlib.redirect_stdout(buf):
        try:
            fn()
        except SystemExit as exc:
            code = exc.code
    return code, buf.getvalue()


def git(root, *argv, env=None):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run(['git'] + list(argv), cwd=root, capture_output=True, text=True, env=e)
    if p.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(argv), p.stdout + p.stderr))
    return p.stdout


def main():
    tmp = tempfile.mkdtemp(prefix='ingest_test_')
    real_subprocess = ING.subprocess
    try:
        print('INGEST TESTS\n  ' + '-' * 70)

        # ---- 1. a failed rebuild / smoke / push is a non-zero exit with a clear last line ------
        ING.subprocess = fake_subprocess([1])
        code, out = stops(ING.rebuild_app)
        last = out.strip().splitlines()[-1]
        ok(code == 1, 'a failed valueboard.html rebuild exits 1')
        ok('landed and committed' in last and 'bundle_standalone.py' in last,
           '...and the last line says the week is landed and names the rebuild command to re-run')
        ok(len(ING.subprocess.calls) == 1, '...and the smoke test is not attempted after it')

        ING.subprocess = fake_subprocess([0, 1])
        code, out = stops(ING.rebuild_app)
        last = out.strip().splitlines()[-1]
        ok(code == 1, 'a failed smoke test exits 1')
        ok('landed and committed' in last and 'standalone_smoke.mjs' in last,
           '...and the last line says the week is landed and names the command to re-run')

        ING.subprocess = fake_subprocess([0, 0])
        code, out = stops(ING.rebuild_app)
        ok(code is None and 'rebuilt' in out, 'a clean rebuild and smoke test does not stop')

        ING.subprocess = fake_subprocess([1])
        code, out = stops(ING.push_head)
        last = out.strip().splitlines()[-1]
        ok(code == 1, 'a failed push exits 1')
        ok('landed and committed' in last and 'git push origin HEAD' in last,
           '...and the last line says the week is landed and names the push to re-run')
        ok(ING.subprocess.calls == [['git', 'push', 'origin', 'HEAD']], '...after one push attempt')
        ING.subprocess = fake_subprocess([0])
        code, out = stops(ING.push_head)
        ok(code is None and 'pushed' in out, 'a clean push does not stop')
        ING.subprocess = real_subprocess

        # ---- 2. the column id is the week's; the date is the first inputs commit's -------------
        week = {'label': 'FW3', 'feed': 27, 'name': 'FINALS WEEK 3', 'prefix': 'fw3-'}
        resolved = {'a-player': ('A Player', 90), 'b-player': ('B Player', 71)}
        edits = [{'key': 'a-player', 'field': 'scoring[2026].games', 'old': 1, 'new': 2}]
        first = datetime.date(2026, 9, 24)
        s1 = ING.build_spec(week, 'scores/FW3.csv', 'ab' * 32, resolved, edits,
                            'scores/resolved/2026_FW3.json', 'docs/evidence/ingest/2026_FW3',
                            date=first)
        s2 = ING.build_spec(week, 'scores/FW3.csv', 'ab' * 32, resolved, edits,
                            'scores/resolved/2026_FW3.json', 'docs/evidence/ingest/2026_FW3',
                            date=first)
        ok(s1['column']['id'] == 'fw3-finals-week-3-2026',
           'the column id is the week and the season only: %s' % s1['column']['id'])
        ok(s1['date'] == '2026-09-24', 'the spec date is the date passed in (the first inputs commit)')
        ok(s1['column']['label'].startswith('24/9 FINALS WEEK 3'),
           'the column label carries that date, not today: %r' % s1['column']['label'])
        ok(s1 == s2, 'two builds from the same inputs and date are identical (no second commit)')
        later = ING.build_spec(week, 'scores/FW3.csv', 'ab' * 32, resolved, edits,
                               'scores/resolved/2026_FW3.json', 'docs/evidence/ingest/2026_FW3',
                               date=datetime.date(2026, 10, 2))
        ok(later['column']['id'] == s1['column']['id'],
           'a different date does not move the column id')
        today = ING.build_spec(week, 'scores/FW3.csv', 'ab' * 32, resolved, edits,
                               'scores/resolved/2026_FW3.json', 'docs/evidence/ingest/2026_FW3')
        ok(today['date'] == datetime.date.today().isoformat(),
           'with no inputs commit yet, the date is today')
        gf = ING.build_spec({'label': 'GF', 'feed': 29, 'name': 'GRAND FINAL', 'prefix': 'gf-'},
                            'scores/GF.csv', 'cd' * 32, resolved, edits,
                            'scores/resolved/2026_GF.json', 'docs/evidence/ingest/2026_GF',
                            date=first)
        ok(gf['column']['id'] == 'gf-grand-final-2026', 'the grand final: %s' % gf['column']['id'])

        # the consumers that key on the prefix still resolve the new shape
        import round_movers as RM
        import finals_report as FR
        ok(RM.football_column(s1['column']['id'])
           and RM.football_column_name(s1['column']['id']) == 'FINALS WEEK 3',
           'round_movers reads the new id as a FINALS WEEK 3 football column')
        ok(FR.feed_round_of(s1['column']['id'], RM) == 27,
           'finals_report.feed_round_of resolves it to feed round 27')
        ok(FR.feed_round_of(gf['column']['id'], RM) == 29, '...and the grand final to 29')
        from tools.landing import spec as SP
        ok(not SP.validate(s1), 'the generated spec validates')

        # first_inputs_date reads the FIRST commit of the resolved file
        root = os.path.join(tmp, 'repo')
        os.makedirs(os.path.join(root, 'scores', 'resolved'))
        git(root, 'init', '-q')
        git(root, 'config', 'user.email', 'test@example.invalid')
        git(root, 'config', 'user.name', 'test')
        rel = 'scores/resolved/2026_FW3.json'
        ok(ING.first_inputs_date(rel, repo=root) is None, 'an uncommitted resolved file: no date')
        with open(os.path.join(root, rel), 'w') as f:
            f.write('{"a": 1}\n')
        when = {'GIT_AUTHOR_DATE': '2026-09-24T10:00:00+10:00',
                'GIT_COMMITTER_DATE': '2026-09-24T10:00:00+10:00'}
        git(root, 'add', rel)
        git(root, 'commit', '-q', '-m', 'inputs', env=when)
        ok(ING.first_inputs_date(rel, repo=root) == datetime.date(2026, 9, 24),
           'after the inputs commit, its date: 2026-09-24')
        with open(os.path.join(root, rel), 'w') as f:
            f.write('{"a": 2}\n')
        later_when = {'GIT_AUTHOR_DATE': '2026-10-02T10:00:00+10:00',
                      'GIT_COMMITTER_DATE': '2026-10-02T10:00:00+10:00'}
        git(root, 'add', rel)
        git(root, 'commit', '-q', '-m', 'touched again', env=later_when)
        ok(ING.first_inputs_date(rel, repo=root) == datetime.date(2026, 9, 24),
           'a later commit touching the file does not move it: still the FIRST')
        ok(ING.first_inputs_date('scores/resolved/none.json', repo=root) is None,
           'a file git never saw: no date')

        print('  ' + '-' * 70)
        print('INGEST TESTS: %s' % ('ALL %d PASS' % n if not fails else '%d FAIL / %d' % (fails, n)))
        return 1 if fails else 0
    finally:
        ING.subprocess = real_subprocess
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
