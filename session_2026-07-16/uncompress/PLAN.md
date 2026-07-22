# PLAN — LEG B: UN-COMPRESS THE OUTPUT→PRICE MAP (`RL_UNCOMP`)

Build session artifact (NOT a docs/ pack doc — CORE: builds never author docs).
**Design of record (READ IN FULL, consumed):** `docs/MEMO_LEGB_functional_form_2026-07-16.md` — decisions (a)–(e) are settled; this leg IMPLEMENTS, it does not redesign.
Directive: `docs/DIRECTIVE_LEGB_uncompress_2026-07-16.md`. Spec: `docs/SPEC_PVC_FLEX_CHAPTER_v1_2026-07-16.md` §3 Leg B (v1.2). Acceptance: `docs/acceptance_v1_17.json` (`leg_b.*`).
Branch `claude/legb-output-price-decompress-3vo8y1`. **AMENDED PLAN — supervisor prescreen PASS with two amendments (register items 211–213), folded in (§2 site 7, §3 additive captain all-six, §13 flags). Segment 1 close: implementation runs in a FRESH chat per `docs/DIRECTIVE_LEGB_segment2_2026-07-16.md` (§14).**

---

## 0 — GUARDS ON ENTRY / BASE PINS (verified, recorded, cited)

- **Engine/store base — STRICT ✓**: `git ls-remote … claude/iso-corr-evidence-fade-jnda76` = `8b8ab7d3772d1d5b653be01a2d76834ea6207b8b` == pinned `8b8ab7d`. Branch reset to this SHA (candidate line continues from `8b8ab7d`). Identity **at the base** (`data/expected_boot.json`): engine_head **`a83c9f6d`** · board **`8d90c9ac`** · store **`b1fd0bce`** · rl_model **`f79fc740`** · config **`c2d233ae`** — **byte-identical to the memo's Leg-A landed state** (engine a83c9f6d · board 8d90c9ac · store b1fd0bce · config c2d233aec104). No HALT condition.
- **Docs base — at/after ✓**: `git ls-remote … main` = `bfbd8566` (at/after `fcbd03a`). `git diff --name-only fcbd03a..main` = **2 files, ALL `docs/`** (`DIRECTIVE_LEGB_uncompress_…`, `OPEN_ITEMS_REGISTER`) — docs-only rule holds. FEED docs fetched from `origin/main bfbd8566`.
- **Guard 5 (boot)**: store `b1fd0bce` == pinned. **Store is NOT touched by this job** (FENCE) — it stays `b1fd0bce` at the head.

## 1 — PRE-VIEW HASH MANIFEST (audit #16/#22/#45 · acceptance `leg_b.preview_hashes`)

**Recorded BEFORE any candidate metric is computed or rendered.** md5 as fetched at the docs base (`origin/main bfbd8566`):

| artifact | md5 | bytes |
|---|---|---|
| `docs/MEMO_LEGB_functional_form_2026-07-16.md` | `3624ce55891f8c40fd561a9a82ab2149` | 11354 |
| `docs/acceptance_v1_17.json` | `c3d5008229d58fab5a67c62085d38314` | 41663 |

Any post-view mutation of either artifact **HALTS the ladder**. These hashes are the leg's pre-view seal.

## 2 — SITE ENUMERATION (memo §2 / §4 — the `raw_ev`/`posval` site family)

**The conversion the map wraps.** `posval(x) = S_SH·log(1+exp(x/S_SH))` (`rl_model.py:307`, S_SH=3.0) is the concave "position value above replacement" — the output→price map (§1 defect). It is reached on the board path as:

```
ev → _prod_path = raw_ev·iso_eff  (_merged_recover.py:1142)
   → price6/b6 → MA.proj_from_peak (=_proj_w4) / MA.prod_floor (=_prod_floor_w4)
   → MA.posval( lev + capt_prem(lev) − REPL[pos] )
```

`_merged_recover.py` rebinds `MA.proj_from_peak=_proj_w4` (`:748`) and `MA.prod_floor=_prod_floor_w4` (`:768`). The W4 versions carry the **proven / ctx-on** population; they **delegate to the original `rl_model.py` functions** for synths, ctx-None, and — critically for the **≤22 Reid extension** — **unproven/young players** (`_prod_floor_w4:758` delegates when `n<PROVEN_N`). So the map MUST wrap posval at **both** families to cover the whole population at both legs. Wiring at every site (synths included → byte-identical, they carry no fade/blend) is the Leg-A doctrine.

| # | file : current line | function | leg | wrapped expression | note |
|---|---|---|---|---|---|
| 1 | `_merged_recover.py:743` | `_proj_w4` (k=0) | **current-year** | `MA.posval(base−MA.REPL[g0])` | proven/ctx-on forward projection, present year |
| 2 | `_merged_recover.py:744` | `_proj_w4` (k≥1) | **projected-year** | `MA.posval(base−MA.REPL[gg])` over `fut` blend | future years, per-year `lev`/E |
| 3 | `_merged_recover.py:766` | `_prod_floor_w4` (k=0..H, H≤3) | **current + near-projected** | `MA.posval(lev+capt−MA.REPL[g])` | proven demonstrated-production floor |
| 4 | `rl_model.py:356` | `proj_from_peak` (k=0) | **current-year** | `posval(base−REPL[g0])` | delegated path: synths + ctx-None |
| 5 | `rl_model.py:357` | `proj_from_peak` (k≥1) | **projected-year** | `posval(base−REPL[gg])` over `fut` | delegated path |
| 6 | `rl_model.py:369` | `prod_floor` (k=0..H) | **current + near-projected** | `posval(lev+capt−REPL[g])` | delegated path: **UNPROVEN/young floor — the Reid side** |
| 7 | `rl_model.py:559` | `_nv_bwd` (backward per-pick ruler) | — | `posval(b2+capt_prem(b2)−(REPL−PVC_REPL_BUF))` | **NOT WIRED** (AMENDMENT 1, item 211) — a backward MEASUREMENT ruler on realised careers, not a forward output→price valuation leg (outside memo §4's family). Wrapping it would move `_natcv34` → PICKEQ → pathway `_eff` (board-reaching) through an unruled channel and pre-empt Leg D's derivation; w=s·E has no coherent year on a career-realised measure. Whether the backward ruler carries the cured map is QUEUED FOR THE LEG-D MEMO (item 204's life-path measurement decides it). |
| dx | `_ov_final.py:37` | diagnostic `approx` | — | raw `posval(...)` in a print-only analysis script | **non-board** (not imported by any builder, not gated, not re-run). Analogue of Leg A's `_ov_angleA.py` diagnostic. **NOT wired — RATIFIED at prescreen** (flag (f)); out of the live board/measured path. |

**Both legs, per site:** at each posval site the k=0 term is the **current-year** leg and each k≥1 term is a **projected-year** leg (`proj_from_peak` runs k=0..17; `prod_floor` runs k=0..H≤3). Each leg carries **that year's own E** (§3). This is the same "current-year AND projected-year" split Leg A's directive named for `iso_eff`.

## 3 — ρ FEED (memo §2.1 / §3 · directive items 2–3) — the exact level function + V_ref construction

- **E (evidence weight)** — `w = s·E`, E = `_ev_qual(p, Y)` (`_merged_recover.py:182`; effective qualifying seasons), **τ = 1.1** = `_EVW_TAU` — the SAME family Leg A's fade rides. Per leg, `Y` = the year being valued (k=0 → 2026; k≥1 → 2026+k). `_ev_qual` counts qualifying seasons with `year≤Y`; no future seasons exist in the store, so E is **flat into the projected years** = the player's current demonstrated evidence — which is exactly the Reid mechanism (a young demonstrated over-performer carries real `w>0` on his projected years the moment evidence exists; no young special-case, no second map).
- **ρ numerator = the SMOOTHED demonstrated level, NEVER single-season** (memo §2.1). Per leg it is the level already computed at that posval site: k=0 = the `level_now`-derived `lev` (`level_now(p)=_dev_advance(level_demo(p),p)`, `rl_model.py:296/234` — multi-season, robust-baseline, injury/thin-filtered); k≥1 = the projected `lev = lp·frac(ag,pa)` rolled forward along the dev curve. `lp` derives from `level_now`, so every leg's `lev` is in the `level_demo/level_now` family by construction. An LTI/injured season does not read as output collapse.
- **V_ref (ρ's positional reference)** — from the **demonstrated-proven population per position**: `L_ref[pos]` = a robust central level (proposed **median**) of `level_now(p)` over `{ p : MA.gfut(p)==pos, _nqual(p,2026) ≥ PROVEN_N (=4), p in valuation scope }`. Built **load-time** (one pass, like the REPL derivation / the calibration pool). Reference **value** `V_ref[pos] = posval(L_ref[pos] − REPL[pos])`.
- **The map** (memo §2, κ = 1; **captain PRESERVED ADDITIVELY at all six sites — AMENDMENT 2 as corrected, supervisor item 213**). ρ is **pre-captain**. Per leg:
  - `ρ_k = lev_k / L_ref[pos]`; target `t_k = V_ref[pos] · ρ_k^κ`, κ=1, `V_ref[pos] = posval(L_ref[pos] − REPL[pos])`.
  - `v0_k = posval(lev_k − REPL[pos])` — the **captain-free** production value.
  - `v0′_k = v0_k^(1−w_k) · t_k^(w_k)` — the log-space blend of the captain-free price toward the output-proportional price.
  - `δ_k = posval(lev_k + capt_prem(lev_k) − REPL[pos]) − posval(lev_k − REPL[pos])` — the **unchanged** L-CAPTAIN increment.
  - **`v′_k = v0′_k + δ_k`** — blend the production side, add the captain premium back on top.
  At `lev=L_ref` (ρ=1) the production blend is identity; above it the concave `v0` is lifted toward the linear-in-output target (β↑); κ stays 1 (the dial is `s`). **L-CAPTAIN untouched by construction** (δ byte-identical pre/post map). All six sites fold `capt_prem(lev)` into the argument (`rl_model.py:355/369` · `_merged_recover.py:742/766`), so the additive construction is applied at **every** site (1–6); the prescreen's "1/2/4/5 captain-free" is superseded (item 213). **Self-test:** δ (captain increment) byte-identical pre/post map over a sampled captain set, at all six sites.

## 4 — ONSET-RAMP WIDTH (memo §2.2 · directive item 4)

`w_k = s · E_k · ramp(m_k)`, with `m_k = lev_k − REPL[pos]` (above-replacement margin, avg-points) and **`ramp(m) = clip(m/Δ, 0, 1)`, Δ = 6.0 avg-points (DECLARED)**. w ramps continuously from 0 at/below the replacement bar to full over 6 avg-points above it. **Rationale:** clears the softplus knee (Δ ≈ 2·S_SH = 6.0, so the map stays identity through the region where `posval` is not yet ≈linear), matches the engine's ~5-unit smooth-onset idiom (`_est` uses `/5` ramps, `:369–372`), no cliff between sub-bar and above-bar players (audit #28). **No age gates anywhere** — responsiveness is continuous in evidence (audit #29; no birthday cliffs by construction). Δ is owner/supervisor-tunable at this checkpoint.

## 5 — CONSERVATION PLACEMENT (memo §3 · directive item 4)

- **Production-side, load-time, PER POSITION, ACROSS ALL YEAR-DEPTHS.** A per-position renorm factor `C[pos]` on the **production-side** value, computed load-time so that Σ(production value over the position's whole population, all year-depths) is unchanged by the map (an explicit budget transfer, not a vanish/create). Applied where the production scale already lives — the `_SCALE` production-scale family (`_merged_recover.py:274`) / the production-side term — **production-side only**.
- **NEVER per-(pos, year-depth) cell** — the pre-sim proves cell conservation makes the gate arithmetic a tautology (ratios frozen at the breach); the path under 1.30 REQUIRES value to flow across year-depths (memo §3).
- **Pedigree pedestals + iso premiums NOMINAL** — not renormed (a global all-value scale would inflate unearned pick priors and walk the census gauge, audit #15).
- **The transfer is EXPLICIT in the whole-system SCAR ledger** (players + held picks + every derived adjustment), reconciling to zero unexplained residual at the acceptance tolerances (`abs 200` / `rel 0.0005`).

## 6 — KILL-SWITCH `RL_UNCOMP` (directive item 5 — the RL_ISOFADE pattern verbatim)

`_UNCOMP = os.environ.get('RL_UNCOMP','1') != '0'` — **default ON**; a **DECLARED kill-switch, NOT a manifest dial** (the `RL_ISOFADE`/`RL_EVW`/`RL_EO2` pattern, confirmed in `data/expected_boot.json` notes: declared exceptions are absent from `data/model_config.json`, so **config `c2d233ae` is UNMOVED** — and the FENCE's "config manifest untouched" holds). Gates the map at **all wired sites** AND the load-time reference/renorm construction. **`RL_UNCOMP=0` ⇒ board `8d90c9ac` BYTE-EXACT** (config_sha256 unmoved). Proven by a **dev-shell** gated A/B board build (the OFF board is built with no `RL_CONFIG_MODE`, so the manifest enforcement never sees the override). Kill-switch regeneration matrix: **`RL_UNCOMP × RL_ISOFADE` (all four)** cold-regenerate from the authored store and hash-equal runtime-switched output (acceptance `killswitch_matrix`; memo §7 separability).

## 7 — THE s DIAL: FROZEN ESTIMATOR + GRID + DETERMINISTIC SELECTION (directive item 6 · acceptance `s_dial_selection` / `beta_proven27`)

- **FROZEN estimator (declared here, before build):** `fit_beta` from the item-165 scoring tool `session_2026-07-15/book_calibration/calibrate.py:40`, verbatim — **β = OLS slope of ln(price) on ln(realised-output)** (`np.polyfit(ln o, ln p, 1)`), **CI = 1000-sample bootstrap percentile**. **Sample:** proven-27+ contributors (`age ≥ 27`, the item-131 low-runway-confound regime), same `(output o, price p)` construction as the tool. **Weighting:** unweighted log-log OLS. **Precision gates (acceptance):** max CI width **0.35**, min effective n **120** — imprecision cannot pass the gate (audit #13). Method/sample/weighting/CI are FROZEN across every grid point.
- **Grid** = `{0.45, 0.50, 0.55, 0.60}` (acceptance). Sweep `s` in **dev-shell** via a build env (`RL_UNCOMP_S`); rebuild the candidate board/book at each grid point; measure **β_c** (map OFF, ≡ β at s→0) and **β(s)** per point, printing **β point + CI + effective n**.
- **Selection rule (deterministic, pre-declared, never result-conditioned):** **s = the SMALLEST grid value whose β point ≥ 0.85.** (Design target, not verdict: memo §2 algebra β_eff=(1−w)β_c+w with β_c≈0.683 ⇒ w≥0.527 ⇒ s≈0.53 — the frozen estimator returns the real number.) **If NO grid value clears ⇒ HALT-AND-ASK with the measured table** (do not extend the grid). The selected `s` is then hard-coded as the canonical constant (τ-style literal); `RL_UNCOMP=0` turns the whole map off.

## 8 — HYGIENE RIDER (spec §4 · directive item 7 — delete-don't-disable)

**DELETE the dead `if not _EVW:` discrete-regime branch** — in `_coreM1`, **current lines `375–389`** (the directive/spec cite the pre-Leg-A range **`358–372`**; Leg A's added iso code, `:287–313`, shifted it +17, and Leg A's PLAN Task 4b listed but did **not** execute the cut — it is still present at the base). The pre-EVW four-regime path is superseded by the continuous evidence weight (`:390–398`) and reachable only with `RL_EVW=0` on a code path the live `_inferM1` no longer routes through here. **Verify dead before cutting** (RL_EVW=0 routes elsewhere; the live `_inferM1` does not reach this branch); **delete with an OBITUARY** (SSI/CORE rule 7). The unrelated live one-liner `if not _EVW:` at `:192` is OUT of scope.

## 9 — DELIVERABLES (committed artifacts; a return without its SHA is incomplete)

Candidate PR continuing the candidate line from `8b8ab7d`; per-task commits; **PLAN first (this commit)**. Then:
- **A/B identity proof:** `RL_UNCOMP=0` board md5 == `8d90c9ac`.
- **Frozen-suite measurements:** β_c and β(s) per grid point (estimator + CI + effective n printed) · ≤22 slope vs 0.111 · English/Briggs (captain IN; base at `8d90c9ac` = 1.766×, must stay ≥1.75) · G-COHORT y4/y5/y6 via the frozen July-8 construction (`ship_gates_check._b1_july8`) + the committed row-level fixture · L-SMOOTH census at the declared threshold · census-v2 global gauge (≤ +15,612) + the predeclared cells.
- **Whole-system SCAR ledger** (players + held picks + adjustments; tolerances per acceptance).
- **Donor-side mover report** (memo §8): top-30 proven markdowns — name · Δ · ρ · w · earned/prior split (owner-viewing quality).
- **Value-flow + R104.8 decomposition** (item-130 standing check): ΣΔ · cohort distribution · over-performer scan · every young trim decomposed, production components byte-identical or HALT.
- **The w-export** (item 204): per-player-year evidence weight `w` + earned/prior decomposition, one committed artifact (Leg D consumes it). **Schema:** CSV `stable_player_id, player, pos, year, leg(current|projected+k), E, rho, w_full=s·E, ramp, w=s·E·ramp, earned_component, prior_component` — one row per player-year-leg.
- **Gate snapshot by engine hash** + panel/self-test per the standing harness (self-tests: ρ/w identity at zero-evidence; RL_UNCOMP=0 site-level byte-exact; monotone onset ramp; **δ captain increment byte-identical pre/post map at all six sites** — L-CAPTAIN preservation, item 213).

## 10 — DERIVED-ARTIFACT REGENERATION (stamped, S1)

`bootstrap.sh` → `rl_export.py` (rebuild board) → re-pin `data/expected_boot.json` `engine_head`+`board`+`panel` in the engine-moving commit → `s4_matrix_M1v7.py` rebuild + re-seal (G-BOOK; the map moved) → `run_panel.sh`/`PANEL_EXPECTED.txt` if any of the 10 named move → `ship_gates_check.py` GREEN. **Store UNCHANGED `b1fd0bce` · config UNMOVED `c2d233ae` · `RL_PVCFIT` stays OFF (Leg D untouched).**

## 11 — TIME (two segments; confirmed, not flagged)

- **Segment 1 (to the checkpoint):** plan + hash manifest — **this commit, ~20–30 min**, then HALT.
- **Segment 2 (on the PROCEED word):** site implementation ~1.5–2.5 h · frozen-suite measurement + s-selection ~1–1.5 h · deliverables (ledger, movers, decomposition, w-export) ~1–1.5 h · return ~30 min.
- Total **4–7 h wall-clock build time** (directive band; confirmed). Actual reported in the RETURN; flag if >2× / <½×.

## 12 — FENCE (self-check)

**IN:** engine files at the enumerated sites (`_merged_recover.py` sites 1–3 + reference/renorm/kill-switch/hygiene; `rl_model.py` sites 4–6 + the `posval`-map helper) · the kill-switch `RL_UNCOMP` · the deliverable artifacts · derived-artifact regeneration (board/matrices/pins, stamped). **OUT (touch = HALT):** the STORE `rl_model_data.json` (untouched, `b1fd0bce`) · docs/ (never authored) · ui/ · the acceptance JSON · gate/guard code (`ship_gates_check.py`, `boot_guard.py`, **the config manifest `data/model_config.json`**) · any other leg's machinery · any retuning of Leg A's τ. Mid-flight scope growth = a NEW directive (S2).

## 13 — SUPERVISOR PRESCREEN — OUTCOME: PASS WITH TWO AMENDMENTS (register items 211–213)

The plan passed the supervisor prescreen (sites · ρ feed · hashes · conservation placement). Amendments 1 (site 7 `_nv_bwd` NOT-WIRED, §2) and 2 (additive captain, §3) are folded in above. Flag dispositions:
- **(a) ρ per-leg `lev`** (k=0 = `level_now`-derived; k≥1 = projected `lev`) — **RATIFIED AS READ.**
- **(b) V_ref construction:** `L_ref[pos]` = **MEDIAN** `level_now` over the demonstrated-proven pop (`gfut==pos` ∧ `_nqual≥4`); `V_ref[pos]=posval(L_ref−REPL)` — **RATIFIED AS READ.**
- **(c) onset width Δ = 6.0** avg-points — **RATIFIED AS READ.**
- **(d) captain — RULED (item 213): ALL SIX captain sites.** Preserve captain ADDITIVELY (`v′=v0′+δ`, §3) at every posval site carrying `capt_prem`; ρ pre-captain; δ byte-identity self-test over all six sites. L-CAPTAIN untouched by construction; English/Briggs measured captain-IN. (The prescreen's "1/2/4/5 captain-free" was superseded after the code showed `base=lev+capt_prem(lev)` feeds every wrapped posval — `rl_model.py:355` / `_merged_recover.py:742`.)
- **(e) conservation home:** per-position production-side renorm `C[pos]` in the `_SCALE` production-scale family (§5) — **RATIFIED AS READ.**
- **(f) `_ov_final.py:37`** diagnostic NOT wired (non-board) — **RATIFIED AS READ.**

## 14 — CHECKPOINT (owner-ruled 2026-07-16) — CLEARED; SEGMENT 1 CLOSED

Prescreen **PASSED WITH TWO AMENDMENTS** (register items 211–213), both folded in above. This **amended** PLAN commit closes Segment 1. Per the supervisor ruling (supersedes the earlier PROCEED, item 212): **implementation does NOT run in this chat** — a fresh chat runs Segment 2 from this committed plan under `docs/DIRECTIVE_LEGB_segment2_2026-07-16.md` (already corrected to all-six captain sites). This chat retires after this commit + push + the SHA return.

**Pre-view seal holds:** memo `3624ce55891f8c40fd561a9a82ab2149` · acceptance `c3d5008229d58fab5a67c62085d38314` re-verified unchanged at the latest docs base `main 64b6585`. Base pins and FENCE unchanged; store untouched (`b1fd0bce`).
