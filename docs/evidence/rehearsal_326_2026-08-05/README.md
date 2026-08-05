# #326 rehearsal evidence — HALTED, nothing landed · 2026-08-05

The #326 per-division pool-levels directive was fired on the owner's slot word and rehearsed end-to-end
on a working copy cut from main tip a6f6076. The rehearsal HALTED on two findings (HALT_AND_ASK.md):

1. The consumption site the audited directive names (rl_model.value's unpl_eq/pedestal) is not on the
   board's price path — rl_export overwrites every exported value from the engine's gated ev(), which
   never calls value(). With all 14 levels installed and resolving correctly, ZERO of 804 board prices
   move. Verified independently by the seam: the rehearsed board differs from the pre-change board in no
   field of any row (order of the active array only).
2. pool_value still sets 12 board prices (all rucks) through draftval -> the ruck prior cap in
   _merged_recover.py — the site the pre-fire audit classified as scaffold.

Both point at the same decision: whether the division lookup belongs in _merged_recover.py (the pinned
engine head) — a larger act than #326 scopes, owed its own directive addendum and fresh audit. The
rehearsal implementation is preserved verbatim in rehearsal_326.patch (base a6f6076); the selftest
additions were left RED on the reach-the-price checks rather than weakened.

Gate outputs in this directory; re-run recipe in RUN_COMMANDS.md. The audit trail is issue #326.
