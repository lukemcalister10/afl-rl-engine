# LANDING ATTEMPT — owner authorised the refit, then the box blocked it

Owner's word, 2026-08-10, issue #334 comment 5235816134: *"Authorise the refit."* Halt option (a)
taken. This page records what landed, what did not, and why.

**Status: the v0surf re-cut is DONE and clean. The gated board rebuild is BLOCKED by a second seat
working in the same shared scratch directory. Nothing is pushed.**

---

## 1 · WHAT COMPLETED — the v0surf re-cut

Run through the sanctioned lane, `session_2026-07-18/legf6/scripts/refit_v0surf.py --bake`, with
`RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1`, from the private workspace, on the written store `d9a24282`.

| | before | after |
|---|---|---|
| `data/v0surf.pkl` | `d594dc034e86935b370c49b240a18370` | **`5a03c9ea3e9a32e6cc6e1ffec5293685`** |
| frozen signature set | `af556bdc…`, `edb15f7a…` | `41af7326…`, **`6ef67f07db98258786189a6316ce24f9`** ← shipped |
| `data/expected_boot.json` `v0surf` | `d594dc03…` | `5a03c9ea…` (re-pinned by the lane itself) |

The shipped signature `6ef67f07` is exactly the one the earlier halt named as missing from the frozen
set. Surfaces frozen: 2 — both the pre-swap and the post-`RL_PVC2` surface, so a normal build performs
no fit at all. Shape unchanged: 18 age-18 positions, surfN 60 ages, surfR 12 ages. Provenance appended
to `session_2026-07-18/legf6/v0surf_refit_log.json`.

**The bake is uncontaminated by the contention described below.** With `RL_V0SURF_REFIT=1` the engine's
`_load_v0surf()` returns `{}` and reads no pickle at all (`_merged_recover.py:1289`), so the re-cut
derives only from the written store, the pinned config, the pinned curve and the pinned fitted
artifacts. All shared pinned inputs were md5-checked before and after the bake and were unchanged.

### On the lane's clean-instance precondition

The lane records `precondition_balanced_board_06d8af60: NOT EVALUATED — unreachable since the pricing
split`, and asks the running job to supply substitute evidence. **This job has unusually strong
substitute evidence:** control run B (`board_impact_diagnostic.md`) refitted v0surf from scratch on
this same box against the *unwritten* store and reproduced the shipped board `6e724cca` **byte-exact**.
A weather box cannot do that. So this box is demonstrably not a weather box for this surface.

## 2 · WHAT IS BLOCKED — the gated board rebuild

The gated rebuild cannot be certified on this box right now. Two facts collide:

1. **The engine's v0surf load precedence is `$RL_V0SURF_PKL → /home/claude/v0surf.pkl →
   <repo>/data/v0surf.pkl`** (`_merged_recover.py:1290`, `boot_guard.py:264`).
2. **`RL_CONFIG_MODE=gate` rejects `RL_V0SURF_PKL`** as an unpinned model override:
   `UNKNOWN model override RL_V0SURF_PKL=… is not in the manifest`.

So under the gated path the engine must resolve v0surf by natural precedence — and on this box the
middle slot is occupied by **another seat's live, non-pinned artifact**.

### The evidence of a second writer

`/home/claude` is shared scratch, and a second seat is actively building in it:

| file | md5 / note | last written |
|---|---|---|
| `/home/claude/v0surf.pkl` | `c309168f494496fb283c91aaf8f7f44a` — **not** any pin of mine | 04:15:01 |
| `/home/claude/g1_v0surf_main.pkl` | `d594dc034e86935b370c49b240a18370` — main's pinned surface, saved aside | 04:23:44 |
| `/home/claude/g1_ws/` | that seat's own workspace | 04:28:09 |
| `/home/claude/g1_export.txt` | that seat's build output | **04:31:07** |

I checked at 04:31:11 — four seconds after their last write. They are mid-build. The pattern is
unmistakable: main's pinned surface parked at `g1_v0surf_main.pkl`, an experimental surface installed
at the shared precedence slot `/home/claude/v0surf.pkl`.

Any gated build I run resolves to **their** surface, not my re-cut one. Guard 5 catches it and halts,
which is the guard working correctly:

```
- v0surf LOAD-PATH MISMATCH: the engine will LOAD /home/claude/v0surf.pkl
  md5 c309168f != pinned d594dc03 … never boot on an unverified LOADED artifact.
```

### Why I did not clear the way

The obvious unblock — `cp -f <my repo>/data/v0surf.pkl /home/claude/v0surf.pkl`, which is exactly what
the canonical seeding scripts do (`session_2026-07-19/envpin/scripts/build_board.sh:20` and siblings)
— **would clobber another seat's artifact in the middle of their build.** Same for deleting it or
moving it aside and restoring it afterwards: their build could import during my window and pick up my
surface, or find no file and take the `FROZEN-LOAD HALT`.

That slot is a single-writer resource. Two seats using it at once is the one-writer violation the #290
runbook flagged against itself (B.6 "I violated the one-writer law, and the workspace makes it easy",
and C.6's serial-engine rule). The fix is serialisation, not a race.

**So I stopped.** The instruction was "all green or halt" and "do not push a surprise". I cannot show
green, therefore I do not push.

## 3 · WHAT IS UNVERIFIED

Everything downstream of the board. The expectations the coordinator set — board `a672ed3a`, the six
±1 movers, total 761,587, pick 1 = 3000, parity 804/804 — are **still only measured under the
diagnostic A/B**, not reproduced through the gated path on the baked artifact. They are expected to
hold (loading a frozen surface is byte-identical to the fit that produced it, by construction), but
expected is not verified, and this act does not get to skip that step.

Not done, and deliberately not done: the board rebuild, the book re-seal, the balanced board and
sibling fixtures, the five UI bundles, and the remaining nine carrier re-pins. Re-pinning carriers to
a board md5 nobody has reproduced would be writing fiction into the manifest.

## 4 · WHAT IT NEEDS

One word, on sequencing rather than on the act:

- **Serialise the box.** When the other seat is done and has released `/home/claude/v0surf.pkl`, this
  job seeds that slot from its own checkout — the canonical pattern — reruns the gated build, and
  lands. Everything else is ready and the expected outputs are already written down, so it is one gate
  run plus the re-pin train.
- **Or give this seat the box** and have the other seat re-seed when it resumes.
- **Or amend the manifest** to admit `RL_V0SURF_PKL` as a pinned override, which would let two seats
  coexist. That is a config-value change and squarely outside this act's scope guard, so it is not
  mine to make.

Gate logs from the blocked attempt are in `landing_attempt/`; the original halt logs beside them are the first run and are unchanged.

Nothing is pushed. No PR is open. The store write, the census and the v0surf re-cut all stand and are
committed on the branch, ready for the gate run that finishes them.
