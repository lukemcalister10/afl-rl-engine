"""GENERATE the R15-R19 movers EVIDENCE from the catch-up (scratch only, gate OFF).

Runs the controlled five-round catch-up on a DISPOSABLE copy of the accepted Round-14 state (the real
canonical store is NEVER used), which — after each round commits + finalizes — produces a durable
movers report. This script copies the RESULTING artifacts into the SESSION EVIDENCE paths ONLY:

  * session_2026-07-20/live_scoring_catchup/movers_bundle_scratch.js   (the accumulated UI bundle)
  * session_2026-07-20/live_scoring_catchup/movers/                    (per-round movers_R{N}.json + .csv)

IMPORTANT: this NEVER writes the production ui/data/movers.js. These R15-R19 results are DISPOSABLE
scratch proof evidence on their OWN superseded lineage (they begin from the superseded board 270a2c5f),
kept SEPARATE from production. The production bundle carries the OWNER-AUTHORISED R15-R19 recovery
history (ITEM 408 Items 6-7, Option A — the recovery is genuine production Movers history, retained and
bridged to the current accepted release by the owner-approved provenance transition; NOT reset to empty).
This script ASSERTS that its scratch run did not touch production, that production still carries the
owner-authorised R15-R19 history whose content digest matches the owner-approved provenance transition,
and that the disposable scratch lineage stayed separate — so the scratch can never overwrite or erase
the production history.

Run:  python3 session_2026-07-20/live_scoring_catchup/generate_movers_bundle.py
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RA = os.path.join(REPO, 'engine', 'rl_after')
ING = os.path.join(RA, 'ingestion')
WUH = os.path.join(REPO, 'session_2026-07-20', 'weekly_updater_hardening')
FIX = os.path.join(HERE, 'fixtures')
sys.path.insert(0, RA)
sys.path.insert(0, ING)
sys.path.insert(0, WUH)

import round_catchup as RC             # noqa: E402
import round_movers as MV              # noqa: E402
import failure_injection_proof as FI   # noqa: E402  (fixture-coherent scratch + gate helpers)

GEN = "2026-07-20T22:00:00Z"
FILES = [(r, os.path.join(FIX, 'R%d.csv' % r)) for r in (15, 16, 17, 18, 19)]


def main():
    scr = FI.make_scratch('genmovers')
    os.makedirs(os.path.join(scr, 'ui', 'tools'), exist_ok=True)
    os.makedirs(os.path.join(scr, 'ui', 'data'), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, 'ui', 'tools', 'extract_board_view.py'),
                    os.path.join(scr, 'ui', 'tools', 'extract_board_view.py'))
    # the scratch starts from a clean EMPTY bundle (exactly what production ships) so the scratch run
    # accumulates onto the same baseline the production app would.
    MV.init_empty_bundle(os.path.join(scr, 'ui', 'data', 'movers.js'), scr)
    FI.arm()
    try:
        cu = RC.RoundCatchup(scr, FILES)
        pre, _rounds = cu.preflight()
        assert pre['clean'], pre['halt_reasons']
        run = cu.run(approved=True, generated_at=GEN)
        assert not run.get('incomplete'), 'catch-up finalization incomplete: %s' % run
        for r in run['rounds']:
            print("R%d %s final=%s players=%s played=%s dnp=%s board=%s->%s movers=%s" % (
                r['round'], r['status'], r.get('finalization'), r.get('players_applied'),
                r.get('movers_played'), r.get('movers_dnp'), (r.get('board_before') or '')[:8],
                (r.get('board_after') or '')[:8], os.path.basename(r.get('movers_report') or '')))
        # copy the accumulated UI movers bundle -> SESSION EVIDENCE (never production)
        src_bundle = os.path.join(scr, 'ui', 'data', 'movers.js')
        dst_bundle = os.path.join(HERE, 'movers_bundle_scratch.js')
        shutil.copyfile(src_bundle, dst_bundle)
        print("wrote", os.path.relpath(dst_bundle, REPO), "(%d bytes)" % os.path.getsize(dst_bundle))
        # copy the per-round JSON/CSV movers reports -> evidence dir (committed)
        src_movers = os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'movers')
        dst_movers = os.path.join(HERE, 'movers')
        if os.path.isdir(dst_movers):
            shutil.rmtree(dst_movers)
        shutil.copytree(src_movers, dst_movers)
        reports = sorted(os.listdir(dst_movers))
        print("wrote", os.path.relpath(dst_movers, REPO) + "/:", reports)
    finally:
        FI.disarm()
        shutil.rmtree(scr, ignore_errors=True)
    # verify the scratch evidence bundle
    with open(dst_bundle) as f:
        text = f.read()
    obj = json.loads(text[text.index('{'):text.rindex('}') + 1])
    print("scratch evidence bundle rounds:", obj['rounds'], "chain_ok:", obj['integrity']['board_chain_ok'],
          "baseline_anchor_ok:", obj['integrity'].get('baseline_anchor_ok'))
    assert obj['rounds'] == [15, 16, 17, 18, 19], obj['rounds']
    assert obj['integrity']['board_chain_ok'], "board-identity chain broken"
    assert obj['integrity'].get('baseline_anchor_ok'), "scratch bundle does not anchor to its baseline"
    # ASSERT this scratch run did NOT touch production, and that production still carries the
    # OWNER-AUTHORISED R15-R19 history (ITEM 408 Items 6-7, Option A). The scratch is DISPOSABLE evidence
    # on its OWN superseded lineage (baseline board 270a2c5f); production is the recovery's own history
    # (baseline board 2ab73a6f, terminating at the R19 store f37d9716) whose content digest is anchored by
    # the owner-approved provenance transition. The scratch's existence must NEVER be used to erase or
    # overwrite the production history.
    prod = MV.load_bundle(os.path.join(REPO, 'ui', 'data', 'movers.js'), repo_root=REPO)
    assert prod['rounds'] == [15, 16, 17, 18, 19], \
        "production must carry the owner-authorised R15-R19 history (found %s)" % prod['rounds']
    trans_path = os.path.join(REPO, 'ui', 'data', 'movers_transition.js')
    with open(trans_path) as tf:
        ttext = tf.read()
    trans = json.loads(ttext[ttext.index('{'):ttext.rindex('}') + 1])
    prod_digest = MV.canonical_reports_digest(prod, [15, 16, 17, 18, 19])
    assert trans.get('owner_approved') is True, "the provenance transition must be owner-approved"
    assert trans['applies_to']['historical_reports_digest'] == prod_digest, \
        "production movers content digest != owner-approved provenance transition (production may be corrupt)"
    # the scratch (270a2c5f lineage) is a SEPARATE artifact and did not overwrite production history
    assert prod['reports']['19']['board_md5_after'] != obj['reports']['19']['board_md5_after'], \
        "the disposable scratch lineage must stay separate from the production history"
    print("PRODUCTION ui/data/movers.js carries the owner-authorised R15-R19 history; digest %s matches "
          "the owner-approved provenance transition; the disposable scratch stayed separate." % prod_digest)
    print("OK — R15-R19 movers evidence regenerated (scratch); production history preserved + untouched")
    return 0


if __name__ == '__main__':
    sys.exit(main())
