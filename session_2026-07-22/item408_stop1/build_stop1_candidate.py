#!/usr/bin/env python3
"""ITEM 408 STOP-1 candidate builder.

Builds the balanced R19 board in the accepted pinned environment, entirely in the existing disposable
FV-provenance staging path. It writes owner-view evidence under THIS session directory only; it never
writes data/expected_boot.json, release contracts, canonical boards, score ledgers, tags, or refs.

Provenance + real fences (GPT Sol review findings 3/4):
  - records the exact input commit + authoritative source identities used for generation;
  - hashes every protected artifact BEFORE and AFTER the build, ABORTS non-zero if any changed,
    and derives each fence flag from the measured before/after equality (never hardcoded False);
  - the candidate board md5 is derived dynamically (never asserted to a pinned answer);
  - board of record 6f07f7cb is NOT replaced: STOP-1 is a balanced/strict-board PIN advance decision.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FV_TEST = REPO / "session_2026-07-20" / "fv_provenance_remediation" / "test_fv_provenance.py"
REF06 = REPO / "session_2026-07-20" / "fv_provenance_remediation" / "fixtures" / "reference_vector_06d8af60.json"
BOARD6F = REPO / "data" / "rl_build" / "rl_app_data.json"
OUT_BOARD = HERE / "candidate_balanced_r19.json"
OUT_VECTOR = HERE / "candidate_value_vector.json"
OUT_DIFF = HERE / "STOP1_CANDIDATE.json"
OUT_REPORT = HERE / "STOP1_REPORT.md"

# Frozen / governed artifacts that this build must NOT mutate. Fence flags are DERIVED from the measured
# before/after hashes of these paths — the report shows False only because the hashes prove no mutation.
PROTECTED = {
    "canonical_board": "data/rl_build/rl_app_data.json",                       # board of record 6f07f7cb
    "expected_boot": "data/expected_boot.json",                               # governed pins
    "release_contract": "data/release_contract.json",                        # governed identities + seal
    "curve_contract": "ui/release_pick_curve.json",                          # frozen ruler contract
    "curve": "engine/rl_after/pvc_curve_v2.json",                            # frozen pick curve
    "per_entrant": "session_2026-07-17/legd_derivation/out/per_entrant.json",  # per-entrant 40d7da7c
    "store": "engine/rl_after/rl_model_data.json",                           # authoritative store
    "score_ledger": "engine/rl_after/ingestion/applied_rounds_ledger.json",    # score-apply state
}
# Which fence flag each protected artifact backs (True == that artifact was written/armed).
FENCE_OF = {
    "canonical_board": "canonical_board_written",
    "expected_boot": "expected_boot_written",
    "release_contract": "release_contract_written",
    "curve_contract": "curve_contract_written",
    "curve": "curve_written",
    "per_entrant": "per_entrant_written",
    "store": "store_written",
    "score_ledger": "score_apply_armed",
}


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot_protected() -> dict:
    return {name: (md5(REPO / rel) if (REPO / rel).exists() else None) for name, rel in PROTECTED.items()}


def input_commit() -> str:
    env = os.environ.get("GITHUB_SHA")
    if env:
        return env
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def pkg_versions() -> dict:
    out = {}
    for mod in ("numpy", "scipy", "sklearn", "openpyxl"):
        try:
            out[mod] = __import__(mod).__version__
        except Exception:
            out[mod] = "unavailable"
    out["python"] = "%d.%d.%d" % sys.version_info[:3]
    return out


def vector(path: Path) -> dict:
    doc = json.load(path.open(encoding="utf-8"))
    return {row["key"]: int(row["v"]) for row in doc["active"]}


def comparison(old: dict, new: dict) -> dict:
    old_keys, new_keys = set(old), set(new)
    common = sorted(old_keys & new_keys)
    movers = [
        {"key": key, "before": old[key], "after": new[key], "delta": new[key] - old[key]}
        for key in common
        if old[key] != new[key]
    ]
    movers.sort(key=lambda row: (-abs(row["delta"]), row["key"]))
    return {
        "before_count": len(old),
        "after_count": len(new),
        "common_count": len(common),
        "only_before": sorted(old_keys - new_keys),
        "only_after": sorted(new_keys - old_keys),
        "mover_count": len(movers),
        "sum_before": sum(old.values()),
        "sum_after": sum(new.values()),
        "sum_delta": sum(new.values()) - sum(old.values()),
        "movers": movers,
    }


def _cmp_block(title: str, ref_md5: str, cand_md5: str, cmp_: dict, sheezel_ref, sheezel_cand) -> str:
    top = cmp_["movers"][:20]
    lines = [
        "### %s" % title, "",
        "| metric | value |", "|---|---|",
        "| candidate board md5 | `%s` |" % cand_md5,
        "| comparison board md5 | `%s` |" % ref_md5,
        "| candidate active count | %d |" % cmp_["after_count"],
        "| comparison active count | %d |" % cmp_["before_count"],
        "| total candidate value | %d |" % cmp_["sum_after"],
        "| total comparison value | %d |" % cmp_["sum_before"],
        "| total-value delta | %+d |" % cmp_["sum_delta"],
        "| Harry Sheezel candidate | %s |" % sheezel_cand,
        "| Harry Sheezel comparison | %s |" % sheezel_ref,
        "| Harry Sheezel delta | %s |" % (
            "%+d" % (sheezel_cand - sheezel_ref) if isinstance(sheezel_cand, int) and isinstance(sheezel_ref, int) else "n/a"),
        "| mover count | %d |" % cmp_["mover_count"],
        "| added keys (only in candidate) | %d |" % len(cmp_["only_after"]),
        "| removed keys (only in comparison) | %d |" % len(cmp_["only_before"]),
        "",
        "Added keys: %s" % (", ".join(cmp_["only_after"]) if cmp_["only_after"] else "(none)"), "",
        "Removed keys: %s" % (", ".join(cmp_["only_before"]) if cmp_["only_before"] else "(none)"), "",
        "Top %d absolute movers:" % len(top), "",
        "| key | before | after | delta |", "|---|---|---|---|",
    ]
    lines += ["| %s | %s | %s | %+d |" % (m["key"], m["before"], m["after"], m["delta"]) for m in top]
    lines.append("")
    return "\n".join(lines)


def render_report(report: dict) -> str:
    c = report["candidate"]
    ident = report["input_identity"]
    md = [
        "# ITEM 408 — R19 STOP-1 candidate report (OWNER VIEW)", "",
        "**%s**" % report["state"], "",
        "Mechanical builder: build-seat-claude-code. This is a candidate for the owner's STOP-1 view only.",
        "**Board of record `6f07f7cb` is NOT replaced by this build and is not replaced at STOP-1.** The STOP-1",
        "decision is whether to approve advancing the balanced/strict board pin from `06d8af60` to the candidate",
        "`%s` and, after the owner's word, moving all dependent balanced-board / FV / reference identities" % c["board_md5"][:8],
        "atomically. No production artifact is written by this build (fences below are measured, not asserted).",
        "",
        "## Input identity (exact, reproducible)", "",
        "| input | identity |", "|---|---|",
        "| generated at commit | `%s` |" % ident["generated_at_commit"],
        "| authoritative store md5 | `%s` |" % ident["authoritative_store_md5"],
        "| rl_model md5 (build prov) | `%s` |" % ident["rl_model_md5"],
        "| forward-valuation identity | `%s` |" % ident["fv_identity"],
        "| forward-valuation module dir | `%s` |" % ident["fv_module_dir"],
        "| distribution-pricing md5 | `%s` |" % ident["distribution_pricing_md5"],
        "| config-manifest identity | `%s` |" % ident["config_manifest_identity"],
        "| expected_boot md5 | `%s` |" % ident["expected_boot_md5"],
        "| release-contract md5 | `%s` |" % ident["release_contract_md5"],
        "| release-pick-curve md5 | `%s` |" % ident["release_pick_curve_md5"],
        "| reference-vector 06d8af60 md5 | `%s` |" % ident["reference_vector_md5"],
        "| board-of-record md5 | `%s` |" % ident["board_of_record_md5"],
        "| pinned env | %s |" % json.dumps(ident["pinned_env"]),
        "| deterministic env | %s |" % json.dumps(ident["deterministic_env"]),
        "",
        "- generation command: `python3 session_2026-07-22/item408_stop1/build_stop1_candidate.py`", "",
        "## Candidate identity (derived dynamically)", "",
        "| field | value |", "|---|---|",
        "| candidate board md5 | `%s` |" % c["board_md5"],
        "| active players | %d |" % c["active"],
        "| total value (sum_v) | %d |" % c["sum_v"],
        "| Harry Sheezel | %s |" % c["harry_sheezel"],
        "| scratch board path | `%s` |" % c["path"],
        "",
        _cmp_block("Comparison 1 — candidate vs historical balanced board 06d8af60 (the stale pin)",
                   report["strict_reference"]["board_md5"], c["board_md5"],
                   report["candidate_vs_strict_06d8af60"],
                   report["strict_reference"]["harry_sheezel"], c["harry_sheezel"]),
        _cmp_block("Comparison 2 — candidate vs board of record 6f07f7cb (frozen; NOT replaced)",
                   report["released_board"]["board_md5"], c["board_md5"],
                   report["candidate_vs_released_6f07f7cb"],
                   report["released_board"]["harry_sheezel"], c["harry_sheezel"]),
        "## Protected artifacts — measured before/after (build mutates nothing)", "",
        "| artifact | path | before md5 | after md5 | unchanged |", "|---|---|---|---|---|",
    ]
    for name, rel in sorted(PROTECTED.items()):
        ba = report["protected_before_after"][name]
        md.append("| %s | `%s` | `%s` | `%s` | %s |" % (name, rel, ba["before"], ba["after"], ba["before"] == ba["after"]))
    md += [
        "",
        "## Fences (measured from the hashes above; True == that artifact was written/armed)", "",
        "| fence | written/armed |", "|---|---|",
    ]
    md += ["| %s | %s |" % (k, v) for k, v in sorted(report["fences"].items())]
    md += [
        "",
        "## STOP-1 owner decision", "",
        "PENDING — the owner is the sole authority to approve advancing the balanced/strict board pin and, after",
        "his word, atomically moving the dependent balanced-board / FV / reference identities. This builder stops",
        "at the candidate; no pin is moved and board of record `6f07f7cb` is not replaced.", "",
    ]
    return "\n".join(md)


def main() -> int:
    spec = importlib.util.spec_from_file_location("item408_fv_test", FV_TEST)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the existing disposable FV builder")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    before = snapshot_protected()

    result = mod._run_build({}, rl_fv=str(REPO / "engine" / "forward_valuation"), balanced=True)
    try:
        if result["rc"] != 0 or not result["board_path"]:
            raise RuntimeError("candidate build failed rc=%s stderr=%s" % (result["rc"], result.get("stderr", "")[-2000:]))
        built_path = Path(result["board_path"])
        shutil.copy2(built_path, OUT_BOARD)
        candidate = vector(OUT_BOARD)
        old06 = {str(k): int(v) for k, v in json.load(REF06.open(encoding="utf-8"))["vector"].items()}
        current6f = vector(BOARD6F)

        after = snapshot_protected()
        changed = [name for name in PROTECTED if before.get(name) != after.get(name)]
        if changed:
            raise RuntimeError("PROTECTED ARTIFACT MUTATED during candidate build: %s" % changed)

        prov = result.get("prov") or {}
        identity = {
            "generated_at_commit": input_commit(),
            "authoritative_store_md5": md5(REPO / PROTECTED["store"]),
            "rl_model_md5": prov.get("rl_model_md5"),
            "fv_identity": prov.get("fv_identity"),
            "fv_module_dir": prov.get("resolved_fv_dir"),
            "distribution_pricing_md5": prov.get("distribution_pricing_md5"),
            "config_manifest_identity": prov.get("config_manifest_identity"),
            "expected_boot_md5": md5(REPO / PROTECTED["expected_boot"]),
            "release_contract_md5": md5(REPO / PROTECTED["release_contract"]),
            "release_pick_curve_md5": md5(REPO / PROTECTED["curve_contract"]),
            "reference_vector_md5": md5(REF06),
            "board_of_record_md5": md5(BOARD6F),
            "pinned_env": pkg_versions(),
            "deterministic_env": {"PYTHONHASHSEED": "0", "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1",
                                  "MKL_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1",
                                  "RL_PVC2": "1", "RL_LEGE": "0", "RL_LEGF": "0", "RL_PRIOR_TREES": "400"},
        }
        protected_ba = {name: {"path": PROTECTED[name], "before": before.get(name), "after": after.get(name)}
                        for name in PROTECTED}
        fences = {FENCE_OF[name]: (before.get(name) != after.get(name)) for name in PROTECTED}

        full = [
            {"key": key, "strict_06d8af60": old06.get(key),
             "released_6f07f7cb": current6f.get(key), "candidate": candidate.get(key)}
            for key in sorted(set(old06) | set(current6f) | set(candidate))
        ]
        json.dump({"vector": full}, OUT_VECTOR.open("w", encoding="utf-8"), indent=2, sort_keys=True)

        report = {
            "state": "STOP-1 OWNER VIEW — CANDIDATE ONLY; NO PIN MOVED; BOARD OF RECORD 6f07f7cb NOT REPLACED",
            "input_identity": identity,
            "candidate": {
                "board_md5": md5(OUT_BOARD),
                "active": len(candidate),
                "sum_v": sum(candidate.values()),
                "harry_sheezel": candidate.get("harry-sheezel"),
                "path": str(OUT_BOARD.relative_to(REPO)),
            },
            "strict_reference": {
                "board_md5": "06d8af60b679a12db07c064c60c065f9",
                "role": "historical balanced pin in expected_boot.json (the stale pin under STOP-1 review)",
                "active": len(old06),
                "sum_v": sum(old06.values()),
                "harry_sheezel": old06.get("harry-sheezel"),
            },
            "released_board": {
                "board_md5": md5(BOARD6F),
                "role": "board of record — FROZEN under the directive; not replaced by STOP-1",
                "active": len(current6f),
                "sum_v": sum(current6f.values()),
                "harry_sheezel": current6f.get("harry-sheezel"),
            },
            "candidate_vs_strict_06d8af60": comparison(old06, candidate),
            "candidate_vs_released_6f07f7cb": comparison(current6f, candidate),
            "protected_before_after": protected_ba,
            "fences": fences,
            "stop1_semantics": {
                "decision": "advance the balanced/strict board pin 06d8af60 -> candidate; move dependent "
                            "balanced-board/FV/reference identities atomically AFTER owner word",
                "candidate_vector_equals_board_of_record_vector": comparison(current6f, candidate)["mover_count"] == 0,
                "candidate_md5_is_board_of_record_md5": md5(OUT_BOARD) == md5(BOARD6F),
                "stop1_replaces_board_of_record_6f07f7cb": False,
            },
        }
        json.dump(report, OUT_DIFF.open("w", encoding="utf-8"), indent=2, sort_keys=True)
        OUT_REPORT.write_text(render_report(report), encoding="utf-8")
        print(json.dumps({
            "board_md5": report["candidate"]["board_md5"],
            "active": report["candidate"]["active"],
            "sum_v": report["candidate"]["sum_v"],
            "harry_sheezel": report["candidate"]["harry_sheezel"],
            "movers_vs_06": report["candidate_vs_strict_06d8af60"]["mover_count"],
            "movers_vs_6f": report["candidate_vs_released_6f07f7cb"]["mover_count"],
            "protected_all_unchanged": not changed,
            "at_commit": identity["generated_at_commit"],
        }, sort_keys=True))
        return 0
    finally:
        if result.get("base"):
            shutil.rmtree(result["base"], ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
