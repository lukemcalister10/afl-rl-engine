#!/usr/bin/env python3
"""Apply the pre-derived D8 graded-staleness treatment to the PRESENT board only.

This is deliberately narrow. It replaces the binary stalled-player cap with the frozen 532-cell
historical D8 grade at the actual evaluation year. Forward-lens anchoring is not changed here and is
preserved for separate review. No score, player row, fitted artifact, knot, or named exception changes.
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
# D8 GRADED STALENESS — PRESENT BOARD CORRECTION (owner-authorized remediation, 2026-07-22).
# Frozen 532-cell historical design; no current-board tuning and no named-player exception.
_D8Q=[0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80]
_D8G1=[0.25789,0.25789,0.25789,0.30834,0.36155,0.42112,0.49276,0.56996,0.59452]
_D8G2=[0.0,0.00275,0.00275,0.04319,0.08776,0.13367,0.18032,0.20098,0.20408]
def _staleness_grade(p,Y,pos):
    \"\"\"Evidence release for the stalled-one-season population at the evaluated evidence year.\"\"\"
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
BLOCK_NEW = """    if el>=onset and ns<=1:                                   # stalled: D8 graded release at evaluated year
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
    if source.count(HEADER_OLD) != 1 or source.count(BLOCK_OLD) != 1:
        raise SystemExit("patch anchors do not match exact Round 19 engine")
    ENGINE.write_text(source.replace(HEADER_OLD, HEADER_NEW, 1).replace(BLOCK_OLD, BLOCK_NEW, 1), encoding="utf-8")
    after = md5(ENGINE)

    boot = json.loads(BOOT.read_text(encoding="utf-8"))
    if boot.get("engine_head") != before:
        raise SystemExit("expected_boot engine_head is not the verified starting engine")
    boot["engine_head"] = after
    boot["_present_staleness_note"] = (
        "OWNER-AUTHORIZED present-board correction 2026-07-22: frozen D8 graded-staleness curves; "
        "forward-lens treatment intentionally unchanged and deferred. No named-player tuning."
    )
    BOOT.write_text(json.dumps(boot, indent=2) + "\n", encoding="utf-8")

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    ids = contract.setdefault("identities", {})
    if ids.get("engine_head") != before:
        raise SystemExit("release contract engine_head is not the verified starting engine")
    ids["engine_head"] = after
    contract.pop("contract_sha256", None)
    contract["contract_sha256"] = contract_hash(contract)
    CONTRACT.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"engine_before": before, "engine_after": after, "forward_lens_changed": False}, indent=2))


if __name__ == "__main__":
    main()
