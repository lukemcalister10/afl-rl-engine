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

from acceptance.checks import standing as _standing


# NOTE (this commit): the TRUNK check — the widened release-manifest coherence gate — lands in the
# NEXT commit and registers itself at position 1, ahead of everything below. The carriers named in
# the `reads=` clauses here are therefore inert for one commit: nothing halts them yet, so nothing
# is BLOCKED yet. They are declared now rather than retrofitted later because a `reads=` clause
# added after the fact is a clause somebody has to remember, and the audit's estate is full of
# instruments that were never wired because wiring them was a separate job.

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
