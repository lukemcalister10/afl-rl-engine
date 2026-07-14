# Reproduction

READ-ONLY measurement harnesses. They exec a copy of the engine and monkeypatch functions **in memory
only** (never the committed engine) to measure counterfactual regime-flip valuations.

Board of record: tag `9f8ae76` · board `81e48293` · store `b0c39d78` · engine `2030e5df`.

```bash
# 1. bootstrap the pinned workspace (Guard 5 must PASS)
bash bootstrap.sh
# 2. scratch workspace pinned to the board-of-record store (b0c39d78 from the v2.9 tag)
mkdir -p /tmp/nq_ws && cp -rf /home/claude/rl_workspace/rl_after/. /tmp/nq_ws/
git cat-file -p 9f8ae76:engine/rl_after/rl_model_data.json > /tmp/nq_ws/rl_model_data.json   # store b0c39d78
git cat-file -p 9f8ae76:data/rl_build/rl_app_data.json     > /tmp/nq_ws/board_of_record.json # board 81e48293
cp session_2026-07-14/nqual_cascade/harness/*.py /tmp/nq_ws/
# 3. run (order: master -> t3 -> t4 -> t5 -> t1t2)
cd /tmp/nq_ws
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/tmp/nq_ws:/home/claude/rl_vendor
python3 01_master_extract.py   # verifies board byte-exact (804/804, maxdiff 0); writes master.json
python3 02_t3_cliff_countertick.py
python3 03_t4_pedigree_worth.py
python3 04_t5_evidence_curve.py
python3 05_t1_t2_tables.py
```

`06_census_551_probe.py` reverse-engineers the census proximity definitions.
Numéraire divisor `F=1.0524` (L7 baked); shipped value = `round(ev(p,2026)/F)`.
