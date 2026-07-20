"""GENERATE the committed Matchday movers bundle from the R15-R19 catch-up (scratch only, gate OFF).

Runs the controlled five-round catch-up on a DISPOSABLE copy of the accepted Round-14 state (the real
canonical store is NEVER used), which — after each round commits — emits a durable movers report. This
script then COPIES the accumulated UI movers bundle + the per-round JSON/CSV reports OUT of the scratch
into the repo so the Matchday UI's Movers view has real R15-R19 data that survives a restart:

  * ui/data/movers.js                                  (the integrated UI movers bundle, committed)
  * session_2026-07-20/live_scoring_catchup/movers/    (per-round movers_R{N}.json + .csv evidence)

It does NOT touch the real store, board, boot manifest or the board_view UI bundles — only ui/data/
movers.js (a new file) and the evidence dir. Idempotent: re-running regenerates the same bundle.

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
import failure_injection_proof as FI   # noqa: E402  (fixture-coherent scratch + gate helpers)

GEN = "2026-07-20T22:00:00Z"
FILES = [(r, os.path.join(FIX, 'R%d.csv' % r)) for r in (15, 16, 17, 18, 19)]


def main():
    scr = FI.make_scratch('genmovers')
    os.makedirs(os.path.join(scr, 'ui', 'tools'), exist_ok=True)
    os.makedirs(os.path.join(scr, 'ui', 'data'), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, 'ui', 'tools', 'extract_board_view.py'),
                    os.path.join(scr, 'ui', 'tools', 'extract_board_view.py'))
    FI.arm()
    try:
        cu = RC.RoundCatchup(scr, FILES)
        pre, _rounds = cu.preflight()
        assert pre['clean'], pre['halt_reasons']
        run = cu.run(approved=True, generated_at=GEN)
        for r in run['rounds']:
            print("R%d %s players=%s played=%s dnp=%s board=%s->%s movers=%s" % (
                r['round'], r['status'], r.get('players_applied'), r.get('movers_played'),
                r.get('movers_dnp'), (r.get('board_before') or '')[:8], (r.get('board_after') or '')[:8],
                os.path.basename(r.get('movers_report') or '')))
        # copy the accumulated UI movers bundle -> repo (committed)
        src_bundle = os.path.join(scr, 'ui', 'data', 'movers.js')
        dst_bundle = os.path.join(REPO, 'ui', 'data', 'movers.js')
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
    # verify the committed bundle
    with open(dst_bundle) as f:
        text = f.read()
    obj = json.loads(text[text.index('{'):text.rindex('}') + 1])
    print("committed bundle rounds:", obj['rounds'], "chain_ok:", obj['integrity']['board_chain_ok'])
    assert obj['rounds'] == [15, 16, 17, 18, 19], obj['rounds']
    assert obj['integrity']['board_chain_ok'], "board-identity chain broken"
    print("OK — committed movers bundle for R15-R19")
    return 0


if __name__ == '__main__':
    sys.exit(main())
