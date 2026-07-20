"""FAST focused unit test — weekly updater snapshot identity + pre-staging refusals (no board regen).

Runs in ~1s against a MINIMAL scratch (a copy of the store + an empty ledger + a manifest) — NEVER the
real repo, and only exercises paths that refuse BEFORE any staging, so no board is generated and no
file is ever written. Complements the full failure-injection proof
(session_2026-07-20/weekly_updater_hardening/failure_injection_proof.py), which covers the write path,
rollback and crash recovery end-to-end.

Run:  python3 engine/rl_after/ingestion/test_weekly_updater.py     (or under pytest)
Exit 0 = PASS.
"""
import os, sys, json, shutil, tempfile, copy

HERE = os.path.dirname(os.path.abspath(__file__))
RA = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, RA)

import round_entry as RE            # noqa: E402
import staged_apply as SA           # noqa: E402
import score_ingestor as SI         # noqa: E402

REAL_STORE = os.path.join(RA, 'rl_model_data.json')


def _mini_repo():
    """A minimal scratch repo: store copy + empty ledger + a manifest pin. Enough for every
    pre-staging refusal; NOT enough to regenerate a board (and we never reach that path)."""
    d = tempfile.mkdtemp(prefix='wkut_')
    os.makedirs(os.path.join(d, 'engine', 'rl_after', 'ingestion'))
    os.makedirs(os.path.join(d, 'data', 'rl_build'))
    shutil.copyfile(REAL_STORE, os.path.join(d, 'engine', 'rl_after', 'rl_model_data.json'))
    with open(os.path.join(d, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json'), 'w') as f:
        json.dump({'version': 1, 'applied': []}, f)
    with open(os.path.join(d, 'data', 'expected_boot.json'), 'w') as f:
        json.dump({'store': RE.md5_of_file_full(REAL_STORE), 'board': 'x' * 32}, f)
    return d


def _snapshot(store_path, rnd=15, n=4):
    store = json.load(open(store_path))
    active = [r for r in store if r.get('stable_player_id') and not r.get('_retired')][:n]
    body = "\n".join("%s,%s" % (r['player'], 80 + i * 9) for i, r in enumerate(active))
    ent = RE.RoundEntry(rnd, store_path=store_path)
    resolved, residue = ent.resolve_body(body)
    assert not residue
    return ent.build_snapshot(resolved, generated_at="2026-07-20T00:00:00Z")


def _arm():
    SI.APPLY_DEFAULT = True
    os.environ['INGEST_SCORE_APPLY'] = 'unit-test-token'


def _disarm():
    SI.APPLY_DEFAULT = False
    os.environ.pop('INGEST_SCORE_APPLY', None)


def _expect(applier, snap, exc, backstop=True):
    """apply_snapshot(snap) must raise `exc` BEFORE any staging. A backstop fault at every phase
    guarantees nothing stages even if a refusal were missing (it would surface as an AssertionError)."""
    def _backstop(phase):
        raise AssertionError("reached staging phase %r — a pre-staging refusal was missed" % phase)
    applier.fault = _backstop if backstop else None
    try:
        applier.apply_snapshot(snap, generated_at="2026-07-20T00:00:00Z")
    except exc:
        return True
    finally:
        applier.fault = None
    raise AssertionError("expected %s, got no raise" % exc.__name__)


def test_snapshot_identity():
    snap = _snapshot(REAL_STORE)
    assert RE.is_strong(snap)
    ok, reason = RE.verify_snapshot(snap)
    assert ok and reason == 'ok', reason
    assert snap['source_store_md5_full'] == RE.md5_of_file_full(REAL_STORE)
    assert snap['source_store_md5'] == RE.md5_of_file(REAL_STORE)
    assert len(snap['source_store_md5_full']) == 32 and len(snap['source_store_md5']) == 8
    # tamper -> content hash fails
    bad = copy.deepcopy(snap); bad['resolved'][0]['score'] = 12345.0
    ok2, _ = RE.verify_snapshot(bad)
    assert not ok2
    # v1 legacy still loads but is NOT strong
    v1 = {'kind': 'round_entry_snapshot', 'round': 1, 'season_year': 2026, 'resolved': [],
          'skipped': [], 'counts': {'resolved': 0, 'skipped': 0, 'residue_open': 0},
          'source_store_md5': 'abcd1234'}
    okv1, rv1 = RE.verify_snapshot(v1)
    assert okv1 and rv1 == 'legacy-v1-no-content-hash'
    assert not RE.is_strong(v1)
    print("  test_snapshot_identity PASS")


def test_bridge_preserves_score_meaning():
    from score_ingestor import ScoreIngestor
    from round_score_parser import parse_feed
    store = json.load(open(REAL_STORE))
    active = [r for r in store if r.get('stable_player_id') and not r.get('_retired')][:6]
    scores = {r['key']: 100.0 + i * 5 for i, r in enumerate(active)}
    body = "\n".join("%s,%s" % (r['player'], scores[r['key']]) for r in active)
    ent = RE.RoundEntry(15, store=store)
    resolved, _ = ent.resolve_body(body)
    snap = ent.build_snapshot(resolved, generated_at="X")
    bridge = {a.key: a.merged_entry for a in SA.preview_from_snapshot(snap, store).appends}
    feed = json.dumps([{'player': r['player'], 'round': 15, 'score': scores[r['key']],
                        'played': 1, 'club': r.get('afl_club')} for r in active])
    ref = {a.key: a.merged_entry for a in ScoreIngestor(store=store).preview(parse_feed(feed)).appends}
    assert set(bridge) == set(ref) and all(bridge[k] == ref[k] for k in bridge)
    print("  test_bridge_preserves_score_meaning PASS")


def test_gate_off_by_default():
    d = _mini_repo()
    try:
        _disarm()
        snap = _snapshot(os.path.join(d, 'engine', 'rl_after', 'rl_model_data.json'))
        ap = SA.StagedRoundApplier.for_repo(d)
        _expect(ap, snap, SI.IngestionGatedError)
        print("  test_gate_off_by_default PASS")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_prestaging_refusals():
    d = _mini_repo()
    sp = os.path.join(d, 'engine', 'rl_after', 'rl_model_data.json')
    before = RE.md5_of_file_full(sp)
    try:
        _arm()
        good = _snapshot(sp)

        # altered content hash
        bad = copy.deepcopy(good); bad['resolved'][0]['score'] = 999.0
        _expect(SA.StagedRoundApplier.for_repo(d), bad, SA.AlteredSnapshotError)

        # not-strong (v1) snapshot
        v1 = copy.deepcopy(good); del v1['content_hash']; del v1['source_store_md5_full']
        v1['snapshot_schema_version'] = 1
        _expect(SA.StagedRoundApplier.for_repo(d), v1, SA.AlteredSnapshotError)

        # stale: snapshot stamped against a different store md5
        stale = copy.deepcopy(good); stale['source_store_md5_full'] = 'f' * 32
        stale['content_hash'] = RE.compute_content_hash(stale)
        _expect(SA.StagedRoundApplier.for_repo(d), stale, SA.StaleSnapshotError)

        # residue open
        res = copy.deepcopy(good); res['counts']['residue_open'] = 1
        res['content_hash'] = RE.compute_content_hash(res)
        _expect(SA.StagedRoundApplier.for_repo(d), res, SA.ResidueOpenError)

        # invalid round (season bound)
        r99 = _snapshot(sp, rnd=99)
        _expect(SA.StagedRoundApplier.for_repo(d), r99, SA.SeasonBoundError)

        # dedup: seed the ledger with this round's triples
        led_path = os.path.join(d, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json')
        triples = [SA.ledger_key(r['stable_player_id'], good['season_year'], good['round'])
                   for r in good['resolved']]
        with open(led_path, 'w') as f:
            json.dump({'version': 1, 'applied': sorted(triples)}, f)
        _expect(SA.StagedRoundApplier.for_repo(d), good, SA.DuplicateRoundError)

        assert RE.md5_of_file_full(sp) == before, "store must be byte-unchanged after every refusal"
        print("  test_prestaging_refusals PASS")
    finally:
        _disarm()
        shutil.rmtree(d, ignore_errors=True)


def main():
    tests = [test_snapshot_identity, test_bridge_preserves_score_meaning,
             test_gate_off_by_default, test_prestaging_refusals]
    print("weekly-updater fast tests:")
    for t in tests:
        t()
    print("ALL FAST TESTS PASS")
    return 0


if __name__ == '__main__':
    sys.exit(main())
