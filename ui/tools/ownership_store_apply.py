#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OWNERSHIP STORE APPLY (#283) — the OUT-OF-ROUND store-write transaction.

WHAT THIS IS.  The owner authors AFFL ownership in docs/inputs/AFFL_Player_Locations.csv.  Under the
2026-07-30 owner ruling the STORE (engine/rl_after/rl_model_data.json, field `affl_team`) is the single
source of that truth; the #232 sidecar ui/data/ownership.js survives as a GENERATED MIRROR rebuilt FROM
the store, never independently authoritative.  This module carries the CSV into the store and moves
every identity pin that the store md5 ripples into — atomically, or not at all.

WHY IT IS NOT THE WEEKLY LANE.  engine/rl_after/ingestion/staged_apply.py is a ROUND apply: it commits
the score ledger + value/rank histories and advances as_of_round, and entering it means arming the
score-write gate that every CI workflow asserts ships OFF.  An ownership edit carries no scores and no
round.  The tree's own prescribed shape for a store move outside a round is the APPENDED
release_transition entry — data/release_lineage.json's own _doc says so: "an APPENDED entry is the
shape the validator's own law prescribes for a future out-of-round board move".  This module is that
lane.  [#283 read-back + seam Ruling 1, 2026-07-30]

WHAT MOVES, AND WHY THE BOARD DOES NOT.  `affl_team` is NOT in the board of record: data/rl_build/
rl_app_data.json carries the key on 128 lensPicks phantoms only, all null, and the 804 active player
rows do not carry it at all.  The UI's affl_team is JOINED FROM THE STORE at extract time
(ui/tools/extract_board_view.py).  So an ownership write moves no board bytes, no board md5, and needs
NO ENGINE BUILD.  Values do not move; identity does.  The board's own byte-integrity pin
(rl_app_data.json.srcmd5 `own_md5`) is asserted UNCHANGED here; only its `source_md5` advances.

THE TEN TARGETS (the transaction commits all ten together or none):
   0  engine/rl_after/rl_model_data.json          the store write itself
   1  data/expected_boot.json                     `store`
   2  data/release_contract.json                  identities.store + contract_sha256 re-seal
   3  data/rl_build/rl_app_data.json.srcmd5       source_md5   (own_md5 UNCHANGED)
   4  data/season_state.json                      source_store_md5   (derived values proven unchanged)
   5  ui/data/board_view_working.js               stamp.store_md5 / .store + 18 affl_team labels
   6  data/release_lineage.json                   APPENDED release_transition_register entry
   7  ui/data/movers_transition.js                the byte-identical UI mirror of (6)
   8  ui/data/board_view_public.js                18 affl_team labels
   9  ui/data/ownership.js                        the generated mirror (rebuilt FROM the store)
  10  ui/data/club_valuation.js                   the ingest's other output

THE JOIN, AND WHY IT IS BY KEY (hazard class 13, demonstrated not theoretical).  The CSV names players.
Store `key` is globally unique (2,651 of 2,651 distinct) and the board universe is name-unique (804,
zero ambiguous) — but FIVE board players have a name-twin elsewhere in the store (harrison-jones,
lachlan-smith, sam-butler-1, tom-lynch-1, will-hayes-b), and one of them — sam-butler-1 — is IN the
2026-07-29 change set.  A name->store join taking [0] would be a coin-flip on which Sam Butler received
the write, and the change count would still read 18.  So the join is:
    CSV name --(normalised, uniqueness asserted)--> BOARD player --> `key` --> store row BY KEY.
Never name->store.  Never substring.  Never fuzzy.  Unmatched or ambiguous HALTs, naming the players.

EXACT BYTES (seam-binding, 2026-07-30).  The store takes the owner's bytes VERBATIM — no
canonicalisation, no case-folding.  The store and the CSV both carry 'Free agents' x73 and
'Free Agents' x2 and the two splits align row-for-row; applying the UI lane's display normalisation on
the way IN would rewrite 2 extra rows that the owner never edited, making them seat-authored and
inflating the change set from 18 to 20.  Canonicalise for the MIRROR (extract_board_view.norm_club /
ingest_inputs.normt), NEVER for the store.

CLI:
  python3 ui/tools/ownership_store_apply.py preflight   # read-only: gates + the plan, no writes
  python3 ui/tools/ownership_store_apply.py apply       # the transaction (no-op if already current)
  python3 ui/tools/ownership_store_apply.py verify      # assert the live tree is coherent (no writes)
"""
import collections
import csv
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# THE MIRROR'S OWN NORMALISER, imported rather than copied (2026-08-20; preregistered at
# docs/evidence/landing_tail_2026-08-20/PREREG_MIRROR_CASING_FIX.md). The staged validation below
# compares the generated mirrors against the plan. The STORE holds the owner's bytes verbatim and the
# MIRRORS hold the display-normalised form — this file's own seam-binding law of 2026-07-30 says so
# ("Canonicalise for the MIRROR (extract_board_view.norm_club / ingest_inputs.normt), NEVER for the
# store") — so a mirror comparison that reads the raw value is comparing two different lanes. It was
# latent from #283 until the owner's 2026-08-20 sheet moved 14 players TO the lowercase spelling
# 'Free agents': the mirror correctly wrote 'Free Agents', the comparison demanded 'Free agents', and
# the SAME BLOCK's next assertion ("free-agent spelling forked in the mirror") demanded the opposite —
# two assertions no mirror could satisfy at once. Imported, not re-implemented, so there is exactly
# one definition of the normalisation and this can never drift from the writer that applies it.
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from extract_board_view import norm_club as _mirror_club    # noqa: E402

STORE_REL = os.path.join("engine", "rl_after", "rl_model_data.json")
BOARD_REL = os.path.join("data", "rl_build", "rl_app_data.json")
SIDECAR_REL = BOARD_REL + ".srcmd5"
BOOT_REL = os.path.join("data", "expected_boot.json")
CONTRACT_REL = os.path.join("data", "release_contract.json")
SEASON_REL = os.path.join("data", "season_state.json")
LINEAGE_REL = os.path.join("data", "release_lineage.json")
CSV_REL = os.path.join("docs", "inputs", "AFFL_Player_Locations.csv")
BVW_REL = os.path.join("ui", "data", "board_view_working.js")
BVP_REL = os.path.join("ui", "data", "board_view_public.js")
OWNERSHIP_REL = os.path.join("ui", "data", "ownership.js")
CLUBVAL_REL = os.path.join("ui", "data", "club_valuation.js")
MOVERS_TRANSITION_REL = os.path.join("ui", "data", "movers_transition.js")

# The ten live targets, committed atomically (the store write is target 0).
TARGETS = (
    ("store", STORE_REL),
    ("manifest", BOOT_REL),
    ("release_contract", CONTRACT_REL),
    ("board_sidecar", SIDECAR_REL),
    ("season_state", SEASON_REL),
    ("board_view_working", BVW_REL),
    ("release_lineage", LINEAGE_REL),
    ("movers_transition", MOVERS_TRANSITION_REL),
    ("board_view_public", BVP_REL),
    ("ownership_sidecar", OWNERSHIP_REL),
    ("club_valuation", CLUBVAL_REL),
)

# Directories the throwaway overlay needs to be a working repo root for the two generators.
OVERLAY_DIRS = ("data", "docs", "ui", os.path.join("engine", "rl_after"))

OWNER_RULING_ID = "OWNERSHIP_SINGLE_SOURCE_2026-07-30"
OWNER_RULING = ('2026-07-30, owner ruling on #283: the store becomes the single source of ownership '
                'truth; the ingest writes the CSV\'s ownership into the store\'s affl_team '
                '(owner authorship by courier), and the #232 sidecar survives as a generated mirror '
                'rebuilt FROM the store, never independently authoritative.')
AUTHORITY = "Luke McAlister (owner) — sole merge authority; relayed by the seam on #283"


class Halt(Exception):
    """Fail closed. Nothing is guessed; nothing is written on an ambiguous or incoherent tree."""


def _md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def _md5_file(path):
    with open(path, "rb") as f:
        return _md5_bytes(f.read())


def nkey(s):
    """The ingest's own normalised name key, character-for-character (ui/tools/ingest_inputs.py).
    Collapse whitespace + casefold: resolves the case-only surname variants without guessing, and
    still keeps the two Max Kings distinct ('max king' != 'maxwell king')."""
    return " ".join(str(s).strip().split()).casefold()


def _readcsv(path):
    """The ingest's own encoding ladder. CRLF in the owner's lane is a known Excel artifact and is
    never 'fixed' — csv.reader consumes it and the file is never rewritten by this tool."""
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return list(csv.reader(f)), enc
        except UnicodeDecodeError:
            continue
    raise Halt("could not decode %s as utf-8/cp1252/latin-1" % os.path.basename(path))


def _bundle_obj(path):
    """Parse a `window.__X__ = {...};` bundle into its dict."""
    t = open(path, encoding="utf-8").read()
    return json.loads(t[t.index("{"):t.rindex("}") + 1])


# ------------------------------------------------------------------ preflight (P1-P8, reads only)
class Plan(object):
    def __init__(self, rows, store_raw, store_new, md5_before, md5_after, board_md5, csv_encoding,
                 root=None):
        self.root = root                  # the LIVE repo root, so validation can compare against it
        self.rows = rows                  # [(key, name, from_club, to_club)]
        self.store_raw = store_raw
        self.store_new = store_new
        self.md5_before = md5_before
        self.md5_after = md5_after
        self.board_md5 = board_md5
        self.csv_encoding = csv_encoding

    @property
    def moves(self):
        return self.md5_before != self.md5_after


def preflight(root, verbose=True):
    """P1-P8. Every gate reads; none writes. Returns a Plan or raises Halt."""
    out = (lambda *a: print(*a)) if verbose else (lambda *a: None)

    # -- P1 the pinned interpreter -------------------------------------------------------------
    if sys.version_info[:2] != (3, 12):
        raise Halt("PINNED INTERPRETER: cp312 required (RL_VENV); this is %d.%d. The container python3 "
                   "is 3.11 and is refused." % sys.version_info[:2])
    out("  [P1] interpreter cp%d%d — pinned" % sys.version_info[:2])

    p = lambda rel: os.path.join(root, rel)
    for rel in (STORE_REL, BOARD_REL, SIDECAR_REL, BOOT_REL, CONTRACT_REL, SEASON_REL,
                LINEAGE_REL, CSV_REL, BVW_REL, MOVERS_TRANSITION_REL):
        if not os.path.exists(p(rel)):
            raise Halt("missing required file: %s" % rel)

    # -- P3 six-way INCOMING coherence ---------------------------------------------------------
    # The write is refused on an incoherent base: if the tree already disagrees with itself about
    # which store it is on, moving the pin would paper over the disagreement instead of surfacing it.
    store_raw = open(p(STORE_REL), "rb").read()
    md5_before = _md5_bytes(store_raw)
    boot = json.load(open(p(BOOT_REL)))
    contract = json.load(open(p(CONTRACT_REL)))
    season = json.load(open(p(SEASON_REL)))
    sidecar = json.load(open(p(SIDECAR_REL)))
    bvw = _bundle_obj(p(BVW_REL))
    seen = {
        "store file": md5_before,
        "expected_boot.store": str(boot.get("store") or ""),
        "release_contract.identities.store": str((contract.get("identities") or {}).get("store") or ""),
        "season_state.source_store_md5": str(season.get("source_store_md5") or ""),
        "rl_app_data.json.srcmd5.source_md5": str(sidecar.get("source_md5") or ""),
        "board_view_working.stamp.store_md5": str((bvw.get("stamp") or {}).get("store_md5") or ""),
    }
    if len(set(seen.values())) != 1:
        raise Halt("INCOHERENT BASE — the six store-identity carriers disagree BEFORE any write:\n    "
                   + "\n    ".join("%-38s %s" % (k, v) for k, v in seen.items()))
    out("  [P3] six-way incoming coherence — all read %s" % md5_before[:8])

    # -- P8 serializer identity gate -----------------------------------------------------------
    # The store is one line, default separators. If a load->dump round trip is not the identity, a
    # write would reformat all 2,651 rows and "the diff is affl_team only" would stop being provable.
    store_doc = json.loads(store_raw)
    if json.dumps(store_doc).encode() != store_raw:
        raise Halt("SERIALIZER DRIFT: json.dumps(json.loads(store)) != store bytes. The write is "
                   "refused rather than reformat the store.")
    out("  [P8] serializer identity — dumps(loads(store)) == store bytes (%d bytes)" % len(store_raw))

    # store key uniqueness (the join's other half)
    by_key = {}
    for r in store_doc:
        k = r.get("key")
        if not k:
            continue
        if k in by_key:
            raise Halt("store key collision: %r appears more than once" % k)
        by_key[k] = r
    out("  [--] store rows %d · distinct keys %d · rows carrying affl_team %d"
        % (len(store_doc), len(by_key), sum(1 for r in store_doc if "affl_team" in r)))

    # -- board universe, name-unique (the ingest's own assertion) -------------------------------
    board_md5 = _md5_file(p(BOARD_REL))
    if board_md5 != str(boot.get("board") or ""):
        raise Halt("board pin mismatch: board %s != expected_boot.board %s"
                   % (board_md5[:8], str(boot.get("board"))[:8]))
    players = bvw.get("players") or []
    bb = collections.defaultdict(list)
    for pl in players:
        bb[nkey(pl["name"])].append(pl)
    ambiguous = sorted(k for k, v in bb.items() if len(v) > 1)
    if ambiguous:
        raise Halt("board name-join keys ambiguous (the join is refused, never disambiguated by "
                   "guessing): %s" % ambiguous)
    out("  [--] board players %d · ambiguous board name-keys 0 · board md5 %s"
        % (len(players), board_md5[:8]))

    # -- P4 the CSV ----------------------------------------------------------------------------
    rows, enc = _readcsv(p(CSV_REL))
    body = [r for r in rows[1:] if r and r[0].strip()]
    if len(rows) != 805 or len(body) != 804:
        raise Halt("CSV shape: expected 805 lines = 1 header + 804 players, got %d lines / %d data rows"
                   % (len(rows), len(body)))
    out("  [P4] CSV %s · %d lines = 1 header + %d players (CRLF preserved, never 'fixed')"
        % (enc, len(rows), len(body)))

    # -- P5 the join: CSV name -> board player -> key -> store row BY KEY -----------------------
    unmatched, no_store_row = [], []
    resolved = []
    for r in body:
        k = nkey(r[0])
        m = bb.get(k)
        if not m:
            unmatched.append(r[0])
            continue
        key = m[0]["key"]
        if key not in by_key:
            no_store_row.append((r[0], key))
            continue
        resolved.append((key, r[0], r[1].strip()))
    if unmatched or no_store_row:
        raise Halt("NAME JOIN FAILED (validate-or-halt; never widened to fuzzy matching)\n"
                   "    unmatched in the board universe: %s\n"
                   "    board key absent from the store : %s" % (unmatched or "none", no_store_row or "none"))
    out("  [P5] join by key — 0 unmatched, 0 board keys missing from the store, %d resolved"
        % len(resolved))

    # -- P6 club spellings ---------------------------------------------------------------------
    known = {pl.get("affl_team") for pl in players if pl.get("affl_team")}
    # the store's own spellings are equally legitimate: the display lane canonicalises casing, the
    # store does not, so BOTH free-agent spellings are permitted here by construction.
    known |= {r.get("affl_team") for r in store_doc if r.get("affl_team")}
    unknown = sorted({c for _, _, c in resolved if c not in known})
    if unknown:
        raise Halt("unknown AFFL club spelling(s) %s — an unknown club would split silently in the UI"
                   % unknown)
    out("  [P6] club spellings — all %d authored values are known spellings" % len(resolved))

    # -- P7 the exact-byte plan ----------------------------------------------------------------
    plan_rows = []
    for key, name, new_club in resolved:
        cur = by_key[key].get("affl_team")
        if cur != new_club:
            plan_rows.append((key, name, cur, new_club))
    plan_rows.sort()

    for key, _name, _cur, new_club in plan_rows:
        by_key[key]["affl_team"] = new_club        # EXACT BYTES — no canonicalisation (seam-binding)
    store_new = json.dumps(store_doc).encode()
    md5_after = _md5_bytes(store_new)

    out("  [P7] plan — %d of %d authored rows move (of %d store rows; %d carry affl_team)"
        % (len(plan_rows), len(body), len(store_doc), sum(1 for r in store_doc if "affl_team" in r)))
    for key, name, cur, new in plan_rows:
        out("         %-24s %-24s %-26s -> %s" % (key, name, cur, new))
    out("  [--] store md5 %s -> %s%s" % (md5_before[:8], md5_after[:8],
                                         "  (NO-OP)" if md5_before == md5_after else ""))
    return Plan(plan_rows, store_raw, store_new, md5_before, md5_after, board_md5, enc, root=root)


# ------------------------------------------------------------------------------- the diff proof
def assert_store_diff_is_affl_team_only(old_bytes, new_bytes, expect_keys):
    """T2. Structural, key-by-key over every store row: ONLY `affl_team`, ONLY on the expected keys,
    every other field byte-identical. Then byte-attribution: re-deriving the new bytes from the old
    document with only those substitutions must reproduce the new bytes exactly."""
    old, new = json.loads(old_bytes), json.loads(new_bytes)
    if len(old) != len(new):
        raise Halt("store row count moved: %d -> %d" % (len(old), len(new)))
    moved = set()
    for a, b in zip(old, new):
        if a.get("key") != b.get("key"):
            raise Halt("store row order moved at key %r / %r" % (a.get("key"), b.get("key")))
        if list(a.keys()) != list(b.keys()):
            raise Halt("store row %r field set moved" % a.get("key"))
        for f in a:
            if a[f] != b[f]:
                if f != "affl_team":
                    raise Halt("store diff touched %r on row %r — this job moves affl_team only"
                               % (f, a.get("key")))
                moved.add(a.get("key"))
    if moved != set(expect_keys):
        raise Halt("store diff key set %s != planned %s" % (sorted(moved), sorted(expect_keys)))
    # byte-attribution
    reapplied = json.loads(old_bytes)
    idx = {r.get("key"): r for r in reapplied}
    for k in expect_keys:
        idx[k]["affl_team"] = {r.get("key"): r for r in new}[k]["affl_team"]
    if json.dumps(reapplied).encode() != new_bytes:
        raise Halt("byte-attribution failed: old bytes + only the planned affl_team substitutions "
                   "do not reproduce the new store bytes")
    return len(moved)


# ------------------------------------------------------------------------------ the pin movers
def restamp_manifest(path, store_md5):
    """Surgically move expected_boot's `store` pin; every other byte preserved. Stronger than the
    weekly lane's version: the pattern must occur EXACTLY ONCE in the whole file, so a second
    `"store":` key could never be silently passed over by a count=1 substitution."""
    text = open(path).read()
    pat = r'("store":\s*")[0-9a-f]{32}(")'
    hits = re.findall(pat, text)
    if len(hits) != 1:
        raise Halt("expected_boot re-stamp: expected exactly 1 'store' pin, found %d" % len(hits))
    text = re.sub(pat, lambda m: m.group(1) + store_md5 + m.group(2), text, count=1)
    _atomic_write_text(path, text)


def restamp_board_sidecar(path, store_md5, expect_own_md5):
    """Move the Guard-2 source stamp; assert the board's OWN content hash is untouched (the board
    does not move in this job, and this is where that claim is enforced rather than asserted)."""
    d = json.load(open(path))
    if str(d.get("own_md5")) != expect_own_md5:
        raise Halt("board sidecar own_md5 %s != live board md5 %s" % (d.get("own_md5"), expect_own_md5))
    d["source_md5"] = store_md5
    _atomic_write_text(path, json.dumps(d, sort_keys=True))


def restamp_season_state(path, store_md5):
    """Move `source_store_md5` ONLY. calendar_progress / exposure_pace / exposure_derivation are
    derived from GAMES, not ownership, and are asserted byte-unchanged here rather than assumed."""
    raw = open(path).read()
    d = json.loads(raw)
    before = {k: json.dumps(d.get(k), sort_keys=True)
              for k in ("calendar_progress", "exposure_pace", "exposure_derivation",
                        "as_of_round", "season_year", "season_total_rounds", "derivation_policy_id")}
    d["source_store_md5"] = store_md5
    after = {k: json.dumps(d.get(k), sort_keys=True) for k in before}
    if before != after:
        raise Halt("season_state derived values moved under an ownership write: %s"
                   % [k for k in before if before[k] != after[k]])
    _atomic_write_text(path, json.dumps(d, indent=1) + "\n" if raw.endswith("\n") else json.dumps(d, indent=1))
    return before


def append_transition(lineage_path, movers_path, store_before, store_after, board_md5,
                      release_version, as_of_round):
    """T5/T6. Append ONE release_transition_register entry — the out-of-round shape the register's own
    _doc prescribes — and write the byte-identical UI mirror. The top-level present-lens baseline
    (balanced_board_md5 06d8af60) and release_version are asserted UNMOVED: round_movers._release_baseline()
    reads them every round and hard-errors on absence."""
    raw = open(lineage_path).read()
    d = json.loads(raw)
    base_balanced = d.get("balanced_board_md5")
    base_version = d.get("release_version")
    reg = d.get("release_transition_register")
    if not isinstance(reg, list) or not reg:
        raise Halt("release_lineage.release_transition_register missing or empty")
    prev = reg[-1]
    prev_dest = (prev.get("destination") or {})
    if str(prev_dest.get("store")) != store_before:
        raise Halt("register tail destination.store %s != the store being superseded %s"
                   % (prev_dest.get("store"), store_before))

    entry = collections.OrderedDict()
    entry["_doc"] = ("OUT-OF-ROUND OWNERSHIP STORE WRITE (#283). The owner's AFFL ownership CSV is "
                     "couriered into the store's affl_team; the #232 sidecar becomes a generated mirror "
                     "rebuilt FROM the store. Appended, not substituted: every prior entry is preserved "
                     "verbatim. The BOARD DOES NOT MOVE — affl_team is not in the board of record (128 "
                     "lensPicks keys, all null; the 804 active rows do not carry it), so this is an "
                     "identity-only transition with no engine build. Per this register's own law an "
                     "APPENDED entry is the shape prescribed for an out-of-round move.")
    entry["kind"] = "movers_release_transition"
    entry["schema_version"] = prev.get("schema_version", 2)
    entry["owner_approved"] = True
    entry["owner_ruling_id"] = [OWNER_RULING_ID]
    entry["owner_ruling"] = OWNER_RULING
    entry["authority"] = AUTHORITY
    # NO `board` KEY ON source/destination — deliberately, and this is load-bearing.
    # round_movers.model_changes() keys the register by `destination.board` and lets a LATER entry
    # supersede an earlier one describing the same landing board. This transition does not move the
    # board, so declaring one would make this entry hijack the board boundary that already belongs to
    # the #271 Addendum 17 record and overwrite its owner_ruling_id — an out-of-round STORE move
    # silently stealing the attribution of an out-of-round BOARD move. model_changes' own law is the
    # remedy: "a register entry that carries no destination board is a pointer note, not a record, and
    # contributes nothing". That is exactly what a store-only transition is to the boundary reader.
    # The board is still recorded, as the invariant it actually is: unmoved.
    entry["source"] = collections.OrderedDict(
        [("release_version", release_version), ("store", store_before), ("as_of_round", as_of_round)])
    entry["destination"] = collections.OrderedDict(
        [("release_version", release_version), ("store", store_after), ("as_of_round", as_of_round)])
    entry["invariants"] = collections.OrderedDict([
        ("store_moved_by_transition", {"from": store_before, "to": store_after}),
        ("board_unmoved_by_transition", board_md5),
        ("declares_no_landing_board",
         "this transition moves the STORE only; it is a pointer note to the boundary reader and must "
         "never supersede a board-boundary record (round_movers.model_changes)"),
        ("fields_written", "affl_team only"),
        ("engine_build", "none — affl_team is not read by ev() and is absent from the board of record"),
    ])
    reg.append(entry)

    if d.get("balanced_board_md5") != base_balanced or d.get("release_version") != base_version:
        raise Halt("release_lineage top-level present-lens baseline moved — it must never move")
    _atomic_write_text(lineage_path, json.dumps(d, indent=1) + ("\n" if raw.endswith("\n") else ""))

    # The UI mirror. Its SHAPE is prescribed by test_movers_transition.py and is not free: the payload is
    # the `release_transition` object's OWN FIELDS spread at top level, plus the register key, and
    # NOTHING else ("zero authorship"). It is written with compact separators and ensure_ascii=False
    # because the transition's serialisation must be a BYTE-VERBATIM PREFIX of the payload — that is how
    # "the ITEM 408 record is never rewritten" is asserted on bytes rather than on parsed equality.
    # Building it as {**transition, register: ...} puts the transition's keys first, which is what makes
    # the prefix property hold rather than merely happen to hold.
    mraw = open(movers_path, encoding="utf-8").read()
    head = mraw[:mraw.index("{")]
    tail = mraw[mraw.rindex("}") + 1:]
    payload = dict(d["release_transition"])
    payload["release_transition_register"] = reg
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    prefix = json.dumps(d["release_transition"], ensure_ascii=False, separators=(",", ":"))[:-1]
    if not text.startswith(prefix):
        raise Halt("movers mirror: the ITEM 408 transition record is not a byte-verbatim prefix of the "
                   "payload — it must never be rewritten")
    _atomic_write_text(movers_path, head + text + tail, encoding="utf-8")
    return entry


def _atomic_write_text(path, text, encoding="utf-8"):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".osa_tmp_", dir=d)
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _load_release_contract_module(root):
    p = os.path.join(root, "release_contract.py")
    spec = importlib.util.spec_from_file_location("release_contract_osa", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------------- the overlay
def _build_overlay(root, dest):
    for rel in OVERLAY_DIRS:
        src = os.path.join(root, rel)
        dst = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copytree(src, dst)
    for name in ("release_contract.py", "season_state.py"):
        s = os.path.join(root, name)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(dest, name))


def _run(cmd, cwd, env=None, label=""):
    e = dict(os.environ)
    e.update(env or {})
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True)
    if r.returncode != 0:
        raise Halt("%s FAILED rc=%s\n--- stdout ---\n%s\n--- stderr ---\n%s"
                   % (label or cmd[0], r.returncode, r.stdout[-4000:], r.stderr[-4000:]))
    return r.stdout


# ------------------------------------------------------------------------------ the transaction
def apply(root=None, verbose=True):
    """T0-T10. Returns 'NOOP' or 'APPLIED'. Nothing live is touched until the atomic commit."""
    root = os.path.abspath(root or DEFAULT_ROOT)
    out = (lambda *a: print(*a)) if verbose else (lambda *a: None)
    out("\n  #283 OWNERSHIP STORE APPLY — out-of-round transaction (seam Ruling 1, 2026-07-30)")
    out("  " + "-" * 78)
    plan = preflight(root, verbose=verbose)

    if not plan.moves:
        out("\n  NO-OP — the store already carries the authored ownership; no pin moves, no register "
            "entry appended.")
        return "NOOP"

    boot = json.load(open(os.path.join(root, BOOT_REL)))
    release_version = boot.get("release_version")
    as_of_round = boot.get("as_of_round")

    tmp = tempfile.mkdtemp(prefix="osa_overlay_")
    try:
        ws = os.path.join(tmp, "repo")
        os.makedirs(ws)
        _build_overlay(root, ws)
        w = lambda rel: os.path.join(ws, rel)
        out("\n  [T0] overlay staged (the live tree is untouched until the atomic commit)")

        # T1 the store write
        _atomic_write_bytes(w(STORE_REL), plan.store_new)
        out("  [T1] store written — %s -> %s" % (plan.md5_before[:8], plan.md5_after[:8]))

        # T2 the diff proof
        n = assert_store_diff_is_affl_team_only(plan.store_raw, plan.store_new,
                                                [r[0] for r in plan.rows])
        out("  [T2] store diff proof — affl_team only, on exactly %d planned keys; byte-attribution OK" % n)

        # T3 the pin moves
        restamp_manifest(w(BOOT_REL), plan.md5_after)
        restamp_board_sidecar(w(SIDECAR_REL), plan.md5_after, plan.board_md5)
        season_frozen = restamp_season_state(w(SEASON_REL), plan.md5_after)
        rc = _load_release_contract_module(ws)
        season_doc = json.load(open(w(SEASON_REL)))
        rc.restamp_dynamic(ws, as_of_round, plan.md5_after, plan.board_md5, season_doc)
        out("  [T3] pins moved — expected_boot.store · release_contract.identities.store + re-seal · "
            "season_state.source_store_md5 · board srcmd5.source_md5")
        out("       season derived values proven unchanged: calendar_progress=%s exposure_pace=%s"
            % (season_frozen["calendar_progress"], season_frozen["exposure_pace"]))

        # T4 the board is unmoved
        if _md5_file(w(BOARD_REL)) != plan.board_md5:
            raise Halt("the board of record moved — impossible in this job")
        out("  [T4] board unmoved — %s byte-identical (no engine build)" % plan.board_md5[:8])

        # T5/T6 the transition entry + its mirror
        append_transition(w(LINEAGE_REL), w(MOVERS_TRANSITION_REL), plan.md5_before, plan.md5_after,
                          plan.board_md5, release_version, as_of_round)
        out("  [T5] release_transition_register entry appended (ruling id %s)" % OWNER_RULING_ID)
        out("  [T6] movers_transition.js mirror written byte-identically")

        # T7 the board_view bundles (the ring-fence now passes against the moved pin).
        # BOTH HALVES OF THE PAIR, ALWAYS: extract_board_view REGENERATES the bundle and DROPS
        # `stamp.release`; only round_movers.inject_release_contract puts it back (the landing's
        # writers 1+2, steps.py ui). This tool ran only the first half until 2026-08-28 — the
        # FOURTH strike of the thrice-proven trap, caught by release_manifest_check + three ui
        # suites on the first apply after the release block moved into the working stamp.
        _run([sys.executable, os.path.join(ws, "ui", "tools", "extract_board_view.py")], cwd=ws,
             label="extract_board_view")
        import importlib.util as _ilu
        _rm_path = os.path.join(ws, "engine", "rl_after", "ingestion", "round_movers.py")
        _spec = _ilu.spec_from_file_location("_osa_round_movers", _rm_path)
        _rm = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_rm)
        _boot = json.load(open(os.path.join(ws, "data", "expected_boot.json")))
        _rm.inject_release_contract(os.path.join(ws, BVW_REL), ws, int(_boot["as_of_round"]))
        out("  [T7] board_view_{working,public}.js regenerated + the release block re-injected "
            "(both halves of the writer pair)")

        # T8 the mirrors: sidecar + club_valuation, generated FROM the store
        _run([sys.executable, os.path.join(ws, "ui", "tools", "ingest_inputs.py")], cwd=ws,
             env={"RL_OSA_SKIP": "1"}, label="ingest_inputs")
        out("  [T8] ownership.js (generated mirror) + club_valuation.js regenerated from the store")

        # T9 overlay validation
        _validate_overlay(ws, plan, out)

        # T10 atomic commit
        _commit(root, ws, out)
        out("\n  APPLIED — %d ownership moves landed; %d targets committed atomically."
            % (len(plan.rows), len(TARGETS)))
        return "APPLIED"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _atomic_write_bytes(path, data):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".osa_tmp_", dir=d)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _validate_overlay(ws, plan, out):
    """T9. The complete staged set at once — identity coherence across every target, the contract
    self-seal, the lineage<->mirror byte-identity, and the two bundles' shape."""
    w = lambda rel: os.path.join(ws, rel)
    fails = []

    seen = {
        "store file": _md5_file(w(STORE_REL)),
        "expected_boot.store": str(json.load(open(w(BOOT_REL))).get("store") or ""),
        "release_contract.identities.store":
            str((json.load(open(w(CONTRACT_REL))).get("identities") or {}).get("store") or ""),
        "season_state.source_store_md5": str(json.load(open(w(SEASON_REL))).get("source_store_md5") or ""),
        "rl_app_data.json.srcmd5.source_md5": str(json.load(open(w(SIDECAR_REL))).get("source_md5") or ""),
        "board_view_working.stamp.store_md5":
            str((_bundle_obj(w(BVW_REL)).get("stamp") or {}).get("store_md5") or ""),
    }
    if set(seen.values()) != {plan.md5_after}:
        fails.append("staged store-identity carriers disagree: %s" % seen)

    if _md5_file(w(BOARD_REL)) != plan.board_md5:
        fails.append("staged board moved")
    if str(json.load(open(w(SIDECAR_REL))).get("own_md5")) != plan.board_md5:
        fails.append("staged board sidecar own_md5 moved")

    rc = _load_release_contract_module(ws)
    c = json.load(open(w(CONTRACT_REL)))
    stored = c.get("contract_sha256")
    recomputed = rc.contract_hash({k: v for k, v in c.items() if k != "contract_sha256"})
    if stored != recomputed:
        fails.append("release_contract self-seal %s != recomputed %s" % (stored, recomputed))

    lin = json.load(open(w(LINEAGE_REL)))
    mov = _bundle_obj(w(MOVERS_TRANSITION_REL))
    # The mirror's shape is prescribed by test_movers_transition.py: the transition's own fields at top
    # level PLUS the register, and nothing else. Checked here rather than left to CI, because getting it
    # wrong produces a file that parses, looks plausible, and fails a suite three steps later.
    if set(mov) != set(lin["release_transition"]) | {"release_transition_register"}:
        fails.append("movers mirror carries keys the lineage does not: %s"
                     % sorted(set(mov) ^ (set(lin["release_transition"]) | {"release_transition_register"})))
    if json.dumps({k: v for k, v in mov.items() if k != "release_transition_register"}, sort_keys=True) \
            != json.dumps(lin["release_transition"], sort_keys=True):
        fails.append("movers mirror transition != lineage release_transition")
    if json.dumps(mov.get("release_transition_register"), sort_keys=True) \
            != json.dumps(lin.get("release_transition_register"), sort_keys=True):
        fails.append("movers mirror register != lineage register")
    _mtext = open(w(MOVERS_TRANSITION_REL), encoding="utf-8").read()
    _payload = _mtext[_mtext.index("{"):_mtext.rindex("}") + 1]
    if not _payload.startswith(json.dumps(lin["release_transition"], ensure_ascii=False,
                                          separators=(",", ":"))[:-1]):
        fails.append("the ITEM 408 record is not preserved byte-verbatim as the mirror payload's prefix")

    # THE BOUNDARY LABELS MUST NOT MOVE. A store-only transition is invisible to the boundary reader by
    # design; if appending it changes what round_movers.model_changes() derives, this entry has claimed
    # a board boundary that is not its own — which is how it would silently overwrite another record's
    # owner_ruling_id. Compared against the LIVE tree's derivation and against the shipped movers bundle,
    # so neither "the reader moved" nor "the bundle went stale" can pass.
    try:
        sys.path.insert(0, os.path.join(ws, "engine", "rl_after", "ingestion"))
        import round_movers as _MV
        importlib.reload(_MV)
        staged_mc = _MV.model_changes(ws)
        shipped_mc = _bundle_obj(w(os.path.join("ui", "data", "movers.js"))).get("model_changes") or []
        if json.dumps(staged_mc, sort_keys=True) != json.dumps(shipped_mc, sort_keys=True):
            fails.append("appending this entry MOVED the derived boundary labels — a store-only "
                         "transition must be invisible to model_changes()")
    except Exception as e:                                        # noqa: BLE001
        fails.append("could not verify model_changes invariance: %s" % e)
    finally:
        if os.path.join(ws, "engine", "rl_after", "ingestion") in sys.path:
            sys.path.remove(os.path.join(ws, "engine", "rl_after", "ingestion"))
    if lin.get("balanced_board_md5") != "06d8af60b679a12db07c064c60c065f9":
        fails.append("release_lineage top-level present-lens baseline moved")
    # APPEND-ONLY, exactly one: compare against the LIVE register's length rather than a hardcoded
    # count, so this stays true for the next out-of-round write as well as this one.
    live_n = len(json.load(open(os.path.join(plan.root, LINEAGE_REL)))["release_transition_register"])
    staged_n = len(lin["release_transition_register"])
    if staged_n != live_n + 1:
        fails.append("expected exactly ONE appended register entry (%d -> %d), got %d"
                     % (live_n, live_n + 1, staged_n))
    if json.dumps(lin["release_transition_register"][:live_n], sort_keys=True) != json.dumps(
            json.load(open(os.path.join(plan.root, LINEAGE_REL)))["release_transition_register"],
            sort_keys=True):
        fails.append("the pre-existing register entries were not preserved verbatim")

    # the mirrors carry the moves, and the free-agent split does not fork a club
    own = _bundle_obj(w(OWNERSHIP_REL))
    bvw = _bundle_obj(w(BVW_REL))
    bvp = _bundle_obj(w(BVP_REL))
    by_key = {p["key"]: p for p in bvw["players"]}
    # Compared THROUGH the mirror's own normaliser, on BOTH sides. The store keeps the owner's raw
    # bytes (asserted separately and exactly by the T2 diff proof, which is untouched); the mirrors
    # carry the display form. `_mirror_club` collapses exactly one documented casing pair and nothing
    # else, so a mirror that genuinely failed to take a move still fails here — this is consistency,
    # not leniency, and the "free-agent spelling forked in the mirror" assertion below is unchanged.
    for key, name, _cur, new in plan.rows:
        if _mirror_club(by_key.get(key, {}).get("affl_team")) != _mirror_club(new):
            fails.append("board_view_working did not take the move for %s" % key)
        if _mirror_club(own["byKey"].get(key)) != _mirror_club(new):
            fails.append("ownership mirror did not take the move for %s" % key)
    clubs = {p.get("affl_team") for p in bvw["players"] if p.get("affl_team")}
    if len(clubs) != 17:
        fails.append("expected 16 clubs + Free Agents = 17 buckets, got %d: %s" % (len(clubs), sorted(clubs)))
    if any(c and c.lower() == "free agents" and c != "Free Agents" for c in clubs):
        fails.append("free-agent spelling forked in the mirror")
    # Leak check on the public bundle's actual FIELD NAMES, never on a substring of its text: the
    # players include Nick Blakey and Nick Larkey and the position label "Key Fwd", so a substring
    # test for "key" reports a leak that is not there. Identity fields must be absent as fields.
    banned = {"key", "slug", "store", "store_md5", "srcmd5", "board_md5", "balanced_board_md5",
              "source_md5", "board", "engine", "guard5", "ov", "levers", "lti_reg"}
    pub_fields = set(bvp.get("stamp") or {})
    for pl in bvp.get("players") or []:
        pub_fields |= set(pl)
    leak = sorted(banned & pub_fields)
    if leak:
        fails.append("public bundle leaks identity field(s) %s" % leak)

    if fails:
        raise Halt("STAGED VALIDATION FAILED (nothing committed):\n    - " + "\n    - ".join(fails))
    out("  [T9] staged validation PASS — 6-way coherence on %s · contract re-sealed · lineage mirror "
        "byte-identical · 17 buckets · public bundle clean" % plan.md5_after[:8])


def _commit(root, ws, out):
    """T10. Journal + per-target backup, atomic replace of every target, byte-for-byte rollback on
    any fault. The ten targets land together or not at all."""
    backup = tempfile.mkdtemp(prefix="osa_backup_")
    done = []
    try:
        for name, rel in TARGETS:
            live = os.path.join(root, rel)
            if os.path.exists(live):
                b = os.path.join(backup, name)
                shutil.copy2(live, b)
        for name, rel in TARGETS:
            src, live = os.path.join(ws, rel), os.path.join(root, rel)
            if not os.path.exists(src):
                raise Halt("staged target missing: %s" % rel)
            os.makedirs(os.path.dirname(live), exist_ok=True)
            shutil.copy2(src, live)
            done.append((name, rel))
        out("  [T10] committed atomically — %d targets" % len(done))
    except BaseException:
        for name, rel in done:
            b = os.path.join(backup, name)
            if os.path.exists(b):
                shutil.copy2(b, os.path.join(root, rel))
        out("  [T10] ROLLED BACK — every target restored byte-for-byte")
        raise
    finally:
        shutil.rmtree(backup, ignore_errors=True)


def verify(root=None, verbose=True):
    """Assert the LIVE tree is coherent. No writes, no build. Non-zero exit on any incoherence."""
    root = os.path.abspath(root or DEFAULT_ROOT)
    p = lambda rel: os.path.join(root, rel)
    store = _md5_file(p(STORE_REL))
    seen = {
        "store file": store,
        "expected_boot.store": str(json.load(open(p(BOOT_REL))).get("store") or ""),
        "release_contract.identities.store":
            str((json.load(open(p(CONTRACT_REL))).get("identities") or {}).get("store") or ""),
        "season_state.source_store_md5": str(json.load(open(p(SEASON_REL))).get("source_store_md5") or ""),
        "rl_app_data.json.srcmd5.source_md5": str(json.load(open(p(SIDECAR_REL))).get("source_md5") or ""),
        "board_view_working.stamp.store_md5":
            str((_bundle_obj(p(BVW_REL)).get("stamp") or {}).get("store_md5") or ""),
    }
    ok = len(set(seen.values())) == 1
    if verbose:
        for k, v in seen.items():
            print("  %-38s %s" % (k, v))
        print("  six-way store coherence: %s" % ("PASS" if ok else "FAIL"))
    if not ok:
        raise Halt("live tree store identity is incoherent")
    return store


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "preflight"
    root = DEFAULT_ROOT
    try:
        if cmd == "preflight":
            preflight(root)
        elif cmd == "apply":
            apply(root)
        elif cmd == "verify":
            verify(root)
        else:
            print(__doc__)
            return 2
    except Halt as e:
        print("\n  HALT — %s" % e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
