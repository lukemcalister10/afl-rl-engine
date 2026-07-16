# How to update the LTI & availability register (no agent, no LLM)

This is the owner's update path for the injury/availability ground truth in `LTI_REGISTER.md`. It is
deterministic: a machine reads the file you edited, checks it, and either **moves the one pin** that tracks
it — or **refuses and tells you exactly why**. No model is in the loop. Same shape as
`ui/HOW_TO_UPDATE_INPUTS.md`: validate-or-HALT, nothing guessed.

## What you edit

One authored file, the register itself:

| File | You change | You never change |
|---|---|---|
| `LTI_REGISTER.md` | the pipe-table rows (add/remove an injury window, flip a `status`, correct a `designation`) | the `key` column — it is the store join key ("Key by ID, never name"); the schema/header prose |

The register is a **PINNED INPUT** (R-REG=R2): its md5 lives in `data/expected_boot.json` under `register`,
and Guard 5 asserts it on boot. Editing the file without moving that pin HALTs the next build. This tool
moves the pin — **and only that pin**.

## The two steps

1. **Edit** `LTI_REGISTER.md` on your machine (or via the GitHub web UI). Keep the same file name.
2. **Re-pin.** Run the one deterministic command:
   ```
   python3 tools/owner/lti_repin.py
   ```
   It validates the edited register, then rewrites **only** `data/expected_boot.json`'s `register` md5 to
   match. It prints the entry diff (added / removed / changed rows), the old → new md5, and the reminder to
   **rebuild the board to consume this**. Exit `0` = re-pinned (or already pinned); exit `2` = it refused.

The tool **never writes the store** (it reads `engine/rl_after/rl_model_data.json` report-only to resolve
names) and **never moves any pin but `register`**. Commit the edited register and the moved pin **together**
(one curation edit — not a store bake). It does **not** rebuild the board; that is a separate engine step.

## Validate-or-HALT: why it might refuse (exit 2)

It stops at the first failure and writes nothing. What each refusal means:

| Refusal | What went wrong | Fix |
|---|---|---|
| **register table did not parse** | a row has the wrong column count, or `window_id` isn't an integer | fix the named line to the 8-column schema |
| **unknown register key … is not in the store** | a row's `key` doesn't resolve to a store player | correct the key so it matches a store `key` |
| **section must be A\|B** / **designation … not in** / **status … not in** | a value is outside the known vocab | use `A`/`B`; designation ∈ {2025, 2026_preseason, 2026}; status ∈ {out_until_2027, may_return_2026, returned} |
| **window_ids must be 1..n contiguous** | a repeat-LTI key skips a window number | number the windows 1, 2, … per key |
| **status 'returned' but returned_year is blank** / **returned_year … set but status is …** | the return date and status disagree | set `returned_year` (a sane 4-digit year) iff `status` is `returned`, blank otherwise |
| **expected_boot.json changed OUTSIDE the register pin** | another pin (store/board/config/…) differs from HEAD | this tool moves only `register` — revert the other pin, or take it through a bake |

A clean run ends by naming the old → new register md5 and printing `NEXT: rebuild the board to consume this`.
Re-running with no further edit is a no-op (`PIN UNCHANGED`, exit 0) — the command is idempotent.

*This tool never re-diagnoses a row (the register is owner ground truth; store anomalies are report-only,
the register governs) and never prices anything. It validates, moves one pin, and reports.*
