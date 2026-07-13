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


def _gate_or_bake():
    """True in the fenced gate/bake modes (RL_CONFIG_MODE). In these modes a missing/unresolvable owner-
    override file HALTS instead of returning a silent [] — the halt-not-warn doctrine (S1 finding, register
    item 24): a shipped/gated board must never silently drop a standing owner ruling."""
    return os.environ.get('RL_CONFIG_MODE') in ('bake', 'gate')


def _repo_root():
    """Locate the checked-out repo (never a workspace copy), like boot_guard."""
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))):
        if cand and os.path.exists(os.path.join(cand, 'data', 'owner_overrides.json')):
            return os.path.abspath(cand)
    return None


def load_overrides(root=None):
    """Return the list of override rows from the repo-homed file (read-once). In gate/bake mode an
    unresolvable root or an absent file HALTS (never a silent []); in dev-shell it returns [] as before."""
    root = root or _repo_root()
    if not root:
        if _gate_or_bake():
            raise SystemExit(
                "OWNER-OVERRIDE HALT (%s mode): cannot resolve the checked-out repo to read "
                "data/owner_overrides.json (RL_REPO / CLAUDE_PROJECT_DIR unset and no ../.. fallback). A "
                "gated/baked board must NOT silently ship without the standing owner rulings — set RL_REPO to "
                "the checkout. (Dev-shell returns [] and skips.)" % os.environ.get('RL_CONFIG_MODE'))
        return []
    path = os.path.join(root, 'data', 'owner_overrides.json')
    if not os.path.exists(path):
        if _gate_or_bake():
            raise SystemExit(
                "OWNER-OVERRIDE HALT (%s mode): data/owner_overrides.json is ABSENT at %s — the standing "
                "owner rulings are missing. Refusing to gate/bake a board that would silently drop them "
                "(halt-not-warn; S1 finding, register item 24)." % (os.environ.get('RL_CONFIG_MODE'), path))
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


def assert_presence(active, root=None):
    """POST-EXPORT PRESENCE ASSERTION (S1 finding, register item 24): every player_key listed in
    data/owner_overrides.json MUST carry its `ov` block on the exported board, key-verified vs the store.
    In gate/bake mode a listed-but-unapplied override (key drift, or a silent drop) HALTS — the
    correction-sticks pattern applied to overrides. Dev-shell only warns. Call AFTER apply_to_board."""
    overrides = load_overrides(root)
    by_key = {r.get('key'): r for r in active}
    missing = []
    for ov in overrides:
        key = ov.get('player_key')
        row = by_key.get(key)
        if row is None or 'ov' not in row:
            missing.append(key)
    if missing:
        msg = ("OWNER-OVERRIDE PRESENCE ASSERTION FAILED: %d listed override(s) carry NO `ov` block on the "
               "exported board (key drift or silent drop): %s. Verify the store key(s) against the board and "
               "re-run — a gated/baked board MUST realize every standing owner ruling." % (len(missing), missing))
        if _gate_or_bake():
            raise SystemExit(msg)
        print("OWNER-OVERRIDE WARNING (dev-shell, non-halting):", msg)
    return missing
