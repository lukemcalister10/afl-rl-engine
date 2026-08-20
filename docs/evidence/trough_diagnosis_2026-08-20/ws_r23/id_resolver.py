"""name/key -> stable_player_id resolver — the SCORE BOUNDARY identity map.

The ID-primary migration attached `stable_player_id` (afl-player-v1-<20hex>) to
every csv-matched row of the single store (engine/rl_after/rl_model_data.json).
That id is the DURABLE identity. Weekly round scores arrive keyed by player NAME
(and, where available, the current AFL club, `afl_club` — imported item 20b from the
authoritative universe; NOT `affl_team`, which is the AFFL keeper side, a different fact:
houston is AFL Collingwood but AFFL St Kilda Saints); this module maps an incoming
(name[, club]) or a legacy_key onto the stable id WITHOUT collapsing distinct
players who share a name — the two Max Kings (`max-king-stk` / `max-king-syd`)
must never merge (collision sentry law, DECISIONS §29).

SCOPE: identity resolution ONLY. No valuation logic, no scoring, no board math.
The resolver reads the store as data and returns ids/keys; it never prices anyone.
"""
import json, os, re

try:
    from unidecode import unidecode
except Exception:                      # vendored offline; fall back to identity if unavailable
    def unidecode(s): return s

_STORE_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rl_model_data.json')

# name/club normalization — SAME convention as rl_model.norm (unidecode + a-z + space)
def _norm(n): return " ".join(re.sub(r"[^a-z ]", " ", unidecode(n or "").lower()).split())

# resolution status codes
RESOLVED   = 'RESOLVED'      # single stable id found
BY_KEY     = 'BY_KEY'        # resolved via exact legacy_key
NO_ID      = 'NO_ID'         # store row found but it carries no stable_player_id (historical/unmatched row)
AMBIGUOUS  = 'AMBIGUOUS'     # name collides and no/again-ambiguous club disambiguator -> caller must disambiguate
UNRESOLVED = 'UNRESOLVED'    # no store row matches


class Resolution:
    __slots__ = ('status', 'stable_player_id', 'key', 'candidates')
    def __init__(self, status, stable_player_id=None, key=None, candidates=None):
        self.status = status
        self.stable_player_id = stable_player_id
        self.key = key
        self.candidates = candidates or []      # list of (key, stable_player_id, afl_club) when AMBIGUOUS
    def __repr__(self):
        return "Resolution(%s id=%s key=%s%s)" % (
            self.status, self.stable_player_id, self.key,
            (" candidates=%d" % len(self.candidates)) if self.candidates else "")


class IdResolver:
    def __init__(self, store=None, store_path=None):
        if store is None:
            store = json.load(open(store_path or _STORE_DEFAULT))
        self._key_to_row = {}
        self._name_to_keys = {}
        for r in store:
            k = r.get('key')
            if k is None:
                continue
            # collapse duplicate-key groups to a single representative (the store is single-keyed today;
            # this is defence-in-depth and mirrors rl_model's earliest-entry collapse intent)
            self._key_to_row.setdefault(k, r)
            self._name_to_keys.setdefault(_norm(r.get('player')), set()).add(k)

    # ---- primary: exact legacy_key (authoritative, unambiguous) ----
    def by_key(self, key):
        r = self._key_to_row.get(key)
        if r is None:
            return Resolution(UNRESOLVED)
        sid = r.get('stable_player_id')
        return Resolution(BY_KEY if sid else NO_ID, stable_player_id=sid, key=key)

    # ---- score boundary: name (+ optional club) ----
    def resolve(self, name=None, club=None, key=None):
        if key is not None:
            return self.by_key(key)
        keys = sorted(self._name_to_keys.get(_norm(name), ()))
        if not keys:
            return Resolution(UNRESOLVED)
        cand = [(k, self._key_to_row[k].get('stable_player_id'),
                 self._key_to_row[k].get('afl_club')) for k in keys]
        # club, when supplied, is a VETO — it must never let a wrong-club player through. This is the
        # safety property the two-Max-Kings collision demands: a Sydney-side score must not attach to
        # the St Kilda player just because the names normalize alike. The disambiguator is `afl_club`
        # (the CURRENT AFL club a feed carries), NOT affl_team (item 20d — affl_team is the AFFL keeper
        # side; matching a feed's "D. Houston, Collingwood" against "St Kilda Saints" would MISS).
        if club:
            cn = _norm(club)
            cand = [c for c in cand if _club_match(cn, c[2])]
            if not cand:
                return Resolution(UNRESOLVED)
        if len(cand) == 1:
            k, sid, _ = cand[0]
            return Resolution(BY_KEY if sid else NO_ID, stable_player_id=sid, key=k)
        return Resolution(AMBIGUOUS, candidates=cand)   # NEVER collapse a genuine collision

    # ---- identity-integrity self-check (NOT a valuation gate) ----
    def integrity(self):
        ids = {}
        for k, r in self._key_to_row.items():
            sid = r.get('stable_player_id')
            if sid:
                ids.setdefault(sid, []).append(k)
        dup = {s: ks for s, ks in ids.items() if len(ks) > 1}
        return {
            'rows': len(self._key_to_row),
            'with_id': sum(1 for r in self._key_to_row.values() if r.get('stable_player_id')),
            'duplicate_ids': dup,                              # must be empty
            'name_collisions': {n: sorted(ks) for n, ks in self._name_to_keys.items() if len(ks) > 1},
        }


def _club_match(norm_club, afl_club):
    """True when the incoming (normalized) club and a row's afl_club (CURRENT AFL club, item 20d) refer
    to the same club. afl_club carries the short name ('Collingwood', 'Port Adelaide'); a feed may pass
    'Collingwood', 'Collingwood Magpies', or 'Pies'. Match on token containment either direction (no
    valuation content). Repointed from affl_team (the AFFL keeper side) — the club-semantics defect fix."""
    if not afl_club:
        return False
    at = set(_norm(afl_club).split())
    ic = set(norm_club.split())
    return bool(ic) and (ic <= at or at <= ic or bool(ic & at))


if __name__ == '__main__':
    import sys
    R = IdResolver(store_path=sys.argv[1] if len(sys.argv) > 1 else None)
    info = R.integrity()
    print("rows=%(rows)d with_id=%(with_id)d duplicate_ids=%(duplicate_ids)s" % info)
    print("name_collisions:", info['name_collisions'])
    for name, club in [("Nick Daicos", None), ("Max King", "St Kilda"), ("Max King", "Sydney"), ("Max King", None)]:
        print("  resolve(%r, club=%r) -> %r" % (name, club, R.resolve(name=name, club=club)))
