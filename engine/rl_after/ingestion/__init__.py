"""Round-score ingestion — PROVISION ONLY (apply switch OFF).

Plumbing for the owner's weekly round-score feed:
    parse (round_score_parser) -> resolve at the score boundary (id_resolver)
    -> aggregate -> VALIDATED PREVIEW + anomaly checks (score_ingestor).

APPLY (store write) is HARD-GATED OFF and deliberately not implemented here — see
score_ingestor.apply and docs/GO_LIVE_round_score_ingestion.md. This package writes
NOTHING to the single source; the preview is a diff artifact, never a store copy.
"""
from .round_score_parser import RoundScore, ParseError, parse_feed, parse_rows
from .score_ingestor import (
    ScoreIngestor, IngestionPreview, SeasonAppend, Exception_, Anomaly,
    IngestionGatedError, APPLY_DEFAULT,
)

__all__ = [
    'RoundScore', 'ParseError', 'parse_feed', 'parse_rows',
    'ScoreIngestor', 'IngestionPreview', 'SeasonAppend', 'Exception_', 'Anomaly',
    'IngestionGatedError', 'APPLY_DEFAULT',
]
