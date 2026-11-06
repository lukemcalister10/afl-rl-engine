# The plan briefs — Phases 2 to 5 (owner word 2026-11-06: "Yes, please proceed with that plan.")

One brief per item: **Done when**, **Facts** (file:line read at ffb2663b — re-read, lines drift), **Change**, **Must
not change**, **Prove it**, **Lands via**. The 2026 season is over (season_state.json as_of_round 24, calendar_progress
1.0; movers.js reports 15–29, GF included). Next: the draft, then the rollover, then 2027 Round 1.
## The common contract
- **Serial rule.** One item at a time in `tools/landing/steps.py`, `tools/ingest.py` and the engine
  (`engine/rl_after/_merged_recover.py`, `rl_model.py`, `rl_export.py`, `engine/forward_valuation/`).
  P2-1, P2-2, P2-3, P2-4, P4-1a, P4-2, P4-3, P4-4 and P5-3 all edit steps.py.
- **Lanes.** A change that moves the board, the store or a pinned identity lands through `tools/land`
  (lever / edit) or `tools/ingest`. Until P4-3 lands, an engine or config source change needs the flip:
  edit the pins in data/expected_boot.json, `python3 tools/restamp.py apply`, commit, then land with those
  identities in `unmoved` (tools/landing/spec.py:65 refuses engine_head/rl_model/fv/config/v0surf in `moves`).
  After P4-3, declare them in `moves`. Anything else is a plain commit after its tests.
- **Gates.** The lander runs DEFAULT_GATES (steps.py:139-185), with acceptance at `--profile in-transaction`
  (:144-147). CI runs `python3 -m acceptance.selftest` and `--profile host-insensitive`
  (.github/actions/host-insensitive-gates/action.yml:72-73). Neither profile runs `lander_selftest`
  (PROFILE 'full', acceptance/checks/landing.py:71); `tools/land lever|round|edit` runs tools/landing/selftest.py
  before its transaction (cli.py:231,293,335) unless a standing proof exists, but tools/ingest drives the steps
  WITHOUT it (ingest.py:450-463; RULEBOOK P14 "no lander self-test"). P2-1 uses tools/ingest; P2-3's tools/player
  uses `tools/land edit` (self-test runs). "Acceptance green" = `--profile full` (plain commit) / the lander's gates.
- **Byte-identical board.** Pin `96896e1c…` = md5 data/rl_build/rl_app_data.json. Bare build as the lander builds it
  (mode 'dev', steps.py:1114): `python3 tools/landing/_build_child.py $PWD <tag> dev <scratch>/b '{}'`, md5
  `<scratch>/b.board.json`. For an act, build_proofs against `prereg.board_after` is the binding proof.
- **Spec baseline.** 29 `ACT_SPEC*.json` under docs/evidence; 28 validate; p3a_pins_out_2026-08-21/ACT_SPEC_P3A.json
  already fails (engine_head in `moves`). "Every spec validates" = the same 28 (say if P3A passes after P4-3).
- **Config rule (corrects "the engine has no env flags since 2026-10-14", which was false).** Distinct RL_* names
  read in code: 66 in _merged_recover.py (69 if you count three named only in "Was os.environ.get" comments at
  :216, :1161, :1162), 20 in rl_model.py, 7 in rl_export.py, 5 in conditional_prior.py. All but six are either
  manifest dials in data/model_config.json `vars` (90 entries) or config_manifest.INFRA_ALLOW (config_manifest.py:50);
  in gate/canonical mode any other RL_/PAR_ var halts the build (config_manifest.py:121-128). The D3 act
  (dd7cad24) hard-wired the adopted chain; it did not remove the pinned dials. RULE: no new UNPINNED switch;
  manifest dials stay — they ARE the config identity. The unpinned reads (six in these four files, eleven in all build-loaded files) are P5-4's. A measurement variant
  is a module constant flipped on a scratch copy, never shipped.
- **Owner word.** Value-moving releases (law 11 blind review, RULEBOOK P1 movers shown first): P5-3, P3-2, P5-5,
  P5-6. RULEBOOK edits (law 10a): P4-4 (P13 names the round lander as the sheet-pin writer). A new step on the
  weekly path (P14, RULEBOOK.md:173: "No session adds a step to this path without the owner's signed word"):
  P2-1. A history rewrite: P4-1b. Everything else is the owner-accepted plan.
## Order
| # | brief | tier | depends on | lands via |
|---|---|---|---|---|
| 1 | P2-2 movers single writer | LOW | — | plain commit, bundle byte-identical |
| 2 | P4-1a hard-fail the two retro exists-guards (in P4-1) | LOW | — | plain commit (~10 lines) |
| 3 | P4-2 retired tooling (re-scoped) | LOW | P4-1a | plain commits, one per unit |
| 4 | P4-3 flip inside the lander (+stash key, +config) | MEDIUM | P4-2 | plain commit + rehearsal act |
| 5 | P5-2 engine file end | MEDIUM | P4-3 | lever act, board unmoved |
| 6 | P5-1 one ev | MEDIUM | P5-2 | lever act, board unmoved |
| 7 | P5-4 unpinned reads in the build + refit lane | MEDIUM | P5-1 | lever act, board unmoved |
| 8 | P5-3 as-at −1/−2 columns (a value move) | HIGH | P4-3 | lever act, owner word, blind review |
| 9 | P2-3 store row verbs + tools/player | MEDIUM | P4-2 | plain commit + rehearsal |
| 10 | P2-4 season-keyed ids | MEDIUM | P2-2 | plain commit (one data migration) |
| 11 | P3-1 one live season | MEDIUM | P4-3, P5-4 | lever act, board unmoved |
| 12 | P3-2 rollover (AFTER THE DRAFT) | HIGH | P3-1, P2-3, P2-4, P5-3, P4-3 | edit act, owner word |
| 13 | P2-1 rounds on ingest (BEFORE 2027 R1) | MEDIUM | P3-1, P2-4, P3-2 | plain commit + rehearsal, owner word |
| 14 | P4-4 retire the round lane (after a real 2027 round) | MEDIUM | P2-1 + one landed 2027 round | plain commits, owner word |
| 15 | P4-1b archive branch / history rewrite (in P4-1) | LOW | owner decision; P4-4 | owner word |
| 16 | P5-5 veteran damper | HIGH | P5-4 | lever act, owner word, blind review |
| 17 | P5-6 grid-surface smoothing | HIGH | P4-3, P5-5 | lever act, owner word, blind review |
| 18 | P4-5 stale-docs sweep | LOW | all others | plain commit, last |
