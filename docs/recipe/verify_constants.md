# verify_constants.md — adversarial verification of CONSTANTS.json

Verifier: independent pass over `scratchpad/wt-lens/` (read-only), 2026-08-05.
Method: every cited line opened; every table transcribed back and compared element-by-element;
env-gated values checked against `data/model_config.json` AND the in-code default; then a reverse
scan of `rl_model.py` + `_merged_recover.py` for value-path literals appearing in no group.

**Verdict rule used.** `WRONG` = a *number* in the JSON disagrees with the code. `INCOMPLETE` = every
number present is right but something numeric/behavioural is missing or a formula string misdescribes
the code. This keeps the counts unambiguous; prose defects that would change a rebuild are called out
in full inside their group.

**Totals: 31 CONFIRMED · 1 WRONG · 4 INCOMPLETE · 36 groups.**

---

## Per-group verdicts

### 1. `L1_step50_replacement_bars` — CONFIRMED
`RM:501` REPL = MID 80.1 / SD 78.3 / RUCK 78.5 / KPD 68.4 / SF 70.9 / KPF 66.8 — all six exact.
`GRP` (`RM:67`) and `_ELIG_MAP` (`RM:145`) carry exactly the six codes listed. `_collapse_elig`
(`RM:146-152`) drops SF when KPF present and SD when KPD present — matches "KPF absorbs SF; KPD
absorbs SD". `_CROSS_CLASS` (`RM:158-159`) is exactly `{KPD,SF},{KPF,SD},{RUCK,SF},{RUCK,SD}` — all
four pairs present, none extra. `y0dpp_bar` (`RM:166-176`) returns None + registry flag on a
cross-class combo and continues (no halt) — matches. Lower-REPL selection at `RM:85`, `RM:175`.
`LIVE_SEASON=2026` at `RM:98`.

### 2. `L2_step2_season_qualification_bars` — **WRONG**
Constants are right: `_EVW_Q0=11.0`, `_EVW_QW=1.1` (`MR:205`); bars 6 (`MR:1063/1066/1686`), 10
(`MR:168`), 14 (`CP:108`), 22 (`CP:49`, `LTI:25`); `SEASON_FE` fallback 0.58 (`MR:106`), effective
0.83 from `data/season_state.json`; `_fEy` returns 1.0 for an out-for-remainder register name
(`MR:126-129`); `G_ADQ=12` un-prorated (`MR:515`); LD's own 12-bar *does* prorate (`MR:841`);
`_playable = cp.SEASON*(max(0,Y-debutyr)+fE)` (`MR:130-131`).

**The `evaluated` sample points are numerically wrong.** JSON gives
`{"g=9": 0.14185106490048777, "g=13": 0.8581489350995122}`. Those are `1/(1+exp(±1.8))`. The code's
exponent is `(g-Q0)/QW = ±2/1.1 = ±1.8181818…`, not ±1.8. Recomputed from `MR:207-208`:

| g | JSON | **correct** |
|---|---|---|
| 9  | 0.14185106490048777 | **0.1396521834167601** |
| 11 | 0.5 | 0.5 (correct) |
| 13 | 0.8581489350995122 | **0.8603478165832398** |

Correction: replace the two values above. The `form`, `Q0`, `QW` and the gate name (`RL_EVW`,
default 1) are all correct, so the defect is confined to the illustrative evaluations — but a
rebuilder calibrating against them would mis-fit the qualifying ramp by ~0.22 pp at both ends.

### 3. `L2_step3_era_adjustment` — CONFIRMED
`MR:51-55`: `for Y in range(2009,2026)`, rows filtered `s['games']>=6`, `era[Y]=mean(avg)`,
`REF=mean(era.values())`. Window `[2009,2025]` inclusive and the `range(2009,2026)` note both exact.
Consumers verified individually: `bestlvl` `MR:1063`, `_kpf_LD` `MR:840/845`, `_staleness_grade`
`MR:1695`, `recent_ratio` `MR:2003` — all four apply `a*REF/era.get(y,REF)`. `_lvlcurr`
(`MR:301-305`) applies no era term — "NOT_era_adjusted" confirmed. Missing-year fallback is `REF`
(factor 1) as stated.

### 4. `L2_step5_pick_split` — CONFIRMED
`ND_CURVE_LAST=64`, `POOL_PICK=65` (`RM:212-213`); `PICKLESS={'SSP','MSD','IRE','UNR','PDA','PDN','PDS'}`
(`RM:179`) — all seven, none extra. Classification loop `RM:260-281` sends national 65+, RD, PSD and
every pickless type to `POOL_PICK`. `KMAX=70` (`CP:48`). `PICKS=list(range(1,71))` (`MR:485`) → iso
domain `[1,70]`. `_teaches_curve = _in_pvc(p) and not is_pool(p)` (`RM:313`, with
`_in_pvc = not _pvc_exclude` at `RM:295`). `CURVE_FIT_SITES` (`RM:332`) is exactly the five names
listed. `hist` window `2003<=year<=2021` (`RM:283`).

### 5. `L2_step6_evidence_dials` — CONFIRMED
`_EVW_R=0.11` (`MR:204`); `_EVW_GK=0.55`, `_EVW_EST=3.6`, `_EVW_TAU=1.1` (`MR:206`). Forms checked
term-for-term: `_ev_rec` `E²/(E²+GK²)` (`MR:209`), `_ev_est` `E³/(E³+EST³)` (`MR:210`), `_ev_pw`
`gate*fade` with `fade = R + (1-R)exp(-E/TAU)` (`MR:293-296`) — the JSON's expanded
`0.11 + 0.89*exp(-E/1.1)` is the identical expression, and "0.89 is not a separate literal" is true.
`PROVEN_N=4` (`MR:100`). `_nqual` (`MR:168`) = seasons with `games>=10`, `year<=Y`, `year>debutyr-1` —
matches the stated definition exactly. `E_q` window (`MR:208`) is `games>0` over the same year
window. `c=n/PROVEN_N` at `MR:876`.

### 6. `L2_step7_recency_and_games_trust` — CONFIRMED
`_DAMP_K=5.8` and `_wg(g)=g²/(g+K)` (`MR:186-187`), gate `_DAMP` (`MR:185`); the "RL_DAMP_K env read
was removed" note is corroborated by the `MR:186` comment. `LDECAY_G={'KEY':0.40,'GEN':0.35,'MR':0.225}`
(`MR:134`) and `_ldg` (`MR:133`) maps KPF/KPD→KEY, SF/SD→GEN, everything else (MID, RUCK)→MR — group
map exact. Applied as `_wg(gm)*ld**max(0,Y-yr)` (`MR:304-305`).
`_dev_advance` (`RM:493-495`): `w=clamp(games/130.0,0.30,0.85)`, blend
`L + w*(L*(c1/c0-1)) + (1-w)*(cp*(c1-c0))` with `cp=basepk_c(...)`, guard `clamp(L1, L*0.5, L*1.6)` —
all five numbers exact. `RECENCY_DECAY=0.72` (`CP:71`), `EXPO_DEN=11.0` (`CP:87`), `EXPO_F` fallback
0.545 / effective 0.773 (`CP:86` + season_state), `EXPO_INPROG_Y=2026` (`CP:85`), `LEVEL_RAMP=14`
(`CP:108`).

### 7. `L2_step8_level_blend` — CONFIRMED
Chain `_coreM1` (`MR:577-580`) matches the stated `(1-pw)[(1-est)(Lo+rec(Lc-Lo)) + est*_est] + pw*par`
term-for-term. `Lo = cp._lvl_eff_orig` — verified this is `PR.lvl_par` (wire_redesign `build()` sets
`cp._lvl_eff = PR.lvl_par` before `MR:167` captures it), i.e. genuinely par-centred
`par + (lvl_wt - par)*min(1, exposure/22)` (`PRD:110-113`, `RAMP=22` at `PRD:44`) — the JSON's
description is correct, not the (different) `CP._lvl_eff`.
Up-branch `MR:551-556`: `DOWN_TOL=3.0` both sides under `_LSYM`, `sw=clip((gap-3.0)/5,0,1)`,
`L=Lo+sw*s*gap`. Superseded path `TOL_M1=5.0`, `S_M1=0.46`, `G_ADQ=12`, `WIN=2` (`MR:515`, `MR:534`).
`FLAT_TOL_G={'KEY':10.3,'GEN':12.0,'MR':14.0}` (`MR:134`) consumed only by the dormant `_est_core`
(`MR:313`) — the "dormant twin" claim is corroborated by `MR:319-324` and by `cp._lvl_eff=_inferM1`
(`MR:628`).
`_L3_AX` 20..31 and `_L3_AY` (`MR:520-521`) transcribed exactly; `_SAGE29_VAL=0.3793` (`MR:531`)
substituted at index 9 (`MR:532`), base 0.026915 restored at `RL_SAGE29=0` — the JSON's
`values_in_effect` array is byte-correct including the 29-knot swap; clip `[0,1]`, None→0.46 (`MR:533`).
`_AGEMULT_X/_Y` (`MR:138`) exact, clip `[0.53,0.95]`, None→0.85 (`MR:139`).
`_FB_AGE`/`_FB_LCR`/`_FB_Z` (`MR:156-158`): all 7×4 = 28 cells match (JSON's `0.0530` == code `0.053`).
`_agemult2` clip `[0.53,0.98]` and the `lcr<=0` hard-zero (`MR:163-166`). `_par_prior` tenure clamp
`[1,6]` and `min(effpk, KMAX=70)` (`MR:306-308`), form-anchored (`MR:224-236`).

### 8. `L2_step9_opportunity_test` — CONFIRMED
`_UP_DLX=[-30,-20,-10,0,10]`, `_UP_NY=[3,4,5,6]`, `_UP_S` 4×5 (`MR:340-341`) — all 20 cells exact,
including row order (N=3 first). Evaluation order (dL within row, then over N) matches `MR:342-345`,
clips `[-30,10]` and `[3,6]` exact. `_eo` (`MR:346-351`): `yrw=clip((N-2)/4,0,1)`,
`exp=clip(gm/(14.0*max(N-1,1)),0,1)`, product. `bar = REPL[gfut] - 3.0`, qualifying `games>=6`,
`T=max(_upS,_lvlcurr)`, blend `(1-eo)L0+eo*T`, `RL_EO2=0` restores `min(L0,T)` (`MR:589-596`).
Pin variant `N = Y-d+1-1` with the data window unmoved (`MR:736-742`).

### 9. `L2_step10_injury_gap_penalty` — CONFIRMED
`_ABS_L_REF=75.0` (`MR:649`), `_ABS_CAP=0.20` (`MR:650`), `_ABS_FADE_K=5.8` (`MR:661`).
`_ABS_AGE` 18..34 (17 entries) and `_ABS_EFF` (`MR:662-665`) — all 17 values exact and in order.
`_abs_frac` = `clip(max(0,-interp)/75.0, 0, 0.20)` with age clipped to `[18,34]` (`MR:666-670`).
`fade=(g+K)/(g²+g+K)` (`MR:711`) — algebraically `1/(1+w(g))` as stated; `pw(0)=1` holds.
`g` = games in seasons `>=ret`, inside the debut window, `<=Y` (`MR:694`) — matches. Charge
`pen=max(0, Lb-Lng*(1-frac))`, `L=Lb-fade*pen` (`MR:713-714`). Gap selection keeps the **latest**
qualifying gap with `ret<=Y` (`MR:695`) — "most recent, one penalty only" confirmed. Real-only scope
(`MR:705`).

### 10. `L2_steps11_13_forward_band` — INCOMPLETE
All numbers CONFIRMED: `Q=[0.10,0.30,0.50,0.70,0.90]` (`CP:45`); hyperparameters
`n_estimators=400 / max_depth=4 / learning_rate=0.05 / min_samples_leaf=25 / random_state=0 /
loss='quantile'` (`CP:159-161`), `RL_PRIOR_TREES` default 400 (`CP:159`); window
`cap=2026, resolved_cut=2021` (`CP:143`) and the engine-side pool `debutyr>2021` + MSD exclusion
(`MR:58-62`); feature vector order verified against `CP:120-123`; q97 floor `max(pred, b[4])`
(`MR:369`); `_v7` knots `[20,22,24,27]→[1.0,0.76,0.58,0.40]` (`MR:599`); `V7_FORM_W=0.6` (`MR:785`);
`phi=clip((lcr-4.0)/26.0,0,1)*min(nq,2)/2*0.6`, gate `lcr>4.0 and nq>=1` (`MR:607-611`); real-only
wrapper (`MR:622-627`); first-evidence 3-point mean over `{max(g-1,1), g, g+1}` (`MR:1669-1676`);
train/serve asymmetry real (`MR:628` vs `PRD:124-126`).

**Missing / misdescribed:**
- `band_target` says "busts: best single season if <3 qualify, else 0". `CP:56-63` actually does:
  `>=3` qualifying → mean of top 3; `1-2` qualifying → **mean of what qualifies** (not "best single");
  `0` qualifying → **max avg over any season with games>0**; only a never-played career returns 0.
  A rebuilder following the JSON would train against a different target.
- The v7 taper is additionally gated on `asc<1.0` (`MR:607`), i.e. it is inert at age<=20; the JSON
  states only the `lcr`/`nqual` conditions.

### 11. `L2_step14_L3_step2_age_path` — CONFIRMED
`DELTAS` (`RM:502`): all 23 keys −8..+14 transcribed exactly, including the 0.58 collision at −8 and
+11. `frac(a,pa)=DELTAS[clamp(round(a-pa),-8,14)]` (`RM:503`), duplicate `_fa` at `RM:1033`.
`PEAK_AGE={MID 25, RUCK 27, SD 26, KPD 27, SF 25, KPF 27}` and
`PEAK={MID 92, RUCK 92, SD 78, KPD 70, SF 70, KPF 72}` — read out of `params.json`, exact.
Horizon `range(18)`, `ag>38 or frac<0.42 → break`, floors `if ag<=pa: max(lev,cl)` and
`if k==0: max(lev,cl)` (`RM:587-592`, W4 copy `MR:917-922`). `_smooth_tail` rule
`out[a]=min(c[a], out[a-1]-0.010)` for `a>peak` (`RM:64`).
*Note (not a defect):* the claim "AGE_CURVE … never [used] by the pricing path
proj_from_peak/prod_floor" is literally true, but `_agecurve` is reached from `_dev_advance` →
`level_now` → `cur`, which **is** on the shipped `ev()` path whenever `AGE_REF>BASE_REF` (the +1/+2
boards). The sentence is accurate as written; a rebuilder should not read it as "AGE_CURVE is not
needed to price".

### 12. `L3_step3_captaincy_premium` — CONFIRMED
`LCAPT_BAR=105.0; LCAPT_M=109.5; LCAPT_W=1.85; LCAPT_G=1.00` (`RM:380`). Closed form and the `>=0`
clamp at `RM:385-387`; `_softplus` switches to identity at `x<30.0` (`RM:383-384`).
Retired curve `CAPT_GAIN=0.35; CAPT_EXP=1.25; CAPT_CAP=18.0` (`RM:382`) with
`cb*CAP/(CAP+cb)` (`RM:388-392`), reachable only at `RL_CAPT=0` (`RM:400`).
`CAPT_THRESH=107.4; CAPT_M=116.0; CAPT_W=5.0` (`RM:531`) — and `CAPT_M`/`CAPT_W` are used only by
`_pcap`/`capt_bonus` (`RM:532-537`), which has no caller on the price path: confirmed.
`_CAPT_OFF` default `{'on':False}` (`RM:393`).

### 13. `L3_step4_replacement_netting` — CONFIRMED
`REPL_DROP_PTS=3` and `REPL_DROP={g:3.0}` over the six positions (`DR:35-39`); applied by lowering
`MA.REPL` around the band evaluation and restored in `finally` (`MR:382-387`). `S_SH=3.0` (`RM:505`),
`posval(x)=3.0*log(1+exp(min(x/3.0, 40.0)))` (`RM:507`) — the 40.0 overflow cap is exact.
Year-zero dual-bar blend verified at all three sites: floor half `RM:621-623`, proven copy
`MR:961-963`, projection half `DP:265-273`; `sp = MA.SEASON_PROG = 0.83`; gated `AGE_REF==BASE_REF`.
`futblend` returns `[(pri,1-q),(low,q)]` with `q=p_dual_stream/100` (`RM:115-128`), gate `RL_FLEX`.
*Minor imprecision (no number affected):* the JSON's `form` string is the **floor** half (two
`posval` calls). The projection half at `DP:265-273` does two full `proj_from_peak` calls blended
before `val()`. Both are "outside the nonlinearity", so the stated rule holds.

### 14. `L3_step5_aggregation_and_discounts` — CONFIRMED
`×21` and `/(1+d)^k` at `RM:595-596`, `RM:626`, `MR:927-928`, `MR:966`.
`LENS` (`RM:540`) = `now 0.34 / bal 0.14 (0.15 at RL_DIAL14=0) / fut 0.05`; `RM:548-552` adds
`balanced` (== bal), `contender 0.18`, `rebuilder 0.10` under `_LEGE`; `POSTURES` tuple at `RM:552`.
Key-position `×1.05` for KPF/KPD (`RM:597`, `MR:929`). `PMAX=0.25` (`RM:180`);
`runway=clamp((25-a)/6.0,0,1)`, `elite=clamp((lp/PEAK[g]-0.97)/0.30,0,1)`, `prod*=(1+runway*elite*PMAX)`
(`RM:598`, `MR:930`); the forward-lens form-anchored `ah` at `MR:913`.

### 15. `L3_step6_currency` — CONFIRMED
`ref=np.percentile([...],99); SCALE=7000/ref**GAMMA` on the `STBL=True` basis (`RM:730-732`).
`GAMMA` default `'1.0'` (`RM:504`); `os.environ.setdefault('RL_GAMMA','1.0')` at `DP:28`, `CP:40`,
`DR:24`; manifest pins `"1.0"`. `RW_S={2026:2.0,2025:1.0,2024:0.4,2023:0.2}` with `games>=2`
(`RM:409-415`). `_P1` default `'3000'` (`RM:929`); `BOARD_FACTOR=(_P1/PVC[1])*_NUM['s']` (`RM:931`);
`_load_numeraire` 1e-9 coherence on both s and the pin (`RM:890`, `RM:897`).
`pvc_curve_v2.json` `numeraire` block read directly: `pooled_head_pre_scale 3068.4647`,
`s 0.9776876364261254`, `published_pin 3000.0` — all three exact (and 3000/3068.4647 reproduces s).
`pick_redenomination.json` `factor = 1.0524`; loaded `EX:132`, applied as `round(ev/F)` on players
only (`EX:177`), picks ship as the adopted ladder undivided (`EX:145-150`). Order gate halts on a
strict inversion, anchor ratios asserted at relative `<0.002` (`EX:227-239`). Numeraire halt at
`EX:161-165` and `RM:981`.
Reference-basis block: `EXP_PEAK_BASE` (`RM:639`), `EXP_RETAIN` all 6×4 (`RM:640-642`),
`EXP_PICK_SLOPE=-10.72`, `EXP_LOGREF=4.0073` (`RM:643`), `EXP_BLEND_GAMES=45.0` (`RM:644`),
clamp `[30.0,105.0]` (`RM:650`), `V4_SPIKE_RETAIN={'KPD':0.69}` (`RM:634`), spike guard
`len(ss)<3` / `games>=6` / `base>=55` / `>=1.30*base` (`RM:679-682`), `conf=clamp(tg/45.0,0,1)`,
`bb=0.60+(BETA_POS-0.60)*conf` (`RM:573`), `BETA_POS`/`ICPT_POS` (`RM:181-182`) both 6/6 exact,
`0.78**(2026-yr)` (`RM:567`), `RWE={1:1.0,2:1.3,3:1.6,4:1.7,5:1.7}` with `.get(s,1.7)` (`RM:562,568`).
Import-fit dials: `ALPHA=0.6` (`RM:769`), `PVC_ALPHA_LO/HI=0.6/0.8` (`RM:812`), `PVC_REPL_BUF=0`
(`RM:813`), ramp `LO+(HI-LO)*min(k-1,49)/49` (`RM:819`), `CURVE_H=1.0` (`RM:906`), ±4 window
(`RM:776,832`), floor 210 (`RM:799,858`), `Wf=round(3+6*min(k-1,60)/60)` (`RM:836`), parametric fit
picks 1-8 (`RM:838`), de-plateau `start_before=46` (`RM:936`), `DEF_CURVE` 10 values (`RM:220`).
*Wording only:* `parametric_blend` says "parametric below pick 6" — `RM:841` is `k<=6` (at or below).
The claim that these constants are off the `ev()` path but set SCALE is **verified**: `price6` →
`v_at_peak` → `proj_from_peak(g, L_from_band, …)` never calls `peak_est`; `peak_est` reaches the board
only through `player_raw` at `RM:731/733`.

### 16. `L3_step7_demonstrated_floor` — CONFIRMED
`H=clamp((40-a)/3.0,1.0,3.0)`, `wt=min(1.0,H-k)` (`RM:615-617`);
`lev=cur*min(1.0, frac(ag,pa_)/max(frac(a,pa_),1e-6))` (`RM:618`) — decline-only. Position axis is
`g=bnow(p)` and `pa_=PEAK_AGE[g]` (`RM:601`) — "present position for the bar and the peak age" exact.
Same captaincy/netting/hinge/×21/discount/`val()` arithmetic (`RM:620-627`). The duplicate-loop
warning is real: `_prod_floor_w4` (`MR:940-967`) is the parallel copy and additionally multiplies by
`_w4_W(k,ctx)` at `MR:966`, exactly as stated.

### 17. `L3_step8_band_averaging` — CONFIRMED
`WQ6=np.array([0.18]*5+[0.10]); WQ6/=WQ6.sum()` (`MR:94`) — the sum is 1.00 exactly, so the
normalisation is a no-op as stated. `SCALE_DIST=1.0` (`DP:48`). `price6 = SCALE_DIST*_det_dot(WQ6, …)`
with `_det_dot` = `math.fsum` (`MR:41-42`, `MR:386`) — determinism claim correct.
`v_at_peak` returns `max(prod, MA.prod_floor(p,lens))` (`DP:283`).

### 18. `L3_step9_proven_reweighting` — INCOMPLETE
All dials CONFIRMED: `W4_CRED=0.17`, `W4_KPFUP=1.6`, `W4_FADE=0.60`, `W4_OVPX=1.0` (`MR:786-789`),
`W4_OVPX_D={'SF':0.12,'SD':0.09,'MID':0.07}` (`MR:790`), `W4_KPFTOP=0.4` (`MR:820`), `_KPF_M0=8.0`,
`_KPF_MS=16.0` (`MR:821-822`). Legs verified against `MR:893-907`: credit
`cw*up*gm*dur*sh*interp(k,[0,2,5],[1,1,0])`; fade `-0.60*(1-gm)*fadew*interp(k,[4,10],[0,1])` gated
on `n>=PROVEN_N`; floor `max(W,0.05)`. `gm` general `clip((m-10.0)/20.0,0,1)` (`MR:878`);
`dur=clip(g3/28.0,0,1)` over `Y-2..Y` (`MR:871,880`); `sh=1-clip((Lo-Lc-3.0)/5.0,0,1)` (`MR:881`);
`fadew=clip((a-23.0)/3.0,0,1)` (`MR:882`). KPF variant: `gm` uses `_KPF_M0/_KPF_MS` (`MR:874`) while
`kt` uses hard-coded `8.0/16.0` (`MR:875`) — the JSON's `note_gm_and_kt_are_numerically_identical_at_defaults`
is correct and well caught. Partial gate `2<=n<4 and dm>8.0`, `cw=n/4`, no fade (`MR:863-876`, `MR:901`).
OVPX ramp `interp(ep,[38,46,99],[0,1,1])`, applied `W*=(1-W4_OVPX*ovpx)` (`MR:885,891,905-906`).

**Missing:** `fadew`'s None-age fallback — `MR:882` reads `((a if a is not None else 25.0)-23.0)/3.0`.
The literal **25.0** appears in no group.
*Wording:* `positions_not_compressed`/`scope` says "a fully proven **non-KPF** player never carries
it" — per `MR:868-891` a fully proven player of *any* position never carries it (only thin careers
and partially-proven KPFs do).

### 19. `L3_step10_young_credit` — CONFIRMED
`_YC_W=0.9` (`MR:998`), `_YC_KPF=0.92` (`MR:999`), `_YC_G0=46.0` then overwritten from the table
(`MR:1000,1007`) — `ycred_table.json` `G0=46`, so the effective value is 46 either way.
`s=min(g/6.0,1.0)`, `R=max((1-s)Rs+s*Rp, 0.0)`, KPF `R*=0.92`, `phi=(1-g/46)²`, return
`1+0.9*R*phi` (`MR:1036-1040`); early return `1.0` when `g>=G0` (`MR:1029`) — "zero for g>=46"
correct. Table read directly: 90 grid picks (1..90), years 2007-2026, row keys `'1'`(sat)/`'0'`(played),
six positions — every JSON claim exact. Pick clamp `min(max(pk,1),90)` on `log` (`MR:1034`).
`T<_YC_TMIN → 1.0` (`MR:1031`). Scope `type in ('ND','RD')`, not `_pickless`, `_isreal`
(`MR:1024-1025`). LTI clock `advance` adds `L*cp.SEASON` (=22) games (`MR:1019-1021`).
Halt-if-table-absent at `MR:1003-1005`.

### 20. `L3_step11_pole` — INCOMPLETE
All tabulated numbers CONFIRMED: `_SCALE={'MID':1.19,'SF':0.93,'KPF':0.95,'SD':1.08,'KPD':1.05,'RUCK':1.13}`
with `.get(pos,1.0)` (`MR:394-395`); synth = 2 seasons × 18 games, `year 2023`, `dob '2005-03-01'`,
type `ND` (`MR:389`); cache key `(pos, int(min(pk,70)), int(clamp(T,1,6)))` (`MR:392`);
`RECX/RECY` 6+6 exact (`MR:94`), `recover=clip(interp(perf/max(1,par),…),0,1)` (`MR:388`);
`perf=cp._lvl_wt` (`MR:465`, `CP:100-104`); `tfade=interp(et,[1..6],[1.00,0.76,0.40,0.16,0.05,0.05])`
(`MR:462`); `POLE_RAMP=22.0` (`MR:100`) with `ramp=min(1, exposure/max(1e-9, 22*min(1,playable/22)))`
and the `ramp + ev_est(E_q)*(1-ramp)` smoothing, base `1.0 if nqual>=4 else ramp` (`MR:297-300`);
`eff_ten` (`MR:309-311`); combination `pr + w*recover*max(0, po-pr)` (`MR:466`); pole table frozen over
1..KMAX × T 1..6 (`MR:498-500`).

**Missing:** `wage` at `MR:461` is `0.0 if pos=='RUCK' else clip(1-((a or 21)-20)/6,0,1)`. The JSON's
`age_fade_wage` records the RUCK zero, the age-20 full point and the age-26 zero but **omits the
None-age fallback literal 21**, which is a genuine in-code value-path constant (it makes a
missing-age player read as age 21 → wage ≈ 0.833).

### 21. `L3_step12_output_proportionality` — CONFIRMED
`UNCOMP_DELTA=6.0`, `UNCOMP_DECAY=0.25`, `UNCOMP_TAU=1.1`, `UNCOMP_S_DEFAULT=0.10` (`RM:524-527`);
`UNCOMP_S` falls back to the default when `RL_UNCOMP_S` is unset (`RM:528-529`); gates `_UNCOMP`
default 1 (`RM:523`) and `_UNCONSERVE` default 0 (`RM:530`). The `_meta` comment-conflict entry is
correct and important: the `MR:405` header still says "INERT by default (UNCOMP_S_DEFAULT=None)"
while `RM:527` is the literal `0.10` — code wins, map is live.
`rho_out` (`MR:412-427`): every season with `games>0`, `u=games*0.25**(2026-year)`, weighted mean of
`(avg-REPL[pos])`, `None` when no played season — "no games floor, no exclusion, no phase test"
verified by reading the loop. Map (`MR:428-453`): `ramp=1.0 if ro>=6.0 else ro/6.0`;
`E=1-exp(-Eq/1.1)`, `0` when `Eq==0`; `w=0.10*E*ramp`; `t=Vb*(ro/Rden)` (kappa=1 — the `# (kappa=1)`
comment at `MR:446` is the source of the JSON's `"kappa": 1`); `v0p=pr0^(1-w)*t^w`; return
`C[pos]*v0p + delta`. Identity conditions all present at `MR:431,438,441,445,447`.
Reference build (`MR:1869-1906`): `_uncomp_scope = _isreal and not delisted and not _retired`,
`nqual>=4`, per-position `np.median` for both `V_ref_b` and `RHO_DEN`, `C=Σpr0/Σv0p` accumulated with
`C==1` (`MR:449-452,1894-1902`).

### 22. `L3_step13_pick_order_guard` — CONFIRMED
`_ISOFADE_TAU=_EVW_TAU` (`MR:478`) — the "bound to, same constant" note is literally true.
`iso_eff = 1 + (iso_corr-1)*exp(-E_q/1.1)` (`MR:497`), synths take the unfaded table (`MR:496`).
Table build (`MR:485-492`): `PICKS=1..70`, synth at `PR.par_at(pos, min(pk,70), 4)` → T=4,
`IsotonicRegression(increasing=False)`, `fs=iso/np.maximum(raw,1e-6)`, second isotonic on `fs` under
`_ISOFADE`. `iso_corr = interp(min(pk,70), xs, fs)` (`MR:493`). Six positions exact (`MR:486`).

### 23. `L3_step15_ruck_caps` — CONFIRMED
`RUC_PRIOR_CAP` default `'1.4'` with the 1.73 pre-bake value in the comment (`MR:1129,1138`);
`RUC_CEIL_HEAD='0.80'`, `RUC_CEIL_REFPK='72'`, `RUC_YRH='0.35'` (`MR:1157-1159`); gate `_W4RUC`
(`MR:1156`). Grid `np.linspace(15.0,150.0,46)` forced non-decreasing (`MR:1162,1167`).
`_ruc_head_core` (`MR:1170-1174`): `1 + 0.35*interp(min(pk,99),[1,4,18,30],[0.7,1,1,0])*clip((25.0-a)/4.0,0,1)`,
None-age → 21.0 — all knots and both fallbacks exact. Age-axis split: production leg uses as-of age
(`MR:1175`), V0/prior-cap leg uses draft-time age (`MR:1176-1177`). Ceiling / no-production fallback
(`MR:1178-1182`). Bind `if _cpv < e <= _v0u` (`MR:1703-1704`). Unconditional start-value cap
`min(v, 1.4*draftval*head_v0)` inside `_v0_raw` → before the curve/guard (`MR:1183-1184`, `MR:1202-1205`,
`MR:1620-1624`).

### 24. `L3_step16_kpf_compress` — CONFIRMED
Gates `nqual>=PROVEN_N`, `age>=24.0`, `gfut=='KPF'`, `_W4KPF` (`MR:1712-1714`).
`W4_KPFSH=0.55` (`MR:791`), `W4_KPFSH_DEM=0.70` (`MR:819`).
Split `e = eP + 0.70*(min(e,eD)-eP) + 0.55*(e-max(eD,eP))` (`MR:1724`) — exact, including the
`eD=eP` short-circuit when `LD is None or LD<=lvl_eff` (`MR:1722-1723`) and the `min(max(...,eP),e)`
clamp. `_kpf_LD` (`MR:823-848`): window `Y-3..Y`, bar `12.0*fE` for the in-progress season only,
top-2 mean, `>=2` required, register-out nuke of 2026 with `_ext=min(2,len(_nuke))` (cap +2), and the
documented fallback to the original window with a report — every element present.

### 25. `L3_step17_scrap_and_delisting` — CONFIRMED
`if delisted(p): return round(0.02*v0_start(p))` is the **first** statement of `ev` (`MR:1699-1700`).
`delisted` = `_retired` or (`_last_listed is not None and < 2026`) (`MR:1060`) — exact.
Floor scope exclusions at `MR:1785`. Back-board recall (`RM:713-719`, `RM:1327-1339`).

### 26. `L3_step18_sitout_retention` — CONFIRMED
`R_SURF` (`MR:1104-1106`): all 3 classes × 4 log-pick knots × 6 depths = **72 values** transcribed
and compared individually — every one matches, including the repeated tails.
`_RS_KNOTS=[5,15,30,50]` (`MR:1107`). KPP pointwise-max floor vs nonKPP, board path only, RUCK
excluded (`MR:1123-1124`). Lookup `interp(log(clamp(pick,1,90)))` then `interp(tau,[0..6],[1.0]+dv)`
(`MR:1114-1125`). `tau = max(0,Y-debutyr) + fE**1.5` (`MR:1651`).
`LAM_SIT=[0.0,0.160,0.493,0.547,0.547,0.816,1.0]` (`MR:1126`), argument `min(gy/fe, 6.0)` (`MR:1654`).
Blend `(1-lam)*R*v0_start + lam*e_full` (`MR:1655`); trigger `nseas_pro==0` (`MR:1729`).
Superseded depth-only `R_SIT` (`MR:1094`): all 18 values match the "for the record" block.

### 27. `L3_step19_staleness` — CONFIRMED
`onset = 4 if pos in ('KPF','KPD','RUCK') else 3` (`MR:1731`).
Stalled: `el>=onset and ns<=1`, `frac=0.25*max(0.4,1-0.10*(el-onset))*(1.6 if keyruc else 1.0)`,
`e=min(e, cap+gr*max(0,e-cap))` (`MR:1732-1736`).
Mediocre: `el>=onset+2 and pr<0.55`, `frac=0.45*max(0.3,1-0.08*(el-onset))*(1.5 if keyruc else 1.0)`,
hard `min` (`MR:1737-1739`). `pr = bestlvl/max(1,par)` with `bestlvl` era-adjusted (`MR:1728,1062-1064`).
`_D8Q` / `_D8G1` / `_D8G2` (`MR:1680-1682`): all 27 values exact. Shortcuts at `MR:1686-1694`
(current clears `6*fE` → 1.0; no live games → 0.0; no prior qualifying → 0.0) and
`gap = Y - max(prior_qual)` (`MR:1696`).

### 28. `L3_step21_midseason_clock_blend` — CONFIRMED
`M3_FE` fallback 0.58 / effective 0.83 (`MR:1752`); `M3_DEN=11.0` (`MR:1753`); `M3_INPROG_Y=2026`
(`MR:725`). `s=clip(1-gy/11.0,0,1)` (`MR:1755-1757`); `w=1-s*(1-fE)`; `round(w*v+(1-w)*vpin)`
(`MR:1763,1767`). Skip set `Y!=M3_INPROG_Y or M3_FE>=1.0 or delisted(p)` plus `s<=0` (`MR:1760-1762`)
— matches all four listed conditions. Pinned clocks exactly the five listed (`MR:727-748`); the
not-pinned list is corroborated by `MR:719-722`. Fenced season-state read `MR:6-30`.

### 29. `L3_step22_start_value_floor` — CONFIRMED
`FLOOR_YRS={1:0.45,2:0.35,3:0.28,4:0.21,5:0.13,6:0.09}` (`MR:1779`), `FLOOR_TAIL=0.05` (`MR:1780`),
`floor_frac = FLOOR_YRS.get(yis, FLOOR_TAIL)` (`MR:1781`). Scope `_isreal and type=='ND' and not
_retired and not _pickless and not delisted` (`MR:1785`); `yis = Y - year`, `<1` out of scope
(`MR:1787-1788`); `max(v, round(floor_frac*v0_start))` (`MR:1789-1790`).

### 30. `L3_step23_availability_layer` — CONFIRMED
`G_FULL=22` (`LTI:25`) and the wire-time assertion vs `cp.SEASON` (`MR:1922`).
`L = 1.0 - min(g2026/22.0, 1.0)`, floored at 0 (`LTI:117`); `return_arm = section=='A' and out`
(`LTI:123`); `ret_year = 2026 if any returned else 2027` (`LTI:122`) — and `MR:860` defaults 2027.
`VALID_DESIG` / `VALID_STATUS` (`LTI:26-27`) exactly the three + three listed.
`_ret_hc_for` (`MR:1933-1940`): `nqual(_,2026) < PROVEN_N → 0.0`, age rounded and clamped to the
surface's key range. `lti_return_table.json` read directly: `young_cut 27`, `cap 0.15`, and all
**13 age-surface values 22..34** match the JSON exactly. Applied at the single `k=ret_k`
(`MR:924`), board path only. `_avail_hc` init 0.0 (`RM:1252`), set at `MR:1948`, consumed at
`RM:593`, `RM:619`, `MR:923`, `MR:959`.
Register counts independently recounted from `LTI_REGISTER.md`: **32 distinct Section-A keys, 11
Section-B** (34 A window rows, 2 repeat-LTI players) — the JSON's 32/11 is correct at the key level,
which is the level `_reg_recs` counts.

### 31. `L3_step25_forward_view_damper` — CONFIRMED
`_LSYM_SEAL` (`MR:260-262`): `r_pop` all 11 keys exact, `s` all 12 keys exact, both sha256_8 strings
(`c62b5ee8`, `efe97ee3`) exact. Age key `int(round((BASE_REF-year)+18.5))` with nearest-key fallback
(`MR:271-282`). Blend `x_form * clip(x_age/x_form, 1e-9, None)**s`, `x_form<=0 → x_age`
(`MR:283-292`). Activation `_LENS_FORM is not None and AGE_REF!=BASE_REF` (`MR:268-270`), plus the
`Y!=MA.BASE_REF` k=0 skip at `MR:373`. Two application sites only: `MR:372-379` (band) and
`MR:944-945` (level_now roll). The `s_semantics` inversion note is correct (`s=1` → identity).
Forward young floor `g<46`, `round((1-g/46)²*_v)`, both `RL_LEGF` and `RL_LEGE` required
(`EX:201-207`). `_LENS_FORM=2026` set for the +1/+2 evaluations only (`EX:187-189`).

### 32. `L2_step22_L3_step35_year_zero_lens` — CONFIRMED
`_LA_HPICK=0.35`, `_LA_HAGE=1.5`, `_LA_KCONF=25.0`, `_LA_B=2.00`, `_LA_TOL=0.005` (`MR:1249-1253`).
Kernel `exp(-0.5*(d/h)²)` (`MR:1450`), inclusion floor `w<1e-12` (`MR:1459`), shrinkage
`n/(n+25)` (`MR:1463-1464`), ladder `(pos,age,pick) → (pos,pick) → (pos) → 1.0` (`MR:1469-1476`).
Neutrality loop: `range(200)`, break at `_worst<=1e-12`, criterion `abs(1/ratio - 1)` over
`_PK`; applied rows restricted to real ND picks `1<=pk<=64` entering as `(pos, age, pick, log-pick,
anchor)` only (`MR:1491-1513`). Bound applied as `min(B, max(1/B, pre*lam))` — "m in [0.5, 2.0]" exact.
Grids `_AGEG=16..30`, `_PK=1..90`, `_V0_GRIDPK=1..90` (`MR:1245,1467`); `star` clamps
`pick→[1,90]`, `age→[16,30]` (`MR:1608-1616`). Anchor tail extrapolation
`A[max]*exp(slope*(log pk - log max))` with `slope=log(A[max]/A[max-1])/(log max - log(max-1))`
(`MR:1443-1446`). Surface split c18 (`age<=18`) / surfR (RUCK, 19+) / surfN (`MR:1515-1522`).
Freeze + signature HALT (`MR:1271-1282`, `MR:1362-1389`), `RL_V0SURF_REFIT=1` the one refit entry.
Pre-#306 control (`MR:1315-1346`, `MR:1586-1591`): `effn_min=35.0`, `h0=0.18`, `hmax=2.2`, `h*=1.15`,
`ha0=1.2`, `hamax=8.0`, `ha*=1.2`, ages `range(19,31)` — all eight values exact. Backtest guard
(`MR:1213-1224`, `MR:1620-1624`).
The `_V0SURF_GATES` comment conflict recorded in `_meta` is real and correctly resolved: `MR:1306`
literally carries `'RL_GAMMA':'0.85'` while `RM:504` defaults `'1.0'`, and `DP:28`/`CP:40`/`DR:24`
`setdefault` to `'1.0'` at import (reached via `MR:49`), so the gate resolves to `'1.0'`.

### 33. `L3_steps27_32_pick_curve_derivation` — CONFIRMED
`HP:87-103`: `EXPECT_N=1197`, `CLASS_CUT=2022`, `K_FOLDS=5`, `FOLD_SEED=20260730`, `MIN_STRATUM=20`,
`PIN1=3000`, `ND_LAST=64`, `YR_LO=2004`, `PW_FLOOR=0.11`, `QUAL_GAMES=6`, `NMIN=35.0`,
`HMIN,HMAX=0.10,0.60`, `RANGES` — every one exact.
`_es(pw) = max(0, 1-(pw-0.11)/(1-0.11))` (`HP:113-116`); `realised_full` returns 0.0 for a
never-established row (`HP:145-148`); completion `sofar(T)*((Σf/n)/(Σsofar/n))` with the
`e[2]<MIN_STRATUM` fallback to `r['v0']`, counted (`HP:180-203`).
`kernel_raw` (`HP:231-247`): `h` from `HMIN`, `+=0.02` while `h<HMAX` until `Σexp(...)>=NMIN`, plain
weighted mean — matches the JSON's growth loop and "alpha = 1, no certainty-equivalent".
`pava_ni` 1e-12 (`HP:262-275`). Superseded `pin_and_check` hard-set + `EPS=1e-3` (`HP:278-293`).
Ruled `curve_pooled` (`PN:69-83`): plain PAVA, `EPS=1e-3` descent, `s=PIN1/pooled_head`, whole curve
scaled, `max(1, round(x))`, post-round descent `ic[i]=ic[i-1]-1` — "pick_1_override: NONE" verified.
`FC:35-36`: `MISS_TOL=0.01`, `_Z_TOL=2.3263478740408408`; `_miss_fraction=0.5*erfc(d/(h*√2))`
(`FC:64-70`); degeneracy `det > 1e-9*max(s0*s2,1e-12)` (`FC:86`); resolved zone picks 1-2 / 51-64 with
3-50 unchanged (`FC:38-44`).
`FL:40-42`: `RIDGE_REL=1e-6`, `COND_MAX=1.0e6`, `NEG_CLAMP=0.0`.
Publication asserts (`HP:310-312`): 64 points, `ladder[0]==PIN1`, strictly descending — matches.
Engine-side `_split_ladder` asserts `nd[1]==3000`, strict descent 1..64, nothing past the pool
(`RM:973-991`).
Shipped artifact values re-read from `pvc_curve_v2.json`: head 3000, pick 64 = 221, pool 234.3,
domain exactly 1-64 — all exact. `EX:357` `RANGES`; `EX:590-592` posture discounts
`balanced 0.10 / contender 0.15 / rebuilder 0.05`.

### 34. `L3_step34_pool_levels` — CONFIRMED
`PN:216-238`: plain mean over the pool population, `concluded → realised_full` (never-established
0.0), `depth<=0` or thin-stratum → `r['v0']` fallback, result reported `× s`, CI `mean ± 1.96*se`.
`MIN_STRATUM` reached via `H.MIN_STRATUM` = 20. `ctab` (`PN:201-213`) is built once over all
`POOLROWS` and reused for MSD and SSP — the "shared completion table" claim is exactly what the code
does. Class window `H.YR_LO <= year <= H.CLASS_CUT` = 2004-2022 (`PN:198`). `pool_value 234.3`
matches the artifact.

### 35. `supporting_par_surface` — INCOMPLETE
CONFIRMED: `H_LOGPICK=0.40`, `MIN_GAMES=6`, `SHRINK_K=30`, `TEN_MAX=6`, `EVAL_PICKS` (9 values),
`PAR_DUAL_RULE='primary'` (`PB:36-42`, `PB:64`); `RAMP=22` (`PRD:44`); `par_at = level_at(pos,
clamp(pick,1,70)) + ramp_shr[pos][clamp(T,1,6)]` (`PRD:59-70`); `tenure = max(1, Y-draft_year)`
(`PRD:72-73`); `lvl_par` (`PRD:110-113`). Mock-only block confirmed dead on the price path (see
spot-check note below): `MULT` (`PRD:42`) reaches only `PVCm` (`PRD:134`), which is called at
`PRD:163/169` — both inside `if __name__=='__main__':` (`PRD:139`); `BETA_MARGIN` (`PRD:167`) and
`BETA_POS` (`PRD:169`) likewise; `TILT_CAP`/`WIDEN_K` live in `tilt_band` (`PRD:116-120`), whose only
callers are `PRD:183/191/213`, all inside `__main__`. All six values match.

**Missing:** the par surface's own fit cohort window — `par_build.py:40`
`DRAFT_LO, DRAFT_HI = 2003, 2018`, used live at `par_build.py:81` to select the teaching population
for `fit()`. This is a load-bearing constant of the surface that feeds `_par_prior` (L2 step 8), the
pole (L3 step 11) and the staleness `par` ratio (L3 step 19), and it appears in no group.

### 36. `global_configuration` — CONFIRMED
`data/season_state.json` re-read: `season_year 2026`, `season_total_rounds 24`, `as_of_round 20`,
`calendar_progress 0.83`, `exposure_pace 0.773`, `source_store_md5` prefix `81d24704` — all six exact.
Code fallbacks 0.58 (`RM:1011`, `MR:106`, `MR:1752`, `CP:109`) and 0.545 (`CP:86`) exact, and the
fencing behaviour (`RL_CONFIG_MODE in bake|gate|canonical` → halt) matches `RM:2-26` / `MR:6-30` /
`CP:9-33`. `AGE_REF=BASE_REF=2026` (`RM:187-188`).
Age clock (`RM:191-196`) matches all four statements, including `by(p) = _by or (year-18)` giving the
"18 in the entry year" assumption and MSD's `debut = year` / `cycle_year = year-1`.
`shipped_env_gate_values`: compared key-by-key against `data/model_config.json` `vars` — **all 59
keys present, all 59 values identical, none missing, none extra**. Spot-checked against code
defaults: `RL_GAMMA` (`RM:504`), `RL_PICK1` (`RM:929`), `RL_REPL_DROP` (`DR:35`), `RL_RECENCY_DECAY`
(`CP:71`), `RL_PRIOR_TREES` (`CP:159`), `PAR_RAMPS` (`PRD:44`), `PAR_BW/PAR_MING/PAR_K` (`PB:36-38`),
`RL_LEVEL_RAMP` (`CP:108`), the W4 family (`MR:785-822`), the ruck family (`MR:1138,1157-1159`),
`RL_UNCONSERVE` (`RM:530`) — every one equals the manifest string, so `_meta`'s "equals every code
default" claim holds.
`gates_NOT_in_the_manifest` verified: `RL_UNCOMP_S` (`RM:528`), `RL_V0_LENS` (`MR:1393`, default
`'1'`), `RL_V0SURF_REFIT` (`MR:1272`), `RL_LSYM_TAB` (`MR:265`), `RL_CONFIG_MODE` (`MR:12-13`).
`layer_order_inside_ev` re-derived by reading `ev` top to bottom (`MR:1698-1740`), then `_ev_m3`
(`MR:1758-1767`), then the floor rebind (`MR:1783-1790`), then `EX:177` — the ten steps and their
order are exactly as listed.

---

## Omissions — value-path constants in NO group

Scan: every numeric literal in `rl_model.py` and `_merged_recover.py` outside comments (2,100
occurrences) was extracted and tested against the JSON text, then every non-match was traced to its
call site to decide whether it is on the shipped `ev()` path.

**Substantive (would change a rebuild):**

1. **`level_demo` + `_role_decay_hc` internals — `rl_model.py:416-417, 423-433, 434-480`.**
   The largest omission. `level_now → level_demo` supplies `cur` to `proj_from_peak` (`RM:584,591-592`),
   `_proj_w4` (`MR:914,921-922`), `prod_floor` (`RM:601,618`), `_prod_floor_w4` (`MR:943,958`) and
   `v_at_peak` (`DP:231`) — it is load-bearing on **every** price. None of its ~20 constants are in
   CONSTANTS.json: qualifying filter `games>=3`; the sub-3-game current-year cameo merge `0<gm<3`;
   prior weights `0.60**(ly-y) * min(gm,18) * (0.25 if gm<8 else 1.0)`; `base=lg/16.0`;
   `proven = count(games>=10) >= 4`; `old = age > peak_age+3`; the `0.5*prior + 0.5*median` robust
   baseline over the last 4 qualifying seasons; the B1 breakout rule (`len>=3`, K=3 run, `ratio>=1.4`,
   only-raise); the recency floor `min(lg,18)`; improving `conf = base*(1+growth/40.0)`, `cap=0.83`;
   `SPIKE_CAP={'KPD':0.60}`; older-decline `agef=clamp((age-peak)/6.0,0,1)`, `conf=base*(0.60+0.60*agef)`,
   `cap=0.92`; prime-dip `conf=base*0.30`, `cap=0.92`; final `clamp(conf, 0.20, cap)`;
   `ROLE_HC_MAX=0.07` with its gates (`_season_games()<7`, `age < peak+1`, `1<=games<3`,
   `games/season_games >= 0.35`, `drop < 0.30`).
   `CONSTANTS_SOURCES.md` **acknowledges** this at the foot of its exclusion table ("live-but-unrecipe'd
   … Flagged, not folded in"). That is an honest disclosure, but the rebuilder receives
   `CONSTANTS.json` alone, so as delivered the level input to every price is unreproducible.

2. **`BASEPK_REG` / `basepk_c` construction — `rl_model.py:235-236, 333-358`.**
   `_dev_advance` calls `cp = basepk_c(g, effpk(p))` (`RM:492`) as the pedigree-catch-up term, so this
   surface is on the value path for the +1/+2 forward boards (inert at `AGE_REF==BASE_REF`). Missing:
   `pkbest` = mean of the top-2 seasons with `games>=10` from debut (`RM:236`); the `len(pw)>=4`
   minimum-sample rule per (position, band) (`RM:342`); the `POOL[b]` / `bandpeak` fallback literal
   `75` (`RM:344,227`); the cross-band monotone clamp `row[b]=min(row[b],row[b-1])` (`RM:356`); and
   `_rw(y)=1.0` (equal year weighting, `RM:333-334`). The JSON names `basepk_c` in the L2 step 7
   formula but records nothing that would let it be rebuilt.

3. **`wage` None-age fallback `21`** — `_merged_recover.py:461`, `(a or 21)`. See group 20.

4. **`fadew` None-age fallback `25.0`** — `_merged_recover.py:882`. See group 18.

5. **par surface fit window `DRAFT_LO, DRAFT_HI = 2003, 2018`** — `par_build.py:40, 81`. See group 35.

**Trivial / unreachable (listed for completeness, not counted as defects):**

6. `build_pvc` NaN-fill sentinel `5000.0` (`RM:779`) — on the import-time fit chain that sets `PVC[1]`
   → `BOARD_FACTOR` → `SCALE`, but reachable only if pick 1 has no samples within ±4.
7. `_fit_mature` / `_build_v0_guard` running-min sentinels `1e9`, `1e18` (`MR:1328,1343`, `RM:1127`) —
   pre-#306 control path and guard initialisation.
8. `_v7`'s implicit `asc<1.0` entry gate (`MR:607`) — noted in group 10.
9. `KAPPA=0.10; SCONV=30.0; LOWBASE=54.0` (`RM:504`) — grep across the whole engine returns only this
   definition line. Genuinely dead; correctly omitted, though not listed in the exclusion table either.

---

## Exclusion spot-checks

The sources file's exclusion table asserts that `rl_model.value()` / `proj_value()` is a superseded
parallel path. I re-verified the supersession itself (`EX:68-69` execs `_merged_recover` and binds
`_ev = _ens['ev']`; `EX:181` prices every player with `_ev`, never `value()`) and then spot-checked
two named exclusions.

### Spot-check A — `pedmix` (`RM:538`, "no caller") — **CONFIRMED DEAD**
`grep -rn '\bpedmix\b' --include=*.py engine/` returns exactly **one** line: the definition itself,
`rl_model.py:538`. No call site anywhere in the engine tree — not in `_merged_recover.py`, not in
`rl_export.py`, not in `forward_valuation/`. The constants `0.50`, `0.32`, `9.0` cannot reach any
value. Exclusion justified.

### Spot-check B — `out_tilt` and `TILT_REF / GAIN_UP / W_UP / UP_MAX / TILT_HI / GAIN_DN / W_DN / DN_MAX / TILT_LO / NBAD_REF / SUS_MIN` (`RM:1029-1051`, "out_tilt cut at cont.21; not called") — **CONFIRMED DEAD on the value path**
`out_tilt` appears at exactly two places: its own `def` (`RM:1039`) and the obituary comment inside
`value()` (`RM:1082`) recording the cut. The dial names appear at their definitions (`RM:1029-1032`),
inside `out_tilt`'s own body, and at **one** other site — `rl_export.py:520`,
`TILT={k:g[k] for k in [...]}`. I opened that line: it is a **metadata dict** copying the literals
into the exported board JSON alongside `DEBUT_AGE`/`TYPEOFF`; it does not call `out_tilt` and does not
enter any price. So the exclusion is correct, with one nuance worth recording: these literals *are*
re-published as board metadata even though they price nothing.

*Corroborating third observation (not one of the two, but it strengthens the table):* `survival`
(`RM:575-580`, excluded as "removed from the value path at `RM:1078`") **is** still called, at
`EX:279` inside `player_rec` — but the result is discarded: the very next line writes the literal
`'surv':1.0` into the record (`EX:286`), and `RM:1078` sets `surv=1.0` in `value()`. So `BUST_BAND`,
the `clamp(1-delta/20,0.4,1.6)` multiplier and the `1-games/40` fade reach no output. Exclusion
justified, and the table's reasoning is sound.
