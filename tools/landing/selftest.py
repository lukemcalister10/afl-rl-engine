"""tools/landing/selftest.py — THE SANDBOX SELF-TEST (PLAN_v6 2a.3).

    tools/land selftest [--only step,step] [--keep] [--evidence DIR]

WHAT IT ASSERTS, and the plan's sentence each assertion comes from:

  * "the program deliberately breaks each step in a sandbox and asserts the failure is caught" —
    every step in LEVER_SEQUENCE is broken exactly once, by a fault that breaks the thing that step
    exists to check (txn.FAULTS), and the run must fail AT THAT STEP.
  * "restores every carrier to its pre-landing identity ... asserts the restoration byte-exact" —
    the PARENT re-hashes every carrier before and after each case and compares them itself. It does
    not read the child's own verdict for this. A self-test that asked the program under test whether
    it had succeeded would certify nothing.
  * "takes the build lock ... asserted in self-test" — one case runs a landing while a second holder
    has the lock, and the landing must refuse to start.
  * "uses explicit-path commits, asserted in self-test" — one case puts a file outside the declared
    carrier set into the tree and the commit step must refuse to sweep it up; the clean control case
    asserts the commit named its paths explicitly.
  * "the claims negative control still fires" — `tools/claims.py selftest` is run inside the sandbox.

THE NON-VACUITY CONTROL, first and always: a CLEAN run with no fault must SUCCEED in the same
sandbox, with the same spec, before any fault case is believed. Ten failing runs prove nothing if
the harness cannot produce a passing one — the estate has retired four instruments that could not
fail, and one (`reconciled_to_f5`) that was an algebraic tautology printing PASS.

THE SANDBOX IS NEVER THE LIVE TREE. It is a `git worktree` of HEAD with the CURRENT lander copied in
and committed inside the sandbox, so the tree under test is clean and carries the code being tested
rather than the code that happened to be committed. The live tree's carriers are hashed before and
after the whole self-test and asserted byte-unmoved — the G1 falsifier, applied to the self-test
itself.

THE fv-PROVENANCE SUITE IS NEVER RUN, here or anywhere in this library (it overwrites a shared
pickle; PLAN_v6 2a.1). The self-test's builds are the SelftestBuilder, which runs no engine at all:
the fault cases prove the TRANSACTION, and the clean end-to-end run with the real builder proves the
transaction on a real build. Which is which is stated in the tally rather than blurred.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools.landing import carriers as CA                                       # noqa: E402
from tools.landing import steps as ST                                          # noqa: E402
from tools.landing import txn as TX                                            # noqa: E402


BANNER = '=' * 102


def _sh(argv, cwd=None, env=None, timeout=3600):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=env, timeout=timeout)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def carrier_md5s(root, carriers=CA.ROUND_CARRIERS):
    """The parent's OWN measurement of every carrier. Never the child's.

    It measures the ROUND set by default, which is a superset of the lever set — so a lever fault
    case that somehow moved a round-only carrier (the store, the sheet, a movers report) would be
    caught here rather than being outside the measurement.
    """
    out = {}
    for rel in CA.expand(root, carriers):
        p = os.path.join(root, rel)
        out[rel] = _md5(p) if os.path.isfile(p) else None
    return out


# ------------------------------------------------------------------------------------- the specs
def _spec_common(evidence_rel):
    return {
        '_doc': ('SELF-TEST FIXTURE — tools/landing/selftest.py writes this file into a sandbox. It '
                 'is not an act spec for any real act, it lands nothing, and the owner_word slot '
                 'says so rather than quoting a word that was never given.'),
        'schema_version': 1,
        'act_kind': 'lever-landing',
        'date': '2026-08-20',
        'owner_word': 'SELF-TEST FIXTURE — no owner word; this spec never lands anything.',
        'authority': 'tools/landing/selftest.py (PLAN_v6 2a.3)',
        'evidence_dir': evidence_rel,
        'claims_file': 'SELFTEST_CLAIMS.json',
        'day0_rebase': {'state': 'off'},
        # A CHEAP gate set: the gate list is a declared spec slot, and a sandbox that ran the heavy
        # determinism leg on every one of eleven cases would be a self-test nobody runs. The FULL
        # default set runs in the clean end-to-end landing, where a landing actually pays for it.
        'gates': [{'name': 'release_manifest_check', 'argv': ['python3', 'release_manifest_check.py'],
                   'must_contain': 'PASS'},
                  {'name': 'release_contract_check', 'argv': ['python3', 'release_contract.py', 'check'],
                   'must_contain': 'PASS'}],
    }


def spec_noop(board_md5, evidence_rel):
    """The declared no-op rehearsal: predicts the board it already has, moves no identity."""
    d = _spec_common(evidence_rel)
    d.update({
        'act': 'SELF-TEST — the no-op rehearsal',
        'prereg': {'path': 'tools/landing/selftest.py (fixture)', 'board_before': board_md5,
                   'board_after': board_md5, 'reference_board': None, 'kill_switch': None},
        'identities': {'moves': [], 'unmoved': ['board', 'store', 'engine_head', 'rl_model', 'fv',
                                                'config', 'register']},
        'column': None,
        'lineage': None,
        'commit_message': 'SELF-TEST sandbox commit (never on main)',
    })
    return d


def spec_moved(board_before, board_after, evidence_rel, after_round):
    """A synthetic board move, so pins / column / lineage run their REAL writers on a real move.

    `after_round` is MEASURED from the sandbox's own expected_boot, never typed: this fixture
    carried a literal `23` until the R24 advance made round 24 the newest history point and the
    lineage validator (correctly) refused a column older than it — the P4 this-month's-number
    class, caught by the first post-advance self-test run (2026-08-23)."""
    d = _spec_common(evidence_rel)
    d.update({
        'act': 'SELF-TEST — the synthetic board move',
        'prereg': {'path': 'tools/landing/selftest.py (fixture)', 'board_before': board_before,
                   'board_after': board_after, 'reference_board': None, 'kill_switch': None},
        'identities': {'moves': ['board'],
                       'unmoved': ['store', 'engine_head', 'rl_model', 'fv', 'config', 'register']},
        'column': {'id': 'selftest-synthetic-move', 'after_round': after_round,
                   'label': 'SELF-TEST SYNTHETIC MOVE — sandbox only, never registered on main'},
        'lineage': {'doc': ('SELF-TEST FIXTURE ENTRY. Written in a sandbox by '
                            'tools/landing/selftest.py to exercise the append-only register and its '
                            'restoration by the abort path. It never reaches the live tree.'),
                    'owner_ruling_id': ['SELFTEST_FIXTURE'],
                    'owner_ruling': 'SELF-TEST FIXTURE — no owner ruling exists or is claimed.',
                    'authority': 'tools/landing/selftest.py (PLAN_v6 2a.3)',
                    'invariants': {'sandbox_only': 'this entry exists only inside a scratch worktree'}},
        'commit_message': 'SELF-TEST sandbox commit (never on main)',
    })
    return d


def measured_store_edit(sandbox_path):
    """The store edit this self-test performs, MEASURED off the sandbox's own store. Never typed.

    P4 IN ITS PLAINEST FORM ("assert the relationship, never this month's number"). A fixture carrying
    a literal row key and a literal old value would be a red waiting for the next legitimate store
    write — which is exactly how `spec_moved`'s hard-coded round 23 red the first post-R24 self-test
    run. So the row is CHOSEN by a rule and its `old` value is READ:

        the first row (in file order) carrying an integer `p_dual_stream` — the dual-stream fraction,
        which is the field the Graham act edits and therefore the field this self-test should rehearse
        — falling back to the first row carrying an integer `games` if a tree has no such row.

    `new` is `old - 1`: a different value, in range, and reversible by inspection.
    """
    from tools.landing import steps as _ST
    p = os.path.join(sandbox_path, _ST.STORE_REL)
    rows = json.load(open(p, encoding='utf-8'))
    for field in ('p_dual_stream', 'games'):
        for r in rows:
            if isinstance(r, dict) and r.get('key') and isinstance(r.get(field), int) \
                    and not isinstance(r.get(field), bool):
                return {'key': r['key'], 'field': field, 'old': r[field], 'new': r[field] - 1}
    raise RuntimeError('no store row carries an integer p_dual_stream or games to rehearse an edit on')


def spec_edit(board_before, board_after, evidence_rel, after_round, edit):
    """THE STORE-EDIT FIXTURE — the spec every edit case is flown or injected into.

    IT DECLARES `expected_movers: []`, WHICH IS A REAL PREDICTION AND NOT A SHRUG. The self-test
    builder produces the tree's own board plus one newline: the board md5 MOVES (so pins, the column
    and the lineage entry all run their real writers on a real move) and no board ROW moves (because
    this builder runs no engine). "No row moves" is therefore the true prediction here, and declaring
    it is what makes `edit_fault_second_mover` — which swaps in a builder that moves two rows — a
    falsifier rather than a coincidence.
    """
    d = _spec_common(evidence_rel)
    d.update({
        'act_kind': 'store-edit',
        'act': 'SELF-TEST — the surgical store edit',
        'prereg': {'path': 'tools/landing/selftest.py (fixture)', 'board_before': board_before,
                   'board_after': board_after, 'reference_board': None, 'kill_switch': None},
        'edit': {'store': [edit], 'expected_movers': []},
        'identities': {'moves': ['board', 'store'],
                       'unmoved': ['engine_head', 'rl_model', 'fv', 'config', 'register']},
        'column': {'id': 'selftest-store-edit', 'after_round': after_round,
                   'label': 'SELF-TEST STORE EDIT — sandbox only, never registered on main'},
        'lineage': {'doc': ('SELF-TEST FIXTURE ENTRY for the EDIT VERB. Written in a sandbox by '
                            'tools/landing/selftest.py to exercise the store_edit step, the '
                            'append-only register and the STRADDLE (source pre-edit, destination '
                            'post-edit). It never reaches the live tree.'),
                    'kind': 'owner-store-edit',
                    'owner_ruling_id': ['SELFTEST_FIXTURE'],
                    'owner_ruling': 'SELF-TEST FIXTURE — no owner ruling exists or is claimed.',
                    'authority': 'tools/landing/selftest.py (THE EDIT VERB, directive 2026-08-24)',
                    'invariants': {'sandbox_only': 'this entry exists only inside a scratch worktree'}},
        'commit_message': 'SELF-TEST sandbox commit (never on main)',
    })
    return d


def spec_round_noop(sandbox_path, board_md5, evidence_rel):
    """THE ROUND REHEARSAL — the fixture every round fault case is injected into.

    It declares the board it already has and the round the tree is already standing on, so the whole
    fourteen-step sequence runs with nothing armed, nothing applied and nothing owed: `sheet` asserts
    the declaration describes the sheet, `scores` and `catchup_preflight` have no owner file to
    assert, `advance` proves the tree held still, `generator_sync` finds the copies already equal,
    `day0` is OFF by default, and the shared seven run exactly as they do under `land lever`.

    That shape is deliberate and it is the same shape as the live-tree DRY RUN the package ships as
    its no-op proof: a rehearsal is the only honest way to exercise a round lander before a round
    exists to land.
    """
    boot = json.load(open(os.path.join(sandbox_path, 'data', 'expected_boot.json'), encoding='utf-8'))
    d = _spec_common(evidence_rel)
    d.update({
        'act_kind': 'round-advance',
        'act': 'SELF-TEST — the round rehearsal',
        'prereg': {'path': 'tools/landing/selftest.py (fixture)', 'board_before': board_md5,
                   'board_after': board_md5, 'round_expected': None},
        'round': {'number': int(boot['as_of_round']), 'scores': None, 'identity_overrides': [],
                  'arming': None},
        'sheet': None,
        'identities': {'moves': [], 'unmoved': ['board', 'store', 'engine_head', 'rl_model', 'fv',
                                                'config', 'register', 'as_of_round']},
        'column': None,
        'lineage': None,
        'movers_page': {'output': '', 'boundary_note': ''},
        'commit_message': 'SELF-TEST sandbox commit (never on main)',
    })
    return d


# ------------------------------------------------------------------------------------ the sandbox
class Sandbox(object):
    """A git worktree of HEAD, carrying the CURRENT lander, committed so the tree reads clean."""

    def __init__(self, root, work_dir, base='HEAD'):
        self.live_root = os.path.abspath(root)
        self.work_dir = work_dir
        self.path = os.path.join(work_dir, 'sandbox')
        #: THE CHECKOUT BASE — the commit the sandbox is cut from. See `main`'s docstring for the
        #: ruling. 'HEAD' for any act that leaves the tree coherent; the last coherent base for an
        #: act that has already committed an engine flip its board has not caught up with.
        self.base = base or 'HEAD'
        self.base_commit = None
        self.lock_file = os.path.join(work_dir, 'selftest.lock')

    def create(self):
        os.makedirs(self.work_dir, exist_ok=True)
        rc, out = _sh(['git', 'worktree', 'add', '--detach', self.path, self.base], cwd=self.live_root)
        if rc != 0:
            raise RuntimeError('cannot create the sandbox worktree:\n%s' % out)
        # The lander under test is the WORKING COPY, not whatever happens to be committed.
        for rel in ('tools/landing', 'tools/land'):
            src = os.path.join(self.live_root, rel)
            dst = os.path.join(self.path, rel)
            if os.path.isdir(src):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__'))
            elif os.path.isfile(src):
                shutil.copyfile(src, dst)
                os.chmod(dst, 0o755)
        _sh(['git', 'add', '-A', 'tools'], cwd=self.path)
        _sh(['git', '-c', 'user.email=selftest@local', '-c', 'user.name=selftest',
             'commit', '-q', '-m', 'self-test sandbox: the lander under test'], cwd=self.path)
        rc, out = _sh(['git', 'rev-parse', 'HEAD'], cwd=self.path)
        self.base_commit = out.strip()
        rc, out = _sh(['git', 'status', '--porcelain'], cwd=self.path)
        if out.strip():
            raise RuntimeError('the sandbox is not clean after creation:\n%s' % out)
        return self

    def reset(self):
        _sh(['git', 'reset', '--hard', '-q', self.base_commit], cwd=self.path)
        _sh(['git', 'clean', '-qfd'], cwd=self.path)

    def destroy(self):
        _sh(['git', 'worktree', 'remove', '--force', self.path], cwd=self.live_root)
        _sh(['git', 'worktree', 'prune'], cwd=self.live_root)

    def env(self):
        env = dict(os.environ)
        env['RL_REPO'] = self.path
        # NEVER CONTEND WITH THE BOX'S REAL LOCK — and never with an `RL_`-PREFIXED FLAG. This line
        # read `RL_BUILD_LOCK_FILE` until 2026-08-21, and the R24 dress rehearsal (§3.3, RUN D)
        # measured what that costs: any seat that copies this isolation recipe and then ARMS gets
        # `staged_apply.ConfigPolicyError: UNKNOWN inherited valuation flag RL_BUILD_LOCK_FILE` at
        # the advance — a message about valuation flags for what is a lock path. The self-test never
        # arms, so it never fired here; it fired on the first seat that followed it. A TOOL'S OWN
        # FLAGS ARE NEVER `RL_*` (carriers.py's header, and this was the FOURTH burn of that class).
        env['BUILD_LOCK_FILE'] = self.lock_file
        for legacy in ('RL_BUILD_LOCK', 'RL_BUILD_LOCK_FILE', 'RL_BUILD_LOCK_HELD'):
            env.pop(legacy, None)
        env['GIT_AUTHOR_NAME'] = env['GIT_COMMITTER_NAME'] = 'selftest'
        env['GIT_AUTHOR_EMAIL'] = env['GIT_COMMITTER_EMAIL'] = 'selftest@local'
        return env

    def head(self):
        rc, out = _sh(['git', 'rev-parse', 'HEAD'], cwd=self.path)
        return out.strip() if rc == 0 else None

    def run_lander(self, spec_rel, fault=None, builder='selftest', report=None, log=None,
                   extra=(), verb='lever'):
        argv = [sys.executable, os.path.join(self.path, 'tools', 'landing', 'cli.py'), verb,
                '--spec', os.path.join(self.path, spec_rel), '--root', self.path,
                '--selftest', '--builder', builder]
        if fault:
            argv += ['--fault', fault]
        if report:
            argv += ['--report', report]
        if log:
            argv += ['--log', log]
        argv += list(extra)
        return _sh(argv, cwd=self.path, env=self.env(), timeout=5400)


# -------------------------------------------------------------------------------------- the cases
def main(root=None, keep=False, only=None, evidence_dir=None, base=None):
    """Run the self-test. `base` is the commit the sandbox is cut from (default HEAD).

    THE CHECKOUT BASE — SUPERVISOR RULING, 2026-08-21, closing the precondition paradox:

        "The lander self-test proves THE LANDER, not the act. It therefore runs on a COHERENT tree:
         the pre-transaction standalone run executes in a sandbox worktree checked out at the LAST
         COHERENT BASE — for a dial-flip act, the commit immediately before the flip (where pins ==
         source); for any non-flip act, HEAD. Fresh proof each landing, no recursion, and the mid-act
         incoherence window (flip committed, board pending) can no longer deadlock its own landing.
         The in-transaction gate profile continues to exclude the self-test, and the self-test remains
         a registered runner check on every coherent tree."

    THE PARADOX IT CLOSES, MEASURED. Process law P9 puts the engine edit in its own commit ahead of
    the landing, so between the flip and the landing the tree is INCOHERENT BY DESIGN: source builds
    a board the pins do not yet name. The self-test's control case lands a NO-OP, which moves no pin,
    so its sibling reconcile rebuilt board `b3e8da99` against a pin still reading `68be10c7` and
    `sibling_repin`'s conformance gate refused — correctly. On 2026-08-21 that made the standalone
    run 11 PASS / 5 FAIL (every abort still byte-exact), and since the run is a precondition of the
    landing, the landing could never start: it needed the coherence only it could restore.

    THE LANDER UNDER TEST IS STILL THE WORKING COPY. `Sandbox.create` overlays `tools/landing` and
    `tools/land` from the live tree on top of whatever base is checked out, so moving the base back
    changes the TREE the lander is exercised against, never the lander. That is exactly the ruling's
    distinction: the self-test proves the lander, not the act.
    """
    root = os.path.abspath(root or _REPO)
    work = os.path.join(os.environ.get('LANDING_SNAPSHOT_DIR') or '/tmp',
                        'landing_selftest_%d' % os.getpid())
    ev = evidence_dir or os.path.join(work, 'transcripts')
    os.makedirs(ev, exist_ok=True)
    only = set((only or '').split(',')) - {''} or None

    print(BANNER)
    print('THE LANDER SELF-TEST — every step broken once, every abort proved (PLAN_v6 2a.3)')
    print('  live tree : %s   (READ-ONLY to this self-test; asserted byte-unmoved at the end)' % root)
    print('  sandbox   : %s' % work)
    print('  transcripts: %s' % ev)
    print('  base      : %s%s' % (base or 'HEAD',
                                  '' if not base or base == 'HEAD' else
                                  '   (the LAST COHERENT BASE — this tree is mid-act; see the ruling '
                                  'in selftest.main)'))
    print(BANNER)

    # THE WRECKAGE OF THE LAST RUN, CLEARED BEFORE THIS ONE. The teardown at the bottom of this
    # function is not in a `finally` and could not save us if it were: a SIGKILLed or SIGTERMed run
    # (a timeout, a `kill`, a closed terminal) runs no Python at all on the way out. This self-test
    # spawns a sandbox plus one work dir per practice landing, so it is the estate's largest producer
    # of orphans — 138 dirs / 1.4GB of them on 2026-08-21. Sweeping here, by liveness of the owning
    # pid, is the only sweep that sees a dead run's leavings.
    from tools.landing import txn as TX
    TX.sweep_orphan_sandboxes(print)

    live_before = carrier_md5s(root)
    sb = Sandbox(root, work, base=base).create()
    print('sandbox created at %s (base %s)' % (sb.path, sb.base_commit[:12]))

    board = _md5(os.path.join(sb.path, 'data', 'rl_build', 'rl_app_data.json'))
    ev_rel = 'docs/evidence/landing_selftest'
    os.makedirs(os.path.join(sb.path, ev_rel), exist_ok=True)
    noop = spec_noop(board, ev_rel)
    with open(os.path.join(sb.path, 'data', 'expected_boot.json'), encoding='utf-8') as fh:
        _cur_round = int(json.load(fh)['as_of_round'])
    moved = spec_moved(board, hashlib_moved(sb.path), ev_rel, _cur_round)
    rnd = spec_round_noop(sb.path, board, ev_rel)
    the_edit = measured_store_edit(sb.path)
    edit = spec_edit(board, hashlib_moved(sb.path), ev_rel, _cur_round, the_edit)
    with open(os.path.join(sb.path, 'SELFTEST_SPEC_NOOP.json'), 'w', encoding='utf-8') as fh:
        json.dump(noop, fh, indent=2)
    with open(os.path.join(sb.path, 'SELFTEST_SPEC_MOVED.json'), 'w', encoding='utf-8') as fh:
        json.dump(moved, fh, indent=2)
    with open(os.path.join(sb.path, 'SELFTEST_SPEC_ROUND.json'), 'w', encoding='utf-8') as fh:
        json.dump(rnd, fh, indent=2)
    with open(os.path.join(sb.path, 'SELFTEST_SPEC_EDIT.json'), 'w', encoding='utf-8') as fh:
        json.dump(edit, fh, indent=2)
    _sh(['git', 'add', '-A'], cwd=sb.path)
    _sh(['git', '-c', 'user.email=selftest@local', '-c', 'user.name=selftest', 'commit', '-q',
         '-m', 'self-test fixtures'], cwd=sb.path)
    rc, out = _sh(['git', 'rev-parse', 'HEAD'], cwd=sb.path)
    sb.base_commit = out.strip()

    results = []

    def record(name, ok, detail):
        results.append((name, ok, detail))
        print('  %-4s %-28s %s' % ('PASS' if ok else 'FAIL', name, detail))

    # ---- 0. THE NON-VACUITY CONTROL ------------------------------------------------------------
    print('')
    print('--- CONTROL: a clean no-op landing in this sandbox must SUCCEED ---')
    rc, out = sb.run_lander('SELFTEST_SPEC_NOOP.json', report=os.path.join(ev, 'control_report.json'),
                            log=os.path.join(ev, 'control.log'))
    open(os.path.join(ev, 'control_stdout.txt'), 'w', encoding='utf-8').write(out)
    ctrl = _read_json(os.path.join(ev, 'control_report.json'))
    record('control_clean_run', rc == 0 and (ctrl or {}).get('ok') is True,
           'exit %s%s' % (rc, '' if rc == 0 else ' — see control.log; every fault case below is '
                                                 'meaningless until this passes'))
    if rc == 0:
        rcg, gout = _sh(['git', 'show', '--stat', '--name-only', '--format=', 'HEAD'], cwd=sb.path)
        paths = [ln.strip() for ln in gout.splitlines() if ln.strip()]
        foreign = [p for p in paths if not (CA.in_scope(p) or p.startswith(ev_rel))]
        record('commit_explicit_paths', not foreign,
               '%d path(s) committed, all declared: %s' % (len(paths), ', '.join(paths[:4]) or '(none)')
               if not foreign else 'foreign paths committed: %s' % foreign)
    sb.reset()

    # ---- 1. THE BUILD LOCK ----------------------------------------------------------------------
    print('')
    print('--- LOCK: a landing must refuse to start while another holder has the lock ---')
    import fcntl
    fd = os.open(sb.lock_file, os.O_RDWR | os.O_CREAT, 0o644)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    os.write(fd, b'other-seat\t1\t2026-08-20T00:00:00Z\thost\t/elsewhere\n')
    rc, out = sb.run_lander('SELFTEST_SPEC_NOOP.json', log=os.path.join(ev, 'lock.log'))
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
    open(os.path.join(ev, 'lock_stdout.txt'), 'w', encoding='utf-8').write(out)
    record('build_lock_refuses', rc != 0 and 'waiting for lock held by' in out,
           'exit %s; the landing refused to become a second writer' % rc)
    sb.reset()

    # ---- 2. EVERY STEP, BROKEN ONCE -------------------------------------------------------------
    print('')
    print('--- FAULTS: every step in LEVER_SEQUENCE broken once ---')
    # steps at or before `lineage` are exercised on a REAL synthetic board move; the rest run the
    # no-op spec, whose sibling step is a no-build no-op (`verify` is already current).
    moved_steps = {'pins', 'lineage'}
    tally = {'broken': 0, 'caught': 0, 'aborted_byte_exact': 0}
    for step_name, _title, _fn in ST.LEVER_SEQUENCE:
        if only and step_name not in only:
            continue
        mode, what, _inj = TX.FAULTS[step_name]
        spec_rel = 'SELFTEST_SPEC_MOVED.json' if step_name in moved_steps else 'SELFTEST_SPEC_NOOP.json'
        builder = 'selftest-moved' if step_name in moved_steps else 'selftest'
        before = carrier_md5s(sb.path)
        rep = os.path.join(ev, 'fault_%s_report.json' % step_name)
        rc, out = sb.run_lander(spec_rel, fault=step_name, builder=builder, report=rep,
                                log=os.path.join(ev, 'fault_%s.log' % step_name))
        open(os.path.join(ev, 'fault_%s_stdout.txt' % step_name), 'w', encoding='utf-8').write(out)
        report = _read_json(rep) or {}
        tally['broken'] += 1

        caught = (rc != 0) and report.get('failed_step') == step_name
        after = carrier_md5s(sb.path)
        moved_carriers = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        byte_exact = not moved_carriers
        if caught:
            tally['caught'] += 1
        if byte_exact:
            tally['aborted_byte_exact'] += 1
        detail = 'fault=%s; exit %s; failed_step=%r; carriers moved after abort: %s' % (
            mode, rc, report.get('failed_step'), moved_carriers or 'NONE (byte-exact)')
        record('fault_%s' % step_name, caught and byte_exact, detail)

        # residue OUTSIDE the carrier set is the fault's own, not the landing's; the parent removes
        # it, and says so, rather than letting the next case start from a dirtied sandbox.
        for residue in ('LANDING_FAULT_DIRT.txt', 'docs/LANDING_FAULT_FOREIGN.md'):
            rp = os.path.join(sb.path, residue)
            if os.path.exists(rp):
                os.remove(rp)
        sb.reset()

    # ---- 2b. THE `ui` STEP'S FIFTH WRITER — the one predicate the loop above cannot reach --------
    #
    # The loop breaks every step ONCE, which is the plan's sentence, and for a step running ONE
    # writer that is the whole story. The `ui` step runs FIVE, and its default fault
    # (`skip_second_writer`, the thrice-proven trap) aborts the step before writers 3, 4 and 5 have
    # said anything. So the ownership mirror's predicate — `ui/app/ownership.js:pin()`, asserted
    # in-step — would have been carried by a case that never reached it.
    #
    # THE FAULT IS THE TREE'S OWN HISTORY. The R23 advance moved the store; nothing regenerated
    # ui/data/ownership.js; its pin therefore named the store BEFORE the advance; and pin() refuses a
    # mirror it cannot authenticate, so the live ownership lane shipped SWITCHED OFF with nothing
    # rendering an error. `ui/tests/ownership_sidecar.test.js` stood at 22/35 for six days. This case
    # puts the sandbox back into exactly that state — writer 5 silenced AND the pin falsified, because
    # an unconditional writer would repair a merely-falsified file and prove nothing — and asserts the
    # landing dies at `ui` and puts every carrier back byte-exact.
    if not only or 'ui' in only:
        print('')
        print('--- FAULT: the ui step\'s WRITER 5 — the ownership mirror\'s pin ---')
        mode, _what, _inj = TX.FAULTS['ui:stale_mirror']
        before = carrier_md5s(sb.path)
        rep = os.path.join(ev, 'fault_ui_stale_mirror_report.json')
        rc, out = sb.run_lander('SELFTEST_SPEC_NOOP.json', fault='ui:stale_mirror', report=rep,
                                log=os.path.join(ev, 'fault_ui_stale_mirror.log'))
        open(os.path.join(ev, 'fault_ui_stale_mirror_stdout.txt'), 'w', encoding='utf-8').write(out)
        report = _read_json(rep) or {}
        tally['broken'] += 1
        caught = (rc != 0) and report.get('failed_step') == 'ui'
        after = carrier_md5s(sb.path)
        moved_carriers = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        byte_exact = not moved_carriers
        if caught:
            tally['caught'] += 1
        if byte_exact:
            tally['aborted_byte_exact'] += 1
        record('fault_ui_stale_mirror', caught and byte_exact,
               'fault=%s; exit %s; failed_step=%r; carriers moved after abort: %s'
               % (mode, rc, report.get('failed_step'), moved_carriers or 'NONE (byte-exact)'))
        sb.reset()

    # ---- 2c. THE `ui` STEP'S SIXTH WRITER — the pick surface (v827) ------------------------------
    #
    # THE SAME ARGUMENT AS 2b, ONE CARRIER ALONG, AND A WORSE DEFECT. `ui/data/club_valuation.js`
    # carries the owner's PICK LOCATIONS and each held pick's price off the engine's canonical curve.
    # On 2026-08-21 it was found stamped to board a05fe951 / store cc02567f (R22) while the tree stood
    # on b3e8da99 / b745002e (R23) — and where the ownership mirror at least REFUSES a pin it cannot
    # authenticate, this bundle had no reader-side guard at all, so the pocket and club pages showed
    # R22-board pick VALUES in silence. Owner, the same night: "It is essential that the UI displays
    # the correct player locations and pick locations."
    #
    # The loop above cannot reach this predicate for the same reason it cannot reach writer 5's: the
    # `ui` step's default fault aborts at writer 2. So this case puts the sandbox into exactly the
    # measured state — writer 6 silenced AND the stamp falsified, because an unconditional writer
    # would repair a merely-falsified file and prove nothing — and asserts the landing dies at `ui`
    # and puts every carrier back byte-exact.
    if not only or 'ui' in only:
        print('')
        print('--- FAULT: the ui step\'s WRITER 6 — the picks bundle\'s stamp ---')
        mode, _what, _inj = TX.FAULTS['ui:stale_picks']
        before = carrier_md5s(sb.path)
        rep = os.path.join(ev, 'fault_ui_stale_picks_report.json')
        rc, out = sb.run_lander('SELFTEST_SPEC_NOOP.json', fault='ui:stale_picks', report=rep,
                                log=os.path.join(ev, 'fault_ui_stale_picks.log'))
        open(os.path.join(ev, 'fault_ui_stale_picks_stdout.txt'), 'w', encoding='utf-8').write(out)
        report = _read_json(rep) or {}
        tally['broken'] += 1
        caught = (rc != 0) and report.get('failed_step') == 'ui'
        after = carrier_md5s(sb.path)
        moved_carriers = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        byte_exact = not moved_carriers
        if caught:
            tally['caught'] += 1
        if byte_exact:
            tally['aborted_byte_exact'] += 1
        record('fault_ui_stale_picks', caught and byte_exact,
               'fault=%s; exit %s; failed_step=%r; carriers moved after abort: %s'
               % (mode, rc, report.get('failed_step'), moved_carriers or 'NONE (byte-exact)'))
        sb.reset()

        # THE CLEAN CONTROL FOR THIS WRITER, and it is not a courtesy: `ui/data/club_valuation.js`
        # became a CARRIER in the same act, so the abort proof above would read byte-exact even if
        # writer 6 could not run at all. A run with no fault must therefore still succeed with the new
        # writer live, and the bundle must come out of it byte-UNMOVED — which is the whole claim that
        # dropping its wall clock bought. A file with a timestamp in it could not make this assertion.
        cv_rel = 'ui/data/club_valuation.js'
        cv_before = carrier_md5s(sb.path).get(cv_rel)
        rep = os.path.join(ev, 'writer6_control_report.json')
        rc, out = sb.run_lander('SELFTEST_SPEC_NOOP.json', report=rep,
                                log=os.path.join(ev, 'writer6_control.log'))
        open(os.path.join(ev, 'writer6_control_stdout.txt'), 'w', encoding='utf-8').write(out)
        rep6 = _read_json(rep) or {}
        ui_facts = (rep6.get('facts') or {}).get('ui') or {}
        cv_after = carrier_md5s(sb.path).get(cv_rel)
        record('writer6_clean_control',
               rc == 0 and rep6.get('ok') is True and ui_facts.get('writers') == 6
               and ui_facts.get('club_valuation_moved') is False and cv_after == cv_before,
               'exit %s; the ui step ran %s writer(s); the picks bundle regenerated BYTE-IDENTICAL '
               '(%s), %s pick(s) stamped to board %s'
               % (rc, ui_facts.get('writers'), str(cv_after)[:12], ui_facts.get('n_picks'),
                  ui_facts.get('club_valuation_pin')))
        sb.reset()

    # ---- 3. THE ABORT WROTE, THEN UNWROTE — proved on the writers that only fire on a move -------
    print('')
    print('--- DEPTH: a landing that WROTE pins + column + lineage + contract, then aborted ---')
    before = carrier_md5s(sb.path)
    rep = os.path.join(ev, 'depth_report.json')
    rc, out = sb.run_lander('SELFTEST_SPEC_MOVED.json', fault='sibling', builder='selftest-moved',
                            report=rep, log=os.path.join(ev, 'depth.log'))
    open(os.path.join(ev, 'depth_stdout.txt'), 'w', encoding='utf-8').write(out)
    report = _read_json(rep) or {}
    after = carrier_md5s(sb.path)
    movedc = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    wrote = [r['path'] for r in (report.get('abort') or {}).get('restored') or []]
    record('abort_restores_writers',
           rc != 0 and report.get('failed_step') == 'sibling' and not movedc and len(wrote) >= 4,
           '%d carrier(s) had been written and were restored: %s' % (len(wrote), ', '.join(wrote[:6])))
    sb.reset()

    # ---- 3b. THE ROUND LANDER (PLAN_v6 2b) — the same standard the lever steps met ---------------
    #
    # THE NON-VACUITY CONTROL FIRST, AGAIN. A clean round REHEARSAL in this sandbox must SUCCEED
    # before any round fault case is believed. Then every step 2b ADDS is broken exactly once, by a
    # fault that breaks the thing that step exists to check, and the parent — never the child —
    # re-hashes every carrier before and after and compares them itself.
    #
    # AND ONE ASSERTION THE LEVER CASES NEVER NEEDED: HEAD IS BACK AT THE BASE COMMIT. The round
    # lander commits mid-flight (PACKAGE 3a's form puts the sheet in its own commit before the
    # advance), so "byte-exact" has to include history or it quietly excludes it. Every round case
    # asserts the sandbox's HEAD is exactly where it started.
    print('')
    print('--- ROUND: a clean round rehearsal in this sandbox must SUCCEED (PLAN_v6 2b) ---')
    round_base = sb.head()
    rc, out = sb.run_lander('SELFTEST_SPEC_ROUND.json', verb='round',
                            report=os.path.join(ev, 'round_control_report.json'),
                            log=os.path.join(ev, 'round_control.log'))
    open(os.path.join(ev, 'round_control_stdout.txt'), 'w', encoding='utf-8').write(out)
    rctrl = _read_json(os.path.join(ev, 'round_control_report.json'))
    record('round_control_clean_run', rc == 0 and (rctrl or {}).get('ok') is True,
           'exit %s%s' % (rc, '' if rc == 0 else ' — see round_control.log; every round fault case '
                                                 'below is meaningless until this passes'))
    if rc == 0:
        rcg, gout = _sh(['git', 'show', '--stat', '--name-only', '--format=', 'HEAD'], cwd=sb.path)
        paths = [ln.strip() for ln in gout.splitlines() if ln.strip()]
        foreign = [p for p in paths
                   if not (CA.in_scope(p, CA.ROUND_CARRIERS) or p.startswith(ev_rel))]
        record('round_commit_explicit_paths', not foreign,
               '%d path(s) committed, all declared: %s'
               % (len(paths), ', '.join(paths[:4]) or '(none)')
               if not foreign else 'foreign paths committed: %s' % foreign)
    sb.reset()

    print('')
    print('--- ROUND FAULTS: every step 2b ADDS, broken once ---')
    shared = {n for n, _t, _f in ST.LEVER_SEQUENCE}
    for step_name, _title, _fn in ST.ROUND_SEQUENCE:
        if step_name in shared:
            continue                    # proved above, on the same code, under `land lever`
        if only and step_name not in only:
            continue
        mode, what, _inj = TX.FAULTS[step_name]
        before = carrier_md5s(sb.path)
        rep = os.path.join(ev, 'round_fault_%s_report.json' % step_name)
        rc, out = sb.run_lander('SELFTEST_SPEC_ROUND.json', fault=step_name, verb='round',
                                report=rep, log=os.path.join(ev, 'round_fault_%s.log' % step_name))
        open(os.path.join(ev, 'round_fault_%s_stdout.txt' % step_name), 'w',
             encoding='utf-8').write(out)
        report = _read_json(rep) or {}
        tally['broken'] += 1
        caught = (rc != 0) and report.get('failed_step') == step_name
        after = carrier_md5s(sb.path)
        moved_carriers = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        head_ok = sb.head() == round_base
        byte_exact = not moved_carriers and head_ok
        if caught:
            tally['caught'] += 1
        if byte_exact:
            tally['aborted_byte_exact'] += 1
        record('round_fault_%s' % step_name, caught and byte_exact,
               'fault=%s; exit %s; failed_step=%r; carriers moved after abort: %s; HEAD %s'
               % (mode, rc, report.get('failed_step'), moved_carriers or 'NONE (byte-exact)',
                  'back at the base' if head_ok else 'MOVED — the abort left a commit behind'))
        sb.reset()

    # ---- 3c. THE SHEET RE-CUT WRITER — the one path a rehearsal cannot reach -------------------
    #
    # Every case above runs with `sheet: null`, which is most weeks and is the path where the step
    # writes NOTHING. But `land round` is the SOLE WRITER of `data/sheet_pins.json`, and a sole
    # writer nobody has watched write is a claim, not a fact. So the sandbox performs a synthetic
    # re-cut — one byte appended to the sheet's first data row, which moves its md5 and leaves rows
    # and injured=Y where they are — and the step is run twice against it:
    #
    #   NEGATIVE first: a prereg-lite that predicts the WRONG md5 must HALT. "A re-cut whose
    #                   measured facts are not the disclosed ones is a halt and a report, not a note."
    #   POSITIVE then : the correct prediction writes the pin, commits sheet + declaration +
    #                   prereg-lite as ONE explicit-path commit, and asserts engine_head UNMOVED.
    #
    # The negative runs FIRST on purpose: a positive that passes because the assertion is dead looks
    # exactly like a positive that passes because the writer works.
    if not only or 'sheet' in only:
        print('')
        print('--- ROUND: the sheet re-cut writer — `land round` is the pin file\'s SOLE WRITER ---')
        prereg_rel = os.path.join(ev_rel, 'SELFTEST_PREREG_LITE.md')

        def _stage_recut():
            """Put the sandbox back into the shape a seat hands the lander: sheet re-cut, prereg
            written, and NOTHING ELSE uncommitted. The residue of the previous attempt — including
            an abort's own ABORT_*.json — is dirt, and step 0 is right to refuse it."""
            sb.reset()
            shutil.rmtree(os.path.join(sb.path, ev_rel), ignore_errors=True)
            os.makedirs(os.path.join(sb.path, ev_rel), exist_ok=True)
            with open(os.path.join(sb.path, prereg_rel), 'w', encoding='utf-8') as fh:
                fh.write('SELF-TEST PREREG-LITE — a synthetic re-cut inside a sandbox worktree. It '
                         'never reaches the live tree and no owner word exists or is claimed.\n')
            return _synthetic_recut(sb.path)

        recut_md5 = _stage_recut()
        for label, predicted_md5, want_ok in (('sheet_recut_wrong_prediction', '0' * 32, False),
                                              ('sheet_recut_writer', recut_md5, True)):
            if label != 'sheet_recut_wrong_prediction':
                assert _stage_recut() == recut_md5, 'the synthetic re-cut is not reproducible'
            spec = spec_round_noop(sb.path, board, ev_rel)
            spec['act'] = 'SELF-TEST — the synthetic sheet re-cut'
            spec['sheet'] = {
                'prereg_lite': prereg_rel,
                'owner_word': 'SELF-TEST FIXTURE — no owner word exists or is claimed.',
                'disclosed_movers': 'nobody: this re-cut appends one byte to a notes cell.',
                'predicted': {'sheet_md5': predicted_md5, 'sheet_rows': 219, 'sheet_injured_y': 35},
                'provenance': 'SELF-TEST FIXTURE — sandbox only.'}
            # THE SPEC LIVES OUTSIDE THE SANDBOX. It is written for this case rather than committed
            # with the other fixtures, and an uncommitted file inside the tree is DIRT — which is
            # exactly what step 0 refuses, and rightly: the only dirt this act may start on is its
            # own DECLARED dirt (the re-cut sheet and its prereg-lite). Keeping the spec out of the
            # tree keeps the assertion honest instead of widening it.
            spec_abs = os.path.join(ev, 'SELFTEST_SPEC_RECUT.json')
            with open(spec_abs, 'w', encoding='utf-8') as fh:
                json.dump(spec, fh, indent=2)
            rep = os.path.join(ev, '%s_report.json' % label)
            rc, out = sb.run_lander(spec_abs, verb='round', report=rep,
                                    log=os.path.join(ev, '%s.log' % label))
            open(os.path.join(ev, '%s_stdout.txt' % label), 'w', encoding='utf-8').write(out)
            report = _read_json(rep) or {}
            pins = _read_json(os.path.join(sb.path, 'data', 'sheet_pins.json')) or {}
            if want_ok:
                ok = (rc == 0 and report.get('ok') is True
                      and pins.get('sheet_md5') == recut_md5
                      and int(pins.get('sheet_rows')) == 219
                      and int(pins.get('sheet_injured_y')) == 35
                      and (report.get('facts') or {}).get('sheet', {}).get('commit'))
                record(label, ok, 'exit %s; the declaration now reads md5=%s rows=%s injured_y=%s; '
                                  'sheet commit %s; engine_head asserted UNMOVED'
                       % (rc, str(pins.get('sheet_md5'))[:12], pins.get('sheet_rows'),
                          pins.get('sheet_injured_y'),
                          str((report.get('facts') or {}).get('sheet', {}).get('commit'))[:12]))
            else:
                head_ok = sb.head() == round_base
                record(label, rc != 0 and report.get('failed_step') == 'sheet' and head_ok
                       and pins.get('sheet_md5') != '0' * 32,
                       'exit %s; failed_step=%r; the declaration was NOT written and HEAD %s'
                       % (rc, report.get('failed_step'),
                          'is back at the base' if head_ok else 'MOVED'))
        sb.reset()

    # ---- 3d. THE INPUT-COMMIT PINCER — the one path a `scores: null` fixture can never reach -----
    #
    # THE REGRESSION CASES ARE THE R24 DRESS REHEARSAL'S RUN A AND RUN C (REHEARSAL_REPORT §3.1),
    # and they were TWO HALTS WITH ONE ROOT CAUSE on the real invocation:
    #
    #   RUN A  score file UNCOMMITTED -> `THE TREE IS NOT CLEAN … ?? scores/R24.csv` at step 0,
    #          because `txn.Ctx.declared_dirt()` enumerated only the sheet and the prereg-lite;
    #   RUN C  score file COMMITTED   -> step 3 reached PREREG MET and then died with
    #          `git commit failed: … nothing added to commit but untracked files present`.
    #
    # "There is no third option. The armed path of `land round` is unreachable as shipped, and the
    # self-test could not see it because its fixture declares no score file."  THIS CASE IS THAT
    # FIXTURE'S MISSING HALF: a flight carrying a REAL score file, UNCOMMITTED, through step 0 and
    # through `catchup_preflight`'s own explicit-path commit — and stopping at the door of the armed
    # advance, because a self-test does not arm a score-write.
    #
    # THE FIXTURE'S PREDICTIONS ARE MEASURED OFF THE TOOL OF RECORD, never typed — the R24 runbook's
    # own step 1 ("measure the seven round_expected falsifiers off the tool, never type them"). What
    # is under test is not the number; it is the LANDER's independent re-measurement of it and its
    # refusal to proceed when the two disagree, which `round_fault_catchup_preflight` already proves
    # from the negative side.
    if not only or 'catchup_preflight' in only:
        print('')
        print('--- ROUND: THE INPUT-COMMIT PINCER — an uncommitted owner score file, carried ---')
        sb.reset()
        pincer_base = sb.head()
        sc = _synthetic_scores(sb.path)
        rc, pre_out = _sh([sys.executable, 'tools/round_entry/round_entry.py', 'catchup',
                           '--file', '%d=%s' % (sc['round'], sc['path'])],
                          cwd=sb.path, env=sb.env())
        open(os.path.join(ev, 'pincer_preflight.txt'), 'w', encoding='utf-8').write(pre_out)
        counts = ST._parse_preflight(pre_out, sc['round'])
        if rc != 0 or 'PREFLIGHT CLEAN' not in pre_out or not counts:
            record('round_input_commit_pincer', False,
                   'the FIXTURE could not be built: the read-only preflight on the synthetic score '
                   'file is not clean (exit %s). See pincer_preflight.txt.' % rc)
        else:
            spec = spec_round_noop(sb.path, board, ev_rel)
            spec['act'] = 'SELF-TEST — the input-commit pincer (R24 rehearsal §3.1 RUN A + RUN C)'
            spec['round'] = {
                'number': sc['round'],
                'scores': {'path': sc['path'], 'md5': sc['md5'], 'sha256': sc['sha256']},
                'identity_overrides': [],
                'arming': {'env': {'INGEST_SCORE_APPLY_ARMED': '1',
                                   'INGEST_SCORE_APPLY': 'selftest-never-armed'},
                           'owner_word': 'SELF-TEST FIXTURE — no owner word exists or is claimed, '
                                         'and this flight stops before the advance.'}}
            spec['prereg']['round_expected'] = {
                'round': sc['round'], 'listed': counts['listed'], 'resolved': counts['resolved'],
                'absent_dnp': counts['absent_dnp'], 'scores_sha256': sc['sha256'],
                'ledger_before': 0, 'ledger_delta': counts['resolved']}
            spec_abs = os.path.join(ev, 'SELFTEST_SPEC_PINCER.json')
            with open(spec_abs, 'w', encoding='utf-8') as fh:
                json.dump(spec, fh, indent=2)
            before = carrier_md5s(sb.path)
            rep = os.path.join(ev, 'pincer_report.json')
            rc, out = sb.run_lander(spec_abs, verb='round', fault='advance:stop_at_the_door',
                                    report=rep, log=os.path.join(ev, 'pincer.log'))
            open(os.path.join(ev, 'pincer_stdout.txt'), 'w', encoding='utf-8').write(out)
            report = _read_json(rep) or {}
            facts = report.get('facts') or {}

            # JAW 1 — step 0 did not refuse the uncommitted owner input, and it ENUMERATED it.
            declared = ('DECLARED DIRT' in out and sc['path'] in out
                        and ST.CATCHUP_OVERRIDES_REL in out)
            past_preflight = bool((facts.get('preflight') or {}).get('base_commit'))
            # JAW 2 — `catchup_preflight` made its own explicit-path input commit and got a sha.
            cp = facts.get('catchup_preflight') or {}
            input_commit = cp.get('commit')
            reached_door = report.get('failed_step') == 'advance'

            after = carrier_md5s(sb.path)
            movedc = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
            head_ok = sb.head() == pincer_base
            record('round_input_commit_pincer',
                   bool(declared and past_preflight and input_commit and reached_door),
                   'step 0 DECLARED the score file + the override record as expected dirt (%s); '
                   'catchup_preflight committed the inputs itself at %s; the flight reached '
                   'failed_step=%r (the door of the armed advance, by request)'
                   % ('yes' if declared else 'NO — jaw 1 is back',
                      str(input_commit)[:12] if input_commit else 'NOTHING — jaw 2 is back',
                      report.get('failed_step')))
            record('round_input_commit_pincer_abort', not movedc and head_ok,
                   'the mid-flight INPUT commit was rewound and every carrier restored: carriers '
                   'moved after abort: %s; HEAD %s'
                   % (movedc or 'NONE (byte-exact)',
                      'back at the base' if head_ok else 'MOVED — the abort left a commit behind'))

            # RUN C'S OTHER SHAPE, AND IT MUST ALSO NOT HALT. Declared dirt makes the ORDINARY path
            # work; a seat who pre-committed the owner's file (the rehearsal's documented interim
            # path, §3.1) then presents `catchup_preflight` with nothing to commit, and
            # `git commit -m … -- <unchanged paths>` exits 1. The step must MEASURE that and carry
            # on, not die — the machine does not punish a seat for having already done the thing the
            # machine wanted done.
            # The previous flight's abort left its own ABORT_<step>.json in the evidence dir, and
            # that residue is dirt at step 0 — a MEASURED operational note of the rehearsal (§8.1),
            # not a defect. The seat moves it aside before re-flying; so does this case.
            shutil.rmtree(os.path.join(sb.path, ev_rel), ignore_errors=True)
            os.makedirs(os.path.join(sb.path, ev_rel), exist_ok=True)
            _sh(['git', 'add', '--', sc['path']], cwd=sb.path)
            _sh(['git', '-c', 'user.email=selftest@local', '-c', 'user.name=selftest', 'commit',
                 '-q', '-m', 'self-test: the owner input, PRE-COMMITTED by the seat',
                 '--', sc['path']], cwd=sb.path)
            precommitted_base = sb.head()
            rep2 = os.path.join(ev, 'pincer_precommitted_report.json')
            rc2, out2 = sb.run_lander(spec_abs, verb='round', fault='advance:stop_at_the_door',
                                      report=rep2,
                                      log=os.path.join(ev, 'pincer_precommitted.log'))
            open(os.path.join(ev, 'pincer_precommitted_stdout.txt'), 'w',
                 encoding='utf-8').write(out2)
            rep2d = _read_json(rep2) or {}
            cp2 = (rep2d.get('facts') or {}).get('catchup_preflight') or {}
            record('round_input_commit_precommitted',
                   rep2d.get('failed_step') == 'advance' and cp2.get('ran') is True
                   and cp2.get('commit') is None and 'NOTHING TO COMMIT' in out2
                   and sb.head() == precommitted_base,
                   'the inputs were already committed: catchup_preflight MEASURED the empty index, '
                   'said so, made no empty commit, and the flight reached failed_step=%r'
                   % rep2d.get('failed_step'))
        # the fixture's own score file is the fault's residue, not the landing's: the abort restores
        # carriers, and an uncommitted synthetic input is neither a carrier nor the next case's dirt.
        try:
            os.remove(os.path.join(sb.path, sc['path']))
        except OSError:
            pass
        sb.reset()

    # ---- 3e. THE CARRIED DAY-0 EMITTER — its refusals, and its mandatory diff --------------------
    #
    # `round_fault_day0` proves the STEP's M1b guard (activated + zero movers = halt). It says
    # nothing about the EMITTER, and until 2026-08-21 there was no emitter to say anything about:
    # R24 rehearsal §5, "there is no runnable day-0 emitter for R24 … it cannot run for R24 as it
    # stands." `tools/landing/day0_emit.py` is the carried replacement and these are its own cases.
    #
    # THE TWO REFUSALS FIRST, AND THEY ARE CHEAP BECAUSE THEY MUST BE: both are decided before the
    # engine is loaded, so an emitter that refuses cannot spend four minutes deciding to.
    if not only or 'day0' in only:
        print('')
        print('--- ROUND: the CARRIED day-0 emitter — %s ---' % ST.DAY0_GENERATOR)
        std_ref = 'docs/evidence/final_candidate_2026-08-19/DAY0_CP.json'
        new_ref = os.path.join(ev_rel, 'DAY0_SELFTEST.json')

        def _emit(spec_doc, label, extra=()):
            p = os.path.join(ev, 'day0_spec_%s.json' % label)
            with open(p, 'w', encoding='utf-8') as fh:
                json.dump(spec_doc, fh, indent=2)
            rc, out = _sh([sys.executable, os.path.join(sb.path, ST.DAY0_GENERATOR),
                           '--spec', p, '--root', sb.path] + list(extra),
                          cwd=sb.path, env=sb.env())
            open(os.path.join(ev, 'day0_emit_%s.txt' % label), 'w', encoding='utf-8').write(out)
            return rc, out

        base_doc = {'act': 'SELF-TEST — the carried day-0 emitter',
                    'day0_rebase': {'state': 'on', 'reference': std_ref, 'new_reference': new_ref,
                                    'activated_by': 'SELF-TEST FIXTURE — no owner word exists or '
                                                    'is claimed.'}}

        off = json.loads(json.dumps(base_doc))
        off['day0_rebase']['state'] = 'off'
        rc, out = _emit(off, 'unactivated')
        record('day0_emitter_refuses_unactivated',
               rc != 0 and 'REFUSING TO WRITE' in out
               and not os.path.exists(os.path.join(sb.path, new_ref)),
               'exit %s; day0_rebase.state=off -> the emitter refused and wrote nothing (M1b: '
               'off-by-default, owner-visible; automation never re-bases itself green)' % rc)

        gone = json.loads(json.dumps(base_doc))
        gone['day0_rebase']['reference'] = 'docs/evidence/NO_SUCH_DIRECTORY/DAY0_ABSENT.json'
        rc, out = _emit(gone, 'missing_reference')
        record('day0_emitter_refuses_missing_reference',
               rc != 0 and 'REFUSING TO WRITE' in out
               and not os.path.exists(os.path.join(sb.path, new_ref)),
               'exit %s; no standing reference -> no mandatory diff is possible, so nothing is '
               'written (there is no lawful silent FIRST write)' % rc)

        # THE POSITIVE PATH. It loads the engine and re-prices every wired entrant off THIS tree's
        # board and store, so it is the expensive case in this self-test and it is the only one that
        # proves the emitter emits. It asserts the emitter's own fail-closed leg (A1, the printed
        # day-0 identity on the board it read) and the M1b diff — EVERY moved row, printed.
        #
        # THE REFERENCE IS A DOCTORED COPY, NOT THE STANDING ONE. Until the R24 advance this case
        # diffed against the live standing reference and passed only because that reference happened
        # to be STALE — the moment the flight installed a fresh one, "some rows moved" became false
        # and the case red-ed on tree state it does not own (caught 2026-08-23, the first
        # post-advance run). One row's printed price is perturbed by +1 here, so the mandatory-diff
        # assertion is non-vacuous BY CONSTRUCTION, forever, and names the row it expects.
        doct_rel = os.path.join(ev_rel, 'DAY0_DOCTORED_REF.json')
        os.makedirs(os.path.join(sb.path, ev_rel), exist_ok=True)
        with open(os.path.join(sb.path, std_ref), encoding='utf-8') as fh:
            _ref_doc = json.load(fh)
        _doct_key = _ref_doc['rows'][0]['key']
        _ref_doc['rows'][0]['printed'] = int(_ref_doc['rows'][0]['printed']) + 1
        _ref_doc['rows'][0]['day0_price'] = float(_ref_doc['rows'][0]['day0_price']) + 1.0
        with open(os.path.join(sb.path, doct_rel), 'w', encoding='utf-8') as fh:
            json.dump(_ref_doc, fh, indent=1, sort_keys=True)
        base_doc['day0_rebase']['reference'] = doct_rel
        rc, out = _emit(base_doc, 'regenerate')
        wrote = os.path.join(sb.path, new_ref)
        emitted = _read_json(wrote) or {}
        moved_lines = [ln for ln in out.splitlines() if ' -> ' in ln and '(+' in ln or
                       (' -> ' in ln and '(-' in ln)]
        identity_ok = 'A1  printed day-0 identity' in out and ' of ' in out
        record('day0_emitter_regenerates',
               rc == 0 and identity_ok and 'THE MANDATORY ROW DIFF' in out
               and bool(emitted.get('rows')) and bool(moved_lines)
               and any(_doct_key in ln for ln in moved_lines),
               'exit %s; identity %r; %d row(s) emitted; the mandatory diff printed %d moved row(s) '
               'individually (the doctored row %r among them), no truncation'
               % (rc, emitted.get('identity_all'), len(emitted.get('rows') or []),
                  len(moved_lines), _doct_key))
        try:
            os.remove(wrote)
        except OSError:
            pass
        sb.reset()

    # ---- 3f. THE EDIT VERB (`land edit`, directive 2026-08-24) ----------------------------------
    #
    # THE SAME STANDARD THE LEVER AND ROUND STEPS MET, AND THE SAME ORDER: the non-vacuity control
    # first — a clean store-edit landing in this sandbox must SUCCEED — then the step the verb ADDS
    # broken once, then the assertion that only this verb has (who moved on the board), then a
    # mid-flight failure with the store already edited.
    #
    # WHAT THE STRADDLE CASE IS FOR, because it is the whole reason the verb exists. Register v836:
    # `land lever` refused an owner-worded store edit three times, and the third refusal was the
    # lineage CHAIN — a store flip committed BEFORE the landing makes the entry's source store a value
    # no movers round report can bridge to. Applying the edit inside the transaction puts the source
    # (measured at the base commit) on the PRE-edit side and the destination (measured live) on the
    # POST-edit side. `edit_lineage_straddles` is that sentence, asserted on the file the landing
    # wrote.
    # WHERE THE POSITIVE CONTROL STOPS, AND WHY IT IS THE SAME WALL THE LEVER FIXTURE MEETS. A clean
    # END-TO-END edit landing cannot be flown with the self-test builder, and the reason is a property
    # of the tree rather than a limitation of this file: the `sibling` step's repin REBUILDS the
    # balanced board FROM THE REAL STORE and refuses to stage a forward view that is not the board the
    # manifest pins ("CONFORMANCE GATE FAILED … this is a STOP", owner ruling v471 §4). A synthetic
    # board can never satisfy it — which is exactly why `SELFTEST_SPEC_MOVED` is only ever used for
    # faults AT OR BEFORE `lineage` under `land lever`, and why the lever control lands a NO-OP.
    #
    # So the coverage is split the way the evidence is: the six steps that carry the edit are proved
    # HERE, cheaply, on their own merit (nothing is injected until `sibling` starts), and the CLEAN
    # END-TO-END landing — real build, real sibling reconcile, real gates, real commit — is proved
    # with the REAL builder in the acceptance flight filed at
    # docs/evidence/edit_verb_2026-08-24/GRAHAM_SANDBOX_FLIGHT.log, which also lands the standing
    # Graham prediction (store daa93053 -> fb640ca0, board 6fd0f7de -> 82fcd8bb, ONE mover).
    if not only or 'store_edit' in only:
        print('')
        print('--- EDIT: the six steps that carry the edit, on their own merit (THE EDIT VERB) ---')
        sb.reset()
        edit_base = sb.head()
        store_p = os.path.join(sb.path, ST.STORE_REL)
        store_before = _md5(store_p)
        before = carrier_md5s(sb.path)
        rep = os.path.join(ev, 'edit_control_report.json')
        rc, out = sb.run_lander('SELFTEST_SPEC_EDIT.json', fault='sibling', builder='selftest-moved',
                                verb='edit', report=rep, log=os.path.join(ev, 'edit_control.log'))
        open(os.path.join(ev, 'edit_control_stdout.txt'), 'w', encoding='utf-8').write(out)
        report = _read_json(rep) or {}
        facts = report.get('facts') or {}
        se, bp = facts.get('store_edit') or {}, facts.get('build_proofs') or {}
        pins, lin = facts.get('pins') or {}, facts.get('lineage') or {}
        store_edited = se.get('store_after')
        record('edit_steps_clean_through_contract',
               (se.get('written') is True and se.get('store_before') == store_before
                and store_edited and store_edited != store_before
                and (se.get('season_state') or {}).get('source_store_md5') == store_edited
                and (bp.get('edit') or {}).get('store_read_by_build') == store_edited
                and sorted(pins.get('moved') or []) == ['board', 'store']
                and (lin.get('column') or {}).get('id') == 'selftest-store-edit'
                and (lin.get('entry') or {}).get('appended') is True
                and (facts.get('contract') or {}).get('check') == 'PASS'),
               'ONE surgical field edit (%s.%s %s -> %s) moved the store %s -> %s; the board was '
               'built FROM it; pins moved %s; the column and the lineage entry were written; the '
               'contract re-sealed and PASSED — then the injected fault stopped it at `sibling`'
               % (the_edit['key'], the_edit['field'], the_edit['old'], the_edit['new'],
                  store_before[:12], str(store_edited)[:12], sorted(pins.get('moved') or [])))

        entry_src = (lin.get('entry') or {}).get('source') or {}
        entry_dst = (lin.get('entry') or {}).get('destination') or {}
        record('edit_lineage_straddles',
               entry_src.get('store') == store_before and entry_dst.get('store') == store_edited
               and entry_src.get('board') == board
               and entry_dst.get('board') == hashlib_moved(sb.path),
               'the entry STRADDLES the edit: source.store %s (measured at the base commit, PRE-edit) '
               '-> destination.store %s (measured live, POST-edit); source.board %s -> '
               'destination.board %s. This is the shape register v836\'s third abort says a '
               'pre-committed flip can never produce.'
               % (str(entry_src.get('store'))[:12], str(entry_dst.get('store'))[:12],
                  str(entry_src.get('board'))[:12], str(entry_dst.get('board'))[:12]))

        after = carrier_md5s(sb.path)
        movedc = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        wrote = [r['path'] for r in (report.get('abort') or {}).get('restored') or []]
        record('edit_abort_restores_store',
               rc != 0 and report.get('failed_step') == 'sibling' and not movedc
               and sb.head() == edit_base and ST.STORE_REL in wrote and len(wrote) >= 4,
               '%d carrier(s) had been written and were restored BYTE-EXACT, the STORE among them '
               '(%s); HEAD %s: %s'
               % (len(wrote), 'yes' if ST.STORE_REL in wrote else 'NO — the point of this case is '
                  'back', 'back at the base' if sb.head() == edit_base else 'MOVED',
                  ', '.join(wrote[:6])))
        sb.reset()

        print('')
        print('--- EDIT FAULTS: the step the verb ADDS, and the mover assertion only it makes ---')
        for label, fault_key, step_name, needle in (
                ('edit_fault_store_edit', 'store_edit', 'store_edit',
                 'THE OLD VALUE THE SPEC ASSERTS IS NOT THE VALUE IN THE STORE'),
                ('edit_fault_second_mover', 'build_proofs:second_mover', 'build_proofs',
                 'UNEXPECTED MOVER')):
            mode, _what, _inj = TX.FAULTS[fault_key]
            before = carrier_md5s(sb.path)
            rep = os.path.join(ev, '%s_report.json' % label)
            rc, out = sb.run_lander('SELFTEST_SPEC_EDIT.json', fault=fault_key,
                                    builder='selftest-moved', verb='edit', report=rep,
                                    log=os.path.join(ev, '%s.log' % label))
            open(os.path.join(ev, '%s_stdout.txt' % label), 'w', encoding='utf-8').write(out)
            report = _read_json(rep) or {}
            tally['broken'] += 1
            caught = (rc != 0) and report.get('failed_step') == step_name
            after = carrier_md5s(sb.path)
            moved_carriers = sorted(k for k in set(before) | set(after)
                                    if before.get(k) != after.get(k))
            head_ok = sb.head() == edit_base
            byte_exact = not moved_carriers and head_ok
            named = needle in out
            if caught:
                tally['caught'] += 1
            if byte_exact:
                tally['aborted_byte_exact'] += 1
            record(label, caught and byte_exact and named,
                   'fault=%s; exit %s; failed_step=%r; the halt NAMES it (%r %s); carriers moved '
                   'after abort: %s; HEAD %s'
                   % (mode, rc, report.get('failed_step'), needle, 'found' if named else 'ABSENT',
                      moved_carriers or 'NONE (byte-exact)',
                      'back at the base' if head_ok else 'MOVED'))
            sb.reset()

    # ---- 4. THE CLAIMS NEGATIVE CONTROL ---------------------------------------------------------
    print('')
    print('--- CLAIMS: the checker\'s own negative control still fires ---')
    rc, out = _sh([sys.executable, 'tools/claims.py', 'selftest'], cwd=sb.path, env=sb.env())
    open(os.path.join(ev, 'claims_selftest.txt'), 'w', encoding='utf-8').write(out)
    last = [ln for ln in out.splitlines() if 'SELF-TEST' in ln]
    record('claims_negative_control', rc == 0 and ' 0 FAIL' in out,
           last[-1].strip() if last else 'exit %s' % rc)

    # ---- 5. THE PACKET VALIDATOR ----------------------------------------------------------------
    rc, out = _sh([sys.executable, '-c',
                   'import sys;sys.path.insert(0,".");from tools.landing import packet as P;'
                   'sys.exit(P.selftest())'], cwd=sb.path, env=sb.env())
    open(os.path.join(ev, 'packet_selftest.txt'), 'w', encoding='utf-8').write(out)
    record('packet_slot_validator', rc == 0,
           [ln for ln in out.splitlines() if 'PACKET SELF-TEST' in ln][-1].strip()
           if 'PACKET SELF-TEST' in out else 'exit %s' % rc)

    # ---- 6. THE LIVE TREE, ASSERTED UNTOUCHED ---------------------------------------------------
    live_after = carrier_md5s(root)
    drift = sorted(k for k in set(live_before) | set(live_after)
                   if live_before.get(k) != live_after.get(k))
    record('live_tree_untouched', not drift,
           'every live carrier byte-unmoved across the whole self-test' if not drift
           else 'THE SELF-TEST TOUCHED THE LIVE TREE: %s' % drift)

    print('')
    print(BANNER)
    ok = sum(1 for _n, o, _d in results if o)
    print('STEPS BROKEN %d   CAUGHT %d   ABORTED BYTE-EXACT %d'
          % (tally['broken'], tally['caught'], tally['aborted_byte_exact']))
    print('SELF-TEST: %d PASS / %d FAIL' % (ok, len(results) - ok))
    print(BANNER)
    summary = {'results': [{'case': n, 'ok': o, 'detail': d} for n, o, d in results], 'tally': tally,
               'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    with open(os.path.join(ev, 'SELFTEST_SUMMARY.json'), 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)

    # CLEANUP LAST, AND NEVER UNDER THE TRANSCRIPTS. An earlier version tore the work directory down
    # BEFORE writing this summary; when no --evidence was given the transcripts lived inside that
    # directory, so the summary write raised and the whole self-test exited non-zero with 17 of 17
    # cases green. It was caught by the acceptance landing, whose gate step runs this self-test
    # without an evidence directory — a defect in the harness, found by the program the harness
    # tests, which is the right way round.
    if not keep:
        sb.destroy()
        if not os.path.abspath(ev).startswith(os.path.abspath(work) + os.sep):
            shutil.rmtree(work, ignore_errors=True)
        else:
            for name in os.listdir(work):
                p = os.path.join(work, name)
                if os.path.abspath(p) != os.path.abspath(ev):
                    shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)
    else:
        print('\nsandbox KEPT at %s' % sb.path)
    return 0 if ok == len(results) else 1


def _synthetic_scores(sandbox_path):
    """A SYNTHETIC owner score file for the round AFTER the one the sandbox stands on. Never data.

    THE SHAPE IS THE OWNER'S EXPORT SHAPE, because the parser of record is what reads it: two
    columns, header `Player,2026 R<N>`, cp1252, CRLF, trailing newline. It is derived from the tree's
    OWN most recent score file so every display name in it is a name that already resolved once —
    the fixture is not allowed to invent people.

    TWO CLASSES ARE DROPPED, and both would halt this flight for a reason that is not the pincer:

      * any player the pinned owner sheet marks `injured=Y` — the H2 check (ORDER 42) fires on those
        and the remedy is an owner-worded sheet re-cut, which `sheet_recut_writer` already proves;
      * any display name whose identity override is scoped to rounds that do not include this one —
        at R24 that is the R23 `Bailey Williams WBD` binding, which would leave a name unresolved and
        the preflight not clean. The lander never guesses a name and neither does this fixture.

    DETERMINISTIC: the scores are carried across verbatim, so the file's md5 is a function of the
    tree alone and two self-test runs on one tree write the same bytes.
    """
    import csv
    import re as _re

    def _norm(s):
        return _re.sub(r'[^a-z0-9]+', '-', str(s).strip().lower().replace('’', "'")).strip('-')

    boot = json.load(open(os.path.join(sandbox_path, 'data', 'expected_boot.json'),
                          encoding='utf-8'))
    n = int(boot['as_of_round']) + 1
    pins = json.load(open(os.path.join(sandbox_path, 'data', 'sheet_pins.json'), encoding='utf-8'))
    with open(os.path.join(sandbox_path, pins['sheet_path']), encoding='utf-8') as fh:
        injured = {_norm(r['player']) for r in csv.DictReader(fh)
                   if (r.get('injured') or '').strip().upper() == 'Y'}
    ov = json.load(open(os.path.join(sandbox_path, ST.CATCHUP_OVERRIDES_REL), encoding='utf-8'))
    out_of_round = {e.get('name') for e in (ov.get('overrides') or [])
                    if e.get('applies_to_rounds') and n not in e['applies_to_rounds']}

    prev = None
    for r in range(n - 1, 0, -1):
        cand = os.path.join(sandbox_path, 'scores', 'R%d.csv' % r)
        if os.path.isfile(cand):
            prev = cand
            break
    if prev is None:
        raise RuntimeError('no previous score file in the sandbox to shape the fixture on')
    text = open(prev, 'rb').read().decode('cp1252')
    rows = [r for r in list(csv.reader(text.splitlines()))[1:] if r]
    kept = [(name, int(score)) for name, score in rows
            if _norm(name) not in injured and name.strip() not in out_of_round]
    data = ('Player,2026 R%d\r\n' % n
            + ''.join('%s,%d\r\n' % (name, score) for name, score in kept)).encode('cp1252')
    rel = os.path.join('scores', 'R%d.csv' % n)
    dst = os.path.join(sandbox_path, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'wb') as fh:
        fh.write(data)
    return {'round': n, 'path': rel, 'listed': len(kept), 'bytes': len(data),
            'md5': hashlib.md5(data).hexdigest(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'SYNTHETIC': 'SELF-TEST FIXTURE — this is not owner data and never was.'}


def _synthetic_recut(sandbox_path, restore_md5=None):
    """Append ONE byte to the sheet's first data row's (empty, unquoted) notes cell. -> the new md5.

    It moves the md5 and leaves the row count and the injured=Y count exactly where they are, which
    is the smallest re-cut that still exercises the writer. It is done to a SANDBOX WORKTREE only;
    the live sheet is an owner input and this package never edits owner data.
    """
    p = os.path.join(sandbox_path, 'docs', 'owner_annotations', 'SITTER_2026_v1.csv')
    raw = open(p, 'rb').read()
    if restore_md5 is not None and hashlib.md5(raw).hexdigest() == restore_md5:
        return restore_md5
    i = raw.index(b'\r\n')                       # end of the header
    j = raw.index(b'\r\n', i + 2)                # end of the first data row
    raw = raw[:j] + b'x' + raw[j:]
    with open(p, 'wb') as fh:
        fh.write(raw)
    return hashlib.md5(raw).hexdigest()


def hashlib_moved(sandbox_path):
    """The md5 the SelftestBuilder(moved=True) will produce: the board plus one newline."""
    raw = open(os.path.join(sandbox_path, 'data', 'rl_build', 'rl_app_data.json'), 'rb').read()
    return hashlib.md5(raw + b'\n').hexdigest()


def _read_json(path):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


if __name__ == '__main__':
    sys.exit(main())
