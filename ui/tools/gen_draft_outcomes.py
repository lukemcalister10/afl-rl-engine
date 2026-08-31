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

#: THE LEAGUE'S OWN STARTING SLOTS, verbatim from ui/app/club_totals.js:37 — the owner's ruled
#: best-23 shape (18 starters + 5 bench). They are what makes a REPLACEMENT LEVEL derivable rather
#: than invented: with 16 clubs, the league starts 5x16 = 80 midfielders and 1x16 = 16 rucks, so the
#: 80th-best midfielder and the 16th-best ruck are, by definition, the last men holding a starting
#: slot at their position. That is replacement level, and it is the anchor every "value over
#: replacement" figure on the Draft day board is measured from.
STARTING_SLOTS = {'KPD': 2, 'SD': 4, 'MID': 5, 'SF': 4, 'KPF': 2, 'RUCK': 1}

#: The club count is COUNTED from the store, not written here — see _club_count().

#: A season needs this many games before it counts toward a replacement level. Lower than
#: REAL_SEASON_GAMES because a replacement level is about who is AVAILABLE to fill a slot, and a
#: part-season fill-in is exactly that; 5 keeps a two-game cameo out without demanding a full year.
REPL_SEASON_GAMES = 5

#: "A difference-maker" is defined once, league-wide, as a season inside the top N by average. 40 is
#: about two and a half per club — the players who decide a season rather than fill a side. It is
#: deliberately POSITION-BLIND: a star is a star, and defining it per position would hand every
#: position the same star rate by construction and delete the very finding the board exists to show.
STAR_RANK = 40


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


def _club_count(store_rows):
    """The league's club count, COUNTED rather than written as 16.

    The Free-Agents pool is not a club and never enters a league denominator (item 191); it is
    matched case-insensitively because the store carries both spellings ("Free Agents" and "Free
    agents"), exactly as ui/app/club_totals.js:isFree folds them. A league that grows moves every
    replacement level with it, with no edit here.
    """
    teams = set()
    for row in store_rows:
        if not row.get('stable_player_id'):
            continue
        t = (row.get('affl_team') or '').strip()
        if t and t.lower() != 'free agents':
            teams.add(t)
    return len(teams)


def _repl_levels(store_rows, season_now, clubs):
    """REPLACEMENT LEVEL PER POSITION, derived from the league's own ruled slots.

    A "value over replacement" figure is only as honest as its replacement level, and the usual sin
    is to pick one. This does not: the owner's best-23 law starts 5 midfielders, 4 general defenders,
    4 general forwards, 2 key defenders, 2 key forwards and 1 ruck per club, and the league has 16
    clubs. So it starts 80 midfielders and 16 rucks, and the 80th-best midfielder is — by the
    league's own definition — the last man holding a midfield slot. That is replacement.

    Measured on the CURRENT season across the tracked roster, keyed on `future_position` (the single
    axis a player is modelled and slotted on), with a five-game qualifier so a two-match fill-in does
    not set the level.

    IT MOVES WITH THE LEAGUE, ON PURPOSE. A season where midfield scoring inflates raises the bar a
    draftee must clear to be worth anything, which is correct: value over replacement is a claim
    about THIS league, not an absolute. It is recomputed every run and published in the stamp with
    the pool size behind it, so a level resting on too few players is visible rather than silent.
    """
    out = {}
    for pos, slots in sorted(STARTING_SLOTS.items()):
        avgs = []
        for row in store_rows:
            if not row.get('stable_player_id') or row.get('future_position') != pos:
                continue
            for s in _seasons(row):
                if s.get('year') == season_now and (s.get('games') or 0) >= REPL_SEASON_GAMES \
                        and s.get('avg') is not None:
                    avgs.append(float(s['avg']))
        avgs.sort(reverse=True)
        need = slots * clubs
        # Too few players to reach the slot count is a REAL state, not an error: the level is the
        # weakest man available and the shortfall is published so the figure is read with it.
        level = avgs[need - 1] if len(avgs) >= need else (avgs[-1] if avgs else None)
        out[pos] = {'repl': round(level, 2) if level is not None else None,
                    'slots': slots, 'slotsLeague': need, 'pool': len(avgs),
                    'short': max(0, need - len(avgs))}
    return out


def _star_bar(store_rows, season_now):
    """"A difference-maker", defined ONCE and league-wide rather than per position.

    A star is a star: the bar is the STAR_RANK-th best season average in the league this year, about
    two and a half per club. Defining it per position would hand every position the same star rate by
    construction and delete the finding the whole board exists to show — that the positions convert
    to genuine difference-makers at wildly different rates.
    """
    avgs = []
    for row in store_rows:
        if not row.get('stable_player_id'):
            continue
        for s in _seasons(row):
            if s.get('year') == season_now and (s.get('games') or 0) >= REPL_SEASON_GAMES \
                    and s.get('avg') is not None:
                avgs.append(float(s['avg']))
    avgs.sort(reverse=True)
    if not avgs:
        return None, 0
    return round(avgs[min(STAR_RANK, len(avgs)) - 1], 2), len(avgs)


def build(store_rows):
    nd = [r for r in store_rows
          if r.get('draft_stream') == 'ND' and r.get('stream_pick') and r.get('stream_year')]
    nd.sort(key=lambda r: (r['stream_year'], r['stream_pick']))

    season_now = max((s.get('year') or 0) for r in store_rows for s in _seasons(r))
    clubs = _club_count(store_rows)
    repl = _repl_levels(store_rows, season_now, clubs)
    star_bar, star_pool = _star_bar(store_rows, season_now)

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
        # ---- THE VALUE FRAME: replacement per position, and one league-wide star bar -------------
        # Both are DERIVED (the owner's own ruled starting slots x the counted club count, measured
        # on the current season) and both are published with the pool behind them, so a level
        # standing on too few players is visible instead of silent.
        'clubs': clubs,
        'startingSlots': STARTING_SLOTS,
        'replSeasonGames': REPL_SEASON_GAMES,
        'repl': repl,
        'starBar': star_bar,
        'starRank': STAR_RANK,
        'starPool': star_pool,
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
    print('  clubs           %d (free-agent pool excluded)' % s['clubs'])
    print('  replacement     %s' % ('  '.join(
        '%s %.1f' % (k, v['repl']) for k, v in sorted(s['repl'].items()) if v['repl'] is not None)))
    print('  star bar        %.1f  (the #%d season average in the league, off %d qualifying seasons)'
          % (s['starBar'], s['starRank'], s['starPool']))
    print('  store           %s' % s['store'][:8])
    return 0


if __name__ == '__main__':
    sys.exit(main())
