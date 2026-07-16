#!/usr/bin/env python3
"""lti_repin.py — the owner's one command AFTER editing LTI_REGISTER.md (owner tool, Tier 3).

The register (`LTI_REGISTER.md`) is OWNER-AUTHORED ground truth, pinned as a versioned engine INPUT
(R-REG=R2, DECISIONS §33). When the owner edits it, its md5 pin in `data/expected_boot.json` must move
in the SAME curation edit (register_note). This tool does exactly that — and nothing else.

WHAT IT DOES
  1. VALIDATE (validate-or-halt). Parse the pipe table; every register key resolves against the store
     (report-only READ of engine/rl_after/rl_model_data.json — this tool NEVER writes the store);
     section/designation/status in the known vocab; returned_year dates sane. Any failure => REFUSE with
     the exact row and reason, writing NOTHING.
  2. RE-PIN. Move `data/expected_boot.json`'s `register` md5 to the edited file — THE ONLY pin this tool
     may move. Every other pin is asserted byte-unchanged before and after (surgical single-field replace,
     the item-147 law: a replace that matches 0 or 2 times is a HARD FAIL). A non-register change to
     expected_boot (a tampered store/board/config/... pin) is DETECTED and REFUSED.
  3. REPORT. Print the register-entry diff (added / removed / changed, HEAD -> working), the old -> new
     register md5, and the plain instruction to rebuild the board. This tool does NOT itself rebuild.

HOUSE LAWS (mirroring tools/seat): stdlib + git only; report-only READ of the store, never a write; the
register pin is the ONLY field it moves; loud non-zero exit on ANY refusal (exit 2) — SILENCE IS A RED;
idempotent (re-running with the pin already at the edited file's md5 writes nothing and exits 0).

Name resolution is BY KEY, never by label. The register's `player` column is a human label that may differ
from the store's canonical name by design (e.g. "Nic Martin" / store "Nicholas Martin"); the `key` column is
the join key ("Key by ID, never name", register NAME GUARD). "Resolves" therefore means: the key maps to
exactly one store record. The canonical parse+vocab validation is reused from engine/rl_after/lti_register.py
so this tool and the engine can never drift on the register's schema.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

REGISTER_FILENAME = 'LTI_REGISTER.md'
EXPECTED_BOOT_REL = os.path.join('data', 'expected_boot.json')
STORE_REL = os.path.join('engine', 'rl_after', 'rl_model_data.json')
PARSER_REL = os.path.join('engine', 'rl_after', 'lti_register.py')
PIN_FIELD = 'register'
# sane bound for a returned_year cell (loud, not clever — a typo'd 20226 or 1900 is caught)
YEAR_LO, YEAR_HI = 2020, 2035


def die(msg, code=2):
    sys.stderr.write("lti_repin: REFUSE — %s\n" % msg)
    raise SystemExit(code)


# --------------------------------------------------------------------------- helpers
def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def load_parser(root):
    """Import the canonical register parser/validator from the target repo (single source of schema)."""
    path = os.path.join(root, PARSER_REL)
    if not os.path.exists(path):
        die("canonical parser not found at %s (is --repo-root a real checkout?)" % path)
    spec = importlib.util.spec_from_file_location('_lti_register_shared', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_show(root, rev_path):
    """`git -C root show <rev_path>` -> text, or None if it does not resolve (no commit / untracked)."""
    r = subprocess.run(['git', '-C', root, 'show', rev_path],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        return None
    return r.stdout.decode('utf-8')


def build_store_by_key(store_path):
    """Report-only READ of the store. Returns {key: record}; refuses on a duplicate key (validation of the
    register against a store with a collided key would be unsound)."""
    with open(store_path) as f:
        store = json.load(f)
    by_key = {}
    for rec in store:
        k = rec.get('key')
        if k in by_key:
            die("store carries a DUPLICATE key %r — cannot soundly resolve register names against it" % k)
        by_key[k] = rec
    return by_key


# --------------------------------------------------------------------------- validation (validate-or-halt)
def strict_table_scan(path, ncols):
    """Catch malformed table rows the tolerant parser would silently skip. Returns line-numbered halts."""
    halts, seen_header = [], False
    with open(path) as f:
        for i, ln in enumerate(f, 1):
            s = ln.rstrip('\n')
            if not s.lstrip().startswith('|'):
                continue
            cells = [c.strip() for c in s.strip().strip('|').split('|')]
            first = cells[0] if cells else ''
            if first == 'key':
                seen_header = True
                continue
            if first and set(first) <= {'-', ':'}:
                continue                                    # md separator row
            if not seen_header:
                continue                                    # a pipe in prose above the table
            if len(cells) < ncols:
                halts.append("line %d: row has %d columns, need %d -> %s" % (i, len(cells), ncols, s.strip()))
                continue
            try:
                int(cells[3])
            except ValueError:
                halts.append("line %d: window_id %r is not an integer -> %s" % (i, cells[3], s.strip()))
    return halts


def dates_sane(rows):
    """returned_year discipline: present + a sane 4-digit year iff status=='returned', blank otherwise."""
    halts = []
    for d in rows:
        rid = "key=%s w%s (player %r)" % (d['key'], d['window_id'], d['player'])
        ry = (d.get('returned_year') or '').strip()
        if d['status'] == 'returned':
            if not ry:
                halts.append("%s: status 'returned' but returned_year is blank" % rid)
            elif not re.fullmatch(r'\d{4}', ry) or not (YEAR_LO <= int(ry) <= YEAR_HI):
                halts.append("%s: returned_year %r is not a sane %d-%d year" % (rid, ry, YEAR_LO, YEAR_HI))
        elif ry:
            halts.append("%s: returned_year %r set but status is %r (blank until a real return)"
                         % (rid, ry, d['status']))
    return halts


def validate_register(L, path, store_by_key):
    """Full validate-or-halt over ONE register file. Returns parsed rows; raises SystemExit(2) with the exact
    offending row(s) on any failure. Structural vocab/key checks are the engine's own (L.validate)."""
    scan = strict_table_scan(path, len(L._COLS))
    if scan:
        die("register table did not parse cleanly:\n  - " + "\n  - ".join(scan))
    rows = L.parse(path)
    if not rows:
        die("register table parsed to ZERO rows (no pipe-table body found)")
    try:
        L.validate(rows, store_by_key)                      # section|designation|status vocab + key resolves + windows
    except ValueError as e:
        die(str(e))
    ds = dates_sane(rows)
    if ds:
        die("register date checks failed:\n  - " + "\n  - ".join(ds))
    return rows


# --------------------------------------------------------------------------- entry diff
def _row_key(d):
    return (d['key'], d['window_id'])


def diff_entries(old_rows, new_rows):
    """added / removed / changed keyed by (key, window_id)."""
    old = {_row_key(d): d for d in old_rows}
    new = {_row_key(d): d for d in new_rows}
    added = [new[k] for k in new if k not in old]
    removed = [old[k] for k in old if k not in new]
    changed = []
    for k in new:
        if k in old:
            deltas = {c: (old[k].get(c), new[k].get(c))
                      for c in new[k] if old[k].get(c) != new[k].get(c)}
            if deltas:
                changed.append((new[k], deltas))
    keyf = lambda d: (d['key'], d['window_id'])
    return (sorted(added, key=keyf), sorted(removed, key=keyf),
            sorted(changed, key=lambda t: keyf(t[0])))


def _tag(d):
    return "%s w%s (%s) [%s %s %s]" % (d['key'], d['window_id'], d['player'],
                                       d['section'], d['designation'], d['status'])


def render_diff(added, removed, changed):
    lines = ["REGISTER ENTRY DIFF (HEAD -> working):"]
    if not (added or removed or changed):
        lines.append("  (no entry changes)")
        return lines
    for d in added:
        lines.append("  + added   " + _tag(d))
    for d in removed:
        lines.append("  - removed " + _tag(d))
    for d, deltas in changed:
        parts = "; ".join("%s: %r -> %r" % (c, o, n) for c, (o, n) in sorted(deltas.items()))
        lines.append("  ~ changed %s w%s (%s)  %s" % (d['key'], d['window_id'], d['player'], parts))
    return lines


# --------------------------------------------------------------------------- expected_boot pin move
def assert_only_register_moved(working, baseline):
    """Every field except the register pin must be byte-identical between the on-disk expected_boot and its
    committed (HEAD) baseline. A difference elsewhere is a tampered pin -> REFUSE."""
    keys = set(working) | set(baseline)
    bad = []
    for k in sorted(keys):
        if k == PIN_FIELD:
            continue
        if working.get(k) != baseline.get(k):
            bad.append(k)
    if bad:
        die("expected_boot.json changed OUTSIDE the register pin (this tool moves ONLY %r): "
            "fields differ vs HEAD -> %s" % (PIN_FIELD, ", ".join(bad)))


def replace_register_value(text, old_hex, new_hex):
    """Surgical single-field replace (item-147 law: assert exactly one match)."""
    needle = '"%s": "%s"' % (PIN_FIELD, old_hex)
    n = text.count(needle)
    if n != 1:
        die("asserted exactly 1 occurrence of the register pin line, found %d — refusing to write" % n)
    return text.replace(needle, '"%s": "%s"' % (PIN_FIELD, new_hex))


# --------------------------------------------------------------------------- main
def run(root):
    reg_path = os.path.join(root, REGISTER_FILENAME)
    boot_path = os.path.join(root, EXPECTED_BOOT_REL)
    store_path = os.path.join(root, STORE_REL)
    for p in (reg_path, boot_path, store_path):
        if not os.path.exists(p):
            die("required file missing: %s" % p)

    L = load_parser(root)
    store_by_key = build_store_by_key(store_path)

    # 1. VALIDATE the edited (working) register — validate-or-halt.
    new_rows = validate_register(L, reg_path, store_by_key)
    new_hex = md5_file(reg_path)

    # baselines from HEAD (the pre-edit register + the committed pin block)
    boot_head_text = git_show(root, 'HEAD:' + EXPECTED_BOOT_REL.replace(os.sep, '/'))
    if boot_head_text is None:
        die("cannot read HEAD:%s — commit a baseline before re-pinning" % EXPECTED_BOOT_REL)
    baseline = json.loads(boot_head_text)
    with open(boot_path) as f:
        boot_text = f.read()
    working = json.loads(boot_text)
    if PIN_FIELD not in working or PIN_FIELD not in baseline:
        die("expected_boot.json has no %r pin field" % PIN_FIELD)

    # 2. tamper guard: on-disk expected_boot may differ from HEAD ONLY in the register pin.
    assert_only_register_moved(working, baseline)
    old_pin = working[PIN_FIELD]

    # entry diff vs the committed register (HEAD)
    reg_head_text = git_show(root, 'HEAD:' + REGISTER_FILENAME)
    if reg_head_text is None:
        old_rows = []
    else:
        tmp = boot_path + '.head_register.tmp'
        with open(tmp, 'w') as f:
            f.write(reg_head_text)
        try:
            old_rows = L.parse(tmp)
        finally:
            os.remove(tmp)
    added, removed, changed = diff_entries(old_rows, new_rows)

    print("register file : %s" % reg_path)
    print("register md5  : %s -> %s" % (old_pin, new_hex))
    for line in render_diff(added, removed, changed):
        print(line)

    # 3. idempotency — pin already at the edited file's md5: write nothing.
    if new_hex == old_pin:
        print("PIN UNCHANGED : expected_boot.json register already == %s (idempotent, no write)" % new_hex)
        print("NEXT          : rebuild the board to consume this (this tool does NOT rebuild).")
        return 0

    # re-pin: surgical replace, then assert only the register field moved before -> after.
    pre = json.loads(boot_text)
    new_text = replace_register_value(boot_text, old_pin, new_hex)
    with open(boot_path, 'w') as f:
        f.write(new_text)
    post = json.loads(new_text)
    if post.get(PIN_FIELD) != new_hex:
        die("post-write assertion failed: register pin is %r, expected %r" % (post.get(PIN_FIELD), new_hex))
    moved = [k for k in (set(pre) | set(post)) if k != PIN_FIELD and pre.get(k) != post.get(k)]
    if moved:
        die("post-write assertion failed: fields other than the register pin moved -> %s" % ", ".join(moved))

    print("RE-PINNED     : data/expected_boot.json register %s -> %s (only field moved)" % (old_pin, new_hex))
    print("NEXT          : rebuild the board to consume this (this tool does NOT rebuild).")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate LTI_REGISTER.md and re-pin its md5 in expected_boot.json.")
    default_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    ap.add_argument('--repo-root', default=default_root,
                    help="repo checkout root (default: two levels up from this tool)")
    args = ap.parse_args(argv)
    return run(os.path.abspath(args.repo_root))


if __name__ == '__main__':
    sys.exit(main())
