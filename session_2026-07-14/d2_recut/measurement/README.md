# D2 re-cut — measurement harness (reproducibility)

**Tier 3, READ-ONLY.** These scripts measure the LIVE engine on the tagged v2.9 board of record; they
modify nothing in the engine, store, board, gates, docs, or pricing. All perturbations are on in-memory
deep-copies or temporary function patches, restored after.

## Board of record
| artifact | md5 / sha |
|---|---|
| tag | `v2.9` = `9f8ae76` |
| board | `81e48293` |
| **store** | **`b0c39d78`** (`git cat-file -p 9f8ae76:engine/rl_after/rl_model_data.json`) |
| engine `_merged_recover.py` | `2030e5df` |
| config / register | `69ead79b` / `652d83e8` |

## Setup (scratch only, never committed) — identical to the prior job (S5 reuse)
```bash
SRC=/home/claude/rl_workspace/rl_after ; BOR=/tmp/bor_ws
rm -rf "$BOR"; mkdir -p "$BOR"; for f in "$SRC"/*; do ln -s "$f" "$BOR/$(basename "$f")"; done
rm -f "$BOR/rl_model_data.json"
git -C /home/user/afl-rl-engine cat-file -p 9f8ae76:engine/rl_after/rl_model_data.json > "$BOR/rl_model_data.json"
md5sum "$BOR/rl_model_data.json"    # -> b0c39d78...
cp session_2026-07-14/d2_recut/measurement/*.py /tmp/ && cd /tmp
python3 r1_form.py ; python3 r2_agecurve.py ; python3 r3_recency_charge.py ; python3 r4_phantom_boards.py
```
`harness.py` execs `_merged_recover.py` up to `=== AFTER` (as `run_panel.sh` does), exposing `MA/ev/cp/g`.
It `chdir`s to `$BOR`, so run the scripts as FILES from `/tmp` (not `python3 -c`).

## Scripts
- `harness.py`            — engine loader (board of record); byte-copy of the prior job's harness.
- `d2common.py`          — event/control construction (VERBATIM prior logic; reproduces −3.42) + gap-year
                           bookkeeping + the mean-reversion counterfactual (`fit_ctrl_model`, R1[G]).
- `r1_form.py`           — R1 additive vs multiplicative; mean-reversion net-out.  → `out_r1.txt`
- `r2_agecurve.py`       — R2 smooth age curve + bootstrap ribbon.                 → `out_r2.txt`
- `r2_make_svg.py`       — renders `../fig_r2_agecurve.svg`.
- `r3_recency_charge.py` — R3 recency-decay charge vs truth; under/over/right.      → `out_r3.txt`
- `r4_phantom_boards.py` — R4 four phantom boards + games-weight sensitivity.       → `out_r4.txt`
- `out_r*.txt`           — captured runs (the figures cited in D2_RECUT.md / RETURN.md).

R5 (LTI register) is a code/doc trace, not a run — see D2_RECUT.md.
