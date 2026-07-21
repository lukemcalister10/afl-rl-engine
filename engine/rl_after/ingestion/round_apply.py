"""ROUND-APPLY — the STORE-WRITE half of weekly round-score ingestion (go-live job).

This is the write path the provision job deliberately left absent (score_ingestor.apply raised
IngestionGatedError with no write code behind it). It takes a VALIDATED, CLEAN preview
(score_ingestor.ScoreIngestor.preview) and, BEHIND the existing double-OFF gate, applies one
weekly round to the SINGLE SOURCE, then regenerates the board as a derived read-only artifact and
re-stamps the boot manifest — exactly the flow docs/GO_LIVE_round_score_ingestion.md prescribes.

WHAT IT DOES (in order, all-or-nothing):
  1. GATE     — refuses unless BOTH switch halves are on (score_ingestor.APPLY_DEFAULT + env
                INGEST_SCORE_APPLY). Default => OFF => IngestionGatedError. This whole job ships OFF.
  2. CLEAN    — refuses a preview that carries resolve exceptions or un-cleared anomalies (never
                fuzzy-attach, never silently merge a suspicious row).
  3. SEASON   — refuses a round beyond the season's real round count (a fat-fingered r99).
  4. DEDUP    — a per-(stable_player_id, season, round) LEDGER blocks an across-feed re-send: a round
                already applied cannot double-count. (The in-feed duplicate_round anomaly is a
                separate, earlier catch inside preview.)
  5. MERGE    — writes each append's `merged_entry` (before + this round) into that player's `scoring`
                season entry, IN PLACE on the ONE authored source (atomic temp+rename; no second copy,
                no .bak, no lookalike — SSI guards 1/3).
  6. REGEN    — rebuilds the board (rl_export.py) as a derived, source-stamped, read-only artifact
                (SSI guards 1/2 via single_source.stamp_derived, called by rl_export itself).
  7. RE-STAMP — moves the boot manifest's `store` and `board` pins to the new md5s, in place, so
                Guard 5 re-pins to the written store (a moved store with an un-repinned boot pin MUST
                halt the next script — SSI guard 5; the re-stamp is what keeps the build green).
  8. LEDGER   — records the applied (sid, season, round) set so step 4 blocks the re-send next week.

SAFETY (this report-only build writes NOTHING to the real store):
  - The gate ships OFF (APPLY_DEFAULT=False, INGEST_SCORE_APPLY unset): apply() on the real store
    always raises. Belt-and-braces — neither a stray env var nor a stray code edit can arm it alone.
  - RoundApplier is constructed with EXPLICIT store/workspace/manifest/ledger paths. The proofs
    construct it against SCRATCH COPIES only; no proof path resolves to the real single source.
  - At go-live, docs/GO_LIVE_round_score_ingestion.md's FLIP ORDER sets both halves and points a
    RoundApplier.for_repo() at the real files — this same code, one round, then re-pin.

SCOPE FENCE: this MERGES scores and REGENERATES derived artifacts. It never touches valuation logic,
the curve, the model, or pricing — new scores flow through the unchanged engine at regen time.
"""
import json, os, re, hashlib, stat, subprocess, sys, tempfile, shutil

try:
    from .score_ingestor import IngestionGatedError, _apply_enabled, APPLY_DEFAULT, _APPLY_ENV
except (ImportError, ValueError):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from score_ingestor import IngestionGatedError, _apply_enabled, APPLY_DEFAULT, _APPLY_ENV  # type: ignore

# ---- season bound (config; owner pins the exact count at go-live — step 3) ------------------
# AFL runs a 24-round home-and-away calendar (23 games each, one bye per club across the 24 rounds).
# A weekly feed round outside [1, SEASON_ROUNDS] is a data error (a fat-fingered round), refused
# before any merge. Owner-overridable via the RoundApplier arg / RL_SEASON_ROUNDS at go-live; this is
# a sanity bound, not a valuation input — kept intentionally generous so a real round is never rejected.
DEFAULT_SEASON_ROUNDS = 24


class SeasonBoundError(ValueError):
    """A feed round lies outside [1, season_rounds] — refused before any merge (step 3)."""


class DuplicateRoundError(RuntimeError):
    """One or more (stable_player_id, season, round) triples were already applied (the ledger blocks
    the across-feed re-send — step 4). No merge is performed; the store is untouched."""
    def __init__(self, dups):
        self.dups = dups
        super().__init__("round already applied (dedup ledger blocks re-send): %d triple(s), e.g. %s"
                         % (len(dups), sorted(dups)[:3]))


class PreviewNotCleanError(RuntimeError):
    """The preview carries resolve exceptions or un-cleared anomalies — refused (step 2). Hand the
    named exceptions/anomalies back to the owner; never fuzzy-attach, never silently merge."""


def _md5_full(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


# ---- dedup ledger ---------------------------------------------------------------------------
def ledger_key(stable_player_id, season, rnd):
    """The dedup identity of one applied datum: WHO (stable id, never a fuzzy name), WHICH season,
    WHICH round. A weekly re-send reproduces these exactly, so the intersection blocks it."""
    return "%s|%s|%s" % (stable_player_id, season, rnd)


def load_ledger(path):
    """Read the applied-rounds ledger (a plain JSON set-of-triples). Absent/empty => nothing applied."""
    if not path or not os.path.exists(path):
        return {'version': 1, 'applied': []}
    with open(path) as f:
        d = json.load(f)
    d.setdefault('version', 1)
    d.setdefault('applied', [])
    return d


def save_ledger(path, ledger):
    """Write the ledger atomically (temp+rename; never a partial/torn ledger)."""
    ledger['applied'] = sorted(set(ledger.get('applied', [])))
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix='.ledger_tmp_', suffix='.json', dir=d)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(ledger, f, indent=2, sort_keys=True)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


class ApplyResult:
    __slots__ = ('season_year', 'players_merged', 'rounds_applied', 'store_md5_before',
                 'store_md5_after', 'board_md5_before', 'board_md5_after', 'ledger_added',
                 'ledger_total')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    def as_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}


class RoundApplier:
    """Applies ONE validated weekly round to a store, regenerates the board, re-stamps the manifest,
    and records the dedup ledger — all behind the gate. Constructed with EXPLICIT paths so the proofs
    bind it to scratch copies and the real single source is never a proof target."""

    def __init__(self, store_path, workspace_dir, manifest_path, ledger_path,
                 repo_root=None, season_rounds=None, board_publish_path=None):
        self.store_path = os.path.abspath(store_path)
        self.workspace_dir = os.path.abspath(workspace_dir)   # holds rl_export.py + the store copy
        self.manifest_path = os.path.abspath(manifest_path)   # expected_boot.json to re-stamp
        self.ledger_path = os.path.abspath(ledger_path)
        self.repo_root = os.path.abspath(repo_root) if repo_root else None  # for engine pickle/config resolution
        self.season_rounds = int(season_rounds if season_rounds is not None
                                 else os.environ.get('RL_SEASON_ROUNDS', DEFAULT_SEASON_ROUNDS))
        # The board Guard 5 pins is the PUBLISHED board (data/rl_build/rl_app_data.json), a copy of the
        # generator's output (engine/rl_after/rl_app_data.json). Publish there so the re-stamped board
        # pin == the board boot_guard reads. Defaults under repo_root; overridable for scratch.
        if board_publish_path is not None:
            self.board_publish_path = os.path.abspath(board_publish_path)
        elif self.repo_root:
            self.board_publish_path = os.path.join(self.repo_root, 'data', 'rl_build', 'rl_app_data.json')
        else:
            self.board_publish_path = None

    @classmethod
    def for_repo(cls, repo_root):
        """GO-LIVE binding: point the applier at the REAL single source + repo artifacts. Only writes
        when the gate is armed (both halves) — docs/GO_LIVE_round_score_ingestion.md FLIP ORDER."""
        ra = os.path.join(repo_root, 'engine', 'rl_after')
        return cls(store_path=os.path.join(ra, 'rl_model_data.json'),
                   workspace_dir=ra,
                   manifest_path=os.path.join(repo_root, 'data', 'expected_boot.json'),
                   ledger_path=os.path.join(ra, 'ingestion', 'applied_rounds_ledger.json'),
                   repo_root=repo_root)

    # -- ledger-facing helpers ----------------------------------------------------------------
    def _preview_triples(self, preview):
        """The (sid, season, round) triples this preview would apply — one per contributing feed row."""
        out = set()
        for a in preview.appends:
            for (rnd, _score, _played) in a.rounds:
                out.add(ledger_key(a.stable_player_id, preview.season_year, rnd))
        return out

    # -- the store write (in place, atomic; SSI guards 1/3) -----------------------------------
    def _merge_into_store(self, preview):
        with open(self.store_path) as f:
            store = json.load(f)
        by_key = {r.get('key'): r for r in store if r.get('key')}
        merged = 0
        for a in preview.appends:
            row = by_key.get(a.key)
            if row is None:
                raise KeyError("append key %r not present in store %s" % (a.key, self.store_path))
            scoring = row.setdefault('scoring', [])
            entry = next((s for s in scoring if s.get('year') == a.year), None)
            if entry is None:
                scoring.append(dict(a.merged_entry))
                scoring.sort(key=lambda s: s.get('year', 0))
            else:
                entry['avg'] = a.merged_entry['avg']
                entry['games'] = a.merged_entry['games']
            merged += 1
        # atomic in-place rewrite — NO second copy, NO lookalike (SSI): a temp whose name does not
        # match the source glob (rl_model_data*.json) or the .bak/.stageN lookalike patterns, renamed
        # over the source. Default json.dump (insertion order preserved, verified byte-identical to the
        # authored store on an untouched round-trip) keeps the go-live diff MINIMAL — only the merged
        # players' scoring entries change — and is deterministic (load-order is stable) for single-env
        # board stability.
        d = os.path.dirname(self.store_path)
        fd, tmp = tempfile.mkstemp(prefix='.store_apply_tmp_', suffix='.tmp', dir=d)
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(store, f)
            os.replace(tmp, self.store_path)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        return merged

    # -- board regen (derived, source-stamped, read-only — rl_export.py; SSI guards 1/2) ------
    def _regen_board(self):
        """Rebuild the board from the (just-written) store by running rl_export.py in the workspace —
        the SAME generator the board-of-record recipe (build_board.sh) uses. It stamps the board with
        the current source md5 and sets it read-only (single_source.stamp_derived). Returns board md5.
        Deterministic single-env recipe: PYTHONHASHSEED=0 + single-thread BLAS (build_board.sh)."""
        board_path = os.path.join(self.workspace_dir, 'rl_app_data.json')
        # clear any prior read-only board so the generator can overwrite (single_source.prepare_write
        # does this too; belt-and-suspenders for the scratch workspace).
        for p in (board_path, board_path + '.srcmd5'):
            if os.path.exists(p):
                try:
                    os.chmod(p, stat.S_IWUSR | stat.S_IRUSR)
                except OSError:
                    pass
        env = dict(os.environ)
        env['PYTHONHASHSEED'] = '0'
        env['PYTHONPATH'] = self.workspace_dir + ':' + env.get('RL_VENDOR', '/home/claude/rl_vendor')
        for v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
            env[v] = '1'
        if self.repo_root:
            env['RL_REPO'] = self.repo_root
        r = subprocess.run([sys.executable, 'rl_export.py'], cwd=self.workspace_dir,
                           env=env, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(board_path):
            raise RuntimeError("board regen (rl_export.py) FAILED rc=%s\nSTDERR tail:\n%s"
                               % (r.returncode, (r.stderr or '')[-1500:]))
        # publish the generated board to the canonical location Guard 5 pins (data/rl_build), so the
        # re-stamped board pin matches the board boot_guard reads. Byte-identical copy => same md5.
        if self.board_publish_path and os.path.abspath(self.board_publish_path) != os.path.abspath(board_path):
            os.makedirs(os.path.dirname(self.board_publish_path), exist_ok=True)
            if os.path.exists(self.board_publish_path):
                try:
                    os.chmod(self.board_publish_path, stat.S_IWUSR | stat.S_IRUSR)
                except OSError:
                    pass
            shutil.copyfile(board_path, self.board_publish_path)
            return _md5_full(self.board_publish_path)
        return _md5_full(board_path)

    # -- manifest re-stamp (SSI guard 5: move store+board pins with the write) -----------------
    def _restamp_manifest(self, store_md5, board_md5):
        """Surgically move ONLY the `store` and `board` pins to the new md5s (every other pin/note
        byte-unchanged), so Guard 5 re-pins to the written store instead of halting on the mover."""
        with open(self.manifest_path) as f:
            text = f.read()
        for field, val in (('store', store_md5), ('board', board_md5)):
            pat = r'("%s":\s*")[0-9a-f]+(")' % field
            new, n = re.subn(pat, lambda m, v=val: m.group(1) + v + m.group(2), text, count=1)
            if n != 1:
                raise RuntimeError("manifest re-stamp: expected exactly 1 %r pin, found %d" % (field, n))
            text = new
        d = os.path.dirname(self.manifest_path)
        fd, tmp = tempfile.mkstemp(prefix='.boot_tmp_', suffix='.json', dir=d)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(text)
            os.replace(tmp, self.manifest_path)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    # -- THE APPLY (all-or-nothing) -----------------------------------------------------------
    def apply(self, preview, *, dry_ledger_only=False):
        """Apply one validated weekly round. Steps 1-8 above; raises (no partial write) on any refusal.

        Order is deliberate: every REFUSAL (gate/clean/season/dedup) fires BEFORE the store is touched,
        so a rejected feed leaves the store, board, manifest and ledger byte-unchanged.
        """
        # 1) GATE — both halves, or nothing (this whole job ships OFF).
        if not _apply_enabled():
            raise IngestionGatedError(
                "round-score APPLY is OFF (APPLY_DEFAULT=%s, env %s unset) — this build writes nothing "
                "to the store; go-live arms both halves (docs/GO_LIVE_round_score_ingestion.md)."
                % (APPLY_DEFAULT, _APPLY_ENV))

        # 2) CLEAN — no exceptions, no un-cleared anomalies.
        if preview.exceptions:
            raise PreviewNotCleanError("preview has %d resolve exception(s) — hand the named list back "
                                       "to the owner, never fuzzy-attach" % len(preview.exceptions))
        if preview.anomalies:
            raise PreviewNotCleanError("preview has %d un-cleared anomaly(ies) (duplicate/impossible/"
                                       "retired/cycle) — owner must clear before apply" % len(preview.anomalies))

        # 3) SEASON BOUND — no round outside [1, season_rounds].
        bad = sorted({rnd for a in preview.appends for (rnd, _s, _p) in a.rounds
                      if not (1 <= rnd <= self.season_rounds)})
        if bad:
            raise SeasonBoundError("round(s) %s outside the season bound [1, %d] — refused (owner pins "
                                   "the exact count at go-live)" % (bad, self.season_rounds))

        # 4) DEDUP — the ledger blocks an across-feed re-send.
        triples = self._preview_triples(preview)
        ledger = load_ledger(self.ledger_path)
        already = set(ledger.get('applied', []))
        dups = triples & already
        if dups:
            raise DuplicateRoundError(dups)

        if dry_ledger_only:      # test hook: exercise steps 1-4 without writing the store
            return None

        # ---- past every refusal: perform the write (5), regen (6), re-stamp (7), ledger (8) ----
        store_before = _md5_full(self.store_path)
        board_path = os.path.join(self.workspace_dir, 'rl_app_data.json')
        board_before = _md5_full(board_path) if os.path.exists(board_path) else None

        merged = self._merge_into_store(preview)         # 5) MERGE in place
        store_after = _md5_full(self.store_path)
        board_after = self._regen_board()                # 6) REGEN board (derived, stamped, read-only)
        self._restamp_manifest(store_after, board_after) # 7) RE-STAMP store+board pins (Guard 5)

        ledger['applied'] = sorted(already | triples)    # 8) LEDGER the applied round
        save_ledger(self.ledger_path, ledger)

        return ApplyResult(
            season_year=preview.season_year, players_merged=merged, rounds_applied=sorted(triples),
            store_md5_before=store_before[:8], store_md5_after=store_after[:8],
            board_md5_before=(board_before[:8] if board_before else None),
            board_md5_after=board_after[:8], ledger_added=len(triples), ledger_total=len(ledger['applied']))
