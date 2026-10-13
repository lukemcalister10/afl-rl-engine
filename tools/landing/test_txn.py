#!/usr/bin/env python3
"""The driver's abort ladder, the build-lock warning and the commit step — the holes Phase 0.5
closed (2026-10-13), each one measured here with a fake step or a stub, no board built.

Run:  python3 tools/landing/test_txn.py       (exit 0 = all pass)

What is tested, and what each case looked like before its fix:
  * a step that raises SystemExit (a writer run in-process halting with sys.exit) is a FAILED
    STEP: run() returns a Result and the abort ladder has run. Before: the SystemExit flew out of
    run() past the ladder, no Result, no report, carriers left as the step left them.
  * a KeyboardInterrupt still reaches the operator — but only AFTER the ladder has run.
  * an abort whose assert_restored raises is RECORDED (byte_exact False, the mismatch list) and
    run() still returns a Result, keeping the work dir. Before: CarrierError out of run().
  * BUILD_LOCK=0 is honoured LOUDLY: one WARNING line on stderr and in the transcript, in both
    the Python lander and tools/build_lock.sh. Before: a quiet transcript line / a stdout echo.
  * the commit step runs ctx.before_commit just before it stages, so the launch paperwork
    (PREFLIGHT.json, the self-test transcripts) rides the landing's own commit and the tree reads
    clean afterwards. Before: filed after the commit, untracked, the next run refused a dirty tree.
  * allowed_extra is a path-component match: evidence dir `docs/evidence/x` does NOT admit
    `docs/evidence/xy/...`. Before: a string prefix did.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT)

from tools.landing import carriers as CA                    # noqa: E402
from tools.landing import cli as CLI                        # noqa: E402
from tools.landing import steps as ST                       # noqa: E402
from tools.landing import txn as TX                         # noqa: E402

fails = 0
n = 0
_ctx_n = [0]


def ok(cond, label):
    global fails, n
    n += 1
    print(('  [PASS] ' if cond else '  [FAIL] ') + label)
    if not cond:
        fails += 1


SPEC = {
    'act_kind': 'store-edit', 'act': 'TEST ACT', 'owner_word': 'a test', 'date': '2026-10-13',
    'prereg': {'path': None, 'board_before': 'before', 'board_after': 'after'},
    'identities': {'moves': ['store']}, 'evidence_dir': 'docs/evidence/x',
    'day0_rebase': {'state': 'off'}, 'commit_message': 'test landing commit',
}


def make_ctx(root, tmp, **kw):
    _ctx_n[0] += 1
    return TX.Ctx(root, dict(SPEC), TX.Options(quiet=True),
                  work_dir=os.path.join(tmp, 'work_%d' % _ctx_n[0]), **kw)


def git(root, *argv, env=None):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run(['git'] + list(argv), cwd=root, capture_output=True, text=True, env=e)
    if p.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(argv), p.stdout + p.stderr))
    return p.stdout


def git_repo(tmp, name):
    root = os.path.join(tmp, name)
    os.makedirs(root)
    git(root, 'init', '-q')
    git(root, 'config', 'user.email', 'test@example.invalid')
    git(root, 'config', 'user.name', 'test')
    with open(os.path.join(root, 'README'), 'w') as f:
        f.write('a tree\n')
    write(root, 'docs/evidence/README.md', 'the evidence dirs live here, as in the real tree\n')
    git(root, 'add', 'README', 'docs/evidence/README.md')
    git(root, 'commit', '-q', '-m', 'init')
    return root


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f:
        f.write(text)
    return p


class StubSnapshot(object):
    """A restore point whose proof fails: restore() runs, assert_restored() raises."""
    def __init__(self, restored_ok=False):
        self.restored_ok = restored_ok
        self.restore_calls = 0

    def diff(self):
        return [] if self.restored_ok else [('data/x.json', 'aaa111', 'bbb222')]

    def restore(self):
        self.restore_calls += 1
        return [('data/x.json', 'rewrite')]

    def assert_restored(self):
        if not self.restored_ok:
            raise CA.CarrierError('ABORT DID NOT RESTORE THE TREE. 1 carrier(s) still differ')
        return True

    def identities(self):
        return {'data/x.json': 'aaa111'}


def main():
    tmp = tempfile.mkdtemp(prefix='txn_test_')
    saved_env = dict(os.environ)
    os.environ['LANDING_SNAPSHOT_DIR'] = tmp
    os.environ.pop('BUILD_LOCK', None)
    try:
        print('TXN TESTS\n  ' + '-' * 70)
        root = git_repo(tmp, 'plain')

        # ---- 3. a SystemExit raised by a step is a failed step, not an escape ------------------
        ctx = make_ctx(root, tmp)
        seq = (('fine', 'a step that works', lambda c: {'did': 'something'}),
               ('halt', 'a writer halting in-process', lambda c: sys.exit('HALT: writer refused')),
               ('never', 'must not run', lambda c: {'ran': True}))
        try:
            res = TX.run(ctx, seq)
        except SystemExit as exc:
            res = None
            print('      SystemExit escaped run(): %r' % (exc,))
        ok(isinstance(res, TX.Result), 'a step that raises SystemExit still yields a Result')
        ok(res is not None and not res.ok and res.failed_step == 'halt',
           '...which names the halting step as the failed one')
        ok(res is not None and 'never' not in res.facts, '...and the steps after it did not run')
        ok(res is not None and 'SystemExit' in str(res.error) and 'writer refused' in str(res.error),
           '...and the recorded error says a SystemExit was raised, with its message')
        ok(res is not None and res.abort is not None and res.abort.get('byte_exact') == 'n/a',
           '...and the abort ladder ran (no restore point yet: n/a, as for any pre-capture failure)')
        ok(os.path.isfile(os.path.join(ctx.evidence_dir, 'ABORT_halt.json')),
           '...and wrote its abort record into the evidence dir')
        ok(res is not None and any(v == 'FAIL' and s == 'halt' for s, _t, v in res.timings),
           '...and the step is timed as FAIL like any other')

        # ---- 3b. a KeyboardInterrupt runs the ladder FIRST, then reaches the operator ----------
        ctx = make_ctx(root, tmp)

        def interrupt(c):
            raise KeyboardInterrupt()
        seq = (('fine', 'ok', lambda c: 1), ('ctrlc', 'operator interrupt', interrupt))
        raised = None
        try:
            TX.run(ctx, seq)
        except KeyboardInterrupt as exc:
            raised = exc
        ok(raised is not None, 'a KeyboardInterrupt is re-raised to the operator')
        ok(ctx.abort_report is not None and ctx.abort_report.get('failed_step') == 'ctrlc',
           '...but only AFTER the abort ladder ran and recorded the interrupted step')
        ok(ctx._lock_fd is None, '...and the lock is released before it is re-raised')

        # ---- 4. a restore that cannot be proved is a RESULT, not an exception ----------------
        ctx = make_ctx(root, tmp)
        stub = StubSnapshot(restored_ok=False)

        def capture(c):
            c.snapshot = stub
            return {'captured': True}

        def boom(c):
            raise ST.StepError('the step failed after the capture')
        seq = (('capture', 'take the restore point', capture), ('boom', 'fail', boom))
        try:
            res = TX.run(ctx, seq)
        except CA.CarrierError as exc:
            res = None
            print('      CarrierError escaped run(): %s' % str(exc).splitlines()[0])
        ok(isinstance(res, TX.Result), 'an abort whose assert_restored raises still yields a Result')
        ok(res is not None and res.failed_step == 'boom' and not res.ok,
           '...naming the step that failed, not the restore')
        ok(res is not None and res.abort is not None and res.abort.get('byte_exact') is False,
           '...with byte_exact recorded as False')
        ok(res is not None and res.abort is not None and res.abort.get('mismatch') ==
           [{'path': 'data/x.json', 'before': 'aaa111', 'after': 'bbb222'}],
           '...and the mismatch list naming each carrier that still differs')
        ok(res is not None and 'DID NOT RESTORE' in (res.abort or {}).get('restore_error', ''),
           '...and the CarrierError text kept as restore_error')
        ok(stub.restore_calls == 1, '...after restore() was attempted exactly once')
        ok(os.path.isdir(ctx.work_dir), '...and the work dir (restore point inside) is KEPT')
        rec = os.path.join(ctx.evidence_dir, 'ABORT_boom.json')
        ok(os.path.isfile(rec) and json.load(open(rec)).get('byte_exact') is False,
           '...and the abort record on disk says byte_exact false')
        ok(any('ABORT PROOF FAILED' in ln for ln in ctx.lines),
           '...and the transcript says the proof failed, in those words')
        # the proved path is unchanged
        ctx = make_ctx(root, tmp)
        good = StubSnapshot(restored_ok=True)

        def capture_good(c):
            c.snapshot = good
            return {}
        res = TX.run(ctx, (('capture', 'ok', capture_good), ('boom', 'fail', boom)))
        ok(res.abort.get('byte_exact') is True and not os.path.isdir(ctx.work_dir),
           'a proved restore still reads byte_exact True and discards the work dir')

        # the cli's one report writer says so, loudly, on an unproved abort
        class A(object):
            report = os.path.join(tmp, 'REPORT.json')
            log = os.path.join(tmp, 'FLIGHT.log')
        unproved = TX.Result(False, failed_step='boom', error='x', abort={
            'byte_exact': False, 'mismatch': [{'path': 'data/x.json'}]}, ctx=ctx)
        buf = io.StringIO()
        _stdout = sys.stdout
        sys.stdout = buf
        try:
            CLI._write_reports(A(), ctx, unproved)
        finally:
            sys.stdout = _stdout
        ok('DID NOT RESTORE THE TREE BYTE-EXACT' in buf.getvalue(),
           'cli._write_reports prints the unproved-abort warning')
        ok(json.load(open(A.report))['abort']['byte_exact'] is False,
           '...and the report carries byte_exact false for the caller to fail on')

        # ---- 6. BUILD_LOCK=0 is honoured LOUDLY -------------------------------------------------
        ctx = make_ctx(root, tmp)
        os.environ['BUILD_LOCK'] = '0'
        err = io.StringIO()
        _stderr = sys.stderr
        sys.stderr = err
        try:
            ctx.acquire_lock()
        finally:
            sys.stderr = _stderr
            os.environ.pop('BUILD_LOCK', None)
        ok(ctx._lock_fd is None, 'BUILD_LOCK=0 still skips the lock')
        ok('WARNING' in err.getvalue() and 'BUILD_LOCK=0' in err.getvalue()
           and 'NOT interlocked' in err.getvalue(),
           '...and prints a WARNING line naming BUILD_LOCK=0 on stderr')
        ok(any('WARNING' in ln and 'BUILD_LOCK=0' in ln for ln in ctx.lines),
           '...and the same line is in the transcript')
        ok(err.getvalue().count('\n') == 1, '...as ONE line')
        sh = subprocess.run(['bash', os.path.join(ROOT, 'tools', 'build_lock.sh'), 'run', 'test',
                             '--', 'true'],
                            cwd=ROOT, capture_output=True, text=True,
                            env=dict(os.environ, BUILD_LOCK='0', BUILD_LOCK_FILE=os.path.join(
                                tmp, 'lock')))
        ok(sh.returncode == 0, 'tools/build_lock.sh run ... with BUILD_LOCK=0 still runs the command')
        ok('WARNING' in sh.stderr and 'BUILD_LOCK=0' in sh.stderr,
           '...and prints a WARNING line naming BUILD_LOCK=0 on stderr')
        ok('WARNING' in sh.stdout, '...and on stdout, where the old line was')

        # ---- 8. allowed_extra is a path-component match ---------------------------------------
        root8 = git_repo(tmp, 'commit8')
        ctx = make_ctx(root8, tmp, carriers=())
        write(root8, 'docs/evidence/xy/NOTE.md', 'another act\n')
        try:
            ST.commit(ctx)
            refused = None
        except ST.StepError as exc:
            refused = str(exc)
        ok(refused is not None and 'docs/evidence/xy/NOTE.md' in refused,
           'evidence dir docs/evidence/x does NOT admit docs/evidence/xy/NOTE.md (foreign, refused)')
        ok(not ctx.commits_made and 'NOTE.md' not in git(root8, 'log', '--format=%s', '--name-only'),
           '...and nothing was committed')
        os.remove(os.path.join(root8, 'docs/evidence/xy/NOTE.md'))
        write(root8, 'docs/evidence/x/NOTE.md', 'this act\n')
        write(root8, 'docs/evidence/x/sub/deeper.txt', 'this act too\n')
        out = ST.commit(ctx)
        ok(out.get('committed') and len(ctx.commits_made) == 1,
           'the evidence dir itself and a subdirectory of it are admitted and committed')
        ok(not git(root8, 'status', '--porcelain').strip(), '...and the tree reads clean after')
        ok(ST._under('docs/evidence/x', 'docs/evidence/x')
           and ST._under('docs/evidence/x/', 'docs/evidence/x')
           and ST._under('docs/evidence/x/a/b', 'docs/evidence/x/')
           and not ST._under('docs/evidence/x2', 'docs/evidence/x')
           and not ST._under('docs/evidence', 'docs/evidence/x'),
           '_under: the path itself, with or without a slash, and anything inside it; nothing else')

        # ---- 7. the launch paperwork rides the landing commit ---------------------------------
        root7 = git_repo(tmp, 'commit7')
        ctx = make_ctx(root7, tmp, carriers=())
        ok(isinstance(getattr(ctx, 'before_commit', None), list) and not ctx.before_commit,
           'a fresh Ctx carries an empty before_commit list')
        pre_ev = tempfile.mkdtemp(prefix='preflight_lander_selftest_', dir=tmp)
        write(pre_ev, 'leg_01.txt', 'transcript\n')
        pf_results = [('clean_tree', 'PASS', 'clean', 0.01), ('lock', 'PASS', 'free', 0.02)]
        try:
            CLI._arm_late_filers(ctx, pre_ev, pf_results)
            armed = len(ctx.before_commit)
        except AttributeError as exc:
            armed = 'no such plumbing: %s' % exc
        ok(armed == 2, 'cli._arm_late_filers registers the two filers (%s)' % armed)
        ok(not os.path.exists(os.path.join(ctx.evidence_dir, 'PREFLIGHT.json')),
           '...and writes nothing at arming time (step 0 would refuse a dirty tree)')
        out = ST.commit(ctx)
        paths = out.get('paths') or []
        ok(out.get('committed') and 'docs/evidence/x/PREFLIGHT.json' in paths,
           'the commit step files PREFLIGHT.json and stages it in the landing commit')
        ok(any(p.startswith('docs/evidence/x/preflight_lander_selftest') for p in paths),
           '...and the self-test transcripts too')
        ok(os.path.isfile(os.path.join(root7, 'docs/evidence/x/preflight_lander_selftest/leg_01.txt')),
           '...copied into the evidence dir')
        ok(not os.path.isdir(pre_ev), '...and the temp transcripts dir is gone')
        ok(not git(root7, 'status', '--porcelain').strip(),
           'git status reads CLEAN after the landing commit')
        committed = git(root7, 'show', '--format=', '--name-only', 'HEAD').split()
        ok('docs/evidence/x/PREFLIGHT.json' in committed
           and 'docs/evidence/x/preflight_lander_selftest/leg_01.txt' in committed,
           '...and HEAD carries both files')
        # the post-close fallback calls are no-ops on a landed run
        CLI._file_preflight_evidence(pre_ev, ctx.evidence_dir)
        CLI._file_cheap_preflight(pf_results, ctx.evidence_dir)
        ok(not git(root7, 'status', '--porcelain').strip(),
           '...and the post-close fallback filers leave it clean')
        ok(json.load(open(os.path.join(root7, 'docs/evidence/x/PREFLIGHT.json')))[0]['check']
           == 'clean_tree', '...with the preflight verdicts in the file')

        print('  ' + '-' * 70)
        print('TXN TESTS: %s' % ('ALL %d PASS' % n if not fails else '%d FAIL / %d' % (fails, n)))
        return 1 if fails else 0
    finally:
        os.environ.clear()
        os.environ.update(saved_env)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
