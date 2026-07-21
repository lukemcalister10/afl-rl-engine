"""DRY-RUN PROOF (directive step 4) — replay historical rounds through the ingestion plumbing.

READ-ONLY. Sources the "known appends" from the store's OWN scoring arrays (the only round-level
granularity available: per-season {year, avg, games}). For every player with a played entry in the
proof season, it:

  1. reconstructs the season as `games` round-rows (round 1..games, score = the stored avg,
     played=1) — a faithful reconstruction: mean == stored avg, played-count == stored games;
  2. builds a weekly feed from those rows (round_score_parser format);
  3. runs parse -> resolve -> preview (score_ingestor);
  4. ASSERTS the previewed season entry (`batch_entry`) reproduces the store's {year,avg,games}
     BYTE-FOR-BYTE, and that the exceptions list is EMPTY for the sampled players.

HONEST DISCLOSURE: the per-round scores are flat (all == the season avg) because the store holds
no round-level variance to replay. The proof therefore exercises the PLUMBING end-to-end
(parse -> resolve -> aggregate -> preview appends), not real round-to-round variance. The avg
reproduces byte-for-byte because the aggregator rounds to the store's own 2dp precision
(verified: every stored avg == round(avg, 2)).

Run:  python3 dry_run_proof.py [--year 2026] [--write PROOF.md proof.json]
Exit code 0 = PROOF PASS; non-zero = FAIL (a plumbing defect).
"""
import json, os, sys

try:
    from .score_ingestor import ScoreIngestor, DEFAULT_SEASON_YEAR, _md5_of
    from .round_score_parser import parse_feed
except (ImportError, ValueError):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from score_ingestor import ScoreIngestor, DEFAULT_SEASON_YEAR, _md5_of   # type: ignore
    from round_score_parser import parse_feed                                # type: ignore

_STORE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rl_model_data.json')


def _reconstruct_feed(player_name, entry, club=None):
    """Build a weekly JSON feed reproducing one player's season entry as flat played rounds.
    `club` (the row's afl_club — the CURRENT AFL club a real feed carries, item 20d; NOT affl_team,
    the AFFL keeper side) is carried so collision names (two Max Kings, etc.) resolve via the club
    veto — exactly as a real weekly feed disambiguates them. JSON avoids CSV-quoting the club
    string ('Free agents')."""
    a, g = entry['avg'], entry['games']
    rows = [{'player': player_name, 'round': rnd, 'score': a, 'played': 1, 'club': club}
            for rnd in range(1, g + 1)]
    return json.dumps(rows)


def run(season_year=DEFAULT_SEASON_YEAR):
    store = json.load(open(_STORE))
    ing = ScoreIngestor(store=store)

    # candidates: every store row with a PLAYED entry for the proof season AND a stable id
    # (id is required for a clean, exceptions-empty resolve — the score boundary's contract).
    candidates = []
    for r in store:
        if not r.get('stable_player_id'):
            continue
        entry = next((s for s in (r.get('scoring') or [])
                      if s.get('year') == season_year and s.get('games', 0) >= 1), None)
        if entry:
            candidates.append((r, {'year': entry['year'], 'avg': entry['avg'], 'games': entry['games']}))

    results = {'season_year': season_year, 'store_md5': _md5_of(_STORE),
               'sampled': len(candidates), 'passed': 0, 'failed': 0,
               'exceptions_total': 0, 'anomalies_total': 0, 'failures': [], 'worked_example': None}

    for row, entry in candidates:
        feed = _reconstruct_feed(row['player'], entry, club=row.get('afl_club'))
        rows = parse_feed(feed)
        pv = ing.preview(rows, season_year=season_year, merge_with_store=False)

        ok = True
        detail = {'player': row['player'], 'key': row['key'], 'expected': entry}
        if pv.exceptions:
            ok = False
            detail['exceptions'] = [e.as_dict() for e in pv.exceptions]
            results['exceptions_total'] += len(pv.exceptions)
        # locate this player's append (resolve may map name->a canonical key/player)
        ap = next((a for a in pv.appends if a.key == row['key']), None)
        if ap is None:
            ok = False
            detail['error'] = 'no append produced for key'
        else:
            got = ap.batch_entry
            detail['got'] = got
            # byte-for-byte: identical JSON serialization of the season entry
            if json.dumps(got, sort_keys=True) != json.dumps(entry, sort_keys=True):
                ok = False
                detail['error'] = 'batch_entry != store entry'
            results['anomalies_total'] += len(ap.anomalies)
            if ap.anomalies:
                # flat single-appearance rounds must not trip duplicate/impossible/cycle/retired
                ok = False
                detail['anomalies'] = [x.as_dict() for x in ap.anomalies]

        if ok:
            results['passed'] += 1
            if results['worked_example'] is None:
                results['worked_example'] = {
                    'player': row['player'], 'key': row['key'],
                    'stable_player_id': row['stable_player_id'],
                    'feed_rounds': entry['games'], 'store_entry': entry,
                    'preview_batch_entry': ap.batch_entry,
                    'byte_for_byte': True}
        else:
            results['failed'] += 1
            if len(results['failures']) < 25:
                results['failures'].append(detail)

    results['proof_pass'] = (results['failed'] == 0 and results['sampled'] > 0)
    return results


def _md_report(res):
    wx = res.get('worked_example') or {}
    lines = [
        "# DRY-RUN PROOF — round-score ingestion plumbing",
        "",
        "Directive step 4. READ-ONLY replay of the store's own scoring arrays through",
        "parse -> resolve -> preview. Regenerate: `python3 dry_run_proof.py`.",
        "",
        "## RESULT: **%s**" % ("PROOF PASS" if res['proof_pass'] else "PROOF FAIL"),
        "",
        "| field | value |",
        "|---|---|",
        "| proof season | %s |" % res['season_year'],
        "| store md5 | `%s` |" % res['store_md5'],
        "| players sampled | %d |" % res['sampled'],
        "| byte-for-byte reproduced | %d |" % res['passed'],
        "| failed | %d |" % res['failed'],
        "| resolve exceptions (sampled) | %d |" % res['exceptions_total'],
        "| anomalies tripped (sampled) | %d |" % res['anomalies_total'],
        "",
        "## WORKED EXAMPLE",
        "```json",
        json.dumps(wx, indent=2, sort_keys=True),
        "```",
        "",
        "## WHAT THIS PROVES",
        "- Names resolve to the correct `stable_player_id`/store key at the boundary "
        "(exceptions list empty across all %d sampled players)." % res['sampled'],
        "- The aggregator reproduces each known season append **byte-for-byte** "
        "(`{year,avg,games}` identical to the store).",
        "- Flat, single-appearance rounds trip no anomaly (duplicate/impossible/cycle/retired).",
        "",
        "## HONEST SCOPE",
        "- Per-round scores are flat (== the season avg): the store holds no round-level variance "
        "to replay. This exercises the PLUMBING, not round-to-round variance.",
        "- avg reproduces byte-for-byte because the aggregator rounds to the store's own 2dp "
        "(verified: every stored avg == round(avg,2)).",
        "- Retirees carry no stable id in this store, so a named retiree is caught at the "
        "*exception* layer (`no_stable_id`); the `retired` *anomaly* is forward-safe defense.",
    ]
    if res['failures']:
        lines += ["", "## FAILURES (first %d)" % len(res['failures']), "```json",
                  json.dumps(res['failures'], indent=2, sort_keys=True), "```"]
    return '\n'.join(lines) + '\n'


def main(argv):
    year = DEFAULT_SEASON_YEAR
    write = None
    i = 1
    while i < len(argv):
        if argv[i] == '--year':
            year = int(argv[i + 1]); i += 2
        elif argv[i] == '--write':
            write = (argv[i + 1], argv[i + 2]); i += 3
        else:
            i += 1
    res = run(season_year=year)
    print(json.dumps(res['proof_pass'] and {k: res[k] for k in
          ('proof_pass', 'season_year', 'store_md5', 'sampled', 'passed', 'failed',
           'exceptions_total', 'anomalies_total', 'worked_example')} or res, indent=2))
    if write:
        md_path, json_path = write
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, md_path), 'w') as f:
            f.write(_md_report(res))
        with open(os.path.join(here, json_path), 'w') as f:
            json.dump(res, f, indent=2, sort_keys=True)
        print("wrote", md_path, "+", json_path)
    return 0 if res['proof_pass'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
