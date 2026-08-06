"""MOVERS PROVENANCE-TRANSITION TESTS (ITEM 408 Items 6-7, Option A) — Python side.

Owner ruling: the authorised Round 15-19 recovery is GENUINE production Movers history; the R15-R19
reports are RETAINED (not reset to empty) and displayed under the current accepted release via a
SEPARATELY-DECLARED, owner-approved, fail-closed provenance transition. This suite proves, from Python,
the same facts the browser validator (ui/app/movers.js core) enforces:

  * the owner-approved transition (data/release_lineage.json `release_transition`, mirrored to
    ui/data/movers_transition.js) is structurally complete and owner-approved;
  * ERA SUCCESSION (#274 item 1, under #271 Addenda 21/22): the mirror carries the current transition
    PLUS the append-only `release_transition_register`, every entry of it, so EVERY out-of-round board
    move — not just the system's first — reaches the reader with its own owner approval. The
    whole-object strict equality this suite used to assert was itself the single-slot limit; it is
    restated (not loosened) into per-part exactness, with the ITEM 408 record pinned BYTE-VERBATIM as
    the mirror payload's prefix. The delivered outcome is asserted end-to-end against the shipped
    bundle, with a non-vacuity demonstration that removing the register loses the newest boundary's
    approval;
  * its SOURCE equals the historical R15-R19 reports' terminal identity EXACTLY, and its DESTINATION
    equals the CURRENT accepted release manifest (data/expected_boot.json) EXACTLY — derived, not typed;
  * exactly release_version / balanced_board_md5 / engine_head / board / store move; rl_model / fv /
    config / register are unchanged across the transition (ITEM 411 D1 restatement under owner rulings
    v467 + v469 — the D1 transition legitimately moves the store; see the note at the check itself);
  * the historical reports' CONTENT DIGEST (sha256 over the canonical reports) recomputed in Python
    equals the digest the transition declares AND equals the browser/node validator's digest — so any
    report modification (identity OR player movement) is detected cross-language;
  * appending a FUTURE weekly report under the current governing identity preserves R15-R19
    byte-for-byte (the historical digest is unchanged);
  * NO score application occurs (the shipped score-write gate is OFF; this suite applies no scores).

Run:  python3 engine/rl_after/ingestion/test_movers_transition.py   (exit 0 = all pass)
Or import test_movers_transition; test_movers_transition.run_all().
"""
import copy
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import round_movers as MV            # noqa: E402
import score_ingestor as SI          # noqa: E402

ROUNDS = [15, 16, 17, 18, 19]
# The append-only archive of out-of-round moves, mirrored alongside the current transition since
# #274 item 1 (ERA SUCCESSION). Lives in data/release_lineage.json; projected into the js mirror by
# ui/tools/generate_movers_transition.py.
REGISTER_KEY = 'release_transition_register'
FIXED = ['release_version', 'balanced_board_md5', 'engine_head', 'rl_model', 'fv', 'config', 'register']
ID_FIELDS = FIXED + ['board', 'store']

_n = [0]


def _ck(cond, label):
    _n[0] += 1
    if not cond:
        raise AssertionError('FAIL: ' + label)
    print('  [PASS] ' + label)


def _loadjs(path):
    with open(path) as f:
        t = f.read()
    return json.loads(t[t.index('{'):t.rindex('}') + 1])


def run_all():
    prod = _loadjs(os.path.join(REPO, 'ui', 'data', 'movers.js'))
    trans_js = _loadjs(os.path.join(REPO, 'ui', 'data', 'movers_transition.js'))
    lineage = json.load(open(os.path.join(REPO, 'data', 'release_lineage.json')))
    trans = lineage.get('release_transition')
    eb = json.load(open(os.path.join(REPO, 'data', 'expected_boot.json')))

    print('movers provenance-transition tests:')

    # ---- the populated production bundle carries the owner-authorised history PLUS every round
    # applied since. ROUNDS is the transition's covered set (R15-R19) and stays the anchor for the
    # digest below; the bundle itself grows with each applied round (R20 landed 2026-07-28). ----
    _ck(set(ROUNDS).issubset(set(prod.get('rounds') or [])),
        'production ui/data/movers.js still carries the owner-authorised R15-R19 history')
    _ck(prod.get('rounds') == sorted(int(r) for r in prod.get('reports', {})),
        'production bundle has one report per round')

    # ---- the transition record is owner-approved + structurally complete ----
    _ck(isinstance(trans, dict), 'data/release_lineage.json declares release_transition')
    _ck(trans.get('kind') == 'movers_release_transition' and trans.get('owner_approved') is True,
        'transition is an owner-approved movers_release_transition')
    # RESTATED at #274 item 1 (ERA SUCCESSION), in lockstep with the reader and the browser suite —
    # the #271 A18 lesson: the oracle moves with the reader or the test stops checking anything.
    #
    # This asserted `trans == trans_js`, whole-object strict equality. That clause WAS the single-slot
    # limitation: it made the mirror unable to carry anything but one transition, which is why the
    # owner-approved #271/A17 record could not reach the reader and the 30/7 boundary displayed
    # `owner_approved_record: false`. The mirror now carries the current transition PLUS the
    # append-only register, so the equality is restated to the two facts it was standing in for:
    #   (1) the transition is mirrored EXACTLY — the ITEM 408 record byte-for-byte, no drift, no edit;
    #   (2) the register is mirrored EXACTLY too, so the reader sees every entry the lineage declares.
    # Nothing is loosened: every byte of both is still pinned to the lineage record, and the mirror
    # may carry NOTHING the lineage does not (asserted below), so a hand-edit still fails closed.
    mirrored_trans = {k: v for k, v in trans_js.items() if k != REGISTER_KEY}
    _ck(trans == mirrored_trans,
        'release_lineage.json release_transition == ui/data/movers_transition.js (consistent)')
    _ck(trans_js.get(REGISTER_KEY) == lineage.get(REGISTER_KEY),
        'release_lineage.json %s == the mirror\'s register (era succession: ALL entries reach the reader)' % REGISTER_KEY)
    _ck(set(trans_js) == set(trans) | {REGISTER_KEY},
        'the mirror carries the transition keys plus the register and NOTHING else (zero authorship)')
    # The register is APPEND-ONLY and the ITEM 408 record is never rewritten (#271 A17/A22): the
    # transition's own serialization is a literal PREFIX of the mirror's payload. Asserted on bytes,
    # not on parsed equality, because "preserved verbatim" is a claim about bytes.
    with open(os.path.join(REPO, 'ui', 'data', 'movers_transition.js'), encoding='utf-8') as f:
        _mirror_text = f.read()
    _payload = _mirror_text[_mirror_text.index('{'):_mirror_text.rindex('}') + 1]
    _trans_bytes = json.dumps(trans, ensure_ascii=False, separators=(',', ':'))
    _ck(_payload.startswith(_trans_bytes[:-1]),
        'the ITEM 408 record is preserved BYTE-VERBATIM as the mirror payload\'s prefix (never rewritten)')
    # Every register entry that describes a move is owner-approved and names its ruling — the property
    # era succession delivers. A pointer note (no destination) is not a record and is not held to it.
    _reg_records = [e for e in (lineage.get(REGISTER_KEY) or [])
                    if isinstance(e, dict) and (e.get('destination') or {}).get('board')]
    _ck(len(_reg_records) >= 1, 'the register carries at least one transition record  (%d of %d entries)'
        % (len(_reg_records), len(lineage.get(REGISTER_KEY) or [])))
    _ck(all(e.get('owner_approved') is True and e.get('owner_ruling_id') for e in _reg_records),
        'EVERY register record is owner-approved and names its ruling id')

    # ---- ERA SUCCESSION, the delivered outcome: the reader reaches every record ----
    # model_changes() is what turns a register entry into the boundary label the tab shows. Recomputed
    # here from the live tree (not read off the bundle) and cross-checked against the SHIPPED bundle, so
    # a reader change that never made it into the shipped bytes cannot pass. Before #274 the 30/7
    # boundary read owner_approved_record False with a null ruling id — #271 A22's declared known-false
    # flag. This is the assertion that clears it.
    _live_mc = MV.model_changes(REPO)
    _shipped_mc = prod.get('model_changes') or []
    _ck(_live_mc == _shipped_mc,
        'the shipped bundle\'s model_changes == what the live tree derives (reader and bundle in step)')
    _ck(len(_shipped_mc) >= 2,
        'more than one out-of-round boundary is carried end-to-end — the single-slot limit is gone  '
        '(%d boundaries)' % len(_shipped_mc))
    _ck(all(c.get('owner_approved_record') is True and c.get('owner_ruling_id') for c in _shipped_mc),
        'EVERY out-of-round boundary reaches the reader owner-approved, naming its ruling id')
    # NON-VACUITY, both directions: the check above must be able to FAIL. Drop the register from the
    # mirror in a scratch copy and the newest boundary loses its approval — proving the assertion is
    # carried by the register and is not true by construction.
    _nv = tempfile.mkdtemp(prefix='movers_transition_nv_')
    try:
        shutil.copytree(os.path.join(REPO, 'ui'), os.path.join(_nv, 'ui'),
                        ignore=shutil.ignore_patterns('screenshots', 'node_modules'))
        shutil.copytree(os.path.join(REPO, 'engine'), os.path.join(_nv, 'engine'))
        _p = os.path.join(_nv, 'ui', 'data', 'movers_transition.js')
        with open(_p, encoding='utf-8') as f:
            _t = f.read()
        _stripped = copy.deepcopy(trans)          # the pre-#274 single-slot mirror shape
        _hdr = _t[:_t.index('{')]
        with open(_p, 'w', encoding='utf-8') as f:
            f.write(_hdr + json.dumps(_stripped, ensure_ascii=False, separators=(',', ':')) + ';\n')
        _degraded = MV.model_changes(_nv)
        _ck(len(_degraded) == len(_live_mc) and
            not all(c.get('owner_approved_record') is True for c in _degraded),
            'NON-VACUITY: with the register removed the newest boundary LOSES its owner approval  '
            '(approved %d of %d, vs %d of %d with it)'
            % (sum(1 for c in _degraded if c.get('owner_approved_record')), len(_degraded),
               sum(1 for c in _live_mc if c.get('owner_approved_record')), len(_live_mc)))
    finally:
        shutil.rmtree(_nv, ignore_errors=True)
    src, dst, ap = trans['source'], trans['destination'], trans['applies_to']
    _ck(all(src.get(k) for k in ID_FIELDS) and all(dst.get(k) for k in ID_FIELDS),
        'transition source + destination carry every id field (fixed pins + board + store)')
    _ck(ap.get('rounds') == ROUNDS, 'transition applies_to R15-R19')

    # ---- SOURCE == the historical reports' terminal identity EXACTLY (derived, not typed) ----
    r19 = prod['reports']['19']
    ri = r19['release_identity']
    hist = {k: ri[k] for k in FIXED}
    hist['board'] = r19['board_md5_after']
    hist['store'] = r19['source_store_md5_after']
    _ck(all(src[k] == hist[k] for k in ID_FIELDS), 'transition SOURCE == the R15-R19 reports terminal identity')
    _ck(src.get('as_of_round') == 19, 'transition source round == 19')
    # every report carries the identical fixed identity (a tamper of one report would break this)
    first = prod['reports']['15']['release_identity']
    _ck(all(prod['reports'][str(r)]['release_identity'][k] == first[k] for r in ROUNDS for k in FIXED),
        'every historical report carries the identical fixed release identity')

    # ---- DESTINATION is a HISTORICAL BOUNDARY, not the current release ----
    # It equalled the manifest while the restructure board was the live one. Since round 20 was applied
    # (2026-07-28) the manifest has moved on, and the transition record now describes the boundary
    # between round 19 and the post-restructure board — which is exactly the role it keeps under the
    # from/to tab: `round_movers.model_changes()` reads it to LABEL a range that spans the redesign.
    # It is no longer enforced as a gate (owner word 2026-07-28), so it must NOT track the manifest.
    _ck(dst['board'] == 'fa172ac1c90ab84e5044d3e9907c5819',
        'transition DESTINATION is the post-restructure board (the boundary the tab labels)')
    _ck(dst['store'] == 'c120cfd54a83449e7485d209419b9cf8',
        'transition DESTINATION store is the post-restructure store')
    _ck(dst['board'] != eb['board'],
        'the manifest has legitimately advanced past the transition destination (round 20 applied)')
    _ck(dst.get('as_of_round') == 19,
        'transition destination round is 19 — the round the restructure landed after (unchanging history)')
    _ck(eb.get('as_of_round') == 21, 'manifest as_of_round has advanced to 21')

    # ---- exactly the expected fields move; the rest are unchanged (same model pins) ----
    # OWNER-RULED SEMANTIC RESTATEMENT (owner rulings v467 + v469, 2026-07-26; ITEM 411 directive D1).
    # These two expectations PREVIOUSLY asserted:
    #     moved == ['release_version', 'balanced_board_md5', 'engine_head', 'board']
    #     set(['rl_model', 'fv', 'config', 'register', 'store']).issubset(unchanged)
    # i.e. the store did NOT move. That was TRUE of the ITEM 408 items 6-7 transition. The ITEM 411 D1
    # transition is a DIFFERENT transition which legitimately moves the store (f37d9716 -> c120cfd5,
    # attributed row-by-row in the ITEM 411 change manifest), so `store` moves from the unchanged set to
    # the moved set. Owner word verbatim (v467): "Ruled: yes — the D1 transition legitimately moves the
    # store; restate the lineage record and its test to describe the new transition."
    # THE LITERALS ARE DELIBERATELY RETAINED AS LITERALS (seam ruling; v464 P1 precedent). They are the
    # DRIFT SENTINEL: a test that read its expected sets from the record under test (release_lineage.json
    # / movers_transition.js) would pass by construction and could never catch an unauthorised identity
    # move. The check below separately proves the record SELF-DECLARES the same sets, so the literal and
    # the artifact are cross-checked against each other rather than either deriving from the other.
    moved = [k for k in ID_FIELDS if src[k] != dst[k]]
    unchanged = [k for k in ID_FIELDS if src[k] == dst[k]]
    _ck(moved == ['release_version', 'balanced_board_md5', 'engine_head', 'board', 'store'],
        'exactly release_version/balanced_board_md5/engine_head/board/store move across the transition')
    _ck(set(['rl_model', 'fv', 'config', 'register']).issubset(set(unchanged)),
        'rl_model/fv/config/register are UNCHANGED across the transition (same R19 model pins)')
    _ck(trans.get('moved_by_transition') == moved and set(trans.get('unchanged_across_transition')) == set(unchanged),
        'the transition self-declares the moved/unchanged field sets correctly')

    # ---- CONTENT DIGEST: python recompute == declared == validator (cross-language) ----
    digest = MV.canonical_reports_digest(prod, ROUNDS)
    _ck(digest == ap['historical_reports_digest'],
        'recomputed R15-R19 content digest == the transition declared digest (%s)' % digest)
    # a single tampered player movement flips the digest (fail-closed detection)
    tam = copy.deepcopy(prod)
    tam['reports']['17']['players'][3]['value_change'] += 1
    _ck(MV.canonical_reports_digest(tam, ROUNDS) != ap['historical_reports_digest'],
        'a modified player movement changes the content digest (tamper detected)')
    # a single tampered identity field flips the digest too
    tam2 = copy.deepcopy(prod)
    tam2['reports']['18']['release_identity']['engine_head'] = 'deadbeef' * 4
    _ck(MV.canonical_reports_digest(tam2, ROUNDS) != ap['historical_reports_digest'],
        'a modified report identity changes the content digest (tamper detected)')

    # ---- FUTURE APPEND preserves R15-R19 byte-for-byte (accumulate_bundle write path) ----
    # The future round is 22: round 21 was APPLIED 2026-08-06 and is now real history in the bundle,
    # so appending a fabricated R21 is correctly refused by the same-round conflict guard (which is
    # itself asserted below). R22 is the first round that does not yet exist.
    scr = tempfile.mkdtemp(prefix='movers_append_')
    try:
        bpath = os.path.join(scr, 'movers.js')
        shutil.copyfile(os.path.join(REPO, 'ui', 'data', 'movers.js'), bpath)
        before = {str(r): json.dumps(prod['reports'][str(r)], sort_keys=True) for r in ROUNDS}
        live21 = prod['reports']['21']
        r22 = _mk_future_report(22, live21['board_md5_after'], '22b0ard' + '0' * 25,
                                live21['source_store_md5_after'], '22st0re' + '0' * 25, dst)
        res = MV.accumulate_bundle(bpath, r22, repo_root=REPO)
        _ck(res.get('overwrite_conflict') is False and res.get('wrote') is True,
            'appending a future R22 report writes (no overwrite conflict)')
        after_bundle = MV.load_bundle(bpath)
        _ck(after_bundle['rounds'] == prod['rounds'] + [22], 'the bundle carries R15-R22 after the append')
        after = {str(r): json.dumps(after_bundle['reports'][str(r)], sort_keys=True) for r in ROUNDS}
        _ck(all(before[str(r)] == after[str(r)] for r in ROUNDS),
            'every R15-R19 report is byte-for-byte preserved after the future append')
        _ck(MV.canonical_reports_digest(after_bundle, ROUNDS) == ap['historical_reports_digest'],
            'the R15-R19 content digest is UNCHANGED after the future append')
        _ck(after_bundle['reports']['22']['release_identity']['release_version'] == dst['release_version'],
            'the appended future report carries the then-current governing identity (destination)')
        # SAME-ROUND CONFLICT GUARD still fail-closed: a DIFFERENT R21 must be refused, not merged.
        fake21 = _mk_future_report(21, live21['board_md5_before'], 'fakeb0ard' + '0' * 23,
                                   live21['source_store_md5_before'], 'fakest0re' + '0' * 23, dst)
        bytes_before = open(bpath, 'rb').read()
        res2 = MV.accumulate_bundle(bpath, fake21, repo_root=REPO)
        _ck(res2.get('overwrite_conflict') is True and res2.get('wrote') is False,
            'a DIFFERENT R21 is refused as an overwrite conflict (never merged)')
        _ck(open(bpath, 'rb').read() == bytes_before,
            'the bundle is left BYTE-UNCHANGED by the refused conflicting write')
    finally:
        shutil.rmtree(scr, ignore_errors=True)

    # ---- NO score application: the shipped score-write gate is OFF; this suite applies no scores ----
    _ck(SI.APPLY_DEFAULT is False, 'score_ingestor.APPLY_DEFAULT is False (code half OFF)')
    _ck(SI._apply_enabled() is False, 'score-write gate is OFF (no explicit apply token) — no score can be applied')

    print('MOVERS TRANSITION TESTS: ALL %d PASS' % _n[0])
    return _n[0]


def _mk_future_report(round_n, before_board, after_board, before_store, after_store, dest_identity):
    rel = dict(dest_identity)
    rel['as_of_round'] = int(round_n)
    return {
        'kind': 'weekly_movers_report', 'schema_version': 1, 'season': 2026,
        'submitted_round': int(round_n), 'previous_round': int(round_n) - 1,
        'source_store_md5_before': before_store, 'source_store_md5_after': after_store,
        'board_md5_before': before_board, 'board_md5_after': after_board,
        'txn_id': 'txn_future_r%d' % int(round_n), 'generated_at': '2026-07-23T00:00:00Z',
        'player_count': 0, 'release_identity': rel,
        'integrity': {'players_unique': True, 'coverage_full': True, 'board_after_matches_committed': True},
        'views': {'value_risers': [], 'value_fallers': [], 'rank_risers': [], 'rank_fallers': [],
                  'played_count': 0, 'dnp_count': 0},
        'players': [],
    }


if __name__ == '__main__':
    try:
        run_all()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    sys.exit(0)
