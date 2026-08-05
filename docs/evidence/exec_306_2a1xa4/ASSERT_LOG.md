# #306 seat `2a1xa4` — THE BOX-CLASS ASSERT LOG

Appended to, never edited in place. N35: the fit-path assert is mandatory before any fit figure, and **both
asserts stale on any observed host migration or restart**. Each entry names its host and the substrate it
asserted on. A host label classifies nothing — only reproduced output bytes do (hazard class 15).

| # | UTC | host (`model name` · stepping · uptime at entry) | substrate | fit-path `fb9efdec` (N35) | verdict |
|---|---|---|---|---|---|
| 1 | 2026-08-04 23:58 | `Xeon @2.80GHz` · stepping 7 · **up 0 min at session start** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (78s) | **FIT-CLASS** |
| 2 | 2026-08-05 00:26 | `Xeon @2.80GHz` · stepping 7 · **up 4 min (container restarted)** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (62s) | **FIT-CLASS, re-classified** |
| 3 | 2026-08-05 01:46 | `Xeon @2.80GHz` · stepping 7 · **up 0 min (container restarted, third time)** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (53s) | **FIT-CLASS, re-classified** |
| 4 | 2026-08-05 02:31 | `Xeon @2.80GHz` · stepping 7 · **up 1 min (container restarted, fourth time)** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (74s) | **FIT-CLASS, re-classified** |
| 5 | 2026-08-05 03:32 | `Xeon @2.80GHz` · stepping 7 · **up 0 min (container restarted, fifth time)** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (55s) | **FIT-CLASS, re-classified** |

## Entry 1 — the arrival assert

`uptime` read **0 min** on my first command of the seat. Both asserts were therefore stale on arrival and no
fit figure was trustworthy until the box was classified. Order of acts: substrate round trip proven to
`13b71c26` **before** anything ran → env re-read from the interpreter (pins 5/5 exact; bundled OpenBLAS
`05c9f9eb…` byte-exact) → `preboot_assert.sh` **as its own command** → `bootstrap.sh` with its **exit code
checked** (rc=0; Guard 5 PASS, store `81d24704`, engine `3c7b0c3c`) → the fit-path assert → substrate round
trip proven again.

**Worth recording rather than passing over:** this box reports `Xeon @2.80GHz` stepping 7 — **the same CPU
string the OFF-CLASS host of the `zlaarm` seat's entry 2 reported**, the one that diverged to `5939fa35`.
Same label; reproduced bytes. That is hazard class 15 confirmed from the opposite direction, and it is the
whole reason N35 requires the assert rather than the label.

## Entry 2 — the mid-job re-classification

The container **restarted again** partway through the fire order: `uptime` read **1 min** while running the
lane-wiring proof, against a session then ~30 min old. Entry 1 went stale at that moment. The lane-wiring
proof itself is a pure derivation over committed JSON and carries its own check (it reproduced the record's
`1a8db02b` exactly), but **no engine act was permitted to proceed on a stale classification**, so the assert
was re-run in full before the matrix emit: substrate round trip → pins re-read → preboot → bootstrap rc
checked → fit-path assert **PASS in 62s** → round trip again.

Every engine act of this seat (the matrix emit at 147s) ran **after** entry 2, on a box classified by
reproduced bytes.

## Entry 3 — the pre-derivation re-classification

The container restarted a **third** time, between the channel ruling and the derivation: `uptime` read
**0 min**. Entry 2 went stale at that moment, so the assert was re-run in full before the derived-curve
figure was produced — substrate round trip to `13b71c26` → pins re-read (5/5 exact, OpenBLAS `05c9f9eb`
byte-exact) → preboot as its own command → bootstrap rc checked → fit-path assert **PASS in 53s**.

**Three restarts, three classifications, three reproductions of `fb9efdec`** — 78s / 62s / 53s. No figure
in this seat's filings was produced on a stale classification.

Additionally, on the LENS substrate (engine `15525b03`, surface `b540833b`), `refit_v0surf.py --verify`
reproduced the baked pin **`b540833b2e251631bf76aeec0040cc05`** in 98s — L-B's passing direction re-proven
independently on this box, and a direct validation of the substrate the derivation consumed.

## Entry 4 — before the separating run

A **fourth** restart, between the pass-1 authorisation and the separating emit: `uptime` read **1 min**.
Re-classified in full before the engine act — substrate round trip to `13b71c26` → pins 5/5 exact,
OpenBLAS `05c9f9eb` byte-exact → preboot as its own command → bootstrap rc checked → fit-path assert
**PASS in 74s**.

**Four restarts, four classifications, four reproductions of `fb9efdec`** — 78s / 62s / 53s / 74s.

Recorded for the cross-box picture: the incoming seam seat reported its own box **FAILING** this same
old-lane assert (`969dba06`, a third distinct old-lane byte-pattern) while reproducing the redesigned
lane's `b540833b` byte-identically. This box reproduces both. Two boxes, same CPU label, divergent on the
old lane and in agreement on the new one — the old lane's machine-sensitivity is the defect the redesign
was built to remove, and it is behaving exactly as the record says it does.

## Entry 5 — before the pass-1 gate measurement

A **fifth** restart, between the pass-1 filing and the owed G-Y0 measurement: `uptime` read **0 min**.
Boot established precisely afterwards from `/proc/uptime` as **03:31:31 UTC**; this entry's bootstrap ran
at **03:32:53**, the board at 03:36:54 and the selftest at 03:42:45 — **every act of the gate chain
post-dates the boot**, so the classification covers the figure. (This row first carried an estimated
03:29 timestamp, which would have placed the assert BEFORE the boot and made the gate figure
unclassified. It was checked against file mtimes rather than trusted, and corrected.)
Re-classified in full before the engine chain — substrate round trip to `13b71c26` → pins 5/5 exact →
preboot as its own command → bootstrap rc checked → fit-path assert **PASS in 55s**.

**Five restarts, five classifications, five reproductions of `fb9efdec`** — 78s / 62s / 53s / 74s / 55s.
On this environment `uptime` is not a formality; it moved under this seat every single time it was checked
at a boundary.
