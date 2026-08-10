# THE 3-AXIS PROBE (RULING 2.4) INSTRUMENTS — landed 2026-08-10

The probe that asked whether a **three-axis** stage-6 surface (log-pick x position class x
demonstrated performance on `sa`) delivers materially more of the measured development
residual than the shipped **two-axis** surface, while holding the already-priced cells at
zero. #334 landing comment **5235775326**. Verdict: **no material gain** — every three-axis
variant is worse than the shipped control, and all of them are newly bound by the declared
picks-41-64 taper.

## PATH CONVENTION

`probe3ax.py` hard-codes the scratchpad root as `S` and reads `S + '/s6_rows.json'`.
`probe3ax2.py` and `probe3ax3.py` do the same. `probe3ax4.py` re-executes its predecessors as
text (`open(S + '/probe3ax2.py')`, `open(S + '/probe3ax3.py')`) to inherit their kernel build
verbatim, and writes `S + '/probe3ax4.json'`. **Keep all four together and do not renumber
them** — passes 3 and 4 will not run otherwise.

No engine load. `numpy` only. Nothing is written outside the scratchpad.

## WHAT THIS SET CONSUMES, AND WHERE IT LIVES

`s6_rows.json` — md5 `9015cda31efc25bd471dcc74fdc265fa`, 3.6 MB, the stage-6 per-row emission
(`key/C/Y/N/pos/pk/nd/v0/price/F` and `sa`). Session scratchpad root; byte-identical to
`s6rows_branch.json`. **NOT on main**, and not landed here (size; it is the shared input of
four acts — see `ruck_act_instruments_2026-08-10/README.md` for its provenance and the emitter
that produced it, `emit_matrix_338.py`, landed at `docs/evidence/noarb_338_2026-08-06/`).

## CONVENTIONS — TAKEN VERBATIM FROM THE STAGE-6 CONFORMANCE REPAIR

Quoted from `probe3ax.py`'s own header (they come from `teach_g6.py` / `probes_g6.py`, which
are NOT landed here — they belong to the stage-6 repair act):

- population `s6_rows.json`, nd, pk 1..64, classes 2004-2022, `N==1` for the kernel (n=414),
  `N` 1..3 pooled on the continuous clock for the fade;
- estimand: the REGISTERED F (fixed career-year-4 discounted at 1.0939); `r = F - price`;
  every local read is the value-weighted residual ratio `loc_delta = sum(K r)/sum(K price)`;
- eff-n on the INFLUENCE weight (kernel x price), threshold 35, bandwidth grown x1.15;
- a single declared conservation scalar `Z` on the taper-supported bonus population;
- declared pick taper 34->48, declared age taper 18->19, KPD excluded from the base kernel.

## RUN ORDER AND WHAT EACH PASS FOUND

1. `probe3ax.py` -> `probe3ax_out.txt` — pass 1. The **control reproduces the shipped
   two-axis teach exactly** (`g6_table` md5 `61450f0b`, Z = 0.772923, kappa = 0.912673,
   Wmax 0.4193 -> 1.024847). That reproduction is this probe's gate: it is what licenses the
   comparison. Three-axis variants A/B/C score 0.2557 / 0.3895 / 0.3129 — all worse.
2. `probe3ax2.py` -> `probe3ax2_out.txt` — pass 2. Thin-cell CIs (median 90% CI width
   **3.39 x D1 for three-axis vs 2.30 x D1 for two-axis** — the width is the finding),
   controls E and F, seam proxy, fallers, taper sensitivity.
3. `probe3ax3.py` -> `probe3ax3_out.txt` — pass 3. Six three-axis specs plus two controls.
4. `probe3ax4.py` -> `probe3ax4_out.txt`, `probe3ax4.json` — pass 4. Seam proxy,
   tail-vs-typical, taught-vs-measured at the registered cells. Final verdict.

`PROBE3AX_PROGRESS.md` is the act's own step log (steps 1-7).

## WHAT IS DELIBERATELY NOT HERE

`teach_g6.py`, `probes_g6.py`, `measure_g6.py` and `g6_table.json` are the **stage-6
conformance repair's** instruments, not this probe's. This probe only reads their conventions
and reproduces their shipped output as a control. They stay unlanded — see the INDEX at
`docs/evidence/INSTRUMENTS_INDEX_2026-08-10.md`.
