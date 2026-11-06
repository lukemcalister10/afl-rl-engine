# P5-4 — The six reads the hard-wiring left (MEDIUM)

**Goal.** Remove the last environment reads in the engine: RL_UNCOMP_S, RL_LSYM_TAB, RL_V0SURF_REFIT (declared
`must_be_unset` in data/release_contract.json and release_contract.py:47 — delete the reads AND the contract
clause together, re-seal the contract) and RL_LENS_BASIS, RL_LANE_EXPECT, RL_V0_LENS (read only inside the
v0-surface refit lane behind RL_V0SURF_REFIT). The refit lane itself (`_merged_recover.py` ~2292–2541, the
fit-from-scratch path, and session_2026-07-18/legf6/scripts/refit_v0surf.py) moves out of the engine into
tools/refit_v0surf.py, which produces data/v0surf.pkl offline; the engine only LOADS the pinned pickle (it
already halts on a signature mismatch).

**Why.** After D3 these are the only switches left; a refit lane inside the pricing file is the last place a
"dev shell" can change a board.

**Rules.** Board byte-identical (the refit lane never runs in a landed build). The frozen v0-surface signature
(`_V0SURF_GATES` md5) must not change — RL_DAMP_K and the other signature constituents stay as literals in the
signature input exactly as the hard-wiring left them. release_contract.py's `DEFAULT_MUST_UNSET` emptied and
the contract re-sealed in the same act (contract identity moves: declare it).

**Proof.** Bare build byte-identical; `python3 release_contract.py check`; config_manifest tests; acceptance green.

**Lands via.** Lever act; engine_head and contract move (flip or P4-3).
