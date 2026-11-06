#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""#283 — OWNERSHIP STORE APPLY: the store-side acceptance proofs.

WHAT IS AT RISK.  This lane WRITES THE STORE — the one authored artifact the whole engine is derived
from — and then moves every identity pin the store md5 ripples into.  The failure that matters is not a
loud crash; it is a quiet one: a write that lands on the wrong player, a diff that carries a field
nobody meant to move, a pin left behind so two readers disagree, or a second register entry appended by
a re-run.  Each of those ships looking clean.

So every guard below is fired IN ANGER on a throwaway copy.  The live tree is never touched by this
file.  A guard that has never been seen to fail is not a guard.

Run: python3 ui/tests/ownership_store_apply.test.py
"""
import collections
import copy
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(REPO, "ui", "tools"))
import ownership_store_apply as OSA          # noqa: E402

PASS = [0]
FAIL = [0]


def check(ok, name, detail=""):
    if ok:
        PASS[0] += 1
        print("  [PASS] %s" % name)
    else:
        FAIL[0] += 1
        print("  [FAIL] %s%s" % (name, ("  — " + str(detail)) if detail else ""))


def halts(fn, name, want_substr=None):
    """Assert fn() raises Halt, and (optionally) that the message NAMES the cause."""
    try:
        fn()
    except OSA.Halt as e:
        if want_substr and want_substr.lower() not in str(e).lower():
            check(False, name, "halted, but the message did not name %r: %s" % (want_substr, str(e)[:160]))
            return
        check(True, name)
        return
    except Exception as e:                                    # noqa: BLE001
        check(False, name, "raised %s, not Halt: %s" % (type(e).__name__, e))
        return
    check(False, name, "did NOT halt — this guard cannot fail")


def sandbox():
    """A throwaway copy of everything the transaction reads. The live tree is never written here."""
    d = tempfile.mkdtemp(prefix="osa_test_")
    ws = os.path.join(d, "repo")
    os.makedirs(ws)
    OSA._build_overlay(REPO, ws)
    return d, ws


def write_json(path, doc):
    with open(path, "w") as f:
        json.dump(doc, f, indent=1)


print("\n#283 — ownership store apply (store side)")
print("-" * 72)

# ---------------------------------------------------------------- the shipped state
store_raw = open(os.path.join(REPO, OSA.STORE_REL), "rb").read()
store_doc = json.loads(store_raw)
live_md5 = OSA._md5_bytes(store_raw)

check(OSA.verify(REPO, verbose=False) == live_md5,
      "the LIVE tree is six-way store-coherent on %s" % live_md5[:8])

# P8 — the serializer identity, the fact that makes "the diff is affl_team only" provable at all
check(json.dumps(store_doc).encode() == store_raw,
      "serializer identity: dumps(loads(store)) == store bytes (%d bytes, one line)" % len(store_raw))

# the join's two halves
keys = [r.get("key") for r in store_doc if r.get("key")]
check(len(keys) == len(set(keys)) == len(store_doc),
      "store `key` is globally unique — %d of %d rows, no collisions" % (len(set(keys)), len(store_doc)))

# THE NAME-TWIN HAZARD, stated as data rather than as a worry (hazard class 13).
by_name = collections.defaultdict(list)
for r in store_doc:
    if r.get("key"):
        by_name[OSA.nkey(r.get("player") or "")].append(r["key"])
twin_names = {n: ks for n, ks in by_name.items() if len(ks) > 1}
bvw = OSA._bundle_obj(os.path.join(REPO, OSA.BVW_REL))
board_keys = {p["key"] for p in bvw["players"]}
board_twins = sorted(n for n, ks in twin_names.items() if any(k in board_keys for k in ks))
check(len(board_twins) > 0,
      "NAME-TWIN HAZARD IS REAL: %d board players share a normalised name with another store row (%s)"
      % (len(board_twins), ", ".join(board_twins)))
check("sam butler" in board_twins,
      "...and one of them (Sam Butler) is IN the 2026-07-29 change set — so a name->store join would "
      "have been a coin flip that still counted 18")

# ---------------------------------------------------------------- idempotency (acceptance 5)
# TWO FIELDS SINCE 2026-10-13 (Phase 0.3). The affl_team half must still be a NO-OP on the applied
# tree; the afl_club half may be PENDING until the owner runs `apply` — so it is asserted against an
# INDEPENDENT derivation (CSV `AFL Club` cell -> table -> store row by key) rather than against a
# hard-coded 15 that the first apply would make stale. `plan.moves` is then true iff either half is.
plan = OSA.preflight(REPO, verbose=False)
check(plan.md5_before == live_md5, "preflight on the live tree reads the live store")
_rows, _enc = OSA._readcsv(os.path.join(REPO, OSA.CSV_REL))
_i_club = OSA._column_index(_rows[0], OSA.AFL_CLUB_COLUMN)
_i_team = OSA._column_index(_rows[0], OSA.AFFL_TEAM_COLUMN)
_bvw_by_name = {OSA.nkey(p["name"]): p["key"] for p in bvw["players"]}
_store_by_key = {r["key"]: r for r in store_doc if r.get("key")}
_known_afl = {r.get("afl_club") for r in store_doc if r.get("afl_club")}
_expect_club, _expect_team = set(), set()
for _r in _rows[1:]:
    if not _r or not _r[0].strip():
        continue
    _full = OSA.afl_club_from_sheet(_r[_i_club] if _i_club < len(_r) else "", _known_afl)
    # the same two-step join the courier makes: the board first, else exactly one store row by name
    _k = _bvw_by_name.get(OSA.nkey(_r[0]))
    if _k is None:
        _cands = by_name.get(OSA.nkey(_r[0])) or []
        check(len(_cands) == 1 and _store_by_key[_cands[0]].get("_retired") is True,
              "off-board sheet row %r resolves to exactly one RETIRED store row (%s)" % (_r[0], _cands))
        _k = _cands[0]
    if _full is not None and _store_by_key[_k].get("afl_club") != _full:
        _expect_club.add((_k, _store_by_key[_k].get("afl_club"), _full))
    _team = _r[_i_team].strip() if _i_team < len(_r) else ""
    if _store_by_key[_k].get("affl_team") != _team:
        _expect_team.add((_k, _store_by_key[_k].get("affl_team"), _team))
# BOTH HALVES are asserted against an independent derivation (2026-11-06): the affl_team half used
# to be asserted a NO-OP on the applied tree, which stopped being true the day the owner's sheet
# first carried a delisted-but-owned player (retired in the store, no affl_team yet) — a real
# pending addition, not a defect.
check({(k, c, n) for k, _nm, c, n in plan.rows} == _expect_team,
      "the affl_team plan equals the independently derived (sheet != store) set — %d pending"
      % len(_expect_team))
check({(k, c, n) for k, _nm, c, n in plan.club_rows} == _expect_club,
      "the afl_club plan equals the independently derived (sheet != store) set — %d pending"
      % len(_expect_club))
check(all((k, f) in plan.added for k, fs in plan.planned.items() for f in fs if f not in _store_by_key[k])
      and all(f not in _store_by_key[k] for k, f in plan.added),
      "every planned move onto a row that LACKS the field is recorded as an addition, and no other is "
      "(%d addition(s))" % len(plan.added))
check(plan.moves == bool(plan.rows or plan.club_rows)
      and (plan.md5_after == live_md5) == (not plan.moves),
      "the store md5 budges iff a planned move exists in either field")
check(set(plan.planned) == {k for k, _nm, _c, _n in plan.rows} | {k for k, _nm, _c, _n in plan.club_rows}
      and all(set(v) <= set(OSA.COURIERED_FIELDS) for v in plan.planned.values()),
      "Plan.planned attributes every move to one of the two couriered fields and no third")

lin = json.load(open(os.path.join(REPO, OSA.LINEAGE_REL)))
reg = lin["release_transition_register"]
ours = [e for e in reg if OSA.OWNER_RULING_ID in (e.get("owner_ruling_id") or [])]
# DERIVED (2026-08-28, the S1 form): each ownership apply appends exactly ONE entry, so the count
# equals the number of DISTINCT store transitions recorded under the ruling — a hard-coded 1 went
# stale on the second-ever apply. A preflight re-run appending nothing is proven by the NO-OP
# check above; duplicates (two entries recording the SAME transition) are refused here.
_trans = [(e.get("source", {}).get("store"), e.get("destination", {}).get("store")) for e in ours]
check(len(ours) >= 1 and len(set(_trans)) == len(_trans),
      "every #283 entry records a DISTINCT store transition (n=%d; a re-run appends no duplicate)" % len(ours))
# THE ERA-BOUND ASSERT, corrected 2026-08-05 by the #328 re-closure (owner ruling OPTION A).
# This used to read `ours[0]["destination"]["store"] == live_md5`. That is true only while #283 is the
# LATEST store transition — it ties a SEALED HISTORICAL entry to a moving head, so the first legitimate
# store write after #283 turns a correct record into a red. #328 is that write (81d24704 -> f1e8c9fe),
# and the entry is still exactly right about its own transition. The check now asserts what the entry
# MEANS: that it records a real move, and that its own three statements of that move agree with each
# other. It still fails if the sealed entry is falsified in any of them.
_D283 = "81d2470440a80f72afea4405e94338c5"      # the store #283 produced — a historical constant
check(ours[0]["source"]["store"] != ours[0]["destination"]["store"]
      and ours[0]["destination"]["store"] == _D283
      and ours[0]["invariants"]["store_moved_by_transition"]["from"] == ours[0]["source"]["store"]
      and ours[0]["invariants"]["store_moved_by_transition"]["to"] == ours[0]["destination"]["store"],
      "the entry records the real transition and its own three statements of it agree")

# THE BOUNDARY-HIJACK REGRESSION.  round_movers.model_changes() keys the register by
# `destination.board` and lets a later entry supersede an earlier one for the same landing board.  A
# store-only transition that declared a board would therefore steal the board boundary already owned by
# the #271 Addendum 17 record and overwrite its owner_ruling_id — silently, with every suite still
# green except one.  It is caught here because it actually happened during this job's execution.
check("board" not in ours[0]["source"] and "board" not in ours[0]["destination"],
      "the #283 entry declares NO landing board — a store-only move is a pointer note to the boundary "
      "reader, never a board-boundary record")
# Same era-bound correction: this compared the sealed invariant to the LIVE expected_boot board. The
# #283 transition ran no engine build, so the board it names (f2df6e0a) is a fact about THAT moment,
# not a claim about today's head — #328 rebuilt the board (f2df6e0a -> 2b7c1a00) and the entry is
# unchanged and still true. Pinned to the historical constant, so falsifying the entry still fails.
check(ours[0]["invariants"]["board_unmoved_by_transition"] == "f2df6e0a2902f48e1df36f35493ba8c1",
      "...and records the board as the INVARIANT it is: unmoved across the transition (no engine build)")

sys.path.insert(0, os.path.join(REPO, "engine", "rl_after", "ingestion"))
import round_movers as MV                                  # noqa: E402
live_mc = MV.model_changes(REPO)
shipped_mc = OSA._bundle_obj(os.path.join(REPO, "ui", "data", "movers.js")).get("model_changes") or []
check(json.dumps(live_mc, sort_keys=True) == json.dumps(shipped_mc, sort_keys=True),
      "the derived boundary labels are UNMOVED by the append — reader and shipped bundle in step")
a17 = [c for c in live_mc if "ITEM_271_Addendum_17" in (c.get("owner_ruling_id") or [])]
check(len(a17) == 1,
      "the #271 Addendum 17 boundary still names ITS OWN ruling id — not overwritten by #283")
check(not any(OSA.OWNER_RULING_ID in (c.get("owner_ruling_id") or []) for c in live_mc),
      "#283 claims NO boundary label at all — it moved the store, not the board")
check(lin["balanced_board_md5"] == "06d8af60b679a12db07c064c60c065f9",
      "the immutable present-lens baseline (06d8af60) did not move — round_movers reads it every round")

mov = OSA._bundle_obj(os.path.join(REPO, OSA.MOVERS_TRANSITION_REL))
check(json.dumps(lin["release_transition_register"], sort_keys=True)
      == json.dumps(mov["release_transition_register"], sort_keys=True),
      "release_lineage and the movers_transition mirror are byte-identical")

# ---------------------------------------------------------------- F3, the exact-byte law
# The store and the CSV each carry BOTH free-agent spellings, aligned row-for-row. Folding them on the
# way in would author 2 rows the owner never edited. This asserts the split exists AND that display
# canonicalisation would really move those extra rows — so the law is load-bearing, not decorative.
spellings = collections.Counter(r.get("affl_team") for r in store_doc if "affl_team" in r)
fa = {k: v for k, v in spellings.items() if k and k.lower() == "free agents"}
check(len(fa) == 2, "the store carries BOTH free-agent spellings: %s" % dict(fa))
would_move = sum(1 for r in store_doc
                 if r.get("affl_team") and r["affl_team"].lower() == "free agents"
                 and r["affl_team"] != "Free agents")
check(would_move == 2,
      "canonicalising on the way IN would rewrite exactly %d rows the owner never edited "
      "(18 -> 20) — the exact-byte law is load-bearing" % would_move)

# ---------------------------------------------------------------- the diff proof can fail
keys18 = [e["key"] for e in ours[0].get("_rows", [])] if ours[0].get("_rows") else None
mutated = copy.deepcopy(store_doc)
mutated[0]["affl_team"] = "Hawthorn Hawks__INJECTED"
halts(lambda: OSA.assert_store_diff_is_affl_team_only(store_raw, json.dumps(mutated).encode(), []),
      "the store-diff proof REJECTS an unplanned affl_team move", "key set")

mutated2 = copy.deepcopy(store_doc)
mutated2[0]["games"] = (mutated2[0].get("games") or 0) + 1
halts(lambda: OSA.assert_store_diff_is_affl_team_only(store_raw, json.dumps(mutated2).encode(), []),
      "the store-diff proof REJECTS a diff that touches a NON-ownership field", "affl_team only")

mutated3 = copy.deepcopy(store_doc)
mutated3.pop()
halts(lambda: OSA.assert_store_diff_is_affl_team_only(store_raw, json.dumps(mutated3).encode(), []),
      "the store-diff proof REJECTS a dropped store row", "row count")

check(OSA.assert_store_diff_is_affl_team_only(store_raw, store_raw, []) == 0,
      "NON-VACUITY the other way: an identical store passes the diff proof with 0 moves")

# ---------------------------------------------------------------- P3, the incoherent-base refusal
d, ws = sandbox()
try:
    boot = json.load(open(os.path.join(ws, OSA.BOOT_REL)))
    boot["store"] = "0" * 32
    write_json(os.path.join(ws, OSA.BOOT_REL), boot)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P3 REFUSES to write onto an incoherent base (expected_boot.store perturbed)", "incoherent")
finally:
    shutil.rmtree(d, ignore_errors=True)

d, ws = sandbox()
try:
    sc = json.load(open(os.path.join(ws, OSA.SIDECAR_REL)))
    sc["source_md5"] = "1" * 32
    write_json(os.path.join(ws, OSA.SIDECAR_REL), sc)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P3 REFUSES when the board's Guard-2 source stamp disagrees with the store", "incoherent")
finally:
    shutil.rmtree(d, ignore_errors=True)

# ---------------------------------------------------------------- V5, the join failure modes
d, ws = sandbox()
try:
    csvp = os.path.join(ws, OSA.CSV_REL)
    rows, enc = OSA._readcsv(csvp)
    rows[1][0] = "Nobody Whatsoever"                      # a name the board does not carry
    with open(csvp, "w", encoding=enc, newline="") as f:
        import csv as _csv
        _csv.writer(f).writerows(rows)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "V5 the join HALTS on an unmatched player name, naming him", "Nobody Whatsoever")
finally:
    shutil.rmtree(d, ignore_errors=True)

d, ws = sandbox()
try:
    bvwp = os.path.join(ws, OSA.BVW_REL)
    t = open(bvwp, encoding="utf-8").read()
    o = json.loads(t[t.index("{"):t.rindex("}") + 1])
    o["players"][1]["name"] = o["players"][0]["name"]     # two board players, one normalised name
    head, tail = t[:t.index("{")], t[t.rindex("}") + 1:]
    open(bvwp, "w", encoding="utf-8").write(head + json.dumps(o) + tail)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "V5 the join HALTS on an AMBIGUOUS board name rather than taking the first match", "ambiguous")
finally:
    shutil.rmtree(d, ignore_errors=True)

d, ws = sandbox()
try:
    csvp = os.path.join(ws, OSA.CSV_REL)
    rows, enc = OSA._readcsv(csvp)
    rows[1][1] = "Sydney Swanns"                          # a club spelling the board does not know
    with open(csvp, "w", encoding=enc, newline="") as f:
        import csv as _csv
        _csv.writer(f).writerows(rows)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P6 HALTS on an unknown club spelling — an unknown club would split silently in the UI",
          "Sydney Swanns")
finally:
    shutil.rmtree(d, ignore_errors=True)

# ---------------------------------------------------------------- THE SHEET'S SHAPE (2026-11-06)
# No longer "1 header + 804 players". The sheet may carry delisted-but-AFFL-owned players — retired
# in the store, off the board — so the rule is: every sheet row maps to exactly ONE store row, every
# board player is on the sheet, and a retired row on the sheet is written like any other (the field
# ADDED when the row lacks it). Each clause fired in anger below.
import csv as _csv                                                 # noqa: E402


def _write_rows(path, rows, enc):
    with open(path, "w", encoding=enc, newline="") as f:
        _csv.writer(f).writerows(rows)


def _rewrite_bvw(path, fn):
    t = open(path, encoding="utf-8").read()
    o = json.loads(t[t.index("{"):t.rindex("}") + 1])
    fn(o)
    open(path, "w", encoding="utf-8").write(t[:t.index("{")] + json.dumps(o) + t[t.rindex("}") + 1:])


d, ws = sandbox()
try:
    csvp = os.path.join(ws, OSA.CSV_REL)
    rows, enc = OSA._readcsv(csvp)
    gone = [r for r in rows[1:] if r and OSA.nkey(r[0]) in _bvw_by_name][0]   # a BOARD player's row
    rows.remove(gone)
    _write_rows(csvp, rows, enc)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P5 HALTS when an ACTIVE BOARD PLAYER is not on the sheet, naming him (%s)" % gone[0],
          gone[0])
finally:
    shutil.rmtree(d, ignore_errors=True)

# a retired store row with a unique name, lacking affl_team and afl_club, not yet on the sheet
_sheet_names = {OSA.nkey(r[0]) for r in _rows[1:] if r and r[0].strip()}
_retired_unique = next(r for r in store_doc
                       if r.get("_retired") and "affl_team" not in r and "afl_club" not in r
                       and len(by_name[OSA.nkey(r["player"])]) == 1
                       and OSA.nkey(r["player"]) not in _sheet_names)
d, ws = sandbox()
try:
    csvp = os.path.join(ws, OSA.CSV_REL)
    rows, enc = OSA._readcsv(csvp)
    i_team = OSA._column_index(rows[0], OSA.AFFL_TEAM_COLUMN)
    i_club = OSA._column_index(rows[0], OSA.AFL_CLUB_COLUMN)
    new = [""] * len(rows[0])
    new[0], new[i_team], new[i_club] = _retired_unique["player"], "Free agents", ""   # club BLANK
    rows.append(new)
    _write_rows(csvp, rows, enc)
    plan = OSA.preflight(ws, verbose=False)
    k = _retired_unique["key"]
    check((k, _retired_unique["player"]) in plan.off_board,
          "a RETIRED store row on the sheet (%s) is admitted, resolved off the board to its one store row" % k)
    check((k, _retired_unique["player"], None, "Free agents") in plan.rows and (k, "affl_team") in plan.added,
          "...its affl_team is PLANNED as an ADDITION (the row lacked the field)")
    check(not any(kk == k for kk, _n, _c, _nw in plan.club_rows) and (k, "afl_club") not in plan.added,
          "...and its BLANK AFL Club adds nothing — blank means unchanged, and an absent field stays absent")
    staged = {r["key"]: r for r in json.loads(plan.store_new)}
    check(list(staged[k])[-1] == "affl_team" and staged[k]["affl_team"] == "Free agents"
          and list(staged[k])[:-1] == list(_retired_unique),
          "the staged row carries affl_team as its LAST field, every other field in place")
    n = OSA.assert_store_diff_is_planned_only(plan.store_raw, plan.store_new, plan.planned, added=plan.added)
    check(n >= 1, "the T2 diff proof PASSES with the addition declared (%d substitutions)" % n)
    halts(lambda: OSA.assert_store_diff_is_planned_only(plan.store_raw, plan.store_new, plan.planned),
          "...and REFUSES the same bytes when the addition is NOT declared", "does not declare")
    check("added" in plan.fields_written,
          "fields_written names the addition for the register entry (%s)" % plan.fields_written)
finally:
    shutil.rmtree(d, ignore_errors=True)

d, ws = sandbox()
try:
    # Sam Butler: one on the board (sam-butler-1), one retired (sam-butler). Take the board one off
    # the board and his sheet row is off-board with TWO store rows: ambiguous, never a coin flip.
    _rewrite_bvw(os.path.join(ws, OSA.BVW_REL),
                 lambda o: o.__setitem__("players", [p for p in o["players"] if p["key"] != "sam-butler-1"]))
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P5 HALTS on an off-board name that matches MORE THAN ONE store row (Sam Butler)", "MORE THAN ONE")
finally:
    shutil.rmtree(d, ignore_errors=True)

d, ws = sandbox()
try:
    # an ACTIVE store row that is not on the board is an incoherent tree, not a delisted player
    _unique_active = next(p for p in bvw["players"] if len(by_name[OSA.nkey(p["name"])]) == 1)
    _rewrite_bvw(os.path.join(ws, OSA.BVW_REL),
                 lambda o: o.__setitem__("players", [p for p in o["players"] if p["key"] != _unique_active["key"]]))
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P5 HALTS when an off-board sheet row resolves to a store row that is NOT retired", "NOT retired")
finally:
    shutil.rmtree(d, ignore_errors=True)

d, ws = sandbox()
try:
    csvp = os.path.join(ws, OSA.CSV_REL)
    rows, enc = OSA._readcsv(csvp)
    rows.append(list(rows[1]))                            # the same name twice
    _write_rows(csvp, rows, enc)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P4 HALTS when the sheet names a player twice", "more than once")
finally:
    shutil.rmtree(d, ignore_errors=True)

mutated4 = copy.deepcopy(store_doc)
_lack = next(r for r in mutated4 if "affl_team" not in r)
_lack["affl_team"] = "Free agents"
halts(lambda: OSA.assert_store_diff_is_planned_only(store_raw, json.dumps(mutated4).encode(), {}),
      "the two-field diff proof REJECTS an added field nobody planned", "does not declare")
mutated5 = copy.deepcopy(store_doc)
_lack5 = next(r for r in mutated5 if "affl_team" not in r)
_lack5["games"] = _lack5.get("games")                     # re-set in place: no change
_lack5["_osa_test"] = 1
halts(lambda: OSA.assert_store_diff_is_planned_only(
          store_raw, json.dumps(mutated5).encode(), {_lack5["key"]: {"_osa_test": 1}},
          added={(_lack5["key"], "_osa_test")}),
      "...and REJECTS adding a NON-couriered field even when 'planned'", "adds affl_team and afl_club only")

# ---------------------------------------------------------------- P8 can fail
# Reformatting the store also moves its md5, so P3 (coherence) fires FIRST — which is the correct guard
# order, and worth stating: the cheap structural gate runs before the expensive one. To see P8 itself
# fail, the six pins are advanced to the reformatted store so the base is coherent and P8 is the ONLY
# gate left standing between the tree and a 2,651-row reformat.
d, ws = sandbox()
try:
    sp = os.path.join(ws, OSA.STORE_REL)
    doc = json.load(open(sp))
    with open(sp, "w") as f:
        json.dump(doc, f, indent=2)                       # round trip is no longer the identity
    new_md5 = OSA._md5_file(sp)
    OSA.restamp_manifest(os.path.join(ws, OSA.BOOT_REL), new_md5)
    sc = json.load(open(os.path.join(ws, OSA.SIDECAR_REL)))
    sc["source_md5"] = new_md5
    write_json(os.path.join(ws, OSA.SIDECAR_REL), sc)
    ss = json.load(open(os.path.join(ws, OSA.SEASON_REL)))
    ss["source_store_md5"] = new_md5
    write_json(os.path.join(ws, OSA.SEASON_REL), ss)
    ct = json.load(open(os.path.join(ws, OSA.CONTRACT_REL)))
    ct["identities"]["store"] = new_md5
    write_json(os.path.join(ws, OSA.CONTRACT_REL), ct)
    bvwp = os.path.join(ws, OSA.BVW_REL)
    t = open(bvwp, encoding="utf-8").read()
    o = json.loads(t[t.index("{"):t.rindex("}") + 1])
    o["stamp"]["store_md5"] = new_md5
    open(bvwp, "w", encoding="utf-8").write(t[:t.index("{")] + json.dumps(o) + t[t.rindex("}") + 1:])
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P8 HALTS on serializer drift rather than silently reformatting 2,651 rows", "serializer")
finally:
    shutil.rmtree(d, ignore_errors=True)

print("-" * 72)
print("%d/%d passed" % (PASS[0], PASS[0] + FAIL[0]))
sys.exit(1 if FAIL[0] else 0)
