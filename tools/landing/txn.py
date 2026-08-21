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
import shutil
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


def _fault_stale_ownership_mirror(ctx):
    """WRITER 5 never runs, AND the shipped mirror carries a foreign store pin.

    THE FAULT IS THE TREE'S OWN HISTORY, NOT AN INVENTION. Between the R23 advance and 2026-08-21 the
    store moved and `ui/data/ownership.js` kept the pin of the store before it, so
    `ui/app/ownership.js:pin()` refused the mirror and the live ownership lane was off with nothing
    rendering an error. This reproduces exactly that: the pin is falsified, and the writer that would
    repair it is silenced — because a fault that only falsified the file would be REPAIRED by the
    unconditional writer and prove nothing about the step's predicate.
    """
    ctx.skip_ownership_writer = True
    p = os.path.join(ctx.root, 'ui', 'data', 'ownership.js')
    boot = json.load(open(os.path.join(ctx.root, 'data', 'expected_boot.json'), encoding='utf-8'))
    raw = open(p, encoding='utf-8').read()
    stale = 'c' * 32
    raw = raw.replace('"generatedFromStore": "%s"' % boot['store'],
                      '"generatedFromStore": "%s"' % stale)
    raw = raw.replace('"store": "%s"' % boot['store'][:8], '"store": "%s"' % stale[:8])
    open(p, 'w', encoding='utf-8').write(raw)


def _fault_gate_red(ctx):
    p = os.path.join(ctx.root, 'data', 'expected_boot.json')
    raw = open(p, encoding='utf-8').read()
    boot = json.loads(raw)
    open(p, 'w', encoding='utf-8').write(raw.replace(boot['board'], 'a' * 32))


def _fault_false_claim(ctx):
    ctx.false_claim = True


def _fault_state_ungeneratable(ctx):
    """The record pointer the state file must QUOTE is taken out of the tree.

    P6 is the step's whole reason to exist — "a derived surface that cannot be generated does not
    exist" — so the fault that tests it is a missing input, not a corrupted output. Corrupting
    `docs/STATE.md` would prove nothing: the step rewrites it. Removing `docs/register/LATEST.md`
    means the register pointer cannot be computed, and the honest behaviour is a HALT with the
    carrier named, never a state file that quietly carries the last landing's line 1 forward.
    """
    p = os.path.join(ctx.root, 'docs', 'register', 'LATEST.md')
    if os.path.isfile(p):
        os.remove(p)


def _fault_foreign_path(ctx):
    open(os.path.join(ctx.root, 'docs', 'LANDING_FAULT_FOREIGN.md'), 'w').write('not a carrier\n')


# ------------------------------------------------------- fault injection: the round lander's steps
def _fault_sheet_pin_drift(ctx):
    """The sheet moves and its ONE declaration does not — the exact drift that halts ORDER 41."""
    p = os.path.join(ctx.root, 'docs', 'owner_annotations', 'SITTER_2026_v1.csv')
    with open(p, 'ab') as fh:
        fh.write(b'\r\n')


def _fault_scores_absent(ctx):
    """The act declares an owner file of record that is not in the tree."""
    ctx.spec['round']['scores'] = {'path': 'scores/R99_NOT_A_REAL_FILE.csv',
                                   'md5': '0' * 32, 'sha256': '0' * 64}
    ctx.spec['prereg']['round_expected'] = {'round': 99, 'listed': 0, 'resolved': 0, 'absent_dnp': 0,
                                            'scores_sha256': '0' * 64, 'ledger_before': 0,
                                            'ledger_delta': 0}
    ctx.spec['round']['arming'] = {'env': {'INGEST_SCORE_APPLY_ARMED': '1',
                                           'INGEST_SCORE_APPLY': 'selftest-never-armed'},
                                   'owner_word': 'SELF-TEST FIXTURE — no owner word exists.'}


def _fault_round_already_applied(ctx):
    """The act points the preflight at a round the dedup ledger has already applied."""
    boot = json.load(open(os.path.join(ctx.root, 'data', 'expected_boot.json'), encoding='utf-8'))
    n = int(boot['as_of_round'])
    ctx.spec['round']['number'] = n
    ctx.spec['round']['scores'] = {'path': 'scores/R%d.csv' % n, 'md5': _md5_of(
        os.path.join(ctx.root, 'scores', 'R%d.csv' % n)), 'sha256': _sha_of(
        os.path.join(ctx.root, 'scores', 'R%d.csv' % n))}
    ctx.spec['prereg']['round_expected'] = {
        'round': n, 'listed': 411, 'resolved': 411, 'absent_dnp': 393,
        'scores_sha256': _sha_of(os.path.join(ctx.root, 'scores', 'R%d.csv' % n)),
        'ledger_before': 0, 'ledger_delta': 0}
    ctx.spec['round']['arming'] = {'env': {'INGEST_SCORE_APPLY_ARMED': '1',
                                           'INGEST_SCORE_APPLY': 'selftest-never-armed'},
                                   'owner_word': 'SELF-TEST FIXTURE — no owner word exists.'}


def _fault_round_mismatch(ctx):
    """The act claims to be advancing a round the tree is not standing on."""
    ctx.spec['round']['number'] = 99


def _fault_generator_drift(ctx):
    """The generator-side copy stops being the published board in an act that moves nothing."""
    with open(os.path.join(ctx.root, 'engine', 'rl_after', 'rl_app_data.json'), 'ab') as fh:
        fh.write(b' ')


def _fault_day0_no_movers(ctx):
    """The day-0 re-base is ACTIVATED and no row moves — the M1b guard, in the round lander.

    `generator: []` — DECLARED EMPTY, not absent — because this fault is about the STEP's refusal to
    install a re-base that changes nothing, and an absent key now means "run the carried emitter"
    (`steps.DAY0_GENERATOR`), which would regenerate `new_reference` and hand the step a diff. The
    emitter's own refusals are proved by their own cases in the self-test, not smuggled in here.
    """
    ref = 'docs/evidence/final_candidate_2026-08-19/DAY0_CP.json'
    ctx.spec['day0_rebase'] = {'state': 'on', 'reference': ref, 'new_reference': ref,
                               'generator': [],
                               'activated_by': 'SELF-TEST FIXTURE — no owner word exists.'}


def _fault_stop_before_arming(ctx):
    """STOP AT THE DOOR OF THE ARMED ADVANCE — the one fault that exists to prove the steps BEFORE it.

    THE SELF-TEST NEVER ARMS. Every other round case runs the `round.scores: null` rehearsal fixture,
    so `preflight`'s declared-dirt path and `catchup_preflight`'s input commit — the two jaws of the
    R24 rehearsal's input-commit pincer (§3.1) — had never been exercised by anything. Proving they
    are gone needs a flight carrying a REAL, UNCOMMITTED score file through steps 0-3, and then needs
    to stop before the advance applies a round to the sandbox's store.

    So this injector raises where it stands. It is not a broken step and it is not counted as one:
    the assertion the case makes is about the four steps that already succeeded.
    """
    raise ST.StepError(
        'STOPPED AT THE DOOR, BY REQUEST (selftest fault `advance:stop_at_the_door`). Steps 0-3 ran '
        'for real against an uncommitted owner score file; the armed advance is where this case '
        'deliberately ends, because a self-test does not arm a score-write.')


def _fault_movers_report_drift(ctx):
    """The movers report stops naming the board the manifest names."""
    boot = json.load(open(os.path.join(ctx.root, 'data', 'expected_boot.json'), encoding='utf-8'))
    p = os.path.join(ctx.root, 'engine', 'rl_after', 'ingestion', 'movers',
                     'movers_R%s.json' % boot['as_of_round'])
    d = json.load(open(p, encoding='utf-8'))
    d['board_md5_after'] = 'f' * 32
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(d, fh)


def _md5_of(path):
    import hashlib
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def _sha_of(path):
    import hashlib
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


#: step -> (mode name, what it breaks, the injector). ONE per step: the plan asks for each step
#: broken once, and each of these breaks the thing that step exists to check.
#:
#: A KEY MAY ALSO BE MODE-QUALIFIED, `'<step>:<mode>'`. `--fault step:mode` was ALWAYS parsed that way
#: (fault_point has split on the colon since the first draft) and the mode half was then thrown away,
#: so a step carrying more than one thing worth breaking had no way to say which. The `ui` step now
#: runs FIVE writers guarding five different predicates; one fault key for all of them would mean
#: four of them were never broken. The plain `'<step>'` key remains the step's default fault, so the
#: self-test's "every step, broken once" loop is untouched — a qualified key ADDS a case, it never
#: replaces one.
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
    'state':        ('state_ungeneratable',
                     'a carrier the state file must READ is gone, so the file cannot be generated',
                     _fault_state_ungeneratable),
    'gates':        ('gate_red', 'a landed pin is wrong, so the manifest gate reds',
                     _fault_gate_red),
    'claims':       ('false_claim', 'the claims file carries a claim the tree contradicts',
                     _fault_false_claim),
    'commit':       ('foreign_path', 'a file outside the declared carrier set is in the tree',
                     _fault_foreign_path),

    # ---- MODE-QUALIFIED: the `ui` step's other writers ------------------------------------------
    'ui:stale_mirror': ('stale_ownership_mirror',
                        'WRITER 5 never runs and the shipped ownership mirror keeps a foreign store '
                        'pin — the live ownership lane ships SWITCHED OFF, silently',
                        _fault_stale_ownership_mirror),

    # ---- the round lander's own steps (PLAN_v6 2b) ----------------------------------------------
    'sheet':             ('sheet_pin_drift',
                          'the owner sheet moves and its ONE pin declaration does not — the drift '
                          'that halts ORDER 41 inside the staged transaction',
                          _fault_sheet_pin_drift),
    'scores':            ('scores_absent',
                          "the act declares an owner file of record that is not in the tree",
                          _fault_scores_absent),
    'catchup_preflight': ('round_already_applied',
                          'the round is already in the dedup ledger — the preflight says CLEAN and '
                          'the advance would certify a round it did not apply',
                          _fault_round_already_applied),
    'advance':           ('round_mismatch',
                          'the act claims a round the tree is not standing on',
                          _fault_round_mismatch),
    'generator_sync':    ('generator_drift',
                          'the generator-side board copy stops being the published board',
                          _fault_generator_drift),
    'day0':              ('day0_no_movers',
                          'THE M1b GUARD: the day-0 re-base is ACTIVATED and no row moves',
                          _fault_day0_no_movers),
    'advance:stop_at_the_door': ('stop_before_arming',
                          'the transaction is stopped at the door of the armed advance, so the case '
                          'measures the four steps that already ran — the input-commit pincer',
                          _fault_stop_before_arming),
    'movers_page':       ('movers_report_drift',
                          'the movers report stops naming the board the manifest names, so the page '
                          'would describe a different tree than the one that produced it',
                          _fault_movers_report_drift),
}


# ------------------------------------------------------------------------------------- the context
class Ctx(object):
    """Everything a step is allowed to know. A step never reaches for global state."""

    #: Seconds to wait for a contended build lock. A real landing waits (the shared workspace is
    #: routinely busy); the self-test sets 0 so its lock case halts at once instead of for an hour.
    DEFAULT_LOCK_TIMEOUT = 3600

    def __init__(self, root, spec, opts, evidence_dir=None, builder=None, fault=None,
                 carriers=CA.LEVER_CARRIERS, work_dir=None, lock_tag=None, lock_timeout=None,
                 keep_work=False):
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
        self.lock_tag = lock_tag or ('land-%s-%d' % (
            'round' if spec.get('act_kind') == 'round-advance' else 'lever', os.getpid()))
        self.lock_timeout = (0 if lock_timeout is None and opts.selftest
                             else (self.DEFAULT_LOCK_TIMEOUT if lock_timeout is None else lock_timeout))
        self._lock_fd = None
        self.lander_dir = os.path.dirname(os.path.abspath(__file__))
        self.work_dir = work_dir or os.path.join(
            os.environ.get('LANDING_SNAPSHOT_DIR') or '/tmp', 'landing_work_%d' % os.getpid())
        os.makedirs(self.work_dir, exist_ok=True)
        #: Keep the work dir (restore point + intermediate boards) after the transaction closes.
        #: The default discards it — see `_discard_work_dir`, and the 1.4GB of orphans that ruling
        #: was written against.
        self.keep_work = keep_work
        self.evidence_dir = evidence_dir or os.path.join(self.root, spec.get('evidence_dir') or
                                                         'docs/evidence/landing_%s' % spec.get('date', 'undated'))
        #: EVERY COMMIT THIS LANDING MAKES, newest last. A lever landing makes one, at the end. A
        #: round advance makes three — the sheet commit, the inputs commit and the landing commit —
        #: because PACKAGE 3a's form puts the data change in its own commit BEFORE the advance and
        #: the owner's input of record must enter the tree before anything is armed. The list is what
        #: `_abort` rewinds: a mid-flight commit that survived an abort would make the abort's
        #: byte-exactness claim quietly exclude history.
        self.commits_made = []
        # fault-injection flags a step reads; all default to the safe value
        self.skip_second_ui_writer = False
        self.skip_ownership_writer = False
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
        """The environment a child gets: RL_REPO set to THIS tree, and NO RL_BUILD_LOCK_HELD.

        THE LOCK'S OWN VARIABLE IS NEVER EXPORTED, and the road to that rule ran through two wrong
        answers, both measured rather than reasoned about:

          1. The first version dropped RL_BUILD_LOCK_HELD from every child. The landing then
             DEADLOCKED AGAINST ITS OWN GATE: it holds the flock, step 7 runs the acceptance runner,
             the runner's determinism check shells out to `build_lock.sh run`, and build_lock.sh —
             which uses exactly that variable to recognise a reentrant grant — blocked on the lock
             the lander was holding.
          2. The second version exported it to gate children. The lander's own gate step then caught
             the side effect: `ruled_red_ledger` went FAIL, "R15-ladder-proof-GFWD is DRIFTED".
             Reproduced on the live tree in one line — `RL_BUILD_LOCK_HELD=probe python3 -m
             acceptance.runner --only ruled_red_ledger` is FAIL where the bare run is PASS. An
             unknown RL_-prefixed variable changes how the r15 proof dies, so the probe no longer
             fails the way its ruling records. THE VARIABLE IS NOT INERT IN A GATE CHILD, and the
             five checks measured before adopting it were the wrong five.

        THE ANSWER IS TO STOP CARRYING THE CONTRADICTION: the lock is held across the steps that
        BUILD (0-6) and released before the gates, which do not write and whose own builds take the
        lock themselves (`acceptance/checks/m1a.py` wraps its determinism build in
        `build_lock.sh run`). See `steps.LOCK_HELD_THROUGH` and the release in `run()`.
        """
        env = dict(os.environ)
        env.pop('RL_BUILD_LOCK_HELD', None)
        env['RL_REPO'] = self.root
        env['PYTHONHASHSEED'] = env.get('PYTHONHASHSEED', '0')
        return env

    def run(self, argv, timeout=1800, env_overrides=None):
        """Run a child in the landing's environment. `env_overrides` is for THE ARMING AND NOTHING
        ELSE: the round advance arms both halves of the score-write gate for one run, from the act
        spec, on the owner's word (law 10c). It is a parameter rather than an exported variable
        precisely so that the arming cannot leak into any other child this landing spawns."""
        env = self.child_env()
        env.update({str(k): str(v) for k, v in (env_overrides or {}).items()})
        p = subprocess.run(argv, cwd=self.root, capture_output=True, text=True,
                           env=env, timeout=timeout)
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

    def declared_dirt(self):
        """THE ONLY DIRT A LANDING MAY START ON, and it is DECLARED, ENUMERATED, and act-specific.

        A LEVER LANDING HAS NONE. It builds what it lands, so a modified file at step 0 is somebody
        else's work and the tree must be clean, full stop.

        A ROUND ADVANCE HAS TWO CLASSES, and neither is an exception so much as the shape of the act.

        (1) THE SHEET RE-CUT, when one is declared. The owner's sheet is re-cut BY THE SEAT, on the
            owner's word — the lander never authors owner data — and the prereg-lite is written by
            the seat before the sheet is touched. Both must therefore be present and uncommitted
            when the lander starts, because committing them is the `sheet` step's job (PACKAGE 3a's
            form: sheet + declaration + prereg-lite, ONE commit).

        (2) THE OWNER'S INPUTS OF RECORD, when `round.scores` is declared: THE SCORE FILE AND THE
            IDENTITY-OVERRIDE RECORD. Same shape, same reason. The runbook's step 0 is "place the
            owner's file, byte-unmodified -> scores/R<N>.csv"; an owner ruling on a name is recorded
            by the seat in `catchup_identity_overrides.json`; and `steps.catchup_preflight`'s
            contract is that IT commits both, as their own explicit-path commit, once the preflight
            is clean — "so the owner's input of record enters the tree BEFORE anything is armed".

        THE PINCER THIS CLOSES (R24 dress rehearsal, 2026-08-21, §3.1 — RUN A and RUN C). Until this
        method enumerated class (2), the armed path of `land round` was UNREACHABLE AS SHIPPED:

          * score file uncommitted -> step 0 halted, `THE TREE IS NOT CLEAN … ?? scores/R24.csv`;
          * score file committed   -> step 3 reached PREREG MET and then died, `git commit failed:
            … nothing added to commit but untracked files present`.

        There was no third option, and the self-test could not see it because its round fixture
        declares no score file. The remedy is the symmetric, obviously-intended one the rehearsal
        recommended: what the lander is contracted to COMMIT is what the lander must EXPECT to find
        uncommitted. (`steps._git_commit` was made graceful about an already-committed input in the
        same act, so a seat who pre-commits the file — the rehearsal's interim path — is no longer
        punished for it either. Both jaws, not one.)

        Every path is NAMED, out of the act spec or out of the pin file, and every one is PRINTED at
        step 0. Nothing is waved through: anything else, including a second edit to either file's
        directory, is dirt and halts.
        """
        if self.spec.get('act_kind') != 'round-advance':
            return ()
        out = []
        sheet = self.spec.get('sheet')
        if sheet:
            rel = sheet.get('path')
            if not rel:
                try:
                    with open(os.path.join(self.root, 'data', 'sheet_pins.json'),
                              encoding='utf-8') as fh:
                        rel = json.load(fh).get('sheet_path')
                except (OSError, ValueError):
                    rel = None
            out.extend(p for p in (rel, sheet.get('prereg_lite')) if p)
        scores = (self.spec.get('round') or {}).get('scores')
        if scores and scores.get('path'):
            out.append(scores['path'])
            out.append(ST.CATCHUP_OVERRIDES_REL)
        return tuple(out)

    def is_ignorable_dirt(self, status_line):
        """Nothing is ignorable except the act's own DECLARED dirt. One named place, always.

        AN UNTRACKED DIRECTORY IS EXPANDED, NEVER WAVED THROUGH. `git status --porcelain` collapses a
        wholly-untracked directory to one `?? dir/` line, and a prereg-lite written into a fresh
        evidence directory arrives exactly that way. Accepting the line because the directory
        CONTAINS a declared path would accept everything else in it too. So the directory is walked,
        and it is ignorable only if EVERY file under it is declared dirt.
        """
        allowed = self.declared_dirt()
        if not allowed:
            return False
        rel = status_line[3:].strip().strip('"')
        if ' -> ' in rel:
            rel = rel.split(' -> ')[-1]
        if rel in allowed:
            return True
        if not rel.endswith('/'):
            return False
        base = os.path.join(self.root, rel.rstrip('/'))
        if not os.path.isdir(base):
            return False
        found = []
        for dirpath, _d, files in os.walk(base):
            for f in files:
                found.append(os.path.relpath(os.path.join(dirpath, f), self.root))
        return bool(found) and all(f in allowed for f in found)

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

        THE LOCK TOOLING'S OWN FLAGS ARE NOT `RL_*` — `BUILD_LOCK` and `BUILD_LOCK_FILE`, matching
        `tools/build_lock.sh` character for character so the two stay interchangeable. They were
        RL_-prefixed until 2026-08-21, and it cost a real armed run: R24 dress rehearsal §3.3, RUN D,
        `ConfigPolicyError: UNKNOWN inherited valuation flag RL_BUILD_LOCK_FILE`. The legacy names
        are HALTED here rather than ignored — a sandbox whose isolation flag stopped being read is a
        sandbox silently contending for the shared lock, which is worse than the halt.
        """
        legacy = [k for k in ('RL_BUILD_LOCK', 'RL_BUILD_LOCK_FILE') if os.environ.get(k)]
        if legacy:
            raise ST.StepError(
                'BUILD-LOCK HALT: %s set in this environment. The lock tooling\'s own flags are no '
                'longer RL_-prefixed (an RL_/PAR_ variable is a MODEL override to '
                'config_manifest.enforce() and halts any armed build that inherits it — R24 '
                'rehearsal §3.3). Use %s. This is a halt and not a silent ignore because an '
                'isolation flag nobody reads is a sandbox contending for the shared lock.'
                % (', '.join(legacy), ', '.join(k[3:] for k in legacy)))
        if os.environ.get('BUILD_LOCK') == '0':
            self.log('build-lock: SKIPPED by BUILD_LOCK=0. This landing is NOT interlocked.')
            return
        path = os.environ.get('BUILD_LOCK_FILE') or LOCK_FILE_DEFAULT
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
        except OSError as e:
            raise ST.StepError('BUILD-LOCK HALT: cannot open %s (%s). A build that cannot prove it '
                               'is the single writer does not start.' % (path, e))
        # THE PROTOCOL IS build_lock.sh's, because the two must be interchangeable: try once without
        # blocking so the uncontended case prints nothing but the grant, and on contention print THE
        # REQUIRED LINE — a named holder and a named time, never "resource temporarily unavailable"
        # — then wait. A landing that refused the instant another seat held the lock would send the
        # seat to retry by hand, which is how a lock stops being taken at all.
        deadline = time.time() + self.lock_timeout
        announced = False
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                holder = ''
                try:
                    holder = open(path, encoding='utf-8').readline().strip().replace('\t', ' ')
                except OSError:
                    pass
                if not announced:
                    parts = (holder or '').split()
                    self.log('waiting for lock held by %s since %s'
                             % (parts[0] if parts else '<unknown>',
                                parts[2] if len(parts) > 2 else '<unknown>'))
                    self.log('  (lock %s; waiting up to %ds; this landing will not start until that '
                             'act finishes — two engine acts through one workspace void both.)'
                             % (path, self.lock_timeout))
                    announced = True
                if time.time() >= deadline:
                    os.close(fd)
                    raise ST.StepError(
                        'BUILD-LOCK HALT: timed out after %ds waiting for lock held by %s. Refusing '
                        'to become a second writer against the shared workspace.'
                        % (self.lock_timeout, holder or '<unknown>'))
                time.sleep(1.0)
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
        # A MODE-QUALIFIED KEY WINS, and an unknown one is a HALT rather than a silent fallback to
        # the step's default fault: a self-test that asked for `ui:stale_mirror`, silently got
        # `skip_second_writer`, and recorded a PASS would be certifying the wrong proof.
        if self.fault not in FAULTS and _mode:
            raise ST.StepError('unknown fault mode %r — txn.FAULTS carries no such key. Known modes '
                               'for step %r: %s' % (self.fault, step_name,
                                                    sorted(k for k in FAULTS
                                                           if k.split(':')[0] == step_name)))
        name, what, injector = FAULTS.get(self.fault) or FAULTS[step_name]
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
    sweep_orphan_sandboxes(ctx.log)
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
            if name == ST.LOCK_HELD_THROUGH and ctx._lock_fd is not None:
                # THE LOCK COVERS THE WRITERS, NOT THE READERS. Everything that builds or depends on
                # a build is behind us; the gates do not write, and the one gate that builds takes
                # the lock itself. Holding it through them would deadlock against that gate, and the
                # variable that would have made it reentrant is not safe to export (see child_env).
                ctx.log('    build-lock: RELEASED after %r — the remaining steps write nothing and '
                        'the one gate that builds takes the lock itself.' % name)
                ctx.release_lock()
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
        _discard_work_dir(ctx, 'the landing completed')
        return Result(True, timings=ctx.timings, facts=ctx.facts, ctx=ctx)

    abort = _abort(ctx, failed_step, err)
    _print_timings(ctx)
    ctx.release_lock()
    if abort.get('byte_exact') in (True, 'n/a'):
        _discard_work_dir(ctx, 'the abort proved every carrier byte-exact')
    else:
        ctx.log('WORK DIR KEPT: %s — the restore point is in it and the abort did not prove '
                'byte-exact.' % ctx.work_dir)
    return Result(False, failed_step=failed_step, error=err, timings=ctx.timings, facts=ctx.facts,
                  abort=abort, ctx=ctx)


#: The sandbox/work dirs this package creates, all named `<prefix><pid>` in the snapshot dir.
SANDBOX_PREFIXES = ('landing_work_', 'landing_selftest_')


def snapshot_root():
    return os.environ.get('LANDING_SNAPSHOT_DIR') or '/tmp'


def sweep_orphan_sandboxes(log=None):
    """REMOVE THE SANDBOXES OF PROCESSES THAT ARE GONE. Returns (count, bytes).

    Every dir this package creates is named `landing_work_<pid>` / `landing_selftest_<pid>`, so an
    orphan is decidable rather than guessed at: if the pid is not alive, nothing can still be using
    the directory. A LIVE pid is left alone, which is the safe direction of the one ambiguity here
    (pid reuse) — the cost of skipping a stale dir is disk, the cost of deleting a live landing's
    restore point is somebody's abort.

    THE END OF THE TRANSACTION CANNOT BE THE ONLY SWEEP. `_discard_work_dir` handles the normal
    close, but a run that is SIGKILLed or SIGTERMed — a timeout, a `kill`, a lost terminal — never
    reaches any finally block, and that is exactly how the box came to hold 138 orphaned dirs and
    1.4GB on 2026-08-21, one of them a self-test sandbox that outlived its killed parent. So the
    sweep runs at the START of a landing and of a self-test, where the wreckage of the LAST run is
    visible and its owner is provably dead.
    """
    root = snapshot_root()
    swept = n = 0
    try:
        names = os.listdir(root)
    except OSError:
        return (0, 0)
    for name in sorted(names):
        pref = next((p for p in SANDBOX_PREFIXES if name.startswith(p)), None)
        if pref is None:
            continue
        tail = name[len(pref):]
        if not tail.isdigit():
            continue
        try:
            os.kill(int(tail), 0)
            continue                          # alive — not ours to remove
        except ProcessLookupError:
            pass                              # dead — an orphan, by construction
        except OSError:
            continue                          # alive but not ours to signal; leave it
        path = os.path.join(root, name)
        size = 0
        for dirpath, _d, files in os.walk(path):
            for f in files:
                try:
                    size += os.lstat(os.path.join(dirpath, f)).st_size
                except OSError:
                    pass
        shutil.rmtree(path, ignore_errors=True)
        if not os.path.exists(path):
            n += 1
            swept += size
    if n and log:
        log('swept %d orphaned sandbox dir(s) from %s (%.1f MB reclaimed) — their owning processes '
            'are gone' % (n, root, swept / 1048576.0))
    return (n, swept)


def _discard_work_dir(ctx, why):
    """THE LANDER CLEANS UP AFTER ITSELF — the /tmp leak, closed.

    The work dir holds the restore point and the build's intermediate boards: ~10MB for a real
    landing, and one per landing PROCESS, which includes each of the self-test's practice landings.
    Nothing removed them. On 2026-08-21 the box carried 138 orphaned `landing_work_*` dirs totalling
    1.4GB, survivors of every landing and self-test run since the package was built, on a disk that
    had to be hand-cleared to 12G to re-fly a landing.

    IT IS REMOVED ONLY WHEN THE RESTORE POINT HAS DONE ITS JOB — the landing completed, or the abort
    proved every carrier byte-exact. If the restore could NOT be proved, the dir is exactly what a
    human needs, and it stays: the failure mode of cleaning up is losing the only copy of the state
    somebody has to put back by hand. `--keep-work` keeps it either way.
    """
    if getattr(ctx, 'keep_work', False):
        ctx.log('WORK DIR KEPT (--keep-work): %s' % ctx.work_dir)
        return
    try:
        shutil.rmtree(ctx.work_dir)
        ctx.log('work dir discarded (%s): %s' % (why, ctx.work_dir))
    except OSError as e:
        ctx.log('could not discard the work dir %s: %s' % (ctx.work_dir, e))


def _rewind_commits(ctx):
    """REWIND EXACTLY THE COMMITS THIS LANDING MADE, AND NEVER ANY OTHER. Runs BEFORE the restore.

    WHY IT EXISTS AT ALL. The lever lander commits once, at the very end, so nothing it could abort
    on had ever been committed. The ROUND lander commits three times — PACKAGE 3a's form puts the
    sheet re-cut in its own commit ahead of the advance, and the owner's score file must be in the
    tree before anything is armed — so for the first time a step can fail with work already
    committed. Restoring the working tree and leaving those commits standing would produce a repo
    that is byte-exact by the abort's own report and two commits ahead by `git log`. That is not an
    abort; it is a half-landing with a certificate.

    IT IS DECIDABLE, NOT CLEVER. The lander knows the sha of every commit it made (`ctx.commits_made`
    from `steps._git_commit`) and the commit it started from (`facts.base.commit`). It rewinds only
    when HEAD IS THE LAST COMMIT THIS LANDING MADE — i.e. nothing else has been committed on top —
    and it rewinds to the recorded base and no further. In any other shape it REFUSES and says so:
    somebody else's commit sits in the range, and a lander that guessed there would be destroying
    work it never wrote.

    `git reset --hard <base>` restores tracked files to the base tree and leaves untracked files
    alone; the carrier restore that follows then covers everything git does not track and everything
    the carrier set knows about. Order matters and is asserted by the caller: rewind, then restore,
    then prove byte-exact.
    """
    if not ctx.commits_made:
        return []
    base = (ctx.facts.get('base') or {}).get('commit')
    rc, head = ctx.run(['git', 'rev-parse', 'HEAD'])
    head = head.strip()
    if rc != 0 or not base:
        ctx.log('CANNOT REWIND: this landing made %d commit(s) and the base commit or HEAD cannot be '
                'read. They are LEFT IN PLACE and named here: %s'
                % (len(ctx.commits_made), ', '.join(c[:12] for c in ctx.commits_made)))
        return {'rewound': False, 'why': 'cannot read HEAD/base', 'commits': list(ctx.commits_made)}
    if head != ctx.commits_made[-1]:
        ctx.log('CANNOT REWIND: HEAD is %s and the last commit this landing made is %s — something '
                'else has been committed on top. This landing\'s commits are LEFT IN PLACE rather '
                'than a range being guessed at: %s'
                % (head[:12], ctx.commits_made[-1][:12],
                   ', '.join(c[:12] for c in ctx.commits_made)))
        return {'rewound': False, 'why': 'HEAD is not this landing\'s last commit',
                'commits': list(ctx.commits_made)}
    ctx.log('REWINDING %d commit(s) this landing made, back to the base %s:'
            % (len(ctx.commits_made), base[:12]))
    for c in ctx.commits_made:
        ctx.log('    %s' % c[:12])
    rc, out = ctx.run(['git', 'reset', '--hard', base])
    if rc != 0:
        ctx.log('THE REWIND FAILED: %s' % out[-500:])
        return {'rewound': False, 'why': out[-300:], 'commits': list(ctx.commits_made)}
    rc, head2 = ctx.run(['git', 'rev-parse', 'HEAD'])
    if head2.strip() != base:
        ctx.log('THE REWIND DID NOT TAKE: HEAD is %s, expected %s' % (head2.strip()[:12], base[:12]))
        return {'rewound': False, 'why': 'HEAD did not return to the base',
                'commits': list(ctx.commits_made)}
    ctx.log('HEAD is back at the base commit %s. History carries no trace of this landing.' % base[:12])
    rewound = list(ctx.commits_made)
    ctx.commits_made = []
    return {'rewound': True, 'to': base, 'commits': rewound}


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
           'byte_exact': None, 'restore_point': None, 'commits_rewound': None}
    out['commits_rewound'] = _rewind_commits(ctx)
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
