"""tools/landing/spec.py — THE ACT SPEC: the fixed slots a landing is told, and nothing else.

WHAT THIS FILE REPLACES. Every landing on 2026-08-20 wrote five scripts whose only real content was
a dozen constants: this act's predicted board, this act's must-not-move list, this act's column id
and label, this act's lineage prose. `land_f5_pins.py` and `land_br_pins.py` differ in FOUR literals
and one docstring. That is the definition of a thing that should be data.

THE SPEC IS AN INPUT AND THE PREDICTION IS PART OF IT. PLAN_v6 2a.1 requires the lander to "assert
predicted board identity" — the prereg's prediction is supplied to the lander BEFORE the build, and
the build is measured against it. A lander that learned the expected board from the build it just
ran would assert nothing at all; that is the shape of instrument the estate has retired four times.

THE SPEC NEVER CARRIES A VALUE THE TREE CAN MEASURE. `board_after` is a PREDICTION, so it is here.
`store`, `config`, `rl_model` and `fv` are MEASUREMENTS, so they are not: the steps re-measure them
from the checkout and assert against the accepted manifest, exactly as `land_f5_contract.py` did.
The spec says which of them are ALLOWED to move — a policy statement, which is the seat's to make
and the tree's to check.

FAIL-CLOSED SHAPE VALIDATION, and it collects every problem rather than raising on the first: a seat
writing a spec should learn all of its gaps in one run.
"""

import json
import os

SCHEMA_VERSION = 1
ACT_KINDS = ('lever-landing', 'round-advance')

#: Every identity the lander tracks in `data/expected_boot.json`. `moves`/`unmoved` must partition it.
TRACKED_IDENTITIES = ('board', 'store', 'engine_head', 'rl_model', 'fv', 'config', 'register',
                      'balanced_board_md5', 'as_of_round', 'v0surf', 'band', 'q97m', 'peak_model',
                      'bust_prior', 'pvc_snapshot', 'release_version', 'rl_model_data', 'season_state')

#: Slots every act spec must fill. Absent slot = refused; the point is that an unfilled slot is
#: VISIBLE, which is the same argument tools/claims.py makes for its own fixed schema.
REQUIRED_SLOTS = ('schema_version', 'act_kind', 'act', 'date', 'owner_word', 'authority',
                  'prereg', 'identities', 'column', 'lineage', 'day0_rebase', 'evidence_dir')

REQUIRED_PREREG = ('path', 'board_after')


class SpecError(RuntimeError):
    """A spec that cannot be trusted to describe the act. Never partially accepted."""


def _declared_no_op(doc):
    """A REHEARSAL: the act predicts the board it already has, so nothing is owed downstream.

    This is the only shape in which `identities.moves` may be empty and no column is owed, and it
    has to be DECLARED (board_before == board_after) rather than inferred from an empty list — an
    empty list is also what a spec looks like when a seat has not filled it in yet.
    """
    pre = doc.get('prereg') or {}
    return bool(pre.get('board_before')) and pre.get('board_before') == pre.get('board_after')


def validate(doc):
    """-> [problems]. Empty list means the spec is structurally fit to drive a landing."""
    bad = []
    for slot in REQUIRED_SLOTS:
        if slot not in doc:
            bad.append('missing required slot %r' % slot)
    if doc.get('schema_version') != SCHEMA_VERSION:
        bad.append('schema_version %r != %r' % (doc.get('schema_version'), SCHEMA_VERSION))
    if doc.get('act_kind') not in ACT_KINDS:
        bad.append('act_kind %r is not one of %s' % (doc.get('act_kind'), '/'.join(ACT_KINDS)))
    if not doc.get('owner_word'):
        bad.append('owner_word is empty — a landing records the word that authorised it, verbatim')

    pre = doc.get('prereg')
    if not isinstance(pre, dict):
        bad.append('prereg must be an object naming the prereg path and its board prediction')
    else:
        for k in REQUIRED_PREREG:
            if not pre.get(k):
                bad.append('prereg.%s is required — the PREDICTION is an input to the lander, never '
                           'a value it learns from its own build' % k)
        b = pre.get('board_after')
        if b and (len(str(b)) != 32 or any(c not in '0123456789abcdef' for c in str(b))):
            bad.append('prereg.board_after %r is not an md5' % b)
        rb = pre.get('board_before')
        if rb and (len(str(rb)) != 32 or any(c not in '0123456789abcdef' for c in str(rb))):
            bad.append('prereg.board_before %r is not an md5' % rb)
        ks = pre.get('kill_switch')
        if ks is not None:
            if not isinstance(ks, dict):
                bad.append('prereg.kill_switch must be an object or null')
            else:
                for k in ('name', 'env', 'board_with_switch_off'):
                    if k not in ks:
                        bad.append('prereg.kill_switch.%s is required when a switch is declared' % k)

    ids = doc.get('identities')
    if not isinstance(ids, dict):
        bad.append('identities must be an object with `moves` and `unmoved`')
    else:
        moves = list(ids.get('moves') or ())
        unmoved = list(ids.get('unmoved') or ())
        if not moves and not _declared_no_op(doc):
            bad.append('identities.moves is empty — a landing that moves no identity is not a '
                       'landing. If this is a REHEARSAL, declare it: set prereg.board_before equal '
                       'to prereg.board_after and the lander runs the whole sequence as a no-op.')
        overlap = sorted(set(moves) & set(unmoved))
        if overlap:
            bad.append('identities %s are declared BOTH moving and unmoved' % overlap)
        for k in moves + unmoved:
            if k not in TRACKED_IDENTITIES:
                bad.append('identity %r is not one this lander tracks (%s)'
                           % (k, ', '.join(TRACKED_IDENTITIES)))

    col = doc.get('column')
    if col is not None:
        if not isinstance(col, dict):
            bad.append('column must be an object or null (null = this act writes no column)')
        else:
            for k in ('id', 'label', 'after_round'):
                if k not in col:
                    bad.append('column.%s is required' % k)

    lin = doc.get('lineage')
    if lin is not None:
        if not isinstance(lin, dict):
            bad.append('lineage must be an object or null (null = no out-of-round entry is owed)')
        else:
            for k in ('doc', 'owner_ruling_id', 'owner_ruling', 'authority'):
                if not lin.get(k):
                    bad.append('lineage.%s is required — the owner citation is an INPUT to the '
                               'lander, never composed by it' % k)

    d0 = doc.get('day0_rebase')
    if not isinstance(d0, dict):
        bad.append('day0_rebase must be an object; use {"state": "off"} to state the default')
    else:
        st = str(d0.get('state', 'off')).lower()
        if st not in ('off', 'on'):
            bad.append('day0_rebase.state %r is neither on nor off' % d0.get('state'))
        if st == 'on':
            if not d0.get('activated_by'):
                bad.append('day0_rebase is ON and names no owner word. The M1b ruling is explicit: '
                           'automation never re-bases itself green. Day-0 re-basing is EXPLICIT, '
                           'OFF-BY-DEFAULT and owner-visible.')
            for k in ('reference', 'new_reference'):
                if not d0.get(k):
                    bad.append('day0_rebase.%s is required when the re-base is activated' % k)

    if doc.get('act_kind') == 'lever-landing' and doc.get('column') is None and \
            'board' in list((doc.get('identities') or {}).get('moves') or ()):
        bad.append('this act moves the BOARD out of round and declares no column. The standing owner '
                   'rule of 2026-07-28 writes a column whenever the board moves outside a round; if '
                   'this act is genuinely exempt, say so in column._exempt_because.')
    return bad


def load(path):
    """Read and validate a spec file. Raises SpecError listing EVERY problem."""
    with open(path, encoding='utf-8') as fh:
        doc = json.load(fh)
    problems = validate(doc)
    if problems:
        raise SpecError('act spec %s cannot drive a landing — %d problem(s):\n  - %s'
                        % (path, len(problems), '\n  - '.join(problems)))
    doc.setdefault('_spec_path', os.path.abspath(path))
    return doc


def template(act_kind='lever-landing'):
    """A blank spec with every slot present, for a seat starting a new act."""
    return {
        '_doc': ('THE ACT SPEC — the fixed slots `land lever` is told. Fill every one. A slot left '
                 'at its placeholder is refused by spec.validate(), which is the point.'),
        'schema_version': SCHEMA_VERSION,
        'act_kind': act_kind,
        'act': '',
        'date': '',
        'owner_word': '',
        'authority': '',
        'prereg': {
            'path': '',
            'board_before': None,
            'board_after': '',
            '_doc_board_after': 'THE PREDICTION, from the prereg, committed before the engine edit.',
            'reference_board': None,
            '_doc_reference_board': ('a board this build must reproduce byte-exact where one exists '
                                     '(the control arm); null when the act has no reference.'),
            'kill_switch': None,
            '_doc_kill_switch': ('{"name","env":{...},"board_with_switch_off"} when the act declares '
                                 'a switch; the lander then builds with it OFF and asserts.'),
        },
        'identities': {'moves': ['board'],
                       'unmoved': ['store', 'engine_head', 'rl_model', 'fv', 'config', 'register',
                                   'as_of_round']},
        'column': {'id': '', 'label': '', 'after_round': 0},
        'lineage': {'doc': '', 'owner_ruling_id': [], 'owner_ruling': '', 'authority': '',
                    'invariants': {}},
        'day0_rebase': {'state': 'off'},
        'evidence_dir': '',
        'gates': None,
        '_doc_gates': 'null = the standard landing gate set (steps.DEFAULT_GATES).',
    }
