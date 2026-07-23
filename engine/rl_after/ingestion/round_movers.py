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
import hashlib
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


# ---- canonical content digest of a set of movers reports -------------------------------------------
# The provenance transition (data/release_lineage.json `release_transition` + ui/data/movers_transition.js,
# validated in ui/app/movers.js `core`) anchors the historical R15-R19 reports by a SHA-256 over a
# CANONICAL serialization of exactly those reports, so ANY modification of a report — an identity field
# OR a player's movement value — is detected and fails closed. The canonicalization mirrors the browser
# validator's JS `JSON.stringify` semantics EXACTLY (recursively key-sorted; integral floats emitted as
# integers, e.g. 59.0 -> "59", as JS does) so the Python emitter and the browser/node validator compute
# the IDENTICAL digest for the same reports. This is verified cross-language by test_movers_transition.py.
def _js_number(x):
    """Render a number as JS `JSON.stringify` does (an integral float loses its `.0`)."""
    if isinstance(x, bool):
        return 'true' if x else 'false'
    if isinstance(x, int):
        return str(x)
    f = float(x)
    if f == int(f) and abs(f) < 1e16:
        return str(int(f))
    return repr(f)


def _js_canon(v):
    """Deterministic canonical JSON matching the browser validator's `core.canonJSON`."""
    if v is None:
        return 'null'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return _js_number(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return '[' + ','.join(_js_canon(e) for e in v) + ']'
    if isinstance(v, dict):
        return '{' + ','.join(json.dumps(k, ensure_ascii=False) + ':' + _js_canon(v[k])
                              for k in sorted(v.keys())) + '}'
    raise TypeError('non-canonicalizable %r' % type(v))


def canonical_reports_digest(bundle, rounds):
    """`sha256:<hex>` over the canonical form of exactly {str(round): report} for `rounds`. Byte-for-byte
    equal to the browser/node validator's `core.reportsDigest(bundle, rounds)`."""
    reports = (bundle or {}).get('reports', {}) or {}
    subset = {str(r): reports.get(str(r)) for r in rounds}
    return 'sha256:' + hashlib.sha256(_js_canon(subset).encode('utf-8')).hexdigest()


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


def _release_baseline(repo_root):
    """The IMMUTABLE release-baseline identity (owner ruling 2026-07-20): release_version +
    balanced_board_md5. Read from data/release_lineage.json — a permanent PRESENT-LENS baseline that is
    NEVER synthesized from the weekly board, NEVER re-stamped by a weekly score transaction, and NOT
    assumed to be the final complete board-file hash (Leg E/F forward-lens acceptance + final full-board
    pinning are external dependencies). Absent file is a hard error; the RC manifest supersedes it on
    integration."""
    p = os.path.join(repo_root, 'data', 'release_lineage.json')
    lin = _load(p)
    bb = lin.get('balanced_board_md5')
    if not bb or not lin.get('release_version'):
        raise ValueError('release_lineage.json missing release_version / balanced_board_md5 at %s' % p)
    return {'release_version': lin['release_version'], 'balanced_board_md5': bb}


# release identity = FIXED baseline (release_version, balanced_board_md5 — immutable, from
# release_lineage.json) + FIXED model pins (engine_head/rl_model/fv/config/register — from the boot
# manifest, which a weekly round never re-stamps) + DYNAMIC weekly fields (board, store — re-stamped
# each round; as_of_round — this round). The two field classes are validated differently by the UI
# lineage check (fixed must equal the loaded release; dynamic latest must equal the loaded current).
RELEASE_FIXED_FIELDS = ('release_version', 'balanced_board_md5', 'engine_head', 'rl_model', 'fv',
                        'config', 'register')
RELEASE_DYNAMIC_FIELDS = ('board', 'store', 'as_of_round')


def release_identity(repo_root, round_n, boot=None):
    """Build a report's release identity: the FIXED baseline (release_version + balanced_board_md5 from
    release_lineage.json) + the FIXED model pins (from expected_boot.json) + the DYNAMIC weekly fields
    (current board + store from expected_boot, and this round as as_of_round).

    balanced_board_md5 is the immutable accepted PRESENT-LENS baseline identity — copied verbatim,
    NEVER synthesized from the weekly `board`, and NOT assumed to be the final complete board-file hash
    (Leg E/F forward-lens acceptance + final full-board pinning are external dependencies). The DYNAMIC
    `board` field is the complete CURRENT board artifact. as_of_round tracks the applied round (15 after
    R15, never left at 14). A historical report keeps its own frozen governing identity."""
    boot = boot if boot is not None else _boot(repo_root)
    base = _release_baseline(repo_root)
    return {
        # FIXED release-baseline identity (immutable across weekly rounds)
        'release_version': base['release_version'],
        'balanced_board_md5': base['balanced_board_md5'],   # permanent PRESENT-LENS baseline; not synthesized
        # FIXED model pins (the boot manifest; a weekly round merges scores, never the model)
        'engine_head': boot.get('engine_head'),
        'rl_model': boot.get('rl_model'),
        'fv': boot.get('fv'),
        'config': boot.get('config'),
        'register': boot.get('register'),
        # DYNAMIC weekly fields
        'board': boot.get('board'),
        'store': boot.get('store'),
        'as_of_round': int(round_n),
        'manifest_source': 'data/expected_boot.json + data/release_lineage.json',
    }


def frozen_release_identity(repo_root, round_n, board_md5, store_md5, boot=None):
    """The release identity a round is FROZEN to for durable storage + historical repair. Same as
    release_identity, but the DYNAMIC board/store are the round's OWN committed ids (from the
    transaction evidence) rather than the current (possibly later-moved) manifest — so repairing R15
    after R19 reproduces R15's exact identity. The FIXED baseline + model pins are immutable across
    weekly rounds, so reading the model pins from the current manifest is historical-safe."""
    rel = release_identity(repo_root, round_n, boot=boot)
    rel['board'] = board_md5
    rel['store'] = store_md5
    return rel


# ---- UI release contract: the FULL release identity the browser validates lineage against ----------
WORKING_BUNDLE_NAME = 'board_view_working.js'


def inject_release_contract(working_path, repo_root, as_of_round):
    """Augment the working board bundle's stamp with the FULL release identity (`stamp.release`), so
    the browser validates movers lineage against verified full-length pins rather than the abbreviated
    stamp fields. Idempotent. Returns the injected release identity (or None if the bundle is absent)."""
    if not os.path.exists(working_path):
        return None
    rel = release_identity(repo_root, as_of_round)
    with open(working_path) as f:
        text = f.read()
    i, j = text.index('{'), text.rindex('}')
    prefix, obj, suffix = text[:i], json.loads(text[i:j + 1]), text[j + 1:]
    stamp = obj.setdefault('stamp', {})
    stamp['release'] = rel
    with open(working_path, 'w') as f:
        f.write(prefix)
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
        f.write(suffix)
    return rel


# ---- the report -----------------------------------------------------------------------------------
def build_report(repo_root, round_n, *, played=None, evidence=None, generated_at=None,
                 release_identity_override=None):
    """Build the full movers report for a committed round from the two committed boards (via histories).

    `played` maps stable key -> submitted score for players LISTED this round (a score of 0 is a
    legitimate played score); a key absent from it is DNP. `evidence` carries the transaction's
    store/board md5 before/after + txn id (from the applier result). `release_identity_override`, when
    given, is the round's FROZEN governing identity (used by a historical repair so the rebuilt report
    keeps its original release/board/store identity instead of the current manifest's)."""
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

    # DETERMINISTIC player order (sorted by stable key), INDEPENDENT of the current board's `active`
    # array order — so a historical repair (which reads a LATER board's roster) reproduces a round's
    # report BYTE-FOR-BYTE, and the report never depends on incidental board ordering.
    players.sort(key=lambda p: p['key'] or '')

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
        'release_identity': (release_identity_override
                             if release_identity_override is not None
                             else release_identity(repo_root, round_n, boot=boot)),
        'integrity': {
            'players_unique': len({p['key'] for p in players}) == len(players),
            'coverage_full': len(players) == len([p for p in active if p.get('key')]),
            # the report carries the round's committed board id (from the transaction evidence). This is
            # a report-level presence check; the STRONG board-matching integrity (report board == the
            # round's committed board; latest report board == the loaded current board) is enforced by
            # round_finalize._validate_derivatives + the UI lineage check. Deliberately NOT compared
            # against the mutable on-disk board, so a HISTORICAL repair reproduces the report byte-for-
            # byte (the current board has legitimately moved on to a later round by repair time).
            'board_after_matches_committed': board_after is not None,
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
def _ui_working_stamp(repo_root):
    """The board/store the LOADED Matchday app is actually on, from ui/data/board_view_working.js's
    stamp (the app ring-fences a specific board id). Returns {'board','store'} or None if absent."""
    p = os.path.join(repo_root, 'ui', 'data', 'board_view_working.js')
    if not os.path.exists(p):
        return None
    try:
        with open(p) as f:
            text = f.read()
        obj = json.loads(text[text.index('{'):text.rindex('}') + 1])
        st = obj.get('stamp') or {}
        return {'board': st.get('srcmd5') or st.get('board'), 'store': st.get('store')}
    except (OSError, ValueError):
        return None


def empty_bundle(repo_root, *, as_of_round=BASELINE_ROUND):
    """A clean, EMPTY initial movers bundle: schema + release-baseline block only, NO round reports.

    This is what the production ui/data/movers.js SHIPS as until real scoring is owner-applied. A fresh
    checkout at the baseline round therefore has no finalized round reports, and the Movers view renders
    an HONEST empty state (not an integrity alarm, not scratch data). The baseline is anchored GENERICALLY
    to the board/store the LOADED app is actually on (board_view_working.js — the app ring-fences a
    specific board id), falling back to the engine board-of-record (expected_boot) when the UI bundle is
    absent (e.g. a fresh scratch, whose UI is generated from the engine board on the first refresh). This
    keeps the shipped empty state coherent with the app WITHOUT assuming any final board/switch posture."""
    boot = _boot(repo_root)
    rel = release_identity(repo_root, as_of_round, boot=boot)
    stamp = _ui_working_stamp(repo_root)
    base_board = (stamp or {}).get('board') or boot.get('board')
    base_store = (stamp or {}).get('store') or boot.get('store')
    rel = dict(rel); rel['board'] = base_board; rel['store'] = base_store   # baseline release is self-consistent
    return {
        'kind': 'matchday_movers_bundle', 'schema_version': SCHEMA_VERSION,
        'rounds': [], 'reports': {},
        'baseline': {
            'as_of_round': int(as_of_round),
            'board': base_board, 'store': base_store, 'release_identity': rel,
            'note': 'Empty initial bundle — no finalized round reports. The Movers view is unavailable '
                    '(honest empty state) until a real round is applied and finalized by the owner. The '
                    'baseline board/store are the LOADED app board (board_view_working.js), so the empty '
                    'state is validated against the app; the fixed release fields are provenance.',
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


# ---- conflict identity: the tuple that makes two same-round reports the SAME report ----------------
def report_identity(report):
    """The identity that distinguishes two reports for the same round: transaction id + committed
    board id + committed store id + submitted round. Two reports whose (COMPLETE) identities differ are
    a CONFLICT (never silently overwritten); identical identities are an idempotent regeneration."""
    r = (report or {}).get('submitted_round')
    return ((report or {}).get('txn_id'), (report or {}).get('board_md5_after'),
            (report or {}).get('source_store_md5_after'), (int(r) if r is not None else None))


def _identity_complete(ident):
    return all(x is not None for x in ident)


def movers_conflict(repo_root, round_n, report, *, movers_dir=None, bundle_path=None):
    """Inspect the EXISTING same-round artifacts (JSON report + accumulated bundle entry) BEFORE any
    write and report a conflict ONLY when an existing report has a VALID, COMPLETE identity (txn +
    board + store + round) that DIFFERS from `report`'s. On conflict the caller must write NOTHING
    (JSON, CSV or bundle) and leave every existing byte unchanged. A missing artifact (first write), an
    identical-identity artifact (idempotent regeneration), or a CORRUPT / incomplete artifact (which a
    repair is meant to rebuild) is NOT a conflict. Returns (conflict: bool, reason: str)."""
    want = report_identity(report)
    jpath, _cpath, _mdir = movers_paths(repo_root, round_n, movers_dir)
    if os.path.exists(jpath):
        try:
            with open(jpath) as f:
                existing = json.load(f)
        except (OSError, ValueError):
            existing = None                    # corrupt/unparseable -> a repair may rebuild it
        if existing is not None:
            eid = report_identity(existing)
            if _identity_complete(eid) and eid != want:
                return True, ('existing movers_R%d.json has a different valid identity (txn/board/store/'
                              'round) %s != %s' % (int(round_n), eid, want))
    bpath = bundle_path or os.path.join(repo_root, 'ui', 'data', 'movers.js')
    if os.path.exists(bpath):
        try:
            bundle = load_bundle(bpath)
        except (OSError, ValueError):
            bundle = None
        rep = (bundle or {}).get('reports', {}).get(str(int(round_n)))
        if rep:
            rid = report_identity(rep)
            if _identity_complete(rid) and rid != want:
                return True, ('bundle already holds R%d with a different valid identity %s != %s'
                              % (int(round_n), rid, want))
    return False, ''


def _baseline_release_identity_from_report(report):
    rel = dict((report or {}).get('release_identity') or {})
    rel['as_of_round'] = (report or {}).get('previous_round')
    rel['board'] = (report or {}).get('board_md5_before')
    rel['store'] = (report or {}).get('source_store_md5_before')
    return rel


def _baseline_from_report(report):
    return {'as_of_round': (report or {}).get('previous_round'),
            'board': (report or {}).get('board_md5_before'),
            'store': (report or {}).get('source_store_md5_before'),
            'release_identity': _baseline_release_identity_from_report(report)}


def accumulate_bundle(path, report, repo_root=None):
    """Add/replace this round's report in the UI bundle. A round already present with a DIFFERENT
    governing identity (txn/board/store/round) is a CONFLICT: the bundle is left BYTE-UNCHANGED (the
    report is NOT assigned and nothing is written), returning overwrite_conflict=True. A same-identity
    round is an idempotent replace.

    The bundle carries a release-baseline block; the board-identity chain must (a) begin at the
    baseline board and (b) be continuous (report[n].board_md5_before == report[n-1].board_md5_after).
    Returns {'path', 'overwrite_conflict', 'chain_ok', 'baseline_anchor_ok'}."""
    existed = os.path.exists(path)
    # A missing bundle or a pre-seeded ZERO-REPORT bundle is an unconsumed seed: when the first real
    # report is accumulated, anchor the immutable baseline to that report's ACTUAL pre-apply identity.
    # Once any report exists, the baseline is never re-anchored.
    bundle = load_bundle(path, repo_root=repo_root) if existed else load_bundle(path, repo_root=None)
    rnd = str(report['submitted_round'])
    reports = bundle.setdefault('reports', {})
    prior = reports.get(rnd)
    if prior:
        pid = report_identity(prior)
        if _identity_complete(pid) and pid != report_identity(report):
            # CONFLICT — do NOT assign reports[rnd]=report; do NOT write. Leave every existing byte intact.
            return {'path': path, 'overwrite_conflict': True, 'wrote': False,
                    'chain_ok': (bundle.get('integrity') or {}).get('board_chain_ok'),
                    'baseline_anchor_ok': (bundle.get('integrity') or {}).get('baseline_anchor_ok')}
    first_real_report = not reports
    reports[rnd] = report
    bundle['rounds'] = sorted(int(r) for r in reports)
    if first_real_report or not bundle.get('baseline'):
        first = reports[str(bundle['rounds'][0])]
        bundle['baseline'] = _baseline_from_report(first)
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
                           'overwrite_conflict_last_write': False, 'rounds': bundle['rounds']}
    write_bundle(path, bundle)
    return {'path': path, 'overwrite_conflict': False, 'wrote': True,
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
