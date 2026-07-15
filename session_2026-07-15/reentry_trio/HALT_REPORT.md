# RE-ENTRY TRIO — HALT & REPORT (measured, not committed)

**Status:** HALTED at the measurement rung. No shared artifact was committed. Working tree restored to
clean base (store `340a7a32`, board `dc43d602`, `expected_boot`/`book_stable_seal` untouched). All numbers
below are from clean runs on the STRICT base pin.

## Base pin (verified)
- rl_model-pin build head `1073f6336ba492316f3921776dc44f41d3ecbefb` — full-URL `ls-remote` on
  `claude/rl-model-pin-assertion-sg5hxv` MATCHES. Branch re-rooted onto it. Base bootstraps green
  (engine `fc7045d6`, store `340a7a32`, board `dc43d602`, config `c2d233ae`; five guards' inputs pinned).

## The store edit (applied to the SOURCE, then reverted)
Per the ruling (item 108a / register 10a; fields per item 17 ii): record the LATER (SSP) entry.
- Flynn Perez:      ND p35 (2019)  -> SSP 2025, pick None, `_pickless` True, `_draft` SSP
- Lachlan McAndrew: MSD p12 (2021) -> SSP 2024, pick None, `_pickless` True, `_draft` SSP
- Mark Keane:       IRE (2018)     -> SSP 2022, pick None, `_pickless` True, `_draft` SSP

Store md5 `340a7a32 -> b1fd0bce`. Board (rebuilt, deterministic) `dc43d602 -> 800d0399`. Engine UNTOUCHED.

## THE FINDING — the ruling's premise is contradicted by measurement
The ruling (item 11 / 108a) predicted: **"McAndrew's relabel is pool-neutral post-11(a); residual cost
≈ Perez's ~7 rows."** The measured reality is the **inverse**:

| member | store change | v-movers it causes | own value |
|---|---|--:|---|
| Flynn Perez | ND -> SSP | **0** | 13 (unchanged) |
| Mark Keane | IRE -> SSP | **0** | 2155 (unchanged) |
| Lachlan McAndrew | MSD -> SSP | **106** (all of them) | 1232 (unchanged) |

- **All 43 material (>=5%) movers are MSD players.** The other 44 movers are hairline float ripple
  (|d|<=3 num-SCAR). Net **+30** num-SCAR. Trio own values do not move (the engine's
  `PRESENT_ID_OVERRIDES`, `_L5_PICKLESS` default-ON, already SSP-prices them at load).
- **Driver:** `rl_model.py:727` builds the pickless PEDESTAL by pooling players **by type**. Removing
  strong performer McAndrew from the MSD type-cohort shifts **`PICKEQ['MSD']` 60 -> 90** — a large
  flattening of the MSD pedigree anchor. Low MSD players rise (Coe +166%, May +32%), high ones fall
  (Newcombe -327/-8%, Noble, Hall, D'Ambrosio, Durham, Peatling).
- **Why the ruling's estimate was wrong:** item 11's "pool-neutral" analysis only accounted for the
  **L4 GBM training pool** (MSD-excluded, and frozen since the q97m freeze). It did **not** account for
  the **PICKEQ pickless-pedestal pool** (line 727), which L4 does not touch. So McAndrew is pool-neutral
  for L4 but NOT for the pedestal — that is the whole 106-mover ripple.
- **Perez's predicted "~7 rows" is actually 0** — the PVC/`hist` cohort he leaves is frozen on the
  shipped board (fits only run under RL_PVCFIT), so his exit moves nothing. Keane's IRE pedestal (92)
  is unchanged by his exit.

## Why I halted rather than committed
1. The directive's own stop-rule: **"if an engine change is genuinely required, HALT and report."**
   Honoring the ruling's *stated intent* (McAndrew pool-neutral, ~7 movers) is **not achievable
   store-only** — making him SSP in the store necessarily removes him from the MSD pedestal cohort.
   Matching the ruled intent would require an ENGINE change (hold the named re-entrants out of the
   pickless PICKEQ pedestal too, SSP-parity with the item-11a MSD ruling) — inside the "engine UNTOUCHED"
   fence, so it needs the owner's word.
2. The row count is **~15x** the ruled estimate (106 vs ~7) — past the directive's `>2x` flag — and the
   direction/magnitude touch the owner's exact item-11 concern ("McAndrew should have no bearing on
   Emmett's value" — Emmett is MSD). This is his call to make at a sealed-reads viewing, not to ride
   silently into a board.

## Options for the owner
- **(A)** Accept the store-only correction as-is: the 43-row MSD-pedestal reprice is the mechanical
  consequence and is arguably item-11-aligned. Proceed to gates/candidate on the owner's word.
- **(B)** Apply Perez + Keane only now (both 0-movers — makes the store the source of truth for them
  with zero board movement) and defer McAndrew pending the pedestal ruling.
- **(C)** Full trio + an engine guard keeping the named re-entrants out of the pickless PICKEQ pedestal
  (true ~neutral, ~a handful of movers) — an engine change; needs explicit authorization (violates the
  fence as written).

Evidence: `measurement/AFFECTED_ROWS.md` (full named list), `board_base_dc43d602.json`,
`board_trio_800d0399.json`, `board_{perez,mcandrew,keane}only.json`, `edit_store.py`, `reseal_book.py`.
