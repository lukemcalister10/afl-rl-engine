"""STAGED-APPLY — the SAFE weekly round-score store-write: STAGE -> VALIDATE -> ATOMIC SWAP.

This is the hardened successor to round_apply.RoundApplier (PR #125). PR #125's applier mutated the
LIVE files in sequence (store, then board, then manifest, then ledger) with NO staging and NO
rollback: a failure after the store write left a NEW store with an OLD board / manifest / ledger — a
silently broken build. This module closes that hole. It:

  1. STAGES every change in a throwaway workspace (a full repo-shaped copy) — the LIVE files are NOT
     touched while validation runs.
  2. VALIDATES the STAGED outputs end-to-end (store parses, only-permitted rows changed, board
     regenerates, board source-stamp == staged store, boot pins == staged store+board, Guard 5 GREEN
     against the staged set, ledger == the snapshot triples, board player-universe unchanged).
  3. Only after EVERY staged gate passes does it ATOMICALLY replace the live files, inside a
     TRANSACTION DIRECTORY that keeps immutable originals + the staged replacements + a manifest + a
     phase journal, so a failure (or a crash) during the swap ROLLS BACK every original — the store
     is never left with a stale board / manifest / ledger.

CONSUMES the round_entry SNAPSHOT (engine/rl_after/ingestion/round_entry.py), not a live re-resolve:
the snapshot already carries stable player IDs + exact scores + the source-store identity, so the
apply is a pure transaction authorization. The snapshot -> preview conversion (preview_from_snapshot)
preserves score meaning EXACTLY — one played game at the snapshot score, merged onto the store entry
with the SAME arithmetic score_ingestor uses — and is cross-checked in the proof.

GATE: like round_apply, the store write is HARD-GATED OFF (score_ingestor.APPLY_DEFAULT=False + env
INGEST_SCORE_APPLY unset). apply_snapshot() refuses on the real store until BOTH halves are armed;
the proofs arm the gate IN-PROCESS against SCRATCH copies only. This module never writes the real
store in this build.

SCOPE FENCE: merges scores and regenerates derived artifacts. It NEVER touches valuation logic, the
curve, the model, or pricing. It NEVER invents a numerical-determinism verdict — the board is
validated for STRUCTURE, source-stamp coherence, Guard-5 pins and player universe, not for a
cross-run/cross-machine value guarantee (that is a separate, external item).
"""
import json, os, sys, shutil, tempfile, subprocess, hashlib, stat

try:
    from . import round_entry as RE
    from . import round_history as RH
    from .score_ingestor import (IngestionGatedError, _apply_enabled, APPLY_DEFAULT, _APPLY_ENV,
                                 IngestionPreview, SeasonAppend, ScoreIngestor, ROUND_DECIMALS)
    from .round_score_parser import RoundScore
    from .round_apply import (RoundApplier, DEFAULT_SEASON_ROUNDS, SeasonBoundError,
                              DuplicateRoundError, PreviewNotCleanError, load_ledger, save_ledger,
                              ledger_key, _md5_full)
except (ImportError, ValueError):    # allow direct-script / non-package execution
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import round_entry as RE  # type: ignore
    import round_history as RH  # type: ignore
    from score_ingestor import (IngestionGatedError, _apply_enabled, APPLY_DEFAULT, _APPLY_ENV,  # type: ignore
                                IngestionPreview, SeasonAppend, ScoreIngestor, ROUND_DECIMALS)
    from round_score_parser import RoundScore  # type: ignore
    from round_apply import (RoundApplier, DEFAULT_SEASON_ROUNDS, SeasonBoundError,  # type: ignore
                             DuplicateRoundError, PreviewNotCleanError, load_ledger, save_ledger,
                             ledger_key, _md5_full)

# transaction-directory + journal terminal states
TXN_DIRNAME = '.weekly_txn'
STATUS_STAGING = 'STAGING'
STATUS_VALIDATED = 'VALIDATED'
STATUS_COMMITTING = 'COMMITTING'
STATUS_COMMITTED = 'COMMITTED'
STATUS_ROLLED_BACK = 'ROLLED_BACK'
STATUS_ABORTED_PRECOMMIT = 'ABORTED_PRECOMMIT'
STATUS_RECOVERED = 'RECOVERED'
_TERMINAL = {STATUS_COMMITTED, STATUS_ROLLED_BACK, STATUS_ABORTED_PRECOMMIT, STATUS_RECOVERED}

# the live targets a weekly apply replaces (repo-root-relative). The store/board/sidecar/manifest/
# ledger are the original five; value_history + rank_history are the persistent per-player round-by-
# round records, added to the transaction so they commit atomically with the board and roll back /
# recover on any failure (a crash can never leave a half-written history). NEW targets that did not
# exist pre-apply are REMOVED on rollback/recovery (pre_apply_present in the manifest), so a first-
# round history leaves no partial state either.
TARGETS = (
    ('store',   os.path.join('engine', 'rl_after', 'rl_model_data.json')),
    ('board',   os.path.join('data', 'rl_build', 'rl_app_data.json')),
    ('sidecar', os.path.join('data', 'rl_build', 'rl_app_data.json.srcmd5')),
    ('manifest', os.path.join('data', 'expected_boot.json')),
    # season-state: the authoritative dynamic calendar_progress + exposure_pace (supervisor 2nd review).
    # Derived from the STAGED store after applying scores + advancing the round, BEFORE the board regen, and
    # committed ATOMICALLY with the store/board so a crash can never leave a new round on stale season-state.
    ('season_state', os.path.join('data', 'season_state.json')),
    ('ledger',  os.path.join('engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json')),
    ('value_history', os.path.join('engine', 'rl_after', 'ingestion', 'value_history.json')),
    ('rank_history',  os.path.join('engine', 'rl_after', 'ingestion', 'rank_history.json')),
    ('pos_rank_history', os.path.join('engine', 'rl_after', 'ingestion', 'pos_rank_history.json')),
)


# ---- refusals (all fire BEFORE any staging; a refused apply leaves everything byte-unchanged) ----
class StaleSnapshotError(RuntimeError):
    """The snapshot's source-store md5 != the CURRENT live store md5 — the store moved since the
    snapshot was stamped. Applying would merge onto a store the owner never inspected. REFUSED."""


class AlteredSnapshotError(RuntimeError):
    """The snapshot's content_hash does not verify (or the snapshot is not the v2 strong form) — it
    was edited after stamping, or is a legacy snapshot the strong apply cannot trust. REFUSED."""


class ResidueOpenError(RuntimeError):
    """The snapshot still carries open residue (unconfirmed lines) — nothing may apply until every
    line is confirmed or skipped. REFUSED."""


class StagedValidationError(RuntimeError):
    """A staged gate failed (store parse / permitted-diff / board / source-stamp / boot pins /
    Guard 5 / ledger / player universe). The live files were NOT touched. REFUSED."""


class IncompleteTransactionError(RuntimeError):
    """An earlier transaction did not reach a terminal state (a crash mid-apply). apply() refuses
    until `recover` restores the originals — never stack a new apply on an unrecovered one."""
    def __init__(self, txns):
        self.txns = txns
        super().__init__("incomplete transaction(s) present — run `recover` first: %s"
                         % ", ".join(os.path.basename(t) for t in txns))


class FaultInjected(RuntimeError):
    """A deliberately injected fault (failure-injection proof only). Treated like any caught failure:
    a pre-commit fault aborts with the live files untouched; a commit-phase fault rolls back."""


class FVProvenanceError(RuntimeError):
    """FAIL-CLOSED forward-valuation provenance (2026-07-20 hardening). The distribution_pricing module
    the staged board build would load is NOT inside the staged repo, or is not byte-identical to the
    staged source. An ambient/workspace forward_valuation (e.g. a stale 21d530bf on the RL_FV default
    path) must NEVER produce, pin or commit a board. HALT before board generation."""


class ConfigPolicyError(RuntimeError):
    """An inherited RL_*/PAR_* valuation flag is unknown to, or conflicts with, the release config
    manifest (data/model_config.json). The weekly board build must use exactly the accepted policy
    surface — never arbitrary inherited shell flags. HALT before any staging."""


# ---- snapshot -> preview bridge (NO re-resolution; score meaning preserved EXACTLY) -------------
def preview_from_snapshot(snapshot, store):
    """Build a score_ingestor.IngestionPreview from a stamped snapshot, WITHOUT re-resolving names.

    Each resolved row is one PLAYED round at its snapshot score (a FootyWire export lists only players
    who played; a score present == played). The batch is one game at that score; merged onto the
    store's season entry with the SAME weighted-mean arithmetic ScoreIngestor.preview uses — so the
    conversion never changes score meaning (proven by equivalence in the failure-injection proof).
    Anomaly checks (impossible score / retired / cycle-year / duplicate) are RE-RUN here so a garbage
    score is still caught by the CLEAN gate. `store` is the parsed store list (rows)."""
    ing = ScoreIngestor(store=store)          # reuses _before_entry / _mean / _anomalies (per-key; no re-resolve)
    season = int(snapshot['season_year'])
    rnd = int(snapshot['round'])
    appends, anomalies = [], []
    for r in snapshot['resolved']:
        key = r['key']; sid = r['stable_player_id']; player = r['name']
        score = float(r['score'])
        row = ing._key_to_row.get(key)
        if row is None:
            # the snapshot's key is not in the current store — a stale/misapplied snapshot. Surfaced
            # as a resolve exception so the CLEAN gate refuses (never merge onto a missing row).
            raise StagedValidationError(
                "snapshot key %r (%s) is not present in the current store — snapshot does not match "
                "this store" % (key, player))
        n = 1; total = score
        batch_entry = {'year': season, 'avg': ing._mean(total, n), 'games': n}
        before = ing._before_entry(key, season)
        if before is None:
            merged_entry = dict(batch_entry)
        else:
            mg = before['games'] + n
            mtotal = before['avg'] * before['games'] + total
            merged_entry = {'year': season, 'avg': ing._mean(mtotal, mg), 'games': mg}
        rlist = [RoundScore(player, rnd, score, True, source_ref="snapshot")]
        anoms = ing._anomalies(sid, key, player, row, season, rlist)
        anomalies.extend(anoms)
        appends.append(SeasonAppend(sid, key, player, season, before, batch_entry, merged_entry,
                                    rounds=[(rnd, score, True)], anomalies=anoms))
    appends.sort(key=lambda a: a.key or '')
    return IngestionPreview(season, appends, [], anomalies, store_md5=None)


# ---- small fs helpers ---------------------------------------------------------------------------
def _md5_file_full(path):
    return _md5_full(path)


def _atomic_place(src, dst):
    """Copy `src` into a temp beside `dst`, fsync, then os.replace it over `dst` (atomic swap on the
    same filesystem). `src` is NOT consumed — the staged copy / immutable original is preserved as
    evidence. Raises if src and dst are not on the same filesystem (a mis-configured txn root)."""
    d = os.path.dirname(os.path.abspath(dst))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.wkupd_swap_', dir=d)
    try:
        with os.fdopen(fd, 'wb') as f:
            with open(src, 'rb') as s:
                shutil.copyfileobj(s, f)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, dst)          # atomic
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _clear_ro(path):
    for p in (path, path + '.srcmd5'):
        if os.path.exists(p):
            try:
                os.chmod(p, stat.S_IWUSR | stat.S_IRUSR)
            except OSError:
                pass


class StagedApplyResult:
    __slots__ = ('round', 'season', 'players_applied', 'store_md5_before', 'store_md5_after',
                 'board_md5_before', 'board_md5_after', 'ledger_added', 'ledger_total',
                 'txn_dir', 'guard5_green', 'triples', 'history')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    def as_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}


class StagedRoundApplier:
    """STAGE -> VALIDATE -> ATOMIC SWAP, transactional, with rollback + crash recovery.

    Constructed with an explicit repo_root so the proofs bind it to SCRATCH repo copies and the real
    single source is never a proof target. The transaction directory lives UNDER repo_root (same
    filesystem as the live files) so the final os.replace swaps are atomic; the heavy validation
    workspace is a disposable tempdir (anywhere)."""

    def __init__(self, repo_root, season_rounds=None, txn_root=None, workspace_base=None, fault=None):
        self.repo_root = os.path.abspath(repo_root)
        self.season_rounds = int(season_rounds if season_rounds is not None
                                 else os.environ.get('RL_SEASON_ROUNDS', DEFAULT_SEASON_ROUNDS))
        # txn root MUST be on the same filesystem as the live files -> default under repo_root.
        self.txn_root = os.path.abspath(txn_root) if txn_root else os.path.join(
            self.repo_root, 'engine', 'rl_after', 'ingestion', TXN_DIRNAME)
        self.workspace_base = workspace_base       # None => tempfile default
        self.fault = fault                          # test hook: fault(phase) may raise
        self.fv_dir_override = None                 # test hook: force RL_FV to a specific dir (red-path)
        self.config_hash = None                     # stamped by _assert_config_policy (item 2)

    @classmethod
    def for_repo(cls, repo_root, **kw):
        return cls(repo_root, **kw)

    # -- live target paths ----------------------------------------------------------------------
    def _live(self, name):
        for n, rel in TARGETS:
            if n == name:
                return os.path.join(self.repo_root, rel)
        raise KeyError(name)

    def _store_path(self):
        return self._live('store')

    def _fault(self, phase):
        if self.fault is not None:
            self.fault(phase)

    # ===========================================================================================
    # RECOVERY — detect + restore incomplete transactions
    # ===========================================================================================
    def _txn_dirs(self):
        if not os.path.isdir(self.txn_root):
            return []
        return sorted(os.path.join(self.txn_root, d) for d in os.listdir(self.txn_root)
                      if os.path.isdir(os.path.join(self.txn_root, d)) and not d.startswith('_'))

    def _read_txn_manifest(self, txn_dir):
        mp = os.path.join(txn_dir, 'manifest.json')
        if not os.path.exists(mp):
            return None
        try:
            with open(mp) as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def scan_incomplete(self):
        """Return [txn_dir] for every transaction not in a terminal state (a crash mid-apply)."""
        out = []
        for d in self._txn_dirs():
            man = self._read_txn_manifest(d)
            if man is None or man.get('status') not in _TERMINAL:
                out.append(d)
        return out

    def recover(self, generated_at=None):
        """Explicitly recover every incomplete transaction: ROLL BACK to the immutable originals (the
        safe direction — a partial commit is reverted to the pre-apply state), then mark the txn
        RECOVERED. Never deletes evidence. Returns a report dict."""
        report = {'recovered': [], 'clean': True}
        for d in self.scan_incomplete():
            man = self._read_txn_manifest(d) or {}
            # restore every backed-up original (COMMIT_BEGIN reached) -> full pre-apply state, and
            # remove any target created by this txn that was absent pre-apply (no partial state).
            restored = self._restore_from_txn(d)
            self._journal(d, 'RECOVER_ROLLBACK', restored=restored, at=generated_at)
            self._set_status(d, STATUS_RECOVERED, failure=man.get('failure'),
                             recovered_restored=restored)
            report['recovered'].append({'txn': os.path.basename(d), 'restored': restored})
            report['clean'] = False
        return report

    # ===========================================================================================
    # JOURNAL + MANIFEST
    # ===========================================================================================
    def _journal(self, txn_dir, event, **fields):
        line = {'event': event}
        line.update(fields)
        jp = os.path.join(txn_dir, 'journal.jsonl')
        with open(jp, 'a') as f:
            f.write(json.dumps(line, sort_keys=True) + '\n')
            f.flush(); os.fsync(f.fileno())

    def _write_manifest(self, txn_dir, man):
        mp = os.path.join(txn_dir, 'manifest.json')
        fd, tmp = tempfile.mkstemp(prefix='.man_', dir=txn_dir)
        with os.fdopen(fd, 'w') as f:
            json.dump(man, f, indent=2, sort_keys=True)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, mp)

    def _set_status(self, txn_dir, status, **extra):
        man = self._read_txn_manifest(txn_dir) or {}
        man['status'] = status
        for k, v in extra.items():
            if v is not None or k not in man:
                man[k] = v
        self._write_manifest(txn_dir, man)
        self._journal(txn_dir, 'STATUS', status=status)

    # ===========================================================================================
    # THE APPLY (staged, transactional)
    # ===========================================================================================
    def apply_snapshot(self, snapshot, *, generated_at=None, txn_id=None, keep_workspace=False):
        """Apply one stamped round snapshot to the store via STAGE -> VALIDATE -> ATOMIC SWAP.

        Order: every REFUSAL (incomplete-txn / gate / stale / altered / residue / clean / season /
        dedup) fires BEFORE any staging, so a refused apply leaves store, board, sidecar, manifest and
        ledger byte-unchanged. Then the change is staged + validated in a workspace; only after every
        staged gate passes are the live files atomically replaced, with rollback on any failure."""
        # (R) refuse if an earlier transaction never finished — never stack on an unrecovered crash.
        incomplete = self.scan_incomplete()
        if incomplete:
            raise IncompleteTransactionError(incomplete)

        # (1) GATE — both halves, or nothing (this build ships OFF).
        if not _apply_enabled():
            raise IngestionGatedError(
                "round-score APPLY is OFF (APPLY_DEFAULT=%s, env %s unset) — this build writes nothing "
                "to the store. To apply locally, arm BOTH halves (see the launcher README); the shipped "
                "branch keeps them OFF." % (APPLY_DEFAULT, _APPLY_ENV))

        # (2) STRONG snapshot form + content-hash + store identity (the stale/altered gates).
        if not RE.is_strong(snapshot):
            raise AlteredSnapshotError(
                "snapshot is not the v2 strong form (missing schema version / full store md5 / content "
                "hash) — re-stamp it with the current round_entry tool before applying.")
        ok, reason = RE.verify_snapshot(snapshot)
        if not ok:
            raise AlteredSnapshotError("snapshot content-hash did not verify: %s" % reason)
        live_store = self._store_path()
        cur_full = _md5_file_full(live_store)
        snap_full = snapshot.get('source_store_md5_full')
        if cur_full != snap_full:
            raise StaleSnapshotError(
                "STALE snapshot: it was stamped against store %s but the live store is now %s. The store "
                "moved since the snapshot was inspected — re-enter the round against the current store."
                % ((snap_full or '')[:8], (cur_full or '')[:8]))

        # (3) RESIDUE — no open (unconfirmed) lines.
        residue_open = int((snapshot.get('counts') or {}).get('residue_open', 0))
        if residue_open:
            raise ResidueOpenError(
                "snapshot has %d open residue line(s) — confirm or skip every line first (nothing enters "
                "a snapshot unresolved)." % residue_open)
        if not snapshot.get('resolved'):
            raise StagedValidationError("snapshot has zero resolved rows — nothing to apply.")

        # (4) build the preview (no re-resolve) + CLEAN / SEASON / DEDUP (mirror round_apply, before write).
        with open(live_store) as f:
            store_rows = json.load(f)
        preview = preview_from_snapshot(snapshot, store_rows)
        if preview.exceptions:
            raise PreviewNotCleanError("snapshot preview has %d resolve exception(s)" % len(preview.exceptions))
        if preview.anomalies:
            kinds = sorted({a.kind for a in preview.anomalies})
            raise PreviewNotCleanError(
                "snapshot preview has %d anomaly(ies) %s — owner must clear before apply"
                % (len(preview.anomalies), kinds))
        bad = sorted({rnd for a in preview.appends for (rnd, _s, _p) in a.rounds
                      if not (1 <= rnd <= self.season_rounds)})
        if bad:
            raise SeasonBoundError("round(s) %s outside the season bound [1, %d]" % (bad, self.season_rounds))
        triples = set()
        for a in preview.appends:
            for (rnd, _s, _p) in a.rounds:
                triples.add(ledger_key(a.stable_player_id, preview.season_year, rnd))
        ledger = load_ledger(self._live('ledger'))
        already = set(ledger.get('applied', []))
        dups = triples & already
        if dups:
            raise DuplicateRoundError(dups)

        # (5) CONFIG POLICY (item 2) — no arbitrary inherited RL_*/PAR_* valuation flags. The board
        #     policy comes from the release config manifest; an unknown/conflicting inherited flag HALTS
        #     before any staging.
        self.config_hash = self._assert_config_policy()

        # ---- past every refusal: STAGE -> VALIDATE -> SWAP -----------------------------------
        allowed_keys = {a.key for a in preview.appends}
        return self._staged_transaction(snapshot, preview, triples, allowed_keys, store_rows,
                                         generated_at=generated_at, txn_id=txn_id,
                                         keep_workspace=keep_workspace)

    # -- STAGE + VALIDATE in a workspace, then COMMIT via the transaction dir -------------------
    def _staged_transaction(self, snapshot, preview, triples, allowed_keys, live_store_rows, *,
                            generated_at, txn_id, keep_workspace):
        os.makedirs(self.txn_root, exist_ok=True)
        txn_id = txn_id or self._mk_txn_id(snapshot, generated_at)
        txn_dir = os.path.join(self.txn_root, txn_id)
        if os.path.exists(txn_dir):
            shutil.rmtree(txn_dir)
        os.makedirs(txn_dir)
        os.makedirs(os.path.join(txn_dir, 'staged'))
        os.makedirs(os.path.join(txn_dir, 'originals'))

        store_before = _md5_file_full(self._store_path())
        board_before = _md5_file_full(self._live('board')) if os.path.exists(self._live('board')) else None
        # which targets EXISTED before this apply — a target absent here that gets created during the
        # commit must be REMOVED (not "restored") on rollback/recovery, so a first-round history (or a
        # fresh board) leaves NO partial state after a failure.
        pre_apply_present = {n: os.path.exists(os.path.join(self.repo_root, rel)) for n, rel in TARGETS}
        # FINALIZATION-RECOVERY payload, written DURABLY into the transaction manifest so the round is
        # never stranded by a crash AFTER the canonical commit but BEFORE the caller records a pending-
        # finalization entry: `played` (the per-key round score map the movers report needs) is captured
        # here from the preview, and board_md5_before is recorded, so a restart can reconstruct the
        # finalization context from the COMMITTED transaction manifest alone (round_finalize.reconcile).
        played_map = {a.key: a.rounds[0][1] for a in preview.appends if a.rounds}
        man = {'txn_id': txn_id, 'kind': 'weekly_round_apply', 'created_at': generated_at,
               'round': int(snapshot['round']), 'season': int(snapshot['season_year']),
               'snapshot_content_hash': snapshot.get('content_hash'),
               'snapshot_source_store_md5_full': snapshot.get('source_store_md5_full'),
               'store_md5_before': store_before, 'board_md5_before': board_before,
               'played': {k: played_map[k] for k in sorted(played_map)},
               'status': STATUS_STAGING, 'failure': None,
               'config_hash': self.config_hash, 'fv_provenance': None,
               'pre_apply_present': pre_apply_present, 'history': None,
               'targets': [{'name': n, 'live': rel} for n, rel in TARGETS]}
        self._write_manifest(txn_dir, man)
        self._journal(txn_dir, 'STAGE_BEGIN', round=man['round'], season=man['season'],
                      players=len(preview.appends))

        ws = None
        try:
            self._fault('before_store_staging')
            ws = self._build_workspace(txn_dir)

            # (a) MERGE into the workspace store (reuse the proven PR#125 merge; on the copy, not live)
            wsapp = self._ws_applier(ws)
            merged = wsapp._merge_into_store(preview)
            staged_store_md5 = _md5_file_full(wsapp.store_path)
            self._journal(txn_dir, 'STORE_STAGED', players_merged=merged, staged_store_md5=staged_store_md5)

            # (a2) DERIVE + ADVANCE the authoritative dynamic SEASON-STATE from the STAGED store + the new
            #      round, AFTER applying scores and BEFORE the board regen (supervisor 2nd review). The board
            #      the next phase builds therefore reflects the advanced calendar_progress and the freshly
            #      DERIVED exposure_pace (RL_REPO=ws, so the engine reads ws/data/season_state.json). Written
            #      into the workspace + committed atomically (it is a TARGET) — a crash can never leave a new
            #      round with stale Round-14 season-state, a new store with a stale exposure pace, or a board
            #      built from season-state different from its stamped state.
            _ssm = self._season_state_module()
            _ss_new = _ssm.derive(int(snapshot['round']), wsapp.store_path,
                                  season_year=int(snapshot['season_year']),
                                  season_total_rounds=self.season_rounds)
            with open(os.path.join(ws, 'data', 'season_state.json'), 'w') as _ssf:
                json.dump(_ss_new, _ssf, indent=2)
            self._journal(txn_dir, 'SEASON_STATE_STAGED', as_of_round=_ss_new['as_of_round'],
                          calendar_progress=_ss_new['calendar_progress'], exposure_pace=_ss_new['exposure_pace'],
                          source_store_md5=_ss_new['source_store_md5'],
                          eligible_durable=_ss_new['exposure_derivation']['eligible_durable_players'],
                          median_current_games=_ss_new['exposure_derivation']['median_current_games'])

            # (b) REGEN the board from the STAGED store under a STRICT, fail-closed environment:
            #     RL_FV bound to the STAGED forward_valuation, PYTHONPATH from the staged repo + pinned
            #     vendor, every ambient valuation redirect cleared, board policy from the release config
            #     manifest (RL_CONFIG_MODE=gate). FV provenance is asserted BEFORE generation, so an
            #     ambient/stale distribution_pricing (e.g. 21d530bf on the RL_FV default) HALTS here and
            #     never produces/pins/commits a board.
            self._fault('during_board_generation')
            staged_board_md5, fv_ev = self._regen_board_strict(ws)
            man = self._read_txn_manifest(txn_dir) or {}
            man['fv_provenance'] = fv_ev
            self._write_manifest(txn_dir, man)
            self._fault('after_board_generation')
            self._journal(txn_dir, 'BOARD_STAGED', staged_board_md5=staged_board_md5,
                          fv_distribution_pricing_md5=fv_ev.get('distribution_pricing_md5'),
                          fv_rl_fv=fv_ev.get('rl_fv'), config_hash=self.config_hash)

            # (c) RE-STAMP the workspace boot manifest (move store+board pins)
            self._fault('during_manifest_staging')
            wsapp._restamp_manifest(staged_store_md5, staged_board_md5)
            self._journal(txn_dir, 'MANIFEST_STAGED')

            # (d) UPDATE the workspace ledger with the exact snapshot triples
            self._fault('during_ledger_staging')
            wsl = load_ledger(wsapp.ledger_path)
            wsl['applied'] = sorted(set(wsl.get('applied', [])) | triples)
            save_ledger(wsapp.ledger_path, wsl)
            self._journal(txn_dir, 'LEDGER_STAGED', added=len(triples), total=len(wsl['applied']))

            # (d2) STAGE the persistent value + rank history from the STAGED board. The FIRST apply
            #      seeds the previous round (round-1) from the PRE-APPLY board — so the round-14 ->
            #      round-15 transition is recorded for every active player — then appends this round.
            #      Existing rounds are never overwritten (append-only). Committed atomically with the
            #      board; rolled back / removed on any failure.
            self._fault('during_history_staging')
            hist_ev = self._stage_history(ws, snapshot)
            man = self._read_txn_manifest(txn_dir) or {}
            man['history'] = hist_ev
            self._write_manifest(txn_dir, man)
            self._journal(txn_dir, 'HISTORY_STAGED', **hist_ev)

            # (e) VALIDATE the STAGED outputs (nothing live touched yet)
            guard5 = self._validate_staged(ws, live_store_rows, allowed_keys, triples, preview,
                                           staged_store_md5, staged_board_md5, snapshot)
            self._set_status(txn_dir, STATUS_VALIDATED, guard5_green=True)
            self._journal(txn_dir, 'VALIDATE_OK', guard5_green=True)

            # (f) copy validated outputs -> txn/staged (same FS as live), md5-verified identical
            staged_paths = self._collect_staged(ws, txn_dir)

            # (g) back up immutable originals -> txn/originals, then COMMIT (atomic swaps)
            self._backup_originals(txn_dir)
            self._journal(txn_dir, 'ORIGINALS_BACKED_UP')
            self._set_status(txn_dir, STATUS_COMMITTING)
            self._commit(txn_dir, staged_paths)
            self._set_status(txn_dir, STATUS_COMMITTED,
                             store_md5_after=staged_store_md5, board_md5_after=staged_board_md5)
            self._journal(txn_dir, 'COMMIT_OK')

            # keep a light permanent record; prune the heavy staged/originals payload on success.
            self._prune_committed_payload(txn_dir)

            return StagedApplyResult(
                round=int(snapshot['round']), season=int(snapshot['season_year']),
                players_applied=merged, store_md5_before=store_before, store_md5_after=staged_store_md5,
                board_md5_before=board_before, board_md5_after=staged_board_md5,
                ledger_added=len(triples), ledger_total=len(wsl['applied']), txn_dir=txn_dir,
                guard5_green=guard5, triples=sorted(triples), history=hist_ev)
        except BaseException as e:
            self._handle_failure(txn_dir, e)
            raise
        finally:
            if ws and not keep_workspace:
                shutil.rmtree(ws, ignore_errors=True)

    # -- failure handling: rollback if we were committing; otherwise pre-commit abort -----------
    def _handle_failure(self, txn_dir, exc):
        man = self._read_txn_manifest(txn_dir) or {}
        failure = {'phase': man.get('status'), 'error': '%s: %s' % (type(exc).__name__, exc)}
        self._journal(txn_dir, 'FAILURE', **failure)
        if man.get('status') == STATUS_COMMITTING:
            # a partial swap may have happened — restore EVERY original (full pre-apply state).
            restored = self._rollback(txn_dir)
            self._journal(txn_dir, 'ROLLBACK_OK', restored=restored)
            self._set_status(txn_dir, STATUS_ROLLED_BACK, failure=failure)
        else:
            # nothing live was touched (failure before COMMIT) — abort, keep evidence.
            self._set_status(txn_dir, STATUS_ABORTED_PRECOMMIT, failure=failure)

    def _restore_from_txn(self, txn_dir):
        """Return the live files to their pre-apply state from a transaction's immutable backups:
        every backed-up original is restored byte-for-byte; a target that was ABSENT pre-apply but was
        created during the commit is REMOVED (so a first-round history / fresh board leaves no partial
        state). Shared by the commit-phase rollback and the crash-recovery path."""
        orig_dir = os.path.join(txn_dir, 'originals')
        man = self._read_txn_manifest(txn_dir) or {}
        present = man.get('pre_apply_present') or {}
        restored = []
        for name, rel in TARGETS:
            ob = os.path.join(orig_dir, name)
            live = os.path.join(self.repo_root, rel)
            if os.path.exists(ob):
                _clear_ro(live)
                _atomic_place(ob, live)
                restored.append(name)
            elif present.get(name, True) is False and os.path.exists(live):
                _clear_ro(live)
                try:
                    os.remove(live)
                    restored.append(name + ':removed')
                except OSError:
                    pass
        return restored

    def _rollback(self, txn_dir):
        return self._restore_from_txn(txn_dir)

    def _commit(self, txn_dir, staged_paths):
        self._journal(txn_dir, 'COMMIT_BEGIN', order=[n for n, _ in TARGETS])
        for i, (name, rel) in enumerate(TARGETS):
            src = staged_paths.get(name)
            if src is None:
                continue
            live = os.path.join(self.repo_root, rel)
            _clear_ro(live)
            _atomic_place(src, live)
            self._journal(txn_dir, 'REPLACED', target=name)
            if i == 0:
                self._fault('after_first_replacement')
            else:
                self._fault('after_subsequent_replacement')

    # -- workspace build (a full repo-shaped copy; mirrors the proven storewrite scratch) -------
    def _build_workspace(self, txn_dir):
        base = self.workspace_base or tempfile.gettempdir()
        os.makedirs(base, exist_ok=True)
        ws = tempfile.mkdtemp(prefix='wkupd_ws_', dir=base)
        R = self.repo_root
        shutil.copytree(os.path.join(R, 'engine', 'rl_after'), os.path.join(ws, 'engine', 'rl_after'))
        shutil.copytree(os.path.join(R, 'engine', 'forward_valuation'),
                        os.path.join(ws, 'engine', 'forward_valuation'))
        wsra = os.path.join(ws, 'engine', 'rl_after')
        # rl_export.py (run with cwd=wsra) now imports fv_provenance + boot_guard + config_manifest at
        # the repo root under df5066a's fail-closed provenance preamble — copy them beside it so the
        # staged build resolves the SAME accepted provenance modules the checkout ships (never an
        # ambient one). boot_guard.py runs BOTH as a script (Guard 5, from ws root) and as an import
        # (rl_export gate mode, from wsra), so it lands in both.
        for f in ('config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py', 'boot_guard.py', 'season_state.py'):
            _src = os.path.join(R, f)
            if os.path.exists(_src):
                shutil.copyfile(_src, os.path.join(wsra, f))
        for f in ('boot_guard.py', 'config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py', 'season_state.py'):
            _src = os.path.join(R, f)
            if os.path.exists(_src):
                shutil.copyfile(_src, os.path.join(ws, f))
        shutil.copytree(os.path.join(R, 'data'), os.path.join(ws, 'data'))
        legf5 = os.path.join('session_2026-07-18', 'legf5')
        if os.path.isdir(os.path.join(R, legf5)):
            shutil.copytree(os.path.join(R, legf5), os.path.join(ws, legf5))
        return ws

    def _ws_applier(self, ws):
        wsra = os.path.join(ws, 'engine', 'rl_after')
        return RoundApplier(
            store_path=os.path.join(wsra, 'rl_model_data.json'),
            workspace_dir=wsra,
            manifest_path=os.path.join(ws, 'data', 'expected_boot.json'),
            ledger_path=os.path.join(wsra, 'ingestion', 'applied_rounds_ledger.json'),
            repo_root=ws,
            season_rounds=self.season_rounds,
            board_publish_path=os.path.join(ws, 'data', 'rl_build', 'rl_app_data.json'))

    def _freshen_published_sidecar(self, ws):
        """The board generator stamps a fresh sidecar beside the WORKSPACE board; the published copy
        (data/rl_build) must carry the SAME sidecar so the board's source-stamp stays coherent after
        the swap (round_apply published only the board, leaving a stale sidecar — fixed here)."""
        wsra = os.path.join(ws, 'engine', 'rl_after')
        src = os.path.join(wsra, 'rl_app_data.json.srcmd5')
        dst = os.path.join(ws, 'data', 'rl_build', 'rl_app_data.json.srcmd5')
        if os.path.exists(src):
            _clear_ro(dst)
            shutil.copyfile(src, dst)
        else:                       # belt-and-braces: synthesize a coherent sidecar
            board = os.path.join(ws, 'data', 'rl_build', 'rl_app_data.json')
            store = os.path.join(wsra, 'rl_model_data.json')
            side = {'source': 'rl_model_data.json', 'source_md5': _md5_file_full(store),
                    'own_md5': _md5_file_full(board), 'derived': 'rl_app_data.json', 'tier': 1}
            with open(dst, 'w') as f:
                json.dump(side, f, sort_keys=True)

    # -- FAIL-CLOSED forward-valuation provenance + accepted-config board build (2026-07-20) --------
    def _fv_dir(self, ws):
        return os.path.join(ws, 'engine', 'forward_valuation')

    def _vendor_path(self):
        v = os.environ.get('RL_VENDOR')
        if v and os.path.isdir(os.path.join(v, 'unidecode')):
            return v
        if os.path.isdir('/home/claude/rl_vendor/unidecode'):
            return '/home/claude/rl_vendor'
        return os.path.join(self.repo_root, 'vendor')

    def _season_state_module(self):
        """Import the immutable season-state derivation POLICY (repo-root season_state.py). The policy
        (population / denominator / formula / rounding) is applied to the STAGED store to derive the
        dynamic calendar_progress + exposure_pace for the new round."""
        import importlib.util
        p = os.path.join(self.repo_root, 'season_state.py')
        spec = importlib.util.spec_from_file_location('season_state_pol', p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    def _strict_regen_env(self, ws):
        """A STRICT, fail-closed environment for the staged board build. It (1) binds RL_FV to the
        STAGED forward_valuation; (2) sets PYTHONPATH from the STAGED repo only + the pinned vendor;
        (3) CLEARS every inherited RL_*/PAR_* variable (model flags AND path redirects like RL_FV,
        RL_APP_DATA, RL_Q97M_PKL, RL_V0SURF_PKL) so nothing ambient can redirect a valuation import or
        the board policy; (4) sets RL_CONFIG_MODE=gate so config_manifest.enforce loads the accepted
        release policy and halts on any conflicting inherited flag. fv_dir_override is a RED-PATH test
        hook that deliberately mis-binds RL_FV to prove the provenance guard halts."""
        wsra = os.path.join(ws, 'engine', 'rl_after')
        # clean base: keep only NON-RL_/PAR_ system vars (PATH/HOME/venv/LD_*/TMPDIR/...).
        env = {k: v for k, v in os.environ.items() if not (k.startswith('RL_') or k.startswith('PAR_'))}
        env['RL_FV'] = os.path.abspath(self.fv_dir_override or self._fv_dir(ws))
        env['PYTHONPATH'] = wsra + os.pathsep + self._vendor_path()
        env['RL_REPO'] = ws
        env['RL_CONFIG_MODE'] = 'gate'
        env['PYTHONHASHSEED'] = '0'
        for v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
            env[v] = '1'
        return env

    def _assert_config_policy(self):
        """ITEM 2: refuse an unknown or conflicting inherited RL_*/PAR_* valuation flag. The board
        policy is the release config manifest (data/model_config.json); an inherited model flag that
        is not in the manifest, or diverges from it, HALTS before any staging. Infrastructure/path
        vars (RL_REPO/RL_FV/... + the updater's own RL_VENDOR/RL_SEASON_ROUNDS) are allowed. Returns
        the canonical config hash (stamped into the transaction evidence)."""
        try:
            import config_manifest as CM
        except ImportError:
            sys.path.insert(0, self.repo_root)
            import config_manifest as CM
        man = CM.load(self.repo_root)
        cvars = man['vars']
        allow = set(CM.INFRA_ALLOW) | {'RL_VENDOR', 'RL_SEASON_ROUNDS', 'RL_REPO', 'RL_FV',
                                       'RL_APP_DATA', 'RL_Q97M_PKL', 'RL_V0SURF_PKL', 'RL_VENV',
                                       'RL_CONFIG_MODE'}
        conflicts = []
        for k, v in os.environ.items():
            if not (k.startswith('RL_') or k.startswith('PAR_')) or k in allow:
                continue
            if k not in cvars:
                conflicts.append("UNKNOWN inherited valuation flag %s=%r (not in the release config "
                                 "manifest data/model_config.json)" % (k, v))
            elif v != cvars[k]:
                conflicts.append("CONFLICTING inherited valuation flag %s=%r != manifest %r" % (k, v, cvars[k]))
        if conflicts:
            raise ConfigPolicyError(
                "the board build must use the accepted release policy, not inherited shell flags:\n  - "
                + "\n  - ".join(conflicts) + "\n  Unset the flag(s) above (dev-shell experimentation runs "
                "outside the weekly updater), or amend the manifest at a bake.")
        return CM.canonical_hash(cvars)

    def _assert_fv_provenance(self, ws, env):
        """ITEM 1: FAIL-CLOSED forward-valuation provenance. Assert the distribution_pricing the engine
        will load (resolved ENTIRELY via RL_FV — dist_redesign loads it from its own dir, and there is
        no plain `import distribution_pricing` anywhere) is INSIDE the staged repo AND byte-identical to
        the staged source. Halt (FVProvenanceError) before board generation on any mismatch. Returns the
        provenance evidence recorded in the transaction manifest + validation record."""
        ws_real = os.path.realpath(ws)
        rl_fv = env.get('RL_FV')
        if not rl_fv:
            raise FVProvenanceError("RL_FV is not bound for the staged build (would inherit an ambient "
                                    "forward_valuation) — refusing to generate a board")
        rl_fv_real = os.path.realpath(rl_fv)
        loaded = os.path.realpath(os.path.join(rl_fv_real, 'distribution_pricing.py'))
        staged_src = os.path.realpath(os.path.join(self._fv_dir(ws), 'distribution_pricing.py'))
        inside = (os.path.commonpath([loaded, ws_real]) == ws_real)
        if not inside:
            raise FVProvenanceError(
                "forward-valuation module the build would load is OUTSIDE the staged repo:\n"
                "    RL_FV -> %s\n    distribution_pricing -> %s\n    staged repo -> %s\n"
                "An ambient/workspace forward_valuation (e.g. a stale 21d530bf on the RL_FV default) must "
                "never produce, pin or commit a board. HALT before generation." % (rl_fv_real, loaded, ws_real))
        if not os.path.exists(loaded):
            raise FVProvenanceError("distribution_pricing.py absent under RL_FV %s" % rl_fv_real)
        md5_loaded = _md5_file_full(loaded)
        md5_staged = _md5_file_full(staged_src)
        if md5_loaded != md5_staged:
            raise FVProvenanceError(
                "distribution_pricing the build would load (%s, md5 %s) is NOT byte-identical to the "
                "staged source (%s, md5 %s) — refusing to generate a board from a mismatched valuation "
                "module." % (loaded, md5_loaded[:8], staged_src, md5_staged[:8]))
        return {'rl_fv': rl_fv_real, 'distribution_pricing_file': loaded,
                'distribution_pricing_md5': md5_loaded, 'inside_staged_repo': True}

    def _regen_board_strict(self, ws):
        """Regenerate the board from the STAGED store under the strict env, with FV provenance asserted
        BEFORE generation. Publishes the board + a coherent sidecar. Returns (board_md5, fv_evidence)."""
        wsra = os.path.join(ws, 'engine', 'rl_after')
        board_path = os.path.join(wsra, 'rl_app_data.json')
        publish = os.path.join(ws, 'data', 'rl_build', 'rl_app_data.json')
        env = self._strict_regen_env(ws)
        fv_ev = self._assert_fv_provenance(ws, env)     # HALT before any generation on a bad FV module
        for p in (board_path, board_path + '.srcmd5'):
            if os.path.exists(p):
                try:
                    os.chmod(p, stat.S_IWUSR | stat.S_IRUSR)
                except OSError:
                    pass
        r = subprocess.run([sys.executable, 'rl_export.py'], cwd=wsra, env=env,
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(board_path):
            raise StagedValidationError("staged board regen FAILED rc=%s (strict env; RL_FV=%s)\n"
                                        "STDERR tail:\n%s" % (r.returncode, env['RL_FV'],
                                                              (r.stderr or '')[-1800:]))
        # confirm the accepted config policy actually engaged (RL_CONFIG_MODE=gate loaded the manifest)
        fv_ev['config_mode_gate_loaded'] = ('config manifest (gate mode) LOADED' in (r.stdout or ''))
        os.makedirs(os.path.dirname(publish), exist_ok=True)
        if os.path.exists(publish):
            try:
                os.chmod(publish, stat.S_IWUSR | stat.S_IRUSR)
            except OSError:
                pass
        shutil.copyfile(board_path, publish)
        self._freshen_published_sidecar(ws)
        return _md5_file_full(publish), fv_ev

    # -- STAGED VALIDATION (every gate runs against the workspace = staged; nothing live touched) --
    def _validate_staged(self, ws, live_store_rows, allowed_keys, triples, preview,
                         staged_store_md5, staged_board_md5, snapshot):
        wsra = os.path.join(ws, 'engine', 'rl_after')
        staged_store = os.path.join(wsra, 'rl_model_data.json')
        staged_board = os.path.join(ws, 'data', 'rl_build', 'rl_app_data.json')
        staged_side = staged_board + '.srcmd5'
        staged_manifest = os.path.join(ws, 'data', 'expected_boot.json')
        staged_ledger = os.path.join(wsra, 'ingestion', 'applied_rounds_ledger.json')
        fails = []

        # (i) staged store parses
        try:
            with open(staged_store) as f:
                staged_rows = json.load(f)
        except (OSError, ValueError) as e:
            raise StagedValidationError("staged store does not parse: %s" % e)

        # (ii) ONLY permitted scoring entries changed (fed players' season entry only; nothing else)
        viol = self._diff_permitted(live_store_rows, staged_rows, allowed_keys,
                                    int(snapshot['season_year']))
        if viol:
            fails.append("unpermitted store change(s): %s" % viol[:5])

        # (iii) board generation succeeded + parses + has an active list
        try:
            with open(staged_board) as f:
                board = json.load(f)
            active = board['active'] if isinstance(board, dict) else board
            assert active, "empty active list"
        except (OSError, ValueError, KeyError, AssertionError) as e:
            raise StagedValidationError("staged board did not generate/parse: %s" % e)

        # (iv) board source-stamp == staged store
        try:
            with open(staged_side) as f:
                side = json.load(f)
        except (OSError, ValueError) as e:
            raise StagedValidationError("staged board sidecar missing/unparseable: %s" % e)
        if side.get('source_md5') != staged_store_md5:
            fails.append("board source-stamp %s != staged store %s"
                         % ((side.get('source_md5') or '')[:8], staged_store_md5[:8]))
        if _md5_file_full(staged_board) != staged_board_md5:
            fails.append("board md5 drifted between regen and validate")

        # (v) boot pins == staged store + board
        try:
            with open(staged_manifest) as f:
                pins = json.load(f)
        except (OSError, ValueError) as e:
            raise StagedValidationError("staged boot manifest unparseable: %s" % e)
        if not staged_store_md5.startswith(pins.get('store', '')) and pins.get('store') != staged_store_md5:
            fails.append("boot store pin %s != staged store %s"
                         % ((pins.get('store') or '')[:8], staged_store_md5[:8]))
        if pins.get('board') != staged_board_md5 and not staged_board_md5.startswith(pins.get('board', 'x')):
            fails.append("boot board pin %s != staged board %s"
                         % ((pins.get('board') or '')[:8], staged_board_md5[:8]))

        # (vi) ledger == the snapshot triples (all present)
        try:
            wsl = load_ledger(staged_ledger)
        except (OSError, ValueError) as e:
            raise StagedValidationError("staged ledger unparseable: %s" % e)
        missing = triples - set(wsl.get('applied', []))
        if missing:
            fails.append("ledger missing %d snapshot triple(s)" % len(missing))

        # (vi-b) VALUE + RANK history: parses, records THIS round for every active board player, and
        #        PRESERVES every earlier round byte-for-byte vs the live histories (append-only). The
        #        recorded value/rank equal the staged board's own value + descending-value rank.
        hist_fail = self._validate_history(ws, active, int(snapshot['round']), int(snapshot['season_year']))
        fails.extend(hist_fail)

        # (vii) board player universe unchanged vs the pre-apply board (a round moves values, not keys)
        uni_fail = self._player_universe_ok(ws, active)
        if uni_fail:
            fails.append(uni_fail)

        # (vii-b) FAIL-CLOSED FV provenance (re-assert at validation): the distribution_pricing the
        #         build resolved is inside the staged repo AND byte-identical to the staged source, and
        #         the staged FV equals the live repo FV (so the staged workspace was not shadowed).
        try:
            self._fv_evidence = self._assert_fv_provenance(ws, self._strict_regen_env(ws))
        except FVProvenanceError as e:
            raise StagedValidationError("forward-valuation provenance failed at validation: %s" % e)
        live_fv_dp = os.path.join(self.repo_root, 'engine', 'forward_valuation', 'distribution_pricing.py')
        if os.path.exists(live_fv_dp):
            live_md5 = _md5_file_full(live_fv_dp)
            if live_md5 != self._fv_evidence['distribution_pricing_md5']:
                fails.append("staged forward_valuation distribution_pricing %s != live repo FV %s"
                             % (self._fv_evidence['distribution_pricing_md5'][:8], live_md5[:8]))

        if fails:
            raise StagedValidationError("STAGED validation failed:\n  - " + "\n  - ".join(fails))

        # (viii) Guard 5 GREEN against the STAGED set (the real boot validation, RL_REPO=ws)
        rc, out = self._run_guard5(ws)
        if rc != 0:
            raise StagedValidationError("Guard 5 (boot validation) FAILED against the staged set:\n"
                                        + out[-1500:])
        return True

    def _diff_permitted(self, live_rows, staged_rows, allowed_keys, season):
        """Return a list of unpermitted differences between live and staged stores. Permitted: for a
        key in allowed_keys, its season `scoring` entry (avg/games) may change (or be added). Nothing
        else — no other row, no other field, no other season entry, no added/removed rows."""
        live_by = {r.get('key'): r for r in live_rows if r.get('key')}
        stg_by = {r.get('key'): r for r in staged_rows if r.get('key')}
        viol = []
        if set(live_by) != set(stg_by):
            added = set(stg_by) - set(live_by)
            removed = set(live_by) - set(stg_by)
            if added:
                viol.append("rows ADDED: %s" % sorted(added)[:5])
            if removed:
                viol.append("rows REMOVED: %s" % sorted(removed)[:5])
        for key in set(live_by) & set(stg_by):
            lr, sr = live_by[key], stg_by[key]
            # compare everything except `scoring`
            lr_nos = {k: v for k, v in lr.items() if k != 'scoring'}
            sr_nos = {k: v for k, v in sr.items() if k != 'scoring'}
            if lr_nos != sr_nos:
                viol.append("row %s non-scoring field changed" % key)
            l_sc = {s.get('year'): s for s in (lr.get('scoring') or [])}
            s_sc = {s.get('year'): s for s in (sr.get('scoring') or [])}
            changed_years = set()
            for y in set(l_sc) | set(s_sc):
                if l_sc.get(y) != s_sc.get(y):
                    changed_years.add(y)
            if changed_years - {season}:
                viol.append("row %s changed scoring for non-target season(s) %s"
                            % (key, sorted(changed_years - {season})))
            if changed_years and key not in allowed_keys:
                viol.append("row %s changed but is NOT in the snapshot's fed set" % key)
        return viol

    def _player_universe_ok(self, ws, staged_active):
        """The staged board's active player set must equal the pre-apply board's — a weekly round
        moves values, never the roster. Compares against the originals backup if present, else the
        live board."""
        live_board = self._live('board')
        try:
            with open(live_board) as f:
                lb = json.load(f)
            la = lb['active'] if isinstance(lb, dict) else lb
        except (OSError, ValueError, KeyError):
            return None    # no pre-apply board to compare — skip (fresh repo)
        live_keys = {r.get('key') for r in la}
        stg_keys = {r.get('key') for r in staged_active}
        if live_keys != stg_keys:
            added = sorted(stg_keys - live_keys)[:5]
            removed = sorted(live_keys - stg_keys)[:5]
            return "board player universe changed (added %s / removed %s)" % (added, removed)
        return None

    def _validate_history(self, ws, staged_active, round_n, season):
        """Gate the three staged histories (value / overall-rank / positional-rank). Returns a list of
        failures (empty == OK). For each history:
          - it parses;
          - THIS round is recorded for EVERY active player in the staged board;
          - the recorded metric equals the staged board's own metric (value / descending-`v` overall
            rank / rank within the position group) — the history agrees with the board it came from;
          - every (player, round) present in the LIVE history is preserved byte-equal (append-only)."""
        fails = []
        truth = RH.board_metrics({'active': staged_active})    # v, rank, pos_rank per active key
        rk = str(round_n)
        for name, target, field in (('value', 'value_history', 'v'), ('rank', 'rank_history', 'rank'),
                                    ('pos_rank', 'pos_rank_history', 'pos_rank')):
            path = self._ws_target_path(ws, target)
            try:
                with open(path) as f:
                    hist = json.load(f)
            except (OSError, ValueError) as e:
                fails.append("staged %s history unparseable: %s" % (name, e))
                continue
            players = hist.get('players', {})
            missing = [k for k in truth if rk not in (players.get(k, {}).get('by_round', {}))]
            if missing:
                fails.append("%s history missing round %d for %d active player(s), e.g. %s"
                             % (name, round_n, len(missing), sorted(missing)[:3]))
            bad = [k for k in truth if k not in missing and players[k]['by_round'][rk] != truth[k][field]]
            if bad:
                fails.append("%s history round %d disagrees with the board for %d player(s), e.g. %s"
                             % (name, round_n, len(bad), sorted(bad)[:3]))
            live = self._live_history(target)
            for k, lentry in (live.get('players', {}) if live else {}).items():
                for r, val in (lentry.get('by_round') or {}).items():
                    if players.get(k, {}).get('by_round', {}).get(r) != val:
                        fails.append("%s history OVERWROTE round %s for %s — append-only" % (name, r, k))
                        break
        return fails

    def _live_history(self, name):
        p = os.path.join(self.repo_root, dict(TARGETS)[name])
        if not os.path.exists(p):
            return None
        try:
            with open(p) as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    # ===========================================================================================
    # POST-COMMIT UI EXTRACTION (TIER 3, read-only; triggered ONLY after a fully committed board)
    # ===========================================================================================
    def refresh_ui(self):
        """Regenerate the Matchday UI view bundles from the COMMITTED board. Runs the checkout's own
        ui/tools/extract_board_view.py (never an ambient copy) against repo_root; the extractor
        ring-fences the board md5 against the boot board pin (which the apply re-stamped), so it can
        only produce coherent bundles from a fully committed board and fails closed otherwise. This is
        a read-only TIER-3 step, deliberately OUTSIDE the store transaction (UI bundles are re-derivable
        and never gate a store write). Skips gracefully if ui/ is absent. Returns an evidence dict."""
        extractor = os.path.join(self.repo_root, 'ui', 'tools', 'extract_board_view.py')
        if not os.path.exists(extractor):
            return {'ran': False, 'reason': 'no ui/tools/extract_board_view.py under repo root'}
        env = dict(os.environ)
        env['RL_REPO'] = self.repo_root
        env.setdefault('PYTHONHASHSEED', '0')
        env.setdefault('RL_VENDOR', os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
        env['PYTHONPATH'] = (os.path.join(self.repo_root, 'engine', 'rl_after') + os.pathsep
                             + env.get('RL_VENDOR', '') + os.pathsep + env.get('PYTHONPATH', ''))
        r = subprocess.run([sys.executable, extractor], cwd=self.repo_root, env=env,
                           capture_output=True, text=True)
        working = os.path.join(self.repo_root, 'ui', 'data', 'board_view_working.js')
        public = os.path.join(self.repo_root, 'ui', 'data', 'board_view_public.js')
        ok = (r.returncode == 0 and os.path.exists(working) and os.path.exists(public))
        ev = {'ran': True, 'rc': r.returncode, 'ok': ok,
              'working_bundle': working if os.path.exists(working) else None,
              'public_bundle': public if os.path.exists(public) else None,
              'stderr_tail': (r.stderr or '')[-500:] if not ok else None}
        if ok:
            ev.update(self._ui_coherence(working, public))
        return ev

    @staticmethod
    def _parse_bundle(path):
        """Parse a `window.__X__ = {...};` bundle back to a dict (the extractor's own emit format)."""
        with open(path) as f:
            text = f.read()
        i = text.index('{')
        j = text.rindex('}')
        return json.loads(text[i:j + 1])

    def _ui_coherence(self, working, public):
        """Coherence of the two emitted bundles vs the committed board: the working bundle's board
        stamp equals the committed board id, the two bundles cover the same players, and the PUBLIC
        bundle carries NO identity leak (no key/id/md5/stamp.srcmd5) — the two-tier UI law."""
        w = self._parse_bundle(working)
        p = self._parse_bundle(public)
        board_id = _md5_file_full(self._live('board'))
        wstamp = (w.get('stamp') or {})
        srcmd5 = wstamp.get('srcmd5') or ''
        pub_leak = any(k in (row or {}) for row in p.get('players', []) for k in ('key', 'stable_player_id'))
        pub_stamp_leak = any(k in (p.get('stamp') or {}) for k in ('srcmd5', 'store', 'register', 'guard5'))
        return {
            'ui_board_stamp': srcmd5[:12], 'committed_board_id': board_id[:12],
            'ui_board_stamp_matches_committed': srcmd5 == board_id,
            'working_players': len(w.get('players', [])), 'public_players': len(p.get('players', [])),
            'players_match': len(w.get('players', [])) == len(p.get('players', [])),
            'public_leak_free': not pub_leak and not pub_stamp_leak,
        }

    def _run_guard5(self, ws):
        wsra = os.path.join(ws, 'engine', 'rl_after')
        # SANITIZE the boot-validation environment exactly as the staged board build does
        # (_strict_regen_env): drop every ambient RL_*/PAR_* redirect and bind RL_FV to the STAGED
        # forward_valuation. df5066a's Guard 5 asserts the forward-valuation LOADED PATH (the exact dir
        # the engine would import via RL_FV) against the pinned `fv` identity; an ambient/adversarial
        # inherited RL_FV must NOT make Guard 5 validate — or reject — against a non-staged tree. Guard 5
        # here validates the SAME forward_valuation the board was just built from.
        vendor = os.environ.get('RL_VENDOR', '/home/claude/rl_vendor')
        env = {k: v for k, v in os.environ.items() if not (k.startswith('RL_') or k.startswith('PAR_'))}
        env['RL_REPO'] = ws
        env['RL_VENDOR'] = vendor
        env['RL_FV'] = os.path.abspath(self.fv_dir_override or self._fv_dir(ws))
        env['PYTHONPATH'] = wsra + os.pathsep + vendor
        env['PYTHONHASHSEED'] = '0'
        r = subprocess.run(
            [sys.executable, os.path.join(ws, 'boot_guard.py'), 'weekly_updater_staged',
             os.path.join(wsra, 'rl_model_data.json'), os.path.join(wsra, '_merged_recover.py'),
             os.path.join(ws, 'data', 'cm_400.pkl'), os.path.join(wsra, 'LTI_REGISTER.md')],
            env=env, capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr)

    # -- staged/originals payload management ----------------------------------------------------
    def _ws_target_path(self, ws, name):
        wsra = os.path.join(ws, 'engine', 'rl_after')
        return {
            'store':   os.path.join(wsra, 'rl_model_data.json'),
            'board':   os.path.join(ws, 'data', 'rl_build', 'rl_app_data.json'),
            'sidecar': os.path.join(ws, 'data', 'rl_build', 'rl_app_data.json.srcmd5'),
            'manifest': os.path.join(ws, 'data', 'expected_boot.json'),
            'ledger':  os.path.join(wsra, 'ingestion', 'applied_rounds_ledger.json'),
            'value_history': os.path.join(wsra, 'ingestion', 'value_history.json'),
            'rank_history':  os.path.join(wsra, 'ingestion', 'rank_history.json'),
            'pos_rank_history': os.path.join(wsra, 'ingestion', 'pos_rank_history.json'),
        }[name]

    # -- persistent value + overall-rank + positional-rank history (a transaction target) ----------
    _HISTORY_TARGETS = (('value', 'value_history', RH.KIND_VALUE),
                        ('rank', 'rank_history', RH.KIND_RANK),
                        ('pos_rank', 'pos_rank_history', RH.KIND_POS_RANK))

    def _stage_history(self, ws, snapshot):
        """Fold the staged board's per-player value + overall-rank + positional-rank into the three
        persistent histories, in the workspace. Seeds the previous round (round-1) from the PRE-APPLY
        live board on the first apply (the round-14 -> round-15 transition), then appends this round;
        never overwrites a recorded round. Returns an evidence dict."""
        season = int(snapshot['season_year'])
        rnd = int(snapshot['round'])
        live_board_path = self._live('board')
        prev_board = None
        if os.path.exists(live_board_path):
            with open(live_board_path) as f:
                prev_board = json.load(f)
        with open(self._ws_target_path(ws, 'board')) as f:
            new_board = json.load(f)
        hists, paths = {}, {}
        for key, target, kind in self._HISTORY_TARGETS:
            paths[key] = self._ws_target_path(ws, target)
            hists[key] = RH.load_history(paths[key], kind, season)
        rounds_before = RH.rounds_recorded(hists['value'])
        hists = RH.update_histories(hists, season=season, round_n=rnd,
                                    prev_board=prev_board, new_board=new_board)
        md5s = {}
        for key, target, _kind in self._HISTORY_TARGETS:
            RH.save_history(paths[key], hists[key])
            md5s[target + '_md5'] = _md5_file_full(paths[key])
        ev = {'season': season, 'round': rnd, 'prev_round': rnd - 1,
              'rounds_before': rounds_before, 'rounds_after': RH.rounds_recorded(hists['value']),
              'players': len(hists['value'].get('players', {}))}
        ev.update(md5s)
        return ev

    def _collect_staged(self, ws, txn_dir):
        """Copy the validated workspace outputs into txn/staged (same FS as live) and md5-verify each
        copy is byte-identical to the validated workspace output — the staged bytes ARE what was
        validated. Returns {name: staged_path}."""
        staged = {}
        for name, _rel in TARGETS:
            srcp = self._ws_target_path(ws, name)
            if not os.path.exists(srcp):
                continue
            dstp = os.path.join(txn_dir, 'staged', name)
            shutil.copyfile(srcp, dstp)
            if _md5_file_full(dstp) != _md5_file_full(srcp):
                raise StagedValidationError("staged copy of %s does not match the validated output" % name)
            staged[name] = dstp
        self._journal(txn_dir, 'STAGED_COLLECTED', targets=sorted(staged))
        return staged

    def _backup_originals(self, txn_dir):
        orig = os.path.join(txn_dir, 'originals')
        for name, rel in TARGETS:
            live = os.path.join(self.repo_root, rel)
            if os.path.exists(live):
                shutil.copyfile(live, os.path.join(orig, name))

    def _prune_committed_payload(self, txn_dir):
        """On success keep manifest.json + journal.jsonl as the permanent record; drop the heavy
        staged/originals copies to save space. (On FAILURE nothing is pruned — evidence is kept.)"""
        for sub in ('staged', 'originals'):
            shutil.rmtree(os.path.join(txn_dir, sub), ignore_errors=True)

    def _mk_txn_id(self, snapshot, generated_at):
        seed = "%s|%s|%s|%s" % (snapshot.get('round'), snapshot.get('season_year'),
                                snapshot.get('content_hash'), generated_at or '')
        return 'txn_' + hashlib.md5(seed.encode()).hexdigest()[:12]
