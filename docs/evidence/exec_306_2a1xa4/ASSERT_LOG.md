# #306 seat `2a1xa4` — THE BOX-CLASS ASSERT LOG

Appended to, never edited in place. N35: the fit-path assert is mandatory before any fit figure, and **both
asserts stale on any observed host migration or restart**. Each entry names its host and the substrate it
asserted on. A host label classifies nothing — only reproduced output bytes do (hazard class 15).

| # | UTC | host (`model name` · stepping · uptime at entry) | substrate | fit-path `fb9efdec` (N35) | verdict |
|---|---|---|---|---|---|
| 1 | 2026-08-04 23:58 | `Xeon @2.80GHz` · stepping 7 · **up 0 min at session start** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (78s) | **FIT-CLASS** |
| 2 | 2026-08-05 00:26 | `Xeon @2.80GHz` · stepping 7 · **up 4 min (container restarted)** | pure pass-0, capture `13b71c26` | **PASS — `fb9efdec4d669d389fe3beef2bca3092`** (62s) | **FIT-CLASS, re-classified** |

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
