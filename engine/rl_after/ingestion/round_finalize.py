"""ROUND FINALIZE — journaled, idempotent post-commit finalization of a committed round.

The core weekly transaction (staged_apply) commits the CANONICAL state ATOMICALLY: store, board,
sidecar, boot manifest, ledger, and the three histories. THAT commit is the source of truth. Everything
downstream — the Matchday UI board bundles + release contract, the per-round movers report (JSON +
CSV), the accumulated UI movers bundle, and the round-delta injection — is RE-DERIVABLE from that
committed state and is produced here as a SEPARATE, JOURNALED FINALIZATION phase.

CRASH-GAP CLOSURE (corrective 2026-07-20, review A). The pending-finalization record does NOT depend on
the caller surviving the canonical commit: the applier writes `played` + board/store ids durably into
the COMMITTED transaction manifest, and `reconcile()` reconstructs the CORE_COMMITTED record from those
committed transaction manifests on restart. A kill immediately after COMMITTED (before the caller runs
`record_core_committed`) therefore never strands the round.

FINALIZED IS THE FINAL DURABLE OP (review C). Derivatives are generated while the round is FINALIZING;
FULL validation runs FIRST; only after validation succeeds is FINALIZED written, as the last state
transition. A crash after derivatives-but-before-validation, or after-validation-but-before-FINALIZED,
restarts as unfinalized and repairs safely.

NEVER MUTATE ON CONFLICT (review B). Before writing ANY same-round artifact, the existing JSON + bundle
entry are inspected; if their governing identity (txn/board/store/round) differs, finalization refuses
and leaves every existing byte unchanged (no JSON, no CSV, no bundle write; status not advanced).

HISTORICAL REPAIR IS SAFE (review E). Each round's FROZEN governing release identity is stored in its
durable finalization record. A repair of an OLDER round rebuilds only that round's report + bundle entry
from the stored identity + committed histories; it does NOT touch the working board (which stays on the
latest round) and does NOT alter any canonical score or ledger entry.

STATES: CORE_COMMITTED -> FINALIZING -> FINALIZED, or -> FINALIZATION_INCOMPLETE on a derivation
failure / conflict. run / catchup REFUSE to advance while a prior committed round is not FINALIZED.

Deliberately NOT finalized here: ui/data/club_valuation.js (Track A owns the club-valuation curve) and
ui/app/positions_data.js (values-free position map derived from the owner CSV, not the board).
"""
import json
import os
import sys
import tempfile

try:
    from . import round_movers as MV
    from . import staged_apply as SA
except (ImportError, ValueError):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import round_movers as MV      # type: ignore
    import staged_apply as SA      # type: ignore

STATE_FILENAME = 'finalization_state.json'
JOURNAL_FILENAME = 'finalization_journal.jsonl'
SCHEMA_VERSION = 1

CORE_COMMITTED = 'CORE_COMMITTED'
FINALIZING = 'FINALIZING'
FINALIZATION_INCOMPLETE = 'FINALIZATION_INCOMPLETE'
FINALIZED = 'FINALIZED'
_UNFINALIZED = {CORE_COMMITTED, FINALIZING, FINALIZATION_INCOMPLETE}

# the ordered finalization fault points (the failure-injection matrix, directives F + C)
FAULT_POINTS = (
    'after_core_commit_before_ui',           # after the canonical commit, before any UI refresh
    'during_working_board_refresh',          # as the working/public board refresh begins
    'after_board_before_movers_json',        # after the board bundles, before the movers JSON
    'after_json_before_csv',                 # after the movers JSON, before the CSV
    'after_json_csv_before_bundle',          # after JSON+CSV, before the accumulated bundle
    'after_bundle_before_delta',             # after the bundle, before the working-board delta inject
    'after_derivatives_before_validation',   # (C) all derivatives written, before validation
    'after_validation_before_finalized',     # (C) validation passed, before the FINALIZED state write
)


class FinalizationFault(RuntimeError):
    """A deliberately injected finalization fault (failure-injection proof only)."""


class RoundFinalizer:
    """Drives + journals the finalization of committed rounds. Bound to an explicit repo_root so the
    proofs run it against SCRATCH copies; the real single source is never a proof target."""

    def __init__(self, repo_root, *, state_path=None, journal_path=None, fault=None, txn_root=None):
        self.repo_root = os.path.abspath(repo_root)
        ing = os.path.join(self.repo_root, 'engine', 'rl_after', 'ingestion')
        self.state_path = state_path or os.path.join(ing, STATE_FILENAME)
        self.journal_path = journal_path or os.path.join(ing, JOURNAL_FILENAME)
        self.fault = fault          # test hook: fault(point) may raise
        self.txn_root = txn_root    # transaction-dir root (default: the applier's default under ingestion)

    # -- state io -------------------------------------------------------------------------------
    def _load(self):
        if not os.path.exists(self.state_path):
            return {'kind': 'round_finalization_state', 'schema_version': SCHEMA_VERSION, 'rounds': {}}
        with open(self.state_path) as f:
            st = json.load(f)
        st.setdefault('rounds', {})
        return st

    def _save(self, st):
        d = os.path.dirname(os.path.abspath(self.state_path))
        os.makedirs(d, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix='.finstate_', suffix='.json', dir=d)
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(st, f, indent=2, sort_keys=True)
                f.flush(); os.fsync(f.fileno())
            os.replace(tmp, self.state_path)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    def _journal(self, event, **fields):
        line = {'event': event}
        line.update(fields)
        os.makedirs(os.path.dirname(os.path.abspath(self.journal_path)), exist_ok=True)
        with open(self.journal_path, 'a') as f:
            f.write(json.dumps(line, sort_keys=True) + '\n')
            f.flush(); os.fsync(f.fileno())

    def _set_status(self, round_n, status, **extra):
        st = self._load()
        entry = st['rounds'].setdefault(str(int(round_n)), {})
        entry['status'] = status
        for k, v in extra.items():
            if k == 'failure' and status == FINALIZED and v is None:
                entry.pop('failure', None)
            elif v is not None or k not in entry:
                entry[k] = v
        self._save(st)
        self._journal('STATUS', round=int(round_n), status=status)
        return entry

    # -- queries --------------------------------------------------------------------------------
    def status(self, round_n):
        return (self._load()['rounds'].get(str(int(round_n))) or {}).get('status')

    def entry(self, round_n):
        return self._load()['rounds'].get(str(int(round_n)))

    def recorded_rounds(self):
        return sorted(int(r) for r in self._load()['rounds'])

    def finalized_rounds(self):
        st = self._load()
        return sorted(int(r) for r, e in st['rounds'].items() if e.get('status') == FINALIZED)

    def unfinalized_rounds(self):
        """Rounds that committed but are NOT yet FINALIZED (a restart must finish these first)."""
        st = self._load()
        return sorted(int(r) for r, e in st['rounds'].items() if e.get('status') in _UNFINALIZED)

    def _latest_committed_round(self):
        rr = self.recorded_rounds()
        return rr[-1] if rr else None

    def advance_blocked(self, next_round):
        """Refuse to advance to `next_round` while the immediately-preceding committed round is not
        FINALIZED. Returns the blocking round number, or None if clear to advance."""
        prev = int(next_round) - 1
        e = self.entry(prev)
        if e and e.get('status') in _UNFINALIZED:
            return prev
        un = [r for r in self.unfinalized_rounds() if r < int(next_round)]
        return min(un) if un else None

    # ===========================================================================================
    # RECONCILE — reconstruct pending-finalization records from the COMMITTED transaction manifests
    # (closes the post-commit / pre-record crash gap; never depends on the caller surviving).
    # ===========================================================================================
    def _applier(self):
        return SA.StagedRoundApplier.for_repo(self.repo_root, txn_root=self.txn_root)

    def _committed_txns(self):
        """[(round, manifest)] for every transaction that reached COMMITTED (durable canonical commit)."""
        ap = self._applier()
        out = []
        for d in ap._txn_dirs():
            man = ap._read_txn_manifest(d)
            if man and man.get('status') == SA.STATUS_COMMITTED and man.get('round') is not None:
                out.append((int(man['round']), man))
        return out

    def reconcile(self, *, generated_at=None):
        """For every COMMITTED transaction with NO finalization record, reconstruct a CORE_COMMITTED
        record from the transaction manifest (round, season, played, board/store ids) + the frozen
        release identity. Idempotent: an existing record (any status) is left untouched. Returns the
        list of rounds reconciled."""
        st = self._load()
        reconciled = []
        for rnd, man in self._committed_txns():
            if str(rnd) in st['rounds']:
                continue                      # already tracked (record present) — leave it
            evidence = {'store_md5_before': man.get('store_md5_before'),
                        'store_md5_after': man.get('store_md5_after'),
                        'board_md5_before': man.get('board_md5_before'),
                        'board_md5_after': man.get('board_md5_after'),
                        'txn_id': man.get('txn_id')}
            self._record(rnd, season=man.get('season'), played=man.get('played') or {},
                         evidence=evidence, generated_at=generated_at or man.get('created_at'),
                         reconciled=True)
            reconciled.append(rnd)
        if reconciled:
            self._journal('RECONCILED', rounds=reconciled)
        return reconciled

    # -- record the canonical commit (fast path; reconcile is the crash-safe backstop) ----------
    def _record(self, round_n, *, season, played, evidence, generated_at=None, reconciled=False):
        round_n = int(round_n)
        st = self._load()
        if (st['rounds'].get(str(round_n)) or {}).get('status') == FINALIZED:
            return st['rounds'][str(round_n)]       # never clobber a finalized round
        rel = MV.frozen_release_identity(self.repo_root, round_n,
                                         (evidence or {}).get('board_md5_after'),
                                         (evidence or {}).get('store_md5_after'))
        entry = {
            'status': CORE_COMMITTED, 'round': round_n, 'season': int(season) if season else None,
            'previous_round': round_n - 1, 'txn_id': (evidence or {}).get('txn_id'),
            'store_md5_before': (evidence or {}).get('store_md5_before'),
            'store_md5_after': (evidence or {}).get('store_md5_after'),
            'board_md5_before': (evidence or {}).get('board_md5_before'),
            'board_md5_after': (evidence or {}).get('board_md5_after'),
            'played': {k: played[k] for k in sorted(played or {})},
            'release_identity': rel,                # FROZEN governing identity (historical repair reads this)
            'generated_at': generated_at, 'core_committed_at': generated_at,
            'reconciled': bool(reconciled), 'finalized_at': None, 'derivatives': None, 'failure': None,
        }
        st['rounds'][str(round_n)] = entry
        self._save(st)
        self._journal('CORE_COMMITTED', round=round_n, txn_id=entry['txn_id'],
                      board_md5_after=entry['board_md5_after'], reconciled=bool(reconciled))
        return entry

    def record_core_committed(self, round_n, *, season, played, evidence, generated_at=None):
        return self._record(round_n, season=season, played=played, evidence=evidence,
                            generated_at=generated_at, reconciled=False)

    def _evidence(self, entry):
        return {'store_md5_before': entry.get('store_md5_before'),
                'store_md5_after': entry.get('store_md5_after'),
                'board_md5_before': entry.get('board_md5_before'),
                'board_md5_after': entry.get('board_md5_after'),
                'txn_id': entry.get('txn_id')}

    def _fault(self, point):
        if self.fault is not None:
            self.fault(point)

    # ===========================================================================================
    # THE FINALIZATION PASS
    # ===========================================================================================
    def finalize_round(self, round_n, *, generated_at=None, force=False):
        """Generate + validate every owner-facing derivative for a committed round, idempotently.

        For the LATEST committed round this refreshes the working board (+ release contract + round
        deltas) and (re)builds the movers report/bundle. For an OLDER round (a historical repair) it
        rebuilds ONLY that round's movers report + bundle entry from the round's FROZEN identity, and
        leaves the working board on the latest round. Validation runs BEFORE FINALIZED is written. A
        conflict or any derivation failure leaves the round unfinalized and writes no conflicting bytes;
        it NEVER rolls back or re-applies the canonical commit. Returns an evidence dict."""
        round_n = int(round_n)
        entry = self.entry(round_n)
        if entry is None:
            raise RuntimeError('round %d has no CORE_COMMITTED record — nothing to finalize' % round_n)
        latest = self._latest_committed_round()
        historical = latest is not None and round_n < latest
        if entry.get('status') == FINALIZED and not force:
            val = self._validate_derivatives(round_n, entry, historical=historical)
            if val['ok']:
                return {'ok': True, 'round': round_n, 'status': FINALIZED, 'already': True,
                        'historical': historical, 'validation': val}

        played = entry.get('played') or {}
        evidence = self._evidence(entry)
        rel = entry.get('release_identity')          # FROZEN identity (E) — repair reproduces it exactly
        self._set_status(round_n, FINALIZING)
        self._journal('FINALIZE_BEGIN', round=round_n, force=bool(force), historical=historical)
        try:
            self._fault('after_core_commit_before_ui')
            ui_data = os.path.join(self.repo_root, 'ui', 'data')
            working = os.path.join(ui_data, MV.WORKING_BUNDLE_NAME)

            if not historical:
                # LATEST round: refresh the working/public board bundles from the committed board, then
                # stamp the FULL release contract (as_of_round = this round) the browser validates against.
                self._fault('during_working_board_refresh')
                ui_ev = self._applier().refresh_ui()
                if not (ui_ev.get('ran') and ui_ev.get('ok')):
                    return self._incomplete(round_n, 'board_view refresh failed: rc=%s %s'
                                            % (ui_ev.get('rc'), (ui_ev.get('stderr_tail') or '')[:200]))
                if os.path.exists(working):
                    MV.inject_release_contract(working, self.repo_root, round_n)
            else:
                ui_ev = {'ran': False, 'reason': 'historical repair — working board left on the latest round'}

            # movers report (built from the round's FROZEN identity)
            self._fault('after_board_before_movers_json')
            report = MV.build_report(self.repo_root, round_n, played=played, evidence=evidence,
                                     generated_at=generated_at or entry.get('generated_at'),
                                     release_identity_override=rel)

            # NEVER MUTATE ON CONFLICT — inspect existing JSON + bundle BEFORE any write (B)
            conflict, why = MV.movers_conflict(self.repo_root, round_n, report)
            if conflict:
                return self._incomplete(round_n, 'artifact identity conflict (no bytes written): %s' % why)

            jpath = MV.write_report_json(self.repo_root, round_n, report)
            self._fault('after_json_before_csv')
            cpath = MV.write_report_csv(self.repo_root, round_n, report)

            self._fault('after_json_csv_before_bundle')
            bundle_path = os.path.join(ui_data, 'movers.js')
            bundle_res = {'path': None}
            if os.path.isdir(ui_data):
                bundle_res = MV.accumulate_bundle(bundle_path, report, repo_root=self.repo_root)
                if bundle_res.get('overwrite_conflict'):
                    return self._incomplete(round_n, 'movers bundle identity conflict for R%d — a '
                                            'DIFFERENT report already recorded (no bytes changed)' % round_n)

            self._fault('after_bundle_before_delta')
            # working-board round deltas ONLY for the latest round (a historical repair must leave the
            # working board's displayed movement on the latest round, not the repaired old round).
            injected = 0
            if not historical and os.path.exists(working):
                injected = MV.inject_working(working, report)

            # ALL derivatives written; VALIDATE FIRST (C), while still FINALIZING.
            self._fault('after_derivatives_before_validation')
            val = self._validate_derivatives(round_n, entry, historical=historical)
            if not val['ok']:
                return self._incomplete(round_n, 'validation failed: %s' % val['why'])

            # FINALIZED is the FINAL durable operation (C).
            self._fault('after_validation_before_finalized')
            derivatives = {
                'board_view_working': ui_ev.get('working_bundle') if not historical else 'unchanged (historical)',
                'board_view_public': ui_ev.get('public_bundle') if not historical else 'unchanged (historical)',
                'release_contract': (not historical),
                'movers_json': jpath, 'movers_csv': cpath, 'movers_bundle': bundle_res.get('path'),
                'working_delta_rows': injected,
                'club_valuation': 'SKIPPED (Track A owns the club-valuation curve)',
                'positions_bundle': 'SKIPPED (values-free position map; not board-derived)',
            }
            self._set_status(round_n, FINALIZED, derivatives=derivatives,
                             finalized_at=generated_at or entry.get('generated_at'), failure=None)
            self._journal('FINALIZED', round=round_n, historical=historical,
                          movers_json=os.path.basename(jpath), injected=injected)
            return {'ok': True, 'round': round_n, 'status': FINALIZED, 'already': False,
                    'historical': historical, 'derivatives': derivatives,
                    'player_count': report['player_count'],
                    'played': report['views']['played_count'], 'dnp': report['views']['dnp_count'],
                    'bundle_chain_ok': bundle_res.get('chain_ok'),
                    'bundle_baseline_anchor_ok': bundle_res.get('baseline_anchor_ok'),
                    'validation': val}
        except FinalizationFault as e:
            # a mid-pass fault leaves the round FINALIZING (the honest unfinalized state a restart
            # detects); the canonical commit is untouched. Re-raise so the caller/test observes it.
            self._journal('FINALIZE_FAULT', round=round_n, point=str(e))
            raise

    def _incomplete(self, round_n, why):
        self._set_status(round_n, FINALIZATION_INCOMPLETE, failure=why)
        self._journal('FINALIZATION_INCOMPLETE', round=int(round_n), why=why)
        return {'ok': False, 'round': int(round_n), 'status': FINALIZATION_INCOMPLETE, 'why': why}

    # -- validation of the derivatives against the committed state -------------------------------
    def _validate_derivatives(self, round_n, entry, *, historical=False):
        """Confirm the round's derivatives exist, parse, and cohere. For the latest round the working
        board stamp must equal the committed board and carry the round delta + release contract; for a
        historical repair those working-board checks are skipped (it stays on the latest round). The
        movers report's committed board id is checked against the round's OWN evidence (not the current
        board). Returns {'ok', 'why', 'checks'}."""
        round_n = int(round_n)
        checks, fails = {}, []
        committed_board = MV._md5(os.path.join(self.repo_root, 'data', 'rl_build', 'rl_app_data.json'))
        board_after = (entry or {}).get('board_md5_after')

        jpath, cpath, _ = MV.movers_paths(self.repo_root, round_n)
        rep = None
        if not os.path.exists(jpath):
            fails.append('movers JSON missing')
        else:
            try:
                with open(jpath) as f:
                    rep = json.load(f)
            except (OSError, ValueError) as e:
                fails.append('movers JSON unparseable: %s' % e)
        if rep is not None:
            checks['movers_board_matches_txn'] = (rep.get('board_md5_after') == board_after)
            if rep.get('board_md5_after') != board_after:
                fails.append('movers report board %s != this round committed board %s'
                             % (str(rep.get('board_md5_after'))[:8], str(board_after)[:8]))
            # the report's frozen release identity must match the stored governing identity
            if entry.get('release_identity') and rep.get('release_identity') != entry.get('release_identity'):
                fails.append('movers report release identity != stored governing identity')
        checks['movers_csv_present'] = os.path.exists(cpath)
        if not os.path.exists(cpath):
            fails.append('movers CSV missing')

        ui_data = os.path.join(self.repo_root, 'ui', 'data')
        bundle_path = os.path.join(ui_data, 'movers.js')
        if os.path.isdir(ui_data):
            try:
                bundle = MV.load_bundle(bundle_path, repo_root=self.repo_root)
            except (OSError, ValueError) as e:
                bundle = None
                fails.append('movers bundle unparseable: %s' % e)
            if bundle is not None:
                bi = bundle.get('integrity') or {}
                checks['bundle_has_round'] = round_n in (bundle.get('rounds') or [])
                checks['bundle_chain_ok'] = bi.get('board_chain_ok')
                checks['bundle_baseline_anchor_ok'] = bi.get('baseline_anchor_ok')
                checks['bundle_no_overwrite_conflict'] = not bi.get('overwrite_conflict_last_write')
                if round_n not in (bundle.get('rounds') or []):
                    fails.append('round %d absent from the movers bundle' % round_n)
                if bi.get('board_chain_ok') is False:
                    fails.append('movers bundle board-identity chain broken')
                if bi.get('baseline_anchor_ok') is False:
                    fails.append('movers bundle does not anchor to the release baseline board')
                if bi.get('overwrite_conflict_last_write'):
                    fails.append('movers bundle overwrite conflict')

            working = os.path.join(ui_data, MV.WORKING_BUNDLE_NAME)
            if not historical and os.path.exists(working):
                try:
                    w = SA.StagedRoundApplier._parse_bundle(working)
                    stamp = (w.get('stamp') or {})
                    wboard = stamp.get('srcmd5') or stamp.get('board')
                    checks['working_stamp_matches_board'] = (wboard == committed_board)
                    if wboard != committed_board:
                        fails.append('working board stamp %s != committed board %s'
                                     % (str(wboard)[:8], str(committed_board)[:8]))
                    # the FULL release contract must be present for the browser lineage check
                    if not (stamp.get('release') or {}).get('balanced_board_md5'):
                        fails.append('working board stamp carries no release contract (stamp.release)')
                    ninj = sum(1 for row in w.get('players', [])
                               if row.get('dRound') is not None or row.get('dRoundRank') is not None)
                    checks['working_delta_injected'] = ninj
                    if ninj == 0:
                        fails.append('no round-delta injected into the working board')
                except (OSError, ValueError, KeyError) as e:
                    fails.append('working board bundle unreadable: %s' % e)

        return {'ok': not fails, 'why': '; '.join(fails), 'checks': checks}

    # -- resume / repair ------------------------------------------------------------------------
    def finalize_pending(self, *, generated_at=None, reconcile=True):
        """RECONCILE first (reconstruct records for committed-but-unrecorded rounds), then finish every
        committed-but-unfinalized round in order. Called on restart + at the start of run/catchup."""
        if reconcile:
            self.reconcile(generated_at=generated_at)
        done = []
        for r in self.unfinalized_rounds():
            res = self.finalize_round(r, generated_at=generated_at)
            done.append(res)
            if not res.get('ok'):
                break
        return {'pending': done, 'clean': all(d.get('ok') for d in done)}

    def repair(self, round_n=None, *, generated_at=None):
        """Rebuild derivatives from the committed inputs. With a round, force-repairs that round (a
        historical round rebuilds only its report + bundle entry, leaving the working board on the
        latest round). Without, reconciles + repairs every unfinalized round in order. Never re-applies
        scores; never alters the canonical store/board/ledger/history."""
        self.reconcile(generated_at=generated_at)
        if round_n is not None:
            return self.finalize_round(int(round_n), generated_at=generated_at, force=True)
        out = []
        for r in self.unfinalized_rounds():
            out.append(self.finalize_round(r, generated_at=generated_at, force=True))
        return {'repaired': out, 'clean': all(o.get('ok') for o in out)}
