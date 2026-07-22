"""JOB 2 — CIRCULARITY, QUANTIFIED. Reads out/per_entrant.json (emitted by emit_matrix.py).

PRINCIPLED PRIOR-SHARE METRIC (why not a single value-%): the engine exposes TWO pick-driven priors —
 (i) the V0 POLE (v0_start, _merged_recover.py:1157) that a ZERO-EVIDENCE entrant is priced ~100% by
     (subagent-confirmed: 0 games -> sitout_ev -> lam=0 -> value == v0_start), and
 (ii) the PEDIGREE PAR (_par_prior) blended by pw=_ev_pw (:186-189), which is GATE*FADE = 0 at zero
     evidence (gated OFF for the unqualified) rising then fading to residual 0.11.
A precise value-% earned/prior split is NOT yet computable: the item-204 earned/prior export (Leg B
deliverable) DOES NOT EXIST in the code yet (subagent-verified). So the robust, model-light statement of
"how much of the anchor is pick-prior vs demonstrated evidence" is the FOOTBALL EVIDENCE PRESENT AT THE
ANCHOR DATE (end of career-year 1 = the derivation window), tiered on EXACT games (model-free integers):
 * >=90% prior  <=> 0 games by end-yr1        = the PURE V0 POLE (zero football evidence) = the tautology core.
 * >=75% prior  <=> 1..10 games               = below the engine's qualifying bar (Q0=11); prior dominant.
 * >=50% prior  <=> 11..21 games              = one partial-to-full qualifying season; prior still material.
Supporting columns (value-space corroboration): mean pw[1], MEDIAN anchor/v0 ratio (~1.0 for pure poles).
Emits JSON + a markdown table. Proposes 3 CUT OPTIONS (rows + marginal names). Decides NOTHING.
"""
import json, collections, statistics
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'
recs = json.load(open(BASE + '/out/per_entrant.json'))
BANDS = ["1-3", "4-7", "8-12", "13-20", "21-27", "28-35", "36-48", "49-99"]

def pool(dtype=None):
    return [r for r in recs if r['incurve'] and r['pick'] and 2004 <= r['year'] <= 2024
            and (dtype is None or r['type'] == dtype)]

def eq1(r): return r['eq']['1']

# Tiers on EXACT games by end-of-yr1 (model-free integers; the engine's qualifying bar is centred at 11 games,
# Q0=11 — a sub-11-game season "counts ~0", _merged_recover.py:180). A rookie has at most ONE season by then.
#  >=90% prior  = 0 games      -> the anchor IS the pure V0 pole (zero football evidence) = the tautology core.
#  >=75% prior  = 1..10 games  -> below the qualifying bar (sub-qualifying sample; prior still dominant).
#  >=50% prior  = 11..21 games -> one partial-to-full qualifying season (prior still material at the yr1 anchor).
def tier(r):
    g = r['games_yr1']
    if g == 0: return 'ge90_pureV0pole'
    if g < 11: return 'ge75_priordom'
    if g < 22: return 'ge50_priormaterial'
    return 'evidence_bearing'

def band_table(P):
    out = []
    for b in BANDS:
        g = [r for r in P if r['band'] == b]
        if not g: continue
        tc = collections.Counter(tier(r) for r in g)
        ge90 = tc['ge90_pureV0pole']
        ge75 = ge90 + tc['ge75_priordom']
        ge50 = ge75 + tc['ge50_priormaterial']
        ratios = [r['anchor'] / r['v0'] for r in g if r['anchor'] and r['v0']]
        out.append(dict(band=b, n=len(g),
                        ge90_count=ge90, ge75_count=ge75, ge50_count=ge50,
                        ge90_pct=round(100 * ge90 / len(g), 1),
                        ge75_pct=round(100 * ge75 / len(g), 1),
                        ge50_pct=round(100 * ge50 / len(g), 1),
                        mean_pw1=round(statistics.mean(r['pw']['1'] for r in g), 3),
                        median_anchor_over_v0=round(statistics.median(ratios), 3) if ratios else None))
    return out

P_all = pool(); P_nd = pool('ND'); P_rd = pool('RD')
tbl_all = band_table(P_all); tbl_nd = band_table(P_nd)

# ---- CUT OPTIONS ----
# Cut A: drop zero-evidence anchors (E_q[1]==0) — the pure V0 pole (tautology). NOTE's "delete the circle at entry".
cutA = [r for r in P_all if r['games_yr1'] == 0]
# Cut B: honest end — re-anchor at end of career-year 4; keep only entrants with >=2 qualifying seasons by C+4.
def eqk(r, k): return r['eq'][str(k)] if str(k) in r['eq'] else r['eq'].get(k)
cutB_keep = [r for r in P_all if r['eq'].get('4', 0) >= 2.0]     # evidence-bearing survivors by yr4
cutB_drop = [r for r in P_all if r not in cutB_keep]
# Cut C: two-ends — entry end = pick pricing directly (no loop) for E_q[1]==0; evidence end = production of
# the E_q[4]>=2 survivors. Report both endpoint pools (no rows dropped; the curve is the line between).
cutC_entry = cutA
cutC_evidence = cutB_keep

def marg_names(rows, key, n=8):
    rows = sorted(rows, key=key)
    return [(r['player'], r['year'], r['pick'], round(key(r), 3)) for r in rows[:n]]

# marginal rows for Cut B: entrants JUST below/above the 2-qual-season bar at yr4
near = sorted(P_all, key=lambda r: abs(r['eq'].get('4', 0) - 2.0))[:12]

out = dict(
    _doc="Job 2 circularity: prior-share by football evidence at the end-of-yr1 derivation window (E_q[1]). "
         "The zero-evidence tautology's size = the E_q[1]==0 (pure V0 pole) count. Value-% split awaits item 204.",
    pool_sizes=dict(all_incurve=len(P_all), ND=len(P_nd), RD=len(P_rd)),
    band_table_all=tbl_all, band_table_ND=tbl_nd,
    totals_all=dict(
        n=len(P_all),
        ge90_pureV0pole=sum(t['ge90_count'] for t in tbl_all),
        ge75=sum(t['ge75_count'] for t in tbl_all),
        ge50=sum(t['ge50_count'] for t in tbl_all),
    ),
    cut_options=dict(
        A_delete_circle_at_entry=dict(
            rule="Exclude E_q[1]==0 entrants (zero football evidence by end-yr1; anchor == pure V0 pole).",
            n_excluded=len(cutA),
            per_band={b: sum(1 for r in cutA if r['band'] == b) for b in BANDS},
            marginal_names_lowest_pick=marg_names(cutA, lambda r: r['pick'])),
        B_honest_calibration_end_yr4=dict(
            rule="Re-anchor at end of career-yr4; keep only entrants with E_q[4]>=2 qualifying seasons (prior faded).",
            n_kept=len(cutB_keep), n_dropped=len(cutB_drop),
            kept_per_band={b: sum(1 for r in cutB_keep if r['band'] == b) for b in BANDS},
            marginal_near_2qual_bar=[(r['player'], r['year'], r['pick'], r['eq'].get('4')) for r in near]),
        C_two_ends=dict(
            rule="Entry end = pick pricing read directly for the E_q[1]==0 poles (no loop); evidence end = "
                 "production of the E_q[4]>=2 survivors; PVC = the line between (NOTE item 1).",
            entry_pool_n=len(cutC_entry), evidence_pool_n=len(cutC_evidence)),
    ),
    caveat="Exact value-% earned/prior decomposition is NOT yet computable: item-204 export (Leg B) not built. "
           "Evidence-at-anchor is the robust proxy; pw[1] and anchor/v0 are supporting, not a fitted split.",
)
json.dump(out, open(BASE + '/out/job2_circularity.json', 'w'), indent=1)

# markdown
L = ["# Job 2 — Circularity, quantified (evidence at the end-of-yr1 derivation window)", "",
     f"In-curve derivation pool (ND/RD, real pick, drafted 2004-2024): **{len(P_all)}** "
     f"(ND {len(P_nd)}, RD {len(P_rd)}).", "",
     "Prior-share proxy = football evidence (exact games) at the anchor date = end of career-yr1 (the derivation window). "
     "`>=90%` = 0 games = **pure V0 pole = the zero-evidence tautology**; `>=75%` = 1-10 games (< qualifying bar); `>=50%` = 11-21 games.",
     "", "## All in-curve entrants, by pick band", "",
     "| band | n | >=90% (pure pole) | >=75% | >=50% | mean pw[1] | median anchor/V0 |",
     "|------|---|-------------------|-------|-------|------------|----------------|"]
for t in tbl_all:
    L.append(f"| {t['band']} | {t['n']} | {t['ge90_count']} ({t['ge90_pct']}%) | "
             f"{t['ge75_count']} ({t['ge75_pct']}%) | {t['ge50_count']} ({t['ge50_pct']}%) | "
             f"{t['mean_pw1']} | {t['median_anchor_over_v0']} |")
tot = out['totals_all']
L += ["", f"**Whole pool:** pure V0 pole (zero-evidence tautology) = **{tot['ge90_pureV0pole']}** "
      f"({round(100*tot['ge90_pureV0pole']/tot['n'],1)}%), >=75% = {tot['ge75']}, >=50% = {tot['ge50']} of {tot['n']}.",
      "", "## Cut options (for the construction memo — decide nothing)",
      f"- **A — delete the circle at entry:** drop the {len(cutA)} zero-evidence poles (anchor == pure V0). "
      "Per-band counts in JSON.",
      f"- **B — honest-calibration end (yr4):** re-anchor at end-yr4, keep the {len(cutB_keep)} entrants with "
      f">=2 qualifying seasons; drops {len(cutB_drop)} (thin/washed-out). Prior faded out => independent curve.",
      f"- **C — two-ends:** entry end read from pick pricing for the {len(cutC_entry)} poles (no loop), evidence "
      f"end from the {len(cutC_evidence)} survivors' production; PVC = the line between.",
      "", "_Value-% earned/prior split awaits the item-204 export (Leg B, not yet built)._"]
open(BASE + '/out/job2_circularity.md', 'w').write("\n".join(L))

print("\n".join(L[:9]))
print("\nband | n | >=90pole | >=75 | >=50 | pw1 | anch/v0")
for t in tbl_all:
    print(f"{t['band']:7} {t['n']:4} {t['ge90_count']:5}({t['ge90_pct']:>4}%) {t['ge75_count']:5} {t['ge50_count']:5}  {t['mean_pw1']:.3f} {t['median_anchor_over_v0']}")
print(f"\nCut A drop={len(cutA)}  Cut B keep={len(cutB_keep)}/drop={len(cutB_drop)}")
print("wrote out/job2_circularity.{json,md}")
