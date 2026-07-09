#!/usr/bin/env python3
"""OWNER OVERRIDES — display-layer application (Brodie override wiring, 2026-07-09).

WHAT
  Reads the repo-homed `data/owner_overrides.json` (single owner-ruled input; owner adds a row without a
  code change) and applies each override to the EXPORTED board rows as a DISPLAY-ONLY adjustment. An
  override is a final multiplier on a single player's DISPLAYED value; it is applied LAST, after every
  lever and after the export<->engine parity gate.

INVARIANT (the whole point)
  The override NEVER touches the engine value `v`. It only ADDS an `ov` block to the matched row:
      ov = {factor, dispv = round(v*factor), mark, note, prov}
  Every guard, aggregate, the walk-forward book (F2), board parity (B4) and the JS parity check read
  `v` (or the engine's gated ev()) — never `ov`. So the board is byte-identical with the override on vs
  off EXCEPT for the added `ov` block on the overridden player's row. That is exactly "display-only,
  excluded from all guards/aggregates/book/G-COHORT inputs" made mechanical.

TOGGLE
  Set RL_NO_OWNER_OVERRIDES=1 to skip application entirely (the OFF state the exclusion test compares
  against). Default = apply.

KEY-DRIFT DISCIPLINE
  Each override key is verified against the live board keys at apply time. A key that matches no board
  row is REPORTED loudly (returned in `warnings`) rather than guessed — per the toby-briggs /
  jeremy-cameron precedents.
"""
import os, json


def _repo_root():
    """Locate the checked-out repo (never a workspace copy), like boot_guard."""
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))):
        if cand and os.path.exists(os.path.join(cand, 'data', 'owner_overrides.json')):
            return os.path.abspath(cand)
    return None


def load_overrides(root=None):
    """Return the list of override rows from the repo-homed file (read-once). [] if the file is absent."""
    root = root or _repo_root()
    if not root:
        return []
    path = os.path.join(root, 'data', 'owner_overrides.json')
    if not os.path.exists(path):
        return []
    with open(path) as f:
        doc = json.load(f)
    return doc.get('overrides', [])


def apply_to_board(active, root=None):
    """Apply owner overrides to the exported active rows IN PLACE (display-only; never touches `v`).

    Adds an `ov` block to each matched row. Returns (applied, warnings) where `applied` is the list of
    (player_key, factor, dispv) applied and `warnings` is the list of key-drift messages.
    Honors RL_NO_OWNER_OVERRIDES=1 (skip). Idempotent-safe: it reads `v`, never a prior `ov`.
    """
    applied, warnings = [], []
    if os.environ.get('RL_NO_OWNER_OVERRIDES', '0') != '0':
        return applied, warnings
    overrides = load_overrides(root)
    if not overrides:
        return applied, warnings
    by_key = {r.get('key'): r for r in active}
    for ov in overrides:
        key = ov.get('player_key')
        factor = ov.get('factor')
        if key is None or factor is None:
            warnings.append("owner override row missing player_key/factor: %r" % ov)
            continue
        row = by_key.get(key)
        if row is None:
            warnings.append("OWNER-OVERRIDE key %r not on the board (key drift? verify the store key) — SKIPPED" % key)
            continue
        v = row.get('v')
        if v is None:
            warnings.append("OWNER-OVERRIDE key %r has no board value v — SKIPPED" % key)
            continue
        dispv = int(round(v * factor))
        row['ov'] = {
            'factor': factor,
            'dispv': dispv,                                   # the DISPLAYED (overridden) value
            'mark': 'OWNER OVERRIDE ×%.2f' % factor,     # visible marker: this is an owner read, not a model price
            'note': ov.get('note', ''),
            'prov': ov.get('provenance', ''),
        }
        applied.append((key, factor, dispv))
    return applied, warnings
