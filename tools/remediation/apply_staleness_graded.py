#!/usr/bin/env python3
"""Apply the already-derived D8 graded staleness treatment to the current v2.11 engine.

This is a mechanism-level correction only. It does not edit a player row, score, value, board, store,
or fitted artifact. The D8 knots are copied exactly from engine/prototypes/staleness_graded_cap.py.
The only adaptation is to the current engine's later D10 semantics:

* the stalled cap is V0-based (not the retired draft-value basis); and
* current-season qualification uses the same prorated six-game bar as nseas_pro().

The script is intentionally one-shot and drift-guarded against the exact Round 19 MVP engine.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "engine" / "rl_after" / "_merged_recover.py"
BOOT = ROOT / "data" / "expected_boot.json"
CONTRACT = ROOT / "data" / "release_contract.json"
EXPECTED_ENGINE_MD5 = "dc7e34b0d50470897af237c638236868"

HEADER_OLD = "# ===== WIRED ev =====\ndef ev(p,Y=2026):"
HEADER_NEW = """# ===== WIRED ev =====
# D8 GRADED STALENESS RELEASE (owner-authorized remediation, 2026-07-22).
# Sole candidate: the already-derived 532-cell historical design in
# session_2026-07-03/d8_ask2_graded_cap.md. Knots are copied byte-for-number;
# no current-board tuning and no named-player exception.
_D8Q=[0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80]
_D8G1=[0.25789,0.25789,0.25789,0.30834,0.36155,0.42112,0.49276,0.56996,0.59452]
_D8G2=[0.0,0.00275,0.00275,0.04319,0.08776,0.13367,0.18032,0.20098,0.20408]
def _staleness_grade(p,Y,pos):
    \"\"\"Evidence release for the stalled-one-season population.

    grade=1 when the sole qualifying season is the season being evaluated; grade=0 with no
    live output; otherwise use the frozen D8 gap=1 / gap>=2 quality curves. The current-season
    qualifying bar is exactly the current engine's nseas_pro bar (6 * _fEy), so this correction
    does not create a second qualification law.
    \"\"\"
    current=[x for x in p['scoring'] if x['year']==Y]
    current_qual=any(x['games']>=6.0*_fEy(Y,p) for x in current)
    if current_qual:
        return 1.0
    live=[x for x in current if x['games']>0]
    if not live:
        return 0.0
    prior_qual=[x['year'] for x in p['scoring'] if x['year']<Y and x['games']>=6]
    if not prior_qual:
        return 0.0
    qv=(live[0]['avg']*REF/era.get(Y,REF))/max(MA.REPL.get(pos,1e-9),1e-9)
    gap=Y-max(prior_qual)
    return float(np.interp(qv,_D8Q,_D8G1 if gap==1 else _D8G2))
def ev(p,Y=2026):"""

BLOCK_OLD = """    if el>=onset and ns<=1:                                   # stalled: essentially no production after the window
        frac=0.25*max(0.4,1-0.10*(el-onset))*(1.6 if keyruc else 1.0)
        e=min(e, v0*frac)"""
BLOCK_NEW = """    if el>=onset and ns<=1:                                   # stalled: D8 graded release by live-output evidence
        frac=0.25*max(0.4,1-0.10*(el-onset))*(1.6 if keyruc else 1.0)
        cap=v0*frac
        gr=_staleness_grade(p,Y,pos)
        e=min(e, cap+gr*max(0.0,e-cap))"""


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def contract_hash(contract: dict) -> str:
    body = {k: v for k, v in contract.items() if k not in ("contract_sha256", "_doc")}
    payload = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> None:
    before = md5(ENGINE)
    if before != EXPECTED_ENGINE_MD5:
        raise SystemExit(f"engine drift: {before} != {EXPECTED_ENGINE_MD5}")
    source = ENGINE.read_text(encoding="utf-8")
    if source.count(HEADER_OLD) != 1:
        raise SystemExit(f"ev header anchor count {source.count(HEADER_OLD)} != 1")
    if source.count(BLOCK_OLD) != 1:
        raise SystemExit(f"stalled block anchor count {source.count(BLOCK_OLD)} != 1")
    source = source.replace(HEADER_OLD, HEADER_NEW, 1).replace(BLOCK_OLD, BLOCK_NEW, 1)
    ENGINE.write_text(source, encoding="utf-8")
    after = md5(ENGINE)
    if after == before:
        raise SystemExit("engine did not move")

    boot = json.loads(BOOT.read_text(encoding="utf-8"))
    if boot.get("engine_head") != before:
        raise SystemExit("expected_boot engine_head is not the verified starting engine")
    boot["engine_head"] = after
    boot["_staleness_graded_note"] = (
        "OWNER-AUTHORIZED candidate remediation 2026-07-22: exact D8 measured graded-staleness "
        "curves wired into the current V0-based stalled branch; no player exception and no current-board "
        "parameter tuning. Current-season qualification uses nseas_pro's prorated six-game bar. Candidate "
        "board/deltas remain review-only until separate owner finalization."
    )
    BOOT.write_text(json.dumps(boot, indent=2) + "\n", encoding="utf-8")

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    identities = contract.setdefault("identities", {})
    if identities.get("engine_head") != before:
        raise SystemExit("release contract engine_head is not the verified starting engine")
    identities["engine_head"] = after
    contract.pop("contract_sha256", None)
    contract["contract_sha256"] = contract_hash(contract)
    CONTRACT.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"engine_before": before, "engine_after": after,
                      "prototype": "engine/prototypes/staleness_graded_cap.py",
                      "knots_changed": False, "player_overrides": 0}, indent=2))


if __name__ == "__main__":
    main()
