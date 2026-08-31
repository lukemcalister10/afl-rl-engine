#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ui/tools/gen_draft_outcomes.py — THE DRAFT-DAY OUTCOME SIDECAR (owner UI item 13).

Writes ui/data_aux/draft_outcomes.js: one row per NATIONAL-DRAFT selection the store carries, with
the few career facts a draft-day question actually turns on. READ-ONLY over the store; it loads no
engine, prices nothing, and ranks nothing.

WHY THIS CAN BE HONEST, WHICH IS NOT THE USUAL CASE
---------------------------------------------------
A "what does pick 12 become" tool is normally worthless because the underlying list is a list of
players who MADE IT. Base rates computed on survivors say every pick is a good pick. This store is
not that list. MEASURED HERE, and re-measured on every run into the stamp:

  · 1570 national-draft selections, draft classes 2003-2025, EVERY class complete from pick 1;
  · exactly 23 observations at every ordinal 1-58 (one per class), tapering only where the real
    drafts were shorter;
  · 226 of them (14.4%) NEVER PLAYED A SENIOR GAME.

Busts are in the population. That is the whole basis on which this tool is allowed to exist, so the
never-played count is recomputed every run and carried in the stamp where it cannot be lost.

THE MATURITY RULE IS DERIVED, NOT CHOSEN
----------------------------------------
A 2025 draftee who has not played is not a bust; he is nineteen. Counting him as one would poison
every recent class — the 2025 class currently reads 44.8% "never played" against a mature-class norm
near 12%. So classes are split into MATURE and STILL RUNNING, and the boundary is measured rather
than picked: among classes with time to settle, this tool computes how long eventual debutants
actually took. On today's store that reads

    +1 season 61.3%   +2 87.5%   +3 96.5%   +4 99.0%   (n=1046 eventual debutants, classes 2003-2019)

so four completed seasons captures 99% of debuts, and a class is called mature once it has had that
many. The threshold is emitted as `maturitySeasons` with the table it came from, so a reader can
check the rule against its own evidence and a future store moves the rule instead of contradicting a
constant nobody re-derived.

NO BARS, NO GRADES, NO VERDICTS
-------------------------------
This file records what happened: games played, when he debuted, his best season and when. It does
NOT decide what a "hit" is. A hit rate needs a threshold, a threshold is a ruling, and no such
ruling exists — so the surface reports distributions and lets the reader put his own line through
them. The one number that IS survivorship-shaped (what these players are worth on today's board) is
left to the reader to join against the live board, where the count of how many survive to be joined
is visible beside it.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')
OUT = os.path.join(REPO, 'ui', 'data_aux', 'draft_outcomes.js')

#: The store fields a draft outcome derives from. Same discipline as ui/tools/v0_identity.py: the
#: signature covers exactly these, so the bundle can be gated on its INPUTS rather than on a board
#: md5 that moves for unrelated reasons. Unlike v0, `games` and `scoring` DO move on a round advance
#: — a draft outcome is a career fact and a career grows — so this bundle legitimately regenerates
#: with the football, and the signature says so instead of pretending otherwise.
#: `games` stays in this list even though _career_games() no longer reads it. The signature is a
#: statement about which store fields could change this bundle, and a store edit that moved the
#: scalar without moving the seasons would be a real inconsistency worth regenerating for — the
#: exact inconsistency measured above. Removing it would make the gate blind to that case.
OUTCOME_INPUT_FIELDS = ('draft_stream', 'stream_pick', 'stream_year', 'games', 'scoring',
                        'player', 'drafted_position', 'future_position', '_draft_club', '_retired')
SIG_VERSION = 'draft-outcomes-inputs-1'

#: A season counts as a real season for the "best season" figure at this many games or more. Below
#: it, an average is one or two matches of noise and would put a 130 cameo on the board as a career
#: peak. 10 is the same bar the engine's own thin-evidence discussions use for a season to be worth
#: reading; it is declared here, not buried, because it is the one judgement in the file.
REAL_SEASON_GAMES = 10

#: NO REPLACEMENT LEVEL, NO STAR BAR, AND NO POSITION CONSTANT IS DEFINED IN THIS FILE.
#:
#: An earlier cut of this generator derived both — a replacement level off the owner's best-23 slot
#: law, and a "star" bar off the 40th-best season in the league. Both were defensible constructions
#: and both were WRONG TO EXIST. The model has carried `REPL` (the replacement bar per position) and
#: `PEAK` (the peak level per position) for months: rl_model.py:824, v3.3, derived by
#: rl_replacement_derive.py with the owner's own 2026-07-04 dial on KPF. They are baked, they are
#: what every other surface measures against, and the derived stand-ins disagreed with them badly
#: — SF read 57.7 against the baked 70.9, which was enough to invert the small-forward reading.
#:
#: They now reach the app the way they should have all along: passed through from the board by
#: ui/tools/extract_board_view.py into the bundle's `REPL` / `PEAK`, and read there. This file emits
#: CAREER FACTS ONLY — games, debut lag, best season — and takes no view on what any of them is
#: worth. The measuring is done where the bars live.


def outcome_inputs_sig(store_rows):
    """A digest over every national-draft row's outcome-determining inputs, sorted by key."""
    parts = []
    for row in store_rows:
        key = row.get('key')
        if not key or row.get('draft_stream') != 'ND':
            continue
        parts.append(key + '\x1f' + json.dumps(
            [row.get(f) for f in OUTCOME_INPUT_FIELDS], sort_keys=True, separators=(',', ':')))
    parts.sort()
    h = hashlib.sha256()
    h.update((SIG_VERSION + '\x1e').encode('utf-8'))
    for p in parts:
        h.update(p.encode('utf-8'))
        h.update(b'\x1e')
    return h.hexdigest()


def _seasons(row):
    return [s for s in (row.get('scoring') or []) if isinstance(s, dict)]


def _career_games(row):
    """Career games SUMMED FROM THE SEASON ROWS, deliberately not the top-level `games` field.

    MEASURED ON THIS STORE, and the reason this function exists rather than a `row['games']`:

        players with NO 2026 season   981 of 981 have games == the sum of their seasons
        players WITH a 2026 season    196 of 589 do

    The top-level field is a snapshot that stops being maintained once a player has a live season:
    Willem Duursma reads 17 there and 21 across his own season rows; Sam Walsh 152 against 157. The
    season rows are the record the weekly ingest actually writes — the Finals Week 1 edit moved them
    and left `games` where it was — so they are the truth and the scalar is the copy.

    This was found by a test rather than by reading: six rows carried games == 0 while their season
    rows recorded football in 2026, which made "never played" false for six men who had played. The
    assertion that caught it (`a debut lag exists exactly when the player played`) is kept, because
    it is the relationship that fails the moment these two ever disagree again.
    """
    return sum(int(s.get('games') or 0) for s in _seasons(row))


def _debut_year(row):
    played = [s['year'] for s in _seasons(row) if (s.get('games') or 0) > 0 and s.get('year')]
    return min(played) if played else None


def _last_year(row):
    played = [s['year'] for s in _seasons(row) if (s.get('games') or 0) > 0 and s.get('year')]
    return max(played) if played else None


def _peak(row):
    """Best average over a season of REAL_SEASON_GAMES or more, with the year it happened."""
    best = None
    for s in _seasons(row):
        if (s.get('games') or 0) >= REAL_SEASON_GAMES and s.get('avg') is not None:
            if best is None or s['avg'] > best[0]:
                best = (float(s['avg']), s.get('year'))
    return best


def _real_seasons(row):
    """EVERY REAL SEASON AS (average, POSITION PLAYED), which is what the owner's rule needs.

    HIS RULING, 2026-08-31, and it is not the obvious one:

        "A player drafted as a mid who then switched to SF mid career and scored 95 over a 67 bar
         is +28, and that's credited to the midfield role he was drafted to. A player drafted as a
         KPF who switched to a mid mid career and scores 75 that season over a 77 bar doesn't
         contribute much even though the KPF bar is lower than his average."

    So the BAR is the bar for the position he was PLAYING that season, and the CREDIT goes to the
    position he was DRAFTED as. Two different axes doing two different jobs, and the reason it is
    right: what you buy on draft day is the midfield selection, so the midfield row owns the result
    — but what the result IS depends on the job he actually did, and a mid playing forward is
    measured as a forward.

    The naive version (measure everyone against his drafted position's bar for life) would have
    credited that KPF-turned-mid with clearing a 63.8 bar by eleven points while the owner's rule
    correctly scores him BELOW his 77.1 one. 272 of 1377 settled selections — one in five — change
    position, so this is not an edge case.

    Emitted as (avg, position) pairs because the bars live on the BOARD, not here: this file still
    holds no bar and takes no view on what any season was worth. Positions are emitted verbatim,
    duals included ("SF/MID", "KPF/RUCK"), for the reader to resolve with the engine's own rule.
    """
    out = []
    for s in _seasons(row):
        if (s.get('games') or 0) >= REAL_SEASON_GAMES and s.get('avg') is not None and s.get('pos'):
            out.append([round(float(s['avg']), 2), str(s['pos'])])
    return out


def build(store_rows):
    nd = [r for r in store_rows
          if r.get('draft_stream') == 'ND' and r.get('stream_pick') and r.get('stream_year')]
    nd.sort(key=lambda r: (r['stream_year'], r['stream_pick']))

    season_now = max((s.get('year') or 0) for r in store_rows for s in _seasons(r))

    rows = []
    for r in nd:
        peak = _peak(r)
        debut = _debut_year(r)
        rows.append({
            'k': r.get('key'),
            'n': r.get('player'),
            'p': int(r['stream_pick']),
            'y': int(r['stream_year']),
            'c': r.get('_draft_club'),
            'dp': r.get('drafted_position'),
            'fp': r.get('future_position'),
            'g': _career_games(r),
            # debut LAG in seasons after the draft, which is the comparable form: an absolute year
            # would make every cross-class comparison arithmetic the reader has to do himself.
            'dl': (debut - int(r['stream_year'])) if debut else None,
            'ly': _last_year(r),
            'pk': round(peak[0], 1) if peak else None,
            'py': peak[1] if peak else None,
            # every real season as (average, position PLAYED) — the owner's bar rule needs both
            's': _real_seasons(r),
            'ret': bool(r.get('_retired')),
        })

    # ---- the maturity rule, measured off the classes old enough to have settled ----------------
    # A class is used to MEASURE the rule only if it has had a long run (>= 7 completed seasons),
    # so the measurement itself is not contaminated by the very immaturity it exists to detect.
    lag_counts = {}
    n_debut = 0
    for row in rows:
        if season_now - row['y'] < 7 or row['dl'] is None:
            continue
        lag_counts[row['dl']] = lag_counts.get(row['dl'], 0) + 1
        n_debut += 1
    cum, maturity, table = 0, None, []
    for lag in sorted(lag_counts):
        cum += lag_counts[lag]
        share = cum / n_debut if n_debut else 0.0
        table.append({'lag': lag, 'n': lag_counts[lag], 'cum': round(share, 4)})
        if maturity is None and share >= 0.99:
            maturity = lag
    if maturity is None:                       # pathological store: refuse to invent a threshold
        maturity = max(lag_counts) if lag_counts else 0

    per_class = {}
    for row in rows:
        c = per_class.setdefault(row['y'], {'n': 0, 'never': 0})
        c['n'] += 1
        if row['g'] == 0:
            c['never'] += 1

    stamp = {
        'generator': 'ui/tools/gen_draft_outcomes.py',
        'store': hashlib.md5(open(STORE, 'rb').read()).hexdigest(),
        'outcomeInputsSig': outcome_inputs_sig(store_rows),
        'outcomeInputsSigVersion': SIG_VERSION,
        'seasonNow': season_now,
        'nRows': len(rows),
        'nClasses': len(per_class),
        'classFrom': min(per_class) if per_class else None,
        'classTo': max(per_class) if per_class else None,
        # THE PROOF THE POPULATION IS NOT SURVIVOR-FILTERED, recomputed every run.
        'nNeverPlayed': sum(1 for r in rows if r['g'] == 0),
        'realSeasonGames': REAL_SEASON_GAMES,
        'maturitySeasons': maturity,
        # No value frame here — REPL and PEAK ride the board bundle. See the note at the top.
        'debutLagTable': table,
        'debutLagN': n_debut,
        'perClass': {str(k): v for k, v in sorted(per_class.items())},
    }
    return {'rows': rows, 'stamp': stamp}


HEADER = """/* GENERATED — DO NOT HAND-EDIT. ui/tools/gen_draft_outcomes.py
   THE DRAFT-DAY OUTCOME RECORD: every national-draft selection the store carries, 2003 onward, with
   the career facts a draft-day question turns on — games, debut lag, best real season, retirement.
   It carries NO verdicts: no hit rate, no bust flag, no grade. A threshold is a ruling and none has
   been made, so the surface reports distributions and the reader draws his own line.
   The stamp re-proves, every run, that busts are IN the population (nNeverPlayed) and carries the
   MEASURED maturity rule (maturitySeasons + the debut-lag table it came from), so a recent class is
   never counted as a failure for being young.
   Regenerate with:  python3 ui/tools/gen_draft_outcomes.py  */
"""


def main():
    with open(STORE, encoding='utf-8') as fh:
        store_rows = json.load(fh)
    payload = build(store_rows)
    body = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(HEADER)
        fh.write('window.__DRAFT_OUTCOMES__ = ' + body + ';\n')
    s = payload['stamp']
    print('wrote %s' % os.path.relpath(OUT, REPO))
    print('  rows            %d national-draft selections' % s['nRows'])
    print('  classes         %d  (%s-%s)' % (s['nClasses'], s['classFrom'], s['classTo']))
    print('  never played    %d  (%.1f%%) — the population is not survivor-filtered'
          % (s['nNeverPlayed'], 100.0 * s['nNeverPlayed'] / max(1, s['nRows'])))
    print('  maturity rule   %d completed seasons (measured: %d%% of %d eventual debutants)'
          % (s['maturitySeasons'],
             round(100 * [t['cum'] for t in s['debutLagTable'] if t['lag'] == s['maturitySeasons']][0]),
             s['debutLagN']))
    print('  store           %s' % s['store'][:8])
    return 0


if __name__ == '__main__':
    sys.exit(main())
