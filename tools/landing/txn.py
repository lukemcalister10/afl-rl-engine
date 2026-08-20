"""tools/landing/txn.py — THE DRIVER: fail-closed sequencing, per-step timing, and the abort path.

THE ABORT PATH IS PART OF THE PROGRAM, NOT AN AFTERTHOUGHT (PLAN_v6 2a.3). A landing that fails
mid-flight restores every carrier to the identity captured at step 0, asserts the restoration
BYTE-EXACT, and reports the failed step. There is no partial-success exit: either the transaction
completed and every step's postcondition held, or the tree is back where it started and the program
says which step it could not complete.

THE RECOVERY LADDER, STATED HONESTLY AND PRINTED AT EVERY ABORT (the plan's own words):
    abort-then-retry is the recovery; a landing the lander cannot complete after abort+retry is a
    round that SLIPS, on the owner's call — never an improvised manual landing under pressure.

STEP TIMING IS MACHINE-RECORDED, ALWAYS (the M2 measure-then-quote ruling, A-F12). Every step is
timed whether it succeeds or fails, the table is printed at the end of every run including aborted
ones, and the timings go into the claims file. The estate's rule is that a target is quoted only
after it is measured; a lander that did not measure itself could never be honestly quoted.
"""

import fcntl
import json
import os
import socket
import subprocess
import sys
import time

from tools.landing import carriers as CA
from tools.landing import steps as ST


LOCK_FILE_DEFAULT = '/home/claude/.rl_build.lock'


class Options(object):
    __slots__ = ('dry_run', 'no_commit', 'selftest', 'quiet')

    def __init__(self, dry_run=False, no_commit=False, selftest=False, quiet=False):
        self.dry_run = dry_run
        self.no_commit = no_commit
        self.selftest = selftest
        self.quiet = quiet


# ------------------------------------------------------------------------------------- the builders
class RealBuilder(object):
    """The only builder a landing may use: the accepted disposable FV builder, in a child process."""

    name = 'real'

    def build(self, ctx, tag, mode='dev', env_overrides=None):
        out_prefix = os.path.join(ctx.work_dir, 'build_%s' % tag)
        argv = [sys.executable, os.path.join(ctx.lander_dir, '_build_child.py'), ctx.root, tag, mode,
                out_prefix, json.dumps(env_overrides or {})]
        env = ctx.child_env()
        t0 = time.time()
        p = subprocess.run(argv, cwd=ctx.root, capture_output=True, text=True, env=env, timeout=5400)
        el = time.time() - t0
        ctx.write_evidence('build_%s.txt' % tag, (p.stdout or '') + (p.stderr or ''))
        meta_p = out_prefix + '.meta.json'
        if not os.path.isfile(meta_p):
            raise ST.StepError('the build child produced no meta: %s\n%s'
                               % (meta_p, ((p.stdout or '') + (p.stderr or ''))[-2000:]))
        meta = json.load(open(meta_p, encoding='utf-8'))
        meta['board_path'] = out_prefix + '.board.json'
        meta['sidecar_path'] = out_prefix + '.board.json.srcmd5'
        meta['stdout_path'] = out_prefix + '.stdout'
        meta['elapsed_s'] = round(el, 1)
        return meta


class SelftestBuilder(object):
    """SELF-TEST ONLY. Produces a board WITHOUT running the engine, so a fault case costs seconds.

    It is refused unless `--selftest` is passed, and it is never used by the clean end-to-end run —
    which uses RealBuilder and must reproduce the tree's own board identity. The distinction matters
    and is stated rather than buried: the fault cases prove the TRANSACTION (detection, abort,
    byte-exact restore); the clean run proves the transaction ON A REAL BUILD.

    `moved=True` appends one newline to the installed board, which is still valid JSON and has a
    different md5 — a synthetic board move, enough to drive pins / column / lineage for real.
    """

    def __init__(self, moved=False, wrong=False):
        self.moved = moved
        self.wrong = wrong
        self.name = 'selftest%s%s' % ('-moved' if moved else '', '-wrong' if wrong else '')

    def build(self, ctx, tag, mode='dev', env_overrides=None):
        import hashlib
        import shutil
        src = os.path.join(ctx.root, 'data', 'rl_build', 'rl_app_data.json')
        dst = os.path.join(ctx.work_dir, 'build_%s.board.json' % tag)
        shutil.copyfile(src, dst)
        if self.moved:
            with open(dst, 'ab') as fh:
                fh.write(b'\n')
        board_md5 = hashlib.md5(open(dst, 'rb').read()).hexdigest()
        store_md5 = hashlib.md5(open(os.path.join(ctx.root, 'engine', 'rl_after',
                                                  'rl_model_data.json'), 'rb').read()).hexdigest()
        with open(dst + '.srcmd5', 'w', encoding='utf-8') as fh:
            json.dump({'derived': 'rl_app_data.json', 'own_md5': board_md5,
                       'source': 'rl_model_data.json', 'source_md5': store_md5, 'tier': 1}, fh)
        reported = board_md5 if not self.wrong else ('0' * 31 + '1')
        return {'rc': 0, 'board_md5': reported, 'board_path': dst, 'sidecar_path': dst + '.srcmd5',
                'elapsed_s': 0.0, 'stdout_path': None, 'tag': tag, 'mode': mode}


BUILDERS = {'real': RealBuilder, 'selftest': lambda: SelftestBuilder(),
            'selftest-moved': lambda: SelftestBuilder(moved=True),
            'selftest-wrong': lambda: SelftestBuilder(wrong=True)}


# --------------------------------------------------------------------------------- fault injection
def _fault_dirty_tree(ctx):
    open(os.path.join(ctx.root, 'LANDING_FAULT_DIRT.txt'), 'w').write('injected dirt\n')


def _fault_wrong_board(ctx):
    ctx.builder = SelftestBuilder(wrong=True)


def _fault_board_corrupt(ctx):
    with open(os.path.join(ctx.root, 'data', 'rl_build', 'rl_app_data.json'), 'ab') as fh:
        fh.write(b' ')


def _fault_chain_broken(ctx):
    p = os.path.join(ctx.root, 'data', 'release_lineage.json')
    d = json.load(open(p, encoding='utf-8'))
    d['release_transition_register'][-1]['destination']['board'] = 'f' * 32
    open(p, 'w', encoding='utf-8').write(json.dumps(d, indent=1))


def _fault_seal_broken(ctx):
    p = os.path.join(ctx.root, 'data', 'release_contract.json')
    d = json.load(open(p, encoding='utf-8'))
    d['contract_sha256'] = 'd' * 64
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, indent=2)


def _fault_sidecar_corrupt(ctx):
    p = os.path.join(ctx.root, 'engine', 'rl_after', 'ingestion', 'sibling_repin_state.json')
    open(p, 'w', encoding='utf-8').write('{ this is not json')


def _fault_skip_second_writer(ctx):
    ctx.skip_second_ui_writer = True


def _fault_gate_red(ctx):
    p = os.path.join(ctx.root, 'data', 'expected_boot.json')
    raw = open(p, encoding='utf-8').read()
    boot = json.loads(raw)
    open(p, 'w', encoding='utf-8').write(raw.replace(boot['board'], 'a' * 32))


def _fault_false_claim(ctx):
    ctx.false_claim = True


def _fault_foreign_path(ctx):
    open(os.path.join(ctx.root, 'docs', 'LANDING_FAULT_FOREIGN.md'), 'w').write('not a carrier\n')


#: step -> (mode name, what it breaks, the injector). ONE per step: the plan asks for each step
#: broken once, and each of these breaks the thing that step exists to check.
FAULTS = {
    'preflight':    ('dirty_tree', 'an uncommitted file appears before the restore point',
                     _fault_dirty_tree),
    'build_proofs': ('wrong_board', 'the build reports a board that is not the prereg prediction',
                     _fault_wrong_board),
    'pins':         ('board_corrupt', 'the installed board no longer matches what was built',
                     _fault_board_corrupt),
    'lineage':      ('chain_broken', 'the register tail names a board no movers report can bridge',
                     _fault_chain_broken),
    'contract':     ('seal_broken', 'the contract seal does not verify BEFORE the act',
                     _fault_seal_broken),
    'sibling':      ('sidecar_corrupt', 'the sibling provenance sidecar is unreadable',
                     _fault_sidecar_corrupt),
    'ui':           ('skip_second_writer', 'THE THRICE-PROVEN TRAP: writer 2 never runs',
                     _fault_skip_second_writer),
    'gates':        ('gate_red', 'a landed pin is wrong, so the manifest gate reds',
                     _fault_gate_red),
    'claims':       ('false_claim', 'the claims file carries a claim the tree contradicts',
                     _fault_false_claim),
    'commit':       ('foreign_path', 'a file outside the declared carrier set is in the tree',
                     _fault_foreign_path),
}


# ------------------------------------------------------------------------------------- the context
class Ctx(object):
    """Everything a step is allowed to know. A step never reaches for global state."""

    def __init__(self, root, spec, opts, evidence_dir=None, builder=None, fault=None,
                 carriers=CA.LEVER_CARRIERS, work_dir=None, lock_tag=None):
        self.root = os.path.abspath(root)
        self.spec = spec
        self.opts = opts
        self.carriers = carriers
        self.builder = builder or RealBuilder()
        self.fault = fault                       # 'step' or 'step:mode'
        self.facts = {}
        self.snapshot = None
        self.timings = []                        # [(step, seconds, verdict)]
        self.lines = []
        self.lock_tag = lock_tag or ('land-lever-%d' % os.getpid())
        self._lock_fd = None
        self.lander_dir = os.path.dirname(os.path.abspath(__file__))
        self.work_dir = work_dir or os.path.join(
            os.environ.get('RL_LANDING_SNAPSHOT_DIR') or '/tmp', 'landing_work_%d' % os.getpid())
        os.makedirs(self.work_dir, exist_ok=True)
        self.evidence_dir = evidence_dir or os.path.join(self.root, spec.get('evidence_dir') or
                                                         'docs/evidence/landing_%s' % spec.get('date', 'undated'))
        # fault-injection flags a step reads; all default to the safe value
        self.skip_second_ui_writer = False
        self.false_claim = False
        self.abort_report = None

    # -------------------------------------------------------------------------------- plumbing
    def log(self, msg):
        self.lines.append(msg)
        if not self.opts.quiet:
            print(msg)
            sys.stdout.flush()

    def write_evidence(self, basename, text):
        os.makedirs(self.evidence_dir, exist_ok=True)
        p = os.path.join(self.evidence_dir, basename)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text if text.endswith('\n') else text + '\n')
        return p

    def child_env(self):
        """The environment a child gets: RL_REPO set to THIS tree, the lock's own var dropped."""
        env = dict(os.environ)
        env.pop('RL_BUILD_LOCK_HELD', None)
        env['RL_REPO'] = self.root
        env['PYTHONHASHSEED'] = env.get('PYTHONHASHSEED', '0')
        return env

    def run(self, argv, timeout=1800):
        p = subprocess.run(argv, cwd=self.root, capture_output=True, text=True,
                           env=self.child_env(), timeout=timeout)
        return p.returncode, (p.stdout or '') + (p.stderr or '')

    def with_child_env(self, fn):
        """Run an in-process writer with the lock's env var out of the way, then put it back."""
        held = os.environ.pop('RL_BUILD_LOCK_HELD', None)
        prev_repo = os.environ.get('RL_REPO')
        os.environ['RL_REPO'] = self.root
        try:
            return fn()
        finally:
            if held is not None:
                os.environ['RL_BUILD_LOCK_HELD'] = held
            if prev_repo is None:
                os.environ.pop('RL_REPO', None)
            else:
                os.environ['RL_REPO'] = prev_repo

    def is_ignorable_dirt(self, status_line):
        """Nothing is ignorable. Kept as one named place so an exception can never be added quietly."""
        return False

    @property
    def claims_path(self):
        return os.path.join(self.root, self.rel_claims_path)

    @property
    def rel_claims_path(self):
        return os.path.join(self.spec.get('evidence_dir') or 'docs/evidence',
                            self.spec.get('claims_file') or 'CLAIMS.json')

    def timings_dict(self):
        return {name: sec for name, sec, _v in self.timings}

    # ------------------------------------------------------------------------------- the lock
    def acquire_lock(self):
        """flock(2), fail-closed, exactly as tools/build_lock.sh does — and for the same reason.

        The kernel arbitrates and the grant is atomic. The holder record is written BEFORE any work
        starts so a waiter has someone to name. RL_BUILD_LOCK_HELD is deliberately NOT exported: the
        config manifest's reject scan treats an unknown RL_-prefixed variable as a model override
        and halts a canonical build, and this process launches canonical builds.
        """
        if os.environ.get('RL_BUILD_LOCK') == '0':
            self.log('build-lock: SKIPPED by RL_BUILD_LOCK=0. This landing is NOT interlocked.')
            return
        path = os.environ.get('RL_BUILD_LOCK_FILE') or LOCK_FILE_DEFAULT
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
        except OSError as e:
            raise ST.StepError('BUILD-LOCK HALT: cannot open %s (%s). A build that cannot prove it '
                               'is the single writer does not start.' % (path, e))
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            holder = ''
            try:
                holder = open(path, encoding='utf-8').readline().strip()
            except OSError:
                pass
            os.close(fd)
            raise ST.StepError('waiting for lock held by %s — refusing to start a second writer '
                               'against the shared workspace.' % (holder or '<unknown>'))
        os.ftruncate(fd, 0)
        os.write(fd, ('%s\t%d\t%s\t%s\t%s\n' % (
            self.lock_tag, os.getpid(), time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            socket.gethostname(), self.root)).encode())
        self._lock_fd = fd
        self.log('build-lock: HELD by %s (pid %d) — single writer for the shared workspace.'
                 % (self.lock_tag, os.getpid()))

    def release_lock(self):
        if self._lock_fd is not None:
            try:
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
                os.close(self._lock_fd)
            except OSError:
                pass
            self._lock_fd = None

    # -------------------------------------------------------------------------- the restore point
    def capture_restore_point(self):
        self.snapshot = CA.Snapshot(self.root, self.carriers,
                                    store_dir=os.path.join(self.work_dir, 'restore_point')).capture()
        return self.snapshot

    # ------------------------------------------------------------------------------ fault hooks
    def fault_point(self, step_name):
        """Called at the START of each step. In a normal landing this does nothing at all."""
        if not self.fault:
            return
        want, _, _mode = self.fault.partition(':')
        if want != step_name:
            return
        if not self.opts.selftest:
            raise ST.StepError('fault injection was requested without --selftest. The lander refuses '
                               'to break itself outside a sandbox.')
        name, what, injector = FAULTS[step_name]
        self.log('*** FAULT INJECTED at step %r: %s — %s' % (step_name, name, what))
        injector(self)


# ------------------------------------------------------------------------------------- the driver
class Result(object):
    __slots__ = ('ok', 'failed_step', 'error', 'timings', 'facts', 'abort', 'ctx')

    def __init__(self, ok, failed_step=None, error=None, timings=(), facts=None, abort=None, ctx=None):
        self.ok = ok
        self.failed_step = failed_step
        self.error = error
        self.timings = list(timings)
        self.facts = facts or {}
        self.abort = abort
        self.ctx = ctx


BANNER = '=' * 102


def run(ctx, sequence=ST.LEVER_SEQUENCE):
    """Execute the sequence fail-closed. On any failure: ABORT, RESTORE, PROVE, REPORT."""
    ctx.log(BANNER)
    ctx.log('LAND %s — %s' % (ctx.spec['act_kind'].upper(), ctx.spec['act']))
    ctx.log('  tree      : %s' % ctx.root)
    ctx.log('  owner word: %s' % ctx.spec['owner_word'])
    ctx.log('  prereg    : %s   predicts board %s'
            % (ctx.spec['prereg'].get('path'), ctx.spec['prereg'].get('board_after')))
    ctx.log('  mode      : %s%s%s builder=%s'
            % ('DRY RUN' if ctx.opts.dry_run else 'APPLY',
               ' (no-commit)' if ctx.opts.no_commit else '',
               ' (SELFTEST)' if ctx.opts.selftest else '', ctx.builder.name))
    if ST.is_no_op(ctx.spec):
        ctx.log('  NOTE      : this act is a DECLARED NO-OP REHEARSAL — it predicts the board it '
                'already has and moves no identity.')
    ctx.log(BANNER)

    failed_step = err = None
    for i, (name, title, fn) in enumerate(sequence):
        ctx.log('')
        ctx.log('--- STEP %d/%d  %-14s %s ---' % (i, len(sequence) - 1, name, title))
        t0 = time.time()
        try:
            ctx.facts[name] = fn(ctx)
            el = time.time() - t0
            ctx.timings.append((name, round(el, 2), 'OK'))
            ctx.log('    [%s OK  %.2fs]' % (name, el))
        except Exception as e:                                        # noqa: BLE001 — deliberate
            el = time.time() - t0
            ctx.timings.append((name, round(el, 2), 'FAIL'))
            failed_step, err = name, e
            ctx.log('    [%s FAILED  %.2fs]' % (name, el))
            break

    if failed_step is None:
        _print_timings(ctx)
        ctx.log('')
        ctx.log(BANNER)
        ctx.log('LANDING COMPLETE — every step\'s postcondition held.')
        ctx.log('SOAK: hand-verification stands until the owner\'s word per act type (G3.iv).')
        ctx.log(BANNER)
        ctx.release_lock()
        return Result(True, timings=ctx.timings, facts=ctx.facts, ctx=ctx)

    abort = _abort(ctx, failed_step, err)
    _print_timings(ctx)
    ctx.release_lock()
    return Result(False, failed_step=failed_step, error=err, timings=ctx.timings, facts=ctx.facts,
                  abort=abort, ctx=ctx)


def _abort(ctx, failed_step, err):
    """THE ABORT PATH. Restore every carrier, prove it byte-exact, report the failed step."""
    ctx.log('')
    ctx.log(BANNER)
    ctx.log('LANDING ABORTED AT STEP %r' % failed_step)
    ctx.log(BANNER)
    for ln in str(err).splitlines():
        ctx.log('  %s' % ln)
    ctx.log('')

    out = {'failed_step': failed_step, 'error': str(err), 'restored': None,
           'byte_exact': None, 'restore_point': None}
    if ctx.snapshot is None:
        ctx.log('NO RESTORE POINT EXISTS: the failure precedes step 0\'s capture, so nothing was '
                'written by this landing and there is nothing to restore. The tree is as the '
                'landing found it.')
        out['restored'] = 'n/a — failure precedes the restore point'
        out['byte_exact'] = 'n/a'
    else:
        moved = ctx.snapshot.diff()
        ctx.log('carriers that moved before the failure: %d' % len(moved))
        for rel, b, a in moved:
            ctx.log('    %-64s %s -> %s' % (rel, (b or 'ABSENT')[:12], (a or 'ABSENT')[:12]))
        actions = ctx.snapshot.restore()
        ctx.log('RESTORING %d carrier(s):' % len(actions))
        for rel, act in actions:
            ctx.log('    %-8s %s' % (act, rel))
        ctx.snapshot.assert_restored()
        ctx.log('')
        ctx.log('ABORT PROOF: every carrier is BYTE-EXACT to the identity captured at step 0.')
        out['restored'] = [{'path': r, 'action': a} for r, a in actions]
        out['byte_exact'] = True
        out['restore_point'] = ctx.snapshot.identities()

    ctx.log('')
    ctx.log('THE RECOVERY LADDER: abort-then-retry is the recovery. A landing this lander cannot')
    ctx.log('complete after abort+retry is a round that SLIPS, on the owner\'s call — never an')
    ctx.log('improvised manual landing under pressure.')
    ctx.log(BANNER)

    try:
        ctx.write_evidence('ABORT_%s.json' % failed_step, json.dumps(out, indent=2, sort_keys=True))
    except OSError:
        pass
    ctx.abort_report = out
    return out


def _print_timings(ctx):
    ctx.log('')
    ctx.log('--- STEP TIMING, MACHINE-RECORDED (the M2 measure-then-quote ruling) ---')
    total = 0.0
    for name, sec, verdict in ctx.timings:
        total += sec
        ctx.log('    %-14s %8.2fs  %s' % (name, sec, verdict))
    ctx.log('    %-14s %8.2fs' % ('TOTAL', total))
