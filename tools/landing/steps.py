"""tools/landing/steps.py — THE ELEVEN STEPS, IN THE DAY'S PROVEN ORDER.

Every step here is a CONSOLIDATION of a script that already ran and already landed a board on
2026-08-20. The provenance of each is named in its own docstring, and the rule throughout is the one
the per-act scripts stated for themselves:

    EVERY VALUE IS COMPUTED HERE, IN THIS PROCESS, FROM THE TREE — NEVER TYPED IN FROM THE BRIEF.

The only values that arrive from outside are PREDICTIONS (the prereg's board), CITATIONS (the owner
word, the lineage authority) and POLICY (which identities this act is allowed to move). Those are
the three things a tree cannot measure about itself, and they are exactly what the act spec carries.

WHAT THE STEPS SHARE WITH THE ROUND LANDER (2b). `preflight`, `contract`, `sibling`, `ui`, `state`,
`gates`, `claims` and `commit` are act-kind agnostic: 2b registers the same functions in its own sequence and
adds `scores`, `catchup` and `advance_repin` beside them. `build_proofs`, `pins` and `lineage` read
`spec['act_kind']` where the two kinds genuinely differ (a round advance moves the store and the
round; a lever landing must not). That is why they are parameterised rather than duplicated.
"""

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time


class StepError(RuntimeError):
    """A step could not prove its own postcondition. The driver aborts on it. Always fail-closed."""


# --------------------------------------------------------------------------------------- helpers
def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _p(ctx, *a):
    return os.path.join(ctx.root, *a)


def _load(ctx, name, rel):
    """Import a module BY PATH FROM THE TREE BEING LANDED, under a root-unique module name.

    The unique name matters: the self-test drives sandboxes and the live tree from processes that
    may share an interpreter, and a cached `config_manifest` from the wrong root is a silent
    cross-tree read — the exact class of defect the mirror-parity check exists to catch.
    """
    key = '%s__%s' % (name, hashlib.md5(ctx.root.encode()).hexdigest()[:8])
    if key in sys.modules:
        return sys.modules[key]
    path = _p(ctx, rel)
    if not os.path.isfile(path):
        raise StepError('the tree at %s has no %s' % (ctx.root, rel))
    spec = importlib.util.spec_from_file_location(key, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    for extra in (ctx.root, _p(ctx, 'engine', 'rl_after'), _p(ctx, 'engine', 'rl_after', 'ingestion')):
        if extra not in sys.path:
            sys.path.insert(0, extra)
    spec.loader.exec_module(mod)
    return mod


#: Identities the PINS step may write into data/expected_boot.json, each measured from the tree.
PIN_MEASURERS = {
    'board':       lambda ctx: md5(_p(ctx, 'data', 'rl_build', 'rl_app_data.json')),
    'store':       lambda ctx: md5(_p(ctx, 'engine', 'rl_after', 'rl_model_data.json')),
    'engine_head': lambda ctx: md5(_p(ctx, 'engine', 'rl_after', '_merged_recover.py')),
    'rl_model':    lambda ctx: md5(_p(ctx, 'engine', 'rl_after', 'rl_model.py')),
    'register':    lambda ctx: md5(_p(ctx, 'LTI_REGISTER.md')),
    'v0surf':      lambda ctx: md5(_p(ctx, 'data', 'v0surf.pkl')),
    'config':      lambda ctx: _load(ctx, 'config_manifest', 'config_manifest.py')
                                   .manifest_hash(ctx.root),
    'fv':          lambda ctx: (lambda m: m.fv_identity(m.checkout_fv_dir(ctx.root)))(
                                   _load(ctx, 'fv_provenance', 'fv_provenance.py')),
}

#: Identities that ARE tracked but belong to another writer of record. Declaring one in
#: `identities.moves` is legal; the pins step refuses to write it and says who does.
DELEGATED_PINS = {
    'balanced_board_md5': 'engine/rl_after/ingestion/sibling_repin.py (the sibling step)',
    'as_of_round': 'the round lander (2b); a lever landing HOLDS the round',
    'season_state': 'the round lander (2b)',
    'rl_model_data': 'the round lander (2b) — the store is written by a score application',
}

#: The standing landing gate set. Each is run and its verdict read off the exit code — never taken
#: on trust, never parsed for a hopeful word.
#:
#: `@EVIDENCE@` in an argv is replaced at run time by a per-gate directory INSIDE this landing's
#: evidence dir. A gate that can write its own per-check raw output is pointed at it, so a gate
#: failure is diagnosable from the landing's evidence alone (F-5). The first A-raw attempt ran the
#: acceptance runner with `evidence: (none)` and the r14 failure arrived as a 110-character truncated
#: reason string with the actual suite output nowhere on disk. One flag, one whole class of blind
#: abort removed.
DEFAULT_GATES = (
    {'name': 'release_manifest_check', 'argv': ['python3', 'release_manifest_check.py'],
     'must_contain': 'PASS'},
    {'name': 'release_contract_check', 'argv': ['python3', 'release_contract.py', 'check'],
     'must_contain': 'PASS'},
    {'name': 'acceptance_runner',
     'argv': ['python3', '-m', 'acceptance.runner',
              '--profile', 'in-transaction', '--evidence', '@EVIDENCE@'],
     'must_contain': 'GREEN'},
    {'name': 'movers_transition', 'argv': ['python3', 'engine/rl_after/ingestion/test_movers_transition.py']},
    {'name': 'movers_ui', 'argv': ['node', 'ui/tests/movers.test.js']},
)


def is_no_op(spec):
    """A declared rehearsal: the act predicts the board it already has and moves no identity."""
    pre = spec.get('prereg') or {}
    return (not (spec.get('identities') or {}).get('moves')
            and pre.get('board_before') and pre.get('board_before') == pre.get('board_after'))


# ============================================================================== STEP 0 — PREFLIGHT
def preflight(ctx):
    """Clean tree, the build lock, and the RESTORE POINT — in that order, and the order is the point.

    The restore point must be a CLEAN tree or it restores somebody else's half-finished work. So the
    cleanliness assertion runs FIRST, the lock second (nothing may write between the assertion and
    the capture), and the snapshot last. A failure here therefore precedes the restore point, and
    the driver says so rather than claiming an abort it did not perform.
    """
    ctx.fault_point('preflight')
    rc, out = ctx.run(['git', 'status', '--porcelain'])
    if rc != 0:
        raise StepError('git status failed in %s: %s' % (ctx.root, out))
    declared_dirt = ctx.declared_dirt() if hasattr(ctx, 'declared_dirt') else ()
    if declared_dirt:
        # WHAT THE LANDER COMMITS IS WHAT THE LANDER EXPECTS UNCOMMITTED. The owner's inputs of
        # record — the score file and the identity-override record — are placed by the SEAT and
        # committed by `catchup_preflight`; a declared sheet re-cut and its prereg-lite are written
        # by the SEAT and committed by `sheet`. Every one is enumerated and printed here; nothing is
        # waved through. (R24 rehearsal §3.1 — the input-commit pincer.)
        ctx.log('DECLARED DIRT (%d path(s), and ONLY these): owner inputs this act is contracted to '
                'COMMIT ITSELF, and which are therefore expected uncommitted at step 0:'
                % len(declared_dirt))
        for p in declared_dirt:
            ctx.log('    %-58s (committed by the `%s` step)'
                    % (p, 'catchup_preflight'
                       if p in ((((ctx.spec.get('round') or {}).get('scores') or {}).get('path'),
                                 CATCHUP_OVERRIDES_REL)) else 'sheet'))
    dirty = [ln for ln in out.splitlines() if ln.strip() and not ctx.is_ignorable_dirt(ln)]
    if dirty:
        raise StepError('THE TREE IS NOT CLEAN. A landing transaction starts from a committed tree, '
                        'or its abort restores a state nobody chose:\n    ' + '\n    '.join(dirty))
    rc, head = ctx.run(['git', 'rev-parse', 'HEAD'])
    if rc != 0:
        raise StepError('cannot read HEAD in %s' % ctx.root)
    base_commit = head.strip()

    # THE RL_-PREFIXED ENVIRONMENT, PRINTED. Every one of these is inherited by every probe and gate
    # child this landing spawns, and `config_manifest.enforce()` treats an unknown one as a divergent
    # model override — which does not always halt loudly; it can instead make an unrelated probe fail
    # a DIFFERENT way, which is how this package's own `RL_LANDING_SNAPSHOT_DIR` red a landing at the
    # ruled-red ledger. It is printed rather than halted on, because RL_REPO and RL_VENV are
    # legitimately present; a seat reading an unexplained gate red should see this line first.
    rl_env = sorted(k for k in os.environ if k.startswith('RL_') or k.startswith('PAR_'))
    ctx.log('RL_/PAR_ environment  %s' % (', '.join(rl_env) or '(none)'))

    ctx.acquire_lock()

    snap = ctx.capture_restore_point()
    boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))
    ctx.facts['base'] = {
        'commit': base_commit,
        'expected_boot': {k: boot.get(k) for k in sorted(boot) if not k.startswith('_')},
        'carriers': snap.identities(),
    }
    ctx.log('base commit        %s' % base_commit)
    ctx.log('board pin (before) %s' % boot.get('board'))
    ctx.log('store pin (before) %s' % boot.get('store'))
    ctx.log('restore point      %d carrier(s) captured, %d present on disk'
            % (len(snap.entries), len(snap.present())))
    return {'base_commit': base_commit, 'carriers_captured': len(snap.entries),
            'lock': ctx.lock_tag, 'board_before': boot.get('board')}


# =========================================================================== STEP 1 — BUILD+PROOFS
def build_proofs(ctx):
    """The bare build, the predicted identity, the kill-switch leg, the byte-diff against a reference.

    Consolidates `d8_build.py` / `br_build.py` / the F5 seat's build driver, all three of which are
    the same file with a different env prefix, plus the assertions their `0*_builds.txt` captures
    recorded by hand afterwards. The assertion the prereg made is now made BY the program, before
    anything is pinned.

    THE BUILD IS A CHILD PROCESS with RL_BUILD_LOCK_HELD dropped from its environment — the lock is
    still held by this process's fd. That is not a nicety: `config_manifest.enforce()` rejects any
    unknown RL_-prefixed variable as a model override, so a canonical-mode build launched from
    inside the lock HALTS. The estate has burned this twice; it is written down here as code.
    """
    ctx.fault_point('build_proofs')
    pre = ctx.spec['prereg']
    predicted = pre['board_after']

    res = ctx.builder.build(ctx, tag='LANDING', mode='dev')
    ctx.log('build         rc=%s board=%s  (%.1fs)' % (res['rc'], res['board_md5'], res['elapsed_s']))
    if res['rc'] != 0:
        raise StepError('the bare build failed (rc=%s). See %s' % (res['rc'], res.get('stdout_path')))
    if res['board_md5'] != predicted:
        raise StepError(
            'THE BUILD DID NOT REPRODUCE THE PREREG PREDICTION.\n'
            '    predicted (prereg %s): %s\n    built                 : %s\n'
            'The prediction is an INPUT to this lander. A landing that accepted its own build as the '
            'answer would assert nothing at all.' % (pre.get('path'), predicted, res['board_md5']))
    ctx.log('PREDICTED BOARD MET: %s == prereg %s' % (res['board_md5'], pre.get('path')))

    facts = {'board_built': res['board_md5'], 'build_elapsed_s': res['elapsed_s'],
             'predicted_board': predicted, 'kill_switch': None, 'reference_board': None,
             'day0_rebase': 'off'}

    # ---- the reference arm, where one exists ----------------------------------------------------
    ref = pre.get('reference_board')
    if ref:
        rp = _p(ctx, ref) if os.path.sep in str(ref) or str(ref).endswith('.json') else None
        if rp and os.path.isfile(rp):
            got = md5(rp)
            if got != res['board_md5']:
                raise StepError('the reference board %s (%s) is not byte-identical to this build (%s)'
                                % (ref, got, res['board_md5']))
            facts['reference_board'] = 'byte-identical to %s' % ref
            ctx.log('reference arm : %s BYTE-IDENTICAL' % ref)
        else:
            if str(ref) != res['board_md5']:
                raise StepError('the declared reference board %s != this build %s'
                                % (ref, res['board_md5']))
            facts['reference_board'] = str(ref)
            ctx.log('reference arm : %s == this build' % ref)

    # ---- the kill-switch leg, when the act declares a switch -------------------------------------
    ks = pre.get('kill_switch')
    if ks:
        off = ctx.builder.build(ctx, tag='SWITCH_OFF', mode='dev', env_overrides=ks['env'])
        ctx.log('switch-off    rc=%s board=%s  (%.1fs)' % (off['rc'], off['board_md5'], off['elapsed_s']))
        if off['rc'] != 0:
            raise StepError('the kill-switch build failed (rc=%s)' % off['rc'])
        if off['board_md5'] != ks['board_with_switch_off']:
            raise StepError('the switch-OFF build produced %s, not the declared %s — the switch does '
                            'not do what the act says it does'
                            % (off['board_md5'], ks['board_with_switch_off']))
        if off['board_md5'] == res['board_md5']:
            raise StepError('the switch-OFF board equals the switch-ON board. A dial that changes '
                            'nothing is either dead or silently deleted, and this is the positive '
                            'control that says so.')
        facts['kill_switch'] = {'name': ks['name'], 'board_off': off['board_md5']}

    # ---- DAY-0 RE-BASING: EXPLICIT, OFF BY DEFAULT, WITH A PRINTED ROW DIFF (M1b / A-F6) ---------
    facts['day0_rebase'] = _day0(ctx)

    # ---- install the board and its sidecars, together (the bake precedent) -----------------------
    if not ctx.opts.dry_run:
        _install_board(ctx, res)
    facts['installed'] = not ctx.opts.dry_run
    return facts


def _day0(ctx):
    """Day-0 re-basing. OFF unless the spec says otherwise AND names the owner word that says so.

    THE RULING, folded in verbatim from MODERNISATION_PROGRAMME M1b: "Day-0 re-basing becomes an
    explicit, owner-visible, off-by-default input with a mandatory printed diff of every moved row —
    a suite inheriting the capability without the judgement re-bases itself green on the first halt."

    THE LANDER DOES NOT COMPUTE DAY-0. It prints the diff between the standing reference and the new
    one the act's own emitter produced, and installs the new one only when the re-base is activated.
    Computing the day-0 law here would create a second implementation of it beside the byte-carried
    emitter — the mirrored-pair hazard M1b itself warns about.
    """
    d0 = ctx.spec.get('day0_rebase') or {'state': 'off'}
    state = str(d0.get('state', 'off')).lower()
    if state != 'on':
        ctx.log('day-0 re-base : OFF (default). No day-0 reference is regenerated by this landing.')
        return 'off'
    old_p, new_p = _p(ctx, d0['reference']), _p(ctx, d0['new_reference'])
    for p in (old_p, new_p):
        if not os.path.isfile(p):
            raise StepError('day-0 re-base is ACTIVATED and %s does not exist' % p)
    old_rows = {r['key']: r.get('printed') for r in json.load(open(old_p, encoding='utf-8'))['rows']}
    new_rows = {r['key']: r.get('printed') for r in json.load(open(new_p, encoding='utf-8'))['rows']}
    moved = [(k, old_rows.get(k), new_rows.get(k))
             for k in sorted(set(old_rows) | set(new_rows))
             if old_rows.get(k) != new_rows.get(k)]
    ctx.log('day-0 re-base : ACTIVATED by %r' % d0.get('activated_by'))
    ctx.log('   %s -> %s' % (d0['reference'], d0['new_reference']))
    ctx.log('   THE MANDATORY ROW DIFF — every moved row, printed, %d of %d:'
            % (len(moved), len(set(old_rows) | set(new_rows))))
    for k, a, b in moved:
        ctx.log('     %-34s %s -> %s' % (k, a, b))
    if not moved:
        raise StepError('day-0 re-base is ACTIVATED and NO row moves. An activated re-base that '
                        'changes nothing is a re-base nobody needed to authorise; refusing.')
    if not ctx.opts.dry_run:
        with open(new_p, 'rb') as s, open(old_p, 'wb') as d:
            d.write(s.read())
    return {'state': 'on', 'activated_by': d0.get('activated_by'), 'rows_moved': len(moved),
            'reference': d0['reference']}


def _install_board(ctx, res):
    """The board + BOTH sidecars + the generator-side copy, installed as ONE lockstep.

    `land_a_pins.py` (D8) moved four files here and named the reason: Guard 5 asserts the published
    copy, the bake moved the generator copy, and the sidecars are written BY the build rather than
    hand-composed. Installing three of the four is the shape of a landing that passes its own gates
    and fails somebody else's.
    """
    src_board, src_sc = res['board_path'], res.get('sidecar_path')
    if not src_sc or not os.path.isfile(src_sc):
        raise StepError('the build produced no .srcmd5 sidecar beside its board. The sidecar is '
                        'written BY the build; a hand-composed one is not the same artifact.')
    for dst in (_p(ctx, 'data', 'rl_build', 'rl_app_data.json'),
                _p(ctx, 'engine', 'rl_after', 'rl_app_data.json')):
        with open(src_board, 'rb') as s, open(dst, 'wb') as d:
            d.write(s.read())
        with open(src_sc, 'rb') as s, open(dst + '.srcmd5', 'wb') as d:
            d.write(s.read())
    ctx.log('installed     board + both sidecars + the generator copy (4 files, lockstep)')


# ================================================================================== STEP 2 — PINS
def pins(ctx):
    """`data/expected_boot.json` — the pins that move, computed from the tree, replaced surgically.

    Carried from `land_f5_pins.py` / `land_a_pins.py`, including the three assertions that make it a
    landing instrument rather than a JSON edit:

      * the published board, the generator copy and BOTH sidecars are proved coherent BEFORE the pin
        moves (and the sidecars are checked against the LIVE STORE, not against each other);
      * the replacement is textual and the old value must occur EXACTLY ONCE — json.load/json.dump
        never touch the file, so every note field, key order and byte of whitespace survives;
      * the set of fields that moved is asserted EQUAL to the declared set. Not a subset.
    """
    ctx.fault_point('pins')
    pin_path = _p(ctx, 'data', 'expected_boot.json')
    raw = open(pin_path, encoding='utf-8').read()
    before = json.loads(raw)

    pub = md5(_p(ctx, 'data', 'rl_build', 'rl_app_data.json'))
    gen = md5(_p(ctx, 'engine', 'rl_after', 'rl_app_data.json'))
    built = ctx.facts['build_proofs']['board_built']
    ctx.log('published board  %s' % pub)
    ctx.log('generator board  %s' % gen)
    if pub != built:
        raise StepError('the published board %s is not the board this landing built (%s)' % (pub, built))
    if gen != pub:
        raise StepError('the generator copy %s != the published copy %s' % (gen, pub))
    store_md5 = md5(_p(ctx, 'engine', 'rl_after', 'rl_model_data.json'))
    for rel in ('data/rl_build/rl_app_data.json.srcmd5', 'engine/rl_after/rl_app_data.json.srcmd5'):
        sc = json.load(open(_p(ctx, rel), encoding='utf-8'))
        if sc.get('own_md5') != pub or sc.get('source_md5') != store_md5:
            raise StepError('sidecar %s disagrees with the board it sits beside or with the live '
                            'store (own_md5=%s source_md5=%s; board=%s store=%s)'
                            % (rel, sc.get('own_md5'), sc.get('source_md5'), pub, store_md5))
    ctx.log('both sidecars agree with the board beside them and with the live store. OK.')

    declared = list((ctx.spec['identities'].get('moves') or ()))
    unmoved = list((ctx.spec['identities'].get('unmoved') or ()))
    writable = [k for k in declared if k in PIN_MEASURERS]
    for k in declared:
        if k in DELEGATED_PINS:
            ctx.log('delegated     %-20s is written by %s, not here' % (k, DELEGATED_PINS[k]))

    new_raw, moved_here = raw, []
    for k in writable:
        new_val = PIN_MEASURERS[k](ctx)
        old_val = before.get(k)
        ctx.log('COMPUTED from the tree (never typed): %-12s = %s' % (k, new_val))
        if old_val == new_val:
            raise StepError('%r is DECLARED MOVING and the tree says it did not move (still %s). '
                            'The prereg and the tree disagree; the tree wins and this halts.'
                            % (k, new_val))
        n = new_raw.count(str(old_val))
        ctx.log('  expected_boot %-12s %s -> %s   (old value occurs %d time(s))'
                % (k, str(old_val)[:12], str(new_val)[:12], n))
        if n != 1:
            raise StepError('the old %s value occurs %d times in expected_boot.json; refusing a '
                            'non-unique textual replacement' % (k, n))
        new_raw = new_raw.replace(str(old_val), str(new_val))
        moved_here.append(k)

    after = json.loads(new_raw)
    for k in unmoved:
        if k in PIN_MEASURERS and k in before:
            measured = PIN_MEASURERS[k](ctx)
            if str(measured) != str(before.get(k)):
                raise StepError('%r is declared UNMOVED and the tree measures %s against a pin of %s'
                                % (k, measured, before.get(k)))
    bad = [k for k in unmoved if before.get(k) != after.get(k)]
    if bad:
        raise StepError('these are declared unmoved and the pin file moved them: %s' % bad)
    moved = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    if moved != sorted(moved_here):
        raise StepError('expected exactly %s to move in expected_boot.json, got %s'
                        % (sorted(moved_here), moved))
    ctx.log('fields that moved in expected_boot.json: %s' % moved)
    ctx.log('must-not-move list: %d checked, 0 moved' % len(unmoved))

    if moved_here:
        rev = new_raw
        for k in moved_here:
            rev = rev.replace(str(after.get(k)), str(before.get(k)))
        if rev != raw:
            raise StepError('bytes beyond the declared pin values changed')
        ctx.log('byte check: the ONLY bytes that differ are the declared pin values.')
    else:
        ctx.log('NO PIN MOVES — this act is a declared no-op rehearsal; expected_boot is untouched.')

    if not ctx.opts.dry_run and moved_here:
        tmp = pin_path + '.landing_tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            fh.write(new_raw)
        os.replace(tmp, pin_path)
        back = json.load(open(pin_path, encoding='utf-8'))
        for k in moved_here:
            if back.get(k) != after.get(k):
                raise StepError('the %s pin did not take' % k)
        for k in unmoved:
            if back.get(k) != before.get(k):
                raise StepError('%r moved on re-read' % k)
        ctx.log('WRITTEN and re-read.')
    return {'moved': moved_here, 'board': pub, 'store': store_md5,
            'unmoved_checked': len(unmoved)}


# =============================================================================== STEP 3 — LINEAGE
def lineage(ctx):
    """The out-of-round history column and the append-only transition entry.

    Two writers of record, both carried:
      * `out_of_round_column.add_column` — the standing owner rule of 2026-07-28: whenever the board
        moves OUTSIDE a round, write a column at that point. It is also what keeps the movers lineage
        honest, because `ui/app/movers.js` requires the NEWEST STORED POINT to be the board the app
        is serving.
      * the append-only register in `data/release_lineage.json`, with the chain assertion in the form
        `append_f5_transition.py` proved correct after its first draft halted: the register records
        OUT-OF-ROUND transitions only, so a gap is legitimate when a SINGLE movers round report
        bridges BOTH legs (board AND store). A gap an independent record can close is a gap; one
        nothing can close is a broken chain, and this halts on it.

    THE IDENTITIES ARE MEASURED, NOT TYPED. `source` is re-hashed from the BASE COMMIT's tree via
    `git show`, `destination` from the live tree — which retires `lineage_measured.json` and the
    `measure_lineage.py` that had to be written for each act.
    """
    ctx.fault_point('lineage')
    spec = ctx.spec
    out = {'column': None, 'entry': None}
    board_moved = 'board' in (ctx.facts.get('pins') or {}).get('moved', [])

    if spec.get('column') and board_moved:
        out['column'] = _column(ctx)
    elif spec.get('column'):
        raise StepError('a column is declared and the board did not move out of round. A column '
                        'marks a point in the histories; there is no point to mark.')
    else:
        ctx.log('no column declared%s' % ('' if not board_moved else
                                          ' — and the board MOVED, which the spec validator refuses'))

    if spec.get('lineage') and board_moved:
        out['entry'] = _append_transition(ctx)
    else:
        ctx.log('no lineage entry owed (board unmoved out of round).')
    return out


def _column(ctx):
    col = ctx.spec['column']
    ooc = _load(ctx, 'out_of_round_column', 'engine/rl_after/ingestion/out_of_round_column.py')
    bp = _p(ctx, 'data', 'rl_build', 'rl_app_data.json')
    board_md5 = md5(bp)
    board = json.load(open(bp, encoding='utf-8'))
    ev = ooc.add_column(ctx.root, column_id=col['id'], label=col['label'],
                        after_round=int(col['after_round']), board=board, board_md5=board_md5,
                        dry_run=ctx.opts.dry_run, registered_at=col.get('registered_at')
                        or ctx.spec.get('date'))
    ctx.log('column        %s registered (dry_run=%s)' % (col['id'], ctx.opts.dry_run))
    if not ctx.opts.dry_run:
        vh = json.load(open(_p(ctx, 'engine/rl_after/ingestion/value_history.json'), encoding='utf-8'))
        pts = ooc.selectable_points(vh)
        last = pts[-1]
        if last['id'] != col['id']:
            raise StepError('the newest stored point is %r, not this column. The movers lineage '
                            'would not name the board the app is serving.' % last['id'])
        if last['board'] != board_md5:
            raise StepError('the newest stored point names board %s, not the live board %s'
                            % (last['board'], board_md5))
        ctx.log('ASSERTED: the newest stored point is this column, naming the live board %s' % board_md5)
    return {'id': col['id'], 'board': board_md5, 'event': ev.get('id') if isinstance(ev, dict) else None}


def _git_show_md5(ctx, commit, rel):
    p = subprocess.run(['git', 'show', '%s:%s' % (commit, rel)], cwd=ctx.root,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise StepError('cannot read %s at %s: %s' % (rel, commit, p.stderr.decode()[-300:]))
    return hashlib.md5(p.stdout).hexdigest()


def _measure_sides(ctx):
    """source = the base commit's tree, destination = the live tree. Both re-hashed, never typed."""
    base = ctx.facts['base']['commit']
    files = {'board': 'data/rl_build/rl_app_data.json',
             'store': 'engine/rl_after/rl_model_data.json',
             'engine_head': 'engine/rl_after/_merged_recover.py',
             'rl_model': 'engine/rl_after/rl_model.py',
             'register': 'LTI_REGISTER.md',
             'v0surf': 'data/v0surf.pkl'}
    src = {k: _git_show_md5(ctx, base, rel) for k, rel in files.items()}
    dst = {k: md5(_p(ctx, rel)) for k, rel in files.items()}
    boot_before = ctx.facts['base']['expected_boot']
    boot_after = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))
    for k in ('config', 'fv', 'balanced_board_md5', 'as_of_round', 'release_version'):
        src[k] = boot_before.get(k)
        dst[k] = boot_after.get(k)
    # The measured side is cross-checked against THAT TREE'S OWN manifest, exactly as the per-act
    # measure_lineage.py did. A side that disagrees with its own manifest is not a side.
    for k in ('board', 'store', 'engine_head', 'rl_model', 'register'):
        if boot_before.get(k) is not None and boot_before[k] != src[k]:
            raise StepError('base-commit %s (%s) disagrees with that tree\'s expected_boot (%s)'
                            % (k, src[k], boot_before[k]))
        if boot_after.get(k) is not None and boot_after[k] != dst[k]:
            raise StepError('live %s (%s) disagrees with the landed expected_boot (%s)'
                            % (k, dst[k], boot_after[k]))
    moved = sorted(k for k in src if src[k] != dst[k])
    unchanged = sorted(k for k in src if src[k] == dst[k])
    return src, dst, moved, unchanged


def _append_transition(ctx):
    lin = ctx.spec['lineage']
    path = _p(ctx, 'data', 'release_lineage.json')
    raw = open(path, 'rb').read()
    doc = json.loads(raw)
    if json.dumps(doc, indent=1).encode() != raw:
        raise StepError('release_lineage.json does not round-trip at indent=1; refusing to reformat it')
    base_balanced, base_version = doc.get('balanced_board_md5'), doc.get('release_version')
    reg = doc.get('release_transition_register')
    if not isinstance(reg, list):
        raise StepError('release_transition_register missing or not a list')
    before_blob = json.dumps(reg)

    src, dst, moved, unchanged = _measure_sides(ctx)
    boundary = lin.get('boundary') or [str(json.load(open(_p(ctx, 'data', 'expected_boot.json'),
                                                          encoding='utf-8')).get('as_of_round')),
                                       (ctx.spec.get('column') or {}).get('id')]
    for e in reg:
        if isinstance(e, dict) and (e.get('applies_to') or {}).get('boundary') == boundary:
            ctx.log('lineage entry for boundary %r already present — no-op' % boundary)
            return {'boundary': boundary, 'appended': False}
    for e in [doc.get('release_transition') or {}] + [x for x in reg if isinstance(x, dict)]:
        if (e.get('destination') or {}).get('board') == dst['board']:
            raise StepError('an existing record already declares destination.board %s (ruling %r)'
                            % (dst['board'], e.get('owner_ruling_id')))

    # ---- THE CHAIN, asserted in the form that is TRUE ------------------------------------------
    prev = (reg[-1].get('destination') or {}) if reg else {}
    tail_board, tail_store = str(prev.get('board')), str(prev.get('store'))
    if (tail_board, tail_store) == (src['board'], src['store']):
        ctx.log('chain OK: register tail destination == this entry\'s source on board and store')
        bridge = None
    else:
        mv = _p(ctx, 'ui', 'data', 'movers.js')
        txt = open(mv, encoding='utf-8').read()
        b = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
        bridge = next((r for r in sorted(b.get('reports', {}), key=int)
                       if b['reports'][r].get('board_md5_before') == tail_board
                       and b['reports'][r].get('board_md5_after') == src['board']
                       and b['reports'][r].get('source_store_md5_before') == tail_store
                       and b['reports'][r].get('source_store_md5_after') == src['store']), None)
        if bridge is None:
            raise StepError(
                'register tail destination (board %s / store %s) != this entry\'s source (board %s / '
                'store %s), and NO SINGLE movers round report bridges BOTH legs. That is a broken '
                'chain, not a gap.' % (tail_board, tail_store, src['board'], src['store']))
        ctx.log('chain GAP, CLOSED BY EVIDENCE — bridged by the ROUND %s advance (board %s -> %s, '
                'store %s -> %s)' % (bridge, tail_board[:8], src['board'][:8], tail_store[:8],
                                     src['store'][:8]))

    keys = ('release_version', 'board', 'store', 'rl_model', 'engine_head', 'fv', 'config',
            'register', 'balanced_board_md5', 'v0surf', 'as_of_round')
    entry = {
        '_doc': lin['doc'],
        'kind': lin.get('kind', 'movers_release_transition'),
        'schema_version': 2,
        'owner_approved': True,
        'owner_ruling_id': lin['owner_ruling_id'],
        'owner_ruling': lin['owner_ruling'],
        'authority': lin['authority'],
        'applies_to': {'bundle': lin.get('bundle', 'ui/data/movers.js'), 'boundary': boundary},
        'source': {k: src.get(k) for k in keys},
        'destination': {k: dst.get(k) for k in keys},
        'moved_by_transition': moved,
        'unchanged_across_transition': unchanged,
        'invariants': lin.get('invariants') or {},
        '_measured_note': (
            'moved/unchanged are MEASURED by tools/landing (steps._measure_sides), not asserted: '
            'every `source` identity is re-hashed from the committed tree at %s via git show, every '
            '`destination` identity from the live tree, and each side is cross-checked against THAT '
            'TREE\'S OWN data/expected_boot.json before the entry is composed.' % ctx.facts['base']['commit'][:7]),
    }
    if bridge:
        entry['_chain_note'] = (
            'This entry\'s source board %s is not the register tail\'s destination %s. The gap is a '
            'ROUND ADVANCE, which moves the board legitimately and gets no register entry because '
            'this register records OUT-OF-ROUND transitions only. It is closed by an independent '
            'record: ui/data/movers.js\'s round %s report carries board_md5_before/after and '
            'source_store_md5_before/after naming exactly both legs.' % (src['board'], tail_board, bridge))

    reg.append(entry)
    if json.dumps(reg[:-1]) != before_blob:
        raise StepError('a prior register entry changed; append-only violated')
    if doc.get('balanced_board_md5') != base_balanced or doc.get('release_version') != base_version:
        raise StepError('release_lineage top-level present-lens baseline moved — it must never move')
    ctx.log('append-only OK: %d prior entries byte-verbatim; top-level baseline %s / %s UNMOVED'
            % (len(reg) - 1, base_balanced, base_version))
    ctx.log('MOVED by this transition: %s (of %d identities)' % (moved, len(moved) + len(unchanged)))

    if not ctx.opts.dry_run:
        out = json.dumps(doc, indent=1).encode()
        open(path, 'wb').write(out)
        back = open(path, 'rb').read()
        d2 = json.loads(back)
        if json.dumps(d2, indent=1).encode() != back:
            raise StepError('the written lineage file does not round-trip at indent=1')
        if json.dumps(d2['release_transition_register'][:-1]) != before_blob:
            raise StepError('re-read shows a prior entry changed')
        ctx.log('re-read OK: round-trips at indent=1; prior entries still byte-verbatim.')
    return {'boundary': boundary, 'appended': True, 'moved': moved, 'entries': len(reg),
            'bridged_by_round': bridge}


# ============================================================================== STEP 4 — CONTRACT
def contract(ctx):
    """`data/release_contract.json` through its writers of record, then the seal check.

    Carried from `land_f5_contract.py` / `land_br_contract.py`. Two writers, in order:
      1. `release_contract.restamp_dynamic(root, as_of_round, store, board, season_state)` — the SAME
         call `staged_apply.py` and `ownership_store_apply.py` make.
      2. the BAKE-LANE identities restamp_dynamic will not touch (config_sha256 / engine_head /
         rl_model / fv), each RE-MEASURED from the checkout and asserted against the accepted
         manifest BEFORE anything is written.

    The seal is asserted self-consistent BEFORE the act as well as after: a contract that does not
    verify going in cannot be shown to have been changed only as declared.
    """
    ctx.fault_point('contract')
    RCT = _load(ctx, 'release_contract', 'release_contract.py')
    cp = _p(ctx, 'data', 'release_contract.json')
    raw = open(cp, 'rb').read()
    rc = json.loads(raw)
    body = json.dumps(rc, indent=2).encode()
    if raw != body and raw != body + b'\n':
        raise StepError('release_contract.json does not round-trip at indent=2; refusing to reformat it')
    trailing_newline = (raw == body + b'\n')
    if rc['contract_sha256'] != RCT.contract_hash(rc):
        raise StepError('the contract seal is not self-consistent BEFORE this act')
    ctx.log('contract seal self-consistent before the act: %s' % rc['contract_sha256'][:12])

    boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))
    measured = {k: PIN_MEASURERS[k](ctx) for k in ('config', 'engine_head', 'rl_model', 'fv')}
    store_md5 = PIN_MEASURERS['store'](ctx)
    board_md5 = PIN_MEASURERS['board'](ctx)
    for k, v in list(measured.items()) + [('store', store_md5), ('board', board_md5)]:
        if boot.get(k) != v:
            raise StepError('manifest and tree disagree on %s: tree %s, expected_boot %s'
                            % (k, v, boot.get(k)))
        ctx.log('  %-12s %s   == expected_boot' % (k, v))

    before = {'config_sha256': rc['config_sha256'], 'as_of_round': rc['as_of_round'],
              'contract_sha256': rc['contract_sha256'],
              **{'identities.' + k: v for k, v in rc['identities'].items()}}
    ss = json.load(open(_p(ctx, 'data', 'season_state.json'), encoding='utf-8'))
    as_of = int(boot['as_of_round'])
    ctx.log('WRITER 1: release_contract.restamp_dynamic(root, as_of_round=%d, store, board, '
            'season_state)' % as_of)
    if ctx.opts.dry_run:
        ctx.log('   --dry-run: not called.')
    else:
        seal = RCT.restamp_dynamic(ctx.root, as_of, store_md5, board_md5, ss)
        ctx.log('   restamp_dynamic returned seal %s' % str(seal)[:12])
        rc = json.loads(open(cp, 'rb').read())

    FROZEN = ('identities.band', 'identities.register', 'release_version', 'switch_posture',
              'pvc_provenance', 'must_be_unset', 'held_checks', 'adopted', 'season_state_policy_id',
              '_retired_checks')
    FROZEN = tuple(list(FROZEN) + list(ctx.spec.get('contract_frozen_extra') or ()))

    def snap(c):
        return {k: json.dumps(c['identities'].get(k.split('.', 1)[1], None), sort_keys=True)
                if k.startswith('identities.') else json.dumps(c.get(k), sort_keys=True)
                for k in FROZEN}

    fb = snap(rc)
    ctx.log('WRITER 2: the bake-lane identities restamp_dynamic does not touch')
    ctx.log('  contract config_sha256      %s -> %s' % (rc['config_sha256'][:12], measured['config'][:12]))
    rc['config_sha256'] = measured['config']
    for f in ('engine_head', 'rl_model', 'fv'):
        ctx.log('  contract identities.%-12s %s -> %s'
                % (f, str(rc['identities'][f])[:12], measured[f][:12]))
        rc['identities'][f] = measured[f]
    old_seal = rc.pop('contract_sha256')
    rc['contract_sha256'] = RCT.contract_hash(rc)
    ctx.log('  contract_sha256             %s -> %s' % (old_seal[:12], rc['contract_sha256'][:12]))
    mv = [k for k in fb if fb[k] != snap(rc)[k]]
    if mv:
        raise StepError('a field writer 2 must not touch moved: %s' % mv)
    ctx.log('  frozen fields asserted unmoved: %d checked, 0 moved' % len(FROZEN))

    out = {'seal_before': before['contract_sha256'], 'seal_after': rc['contract_sha256'],
           'trailing_newline_in_committed_file': trailing_newline}
    if not ctx.opts.dry_run:
        # THE TRAILING NEWLINE IS PRESERVED, and that is a repair rather than a nicety. The committed
        # file carries one; `json.dump(indent=2)` emits none. Every hand-written landing script this
        # library consolidates NOTED the discrepancy in a print and then dropped the byte anyway, so
        # a landing that moved nothing still moved a file. Writing back the convention the file
        # arrived with is what makes a no-op rehearsal genuinely byte-exact — and it is the same rule
        # the pins step already follows: the ONLY bytes that differ are the declared values.
        tmp = cp + '.landing_tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(rc, indent=2) + ('\n' if trailing_newline else ''))
        os.replace(tmp, cp)
        rc2 = json.load(open(cp, encoding='utf-8'))
        if rc2['contract_sha256'] != RCT.contract_hash(rc2):
            raise StepError('the seal must verify after the write')
        if rc2['identities']['store'] != boot['store'] or rc2['identities']['board'] != boot['board']:
            raise StepError('the contract store/board pins do not name the live tree')
        if int(rc2['as_of_round']) != as_of:
            raise StepError('the contract must name round %d — the round expected_boot names. A '
                            'lever landing HOLDS the round it found; a round advance has already '
                            'moved it, and either way the contract follows the manifest, never the '
                            'other way about.' % as_of)
        rcc, cout = ctx.run(['python3', 'release_contract.py', 'check'])
        if rcc != 0 or 'PASS' not in cout:
            raise StepError('release_contract.py check did not PASS after the restamp:\n%s' % cout[-1500:])
        ctx.log('RE-STAMPED, re-read, and release_contract.py check PASSES.')
        out['check'] = 'PASS'
    return out


# =============================================================================== STEP 5 — SIBLING
def sibling(ctx):
    """The balanced sibling: rebuild and reconcile IF it moves, through its writer of record.

    `sibling_repin.py` is BUILD-AND-COMPARE only — the pin is moved to a value that was just BUILT
    and derived from the built artifact, never to an expectation. This step verifies before, plans,
    reconciles only when the plan says something changed, and verifies after. A `verify` that still
    reports fails after a reconcile is a halt, not a note: the D8 landing discharged an eight-fail
    backlog here precisely because it was never allowed to be a note.
    """
    ctx.fault_point('sibling')
    SR = _load(ctx, 'sibling_repin', 'engine/rl_after/ingestion/sibling_repin.py')
    sr = SR.SiblingRepin(ctx.root)
    before = sr.verify()
    ctx.log('verify BEFORE : ok=%s balanced=%s fails=%d'
            % (before.get('ok'), str(before.get('balanced_board_md5'))[:12], len(before.get('fails') or [])))
    for f in (before.get('fails') or []):
        ctx.log('    - %s' % f)
    if before.get('ok'):
        ctx.log('the sibling is CURRENT — nothing to reconcile, and this step writes nothing.')
        return {'reconciled': False, 'balanced_board_md5': before.get('balanced_board_md5'),
                'fails_before': 0, 'fails_after': 0}
    if ctx.opts.dry_run:
        ctx.log('--dry-run: the sibling is stale and would be reconciled (a BUILD). Not run.')
        return {'reconciled': 'dry-run', 'fails_before': len(before.get('fails') or [])}

    res = ctx.with_child_env(lambda: sr.reconcile(
        round_n=int(json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))['as_of_round'])))
    ctx.log('reconcile     ok=%s changed=%s balanced %s -> %s'
            % (res.get('ok'), res.get('changed'), str(res.get('old_balanced_board_md5'))[:12],
               str(res.get('balanced_board_md5'))[:12]))
    ctx.log('  committed targets: %s' % ', '.join(res.get('committed_targets') or []))
    if not res.get('ok'):
        raise StepError('the sibling reconcile did not complete: %s' % json.dumps(res)[:800])
    after = SR.SiblingRepin(ctx.root).verify()
    ctx.log('verify AFTER  : ok=%s fails=%d' % (after.get('ok'), len(after.get('fails') or [])))
    if not after.get('ok'):
        raise StepError('sibling verify still reports %d fail(s) after the reconcile: %s'
                        % (len(after['fails']), after['fails']))
    return {'reconciled': True, 'balanced_board_md5': after.get('balanced_board_md5'),
            'fails_before': len(before.get('fails') or []), 'fails_after': 0,
            'committed_targets': res.get('committed_targets')}


# ==================================================================================== STEP 6 — UI
def _js_obj(path):
    """The payload of a `window.__X__ = {...}` bundle, read the way the r14 gate reads it.

    Deliberately the SAME crude slice `test_movers_transition._loadjs` uses — first `{` to last `}`.
    A different parser here could accept a file the gate rejects, and the whole point of asserting
    the gate's predicates in this step is that they ARE the gate's predicates, not near neighbours.
    """
    with open(path, encoding='utf-8') as fh:
        t = fh.read()
    return json.loads(t[t.index('{'):t.rindex('}') + 1])


def _mirror_register(path):
    """The mirror's `release_transition_register`."""
    return _js_obj(path).get('release_transition_register')


def _lines_with(out, *needles):
    """The child's own verdict lines, SELECTED BY NAME rather than by position.

    Writers 3 and 4 log `splitlines()[-1]`, which is the writer's verdict only while the writer's
    verdict happens to be the last thing written. `ingest_inputs.py` emits a DeprecationWarning on
    3.12 (`datetime.utcnow`) AFTER its summary, so the tail read `drift guard: return
    datetime.datetime.utcnow()...` — a log line that names no verdict at all, in the transcript a
    landing is judged from. Naming the line we want cannot drift that way.
    """
    return [ln.strip() for ln in out.strip().splitlines()
            if any(n in ln for n in needles)]


def _own_stamp(path):
    """The ownership mirror's `stamp` — the block `ui/app/ownership.js:pin()` authenticates.

    Read through the SAME crude slice the rest of this module uses, and fail-soft to `{}`: a mirror
    the browser cannot parse is a mirror the browser refuses, and the predicate below must report
    that as a refusal rather than dying with a traceback that names no file.
    """
    try:
        return _js_obj(path).get('stamp') or {}
    except (OSError, ValueError):
        return {}


def ui(ctx):
    """ALL FIVE UI writers. The thrice-proven trap, now code — and it keeps proving there is one more.

    THE CLASS, CLOSED ONE CARRIER AT A TIME: the UI bundles this estate ships are all written in this
    transaction now — `board_view_working.js` and `board_view_public.js` (writers 1-2),
    `movers_transition.js` (writer 3, the lineage's mirror), `movers.js` (writer 4, the blocks DERIVED
    from that mirror), and `ownership.js` (writer 5, the store's ownership mirror). Each was found the
    same way: a landing moved a record or an identity, shipped a reader that could not see it, and a
    standing gate said so.

    THE FOURTH TIME, AND WHY THE "CLOSED BY EXHAUSTION" LINE THAT USED TO STAND HERE WAS WRONG. This
    docstring said in as many words "There is no fifth bundle behind them." There was.
    `ui/data/ownership.js` is a MIRROR of the store's `affl_team`, and it carries the board + store
    identity it was generated from because `ui/app/ownership.js:pin()` REFUSES a mirror whose pin does
    not match the loaded app — the #232 hole, closed by #283. So the failure mode is not a wrong club
    on the board; it is the LIVE OWNERSHIP LANE SWITCHED OFF, and nothing renders an error. Measured
    on 2026-08-21: the tree stood on board b3e8da99 / store b745002e (R23) while the shipped mirror
    still carried a05fe951 / cc02567f (R22) — the R23 advance moved the store and no writer moved the
    mirror. `ui/tests/ownership_sidecar.test.js` was 22/35, `ownership_single_source` 15/17, and all
    of it was one stale stamp. Exhaustion is not a proof; enumeration against the carrier set is, and
    carriers.py now names this file's writer of record.

    `ui/tools/extract_board_view.py` REGENERATES the bundle from the board and DROPS `stamp.release`;
    only `round_movers.inject_release_contract` puts it back. Running the first without the second
    leaves the html app with no release block — a failure this tree has caught THREE times
    (landing_tail 02a_*.txt, 28_reinject_release_contract.txt, and d8_restamp.py §3, which runs them
    as a pair for exactly this reason). Every landing since has carried a hand-written script whose
    docstring explains the trap. This function is that docstring, executable.

    WRITER 3 — SUPERVISOR RULING, 2026-08-21, on finding F-9:

        "A landing that moves the lineage record moves its mirror in the same transaction — the
         projector ui/tools/generate_movers_transition.py becomes the lever landing's third UI
         writer, and ui/data/movers_transition.js's writer-of-record entry in carriers.py names the
         lever landing alongside round_movers (2b inherits, no conflict: same projector, same law).
         This is the T7 both-writers law completing itself: the trap was thrice-proven for two
         writers and today proved there was a third. Option 2 is rejected in the ruling's own words —
         a board whose reader cannot see the transition that produced it; option 3 spends the owner's
         given word on a dependency it does not need."

    HOW IT WAS FOUND, because the shape of the defect is the argument for the fix. Step 3 appends to
    `data/release_lineage.json`'s `release_transition_register`; `ui/data/movers_transition.js` is the
    mirror a standing gate asserts EQUAL to it; and no lever landing wrote the mirror, because
    `carriers.py` named its writer of record as the 2b round lander, WHICH IS NOT BUILT. So every
    lever landing that registered an out-of-round column red its own `gates` step by construction:
    on 2026-08-21 the record went 12 entries -> 13 while the mirror stayed at 12, and
    `oneliner_r14_restore` failed on exactly that inequality. The landing was writing a record its
    own reader could never see.

    IT IS AUTHORLESS AND IT IS SELF-VERIFYING. The projector is a MECHANICAL SERIALIZATION of the
    lineage carrying, in its own charter's words, "ZERO authorship" — so running it can only make the
    mirror equal the record, never assert anything of its own. It runs UNCONDITIONALLY: a projection
    of a record that did not move produces a byte-identical file and no carrier movement, so there is
    no branch to get wrong, and pre-existing drift is repaired rather than carried. Then its own
    `--check` drift guard is run, and the r14 predicate — mirror register == lineage register — is
    asserted here, on the two files, BEFORE the gate that will assert it again. THE GATE NOW PASSES
    ON TRUE EQUALITY, NOT ON SCOPING.

    The identity is then read back OUT of the html bundle — the page's own embedded stamp — because
    a bundle that was regenerated but not re-stamped renders perfectly and says nothing true.
    """
    ctx.fault_point('ui')
    bundle = _p(ctx, 'ui', 'data', 'board_view_working.js')
    public = _p(ctx, 'ui', 'data', 'board_view_public.js')
    boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))

    def has_release(p):
        return '"release"' in open(p, encoding='utf-8').read()

    mirror = _p(ctx, 'ui', 'data', 'movers_transition.js')
    movers = _p(ctx, 'ui', 'data', 'movers.js')
    own = _p(ctx, 'ui', 'data', 'ownership.js')
    ctx.log('BEFORE  working %s  release-block=%s' % (md5(bundle), has_release(bundle)))
    ctx.log('BEFORE  public  %s  release-block=%s' % (md5(public), has_release(public)))
    ctx.log('BEFORE  mirror  %s  register=%d entr(ies)'
            % (md5(mirror), len(_mirror_register(mirror) or [])))
    ctx.log('BEFORE  movers  %s  model_changes=%d boundar(ies)'
            % (md5(movers), len(_js_obj(movers).get('model_changes') or [])))
    ctx.log('BEFORE  owners %s  pinned board=%s store=%s'
            % (md5(own), _own_stamp(own).get('board', '?')[:8],
               _own_stamp(own).get('generatedFromStore', '?')[:8]))
    if ctx.opts.dry_run:
        ctx.log('--dry-run: none of the five writers is run.')
        return {'writers': 0, 'dry_run': True}

    ctx.log('WRITER 1/5: ui/tools/extract_board_view.py')
    rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'extract_board_view.py')], timeout=900)
    if rc != 0:
        raise StepError('extract_board_view failed:\n%s' % out[-2000:])
    ctx.log('  working after writer 1: %s   release-block=%s   <-- DROPPED, as it always is'
            % (md5(bundle), has_release(bundle)))

    if not ctx.skip_second_ui_writer:
        ctx.log('WRITER 2/5: round_movers.inject_release_contract(bundle, root, %s)' % boot['as_of_round'])
        rm = _load(ctx, 'round_movers', 'engine/rl_after/ingestion/round_movers.py')
        rel = rm.inject_release_contract(bundle, ctx.root, int(boot['as_of_round']))
        ctx.log('  release block: %s' % json.dumps(rel, sort_keys=True)[:200])
    else:
        ctx.log('WRITER 2/5: SKIPPED BY FAULT INJECTION — the trap is live in this transaction.')

    mirror_before = md5(mirror)
    ctx.log('WRITER 3/5: ui/tools/generate_movers_transition.py  '
            '(the lineage projection — supervisor ruling on F-9)')
    rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'generate_movers_transition.py')],
                      timeout=300)
    if rc != 0:
        raise StepError('the movers-transition projector failed (exit %s):\n%s' % (rc, out[-2000:]))
    for ln in out.strip().splitlines():
        ctx.log('  %s' % ln.strip())

    # ITS OWN DRIFT GUARD, RUN — the projector ships a `--check` that recomputes the projection and
    # compares it to what is on disk. Running the writer and then asking the writer's own checker is
    # the same discipline writer 2 gets from the stamp read-back below: a writer that reports success
    # has not proved anything until something re-derives its output.
    rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'generate_movers_transition.py'),
                       '--check'], timeout=300)
    if rc != 0:
        raise StepError('the mirror does not match what the lineage projects after regenerating it '
                        '(exit %s):\n%s' % (rc, out[-2000:]))
    ctx.log('  drift guard: %s' % out.strip().splitlines()[-1].strip())

    # THE r14 PREDICATE, ASSERTED HERE ON THE TWO FILES, before the gate asserts it again. This is
    # the exact comparison test_movers_transition.py:107 makes ("era succession: ALL entries reach
    # the reader"), and F-9 is the record of what happens when a landing reaches step 7 without it.
    lin_reg = json.load(open(_p(ctx, 'data', 'release_lineage.json'),
                             encoding='utf-8')).get('release_transition_register')
    mir_reg = _mirror_register(mirror)
    if mir_reg != lin_reg:
        raise StepError('THE MIRROR\'S REGISTER IS NOT THE LINEAGE\'S REGISTER after writer 3: '
                        'mirror %d entr(ies), lineage %d. This is the F-9 predicate '
                        '(test_movers_transition.py:107) and it must hold BEFORE the gates step.'
                        % (len(mir_reg or []), len(lin_reg or [])))
    ctx.log('  mirror register == lineage register: %d entr(ies), EQUAL  (the F-9 predicate holds)'
            % len(lin_reg or []))

    # ---- WRITER 4: the movers bundle's DERIVED blocks (supervisor ruling on F-10) ----------------
    # THE SAME LAW, ONE CARRIER ALONG, AND THE SAME PATTERN: unconditional, self-verifying, and the
    # gate's own predicate asserted here in-step. `model_changes` is DERIVED from the register that
    # writer 3 just mirrored, and it is BAKED into ui/data/movers.js at write time — so a landing that
    # appends to the register and stops at writer 3 ships a bundle whose boundary labels do not know
    # about the move that produced them. That is F-10, and it red attempt 3 at
    # test_movers_transition.py:137.
    #
    # THIS IS THE WRITER THE PROVEN HAND-WALKED LANDINGS USED, NOT A NEW INVENTION. The backrows
    # reseal's own UI step (docs/evidence/backrows_reseal_2026-08-20/09_landing_e_ui.txt) records
    # exactly this pair, in this order:
    #     --- WRITER 3: ui/tools/generate_movers_transition.py (mirror the lineage register) ---
    #     --- WRITER 4: ui/tools/rebuild_movers_derived.py (points / values / model_changes) ---
    #     --- both --check ---
    # That landing passed this suite after registering a column. The recipe was already in the tree;
    # what was missing was the lander running it.
    movers_before = md5(movers)
    ctx.log('WRITER 4/5: ui/tools/rebuild_movers_derived.py  '
            '(points / values / model_changes — supervisor ruling on F-10)')
    rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'rebuild_movers_derived.py')],
                      timeout=900)
    if rc != 0:
        raise StepError('the movers derived-block rebuild failed (exit %s):\n%s' % (rc, out[-2000:]))
    for ln in out.strip().splitlines():
        ctx.log('  %s' % ln.strip())

    rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'rebuild_movers_derived.py'),
                       '--check'], timeout=900)
    if rc != 0:
        raise StepError('the movers bundle\'s derived blocks do not match what the live tree rebuilds '
                        '(exit %s):\n%s' % (rc, out[-2000:]))
    ctx.log('  drift guard: %s' % out.strip().splitlines()[-1].strip())

    # THE F-10 PREDICATE, ASSERTED HERE — the exact comparison test_movers_transition.py:137 makes:
    # model_changes recomputed from the LIVE TREE against the SHIPPED bundle's baked copy.
    rm4 = _load(ctx, 'round_movers', 'engine/rl_after/ingestion/round_movers.py')
    live_mc = rm4.model_changes(ctx.root)
    shipped_mc = _js_obj(movers).get('model_changes') or []
    if live_mc != shipped_mc:
        raise StepError('THE SHIPPED MOVERS BUNDLE\'S model_changes IS NOT WHAT THE LIVE TREE DERIVES '
                        'after writer 4: live %d boundar(ies), shipped %d. This is the F-10 predicate '
                        '(test_movers_transition.py:137) and it must hold BEFORE the gates step.'
                        % (len(live_mc), len(shipped_mc)))
    ctx.log('  shipped model_changes == live-derived: %d boundar(ies), EQUAL  (the F-10 predicate holds)'
            % len(shipped_mc))

    # ---- WRITER 5: the ownership mirror, re-pinned to the board and store this landing lands ------
    # THE SAME LAW AGAIN, ONE CARRIER ALONG, AND THE SAME THREE-PART PATTERN writers 3 and 4 use:
    # run the writer UNCONDITIONALLY, run the writer's OWN checker, then assert the reader's own
    # predicate here, in-step, before any gate asserts it.
    #
    # UNCONDITIONAL FOR THE REASON WRITER 3 IS: the mirror is a pure function of the store and the
    # board (no wall clock — #283 acceptance 4 requires exactly that so "regenerate and compare" can
    # be an equality), so regenerating it on a landing that moved neither produces a byte-identical
    # file and no carrier movement. There is no branch to get wrong, and pre-existing drift — the
    # state this tree was actually in — is repaired rather than carried.
    #
    # `--mirror-only` IS NOT A SHORTCUT, IT IS THE FENCE. The full ingest also writes
    # ui/data/club_valuation.js (a wall-clock bundle that is not a carrier and could not be proved
    # byte-exact) and performs the #283 STORE APPLY as its step 0 — an identity-moving write with its
    # own writer of record. A landing is not that writer. In this lane the store is read and never
    # written, and an un-couriered CSV edit HALTs the step by name instead of moving the store
    # mid-flight.
    own_before = md5(own)
    if not ctx.skip_ownership_writer:
        ctx.log('WRITER 5/5: ui/tools/ingest_inputs.py --mirror-only  '
                '(the ownership mirror, re-pinned to the landed board + store)')
        rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'ingest_inputs.py'),
                           '--mirror-only'], timeout=900)
        if rc != 0:
            raise StepError('the ownership mirror regeneration failed (exit %s):\n%s' % (rc, out[-2000:]))
        for ln in _lines_with(out, 'LIVE MIRROR', 'MIRROR-ONLY'):
            ctx.log('  %s' % ln)

        rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'ingest_inputs.py'),
                           '--check'], timeout=900)
        if rc != 0:
            raise StepError('the ownership mirror is not what this tree projects after regenerating '
                            'it (exit %s):\n%s' % (rc, out[-2000:]))
        ctx.log('  drift guard: %s'
                % (_lines_with(out, 'MIRROR DRIFT GUARD') or ['(no verdict line)'])[-1])
    else:
        ctx.log('WRITER 5/5: SKIPPED BY FAULT INJECTION — the mirror keeps the pin of a store this '
                'landing is replacing.')

    # THE READER'S OWN PREDICATE, ASSERTED HERE: this is `ui/app/ownership.js:pin()`, which compares
    # the mirror's stamped board + store against the working bundle's stamp and DEACTIVATES the mirror
    # on any mismatch. Asserting it in-step is what turns "the writer ran" into "the browser will
    # honour what the writer wrote" — the same distinction the stamp read-back below draws for
    # writer 2. A mirror that is regenerated but not authenticated renders perfectly and says nothing.
    ost = _own_stamp(own)
    own_fails = []
    for k, exp in (('board', boot['board']), ('generatedFromStore', boot['store']),
                   ('store', boot['store'][:8]), ('expectedBoard', boot['board'][:8]),
                   ('asOfRound', boot['as_of_round'])):
        if str(ost.get(k)) != str(exp):
            own_fails.append('stamp.%s (%s != %s)' % (k, ost.get(k), exp))
    if ost.get('nOverriding') not in (0, '0'):
        own_fails.append('stamp.nOverriding is %r — a mirror cannot override the field it mirrors'
                         % ost.get('nOverriding'))
    if own_fails:
        raise StepError('THE OWNERSHIP MIRROR WOULD BE REFUSED BY ui/app/ownership.js:pin() — %s. '
                        'The live ownership lane would ship SWITCHED OFF, which is what happened '
                        'between the R23 advance and 2026-08-21, and it must hold BEFORE the gates '
                        'step.' % own_fails)
    ctx.log('  mirror pin == the landed identity: board %s store %s R%s, %d player(s) mirrored '
            '(pin() would ACTIVATE it)'
            % (str(ost.get('board'))[:8], str(ost.get('generatedFromStore'))[:8],
               ost.get('asOfRound'), ost.get('nAuthored')))

    ctx.log('AFTER   working %s  release-block=%s' % (md5(bundle), has_release(bundle)))
    ctx.log('AFTER   public  %s  release-block=%s' % (md5(public), has_release(public)))
    ctx.log('AFTER   movers  %s  %s' % (md5(movers),
                                        'UNMOVED (nothing it derives from moved)'
                                        if md5(movers) == movers_before else
                                        'MOVED %s -> %s, tracking the register append'
                                        % (movers_before[:12], md5(movers)[:12])))
    ctx.log('AFTER   mirror  %s  %s' % (md5(mirror),
                                        'UNMOVED (the lineage did not move)'
                                        if md5(mirror) == mirror_before else
                                        'MOVED %s -> %s, tracking the lineage append'
                                        % (mirror_before[:12], md5(mirror)[:12])))
    ctx.log('AFTER   owners %s  %s' % (md5(own),
                                       'UNMOVED (neither the board nor the store moved)'
                                       if md5(own) == own_before else
                                       'MOVED %s -> %s, tracking the landed board + store'
                                       % (own_before[:12], md5(own)[:12])))

    src = open(bundle, encoding='utf-8').read()
    m = re.search(r'window\.__MATCHDAY_WORKING__\s*=\s*(\{.*)\n?', src, re.S)
    if not m:
        raise StepError('the working bundle carries no __MATCHDAY_WORKING__ payload')
    st = json.loads(m.group(1).rstrip().rstrip(';'))['stamp']
    fails = []
    for k, exp in (('board_md5', boot['board']), ('board', boot['board']), ('srcmd5', boot['board']),
                   ('store_md5', boot['store']),
                   ('balanced_board_md5', boot['balanced_board_md5']),
                   ('asOfRound', boot['as_of_round'])):
        ok = str(st.get(k)) == str(exp)
        ctx.log('  stamp.%-20s %-34s %s' % (k, st.get(k), 'OK' if ok else '*** != %s ***' % exp))
        if not ok:
            fails.append('stamp.' + k)
    for k, exp in (('engine', boot['engine_head'][:8]), ('store', boot['store'][:8]),
                   ('register', boot['register'][:8]), ('config', boot['config'][:12])):
        ok = str(st.get(k)) == exp
        if not ok:
            fails.append('stamp.' + k)

    # stamp.release is assembled from TWO sources and says so in its own manifest_source field: the
    # identity pins come from expected_boot; balanced_board_md5 and release_version come from the
    # LINEAGE file's frozen present-lens baseline. Asserted against its REAL source rather than the
    # one it does not read — the correction land_f5_ui.py recorded and every later landing inherits.
    relb = st.get('release') or {}
    lin = json.load(open(_p(ctx, 'data', 'release_lineage.json'), encoding='utf-8'))
    expect_rel = {'board': boot['board'], 'store': boot['store'], 'engine_head': boot['engine_head'],
                  'rl_model': boot['rl_model'], 'fv': boot['fv'], 'config': boot['config'],
                  'register': boot['register'], 'as_of_round': boot['as_of_round'],
                  'balanced_board_md5': lin['balanced_board_md5'],
                  'release_version': lin['release_version']}
    if not relb:
        fails.append('stamp.release IS ABSENT — writer 2 did not run, or did not take')
    for k, exp in sorted(expect_rel.items()):
        if relb and str(relb.get(k)) != str(exp):
            fails.append('stamp.release.%s (%s != %s)' % (k, relb.get(k), exp))
    if fails:
        raise StepError('THE UI BUNDLE IDENTITY IS WRONG: %s' % fails)
    ctx.log("THE HTML APP'S EMBEDDED BOARD IDENTITY IS %s. All five writers ran; the release block "
            "is back, the reader can see the transition that produced this board, and the ownership "
            "mirror is pinned to it rather than to the store it replaced." % boot['board'])
    return {'writers': 5, 'bundle_md5': md5(bundle), 'public_md5': md5(public),
            'embedded_board': st.get('board_md5'),
            'mirror_md5': md5(mirror), 'mirror_moved': md5(mirror) != mirror_before,
            'register_entries': len(lin_reg or []),
            'movers_md5': md5(movers), 'movers_moved': md5(movers) != movers_before,
            'model_changes': len(shipped_mc),
            'ownership_md5': md5(own), 'ownership_moved': md5(own) != own_before,
            'ownership_pin': str(ost.get('generatedFromStore'))[:8]}


# ================================================================================= STEP 7 — GATES
def gates(ctx):
    """The landing gate set. Verdicts are read off exit codes; none is taken on trust.

    fv-provenance is NEVER run here. PLAN_v6 2a.1: the suite overwrites a shared pickle, so it runs
    in isolated workspaces only and CI excludes it on shared runners. The lander calls the FV
    builder FUNCTION for its builds (which is safe and is what the day's build drivers did) and
    never the suite.

    THE ACCEPTANCE RUNNER RUNS UNDER `--profile in-transaction`, which is `full` minus TWO checks:
    the lander's own self-test (not skipped, MOVED — `cli.cmd_lever` runs it standalone immediately
    before the transaction opens and refuses to open one if it fails; see the ruling quoted in
    `acceptance/checks/landing.py`) and build_twice_determinism (owner word "Skip it.", 2026-08-21,
    register v820 — the transaction's own machinery builds the board, and the determinism proof
    keeps running in the full profile CI and every supervisor verification use; see the ruling
    recorded at `acceptance/checks/m1a.py` per P11). Coverage identical outside the flight.

    EVERY GATE'S RAW OUTPUT LANDS IN THE EVIDENCE DIR, and a gate that can write per-check output of
    its own gets `@EVIDENCE@` substituted for a directory to write it into (F-5).
    """
    ctx.fault_point('gates')
    rows = []
    for g in (ctx.spec.get('gates') or DEFAULT_GATES):
        if 'fv_provenance' in ' '.join(g['argv']):
            raise StepError('a gate names the fv-provenance suite. It overwrites a shared pickle and '
                            'is never run on the shared box (PLAN_v6 2a.1).')
        argv = _gate_argv(ctx, g)
        t0 = time.time()
        rc, out = ctx.run(argv, timeout=g.get('timeout_s', 1800))
        el = time.time() - t0
        ok = (rc == 0) and (g.get('must_contain') is None or g['must_contain'] in out)
        ctx.write_evidence('gate_%s.txt' % g['name'], '$ %s\n\n%s\n[exit %s]' % (' '.join(argv), out, rc))
        ctx.log('  %-24s %-6s exit=%s  (%.1fs)' % (g['name'], 'PASS' if ok else 'FAIL', rc, el))
        rows.append({'name': g['name'], 'argv': argv, 'exit': rc, 'ok': ok,
                     'elapsed_s': round(el, 1)})
        if not ok:
            raise StepError('gate %s did not pass (exit %s%s):\n%s\n\nPER-CHECK RAW OUTPUT: %s'
                            % (g['name'], rc,
                               '' if g.get('must_contain') is None or g['must_contain'] in out
                               else '; %r absent from output' % g['must_contain'], out[-2500:],
                               _gate_evidence_dir(ctx, g) if '@EVIDENCE@' in g['argv']
                               else os.path.join(ctx.evidence_dir, 'gate_%s.txt' % g['name'])))
    return {'gates': rows, 'all_pass': True}


def _gate_evidence_dir(ctx, g):
    """Where a gate that writes its own per-check output writes it: inside THIS landing's evidence."""
    return os.path.join(ctx.evidence_dir, 'gate_%s_evidence' % g['name'])


def _gate_argv(ctx, g):
    """Substitute `@EVIDENCE@` for a per-gate evidence directory, creating it. (F-5)"""
    if '@EVIDENCE@' not in g['argv']:
        return list(g['argv'])
    d = _gate_evidence_dir(ctx, g)
    os.makedirs(d, exist_ok=True)
    return [d if tok == '@EVIDENCE@' else tok for tok in g['argv']]


# ================================================================================ STEP 8 — CLAIMS
def claims(ctx):
    """Emit the act's claims file (tools/claims.py, this act's own kind) and VERIFY it.

    PLAN_v6 1c: every seat's final act includes a claims file, and one standard checker verifies
    claims against artifacts. The lander does not hand the seat a template to fill in — it emits the
    claims from what it MEASURED during the transaction, and then runs the checker, which recomputes
    every one of them from the tree. A claims file the lander wrote and nobody re-derived would
    certify nothing but the lander's consistency with itself.

    The negative control lives in the checker (`tools/claims.py selftest`) and is asserted by the
    lander's own self-test; a false claim emitted here must red this step.
    """
    ctx.fault_point('claims')
    boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))
    board_path = 'data/rl_build/rl_app_data.json'
    board = json.load(open(_p(ctx, board_path), encoding='utf-8'))
    section = next((s for s in ('active', 'players', 'rows') if isinstance(board.get(s), list)), None)

    cl = [{'kind': 'file_md5', 'path': board_path, 'value': md5(_p(ctx, board_path)),
           'label': 'the published board of record'},
          {'kind': 'file_md5', 'path': 'engine/rl_after/rl_model_data.json',
           'value': md5(_p(ctx, 'engine/rl_after/rl_model_data.json')), 'label': 'the store'},
          {'kind': 'json_field', 'path': 'data/expected_boot.json', 'field': 'board',
           'value': boot['board'], 'label': 'expected_boot.board'},
          {'kind': 'json_field', 'path': 'data/expected_boot.json', 'field': 'engine_head',
           'value': boot['engine_head'], 'label': 'expected_boot.engine_head'},
          {'kind': 'json_field', 'path': 'data/expected_boot.json', 'field': 'as_of_round',
           'value': boot['as_of_round'],
           'label': ('the round, ADVANCED to' if ctx.spec['act_kind'] == 'round-advance'
                     else 'the round, HELD by a lever landing')},
          {'kind': 'json_field', 'path': 'data/release_contract.json', 'field': 'contract_sha256',
           'value': json.load(open(_p(ctx, 'data/release_contract.json'),
                                   encoding='utf-8'))['contract_sha256'],
           'label': 'the release seal'}]
    if section:
        cl.append({'kind': 'board_count', 'path': board_path, 'section': section, 'metric': 'rows',
                   'value': len(board[section]), 'label': 'board rows'})
    for g in (ctx.facts.get('gates') or {}).get('gates', []):
        cl.append({'kind': 'gate', 'name': g['name'], 'argv': g['argv'], 'expect': 'PASS',
                   'label': g['name'], 'timeout_s': 1800})
    # The carriers this landing did NOT move, claimed as unmoved against the restore point.
    #
    # WHICH CARRIERS THOSE ARE IS THE ACT KIND'S ONE REAL DIFFERENCE HERE. A lever landing must leave
    # the STORE byte-unmoved and claims exactly that. A round advance moves the store by definition —
    # so what it claims unmoved instead is the SHEET PIN DECLARATION, whenever it declares no re-cut:
    # `land round` is that file's sole writer, and "the sole writer did not write it this week" is a
    # claim worth being able to recompute.
    snap = ctx.snapshot
    unmoved_claims = ()
    if ctx.spec['act_kind'] == 'lever-landing':
        unmoved_claims = ('engine/rl_after/rl_model_data.json',)
    elif not ctx.spec.get('sheet'):
        unmoved_claims = (SHEET_PIN_REL, 'docs/owner_annotations/SITTER_2026_v1.csv')
    for rel, before_md5 in sorted((snap.identities() if snap else {}).items()):
        if before_md5 and rel in unmoved_claims:
            cl.append({'kind': 'unmoved', 'path': rel, 'value': before_md5,
                       'label': 'BYTE-UNMOVED by this %s' % ctx.spec['act_kind']})

    # DAY-0 ACTIVATION STATE IS ON EVERY LANDING'S CLAIMS FILE (PLAN_v6 1c), and it is read from
    # whichever step owns it: `build_proofs` for a lever landing, the `day0` step for a round advance
    # (where the re-base has its natural home — register v810 item 1).
    d0 = ctx.facts.get('day0') if 'day0' in ctx.facts else \
        (ctx.facts.get('build_proofs') or {}).get('day0_rebase', 'off')
    activation = {'day0_rebase': ({'state': 'off',
                                   '_doc': 'off by default; the M1b ruling — automation never '
                                           're-bases itself green'}
                                  if d0 == 'off' else
                                  {'state': 'on', 'activated_by': d0.get('activated_by'),
                                   'rows_moved': d0.get('rows_moved')})}
    for name, spec_sw in (ctx.spec.get('activation') or {}).items():
        activation[name] = spec_sw

    is_round = ctx.spec['act_kind'] == 'round-advance'
    doc = {'schema_version': 1, 'act_type': ctx.spec['act_kind'], 'act': ctx.spec['act'],
           'date': ctx.spec['date'], 'base_commit': ctx.facts['base']['commit'],
           'owner_word': ctx.spec['owner_word'], 'activation': activation, 'claims': cl,
           '_restore_point': ctx.facts['base']['carriers'],
           '_step_timings_s': ctx.timings_dict(),
           '_landed_by': ('tools/landing (`land round`), PLAN_v6 PACKAGE 2b' if is_round
                          else 'tools/landing (`land lever`), PLAN_v6 PACKAGE 2a')}

    if ctx.false_claim:
        # SELF-TEST ONLY (txn.FAULTS['claims']). One claim is made false, and the checker — the same
        # one every seat runs — must red it. This is the negative control firing INSIDE the lander.
        cl[0] = dict(cl[0], value='0' * 32)
        ctx.log('*** the emitted claims file now carries a FALSE board md5 (fault injection)')

    out_path = ctx.claims_path
    if not ctx.opts.dry_run:
        with open(out_path, 'w', encoding='utf-8') as fh:
            json.dump(doc, fh, indent=2, sort_keys=False)
            fh.write('\n')
        rc, out = ctx.run(['python3', 'tools/claims.py', 'check', os.path.relpath(out_path, ctx.root),
                           '--root', ctx.root], timeout=2400)
        ctx.write_evidence('claims_check.txt', out)
        ctx.log(out.strip().splitlines()[-1] if out.strip() else '(claims checker printed nothing)')
        if rc != 0:
            raise StepError('THE CLAIMS FILE DOES NOT VERIFY AGAINST THE TREE:\n%s' % out[-2500:])
    return {'claims_path': out_path, 'n_claims': len(cl), 'verified': not ctx.opts.dry_run,
            'activation': activation}


# ================================================================================ STEP 9 — COMMIT
def _git_commit(ctx, rel_paths, message, skip_if_unchanged=False):
    """THE ONE PLACE THIS PACKAGE MAKES A COMMIT. Explicit paths, both verbs, no sweep.

    Process law P8: "Every commit stages named paths. No `git add -A`, no sweep, no bare
    `git commit`." Every commit the lander makes — the final landing commit, and the round lander's
    two INPUT commits (the sheet re-cut and the owner's score file) — comes through here, so the law
    is asserted in one function rather than three times over.

    THE SHA IS RECORDED ON `ctx.commits_made`, and that is what makes a mid-flight commit safe to
    abort: `txn._abort` rewinds exactly the commits this landing created and no others, before the
    carrier restore runs. A landing that committed and then failed must leave no commit behind, or
    the abort's byte-exactness claim stops at the working tree and quietly excludes history.

    `skip_if_unchanged` IS FOR AN INPUT COMMIT AND NOTHING ELSE, and it is a MEASUREMENT, not a
    shrug: after the explicit `git add`, the index is asked whether those exact paths carry a staged
    change, and only a measured NOTHING returns None — with the reason printed. It exists because
    `git commit -m … -- <unchanged paths>` exits 1 ("nothing added to commit"), which turned a seat
    who had already committed the owner's score file into a step-3 halt (R24 rehearsal §3.1, RUN C).
    An OUTPUT commit never gets it: a landing step that believes it wrote something and staged
    nothing is a defect, and it must still die where it stands.
    """
    rel_paths = sorted(set(rel_paths))
    if not rel_paths:
        return None
    ctx.log('explicit paths (%d):' % len(rel_paths))
    for rel in rel_paths:
        ctx.log('    %s' % rel)
    if ctx.opts.dry_run or ctx.opts.no_commit:
        ctx.log('--%s: not committing.' % ('dry-run' if ctx.opts.dry_run else 'no-commit'))
        return None
    rc, out = ctx.run(['git', 'add', '--'] + rel_paths)
    if rc != 0:
        raise StepError('git add failed: %s' % out)
    if skip_if_unchanged:
        rc, staged = ctx.run(['git', 'diff', '--cached', '--name-only', '--'] + rel_paths)
        if rc != 0:
            raise StepError('cannot read the index for %s: %s' % (rel_paths, staged))
        if not staged.strip():
            ctx.log('NOTHING TO COMMIT: every named path is already committed at this content. '
                    'The inputs of record are in the tree, which is what this commit exists to '
                    'ensure; no empty commit is manufactured to say so.')
            return None
    rc, out = ctx.run(['git', 'commit', '-m', message, '--'] + rel_paths)
    if rc != 0:
        raise StepError('git commit failed: %s' % out)
    rc, head = ctx.run(['git', 'rev-parse', 'HEAD'])
    if rc != 0:
        raise StepError('cannot read HEAD after the commit')
    sha = head.strip()
    ctx.commits_made.append(sha)
    ctx.log('committed %s' % sha[:12])
    return sha


# ============================================================== ROUND STEP — THE SHEET / DATA COMMIT
def _sheet_facts(ctx, rel):
    """The three facts the ORDER 41 / ORDER 42 guards assert, measured THE ENGINE'S OWN WAY.

    md5 of the raw bytes; rows = `csv.DictReader` over the utf-8 decode of the file's own lines;
    injured=Y = rows whose `injured` cell strips-and-uppers to 'Y'. Character for character what
    `_merged_recover.py`'s ORDER 41 block does (and ORDER 42 after it), because a gate that measured
    the sheet a NEARLY identical way would pass a file the build then halts on — which is the whole
    failure mode ERRATUM E1b records for a hand-rolled decode.
    """
    import csv
    raw = open(_p(ctx, rel), 'rb').read()
    rows = list(csv.DictReader(raw.decode('utf-8').splitlines()))
    ys = [r for r in rows if (r.get('injured') or '').strip().upper() == 'Y']
    return hashlib.md5(raw).hexdigest(), len(rows), len(ys)


SHEET_PIN_REL = 'data/sheet_pins.json'

#: The owner's identity rulings on export display names. It is an INPUT OF RECORD, written by the
#: SEAT on the owner's word and committed by `catchup_preflight` beside the score file — so it is
#: named ONCE, here, and read by both the commit and `txn.Ctx.declared_dirt` (the R24 rehearsal's
#: input-commit pincer, §3.1: what the lander commits is what the lander must expect uncommitted).
CATCHUP_OVERRIDES_REL = 'engine/rl_after/ingestion/catchup_identity_overrides.json'


def _replace_json_scalar(raw, key, old, new, where):
    """Replace ONE `"key": <old>` with `"key": <new>`, textually, or refuse.

    KEY-ANCHORED, NOT VALUE-ANCHORED. `pins` can replace a bare old value in `expected_boot.json`
    because it asserts that value occurs exactly once. In the sheet declaration it does not: the
    `provenance` prose quotes the md5 and the row count in its own sentence ("rows unchanged at 219,
    md5 b26798c3... -> 21361291f26d..."). A bare-value replacement would either refuse a legitimate
    re-cut for non-uniqueness or, worse, rewrite the history sentence.

    BOTH JSON ESCAPINGS ARE TRIED, and that is a defect measured out of this function rather than
    reasoned about. `json.dumps` escapes non-ASCII by default, so the em dash in the declaration's
    own provenance sentence serialises as `\\u2014` while the file on disk carries the literal
    character. The first draft matched zero times and halted a legitimate re-cut. Trying
    `ensure_ascii=False` first and the escaped form second matches the file whichever convention
    wrote it, and REFUSES unless exactly one match exists either way.
    """
    for enc in (False, True):
        pat = re.compile(r'("%s"\s*:\s*)%s'
                         % (re.escape(key), re.escape(json.dumps(old, ensure_ascii=enc))))
        hits = pat.findall(raw)
        if len(hits) == 1:
            return pat.sub(lambda m: m.group(1) + json.dumps(new, ensure_ascii=enc), raw, count=1)
        if len(hits) > 1:
            raise StepError('the "%s" declaration occurs %d times in %s; refusing a non-unique '
                            'replacement' % (key, len(hits), where))
    raise StepError('the "%s" declaration is not locatable in %s under either JSON escaping. The '
                    'lander will not reformat a file it cannot edit surgically.' % (key, where))


def sheet(ctx):
    """THE SHEET / DATA COMMIT, in PACKAGE 3a's form — and `land round` is the pin file's SOLE WRITER.

    PLAN_v6 3a put the sheet md5 + row/injured-Y counts into ONE data file, `data/sheet_pins.json`,
    with "the round lander as sole writer once 2b lands". This step is that sole writer. Until it
    existed the writer was the amended R23 runbook's manual path (ERRATUM E7); that path is now the
    documented fallback, retired for this act type on the owner's word (2a.4 — an unexercised
    fallback is fake safety).

    WHAT IT DOES WHEN NO RE-CUT IS DECLARED, WHICH IS MOST WEEKS: it MEASURES the sheet and asserts
    the declaration already describes it, and writes nothing. That is not a formality. A drifted
    sheet halts the board regen INSIDE the staged transaction (ORDER 41 first, ORDER 42 after it),
    and the whole point of a preflighting lander is that a halt which is knowable before anything is
    armed happens before anything is armed.

    WHAT IT DOES WHEN A RE-CUT IS DECLARED: the seat re-cuts the owner's sheet on the owner's word —
    the lander never authors owner data — and this step
      * asserts the prereg-lite exists (3a's review-forcing step: predicted md5 + row/injured-Y
        counts + disclosed movers, committed WITH the data change);
      * MEASURES the sheet and asserts every measured fact equals the PREDICTED one. Predicted
        first, measured after: "a re-cut whose measured facts are not the disclosed ones is a halt
        and a report, not a note";
      * writes the three MEASURED values into the declaration textually — the same surgical
        replacement `pins` uses, so every note field, key order and byte of whitespace survives;
      * commits sheet + declaration + prereg-lite as ONE explicit-path commit;
      * and asserts `engine_head` DID NOT MOVE across that commit. That assertion is the entire
        effect 3a bought: engine_head moves if and only if code changed. "ENGINE_HEAD MOVING ON A
        SHEET UPDATE IS A RED, NOT A CHORE."
    """
    ctx.fault_point('sheet')
    pins_raw = open(_p(ctx, SHEET_PIN_REL), encoding='utf-8').read()
    pins = json.loads(pins_raw)
    sheet_rel = pins.get('sheet_path')
    if not sheet_rel:
        raise StepError('%s names no sheet_path. A pin declaration with a hole in it pins nothing.'
                        % SHEET_PIN_REL)
    md5_now, rows_now, y_now = _sheet_facts(ctx, sheet_rel)
    ctx.log('sheet         %s' % sheet_rel)
    ctx.log('  MEASURED (never typed): md5=%s rows=%d injured_y=%d' % (md5_now, rows_now, y_now))
    ctx.log('  PINNED                : md5=%s rows=%s injured_y=%s'
            % (pins.get('sheet_md5'), pins.get('sheet_rows'), pins.get('sheet_injured_y')))

    declared = ctx.spec.get('sheet')
    engine_head_before = PIN_MEASURERS['engine_head'](ctx)

    if not declared:
        bad = [k for k, v in (('sheet_md5', md5_now), ('sheet_rows', rows_now),
                              ('sheet_injured_y', y_now)) if str(pins.get(k)) != str(v)]
        if bad:
            raise StepError(
                'THE SHEET AND ITS DECLARATION DISAGREE ON %s, and this act declares no re-cut.\n'
                'A drifted sheet HALTS the board regen inside the staged transaction — ORDER 41 '
                'first, then ORDER 42 — so it halts HERE instead, before anything is armed. Either '
                'declare the re-cut (spec.sheet, with its prereg-lite) or find out who moved the '
                'sheet without moving its pins.' % bad)
        ctx.log('the declaration describes the sheet on disk. NO RE-CUT DECLARED — this step writes '
                'nothing, and `land round` remains the pin file\'s sole writer by not writing.')
        return {'recut': False, 'sheet_md5': md5_now, 'sheet_rows': rows_now,
                'sheet_injured_y': y_now, 'commit': None}

    prereg_lite = declared['prereg_lite']
    if not os.path.isfile(_p(ctx, prereg_lite)):
        raise StepError('the prereg-lite %s does not exist. PLAN_v6 3a: a data change keeps a '
                        'review-forcing step, and it is committed WITH the data change.' % prereg_lite)
    pred = declared['predicted']
    ctx.log('  PREDICTED (prereg-lite %s): md5=%s rows=%s injured_y=%s'
            % (prereg_lite, pred.get('sheet_md5'), pred.get('sheet_rows'),
               pred.get('sheet_injured_y')))
    ctx.log('  owner word: %s' % declared.get('owner_word'))
    ctx.log('  disclosed movers: %s' % declared.get('disclosed_movers'))
    mismatch = [(k, pred.get(k), v) for k, v in (('sheet_md5', md5_now), ('sheet_rows', rows_now),
                                                 ('sheet_injured_y', y_now))
                if str(pred.get(k)) != str(v)]
    if mismatch:
        raise StepError(
            'THE RE-CUT IS NOT THE RE-CUT THAT WAS PREDICTED:\n    %s\nThe prereg-lite is corrected '
            'against the tree, never the tree against the prereg-lite, and a re-cut whose measured '
            'facts are not the disclosed ones is a HALT AND A REPORT.'
            % '\n    '.join('%s: predicted %s, measured %s' % m for m in mismatch))

    new_raw = pins_raw
    moved = []
    for k, v in (('sheet_md5', md5_now), ('sheet_rows', rows_now), ('sheet_injured_y', y_now)):
        old = pins.get(k)
        if str(old) == str(v):
            continue
        new_raw = _replace_json_scalar(new_raw, k, old, v, SHEET_PIN_REL)
        moved.append(k)
        ctx.log('  %-16s %s -> %s' % (k, old, v))
    if not moved:
        raise StepError('a sheet re-cut is DECLARED and the declaration already describes the sheet. '
                        'A re-cut that moves no pin is a re-cut nobody needed to authorise.')
    for k, v in (('pinned_at', ctx.spec.get('date')),
                 ('provenance', declared.get('provenance'))):
        if v and pins.get(k) is not None and str(pins.get(k)) != str(v):
            new_raw = _replace_json_scalar(new_raw, k, pins[k], v, SHEET_PIN_REL)
            moved.append(k)
    after = json.loads(new_raw)
    unexpected = sorted(k for k in set(pins) | set(after)
                        if pins.get(k) != after.get(k) and k not in moved)
    if unexpected:
        raise StepError('bytes beyond the declared pin values changed in %s: %s'
                        % (SHEET_PIN_REL, unexpected))
    ctx.log('  fields that moved in %s: %s' % (SHEET_PIN_REL, moved))

    if not ctx.opts.dry_run:
        tmp = _p(ctx, SHEET_PIN_REL) + '.landing_tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            fh.write(new_raw)
        os.replace(tmp, _p(ctx, SHEET_PIN_REL))
        back = json.load(open(_p(ctx, SHEET_PIN_REL), encoding='utf-8'))
        if (str(back.get('sheet_md5')), int(back['sheet_rows']), int(back['sheet_injured_y'])) != \
                (md5_now, rows_now, y_now):
            raise StepError('the sheet pins did not take')
        ctx.log('WRITTEN and re-read.')

    sha = _git_commit(ctx, [sheet_rel, SHEET_PIN_REL, prereg_lite],
                      ctx.spec.get('sheet_commit_message')
                      or ('%s — THE SHEET RE-CUT: the owner input and its ONE pin declaration, '
                          'one commit, no engine file touched' % ctx.spec['act']))
    head_after = PIN_MEASURERS['engine_head'](ctx)
    if head_after != engine_head_before:
        raise StepError(
            'ENGINE_HEAD MOVED ON A SHEET UPDATE (%s -> %s). That is a RED, NOT A CHORE: the whole '
            'effect PACKAGE 3a bought is that engine_head moves if and only if CODE changed. This '
            'commit touched the engine and the act is not the data act it claims to be. Stop and '
            'find out why; do not restamp it forward.' % (engine_head_before, head_after))
    ctx.log('engine_head UNMOVED across the sheet commit: %s  (the 3a property, asserted)'
            % head_after)
    return {'recut': True, 'sheet_md5': md5_now, 'sheet_rows': rows_now, 'sheet_injured_y': y_now,
            'moved': moved, 'commit': sha, 'engine_head': head_after,
            'prereg_lite': prereg_lite}


# ============================================================== ROUND STEP — THE OWNER'S SCORE FILE
def scores(ctx):
    """The owner's file of record, asserted — never placed, never edited, never cleaned up.

    The runbook's step 0 is "place the owner's file, byte-unmodified -> scores/R<N>.csv (record its
    md5 + sha256 before anything else)". The placing is the seat's; the RECORDING is this step's,
    and it is an assertion rather than a note: the spec declares the md5 and sha256 of the file the
    act was written against, and a file on disk that is not that file halts here.

    "Send the file exactly as your league site gives it — do not clean it up." The lander cannot
    clean it up: it opens it 'rb', hashes it, and never writes to it.

    THE IDENTITY OVERRIDES ARE ASSERTED, NEVER AUTHORED. An owner ruling on a name lives in
    `catchup_identity_overrides.json` (the R22 Bailey ruling, the R23 WBD binding), and it is the
    SEAT that records the owner's verbatim word there. This step checks that every override the act
    declares is actually present and reads back the reason each carries — so a landing can never
    quietly invent a binding, and an act that says it needs one cannot proceed without it.
    """
    ctx.fault_point('scores')
    rnd = ctx.spec['round']
    sc = rnd.get('scores')
    if not sc:
        ctx.log('no scores file declared — this act is a REHEARSAL and applies nothing.')
        return {'scores': None, 'rehearsal': True}

    path = _p(ctx, sc['path'])
    if not os.path.isfile(path):
        raise StepError('the owner\'s score file is ABSENT at %s. The lander does not create it, '
                        'guess at it, or proceed without it.' % sc['path'])
    raw = open(path, 'rb').read()
    got_md5 = hashlib.md5(raw).hexdigest()
    got_sha = hashlib.sha256(raw).hexdigest()
    ctx.log('scores file   %s  (%d bytes)' % (sc['path'], len(raw)))
    ctx.log('  md5    %s   %s' % (got_md5, 'OK' if got_md5 == sc['md5'] else '*** != declared %s'
                                  % sc['md5']))
    ctx.log('  sha256 %s   %s' % (got_sha, 'OK' if got_sha == sc['sha256'] else
                                  '*** != declared %s' % sc['sha256']))
    if got_md5 != sc['md5'] or got_sha != sc['sha256']:
        raise StepError('THE SCORE FILE ON DISK IS NOT THE FILE THIS ACT DECLARES (md5 %s vs %s). '
                        'The owner\'s input is an INPUT OF RECORD; the act is written against a '
                        'specific file and the lander refuses a different one.' % (got_md5, sc['md5']))

    ov_rel = CATCHUP_OVERRIDES_REL
    ov = json.load(open(_p(ctx, ov_rel), encoding='utf-8'))
    entries = ov if isinstance(ov, list) else (ov.get('overrides') or [])
    by_name = {e.get('name'): e for e in entries if isinstance(e, dict)}
    declared_ov = list(rnd.get('identity_overrides') or ())
    for name in declared_ov:
        e = by_name.get(name)
        if not e:
            raise StepError('the act declares an identity override for %r and '
                            '%s carries none. IdentityOverrides._by_name is keyed by the EXACT '
                            'display string (ERRATUM E2): a rule under a different name is never '
                            'consulted. The lander asserts bindings; it never authors one.'
                            % (name, ov_rel))
        ctx.log('  override %-24s -> %-22s rule=%-9s rounds=%s'
                % (name, e.get('stable_key'), e.get('rule'), e.get('applies_to_rounds')))
        ctx.log('      reason: %s' % str(e.get('reason'))[:150])
    ctx.log('%d declared override(s), all present; %d in the file overall'
            % (len(declared_ov), len(by_name)))
    return {'scores': sc['path'], 'md5': got_md5, 'sha256': got_sha, 'bytes': len(raw),
            'overrides_declared': declared_ov, 'overrides_in_file': sorted(by_name)}


# ==================================================================== ROUND STEP — CATCH-UP PREFLIGHT
def catchup_preflight(ctx):
    """The read-only preflight, run for real, plus the ONE check the runbook says to run before it.

    `round_entry catchup --file N=<file>` without `--approve` is read-only by contract ("PREFLIGHT —
    read-only, writes nothing. Run this first, always") and stops at "NOT APPROVED — nothing
    applied." This step runs it, and requires FOUR things of the result rather than one:

      1. `PREFLIGHT CLEAN` — every name resolves to a stable identity, nothing ambiguous or
         duplicate. Anything else and the advance never arms.
      2. the round is NOT already applied. The preflight prints "(already applied — will be SKIPPED
         on resume)" and still reports CLEAN, which is correct for a resume and wrong for an act
         that claims to be advancing the season.
      3. the counts match the prereg's round_expected — listed, resolved, absent/DNP and the score
         file's own sha256, asserted against what the parser of record actually read.
      4. THE H2 CHECK: no `injured=Y` player on the pinned owner sheet appears in the score file.
         ORDER 42 requires every injured-marked row's `games_2026` to equal the store's, and an
         advance increments `games` for every listed player — so an injured-marked player who
         played desynchronises the sheet and HALTS THE BOARD REGEN INSIDE THE TRANSACTION. The
         runbook rated it "a coin flip on the owner's file"; at R23 it landed. It is cheap, it is
         read-only, and it turns a mid-transaction halt into a pre-arming one.

    THE PARSER OF RECORD READS THE SCORE FILE, never a hand-rolled decode. ERRATUM E1b deleted the
    snippet that used `.decode("utf-8", errors="replace")` and mangled 16 of 411 names on exactly the
    file it was written to check — "a check that silently mis-reads 16 of 411 rows is worse than no
    check". `footywire_parser.decode_bytes` handles BOM / utf-8 / cp1252 by spec.

    THEN IT COMMITS THE INPUTS — the score file and the override record — as their own explicit-path
    commit, so the owner's input of record enters the tree BEFORE anything is armed and the advance's
    own commit carries outputs only. That is the R23 shape (ACT 2, commit `27458ad`).
    """
    ctx.fault_point('catchup_preflight')
    rnd = ctx.spec['round']
    sc = rnd.get('scores')
    if not sc:
        ctx.log('no scores file — nothing to preflight. (REHEARSAL.)')
        return {'ran': False, 'rehearsal': True}
    n = int(rnd['number'])

    # ---- 4. THE H2 CHECK, before the tool is even asked -------------------------------------------
    hits = _injured_listed(ctx, sc['path'])
    ctx.log('injured=Y players listed in R%d: %d %s' % (n, len(hits), hits))
    if hits:
        raise StepError(
            'ORDER 42 WILL HALT THE ADVANCE. %d player(s) marked injured=Y on the pinned owner '
            'sheet appear in the score file: %s. The advance increments games_2026 for every listed '
            'player, so the sheet and the store would disagree and the board regen halts INSIDE the '
            'staged transaction. The remedy is the owner-worded re-cut (R23 runbook §4 H2 / ERRATUM '
            'E7), declared as spec.sheet with its prereg-lite — not a weakened guard.'
            % (len(hits), hits))

    rc, out = ctx.run(['python3', 'tools/round_entry/round_entry.py', 'catchup',
                       '--file', '%d=%s' % (n, sc['path'])], timeout=1800)
    ctx.write_evidence('08_preflight_r%d.txt' % n, out)
    for ln in out.strip().splitlines():
        ctx.log('  %s' % ln)
    if rc != 0:
        raise StepError('the catch-up preflight did not complete (exit %s):\n%s' % (rc, out[-2000:]))
    if 'PREFLIGHT CLEAN' not in out:
        raise StepError('THE PREFLIGHT IS NOT CLEAN, so nothing arms. Resolve the identity issues '
                        'it names — with the owner\'s word, recorded in '
                        'catchup_identity_overrides.json, never by editing the score file:\n%s'
                        % out[-2000:])
    if 'already applied' in out:
        raise StepError('ROUND %d IS ALREADY APPLIED. The preflight reports it and still says CLEAN, '
                        'which is right for a RESUME and wrong for an act that claims to be '
                        'advancing the season. The dedup ledger would skip it and this landing would '
                        'certify a round it did not apply.' % n)

    exp = (ctx.spec['prereg'].get('round_expected') or {})
    got = _parse_preflight(out, n)
    ctx.log('preflight counts, MEASURED: %s' % json.dumps(got, sort_keys=True))
    bad = []
    for k, ek in (('listed', 'listed'), ('resolved', 'resolved'), ('absent_dnp', 'absent_dnp')):
        if got.get(k) is not None and int(exp.get(ek)) != int(got[k]):
            bad.append('%s: prereg %s, preflight %s' % (k, exp.get(ek), got[k]))
    if str(exp.get('scores_sha256'))[:12] != str(got.get('sha256'))[:12]:
        bad.append('scores_sha256: prereg %s, preflight %s' % (exp.get('scores_sha256'),
                                                               got.get('sha256')))
    if int(exp.get('round')) != n:
        bad.append('round: prereg %s, act %s' % (exp.get('round'), n))
    if bad:
        raise StepError('THE PREFLIGHT DOES NOT MATCH THE PREREG:\n    %s\nThe prediction is an '
                        'INPUT to this lander; a landing that accepted its own preflight as the '
                        'answer would assert nothing at all.' % '\n    '.join(bad))
    ctx.log('PREREG MET: listed/resolved/absent-DNP and the score file sha256 all as predicted.')

    # THE INPUT COMMIT. Both paths are DECLARED DIRT at step 0 (`txn.Ctx.declared_dirt`), so the
    # ordinary shape is: the seat places the owner's file, the lander finds it uncommitted, and this
    # commit is where it enters the tree. `skip_if_unchanged` covers the OTHER lawful shape — a seat
    # who pre-committed the inputs, which is the rehearsal's documented interim path — where there
    # is legitimately nothing to commit and a halt would be the machine punishing the seat for
    # having already done the thing the machine wanted done.
    sha = _git_commit(ctx, [sc['path'], CATCHUP_OVERRIDES_REL],
                      ctx.spec.get('scores_commit_message')
                      or ('%s — THE OWNER\'S SCORES AND THE BINDINGS: preflight CLEAN %s/%s, '
                          'nothing applied' % (ctx.spec['act'], got.get('listed'),
                                               got.get('resolved'))),
                      skip_if_unchanged=True)
    return {'ran': True, 'clean': True, 'counts': got, 'commit': sha,
            'injured_listed': hits}


def _injured_listed(ctx, scores_rel):
    """The H2 intersection: injured=Y on the pinned sheet ∩ listed in the score file. Parser of record."""
    import csv
    import re as _re
    fp = _load(ctx, 'footywire_parser', 'engine/rl_after/ingestion/footywire_parser.py')
    norm = lambda s: _re.sub(r'[^a-z0-9]+', '-', str(s).strip().lower().replace('’', "'")).strip('-')
    pins = json.load(open(_p(ctx, SHEET_PIN_REL), encoding='utf-8'))
    with open(_p(ctx, pins['sheet_path']), encoding='utf-8') as fh:
        inj = {norm(r['player']) for r in csv.DictReader(fh)
               if (r.get('injured') or '').strip().upper() == 'Y'}
    parsed = fp.parse_round_file(_p(ctx, scores_rel))
    rows = parsed['rows'] if isinstance(parsed, dict) else parsed
    names = {norm(r[0] if isinstance(r, (list, tuple)) else r.get('name')) for r in rows}
    return sorted(names & inj)


def _parse_preflight(out, n):
    """Read the preflight's own verdict line. The tool's numbers, not a recount of the file."""
    got = {}
    m = re.search(r'^\s*R%d\s+enc=(\S+)\s+listed/played=(\d+)\s+resolved=(\d+)\s+listed-zero=(\d+)'
                  r'\s+absent/DNP=(\d+)\s+sha256\s+(\S+)' % n, out, re.M)
    if m:
        got = {'encoding': m.group(1), 'listed': int(m.group(2)), 'resolved': int(m.group(3)),
               'listed_zero': int(m.group(4)), 'absent_dnp': int(m.group(5)), 'sha256': m.group(6)}
    return got


# ======================================================================== ROUND STEP — THE ADVANCE
def advance(ctx):
    """THE ARMED CATCH-UP: one sequential staged transaction, and ADVANCE-REPIN inside it.

    THE LANDER WRAPS THE STAGED MACHINERY; IT DOES NOT REIMPLEMENT ANY OF IT. `staged_apply` runs
    STAGE -> VALIDATE -> ATOMIC SWAP with rollback and crash recovery, and `_stage_sibling` (step c3)
    runs the repin INSIDE the same transaction — so the balanced board and the FV reference vector
    move in the SAME COMMIT as the store, built and compared, never pinned to an expectation. That
    is ADVANCE-REPIN, it is proven, and a lander that re-implemented it would own a second copy of
    the one thing in this estate that must not have two.

    ARMING IS AN OWNER WORD (LAW 10c). Both halves of the gate are armed for this run only, from the
    act spec, which carries the owner's verbatim word beside the token. The lander composes neither
    and there is no code edit: `INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=<token>`.

    EVERY POSTCONDITION IS READ OFF THE TOOL'S OWN APPLIED LINE and asserted against the prereg or
    the tree: the store and board moved, the round is the declared one, Guard 5 is green, the
    histories reach round N, finalization is FINALIZED (not INCOMPLETE — exit 6 is a halt here, not
    a note), the movers went to the UI, and the dedup ledger grew by exactly the predicted number of
    triples with no duplicate.

    ON A DECLARED REHEARSAL IT ARMS NOTHING AND ASSERTS THE TREE HELD STILL. That is what makes the
    no-op dry run a real proof rather than a skipped step: the whole sequence runs, and the one step
    that could move the board proves it did not.
    """
    ctx.fault_point('advance')
    rnd = ctx.spec['round']
    n = int(rnd['number'])
    boot_before = ctx.facts['base']['expected_boot']
    sc = rnd.get('scores')

    if not sc:
        boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))
        held = {'board': md5(_p(ctx, 'data', 'rl_build', 'rl_app_data.json')),
                'store': md5(_p(ctx, 'engine', 'rl_after', 'rl_model_data.json')),
                'as_of_round': boot.get('as_of_round')}
        ctx.log('REHEARSAL — nothing is armed and nothing is applied.')
        for k, v in sorted(held.items()):
            was = boot_before.get(k)
            ctx.log('  %-12s %-34s %s' % (k, v, 'HELD' if str(was) == str(v) else
                                          '*** MOVED from %s ***' % was))
        moved = [k for k, v in held.items() if str(boot_before.get(k)) != str(v)]
        if moved:
            raise StepError('a REHEARSAL moved %s. A no-op that moves the board is not a no-op.'
                            % moved)
        if int(held['as_of_round']) != n:
            raise StepError('the act declares round %d and the tree is at round %s. A rehearsal '
                            'holds the round it is standing on.' % (n, held['as_of_round']))
        return {'applied': False, 'rehearsal': True, 'round': n, **held}

    arming = rnd['arming']
    ctx.log('ARMED BY OWNER WORD (law 10c): %s' % arming['owner_word'])
    ctx.log('  arming both halves for this run only, no code edit: %s'
            % ' '.join('%s=%s' % (k, '<token>' if 'APPLY' == k[-5:] else v)
                       for k, v in sorted(arming['env'].items())))
    if ctx.opts.dry_run:
        ctx.log('--dry-run: THE ADVANCE IS NOT ARMED AND NOT RUN.')
        return {'applied': False, 'dry_run': True, 'round': n}

    ledger_rel = 'engine/rl_after/ingestion/applied_rounds_ledger.json'
    led_before = _ledger_triples(ctx, ledger_rel)
    env = dict(arming['env'])
    argv = ['python3', 'tools/round_entry/round_entry.py', 'catchup',
            '--file', '%d=%s' % (n, sc['path']), '--approve']
    t0 = time.time()
    rc, out = ctx.run(argv, timeout=ctx.spec.get('advance_timeout_s', 7200), env_overrides=env)
    el = time.time() - t0
    ctx.write_evidence('09_armed_r%d.txt' % n, '$ %s\n\n%s\n[exit %s]' % (' '.join(argv), out, rc))
    for ln in out.strip().splitlines():
        ctx.log('  %s' % ln)
    ctx.log('armed run     exit=%s  (%.1fs)' % (rc, el))
    if rc != 0:
        raise StepError('THE ARMED ADVANCE DID NOT COMPLETE (exit %s). Exit 3 = the store-write gate '
                        'was not armed; 4 = an incomplete transaction is open (round_entry recover); '
                        '6 = finalization incomplete (round_entry finalize --round %d). The staged '
                        'transaction rolls itself back; this lander then restores every carrier.\n%s'
                        % (rc, n, out[-2500:]))

    m = re.search(r'^\s*R%d\s+store\s+(\w+)->(\w+)\s+board\s+(\w+)->(\w+)\s+players=(\d+)\s+'
                  r'guard5=(\w+)\s+hist=\[([^\]]*)\]\s+final=(\w+)\s+movers->UI=(\d+)' % n, out, re.M)
    if not m:
        raise StepError('the applied line for R%d is not in the tool\'s output. A landing does not '
                        'infer a verdict it cannot read:\n%s' % (n, out[-2000:]))
    facts = {'applied': True, 'round': n, 'store_before': m.group(1), 'store_after': m.group(2),
             'board_before': m.group(3), 'board_after': m.group(4),
             'players_applied': int(m.group(5)), 'guard5': m.group(6),
             'history_rounds': [int(x) for x in m.group(7).replace(' ', '').split(',') if x],
             'finalization': m.group(8), 'movers_ui_rows': int(m.group(9)),
             'elapsed_s': round(el, 1)}
    if facts['guard5'] != 'True':
        raise StepError('Guard 5 is not green on the applied round (guard5=%s). NEVER BOOT ON AN '
                        'UNVERIFIED STORE (process law P2).' % facts['guard5'])
    if facts['finalization'] != 'FINALIZED':
        raise StepError('finalization is %r, not FINALIZED. A re-derivable output failed or was '
                        'blocked; nothing was rolled back. Finish it (round_entry finalize --round '
                        '%d) — an unfinalized round is not a landed round.'
                        % (facts['finalization'], n))
    if n not in facts['history_rounds']:
        raise StepError('the histories do not reach round %d: %s' % (n, facts['history_rounds']))

    # ---- the tree, re-measured, against the tool's own line and against the prereg ---------------
    boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))
    board_now = md5(_p(ctx, 'data', 'rl_build', 'rl_app_data.json'))
    store_now = md5(_p(ctx, 'engine', 'rl_after', 'rl_model_data.json'))
    if not board_now.startswith(facts['board_after']):
        raise StepError('the published board %s is not the board the advance reports (%s)'
                        % (board_now, facts['board_after']))
    if not store_now.startswith(facts['store_after']):
        raise StepError('the store %s is not the store the advance reports (%s)'
                        % (store_now, facts['store_after']))
    if str(boot.get('board')) != board_now or str(boot.get('store')) != store_now:
        raise StepError('expected_boot does not name the tree the advance produced (board %s/%s, '
                        'store %s/%s)' % (boot.get('board'), board_now, boot.get('store'), store_now))
    if int(boot.get('as_of_round')) != n:
        raise StepError('expected_boot.as_of_round is %s after an advance to round %d'
                        % (boot.get('as_of_round'), n))
    season = json.load(open(_p(ctx, 'data', 'season_state.json'), encoding='utf-8'))
    if int(season.get('as_of_round')) != n:
        raise StepError('season_state.as_of_round is %s after an advance to round %d'
                        % (season.get('as_of_round'), n))
    if str(ctx.spec['prereg'].get('board_before')) != facts['board_before'] and \
            not str(ctx.spec['prereg'].get('board_before')).startswith(facts['board_before']):
        raise StepError('the advance started from board %s; the prereg says it starts from %s'
                        % (facts['board_before'], ctx.spec['prereg'].get('board_before')))

    exp = ctx.spec['prereg']['round_expected']
    led_after = _ledger_triples(ctx, ledger_rel)
    delta = led_after['total'] - led_before['total']
    ctx.log('ledger        %d -> %d (+%d), %d triple(s) for R%d, duplicates %d'
            % (led_before['total'], led_after['total'], delta, led_after['for_round'].get(n, 0), n,
               led_after['duplicates']))
    if led_after['duplicates']:
        raise StepError('the dedup ledger holds %d duplicate triple(s) — a round has been '
                        'double-counted' % led_after['duplicates'])
    if int(exp['ledger_before']) != led_before['total'] or int(exp['ledger_delta']) != delta:
        raise StepError('THE LEDGER DOES NOT MATCH THE PREREG: predicted %s + %s, measured %s + %s'
                        % (exp['ledger_before'], exp['ledger_delta'], led_before['total'], delta))
    if delta != facts['players_applied'] or led_after['for_round'].get(n) != facts['players_applied']:
        raise StepError('the ledger grew by %d and %d players were applied' % (delta, facts['players_applied']))
    facts.update({'ledger_before': led_before['total'], 'ledger_after': led_after['total'],
                  'ledger_delta': delta, 'board': board_now, 'store': store_now})
    ctx.log('ROUND %d IS APPLIED. store %s -> %s · board %s -> %s · %d played / %d DNP'
            % (n, facts['store_before'], facts['store_after'], facts['board_before'],
               facts['board_after'], facts['players_applied'],
               int(exp.get('absent_dnp') or 0)))
    return facts


def _ledger_triples(ctx, rel):
    """The dedup ledger, counted: total triples, per-round counts, and duplicates."""
    doc = json.load(open(_p(ctx, rel), encoding='utf-8'))
    trips = doc if isinstance(doc, list) else (doc.get('applied') or doc.get('triples') or
                                               doc.get('entries') or [])
    if isinstance(trips, dict):
        trips = sorted(trips)
    flat = [t if isinstance(t, str) else '|'.join(str(x) for x in t) for t in trips]
    per = {}
    for t in flat:
        parts = t.split('|')
        if len(parts) >= 3 and parts[-1].isdigit():
            per[int(parts[-1])] = per.get(int(parts[-1]), 0) + 1
    return {'total': len(flat), 'for_round': per, 'duplicates': len(flat) - len(set(flat))}


# ============================================================ ROUND STEP — THE GENERATOR-SIDE COPY
def generator_sync(ctx):
    """The generator-side board copy, synced — and DISCLOSED, which is the whole of the ruling.

    `ERRATUM E5`: "engine/rl_after/rl_app_data.json (+ .srcmd5) is the GENERATOR-side copy and the
    transaction does NOT publish to it — round_apply.py:139-141 publishes only to data/rl_build/. R22
    left it stale with every gate green. R23 synced it by hand AND DISCLOSED THE SYNC, because THE
    BAKE and THE D8 ADOPTION both moved the pair in lockstep. Either choice is defensible; the one
    thing that is not is moving it silently."

    So the lander syncs it, in lockstep with its sidecar, and prints both identities before and
    after. The `pins` step's own precondition — published copy, generator copy and BOTH sidecars
    coherent — is the thing this keeps true after an advance, which is why it runs before `contract`
    reads them.

    ON A REHEARSAL IT REFUSES TO WRITE. If the two copies already disagree in an act that moves
    nothing, that is a pre-existing incoherence the act did not create and must not paper over.
    """
    ctx.fault_point('generator_sync')
    pub = _p(ctx, 'data', 'rl_build', 'rl_app_data.json')
    gen = _p(ctx, 'engine', 'rl_after', 'rl_app_data.json')
    pm, gm = md5(pub), md5(gen)
    ps, gs = md5(pub + '.srcmd5'), md5(gen + '.srcmd5')
    ctx.log('published board  %s   sidecar %s' % (pm, ps))
    ctx.log('generator board  %s   sidecar %s' % (gm, gs))
    if pm == gm and ps == gs:
        ctx.log('the generator-side copy is already the published board. Nothing to sync.')
        return {'synced': False, 'board': pm}
    if is_no_op(ctx.spec):
        raise StepError('the generator-side copy (%s) is not the published board (%s) and this act '
                        'is a declared no-op. A rehearsal does not repair a tree it did not break; '
                        'this incoherence pre-dates the act and is reported, not absorbed.' % (gm, pm))
    if ctx.opts.dry_run:
        ctx.log('--dry-run: would sync the generator copy %s -> %s (DISCLOSED).' % (gm, pm))
        return {'synced': 'dry-run', 'board': pm}
    for src, dst in ((pub, gen), (pub + '.srcmd5', gen + '.srcmd5')):
        with open(src, 'rb') as s, open(dst, 'wb') as d:
            d.write(s.read())
    if md5(gen) != pm or md5(gen + '.srcmd5') != ps:
        raise StepError('the generator-side sync did not take')
    ctx.log('SYNCED, byte-identical, and DISCLOSED: generator board %s -> %s, sidecar %s -> %s'
            % (gm, pm, gs, ps))
    return {'synced': True, 'board': pm, 'was': gm}


# ================================================================= ROUND STEP — THE DAY-0 REFERENCE
def day0(ctx):
    """The day-0 print reference, regenerated AT THE ADVANCE — its natural home, and only here.

    REGISTER v810, ITEM 1, verbatim on the point: "THE DAY-0 REFERENCE IS STALE FOR R23 ... 63 of 89
    printed prices moved at the R23 clock advance while derived_v0 moved on 0 — the standing
    DAY0_CP.json wants regeneration AT THE R24 ADVANCE (its natural home; the round lander 2b
    inherits it as a step or the advance does it once by hand — DO NOT re-base mid-round)."

    THIS STEP IS HOW "DO NOT RE-BASE MID-ROUND" BECOMES STRUCTURAL rather than remembered: the day-0
    re-base exists in `ROUND_SEQUENCE` and nowhere else. `land lever` has no such step, so a
    mid-round act cannot activate one even if its spec asked.

    IT IS STILL EXPLICIT AND STILL OFF BY DEFAULT — the M1b ruling is not relaxed by giving the
    capability a home: "Day-0 re-basing becomes an explicit, owner-visible, off-by-default input with
    a mandatory printed diff of every moved row — a suite inheriting the capability without the
    judgement re-bases itself green on the first halt."

    AND THE LANDER STILL DOES NOT COMPUTE DAY-0. It runs the GENERATOR — the emitter of record,
    which is where the day-0 law is carried (the R23-era chain: ORDER K's `ok_day0.py` ->
    `fcrb_day0.py` -> `cprb_day0.py` -> `sfx_day0.py`) — then prints the mandatory row diff between
    the standing reference and what the generator produced, and installs. Computing the law here
    would create a second implementation of it beside the emitter, which is the mirrored-pair hazard
    M1b itself warns about.

    THE GENERATOR OF RECORD IS NOW A CARRIED ONE AND IT IS THE DEFAULT — `tools/landing/day0_emit.py`
    (DAY0_GENERATOR), which regenerates the reference from THIS TREE'S board and store, prints the
    full row diff, refuses to write when day-0 is not activated, and is byte-stable across two runs.
    Every emitter before it was ACT-PINNED, and the R24 rehearsal §5 measured the cost: *"there is no
    runnable day-0 emitter for R24 … it reads its board from a named scratch directory that no longer
    exists … and hard-asserts SIX named movers with their exact old and new printed integers. It
    cannot run for R24 as it stands."* An advance that has to author a new emitter before it can fly
    is an advance whose day-0 step is theatre.

    THE SPEC MAY STILL NAME ITS OWN GENERATOR (`day0_rebase.generator`), and an act that supplies the
    regenerated file by other means declares `"generator": []` — an EMPTY list, which is the explicit
    "this act brings its own new_reference" and is distinct from an absent key (= the carried
    emitter). Absent is the default because a defaulted-to-nothing generator is how a day-0 step ends
    up installing whatever happened to be lying at `new_reference`.
    """
    ctx.fault_point('day0')
    d0 = ctx.spec.get('day0_rebase') or {'state': 'off'}
    if str(d0.get('state', 'off')).lower() != 'on':
        ctx.log('day-0 re-base : OFF (default). The standing reference is NOT regenerated by this '
                'advance, and the M1b ruling is why: automation never re-bases itself green.')
        ctx.log('  (register v810 item 1: the reference wants regeneration AT an advance. Activating '
                'it is an owner-visible input, not a default.)')
        return 'off'
    gen = d0.get('generator')
    if gen is None:
        gen = _carried_day0_generator(ctx)
        ctx.log('day-0 generator: none declared — THE CARRIED EMITTER (%s) is the default.'
                % DAY0_GENERATOR)
    elif not gen:
        ctx.log('day-0 generator: DECLARED EMPTY — this act supplies %s by its own means and the '
                'lander runs no emitter. The diff below is still mandatory.'
                % d0.get('new_reference'))
    if gen:
        ctx.log('day-0 generator (the emitter of record, run as a child): %s' % ' '.join(gen))
        if ctx.opts.dry_run:
            ctx.log('--dry-run: the generator is not run.')
        else:
            rc, out = ctx.run(list(gen), timeout=d0.get('generator_timeout_s', 5400))
            ctx.write_evidence('day0_generator.txt', out)
            for ln in out.strip().splitlines()[-40:]:
                ctx.log('  %s' % ln)
            if rc != 0:
                raise StepError('the day-0 generator failed (exit %s). The lander does not compute '
                                'day-0 and will not stand in for its emitter:\n%s' % (rc, out[-2000:]))
    return _day0(ctx)


#: THE CARRIED EMITTER OF RECORD. Named once, here, so the step, the spec template and the self-test
#: all point at the same file and a rename cannot leave one of them behind.
DAY0_GENERATOR = 'tools/landing/day0_emit.py'


def _carried_day0_generator(ctx):
    """The default generator argv: the carried emitter, pointed at THIS act's spec and THIS tree.

    It is handed the act spec rather than a set of flags on purpose. The emitter's first refusal is
    the M1b activation check, and a check that reads its own activation off the same document the
    owner's word is recorded in cannot be talked out of it by a caller's argv.
    """
    spec_rel = ctx.spec.get('_spec_rel')
    if not spec_rel:
        raise StepError('the act spec\'s own path is not recorded on this run, so the carried day-0 '
                        'emitter cannot be handed the document that activates it. Declare '
                        'day0_rebase.generator explicitly, or run through `tools/land`.')
    spec_abs = os.path.normpath(os.path.join(ctx.root, spec_rel))
    return [sys.executable, _p(ctx, DAY0_GENERATOR), '--spec', spec_abs, '--root', ctx.root]


# ==================================================================== ROUND STEP — THE MOVERS PAGE
def movers_page(ctx):
    """The owner-facing movers page for this round, rendered through the frozen template.

    PLAN_v6 1d, a free habit needing no ruling: "rendered board/movers page delivered to the owner at
    every round". This is that delivery, and it is a step of the transaction rather than an errand
    afterwards, because a page rendered later is a page rendered from a tree that has moved.

    A SEAT INJECTS DATA. A SEAT NEVER INJECTS LAYOUT. Every value comes out of the movers report of
    record, written INSIDE the advance transaction by round_finalize/round_movers; nothing is
    recomputed here and no markup is authored here. `slots.render` fills the frozen skeleton
    `ui/templates/movers.html` and REFUSES an absent slot, a None, an empty string or a dash
    sentinel — and `score` is passed as `slots.ABSENT` for the players who did not play, which is
    the honest use of the sentinel the slot contract exists to force.

    THE FENCES ARE THE POINT, and they are the ones the R23 renderer carried: the report must name
    the board and store the manifest names, its baseline must be the stored point IMMEDIATELY BEFORE
    this round (rule M0, asserted through `round_movers.previous_point`, never assumed), and that
    baseline must sit at as_of_round N-1. A page that fails any of them is describing a different
    tree than the one that produced it.
    """
    ctx.fault_point('movers_page')
    n = int(ctx.spec['round']['number'])
    rep_rel = 'engine/rl_after/ingestion/movers/movers_R%d.json' % n
    rep_path = _p(ctx, rep_rel)
    if not os.path.isfile(rep_path):
        raise StepError('there is no movers report of record at %s. The page is RENDERED FROM the '
                        'report the advance transaction wrote; it is never composed from the board.'
                        % rep_rel)
    rep = json.load(open(rep_path, encoding='utf-8'))
    boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))
    vh = json.load(open(_p(ctx, 'engine/rl_after/ingestion/value_history.json'), encoding='utf-8'))
    col = {c['id']: c for c in vh['columns']}

    # ---- the fences ------------------------------------------------------------------------------
    #
    # THE BOARD FENCE HAS TWO FORMS AND THE DIFFERENCE IS NOT A LOOPHOLE, IT IS THE TRUTH.
    #
    # Immediately after an advance the report of record names the live board, and the strict form
    # asserts exactly that. But the report is FROZEN ERA HISTORY: out-of-round acts land after it,
    # and every one of them moves the live board while the round's own report stays where it was.
    # On this tree today the R23 report names 7a3f4fe2 and the live board is b3e8da99, three
    # registered out-of-round columns later, and BOTH FACTS ARE CORRECT. A fence that demanded
    # equality unconditionally would be the estate's fifth hand-typed instrument: true the day it was
    # written, a false red the day the tree legitimately moved (process law P4).
    #
    # So the strict form binds when THIS transaction applied the round, and the standing form — which
    # binds always — is a CROSS-ARTIFACT EQUALITY that catches a tampered report either way: the
    # shipped movers bundle's own copy of the round-N report must agree with the report of record on
    # all four identities. Plus the drift, when there is drift, must be EXPLAINED by stored
    # out-of-round points at this round; an unexplained live board still halts.
    fails = []
    if int(rep.get('submitted_round')) != n:
        fails.append('the report is for round %s, not %d' % (rep.get('submitted_round'), n))

    shipped = (_js_obj(_p(ctx, 'ui', 'data', 'movers.js')).get('reports') or {}).get(str(n))
    if not shipped:
        fails.append('the shipped movers bundle carries no report for round %d' % n)
    else:
        for k in ('board_md5_before', 'board_md5_after', 'source_store_md5_before',
                  'source_store_md5_after', 'previous_round'):
            if str(shipped.get(k)) != str(rep.get(k)):
                fails.append('the shipped bundle and the report of record disagree on %s (%s vs %s)'
                             % (k, shipped.get(k), rep.get(k)))

    applied = bool((ctx.facts.get('advance') or {}).get('applied'))
    if applied:
        if rep.get('board_md5_after') != boot['board']:
            fails.append('report board_md5_after %s != manifest board %s'
                         % (rep.get('board_md5_after'), boot['board']))
        if rep.get('source_store_md5_after') != boot['store']:
            fails.append('report store %s != manifest store %s'
                         % (rep.get('source_store_md5_after'), boot['store']))
    elif rep.get('board_md5_after') != boot['board']:
        later = [c for c in vh['columns']
                 if int(c.get('after_round') or -1) == n and c.get('kind') == 'out_of_round']
        ctx.log('THE LIVE BOARD HAS MOVED SINCE THIS REPORT, OUT OF ROUND — and that is a fact about '
                'the tree, not a defect in the report:')
        ctx.log('  report board  %s   (what round %d\'s scores produced)' % (rep['board_md5_after'], n))
        ctx.log('  live board    %s   (%d out-of-round point(s) registered at round %d since)'
                % (boot['board'], len(later), n))
        for c in later:
            ctx.log('      %-30s %s' % (c.get('id'), c.get('board')))
        if boot['board'] not in {c.get('board') for c in later}:
            fails.append('the live board %s is neither this report\'s board nor any stored '
                         'out-of-round point at round %d. The drift is UNEXPLAINED.'
                         % (boot['board'], n))
    prev = rep.get('previous_round')
    rm = _load(ctx, 'round_movers', 'engine/rl_after/ingestion/round_movers.py')
    pp = rm.previous_point(ctx.root, n)
    pp_id = pp.get('id') if isinstance(pp, dict) else pp
    if str(prev) != str(pp_id):
        fails.append('the report compared FROM %r; previous_point(%d) is %r (rule M0)'
                     % (prev, n, pp_id))
    base_col = col.get(str(prev))
    if base_col is None:
        fails.append('the baseline point %r is not a stored column' % prev)
    else:
        if base_col.get('board') != rep.get('board_md5_before'):
            fails.append('baseline column board %s != report board_md5_before %s'
                         % (base_col.get('board'), rep.get('board_md5_before')))
        if int(base_col.get('after_round')) != n - 1:
            fails.append('RULE M0: the baseline sits at as_of_round %s, not %d'
                         % (base_col.get('after_round'), n - 1))
    if not (rep.get('integrity') or {}).get('coverage_full'):
        fails.append('the report does not claim full coverage')
    if int(rep.get('player_count') or 0) != len(rep.get('players') or []):
        fails.append('player_count %s != %d rows' % (rep.get('player_count'), len(rep.get('players') or [])))
    if fails:
        raise StepError('THE MOVERS PAGE WOULD NOT DESCRIBE THE TREE IT WAS BUILT FROM:\n    %s'
                        % '\n    '.join(fails))
    ctx.log('fences OK: report R%d, board %s, baseline %r at round %d (rule M0, via previous_point)'
            % (n, rep['board_md5_after'][:12], prev, n - 1))

    sys.path.insert(0, _p(ctx, 'ui', 'templates'))
    try:
        import importlib
        slots = importlib.import_module('slots')
        importlib.reload(slots)
    finally:
        if sys.path and sys.path[0] == _p(ctx, 'ui', 'templates'):
            sys.path.pop(0)

    order = sorted(rep['players'], key=lambda p: (-p['value_change'], p['name']))
    players = [{
        'name': p['name'], 'pos': p['pos'], 'club': p['club'],
        'played': 'yes' if p['played'] else 'no',
        'score': ('%g' % p['score']) if p['played'] else slots.ABSENT,
        'prev_value': p['prev_value'], 'cur_value': p['cur_value'],
        'value_change': '%+d' % p['value_change'],
        'value_change_pct': '%+.1f%%' % p['value_change_pct'],
        'prev_rank': p['prev_rank'], 'cur_rank': p['cur_rank'],
        'rank_change': '%+d' % p['rank_change'],
        'prev_pos_rank': p['prev_pos_rank'], 'cur_pos_rank': p['cur_pos_rank'],
        'pos_rank_change': '%+d' % p['pos_rank_change'],
    } for p in order]
    up = sum(1 for p in rep['players'] if p['value_change'] > 0)
    dn = sum(1 for p in rep['players'] if p['value_change'] < 0)
    tb = sum(p['prev_value'] for p in rep['players'])
    ta = sum(p['cur_value'] for p in rep['players'])
    mp = ctx.spec.get('movers_page') or {}
    note = mp.get('boundary_note') or (
        'THE BASELINE IS THE STORED POINT IMMEDIATELY BEFORE THIS ROUND, not the previous round\'s '
        'report: the point compared FROM is %r (board %s, as_of_round %d), chosen by '
        'round_movers.previous_point and asserted by the lander. That is rule M0 — a diff baseline '
        'must share as_of_round with the candidate — so any board move that landed between the last '
        'round report and this round sits on the ROUND-%d side of this boundary and appears nowhere '
        'in the numbers below. EVERY DELTA ON THIS PAGE IS WHAT ROUND %d\'S SCORES DID.'
        % (prev, rep['board_md5_before'][:8], n - 1, n - 1, n))
    data = {
        'page_title': 'THE MOVERS — round %d, %s' % (n, rep.get('season', 2026)),
        'subtitle': ('%d players · %d played, %d did not · %d moved (%d up, %d down) · '
                     'board total %s -> %s (%+d)'
                     % (len(players), (rep.get('views') or {}).get('played_count', 0),
                        (rep.get('views') or {}).get('dnp_count', 0), up + dn, up, dn,
                        format(tb, ','), format(ta, ','), ta - tb)),
        'boundary_note': note,
        'from_label': '%s (%s, round %d)' % (prev, rep['board_md5_before'][:8], n - 1),
        'to_label': 'R%d board %s' % (n, rep['board_md5_after'][:8]),
        'board_md5_before': rep['board_md5_before'], 'board_md5': rep['board_md5_after'],
        'store_md5_before': rep['source_store_md5_before'], 'store_md5': rep['source_store_md5_after'],
        'engine_head': rep['release_identity']['engine_head'],
        'config': rep['release_identity']['config'][:12],
        'as_of_round': rep['submitted_round'],
        'previous_round': prev,
        'generated_at': rep['generated_at'],
        'players': players,
    }
    probs = slots.validate('movers', data)
    ctx.log('slots.validate("movers", <the R%d payload>) -> %s'
            % (n, 'NO PROBLEMS — the template fits.' if not probs else probs[:5]))
    if probs:
        raise StepError('the movers payload does not satisfy the slot contract: %d problem(s): %s'
                        % (len(probs), probs[:5]))
    html = slots.render('movers', data)
    out_rel = mp.get('output') or os.path.join(ctx.spec.get('evidence_dir') or 'docs/evidence',
                                               'MOVERS_R%d.html' % n)
    if ctx.opts.dry_run:
        ctx.log('--dry-run: the page RENDERS and validates (%d bytes, %d rows) and is NOT written '
                'to %s.' % (len(html.encode()), len(players), out_rel))
        return {'rendered': True, 'written': False, 'rows': len(players),
                'bytes': len(html.encode())}
    os.makedirs(os.path.dirname(_p(ctx, out_rel)), exist_ok=True)
    with open(_p(ctx, out_rel), 'w', encoding='utf-8') as fh:
        fh.write(html)
    ctx.log('wrote %s  (%d bytes, %d rows, md5 %s)'
            % (out_rel, len(html.encode()), len(players), md5(_p(ctx, out_rel))))
    return {'rendered': True, 'written': True, 'path': out_rel, 'rows': len(players),
            'md5': md5(_p(ctx, out_rel)), 'up': up, 'down': dn,
            'board_total_before': tb, 'board_total_after': ta}


# ================================================================================= STEP — STATE
def state(ctx):
    """docs/STATE.md — the machine-written state file, regenerated (PLAN_v6 3c, process law P6).

    A LATE STEP OF BOTH SEQUENCES, AND ITS POSITION IS THE DESIGN. It runs AFTER every writer that
    can move an identity (pins, lineage, contract, sibling, ui — and the advance, in a round) and
    BEFORE `gates`, so the state file that the gate set then reads is the one this landing produced.
    Put it after `gates` and the landing's own `acceptance::state_file` row would be measuring the
    PREVIOUS landing's file; put it after `commit` and it would never be committed at all.

    IT WRITES NO VALUE OF ITS OWN. Everything in the file is computed by `tools/landing/state.py`
    from the carriers — that module is the sole writer, this step is one of its three callers, and
    the postcondition asserted here is the same one the acceptance check asserts: what is on disk IS
    a regeneration of this tree. A file that cannot be regenerated does not get written half-way.

    THE PREDECESSOR IS WHY THE STEP EXISTS. `docs/CURRENT_STATE.md` was hand-maintained behind an
    authority banner and sat 156 register versions stale; it is retired to a tombstone at its own
    path in the 3c act. Nothing about this file is hand-maintained, and the moment that stops being
    true the freshness gate says so.
    """
    ctx.fault_point('state')
    from tools.landing import state as STATE

    try:
        if ctx.opts.dry_run:
            text = STATE.render(ctx.root, STATE.head_commit(ctx.root))
            ctx.log('DRY RUN: docs/STATE.md would be %d bytes; not written.' % len(text.encode()))
            return {'written': False, 'dry_run': True, 'bytes': len(text.encode())}
        rel, md5_after, changed = STATE.write(ctx.root)
    except STATE.StateError as e:
        # P6 IN ITS LITERAL FORM: a derived surface that cannot be generated does not exist. The step
        # does not write a partial file and does not carry the previous landing's copy forward as
        # though it were current — it halts the landing and names the carrier it could not read.
        raise StepError('the state file CANNOT be generated from this tree: %s' % e)
    problems = STATE.check(ctx.root)
    if problems:
        raise StepError('the state file was written and does not verify as a regeneration of this '
                        'tree:\n    %s' % '\n    '.join(problems))
    ctx.log('state: %s md5 %s (%s); regeneration verified'
            % (rel, md5_after, 'moved' if changed else 'byte-unmoved'))
    return {'written': True, 'path': rel, 'md5': md5_after, 'changed': changed,
            'stamp_commit': STATE.recorded_commit(ctx.root)}


# ================================================================================ STEP 9 — COMMIT
def commit(ctx):
    """ONE commit, EXPLICIT PATHS ONLY. Never `git add -A`, never `git commit -a`.

    PLAN_v6 2a.1 requires explicit-path commits, asserted in self-test. The assertion is here and it
    is two-sided: every path staged must be inside the declared carrier set (plus the act's own
    evidence and claims files), and every modified path in the tree must be one this landing meant
    to write. A landing that swept up another seat's in-flight edit would be indistinguishable from
    one that did not, right up until someone bisected it.
    """
    ctx.fault_point('commit')
    from tools.landing import carriers as CA

    rc, out = ctx.run(['git', 'status', '--porcelain'])
    if rc != 0:
        raise StepError('git status failed')
    changed = []
    for ln in out.splitlines():
        if not ln.strip():
            continue
        rel = ln[3:].strip().strip('"')
        if ' -> ' in rel:
            rel = rel.split(' -> ')[-1]
        changed.append(rel)

    allowed_extra = tuple(p for p in (ctx.spec.get('evidence_dir'), ctx.rel_claims_path,
                                      ctx.spec.get('_spec_rel')) if p)
    staged, foreign = [], []
    for rel in changed:
        if CA.in_scope(rel, ctx.carriers) or any(rel.startswith(a) for a in allowed_extra):
            staged.append(rel)
        else:
            foreign.append(rel)
    if foreign:
        raise StepError(
            'THE TREE CARRIES CHANGES THIS LANDING DID NOT MAKE, and an explicit-path commit will '
            'not sweep them up:\n    %s\nDeclare them as carriers or take them out of the tree.'
            % '\n    '.join(sorted(foreign)))
    if not staged:
        ctx.log('nothing to commit — this landing wrote no file (a declared no-op).')
        return {'commit': None, 'paths': []}

    verb = 'land round' if ctx.spec['act_kind'] == 'round-advance' else 'land lever'
    msg = ctx.spec.get('commit_message') or ('%s — the landing transaction (%s)'
                                             % (ctx.spec['act'], verb))
    sha = _git_commit(ctx, staged, msg)
    return {'commit': sha, 'paths': sorted(staged), 'committed': sha is not None}


#: THE LAST STEP THAT NEEDS THE SINGLE-WRITER LOCK. Steps 0-6 build, or depend on something just
#: built, so they run behind the lock. `gates`, `claims` and `commit` write nothing to the shared
#: workspace, and the one gate that DOES build (`build_twice_determinism`) takes the lock itself —
#: so the lander releases here. Holding it further deadlocks the landing against its own gate, and
#: the variable that would make that gate's acquisition reentrant cannot be exported safely (it
#: drifts a ruled-red probe; see txn.Ctx.child_env).
LOCK_HELD_THROUGH = 'ui'

#: THE SEQUENCE. The day's proven order, and the single place it is stated.
LEVER_SEQUENCE = (
    ('preflight',    'clean tree, build lock, the restore point',            preflight),
    ('build_proofs', 'bare build, predicted identity, switch leg, day-0',    build_proofs),
    ('pins',         'expected_boot + both sidecars + the generator copy',   pins),
    ('lineage',      'the out-of-round column and the append-only entry',    lineage),
    ('contract',     'restamp_dynamic + the bake-lane repin + check',        contract),
    ('sibling',      'the balanced sibling, rebuilt and reconciled if moved', sibling),
    ('ui',           'ALL FIVE UI writers, and the identity read back out',  ui),
    ('state',        'docs/STATE.md regenerated from the carriers (3c)',     state),
    ('gates',        'the landing gate set, verdicts off exit codes',        gates),
    ('claims',       'emit the claims file and verify it against the tree',  claims),
    ('commit',       'ONE commit, explicit paths only',                      commit),
)

#: THE ROUND-ADVANCE SEQUENCE (PLAN_v6 2b) — the R23 hand-walk's proven order, as a program.
#:
#: EIGHT OF THESE FIFTEEN STEPS ARE THE LEVER LANDER'S OWN FUNCTIONS, registered again here rather
#: than copied: `preflight`, `contract`, `sibling`, `ui`, `state`, `gates`, `claims`, `commit`. That is the S7
#: law made structural — two commands, one library, and no way for the shared half to drift apart,
#: because there is only one of it. What 2b adds is the seven steps a round genuinely has and a lever
#: landing genuinely does not.
#:
#: THE ORDER IS THE HAND-WALK'S, and the hand-walk is `docs/evidence/r23_advance_2026-08-20/`:
#:
#:   sheet             ACT 1 — the sheet re-cut and its ONE pin declaration, own commit (3a form)
#:   scores            ACT 2 — the owner's file of record, asserted
#:   catchup_preflight ACT 2 — 08_preflight_r23.txt: read-only, CLEAN, then the inputs commit
#:   advance           ACT 3 — 09_armed_r23.txt: the armed catch-up; ADVANCE-REPIN runs inside it
#:   generator_sync    09b_generator_board_sync.txt: the disclosed generator-side sync (ERRATUM E5)
#:   day0              register v810 item 1: the day-0 reference's natural home, and only here
#:   contract          05_landing_c_contract.txt: restamp + the bake-lane repin + check
#:   sibling           05b/13: verify — after an advance the repin has already run IN-transaction
#:   ui                10_ui_writers_r23.txt, now ALL FIVE writers (F-9, F-10 and the ownership mirror)
#:   movers_page       ACT 4 — MOVERS_R23.html through the frozen template
#:   state             PLAN_v6 3c: docs/STATE.md regenerated from the carriers, before the gates
#:   gates             13_gates.txt: the standard landing gate set
#:   claims            PLAN_v6 1c
#:   commit            ONE commit, explicit paths — the advance's OUTPUTS only
#:
#: THERE IS NO `build_proofs` STEP AND NO `lineage` STEP, and both absences are load-bearing. A round
#: advance does not build a candidate board and assert a predicted md5 — `staged_apply` regenerates
#: the board inside its own transaction from the staged store, which is a stronger arrangement than
#: any board a lander could hand it. And a round advance earns no lineage entry and no out-of-round
#: column (ERRATUM E5); the spec validator refuses a spec that declares either.
ROUND_SEQUENCE = (
    ('preflight',         'clean tree, build lock, the restore point',              preflight),
    ('sheet',             'the sheet re-cut + its ONE pin declaration, own commit', sheet),
    ('scores',            "the owner's score file and the bindings, asserted",      scores),
    ('catchup_preflight', 'read-only preflight, CLEAN, then the inputs commit',     catchup_preflight),
    ('advance',           'THE ARMED CATCH-UP — ADVANCE-REPIN runs inside it',      advance),
    ('generator_sync',    'the generator-side board copy, synced and DISCLOSED',    generator_sync),
    ('day0',              'the day-0 reference — regenerated AT the advance, only', day0),
    ('contract',          'restamp_dynamic + the bake-lane repin + check',          contract),
    ('sibling',           'the balanced sibling: verify (the repin ran in-txn)',    sibling),
    ('ui',                'ALL FIVE UI writers, and the identity read back out',    ui),
    ('movers_page',       "the owner's movers page, through the frozen template",   movers_page),
    ('state',             'docs/STATE.md regenerated from the carriers (3c)',       state),
    ('gates',             'the landing gate set, verdicts off exit codes',          gates),
    ('claims',            'emit the claims file and verify it against the tree',    claims),
    ('commit',            'ONE commit, explicit paths only',                        commit),
)

#: act_kind -> (sequence, carrier set). The ONE place a verb is bound to what it runs and what it may
#: write, so a new act kind cannot half-exist.
SEQUENCES = {'lever-landing': 'LEVER_SEQUENCE', 'round-advance': 'ROUND_SEQUENCE'}
