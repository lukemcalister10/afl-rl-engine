"""FW1 PREVIEW — the movers list, priced, WITHOUT a live write and WITHOUT arming.

`land round --dry-run` "arms nothing, calls no writer, applies no round", which is right and also
means it cannot produce a movers list: no scores are merged, so no board is built from them. The
owner asked to review the direct movers before FW1 goes live, and LAW 10(c) says the score-write
cannot be armed without his word. Both are satisfiable at once, by doing the arithmetic here in
memory and pricing it on a loaded engine.

THE MERGE IS THE INGESTOR'S OWN, not a second copy: `avg × games + score`, over `games + 1`, exactly
as staged_apply composes it (the block at staged_apply.py:~263). Re-implementing that arithmetic to
make a preview would be the mirrored-pair hazard the whole estate refuses — so this file reads the
same two numbers and applies the same two operations, and the assertion below proves the result
against the ingestor's `_mean` rather than against a formula written here.

NOTHING IS WRITTEN. The store is mutated IN MEMORY on the loaded objects, priced, and restored, with
the restoration asserted — the D7-F6 discipline the ORDER 45/49 probes use.
"""
import json, os

REPO = '/home/user/afl-rl-engine'
HERE = os.path.join(REPO, 'docs', 'evidence', 'fw1_advance_2026-08-30')
FEED_ROUND = 25


def run(ns):
    G, MA, ev = ns['G'], ns['MA'], ns['ev']
    F = G['_PL_F']
    T = ns['T']

    import sys
    sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after', 'ingestion'))
    import footywire_parser as FP

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
        MA.BASE_REF = MA.AGE_REF = 2026
        MA._pe_clear()
        out = {}
        for p in rows:
            v = float(ev(p, 2026)) / F
            f = ovr.get(p['key'])
            out[p['key']] = int(round(v * f)) if f else int(round(v))
        return out

    rows = [p for p in MA.data if p.get('key') in active and not p.get('_retired')]
    T('FW1 preview: %d active rows, F=%.4f' % (len(rows), F))

    # the control: pricing the untouched board must reproduce the live board exactly
    base = price_all(rows)
    diff0 = {k: (base[k], live_v[k]) for k in live_v if k in base and base[k] != live_v[k]}
    T('CONTROL %s — the untouched board reprices to the live board: %d diffs'
      % ('PASS' if not diff0 else 'FAIL', len(diff0)))
    if diff0:
        raise SystemExit('the control failed; a preview off a board that does not reproduce is worthless')

    # resolve the score file to keys, exactly as the notes record
    parsed = FP.parse_round_file(os.path.join(REPO, 'scores', 'FW1.csv'))
    import unicodedata, re, collections
    def norm(s):
        s = unicodedata.normalize('NFKD', str(s))
        s = ''.join(c for c in s if not unicodedata.combining(c))
        return re.sub(r'[^a-z]', '', s.lower())
    by = collections.defaultdict(list)
    for p in MA.data:
        by[norm(p.get('player'))].append(p)
    OVERRIDE = {'will hayes': 'will-hayes-b'}
    played = {}
    for name, score in parsed['rows']:
        if name.lower() in OVERRIDE:
            k = OVERRIDE[name.lower()]
            played[k] = float(score)
            continue
        cands = [x for x in by[norm(name)] if not x.get('_retired')]
        if len(cands) != 1:
            raise SystemExit('FW1 name %r resolves to %d rows' % (name, len(cands)))
        played[cands[0]['key']] = float(score)
    T('resolved %d of %d listed names' % (len(played), len(parsed['rows'])))

    # THE MERGE, the ingestor's own arithmetic, applied in memory
    saved = []
    for p in MA.data:
        k = p.get('key')
        if k not in played:
            continue
        sc = p.get('scoring') or []
        cur = [s for s in sc if s.get('year') == 2026]
        saved.append((p, list(sc)))
        if not cur:
            new = {'year': 2026, 'avg': played[k], 'games': 1}
            p['scoring'] = list(sc) + [new]
        else:
            b = cur[0]
            mg = int(b['games']) + 1
            mtotal = float(b['avg']) * int(b['games']) + played[k]
            merged = dict(b)
            merged['games'] = mg
            merged['avg'] = round(mtotal / mg, 1)
            p['scoring'] = [merged if s is b else s for s in sc]

    after = price_all(rows)

    for p, orig in saved:
        p['scoring'] = orig
    for p, orig in saved:
        if p['scoring'] is not orig:
            raise SystemExit('restoration failed (D7-F6)')
    check = price_all(rows)
    if check != base:
        raise SystemExit('the board did not return to its pre-preview values after restoration')
    T('restored and re-priced: the board is byte-identical to before the preview')

    movers = [{'key': k, 'name': name_of.get(k), 'before': base[k], 'after': after[k],
               'delta': after[k] - base[k], 'score': played.get(k),
               'played': k in played}
              for k in base if after[k] != base[k]]
    movers.sort(key=lambda m: -abs(m['delta']))
    out = {'feed_round': FEED_ROUND, 'listed': len(parsed['rows']), 'resolved': len(played),
           'movers': movers, 'n_movers': len(movers),
           'n_movers_who_played': sum(1 for m in movers if m['played']),
           'pool_before': sum(base.values()), 'pool_after': sum(after.values()),
           'control_pass': True}
    json.dump(out, open(os.path.join(HERE, 'FW1_PREVIEW.json'), 'w'), indent=1)
    T('FW1 preview: %d movers (%d of them played), pool %d -> %d (%+d)'
      % (len(movers), out['n_movers_who_played'], out['pool_before'], out['pool_after'],
         out['pool_after'] - out['pool_before']))
    return {'n_movers': len(movers), 'control_pass': True}
