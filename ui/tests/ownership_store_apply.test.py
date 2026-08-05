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
plan = OSA.preflight(REPO, verbose=False)
check(not plan.moves and plan.md5_before == plan.md5_after == live_md5,
      "re-running preflight on the applied tree is a NO-OP — 0 rows move, the store md5 does not budge")

lin = json.load(open(os.path.join(REPO, OSA.LINEAGE_REL)))
reg = lin["release_transition_register"]
ours = [e for e in reg if OSA.OWNER_RULING_ID in (e.get("owner_ruling_id") or [])]
check(len(ours) == 1,
      "exactly ONE #283 register entry exists — a re-run appends no second one (%d total entries)" % len(reg))
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

d, ws = sandbox()
try:
    csvp = os.path.join(ws, OSA.CSV_REL)
    rows, enc = OSA._readcsv(csvp)
    rows.pop()                                            # 803 players, not 804
    with open(csvp, "w", encoding=enc, newline="") as f:
        import csv as _csv
        _csv.writer(f).writerows(rows)
    halts(lambda: OSA.preflight(ws, verbose=False),
          "P4 HALTS when the CSV is not 1 header + 804 players", "CSV shape")
finally:
    shutil.rmtree(d, ignore_errors=True)

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
