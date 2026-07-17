#!/usr/bin/env python3
"""round_entry.py — the owner's weekly round-entry CLI (DRY-RUN ONLY; store READ-ONLY).

The 2-minute workflow (item 305): paste a FootyWire `name,score` body + a round number; the tool
exact-matches each name to a live active `stable_player_id` and emits a stamped per-round snapshot.
Any name that does not cleanly resolve is a FLAGGED RESIDUE line for a one-tap confirm — never a
silent drop, never the wrong row, never a new-row invention.

COMMANDS
  enter   --round N  [--body-file F | --body - ]  [--store PATH] [--out DIR]
          Parse + resolve a round's `name,score` body. Writes the preview + (if any) the residue
          file. A CLEAN round (no residue) also writes the stamped snapshot immediately. Re-running
          `enter` for a round REPLACES that round's artifacts LOUDLY (idempotent, never duplicates).

  confirm --round N  [--residue FILE] [--store PATH] [--out DIR]
          Consume the owner-edited residue file (one ACTION per block: a candidate number or `skip`)
          and write the round's stamped snapshot. Refuses loudly on any blank/invalid ACTION.

  show    --round N  [--out DIR]
          Print the round's snapshot summary (or say none exists yet).

HOUSE LAWS (mirroring tools/seat, tools/owner): stdlib only; the store is READ-ONLY (never written);
snapshots are DERIVED/read-only/source-stamped (SSI); loud non-zero exit on ANY refusal — SILENCE IS
A RED. The store-WRITE path is ABSENT BY DESIGN; go-live is a separate owner-worded job (GO_LIVE).
"""
import argparse
import json
import os
import sys
import time


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


# import the engine-side library (read-only reuse; the tool is a thin shell over it)
sys.path.insert(0, os.path.join(repo_root(), "engine", "rl_after", "ingestion"))
sys.path.insert(0, os.path.join(repo_root(), "engine", "rl_after"))
import round_entry as RE   # noqa: E402


DEFAULT_OUT = os.path.join(repo_root(), "engine", "rl_after", "ingestion", "round_snapshots")


def die(msg, code=2):
    sys.stderr.write("round_entry: FAIL — %s\n" % msg)
    raise SystemExit(code)


def _paths(out_dir, round_n):
    return {
        'preview': os.path.join(out_dir, "round_%d.preview.json" % round_n),
        'residue': os.path.join(out_dir, "round_%d.residue.txt" % round_n),
        'snapshot': os.path.join(out_dir, "round_%d.snapshot.json" % round_n),
    }


def _read_body(args):
    if args.body_file:
        with open(args.body_file) as f:
            return f.read()
    if args.body == '-' or args.body is None:
        data = sys.stdin.read()
        if not data.strip():
            die("no body on stdin (paste `name,score` lines, or pass --body-file)")
        return data
    return args.body


def _now(args):
    """Wall-clock stamp for the snapshot. `--now ISO` pins it (used by the determinism check)."""
    if getattr(args, 'now', None):
        return args.now
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _announce_replace(paths):
    existing = [os.path.basename(p) for p in paths.values() if os.path.exists(p)]
    if existing:
        print("  REPLACING this round's prior artifacts (idempotent): %s" % ", ".join(sorted(existing)))
        for p in paths.values():
            if os.path.exists(p):
                os.remove(p)


def cmd_enter(args):
    out_dir = args.out or DEFAULT_OUT
    os.makedirs(out_dir, exist_ok=True)
    paths = _paths(out_dir, args.round)
    body = _read_body(args)

    ent = RE.RoundEntry(args.round, store_path=args.store or RE._STORE_DEFAULT)
    try:
        resolved, residue = ent.resolve_body(body)
    except RE.RoundEntryParseError as e:
        die("parse error: %s" % e)

    _announce_replace(paths)   # idempotent: wipe the round's prior artifacts LOUDLY first

    preview = {'round': args.round, 'season_year': ent.season_year,
               'source_store_md5': RE.md5_of_file(ent.store_path),
               'module_code_md5': RE.module_code_md5(),
               'active_pool_size': ent.resolver.active_count,
               'resolved': [r.as_dict() for r in resolved],
               'residue': [r.as_dict() for r in residue],
               'counts': {'resolved': len(resolved), 'residue': len(residue)}}
    with open(paths['preview'], 'w') as f:
        f.write(json.dumps(preview, sort_keys=True, indent=2) + "\n")

    print("ROUND %d — active pool %d — %d resolved, %d residue"
          % (args.round, ent.resolver.active_count, len(resolved), len(residue)))
    for r in resolved:
        print("  OK   %-24s %6s  -> %s" % (r.name, r.score, r.key))

    if residue:
        RE.write_residue(args.round, residue, paths['residue'])
        for r in residue:
            near = ", ".join("%d)%s" % (c['index'], c['name']) for c in r.candidates) or "(none)"
            print("  ??   %-24s %6s  [%s] candidates: %s" % (r.name, r.score, r.reason, near))
        print("\n%d line(s) need a one-tap confirm. Edit the ACTION lines in:\n  %s\nthen run:  "
              "round_entry confirm --round %d" % (len(residue), paths['residue'], args.round))
        print("(no snapshot written — nothing enters a snapshot unresolved)")
        return 0

    # clean round: write the snapshot now
    snap = ent.build_snapshot(resolved, generated_at=_now(args))
    with open(paths['snapshot'], 'w') as f:
        f.write(RE.snapshot_bytes(snap).decode('utf-8'))
    print("\nCLEAN round — snapshot written: %s" % paths['snapshot'])
    print("  store md5 %s (read-only) · module md5 %s · resolved %d"
          % (snap['source_store_md5'], snap['module_code_md5'], snap['counts']['resolved']))
    return 0


def cmd_confirm(args):
    out_dir = args.out or DEFAULT_OUT
    paths = _paths(out_dir, args.round)
    residue_path = args.residue or paths['residue']
    preview_path = paths['preview']
    if not os.path.exists(residue_path):
        die("no residue file for round %d at %s (run `enter` first, or there was no residue)"
            % (args.round, residue_path))
    if not os.path.exists(preview_path):
        die("no preview for round %d at %s (run `enter` first)" % (args.round, preview_path))

    try:
        decisions = RE.read_confirmed_residue(residue_path)
    except RE.ResidueConfirmError as e:
        die("residue not fully confirmed: %s" % e)
    confirmed_rows, skipped = RE.confirmed_to_rows(decisions)

    preview = json.load(open(preview_path))
    base_rows = [RE.ResolvedRow(d['stable_player_id'], d['key'], d['name'], d['score'], d['via'])
                 for d in preview['resolved']]
    all_rows = base_rows + confirmed_rows
    all_rows.sort(key=lambda r: r.key or '')

    ent = RE.RoundEntry(args.round, season_year=preview['season_year'],
                        store_path=args.store or RE._STORE_DEFAULT)
    snap = ent.build_snapshot(all_rows, generated_at=_now(args), skipped=skipped)
    with open(paths['snapshot'], 'w') as f:
        f.write(RE.snapshot_bytes(snap).decode('utf-8'))

    print("ROUND %d confirmed — snapshot written: %s" % (args.round, paths['snapshot']))
    print("  resolved %d (%d exact + %d confirmed) · skipped %d · residue_open %d"
          % (snap['counts']['resolved'], len(base_rows), len(confirmed_rows),
             snap['counts']['skipped'], snap['counts']['residue_open']))
    for d in decisions:
        if d['action'] == 'attach':
            print("  PICK %-24s %6s -> %s" % (d['name'], d['score'], d['pick']['key']))
        else:
            print("  SKIP %-24s %6s (owner-skip)" % (d['name'], d['score']))
    return 0


def cmd_show(args):
    out_dir = args.out or DEFAULT_OUT
    paths = _paths(out_dir, args.round)
    if not os.path.exists(paths['snapshot']):
        print("round %d: no snapshot yet." % args.round)
        if os.path.exists(paths['residue']):
            print("  a residue file awaits confirm: %s" % paths['residue'])
        return 0
    snap = json.load(open(paths['snapshot']))
    print("ROUND %d snapshot — %s" % (snap['round'], paths['snapshot']))
    print("  season %s · generated %s" % (snap['season_year'], snap['generated_at']))
    print("  source_store_md5 %s · module_code_md5 %s"
          % (snap['source_store_md5'], snap['module_code_md5']))
    print("  counts: %s" % json.dumps(snap['counts'], sort_keys=True))
    for r in snap['resolved']:
        print("    %-24s %6s  %s (%s)" % (r['name'], r['score'], r['key'], r['via']))
    for s in snap['skipped']:
        print("    [skip] %-18s %6s  %s" % (s['name'], s['score'], s['reason']))
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="round_entry", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("enter", help="parse+resolve a round's name,score body")
    pe.add_argument("--round", type=int, required=True)
    pe.add_argument("--body-file", help="read the name,score body from this file (.csv or text)")
    pe.add_argument("--body", default="-", help="'-' (default) reads the body from stdin")
    pe.add_argument("--store", help="store path (default: the single source)")
    pe.add_argument("--out", help="artifact dir (default: engine/.../ingestion/round_snapshots)")
    pe.add_argument("--now", help="pin generated_at (ISO); used by the determinism check")
    pe.set_defaults(func=cmd_enter)

    pc = sub.add_parser("confirm", help="consume the edited residue file -> snapshot")
    pc.add_argument("--round", type=int, required=True)
    pc.add_argument("--residue", help="residue file (default: the round's residue in --out)")
    pc.add_argument("--store", help="store path (default: the single source)")
    pc.add_argument("--out", help="artifact dir")
    pc.add_argument("--now", help="pin generated_at (ISO); used by the determinism check")
    pc.set_defaults(func=cmd_confirm)

    ps = sub.add_parser("show", help="print a round's snapshot summary")
    ps.add_argument("--round", type=int, required=True)
    ps.add_argument("--out", help="artifact dir")
    ps.set_defaults(func=cmd_show)
    return p


def main(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
