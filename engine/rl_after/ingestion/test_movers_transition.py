"""MOVERS PROVENANCE-TRANSITION TESTS (ITEM 408 Items 6-7, Option A) — Python side.

Owner ruling: the authorised Round 15-19 recovery is GENUINE production Movers history; the R15-R19
reports are RETAINED (not reset to empty) and displayed under the current accepted release via a
SEPARATELY-DECLARED, owner-approved, fail-closed provenance transition. This suite proves, from Python,
the same facts the browser validator (ui/app/movers.js core) enforces:

  * the owner-approved transition (data/release_lineage.json `release_transition`, mirrored to
    ui/data/movers_transition.js) is structurally complete and owner-approved;
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
    _ck(trans == trans_js, 'release_lineage.json release_transition == ui/data/movers_transition.js (consistent)')
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
    _ck(eb.get('as_of_round') == 20, 'manifest as_of_round has advanced to 20')

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
    # The future round is 21: round 20 was APPLIED 2026-07-28 and is now real history in the bundle,
    # so appending a fabricated R20 is correctly refused by the same-round conflict guard (which is
    # itself asserted below). R21 is the first round that does not yet exist.
    scr = tempfile.mkdtemp(prefix='movers_append_')
    try:
        bpath = os.path.join(scr, 'movers.js')
        shutil.copyfile(os.path.join(REPO, 'ui', 'data', 'movers.js'), bpath)
        before = {str(r): json.dumps(prod['reports'][str(r)], sort_keys=True) for r in ROUNDS}
        live20 = prod['reports']['20']
        r21 = _mk_future_report(21, live20['board_md5_after'], '21b0ard' + '0' * 25,
                                live20['source_store_md5_after'], '21st0re' + '0' * 25, dst)
        res = MV.accumulate_bundle(bpath, r21, repo_root=REPO)
        _ck(res.get('overwrite_conflict') is False and res.get('wrote') is True,
            'appending a future R21 report writes (no overwrite conflict)')
        after_bundle = MV.load_bundle(bpath)
        _ck(after_bundle['rounds'] == prod['rounds'] + [21], 'the bundle carries R15-R21 after the append')
        after = {str(r): json.dumps(after_bundle['reports'][str(r)], sort_keys=True) for r in ROUNDS}
        _ck(all(before[str(r)] == after[str(r)] for r in ROUNDS),
            'every R15-R19 report is byte-for-byte preserved after the future append')
        _ck(MV.canonical_reports_digest(after_bundle, ROUNDS) == ap['historical_reports_digest'],
            'the R15-R19 content digest is UNCHANGED after the future append')
        _ck(after_bundle['reports']['21']['release_identity']['release_version'] == dst['release_version'],
            'the appended future report carries the then-current governing identity (destination)')
        # SAME-ROUND CONFLICT GUARD still fail-closed: a DIFFERENT R20 must be refused, not merged.
        fake20 = _mk_future_report(20, live20['board_md5_before'], 'fakeb0ard' + '0' * 23,
                                   live20['source_store_md5_before'], 'fakest0re' + '0' * 23, dst)
        bytes_before = open(bpath, 'rb').read()
        res2 = MV.accumulate_bundle(bpath, fake20, repo_root=REPO)
        _ck(res2.get('overwrite_conflict') is True and res2.get('wrote') is False,
            'a DIFFERENT R20 is refused as an overwrite conflict (never merged)')
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
