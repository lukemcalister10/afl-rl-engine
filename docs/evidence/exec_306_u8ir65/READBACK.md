# #306 — INCOMING EXECUTION SEAT `u8ir65` · READ-BACK AND HOLD · 2026-08-05

Filed against the pass-2 pre-authorisation
([#306 comment 5187094806](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5187094806),
re-affirmed at [5187347144](https://github.com/lukemcalister10/afl-rl-engine/issues/306#issuecomment-5187347144)).
**Nothing has been run against the loop. No curve installed. Bake held; EXECUTION word WITHHELD.**

---

## 1 · WHAT I READ

`docs/CURRENT_STATE.md` v62 on main (`d9e983f`, register v571) in full — my local `main` was stale at v46
and I fetched before reading, which is itself worth recording. Issue #306's body in full. Comments
`5186041140` (the pre-fire audit and the seven-step fire order), `5186208519` (the channel ruling and its
own correction of the narrow-channel statement), `5187094806` (the pass-2 pre-authorisation), and every
filing after them through `5187347144`. Also `5186277660`, since v62 names it as required reading. The
hand-off at `docs/evidence/exec_306_2a1xa4/HANDOFF.md` on `claude/exec-seat-306-handoff-2a1xa4` at the
named tip `489587b`.

## 2 · SUBSTRATE — VERIFIED BY APPLY-AND-HASH, NOT READ

**All nine captures re-hashed from their carriers; all nine match the hand-off's table** (details and the
carrier for each in `ASSERT_LOG.md`). Capture 9 `bc1001f9` is identified as live and capture 8 `ebaca58e`
is retained, not stale.

The live capture applied to its recorded base and regenerated **byte-identically**:

```
L6_pass1c_state.diff   bc1001f978f1b226b3323fad6bd82132  ->  bc1001f978f1b226b3323fad6bd82132
sections 20   base 472c39d on claude/exec-seat-306-afl-rl-zlaarm
```

**State now live, read from the applied substrate:**

| | |
|---|---|
| store | `81d24704` (Guard 5 asserted; `curve_source_store_md5` kept FULL 32, E.5 finding 5) |
| installed curve payload | **FULL `9f7848f41d3b041b7397b5fe0d5d909a`** |
| surface | `6ba4f4c3` (`data/v0surf.pkl`) |
| engine | `15525b03` **both** pins (`data/expected_boot.json`, `data/release_contract.json`) |
| `contract_sha256` | `a6b04a3e` — fresh, the N44-addendum re-stamp |
| sealed history | `release_lineage.json` `6925d4b5`, untouched |
| selftest pins | `_contract_md5` FULL 32 `5f5ffdfdf2ee67ac99f4076245c89558` · `_per_entrant_md5` 8-char `e1c62f86` |

**The full-hash-versus-8-character-stamp trap is understood and I have confirmed the corrected state in
the substrate, not assumed it.** The two pins in that one file have different lengths and neither declares
it; my predecessor's installer wrote an 8-character stamp over the head of the 32-character hash and
produced a true hash of the wrong bytes. I read both pins out of the source and confirmed the full pin is
whole and equals the md5 of `ui/release_pick_curve.json`.

## 3 · BOX CLASS — **FIT-CLASS**, classified by reproduced bytes

`uptime` read **0 min** on my first command. Boot **04:18:42 UTC** from `/proc/uptime`; the assert ran at
**04:29**, after it.

```
refit_v0surf.py --verify, pure pass-0 substrate (capture 13b71c26), installed curve e69a3f38
  new md5  fb9efdec4d669d389fe3beef2bca3092
  pin      fb9efdec4d669d389fe3beef2bca3092
  VERIFY: refit REPRODUCES the committed pin.          55s
```

Preceded by: substrate round trip to `13b71c26` · pins **5/5 exact** · OpenBLAS **sha256 `05c9f9eb…`
byte-exact** · `preboot_assert.sh` as its own command · `bootstrap.sh` **rc=0**, Guard 5 PASS · the two
tier-2 stamps regenerated to N33's `d14f0f12` / `aaccad1c`. Round trip proven again afterwards.

`Intel(R) Xeon(R) Processor @ 2.80GHz`, stepping 7 — **the same label as the seam's box, which fails this
assert at `969dba06`**. Hazard class 15 confirmed from both directions again; the label classifies nothing.

**N35 is live for me: I re-run this in full after ANY restart, and I check `uptime` before every fit
figure.** The outgoing seat was restarted five times in one day on this environment.

## 4 · A RECONSTRUCTION FINDING, filed so a successor does not pay for it twice

The capture's base `472c39d` carries **39 non-docs files the `2a1xa4` evidence branch does not** — the
#279 panel machinery and `tools/preboot_assert.sh`. Applying the live capture to the evidence-branch tree
fails on the first missing file. The operating tree is **zlaarm's non-docs content plus the `2a1xa4` docs
tree**, and the committed instruments assume exactly that. I reconstructed it without a commit by
checking those 39 paths into index and worktree from `472c39d`. **Both round trips being byte-exact is the
proof the reconstruction is right** — a wrong base cannot reproduce a capture byte-identically.

## 5 · THE FIRE ORDER I HOLD FOR PASS 2 — my understanding, for audit before anything runs

**This is pass 2 of bound 4.** Fixed point = derived payload md5 **== installed payload md5, FULL md5 per
N22**. Exhausted → **HALT-and-report, never declare**. No gate re-spec'd; "converged" not redefined.

1. **Install derived payload `b61c01b0350cf113deec5b739c5f679f`** via the **L1(b) enumerated same-commit
   set — the recorded set, nothing improvised** — using the corrected `install_pass1.py`, all-or-nothing,
   **dry-run first**. Carried disciplines: the paired-value edit rule where a sealed twin shares a token
   with a live pin (`3068.4647` appears twice in `pvc_curve_v2.json`, as the field and inside that field's
   own prose) — by JSON path, occurrence counts asserted before and after; **pin lengths read out of the
   source, never inferred from a sibling**; N32 payload recipe; N22 full-md5 identity; E.5 finding 5's
   full-32 store stamp; `contract_sha256` re-stamped in the same act; sealed history byte-asserted
   untouched; N33 srcmd5 re-stamps; evidence committed **before** any substrate op.
2. **Refit** — C.3 step 3: re-bake `v0surf`, re-stamp `expected_boot.v0surf` **inside Addendum C.1's
   identity set**; re-pin the harness to the new signature with its **in-file old→new ledger, dated**, and
   **non-vacuity proven both directions**.
3. **Emit** — backup `2f8b4bd4` proven first; **channel check: counted fallback 71 / 5.931% or STOP**; the
   **F-C full-md5 surface binding recorded and asserted** (the signature only selects — pass 0 proved two
   surfaces can share one); restore proven `2f8b4bd4` → `2f8b4bd4`.
4. **Basis byte-identity** — the lens basis re-emitted **byte-identical at `25a72f85`**, with the two-axis
   separation re-proven (frozen harness still `e0130cc2`).
5. **Derive → the fixed-point comparison on FULL md5.**
6. **Round trip proven**; new sealed capture with its BASE annotation written at generation.
7. **File** with the gate figure — **G-Y0 naming its surface md5 and its denominator (n=1,326 over 64
   picks, 2.000% HARD)** — and **the lane expectation at the current key**. The key becomes
   `…|b61c01b0|…` and will report **INAPPLICABLE before recording**; that is the instrument working, and
   the expectation gets **recorded at that pass, never assumed**.

**The repeat-payload instruction, held explicitly.** The payloads already on this lane are `e69a3f38`
(pass-0 installed), `9f7848f4` (pass-0 derived, pass-1 installed) and `b61c01b0` (pass-1 derived, pass-2
installed). If pass 2 derives any of them I name it in the filing **as a repeat** — a derived `9f7848f4`
would be the two-cycle signature, and a derived `b61c01b0` would be the fixed point itself.

**The head-bounce is on watch and NOT interpreted.** Pooled head `3068.4647` → `3010.1221` → `3064.3712`
while the ladder falls monotonically `54,722` → `53,678` → `53,511`. Two derived curves cannot separate a
cycle from a damped approach; R-I's bound decides it by measurement, not by pattern-matching.

**Carried into every number I file:** the channel is wide (55.78% of movement on the 71 counted rows,
44.22% on the other 1,126 — the narrow story is never told again); the engine contributes exactly zero and
these are isolated **surface** effects; wholesale belief is **6.18% of teaching signal by value**, and the
−0.63% level move in evidence-backed rows is a **floor** on prior-shaping, not the share. Every count names
what it is a share of.

## 6 · WHERE I STOP

**Held at the boundary.** Nothing runs until the seam has audited this read-back. Bake held; EXECUTION word
WITHHELD; N43's levels are the owner's at the landing; nothing lands.
