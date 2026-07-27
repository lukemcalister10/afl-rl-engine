#!/usr/bin/env python3
# ===== BEGIN ITEM 411 D1 PROVENANCE HEADER — NOT PART OF THE PROVEN ARTIFACT =====
#
# ITEM 411 / D1 — MANIFEST-DRIVEN STORE TRANSFORM: COLD RECONSTRUCTION.
#
#   Reconstruction label : ITEM_411_D1_transform.py — cold reconstruction, artifact of record
#   Author               : d1-cold-review
#   Date                 : 2026-07-27
#
# THIS IS A COLD RECONSTRUCTION. IT IS NOT THE ORIGINAL SCRIPT. The build seat's own
# transform was never committed to ci/item-411-d1-staging and is not in the verified
# bundle. Nothing below was copied from it. It was written from the declared contract
# ("the 10,493-row change manifest is the source of truth", commit 8ecf8f8) plus the two
# committed stores' observable serialization, and then tested against them.
#
# DELETION RULE
#   This header is provenance, not code. To remove it, delete from the FIRST BYTE of the
#   BEGIN line above through and INCLUDING the newline that terminates the END line below.
#   Deleting exactly that span, no more and no less, restores the as-run file byte-for-byte
#   (as-run sha256 recorded at the foot of this header). Every line of this header is a `#`
#   comment and Python comments are not statements, so the module docstring below is still
#   __doc__ and no semantic of the script is altered by the header's presence.
#
# ----------------------------------------------------------------------------------------
# THE ORIGINAL IS UNRECOVERABLE
# ----------------------------------------------------------------------------------------
# Three searched negatives, each re-run against this repo on 2026-07-27:
#
#   (i)   NO SUCH TRANSFORM ON ANY REF, INCLUDING TAGS. A ref-by-ref tree walk over every
#         entry in refs/ (heads, remotes and tags) found only two paths matching
#         *transform*, both long-lived and neither manifest-driven. EVERY COMMITTED TOOL
#         THAT WRITES OR BATCH-EDITS STORE BYTES ON ANY REF WAS READ AT ITS HEADER AND IS
#         EXCLUDED BY NAME. Not one of them is manifest-driven; each is bound instead to a
#         different ENUMERATED edit set, or is not an applicator at all:
#           - session_2026-07-13/store_identity_job/scripts/store_identity_transform.py
#                 ITEM 20 store-identity job; BRAMBLE / afl_club / _draft_club edits
#           - session_2026-07-11/pick_corrections/scripts/apply_store_corrections.py
#                 pick-corrections c.1 / c.3 / c.4
#           - session_2026-07-11/pick_corrections/scripts/apply_store_corrections_expand.py
#                 c-expand, the 199-row rookie/PSD verification pass
#           - session_2026-07-15/reentry_trio/edit_store.py
#                 re-entry trio, three named players
#           - docs/archive/pre-mvp-2026-07/returns/id-migration/repro/migrate_transform.py
#                 pre-MVP id-primary migration
#           - session_2026-07-19/storewrite/storewrite_proof.py
#                 NOT AN APPLICATOR AT ALL, and listed for exactly that reason. It is a
#                 PROOF HARNESS for the weekly-apply write path (round_apply.py), bound to
#                 THROWAWAY SCRATCH COPIES of the tree and writing NOTHING to the real
#                 single source; it arms the apply gate IN-PROCESS ONLY, and its sole
#                 persistent outputs are its own proof.json and PROOF.md. It is named here
#                 so that the exclusion set is complete under the BROADER reading of
#                 "near-neighbour" as well as the narrow applicator-only one.
#
#         THIS NEGATIVE IS STATED AS A PROPERTY, NOT AS A COUNT. The property is the one
#         above: every committed tool that writes or batch-edits store bytes on any ref was
#         read at its header and excluded by name, and none is manifest-driven. The
#         directive of record says FOUR such tools; this list holds SIX. THE TWO DIFFER
#         BECAUSE THE CATEGORY BOUNDARY DIFFERS — proof harnesses versus applicators — AND
#         NOT BECAUSE ANY TOOL WAS DISCOVERED OR DROPPED between the sweeps. A number that
#         moves with the search pattern is precisely the wrong thing to freeze into a
#         permanent header, so no number is load-bearing here.
#
#         AND THE DECISIVE NEGATIVE DOES NOT REST ON THE COUNT IN ANY CASE. It rests on
#         (ii) below: a grep for the change-manifest input path across every ref's .py
#         returns ZERO. That, not any enumeration of neighbours, is what makes the original
#         unrecoverable.
#
#   (ii)  A REPO-WIDE GREP FOR THE CHANGE-MANIFEST INPUT PATH ACROSS EVERY REF'S .py FILES
#         RETURNED EMPTY. No Python file on any ref in this repository references
#         ITEM_411_CHANGE_MANIFEST. Nothing committed anywhere reads this manifest.
#
#   (iii) NO CONTAINER REMNANT. The predecessor build seat's hands container was reclaimed
#         before this review opened, so the as-run file could not be recovered from it.
#         (Reported by supervisor-411; a negative about infrastructure, not independently
#         verifiable from this repository.)
#
# Plus the pen's two independent re-verifications, both re-run here on 2026-07-27:
#
#   - NO .py ON ci/item-411-d1-staging REFERENCES draft_stream, stream_pick OR stream_year.
#     Re-run: confirmed, zero hits across every .py on the branch.
#
#   - THE .py CHANGE PROFILE AT 2ca3df8. Re-run: 4 MODIFIED, 0 ADDED .py files
#     (test_movers_transition.py, test_fv_provenance.py, build_final_board.py,
#     invariant_proof.py), whole-tree name-status with rename/copy detection on.
#     DISCREPANCY, RECORDED NOT SMOOTHED: the pen recorded 5 modified; this review
#     recomputes 4. The load-bearing half — ZERO ADDED .py, i.e. that commit introduced no
#     transform script — reproduces exactly. The count of modified files is not what the
#     negative rests on, but the disagreement is left visible rather than reconciled.
#
# ----------------------------------------------------------------------------------------
# THE NARROW CLAIM — the author's own wording, verbatim. Do not paraphrase it and do not
# widen it.
# ----------------------------------------------------------------------------------------
#
#   reproduces the committed candidate store eb02f754 from the committed baseline 4cbd01ce
#   byte-exact, and returns the baseline unchanged on zero rows — equivalence to the
#   unrecoverable original is established on this one input pair only and is an inference
#   from identical output, never an inspection of the original's code.
#
# Read the last clause literally. NOBODY HAS SEEN THE ORIGINAL'S CODE. Two programs that
# agree on one input pair are not the same program, and this one is claimed no further.
#
# ----------------------------------------------------------------------------------------
# FOUR SILENT FAILURE MODES — ALL REAL, ALL EXIT 0, ALL SILENT
# ----------------------------------------------------------------------------------------
# None of these raises, warns, logs, or changes the exit status. Each is safe HERE, and
# only here, because the real inputs happen to contain ZERO instances of it. That was
# established BY COUNTING ON 2026-07-27, not by any check in the code below. The code
# cannot tell you when it stops being true.
#
#   (A) NO old_value PRECONDITION CHECK. The script never compares the manifest's old_value
#       against what is actually in the store. A manifest row that DISAGREES with the store
#       is applied anyway and overwrites whatever was there. Exit 0, silent.
#       Zero instances here: all 10,444 manifest old_values agree with the baseline store.
#
#   (B) DUPLICATE STORE KEYS LAND THE EDIT ON THE LAST ROW. The index built as
#       {r["key"]: r for r in store} keeps the LAST row for any repeated key, so every edit
#       for that key lands there and the earlier duplicates are never touched. Exit 0,
#       silent. Zero instances here: 2,652 store rows, 2,652 distinct keys.
#
#   (C) AN EMPTY new_value WRITES NULL, NOT EMPTY-STRING. coerce() returns None for any
#       cell that is empty or whitespace, so an intentionally-blank string edit becomes
#       JSON null and the distinction is destroyed. Exit 0, silent.
#       Zero instances here: no applied row has an empty new_value.
#
#   (D) ZERO-PADDING IS LOST. A cell like "007" taking the int path or the inference path
#       becomes the integer 7; the padding is gone and cannot be recovered from the output.
#       Exit 0, silent. Zero instances here: no applied numeric new_value has a leading
#       zero.
#
# ----------------------------------------------------------------------------------------
# THE TYPE-INFERENCE BRANCH CARRIED MOST OF THE RUN
# ----------------------------------------------------------------------------------------
# 8,711 OF 10,444 EDITS (83.4%) TOOK coerce()'s TYPE-INFERENCE BRANCH — the fallback taken
# when the baseline field is absent or null, which GUESSES int-versus-string from the shape
# of the literal. It was correct every single time on this run.
#
# It was correct BY LUCK OF THIS INPUT, NOT BY CONTRACT. The change manifest carries NO TYPE
# COLUMN — its columns are entity_type, entity_id, player, stable_player_id, field,
# old_value, new_value, edit_class, reason, source — so there is nothing for the script to
# check its guess against and nothing that would make a wrong guess visible. A future
# manifest whose literals merely read differently would be coerced differently, silently.
# The remaining edits took typed paths: 679 int, 1,054 str, 0 bool, 0 float.
#
# ----------------------------------------------------------------------------------------
# THIS TRANSFORM VALIDATES NOTHING
# ----------------------------------------------------------------------------------------
# Past two hard exits — entity not in baseline, unsupported __ROW__ op — THIS SCRIPT CHECKS
# NOTHING. Every precondition that made this transition trustworthy — forward attribution of
# each manifest row into the candidate store, reverse attribution of each store delta back
# to a manifest row, old_value agreement against the base, removal and addition accounting,
# duplicate-key rejection — LIVES IN attribute.py, A DIFFERENT FILE, committed alongside as
# docs/directives/ITEM_411_D1_attribute.py.
#
# WHAT YOU ARE READING IS THE APPLICATOR WITHOUT ITS INTERLOCK. Running it alone reproduces
# the bytes. It does not reproduce the assurance.
#
# ----------------------------------------------------------------------------------------
# LOAD-BEARING INVISIBLE CHARACTER — U+FEFF — DO NOT LET ANY TOOL TOUCH THIS FILE
# ----------------------------------------------------------------------------------------
# There is a literal U+FEFF (bytes EF BB BF) INSIDE A STRING LITERAL, in the line that reads
#
#       r["entity_type"] = r.pop("<U+FEFF HERE>entity_type")
#
# It is NOT a leading byte-order mark. It sits mid-source and is INVISIBLE in every editor.
# It is REQUIRED: the change manifest's first header cell is BOM-prefixed, and
# csv.DictReader yields that key verbatim, BOM and all. STRIP IT OR NORMALISE IT AND THE
# SCRIPT DIES WITH KeyError, and the byte-exact result recorded above no longer attaches to
# anything. DO NOT lint, format, reflow, retype, re-encode, or round-trip this file through
# any tool that may alter encoding or line endings. There is exactly ONE occurrence of it in
# this file; if a tool reports zero, or two, the file is already damaged.
#
# COORDINATES — AS-RUN VERSUS COMMITTED. The AS-RUN coordinate of that character is
# BYTE 1723 (0-based) / LINE 48. THAT IS TRUE OF THE AS-RUN FILE AND IT BECOMES FALSE OF
# THIS COMMITTED FILE, because this header shifts every byte below it. In THIS COMMITTED
# FILE the same single character sits at BYTE 15038 (0-based) / LINE 249. Strip this header
# per the deletion rule above and the as-run coordinate is restored exactly.
#
# ----------------------------------------------------------------------------------------
# SCOPE FENCE
# ----------------------------------------------------------------------------------------
# This script is fenced TO THE ITEM 411 D1 TRANSITION ALONE. It is EXPLICITLY NOT APPROVED
# FOR REUSE BY THE ROUTINE STORE-MAINTENANCE LANE, which gets a HARDENED SUCCESSOR built to
# the specification recorded in ITEM_411_D1_attribute.py. Do not import it, do not
# generalise it, do not point it at another manifest, do not lift coerce() out of it.
#
# ----------------------------------------------------------------------------------------
# HASH AND INDEPENDENT SCREENING
# ----------------------------------------------------------------------------------------
# AS-RUN sha256 — this file with this header stripped per the deletion rule:
#
#   0a27636fb379e95b3a8843998ac9d39b73aeba4850aaa378830052beeaf5f9bb
#
# This file's OWN committed hash is deliberately NOT recorded here; a file cannot contain
# its own hash. It is in the commit message.
#
# INDEPENDENT SCREENING: re-run by supervisor-411 on 2026-07-27 under Python 3.11.15, a
# DIFFERENT INTERPRETER than the author's 3.12.3 — byte-exact both ways: the no-op control
# (--rows 0) returns the baseline 4cbd01ce unchanged, and the full run reproduces the
# candidate eb02f754.
#
# ===== END ITEM 411 D1 PROVENANCE HEADER =====
"""ITEM 411 — independent manifest-driven store transform (cold-review reconstruction).

The build seat's own transform script was never committed to ci/item-411-d1-staging and
is not in the verified bundle, so this is a COLD RECONSTRUCTION written only from the
declared contract ("the 10,493-row change manifest is the source of truth", commit
8ecf8f8) plus the two committed stores' observable serialization.

  usage: transform.py <baseline_store.json> <manifest.csv> <out.json> [--rows N]

  --rows 0   NO-OP CONTROL: apply zero manifest rows.
  (default)  apply every player-level manifest row.

Writes nothing into the tracked tree.
"""
import csv, json, sys

def coerce(new_s, old_val, field):
    """Manifest cells are strings; the store is typed. Match the field's existing type
    where there is one, otherwise infer from the literal."""
    s = new_s if new_s is not None else ""
    if s.strip() == "":
        return None
    if isinstance(old_val, bool):
        return s.strip().lower() == "true"
    if isinstance(old_val, int) and not isinstance(old_val, bool):
        return int(s)
    if isinstance(old_val, float):
        return float(s)
    if isinstance(old_val, str):
        return s
    # field absent or null in the baseline -> infer
    t = s.strip()
    if t.lstrip("-").isdigit():
        return int(t)
    return s


def main():
    base_path, man_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    limit = None
    if "--rows" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--rows") + 1])

    store = json.loads(open(base_path, "rb").read())
    rows = list(csv.DictReader(open(man_path)))
    for r in rows:
        r["entity_type"] = r.pop("﻿entity_type")

    player_rows = [r for r in rows if r["entity_type"] == "player"]
    if limit is not None:
        player_rows = player_rows[:limit]

    idx = {r["key"]: r for r in store}
    removed = set()
    edits = 0

    for r in player_rows:
        k, f = r["entity_id"], r["field"]
        rec = idx.get(k)
        if rec is None:
            sys.exit(f"FAIL: manifest entity {k!r} not in baseline store")
        if f == "__ROW__":
            if r["new_value"].strip().lower() != "removed":
                sys.exit(f"FAIL: unsupported __ROW__ op {r['new_value']!r}")
            removed.add(k)
            continue
        rec[f] = coerce(r["new_value"], rec.get(f), f)
        edits += 1

    out = [rec for rec in store if rec["key"] not in removed]
    # the store is serialized as single-line JSON with json.dumps defaults
    # (verified byte-exact by round-tripping the committed baseline).
    blob = json.dumps(out).encode()
    open(out_path, "wb").write(blob)

    sys.stderr.write(
        f"applied: {edits} field edits, {len(removed)} removal(s); "
        f"{len(store)} -> {len(out)} players; {len(blob)} bytes\n")


if __name__ == "__main__":
    main()
