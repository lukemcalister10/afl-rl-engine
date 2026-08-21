"""acceptance/checks — the registered checks, in execution order.

REGISTRATION ORDER IS EXECUTION ORDER, and it is load-bearing: a check that can halt a carrier MUST
be registered before every check that reads it, or the downstream check runs first and produces the
duplicate red the whole contract exists to prevent. `runner.validate_registry()` asserts this and
refuses to run a registry that violates it, so the ordering below is checked, not merely intended.

WHAT IS IN SCOPE FOR THIS TRANCHE. Every check here is CHEAP — file reads, hashes, and the existing
standing gates that already run in seconds. Nothing here builds a board, seeds the shared workspace,
or imports the engine. That is deliberate: the spine has to be runnable often enough that people
actually run it. The expensive legs (Guard 4's correction canary, the twice-build determinism leg,
the frozen acceptance suite) hang off this trunk in a later tranche, not in it.

WHAT IS DELIBERATELY NOT HERE. The seven UI-seam suites and the two Track B suites that the audit
measured red are not registered yet. They are red for R1/R2 carrier reasons the manifest check
already reports once, and registering them before the widened manifest check had proven itself
would have produced exactly the wall of restatements this order was commissioned to end. They are
the natural second tranche, and they will arrive already wired to carriers, which is the point.
"""

from acceptance import contract as C

from acceptance.checks import manifest as _manifest
from acceptance.checks import standing as _standing


# 1. THE TRUNK. The widened coherence gate — the furthest-upstream check in the estate, and the one
#    that can halt carriers everything else reads. AUDIT_CI.md §5/BUILD FRESH item 1: "the widened
#    coherence gate above. First build, everything else hangs off it."
C.register('release_manifest', _manifest.check,
           reads=(),
           doc='All 11 identities agree across all 43 carrier fields in 8 files')

# 2. Guard 5 checkout legs. The audit calls this "the strongest thing in the estate" and
#    "COVERED — non-vacuous on every leg I probed". It anchors on expected_boot, so it reads those
#    carriers; if the manifest check found expected_boot drifted, this is BLOCKED, not re-failed.
C.register('boot_guard_checkout', _standing.boot_guard_checkout,
           reads=('expected_boot:store', 'expected_boot:engine_head', 'expected_boot:register'),
           doc='Guard 5 checkout legs: store / engine_head / register == pinned boot identity')

# 3. The config manifest hash matches its pin and its stored value.
C.register('config_manifest', _standing.config_manifest,
           reads=('expected_boot:config',),
           doc='manifest hash == pinned boot config == stored config_sha256')

# 4. The ruled dial postures, asserted STRUCTURALLY (source default + live env + manifest pin).
#    The audit names this file's form as the right template for the whole dial layer.
C.register('ruling_config', _standing.ruling_config,
           reads=(),
           doc='RL_PVCFIT=0 default + R3 export bake-guard + RL_LTI_CLOCK=advance, structurally')

# 5. The release seal. Reads exactly the four carriers R2 halted — so on a tree carrying R2 this is
#    BLOCKED and says so once, instead of restating the same four stale pins a second time.
C.register('release_contract_seal', _standing.release_contract_seal,
           reads=('release_contract:engine_head', 'release_contract:rl_model',
                  'release_contract:fv', 'release_contract:config'),
           doc='release_contract.py check — the stamped release-state seal')

# 6. The original six-way STORE coherence, kept as its own row. It reads only the STORE carriers, so
#    R2's drift in engine_head/rl_model/fv/config in the SAME FILE does not block it — that carrier
#    precision is the point of naming carriers <file>:<identity> rather than per file.
C.register('store_coherence_six_way', _standing.store_coherence_six_way,
           reads=('expected_boot:store', 'release_contract:store', 'season_state:store',
                  'board_sidecar:store', 'ui_bundle.stamp:store'),
           doc='the original six-carrier store check, retained as its own verdict row')

# 7. Documentation lint. Unwired in every workflow today (AUDIT_CI.md gap G9).
C.register('doc_lint', _standing.doc_lint,
           reads=(),
           doc='doc_lint.py — live/history doc consistency (gap G9: wired nowhere before now)')

# --------------------------------------------------------------------------------------------------
# PACKAGE 1 ADDITIONS (PLAN_v6, 2026-08-20). Seven new rows: 1a's two instruments and 1f's five
# M1a-residue checks. Registration order still equals execution order, and none of these halts a
# carrier, so they are all safe below the trunk.

from acceptance.checks import ledger as _ledger                              # noqa: E402
from acceptance.checks import m1a as _m1a                                    # noqa: E402

# 8. THE RULEBOOK LINT (1a). A NEW instrument — doc_lint would false-red on the RULEBOOK's own
#    prose, so it was never pointed at it. Consults the ruled-red ledger's STEP half.
C.register('rulebook_lint', _standing.rulebook_lint,
           reads=(),
           doc='tools/rulebook_lint.py — laws numbered, counted, and no second laws file')

# 9. THE LEDGER'S OWN LIVENESS (1a + REVIEW_COLD_OPUS O1). Every step-keyed ruled-red entry is
#    re-probed; an entry whose step stopped failing FAILS the run instead of ageing quietly.
C.register('ruled_red_ledger', _ledger.check,
           reads=(),
           doc='every step-keyed RULED-RED entry still fails the way its ruling records')

# 10. THE OWNER-INPUTS PROVENANCE ARCHIVE (1d), generated and asserted current.
C.register('inbox_manifest', _standing.inbox_manifest,
           reads=(),
           doc='docs/inputs/incoming/MANIFEST.md is current, and every input names its canonical copy')

# 11-15. THE M1a RESIDUE, cheap legs (1f).
C.register('mirror_parity', _m1a.mirror_parity,
           reads=(),
           doc='boot_guard\'s fitted-artifact resolvers mirror the engine; q97m/v0surf/cm == pins')

C.register('dial_coverage', _m1a.dial_coverage,
           reads=(),
           doc='every declared dial is read with a default in engine source')

C.register('oneliner_gamma', _m1a.oneliner_gamma,
           reads=(),
           doc='M1a repair 1 — ship_gates_check model env == the pinned manifest')

C.register('oneliner_r14_restore', _m1a.oneliner_r14_restore,
           reads=(),
           doc='M1a repair 3 — the R14 disposable fixture verifies (the real suite, run)')

C.register('oneliner_f1_lens', _m1a.oneliner_f1_lens,
           reads=(),
           doc='M1a repair 4 — the F1 export-parity leg is repaired, not removed')

# 16. THE HEAVY LEG (1f). Two bare builds, byte-identical. ~3.5 minutes; excluded from
#     --profile host-insensitive, which is what every push runs.
C.register('build_twice_determinism', _m1a.build_twice_determinism,
           reads=(),
           doc='two bare builds of this tree produce byte-identical boards')

# --------------------------------------------------------------------------------------------------
# PACKAGE 2a ADDITION (PLAN_v6, 2026-08-20). One row: the landing library's own self-test.
# Registered rather than left as a landing-time script because it is fast (measured 10.5s) and runs
# no build — the brief's own test. It halts no carrier, so it sits at the bottom of the registry.

from acceptance.checks import landing as _landing                            # noqa: E402

# 17. THE LANDER SELF-TEST (2a.3). Every step of the landing transaction broken once in a sandbox,
#     every abort proved byte-exact, the claims negative control fired. PROFILE='full', so the
#     per-push host-insensitive lane does not pay for a git worktree.
C.register('lander_selftest', _landing.lander_selftest,
           reads=(),
           doc='the landing library\'s self-test: every step broken once, every abort byte-exact')

# --------------------------------------------------------------------------------------------------
# 3b ADDITION (the register act, 2026-08-21). One row, sub-second, no build: the frozen register's
# byte seal + new-form well-formedness (pen.py verify) and the generated incident index's currency
# (incident_index check — the READERS_3B defect-1 gap). Halts no carrier; sits at the bottom.

# 18. THE REGISTER FORM.
C.register('register_form', _standing.register_form,
           reads=(),
           doc='frozen register seal + new-form entries valid + incident index current')

# --------------------------------------------------------------------------------------------------
# 3c ADDITION (the state file, 2026-08-21). One row, sub-second, no build: the machine-written
# docs/STATE.md is regenerated from the carriers and compared byte-for-byte with what is committed.
# It is the falsifier the retired predecessor never had — docs/CURRENT_STATE.md carried an authority
# banner, had a named writer, and still sat 156 register versions stale. Halts no carrier.

# 19. THE STATE FILE'S FRESHNESS.
C.register('state_file', _standing.state_file,
           reads=(),
           doc='docs/STATE.md is a byte-exact regeneration of this tree (generated-only, P6)')
