"""Round-score ingestion — weekly feed plumbing + the gated APPLY store-write.

Pipeline for the owner's weekly round-score feed:
    parse (round_score_parser) -> resolve at the score boundary (id_resolver)
    -> aggregate -> VALIDATED PREVIEW + anomaly checks (score_ingestor)
    -> APPLY: merge -> regen board -> re-stamp boot manifest -> dedup ledger (round_apply).

APPLY (the store write) is HARD-GATED OFF (score_ingestor.APPLY_DEFAULT=False + env
INGEST_SCORE_APPLY unset — both halves default OFF, belt-and-braces). The write path
(round_apply.RoundApplier) is implemented behind that gate and proven on SCRATCH copies;
this package writes NOTHING to the single source until go-live arms both halves. See
docs/GO_LIVE_round_score_ingestion.md.
"""
from .round_score_parser import RoundScore, ParseError, parse_feed, parse_rows
from .score_ingestor import (
    ScoreIngestor, IngestionPreview, SeasonAppend, Exception_, Anomaly,
    IngestionGatedError, APPLY_DEFAULT,
)
from .round_apply import (
    RoundApplier, ApplyResult, SeasonBoundError, DuplicateRoundError, PreviewNotCleanError,
    load_ledger, save_ledger, ledger_key, DEFAULT_SEASON_ROUNDS,
)
from . import round_entry
from .round_entry import (
    RoundEntry, ActivePoolResolver, ResolvedRow, ResidueLine, snapshot_bytes,
    compute_content_hash, verify_snapshot, load_snapshot, is_strong, SNAPSHOT_SCHEMA_VERSION,
)
from .staged_apply import (
    StagedRoundApplier, StagedApplyResult, preview_from_snapshot,
    StaleSnapshotError, AlteredSnapshotError, ResidueOpenError, StagedValidationError,
    IncompleteTransactionError,
)

__all__ = [
    'RoundScore', 'ParseError', 'parse_feed', 'parse_rows',
    'ScoreIngestor', 'IngestionPreview', 'SeasonAppend', 'Exception_', 'Anomaly',
    'IngestionGatedError', 'APPLY_DEFAULT',
    'RoundApplier', 'ApplyResult', 'SeasonBoundError', 'DuplicateRoundError',
    'PreviewNotCleanError', 'load_ledger', 'save_ledger', 'ledger_key', 'DEFAULT_SEASON_ROUNDS',
    'round_entry', 'RoundEntry', 'ActivePoolResolver', 'ResolvedRow', 'ResidueLine',
    'snapshot_bytes', 'compute_content_hash', 'verify_snapshot', 'load_snapshot', 'is_strong',
    'SNAPSHOT_SCHEMA_VERSION',
    'StagedRoundApplier', 'StagedApplyResult', 'preview_from_snapshot',
    'StaleSnapshotError', 'AlteredSnapshotError', 'ResidueOpenError', 'StagedValidationError',
    'IncompleteTransactionError',
]
