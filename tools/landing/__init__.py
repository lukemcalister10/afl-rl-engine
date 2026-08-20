"""tools/landing — THE LANDING-TRANSACTION LIBRARY (PLAN_v6, PACKAGE 2a).

ONE LIBRARY, TWO ENTRY POINTS. `land lever` is built here. `land round` (PACKAGE 2b, after 3a) is
the SECOND thin entry point over this same library — not a second script. The plan says why in one
line: "mirrored script pairs drift; the repo's loader/emitter history proves it" (2a.1). The estate
carries seventeen emitter forks as the standing evidence for that sentence, so the round lander gets
a step list and a spec type in THIS package's modules, never a copy of them.

WHAT THIS LIBRARY IS, HONESTLY: it is a CONSOLIDATION, not an invention. Three landings walked the
identical sequence by hand on 2026-08-20 —

    docs/evidence/d8_adoption_2026-08-20/      the D8 adoption
    docs/evidence/backrows_reseal_2026-08-20/  the back-rows repair + reseal
    docs/evidence/f5_and_sort_2026-08-20/      the F5 rounding act

— each writing its own `land_*_pins.py`, `land_*_contract.py`, `land_*_ui.py`,
`append_*_transition.py` and `register_*_column.py`, each adapted from the last, each carrying a
docstring explaining which assertion it re-pointed and which one it must NOT copy. Those five
scripts per act are the specification of this library and its steps call the SAME writers of record
they called: `ui/tools/extract_board_view.py`, `round_movers.inject_release_contract`,
`release_contract.restamp_dynamic`, `sibling_repin`, `out_of_round_column.add_column`. Nothing here
reimplements a writer. Where a per-act script hard-coded a constant (this act's board, this act's
must-not-move list, this act's column label), the constant moves into an ACT SPEC file — which is
the whole of the difference between a landing that is scripted and a landing that is programmed.

THE MODULES

    carriers.py   the enumerated carrier set + Snapshot: capture, restore, verify-byte-exact.
                  This is the abort ladder's foundation (2a.3).
    spec.py       the act spec — fixed slots, validated before anything runs.
    steps.py      the ten steps, in the day's proven order.
    txn.py        the driver: fail-closed sequencing, per-step timing, the abort path, claims.
    packet.py     the decision-packet template + slot validator (2a.2).
    selftest.py   the sandbox self-test (2a.3): every step broken once, every abort proved.
    cli.py        `land lever` — and where `land round` will attach.

THE ONE RULE THAT GOVERNS EVERY STEP: FAIL-CLOSED. A step that cannot prove its own postcondition
raises. The driver aborts, restores every carrier to the identity captured at step 0, asserts the
restoration BYTE-EXACT, and names the step that failed. There is no "continue anyway" path and no
flag that creates one.
"""

__all__ = ('carriers', 'spec', 'steps', 'txn', 'packet', 'selftest')
