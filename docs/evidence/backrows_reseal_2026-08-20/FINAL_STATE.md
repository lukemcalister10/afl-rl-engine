# FINAL STATE — THE BACK-ROWS REPAIR AND THE BOOK RE-SEAL

**Owner words, VERBATIM:** *"Let's fix it now please."* (ACT A) and *"And I'll re seal once that is
done."* (ACT B) · **Date:** 2026-08-20 · **Base:** `main` @ `78ebc08`

Two acts, in the owner's order, each with its own prereg committed before any edit, its own gates and
its own evidence. One read-only addendum. **Nothing was pushed.** `docs/OPEN_ITEMS_REGISTER.md` was
not touched.

---

## 1. THE COMMITS

| # | sha | what |
|---|---|---|
| 1 | `15729e7` | **PREREG (ACT A)** — the back-rows `AGE_REF` repair. Before any engine edit. |
| 2 | `11fe287` | **ACT A** — the one-statement repair + the built board + sidecars. `c97a4d9f → 68be10c7` |
| 3 | `b3c7518` | **ACT A** — the landing transaction: pins, column, contract, sibling, UI, lineage |
| 4 | `5aaa654` | **ACT A ADDENDUM** — the 26-vs-25 discrepancy attributed (read-only) |
| 5 | `401aa05` | **PREREG (ACT B)** — the book re-seal. Before any seal was written. |
| 6 | `c0c920a` | **ACT B** — the re-seal. Sealed-lag `2 → 0`. |

## 2. FINAL IDENTITIES

| identity | before (`78ebc08`) | after | moved by |
|---|---|---|---|
| **board** | `c97a4d9f9fa42597f85517c7850d3943` | **`68be10c79d0ee096455754e084bcf757`** | **ACT A** |
| **balanced_board_md5** | `3970156c8658fc9ecea8089e8b3ecdf1` | **`556ad70d295923455982ae33e4b8bfd3`** | **ACT A** (sibling repin) |
| **contract_sha256** | `c5149774b8ec…` | **`cde9f70a49b6…`** | **ACT A** |
| **book `stable_sha256`** | `86a82e6ebce6…` | **`9f46aba3ba8b…`** | **ACT B** |
| **book seal `head_md5` / `store_md5`** | `5ac6780f` / `cb38ef11` | **`1867e953` / `b745002e`** | **ACT B** |
| **book seal `n_players`** | 2650 | 2650 *(re-counted, not carried)* | — |
| **store** | `b745002eb0a0fbb1c34fa44f1ef708d6` | *unchanged* | — |
| **engine_head** | `1867e953cf844d089ab1da68379b1742` | *unchanged* | **neither act** |
| **config / rl_model / fv / register / v0surf** | — | *all unchanged* | — |
| **as_of_round** | 23 | 23 (held) | — |
| **F5 entrant seal** | `ccc26a9e` | *unchanged* | — |
| board totals | 692,296 / 804 active · 3,190 / 198 back | **692,296 / 804 · 3,118 / 198** | **ACT A** |

**`engine_head` did not move, and that is a finding rather than an oversight.** It is
`md5(engine/rl_after/_merged_recover.py)`. This act edits `rl_export.py`, the **exporter**. The
valuation engine was not touched, which is exactly why all 804 active prices are byte-identical — and
`land_br_pins.py` and `land_br_contract.py` both **assert** it does not move.

---

## 3. ACT A — THE BACK-ROWS `AGE_REF` REPAIR

### The defect, and where the residue lived

Entering `rl_export.py`'s `back_extra` loop the ambient engine clock was `BASE_REF=2026` but
**`AGE_REF=2028`**, left standing by the players loop's last forward call `ev(_p, 2028)`; these rows do
not traverse the `_b6_core`/`price6` re-pin that would correct it. A retired row's recalled price
therefore depended on the fact that 804 *other* rows had just been priced forward to 2028.

**WHERE THE RESIDUE LIVES — the brief's question, answered by measurement (`02_where…txt`): the EXPORT
PATH, not a cached input.** `back_extra` rows are priced inline on every build from `_ev(_p, 2026)`;
nothing caches a back-row value in a sidecar, a store field or a pickle, and the only post-loop writer
(`owner_overrides`) adds a display block and never touches `v`. **So the durable fix is one statement,
and from the moment it landed EVERY BARE BUILD produces the corrected back rows forever.** No number
was hand-edited.

### The fix

```python
    for _p in g['back_extra']:
        g['BASE_REF']=g['AGE_REF']=2026; g['_pe_clear']()   # THE BACK-ROWS REPAIR
```

Byte-for-byte `PREREG_H3_REPAIR.md` §2 variant **(b)** — the statement the H3 seat applied, measured,
and correctly reverted because curing it moves the board of record and no owner word then covered it.
That word was given. No expression, constant, threshold or law was touched.

### Predictions vs outcomes

| | prediction | outcome |
|---|---|---|
| P1/F2 | control build reproduces the live board `c97a4d9f` | **MET** — exactly, so every diff is attributable |
| **P2/F1** | **post-repair bare build == the probe's rebuild `68be10c7` BYTE-EXACT** | **MET — byte-exact** |
| P3/F6 | dev == canonical | **MET** — both `68be10c7` |
| P4/F3 | 804 actives byte-identical | **MET** — 0 differing leaves; sum held at 692,296 |
| P5/F4 | 25 back rows move, all down, `−72` | **MET on substance, ONE SCOPE ERROR IN THE PREREG — see §6.1** |
| P6 | the 25 movers match the probe list exactly | **MET** — exact match on key, name, current and corrected, parsed from the committed probe file rather than retyped |
| P7/F5 | nothing outside back rows + `lensConservation` moves | **MET** — 131 leaves total: 125 back (25 rows × 5 fields) + 6 `lensConservation` |
| P8/F7/F8 | engine_head, config, rl_model, fv, store, register, v0surf, round all held | **MET** |
| P9 | **the balanced board MOVES** | **MET** — `3970156c → 556ad70d`, and its ACTIVE vector is unmoved (`sum_v` 692,296, sheezel 10,428) |
| P10 | the full landing transaction | **MET** |
| P11/F9 | gates | **MET** — see §5 |

### The 25 movers — the priced consequence, disclosed

All down. Movers aggregate **772 → 700**; whole back section **3,190 → 3,118**; `lensConservation`
lens −1 `755,307 → 755,235` and lens −2 `782,108 → 782,036`, each −72. `charlie-dean 41→39` and
`jacob-bauer 29→27` — the H3-era named examples — reproduce exactly. Full table in
`03_builds_and_proofs.txt`.

**No player price, club total, pick price or numéraire moved.** The F5 entrant layer (56,773), its
seal (`ccc26a9e`) and lens 0 (the k=0 zero-phantom invariant, 692,296) are all held.

---

## 4. THE 26-vs-25 DISCREPANCY — ATTRIBUTED, AND THE BRIEF'S HYPOTHESIS REFUTED

The record has carried this as *unattributable*: the H3 account reported 26 and never listed them. That
is true **of the record**; it is not true **of the tree**. Both eras are still buildable, so the H3-era
list was **re-derived** in a throwaway worktree at base `702e25d` — and **both era boards reproduce
byte-exact** (`a05fe951` unmodified, `b507446e` with variants (a)+(b) applied), which is what makes the
list the H3 seat's list rather than a reconstruction of one.

**It is `karl-gallagher`.** He moved `7 → 6` at the H3 era and does not move today.

**The brief's anticipated explanation — "one row left the back section between eras" — is REFUTED, not
confirmed.** The back section is 198 rows in both eras with an *identical key set*: nothing joined,
nothing left. What changed is the row's **value**: on the current store he prices at 8 and rounds to
the same integer with the clock pinned as without, so he is simply no longer a mover. The store has
moved three times since. The probe's reading — *"consistent with ordinary era movement … NOT evidence
of partial repair"* — is **confirmed, and now attributed rather than inferred**.

---

## 5. ACT B — THE BOOK RE-SEAL

### The price line, settled and measured

Certification runs on the **BARE SHIPPED LINE** — no env dials. The identity that ruling rests on was
**re-verified on the post-Act-A board before anything was sealed**: a bare gate-mode board build
(`RL_CONFIG_MODE=gate`, no dial env at all) reproduces the live board `68be10c7` **byte-exact**.

### The instrument

`docs/evidence/bake_2026-08-20/reseal_bake.py` — the act that last moved the seal — carried with its
**logic unchanged byte-for-byte**; only the docstring, three print strings, the temp prefix and the two
narrative seal fields differ. Its declared change (2), dropping the `RL_GAMMA=0.85` dial block, **IS
the price-line ruling already implemented**, so this act carried it forward rather than re-deciding it.

### Old seal → new seal

| field | before | after |
|---|---|---|
| `head_md5` | `5ac6780f` | **`1867e953`** |
| `store_md5` | `cb38ef11` | **`b745002e`** |
| `n_players` | 2650 | 2650 — **re-counted, not carried** |
| `stable_sha256` | `86a82e6ebce668448ffb…` | **`9f46aba3ba8b056d0835…`** |
| `config` | `eed19a75f775…` | *unmoved* |

**Why `n_players` held.** The instrument writes `len(stable keys)` from the freshly built matrix and
never reads the old value; the generator's own line reads `eligible players: 2650`. The store moved by
**score application** (R23) and the injury-sheet re-cut, which change what players are *worth*, not who
is *eligible*. No row entered or left the cohort. The count holding while the content hash moves is the
correct pair of outcomes.

### Certification and the lag

* **Certified**: the same instrument's `--check` re-verifies the committed seal against a freshly
  regenerated gate-mode book and **PASSES on every field**. Its B3 procedure is byte-identical to
  `ship_gates_check.py`'s own `_b3_stable_sha`.
* **Sealed-lag `2 → 0`.** `release_manifest_check` now reads **40 of 40** carrier fields coherent, 0
  incoherent, **0 sealed-lag**. The two lines that lagged were exactly `book_stable_seal.head_md5` and
  `.store_md5`. **There is no remainder to disclose.**
* **One file was written.** Board, store, `expected_boot`, `release_contract`, `release_lineage` and
  every UI bundle are byte-unmoved by Act B.

---

## 6. DEVIATIONS, MISSES AND CORRECTIONS — NONE ABSORBED

1. **PREREG P5 NAMED THE WRONG SCOPE.** It read the probe's *"aggregate: sum 772 → 700"* as the whole
   back section. It is the aggregate over the **25 movers** (confirmed exactly, 772 → 700); the whole
   198-row section sums **3,190 → 3,118**. The **delta −72**, which is the quantity that was predicted,
   is met on both readings. **The prereg was corrected against the tree, not the reverse**, and the
   verify instrument now prints both figures with the correction named in its own output.
2. **THE BRIEF SAID THE BOOK SEAL WAS STALE SINCE 2026-07-17. IT WAS NOT.** THE BAKE re-sealed it on
   2026-08-20 (head `5ac6780f` / store `cb38ef11` / n 2650). The brief's figures came from
   `RESEAL_HALT.md`, which predates the bake. The lag closed here is **one chapter old** — the D8
   adoption, the injury-sheet re-cut and the R23 advance moved engine and store without a re-seal.
   Declared in the Act B prereg **before** the act, not discovered afterwards.
3. **THE BRIEF SAID `n_players` READ 2649. IT READ 2650.** 2649 was the pre-bake count.
4. **THE `ship_gates_check.py` CAUTION IS OUT OF DATE.** The `RL_GAMMA=0.85` self-brick (the v787
   finding) is **already repaired in tree** by M1a; the line reads `1.0`. The suite still does not run
   here for a **different** standing reason: `:49` hardcodes `/home/claude/rl_workspace/rl_after`, which
   this box carries at engine `338a790b` / store `cc02567f` — stale. Guard 5 halts it pre-flight, which
   is Guard 5 working. **It was not edited**, per the brief; certification was carried by the B3 steps
   run directly. **P1 item restated: the hardcoded `RA`, not `RL_GAMMA`.**
5. **ONE DISCLOSED HALT IN ACT B, AND ITS REMEDY — no instrument edit.** The first re-seal invocation
   died because `tools/build_lock.sh` **exports** `RL_BUILD_LOCK_HELD` and gate mode rejects any unknown
   `RL_*` var as a model override — the trap `PREREG_D8` §3 disclosed and the R23 build driver pops.
   Remedy: hold the lock in the parent shell (the flock fd stays held, so the interlock is real) and
   strip the variable from the child with `env -u`.
6. **P2, RECORDED NOT REPAIRED.** The re-seal instrument's own `FAILED: no __meta__` diagnostic path is
   unreachable when the matrix dies before writing anything, because `json.load()` on the empty
   `mkstemp` file raises first. Inherited from the bake's port and from the 2026-07-17 original. Not
   this act's warrant.
7. **ONE WEEKLY TEST PIN MOVED** in `ui/tests/movers.test.js` — the out-of-round boundary count `9 → 10`
   — because this act writes a tenth boundary. Documented in place like the eight bumps before it, with
   the note that this boundary is **different in kind** from the ninth (the F5 act moved no priced
   value; this one re-prices 25 back rows). A second, **non-asserting** line was corrected for accuracy.
   **Nothing was loosened**: both non-vacuity assertions were re-run at the swing and still discriminate
   in both directions; all 10 boundaries remain anchored to owner-approved lineage records.
8. **STILL REFERRED, NOT SMUGGLED IN.** The strictly larger in-`ev()` structural cure
   (`H3_DIAGNOSIS.md` §6 q2/q3) — making `ev(p,Y)` pin its own clock before *any* evaluation — is **not
   done**. This act removes the *exposure* on one loop; the ambient-state sensitivity of `ev()` remains
   a modernisation item with its own prereg to write. Doing it here would also have falsified F1.
9. **`r15_ladder_survival_proof.py` still cannot run** (`KeyError: 'GFWD'`, pre-existing, unowned). Not
   touched, not referred further than the F5 seat already referred it.

## 7. GATES — AFTER EACH ACT

| gate | after ACT A | after ACT B |
|---|---|---|
| `python3 -m acceptance.runner` | **GREEN** 7/7 | **GREEN** 7/7 |
| `python3 release_manifest_check.py` | **PASS** — 38/40 coherent, **2 sealed-lag** | **PASS** — **40/40, 0 sealed-lag** |
| `python3 release_contract.py check` | **PASS** `cde9f70a49b6` | **PASS** `cde9f70a49b6` |
| `test_movers_transition.py` | **39/39** | — |
| `ui/tests/movers.test.js` | **66/66** | — |
| `invariant_proof.py` | **28/28** | — |
| book B3 certification | — | **PASS, every field** |

## 8. OPEN, REFERRED TO THE OWNER

1. **The in-`ev()` structural cure** — the durable, strictly larger fix for the same defect class.
   Modernisation programme; needs its own prereg.
2. **`ship_gates_check.py:49`'s hardcoded `RA`** — the suite cannot run on this box. Standing P1,
   reported by the bake and again here; deliberately not edited by either.
3. **The re-seal instrument's unreachable failure diagnostic** — P2, recorded above.
4. **`r15_ladder_survival_proof.py`** — cannot run, pre-existing, unowned.
5. **The `withPhantom` extension** from the F5 act — still one line to revert if unwanted.
