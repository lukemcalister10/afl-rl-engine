# REQUIRED_INPUTS — verify presence at restore-verify; report gaps TURN ONE (PROCESS_CHANGES §7)

| input | where | status at handover | needed for |
|---|---|---|---|
| This tarball (whole workspace + vendored deps) | the bundle itself | PRESENT | everything |
| Engine head `_merged_recover.py` (8aed420a) | engine/rl_after/ | PRESENT (md5 verified) | all pricing |
| Store `rl_model_data.json` / `.pre_stage0` (644d1254) | engine/rl_after/ | PRESENT | all pricing |
| Band pickle `cm_400.pkl` (34faa865) | data/ | PRESENT | conditional prior |
| GATE-1 + walk-forward harnesses | engine/rl_after/ (`_gate1_wf.py`, `_gate1_picksplit.py`, `s4_matrix_M1v7.py`, `s4_render_M1v7.py`) | PRESENT | book / gates |
| Vendored deps (numpy/sklearn/unidecode, etc.) | vendor/ | PRESENT (confirm satisfies imports on clean restore — see verify) | engine load |
| **103-player dev-position template** | — | **ABSENT — Luke supplies at kickoff** | dev-position fold-in workstream |
| Board / HTML + JS-parity pipeline | engine/rl_after/ (`rl_build_html.py`, `rl_export.py`, `rl_model.py`) | PRESENT (confirm JS-parity harness runs) | board build / parity gate |
| SHIP_GATES.md (~15-20 named relativities) | — | **NOT YET CREATED — Luke picks before PVC stage** (PROCESS_CHANGES §3) | stopping rule |
| BAKE_CHECKLIST.md | to be written before first bake (M1+v7) | NOT YET CREATED (PROCESS_CHANGES §8) | M1+v7 bake |

**Turn-one action for successor:** run `verify_restore.sh`; then emit a REQUIRED_INPUTS gap report (the two ABSENT/NOT-YET items above are known gaps — the dev-position template must come from Luke before the fold-in workstream can run).
