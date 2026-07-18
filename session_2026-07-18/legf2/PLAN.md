# LEG F2 — PLAN: recorded history the store carries for 2024/2025 list membership + evidence

Store md5 `968de0c7` · engine `6ad07bb2` · rl_model `cc626d7d` · curve payload `89c14729` · code `240c737`

## Records available per store row (n=2652 valuable rows, pos in GRP)
- `year` present: 2652/2652
- `_last_listed` present: 13/2652
- `_retired` present: 2652/2652
- `scoring` present: 1909/2652
- `_bd` present: 848/2652
- `pick` present: 2369/2652
- `type` present: 2652/2652
- `afl_club` present: 804/2652

## Board -1 (as-of end 2025): list membership = 772 players
- with in-window played evidence (scoring year<=2025, games>=1): 689
- unplayed prospects (priced by pedigree/pedestal V0): 83 (of which pickless: 18)
- members missing birthdate `_bd` (age falls back — engine handles): 86
- **engine priced every member: 772/772 OK, 0 FAIL**

## Board -2 (as-of end 2024): list membership = 777 players
- with in-window played evidence (scoring year<=2024, games>=1): 671
- unplayed prospects (priced by pedigree/pedestal V0): 106 (of which pickless: 23)
- members missing birthdate `_bd` (age falls back — engine handles): 189
- **engine priced every member: 777/777 OK, 0 FAIL**

## GAP VERDICT
**NO GAP** — the engine produced a finite as-of value for every on-board member of both the 2024 and 2025 lists. Membership is read from `_last_listed`/debut/last-game (as recorded); evidence is the per-season scoring truncated to <=Y. Nothing reconstructed by guess.
