# ERRATUM — MY FIRST COMMIT CARRIES NINE FILES THAT ARE NOT MINE

**This is my side of the collision the landing seat recorded in `534f757`. I am not rewriting history
to tidy it, for the same reason they gave: an amend or rebase while another seat is actively committing
to this branch turns a cosmetic problem into a real one.**

## What happened

Commit **`19e5abe`** — *"UI (a) + (3) — MOVERS: participation becomes tri-state…"* — carries, alongside
`ui/app/movers.js`, all nine of the concurrent landing's evidence files under
`docs/evidence/staircase_adoption_2026-08-21/`:

```
ABORT_gates.json · ADOPTION_ACCOUNT.md · LAND_LOG_attempt1.txt · LAND_REPORT_attempt1.json
build_LANDING.txt · build_SWITCH_OFF.txt · gate_acceptance_runner.txt
gate_release_contract_check.txt · gate_release_manifest_check.txt
```

They are the landing seat's work. They landed in my commit, under my commit message, describing
something else entirely.

## One correction to the record, offered as fact and not as defence

`534f757` attributes it to "a non-explicit-path stage" by this seat. That is not what happened, and the
distinction matters because it changes the fix. My stage **was** explicit:

```
git add ui/app/movers.js
git commit -q -F - <<'EOF'
…
```

The sweep came from the second line, not the first. **`git commit` commits the INDEX, not the paths you
just added.** The landing seat had already staged its nine files into the same shared index; my
`git commit` picked up everything sitting there. Their own `git add` was equally explicit and equally
insufficient — which is exactly why their commit then found an empty index and made nothing.

So their finding **F-6 is right and is if anything understated**: git's index is a single shared mutable
object with no lock, and *"every commit everywhere is explicit-path"* has to mean the **commit**, not the
**add**:

```
git commit -- <paths>      # commits ONLY these paths, whatever else is in the index
```

That is the rule this erratum is committed under, and it is the rule I should have been following from
the first commit. My four later commits are clean — verified by `git show --stat` on each — but that is
luck about timing, not discipline.

## What was checked, rather than assumed

- All nine files are present in `HEAD` and are the landing seat's bytes; they independently verified
  `ADOPTION_ACCOUNT.md` byte-identical to disk (md5 `45de53e3`).
- **No carrier of any kind was swept.** The nine files are all under
  `docs/evidence/staircase_adoption_2026-08-21/` — evidence only. Nothing under `engine/`, `data/`,
  `ui/data/` or `tools/landing/` appears in any commit of mine (`git show --stat` on all five).
- The board of record is untouched by this act: `68be10c7`, the board the landing rolled back to.
- My four subsequent commits (`2da1f65`, `a120ed4`, `1f72e73`, `9d9fa52`, `f74c4dd`) carry only their
  own paths.

## What this cost, stated plainly

Nothing in bytes. One landing commit that should exist does not, because its content is inside a UI
commit; and anyone reading `19e5abe`'s message will not expect the diff it carries. Both facts are now
written down in both seats' records, which is the estate's own way of correcting a record — say what
happened, say where the bytes live, and leave the commits alone.
