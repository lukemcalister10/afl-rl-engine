#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""THE afl_club COURIER (Phase 0.3, 2026-10-13) — the mapping, the blank rule, the diff proof.

WHAT IS AT RISK. `afl_club` had no maintained writer: the store carried 15 active players at a club
they had left, and the finals fixture logic (round_movers) keyed its DNP/unrecorded split on that
stale value. The courier maps the owner's sheet abbreviation to the store's own spelling and writes
it through the same ten-target transaction as `affl_team`. The failures that would ship clean are
quiet ones: an abbreviation mapped to a spelling the store never uses (a club silently forks), a
blank cell read as "no club" (71 owner-silent rows wiped), a move counted under one field and
written under another, or a plan that adds a field to a row that never carried it.

Every rule below is proven BOTH DIRECTIONS: the clean case passes, the injected fault is refused.

Run:  python3 ui/tests/afl_club_courier.test.py      (also collected by unittest / pytest)
"""
import csv
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(REPO, "ui", "tools"))
import ownership_store_apply as OSA          # noqa: E402

STORE_SPELLINGS = {"Adelaide", "Brisbane", "Carlton", "Collingwood", "Essendon", "Fremantle",
                   "Geelong", "Gold Coast", "GWS", "Hawthorn", "Melbourne", "North Melbourne",
                   "Port Adelaide", "Richmond", "St Kilda", "Sydney", "Western Bulldogs", "West Coast"}


class MappingRule(unittest.TestCase):
    """afl_club_from_sheet: the pure half, no tree needed."""

    def test_every_abbreviation_lands_on_a_store_spelling(self):
        for abbr, full in OSA.AFL_CLUB_BY_ABBR.items():
            self.assertIn(full, STORE_SPELLINGS, abbr)
            self.assertEqual(OSA.afl_club_from_sheet(abbr, STORE_SPELLINGS), full)

    def test_every_store_spelling_is_reachable(self):
        self.assertEqual(set(OSA.AFL_CLUB_BY_ABBR.values()), STORE_SPELLINGS)

    def test_the_fifteen_measured_abbreviations(self):
        pairs = {"WCE": "West Coast", "SYD": "Sydney", "NM": "North Melbourne", "PA": "Port Adelaide",
                 "BRI": "Brisbane", "HAW": "Hawthorn", "ESS": "Essendon", "GWS": "GWS",
                 "GEE": "Geelong", "RIC": "Richmond"}
        for abbr, full in pairs.items():
            self.assertEqual(OSA.afl_club_from_sheet(abbr, STORE_SPELLINGS), full)

    def test_gold_coast_both_spellings(self):
        self.assertEqual(OSA.afl_club_from_sheet("GC", STORE_SPELLINGS), "Gold Coast")
        self.assertEqual(OSA.afl_club_from_sheet("GCS", STORE_SPELLINGS), "Gold Coast")

    def test_blank_means_unchanged(self):
        for blank in ("", " ", "\t", None, "  \r\n"):
            self.assertIsNone(OSA.afl_club_from_sheet(blank, STORE_SPELLINGS))

    def test_case_and_whitespace_are_forgiven_in_the_abbreviation(self):
        self.assertEqual(OSA.afl_club_from_sheet(" wce ", STORE_SPELLINGS), "West Coast")

    def test_a_full_store_spelling_passes_verbatim(self):
        self.assertEqual(OSA.afl_club_from_sheet("Gold Coast", STORE_SPELLINGS), "Gold Coast")

    def test_unknown_abbreviation_halts_by_name(self):
        with self.assertRaises(OSA.Halt) as cm:
            OSA.afl_club_from_sheet("XYZ", STORE_SPELLINGS)
        self.assertIn("XYZ", str(cm.exception))

    def test_a_mapped_target_the_store_does_not_spell_halts(self):
        # the table is a claim, the store is the fact: drop one spelling from the known set
        known = STORE_SPELLINGS - {"West Coast"}
        with self.assertRaises(OSA.Halt) as cm:
            OSA.afl_club_from_sheet("WCE", known)
        self.assertIn("West Coast", str(cm.exception))

    def test_column_index_finds_the_header_once(self):
        self.assertEqual(OSA._column_index(["Player Name", "AFFL Team", "Position/s", "AFL Club"],
                                           "AFL Club"), 3)
        with self.assertRaises(OSA.Halt):
            OSA._column_index(["Player Name", "AFFL Team"], "AFL Club")
        with self.assertRaises(OSA.Halt):
            OSA._column_index(["AFL Club", "AFL Club"], "AFL Club")


class PlanShape(unittest.TestCase):
    def test_planned_attributes_each_move_to_its_field(self):
        p = OSA.Plan(rows=[("a", "A", "X", "Y")], store_raw=b"", store_new=b"", md5_before="1",
                     md5_after="2", board_md5="b", csv_encoding="utf-8",
                     club_rows=[("a", "A", "Carlton", "Sydney"), ("b", "B", "Geelong", "Brisbane")])
        self.assertEqual(p.planned, {"a": {"affl_team": "Y", "afl_club": "Sydney"},
                                     "b": {"afl_club": "Brisbane"}})
        self.assertEqual(p.fields_written, "affl_team (1 rows), afl_club (2 rows)")
        self.assertTrue(p.moves)

    def test_no_moves_reads_none(self):
        p = OSA.Plan(rows=[], store_raw=b"", store_new=b"", md5_before="1", md5_after="1",
                     board_md5="b", csv_encoding="utf-8")
        self.assertEqual(p.planned, {})
        self.assertEqual(p.fields_written, "none")
        self.assertFalse(p.moves)


def _store(rows):
    return json.dumps(rows).encode()


BASE = [
    {"key": "a", "player": "A", "games": 1, "afl_club": "Carlton", "affl_team": "T1"},
    {"key": "b", "player": "B", "games": 2, "afl_club": "Geelong", "affl_team": "T2"},
    {"key": "c", "player": "C", "games": 3, "afl_club": "Sydney", "affl_team": "T3"},
]


class DiffProof(unittest.TestCase):
    """assert_store_diff_is_planned_only — the two-field T2."""

    def _new(self, **changes):
        rows = json.loads(json.dumps(BASE))
        for key, fields in changes.items():
            for r in rows:
                if r["key"] == key:
                    r.update(fields)
        return _store(rows)

    def test_a_two_field_diff_on_the_planned_pairs_passes(self):
        new = self._new(a={"afl_club": "Sydney"}, b={"affl_team": "T9", "afl_club": "Brisbane"})
        planned = {"a": {"afl_club": "Sydney"}, "b": {"affl_team": "T9", "afl_club": "Brisbane"}}
        self.assertEqual(OSA.assert_store_diff_is_planned_only(_store(BASE), new, planned), 3)

    def test_identical_store_passes_with_zero(self):
        self.assertEqual(OSA.assert_store_diff_is_planned_only(_store(BASE), _store(BASE), {}), 0)

    def test_an_undeclared_club_move_is_refused(self):
        new = self._new(a={"afl_club": "Sydney"})
        with self.assertRaises(OSA.Halt) as cm:
            OSA.assert_store_diff_is_planned_only(_store(BASE), new, {})
        self.assertIn("does not declare", str(cm.exception))

    def test_a_move_written_under_the_wrong_field_is_refused(self):
        new = self._new(a={"affl_team": "Sydney"})            # planned as afl_club, written as affl_team
        with self.assertRaises(OSA.Halt):
            OSA.assert_store_diff_is_planned_only(_store(BASE), new, {"a": {"afl_club": "Sydney"}})

    def test_the_wrong_value_is_refused(self):
        new = self._new(a={"afl_club": "Sydney"})
        with self.assertRaises(OSA.Halt) as cm:
            OSA.assert_store_diff_is_planned_only(_store(BASE), new, {"a": {"afl_club": "Brisbane"}})
        self.assertIn("the plan says", str(cm.exception))

    def test_a_non_couriered_field_is_refused(self):
        new = self._new(a={"games": 99})
        with self.assertRaises(OSA.Halt) as cm:
            OSA.assert_store_diff_is_planned_only(_store(BASE), new, {})
        self.assertIn("affl_team and afl_club only", str(cm.exception))

    def test_a_planned_move_that_did_not_land_is_refused(self):
        with self.assertRaises(OSA.Halt):
            OSA.assert_store_diff_is_planned_only(_store(BASE), _store(BASE), {"a": {"afl_club": "Sydney"}})

    def test_an_added_field_is_refused(self):
        rows = json.loads(json.dumps(BASE))
        rows[0]["new_field"] = 1
        with self.assertRaises(OSA.Halt) as cm:
            OSA.assert_store_diff_is_planned_only(_store(BASE), _store(rows), {})
        self.assertIn("field set", str(cm.exception))


class LiveTreePlan(unittest.TestCase):
    """The courier against the real tree, in a sandbox copy: the blank rule and the unknown-club
    refusal fired through preflight, never through the live files."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="afl_club_test_")
        cls.ws = os.path.join(cls.tmp, "repo")
        os.makedirs(cls.ws)
        OSA._build_overlay(REPO, cls.ws)
        cls.live = OSA.preflight(REPO, verbose=False)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self):
        # every test starts from the OWNER'S sheet, byte for byte — a mutation in one test must
        # never become another test's input
        shutil.copyfile(os.path.join(REPO, OSA.CSV_REL), os.path.join(self.ws, OSA.CSV_REL))

    def _rewrite_csv(self, fn):
        p = os.path.join(self.ws, OSA.CSV_REL)
        rows, enc = OSA._readcsv(p)
        i = OSA._column_index(rows[0], OSA.AFL_CLUB_COLUMN)
        for r in rows[1:]:
            if r and r[0].strip():
                while len(r) <= i:
                    r.append("")
                r[i] = fn(r[0], r[i])
        with open(p, "w", encoding=enc, newline="") as f:
            csv.writer(f).writerows(rows)

    def test_the_live_plan_never_touches_a_blank_row(self):
        blank_keys = set()
        rows, _ = OSA._readcsv(os.path.join(REPO, OSA.CSV_REL))
        i = OSA._column_index(rows[0], OSA.AFL_CLUB_COLUMN)
        bvw = OSA._bundle_obj(os.path.join(REPO, OSA.BVW_REL))
        by_name = {OSA.nkey(p["name"]): p["key"] for p in bvw["players"]}
        for r in rows[1:]:
            if r and r[0].strip() and not (r[i] if i < len(r) else "").strip():
                blank_keys.add(by_name[OSA.nkey(r[0])])
        self.assertGreater(len(blank_keys), 0)
        self.assertFalse(blank_keys & {k for k, _n, _c, _nw in self.live.club_rows})

    def test_blanking_every_cell_plans_zero_club_moves(self):
        self._rewrite_csv(lambda name, cell: "")
        plan = OSA.preflight(self.ws, verbose=False)
        self.assertEqual(plan.club_rows, [])
        self.assertEqual(plan.rows, self.live.rows)

    def test_an_unknown_abbreviation_halts_the_whole_plan(self):
        self._rewrite_csv(lambda name, cell: "ZZZ" if name == "Aaron Cadman" else cell)
        with self.assertRaises(OSA.Halt) as cm:
            OSA.preflight(self.ws, verbose=False)
        self.assertIn("ZZZ", str(cm.exception))

    def test_a_missing_afl_club_column_halts(self):
        p = os.path.join(self.ws, OSA.CSV_REL)
        rows, enc = OSA._readcsv(p)
        i = OSA._column_index(rows[0], OSA.AFL_CLUB_COLUMN)
        rows[0][i] = "Club?"
        with open(p, "w", encoding=enc, newline="") as f:
            csv.writer(f).writerows(rows)
        with self.assertRaises(OSA.Halt) as cm:
            OSA.preflight(self.ws, verbose=False)
        self.assertIn(OSA.AFL_CLUB_COLUMN, str(cm.exception))

    def test_the_live_plan_is_the_sheet_minus_the_store(self):
        # every planned target is a store spelling; every planned row currently differs
        store = json.loads(self.live.store_raw)
        by_key = {r["key"]: r for r in store if r.get("key")}
        known = {r.get("afl_club") for r in store if r.get("afl_club")}
        for key, _name, cur, new in self.live.club_rows:
            self.assertIn(new, known)
            self.assertEqual(by_key[key].get("afl_club"), cur)
            self.assertNotEqual(cur, new)
        # and the staged bytes are exactly old + the plan (the T2 proof, run on the live plan)
        n = OSA.assert_store_diff_is_planned_only(self.live.store_raw, self.live.store_new,
                                                  self.live.planned)
        self.assertEqual(n, len(self.live.rows) + len(self.live.club_rows))


if __name__ == "__main__":
    unittest.main(verbosity=2)
