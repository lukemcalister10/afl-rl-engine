"""FOOTYWIRE ROUND PARSER — decode + normalize a weekly FootyWire round export, encoding-safe.

The owner's genuine weekly exports come as a two-row-header CSV:

    Player,2026 R15
    ,Score
    Luke Jackson,176
    Nick Daicos,159
    ...

and in varying encodings (Windows/CP1252 for some rounds, UTF-8 — with or without a BOM — for others).
This module decodes the bytes WITHOUT altering any name or score, records the detected encoding + a
byte-level file hash, strips the two header rows, and returns clean `(name, score)` rows. It never
resolves identities and never writes anything — it is the safe front door to the round entry / catch-up.

Participation is defined by FILE MEMBERSHIP (owner ruling): a listed row = the player PLAYED; the score
is appended and one game is added to the denominator; a listed score of 0 is a legitimate played score
(a genuine zero, not a placeholder). Absence from the file = did-not-play and is NOT a parse error. The
parser therefore preserves EVERY listed row (including score 0) and drops nothing.
"""
import csv
import hashlib
import io
import os

SCORE_DECIMALS = 1
_HEADER_NAME_TOKENS = {'player', 'name', 'playername'}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def decode_bytes(raw):
    """Decode round bytes to text WITHOUT altering content; return (text, encoding_label).

    A UTF-8 BOM -> utf-8-sig; else strict UTF-8; else CP1252 (Windows-1252, a strict superset of
    Latin-1 over the byte range these exports use). The label is reported in the preflight so the owner
    sees exactly how each file was read."""
    if raw[:3] == b'\xef\xbb\xbf':
        return raw[3:].decode('utf-8'), 'utf-8-sig'
    try:
        return raw.decode('utf-8'), 'utf-8'
    except UnicodeDecodeError:
        return raw.decode('cp1252'), 'cp1252'


class FootyWireParseError(ValueError):
    """A round row that cannot be parsed (missing name, non-numeric score) — loud, never a silent drop."""


def _is_header_row(cells):
    """The FootyWire two-row header: `Player,2026 R15` then `,Score`. Row 1 has a name-token in col 0;
    row 2 has an empty col 0 and a `Score` label. Recognised structurally so the round number in the
    header (`2026 R15`) is never mistaken for a score."""
    first = (cells[0] or '').strip().lower()
    if first in _HEADER_NAME_TOKENS:
        return True
    if first == '' and any((c or '').strip().lower() == 'score' for c in cells[1:]):
        return True
    return False


def parse_text(text):
    """Parse decoded round text -> [(name, score)]. Skips the two header rows + blank/`#` lines. A row
    with a blank/non-numeric score fails LOUDLY. A score of 0 is preserved (a legitimate played score)."""
    rows = []
    for lineno, raw in enumerate(io.StringIO(text), start=1):
        line = raw.rstrip('\n').rstrip('\r')
        if not line.strip():
            continue
        cells = next(csv.reader([line]))
        if not cells:
            continue
        if (cells[0] or '').strip().startswith('#'):
            continue
        if _is_header_row(cells):
            continue
        name = (cells[0] or '').strip()
        score_raw = (cells[-1] or '').strip()
        if not name:
            raise FootyWireParseError("line %d: missing player name (%r)" % (lineno, line))
        if score_raw == '':
            raise FootyWireParseError("line %d: missing score for %r" % (lineno, name))
        try:
            score = round(float(score_raw), SCORE_DECIMALS)
        except ValueError:
            raise FootyWireParseError("line %d: score %r for %r is not numeric" % (lineno, score_raw, name))
        rows.append((name, score))
    if not rows:
        raise FootyWireParseError("no `name,score` rows found after the header")
    return rows


def parse_round_file(path):
    """Read one round file -> {path, sha256, encoding, listed, listed_zero, rows:[(name,score)]}."""
    raw = open(path, 'rb').read()
    text, encoding = decode_bytes(raw)
    rows = parse_text(text)
    listed_zero = sum(1 for _n, s in rows if s == 0)
    return {'path': os.path.abspath(path), 'sha256': sha256_file(path), 'encoding': encoding,
            'listed': len(rows), 'listed_zero': listed_zero, 'rows': rows}
