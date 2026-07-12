"""SCORE INGESTOR — parse -> resolve -> aggregate -> VALIDATED PREVIEW. APPLY GATED OFF.

The pipeline for the owner's weekly round-score feed, PROVISION ONLY:

    rows = parse_feed(text)                      # round_score_parser
    preview = ScoreIngestor().preview(rows)      # resolve + aggregate + anomaly-check
    # preview.appends     : the exact `scoring` season appends it WOULD make (a DIFF artifact)
    # preview.exceptions  : names that FAILED to resolve — never guessed, never fuzzy-attached
    # preview.anomalies   : resolved-but-suspicious rows (duplicate round / impossible score /
    #                       retired / cycle-year) — FLAGGED, never silently dropped
    ScoreIngestor().apply(preview)               # RAISES IngestionGatedError — switch is OFF

SSI-safe: the preview is a diff, NOT a store and NOT a store copy. This module writes NOTHING to
`rl_model_data.json`. The store-write path is deliberately absent (see `apply`); implementing it
AND flipping the switch is a future owner-worded go-live job — docs/GO_LIVE_round_score_ingestion.md.

SCOPE: identity boundary + aggregation + validation only. No valuation, no board math, no pricing.
"""
import json, os

try:
    from .round_score_parser import RoundScore, parse_feed  # noqa: F401 (re-exported convenience)
except (ImportError, ValueError):        # allow direct-script / non-package execution
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from round_score_parser import RoundScore, parse_feed   # type: ignore  # noqa: F401

# id_resolver lives beside this package (engine/rl_after/id_resolver.py) — the score boundary.
try:
    from ..id_resolver import IdResolver, RESOLVED, BY_KEY, NO_ID, AMBIGUOUS, UNRESOLVED
except (ImportError, ValueError):        # allow direct-script / non-package execution
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from id_resolver import IdResolver, RESOLVED, BY_KEY, NO_ID, AMBIGUOUS, UNRESOLVED  # type: ignore

_STORE_DEFAULT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'rl_model_data.json')

# ---- CONFIG (documented; confirmed with the owner at go-live) ------------------------------
DEFAULT_SEASON_YEAR = 2026        # the live season; == rl_model.py BASE_REF (rl_model.py:57)
ROUND_DECIMALS = 2                # store `avg` precision (verified: every stored avg == round(avg,2))
DEFAULT_SCORE_BOUNDS = (-100.0, 400.0)   # a PLAYED round outside this band is an impossible-score anomaly

# ---- THE HARD APPLY SWITCH (env + code, default OFF) ---------------------------------------
APPLY_DEFAULT = False                     # code half of the switch — MUST stay False in this job
_APPLY_ENV = 'INGEST_SCORE_APPLY'         # env half — unset by default; owner-worded token at go-live


class IngestionGatedError(RuntimeError):
    """Raised by apply() while the ingestion switch is OFF (the default, this whole job)."""


def _apply_enabled():
    """Both halves must be on: the code default AND an explicit env opt-in. Default => OFF."""
    return bool(APPLY_DEFAULT) and bool(os.environ.get(_APPLY_ENV))


# ---- identity/eligibility helpers (pure; mirror rl_model, NO valuation) --------------------
def _debut_year(row):
    """Season a player first plays. ONLY MSD (mid-season) debuts in its draft year; every other
    entry type debuts the following season. Mirrors rl_model.py:63 (identity, not pricing)."""
    return row['year'] if row.get('type') == 'MSD' else row.get('year', 0) + 1


# ---- artifact records ----------------------------------------------------------------------
class Exception_:
    """A feed row whose IDENTITY could not be resolved to a stable id — FAILS LOUDLY here."""
    __slots__ = ('player', 'club', 'reason', 'status', 'candidates', 'source_refs')

    def __init__(self, player, club, reason, status, candidates=None, source_refs=None):
        self.player = player
        self.club = club
        self.reason = reason                 # 'unresolved' | 'ambiguous' | 'no_stable_id'
        self.status = status                 # the raw resolver status
        self.candidates = candidates or []   # [(key, stable_player_id, affl_team)] when ambiguous
        self.source_refs = source_refs or []

    def as_dict(self):
        return {'player': self.player, 'club': self.club, 'reason': self.reason,
                'status': self.status, 'candidates': self.candidates,
                'source_refs': self.source_refs}


class Anomaly:
    """A resolved row that is suspicious — FLAGGED for owner review, never silently dropped."""
    __slots__ = ('stable_player_id', 'key', 'player', 'kind', 'detail')

    def __init__(self, stable_player_id, key, player, kind, detail):
        self.stable_player_id = stable_player_id
        self.key = key
        self.player = player
        self.kind = kind                     # 'duplicate_round'|'impossible_score'|'retired'|'cycle_year'
        self.detail = detail

    def as_dict(self):
        return {'stable_player_id': self.stable_player_id, 'key': self.key, 'player': self.player,
                'kind': self.kind, 'detail': self.detail}


class SeasonAppend:
    """The exact `scoring` season-entry append the pipeline WOULD make for one player, as a DIFF."""
    __slots__ = ('stable_player_id', 'key', 'player', 'year', 'before',
                 'batch_entry', 'merged_entry', 'rounds', 'anomalies')

    def __init__(self, stable_player_id, key, player, year, before, batch_entry, merged_entry,
                 rounds, anomalies):
        self.stable_player_id = stable_player_id
        self.key = key
        self.player = player
        self.year = year
        self.before = before                 # current store season entry {year,avg,games} or None
        self.batch_entry = batch_entry       # season entry implied by THIS batch alone
        self.merged_entry = merged_entry     # batch merged onto `before` (the weekly go-live append)
        self.rounds = rounds                 # [(round, score, played)] contributing rows
        self.anomalies = anomalies           # list[Anomaly] attached to this player

    def as_dict(self):
        return {'stable_player_id': self.stable_player_id, 'key': self.key, 'player': self.player,
                'year': self.year, 'before': self.before, 'batch_entry': self.batch_entry,
                'merged_entry': self.merged_entry, 'rounds': self.rounds,
                'anomalies': [a.as_dict() for a in self.anomalies]}


class IngestionPreview:
    """The validated preview artifact: appends + exceptions + anomalies. A DIFF, not a store."""
    __slots__ = ('season_year', 'appends', 'exceptions', 'anomalies', 'store_md5')

    def __init__(self, season_year, appends, exceptions, anomalies, store_md5=None):
        self.season_year = season_year
        self.appends = appends
        self.exceptions = exceptions
        self.anomalies = anomalies
        self.store_md5 = store_md5

    @property
    def clean(self):
        """True iff every row resolved (no exceptions) and nothing tripped an anomaly."""
        return not self.exceptions and not self.anomalies

    def summary(self):
        return {'season_year': self.season_year, 'appends': len(self.appends),
                'exceptions': len(self.exceptions), 'anomalies': len(self.anomalies),
                'clean': self.clean, 'store_md5': self.store_md5}

    def as_dict(self):
        return {'season_year': self.season_year, 'store_md5': self.store_md5,
                'summary': self.summary(),
                'appends': [a.as_dict() for a in self.appends],
                'exceptions': [e.as_dict() for e in self.exceptions],
                'anomalies': [a.as_dict() for a in self.anomalies]}


# ---- the ingestor --------------------------------------------------------------------------
class ScoreIngestor:
    def __init__(self, store=None, store_path=None, resolver=None,
                 round_decimals=ROUND_DECIMALS, score_bounds=DEFAULT_SCORE_BOUNDS):
        if store is None:
            store = json.load(open(store_path or _STORE_DEFAULT))
        self._store = store
        self._resolver = resolver or IdResolver(store=store)
        self._key_to_row = {r['key']: r for r in store if r.get('key')}
        self.round_decimals = round_decimals
        self.score_bounds = score_bounds

    # -- current store season entry for (key, year), read-only -------------------------------
    def _before_entry(self, key, year):
        row = self._key_to_row.get(key)
        if not row:
            return None
        for s in (row.get('scoring') or []):
            if s.get('year') == year:
                return {'year': s['year'], 'avg': s['avg'], 'games': s['games']}
        return None

    def _mean(self, total, n):
        return round(total / n, self.round_decimals) if n else None

    # -- PREVIEW: parse output -> resolved appends + exceptions + anomalies -------------------
    def preview(self, rows, season_year=DEFAULT_SEASON_YEAR, merge_with_store=True):
        # 1) resolve each row; group the resolved ones by key, collect exceptions for the rest.
        grouped = {}                     # key -> {'row':store_row,'sid':..,'player':..,'rounds':[...]}
        exc_by_sig = {}                  # (player_norm, reason) -> Exception_ (dedup across rounds)
        for rs in rows:
            res = self._resolver.resolve(name=rs.player, club=rs.club)
            if res.status in (RESOLVED, BY_KEY) and res.stable_player_id:
                g = grouped.get(res.key)
                if g is None:
                    row = self._key_to_row.get(res.key, {})
                    g = grouped[res.key] = {'row': row, 'sid': res.stable_player_id,
                                            'player': row.get('player', rs.player), 'rounds': []}
                g['rounds'].append(rs)
            else:
                reason = {NO_ID: 'no_stable_id', AMBIGUOUS: 'ambiguous',
                          UNRESOLVED: 'unresolved'}.get(res.status, 'unresolved')
                sig = (rs.player.lower(), reason)
                e = exc_by_sig.get(sig)
                if e is None:
                    e = exc_by_sig[sig] = Exception_(rs.player, rs.club, reason, res.status,
                                                     candidates=list(res.candidates))
                e.source_refs.append(rs.source_ref)

        # 2) aggregate each resolved player's batch into a season append + anomaly checks.
        appends, all_anoms = [], []
        for key, g in grouped.items():
            row, sid, player, rlist = g['row'], g['sid'], g['player'], g['rounds']
            played = [r for r in rlist if r.played]
            n = len(played)
            total = sum(r.score for r in played) if n else 0.0
            batch_entry = {'year': season_year, 'avg': self._mean(total, n), 'games': n}

            before = self._before_entry(key, season_year)
            if not merge_with_store or before is None:
                merged_entry = dict(batch_entry)
            else:
                mg = before['games'] + n
                mtotal = before['avg'] * before['games'] + total
                merged_entry = {'year': season_year, 'avg': self._mean(mtotal, mg), 'games': mg}

            anoms = self._anomalies(sid, key, player, row, season_year, rlist)
            all_anoms.extend(anoms)
            appends.append(SeasonAppend(
                sid, key, player, season_year, before, batch_entry, merged_entry,
                rounds=[(r.round, r.score, r.played) for r in sorted(rlist, key=lambda x: x.round)],
                anomalies=anoms))

        appends.sort(key=lambda a: a.key)
        exceptions = sorted(exc_by_sig.values(), key=lambda e: (e.reason, e.player.lower()))
        store_md5 = _md5_of(_STORE_DEFAULT)
        return IngestionPreview(season_year, appends, exceptions, all_anoms, store_md5)

    # -- anomaly checks (flag, never drop) ---------------------------------------------------
    def _anomalies(self, sid, key, player, row, season_year, rlist):
        out = []
        # duplicate round: same round appears more than once in the batch for this player.
        seen = {}
        for r in rlist:
            seen[r.round] = seen.get(r.round, 0) + 1
        dups = sorted(rnd for rnd, c in seen.items() if c > 1)
        if dups:
            out.append(Anomaly(sid, key, player, 'duplicate_round',
                               "round(s) %s appear more than once in the feed" % dups))
        # impossible score: a PLAYED round outside the sane band.
        lo, hi = self.score_bounds
        bad = [(r.round, r.score) for r in rlist if r.played and not (lo <= r.score <= hi)]
        if bad:
            out.append(Anomaly(sid, key, player, 'impossible_score',
                               "score(s) outside [%s,%s]: %s" % (lo, hi, bad)))
        # retired / out-of-universe: resolved row is a retiree (or carries no live identity).
        if row.get('_retired'):
            out.append(Anomaly(sid, key, player, 'retired',
                               "resolved row is marked _retired — scores for a retired player"))
        # cycle-year sanity (item 13): the season must be >= the player's debut year.
        d = _debut_year(row) if row else None
        if d is not None and season_year < d:
            out.append(Anomaly(sid, key, player, 'cycle_year',
                               "season %s precedes debut year %s (cannot have played)"
                               % (season_year, d)))
        return out

    # -- APPLY: HARD-GATED OFF. No store write exists in this job. ---------------------------
    def apply(self, preview):
        """Would apply the preview's appends to the single source. GATED OFF for this whole job.

        The switch has two halves (code APPLY_DEFAULT + env INGEST_SCORE_APPLY), both default OFF,
        so this raises IngestionGatedError. The store-write itself is DELIBERATELY NOT IMPLEMENTED
        here — even a flipped switch cannot write, because there is no write code. Building the
        write AND flipping the switch is the future owner-worded go-live job.
        See docs/GO_LIVE_round_score_ingestion.md.
        """
        if not _apply_enabled():
            raise IngestionGatedError(
                "round-score APPLY is OFF (APPLY_DEFAULT=%s, env %s unset). This provision job "
                "writes nothing to the store; go-live is a separate owner-worded job."
                % (APPLY_DEFAULT, _APPLY_ENV))
        raise NotImplementedError(
            "the store-write path is intentionally absent from the provision job — implementing "
            "it behind this switch is the go-live job (docs/GO_LIVE_round_score_ingestion.md).")


def _md5_of(path):
    import hashlib
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    except OSError:
        return None
