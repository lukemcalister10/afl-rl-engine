"""LAND PREFLIGHT — every sub-second check runs BEFORE the lock, the sandbox and the first build.

THE TEN-ATTEMPT LEDGER IS THE SPEC (ORDER 45, register v858). Ten attempts landed one act; the
post-mortem found that SIX of the nine failures were knowable in under a second before launch, and
each of them instead surfaced minutes-to-hours in, mid-transaction, after builds:

    attempt 1  kill_switch.env typed wrong        -> now refused by spec.validate (typed checks)
    attempt 4  act-scoped identities in `moves`   -> now refused by spec.validate (scope partition)
    attempt 6  stale contract identity pins       -> release_contract.py check, HERE, pre-launch
    attempt 7  mirror_parity could not parse      -> acceptance --only m1a, HERE, pre-launch
    attempt 8  movers test's hardcoded count      -> node ui/tests/movers.test.js, HERE, pre-launch
    attempts 2+5  poisoned /home/claude pickles   -> isolation fix (Sandbox.env/Ctx.child_env) +
                                                     the shared-vs-tree md5 NOTE line HERE

DOCTRINE (steps.sheet said it first, for the round lander): "a halt which is knowable before
anything is armed happens before anything is armed." This module is that sentence applied to the
whole battery of cheap checks. Nothing here writes, locks, or builds; every check is a read or a
short subprocess, and the whole pass is seconds. The gates at the END of the transaction still run
— they assert the post-build state; this pass asserts the pre-launch state. Same instruments, both
ends, no third implementation (each check below INVOKES the standing checker, never re-implements
it).

Wired in two places: `land preflight --spec X` standalone, and automatically at the top of
cmd_lever/cmd_round/cmd_edit — before the pre-transaction selftest, which is minutes; a spec or
tree defect should never cost a sandbox build to discover.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

from . import spec as SP


def _md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def _run(argv, root, timeout=300):
    p = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def run_preflight(root, spec_path, out=print):
    """-> (ok, results). results = [(name, verdict, detail, seconds)]; verdicts PASS/FAIL/NOTE/SKIP."""
    results = []
    doc = None

    def check(name, fn):
        t0 = time.time()
        try:
            verdict, detail = fn()
        except Exception as e:                                    # a check that DIES has failed (law 2)
            verdict, detail = 'FAIL', 'raised %r' % (e,)
        results.append((name, verdict, detail, round(time.time() - t0, 2)))
        out('  %-24s %-5s %6.2fs  %s' % (name, verdict, time.time() - t0, detail[:140]))
        return verdict

    out('=' * 102)
    out('PREFLIGHT — the sub-second battery, before the lock, the sandbox and the first build.')
    out('=' * 102)

    # 1 · the spec itself (typed validate: attempts 1 + 4 refused here)
    def _spec():
        nonlocal doc
        doc = SP.load(spec_path)          # raises SpecError listing EVERY problem
        return 'PASS', 'act %r, kind %s, %d moves' % (doc.get('act'), doc.get('act_kind'),
                                                      len((doc.get('identities') or {}).get('moves') or ()))
    if check('spec_validate', _spec) != 'PASS':
        out('the spec is unfit; nothing else is worth measuring against it.')
        return False, results

    # 2 · declared inputs exist
    def _paths():
        missing = []
        pre = doc.get('prereg') or {}
        if pre.get('path') and not os.path.exists(os.path.join(root, pre['path'])):
            missing.append('prereg.path %s' % pre['path'])
        ev = doc.get('evidence_dir')
        if ev:
            parent = os.path.dirname(os.path.join(root, ev).rstrip('/'))
            if not os.path.isdir(parent):
                missing.append('evidence_dir parent %s' % parent)
        return ('FAIL', '; '.join(missing)) if missing else ('PASS', 'prereg + evidence paths resolve')
    check('declared_paths', _paths)

    # 3 · coherent_base resolves (the selftest would otherwise die minutes in)
    def _base():
        base = doc.get('coherent_base')
        if not base:
            return 'SKIP', 'no coherent_base declared (sandbox cuts from HEAD)'
        rc, o = _run(['git', 'rev-parse', '--verify', '%s^{commit}' % base], root)
        return ('PASS', '%s -> %s' % (base, o.strip()[:12])) if rc == 0 else \
               ('FAIL', 'git cannot resolve %r' % base)
    check('coherent_base', _base)

    # 4 · expected_boot pins vs the tree, for every measurable identity declared NOT moving
    #     (attempt 6's stale-pin class, caught pre-launch instead of at the contract step)
    def _pins():
        from . import steps as ST
        exp = json.load(open(os.path.join(root, 'data', 'expected_boot.json')))
        moves = set((doc.get('identities') or {}).get('moves') or ())

        class _C:                                   # the minimal ctx PIN_MEASURERS needs
            pass
        c = _C(); c.root = root
        bad = []
        for k, fn in ST.PIN_MEASURERS.items():
            if k in moves:
                continue                             # it may legitimately differ mid-flip; the pins step owns it
            pin = exp.get(k)
            if pin is None:
                continue
            got = fn(c)
            if str(got)[:8] != str(pin)[:8]:
                bad.append('%s: tree %s != pin %s' % (k, str(got)[:8], str(pin)[:8]))
        return ('FAIL', '; '.join(bad)) if bad else ('PASS', '%d unmoved pins == tree' %
                                                     (len(ST.PIN_MEASURERS) - len(moves & set(ST.PIN_MEASURERS))))
    check('pins_vs_tree', _pins)

    # 5 · the contract checker (attempt 6's own instrument, invoked not re-implemented)
    def _contract():
        rc, o = _run([sys.executable, 'release_contract.py', 'check'], root)
        return ('PASS', 'release_contract check PASS') if rc == 0 and 'PASS' in o else \
               ('FAIL', o.strip().splitlines()[-1][:200] if o.strip() else 'exit %s' % rc)
    check('release_contract', _contract)

    # 6 · the manifest lag checker
    def _manifest():
        rc, o = _run([sys.executable, 'release_manifest_check.py'], root)
        return ('PASS', 'release_manifest_check PASS') if rc == 0 and 'PASS' in o else \
               ('FAIL', o.strip().splitlines()[-1][:200] if o.strip() else 'exit %s' % rc)
    check('release_manifest', _manifest)

    # 7 · mirror parity (attempt 7: the parity check must be able to PARSE both resolver sides —
    #     a source refactor that defeats the parser is discovered here, not at gate time)
    def _mirror():
        # --only takes CHECK names; mirror_parity is the parse+pin half of m1a. Its module sibling
        # build_twice_determinism is ~3.5 min of engine and is exactly what this pass must NOT run.
        rc, o = _run([sys.executable, '-m', 'acceptance.runner', '--only', 'mirror_parity'], root)
        return ('PASS', 'acceptance mirror_parity GREEN') if rc == 0 else \
               ('FAIL', o.strip().splitlines()[-1][:200] if o.strip() else 'exit %s' % rc)
    check('mirror_parity', _mirror)

    # 8 · the ui movers tests (attempt 8: the boundary count lives here; a count the act will bump
    #     must be bumped IN the act's own tree before launch, per that test's own convention)
    def _movers():
        rc, o = _run(['node', 'ui/tests/movers.test.js'], root)
        return ('PASS', 'movers.test.js green') if rc == 0 else \
               ('FAIL', ([l for l in o.splitlines() if 'FAIL' in l] or [o.strip()[:200]])[0][:200])
    check('movers_ui', _movers)

    # 8a · THE PROOF STASH'S OWN TESTS (shrink S8, 2026-08-29). The stash is the one instrument whose
    #      purpose is to NOT run the thing it stands in for, and the lander selftest deliberately
    #      disables it — so nothing else in the estate proves its decision boundary. If it is going to
    #      be trusted to skip a 36-minute rebuild in the next few minutes, its own 23 assertions cost
    #      a fraction of a second here.
    def _stash():
        rc, o = _run([sys.executable, 'tools/landing/test_proofstash.py'], root)
        return ('PASS', 'proof-stash tests green') if rc == 0 else \
               ('FAIL', ([l for l in o.splitlines() if 'FAIL' in l] or [o.strip()[:200]])[0][:200])
    check('proof_stash', _stash)

    # 8b · EVERY IDENTITY STAMP AGAINST THE TREE (shrink S6, 2026-08-30). The contract step already
    #      refuses if a carrier disagrees, but it runs deep inside the transaction, after the build.
    #      The ORDER 49 flip left five stamps behind and each was found by a gate run costing
    #      minutes; the same divergence is visible here, before the lock, in well under a second.
    def _restamp():
        rc, o = _run([sys.executable, 'tools/restamp.py', 'check'], root)
        if rc == 0:
            return ('PASS', ([l for l in o.splitlines() if l.startswith('RESTAMP:')] or ['stamps agree'])[-1][9:].strip())
        return ('FAIL', ([l.strip() for l in o.splitlines() if 'STALE' in l or 'VACUOUS' in l]
                         or [o.strip()[:200]])[0][:200])
    check('identity_stamps', _restamp)

    # 8c · THE STORE'S CONTENT, not its identity (2026-08-30). Every other guard in the estate
    #      asserts the store's md5; none of them reads what the numbers say, so an impossible row
    #      hashes green forever. jesse-joyce carried 61/60/60 games for 2017-2019 from the initial
    #      seed onward, through owner corrections that never reached the store. Milliseconds here.
    def _store_sanity():
        rc, o = _run([sys.executable, 'tools/store_sanity.py'], root)
        if rc == 0:
            return ('PASS', ([l.strip() for l in o.splitlines() if 'PASS' in l] or ['store rows sane'])[0][:120])
        return ('FAIL', ([l.strip() for l in o.splitlines() if 'IMPOSSIBLE' in l] or [o.strip()[:200]])[0][:200])
    check('store_sanity', _store_sanity)

    # 8d · THE SURGICAL EDITOR'S OWN REFUSALS (2026-08-30). The season path reaches INSIDE a
    #      container the editor had until now refused to touch, and a narrower target is one that
    #      can be missed. Its 14 assertions are almost all refusals; they cost milliseconds.
    def _store_edit():
        rc, o = _run([sys.executable, 'tools/landing/test_store_edit.py'], root)
        return ('PASS', 'store-edit season-path tests green') if rc == 0 else \
               ('FAIL', ([l for l in o.splitlines() if 'FAIL' in l] or [o.strip()[:200]])[0][:200])
    check('store_edit_paths', _store_edit)

    # 8b · CLEAN TREE, before the selftest instead of after it (shrink review S11, 2026-08-28).
    #      Step 0 asserts this too — but step 0 runs after the pre-transaction selftest (minutes),
    #      and two takes of the combined-build landing paid that price to discover dirt knowable
    #      here in milliseconds. Same law, earlier door. Declared act inputs and the act's own
    #      evidence/claims/spec paths are the only permitted dirt (txn.declared_dirt's classes).
    def _clean():
        rc, o = _run(['git', 'status', '--porcelain'], root)
        if rc != 0:
            return ('FAIL', 'git status failed')
        d = doc or {}
        allowed = [p for p in (d.get('evidence_dir'), d.get('claims_file')) if p]
        allowed.append(os.path.relpath(os.path.abspath(spec_path), root))
        sheet = (d.get('sheet') or {}) if isinstance(d.get('sheet'), dict) else {}
        rnd = (d.get('round') or {}) if isinstance(d.get('round'), dict) else {}
        for p in (sheet.get('path'), sheet.get('declaration'), sheet.get('prereg'),
                  (rnd.get('scores') or {}).get('path') if isinstance(rnd.get('scores'), dict) else None,
                  'engine/rl_after/ingestion/catchup_identity_overrides.json' if rnd else None):
            if p:
                allowed.append(p)
        foreign = []
        for ln in o.splitlines():
            if not ln.strip():
                continue
            rel = ln[3:].strip().strip('"').split(' -> ')[-1]
            if not any(rel == a or rel.startswith(a.rstrip('/') + '/') for a in allowed):
                foreign.append(rel)
        return ('FAIL', 'undeclared dirt (step 0 would refuse after the selftest): %s'
                % ', '.join(foreign[:6])) if foreign else ('PASS', 'tree clean up to declared inputs')
    check('clean_tree', _clean)

    # 8c · the picks/curve halt battery, read-only (S11; the take-8 class: a stale curve-mirror or
    #      contract pin died at ui writer 5, ~55 build-minutes in — the same standing checker runs
    #      here in --clubs-check mode, which writes NOTHING and fires every coherence halt).
    def _picks():
        rc, o = _run([sys.executable, 'ui/tools/ingest_inputs.py', '--clubs-check'], root)
        return ('PASS', 'picks/curve halt battery clean (read-only)') if rc == 0 else \
               ('FAIL', ([l for l in o.splitlines() if 'HALT' in l or 'DRIFT' in l] or
                         [o.strip()[:200]])[0][:200])
    check('picks_curve', _picks)

    # 8d · the py movers suite (S11; it was the one cheap landing gate absent from this battery —
    #      its js twin has run here since ORDER 45).
    def _movers_py():
        rc, o = _run([sys.executable, 'engine/rl_after/ingestion/test_movers_transition.py'], root)
        return ('PASS', 'test_movers_transition.py green') if rc == 0 else \
               ('FAIL', ([l for l in o.splitlines() if 'FAIL' in l] or [o.strip()[:200]])[0][:200])
    check('movers_py', _movers_py)

    # 9 · shared pickles vs this tree (attempts 2+5 — isolation makes this non-fatal, so it is a
    #     NOTE, but a mismatch means some other tree bootstrapped last; say so before launching)
    def _pickles():
        diffs = []
        for name in ('cm_400.pkl', 'q97m.pkl'):
            shared, mine = '/home/claude/%s' % name, os.path.join(root, 'data', name)
            if os.path.exists(shared) and os.path.exists(mine) and _md5(shared) != _md5(mine):
                diffs.append(name)
        return ('NOTE', 'SHARED /home/claude %s differ from this tree — harmless post-isolation '
                        '(children read the tree copies), but another tree bootstrapped last'
                        % '+'.join(diffs)) if diffs else ('PASS', 'shared pickles == tree pickles')
    check('shared_pickles', _pickles)

    # 10 · the lock is free (the transaction takes it; a held lock means a wait or a stale holder)
    def _lock():
        rc, o = _run(['bash', 'tools/build_lock.sh', 'status'], root)
        line = o.strip().splitlines()[-1] if o.strip() else ''
        return ('PASS', line[:160]) if 'FREE' in line else ('NOTE', line[:160] or 'status unknown')
    check('build_lock', _lock)

    failed = [r for r in results if r[1] == 'FAIL']
    out('-' * 102)
    out('PREFLIGHT %s — %d checks, %d failed, %.1fs total.  (Attempts 3+9 died to PLATFORM '
        'RECLAIMS: arm the keep-alive chain before any launch longer than minutes.)'
        % ('FAILED' if failed else 'CLEAN', len(results), len(failed),
           sum(r[3] for r in results)))
    out('=' * 102)
    return not failed, results


def file_evidence(results, evidence_dir):
    """Write the preflight table into the act's evidence dir (best-effort; preflight never blocks
    on its own paperwork).

    THE RECORD IS DETERMINISTIC — VERDICTS AND DETAILS, NEVER TIMINGS (2026-08-27, the combined
    build's step-0 catch): this file lives in the TRACKED evidence dir and is rewritten by every
    launch BEFORE the transaction's step-0 clean-tree law reads the tree. With per-run `seconds`
    in the file, a re-launch of an already-recorded act dirtied its own tree by timing jitter
    alone and step 0 aborted the landing the preflight had just cleared — measured live, twice.
    Timings stay on stdout (the M2 measure-then-quote surface); the FILE carries what the record
    is FOR: which checks ran and what they said. A re-run with identical verdicts is now
    byte-identical and the tree stays clean."""
    try:
        os.makedirs(evidence_dir, exist_ok=True)
        p = os.path.join(evidence_dir, 'PREFLIGHT.json')
        body = json.dumps([{'check': n, 'verdict': v, 'detail': d} for n, v, d, _s in results],
                          indent=1)
        if os.path.exists(p) and open(p).read() == body:
            return p
        open(p, 'w').write(body)
        return p
    except OSError:
        return None
