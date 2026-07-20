"""ROUND MOVERS — durable weekly movers report + integrated HTML-engine movers data (finalization).

After a round COMMITS (store + board + ledger + value/overall-rank/positional-rank history swapped
atomically) the FINALIZATION phase (round_finalize.py) derives — from the two consecutive committed
boards, via the persistent histories — a DURABLE movers report comparing the newly committed round with
the immediately preceding committed round. This module is the movers half of that finalization: it is
re-derivable, runs OUTSIDE the store transaction, and NEVER writes the store or re-values a board.

For EVERY active player (including DNP players — whose value/rank can still move via ageing,
competition, conservation or universe effects) the report records: stable key, name, AFL club, AFFL
ownership team, position, previous/current round, played/DNP status, submitted score (or an explicit
DNP marker), previous and current value + absolute and % value change, previous/current overall rank +
rank change (positive == improved), and previous/current positional rank + positional-rank change.

The deltas are the EXACT difference of the two committed boards' own value/overall-rank/positional-rank
(read from the histories, which are byte-for-byte board projections), never a re-valuation. Ties are
broken deterministically: primary movement field, then current value descending, then stable key
ascending.

RELEASE IDENTITY (corrective 2026-07-20, review directive B). Each report's `release_identity` is
DERIVED from the coherent release manifest (data/expected_boot.json) at emit time — never a hardcoded
tag. It records release_version, as_of_round, board, balanced_board_md5, store, engine_head, rl_model,
fv, config, register. A historical report keeps its OWN governing identity (the manifest as it stood
when that round committed); a later round never rewrites an earlier report's identity.

Artifacts (finalization, re-derivable, OUTSIDE the store transaction):
  * movers/movers_R<N>.json  — the full machine-readable report (keyed by stable key; exact).
  * movers/movers_R<N>.csv   — the same table as CSV.
  * ui/data/movers.js        — the Matchday UI movers bundle (window.__MATCHDAY_MOVERS__), an ACCUMULATED
                               bundle carrying a release-baseline block + each report's board-identity
                               chain + release identity so the UI can anchor lineage and fail-closed on
                               a mismatched / incomplete / out-of-lineage report. SHIPS EMPTY (no
                               finalized rounds) until real scoring is owner-applied.
  * ui/data/board_view_working.js — augmented in place with dRound / dRoundRank / dRoundPosRank per row.

NO valuation, NO store write.
"""
import csv
import io
import json
import os

try:
    from . import round_history as RH
except (ImportError, ValueError):
    import round_history as RH  # type: ignore

SCHEMA_VERSION = 1
POS_LABEL = {'MID': 'Mid', 'RUC': 'Ruck', 'KEY_FWD': 'Key Fwd', 'GEN_FWD': 'Fwd',
            'KEY_DEF': 'Key Def', 'GEN_DEF': 'Def'}
BASELINE_ROUND = 14   # the accepted board-of-record round; no finalized transactions precede it


def _label_pos(code):
    return POS_LABEL.get(code, (code or '').replace('_', ' ').title() or '—')


def _load(path):
    with open(path) as f:
        return json.load(f)


def _md5(path):
    import hashlib
    if not os.path.exists(path):
        return None
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


# ---- release identity (DERIVED from the coherent release manifest; never hardcoded) --------------
def _boot(repo_root):
    return _load(os.path.join(repo_root, 'data', 'expected_boot.json'))


def _release_version(boot):
    """A DERIVED release version — never a hardcoded marketing tag. Prefers an explicit
    `release_version` in the manifest; otherwise names the board-of-record the release rides on
    (`candidate:<board8>`), so the value can only ever describe the actual pinned board."""
    v = boot.get('release_version')
    if v:
        return v
    board = boot.get('board') or ''
    return 'candidate:%s' % board[:8] if board else 'candidate:unknown'


def release_identity(repo_root, round_n, boot=None):
    """Build a report's release identity from the coherent release manifest (data/expected_boot.json).

    Records the DERIVED release_version, the as-of round, and the manifest's coherent pin set
    (board == balanced board of record, store, engine_head, rl_model, fv, config, register). No field
    is hardcoded; every value comes from the manifest as it stands when this round is finalized, so a
    historical report keeps its own governing identity."""
    boot = boot if boot is not None else _boot(repo_root)
    return {
        'release_version': _release_version(boot),
        'as_of_round': int(round_n),
        'board': boot.get('board'),
        'balanced_board_md5': boot.get('board'),   # the pinned board IS the balanced board of record
        'store': boot.get('store'),
        'engine_head': boot.get('engine_head'),
        'rl_model': boot.get('rl_model'),
        'fv': boot.get('fv'),
        'config': boot.get('config'),
        'register': boot.get('register'),
        'manifest_source': 'data/expected_boot.json',
    }


# ---- the report -----------------------------------------------------------------------------------
def build_report(repo_root, round_n, *, played=None, evidence=None, generated_at=None):
    """Build the full movers report for a committed round from the two committed boards (via histories).

    `played` maps stable key -> submitted score for players LISTED this round (a score of 0 is a
    legitimate played score); a key absent from it is DNP. `evidence` carries the transaction's
    store/board md5 before/after + txn id (from the applier result)."""
    round_n = int(round_n)
    prev_round = round_n - 1
    played = played or {}
    ing = os.path.join(repo_root, 'engine', 'rl_after', 'ingestion')
    vh = _load(os.path.join(ing, 'value_history.json'))
    rh = _load(os.path.join(ing, 'rank_history.json'))
    ph = _load(os.path.join(ing, 'pos_rank_history.json'))
    board = _load(os.path.join(repo_root, 'data', 'rl_build', 'rl_app_data.json'))
    boot = _boot(repo_root)
    store_rows = _load(os.path.join(repo_root, 'engine', 'rl_after', 'rl_model_data.json'))
    affl_by_key = {r.get('key'): r.get('affl_team') for r in store_rows if r.get('key')}
    club_by_key = {r.get('key'): r.get('afl_club') for r in store_rows if r.get('key')}

    active = board['active'] if isinstance(board, dict) else board
    season = int(vh.get('season', 2026))

    def by_round(hist, key, rnd):
        return (hist.get('players', {}).get(key, {}).get('by_round', {}) or {}).get(str(int(rnd)))

    players = []
    for p in active:
        key = p.get('key')
        if not key:
            continue
        pv = by_round(vh, key, prev_round)
        cv = by_round(vh, key, round_n)
        pr = by_round(rh, key, prev_round)
        cr = by_round(rh, key, round_n)
        pp = by_round(ph, key, prev_round)
        cp = by_round(ph, key, round_n)
        dv = (cv - pv) if (cv is not None and pv is not None) else None
        dvp = (round(dv / pv * 100.0, 2) if (dv is not None and pv not in (None, 0)) else None)
        drank = (pr - cr) if (pr is not None and cr is not None) else None      # +ve == improved
        dpos = (pp - cp) if (pp is not None and cp is not None) else None       # +ve == improved
        did_play = key in played
        players.append({
            # `club` is the AFL club (where the player actually plays); `affl_team` is the AFFL
            # ownership/fantasy team — distinct concepts, both carried so the UI never conflates them.
            'key': key, 'name': p.get('name'), 'club': club_by_key.get(key) or p.get('club'),
            'affl_team': affl_by_key.get(key), 'pos': _label_pos(p.get('grp') or p.get('gf')),
            'posCode': p.get('grp') or p.get('gf'),
            'previous_round': prev_round, 'current_round': round_n,
            'played': did_play, 'dnp': not did_play,
            'score': (played.get(key) if did_play else None),
            'prev_value': pv, 'cur_value': cv, 'value_change': dv, 'value_change_pct': dvp,
            'prev_rank': pr, 'cur_rank': cr, 'rank_change': drank,
            'prev_pos_rank': pp, 'cur_pos_rank': cp, 'pos_rank_change': dpos,
        })

    def rank_view(field, reverse):
        # deterministic tie-break: primary field, then cur_value desc, then key asc
        elig = [p for p in players if p.get(field) is not None]
        if reverse:  # descending primary; secondary cur_value desc; tertiary key asc
            elig.sort(key=lambda p: (-p[field], -(p['cur_value'] if p['cur_value'] is not None else -1e18), p['key']))
        else:
            elig.sort(key=lambda p: (p[field], -(p['cur_value'] if p['cur_value'] is not None else -1e18), p['key']))
        return [p['key'] for p in elig]

    views = {
        'value_risers': rank_view('value_change', True)[:50],
        'value_fallers': rank_view('value_change', False)[:50],
        'rank_risers': rank_view('rank_change', True)[:50],
        'rank_fallers': rank_view('rank_change', False)[:50],
        'played_count': sum(1 for p in players if p['played']),
        'dnp_count': sum(1 for p in players if p['dnp']),
    }

    ev = evidence or {}
    board_after = ev.get('board_md5_after')
    report = {
        'kind': 'weekly_movers_report', 'schema_version': SCHEMA_VERSION,
        'season': season, 'submitted_round': round_n, 'previous_round': prev_round,
        'source_store_md5_before': ev.get('store_md5_before'), 'source_store_md5_after': ev.get('store_md5_after'),
        'board_md5_before': ev.get('board_md5_before'), 'board_md5_after': board_after,
        'txn_id': ev.get('txn_id'), 'generated_at': generated_at, 'player_count': len(players),
        'release_identity': release_identity(repo_root, round_n, boot=boot),
        'integrity': {
            'players_unique': len({p['key'] for p in players}) == len(players),
            'coverage_full': len(players) == len([p for p in active if p.get('key')]),
            'board_after_matches_committed': board_after == _md5(
                os.path.join(repo_root, 'data', 'rl_build', 'rl_app_data.json')),
        },
        'views': views, 'players': players,
    }
    return report


# ---- CSV ------------------------------------------------------------------------------------------
_CSV_FIELDS = ['key', 'name', 'club', 'affl_team', 'pos', 'previous_round', 'current_round',
               'played', 'score', 'prev_value', 'cur_value', 'value_change', 'value_change_pct',
               'prev_rank', 'cur_rank', 'rank_change', 'prev_pos_rank', 'cur_pos_rank', 'pos_rank_change']


def report_csv(report):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=_CSV_FIELDS, extrasaction='ignore')
    w.writeheader()
    for p in report['players']:
        row = dict(p)
        row['played'] = 'PLAYED' if p['played'] else 'DNP'
        row['score'] = ('DNP' if not p['played'] else p['score'])
        w.writerow(row)
    return buf.getvalue()


# ---- the accumulated UI bundle (window.__MATCHDAY_MOVERS__) ---------------------------------------
def empty_bundle(repo_root, *, as_of_round=BASELINE_ROUND):
    """A clean, EMPTY initial movers bundle: schema + release-baseline block only, NO round reports.

    This is what the production ui/data/movers.js SHIPS as until real scoring is owner-applied. A fresh
    checkout at the baseline round therefore has no finalized round reports, and the Movers view renders
    an HONEST empty state (not an integrity alarm, not scratch data). The baseline block records the
    release identity the app runs on so the UI can anchor lineage the moment a first real round lands."""
    boot = _boot(repo_root)
    return {
        'kind': 'matchday_movers_bundle', 'schema_version': SCHEMA_VERSION,
        'rounds': [], 'reports': {},
        'baseline': {
            'as_of_round': int(as_of_round),
            'board': boot.get('board'), 'store': boot.get('store'),
            'release_identity': release_identity(repo_root, as_of_round, boot=boot),
            'note': 'Empty initial bundle — no finalized round reports. The Movers view is unavailable '
                    '(honest empty state) until a real round is applied and finalized by the owner.',
        },
        'integrity': {'board_chain_ok': True, 'baseline_anchor_ok': True, 'rounds': []},
    }


def write_bundle(path, bundle):
    """Serialize a movers bundle to `window.__MATCHDAY_MOVERS__ = {...};` (deterministic, compact)."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w') as f:
        f.write('// GENERATED — Matchday movers bundle (weekly movers reports, one per committed round).\n')
        f.write('// Ships EMPTY until real scoring is owner-applied; regenerate via '
                'engine/rl_after/ingestion/round_movers.py / round_finalize.py. Do not hand-edit.\n')
        f.write('window.__MATCHDAY_MOVERS__ = ')
        json.dump(bundle, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
    return path


def init_empty_bundle(path, repo_root, *, as_of_round=BASELINE_ROUND):
    """Write (or reset) the production bundle to the clean empty initial bundle."""
    return write_bundle(path, empty_bundle(repo_root, as_of_round=as_of_round))


def load_bundle(path, repo_root=None):
    """Parse the `window.__MATCHDAY_MOVERS__ = {...};` bundle, or a fresh empty bundle. When `repo_root`
    is given, a missing bundle is seeded with the release-baseline block; otherwise a bare empty."""
    if not os.path.exists(path):
        if repo_root:
            return empty_bundle(repo_root)
        return {'kind': 'matchday_movers_bundle', 'schema_version': SCHEMA_VERSION, 'rounds': [], 'reports': {}}
    with open(path) as f:
        text = f.read()
    i, j = text.index('{'), text.rindex('}')
    return json.loads(text[i:j + 1])


def accumulate_bundle(path, report, repo_root=None):
    """Add/replace this round's report in the UI bundle. A round already present is only replaced when
    its board_md5_after MATCHES (idempotent re-emit); a DIFFERENT board for the same round is an
    integrity break — kept as a flag, never a silent overwrite of history.

    The bundle carries a release-baseline block; the board-identity chain must (a) begin at the
    baseline board and (b) be continuous (report[n].board_md5_before == report[n-1].board_md5_after).
    Returns {'path', 'overwrite_conflict', 'chain_ok', 'baseline_anchor_ok'}."""
    existed = os.path.exists(path)
    # A pre-seeded bundle (as production ships) carries the board-of-record baseline; only when NO
    # bundle exists do we lazily create one — and then the baseline is the FIRST round's PRE-apply
    # board (the board the app was at before any round), NOT the manifest (which has already moved to
    # the just-committed board by the time finalization runs).
    bundle = load_bundle(path, repo_root=None) if not existed else load_bundle(path, repo_root=repo_root)
    rnd = str(report['submitted_round'])
    reports = bundle.setdefault('reports', {})
    prior = reports.get(rnd)
    overwrite_conflict = bool(prior and prior.get('board_md5_after') != report['board_md5_after'])
    reports[rnd] = report
    bundle['rounds'] = sorted(int(r) for r in reports)
    if not bundle.get('baseline'):
        first = reports[str(bundle['rounds'][0])]
        bundle['baseline'] = {'as_of_round': first.get('previous_round'),
                              'board': first.get('board_md5_before'),
                              'store': first.get('source_store_md5_before'),
                              'release_identity': first.get('release_identity')}
    baseline = bundle.get('baseline') or {}
    base_board = baseline.get('board')
    # board-identity chain: report[n].board_md5_before must equal report[n-1].board_md5_after,
    # and the FIRST report must attach to the release baseline board.
    chain_ok = True
    baseline_anchor_ok = True
    for idx, r in enumerate(bundle['rounds']):
        rep = reports[str(r)]
        prevr = reports.get(str(r - 1))
        if prevr and rep.get('board_md5_before') and rep['board_md5_before'] != prevr.get('board_md5_after'):
            chain_ok = False
        if idx == 0 and base_board and rep.get('board_md5_before') and rep['board_md5_before'] != base_board:
            baseline_anchor_ok = False
    bundle['integrity'] = {'board_chain_ok': chain_ok, 'baseline_anchor_ok': baseline_anchor_ok,
                           'overwrite_conflict_last_write': overwrite_conflict,
                           'rounds': bundle['rounds']}
    write_bundle(path, bundle)
    return {'path': path, 'overwrite_conflict': overwrite_conflict,
            'chain_ok': chain_ok, 'baseline_anchor_ok': baseline_anchor_ok}


def inject_working(path, report):
    """Augment board_view_working.js in place with dRound/dRoundRank/dRoundPosRank per row. Returns the
    number of rows injected."""
    with open(path) as f:
        text = f.read()
    i, j = text.index('{'), text.rindex('}')
    prefix, obj, suffix = text[:i], json.loads(text[i:j + 1]), text[j + 1:]
    by_key = {p['key']: p for p in report['players']}
    injected = 0
    for row in obj.get('players', []):
        mv = by_key.get(row.get('key'))
        if mv:
            row['dRound'] = mv['value_change']
            row['dRoundRank'] = mv['rank_change']
            row['dRoundPosRank'] = mv['pos_rank_change']
            injected += 1
    with open(path, 'w') as f:
        f.write(prefix)
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
        f.write(suffix)
    return injected


# ---- per-round report files -----------------------------------------------------------------------
def movers_paths(repo_root, round_n, movers_dir=None):
    ing = os.path.join(repo_root, 'engine', 'rl_after', 'ingestion')
    movers_dir = movers_dir or os.path.join(ing, 'movers')
    return (os.path.join(movers_dir, 'movers_R%d.json' % int(round_n)),
            os.path.join(movers_dir, 'movers_R%d.csv' % int(round_n)), movers_dir)


def write_report_json(repo_root, round_n, report, movers_dir=None):
    jpath, _cpath, mdir = movers_paths(repo_root, round_n, movers_dir)
    os.makedirs(mdir, exist_ok=True)
    RH.save_json_atomic(jpath, RH.report_bytes(report))
    return jpath


def write_report_csv(repo_root, round_n, report, movers_dir=None):
    _jpath, cpath, mdir = movers_paths(repo_root, round_n, movers_dir)
    os.makedirs(mdir, exist_ok=True)
    with open(cpath, 'w') as f:
        f.write(report_csv(report))
    return cpath


# ---- emit (single-shot; used by the finalizer's happy path + legacy callers) ----------------------
def emit(repo_root, round_n, *, played=None, evidence=None, generated_at=None,
         movers_dir=None, ui_data_dir=None):
    """Build + persist the round's movers report in one shot: JSON + CSV under movers/, the accumulated
    UI bundle under ui/data/movers.js (never silently overwriting a DIFFERENT prior report), and the
    dRound/dRoundRank/dRoundPosRank injection into the working UI bundle. Returns an evidence dict.

    The FINALIZATION phase (round_finalize.py) drives these same primitives step-by-step so a failure
    can be journaled between any two writes; `emit` is the equivalent single call for the happy path."""
    report = build_report(repo_root, round_n, played=played, evidence=evidence, generated_at=generated_at)
    jpath = write_report_json(repo_root, round_n, report, movers_dir)
    cpath = write_report_csv(repo_root, round_n, report, movers_dir)

    ui_data_dir = ui_data_dir or os.path.join(repo_root, 'ui', 'data')
    bundle_path = os.path.join(ui_data_dir, 'movers.js')
    bundle_res = None
    if os.path.isdir(ui_data_dir):
        bundle_res = accumulate_bundle(bundle_path, report, repo_root=repo_root)

    working = os.path.join(ui_data_dir, 'board_view_working.js')
    injected = inject_working(working, report) if os.path.exists(working) else 0

    return {'round': int(round_n), 'movers_json': jpath, 'movers_csv': cpath,
            'ui_bundle': (bundle_res or {}).get('path'),
            'bundle_chain_ok': (bundle_res or {}).get('chain_ok'),
            'bundle_baseline_anchor_ok': (bundle_res or {}).get('baseline_anchor_ok'),
            'bundle_overwrite_conflict': (bundle_res or {}).get('overwrite_conflict'),
            'ui_rows_injected': injected,
            'player_count': report['player_count'], 'played': report['views']['played_count'],
            'dnp': report['views']['dnp_count'], 'board_md5_after': report['board_md5_after']}
