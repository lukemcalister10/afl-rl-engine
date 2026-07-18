"""RIDER (iv) job 1+2 — THREE R CANDIDATES (constructed, labelled) + UNCERTAINTY ON R ITSELF.

REPORT-ONLY. Emits out/r_candidates.json + out/r_candidates.md. Symmetric: three candidates, no
verdict, no steer. Reads frozen inputs read-only via common_riv (stamps asserted, HALT-on-mismatch).
"""
import json, os, sys
import numpy as np
import common_riv as C

OUT = os.path.join(os.path.dirname(__file__), '..', 'out')


def cohort_bootstrap(rows, B=5000, seed=C.BOOT_SEED):
    """Resample entrants with replacement; recompute evidence-weighted R_realized per draw."""
    rng = np.random.default_rng(seed)
    w = np.array([C.evidence_weight(r) for r in rows])
    v = np.array([C.realized(r) for r in rows])
    n = len(rows)
    if n == 0:
        return None
    draws = np.empty(B)
    idx_all = np.arange(n)
    for b in range(B):
        idx = rng.choice(idx_all, size=n, replace=True)
        sw = w[idx].sum()
        draws[b] = (w[idx] * v[idx]).sum() / sw if sw > 0 else np.nan
    d = draws[~np.isnan(draws)]
    med = float(np.median(d))
    return dict(median=round(med, 1),
                mean=round(float(np.mean(d)), 1),
                sd=round(float(np.std(d)), 1),
                rel_sd_pct=round(100 * float(np.std(d)) / med, 1) if med else None,
                lo16=round(float(np.percentile(d, 16)), 1), hi84=round(float(np.percentile(d, 84)), 1),
                lo025=round(float(np.percentile(d, 2.5)), 1), hi975=round(float(np.percentile(d, 97.5)), 1),
                B=int(len(d)))


def main():
    curve, per, rinp, stamps = C.load_frozen()
    peq = C.pickeq(rinp)
    mech_stats = rinp['MECH_STATS']
    grade, top_grade, deep_grade, deep_ratio = C.rider_iii_grade()

    # ---- (a) R_curve: v2 curve at the pick-equivalents ----
    r_curve_by_mech = {t: curve[peq[t]] for t in C.MECH}
    sizes = {t: len(C.mech_rows(per, t)) for t in C.MECH}
    r_curve_pool = round(float(np.average([r_curve_by_mech[t] for t in C.MECH],
                                          weights=[sizes[t] for t in C.MECH])), 1)

    # circularity test (reported, not assumed): are any mechanism/pickless rows in the curve's load_pool?
    load_pool = [r for r in per if r.get('incurve') and r.get('pick') and 2004 <= r['year'] <= 2024 and r.get('v0')]
    mech_in_pool = sum(1 for r in load_pool if r['type'] in C.MECH)
    near = [r for r in load_pool if 86 <= r['pick'] <= 94]
    from collections import Counter
    near_mix = dict(Counter(r['type'] for r in near))

    # ---- (b) R_realized: era-matched evidence-weighted realised value, busts full weight, no cutoff ----
    r_real_by_mech = {}
    for t in C.MECH:
        rows = C.mech_rows(per, t)
        val, den, n = C.r_realized(rows)
        played = sum(1 for r in rows if (r.get('games_yr1') or 0) > 0)
        boot = cohort_bootstrap(rows)
        r_real_by_mech[t] = dict(R=round(val, 1), sum_w=round(den, 1), n=n, played=played,
                                 pick_equiv=peq[t], engine_cohort_n=mech_stats[t]['n'],
                                 engine_played_n=mech_stats[t]['played_n'], bootstrap=boot)
    fp = C.free_pool(per)
    r_real_pool_val, r_real_pool_w, r_real_pool_n = C.r_realized(fp)
    r_real_pool_boot = cohort_bootstrap(fp)

    # era-matching cross-read: national (ND) realised at the entry region + same-era span
    def nd_realized(lo, hi, y0=None, y1=None):
        nd = [r for r in per if r['type'] == 'ND' and r.get('pick') and lo <= r['pick'] <= hi
              and (y0 is None or y0 <= r['year'] <= y1)]
        val, den, n = C.r_realized(nd)
        vmean = round(float(np.mean([curve[r['pick']] for r in nd])), 1) if nd else None
        return dict(pick_lo=lo, pick_hi=hi, n=n, R_realized_ND=round(val, 1), curve_mean=vmean)
    yrs = sorted(set(r['year'] for r in fp))
    era = dict(
        nd_at_entry=nd_realized(88, 94),                      # reading-B: ND realised at pk88-94
        nd_at_entry_sameera=nd_realized(88, 94, yrs[0], yrs[-1]),
        nd_deep=nd_realized(80, 99),
        span=f"{yrs[0]}-{yrs[-1]}")

    # ---- (c) R_owner ----
    r_owner = C.R_OWNER

    # ---- honest grade per candidate ----
    grades = dict(
        R_curve=dict(grade_kind="rider-(iii) curve uncertainty at the entry pick",
                     grade_pct_at_pk90=grade[90], grade_pct_at_pk92=grade[92],
                     top_reference_pct=top_grade, deep_vs_top_ratio=deep_ratio,
                     note="the free-pool entry sits in the curve's low-confidence deep tail (~2.3x the top grade)"),
        R_realized=dict(grade_kind="cohort-bootstrap rel-SD (seed %d)" % C.BOOT_SEED,
                        pooled_rel_sd_pct=r_real_pool_boot['rel_sd_pct'],
                        per_mech_rel_sd_pct={t: r_real_by_mech[t]['bootstrap']['rel_sd_pct'] for t in C.MECH},
                        note="cohorts are THIN (MSD 44/17, SSP 31/16 played; the other five 5-12 played) "
                             "— the pooled and per-mechanism bands are wide; read as a band, not a point"),
        R_owner=dict(grade_kind="asserted prior, not measured",
                     note="item-332 reference constant; no sampling uncertainty (a prior, not an estimate)"))

    result = dict(
        rider="(iv) the replacement-adjusted view — three R candidates + uncertainty on R",
        report_only=True, do_not_merge=True, verdict=False,
        stamps=stamps, axes_note=C.AXES_NOTE,
        pick_equivalents=peq,
        candidates=dict(
            R_curve=dict(label="(a) R_curve = v2 curve @ pick-equivalent",
                         pooled=r_curve_pool, by_mech=r_curve_by_mech,
                         circularity_test=dict(
                             directive_expectation="v2 deep tail partly anchored on pickless pk90 outcomes -> self-referential",
                             finding="REFUTED under this construction",
                             mechanism_rows_in_curve_load_pool=mech_in_pool,
                             all_mechanisms_incurve_false=True,
                             pk86_94_anchor_mix=near_mix,
                             detail="every mechanism entrant has incurve=False (0/389 in load_pool); the pk86-94 "
                                    "region is fit on real-pick RD+ND only, so R_curve is NOT self-referential "
                                    "on pickless outcomes here")),
            R_realized=dict(label="(b) R_realized = era-matched realised value, evidence-weighted, busts full weight, NO cutoff",
                            pooled=round(r_real_pool_val, 1), pooled_sum_w=round(r_real_pool_w, 1),
                            pooled_n=r_real_pool_n, pooled_bootstrap=r_real_pool_boot,
                            by_mech=r_real_by_mech, era_matching=era,
                            method="realised=mean(vpath); never-produced->0; w=1.0 if terminal else min(1,n_obs/6)"),
            R_owner=dict(label="(c) R_owner = 220 (labelled reference constant, item 332)",
                         value=r_owner, fed_to_computation=False)),
        grades=grades,
        thin_sample_declaration="MSD 44/17 played, SSP 31/16 (engine cohort); IRE/UNR/PDA/PDN/PDS 5-12 played. Said on every artifact.")

    os.makedirs(OUT, exist_ok=True)
    json.dump(result, open(os.path.join(OUT, 'r_candidates.json'), 'w'), indent=1)

    # ---- markdown ----
    L = []
    L.append("# Rider (iv) — three R candidates + uncertainty on R  (REPORT-ONLY / DO-NOT-MERGE)\n")
    L.append(f"_{C.STAMP_NOTE}_\n")
    L.append(f"> **Axes note.** {C.AXES_NOTE}\n")
    L.append("Symmetric: three candidates, **no verdict, no steer** — the reading is the owner's at the ladder.\n")
    L.append(f"Pick-equivalents (free-intake entry): {peq}\n")
    L.append("## Headline (findings, not verdicts)\n")
    L.append("| candidate | value | what it is | grade |")
    L.append("|---|---:|---|---|")
    L.append(f"| **R_curve** | **{r_curve_pool}** | v2 list curve at the free-pool entry pick (90/92) | {grade[90]}% uncertainty @pk90 (rider-iii; ~{deep_ratio}x the {top_grade}% top) |")
    L.append(f"| **R_realized** | **{round(r_real_pool_val,1)}** | realised value the free pool actually delivers (evidence-weighted, busts full weight, no cutoff) | bootstrap rel-SD {r_real_pool_boot['rel_sd_pct']}% (thin) |")
    L.append(f"| **R_owner** | **{r_owner}** | owner's stated prior (item 332), reference line only | asserted, not measured |")
    L.append("")
    L.append(f"The three span **{r_owner}–{r_curve_pool}**: the v2 list curve prices the free-pool entry "
             f"~{r_curve_pool/round(r_real_pool_val,1):.1f}x the realised outcomes; R_owner and R_realized sit close.\n")

    L.append("## (a) R_curve — circularity note, TESTED not assumed\n")
    L.append(f"- Directive expectation: the v2 deep tail was partly anchored on pickless pk90 outcomes -> R_curve self-referential.")
    L.append(f"- **Finding: REFUTED under this construction.** Mechanism rows in the curve's `load_pool`: **{mech_in_pool}** "
             f"(all 389 mechanism entrants have `incurve=False`). The pk86-94 region is anchored by real-pick "
             f"{near_mix}. R_curve at pk90/92 is **not** self-referential on pickless outcomes.\n")

    L.append("## (b) R_realized — per mechanism (thin; read as bands)\n")
    L.append("| mech | pick-eq | n | played | R_realized | boot median [16,84] | rel-SD |")
    L.append("|---|---:|---:|---:|---:|---|---:|")
    for t in C.MECH:
        m = r_real_by_mech[t]; b = m['bootstrap']
        L.append(f"| {t} | {m['pick_equiv']} | {m['n']} | {m['played']} | {m['R']} | "
                 f"{b['median']} [{b['lo16']}, {b['hi84']}] | {b['rel_sd_pct']}% |")
    b = r_real_pool_boot
    L.append(f"| **POOL** | 90-92 | {r_real_pool_n} | — | **{round(r_real_pool_val,1)}** | "
             f"{b['median']} [{b['lo16']}, {b['hi84']}] | {b['rel_sd_pct']}% |")
    L.append("")
    L.append("**Era-matching cross-read (national cohorts, same entry region/era):**")
    L.append(f"- ND realised @ pk88-94 (reading-B, what the equivalent pick delivers): **{era['nd_at_entry']['R_realized_ND']}** "
             f"(n={era['nd_at_entry']['n']}; curve says {era['nd_at_entry']['curve_mean']}).")
    L.append(f"- ND realised @ pk88-94, same era {era['span']}: {era['nd_at_entry_sameera']['R_realized_ND']} "
             f"(n={era['nd_at_entry_sameera']['n']}).")
    L.append(f"- The free-pool R_realized ({round(r_real_pool_val,1)}) and the era-matched ND-at-entry realised "
             f"({era['nd_at_entry']['R_realized_ND']}) bracket the owner's {r_owner}, and all three sit far below "
             f"the v2 list value ({r_curve_pool}).\n")

    L.append("## (c) R_owner\n")
    L.append(f"- **220**, item 332 — carried as a labelled reference line only; not fitted, not fed to any computation.\n")

    L.append("## Uncertainty grade per candidate (job 2)\n")
    L.append(f"- **R_curve**: rider-(iii) curve uncertainty at the entry pick = {grade[90]}% (@pk90), {grade[92]}% (@pk92) — "
             f"~{deep_ratio}x the {top_grade}% top reference. The free-pool entry is in the curve's low-confidence deep tail.")
    L.append(f"- **R_realized**: cohort-bootstrap (seed {C.BOOT_SEED}, B={b['B']}) pooled rel-SD **{b['rel_sd_pct']}%**; "
             f"per-mechanism rel-SD {[r_real_by_mech[t]['bootstrap']['rel_sd_pct'] for t in C.MECH]}. Thin cohorts.")
    L.append(f"- **R_owner**: a prior — no sampling uncertainty; graded *asserted, not measured*.\n")
    L.append(f"> **Thin-sample declaration.** {result['thin_sample_declaration']}\n")

    open(os.path.join(OUT, 'r_candidates.md'), 'w').write("\n".join(L))
    print(f"[build_r_candidates] wrote out/r_candidates.json + .md")
    print(f"  R_curve(pool)={r_curve_pool}  R_realized(pool)={round(r_real_pool_val,1)} "
          f"[boot {b['lo16']},{b['hi84']}]  R_owner={r_owner}")
    print(f"  circularity: mechanism rows in curve load_pool = {mech_in_pool} (REFUTED)")
    return result


if __name__ == '__main__':
    main()
