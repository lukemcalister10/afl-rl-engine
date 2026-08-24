"""tools/landing/preview.py — `land edit --dry-run`: THE OWNER'S ONE-SCREEN PREDICTION.

    tools/land edit --spec <edit_spec.json> --dry-run

THE USER-FRIENDLY HALF OF THE EDIT VERB, and the reason the verb was ruled into existence. The owner's
words, 2026-08-24: *"There will likely be lots of out of round edits. So that lander needs to be
redone so round edits are one option, but there's also a general edit option. That is user unfriendly
as it stands."*

THE LOOP THIS FILE CLOSES. One command predicts, one command lands:

    1. the seat writes the edit spec — {key, field, old, new}, the owner's word, the citations;
    2. `--dry-run` applies that edit in a SCRATCH GIT WORKTREE, builds the board there, and prints ONE
       SCREEN: the store's md5 old -> new, the board's md5 old -> new, EVERY mover with its values,
       the pool, and every declared identity with a MOVES/unmoved verdict;
    3. the owner reads it and gives his word; the word goes into the spec VERBATIM;
    4. the same command WITHOUT `--dry-run` flies the landing transaction.

IT WRITES NOTHING TO ANY CARRIER, AND THAT IS A MEASURED FACT RATHER THAN A DESIGN INTENTION. Every
carrier of the round set (a superset of the lever set) is hashed before the preview and again after
it, by this process, and any difference is a loud failure. The prediction happens in a `git worktree`
of HEAD which is removed at the end; the only thing this file writes inside the repo is nothing at
all.

WHY A SCRATCH WORKTREE AND NOT `--dry-run` THROUGH THE SEQUENCE. The board is built by staging a copy
of `engine/rl_after` and running the exporter over it, so a board that reflects the edit can only come
from a tree where the edit exists. A dry run that "called no writer" would build the PRE-edit store
and predict the board the tree already has — a prediction of record that predicted nothing. So the
edit is real, and the tree it is real in is disposable. This is also exactly how the standing Graham
prediction was measured before its prereg was committed (`docs/evidence/graham_dual_2026-08-24/`).

THE TREE MUST BE CLEAN, and the preview refuses otherwise rather than warning. A dry run against a
dirty tree predicts a tree nobody will land: the worktree is cut from HEAD, and uncommitted work is
invisible to it.
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


def _git(root, argv):
    p = subprocess.run(argv, cwd=root, capture_output=True, text=True)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


class _Out(object):
    """Print and keep. The transcript is handed back so `--log` can file it verbatim."""

    def __init__(self):
        self.lines = []

    def __call__(self, msg=''):
        self.lines.append(msg)
        print(msg)
        sys.stdout.flush()


def _identity_table(ctx, doc, boot, board_md5, out):
    """Every identity the act DECLARES, measured on the edited tree against the standing pins.

    IT MEASURES WHAT THE ACT TALKS ABOUT. `identities.moves` and `identities.unmoved` are the act's
    own policy statement, and this table is that statement checked against a tree where the edit has
    actually happened — which is the question the owner is being asked to rule on.

    THE TWO COMPUTED IDENTITIES ARE ALLOWED TO BE UNMEASURABLE HERE and say so in the cell. `config`
    and `fv` are computed by importing the tree's own modules; in a PREDICTION that is a convenience,
    and the LANDING asserts both properly (`contract`, `pins`). A preview that died because it could
    not import a module would be a preview nobody could run on a broken branch — which is one of the
    times it is most wanted.
    """
    ids = doc.get('identities') or {}
    declared = [(k, 'MOVES') for k in (ids.get('moves') or ())] + \
               [(k, 'unmoved') for k in (ids.get('unmoved') or ())]
    rows = []
    for k, want in declared:
        pin = boot.get(k)
        if k == 'board':
            got = board_md5
        elif k in ST.PIN_MEASURERS:
            try:
                got = ST.PIN_MEASURERS[k](ctx)
            except Exception as e:                                    # noqa: BLE001 — see docstring
                got = 'unmeasurable here (%s)' % str(e)[:60]
        else:
            got = '(written by another writer of record — %s)' % ST.DELEGATED_PINS.get(k, 'not pinned')
        moved = (str(got) != str(pin)) if isinstance(got, str) and len(str(got)) in (32, 64) else None
        rows.append({'identity': k, 'declared': want, 'pinned': pin, 'measured': got, 'moved': moved})
    out('IDENTITIES — every one this act declares, measured on the EDITED tree against the pins')
    for r in rows:
        verdict = ('MOVES   ' if r['moved'] else 'unmoved ') if r['moved'] is not None else '        '
        agree = ''
        if r['moved'] is not None:
            want_move = r['declared'] == 'MOVES'
            agree = 'as declared' if want_move == bool(r['moved']) else \
                    '*** DISAGREES WITH THE SPEC (declared %s) ***' % r['declared']
        out('    %-20s %s %-34s -> %-34s %s'
            % (r['identity'], verdict, str(r['pinned'])[:34], str(r['measured'])[:34], agree))
    return rows


def dry_run(root, doc, keep=False, report=None, log=None):
    """THE PREDICTION. -> exit code. Writes nothing inside `root`, and proves it."""
    out = _Out()
    root = os.path.abspath(root)
    t0 = time.time()

    out(BANNER)
    out('LAND EDIT — DRY RUN. THE PREDICTION, MEASURED IN A SCRATCH WORKTREE.')
    out('  act        : %s' % doc.get('act'))
    out('  owner word : %s' % doc.get('owner_word'))
    out('  tree       : %s' % root)
    out(BANNER)

    rc, status = _git(root, ['git', 'status', '--porcelain'])
    if rc != 0:
        out('cannot read the tree\'s status: %s' % status)
        return 2
    if status.strip():
        out('THE TREE IS NOT CLEAN, and this preview is cut from HEAD — so it would predict a tree '
            'nobody is going to land:')
        for ln in status.strip().splitlines():
            out('    %s' % ln)
        out('Commit or remove the above and run the dry run again.')
        return 2

    before = _carrier_md5s(root)
    out('live carriers hashed BEFORE the preview: %d' % len(before))

    from tools.landing import selftest as SELF
    work = os.path.join(os.environ.get('LANDING_SNAPSHOT_DIR') or '/tmp',
                        'landing_preview_%d' % os.getpid())
    TX.sweep_orphan_sandboxes(out)
    sb = SELF.Sandbox(root, work, base='HEAD').create()
    out('scratch worktree: %s  (a git worktree of HEAD; removed when this run ends)' % sb.path)

    try:
        store_p = os.path.join(sb.path, ST.STORE_REL)
        board_p = os.path.join(sb.path, 'data', 'rl_build', 'rl_app_data.json')
        boot = json.load(open(os.path.join(sb.path, 'data', 'expected_boot.json'), encoding='utf-8'))
        store_before, board_before = _md5(store_p), _md5(board_p)

        # quiet=True: the context's own lines are echoed through `out` below, so the transcript this
        # function hands to `--log` is the WHOLE screen rather than the half of it this file printed.
        ctx = TX.Ctx(sb.path, doc, TX.Options(dry_run=False, selftest=False, quiet=True),
                     evidence_dir=os.path.join(work, 'transcripts'),
                     work_dir=os.path.join(work, 'build'))

        # ---- THE EDIT, through the step's own applier. One implementation, never a second ---------
        text = open(store_p, 'rb').read().decode('utf-8')
        new_text, applied = ST.apply_store_edits(text, (doc.get('edit') or {}).get('store') or ())
        with open(store_p, 'wb') as fh:
            fh.write(new_text.encode('utf-8'))
        store_after = _md5(store_p)
        # AND THE SEASON CLOCK'S PROVENANCE STAMP, through the step's own function — so the scratch
        # tree this preview builds is the same tree the flight will build, not a near neighbour.
        ST.season_state_rederive(ctx, store_after)

        out('')
        out('THE EDIT — surgical, inside the named row\'s span; `old` is asserted, never repaired')
        for a in applied:
            out('    %-28s %-18s %s -> %s'
                % (a['key'], a['field'], json.dumps(a['old']), json.dumps(a['new'])))
            out('        row span %d..%d of the store, %d char(s) -> %d char(s) in the file'
                % (a['row_span'][0], a['row_span'][1], a['chars_before'], a['chars_after']))

        # ---- THE BUILD, on the edited scratch tree, under the shared build lock -------------------
        ctx.acquire_lock()
        try:
            res = ctx.builder.build(ctx, tag='PREVIEW', mode='dev')
        finally:
            ctx.release_lock()
        for ln in ctx.lines:
            out('  %s' % ln)
        if res['rc'] != 0:
            out('THE PREVIEW BUILD FAILED (rc=%s). Transcript: %s'
                % (res['rc'], os.path.join(work, 'transcripts')))
            return 1
        board_after = res['board_md5']
        movers, facts = ST.board_movers(board_p, res['board_path'])

        # ---- THE ONE SCREEN -----------------------------------------------------------------------
        out('')
        out(BANNER)
        out('THE PREDICTION')
        out(BANNER)
        out('    store   %s -> %s' % (store_before, store_after))
        out('    board   %s -> %s' % (board_before, board_after))
        out('')
        out('MOVERS — EVERY ONE, WITH VALUES  (%d of %d valued row(s) moved)'
            % (facts['n_movers'], facts['rows_compared']))
        for m in movers:
            out('    %-28s %-26s %8s -> %-8s (%s)  [%s]'
                % (m['key'], (m['name'] or '')[:26], m['before'], m['after'],
                   '%+d' % m['delta'] if m['delta'] is not None else 'appeared/vanished',
                   m['section']))
        if not movers:
            out('    (none — no valued board row moves)')
        out('    pool (sum of active v)   %d -> %d  (%+d)'
            % (facts['pool_before'], facts['pool_after'], facts['pool_delta']))
        if facts['rows_added'] or facts['rows_removed']:
            out('    ROWS ADDED %s   ROWS REMOVED %s' % (facts['rows_added'], facts['rows_removed']))
        out('')
        id_rows = _identity_table(ctx, doc, boot, board_after, out)

        out('')
        declared_board = (doc.get('prereg') or {}).get('board_after')
        if declared_board:
            out('PREDICTION OF RECORD: the spec declares prereg.board_after %s — the flight will '
                'assert it BYTE-EXACT.' % declared_board)
            out('    this preview built %s: %s' % (board_after,
                                                   'THEY AGREE' if board_after == declared_board
                                                   else '*** THEY DISAGREE — the flight will ABORT '
                                                        'at build_proofs ***'))
        else:
            out('PREDICTION OF RECORD: this dry run IS it. The spec declares no prereg.board_after, so')
            out('    the flight asserts internal consistency only. Paste the two md5s above into the')
            out('    prereg (or into the spec\'s board_after) if this act should assert a prediction.')
        declared_movers = (doc.get('edit') or {}).get('expected_movers')
        if declared_movers is None:
            out('    edit.expected_movers is not declared — the movers above are printed and')
            out('    asserted against nothing. Declaring them makes each one a falsifier.')
        out('    build: rc=%s in %.1fs' % (res['rc'], res['elapsed_s']))
    finally:
        if keep:
            out('')
            out('SCRATCH WORKTREE KEPT (--keep-work): %s' % sb.path)
        else:
            sb.destroy()
            shutil.rmtree(work, ignore_errors=True)

    # ---- WROTE NOTHING, MEASURED ------------------------------------------------------------------
    after = _carrier_md5s(root)
    drift = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    out('')
    if drift:
        out('*** THIS PREVIEW MOVED %d LIVE CARRIER(S): %s' % (len(drift), drift))
        out(BANNER)
        return 1
    out('WROTE NOTHING: every one of the %d live carriers re-hashed after the run, 0 moved.'
        % len(after))
    out('  (the prediction happened in the scratch worktree; the tree you are standing in is '
        'byte-identical to the tree you started with.)')
    out('TO FLY IT: the same command WITHOUT --dry-run, once the owner\'s word is in the spec.')
    out('total %.1fs' % (time.time() - t0))
    out(BANNER)

    if report:
        with open(report, 'w', encoding='utf-8') as fh:
            json.dump({'ok': True, 'act': doc.get('act'), 'dry_run': True,
                       'store': {'before': store_before, 'after': store_after},
                       'board': {'before': board_before, 'after': board_after},
                       'edits': applied, 'movers': movers, 'board_facts': facts,
                       'identities': id_rows, 'carriers_checked': len(after), 'carriers_moved': [],
                       'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())},
                      fh, indent=2, sort_keys=True, default=str)
    if log:
        with open(log, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(out.lines) + '\n')
    return 0


def _carrier_md5s(root):
    """The ROUND carrier set — a superset of what an edit can write — hashed by THIS process."""
    res = {}
    for rel in CA.expand(root, CA.ROUND_CARRIERS):
        p = os.path.join(root, rel)
        res[rel] = _md5(p) if os.path.isfile(p) else None
    return res
