#!/usr/bin/env python3
"""pen.py — SEAT TOOLS 2 · the register pen, mechanised (register item 148).

Subcommands
  append --item-file F --header-summary "…" -m MSG [--register PATH] [--dry-run]
      Insert F's item text before the `## FABLE'S QUEUE` section; bump the header version vN -> vN+1
      (date kept); rewrite ONLY the PEN summary's leading segment, keeping a trailing
      `· prior: <old first clause>` pointer so headers stay SHORT. ASSERT every replacement count
      (the item-147 law — a str.replace that matches 0 or 2 times is a HARD FAIL), assert the new
      version == old+1, assert item numbers are unique. Then git add the register ONLY, commit MSG,
      push HEAD:main with a token read from env var PEN_TOKEN (NEVER echoed, NEVER written to a file),
      re-read the pushed commit's header first-200-chars and print it with the new main SHA and a
      `git diff --name-only` proving docs/-only. One call, <=12 output lines.
      --dry-run does every parse/assert but WRITES NOTHING (no commit, no push) — for safe samples.

  verify [--register PATH]
      Header version + item-count sanity + duplicate-item scan. <=6 lines.

House laws: WRITES NOTHING except append's single intended commit. Every line carries raw evidence.
Loud non-zero exit on ANY failure or missing input; the exit code is the authority (SILENCE IS A RED).
python3 stdlib + git only. PEN_TOKEN lives in the env and nowhere else.
"""
import argparse
import os
import re
import subprocess
import sys

URL = "https://github.com/lukemcalister10/afl-rl-engine.git"
DEFAULT_REGISTER = "docs/OPEN_ITEMS_REGISTER.md"
FABLE_MARKER = "## FABLE'S QUEUE"
# `· vN YYYY-MM-DD · PEN: <body to end of line>`
HDR_RE = re.compile(r"· v(\d+) (\d{4}-\d{2}-\d{2}) · PEN: (.*)$")
ITEM_RE = re.compile(r"^(\d+)\. ", re.M)


def die(msg):
    sys.stderr.write("pen: FAIL — %s\n" % msg)
    raise SystemExit(1)


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def git(root, *args, check=True):
    p = subprocess.run(["git", "-C", root, *args],
                       capture_output=True, text=True)
    if check and p.returncode != 0:
        die("git %s failed: %s" % (" ".join(args), (p.stderr or p.stdout).strip()[:200]))
    return p.stdout


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        die("register not found: %s" % path)
    except OSError as e:
        die("cannot read %s: %s" % (path, e))


def assert_replace(content, old, new, label):
    """The item-147 law: a replacement must match EXACTLY once. 0 or 2 -> HARD FAIL."""
    n = content.count(old)
    if n != 1:
        die("asserted 1 replacement of [%s], found %d (item-147 law: refusing to write)" % (label, n))
    return content.replace(old, new, 1)


def first_clause(seg):
    """Short pointer from the old leading segment: strip markdown, cut at the first clause break."""
    s = seg.strip().strip("*").strip()
    for delim in (": ", ":", " — ", " - ", ". "):
        i = s.find(delim)
        if 0 < i <= 80:
            return s[:i].strip()
    return s[:80].strip()


def parse_header(content):
    line0 = content.split("\n", 1)[0]
    m = HDR_RE.search(line0)
    if not m:
        die("header line 1 does not carry `· vN DATE · PEN: …` — cannot pen")
    return line0, m, int(m.group(1)), m.group(2), m.group(3)


def numbered_before_fable(content):
    idx = content.find(FABLE_MARKER)
    region = content[:idx] if idx >= 0 else content
    return [int(x) for x in ITEM_RE.findall(region)]


# --------------------------------------------------------------------------- append
def cmd_append(a):
    root = repo_root()
    reg_path = a.register if os.path.isabs(a.register) else os.path.join(root, a.register)

    # PEN_TOKEN is required for the real push path — checked EARLY, before ANY write, and never echoed.
    token = os.environ.get("PEN_TOKEN")
    if not a.dry_run and not token:
        die("PEN_TOKEN is unset — refusing to push (set it in the env; it is never printed or written)")

    item_text = read(a.item_file).rstrip("\n")
    if not item_text.strip():
        die("item file %s is empty" % a.item_file)

    content = read(reg_path)
    line0, m, old_v, date, pen_body = parse_header(content)

    # --- rewrite ONLY the PEN summary's leading segment; keep a SHORT prior-pointer ---
    leading = pen_body.split(" · prior", 1)[0]
    new_body = "%s · prior: %s" % (a.header_summary.strip(), first_clause(leading))
    new_v = old_v + 1
    new_header = line0[:m.start()] + "· v%d %s · PEN: %s" % (new_v, date, new_body)
    content = assert_replace(content, line0, new_header, "header line 1")

    # --- version assert: re-parse the rewritten header, new == old+1 ---
    _, m2, chk_v, _, _ = parse_header(content)
    if chk_v != old_v + 1:
        die("version bump assert failed: header now v%d, expected v%d" % (chk_v, old_v + 1))

    # --- insert the item text before the FABLE'S QUEUE section (asserted single match) ---
    before = len(numbered_before_fable(content))
    content = assert_replace(content, FABLE_MARKER, item_text + "\n\n" + FABLE_MARKER,
                             "FABLE'S QUEUE marker")

    # --- item-number uniqueness (the item-147 twin defect: item existed twice) ---
    nums = numbered_before_fable(content)
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    if dupes:
        die("duplicate item numbers before FABLE'S QUEUE: %s" % dupes)
    after = len(nums)

    print("== pen · append%s ==" % (" (dry-run)" if a.dry_run else ""))
    print("version    : v%d -> v%d  (date %s kept)" % (old_v, new_v, date))
    print("item       : inserted before FABLE'S QUEUE  (items %d -> %d, numbers unique)" % (before, after))
    print("header     : %s" % new_header[:200])

    if a.dry_run:
        print("dry-run    : NO write / NO commit / NO push (asserts passed)")
        print("== pen append OK (dry-run) ==")
        return 0

    # --- write, stage ONLY the register, commit ---
    with open(reg_path, "w", encoding="utf-8") as f:
        f.write(content)
    rel = os.path.relpath(reg_path, root)
    old_main = git(root, "rev-parse", "HEAD").strip()
    git(root, "add", rel)
    git(root, "commit", "-m", a.message)
    new_sha = git(root, "rev-parse", "HEAD").strip()

    # diff proving docs/-only BEFORE we push
    names = [ln for ln in git(root, "diff", "--name-only", old_main, new_sha).splitlines() if ln.strip()]
    nondocs = [n for n in names if not n.startswith("docs/")]
    if nondocs:
        die("commit touches non-docs paths, refusing to push: %s" % nondocs)

    # --- push HEAD:main with the token built in-memory; token NEVER echoed ---
    push_url = URL.replace("https://", "https://x-access-token:%s@" % token)
    p = subprocess.run(["git", "-C", root, "push", push_url, "HEAD:main"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        err = (p.stderr or p.stdout).replace(token, "***").strip()[:200]
        die("push HEAD:main failed: %s" % err)

    # --- re-read the pushed commit's header (first 200) as proof ---
    pushed_hdr = git(root, "show", "%s:%s" % (new_sha, rel)).split("\n", 1)[0][:200]
    print("commit     : %s  \"%s\"" % (new_sha[:12], a.message[:60]))
    print("push       : main %s -> %s" % (old_main[:8], new_sha[:8]))
    print("head@main  : %s" % pushed_hdr)
    print("diff       : %s  (docs/-only OK)" % "  ".join(names))
    print("== pen append OK ==")
    return 0


# --------------------------------------------------------------------------- verify
def cmd_verify(a):
    root = repo_root()
    reg_path = a.register if os.path.isabs(a.register) else os.path.join(root, a.register)
    content = read(reg_path)
    _, _, ver, date, _ = parse_header(content)
    nums = numbered_before_fable(content)
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    fable_n = len(ITEM_RE.findall(content[content.find(FABLE_MARKER):])) if FABLE_MARKER in content else 0

    print("== pen · verify ==")
    print("version    : v%d %s  (header line 1)" % (ver, date))
    print("items      : %d numbered before FABLE'S QUEUE  (max=%s)" % (len(nums), max(nums) if nums else "?"))
    if dupes:
        print("duplicates : %s  <-- DEFECT (item-147 class)" % dupes)
    else:
        print("duplicates : none")
    print("fable queue: %d items" % fable_n)
    if dupes or FABLE_MARKER not in content:
        die("verify RED — %s" % ("duplicate items" if dupes else "no FABLE'S QUEUE section"))
    print("== pen verify OK ==")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(prog="pen.py", add_help=True)
    sub = ap.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("append", help="append an item + bump header + commit + push")
    pa.add_argument("--item-file", required=True, dest="item_file")
    pa.add_argument("--header-summary", required=True, dest="header_summary")
    pa.add_argument("-m", "--message", required=True)
    pa.add_argument("--register", default=DEFAULT_REGISTER)
    pa.add_argument("--dry-run", action="store_true")
    pa.set_defaults(func=cmd_append)

    pv = sub.add_parser("verify", help="header + item-count + duplicate scan")
    pv.add_argument("--register", default=DEFAULT_REGISTER)
    pv.set_defaults(func=cmd_verify)

    a = ap.parse_args(argv[1:])
    return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
