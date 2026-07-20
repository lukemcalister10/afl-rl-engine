"""ROUND CATCH-UP — a controlled multi-round catch-up: R14 baseline -> R15 -> ... -> R19.

The owner supplies several consecutive weekly score files at once and wants to catch up without
approving each round separately — but with the SAME safety as the single-round updater. This module
gives ONE consolidated preflight + ONE approval, then applies every round as its OWN separate,
sequential, staged transaction against the running committed store. It never combines files into one
update: each round merges only its own listed scores and is committed completely before the next round
begins.

SAFETY (all inherited from staged_apply, per round)
  * gate OFF by default (both halves) — this build applies no real round; the proofs arm it in-process
    against a SCRATCH repo only;
  * every round is a staged STAGE -> VALIDATE -> ATOMIC SWAP transaction with rollback + crash recovery;
  * the dedup ledger blocks re-applying any already-committed round (restart-safe: a resumed catch-up
    skips committed rounds and continues from the next unapplied one);
  * a crash mid-commit leaves an incomplete transaction that the next run REFUSES until `recover`.

PARTICIPATION (owner ruling 2026-07-20 — FILE MEMBERSHIP defines participation)
  * a player LISTED in a round file PLAYED: their score is appended and one game added to the
    denominator (this is exactly score_ingestor's merge; a listed score of 0 is a legitimate played
    zero);
  * a player ABSENT from a file DID NOT PLAY: nothing is appended, no placeholder, no game, no
    carry-forward — and absence is NOT an unresolved-input condition;
  * participation is never inferred from fixtures, byes, injuries or row counts (different per-round
    listed counts are expected).

IDENTITY (owner ruling — resolve by STABLE identity, never display name / row order alone)
  * each listed name resolves to exactly one ACTIVE stable key, OR to an owner identity override
    (catchup_identity_overrides.json: the two Bailey Williams by (round, score); Callum Brown ->
    callum-brown-ire);
  * ANY unresolved name, ambiguous name, or duplicate stable-key assignment in a round HALTS the whole
    catch-up before the first write — never a silent drop, never the wrong row.
"""
import json
import os
import sys

try:
    from . import round_entry as RE
    from . import footywire_parser as FW
    from . import staged_apply as SA
    from . import round_movers as MV
    from .round_apply import ledger_key, load_ledger
except (ImportError, ValueError):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import round_entry as RE            # type: ignore
    import footywire_parser as FW       # type: ignore
    import staged_apply as SA           # type: ignore
    import round_movers as MV           # type: ignore
    from round_apply import ledger_key, load_ledger  # type: ignore

DEFAULT_SEASON = 2026
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OVERRIDES = os.path.join(_HERE, 'catchup_identity_overrides.json')


class CatchupError(RuntimeError):
    """A catch-up-level refusal (unresolved / ambiguous / duplicate identity, or an unclean preflight).
    Raised before any write — a refused catch-up leaves every round byte-unchanged."""


# ---- owner identity overrides --------------------------------------------------------------------
class IdentityOverrides:
    """Owner-authored display-name -> stable-key overrides. Applied BEFORE the name resolver; a covered
    name with no matching rule is UNRESOLVED (halt), never guessed."""

    def __init__(self, spec):
        self.season = spec.get('season', DEFAULT_SEASON)
        self._by_name = {o['name']: o for o in spec.get('overrides', [])}

    @classmethod
    def load(cls, path=DEFAULT_OVERRIDES):
        with open(path) as f:
            return cls(json.load(f))

    @property
    def names(self):
        return set(self._by_name)

    def resolve(self, round_n, name, score):
        """Return (stable_key or None, kind). kind: 'map_all' | 'by_round_score' | 'unmapped' |
        'not_overridden'."""
        o = self._by_name.get(name)
        if o is None:
            return None, 'not_overridden'
        if o['rule'] == 'map_all':
            return o['stable_key'], 'map_all'
        if o['rule'] == 'by_round_score':
            key = o.get('map', {}).get('%d|%d' % (int(round_n), int(round(score))))
            return (key, 'by_round_score') if key else (None, 'unmapped')
        return None, 'unmapped'


# ---- the catch-up --------------------------------------------------------------------------------
class RoundCatchup:
    def __init__(self, repo_root, files, *, overrides=None, season=DEFAULT_SEASON):
        """`files` is [(round_n, path)] in any order (sorted internally). `overrides` is an
        IdentityOverrides (defaults to the shipped owner override file)."""
        self.repo_root = os.path.abspath(repo_root)
        self.files = sorted(((int(r), p) for r, p in files), key=lambda rp: rp[0])
        self.overrides = overrides or IdentityOverrides.load()
        self.season = int(season)

    def _store_path(self):
        return os.path.join(self.repo_root, 'engine', 'rl_after', 'rl_model_data.json')

    def _ledger_path(self):
        return os.path.join(self.repo_root, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json')

    def _store_rows(self):
        with open(self._store_path()) as f:
            return json.load(f)

    # -- resolve one round's rows to stable identities (override-first) ---------------------------
    def _resolve_round(self, round_n, rows, resolver, by_key):
        """Return (resolved:[ResolvedRow], residue:[dict]). residue carries unresolved / unmapped-
        override lines. Duplicate detection is done by the caller across the resolved set."""
        resolved, residue = [], []
        for name, score in rows:
            okey, kind = self.overrides.resolve(round_n, name, score)
            if kind in ('map_all', 'by_round_score'):
                row = by_key.get(okey)
                if row is None or not row.get('stable_player_id') or row.get('_retired'):
                    residue.append({'name': name, 'score': score, 'reason': 'override-target-invalid',
                                    'override_key': okey})
                    continue
                resolved.append(RE.ResolvedRow(row['stable_player_id'], row['key'], row['player'],
                                               score, 'owner-override:%s' % kind))
                continue
            if kind == 'unmapped':
                residue.append({'name': name, 'score': score, 'reason': 'override-unmapped',
                                'note': 'owner override covers this name but not (round %d, score %g)'
                                % (round_n, score)})
                continue
            # not overridden -> the live active-pool resolver (exact active match, else residue)
            status, srow, cands = resolver.resolve(name)
            if status == RE.RESOLVED:
                resolved.append(RE.ResolvedRow(srow['stable_player_id'], srow['key'], srow['player'],
                                               score, 'exact'))
            else:
                residue.append({'name': name, 'score': score,
                                'reason': 'ambiguous' if status == RE.AMBIGUOUS else 'unresolved',
                                'candidates': [c['name'] for c in cands[:4]]})
        return resolved, residue

    # -- PREFLIGHT: read+validate ALL files, resolve, classify, detect every halt condition -------
    def preflight(self):
        store_rows = self._store_rows()
        by_key = {r['key']: r for r in store_rows if r.get('key')}
        resolver = RE.ActivePoolResolver(store=store_rows)
        active_keys = {r['key'] for r in store_rows if RE.is_active(r)}
        ledger_applied = set(load_ledger(self._ledger_path()).get('applied', []))

        rounds = []
        halt_reasons = []
        for round_n, path in self.files:
            parsed = FW.parse_round_file(path)
            resolved, residue = self._resolve_round(round_n, parsed['rows'], resolver, by_key)
            # duplicate stable-key assignments within the round (after overrides)
            seen = {}
            dups = []
            for r in resolved:
                seen.setdefault(r.key, []).append(r.score)
            for k, scores in seen.items():
                if len(scores) > 1:
                    dups.append({'key': k, 'scores': sorted(scores)})
            listed_keys = set(seen)
            absent = sorted(active_keys - listed_keys)
            overrides_applied = [{'name': r.name, 'key': r.key, 'score': r.score, 'via': r.via}
                                 for r in resolved if r.via.startswith('owner-override')]
            triples = {ledger_key(r.stable_player_id, self.season, round_n) for r in resolved}
            already = triples <= ledger_applied and bool(triples)
            rd = {
                'round': round_n, 'file': parsed['path'], 'sha256': parsed['sha256'],
                'encoding': parsed['encoding'], 'listed': parsed['listed'],
                'played': len(resolved) + len([1 for _r in residue]),   # listed==played (file membership)
                'resolved': len(resolved), 'listed_zero': parsed['listed_zero'],
                'absent_dnp': len(absent), 'active_universe': len(active_keys),
                'unresolved': [r for r in residue if r['reason'] in ('unresolved', 'override-unmapped',
                                                                     'override-target-invalid')],
                'ambiguous': [r for r in residue if r['reason'] == 'ambiguous'],
                'duplicate_keys': dups, 'identity_overrides': overrides_applied,
                'already_applied': already, 'resolved_rows': resolved, 'triples': sorted(triples),
            }
            if rd['unresolved']:
                halt_reasons.append('round %d: %d unresolved/unmapped name(s): %s'
                                    % (round_n, len(rd['unresolved']),
                                       [r['name'] for r in rd['unresolved']][:5]))
            if rd['ambiguous']:
                halt_reasons.append('round %d: %d ambiguous name(s): %s'
                                    % (round_n, len(rd['ambiguous']), [r['name'] for r in rd['ambiguous']][:5]))
            if dups:
                halt_reasons.append('round %d: duplicate stable-key assignment(s): %s'
                                    % (round_n, dups))
            rounds.append(rd)
        report = {
            'kind': 'catchup_preflight', 'season': self.season,
            'rounds': [{k: v for k, v in rd.items() if k not in ('resolved_rows',)} for rd in rounds],
            'halt_reasons': halt_reasons, 'clean': not halt_reasons,
            'identity_override_names': sorted(self.overrides.names),
        }
        return report, rounds

    # -- build one round's snapshot against the CURRENT committed store ----------------------------
    def _build_snapshot(self, round_n, resolved_rows, generated_at):
        ent = RE.RoundEntry(round_n, season_year=self.season, store_path=self._store_path())
        return ent.build_snapshot(resolved_rows, generated_at=generated_at)

    # -- RUN: sequential per-round transactions after ONE approval --------------------------------
    def run(self, *, approved, generated_at, refresh_ui=True, emit_movers=True, txn_root=None):
        """Apply every round in numerical order, each as its own committed transaction, using the
        immediately-preceding committed round as the next baseline. Requires ONE approval. Stops
        immediately on any round failure (the last fully committed round is preserved). Restart-safe:
        an already-committed round (all triples in the ledger) is SKIPPED and the catch-up resumes from
        the next unapplied round; a crash mid-commit is refused until recovered."""
        if not approved:
            raise CatchupError("catch-up not approved — no round applied (one consolidated approval "
                               "is required before the first write).")
        report, rounds = self.preflight()
        if not report['clean']:
            raise CatchupError("preflight is NOT clean — halting before the first write:\n  - "
                               + "\n  - ".join(report['halt_reasons']))

        applier = SA.StagedRoundApplier.for_repo(self.repo_root, txn_root=txn_root)
        # a crash mid-commit from a prior run must be recovered before continuing
        if applier.scan_incomplete():
            raise SA.IncompleteTransactionError(applier.scan_incomplete())

        results = []
        for rd in rounds:
            round_n = rd['round']
            # restart-safe / dedup: skip a round already fully committed
            ledger_applied = set(load_ledger(self._ledger_path()).get('applied', []))
            if set(rd['triples']) <= ledger_applied and rd['triples']:
                results.append({'round': round_n, 'status': 'skipped_already_applied',
                                'store_after': _md5(self._store_path())})
                continue
            snap = self._build_snapshot(round_n, rd['resolved_rows'], generated_at)
            res = applier.apply_snapshot(snap, generated_at=generated_at, txn_id='txn_catchup_r%d' % round_n)
            ui_ev = applier.refresh_ui() if refresh_ui else {'ran': False}
            # movers is generated ONLY after the round fully committed (store+board+ledger+history+UI):
            # played = the keys LISTED this round (a score of 0 is a played score); absent keys are DNP.
            mv_ev = None
            if emit_movers:
                played = {r.key: r.score for r in rd['resolved_rows']}
                evidence = {'store_md5_before': res.store_md5_before, 'store_md5_after': res.store_md5_after,
                            'board_md5_before': res.board_md5_before, 'board_md5_after': res.board_md5_after,
                            'txn_id': os.path.basename(res.txn_dir)}
                mv_ev = MV.emit(self.repo_root, round_n, played=played, evidence=evidence,
                                generated_at=generated_at)
            results.append({
                'round': round_n, 'status': 'applied', 'players_applied': res.players_applied,
                'store_before': res.store_md5_before, 'store_after': res.store_md5_after,
                'board_before': res.board_md5_before, 'board_after': res.board_md5_after,
                'guard5_green': res.guard5_green, 'ledger_total': res.ledger_total,
                'history_rounds': (res.history or {}).get('rounds_after'),
                'value_history_md5': (res.history or {}).get('value_history_md5'),
                'rank_history_md5': (res.history or {}).get('rank_history_md5'),
                'pos_rank_history_md5': (res.history or {}).get('pos_rank_history_md5'),
                'ui_ok': ui_ev.get('ok'), 'ui_board_stamp': ui_ev.get('ui_board_stamp'),
                'movers_report': (mv_ev or {}).get('movers_json'),
                'movers_ui_bundle': (mv_ev or {}).get('ui_bundle'),
                'movers_played': (mv_ev or {}).get('played'),
                'movers_dnp': (mv_ev or {}).get('dnp'),
                'movers_ui_rows_injected': (mv_ev or {}).get('ui_rows_injected'),
                'txn_dir': os.path.basename(res.txn_dir),
            })
        return {'kind': 'catchup_run', 'season': self.season, 'rounds': results,
                'final_store': _md5(self._store_path()), 'final_board': _md5(
                    os.path.join(self.repo_root, 'data', 'rl_build', 'rl_app_data.json'))}


def _md5(path):
    import hashlib
    if not os.path.exists(path):
        return None
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()
