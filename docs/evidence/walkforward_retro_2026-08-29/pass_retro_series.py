"""THE WALK-FORWARD RETROSPECTIVE, ON ONE ENGINE LOAD (owner directive: "Load things once").

Supersedes the per-round subprocess builds in retro_walkforward.py. Those paid a full engine load
(~15-20 min) PER ROUND — eleven loads for eleven rounds — and with container reclaims landing every
20-30 minutes not one of them ever finished. The pricing itself is milliseconds per player; only the
load is expensive, and the load does not depend on the round.

SO: load once (the harness does it), then for each round R in 14..24 —
    1. set the season clock globals to the round's DERIVED values (from the stores already emitted
       by retro_walkforward.py emit-stores, each derived by the immutable repo-root policy):
           MA.SEASON_PROG  <- calendar_progress(R)          (rl_model)
           cp.EXPO_F       <- exposure_pace(R)              (conditional_prior)
    2. truncate every player's 2026 row IN PLACE to as-at-R (the same arithmetic as the store
       emitter, applied to the loaded objects),
    3. clear the memoised peak/prior caches and price the whole active board with the engine's own
       ev() — the SAME function the export path calls,
    4. restore every mutated row EXACTLY and assert the restoration (the D7-F6 discipline the ORDER
       45/49 counterfactual probes use: a probe that corrupts the board it prices is worthless).

CURRENCY: ev() answers in engine currency; the board's `v` is round(ev / _PL_F) with the display
layer's owner overrides applied. Both are read from the engine itself, and R24 — whose truncation
is a no-op — is the CONTROL: its output must reproduce the live board's values exactly, which
validates the clock handling, the currency mapping and the display layer in one assertion.
"""
import json, os

HERE = '/home/user/afl-rl-engine/docs/evidence/walkforward_retro_2026-08-29'
REPO = '/home/user/afl-rl-engine'
WORK = '/home/claude/retro_walkforward'
ROUNDS = list(range(14, 26))   # 25 = FINALS WEEK 1 (feed round above the H&A season)


def run(ns):
    G, MA, ev = ns['G'], ns['MA'], ns['ev']
    cp = G.get('cp')
    if cp is None or not hasattr(cp, 'EXPO_F'):
        raise SystemExit('HALT: conditional_prior (cp.EXPO_F) not reachable — the season clock '
                         'cannot be set per round; refusing to price a wrong-clock series.')
    F = G['_PL_F']

    live = json.load(open(os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')))
    live_v = {r['key']: r['v'] for r in live['active']}
    active_keys = set(live_v)

    # THE OWNER DISPLAY OVERRIDES ARE DELIBERATELY NOT APPLIED HERE (2026-09-01). This block used to
    # re-read data/owner_overrides.json and multiply the priced value by the row's factor. It never
    # worked — it looked for `key` where that file writes `player_key`, so it reported "0 overrides"
    # with one on file (will-brodie x0.5, DECISIONS v85 §20) and applied nothing.
    #
    # AND IT MUST NOT BE FIXED, because it contradicts this pass's own control. `live_v` above reads
    # r['v'] — the PRE-override engine value (Brodie 117). The export writes the override as an `ov`
    # block beside it (`{factor: 0.5, dispv: 58}`) and never touches `v`, exactly as
    # data/owner_overrides.json says: "Applied LAST at the export/display layer ... NEVER touches the
    # engine value `v`". So a working multiplication here would bank 58 against a control expecting
    # 117 and red the control by one row, forever.
    #
    # The override has ONE application site and it is the display layer — ui/app/seam.js:113,
    # `(p.ov && p.ov.dispv != null) ? p.ov.dispv : p.v`, which substitutes it wherever the board
    # shows his value, ordering included. A second site here is the duplicated-assertion class this
    # estate keeps paying for. Banking the pre-override value is what keeps the two consistent.
    ovr = {}

    rows = [p for p in MA.data if p.get('key') in active_keys and not p.get('_retired')]
    ns['T']('retro: %d active rows, %d overrides, F=%.4f' % (len(rows), len(ovr), F))

    def price_all():
        MA.BASE_REF = MA.AGE_REF = 2026
        MA._pe_clear()
        out = {}
        for p in rows:
            v = float(ev(p, 2026)) / F
            f = ovr.get(p['key'])
            out[p['key']] = int(round(v * f)) if f else int(round(v))
        return out

    banked = []
    for R in ROUNDS:
        # RESUMABLE: a banked round is skipped, so a reclaim mid-series costs only the load, and
        # the next run finishes the remainder. (Container reclaims are landing every ~15 min.)
        if os.path.exists(os.path.join(HERE, 'values_r%d.json' % R)):
            banked.append(R)
            ns['T']('r%-3d already banked — skipped' % R)
            continue
        meta = json.load(open(os.path.join(WORK, 'r%d' % R, 'META.json')))
        st = json.load(open(os.path.join(WORK, 'r%d' % R, 'season_state.json')))
        trunc = json.load(open(os.path.join(WORK, 'r%d' % R, 'rl_model_data.json')))
        tp = trunc['players'] if isinstance(trunc, dict) and 'players' in trunc else trunc
        by_sid, by_name = {}, {}
        for q in tp:
            if q.get('stable_player_id'):
                by_sid[q['stable_player_id']] = q
            by_name.setdefault(q.get('player'), []).append(q)

        # 1. the round's season clock
        MA.SEASON_PROG = st['calendar_progress']
        cp.EXPO_F = st['exposure_pace']
        if 'SEASON_PROG' in G:
            G['SEASON_PROG'] = st['calendar_progress']

        # 2. truncate in place, remembering the originals
        saved = []
        for p in MA.data:
            sid = p.get('stable_player_id')
            q = by_sid.get(sid) if sid else None
            if q is None:
                cands = by_name.get(p.get('player')) or []
                q = cands[0] if len(cands) == 1 else None
            if q is None:
                continue
            if q.get('scoring') != p.get('scoring'):
                saved.append((p, p['scoring']))
                p['scoring'] = q['scoring']

        # 3. price the board as at R
        vals = price_all()

        # 4. restore EXACTLY, and prove it
        for p, orig in saved:
            p['scoring'] = orig
        for p, orig in saved:
            if p['scoring'] is not orig:
                raise SystemExit('HALT r%d: restoration failed on %r (D7-F6).' % (R, p.get('key')))

        out = os.path.join(HERE, 'values_r%d.json' % R)
        json.dump({'round': R, 'n': len(vals), 'store_md5': meta['store_md5'],
                   'calendar_progress': st['calendar_progress'],
                   'exposure_pace': st['exposure_pace'],
                   'board_md5': 'in-process-ev/%s' % meta['store_md5'][:8],
                   'values': vals}, open(out, 'w'), indent=1)
        banked.append(R)
        ns['T']('r%-3d priced %d rows (cal %.2f pace %.3f) -> values_r%d.json'
                % (R, len(vals), st['calendar_progress'], st['exposure_pace'], R))

    # THE CONTROL, asserted immediately on the same load
    # THE CONTROL IS THE LAST POINT, WHICH IS THE ONE WHOSE TRUNCATION IS A NO-OP. It was r24 while
    # r24 was the last football; once FINALS WEEK 1 landed, r24 legitimately EXCLUDES the finals game
    # and can no longer reproduce a live board that includes it. Leaving the control on r24 is what
    # made the series wrong: on 2026-09-01 it failed, and the fix applied was to push the finals game
    # back into every round until it passed — the data bent to satisfy a stale check. The check was
    # the thing that was stale. It now names the last round in the window, whatever that is.
    _ctl = ROUNDS[-1]
    got = json.load(open(os.path.join(HERE, 'values_r%d.json' % _ctl)))['values']
    diff = {k: (got[k], live_v[k]) for k in live_v if k in got and got[k] != live_v[k]}
    missing = [k for k in live_v if k not in got]
    verdict = {'rounds': banked, 'control_diffs': len(diff), 'control_missing': len(missing),
               'control_pass': not diff and not missing,
               'sample_diffs': dict(list(diff.items())[:12])}
    json.dump(verdict, open(os.path.join(HERE, 'RETRO_ONELOAD_VERDICT.json'), 'w'), indent=1)
    ns['T']('CONTROL %s — r%d vs live board: %d diffs, %d missing'
            % ('PASS' if verdict['control_pass'] else 'FAIL', _ctl, len(diff), len(missing)))
    return verdict
