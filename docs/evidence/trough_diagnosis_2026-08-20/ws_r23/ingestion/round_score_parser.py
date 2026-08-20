"""ROUND-SCORE PARSER — the owner's weekly score format -> validated rows.

FORMAT (directive step 1, four named fields): name . round . score . games flag.
Mapped to a canonical row:

    player   (str)         the player's name, as the owner writes it
    round    (int >= 1)    round number within the season
    score    (float|None)  that round's rating/fantasy score; meaningful only when played
    played   (bool)        the "games flag": True = played this round, False = named DNP
    club     (str|None)    OPTIONAL disambiguator; passed to the resolver as a veto, never a guess

Season YEAR is a pipeline context (default = BASE_REF, the live season), NOT a per-row field —
the weekly feed is implicitly the current season.

Accepted serializations (both discoverable from the four fields; exact on-disk form is confirmed
with the owner at go-live — see the runbook):
  * CSV  with a header row containing (case/space-insensitive) the columns above. The games flag
         accepts 1/0, true/false, yes/no, y/n, played/dnp (blank -> played iff a score is present).
  * JSON list of objects with the same keys (or a {"rows": [...]} envelope).

This module is PARSE-ONLY: it validates shape and types and normalizes the games flag. It does NOT
resolve names, does NOT touch the store, and does NOT price anyone. Bad rows raise ParseError with
the offending line/index so the feed fails LOUDLY rather than silently ingesting garbage.
"""
import csv, io, json


class ParseError(ValueError):
    """A weekly-feed row that cannot be parsed into a RoundScore (bad shape/type/flag)."""


class RoundScore:
    """One player's score for one round of one season (pre-resolution)."""
    __slots__ = ('player', 'round', 'score', 'played', 'club', 'source_ref')

    def __init__(self, player, round, score, played, club=None, source_ref=None):
        self.player = player
        self.round = round
        self.score = score
        self.played = played
        self.club = club
        self.source_ref = source_ref     # e.g. "row 4" / "csv line 5" — for loud error/exception messages

    def as_dict(self):
        return {'player': self.player, 'round': self.round, 'score': self.score,
                'played': self.played, 'club': self.club, 'source_ref': self.source_ref}

    def __repr__(self):
        return "RoundScore(%r r%s=%s played=%s%s)" % (
            self.player, self.round, self.score, self.played,
            " club=%r" % self.club if self.club else "")


# ---- games-flag normalization -------------------------------------------------------------
_TRUE = {'1', 'true', 't', 'yes', 'y', 'played', 'p', 'g'}
_FALSE = {'0', 'false', 'f', 'no', 'n', 'dnp', 'out', 'sit', 'sat', 'rest', 'rested'}


def _parse_flag(raw, has_score, ref):
    """Normalize the games flag to a bool. Blank -> played iff a score is present (a bare score row
    means the player played). Anything unrecognized fails loudly."""
    if raw is None:
        return has_score
    s = str(raw).strip().lower()
    if s == '':
        return has_score
    if s in _TRUE:
        return True
    if s in _FALSE:
        return False
    raise ParseError("%s: unrecognized games flag %r (want one of 1/0, true/false, yes/no, played/dnp)"
                     % (ref, raw))


def _to_int_round(raw, ref):
    try:
        r = int(str(raw).strip())
    except (TypeError, ValueError):
        raise ParseError("%s: round %r is not an integer" % (ref, raw))
    if r < 1:
        raise ParseError("%s: round %r must be >= 1" % (ref, r))
    return r


def _to_score(raw, ref):
    """Score may be blank/None (a DNP row can omit it). Non-blank must be numeric."""
    if raw is None:
        return None
    s = str(raw).strip()
    if s == '':
        return None
    try:
        return float(s)
    except ValueError:
        raise ParseError("%s: score %r is not numeric" % (ref, raw))


# ---- header/key normalization (case & separator insensitive) -----------------------------
def _canon_key(k):
    return "".join(ch for ch in str(k).strip().lower() if ch.isalnum())


# canonical field -> accepted header aliases (all canon-keyed)
_ALIASES = {
    'player': {'player', 'name', 'playername'},
    'round':  {'round', 'rd', 'roundno', 'roundnumber', 'week'},
    'score':  {'score', 'points', 'rating', 'fantasy', 'sc', 'af'},
    'played': {'played', 'gamesflag', 'games', 'game', 'flag', 'g', 'didplay', 'gp'},
    'club':   {'club', 'team', 'afflteam', 'clubname'},
}


def _build_colmap(headers):
    """Map each canonical field to its column index in the header row. player/round required;
    score/played/club optional (score/played default per-row)."""
    canon = [_canon_key(h) for h in headers]
    colmap = {}
    for field, aliases in _ALIASES.items():
        for i, c in enumerate(canon):
            if c in aliases:
                colmap[field] = i
                break
    for req in ('player', 'round'):
        if req not in colmap:
            raise ParseError("CSV header missing required column %r (have: %s)" % (req, list(headers)))
    return colmap


def parse_rows(rows, season_year=None):
    """Parse an iterable of dict-like rows (already keyed by canonical field name) into RoundScores.
    `rows` items are plain dicts with keys among player/round/score/played/club. Used by the JSON
    path and by callers that already have structured rows. season_year is metadata only (attached by
    the ingestor, not stored on the row)."""
    out = []
    for i, raw in enumerate(rows):
        ref = raw.get('source_ref') or ("row %d" % (i + 1))
        if 'player' not in raw or raw.get('player') in (None, ''):
            raise ParseError("%s: missing player name" % ref)
        rnd = _to_int_round(raw.get('round'), ref)
        score = _to_score(raw.get('score'), ref)
        played = _parse_flag(raw.get('played'), has_score=(score is not None), ref=ref)
        club = raw.get('club') or None
        if club is not None:
            club = str(club).strip() or None
        if played and score is None:
            raise ParseError("%s: played=True but no score given" % ref)
        out.append(RoundScore(str(raw['player']).strip(), rnd, score, played, club, ref))
    return out


def _parse_csv(text):
    reader = csv.reader(io.StringIO(text))
    try:
        headers = next(reader)
    except StopIteration:
        raise ParseError("empty CSV feed")
    colmap = _build_colmap(headers)
    rows = []
    for lineno, cells in enumerate(reader, start=2):   # line 1 is the header
        if not any(str(c).strip() for c in cells):
            continue                                   # skip blank lines
        ref = "csv line %d" % lineno

        def cell(field):
            idx = colmap.get(field)
            return cells[idx] if (idx is not None and idx < len(cells)) else None

        rows.append({'player': cell('player'), 'round': cell('round'), 'score': cell('score'),
                     'played': cell('played'), 'club': cell('club'), 'source_ref': ref})
    return parse_rows(rows)


def _parse_json(text):
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise ParseError("invalid JSON feed: %s" % e)
    if isinstance(obj, dict):
        obj = obj.get('rows', obj.get('scores'))
        if obj is None:
            raise ParseError("JSON object feed must carry a 'rows' (or 'scores') list")
    if not isinstance(obj, list):
        raise ParseError("JSON feed must be a list of row objects (or a {'rows': [...]} envelope)")
    rows = []
    for i, r in enumerate(obj):
        if not isinstance(r, dict):
            raise ParseError("row %d: expected an object, got %s" % (i + 1, type(r).__name__))
        rows.append({'player': r.get('player', r.get('name')),
                     'round': r.get('round', r.get('rd')),
                     'score': r.get('score', r.get('points')),
                     'played': r.get('played', r.get('games_flag', r.get('games'))),
                     'club': r.get('club', r.get('team')),
                     'source_ref': "row %d" % (i + 1)})
    return parse_rows(rows)


def parse_feed(text, fmt=None):
    """Parse a raw weekly feed string. fmt in {'csv','json'} or None to auto-detect
    (leading '[' or '{' -> JSON, else CSV). Returns a list[RoundScore]. Raises ParseError."""
    if fmt is None:
        stripped = text.lstrip()
        fmt = 'json' if stripped[:1] in ('[', '{') else 'csv'
    if fmt == 'json':
        return _parse_json(text)
    if fmt == 'csv':
        return _parse_csv(text)
    raise ParseError("unknown feed format %r" % fmt)
