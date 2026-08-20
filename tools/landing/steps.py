"""tools/landing/steps.py — THE TEN STEPS, IN THE DAY'S PROVEN ORDER.

Every step here is a CONSOLIDATION of a script that already ran and already landed a board on
2026-08-20. The provenance of each is named in its own docstring, and the rule throughout is the one
the per-act scripts stated for themselves:

    EVERY VALUE IS COMPUTED HERE, IN THIS PROCESS, FROM THE TREE — NEVER TYPED IN FROM THE BRIEF.

The only values that arrive from outside are PREDICTIONS (the prereg's board), CITATIONS (the owner
word, the lineage authority) and POLICY (which identities this act is allowed to move). Those are
the three things a tree cannot measure about itself, and they are exactly what the act spec carries.

WHAT THE STEPS SHARE WITH THE ROUND LANDER (2b). `preflight`, `contract`, `sibling`, `ui`, `gates`,
`claims` and `commit` are act-kind agnostic: 2b registers the same functions in its own sequence and
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
DEFAULT_GATES = (
    {'name': 'release_manifest_check', 'argv': ['python3', 'release_manifest_check.py'],
     'must_contain': 'PASS'},
    {'name': 'release_contract_check', 'argv': ['python3', 'release_contract.py', 'check'],
     'must_contain': 'PASS'},
    {'name': 'acceptance_runner', 'argv': ['python3', '-m', 'acceptance.runner'],
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
    dirty = [ln for ln in out.splitlines() if ln.strip() and not ctx.is_ignorable_dirt(ln)]
    if dirty:
        raise StepError('THE TREE IS NOT CLEAN. A landing transaction starts from a committed tree, '
                        'or its abort restores a state nobody chose:\n    ' + '\n    '.join(dirty))
    rc, head = ctx.run(['git', 'rev-parse', 'HEAD'])
    if rc != 0:
        raise StepError('cannot read HEAD in %s' % ctx.root)
    base_commit = head.strip()

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
            raise StepError('the round must be HELD at %d in a lever landing' % as_of)
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
def ui(ctx):
    """BOTH UI writers. The thrice-proven trap, now code instead of a note in a docstring.

    `ui/tools/extract_board_view.py` REGENERATES the bundle from the board and DROPS `stamp.release`;
    only `round_movers.inject_release_contract` puts it back. Running the first without the second
    leaves the html app with no release block — a failure this tree has caught THREE times
    (landing_tail 02a_*.txt, 28_reinject_release_contract.txt, and d8_restamp.py §3, which runs them
    as a pair for exactly this reason). Every landing since has carried a hand-written script whose
    docstring explains the trap. This function is that docstring, executable.

    The identity is then read back OUT of the html bundle — the page's own embedded stamp — because
    a bundle that was regenerated but not re-stamped renders perfectly and says nothing true.
    """
    ctx.fault_point('ui')
    bundle = _p(ctx, 'ui', 'data', 'board_view_working.js')
    public = _p(ctx, 'ui', 'data', 'board_view_public.js')
    boot = json.load(open(_p(ctx, 'data', 'expected_boot.json'), encoding='utf-8'))

    def has_release(p):
        return '"release"' in open(p, encoding='utf-8').read()

    ctx.log('BEFORE  working %s  release-block=%s' % (md5(bundle), has_release(bundle)))
    ctx.log('BEFORE  public  %s  release-block=%s' % (md5(public), has_release(public)))
    if ctx.opts.dry_run:
        ctx.log('--dry-run: neither writer is run.')
        return {'writers': 0, 'dry_run': True}

    ctx.log('WRITER 1/2: ui/tools/extract_board_view.py')
    rc, out = ctx.run([sys.executable, _p(ctx, 'ui', 'tools', 'extract_board_view.py')], timeout=900)
    if rc != 0:
        raise StepError('extract_board_view failed:\n%s' % out[-2000:])
    ctx.log('  working after writer 1: %s   release-block=%s   <-- DROPPED, as it always is'
            % (md5(bundle), has_release(bundle)))

    if not ctx.skip_second_ui_writer:
        ctx.log('WRITER 2/2: round_movers.inject_release_contract(bundle, root, %s)' % boot['as_of_round'])
        rm = _load(ctx, 'round_movers', 'engine/rl_after/ingestion/round_movers.py')
        rel = rm.inject_release_contract(bundle, ctx.root, int(boot['as_of_round']))
        ctx.log('  release block: %s' % json.dumps(rel, sort_keys=True)[:200])
    else:
        ctx.log('WRITER 2/2: SKIPPED BY FAULT INJECTION — the trap is live in this transaction.')

    ctx.log('AFTER   working %s  release-block=%s' % (md5(bundle), has_release(bundle)))
    ctx.log('AFTER   public  %s  release-block=%s' % (md5(public), has_release(public)))

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
    ctx.log("THE HTML APP'S EMBEDDED BOARD IDENTITY IS %s. Both writers ran; the release block is back."
            % boot['board'])
    return {'writers': 2, 'bundle_md5': md5(bundle), 'public_md5': md5(public),
            'embedded_board': st.get('board_md5')}


# ================================================================================= STEP 7 — GATES
def gates(ctx):
    """The landing gate set. Verdicts are read off exit codes; none is taken on trust.

    fv-provenance is NEVER run here. PLAN_v6 2a.1: the suite overwrites a shared pickle, so it runs
    in isolated workspaces only and CI excludes it on shared runners. The lander calls the FV
    builder FUNCTION for its builds (which is safe and is what the day's build drivers did) and
    never the suite.
    """
    ctx.fault_point('gates')
    rows = []
    for g in (ctx.spec.get('gates') or DEFAULT_GATES):
        if 'fv_provenance' in ' '.join(g['argv']):
            raise StepError('a gate names the fv-provenance suite. It overwrites a shared pickle and '
                            'is never run on the shared box (PLAN_v6 2a.1).')
        t0 = time.time()
        rc, out = ctx.run(g['argv'], timeout=g.get('timeout_s', 1800))
        el = time.time() - t0
        ok = (rc == 0) and (g.get('must_contain') is None or g['must_contain'] in out)
        ctx.write_evidence('gate_%s.txt' % g['name'], '$ %s\n\n%s\n[exit %s]' % (' '.join(g['argv']), out, rc))
        ctx.log('  %-24s %-6s exit=%s  (%.1fs)' % (g['name'], 'PASS' if ok else 'FAIL', rc, el))
        rows.append({'name': g['name'], 'argv': g['argv'], 'exit': rc, 'ok': ok,
                     'elapsed_s': round(el, 1)})
        if not ok:
            raise StepError('gate %s did not pass (exit %s%s):\n%s'
                            % (g['name'], rc,
                               '' if g.get('must_contain') is None or g['must_contain'] in out
                               else '; %r absent from output' % g['must_contain'], out[-2500:]))
    return {'gates': rows, 'all_pass': True}


# ================================================================================ STEP 8 — CLAIMS
def claims(ctx):
    """Emit the act's claims file (tools/claims.py, `lever-landing`) and VERIFY it.

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
           'value': boot['as_of_round'], 'label': 'the round, HELD by a lever landing'},
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
    snap = ctx.snapshot
    for rel, before_md5 in sorted((snap.identities() if snap else {}).items()):
        if before_md5 and rel in ('engine/rl_after/rl_model_data.json',) and ctx.spec['act_kind'] == 'lever-landing':
            cl.append({'kind': 'unmoved', 'path': rel, 'value': before_md5,
                       'label': 'BYTE-UNMOVED by this lever landing'})

    d0 = (ctx.facts.get('build_proofs') or {}).get('day0_rebase', 'off')
    activation = {'day0_rebase': ({'state': 'off',
                                   '_doc': 'off by default; the M1b ruling — automation never '
                                           're-bases itself green'}
                                  if d0 == 'off' else
                                  {'state': 'on', 'activated_by': d0.get('activated_by'),
                                   'rows_moved': d0.get('rows_moved')})}
    for name, spec_sw in (ctx.spec.get('activation') or {}).items():
        activation[name] = spec_sw

    doc = {'schema_version': 1, 'act_type': 'lever-landing', 'act': ctx.spec['act'],
           'date': ctx.spec['date'], 'base_commit': ctx.facts['base']['commit'],
           'owner_word': ctx.spec['owner_word'], 'activation': activation, 'claims': cl,
           '_restore_point': ctx.facts['base']['carriers'],
           '_step_timings_s': ctx.timings_dict(),
           '_landed_by': 'tools/landing (`land lever`), PLAN_v6 PACKAGE 2a'}

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

    ctx.log('explicit paths (%d):' % len(staged))
    for rel in sorted(staged):
        ctx.log('    %s' % rel)
    if ctx.opts.dry_run or ctx.opts.no_commit:
        ctx.log('--%s: not committing.' % ('dry-run' if ctx.opts.dry_run else 'no-commit'))
        return {'commit': None, 'paths': sorted(staged), 'committed': False}

    rc, out = ctx.run(['git', 'add', '--'] + sorted(staged))
    if rc != 0:
        raise StepError('git add failed: %s' % out)
    msg = ctx.spec.get('commit_message') or ('%s — the landing transaction (land lever)' % ctx.spec['act'])
    rc, out = ctx.run(['git', 'commit', '-m', msg])
    if rc != 0:
        raise StepError('git commit failed: %s' % out)
    rc, head = ctx.run(['git', 'rev-parse', 'HEAD'])
    ctx.log('committed %s' % head.strip()[:12])
    return {'commit': head.strip(), 'paths': sorted(staged), 'committed': True}


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
    ('ui',           'BOTH UI writers, and the identity read back out',      ui),
    ('gates',        'the landing gate set, verdicts off exit codes',        gates),
    ('claims',       'emit the claims file and verify it against the tree',  claims),
    ('commit',       'ONE commit, explicit paths only',                      commit),
)
