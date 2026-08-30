#!/usr/bin/env python3
"""tools/score_sheet_check.py — does a scores file say something possible?

  python3 tools/score_sheet_check.py <file.csv> [--per-match 23] [--expect-match-total 3300]
                                                [--tolerance 60]

WHAT THIS CATCHES THAT NOTHING ELSE DOES. The applier resolves every name against the store and
stops on one it cannot place, so a misread NAME is already caught. A misread SCORE on a correctly
spelled name is caught by nothing: `Bontempelli,184` for `Bontempelli,134` resolves perfectly,
applies cleanly, and is wrong forever.

SuperCoach distributes a near-fixed pool per match, so the two teams' scores in one match sum to
about the same number every week — the owner's own check, given 2026-08-30: "double check your
transcription and that the sum of all scores from the WBD + Coll match and the Melbourne + Carlton
match add up to close to 3300 combined". That is a CONSERVATION LAW over the sheet, and it is
independent of every name in it. A single transposed digit moves a match total by 9 to 90 — far
outside the tolerance a real match varies by.

It is a check on the sheet as a whole, so it can only run when the file is ordered by match (each
consecutive pair of team blocks being one match), which is how a transcription from match pages
arrives. Pass `--per-match` the squad size (23 in the AFL) and the blocks are taken in order.
"""
import argparse
import csv
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def read(path):
    # DECODED THROUGH THE ESTATE'S OWN PARSER, not through a second convention. The real files are
    # cp1252 with a trailing non-breaking space on names copied from the web (16 of them in R23), and
    # a strict utf-8 read of one dies at byte 43 — which is what the first draft of this function
    # did. `footywire_parser` already detects the encoding and strips those; using it here means the
    # check reads exactly the bytes the applier will.
    sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after', 'ingestion'))
    import footywire_parser as FP
    parsed = FP.parse_round_file(path)
    header = ['Player', 'score']
    out = [(name, float(score)) for name, score in parsed['rows']]
    return header, out


def _unused_read(path):
    with open(path, newline='', encoding='utf-8', errors='strict') as f:
        rows = [r for r in csv.reader(f) if r and r[0].strip()]
    header, body = rows[0], rows[1:]
    out = []
    for r in body:
        try:
            out.append((r[0].strip(), float(r[1])))
        except (IndexError, ValueError):
            raise SystemExit('row %r is not name,score' % (r,))
    return header, out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--squad', type=int, default=23, help='players per team block (AFL: 23)')
    ap.add_argument('--expect-match-total', type=float, default=3300.0)
    # THE TOLERANCE IS TIGHT ON PURPOSE, AND THE FIRST DRAFT'S WAS NOT. At +/-60 a seeded
    # single-digit misread — Bontempelli 134 -> 184, exactly the error this exists to catch — passed
    # the check. A bar that admits the failure it was built for is worse than no bar, because it
    # reads as assurance. The two measured matches came in at 3301 and 3300, so the real quantity is
    # near-conserved and +/-25 leaves ample room for genuine variation while catching any two-digit
    # slip. PROVISIONAL: calibrated on two matches, and worth re-deriving once a season of them
    # exists — widen it on measured evidence, never to make a red go away.
    ap.add_argument('--tolerance', type=float, default=25.0)
    a = ap.parse_args(argv)

    header, rows = read(a.path)
    n = len(rows)
    print('SCORE SHEET — %s' % a.path)
    print('  header %s · %d rows' % (header, n))
    if n % (a.squad * 2):
        print('  FAIL — %d rows is not a whole number of MATCHES at %d per team (%d per match). A '
              'block that lost or gained a row is the transcription error this counts.'
              % (n, a.squad, a.squad * 2))
        return 1

    dupes = {}
    for name, _ in rows:
        dupes[name] = dupes.get(name, 0) + 1
    repeated = sorted(k for k, v in dupes.items() if v > 1)
    if repeated:
        print('  FAIL — the same player appears more than once: %s' % repeated)
        return 1

    bad = 0
    for i in range(0, n, a.squad * 2):
        match = rows[i:i + a.squad * 2]
        t1 = sum(s for _, s in match[:a.squad])
        t2 = sum(s for _, s in match[a.squad:])
        tot = t1 + t2
        off = tot - a.expect_match_total
        okish = abs(off) <= a.tolerance
        if not okish:
            bad += 1
        print('  match %d  %7.0f + %7.0f = %7.0f   vs %.0f  (%+.0f)  %s'
              % (i // (a.squad * 2) + 1, t1, t2, tot, a.expect_match_total, off,
                 'ok' if okish else 'OUT OF TOLERANCE'))
    lo = min(s for _, s in rows)
    hi = max(s for _, s in rows)
    print('  scores %.0f .. %.0f, mean %.1f' % (lo, hi, sum(s for _, s in rows) / n))
    if lo < 0 or hi > 250:
        print('  FAIL — a score outside 0..250 is not a SuperCoach score')
        return 1
    print('  %s' % ('PASS — every match total is within %.0f of %.0f'
                    % (a.tolerance, a.expect_match_total) if not bad
                    else 'FAIL — %d match total(s) out of tolerance' % bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
