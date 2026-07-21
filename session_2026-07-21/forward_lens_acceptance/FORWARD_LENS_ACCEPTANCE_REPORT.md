# Forward Lens Acceptance Diagnostic

Verdict: **FAIL** — Board A reproduced and present invariance was measured, but required original Leg E/F historical/acceptance harnesses could not all be located and rerun unchanged; directive requires FAIL in that case.

Board A MD5: `06d8af60b679a12db07c064c60c065f9`. Board B MD5: `1f10220c341679903b79a319f554672c`.

Present value diffs: 0; present rank diffs: 0; present order diffs: 0; active added/removed: 0/0; pick 1 A/B: 3000/3000.

Limitation: RL_CONFIG_MODE was intentionally left unset for diagnostic builds because the manifest cannot represent RL_PVC2/RL_LEGE/RL_LEGF switches correctly; neither board is a canonical bake or release-certified build.

## Gate Table

| Test | Source | Threshold | Command | Result | Artifact |
|---|---|---|---|---|---|
| bootstrap fail-closed provenance | bootstrap.sh / boot_guard.py | pinned md5 equality | `bash bootstrap.sh` | PASS | session_2026-07-21/forward_lens_acceptance/bootstrap_fail-closed_provenance.txt |
| k=0 dormancy f3 | session_2026-07-18/legf3/tests/test_k0_dormancy.py | unchanged script passes | `python3 session_2026-07-18/legf3/tests/test_k0_dormancy.py` | FAIL | session_2026-07-21/forward_lens_acceptance/k=0_dormancy_f3.txt |
| k=0 dormancy f4 | session_2026-07-18/legf4/tests/test_k0_dormancy_f4.py | unchanged script passes | `python3 session_2026-07-18/legf4/tests/test_k0_dormancy_f4.py` | FAIL | session_2026-07-21/forward_lens_acceptance/k=0_dormancy_f4.txt |
| k=0 dormancy f5 | session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py | unchanged script passes | `python3 session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py` | FAIL | session_2026-07-21/forward_lens_acceptance/k=0_dormancy_f5.txt |
| Leg F4 gate | session_2026-07-18/legf4/scripts/gate_f4.py | predeclared script pass | `python3 session_2026-07-18/legf4/scripts/gate_f4.py` | FAIL | session_2026-07-21/forward_lens_acceptance/Leg_F4_gate.txt |
| Leg F5 gate | session_2026-07-18/legf5/scripts/gate_f5.py | predeclared script pass | `python3 session_2026-07-18/legf5/scripts/gate_f5.py` | FAIL | session_2026-07-21/forward_lens_acceptance/Leg_F5_gate.txt |
| historical -1 -> now projection comparison unchanged harness | not located as unchanged runnable harness | original threshold unavailable | n/a | FAIL | gate_results.json |
| historical -2 -> -1 projection comparison unchanged harness | not located as unchanged runnable harness | original threshold unavailable | n/a | FAIL | gate_results.json |
| original ±5% projected league-total gate unchanged harness | not located as unchanged runnable harness | original threshold unavailable | n/a | FAIL | gate_results.json |
| developing >= mid-career >= veteran gradient unchanged harness | not located as unchanged runnable harness | original threshold unavailable | n/a | FAIL | gate_results.json |
| age/evidence continuity, horizon cliffs, pedigree fading, LTI/availability, retirement/exit unchanged harness inventory | not located as unchanged runnable harness | original threshold unavailable | n/a | FAIL | gate_results.json |

## Population Summary
```json
{
  "league_totals": {
    "A": {
      "v": 752427,
      "vP1": 559828,
      "vP2": 434182
    },
    "B": {
      "v": 752427,
      "vP1": 686000,
      "vP2": 635411
    }
  },
  "ratios": {
    "A_vP1_v": {
      "n": 804,
      "min": 0.1111111111111111,
      "q1": 0.5112913824680105,
      "median": 0.7067435863817141,
      "q3": 0.85,
      "max": 2.8461538461538463
    },
    "B_vP1_v": {
      "n": 804,
      "min": 0.1308411214953271,
      "q1": 0.7329564489112228,
      "median": 0.8944113693105435,
      "q3": 1.0,
      "max": 2.272727272727273
    },
    "A_vP2_v": {
      "n": 804,
      "min": 0.0,
      "q1": 0.35459140867522443,
      "median": 0.5276575276575277,
      "q3": 0.73470673709292,
      "max": 2.6538461538461537
    },
    "B_vP2_v": {
      "n": 804,
      "min": 0.09345794392523364,
      "q1": 0.6113061397364262,
      "median": 0.8019842419559934,
      "q3": 1.0,
      "max": 2.0
    }
  },
  "A_counts": {
    "vP1": {
      "zero": 0,
      "near_zero_lt100": 200,
      "fall_gt10": 668,
      "fall_gt25": 466,
      "fall_gt50": 183,
      "rise_gt10": 9,
      "rise_gt25": 7,
      "rise_gt50": 4
    },
    "vP2": {
      "zero": 1,
      "near_zero_lt100": 259,
      "fall_gt10": 732,
      "fall_gt25": 617,
      "fall_gt50": 358,
      "rise_gt10": 8,
      "rise_gt25": 5,
      "rise_gt50": 3
    }
  },
  "B_counts": {
    "vP1": {
      "zero": 0,
      "near_zero_lt100": 168,
      "fall_gt10": 412,
      "fall_gt25": 214,
      "fall_gt50": 39,
      "rise_gt10": 11,
      "rise_gt25": 3,
      "rise_gt50": 2
    },
    "vP2": {
      "zero": 0,
      "near_zero_lt100": 194,
      "fall_gt10": 483,
      "fall_gt25": 334,
      "fall_gt50": 109,
      "rise_gt10": 20,
      "rise_gt25": 6,
      "rise_gt50": 2
    }
  }
}
```

## Top changes
See CSV/HTML for sortable complete player-level review. Deterministic cohort rule: sort active players by current rank, choose first five under age 23 (young), first five age 24-28 (prime), and first five age 29+ (veteran); rule defined before listing outputs.

## Artifact Manifest
- FORWARD_LENS_ACCEPTANCE_REPORT.md
- forward_lens_all_players.csv
- forward_lens_review.html
- board_A_lege0_legf0.json
- board_B_lege1_legf1.json
- gate_results.json
- field_diff_inventory.json
- provenance.json
- README.md
- scripts/run_diagnostic.py
