# PACKAGE 2b — THE ROUND LANDER: THE DRY-RUN DECLARATION

**Written and committed BEFORE the dry run is executed.** This act touches no engine file, so process
law P9's prereg is not owed in its full form; the declaration is written anyway, in P9's shape,
because the dry run is the proof this package ships and a proof whose predictions were written
afterwards proves nothing. **The declaration is corrected against the tree, never the tree against
the declaration.**

## WHAT THE DRY RUN IS

`tools/land round --spec ACT_SPEC_DRYRUN.json --dry-run` against the live tree, with the spec
declaring a **REHEARSAL**: `prereg.board_before == prereg.board_after`, `identities.moves` empty,
`round.scores` null, `sheet` null, `day0_rebase` off.

It is the same proof the lever lander gave before its first real flight, in the same shape: the whole
fourteen-step sequence executes, nothing is armed, nothing is applied, and the standing falsifier is
that **no carrier moves**.

**NO REAL ROUND IS LANDED BY THIS ACT.** Round 24's scores do not exist. The deliverable is the
proven machine.

## THE PREDICTIONS, AND THEIR FALSIFIERS

| # | prediction | falsifier |
|---|---|---|
| P1 | the board of record `data/rl_build/rl_app_data.json` is **`b3e8da99bc7f632e5d1eebc732f9cf01`** before the dry run and **byte-identical** after | any other md5 after |
| P2 | the store `engine/rl_after/rl_model_data.json` is **`b745002eb0a0fbb1c34fa44f1ef708d6`** and byte-identical after | any other md5 after |
| P3 | **ZERO** of the round lander's 33 declared carriers move across the dry run — the parent measures them itself, before and after, path by path | one carrier moved |
| P4 | `as_of_round` stays **23** in `data/expected_boot.json`, `data/season_state.json` and `data/release_contract.json` | any of the three moves |
| P5 | `engine_head` stays **`3af8c1f7d61275c198a5df70c34608c7`** — this act edits tooling and documentation only | engine_head moves |
| P6 | `data/sheet_pins.json`'s three pinned facts stay **`21361291f26d35108b88f92f885c5063` / 219 / 35** | any of the three moves |
| P7 | every step of `ROUND_SEQUENCE` runs and reports OK; the transaction reaches `commit`, which commits nothing because nothing was written | an aborted dry run, or a step skipped |
| P8 | the pre-transaction self-test runs standalone first and PASSES, including all seven round faults broken / caught / aborted byte-exact | any self-test failure — no transaction opens |
| P9 | the gate step runs the **standard landing gate set** (`steps.DEFAULT_GATES`, acceptance runner under `--profile in-transaction`) and every gate passes | any gate red |

## WHAT IS ALLOWED TO MOVE IN THIS ACT AS A WHOLE (G1 enumeration)

The dry run itself writes **nothing but evidence**. The act's commits carry, and nothing else:

* `tools/landing/{spec,steps,txn,carriers,cli,selftest}.py` — the library gains the round act type.
* `tools/land` — unchanged (it is a shim; the verb is inside the library).
* `release_manifest_check.py`, `acceptance/checks/manifest.py`, `acceptance/checks/__init__.py` —
  the sheet's three facts become manifest-checked carrier fields (40 → 43 fields, 8 → 11 identities,
  7 → 8 files).
* `data/sheet_pins.json` — **PROSE ONLY**: the `_writer_of_record` header records that 2b landed and
  a `_manifest_checked` header is added. **The three pinned facts and `sheet_path`, `pinned_at`,
  `provenance` are byte-unchanged.** The pin file is G1's named allowed churn since 3a; the values it
  pins are not touched by this act at all.
* `docs/runbooks/R23_RUNBOOK.md` — `ERRATUM E8`.
* `docs/evidence/p2b_round_lander_2026-08-21/*` — this packet.

**`docs/OPEN_ITEMS_REGISTER.md` and `docs/register/` are NOT touched.** That pen is the supervisor's.

## THE ONE PREDICTION THIS DECLARATION MAKES ABOUT THE FUTURE

The round lander is **unflown**. Its first real flight is round 24, under the soak rule (PLAN_v6
2a.4): supervisor hand-verification runs ALONGSIDE it, and stands down for this act type only on the
owner's word. The manual path in the R23 runbook §3 is the fallback and stays written down, because
an unexercised fallback is fake safety.
