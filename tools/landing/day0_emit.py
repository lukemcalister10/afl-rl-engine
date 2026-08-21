#!/usr/bin/env python3
"""tools/landing/day0_emit.py — THE CARRIED DAY-0 EMITTER. Generic, tree-driven, act-free.

    python3 tools/landing/day0_emit.py --spec <act spec> [--root <repo>] [--out <path>]

WHY IT EXISTS — THE R24 REHEARSAL'S §5 FINDING, VERBATIM ON THE POINT: *"THE FINDING THE REAL R24
MUST ACT ON BEFORE IT FLIES: there is no runnable day-0 emitter for R24. The emitter of record,
`docs/evidence/final_candidate_2026-08-19/cprb_day0.py`, is act-pinned: it reads its board from a
named scratch directory that no longer exists, diffs against `order_k_2026-08-18/DAY0_K.json`, and
hard-asserts SIX named movers with their exact old and new printed integers (assertions A3/A4). It
cannot run for R24 as it stands."*

THIS IS THE CARRIED REPLACEMENT — the R23-era chain's own pattern (`ok_day0.py` -> `fcrb_day0.py` ->
`cprb_day0.py` -> `sfx_day0.py`, each carried with its changes declared), carried ONE more time with
every act-pinning removed and NOTHING ELSE changed about the law it measures:

  (1) THE BOARD IS THE CURRENT TREE'S BOARD (`data/rl_build/rl_app_data.json`), not a named scratch
      staging directory. No build is run here; the emitter is READ-ONLY on the engine and the store.
  (2) THE STANDING REFERENCE IS WHATEVER THE ACT SPEC NAMES (`day0_rebase.reference`), not a
      hard-coded `order_k_2026-08-18/DAY0_K.json`.
  (3) THE ASSERTION BLOCK CARRIES NO NAMED ROWS AND NO EXPECTED INTEGERS. cprb's A3/A4/A8/A9 were
      that act's own D7 parity findings written into the instrument — correct there, unrunnable
      anywhere else, and process law P4 in its purest form ("a hand-typed identity in a check is a
      red waiting for the next legitimate move"). What survives is the leg that is TRUE OF ANY
      TREE and is the emitter's whole fail-closed guard:

          A1  THE PRINTED DAY-0 IDENTITY HOLDS ON THE BOARD BEING READ, at tolerance 0.

      Every row's day-0 price is recomputed and must equal the integer the board prints. A single
      mismatch HALTS and writes nothing — which is exactly how `sfx_day0.py` caught a stale
      reference (24 of 89) instead of quietly re-basing onto it.
  (4) NO WALL CLOCK ANYWHERE. Nothing in the emitted document comes from the current time, so two
      runs on one tree are BYTE-IDENTICAL — asserted by the lander self-test.

THE LAW IT COMPUTES IS THE ENGINE'S OWN, NOT A SECOND COPY OF IT. The price comes from the engine's
own day-0 predicate `_entry30b_price` where the loaded engine exposes one, and only falls back to
`_entry29b_derived(p,Y) * o31_D(p,Y)` — the same expression, spelled out — where it does not. M1b's
mirrored-pair hazard is the reason: a re-implementation of the law beside the law is how a suite
re-bases itself green.

THE M1b REFUSALS, both of them, and they are the reason this file may be called by anything:

  * IT REFUSES TO WRITE WHEN DAY-0 IS NOT ACTIVATED IN THE ACT SPEC. `day0_rebase.state` must be
    "on" and must name the owner word that turned it on. "Day-0 re-basing becomes an explicit,
    owner-visible, off-by-default input" — an emitter that regenerated the reference whenever it was
    run would hand the capability back to automation the moment anyone scripted it.
  * IT REFUSES TO WRITE WITHOUT THE STANDING REFERENCE TO DIFF AGAINST. The printed row diff is
    MANDATORY, so no reference means no diff means no write — never a silent first write.

WHAT IT PRINTS: every moved row, in full, with no truncation and no summary-instead-of-rows, plus
the population added/dropped and the `derived_v0` movement (the raw entry object the walk-forward
matrix writes as its year-0 column — it is REPORTED, never asserted, because a round advance may
lawfully move it).
"""
import argparse
import contextlib
import hashlib
import io
import json
import os
import sys


LAW = ('printed = round(day0_v0(p) * D(c_u)) — the ONE LAW at g=0, where rho(0)=0 and '
       'pi(0,c,s) == D(c) exactly')

#: The board of record this emitter prices against. The PUBLISHED copy, which is the one Guard 5
#: asserts and the one every derived surface is built from.
BOARD_REL = 'data/rl_build/rl_app_data.json'
STORE_REL = 'engine/rl_after/rl_model_data.json'
ENGINE_HEAD_REL = 'engine/rl_after/_merged_recover.py'

#: Infrastructure/path variables the engine legitimately reads. EVERY OTHER `RL_`/`PAR_` variable is
#: cleared before the engine loads, so a dial left in a seat's shell cannot silently price a line
#: nobody ruled — `cprb_day0.py`'s clear-list, generalised from a hand-typed list of six names to
#: the rule the config manifest itself uses.
INFRA_KEEP = ('RL_REPO', 'RL_APP_DATA', 'RL_FV', 'RL_VENV', 'RL_V0SURF_PKL',
              'RL_ALLOW_PVCFIT_BOARD')


class EmitError(RuntimeError):
    """A refusal or a failed assertion. Nothing is ever written on one."""


def _md5(path):
    with open(path, 'rb') as fh:
        return hashlib.md5(fh.read()).hexdigest()


def _engine(root):
    """Load the engine READ-ONLY, on the shipped default expression, and hand back its namespace.

    The dial line is NOT enumerated here and that is deliberate: the shipped expression IS the
    engine's own defaults (the 2026-08-20 bake made RL_O42/RL_O43 and the O36-O38 stack default-on),
    so a file that re-typed the dials would be pricing whatever line its author last remembered.
    What this does instead is CLEAR — every RL_/PAR_ variable that is not infrastructure — so the
    expression cannot be perturbed by the calling shell either way.
    """
    for k in [k for k in os.environ
              if (k.startswith('RL_') or k.startswith('PAR_')) and k not in INFRA_KEEP]:
        os.environ.pop(k, None)
    os.environ.pop('RL_CONFIG_MODE', None)
    os.environ.update(PYTHONHASHSEED='0', RL_REPO=root,
                      OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                      NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                      RL_V0SURF_PKL=os.path.join(root, 'data', 'v0surf.pkl'),
                      RL_FV=os.path.join(root, 'engine', 'forward_valuation'))
    sys.path[:0] = [root, os.path.join(root, 'vendor'),
                    os.path.join(root, 'engine', 'forward_valuation'),
                    os.path.join(root, 'engine', 'rl_after')]
    cwd = os.getcwd()
    os.chdir(os.path.join(root, 'engine', 'rl_after'))
    ns = {}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import rl_model as MA                                            # noqa: F401
            src = open('_merged_recover.py', encoding='utf-8').read()
            exec(src.split('print("=== AFTER')[0], ns)                       # noqa: S102
    finally:
        os.chdir(cwd)
    ns['MA'] = ns.get('MA', MA)
    return ns


def compute_rows(root, board_rel=BOARD_REL):
    """-> (rows, mismatches, counts). The day-0 table off THIS tree's board and store."""
    board_path = os.path.join(root, board_rel)
    if not os.path.isfile(board_path):
        raise EmitError('there is no board at %s. The emitter READS the tree\'s board of record; '
                        'it never builds one.' % board_rel)
    ns = _engine(root)
    MA = ns['MA']
    derived = ns['_entry29b_derived']
    fade = ns['o31_D']
    price_of = ns.get('_entry30b_price')
    printed_by_key = {r['key']: r for r in json.load(open(board_path, encoding='utf-8'))['active']}
    Y = MA.BASE_REF

    rows, mismatches = [], []
    n_nd = n_pool = 0
    for p in MA.data:
        with contextlib.redirect_stdout(io.StringIO()):
            d0 = derived(p, Y)
        if d0 is None:
            continue
        key = p.get('key') or MA.slug(p['player'])
        with contextlib.redirect_stdout(io.StringIO()):
            price = float(price_of(p, Y)) if price_of is not None else float(d0) * float(fade(p, Y))
        d0 = float(d0)
        # fade_D is REPORTED as the ratio the price was actually formed with, so the record can
        # never disagree with the price beside it.
        fade_d = (price / d0) if d0 else float(fade(p, Y))
        board_row = printed_by_key.get(key)
        printed = board_row['v'] if board_row else None
        if printed is None or int(round(price)) != int(printed):
            mismatches.append([key, printed, price])
        if p.get('_pool'):
            n_pool += 1
        else:
            n_nd += 1
        rows.append({'key': key, 'ty': p.get('type'), 'pos': MA.gfut(p), 'pick': p.get('pick'),
                     'cell': ('%s|%s' % (p.get('type'), MA.gfut(p))) if p.get('_pool') else None,
                     'printed': int(printed) if printed is not None else None,
                     'derived_v0': d0, 'fade_D': fade_d, 'day0_price': price})
    rows.sort(key=lambda r: r['key'])
    return rows, mismatches, {'base_ref': Y, 'n_wired': len(rows), 'n_fresh_nd': n_nd,
                              'n_pool': n_pool,
                              'engine_predicate': '_entry30b_price' if price_of is not None
                                                  else '_entry29b_derived * o31_D'}


def diff(reference_rows, new_rows):
    """The M1b diff object: population change plus EVERY moved printed row. No truncation."""
    old = {r['key']: r for r in reference_rows}
    new = {r['key']: r for r in new_rows}
    common = sorted(set(old) & set(new))
    return {
        'added': sorted(set(new) - set(old)),
        'dropped': sorted(set(old) - set(new)),
        'printed_moved': [{'key': k, 'printed_old': old[k].get('printed'),
                           'printed_new': new[k].get('printed'),
                           'fade_D_old': old[k].get('fade_D'), 'fade_D_new': new[k].get('fade_D'),
                           'derived_v0': new[k].get('derived_v0')}
                          for k in common if old[k].get('printed') != new[k].get('printed')],
        'derived_v0_moved': [k for k in common
                             if old[k].get('derived_v0') != new[k].get('derived_v0')],
        'n_common': len(common),
    }


def emit(root, spec, out_rel=None, board_rel=BOARD_REL, log=print):
    """Regenerate, assert, print the mandatory diff, and write. -> the written path.

    Raises EmitError — writing NOTHING — on every refusal: day-0 not activated, no standing
    reference to diff against, or the printed day-0 identity not holding on the board being read.
    """
    d0 = spec.get('day0_rebase') or {'state': 'off'}
    state = str(d0.get('state', 'off')).lower()

    # ---- REFUSAL 1: THE M1b ACTIVATION -----------------------------------------------------------
    if state != 'on':
        raise EmitError(
            'REFUSING TO WRITE: day-0 re-basing is %r in this act spec. The M1b ruling is explicit — '
            '"Day-0 re-basing becomes an explicit, owner-visible, off-by-default input with a '
            'mandatory printed diff of every moved row; a suite inheriting the capability without '
            'the judgement re-bases itself green on the first halt." This emitter regenerates the '
            'standing reference ONLY inside an act whose spec says day0_rebase.state = "on" and '
            'names the owner word that turned it on. Nothing was written.' % state)
    if not str(d0.get('activated_by') or '').strip():
        raise EmitError('REFUSING TO WRITE: day0_rebase is ON and names no owner word '
                        '(day0_rebase.activated_by). Automation never re-bases itself green.')

    ref_rel = d0.get('reference')
    out_rel = out_rel or d0.get('new_reference')
    if not ref_rel or not out_rel:
        raise EmitError('day0_rebase must name BOTH `reference` (the standing file this diffs '
                        'against) and `new_reference` (where the regenerated one is written).')
    ref_path = os.path.join(root, ref_rel)

    # ---- REFUSAL 2: THE MANDATORY DIFF NEEDS SOMETHING TO DIFF AGAINST ---------------------------
    if not os.path.isfile(ref_path):
        raise EmitError(
            'REFUSING TO WRITE: the standing day-0 reference is ABSENT at %s. The printed row diff '
            'is MANDATORY (M1b), so there is no lawful first write: a regeneration nobody can '
            'compare to the reference it replaces is exactly the unreviewable re-base the ruling '
            'exists to prevent. Name the standing reference, or install one deliberately in its own '
            'act.' % ref_rel)
    reference = json.load(open(ref_path, encoding='utf-8'))

    rows, mismatches, counts = compute_rows(root, board_rel)
    board_md5 = _md5(os.path.join(root, board_rel))
    identity = '%d of %d at tolerance 0' % (len(rows) - len(mismatches), len(rows))

    log('=' * 102)
    log('DAY-0 PRINT REFERENCE — REGENERATED FROM THIS TREE  (tools/landing/day0_emit.py)')
    log('=' * 102)
    log('  board      %s   %s' % (board_md5, board_rel))
    log('  store      %s' % _md5(os.path.join(root, STORE_REL)))
    log('  engine     %s   (READ-ONLY: no engine file is touched, no board is built)'
        % _md5(os.path.join(root, ENGINE_HEAD_REL)))
    log('  predicate  %s   BASE_REF %s' % (counts['engine_predicate'], counts['base_ref']))
    log('  activated  %s' % str(d0.get('activated_by'))[:150])
    log('  reference  %s' % ref_rel)
    log('  writing    %s' % out_rel)
    log('')

    # ---- A1, THE ONE ASSERTION, AND IT IS FAIL-CLOSED --------------------------------------------
    log('  A1  printed day-0 identity on the board being read : %s  (fresh ND %d, pool %d)'
        % (identity, counts['n_fresh_nd'], counts['n_pool']))
    if mismatches:
        for k, printed, price in mismatches[:20]:
            log('      %-34s board %-8s recomputed %.6f' % (k, printed, price))
        raise EmitError(
            'THE PRINTED DAY-0 IDENTITY DOES NOT HOLD on %s: %d of %d rows disagree with the board '
            'they are priced from. NOTHING IS WRITTEN. A reference regenerated on a board its own '
            'law does not reproduce is not a reference, it is a record of a broken lens.'
            % (board_rel, len(mismatches), len(rows)))

    # ---- THE MANDATORY PRINTED ROW DIFF ----------------------------------------------------------
    d = diff(reference.get('rows') or [], rows)
    log('')
    log('  THE MANDATORY ROW DIFF vs %s' % ref_rel)
    log('    population  %d row(s) added %s   %d row(s) dropped %s'
        % (len(d['added']), d['added'] or '', len(d['dropped']), d['dropped'] or ''))
    log('    printed day-0 MOVED on %d of %d rows in common — every one printed, no truncation:'
        % (len(d['printed_moved']), d['n_common']))
    for m in d['printed_moved']:
        log('      %-34s %s -> %s   (%+d)'
            % (m['key'], m['printed_old'], m['printed_new'],
               int(m['printed_new']) - int(m['printed_old'])))
    if not d['printed_moved']:
        log('      (none — the standing reference already describes this tree\'s day-0 prints)')
    log('    derived_v0 (the matrix year-0 column) moved on %d row(s)%s'
        % (len(d['derived_v0_moved']),
           (': %s' % d['derived_v0_moved']) if d['derived_v0_moved'] else
           ' — the raw entry object does not move'))

    doc = {
        'generator': 'tools/landing/day0_emit.py',
        'label': 'DAY-0 PRINT REFERENCE — regenerated on the tree\'s own board %s' % board_md5[:8],
        'law': LAW,
        'authority': '%s — day0_rebase ACTIVATED by: %s'
                     % (spec.get('act') or '(act unnamed)', d0.get('activated_by')),
        'activated_by': d0.get('activated_by'),
        'board': board_rel,
        'board_md5': board_md5,
        'store_md5': _md5(os.path.join(root, STORE_REL)),
        'engine_head': _md5(os.path.join(root, ENGINE_HEAD_REL)),
        'engine_predicate': counts['engine_predicate'],
        'as_of_round': _as_of_round(root),
        'base_ref': counts['base_ref'],
        'n_wired': counts['n_wired'],
        'n_fresh_nd': counts['n_fresh_nd'],
        'n_pool': counts['n_pool'],
        'identity_all': identity,
        'mismatches': mismatches,
        'supersedes': '%s (board %s)' % (ref_rel, reference.get('board_md5')),
        'n_byte_identical': d['n_common'] - len(d['printed_moved']),
        'population_added': d['added'],
        'population_dropped': d['dropped'],
        'movers': d['printed_moved'],
        'derived_v0_moved': d['derived_v0_moved'],
        'rows': rows,
    }
    out_path = out_rel if os.path.isabs(out_rel) else os.path.join(root, out_rel)
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    # DETERMINISTIC BYTES: sorted keys, fixed indent, no wall clock anywhere in `doc`. Two runs on
    # one tree produce the same file, and the self-test asserts exactly that.
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(doc, indent=1, sort_keys=True) + '\n')
    log('')
    log('  WRITTEN  %s   md5 %s' % (out_rel, _md5(out_path)))
    return out_path


def _as_of_round(root):
    try:
        with open(os.path.join(root, 'data', 'expected_boot.json'), encoding='utf-8') as fh:
            return json.load(fh).get('as_of_round')
    except (OSError, ValueError):
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description='regenerate the day-0 print reference from this tree')
    ap.add_argument('--spec', required=True, help='the act spec; day0_rebase must be ON')
    ap.add_argument('--root', default=None, help='the repo root (default: this file\'s repo)')
    ap.add_argument('--out', default=None,
                    help='override day0_rebase.new_reference (testing; the act spec is the source)')
    ap.add_argument('--board', default=BOARD_REL, help='the board to price against')
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root or os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
    with open(a.spec, encoding='utf-8') as fh:
        spec = json.load(fh)
    try:
        emit(root, spec, out_rel=a.out, board_rel=a.board)
    except EmitError as e:
        print('')
        print('DAY-0 EMITTER HALT — NOTHING WAS WRITTEN')
        print('  %s' % e)
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
