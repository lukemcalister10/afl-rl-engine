# #306 seat `zlaarm` — THE BOX-CLASS ASSERT LOG

Every measurement act of this job runs behind two asserts. **N35** makes the fit-path assert mandatory and
makes both stale on any observed host migration or restart. This file is appended to, never edited in place.
Each entry names its host and the substrate it asserted on.

| # | UTC | host (`model name` · stepping · uptime at entry) | compute-path `92e397bd` | fit-path `fb9efdec` (N35) | verdict |
|---|---|---|---|---|---|
| 1 | 2026-08-04 05:13 | `Xeon @2.80GHz` · stepping 7 · up 8 min | **PASS** (96.7s) | not yet ruled — N35 postdates this act | box compute-class, **fit-class UNKNOWN** |
| 2 | 2026-08-04 05:16–05:24 | same host | — | **`5939fa35` ×5 — DIVERGES** | **OFF-CLASS → act-3 HALT** |
| 3 | 2026-08-04 06:18 | `Xeon @2.10GHz` · **stepping 2** · up 0 min | **PASS** (78.1s) | **PASS — `fb9efdec4d669d389fe3beef2bca3092` (47.9s)** | **FIT-CLASS — measurement acts lawful** |

## Entry 3 — the resume assert, in full

The container **restarted of its own accord** between the act-3 halt and the seam's word: `uptime` read
**0 min** against a session then ~1h50m old, and the host changed again —
`Xeon @2.80GHz`/stepping 7 → **`Xeon @2.10GHz`/stepping 2**. Third distinct host this session. The restart
the ruling called for was therefore already delivered by the environment; I did not need to force one.

**Order of acts, per N35 and R-H:**

1. **Substrate re-verified first, by round trip** — `git diff --binary` reproduced `13b71c26` byte-identically
   before anything ran. `data/v0surf.pkl` `fb9efdec` · both `.srcmd5` `d14f0f12` / `aaccad1c` intact through
   the restart.
2. **Environment re-provisioned** — pins **5/5 exact** re-read from the interpreter; item-392 bundled
   OpenBLAS sha256 **`05c9f9eb` byte-exact**; Guard 5 **PASS** (store `81d24704` · rl_model `3b011802` ·
   fv `d920557e`); cm_400 `34faa865` · q97m `cfdc7321` · register `652d83e8` · engine head `3c7b0c3c`.
3. **FIT-PATH ASSERT (N35), the ruled first act:**

```
refit_v0surf.py --verify, pass-0 substrate, installed curve e69a3f38
  new md5  fb9efdec4d669d389fe3beef2bca3092
  pin      fb9efdec4d669d389fe3beef2bca3092
  VERIFY: refit REPRODUCES the committed pin.          47.9s
```

**PASS. This box is FIT-CLASS.** It reproduces the record's fit, so every comparison to the record's figures
is valid from here.

4. **COMPUTE-PATH ASSERT re-run**, because the restart made entry 1 stale — my own act-2 filing committed to
   this and R-H gate (a) requires it. Control rebuilt not inherited (pre-L4 `b763f59e` + `735d2dec` +
   surface `84fb0cde`, three pins field-level re-stamped, tier-2 sidecars re-stamped):
   NUMÉRAIRE GUARD PASS · **PARITY GATE PASS 804/804 eps=0** · board **`92e397bd` byte-exact**, 78.1s.
5. **Substrate restored and proven** — round trip to `13b71c26` byte-identical. Fifth round trip this session.

## WHAT ENTRY 3 SETTLES, AND WHAT IT DOES NOT

**Settles:** the `5939fa35` divergence was a property of that host, not of this seat's method, this
substrate, or the committed scripts. The same commands, the same bytes, the same seat — a different host —
and the record reproduces exactly. The seam's third-container re-run and this one agree.

**Does not settle:** *why* the off-class host diverged. Both boxes passed every version pin, the OpenBLAS
byte-pin, Guard 5, and the compute-path assert; the off-class one reported an **identical CPU string** to
the seam's fit-class box. **A host label cannot classify a box — only output bytes can** (N35). The
mechanism remains item 380's `DYNAMIC_ARCH` dispatch, undiagnosed at the tier level, and it is L-C's target
rather than this leg's.

**Standing consequence I will observe for the rest of this job:** before every fit, acceptance run or loop
pass I check `uptime`/host, and re-run both asserts if either moved. `5939fa35` is recorded as an off-class
artefact and **pins nothing**; it will never appear as an expectation.
