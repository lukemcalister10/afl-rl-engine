"""FW1 AS A STORE EDIT — emit the edit list AND the movers it predicts, from one engine load.

THE OWNER'S POINT, 2026-08-30: "We're literally just updating player averages and game counts.
Before round 14 we didn't add games one by one, we just priced based off averages and total season
game counts." The store agrees with him — Bontempelli's 2016 row reads 26 games, which is 22
home-and-away plus four finals — so a finals week has always been two numbers on a season row, and
the round-advance lane's calendar apparatus was machinery in search of a problem.

SO THIS EMITS AN `act_kind: store-edit` SPEC. 92 players, two fields each:
    scoring[2026].games   g      -> g + 1
    scoring[2026].avg     a      -> round((a*g + score) / (g+1), 2)
and NOTHING else. The career `games` field is deliberately untouched: `_merge_into_store` does not
touch it either (round_apply.py:185), and an edit that "helpfully" also moved it would be a second
writer inventing a rule the ingestor never had.

TWO DECIMALS, NOT ONE. The earlier preview (pass_fw1_preview.py) rounded to ONE decimal. The
ingestor's own constant is `ROUND_DECIMALS = 2` (score_ingestor.py:41, "verified: every stored avg
== round(avg,2)"), and the store shows two — Bontempelli 2026 is 117.17. That preview's 87-mover
list was therefore computed at the wrong precision, and this pass reads the constant rather than
restating it.

THE ARITHMETIC IS THE INGESTOR'S, READ FROM THE INGESTOR. `_mean` and `ROUND_DECIMALS` are imported
and called, not re-implemented: a mirrored pair that drifts is the hazard the estate refuses.

NOTHING IS WRITTEN TO THE STORE. The rows are mutated in memory, priced, restored, and the
restoration is asserted by re-pricing (D7-F6).
"""
import collections
import json
import os
import re
import sys
import unicodedata

REPO = '/home/user/afl-rl-engine'
OUT_DIR = os.path.join(REPO, 'docs', 'evidence', 'finals_fw1_2026-08-30')
SEASON = 2026
SCORES = os.path.join(REPO, 'scores', 'FW1.csv')


def _norm(s):
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower())


def run(ns):
    G, MA, ev, T = ns['G'], ns['MA'], ns['ev'], ns['T']
    F = G['_PL_F']
    sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after', 'ingestion'))
    import footywire_parser as FP
    import score_ingestor as SI

    decimals = SI.ROUND_DECIMALS
    T('ingestor precision read from the ingestor: ROUND_DECIMALS=%d' % decimals)
    if decimals != 2:
        raise SystemExit('ROUND_DECIMALS is %r; the store carries two-decimal averages' % decimals)

    live = json.load(open(os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')))
    live_v = {r['key']: r['v'] for r in live['active']}
    name_of = {r['key']: r.get('name') for r in live['active']}
    active = set(live_v)

    ovr = {}
    op = os.path.join(REPO, 'data', 'owner_overrides.json')
    if os.path.exists(op):
        try:
            _o = json.load(open(op))
            for row in (_o.get('overrides') or _o if isinstance(_o, list) else []):
                if isinstance(row, dict) and row.get('key') and row.get('factor'):
                    ovr[row['key']] = float(row['factor'])
        except Exception:
            pass

    def price_all(rows):
        MA.BASE_REF = MA.AGE_REF = SEASON
        MA._pe_clear()
        out = {}
        for p in rows:
            v = float(ev(p, SEASON)) / F
            f = ovr.get(p['key'])
            out[p['key']] = int(round(v * f)) if f else int(round(v))
        return out

    rows = [p for p in MA.data if p.get('key') in active and not p.get('_retired')]
    base = price_all(rows)
    diff0 = {k: (base[k], live_v[k]) for k in live_v if k in base and base[k] != live_v[k]}
    T('CONTROL %s — the untouched board reprices to the live board: %d diff(s)'
      % ('PASS' if not diff0 else 'FAIL', len(diff0)))
    if diff0:
        raise SystemExit('the control failed; an edit list measured against a board that does not '
                         'reproduce is worthless')

    parsed = FP.parse_round_file(SCORES)
    by = collections.defaultdict(list)
    for p in MA.data:
        by[_norm(p.get('player'))].append(p)
    OVERRIDE = {'will hayes': 'will-hayes-b'}          # owner: "Will Hayes is Will Hayes b"
    by_key = {p.get('key'): p for p in MA.data if p.get('key')}

    played = {}
    for name, score in parsed['rows']:
        if name.lower() in OVERRIDE:
            played[OVERRIDE[name.lower()]] = float(score)
            continue
        cands = [x for x in by[_norm(name)] if not x.get('_retired')]
        if len(cands) != 1:
            raise SystemExit('FW1 name %r resolves to %d row(s)' % (name, len(cands)))
        played[cands[0]['key']] = float(score)
    if len(played) != len(parsed['rows']):
        raise SystemExit('%d listed names collapsed to %d keys' % (len(parsed['rows']), len(played)))
    T('resolved %d of %d listed names to distinct store keys' % (len(played), len(parsed['rows'])))

    # ---- the edit list, and the in-memory merge that proves it
    edits, saved = [], []
    for key in sorted(played):
        p = by_key.get(key)
        if p is None:
            raise SystemExit('resolved key %r is not in the store' % key)
        sc = p.get('scoring') or []
        cur = [s for s in sc if s.get('year') == SEASON]
        if len(cur) != 1:
            raise SystemExit('%s has %d %d-season rows; a finals edit needs exactly one to amend'
                             % (key, len(cur), SEASON))
        b = cur[0]
        g0, a0 = int(b['games']), float(b['avg'])
        g1 = g0 + 1
        a1 = SI.ScoreIngestor._mean(_D(decimals), a0 * g0 + played[key], g1)
        edits.append({'key': key, 'field': 'scoring[%d].games' % SEASON, 'old': g0, 'new': g1})
        edits.append({'key': key, 'field': 'scoring[%d].avg' % SEASON, 'old': b['avg'], 'new': a1})
        saved.append((p, list(sc), dict(b)))
        merged = dict(b); merged['games'] = g1; merged['avg'] = a1
        p['scoring'] = [merged if s is b else s for s in sc]

    after = price_all(rows)

    for p, orig_list, orig_entry in saved:
        p['scoring'] = orig_list
        for s in orig_list:
            if s.get('year') == SEASON:
                s.update(orig_entry)
    if price_all(rows) != base:
        raise SystemExit('the board did not return to its pre-edit values after restoration (D7-F6)')
    T('restored and re-priced: the board is identical to before the edit was simulated')

    movers = [{'key': k, 'name': name_of.get(k), 'before': base[k], 'after': after[k],
               'delta': after[k] - base[k], 'score': played.get(k), 'played': k in played}
              for k in sorted(base) if after[k] != base[k]]
    movers.sort(key=lambda m: -abs(m['delta']))
    non_players = [m for m in movers if not m['played']]

    os.makedirs(OUT_DIR, exist_ok=True)
    out = {'season': SEASON, 'scores_file': 'scores/FW1.csv', 'round_decimals': decimals,
           'listed': len(parsed['rows']), 'resolved': len(played),
           'edits': edits, 'n_edits': len(edits),
           'expected_movers': [{'key': m['key'], 'before': m['before'], 'after': m['after']}
                               for m in movers],
           'movers_detail': movers, 'n_movers': len(movers),
           'n_movers_who_played': sum(1 for m in movers if m['played']),
           'n_movers_who_did_not_play': len(non_players),
           'pool_before': sum(base.values()), 'pool_after': sum(after.values()),
           'control_pass': True}
    json.dump(out, open(os.path.join(OUT_DIR, 'FW1_EDIT_PLAN.json'), 'w'), indent=1)
    T('FW1 edit plan: %d edits over %d players; %d movers (%d played, %d did not); pool %d -> %d (%+d)'
      % (len(edits), len(played), len(movers), out['n_movers_who_played'],
         out['n_movers_who_did_not_play'], out['pool_before'], out['pool_after'],
         out['pool_after'] - out['pool_before']))
    return {'n_edits': len(edits), 'n_movers': len(movers),
            'n_movers_who_did_not_play': len(non_players),
            'pool_delta': out['pool_after'] - out['pool_before']}


class _D(object):
    """Adapter so the ingestor's own `_mean` runs with its own precision and nothing is restated."""
    def __init__(self, decimals):
        self.round_decimals = decimals
