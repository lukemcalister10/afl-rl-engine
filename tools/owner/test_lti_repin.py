#!/usr/bin/env python3
"""Tests for tools/owner/lti_repin.py.

Required behaviours (directive): a good edit RE-PINS · a bad name REFUSES · a non-register change to
expected_boot is DETECTED and refused · the tool is IDEMPOTENT on re-run. Each test builds a throwaway
git repo with a copied canonical parser, a minimal store, register, and expected_boot, then drives the
real CLI (subprocess) so git baselines are exercised end-to-end. stdlib unittest only.

Run:  python3 tools/owner/test_lti_repin.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
TOOL = os.path.join(HERE, 'lti_repin.py')
REAL_PARSER = os.path.join(REPO, 'engine', 'rl_after', 'lti_register.py')

HEADER = ("| key | player | section | window_id | designation | status | returned_year | notes |\n"
          "|---|---|---|---|---|---|---|---|\n")
ROW_A = "| alpha-one | Alpha One | A | 1 | 2025 | may_return_2026 |  | note a |\n"
ROW_B = "| beta-two | Beta Two | B | 1 | 2026 | out_until_2027 |  | note b |\n"

STORE = [
    {"key": "alpha-one", "player": "Alpha One", "scoring": [{"year": 2025, "games": 3, "avg": 70.0}]},
    {"key": "beta-two", "player": "Beta Two", "scoring": [{"year": 2026, "games": 2, "avg": 60.0}]},
    {"key": "gamma-three", "player": "Gamma Three", "scoring": [{"year": 2026, "games": 5, "avg": 80.0}]},
]


def md5_text(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def boot_dict(register_md5):
    # a representative pin block: the register pin plus other pins the tool must NOT touch.
    return {
        "_doc": "pinned boot identity (test fixture)",
        "band": "b" * 32,
        "board": "0" * 32,
        "config": "c" * 64,
        "register": register_md5,
        "register_note": "owner sidecar pin",
        "store": "5" * 32,
    }


class Base(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="lti_repin_test_")
        os.makedirs(os.path.join(self.root, 'engine', 'rl_after'))
        os.makedirs(os.path.join(self.root, 'data'))
        shutil.copy(REAL_PARSER, os.path.join(self.root, 'engine', 'rl_after', 'lti_register.py'))
        with open(os.path.join(self.root, 'engine', 'rl_after', 'rl_model_data.json'), 'w') as f:
            json.dump(STORE, f)
        self.register = HEADER + ROW_A + ROW_B
        self.write_register(self.register)
        self.write_boot(boot_dict(md5_text(self.register)))
        self._git('init', '-q')
        self._git('config', 'user.email', 't@t')
        self._git('config', 'user.name', 't')
        self._git('add', '-A')
        self._git('commit', '-qm', 'baseline')

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def _git(self, *a):
        subprocess.run(['git', '-C', self.root, *a], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def write_register(self, text):
        with open(os.path.join(self.root, 'LTI_REGISTER.md'), 'w') as f:
            f.write(text)

    def write_boot(self, d):
        with open(os.path.join(self.root, 'data', 'expected_boot.json'), 'w') as f:
            json.dump(d, f, indent=2)

    def read_boot(self):
        with open(os.path.join(self.root, 'data', 'expected_boot.json')) as f:
            return json.load(f)

    def run_tool(self):
        return subprocess.run([sys.executable, TOOL, '--repo-root', self.root],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


class TestGoodEdit(Base):
    def test_good_edit_repins(self):
        # owner edits the register (flip beta-two status) -> pin must move to the new md5.
        edited = HEADER + ROW_A + "| beta-two | Beta Two | B | 1 | 2026 | returned | 2026 | came back |\n"
        self.write_register(edited)
        r = self.run_tool()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("RE-PINNED", r.stdout)
        self.assertIn("~ changed beta-two", r.stdout)
        self.assertEqual(self.read_boot()['register'], md5_text(edited))
        # every other pin is byte-unchanged
        base = boot_dict(md5_text(self.register))
        now = self.read_boot()
        for k, v in base.items():
            if k != 'register':
                self.assertEqual(now[k], v, "pin %r moved" % k)


class TestBadName(Base):
    def test_bad_name_refuses(self):
        # a register key that does not resolve against the store -> REFUSE, write nothing.
        bad = HEADER + ROW_A + ROW_B + "| ghost-nine | Ghost Nine | A | 1 | 2026 | out_until_2027 |  | x |\n"
        self.write_register(bad)
        before = self.read_boot()
        r = self.run_tool()
        self.assertEqual(r.returncode, 2)
        self.assertIn("ghost-nine", r.stderr)
        self.assertEqual(self.read_boot(), before, "expected_boot must be untouched on refuse")

    def test_bad_vocab_refuses(self):
        bad = HEADER + ROW_A + "| beta-two | Beta Two | C | 1 | 2026 | out_until_2027 |  | bad section |\n"
        self.write_register(bad)
        r = self.run_tool()
        self.assertEqual(r.returncode, 2)
        self.assertIn("beta-two", r.stderr)

    def test_bad_date_refuses(self):
        bad = HEADER + ROW_A + "| beta-two | Beta Two | B | 1 | 2026 | out_until_2027 | 2026 | date w/o return |\n"
        self.write_register(bad)
        r = self.run_tool()
        self.assertEqual(r.returncode, 2)
        self.assertIn("returned_year", r.stderr)


class TestTamper(Base):
    def test_nonregister_change_refuses(self):
        # someone hand-edited the store pin in the working tree -> DETECT + refuse even with a valid register edit.
        edited = HEADER + ROW_A + ROW_B + "| gamma-three | Gamma Three | A | 1 | 2026 | out_until_2027 |  | new |\n"
        self.write_register(edited)
        tampered = boot_dict(md5_text(self.register))
        tampered['store'] = "9" * 32                          # a pin the tool must never move
        self.write_boot(tampered)
        r = self.run_tool()
        self.assertEqual(r.returncode, 2)
        self.assertIn("store", r.stderr)
        self.assertIn("OUTSIDE the register pin", r.stderr)


class TestIdempotent(Base):
    def test_idempotent_on_rerun(self):
        # pin already at the register's md5 -> no write, exit 0, and stable across repeated runs.
        before = self.read_boot()
        for _ in range(2):
            r = self.run_tool()
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("PIN UNCHANGED", r.stdout)
            self.assertEqual(self.read_boot(), before)

    def test_repin_then_idempotent(self):
        edited = HEADER + ROW_A + ROW_B + "| gamma-three | Gamma Three | A | 1 | 2025 | may_return_2026 |  | new |\n"
        self.write_register(edited)
        r1 = self.run_tool()
        self.assertEqual(r1.returncode, 0, r1.stderr)
        self.assertIn("RE-PINNED", r1.stdout)
        # re-run without further edit: pin already moved -> idempotent no-op
        r2 = self.run_tool()
        self.assertEqual(r2.returncode, 0, r2.stderr)
        self.assertIn("PIN UNCHANGED", r2.stdout)
        self.assertEqual(self.read_boot()['register'], md5_text(edited))


if __name__ == '__main__':
    unittest.main(verbosity=2)
