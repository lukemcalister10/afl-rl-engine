#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""THE ENGINE'S OWN BAR, APPLIED TO DRAFT HISTORY.

WHY THIS EXISTS, AND WHAT IT REPLACES
-------------------------------------
The first Draft day board derived its own replacement level — one number per position, off the
owner's ruled starting slots. It was defensible and it was unnecessary: the estate already carries
LOCKED, DERIVED BARS, and the owner said so.

    engine/rl_after/rl_passmark.json   pm_pos["<band>|<POS>"] -> a TEN-SEASON expected trajectory
                                       for a player of that position drafted in that pick band.

That is a far better instrument than a flat replacement level, because it is conditional on all
three things that matter: position, pedigree (the pick band) and TENURE. A first-year pick-2
midfielder is measured against 68; the same man in year five against 92.

THE MEASURE IS THE ENGINE'S OWN, NOT A NEW ONE. `rl_model.track_delta(g, pk, sr)` is how the engine
decides whether a player is tracking above or below his own bar, and it is reproduced here exactly:

  * the bar is `expected_c(g, pk, s)` — the pass mark INTERPOLATED on the pick via bandcoord, not
    snapped to a band, so pick 12 and pick 13 do not step;
  * seasons are debut-relative and need >= 4 games (rl_model.srel);
  * seasons 1-8 only, and calendar recency is 1.0 — both are what STBL=True gives on the live board
    (rl_model.py:1307), which is the mode the shipped board is priced in;
  * the weight is RWE[s] * min(games, 22) — season weight times exposure.

Reproduced from the committed JSON artifacts alone, with NO engine load: every input is a table
lookup, so this runs in a second and can be re-run on any future store.

WHAT IT IS NOT
--------------
It is not a claim that the bars are wrong. A mean delta near zero is the bars being well calibrated,
which is what the ALL-BANDS line shows for four of six positions. The signal is the DISPERSION
BETWEEN positions: where a position systematically clears the bar the model sets for it, the model
is conservative about that position, and on draft day — where the pick costs the same whoever you
take — that is an edge.

ONE THING DELIBERATELY NOT REPORTED. An earlier cut of this compared BUST_BAND against the realised
"never played" rate and found the priced rate far higher at every band. That comparison is FALSE:
BUST_BAND is a washout probability already priced into the pedigree curve (rl_model.py:1058-1060),
not a never-debuted rate, and the two are not the same quantity. It was measured, recognised as a
category error, and dropped rather than published.

Run:  python3 docs/evidence/draft_bars_2026-08-31/track_delta_draft_history.py
"""
import collections
import json
import os
import statistics as st
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENG = os.path.join(REPO, 'engine', 'rl_after')

PM = json.load(open(os.path.join(ENG, 'rl_passmark.json'), encoding='utf-8'))
BANDS, ANCH = PM['bands'], PM['BAND_ANCHOR']
pm_pos, pm_band, NB = PM['pm_pos'], PM['pm_band'], len(PM['bands'])
DEF_CURVE = [56, 62, 67, 71, 74, 77, 79, 80, 80, 79]   # rl_model.py:265
RWE = {1: 1.0, 2: 1.3, 3: 1.6, 4: 1.7, 5: 1.7}         # rl_model.py:1039
MATURE_SEASONS = 4
POS = ['MID', 'RUCK', 'SF', 'KPF', 'SD', 'KPD']


def expected(g, band, s):                               # rl_model.expected
    s = max(1, min(10, int(s)))
    c = pm_pos.get('%d|%s' % (band, g)) or pm_band.get(str(band)) or DEF_CURVE
    v = c[s - 1]
    if v is None:
        vv = [x for x in c if x is not None]
        v = vv[min(s - 1, len(vv) - 1)] if vv else DEF_CURVE[s - 1]
    return v


def bandcoord(pk):                                      # rl_model.bandcoord
    if pk <= ANCH[0]:
        return 0.0
    if pk >= ANCH[-1]:
        return float(NB - 1)
    for i in range(NB - 1):
        if ANCH[i] <= pk <= ANCH[i + 1]:
            return i + (pk - ANCH[i]) / (ANCH[i + 1] - ANCH[i])
    return float(NB - 1)


def expected_c(g, pk, s):                               # rl_model.expected_c
    fb = bandcoord(pk)
    lo = int(fb)
    hi = min(NB - 1, lo + 1)
    f = fb - lo
    return (1 - f) * expected(g, lo, s) + f * expected(g, hi, s)


def bandof(pk):
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= pk <= hi:
            return i
    return NB - 1


def srel(row):                                          # rl_model.srel
    played = [s['year'] for s in (row.get('scoring') or []) if (s.get('games') or 0) > 0]
    if not played:
        return {}
    d = min(played)
    out = {}
    for s in (row.get('scoring') or []):
        k = s['year'] - d + 1
        if (s.get('games') or 0) >= 4 and 1 <= k <= 14 and s.get('avg') is not None:
            out[k] = (float(s['avg']), int(s['games']), int(s['year']))
    return out


def track_delta(g, pk, sr):                             # rl_model.track_delta, STBL semantics
    num = den = tg = 0.0
    for s, (a, gm, _yr) in sr.items():
        if s > 8:
            continue
        w = RWE.get(s, 1.7) * min(gm, 22)
        num += (a - expected_c(g, pk, s)) * w
        den += w
        tg += gm
    return (num / den, tg) if den else (None, 0)


def main():
    store = json.load(open(os.path.join(ENG, 'rl_model_data.json'), encoding='utf-8'))
    season_now = max((s.get('year') or 0) for r in store for s in (r.get('scoring') or []))
    nd = [r for r in store
          if r.get('draft_stream') == 'ND' and r.get('stream_pick') and r.get('stream_year')
          and season_now - r['stream_year'] >= MATURE_SEASONS
          and r.get('drafted_position') in POS]

    res = collections.defaultdict(lambda: {'d': [], 'beat': 0, 'never': 0})
    for r in nd:
        key = (bandof(r['stream_pick']), r['drafted_position'])
        d, _tg = track_delta(r['drafted_position'], r['stream_pick'], srel(r))
        if d is None:
            res[key]['never'] += 1
            continue
        res[key]['d'].append(d)
        if d > 0:
            res[key]['beat'] += 1

    print("TRACK-DELTA ON DRAFT HISTORY — the engine's own bar, its own measure, its own semantics")
    print("positive = the men taken there beat the bar the model sets for that exact pedigree\n")
    print("%-11s" % 'band' + ''.join('%15s' % p for p in POS))
    for b in range(NB):
        line = '%-11s' % str(tuple(BANDS[b]))
        for p in POS:
            e = res.get((b, p))
            if not e or len(e['d']) < 10:
                line += '%15s' % ('n=%d' % (len(e['d']) if e else 0))
            else:
                line += '%15s' % ('%+.1f %d%% n%d' % (st.mean(e['d']),
                                                      round(100 * e['beat'] / len(e['d'])),
                                                      len(e['d'])))
        print(line)

    print("\nALL BANDS")
    for p in POS:
        d = [x for b in range(NB) for x in res.get((b, p), {'d': []})['d']]
        beat = sum(res.get((b, p), {'beat': 0})['beat'] for b in range(NB))
        never = sum(res.get((b, p), {'never': 0})['never'] for b in range(NB))
        if d:
            print('  %-5s delta %+6.2f   above bar %4.0f%%   n=%-4d  washed out %d (%.0f%%)'
                  % (p, st.mean(d), 100 * beat / len(d), len(d), never,
                     100 * never / (len(d) + never)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
