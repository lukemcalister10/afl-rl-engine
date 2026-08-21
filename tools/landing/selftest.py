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


def carrier_md5s(root):
    """The parent's OWN measurement of every carrier. Never the child's."""
    out = {}
    for rel in CA.expand(root):
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


def spec_moved(board_before, board_after, evidence_rel):
    """A synthetic board move, so pins / column / lineage run their REAL writers on a real move."""
    d = _spec_common(evidence_rel)
    d.update({
        'act': 'SELF-TEST — the synthetic board move',
        'prereg': {'path': 'tools/landing/selftest.py (fixture)', 'board_before': board_before,
                   'board_after': board_after, 'reference_board': None, 'kill_switch': None},
        'identities': {'moves': ['board'],
                       'unmoved': ['store', 'engine_head', 'rl_model', 'fv', 'config', 'register']},
        'column': {'id': 'selftest-synthetic-move', 'after_round': 23,
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


# ------------------------------------------------------------------------------------ the sandbox
class Sandbox(object):
    """A git worktree of HEAD, carrying the CURRENT lander, committed so the tree reads clean."""

    def __init__(self, root, work_dir):
        self.live_root = os.path.abspath(root)
        self.work_dir = work_dir
        self.path = os.path.join(work_dir, 'sandbox')
        self.base_commit = None
        self.lock_file = os.path.join(work_dir, 'selftest.lock')

    def create(self):
        os.makedirs(self.work_dir, exist_ok=True)
        rc, out = _sh(['git', 'worktree', 'add', '--detach', self.path, 'HEAD'], cwd=self.live_root)
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
        env['RL_BUILD_LOCK_FILE'] = self.lock_file       # never contend with the box's real lock
        env.pop('RL_BUILD_LOCK_HELD', None)
        env['GIT_AUTHOR_NAME'] = env['GIT_COMMITTER_NAME'] = 'selftest'
        env['GIT_AUTHOR_EMAIL'] = env['GIT_COMMITTER_EMAIL'] = 'selftest@local'
        return env

    def run_lander(self, spec_rel, fault=None, builder='selftest', report=None, log=None,
                   extra=()):
        argv = [sys.executable, os.path.join(self.path, 'tools', 'landing', 'cli.py'), 'lever',
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
def main(root=None, keep=False, only=None, evidence_dir=None):
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
    sb = Sandbox(root, work).create()
    print('sandbox created at %s (base %s)' % (sb.path, sb.base_commit[:12]))

    board = _md5(os.path.join(sb.path, 'data', 'rl_build', 'rl_app_data.json'))
    ev_rel = 'docs/evidence/landing_selftest'
    os.makedirs(os.path.join(sb.path, ev_rel), exist_ok=True)
    noop = spec_noop(board, ev_rel)
    moved = spec_moved(board, hashlib_moved(sb.path), ev_rel)
    with open(os.path.join(sb.path, 'SELFTEST_SPEC_NOOP.json'), 'w', encoding='utf-8') as fh:
        json.dump(noop, fh, indent=2)
    with open(os.path.join(sb.path, 'SELFTEST_SPEC_MOVED.json'), 'w', encoding='utf-8') as fh:
        json.dump(moved, fh, indent=2)
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
