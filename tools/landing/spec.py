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

#: A ROUND ADVANCE PREDICTS ROUND-SHAPED FACTS, NOT A BOARD MD5, and the difference is not a
#: weakening — it is the only honest form the prediction has.
#:
#: A lever landing's board IS predictable: the seat builds the candidate, records the md5 in the
#: prereg, and the lander refuses any other. A ROUND ADVANCE's board is a function of scores nobody
#: has seen until the owner sends them; a seat "predicting" it would be copying it out of a build it
#: had already run, which is the exact instrument shape `spec.py`'s own header refuses.
#:
#: So the round prereg predicts what a seat CAN know before arming, and every one of these is a
#: falsifier the advance step asserts against the tool's own output: the seven facts below are read
#: straight off the R23 evidence's preflight and apply lines (411 listed / 411 resolved / 393 DNP,
#: sha256 e3d5410e0e57, ledger 3,086 -> 3,497). `board_before` is still required and still an md5 —
#: the board the advance STARTS from is a fact of the tree the act was written against.
REQUIRED_ROUND_EXPECTED = ('round', 'listed', 'resolved', 'absent_dnp', 'scores_sha256',
                           'ledger_before', 'ledger_delta')


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


def _validate_round(doc):
    """The slots `land round` needs, and the two a round advance must NOT carry.

    THE TWO REFUSALS ARE THE INTERESTING HALF, and both come from the R23 record rather than from
    taste. `ERRATUM E5`: "A ROUND ADVANCE EARNS NO `data/release_lineage.json` ENTRY. The lineage
    register records OUT-OF-ROUND board moves." A round advance moves the board IN round, so it
    registers no out-of-round column and appends no transition entry — and a spec that declared
    either would drive the shared `lineage` step into writing a record the estate's own gates would
    then have to be taught to forgive. Refused here, at the door.
    """
    bad = []
    pre = doc.get('prereg') or {}
    rnd = doc.get('round')

    if 'sheet' not in doc:
        bad.append('the `sheet` slot must be PRESENT on a round-advance spec — null when this '
                   'advance re-cuts no sheet. An unfilled slot has to be visible; an absent one is '
                   'indistinguishable from a seat who has not got to it yet.')
    if doc.get('column') is not None:
        bad.append('a ROUND ADVANCE declares a column. It earns none: the out-of-round history '
                   'column marks a board move OUTSIDE a round (standing owner rule 2026-07-28), and '
                   'this move is the round. (R23 runbook ERRATUM E5.)')
    if doc.get('lineage') is not None:
        bad.append('a ROUND ADVANCE declares a lineage entry. It earns none: '
                   'data/release_lineage.json records OUT-OF-ROUND transitions only, and R23\'s '
                   'register tail correctly stayed at the round-22 re-cut boundary. (ERRATUM E5.)')

    if not isinstance(rnd, dict):
        bad.append('round must be an object: {"number", "scores", "arming", "identity_overrides"}')
        return bad
    if not str(rnd.get('number') or '').isdigit():
        bad.append('round.number is required and must be the round being applied')

    scores = rnd.get('scores')
    if scores is None:
        # A REHEARSAL. The lander runs the whole sequence with nothing armed and nothing applied —
        # which is the shape of the no-op dry run that proves the machine before its first flight.
        if not _declared_no_op(doc):
            bad.append('round.scores is null and this act is not a declared no-op rehearsal. An '
                       'advance with no owner file to apply advances nothing; if this IS a '
                       'rehearsal, declare it (prereg.board_before == prereg.board_after).')
    else:
        if not isinstance(scores, dict):
            bad.append('round.scores must be an object: {"path", "md5", "sha256"}')
        else:
            for k in ('path', 'md5', 'sha256'):
                if not scores.get(k):
                    bad.append('round.scores.%s is required — the owner\'s file is an INPUT OF '
                               'RECORD and the lander asserts its identity rather than trusting '
                               'whatever is on disk' % k)
        exp = pre.get('round_expected')
        if not isinstance(exp, dict):
            bad.append('prereg.round_expected is required when a scores file is declared: %s'
                       % ', '.join(REQUIRED_ROUND_EXPECTED))
        else:
            for k in REQUIRED_ROUND_EXPECTED:
                if exp.get(k) is None:
                    bad.append('prereg.round_expected.%s is required — it is a FALSIFIER the '
                               'advance step asserts against the tool\'s own output' % k)
        arming = rnd.get('arming')
        if not isinstance(arming, dict) or not arming.get('env') or not arming.get('owner_word'):
            bad.append('round.arming must carry {"env": {...}, "owner_word": "<verbatim>"}. LAW 10 '
                       '(c): arming the score-write needs Luke\'s explicit word, under any level of '
                       'model autonomy. The lander is handed the word and the token; it never '
                       'composes either.')
        elif not str(arming['env'].get('INGEST_SCORE_APPLY') or '').strip() or \
                str(arming['env'].get('INGEST_SCORE_APPLY_ARMED') or '') != '1':
            bad.append('round.arming.env must arm BOTH halves of the gate: '
                       'INGEST_SCORE_APPLY_ARMED=1 and INGEST_SCORE_APPLY=<owner-worded token>')

    sheet = doc.get('sheet')
    if sheet is not None:
        if not isinstance(sheet, dict):
            bad.append('sheet must be an object or null (null = this advance re-cuts no sheet)')
        else:
            for k in ('prereg_lite', 'owner_word', 'disclosed_movers'):
                if sheet.get(k) in (None, ''):
                    bad.append('sheet.%s is required — PLAN_v6 3a: a data change keeps a '
                               'review-forcing step (prereg-lite committed WITH the data change: '
                               'predicted md5 + row/injured-Y counts + disclosed movers)' % k)
            predicted = sheet.get('predicted')
            if not isinstance(predicted, dict):
                bad.append('sheet.predicted must carry the three PREDICTED facts: sheet_md5, '
                           'sheet_rows, sheet_injured_y')
            else:
                for k in ('sheet_md5', 'sheet_rows', 'sheet_injured_y'):
                    if predicted.get(k) in (None, ''):
                        bad.append('sheet.predicted.%s is required' % k)
    return bad


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

    is_round = doc.get('act_kind') == 'round-advance'
    pre = doc.get('prereg')
    if not isinstance(pre, dict):
        bad.append('prereg must be an object naming the prereg path and its board prediction')
    else:
        needed = ('path', 'board_before') if is_round else REQUIRED_PREREG
        for k in needed:
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

    if is_round:
        bad.extend(_validate_round(doc))

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
    if act_kind == 'round-advance':
        return _round_template()
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


def _round_template():
    """A blank ROUND-ADVANCE spec. Every slot present, every placeholder refused by validate()."""
    return {
        '_doc': ('THE ACT SPEC — the fixed slots `land round` is told (PLAN_v6 2b). Fill every one. '
                 'A slot left at its placeholder is refused by spec.validate(), which is the point. '
                 'The three things a tree cannot measure about itself are still the only things '
                 'here: PREDICTIONS, CITATIONS and POLICY.'),
        'schema_version': SCHEMA_VERSION,
        'act_kind': 'round-advance',
        'act': '',
        'date': '',
        'owner_word': '',
        'authority': '',
        'prereg': {
            'path': '',
            'board_before': '',
            '_doc_board_before': 'the board the advance STARTS from — a fact of the tree, measured.',
            'board_after': None,
            '_doc_board_after': ('null for a real advance: a round board is a function of scores '
                                 'nobody has seen yet, and a seat "predicting" it would be copying '
                                 'it out of a build already run. For a REHEARSAL, set it equal to '
                                 'board_before and the lander runs the whole sequence as a no-op.'),
            'round_expected': {'round': 0, 'listed': 0, 'resolved': 0, 'absent_dnp': 0,
                               'scores_sha256': '', 'ledger_before': 0, 'ledger_delta': 0},
            '_doc_round_expected': ('THE ROUND-SHAPED PREDICTION, and every field is a falsifier the '
                                    'advance step asserts against the tool\'s own output.'),
        },
        'round': {
            'number': 0,
            'scores': {'path': 'scores/R00.csv', 'md5': '', 'sha256': ''},
            '_doc_scores': ('the owner\'s file, byte-unmodified. The lander places nothing and edits '
                            'nothing: it asserts this identity against the file on disk.'),
            'identity_overrides': [],
            '_doc_identity_overrides': ('names the lander asserts are bound in '
                                        'engine/rl_after/ingestion/catchup_identity_overrides.json. '
                                        'An owner ruling on a name lives in that file, never in the '
                                        'score file, and the lander AUTHORS none of them.'),
            'arming': {'env': {'INGEST_SCORE_APPLY_ARMED': '1', 'INGEST_SCORE_APPLY': ''},
                       'owner_word': ''},
            '_doc_arming': ('LAW 10(c): arming the score-write needs Luke\'s explicit word. The word '
                            'goes here VERBATIM and the token is his; the lander composes neither.'),
        },
        'sheet': {
            'prereg_lite': '',
            'owner_word': '',
            'disclosed_movers': '',
            'predicted': {'sheet_md5': '', 'sheet_rows': 0, 'sheet_injured_y': 0},
            '_doc': ('null when this advance re-cuts no sheet. When it does: the prereg-lite is '
                     'committed WITH the data change, in the same commit as the sheet and the pin '
                     'file (PLAN_v6 3a / R23 runbook ERRATUM E7).'),
        },
        'identities': {'moves': ['board', 'store', 'as_of_round', 'season_state',
                                 'balanced_board_md5', 'rl_model_data'],
                       'unmoved': ['engine_head', 'rl_model', 'fv', 'config', 'register']},
        'column': None,
        'lineage': None,
        'day0_rebase': {'state': 'off'},
        '_doc_day0_rebase': ('THE ADVANCE IS THE DAY-0 REFERENCE\'S NATURAL HOME (register v810 item '
                             '1) — and it is still EXPLICIT and OFF BY DEFAULT (the M1b ruling). To '
                             'activate: {"state":"on", "activated_by":"<owner word>", '
                             '"reference":"docs/evidence/.../DAY0_CP.json", "new_reference":"<the '
                             'regenerated file>", "generator":["python3","<the emitter of record>"]}'
                             '. The lander runs the generator, prints the mandatory row diff and '
                             'installs; it never computes day-0 itself.'),
        'movers_page': {'output': '', 'boundary_note': ''},
        '_doc_movers_page': ('the owner-facing movers page for this round (PLAN_v6 1d: rendered '
                             'board/movers page delivered at every round). `output` defaults to '
                             'MOVERS_R<N>.html inside the evidence dir; `boundary_note` is the '
                             'seat\'s prose about what sits on which side of the boundary, and the '
                             'lander composes a mechanical one when it is empty.'),
        'evidence_dir': '',
        'gates': None,
        '_doc_gates': 'null = the standard landing gate set (steps.DEFAULT_GATES).',
    }
