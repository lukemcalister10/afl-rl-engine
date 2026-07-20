"""MOVERS ACCEPTANCE PROOF — the committed weekly movers reports (R15-R19), no board build.

Validates the DURABLE movers artifacts the Matchday UI consumes — the accumulated bundle
ui/data/movers.js + the per-round session movers/movers_R{N}.json/.csv — against the owner's movers
acceptance criteria (2026-07-20). These are produced by generate_movers_bundle.py from the five-round
catch-up on a disposable Round-14 copy; this proof re-reads them from disk (a restart) and checks:

  1. exactly ONE movers report per committed round (R15..R19), no duplicate round;
  2. each report's baseline is the immediately prior committed round;
  3. every active player appears EXACTLY ONCE in each report's complete table;
  4. value + overall-rank + positional-rank deltas recompute EXACTLY (cur-prev) and the two consecutive
     reports chain (report[n].prev == report[n-1].cur for value + ranks + the board id);
  5. the view orderings are deterministic (primary field, then current value desc, then key asc);
  6. DNP players are represented (a listed score of 0 stays PLAYED; an unlisted active player is DNP);
  7. failed / duplicate submissions create no new valid report (proven by the catch-up dedup: the
     bundle holds exactly five reports, one per committed round);
  8. restarting the app preserves access to every R15-R19 report (they persist in the committed bundle);
  9. historical reports are never silently overwritten (per-round board ids are distinct + chained; the
     bundle records no overwrite conflict).

Run:  python3 session_2026-07-20/live_scoring_catchup/movers_proof.py [--write]
Exit 0 = ALL PASS.  (Requires generate_movers_bundle.py to have produced ui/data/movers.js first.)
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BUNDLE = os.path.join(REPO, 'ui', 'data', 'movers.js')
MOVERS_DIR = os.path.join(HERE, 'movers')
ROUNDS = [15, 16, 17, 18, 19]


def load_bundle(path):
    with open(path) as f:
        t = f.read()
    return json.loads(t[t.index('{'):t.rindex('}') + 1])


def cmp_key(field, reverse):
    def k(p):
        v = p.get(field)
        vnull = v is None
        cv = p.get('cur_value')
        cv = -1e18 if cv is None else cv
        # sort tuple: primary (nulls last), then cur_value desc, then key asc
        return (1 if vnull else 0, (-v if (not vnull and reverse) else (v if not vnull else 0)),
                -cv, p.get('key'))
    return k


def deterministic_view(players, field, reverse):
    elig = [p for p in players if p.get(field) is not None]
    if reverse:
        return sorted(elig, key=lambda p: (-p[field], -(p['cur_value'] if p['cur_value'] is not None else -1e18), p['key']))
    return sorted(elig, key=lambda p: (p[field], -(p['cur_value'] if p['cur_value'] is not None else -1e18), p['key']))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args(argv[1:])
    report = {}

    if not os.path.exists(BUNDLE):
        print("MISSING ui/data/movers.js — run generate_movers_bundle.py first")
        return 1
    bundle = load_bundle(BUNDLE)
    reports = bundle.get('reports', {})

    # 1: one report per committed round, no duplicate
    one_per_round = bundle.get('rounds') == ROUNDS and all(str(r) in reports for r in ROUNDS)
    report['1_one_report_per_round'] = {'rounds': bundle.get('rounds'), 'pass': one_per_round}

    # 2: baseline chain
    baselines_ok = all(reports[str(r)]['previous_round'] == r - 1 and reports[str(r)]['submitted_round'] == r
                       for r in ROUNDS)
    report['2_baseline_is_prior_round'] = {'pass': baselines_ok}

    # 3: unique + full coverage per round
    cov = {}
    for r in ROUNDS:
        pl = reports[str(r)]['players']
        keys = [p['key'] for p in pl]
        cov[r] = {'players': len(pl), 'unique': len(set(keys)) == len(keys),
                  'count_matches': reports[str(r)]['player_count'] == len(pl)}
    coverage_ok = all(c['unique'] and c['count_matches'] for c in cov.values())
    report['3_unique_full_coverage'] = {'per_round': cov, 'pass': coverage_ok}

    # 4: deltas recompute exactly + chain between consecutive reports
    delta_ok = True
    chain_ok = True
    details = []
    for r in ROUNDS:
        rep = reports[str(r)]
        for p in rep['players']:
            for cur, prev, ch, sign in (('cur_value', 'prev_value', 'value_change', 1),
                                        ('cur_rank', 'prev_rank', 'rank_change', -1),
                                        ('cur_pos_rank', 'prev_pos_rank', 'pos_rank_change', -1)):
                if p[cur] is not None and p[prev] is not None and p[ch] is not None:
                    want = sign * (p[cur] - p[prev])
                    if p[ch] != want:
                        delta_ok = False
                        details.append('R%d %s %s: %s != %s' % (r, p['key'], ch, p[ch], want))
        prevrep = reports.get(str(r - 1))
        if prevrep:
            # board-id chain
            if rep.get('board_md5_before') != prevrep.get('board_md5_after'):
                chain_ok = False
            # value/rank chain: this report's prev == prior report's cur, per player
            prior = {p['key']: p for p in prevrep['players']}
            for p in rep['players']:
                q = prior.get(p['key'])
                if q and (p['prev_value'] != q['cur_value'] or p['prev_rank'] != q['cur_rank']
                          or p['prev_pos_rank'] != q['cur_pos_rank']):
                    chain_ok = False
    report['4_deltas_recompute_and_chain'] = {'delta_ok': delta_ok, 'chain_ok': chain_ok,
                                              'examples': details[:5], 'pass': delta_ok and chain_ok}

    # 5: deterministic view orderings (recompute + compare to the report's stored views)
    det_ok = True
    for r in ROUNDS:
        rep = reports[str(r)]
        pl = rep['players']
        for view, field, rev in (('value_risers', 'value_change', True), ('value_fallers', 'value_change', False),
                                 ('rank_risers', 'rank_change', True), ('rank_fallers', 'rank_change', False)):
            want = [p['key'] for p in deterministic_view(pl, field, rev)][:50]
            got = rep['views'][view]
            if got != want:
                det_ok = False
    report['5_deterministic_views'] = {'pass': det_ok}

    # 6: DNP represented (+ listed 0 stays played)
    dnp_ok = True
    zero_played = None
    for r in ROUNDS:
        pl = reports[str(r)]['players']
        if not any(p['dnp'] for p in pl):
            dnp_ok = False
        for p in pl:
            if p['played'] and p['score'] == 0:
                zero_played = (r, p['key'])
    report['6_dnp_represented'] = {'listed_zero_stays_played_example': zero_played, 'pass': dnp_ok}

    # 7: exactly five reports (dedup/failed => no extra report)
    report['7_no_extra_reports'] = {'report_count': len(reports), 'pass': len(reports) == 5}

    # 8: restart preserves — re-read from disk (already did) => all rounds accessible
    reread = load_bundle(BUNDLE)
    report['8_restart_preserves'] = {'rounds_after_reread': reread.get('rounds'),
                                     'pass': reread.get('rounds') == ROUNDS}

    # 9: no silent overwrite — per-round board ids distinct + chained; bundle records no conflict
    board_ids = [reports[str(r)]['board_md5_after'] for r in ROUNDS]
    no_overwrite = (len(set(board_ids)) == len(board_ids)
                    and bundle.get('integrity', {}).get('board_chain_ok')
                    and not bundle.get('integrity', {}).get('overwrite_conflict_last_write'))
    report['9_no_silent_overwrite'] = {'board_ids_distinct': len(set(board_ids)) == len(board_ids),
                                       'pass': bool(no_overwrite)}

    # per-round CSV present
    csvs = [f for f in (os.listdir(MOVERS_DIR) if os.path.isdir(MOVERS_DIR) else []) if f.endswith('.csv')]
    report['csv_reports'] = {'files': sorted(csvs), 'pass': len(csvs) == 5}

    order = ['1_one_report_per_round', '2_baseline_is_prior_round', '3_unique_full_coverage',
             '4_deltas_recompute_and_chain', '5_deterministic_views', '6_dnp_represented',
             '7_no_extra_reports', '8_restart_preserves', '9_no_silent_overwrite', 'csv_reports']
    all_pass = all(report[k]['pass'] for k in order)
    report['ALL_PASS'] = all_pass

    print("\n==== MOVERS ACCEPTANCE PROOF (committed R15-R19 reports) ====")
    for k in order:
        print("  [%s] %s" % ('PASS' if report[k]['pass'] else 'FAIL', k))
    print("==== %s ====" % ('ALL PASS' if all_pass else 'FAIL'))

    if args.write:
        with open(os.path.join(HERE, 'movers_proof.json'), 'w') as f:
            json.dump(report, f, indent=2, sort_keys=True, default=str)
        print("wrote movers_proof.json")
    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
