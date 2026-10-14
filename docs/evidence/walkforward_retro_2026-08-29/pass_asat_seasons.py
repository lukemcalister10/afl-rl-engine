"""THE AS-AT SEASON BOARDS, ON ONE ENGINE LOAD (owner ruling 2026-10-14).

THE RULING. The -1 and -2 lens columns must become TRUE AS-AT BOARDS: the board as it stood at the end
of the 2025 season (-1) and at the end of 2024 (-2). Every player listed then — about 780-820, the
since-retired included — priced by the engine with THAT season as the base year; players not yet
debuted excluded. Today the live board's vM1/vM2 are ev(p,2024)/ev(p,2025) on the CURRENT 804 rows
(rl_export.py:210-212), so a November-2025 draftee carries a -1 value he never had and a 2025
retiree is scrap on the board he finished. This pass prices the as-at boards instead and BANKS them;
it does not touch the engine's export (the live board's vM1/vM2 stay as they are until the owner has
seen the as-at numbers — emit_asat_seasons.py carries the bank into the UI as derived data).

THE ROSTER RULE (R1, "for now"; the owner may later supply list files, which would replace it):
    on the board at end of Y  iff  debut(p) <= Y                                   (not yet debuted: out)
                              and ( played a game in Y
                                 or _last_listed >= Y                              (owner ground truth)
                                 or active now                                     (listed today => listed at Y)
                                 or never played and debut(p) <= Y <= debut(p)+1 ) (unplayed, inside the
                                                                                    entry window — _on_board's
                                                                                    own rule, rl_model.py:2161)
    debut = draft year + 1, except MSD = draft year (rl_model.py:171). "Active now" = on the live board
    (data/rl_build/rl_app_data.json active keys) and neither _retired nor delisted. Duplicate-key groups
    collapse by the engine's own _dkey/_rich helpers (rl_model.py:1325-1326), an active-now record
    winning its group as the engine's recall loop does (rl_model.py:2171-2178).
    KNOWN R1 GAP, stated so it is not mistaken for a bug: a player listed at Y who played no game in Y
    and later left (a season-long injury, then retirement) is on no as-at board unless _last_listed says
    so. The store carries 13 _last_listed rows today; a list file closes this.

PRICING AT A PAST BASE YEAR (per row, then everything restored):
    MA.BASE_REF = MA.AGE_REF = Y; MA._pe_clear(); MA._LENS_FORM = None (the balanced/back path:
    _b6_core pins BASE_REF=AGE_REF=Y, byte-exact — _merged_recover.py:450);
    the row's scoring is rewound to seasons <= Y and `games` recomputed (the engine's own _trunc_p
    arithmetic, rl_model.py:2151-2153); `_retired` / `_last_listed` are cleared for the duration so
    delisted() (_merged_recover.py:1598) does not scrap a player who was LISTED at Y (ev's first line,
    :2966, returns 2% of v0 for a delisted row — the right answer on the Now board, the wrong one on
    the board he was still playing on). Season state stays at 2026: a completed season is handled as
    completed because Y != INPROG_Y. Scoring is rewound on EVERY store row, not only the roster, so a
    peer read at call time (if any) sees the same as-at world; the flags are cleared on roster rows only.
    LAYERS GATED ON Y==2026 ARE OFF BY CONSTRUCTION for Y in (2025, 2024): the sitter-sheet haircut
    and the D7 / ORDER 45 / ORDER 49 guards all test `int(Y)!=2026` and pass the inner value through;
    ORDER 46 is as-of-Y by its own class definition (_o46_class(p,Y)). Guard 5 / boot_guard /
    release_manifest_check do not fire on the in-process harness route; the harness ran them on entry.

CURRENCY: ev() answers in engine currency; the board's `v` is round(ev / _PL_F) — the exact
normalisation pass_retro_series.py uses, owner display overrides deliberately NOT applied (that file's
2026-09-01 note: the override has ONE application site, the display layer, and `v` is pre-override).

THE CONTROL RUNS FIRST. Y=2026 priced on the live active set through the SAME rewind / clear / price
/ restore machinery (its rewind is a no-op) must reproduce the live board's `v` on every row — the
identity pass_retro_series.py asserts as its control. A machinery that cannot reproduce the present
has no business pricing the past, so a failed control HALTS before a single as-at value is banked.

RESTORATION IS ASSERTED BYTE-EXACT (the D7-F6 discipline): every mutated row is snapshotted as
canonical JSON before the rewind and compared after the restore; the original `scoring` list object is
put back by identity; a `_last_listed` that was absent is absent again, not None. A probe that
corrupts the board it prices is worthless.

RUN:  tools/harness docs/evidence/walkforward_retro_2026-08-29/pass_asat_seasons.py
      (one engine load; the control plus two seasons, ~1,600 ev() calls, a few minutes after the load)
WRITES: values_asat_2025.json, values_asat_2024.json, ASAT_VERDICT.json beside this file.
"""
import copy
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = HERE                       # tests point this at a temp dir
NOW = 2026                           # the present season (INPROG_Y); "active now" and the control are measured here
SEASONS = (2025, 2024)               # -1, -2
GRP = ('MID', 'RUCK', 'SF', 'KPF', 'SD', 'KPD')     # rl_model.GRP — the positions the board values
RULE = ('R1 (owner ruling 2026-10-14): on the board at end of Y iff debut<=Y (debut=year+1; MSD=year) and '
        '(played a game in Y, or _last_listed>=Y, or active now, or never played and debut<=Y<=debut+1). '
        'Priced with BASE_REF=AGE_REF=Y, scoring rewound to <=Y, _retired/_last_listed cleared for the '
        'duration; v=round(ev/_PL_F), no display override.')
_ABSENT = object()                   # sentinel: the field was not on the row (restore must DELETE it, not None it)


# ---------------------------------------------------------------- the rule, as pure functions (dry-testable)
def debut(p):
    """rl_model.debut: ONLY MSD debuts in its draft year; everyone else is an off-season entry -> year+1."""
    return p['year'] if p.get('type') == 'MSD' else p['year'] + 1


def last_game_year(p):
    ys = [r['year'] for r in (p.get('scoring') or []) if (r.get('games') or 0) >= 1]
    return max(ys) if ys else None


def played_in(p, Y):
    return any(r['year'] == Y and (r.get('games') or 0) >= 1 for r in (p.get('scoring') or []))


def delisted_now(p):
    """_merged_recover.delisted, verbatim: retired, or an owner-recorded last listing before NOW."""
    ll = p.get('_last_listed')
    return bool(p.get('_retired')) or (ll is not None and ll < NOW)


def active_now(p, active_keys):
    return p.get('key') in active_keys and not delisted_now(p)


def on_board_asat(p, Y, active_keys):
    """R1. Returns the REASON the row is on the board at end of Y (a short code), or None."""
    if p.get('pos') not in GRP:
        return None
    if debut(p) > Y:
        return None                                        # not yet debuted by end of Y (Nov-Y draftees, Y+1 MSDs)
    if played_in(p, Y):
        return 'played'
    ll = p.get('_last_listed')
    if ll is not None and ll >= Y:
        return 'listed'                                    # owner ground truth: listed through Y
    if active_now(p, active_keys):
        return 'active_now'                                # listed today and debuted by Y => listed at Y
    if last_game_year(p) is None and debut(p) <= Y <= debut(p) + 1:
        return 'entry_window'                              # unplayed prospect inside his initial-contract window
    return None


def dkey(p):
    """rl_model._dkey (the slug branch is only for key-less rows; the store carries a key on every row)."""
    return (p.get('key') or p['player']) + ('|u' if p.get('_unplayed') and not p.get('key') else '')


def rich(p):
    """rl_model._rich: earliest entry (original draft record), fuller history / real pick as tiebreak."""
    return (-(p.get('year') or 9999), len(p.get('scoring') or []), 1 if p.get('pick') else 0)


def roster(data, Y, active_keys):
    """The as-at population for Y over ALL store rows, one row per key. An active-now record wins its
    duplicate-key group (the engine's recall loop skips retired records whose key is active); otherwise
    the richest record by _rich. Returns [(row, reason)] in store order."""
    best, order = {}, []
    for p in data:
        why = on_board_asat(p, Y, active_keys)
        if why is None:
            continue
        k = dkey(p)
        cur = best.get(k)
        if cur is None:
            order.append(k); best[k] = (p, why); continue
        a_new, a_cur = active_now(p, active_keys), active_now(cur[0], active_keys)
        if (a_new and not a_cur) or (a_new == a_cur and rich(p) > rich(cur[0])):
            best[k] = (p, why)
    return [best[k] for k in order]


# ---------------------------------------------------------------- rewind / restore (dry-testable)
def snapshot(p):
    return json.dumps(p, sort_keys=True, default=str)


def rewind(p, Y, clear_flags):
    """Rewind ONE row in place to the end of season Y; return what it takes to put it back exactly.
    scoring -> seasons <= Y (a NEW list; the original object is kept and restored by identity);
    games -> recomputed over the kept seasons (rl_model._trunc_p); with clear_flags, _retired -> False
    and _last_listed -> None so delisted() is False for the duration."""
    saved = {'_snap': snapshot(p), 'scoring': p['scoring'],
             'games': p['games'] if 'games' in p else _ABSENT}
    p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
    p['games'] = sum(int(r.get('games') or 0) for r in p['scoring'])
    if clear_flags:
        saved['_retired'] = p['_retired'] if '_retired' in p else _ABSENT
        saved['_last_listed'] = p['_last_listed'] if '_last_listed' in p else _ABSENT
        p['_retired'] = False
        p['_last_listed'] = None
    return saved


def restore(p, saved):
    """Put the row back and PROVE it: identity on the scoring object, byte-exact on the whole row."""
    for f in ('scoring', 'games', '_retired', '_last_listed'):
        if f not in saved:
            continue
        if saved[f] is _ABSENT:
            p.pop(f, None)
        else:
            p[f] = saved[f]
    if p['scoring'] is not saved['scoring']:
        raise RuntimeError('HALT (D7-F6): scoring object not restored by identity on %r' % p.get('key'))
    after = snapshot(p)
    if after != saved['_snap']:
        b, a = json.loads(saved['_snap']), json.loads(after)
        bad = sorted(k for k in set(b) | set(a) if b.get(k, _ABSENT) != a.get(k, _ABSENT))
        raise RuntimeError('HALT (D7-F6): row %r not byte-exact after restore; fields differ: %s'
                           % (p.get('key'), bad))


def price_rows(ns, Y, rows, all_rows=None):
    """Rewind -> price every row at base year Y -> restore everything and assert it. Returns {key: v}.
    `rows` is the roster (flags cleared, priced); `all_rows` (default: MA.data) has its scoring rewound
    too, so the as-at world is whole. The clock globals are pinned per row, as rl_export does, and put
    back afterwards."""
    G, MA, ev = ns['G'], ns['MA'], ns['ev']
    F = float(G['_PL_F'])
    if all_rows is None:
        all_rows = MA.data
    roster_ids = set(id(p) for p in rows)
    clock = (MA.BASE_REF, MA.AGE_REF, getattr(MA, '_LENS_FORM', None),
             G.get('BASE_REF', _ABSENT), G.get('AGE_REF', _ABSENT), G.get('_LENS_FORM', _ABSENT))
    saved = []
    try:
        for p in all_rows:
            if id(p) in roster_ids:
                continue
            if any(r['year'] > Y for r in p.get('scoring') or []):
                saved.append((p, rewind(p, Y, clear_flags=False)))
        for p in rows:
            saved.append((p, rewind(p, Y, clear_flags=True)))
        MA._LENS_FORM = None
        if '_LENS_FORM' in G: G['_LENS_FORM'] = None
        out = {}
        for p in rows:
            MA.BASE_REF = MA.AGE_REF = Y
            if 'BASE_REF' in G: G['BASE_REF'] = Y
            if 'AGE_REF' in G: G['AGE_REF'] = Y
            MA._pe_clear()
            out[p['key']] = int(round(float(ev(p, Y)) / F))
        return out
    finally:
        for p, s in saved:
            restore(p, s)
        MA.BASE_REF, MA.AGE_REF, MA._LENS_FORM = clock[0], clock[1], clock[2]
        for name, val in (('BASE_REF', clock[3]), ('AGE_REF', clock[4]), ('_LENS_FORM', clock[5])):
            if val is not _ABSENT: G[name] = val
        MA._pe_clear()


# ---------------------------------------------------------------- the pass
def _md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def store_path(repo):
    """The store the loaded engine read: the harness workdir's copy (cwd) when it is there, else the
    repo's pinned store. Either way its md5 must equal the boot pin."""
    cand = os.path.join(os.getcwd(), 'rl_model_data.json')
    return cand if os.path.exists(cand) else os.path.join(repo, 'engine', 'rl_after', 'rl_model_data.json')


def run(ns):
    G, MA, ev, T = ns['G'], ns['MA'], ns['ev'], ns['T']
    repo = ns['repo']
    board_path = os.path.join(repo, 'data', 'rl_build', 'rl_app_data.json')
    live = json.load(open(board_path))
    live_v = {r['key']: r['v'] for r in live['active']}
    active_keys = set(live_v)
    board_md5 = _md5(board_path)
    sp = store_path(repo)
    store_md5 = _md5(sp)
    boot = json.load(open(os.path.join(repo, 'data', 'expected_boot.json')))
    if boot.get('store') and boot['store'] != store_md5:
        raise RuntimeError('HALT: store %s (%s) is not the pinned store %s — refusing to bank an as-at '
                           'board against an unpinned store.' % (store_md5[:8], sp, boot['store'][:8]))
    if boot.get('board') and boot['board'] != board_md5:
        raise RuntimeError('HALT: live board %s is not the pinned board %s.' % (board_md5[:8], boot['board'][:8]))
    T('asat: live board %s (%d active), store %s, F=%.4f'
      % (board_md5[:8], len(active_keys), store_md5[:8], float(G['_PL_F'])))

    # THE CONTROL FIRST: the present, through the as-at machinery, must BE the live board.
    ctl_rows = [p for p in MA.data if p.get('key') in active_keys and not delisted_now(p)]
    got = price_rows(ns, NOW, ctl_rows)
    diff = {k: (got[k], live_v[k]) for k in live_v if k in got and got[k] != live_v[k]}
    missing = [k for k in live_v if k not in got]
    control = {'n': len(got), 'diffs': len(diff), 'missing': len(missing),
               'pass': not diff and not missing, 'sample_diffs': dict(list(diff.items())[:12])}
    T('CONTROL %s — Y=%d through the as-at machinery vs the live board: %d diffs, %d missing'
      % ('PASS' if control['pass'] else 'FAIL', NOW, len(diff), len(missing)))
    verdict = {'control': control, 'seasons': {}, 'board_md5': board_md5, 'store_md5': store_md5, 'rule': RULE}
    os.makedirs(OUT_DIR, exist_ok=True)
    if not control['pass']:
        json.dump(verdict, open(os.path.join(OUT_DIR, 'ASAT_VERDICT.json'), 'w'), indent=1)
        raise RuntimeError('HALT: the control failed (%d diffs, %d missing) — the as-at machinery does not '
                           'reproduce the live board, so nothing is banked.' % (len(diff), len(missing)))

    for Y in SEASONS:
        rows = roster(MA.data, Y, active_keys)
        vals = price_rows(ns, Y, [p for p, _ in rows])
        retired_now = [p['key'] for p, _ in rows if delisted_now(p)]
        reasons = {p['key']: why for p, why in rows}
        n_act = sum(1 for p, _ in rows if p.get('key') in active_keys)
        bank = {'season': Y, 'rule': RULE, 'n': len(vals), 'values': vals, 'retired_now': retired_now,
                'reasons': reasons, 'n_active_now': n_act, 'store_md5': store_md5, 'board_md5': board_md5,
                'base_ref': Y, 'control': 'Y=%d via the same machinery == live board (%d rows, 0 diffs)'
                % (NOW, control['n'])}
        out = os.path.join(OUT_DIR, 'values_asat_%d.json' % Y)
        json.dump(bank, open(out, 'w'), indent=1)
        by = {}
        for _, why in rows: by[why] = by.get(why, 0) + 1
        verdict['seasons'][str(Y)] = {'n': len(vals), 'retired_now': len(retired_now), 'active_now': n_act, 'by_reason': by}
        T('as-at %d: %d on the board (%d retired/delisted today, %d active today; %s) -> %s'
          % (Y, len(vals), len(retired_now), n_act,
             ', '.join('%s %d' % kv for kv in sorted(by.items())), os.path.basename(out)))
    json.dump(verdict, open(os.path.join(OUT_DIR, 'ASAT_VERDICT.json'), 'w'), indent=1)
    return verdict
