# #306 ACT (3) — **HALT AND REPORT.** The v0surf fit does not reproduce the record's bytes on this box, and today's lane shows NO path memory here

**2026-08-04, the #306 cold execution seat `zlaarm`.** Five fits run under the seam's go. Every figure was
measured here on the reconstructed pass-0 substrate. **Nothing was written by any of them** — all five ran
`refit_v0surf.py --verify`, which computes the surface into memory and prints its md5 without touching
`data/v0surf.pkl`, the pin, or the provenance log. Substrate restored and proven byte-identical to
`13b71c26` afterwards. **Reported, not declared.**

---

## WHAT I SET OUT TO DO

Acceptance 1 requires L-B's determinism test to be proven **in both directions**, and the failing direction
first: *"It must FAIL when re-pointed at the current lane, naming the differing bytes — i.e. the test is
demonstrated to reproduce the defect it exists to catch."* So before designing anything, I ran today's lane
from the starting surfaces C3′ names, expecting to watch it produce different bytes.

**It did not. The measurement went the other way, twice over.**

## THE FIVE FITS — every one byte-identical

Installed curve **`e69a3f38`** throughout (the ruled re-entry anchor). Frozen fitted stack unmoved:
peak `f305fe53` · pvc_snapshot `ade79790` · cm_400 `34faa865` · q97m `cfdc7321` · store `81d24704`.
Fresh process each time. Output compared on **FULL md5** (N22), never the signature key — the shipped-config
signature was `96d671c952c8` in all five and is not the identity.

| # | starting surface on disk | pin | threads | **output surface md5** | real |
|---|---|---|---|---|---|
| A1 | `fb9efdec` — pass-0 | `fb9efdec` | 4 | **`5939fa35b98b1286f0551b6ebe3017e3`** | 53.6s |
| A2 | `fb9efdec` — pass-0 | `fb9efdec` | 4 | **`5939fa35…`** | 52.9s |
| C | `84fb0cde` — the L3–L5 record / L4-exit state | `84fb0cde` | 4 | **`5939fa35…`** | 51.1s |
| B | `31e7f00b` — the halt state | `31e7f00b` | 4 | **`5939fa35…`** | 54.2s |
| C′ | `84fb0cde` | `84fb0cde` | **1** | **`5939fa35…`** | 49.5s |

**All five identical.** A1/A2 give the R-H.1(b) double-fit gate: **PASS**, on-box fit determinism holds.

## FINDING 1 — **C3′'S BYTE-AGREEMENT ALREADY HOLDS, ON TODAY'S UNMODIFIED LANE**

Three materially different held starting surfaces — the record's furthest-apart pair plus the pass-0
surface — fed to the **current** fit lane at one curve produce **byte-identical output**. The starting
surface made no difference at all.

**This is not L-B succeeding early. It is L-B's acceptance becoming unfalsifiable on this box, which is
hazard class 5 by name.** Acceptance 1 demands the test be shown to fail on today's lane before it may be
claimed on tomorrow's. **I cannot produce that failure here.** A determinism guard built and "proven" in
this container would be a check that has never seen the non-determinism it targets — the costume the
directive explicitly refuses, twice on the record.

**What I did NOT test, stated so the claim is not read wider than it is.** The record's path-memory pair was
curve `ca662051` from surfaces `aaf45964` vs `2d7dab64`. I tested curve `e69a3f38` from three surfaces —
the same *shape* of test, at the curve C3′ actually binds, but **not the record's exact pair**. Re-running
that pair needs a deliberate curve install (sealed-twin discipline, N32 recipe), which is an act outside my
re-entry curve. **Offered as the next measurement if the seam wants it; not taken unilaterally.**

## FINDING 2 — **THE FIT DIVERGES ACROSS HOSTS WHILE EVERY PIN PASSES.** This is the bigger one.

Fit C ran from the **exact state the record fitted at L6 pass 0** — the L4-exit tree, surface `84fb0cde`,
curve `e69a3f38`. The record's own committed filing says that state yielded `fb9efdec`, twice, in two fresh
processes (`L6_PASS0.md`, R-H.1(b): *"→ `fb9efdec` twice (72s, 74s)"*), and the resulting bytes are
committed at `pass0_surface/v0surf.pkl` with their `IDENTITY.json`.

```
same declared inputs, same lane, same instrument:

  recorded host   ->  fb9efdec4d669d389fe3beef2bca3092      (committed bytes, L6 pass 0)
  THIS host       ->  5939fa35b98b1286f0551b6ebe3017e3      (5 fits, invariant)
```

**Every pin the project has passes, and the output still diverges:**

| checked here | result |
|---|---|
| 5 version pins (py 3.12.3 · numpy 2.4.4 · scipy 1.17.1 · sklearn 1.8.0 · openpyxl 3.1.5) | **5/5 exact**, re-read from the interpreter |
| item-392 ENV PIN — bundled OpenBLAS sha256 | **`05c9f9eb…` byte-exact to the pin** |
| Guard 5 — store · rl_model · fv | **PASS** (`81d24704` · `3b011802` · `d920557e`) |
| cm_400 · q97m · register · engine head · config manifest | `34faa865` · `cfdc7321` · `652d83e8` · `3c7b0c3c` · `cef06fd6` — all as pinned |
| installed curve, re-derived under N32 | **`e69a3f38`** |
| **compute-path assert — the board path, same box, same session** | **PASS, `92e397bd` byte-exact** |
| thread count as a candidate cause | **excluded** — single-threaded gives the same bytes |

**This is the trap the directive names, reproduced in anger:** *"the OpenBLAS byte-pin passed on both hosts
while the dispatch tier differed — THE PIN WAS NEVER THE GUARD."* The library bytes are identical to the
pin and the fitted output bytes are not. It is also exactly where N16 said the sensitivity lives: the board
path reproduced byte-exact on this same box minutes earlier, so **the divergence is isolated to the v0surf
FIT** — item 380's defect, appearing for the third time.

**And it lands on L-C.** That leg has stood DEFERRED as UNMEASURED since 2026-07-22 for want of a second
architecture. **There is now a measured two-host divergence of FITTED OUTPUT BYTES** — not a version pin, not
a same-box proxy, the actual quantity L-C says must be compared.

**The honest limitation, stated rather than buried:** host 1's figure comes from the committed record, not
from a live host I control — that container is gone. This is a comparison against sealed committed evidence,
which is the standard this project uses, but it is not two live hosts side by side. And I have verified every
**declared** input; I cannot exclude an **undeclared** one that differs between the two containers. Naming
that possibility is part of the finding, not a hedge against it.

## WHY THIS IS A HALT AND NOT A NOTE

1. **The record's entire L6 surface family is not reproducible here.** `fb9efdec` · `aaf45964` · `864c11b9` ·
   `2d7dab64` · `31e7f00b` were fitted on a host whose fit this box does not reproduce. Re-entering L6 here
   produces a **different surface family**, so no G-Y0 I measure can be compared limb-for-limb to
   8.084 / 11.030 / 8.842 / 11.028. Publishing numbers that *look* comparable and are not is hazard class 1
   and 4 together.
2. **Acceptance 1 cannot be satisfied in this container.** Its failing-direction demonstration is
   unavailable here, and no amount of design work changes that.
3. **The period-2 cycle itself is now in question as a portable fact.** It was measured through a fit this
   box does not reproduce. Whether the cycle survives on this host is a real question with a real answer,
   and it is a ruling, not a seat's call.
4. **Both R-H pre-loop gates PASS.** Gate (a) `92e397bd` byte-exact; gate (b) double-fit identical. The
   gates are behaving exactly as designed — and they are, by construction, blind to precisely this. That is
   L-C's whole thesis, and it means "the gates are green" is not a licence to proceed.

**R-I's posture governs: HALT and report, never declare.** I have not designed L-A, have not built a lane,
have not run a pass, and have picked nothing.

## WHAT I DID NOT DO, and why each is the seam's

1. **I did not re-run the record's `ca662051` pair.** It needs a curve install outside my ruled re-entry
   anchor. It is the sharpest remaining discriminator and I recommend it.
2. **I did not treat `5939fa35` as the new truth.** It is this box's answer, named with its host, and it
   pins nothing.
3. **I did not re-point, re-spec or soften any gate**, including L-B's acceptance. Weakening
   "byte-identical" to "identical on the box that happens to be running" is the H.3 failure with a new coat.
4. **I did not bake.** All five fits were `--verify`. Nothing was written.

## POSTURE

Acts (1) and (2) stand as filed and verified. **Nothing landed.** The substrate is restored and proven
byte-identical to `13b71c26` by round trip — three times now across this session. The carrier, the frozen
ancestors, the HOLD branches and main are untouched. **The EXECUTION word remains WITHHELD.**

**HALTING. The lane's cross-host behaviour is the seam's to rule on.**
