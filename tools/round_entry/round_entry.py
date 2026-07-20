#!/usr/bin/env python3
"""round_entry.py — the owner's weekly round workflow CLI (one tool, seven verbs).

The one-command weekly workflow (register item 305 + the 2026-07-20 live-scoring hardening):

    place ONE score file  ->  round_entry run --round N --body-file scores.csv  ->  review  ->  approve

`run` does the whole clean-round job in one command: resolve every name, print a human-readable
preview + unresolved-name report, require an EXPLICIT approval, then apply the exact snapshot and
refresh the UI + history. The five lower-level verbs remain for power users / a residue round:

    1. enter    paste/supply `name,score` + a round -> resolve every name -> stamped snapshot
    2. confirm   one-tap resolve any residue (a number or `skip`) -> stamped snapshot
    3. show      inspect the EXACT stamped snapshot before applying anything
    4. apply     apply THAT EXACT snapshot to the store, staged+validated+atomic (gate-guarded)
    5. recover   restore after an interrupted apply (crash recovery)
    6. run       the one-command owner path: resolve -> preview -> approve -> apply -> UI + history
    7. catchup   controlled multi-round catch-up (several rounds, ONE preflight + ONE approval,
                 each round its own sequential committed transaction; restart-safe)

The owner never constructs the older structured feed by hand and never edits Python: place a score
file, run one command, review the preview, approve. A name that does not resolve is the one human
review — a candidate number or `skip`, never a silent drop. A successful apply moves the store +
board atomically, records the persistent per-player value + rank history, and refreshes the Matchday
UI bundles; backups, the transaction record, the dedup ledger and the history are all kept.

COMMANDS
  enter   --round N  [--body-file F | --body - ]  [--store PATH] [--out DIR]
          Parse + resolve a round's `name,score` body. Writes the preview + (if any) the residue
          file. A CLEAN round (no residue) also writes the stamped snapshot immediately. Re-running
          `enter` for a round REPLACES that round's artifacts LOUDLY (idempotent, never duplicates).

  confirm --round N  [--residue FILE] [--store PATH] [--out DIR]
          Consume the owner-edited residue file (one ACTION per block: a candidate number or `skip`)
          and write the round's stamped snapshot. Refuses loudly on any blank/invalid ACTION.

  show    --round N  [--out DIR]
          Print the round's snapshot summary + its STRONG identity (store md5, content hash, verify).

  apply   --round N  [--out DIR] [--repo DIR] [--store PATH] [--now ISO] [--txn-root DIR]
          Apply THAT EXACT snapshot (never re-resolves) via the staged transaction: STAGE ->
          VALIDATE (incl. Guard 5) -> ATOMIC SWAP, with rollback + crash recovery. Refuses loudly if
          the store moved (stale), the snapshot was edited (content hash), residue is open, the round
          is invalid, the round is a duplicate, or the apply gate is OFF (the shipped default).

  recover [--repo DIR] [--txn-root DIR]
          Detect + explicitly roll back an interrupted transaction (a crash mid-apply); restores the
          originals so the store is never left with a stale board/manifest/ledger. Keeps evidence.

HOUSE LAWS (mirroring tools/seat, tools/owner): stdlib only; enter/confirm/show never write the
store; apply writes ONLY behind the double-OFF gate (score_ingestor.APPLY_DEFAULT + env
INGEST_SCORE_APPLY, both default OFF); snapshots are DERIVED/read-only/source-stamped (SSI); loud
non-zero exit on ANY refusal — SILENCE IS A RED. The shipped branch keeps the gate OFF and applies
no real round; the failure-injection proof exercises the write path on SCRATCH copies only.
"""
import argparse
import json
import os
import sys
import time


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


# import the engine-side libraries (read-only reuse; the tool is a thin shell over them)
sys.path.insert(0, os.path.join(repo_root(), "engine", "rl_after", "ingestion"))
sys.path.insert(0, os.path.join(repo_root(), "engine", "rl_after"))
import round_entry as RE          # noqa: E402
import staged_apply as SA         # noqa: E402
import score_ingestor as SI       # noqa: E402
import round_catchup as RC        # noqa: E402


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


def _write_snapshot(path, snap):
    with open(path, 'w') as f:
        f.write(RE.snapshot_bytes(snap).decode('utf-8'))


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
               'source_store_md5_full': RE.md5_of_file_full(ent.store_path),
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
    _write_snapshot(paths['snapshot'], snap)
    print("\nCLEAN round — snapshot written: %s" % paths['snapshot'])
    print("  store md5 %s (full %s, read-only) · content_hash %s · resolved %d"
          % (snap['source_store_md5'], snap['source_store_md5_full'][:8],
             snap['content_hash'][:12], snap['counts']['resolved']))
    print("  inspect it:  round_entry show --round %d" % args.round)
    print("  apply it:    round_entry apply --round %d" % args.round)
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
    _write_snapshot(paths['snapshot'], snap)

    print("ROUND %d confirmed — snapshot written: %s" % (args.round, paths['snapshot']))
    print("  resolved %d (%d exact + %d confirmed) · skipped %d · residue_open %d · content_hash %s"
          % (snap['counts']['resolved'], len(base_rows), len(confirmed_rows),
             snap['counts']['skipped'], snap['counts']['residue_open'], snap['content_hash'][:12]))
    for d in decisions:
        if d['action'] == 'attach':
            print("  PICK %-24s %6s -> %s" % (d['name'], d['score'], d['pick']['key']))
        else:
            print("  SKIP %-24s %6s (owner-skip)" % (d['name'], d['score']))
    print("  inspect it:  round_entry show --round %d" % args.round)
    print("  apply it:    round_entry apply --round %d" % args.round)
    return 0


def cmd_show(args):
    out_dir = args.out or DEFAULT_OUT
    paths = _paths(out_dir, args.round)
    if not os.path.exists(paths['snapshot']):
        print("round %d: no snapshot yet." % args.round)
        if os.path.exists(paths['residue']):
            print("  a residue file awaits confirm: %s" % paths['residue'])
        return 0
    snap = RE.load_snapshot(paths['snapshot'])
    ok, reason = RE.verify_snapshot(snap)
    print("ROUND %d snapshot — %s" % (snap['round'], paths['snapshot']))
    print("  schema v%s · season %s · generated %s"
          % (snap.get('snapshot_schema_version', 1), snap['season_year'], snap['generated_at']))
    print("  source_store_md5 %s (full %s) · module_code_md5 %s"
          % (snap['source_store_md5'], (snap.get('source_store_md5_full') or '')[:8],
             snap['module_code_md5']))
    print("  content_hash %s · verify: %s (%s) · strong: %s"
          % ((snap.get('content_hash') or '')[:12], ok, reason, RE.is_strong(snap)))
    print("  counts: %s" % json.dumps(snap['counts'], sort_keys=True))
    for r in snap['resolved']:
        print("    %-24s %6s  %s (%s)" % (r['name'], r['score'], r['key'], r['via']))
    for s in snap['skipped']:
        print("    [skip] %-18s %6s  %s" % (s['name'], s['score'], s['reason']))
    return 0


# ---- APPLY (JOB 1): consume the EXACT stamped snapshot; staged transaction; owner summary --------
_REFUSALS = (SA.StaleSnapshotError, SA.AlteredSnapshotError, SA.ResidueOpenError,
             SA.StagedValidationError, SA.IncompleteTransactionError, SI.IngestionGatedError,
             SA.SeasonBoundError, SA.DuplicateRoundError, SA.PreviewNotCleanError)


def cmd_apply(args):
    out_dir = args.out or DEFAULT_OUT
    paths = _paths(out_dir, args.round)
    if not os.path.exists(paths['snapshot']):
        die("no snapshot for round %d at %s (run `enter`/`confirm` first, then `show`)"
            % (args.round, paths['snapshot']))
    snap = RE.load_snapshot(paths['snapshot'])
    ok, reason = RE.verify_snapshot(snap)
    if not ok:
        die("snapshot for round %d FAILED self-verification (%s) — do NOT apply an edited snapshot; "
            "re-enter the round." % (args.round, reason))

    repo = os.path.abspath(args.repo) if args.repo else repo_root()
    print("APPLYING round %d snapshot (season %s) — %d players — from %s"
          % (snap['round'], snap['season_year'], snap['counts']['resolved'], paths['snapshot']))
    print("  snapshot store id %s · content_hash %s (verified)"
          % (snap['source_store_md5'], (snap.get('content_hash') or '')[:12]))
    return _apply_and_report(snap, args, repo)


def _apply_and_report(snap, args, repo):
    """Run the staged transaction for a verified snapshot, then (only after a fully committed board)
    refresh the UI bundles and print the owner summary. Shared by `apply` and `run`."""
    applier = SA.StagedRoundApplier.for_repo(
        repo, txn_root=(os.path.abspath(args.txn_root) if getattr(args, 'txn_root', None) else None))
    try:
        res = applier.apply_snapshot(snap, generated_at=(getattr(args, 'now', None) or _now(args)))
    except SI.IngestionGatedError as e:
        # the shipped default: gate OFF. Refuse to write; tell the owner how to arm locally.
        print("\nAPPLY REFUSED — the store-write gate is OFF (shipped default; nothing was written).")
        print("  %s" % e)
        print("\n  To apply LOCALLY (owner only, after v2.11 ships), arm BOTH halves for this run")
        print("  (two env vars — NO Python editing; nothing is armed in the committed repo):")
        print("    INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=<your-token> \\")
        print("      round_entry apply --round %d      # or via tools/round_entry/weekly_update.sh"
              % snap['round'])
        print("  See tools/round_entry/README.md.")
        return 3
    except SA.IncompleteTransactionError as e:
        die("%s\n  run:  round_entry recover" % e, code=4)
    except _REFUSALS as e:
        die("%s: %s" % (type(e).__name__, e), code=2)

    # POST-COMMIT (only after a fully committed board): refresh the Matchday UI view bundles.
    ui_ev = applier.refresh_ui()
    _print_apply_summary(res, repo, ui_ev)
    return 0


def _print_apply_summary(res, repo, ui_ev=None):
    h = res.history or {}
    print("\n================ WEEKLY UPDATE APPLIED ================")
    print("  Round applied      : R%d, season %d" % (res.round, res.season))
    print("  Players applied    : %d" % res.players_applied)
    print("  Store hash         : %s  ->  %s" % (res.store_md5_before[:8], res.store_md5_after[:8]))
    print("  Board hash         : %s  ->  %s"
          % ((res.board_md5_before or 'none')[:8], res.board_md5_after[:8]))
    print("  Guard 5 (boot)     : %s" % ("GREEN (validated on the staged build)" if res.guard5_green else "?"))
    print("  Transaction/backup : %s" % res.txn_dir)
    print("  Duplicate guard    : recorded %d triple(s); ledger now holds %d (a re-send is blocked)"
          % (res.ledger_added, res.ledger_total))
    print("  Value+rank history : rounds %s recorded for %d players (append-only; earlier rounds kept)"
          % (h.get('rounds_after'), h.get('players', 0)))
    print("  FV provenance      : board built from the STAGED valuation module (recorded in the txn)")
    if ui_ev is None or not ui_ev.get('ran'):
        reason = (ui_ev or {}).get('reason', 'not run')
        print("  UI bundles         : not refreshed (%s)" % reason)
    elif ui_ev.get('ok'):
        print("  UI bundles         : refreshed — working + public (board stamp %s == committed %s%s)"
              % (ui_ev.get('ui_board_stamp'), ui_ev.get('committed_board_id'),
                 ", public leak-free" if ui_ev.get('public_leak_free') else ""))
    else:
        print("  UI bundles         : FAILED to refresh (rc=%s) — %s"
              % (ui_ev.get('rc'), (ui_ev.get('stderr_tail') or '').strip()[:120]))
    print("  The store/board/manifest/ledger/history were staged, validated, and swapped atomically;")
    print("  a crash mid-swap rolls back. Backups, transaction record, ledger and history are kept.")
    print("======================================================")


def cmd_recover(args):
    repo = os.path.abspath(args.repo) if args.repo else repo_root()
    applier = SA.StagedRoundApplier.for_repo(
        repo, txn_root=(os.path.abspath(args.txn_root) if args.txn_root else None))
    incomplete = applier.scan_incomplete()
    if not incomplete:
        print("recover: no incomplete transaction found — nothing to recover (clean).")
        return 0
    print("recover: %d incomplete transaction(s) detected — rolling back to the originals:" % len(incomplete))
    report = applier.recover(generated_at=_now(args))
    for r in report['recovered']:
        print("  %s: restored %s" % (r['txn'], ", ".join(r['restored']) or "(nothing to restore)"))
    print("recover: done — the store/board/manifest/ledger are back to their pre-apply state. Evidence kept.")
    return 0


# ---- RUN (the one-launcher owner path): resolve -> preview -> approve -> apply -> UI + history ----
def cmd_run(args):
    """One command for the whole weekly job: place a score file, run this, review the preview, approve.

    resolve the round -> print a human-readable preview + unresolved-name report -> (clean round only)
    require an EXPLICIT approval (interactive `yes`, or --approve) -> apply the exact snapshot through
    the staged transaction -> refresh the UI bundles -> print a clear SUCCESS or REFUSAL. No Python, no
    manual file editing on a clean round; a residue line is the one human review (a number or `skip`)."""
    out_dir = args.out or DEFAULT_OUT
    os.makedirs(out_dir, exist_ok=True)
    paths = _paths(out_dir, args.round)
    repo = os.path.abspath(args.repo) if args.repo else repo_root()
    body = _read_body(args)

    ent = RE.RoundEntry(args.round, store_path=args.store or RE._STORE_DEFAULT)
    try:
        resolved, residue = ent.resolve_body(body)
    except RE.RoundEntryParseError as e:
        die("parse error: %s" % e)

    _announce_replace(paths)
    print("ROUND %d — active pool %d — %d resolved, %d unresolved"
          % (args.round, ent.resolver.active_count, len(resolved), len(residue)))
    for r in resolved:
        print("  OK   %-24s %8s  -> %s" % (r.name, r.score, r.key))

    if residue:
        RE.write_residue(args.round, residue, paths['residue'])
        print("\n%d name(s) did NOT cleanly resolve — a one-tap review (never a silent drop):" % len(residue))
        for r in residue:
            near = ", ".join("%d)%s" % (c['index'], c['name']) for c in r.candidates) or "(none)"
            print("  ??   %-24s %8s  [%s] candidates: %s" % (r.name, r.score, r.reason, near))
        print("\n  Edit the ACTION line (a candidate NUMBER or `skip`) in:\n    %s" % paths['residue'])
        print("  then finish with:\n    round_entry confirm --round %d && round_entry run --round %d --approve"
              % (args.round, args.round))
        print("  (nothing is applied while a name is unresolved.)")
        return 0

    snap = ent.build_snapshot(resolved, generated_at=_now(args))
    _write_snapshot(paths['snapshot'], snap)
    print("\nPREVIEW — clean round, snapshot stamped:")
    print("  store id %s (full %s) · content_hash %s · %d players"
          % (snap['source_store_md5'], snap['source_store_md5_full'][:8],
             snap['content_hash'][:12], snap['counts']['resolved']))

    if not _approved(args):
        print("\nNOT APPROVED — nothing was applied. Re-run with --approve (or answer `yes`) to apply.")
        return 0

    print("\nAPPROVED — applying round %d ..." % args.round)
    return _apply_and_report(snap, args, repo)


def _approved(args, prompt="Apply this round to the store now? type `yes` to confirm: "):
    """Explicit owner approval: the --approve flag, or an interactive `yes` on the prompt. A
    non-interactive run without --approve is treated as NOT approved (never applies unattended)."""
    if getattr(args, 'approve', False):
        return True
    if not sys.stdin or not sys.stdin.isatty():
        return False
    try:
        ans = input(prompt).strip().lower()
    except EOFError:
        return False
    return ans in ('yes', 'y')


# ---- CATCHUP (controlled multi-round): ONE preflight + ONE approval, per-round transactions --------
import re as _re


def _collect_catchup_files(args):
    """Gather [(round, path)]: from `--dir DIR` (round parsed from each filename's `R<N>`), and/or
    repeated `--file N=path` (or `N:path`). Sorted by round; a duplicate round is an error."""
    files = {}
    if args.dir:
        for name in sorted(os.listdir(args.dir)):
            m = _re.search(r'[Rr](\d+)', name)
            if m and name.lower().endswith(('.csv', '.txt')):
                files[int(m.group(1))] = os.path.join(args.dir, name)
    for spec in (args.file or []):
        sep = '=' if '=' in spec else ':'
        rnd, path = spec.split(sep, 1)
        r = int(rnd.lstrip('Rr'))
        if r in files and os.path.abspath(files[r]) != os.path.abspath(path):
            die("two files given for round %d" % r)
        files[r] = path
    if not files:
        die("no round files — pass --dir DIR (files named R15.csv ...) or --file 15=path")
    return sorted(files.items())


def _print_preflight(report):
    print("================ CATCH-UP PREFLIGHT ================")
    print("  season %s · %d round(s) · identity overrides: %s"
          % (report['season'], len(report['rounds']), ", ".join(report['identity_override_names']) or "none"))
    for rd in report['rounds']:
        print("  R%-2d  enc=%-9s listed/played=%-4d resolved=%-4d listed-zero=%-3d absent/DNP=%-4d  sha256 %s"
              % (rd['round'], rd['encoding'], rd['listed'], rd['resolved'], rd['listed_zero'],
                 rd['absent_dnp'], rd['sha256'][:12]))
        for o in rd['identity_overrides']:
            print("        identity override: %-22s -> %-22s (score %g, %s)"
                  % (o['name'], o['key'], o['score'], o['via']))
        for u in rd['unresolved']:
            print("        UNRESOLVED: %r score=%s (%s)" % (u['name'], u.get('score'), u['reason']))
        for a in rd['ambiguous']:
            print("        AMBIGUOUS: %r score=%s" % (a['name'], a.get('score')))
        for d in rd['duplicate_keys']:
            print("        DUPLICATE stable key: %s scores=%s" % (d['key'], d['scores']))
        if rd['already_applied']:
            print("        (already applied — will be SKIPPED on resume)")
    if report['clean']:
        print("  PREFLIGHT CLEAN — every name resolves to a stable identity; no duplicate/ambiguous.")
    else:
        print("  PREFLIGHT HALTED:")
        for h in report['halt_reasons']:
            print("    - %s" % h)
    print("===================================================")


def cmd_catchup(args):
    repo = os.path.abspath(args.repo) if args.repo else repo_root()
    files = _collect_catchup_files(args)
    overrides = (RC.IdentityOverrides.load(args.overrides) if args.overrides else RC.IdentityOverrides.load())
    cu = RC.RoundCatchup(repo, files, overrides=overrides)
    report, _rounds = cu.preflight()
    _print_preflight(report)
    if not report['clean']:
        die("catch-up preflight HALTED — resolve the identity issues above; NOTHING was applied.", code=2)

    print("\nAbout to apply rounds %s — each as its own sequential transaction, committed in order."
          % [r for r, _ in files])
    if not _approved(args, prompt="Approve this catch-up (all rounds above)? type `yes`: "):
        print("NOT APPROVED — nothing applied. Re-run with --approve (or answer `yes`).")
        return 0

    try:
        run = cu.run(approved=True, generated_at=_now(args),
                     txn_root=(os.path.abspath(args.txn_root) if args.txn_root else None))
    except SI.IngestionGatedError as e:
        print("\nCATCH-UP REFUSED — the store-write gate is OFF (shipped default; nothing was written).")
        print("  %s" % e)
        print("  Arm BOTH halves LOCALLY for the run (no code edit):")
        print("    INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=<your-token> \\")
        print("      round_entry catchup --dir <scores> --approve")
        return 3
    except SA.IncompleteTransactionError as e:
        die("%s\n  run:  round_entry recover" % e, code=4)
    except (RC.CatchupError, *_REFUSALS) as e:
        die("%s: %s" % (type(e).__name__, e), code=2)

    print("\n================ CATCH-UP APPLIED ================")
    for r in run['rounds']:
        if r['status'] == 'applied':
            print("  R%-2d  store %s->%s  board %s->%s  players=%d  guard5=%s  hist=%s  movers->UI=%s"
                  % (r['round'], (r.get('store_before') or '')[:8], (r.get('store_after') or '')[:8],
                     (r.get('board_before') or '')[:8], (r.get('board_after') or '')[:8],
                     r['players_applied'], r['guard5_green'], r['history_rounds'],
                     r.get('movers_ui_rows_injected')))
        else:
            print("  R%-2d  SKIPPED (already applied — restart-safe)" % r['round'])
    print("  Final store %s · board %s" % (run['final_store'][:8], run['final_board'][:8]))
    print("  Per-round backups, transaction records, dedup ledger, value/overall-rank/positional-rank")
    print("  histories and movers reports are all retained.")
    print("=================================================")
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

    ps = sub.add_parser("show", help="print a round's snapshot summary + identity")
    ps.add_argument("--round", type=int, required=True)
    ps.add_argument("--out", help="artifact dir")
    ps.set_defaults(func=cmd_show)

    pa = sub.add_parser("apply", help="apply THAT EXACT snapshot (staged transaction; gate-guarded)")
    pa.add_argument("--round", type=int, required=True)
    pa.add_argument("--out", help="artifact dir (where the snapshot lives)")
    pa.add_argument("--repo", help="repo root to apply against (default: this checkout)")
    pa.add_argument("--store", help="(unused; store is read from the repo) kept for symmetry")
    pa.add_argument("--now", help="pin the transaction timestamp (ISO)")
    pa.add_argument("--txn-root", help="transaction directory root (default: under ingestion/)")
    pa.set_defaults(func=cmd_apply)

    pr = sub.add_parser("recover", help="roll back an interrupted apply (crash recovery)")
    pr.add_argument("--repo", help="repo root (default: this checkout)")
    pr.add_argument("--txn-root", help="transaction directory root (default: under ingestion/)")
    pr.add_argument("--now", help="pin the recovery timestamp (ISO)")
    pr.set_defaults(func=cmd_recover)

    pn = sub.add_parser("run", help="one command: resolve -> preview -> approve -> apply -> UI+history")
    pn.add_argument("--round", type=int, required=True)
    pn.add_argument("--body-file", help="read the name,score body from this file (.csv or text)")
    pn.add_argument("--body", default="-", help="'-' (default) reads the body from stdin")
    pn.add_argument("--approve", action="store_true",
                    help="explicit approval to apply a clean round (else you are prompted / it stops)")
    pn.add_argument("--store", help="store path (default: the single source)")
    pn.add_argument("--out", help="artifact dir")
    pn.add_argument("--repo", help="repo root to apply against (default: this checkout)")
    pn.add_argument("--now", help="pin timestamps (ISO)")
    pn.add_argument("--txn-root", help="transaction directory root (default: under ingestion/)")
    pn.set_defaults(func=cmd_run)

    pcu = sub.add_parser("catchup", help="controlled multi-round catch-up: one preflight + one approval")
    pcu.add_argument("--dir", help="directory of round files (round parsed from each filename's R<N>)")
    pcu.add_argument("--file", action="append", help="explicit round file: `15=path` (repeatable)")
    pcu.add_argument("--overrides", help="owner identity-override JSON (default: the shipped catch-up overrides)")
    pcu.add_argument("--approve", action="store_true", help="approve the whole catch-up (else prompted/stops)")
    pcu.add_argument("--repo", help="repo root to apply against (default: this checkout)")
    pcu.add_argument("--now", help="pin timestamps (ISO)")
    pcu.add_argument("--txn-root", help="transaction directory root (default: under ingestion/)")
    pcu.set_defaults(func=cmd_catchup)
    return p


def main(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
