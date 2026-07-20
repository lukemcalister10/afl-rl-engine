"""ROUND FINALIZE — journaled, idempotent post-commit finalization of a committed round.

The core weekly transaction (staged_apply) commits the CANONICAL state ATOMICALLY: store, board,
sidecar, boot manifest, ledger, and the three histories. THAT commit is the source of truth. Everything
downstream — the Matchday UI board bundles (board_view_working.js / board_view_public.js), the
per-round movers report (JSON + CSV), the accumulated UI movers bundle (ui/data/movers.js), and the
round-delta injection into the working board — is RE-DERIVABLE from that committed state.

This module runs those derivations as a SEPARATE, JOURNALED FINALIZATION phase, so that:

  * a failure in a re-derivable output NEVER rolls back a valid canonical commit — the scores stay
    committed exactly once; only the derived outputs are (re)built;
  * the finalization status of every round is DURABLE (finalization_state.json + a journal), so a
    restart can DETECT a committed-but-unfinalized round and FINISH it (finalize) or REBUILD a
    partial / failed derivation (repair) before the round is treated complete or the next round is
    allowed to advance;
  * finalization is IDEMPOTENT — re-running it reproduces the same derivatives and NEVER silently
    overwrites a DIFFERENT historical movers report (a same-round report with a different board id is
    an integrity break, kept as a flag, not overwritten).

STATES (per round, in finalization_state.json):
    CORE_COMMITTED         the canonical transaction committed; finalization has not completed.
    FINALIZING             a finalization pass is in progress (a crash here is detected on restart).
    FINALIZATION_INCOMPLETE a derivation step failed; the canonical commit stands; repair is required.
    FINALIZED              every owner-facing derivative was generated AND validated.

run / catchup REFUSE to advance while a prior committed round is not FINALIZED (advance_blocked()).

Derivatives finalized here:
    board_view_working.js + board_view_public.js       (refresh_ui / ui/tools/extract_board_view.py)
    dRound / dRoundRank / dRoundPosRank in the working  (round_movers.inject_working)
    movers/movers_R<N>.json + .csv                      (round_movers.write_report_json/_csv)
    ui/data/movers.js accumulated bundle                (round_movers.accumulate_bundle)
Deliberately NOT finalized here (out of scope this build):
    ui/data/club_valuation.js   — Track A owns the club-valuation curve; no temporary curve rule here.
    ui/app/positions_data.js    — values-free position map derived from the owner CSV, not the board.
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

# the ordered finalization fault points (the failure-injection matrix, directive F)
FAULT_POINTS = (
    'after_core_commit_before_ui',        # (a) after the canonical commit, before any UI refresh
    'during_working_board_refresh',       # (b) as the working/public board refresh begins
    'after_board_before_movers_json',     # (c) after the board bundles, before the movers JSON
    'after_json_before_csv',              # (d) after the movers JSON, before the CSV
    'after_json_csv_before_bundle',       # (e) after JSON+CSV, before the accumulated bundle
    'after_bundle_before_delta',          # (f) after the bundle, before the working-board delta inject
    'after_all_before_final_validation',  # (g) after every file, before the final validation
    # (h) a hard termination anywhere in finalization is simulated by killing the process mid-pass;
    #     on restart the FINALIZING status is detected and repaired.
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
        self.txn_root = txn_root    # forwarded to the applier's refresh_ui environment

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
            if v is not None or k not in entry:
                entry[k] = v
        self._save(st)
        self._journal('STATUS', round=int(round_n), status=status)
        return entry

    # -- queries --------------------------------------------------------------------------------
    def status(self, round_n):
        return (self._load()['rounds'].get(str(int(round_n))) or {}).get('status')

    def entry(self, round_n):
        return self._load()['rounds'].get(str(int(round_n)))

    def finalized_rounds(self):
        st = self._load()
        return sorted(int(r) for r, e in st['rounds'].items() if e.get('status') == FINALIZED)

    def unfinalized_rounds(self):
        """Rounds that committed but are NOT yet FINALIZED (a restart must finish these first)."""
        st = self._load()
        return sorted(int(r) for r, e in st['rounds'].items() if e.get('status') in _UNFINALIZED)

    def advance_blocked(self, next_round):
        """Refuse to advance to `next_round` while the immediately-preceding committed round is not
        FINALIZED. Returns the blocking round number, or None if clear to advance."""
        prev = int(next_round) - 1
        e = self.entry(prev)
        if e and e.get('status') in _UNFINALIZED:
            return prev
        # also block if ANY earlier committed round is unfinalized (never leapfrog a broken round)
        un = [r for r in self.unfinalized_rounds() if r < int(next_round)]
        return min(un) if un else None

    # -- record the canonical commit (called immediately after apply_snapshot succeeds) ---------
    def record_core_committed(self, round_n, *, season, played, evidence, generated_at=None):
        """Persist the CORE_COMMITTED record with everything finalization + repair need to re-derive
        the round's outputs WITHOUT re-applying scores (the played score-map + the txn evidence)."""
        round_n = int(round_n)
        entry = {
            'status': CORE_COMMITTED, 'round': round_n, 'season': int(season),
            'previous_round': round_n - 1,
            'txn_id': (evidence or {}).get('txn_id'),
            'store_md5_before': (evidence or {}).get('store_md5_before'),
            'store_md5_after': (evidence or {}).get('store_md5_after'),
            'board_md5_before': (evidence or {}).get('board_md5_before'),
            'board_md5_after': (evidence or {}).get('board_md5_after'),
            'played': {k: played[k] for k in sorted(played or {})},
            'generated_at': generated_at, 'core_committed_at': generated_at,
            'finalized_at': None, 'derivatives': None, 'failure': None,
        }
        st = self._load()
        st['rounds'][str(round_n)] = entry
        self._save(st)
        self._journal('CORE_COMMITTED', round=round_n, txn_id=entry['txn_id'],
                      board_md5_after=entry['board_md5_after'])
        return entry

    def _evidence(self, entry):
        return {'store_md5_before': entry.get('store_md5_before'),
                'store_md5_after': entry.get('store_md5_after'),
                'board_md5_before': entry.get('board_md5_before'),
                'board_md5_after': entry.get('board_md5_after'),
                'txn_id': entry.get('txn_id')}

    def _fault(self, point):
        if self.fault is not None:
            self.fault(point)

    # -- the finalization pass ------------------------------------------------------------------
    def finalize_round(self, round_n, *, generated_at=None, force=False):
        """Generate + validate every owner-facing derivative for a committed round, idempotently.

        A FINALIZED round with valid derivatives is a no-op unless `force` (repair). Any derivation
        failure marks the round FINALIZATION_INCOMPLETE and returns {'ok': False, ...} — it NEVER
        rolls back or re-applies the canonical commit. Returns an evidence dict."""
        round_n = int(round_n)
        entry = self.entry(round_n)
        if entry is None:
            raise RuntimeError('round %d has no CORE_COMMITTED record — nothing to finalize' % round_n)
        if entry.get('status') == FINALIZED and not force:
            val = self._validate_derivatives(round_n, entry)
            if val['ok']:
                return {'ok': True, 'round': round_n, 'status': FINALIZED, 'already': True,
                        'validation': val}
            # FINALIZED but a derivative drifted / is missing -> fall through and repair.

        played = entry.get('played') or {}
        evidence = self._evidence(entry)
        self._set_status(round_n, FINALIZING)
        self._journal('FINALIZE_BEGIN', round=round_n, force=bool(force))
        try:
            self._fault('after_core_commit_before_ui')

            # (1) UI board bundles (working + public) from the committed board
            self._fault('during_working_board_refresh')
            applier = SA.StagedRoundApplier.for_repo(self.repo_root, txn_root=self.txn_root)
            ui_ev = applier.refresh_ui()
            if not (ui_ev.get('ran') and ui_ev.get('ok')):
                return self._incomplete(round_n, 'board_view refresh failed: rc=%s %s'
                                        % (ui_ev.get('rc'), (ui_ev.get('stderr_tail') or '')[:200]))

            # (2) movers report JSON
            self._fault('after_board_before_movers_json')
            report = MV.build_report(self.repo_root, round_n, played=played, evidence=evidence,
                                     generated_at=generated_at or entry.get('generated_at'))
            jpath = MV.write_report_json(self.repo_root, round_n, report)

            # (3) movers report CSV
            self._fault('after_json_before_csv')
            cpath = MV.write_report_csv(self.repo_root, round_n, report)

            # (4) accumulated UI movers bundle (never silently overwrite a DIFFERENT historical report)
            self._fault('after_json_csv_before_bundle')
            ui_data = os.path.join(self.repo_root, 'ui', 'data')
            bundle_path = os.path.join(ui_data, 'movers.js')
            bundle_res = {'path': None}
            if os.path.isdir(ui_data):
                bundle_res = MV.accumulate_bundle(bundle_path, report, repo_root=self.repo_root)
                if bundle_res.get('overwrite_conflict'):
                    return self._incomplete(round_n, 'movers bundle overwrite conflict for R%d — a '
                                            'DIFFERENT board id already recorded for this round' % round_n)

            # (5) round-delta injection into the working board bundle
            self._fault('after_bundle_before_delta')
            working = os.path.join(ui_data, 'board_view_working.js')
            injected = MV.inject_working(working, report) if os.path.exists(working) else 0

            # (6) final validation of everything above
            self._fault('after_all_before_final_validation')
            derivatives = {
                'board_view_working': ui_ev.get('working_bundle'),
                'board_view_public': ui_ev.get('public_bundle'),
                'movers_json': jpath, 'movers_csv': cpath,
                'movers_bundle': bundle_res.get('path'),
                'working_delta_rows': injected,
                'club_valuation': 'SKIPPED (Track A owns the club-valuation curve)',
                'positions_bundle': 'SKIPPED (values-free position map; not board-derived)',
            }
            self._set_status(round_n, FINALIZED, derivatives=derivatives,
                             finalized_at=generated_at or entry.get('generated_at'), failure=None)
            val = self._validate_derivatives(round_n, self.entry(round_n))
            if not val['ok']:
                return self._incomplete(round_n, 'post-finalization validation failed: %s' % val['why'])
            self._journal('FINALIZED', round=round_n, movers_json=os.path.basename(jpath),
                          injected=injected, chain_ok=bundle_res.get('chain_ok'))
            return {'ok': True, 'round': round_n, 'status': FINALIZED, 'already': False,
                    'derivatives': derivatives, 'player_count': report['player_count'],
                    'played': report['views']['played_count'], 'dnp': report['views']['dnp_count'],
                    'bundle_chain_ok': bundle_res.get('chain_ok'),
                    'bundle_baseline_anchor_ok': bundle_res.get('baseline_anchor_ok'),
                    'validation': val}
        except FinalizationFault as e:
            # a mid-pass fault leaves the round FINALIZING (the honest "unfinalized" state a restart
            # detects); the canonical commit is untouched. Re-raise so the caller/test observes it.
            self._journal('FINALIZE_FAULT', round=round_n, point=str(e))
            raise

    def _incomplete(self, round_n, why):
        self._set_status(round_n, FINALIZATION_INCOMPLETE, failure=why)
        self._journal('FINALIZATION_INCOMPLETE', round=int(round_n), why=why)
        return {'ok': False, 'round': int(round_n), 'status': FINALIZATION_INCOMPLETE, 'why': why}

    # -- validation of the derivatives against the committed state -------------------------------
    def _validate_derivatives(self, round_n, entry):
        """Confirm the round's derivatives exist, parse, and cohere with the committed board/store.
        Returns {'ok': bool, 'why': str, 'checks': {...}}."""
        round_n = int(round_n)
        checks, fails = {}, []
        committed_board = MV._md5(os.path.join(self.repo_root, 'data', 'rl_build', 'rl_app_data.json'))
        board_after = (entry or {}).get('board_md5_after')

        # movers JSON exists, parses, and its committed board id matches this round's txn evidence
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
                fails.append('movers report board %s != committed round board %s'
                             % (str(rep.get('board_md5_after'))[:8], str(board_after)[:8]))
        checks['movers_csv_present'] = os.path.exists(cpath)
        if not os.path.exists(cpath):
            fails.append('movers CSV missing')

        # accumulated bundle: this round present, chain + baseline anchor intact, no overwrite conflict
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

            # board_view working stamp coheres with the committed board
            working = os.path.join(ui_data, 'board_view_working.js')
            if os.path.exists(working):
                try:
                    w = SA.StagedRoundApplier._parse_bundle(working)
                    stamp = (w.get('stamp') or {})
                    wboard = stamp.get('srcmd5') or stamp.get('board')
                    checks['working_stamp_matches_board'] = (wboard == committed_board)
                    if wboard != committed_board:
                        fails.append('working board stamp %s != committed board %s'
                                     % (str(wboard)[:8], str(committed_board)[:8]))
                    # the round-delta was injected for at least some rows
                    ninj = sum(1 for row in w.get('players', [])
                               if row.get('dRound') is not None or row.get('dRoundRank') is not None)
                    checks['working_delta_injected'] = ninj
                    if ninj == 0:
                        fails.append('no round-delta injected into the working board')
                except (OSError, ValueError, KeyError) as e:
                    fails.append('working board bundle unreadable: %s' % e)

        return {'ok': not fails, 'why': '; '.join(fails), 'checks': checks}

    # -- resume / repair ------------------------------------------------------------------------
    def finalize_pending(self, *, generated_at=None):
        """Finish every committed-but-unfinalized round, in order. Called on restart and at the start
        of a run/catchup so a prior crash's half-finalized round is completed before new work."""
        done = []
        for r in self.unfinalized_rounds():
            res = self.finalize_round(r, generated_at=generated_at)
            done.append(res)
            if not res.get('ok'):
                break   # stop at the first round that will not finalize — do not leapfrog it
        return {'pending': done, 'clean': all(d.get('ok') for d in done)}

    def repair(self, round_n=None, *, generated_at=None):
        """Explicitly rebuild derivatives from the committed inputs. With a round, repairs that round
        (force). Without, repairs every unfinalized round in order. Never re-applies scores."""
        if round_n is not None:
            return self.finalize_round(int(round_n), generated_at=generated_at, force=True)
        out = []
        for r in self.unfinalized_rounds():
            out.append(self.finalize_round(r, generated_at=generated_at, force=True))
        return {'repaired': out, 'clean': all(o.get('ok') for o in out)}
