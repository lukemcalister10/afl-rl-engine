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
ACT_KINDS = ('lever-landing', 'round-advance', 'store-edit')
#: the home-and-away season; a feed round above it is a finals week, which HOLDS the calendar
HOME_AND_AWAY_ROUNDS = 24
#: ...and the finals end. Feed rounds 25-29 are FW1/FW2/SF/PF/GF; there is no round 30. The ceiling
#: is load-bearing, not decoration: without it `min(n, HOME_AND_AWAY_ROUNDS)` reads ANY round above
#: 24 as "a finals week holding the calendar at 24", so a spec claiming round 99 describes a tree
#: standing at 24 and passes. Named week-by-week in round_movers.FINALS_WEEK_NAMES, which this must
#: agree with (tools/landing/test_finals_bounds.py asserts they do).
FINALS_FEED_CEILING = 29

#: Every identity the lander tracks in `data/expected_boot.json`. `moves`/`unmoved` must partition it.
TRACKED_IDENTITIES = ('board', 'store', 'engine_head', 'rl_model', 'fv', 'config', 'register',
                      'balanced_board_md5', 'as_of_round', 'v0surf', 'band', 'q97m', 'peak_model',
                      'bust_prior', 'pvc_snapshot', 'release_version', 'rl_model_data', 'season_state')

#: THE SCOPE PARTITION (ORDER 45 attempt-4 class, 2026-08-25; the Graham `_doc_store` precedent).
#: `identities.moves` means MOVES DURING THE LANDING TRANSACTION. An identity that moved at the FLIP
#: COMMIT — before the transaction opened — is byte-stable inside it and belongs in `unmoved`.
#: Declaring it in `moves` used to fail in one of two ways, both discovered mid-transaction:
#:   - a PIN_MEASURERS identity (engine_head, fv, config, ...) HALTED at the pins step, minutes after
#:     the first build: "DECLARED MOVING and the tree says it did not move" (ABORT_pins.json);
#:   - an identity with NO writer of record at all was silently filtered out at the same step — a
#:     declared move that was a complete no-op, which is worse than a halt.
#: Both are now refused at VALIDATION time, seconds after the spec is written. The two tables below
#: are cross-asserted against steps.PIN_MEASURERS / steps.DELEGATED_PINS at steps import (P4: assert
#: the relationship, never this month's list), so they cannot drift from the code that enforces them.
FLIP_SCOPED_IDENTITIES = ('engine_head', 'rl_model', 'fv', 'config', 'v0surf')
NO_WRITER_IDENTITIES = ('band', 'q97m', 'peak_model', 'bust_prior', 'pvc_snapshot', 'release_version')

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

#: THE STORE EDIT'S DECLARATION — the four slots one field edit needs, and no fifth.
#:
#: `old` IS AN ASSERTION, NOT A HINT. The lander reads the named row, compares the named field to
#: `old`, and ABORTS on a mismatch — it never repairs, never widens the match, and never edits a row
#: it could not find exactly once. That is the exact-string law in the shape a store edit takes it
#: (ERRATUM E2 class), and it is why the edit is declared as {key, field, old, new} rather than as a
#: patch: a patch says what to write, a declaration says what must be TRUE before anything is written.
REQUIRED_EDIT_FIELDS = ('key', 'field', 'old', 'new')


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

    # IS THIS ACT THE ROUND, OR IS IT OUT OF ROUND? That is what decides the two refusals below, and
    # until the finals it was the same question as "is this act_kind round-advance". It is not any
    # more. A FINALS WEEK (feed round 25-29) applies real football to the store but HOLDS the calendar
    # at 24 — `as_of_round` does not move, `calendar_progress` stays 1.00, and a non-finalist's
    # completed season is untouched. By the standing rule of 2026-07-28 a board move that is not the
    # round IS an out-of-round move, so a finals week EARNS its column and its lineage entry exactly
    # as a dial flip does. Refusing them here would have forced the FW1..GF board moves to go
    # unrecorded in the very register that exists to record board moves outside a round.
    _feed = None
    if isinstance(rnd, dict):
        try:
            _feed = int(rnd.get('number'))
        except (TypeError, ValueError):
            _feed = None
    _is_finals = _feed is not None and _feed > HOME_AND_AWAY_ROUNDS
    if _feed is not None and _feed > FINALS_FEED_CEILING:
        bad.append('the act declares feed round %d. The season ends at the Grand Final (feed round '
                   '%d); there is no week past it for the calendar hold to hold FOR, and reading '
                   'one as a finals week would let any number at all name a tree standing at %d.'
                   % (_feed, FINALS_FEED_CEILING, HOME_AND_AWAY_ROUNDS))

    if 'sheet' not in doc:
        bad.append('the `sheet` slot must be PRESENT on a round-advance spec — null when this '
                   'advance re-cuts no sheet. An unfilled slot has to be visible; an absent one is '
                   'indistinguishable from a seat who has not got to it yet.')
    if doc.get('column') is not None and not _is_finals:
        bad.append('a ROUND ADVANCE declares a column. It earns none: the out-of-round history '
                   'column marks a board move OUTSIDE a round (standing owner rule 2026-07-28), and '
                   'this move is the round. (R23 runbook ERRATUM E5.)')
    if doc.get('column') is None and _is_finals:
        bad.append('a FINALS week (feed round %d) declares no column. It earns one: the round is '
                   'HELD at %d, so this is a board move OUTSIDE a round and the standing rule of '
                   '2026-07-28 gives it a column.' % (_feed, HOME_AND_AWAY_ROUNDS))
    if doc.get('lineage') is not None and not _is_finals:
        bad.append('a ROUND ADVANCE declares a lineage entry. It earns none: '
                   'data/release_lineage.json records OUT-OF-ROUND transitions only, and R23\'s '
                   'register tail correctly stayed at the round-22 re-cut boundary. (ERRATUM E5.)')
    if doc.get('lineage') is None and _is_finals:
        bad.append('a FINALS week declares no lineage entry. The board moves and the round does '
                   'not, which is the definition of an out-of-round transition.')
    if _is_finals and not (doc.get('round') or {}).get('clubs_played'):
        bad.append('a FINALS week must declare `round.clubs_played` — the clubs that actually '
                   'played. Without it every active player at a club that did NOT play is recorded '
                   'as a DNP (712 of 804 in FW1), which is the owner ruling of 2026-08-30 exactly '
                   'inverted. It cannot be inferred from the scores file: a club can field a player '
                   'the store has at another club, and three did in FW1.')

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
        elif not isinstance(arming['env'], dict):
            # a string env survived the truthiness test above and then raised AttributeError out of
            # validate(), defeating the collect-every-problem contract (found in the speed-act audit,
            # same wrong-typed-env class as kill_switch attempt 1)
            bad.append('round.arming.env must be an OBJECT of env-var name -> value strings, '
                       'not a %s' % type(arming['env']).__name__)
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


def _validate_edit(doc):
    """The slots `land edit` needs (THE EDIT VERB, directive 2026-08-24), and the one it may omit.

    THE ACT KIND EXISTS BECAUSE OF A MEASURED GAP, and the gap is worth restating where the validator
    enforces its shape. Register v836: an owner-worded one-field store edit was refused three times by
    `land lever`, each refusal byte-exact and CORRECT — the lineage chain demands the store move
    INSIDE the transaction (the source side is measured at HEAD and must bridge from the register
    tail), and the lever sequence has no step that edits a store. A pre-committed store flip is
    therefore unbridgeable by construction. This kind adds the missing step and nothing else.

    WHAT IS REQUIRED HERE AND NOT BY THE OTHER KINDS:

      * `edit.store` — a non-empty list of {key, field, old, new}. `old` is ASSERTED (see
        REQUIRED_EDIT_FIELDS); `old == new` is refused, because an edit that changes nothing is an
        edit nobody needed to authorise and its "abort on mismatch" leg could never fire.
      * `identities.moves` must carry `store`. The act moves the store BY DEFINITION, the pins step
        re-pins it MEASURED-not-typed, and a spec that declared it unmoved would be asking the pins
        step to prove a falsehood.

    WHAT IS OPTIONAL HERE AND NOT ELSEWHERE — `prereg.board_after`:

      * PRESENT: the standing prediction of record; `build_proofs` asserts the built board against it
        BYTE-EXACT, exactly as a lever landing does. This is the shape the Graham re-flight uses
        (82fcd8bb, predicted at prereg 2feaf25 before the store was touched).
      * ABSENT: the DRY RUN is the prediction of record — the owner reads it, gives his word, the spec
        cites the word verbatim, and the same command without `--dry-run` flies. `build_proofs` then
        asserts INTERNAL CONSISTENCY instead (the built board's own sidecar names the POST-edit store
        as its source, and the board moves if and only if the act says it does). It asserts less, and
        it says so in the transcript rather than quietly pretending otherwise.

    `edit.expected_movers` is optional in both shapes and is a FALSIFIER when present: the set of
    board rows whose `v` moved is measured off the two boards and asserted EQUAL to the declaration.
    An empty list is a real prediction (a store edit may legitimately move an identity field and no
    board row); `null` means "not declared" and the movers are printed but asserted against nothing.
    """
    bad = []
    ed = doc.get('edit')
    if not isinstance(ed, dict):
        bad.append('a store-edit act must carry an `edit` block: '
                   '{"store": [{"key", "field", "old", "new"}, ...]}. The edit is DECLARATIVE — the '
                   'lander is told the row, the field, the value it must find and the value to write, '
                   'and it applies the change as a surgical byte replacement inside that row\'s span.')
        return bad

    rows = ed.get('store')
    if not isinstance(rows, list) or not rows:
        bad.append('edit.store must be a NON-EMPTY list of {key, field, old, new}. A store-edit act '
                   'that edits nothing is not a store-edit act.')
    else:
        seen = set()
        for i, e in enumerate(rows):
            if not isinstance(e, dict):
                bad.append('edit.store[%d] must be an object with %s'
                           % (i, ', '.join(REQUIRED_EDIT_FIELDS)))
                continue
            for k in REQUIRED_EDIT_FIELDS:
                if k not in e:
                    bad.append('edit.store[%d].%s is required — `old` is ASSERTED against the store '
                               'before anything is written, and a mismatch is an ABORT, never a '
                               'repair' % (i, k))
            if 'old' in e and 'new' in e and e['old'] == e['new']:
                bad.append('edit.store[%d] declares old == new (%r). An edit that changes nothing '
                           'cannot be told from an edit that failed to apply.' % (i, e['old']))
            pair = (e.get('key'), e.get('field'))
            if all(pair) and pair in seen:
                bad.append('edit.store declares %r twice. Two edits to one field would make the '
                           'second one\'s `old` assertion a statement about the first one\'s output.'
                           % (pair,))
            seen.add(pair)

    mv = ed.get('expected_movers')
    if mv is not None:
        if not isinstance(mv, list):
            bad.append('edit.expected_movers must be a list of {key, before, after} or null '
                       '(null = not declared; [] = the real prediction that NO board row moves)')
        else:
            for i, m in enumerate(mv):
                if not isinstance(m, dict) or any(k not in m for k in ('key', 'before', 'after')):
                    bad.append('edit.expected_movers[%d] must be {"key", "before", "after"}' % i)

    ids = doc.get('identities')
    if isinstance(ids, dict):
        moves = list(ids.get('moves') or ())
        unmoved = list(ids.get('unmoved') or ())
        if 'store' not in moves:
            bad.append('a STORE EDIT moves the store, and `identities.moves` does not declare it. The '
                       'pins step re-pins `store` MEASURED from the tree; a spec that declared it '
                       'unmoved would be asking the tree to agree with a falsehood.')
        if 'store' in unmoved:
            bad.append('`store` is declared UNMOVED by a store-edit act. That is the one thing this '
                       'act kind cannot be.')

    if doc.get('sheet') is not None:
        bad.append('a store-edit act declares a `sheet`. The owner sheet is a ROUND input '
                   '(`land round` is its pin file\'s sole writer, P13); this verb never touches it.')
    if doc.get('round') is not None:
        bad.append('a store-edit act declares a `round`. It HOLDS the round it finds, exactly as a '
                   'lever landing does.')
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
    is_edit = doc.get('act_kind') == 'store-edit'
    if doc.get('edit') is not None and not is_edit:
        bad.append('this spec carries an `edit` block and is act_kind %r. Only a store-edit act has a '
                   'step that applies one; a lever landing or a round advance would run the whole '
                   'sequence and silently ignore the edit, which is the worst of the three outcomes.'
                   % doc.get('act_kind'))
    pre = doc.get('prereg')
    if not isinstance(pre, dict):
        bad.append('prereg must be an object naming the prereg path and its board prediction')
    else:
        # A STORE EDIT NEEDS `board_before` AND MAY OMIT `board_after`. The board it starts from is a
        # FACT of the tree and the movers are measured against it; the board it arrives at is either
        # the standing prereg's prediction or — when the owner is reading a dry run instead — nothing
        # this file is allowed to invent. See `_validate_edit`.
        needed = ('path', 'board_before') if (is_round or is_edit) else REQUIRED_PREREG
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
                # TYPED, not just present (ORDER 45 attempt-1, 2026-08-25: env declared as the STRING
                # "RL_O45=0" passed this validator and died ~2 minutes into the SECOND build inside
                # dict(...) — "dictionary update sequence element #0 has length 1". A wrong-typed
                # switch is refused here, in the first second, with the shape spelled out.)
                if 'name' in ks and not (isinstance(ks.get('name'), str) and ks['name'].strip()):
                    bad.append('prereg.kill_switch.name must be a non-empty string')
                if 'env' in ks:
                    env = ks['env']
                    if not isinstance(env, dict) or not env:
                        bad.append('prereg.kill_switch.env must be a NON-EMPTY OBJECT of env-var '
                                   'name -> value strings, e.g. {"RL_O45": "0"} — not a string, not '
                                   'a list. It is handed verbatim to the switch-off build\'s '
                                   'environment (attempt-1 class, 2026-08-25).')
                    elif not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
                        bad.append('prereg.kill_switch.env carries a non-string key or value — env '
                                   'vars are strings on both sides; write "0", not 0')
                bso = ks.get('board_with_switch_off')
                if bso and (len(str(bso)) != 32 or any(c not in '0123456789abcdef' for c in str(bso))):
                    bad.append('prereg.kill_switch.board_with_switch_off %r is not an md5 — it is '
                               'the byte-exact board the switch-off build must reproduce' % bso)

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
        # THE SCOPE PARTITION (attempt-4 class — see the table comments at the top of this file).
        # `moves` is TRANSACTION scope. Flip-carried identities go in `unmoved`.
        for k in moves:
            if k in FLIP_SCOPED_IDENTITIES:
                bad.append('identities.moves declares %r, which moves at the FLIP COMMIT, not inside '
                           'the landing transaction — the pins step would HALT minutes in with '
                           '"DECLARED MOVING and the tree says it did not move" (ORDER 45 attempt 4, '
                           '2026-08-25). Declare it in `unmoved`: the flip-carried identity is '
                           'byte-stable inside the transaction (the Graham _doc_store precedent).' % k)
            elif k in NO_WRITER_IDENTITIES:
                bad.append('identities.moves declares %r, which has NO writer of record in the '
                           'landing transaction — the pins step would silently ignore it, making the '
                           'declaration a no-op (worse than a halt). It is act-scoped: it moves at a '
                           'bake/flip and rides into the transaction already moved. Declare it in '
                           '`unmoved`.' % k)

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
    if is_edit:
        bad.extend(_validate_edit(doc))

    if doc.get('act_kind') in ('lever-landing', 'store-edit') and doc.get('column') is None and \
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
    if act_kind == 'store-edit':
        return _edit_template()
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


def _edit_template():
    """A blank STORE-EDIT spec (THE EDIT VERB). Every slot present, every placeholder refused.

    THE USER-FRIENDLY LOOP THIS TEMPLATE IS THE FIRST HALF OF, stated where a seat starting an act
    will read it: fill this in, run `tools/land edit --spec <spec> --dry-run`, and hand the owner the
    one-screen summary it prints (store and board old -> new, EVERY mover with its values, the
    identities that move). The dry run writes NOTHING to any carrier — it applies the edit in a
    scratch git worktree and takes the worktree away again. The owner gives his word; the word goes
    into `owner_word` VERBATIM; the same command without `--dry-run` flies. One command to predict,
    one to land.
    """
    return {
        '_doc': ('THE ACT SPEC — the fixed slots `land edit` is told (THE EDIT VERB, directive '
                 '2026-08-24). Fill every one. The three things a tree cannot measure about itself '
                 'are still the only things here: PREDICTIONS, CITATIONS and POLICY — and one more '
                 'that only this kind has, THE EDIT ITSELF, which is an owner-worded instruction '
                 'rather than anything the tree could tell you.'),
        'schema_version': SCHEMA_VERSION,
        'act_kind': 'store-edit',
        'act': '',
        'date': '',
        'owner_word': '',
        '_doc_owner_word': ('THE OWNER\'S WORD, VERBATIM. The store is the ONE SOURCE and its data '
                            'fields are owner-supplied; this verb is a LANE, not an authority.'),
        'authority': '',
        'edit': {
            'store': [{'key': '', 'field': '', 'old': None, 'new': None,
                       '_doc': ('key = the store row\'s `key`; field = the field inside THAT ROW; '
                                'old = the value the lander must FIND (asserted, never repaired — a '
                                'mismatch aborts); new = the value it writes. The replacement is a '
                                'surgical byte replacement inside the row\'s own span: the store\'s '
                                'serialization is not re-emitted, and no byte outside the span may '
                                'move.')}],
            'expected_movers': None,
            '_doc_expected_movers': ('null = not declared (the movers are printed and asserted '
                                     'against nothing). A list of {"key","before","after"} is a '
                                     'FALSIFIER: the movers measured off the two boards must equal '
                                     'it exactly. [] is the real prediction that NO board row moves.'),
        },
        'prereg': {
            'path': '',
            'board_before': '',
            '_doc_board_before': 'the board the edit starts from — a fact of the tree, measured.',
            'board_after': None,
            '_doc_board_after': ('OPTIONAL for this kind. An md5 = the standing prediction of record, '
                                 'asserted BYTE-EXACT at build_proofs. null = the DRY RUN is the '
                                 'prediction of record: build_proofs then asserts internal '
                                 'consistency (the built board\'s sidecar names the POST-edit store) '
                                 'and says in the transcript that it asserted no prediction.'),
            'reference_board': None,
            'kill_switch': None,
            '_doc_kill_switch': ('normally null: a store data edit is not a dial, and its revert is '
                                 'a git revert of the landing commit.'),
        },
        'identities': {'moves': ['board', 'store'],
                       'unmoved': ['engine_head', 'rl_model', 'fv', 'config', 'register', 'v0surf',
                                   'as_of_round']},
        '_doc_identities': ('`store` is REQUIRED in moves — this act moves it by definition and the '
                            'pins step re-pins it MEASURED from the tree, never typed.'),
        'column': {'id': '', 'label': '', 'after_round': 0},
        '_doc_column': ('An out-of-round board move still earns its column — the standing owner rule '
                        'of 2026-07-28 does not care which verb moved the board.'),
        'lineage': {'doc': '', 'owner_ruling_id': [], 'owner_ruling': '', 'authority': '',
                    'kind': 'owner-store-edit', 'invariants': {}},
        '_doc_lineage': ('The entry STRADDLES the edit: `source` is measured from the base commit '
                         '(pre-edit) and `destination` from the live tree (post-edit), because the '
                         'edit is applied IN THE WORK DIR inside this transaction. That is the whole '
                         'reason this verb exists — a pre-committed store flip leaves a source the '
                         'register tail cannot bridge to (register v836, the third abort).'),
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
                             'regenerated file, inside this act\'s evidence dir>"}. LEAVE '
                             '`generator` ABSENT and the CARRIED emitter tools/landing/day0_emit.py '
                             'regenerates the reference from this tree\'s own board and store — it '
                             'is generic, deterministic, and refuses to write unless this spec says '
                             'state=on. Name `generator` only to run a different emitter; declare '
                             '"generator": [] to state that this act supplies new_reference itself. '
                             'The lander runs the generator, prints the mandatory row diff of every '
                             'moved row and installs; it never computes day-0 itself.'),
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
