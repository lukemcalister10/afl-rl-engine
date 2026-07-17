# DIRECTIVE — LEG-D/E GROUNDWORK (read-only; design evidence, input verification, acceptance harness)
2026-07-17 · supervisor seat 11 · Opus · ONE JOB, ONE CHAT (S2) · runs IN PARALLEL with the R106.7 writer (S3)
STATUS: ISSUED — fire when pasted by the owner.

## ⛔ EXECUTE FIRST — BEFORE READING FURTHER (commit output as FIRST_COMMANDS_PROOF.txt, your first commit)
```
git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/claude/legc-relay-dpp-law-10c4z7
#   MUST print 6306378691d178551a7f8a461c73811f7a29df4e — else HALT.
git fetch origin claude/legc-relay-dpp-law-10c4z7
git checkout -B claude/legd-groundwork 6306378691d178551a7f8a461c73811f7a29df4e
git merge-base --is-ancestor 6306378691d178551a7f8a461c73811f7a29df4e HEAD && echo ANCESTOR-PROOF-PASS
md5sum engine/rl_after/rl_model_data.json   # MUST begin 0efdc5d6 — else HALT.
```
You are READ-ONLY on everything outside `session_2026-07-17/legd_groundwork/`. You never touch the store,
the engine, docs/, or tools/. NOTE: player VALUES on this base will move again (R106.7 in flight) — your
work must not depend on exact current values; it is design evidence and data verification, never a fit.

## THE FIVE
EFFORT: High (the evidence base for the chapter's biggest remaining build; why not Extra: no design
decisions are yours — evidence only). MODE: auto; PLAN first commit after the proof. TIME: 2–4 h.
FEED: docs/NOTE_seat8_legD_circularity_survivorship_2026-07-16.md (hypotheses, NOT rulings) ·
docs/AUDIT_gpt_spec_findings_2026-07-16.md (Surface 7/8) · DECISIONS v121 · CONSTRAINTS v1.18 +
acceptance_v1_20.json (the G-Y0 entry; ⚠ its fix_direction field is STALE — never apply it) · the
register greps you need (R104.5 · R104.7 · R104.9 · the 2026-07-11 pick-correction items).
FENCE: writes ONLY inside session_2026-07-17/legd_groundwork/. Everything else read-only.

## THE JOBS (evidence, with script-emitted numbers — never typed counts; propose options, decide nothing)
1. **DERIVATION WINDOW, FROM THE CODE:** how does the CURRENT tree define a draftee's delivered
   value (entry vs end-of-year-1 vs other)? Name files:lines. The owner's correction (end-of-y1
   evidence; distinct from the G-Y0 day-after identity) is the hypothesis to verify, not assume.
2. **CIRCULARITY, QUANTIFIED:** per pick band, how many entrants are priced ≥ (50/75/90)% by their
   (position-adjusted) pick prior vs demonstrated evidence — the zero-evidence tautology's real
   size. Emit the table (JSON+md). Propose 2–3 principled CUT OPTIONS with the rows each would
   exclude (counts + names at the margin) — options for the construction memo, not a choice.
3. **SURVIVORSHIP, MAPPED:** who exits the sample when (delistings/retirements per band per year in
   the data); what the current data does with them; where a naive per-band mean would bias and in
   which direction. Emit the exit table.
4. **INPUT VERIFICATION (the owner's bug-class argument):** (a) national_draft_last_pick.json vs
   the store's own per-year National max — every year, every mismatch named; (b) the pickless
   pathways' _eff derivation — current values, their provenance stamps, and whether the flex-era
   store changes any input to them; (c) per-band sample counts at the finest resolution the sample
   supports (smoothed presentation per CORE rule 7 — no wide-bin single numbers).
5. **ACCEPTANCE HARNESS, ASSEMBLED (draft — the seal is the supervisor's pen, never yours):** the
   machine-checkable draft list the new curve must pass: R104.9 strict descent (formal statement:
   every pick n value > n+1, no plateaus unless owner-ruled) · the G-Y0 identity as the acceptance
   JSON constructs it · R104.5 per-posture discounts 10/15/5. One JSON draft + one md explainer.
6. **LEG-E RIDER (inventory only):** the posture rulings verbatim (register-grepped) · the Rozee
   case state (what the register/docs carry) · where postures live in the code TODAY (files:lines
   or "nowhere") · open questions for the Leg-E memo.

## RETURN
≤30 lines · branch + head SHA + PR · the memo `GROUNDWORK_LEGD.md` + per-job JSON artifacts ·
"in plain terms" close · actual time. SILENCE IS A RED: every table your memo cites exists as a
committed artifact its numbers were emitted into by the script that computed them.
