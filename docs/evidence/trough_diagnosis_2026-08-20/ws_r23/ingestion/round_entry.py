"""ROUND-ENTRY TOOL — the owner's weekly `name,score` paste -> resolved rows + stamped snapshot.

DRY-RUN ONLY at THIS layer. This module reads the single source (`rl_model_data.json`) READ-ONLY
and writes NOTHING to it. The store-write is a SEPARATE, hard-gated, staged transaction
(engine/rl_after/ingestion/staged_apply.py) that consumes the stamped snapshot produced here; that
apply gate ships OFF (score_ingestor.APPLY_DEFAULT=False + env INGEST_SCORE_APPLY unset). Snapshots
produced here are DERIVED artifacts (SSI): read-only, source-stamped, disposable.

THE LAW (register item 305, owner ground-truth — verbatim):
    Input of record: a FootyWire weekly export, `name, score`, names identical to the DB, CURRENT
    players only. The owner's workflow is PRESERVED: paste round + name + score — a 2-minute job;
    unique IDs are NOT required and not asked for. The resolver exact-matches name ->
    active-stable-ID over the LIVE active pool read at RUN TIME (new-intake IDs picked up
    automatically the moment they enter the DB). The real failure mode is a SILENT MISS, not a
    clash: any export name that does not cleanly resolve is a FLAGGED RESIDUE LINE for a one-tap
    owner confirm — NEVER a silent drop, NEVER attached to the wrong row, NEVER a new-row
    invention. A scoring player not yet in the DB is residue (ask), never a guess.

SNAPSHOT IDENTITY (2026-07-20 hardening, JOB 2). A snapshot is now a self-verifying transaction
authorization. It carries, beyond the resolved rows:
    * source_store_md5_full  — the FULL 32-char md5 of the store it was resolved against (the apply
                               refuses unless the LIVE store still hashes to this — a stale snapshot
                               cannot apply to a moved store);
    * source_store_md5       — the 8-char short md5 (display only; kept for backward compat);
    * round / season_year    — the (round, season) the triples belong to;
    * stable player IDs      — the identity of record for each resolved row (never a fuzzy name);
    * exact scores           — the round score, verbatim;
    * module identity        — snapshot_schema_version + module_code_md5 + per-file module_identity
                               (the behaviour-defining code that produced it);
    * content_hash           — a deterministic md5 over the snapshot's own canonical bytes (with the
                               content_hash field itself excluded), so any post-hoc edit is detected
                               before apply.
Backward compatibility: a v1 snapshot (no schema version / no full md5 / no content hash) still
loads and shows; the STRONG checks the apply enforces only pass for a v2 snapshot re-stamped here.

SCOPE: identity resolution over the active pool + aggregation into a stamped per-round snapshot.
No valuation, no board math, no pricing, no store write. The active pool is read live so a
new-intake id resolves the moment it enters the DB.
"""
import csv
import difflib
import hashlib
import io
import json
import os
import re

# --- read-only reuse of the engine's normalisation + gate (imported, NEVER modified) ---------
try:
    from ..id_resolver import _norm as _engine_norm     # unidecode + lower + a-z/space + collapse
except (ImportError, ValueError):        # allow direct-script / non-package execution
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from id_resolver import _norm as _engine_norm        # type: ignore

_HERE = os.path.dirname(os.path.abspath(__file__))
_STORE_DEFAULT = os.path.join(os.path.dirname(_HERE), 'rl_model_data.json')
_RESOLVER_SRC = os.path.join(os.path.dirname(_HERE), 'id_resolver.py')
_THIS_SRC = os.path.abspath(__file__)

DEFAULT_SEASON_YEAR = 2026               # live season; == rl_model.py BASE_REF (identity, not pricing)
SCORE_DECIMALS = 1                        # FootyWire scores are integers/1dp; snapshot rounds to 1dp
_NEAR_MATCH_N = 4                         # nearest candidates surfaced on a residue line
_NEAR_MATCH_CUTOFF = 0.6                  # difflib ratio floor for a "near-match" suggestion

# snapshot schema version: v1 = original (short store md5, no content hash); v2 = strong identity.
SNAPSHOT_SCHEMA_VERSION = 2
_CONTENT_HASH_FIELD = 'content_hash'      # excluded from its own hash input

# resolution status codes (this tool's active-pool view)
RESOLVED   = 'RESOLVED'                   # exactly one ACTIVE exact-name match
AMBIGUOUS  = 'AMBIGUOUS'                  # >= 2 ACTIVE exact-name matches (a genuine live clash)
UNRESOLVED = 'UNRESOLVED'                 # no ACTIVE exact-name match (unknown / misspelled / retired)


def norm(name):
    """Case/whitespace-insensitive EXACT key — the engine's own convention, reused not re-invented."""
    return _engine_norm(name)


def is_active(row):
    """A live active-pool row: carries a durable stable_player_id AND is not retired. Retirees carry
    no stable id in this store, so they fall out naturally; the _retired guard is belt-and-braces."""
    return bool(row.get('stable_player_id')) and not row.get('_retired')


# ---- artifact records ----------------------------------------------------------------------
class ResolvedRow:
    """One export line cleanly attached to an active player. IDs are identity; name is display."""
    __slots__ = ('stable_player_id', 'key', 'name', 'score', 'via', 'source_ref')

    def __init__(self, stable_player_id, key, name, score, via, source_ref=None):
        self.stable_player_id = stable_player_id
        self.key = key
        self.name = name                 # the store's canonical player name (display)
        self.score = score
        self.via = via                   # 'exact' | 'confirm'
        self.source_ref = source_ref

    def as_dict(self):
        return {'stable_player_id': self.stable_player_id, 'key': self.key, 'name': self.name,
                'score': self.score, 'via': self.via}


class ResidueLine:
    """An export line that did NOT cleanly resolve — a FLAGGED one-tap confirm, never a guess.

    reason: 'unresolved' (no active exact match) | 'ambiguous' (>=2 active exact matches).
    candidates: [{index, key, stable_player_id, name, kind}] the owner picks ONE from, or skips.
    """
    __slots__ = ('name', 'score', 'reason', 'candidates', 'source_ref')

    def __init__(self, name, score, reason, candidates, source_ref=None):
        self.name = name
        self.score = score
        self.reason = reason
        self.candidates = candidates
        self.source_ref = source_ref

    def as_dict(self):
        return {'name': self.name, 'score': self.score, 'reason': self.reason,
                'candidates': self.candidates, 'source_ref': self.source_ref}


# ---- the active-pool resolver --------------------------------------------------------------
class ActivePoolResolver:
    """Exact-match a name onto an active `stable_player_id`, reading the LIVE active pool.

    No fuzzy AUTO-attach: a near-miss returns UNRESOLVED with the nearest active candidates listed
    for the owner's one-tap confirm. A name shared by >=2 active players returns AMBIGUOUS with both
    candidates. A genuine live clash is never collapsed (the two-Max-Kings law) — but note both Max
    Kings are inactive, so today the live pool holds ZERO name collisions.
    """

    def __init__(self, store=None, store_path=None):
        if store is None:
            store = json.load(open(store_path or _STORE_DEFAULT))
        self._by_norm = {}               # norm(name) -> [active rows]
        self._active_names = []          # canonical display names of the active pool (for near-match)
        for r in store:
            if not is_active(r):
                continue
            self._by_norm.setdefault(norm(r.get('player')), []).append(r)
            self._active_names.append(r.get('player'))
        self._active_names.sort()        # deterministic near-match ordering
        # a normalised-name -> canonical-name map so near-matches can carry the store spelling
        self._norm_to_names = {}
        for r_list in self._by_norm.values():
            for r in r_list:
                self._norm_to_names.setdefault(norm(r.get('player')), r.get('player'))

    @property
    def active_count(self):
        return sum(len(v) for v in self._by_norm.values())

    def _candidate(self, index, row, kind):
        return {'index': index, 'key': row.get('key'),
                'stable_player_id': row.get('stable_player_id'),
                'name': row.get('player'), 'kind': kind}

    def resolve(self, name):
        """Return (status, resolved_row_or_None, candidates). candidates is 1-indexed for the owner."""
        rows = self._by_norm.get(norm(name), [])
        if len(rows) == 1:
            r = rows[0]
            return RESOLVED, r, [self._candidate(1, r, 'active exact')]
        if len(rows) >= 2:               # genuine live clash — NEVER collapse; show BOTH
            rows_sorted = sorted(rows, key=lambda x: x.get('key') or '')
            cands = [self._candidate(i + 1, r, 'active exact') for i, r in enumerate(rows_sorted)]
            return AMBIGUOUS, None, cands
        # no exact active match -> residue with nearest active candidates (suggestions, never auto)
        near = difflib.get_close_matches(norm(name), list(self._norm_to_names.keys()),
                                         n=_NEAR_MATCH_N, cutoff=_NEAR_MATCH_CUTOFF)
        cands = []
        for i, nk in enumerate(near):
            disp = self._norm_to_names[nk]
            row = self._by_norm[nk][0]
            c = self._candidate(i + 1, row, 'near-match %.2f'
                                % difflib.SequenceMatcher(None, norm(name), nk).ratio())
            cands.append(c)
        return UNRESOLVED, None, cands


# ---- the `name,score` parser (FootyWire weekly export) -------------------------------------
class RoundEntryParseError(ValueError):
    """A weekly `name,score` line that cannot be parsed (missing name, non-numeric score)."""


_HEADER_NAME = {'name', 'player', 'playername'}
_HEADER_SCORE = {'score', 'points', 'rating', 'fantasy', 'af', 'sc'}


def _canon(s):
    return "".join(ch for ch in str(s).strip().lower() if ch.isalnum())


def parse_name_score(body):
    """Parse a FootyWire weekly `name,score` body into [(name, score, source_ref)].

    Accepts CSV (comma OR tab separated) with or without a header row, and pasted lines. Round is
    NOT a per-row field — it comes from `--round N`. A row with a blank/non-numeric score fails
    LOUDLY (never silently dropped). Blank lines and `#` comment lines are skipped.
    """
    text = body if isinstance(body, str) else body.read()
    rows = []
    reader = _split_rows(text)
    header_cols = None
    for lineno, cells in reader:
        if not cells or not any(str(c).strip() for c in cells):
            continue
        first = str(cells[0]).strip()
        if first.startswith('#'):
            continue
        # header detection (only on the first content line): a row whose cells are known headers
        if header_cols is None and _looks_like_header(cells):
            header_cols = _map_header(cells)
            continue
        ref = "line %d" % lineno
        if header_cols is not None:
            name = _cell(cells, header_cols.get('name'))
            score_raw = _cell(cells, header_cols.get('score'))
        else:
            if len(cells) < 2:
                raise RoundEntryParseError(
                    "%s: expected `name,score`, got %r" % (ref, ",".join(cells)))
            name = cells[0]
            score_raw = cells[-1]         # score is the last field (names may contain commas? no —
            #                               FootyWire uses `name,score`; last-field is robust to a
            #                               stray trailing empty cell)
        name = (name or '').strip()
        if not name:
            raise RoundEntryParseError("%s: missing player name" % ref)
        rows.append((name, _to_score(score_raw, ref), ref))
    if not rows:
        raise RoundEntryParseError("empty feed: no `name,score` rows found")
    return rows


def _split_rows(text):
    """Yield (lineno, [cells]) splitting on comma or tab. csv handles quoted commas correctly."""
    for lineno, raw in enumerate(io.StringIO(text), start=1):
        line = raw.rstrip('\n').rstrip('\r')
        if '\t' in line and ',' not in line:
            cells = line.split('\t')
        else:
            cells = next(csv.reader([line])) if line else []
        yield lineno, cells


def _looks_like_header(cells):
    canon = {_canon(c) for c in cells}
    return bool(canon & _HEADER_NAME) and bool(canon & _HEADER_SCORE)


def _map_header(cells):
    out = {}
    for i, c in enumerate(cells):
        cc = _canon(c)
        if cc in _HEADER_NAME and 'name' not in out:
            out['name'] = i
        elif cc in _HEADER_SCORE and 'score' not in out:
            out['score'] = i
    if 'name' not in out or 'score' not in out:
        raise RoundEntryParseError("header row missing a name and/or score column: %r" % cells)
    return out


def _cell(cells, idx):
    return cells[idx] if (idx is not None and idx < len(cells)) else None


def _to_score(raw, ref):
    if raw is None:
        raise RoundEntryParseError("%s: missing score" % ref)
    s = str(raw).strip()
    if s == '':
        raise RoundEntryParseError("%s: missing score" % ref)
    try:
        return round(float(s), SCORE_DECIMALS)
    except ValueError:
        raise RoundEntryParseError("%s: score %r is not numeric" % (ref, raw))


# ---- code / store stamping (SSI) -----------------------------------------------------------
def _md5_hex(b):
    return hashlib.md5(b).hexdigest()


def _md5_bytes(b):
    return _md5_hex(b)[:8]


def md5_of_file(path):
    """SHORT (8-char) md5 of a file — display + backward-compatible identity."""
    try:
        with open(path, 'rb') as f:
            return _md5_bytes(f.read())
    except OSError:
        return None


def md5_of_file_full(path):
    """FULL (32-char) md5 of a file — the strong store-identity the apply gates on (JOB 2)."""
    try:
        h = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 16), b''):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def module_code_md5():
    """Stamp the behaviour-defining code: this module XOR-order-independent with the resolver it
    reuses. md5 over (round_entry.py bytes || id_resolver.py bytes), stable & documented."""
    parts = []
    for p in sorted([_THIS_SRC, _RESOLVER_SRC]):
        try:
            with open(p, 'rb') as f:
                parts.append(f.read())
        except OSError:
            parts.append(b'')
    return _md5_bytes(b"\x00".join(parts))


def module_identity():
    """Per-file behaviour-defining code identity (JOB 2 'module/version identity'): the short md5 of
    each source that shapes a snapshot, keyed by role. Auditable and stable; a code change here moves
    module_code_md5 too, so a snapshot produced by different code is visibly a different snapshot."""
    return {'round_entry': md5_of_file(_THIS_SRC), 'id_resolver': md5_of_file(_RESOLVER_SRC)}


# ---- the round entry: resolve a whole body -------------------------------------------------
class RoundEntry:
    """Resolve one round's `name,score` body against the live active pool -> resolved + residue."""

    def __init__(self, round_n, season_year=DEFAULT_SEASON_YEAR, store=None, store_path=None):
        if int(round_n) < 1:
            raise ValueError("round must be >= 1, got %r" % round_n)
        self.round = int(round_n)
        self.season_year = int(season_year)
        self.store_path = store_path or _STORE_DEFAULT
        self.resolver = ActivePoolResolver(store=store, store_path=self.store_path)

    def resolve_body(self, body):
        """Parse + resolve. Returns (resolved:[ResolvedRow], residue:[ResidueLine])."""
        parsed = parse_name_score(body)
        resolved, residue = [], []
        for name, score, ref in parsed:
            status, row, cands = self.resolver.resolve(name)
            if status == RESOLVED:
                resolved.append(ResolvedRow(row.get('stable_player_id'), row.get('key'),
                                            row.get('player'), score, 'exact', ref))
            else:
                reason = 'ambiguous' if status == AMBIGUOUS else 'unresolved'
                residue.append(ResidueLine(name, score, reason, cands, ref))
        resolved.sort(key=lambda r: r.key or '')
        return resolved, residue

    # -- snapshot (SSI-conformant, deterministic, self-verifying) ----------------------------
    def build_snapshot(self, resolved, generated_at, skipped=None):
        """A DERIVED, read-only, source-stamped snapshot carrying STRONG identity (JOB 2).

        Deterministic given identical inputs (including `generated_at`, which the caller supplies
        explicitly). The snapshot stamps BOTH the short and the full store md5, the module/version
        identity, and — last — a content_hash over its own canonical bytes so any later edit is
        caught before an apply touches the store.
        """
        skipped = skipped or []
        rows = sorted((r.as_dict() for r in resolved), key=lambda d: d['key'] or '')
        skips = sorted((s if isinstance(s, dict) else s.as_dict() for s in skipped),
                       key=lambda d: (d.get('name') or '').lower())
        snap = {
            'kind': 'round_entry_snapshot',
            'snapshot_schema_version': SNAPSHOT_SCHEMA_VERSION,
            'round': self.round,
            'season_year': self.season_year,
            'generated_at': generated_at,
            'source_store_md5': md5_of_file(self.store_path),           # short, display
            'source_store_md5_full': md5_of_file_full(self.store_path),  # full, the strong gate
            'module_code_md5': module_code_md5(),
            'module_identity': module_identity(),
            'resolved': rows,
            'skipped': skips,
            'counts': {'resolved': len(rows), 'skipped': len(skips), 'residue_open': 0},
        }
        snap[_CONTENT_HASH_FIELD] = compute_content_hash(snap)
        return snap


def snapshot_bytes(snapshot):
    """Canonical, byte-deterministic serialization of a snapshot (sort_keys, fixed indent, ascii)."""
    return (json.dumps(snapshot, sort_keys=True, indent=2, ensure_ascii=True) + '\n').encode('utf-8')


def compute_content_hash(snapshot):
    """Deterministic md5 over the snapshot's canonical bytes with the content_hash field EXCLUDED.

    The hash is over exactly the fields that carry meaning (identity + rows + counts), serialized
    canonically, so it is stable across re-serialization and independent of key order. Excluding the
    content_hash field lets the value be embedded in the same object it authenticates."""
    body = {k: v for k, v in snapshot.items() if k != _CONTENT_HASH_FIELD}
    return _md5_hex(snapshot_bytes(body))


def load_snapshot(path):
    """Load a snapshot JSON from disk. Raises OSError/json errors to the caller (loud)."""
    with open(path) as f:
        return json.load(f)


def verify_snapshot(snapshot):
    """Verify a snapshot's self-consistency. Returns (ok: bool, reason: str).

    v2 (has content_hash): recompute and compare — any post-hoc edit fails.
    v1 (no content_hash):  ok=True with reason 'legacy-v1-no-content-hash' (backward compatible; the
                           STRONG apply path additionally requires v2, so a v1 snapshot cannot silently
                           apply — the caller decides). A malformed v2 (content_hash present but wrong)
                           always fails.
    """
    if not isinstance(snapshot, dict) or snapshot.get('kind') != 'round_entry_snapshot':
        return False, 'not a round_entry_snapshot'
    if _CONTENT_HASH_FIELD not in snapshot:
        return True, 'legacy-v1-no-content-hash'
    got = snapshot.get(_CONTENT_HASH_FIELD)
    want = compute_content_hash(snapshot)
    if got != want:
        return False, 'content_hash mismatch (got %s, want %s) — snapshot was edited after stamping' % (
            (got or '')[:12], want[:12])
    return True, 'ok'


def is_strong(snapshot):
    """True iff the snapshot carries the v2 strong identity the apply gate requires."""
    return (isinstance(snapshot, dict)
            and snapshot.get('snapshot_schema_version', 1) >= 2
            and bool(snapshot.get('source_store_md5_full'))
            and _CONTENT_HASH_FIELD in snapshot)


# ---- the residue file (human-first; the single edit the owner makes) -----------------------
_RESIDUE_HEADER = """\
# ============================================================================
# ROUND {round} · RESIDUE · {n} line(s) need a one-tap confirm
# ----------------------------------------------------------------------------
# For EACH block below, edit its ACTION line: put a candidate NUMBER (1, 2, ...)
# to attach the score to that player, OR the word `skip` to drop the line.
# Then run:  round_entry confirm --round {round}
#
# Nothing enters the snapshot until you confirm. No name is ever guessed, never
# attached to the wrong row, never invents a new row. A not-yet-in-DB scorer is
# a `skip` (or add them to the DB first, then re-enter the round).
# ============================================================================
"""


def write_residue(round_n, residue, path):
    """Write the human-first residue file. The owner edits only the ACTION line per block."""
    out = [_RESIDUE_HEADER.format(round=round_n, n=len(residue))]
    for i, r in enumerate(residue, start=1):
        out.append("")
        out.append("[%d] %s  name=%r  score=%s" % (i, r.reason.upper(), r.name, r.score))
        out.append("    ACTION: ")            # <- the owner edits exactly this (number or `skip`)
        if r.candidates:
            out.append("    candidates:")
            for c in r.candidates:
                out.append("      %d) %-24s key=%-22s id=%s   (%s)"
                           % (c['index'], c['name'], c['key'], c['stable_player_id'], c['kind']))
        else:
            out.append("    candidates: (none found — likely not in the DB; use `skip`)")
    text = "\n".join(out) + "\n"
    with open(path, 'w') as f:
        f.write(text)
    return text


_BLOCK_RE = re.compile(r"^\[(\d+)\]\s+(\w+)\s+name=(.+?)\s+score=(\S+)\s*$")
_ACTION_RE = re.compile(r"^\s*ACTION:\s*(.*?)\s*$")
_CAND_RE = re.compile(r"^\s*(\d+)\)\s+(.+?)\s+key=(\S+)\s+id=(\S+)\s+\((.+)\)\s*$")


class ResidueConfirmError(ValueError):
    """The edited residue file is incomplete or invalid — REFUSE loudly, write no snapshot."""


def read_confirmed_residue(path):
    """Parse an owner-edited residue file into confirmed decisions.

    Returns [{'name','score','action','pick'}] where action is 'attach'|'skip' and, for attach,
    'pick' is the chosen candidate {index,key,stable_player_id,name}. Every block MUST carry a
    filled, valid ACTION — a blank or out-of-range ACTION raises ResidueConfirmError.
    """
    with open(path) as f:
        lines = f.read().splitlines()
    decisions, i, n = [], 0, len(lines)
    while i < n:
        m = _BLOCK_RE.match(lines[i])
        if not m:
            i += 1
            continue
        idx, reason, name_repr, score_raw = m.groups()
        try:
            name = _unrepr(name_repr)
        except Exception:
            name = name_repr.strip()
        score = _to_score(score_raw, "residue block %s" % idx)
        i += 1
        action = None
        candidates = {}
        while i < n and not _BLOCK_RE.match(lines[i]):
            am = _ACTION_RE.match(lines[i])
            if am and action is None:
                action = am.group(1).strip()
            cm = _CAND_RE.match(lines[i])
            if cm:
                cnum = int(cm.group(1))
                candidates[cnum] = {'index': cnum, 'name': cm.group(2).strip(),
                                    'key': cm.group(3), 'stable_player_id': cm.group(4)}
            i += 1
        if action is None or action == '':
            raise ResidueConfirmError(
                "block [%s] name=%r has a BLANK ACTION — put a candidate number or `skip`."
                % (idx, name))
        low = action.lower()
        if low in ('skip', 's', 'x', '-'):
            decisions.append({'name': name, 'score': score, 'action': 'skip', 'pick': None})
            continue
        if not action.isdigit():
            raise ResidueConfirmError(
                "block [%s] name=%r ACTION=%r is not a candidate number or `skip`."
                % (idx, name, action))
        pick = candidates.get(int(action))
        if pick is None:
            raise ResidueConfirmError(
                "block [%s] name=%r ACTION=%s has no candidate %s (choices: %s)."
                % (idx, name, action, action, sorted(candidates) or 'none'))
        decisions.append({'name': name, 'score': score, 'action': 'attach', 'pick': pick})
    if not decisions:
        raise ResidueConfirmError("no residue blocks found in %s" % path)
    return decisions


def _unrepr(s):
    """Recover the raw name from its repr() (single- or double-quoted)."""
    s = s.strip()
    if len(s) >= 2 and s[0] in "'\"" and s[-1] == s[0]:
        return s[1:-1]
    return s


def confirmed_to_rows(decisions):
    """Turn confirmed decisions into (resolved:[ResolvedRow], skipped:[dict])."""
    resolved, skipped = [], []
    for d in decisions:
        if d['action'] == 'attach':
            p = d['pick']
            resolved.append(ResolvedRow(p['stable_player_id'], p['key'], p['name'],
                                        d['score'], 'confirm'))
        else:
            skipped.append({'name': d['name'], 'score': d['score'], 'reason': 'owner-skip'})
    resolved.sort(key=lambda r: r.key or '')
    return resolved, skipped
