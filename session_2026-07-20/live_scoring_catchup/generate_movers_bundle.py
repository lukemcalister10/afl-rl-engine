"""GENERATE the R15-R19 movers EVIDENCE from the catch-up (scratch only, gate OFF).

Runs the controlled five-round catch-up on a DISPOSABLE copy of the accepted Round-14 state (the real
canonical store is NEVER used), which — after each round commits + finalizes — produces a durable
movers report. This script copies the RESULTING artifacts into the SESSION EVIDENCE paths ONLY:

  * session_2026-07-20/live_scoring_catchup/movers_bundle_scratch.js   (the accumulated UI bundle)
  * session_2026-07-20/live_scoring_catchup/movers/                    (per-round movers_R{N}.json + .csv)

IMPORTANT (corrective 2026-07-20, review directive A): this NO LONGER writes the production
ui/data/movers.js. The production bundle SHIPS EMPTY (schema + release-baseline block only) until a
real round is applied and finalized by the owner — a fresh Round-14 checkout must show the Movers view
as unavailable / "no finalized round reports". These R15-R19 results are disposable scratch proof
evidence (they begin from the superseded board 270a2c5f), NOT production state. This script also ASSERTS
that the committed production bundle is still the empty initial bundle, so it can never re-introduce
scratch data into production.

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
    # ASSERT the production bundle is still the EMPTY initial bundle (never scratch data)
    prod = MV.load_bundle(os.path.join(REPO, 'ui', 'data', 'movers.js'), repo_root=REPO)
    assert prod['rounds'] == [], "production ui/data/movers.js must ship EMPTY (found %s)" % prod['rounds']
    assert not prod.get('reports'), "production bundle must carry no reports"
    print("PRODUCTION ui/data/movers.js is EMPTY (rounds=[]) — scratch evidence written to session paths only")
    print("OK — R15-R19 movers evidence regenerated (scratch); production bundle untouched + empty")
    return 0


if __name__ == '__main__':
    sys.exit(main())
