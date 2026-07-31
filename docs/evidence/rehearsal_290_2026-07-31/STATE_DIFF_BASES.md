# STATE-DIFF BASES — the index for the new clause

**#290, 2026-07-31.** Filed by the incoming execution seat as ruled opening act (1)
(seam go and audit: [#290 issuecomment-5143115766](https://github.com/lukemcalister10/afl-rl-engine/issues/290#issuecomment-5143115766)).

## The clause

> **A state diff names its base commit beside itself.**

Entered the standing law at register v553, after the seam's round-trip re-run caught an unnamed
diff base that the filing's own proof had missed.

## Why it is a law and not a nicety

A base is **free to record when the diff is cut** and **impossible to recover afterwards.**

The instrument beside this file (`state_diff_base_probe.py`) tests a candidate base from the diff's
own `index <pre>..<post>` lines, without applying anything. What it returns is an **interval**, never
a point — every commit that did not touch the diff's targets is indistinguishable from every other:

| diff | targets | admissible bases | recoverable? |
|---|---|---|---|
| `L3_T1_applied/L3_T1_state.diff` | 18 | **6** — `3d253c6` … `79ee8e5` | narrowed, then decided by provenance |
| `L1_amended/L1_amended_state.diff` | 17 | **25** on the carrier line; **8 of 8** on the rehearsal line | **no** |

The second row is the argument. Nothing on the #290 line touches a product file, so every one of
that diff's targets is byte-identical at every commit, and the probe rejects nothing at all.

**Measurement narrows. Provenance decides. Recording is the only thing that works.**

## The two artifacts

| | base | state |
|---|---|---|
| `L3_T1_state.diff` | **`79ee8e5`**, on the **#290 carrier** | **PROVEN** — full apply at base reproduces `data/v0surf.pkl` = `84fb0cde` byte-exact |
| `L1_amended_state.diff` | **UNRESOLVED** | inferred `106adf4`/`62cdd00`-pre-commit; the two are the same tree for all 17 targets and nothing distinguishes them |

Each carries its own annotation file beside it — `<name>.BASE` — with the reproduction recipe, the
identities, and the limits. **Neither `.diff` file's bytes were touched by this act**, and both md5s
are asserted in their annotations.

## The carrier-commit clause

A state diff's base names a commit on the line that carries **all** of its targets.

For `L3_T1_state.diff`: 17 of its 18 targets are byte-identical at `79ee8e5` and at `origin/main`,
but the 18th — `session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py` — **does not exist
on main at all**; the step-4 evidence pack lives only on the #290 line. "This diff applies at main"
would be a true statement about 17 files and a wrong one about the diff.

## The instrument, and its non-vacuity

`state_diff_base_probe.py` rejects on two distinct grounds, both exercised in the committed run
`L3_T1_applied/BASE_PROBE_L3_T1.txt`:

| ground | commits that reject |
|---|---|
| pre-image **mismatch** (target exists, blob differs) | `abf8f4c` · `6128b20` · `af12049` |
| target **absent** (path not in that tree) | `e73e6bf` · `987a508` · `6081f8e` |

A probe that called every commit admissible would be hazard class 5. This one is shown failing in
both available directions, on the real artifact, in a committed run.

## Applying `L3_T1_state.diff` after the base has moved

At `af12049` and every descendant, exactly one file fails — the harness — because that commit
already landed the same re-pin (`EXPECT_V0SURF '12d903336f6e'` → `'96d671c952c8'`). It is a
duplicate, not a conflict of substance:

```
git apply --binary \
  --exclude='session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py' \
  L3_T1_state.diff
```

→ 17 files · `data/v0surf.pkl` = `84fb0cde29f36c1a91d440e63b753c3c` · `fv 95277b76` — **identical
result**, re-run at `abf8f4c` by this seat. Regenerating at the tip reaches the same bytes.

## Scope disclosure

The seam's act (1) named `L3_T1_state.diff` only. The `L1_amended_state.diff` annotation is an
**extension by this seat**, taken because a clause satisfied on one of two copies is hazard class 2
(duplicated assertion) — and disclosed on-issue rather than performed silently. Nothing depends on
it; one word reverses it.
