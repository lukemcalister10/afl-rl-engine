# CONSTANTS.json — provenance

Verification appendix material. **Not for the rebuilder** — the rebuilder gets `CONSTANTS.json` alone.

Code root (read-only):
`/tmp/claude-0/-home-user-afl-rl-engine/857170f9-1a0a-5fff-ab5e-32b13cff3f0e/scratchpad/wt-lens/`

All paths below are relative to that root. Line numbers are as of the tree read on 2026-08-05.

**Verification round 1 applied — 2026-08-05.** `verify_constants.md` returned 31 CONFIRMED / 1 WRONG /
4 INCOMPLETE over the 36 groups then present. All 11 corrections were applied to `CONSTANTS.json`
(2 value fixes, 6 completions, 3 new groups; 36 → 39 groups). Provenance for every new or changed
entry is marked **[R1]** below.

Short names used throughout:

| short | file |
|---|---|
| `RM` | `engine/rl_after/rl_model.py` |
| `MR` | `engine/rl_after/_merged_recover.py` |
| `EX` | `engine/rl_after/rl_export.py` |
| `LTI` | `engine/rl_after/lti_register.py` |
| `DP` | `engine/forward_valuation/distribution_pricing.py` |
| `CP` | `engine/forward_valuation/conditional_prior.py` |
| `DR` | `engine/forward_valuation/dist_redesign.py` |
| `PB` | `engine/forward_valuation/par_build.py` |
| `PRD` | `engine/forward_valuation/par_redesign.py` |
| `HP` | `session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py` |
| `FC` | `session_2026-07-30/item279/panel/fitter_control.py` |
| `FL` | `session_2026-07-30/item279/panel/fitter_loclin.py` |
| `PN` | `session_2026-07-30/item279/panel/pooled_numeraire.py` |

Data/artifact files quoted for values the recipe treats as engine constants:
`engine/rl_after/params.json`, `engine/rl_after/ycred_table.json`,
`engine/rl_after/lti_return_table.json`, `engine/rl_after/pvc_curve_v2.json`,
`engine/rl_after/pick_redenomination.json`, `data/model_config.json`, `data/season_state.json`.

---

## Per-group provenance

### `_meta`
- shipped price function is `MR:1698` (`def ev`) then rebound at `MR:1783`; `EX:68-69` execs `_merged_recover` and takes `ev` as the board's single valuation source.
- comment conflict 1: `MR:405-407` and `MR:530` (comments) vs `RM:527` (`UNCOMP_S_DEFAULT=0.10`).
- comment conflict 2: `MR:1306` (`'RL_GAMMA':'0.85'`) and `MR:1305` (comment claiming engine defaults) vs `RM:504` (`RL_GAMMA` default `'1.0'`); neutralised by `DP:28` / `CP:40` / `DR:24` `os.environ.setdefault('RL_GAMMA','1.0')`, which run at import via `MR:49`.
- comment conflict 3: `RM:908-928` (block comment) vs `RM:931` (`BOARD_FACTOR=(_P1/PVC[1])*_NUM['s']`).
- **[R1]** `verification_round_1_applied` block — sourced from `verify_constants.md` (2026-08-05); the
  per-value provenance for each correction it records is marked **[R1]** in the sections below.

### `L1_step50_replacement_bars`
- `REPL` — `RM:501`
- position vocabulary `GRP` — `RM:67`; `_ELIG_MAP` — `RM:145`
- collapse rule `_collapse_elig` — `RM:146-152`
- `_CROSS_CLASS` data-error pairs — `RM:158-159`; handling `RM:166-176`
- lower-bar selection — `RM:83-86`, `RM:99-109`
- `LIVE_SEASON` — `RM:98`

### `L2_step2_season_qualification_bars`
- soft logistic `_EVW_Q0`, `_EVW_QW` — `MR:205`; used in `_ev_qual` `MR:207-208`
- **[R1]** `evaluated` sample points recomputed from `MR:207-208` against `MR:205`: the exponent is
  `(g - _EVW_Q0)/_EVW_QW = (g-11.0)/1.1 = ±1.8181818…`, so `q(9)=0.1396521834167601` and
  `q(13)=0.8603478165832398` (the file previously carried the `±1.8` pair `0.14185106490048777` /
  `0.8581489350995122`). `q(11)=0.5` unchanged.
- hard bars: 6 → `MR:1063`, `MR:1065-1067`, `MR:1686`; 10 → `MR:168` (`_nqual`); 14 → `CP:108` (`LEVEL_RAMP`); 22 → `CP:49` (`SEASON`), `LTI:25`
- proration `_fEy` — `MR:126-129`; `SEASON_FE` — `MR:106`; `_playable` — `MR:130-131`
- fE fenced read — `MR:6-30`, `RM:2-26`, `CP:9-33`
- register out-name fE = 1.0 — `MR:123-128`
- 10-bar not prorated (declared) — `MR:169-175`; `G_ADQ` 12 unprorated — `MR:101-105`, `MR:515`
- prorated 12-bar for LD — `MR:841`, `MR:846`
- fE in effect 0.83 — `data/season_state.json` `calendar_progress`

### `L2_step3_era_adjustment`
- `era` loop and games≥6 bar — `MR:51-54`
- `REF` — `MR:55`
- consumers — `MR:1063` (`bestlvl`), `MR:840-847` (`_kpf_LD`), `MR:1695` (`_staleness_grade`), `MR:2003` (`recent_ratio`)
- "not era-adjusted" for `_lvlcurr` — `MR:301-305`

### `L2_step5_pick_split`
- `ND_CURVE_LAST` / `POOL_PICK` — `RM:212-213`
- `PICKLESS` — `RM:179`
- `effpk` / `is_pool` — `RM:214-215`; classification loop `RM:260-281`
- `KMAX` 70 — `CP:48`
- iso pick domain — `MR:485`
- `_teaches_curve` — `RM:313`; `CURVE_FIT_SITES` — `RM:332`
- `hist` window 2003–2021 — `RM:283`

### `L2_step6_evidence_dials`
- `_EVW_R` — `MR:204`; `_EVW_GK`, `_EVW_EST`, `_EVW_TAU` — `MR:206`
- `_ev_qual` / `_ev_rec` / `_ev_est` — `MR:207-210`; `_ev_pw` — `MR:293-296`
- `PROVEN_N` — `MR:100`; `_nqual` — `MR:168`
- `c = n/4` partial convention — `MR:876`
- gate `_EVW` — `MR:203`

### `L2_step7_recency_and_games_trust`
- `_DAMP_K` / `_wg` — `MR:186-187`; gate `_DAMP` — `MR:185`
- `LDECAY_G` and `_ldg` — `MR:133-134`; applied in `_lvlcurr` `MR:301-305`
- games/130 clamp — `RM:493-495` (`_dev_advance`)
- `RL_RECENCY_DECAY` — `CP:71`; `EXPO_INPROG_Y` / `EXPO_F` / `EXPO_DEN` — `CP:85-87`; `LEVEL_RAMP` — `CP:108`
- exposure_pace 0.773 in effect — `data/season_state.json`

### `L2_step8_level_blend`
- chain `_coreM1` — `MR:560-580`
- `_est` up/down branches — `MR:550-559`; `DOWN_TOL` — `MR:140`; `TOL_M1`/`G_ADQ`/`WIN`/`S_M1` — `MR:515`; gate `_LSYM` — `MR:549`
- `FLAT_TOL_G` (dormant twin only) — `MR:134`, consumed at `MR:313`
- `_L3_AX` / `_L3_AY` — `MR:520-521`; `_SAGE29_VAL` — `MR:531`; `_L3_AY_EFF` — `MR:532`; `_S_AGE` — `MR:533`; gate `_SAGE29` — `MR:530`, `_L3_AGE` — `MR:519`
- `_AGEMULT_X` / `_AGEMULT_Y` and clip — `MR:138-139`
- `_FB_AGE` / `_FB_LCR` / `_FB_Z` — `MR:156-158`; `_fbump` — `MR:159-162`; `_agemult2` and clip [0.53,0.98] — `MR:163-166`; gate `_FORMDECL` — `MR:155`
- `_par_prior` and the 1..6 tenure clamp — `MR:306-308`
- form-anchor clock — `MR:224-236`, gate `_LEGF_ON` `MR:223`

### `L2_step9_opportunity_test`
- `_eo` — `MR:346-351`; pin-aware rebind — `MR:736-742`
- `_upS` tables `_UP_DLX` / `_UP_NY` / `_UP_S` — `MR:340-341`; evaluation `MR:342-345`
- `_inferM1` target and bar −3 — `MR:589-596`; gate `_EO2` — `MR:588`

### `L2_step10_injury_gap_penalty`
- `_ABS_L_REF` — `MR:649`; `_ABS_CAP` — `MR:650`; `_ABS_FADE_K` — `MR:661`
- `_ABS_AGE` / `_ABS_EFF` — `MR:662-665`; `_abs_frac` — `MR:666-670`
- gap selection `_abs_gap` — `MR:671-697`; shift `_abs_shift` — `MR:698-701`
- charge/fade `_lvl_eff_abs` — `MR:703-714`; bind `MR:715`; gate `_ABSENCE` — `MR:648`

### `L2_steps11_13_forward_band`
- `Q` — `CP:45`; `GROUPS`/`GIDX` — `CP:46-47`; `_feat` — `CP:120-123`
- `fwd_best3_from` — `CP:56-63`
- **[R1]** `band_target` four-branch ladder read line-by-line: window `lo=max(Y,debutyr)` `CP:58`;
  qualifying filter `games>=6` and `lo<=year<=cap` `CP:59`; `>=3` → mean of top 3 `CP:60`;
  `>=1` → mean of what qualifies `CP:61`; `0` qualifying → `max` over any season with `games>0`
  `CP:62`; never played → `0.0` `CP:63`
- **[R1]** v7 form-relax entry gate `asc < 1.0` — `MR:607` (`if _W4V7 and asc<1.0:`), with
  `asc` set at `MR:599`
- `build_cond_prior` window and hyperparameters — `CP:143-162` (`_NTREES` `CP:159`)
- training pool + MSD exclusion — `MR:58-62`, gate `_L4_MSD` `MR:58`
- `q97m` frozen load — `MR:84-93`; ceiling floor at band[4] — `MR:369`
- `_v7` taper — `MR:597-612`; `V7_FORM_W` — `MR:785`; gate `_W4V7` — `MR:784`; real-only wrapper `MR:622-627`
- train/serve level asymmetry — `MR:628` (`cp._lvl_eff=_inferM1`) vs `PRD:124-126` (`retrain` binds `lvl_par`)
- first-evidence smoothing `_prod_path` — `MR:1656-1676`

### `L2_step14_L3_step2_age_path`
- `DELTAS` — `RM:502`; `frac` — `RM:503`; duplicate `_fa` — `RM:1033`
- horizon/stop/floors — `RM:587-596` and the W4 copy `MR:917-928`
- `PEAK`, `PEAK_AGE` — `RM:58` reading `engine/rl_after/params.json`
- `params.json` `AGE_CURVE` and `_smooth_tail` −0.010 rule — `RM:59-66`
- proof that `AGE_CURVE` is off the pricing path: only consumer is `_agecurve` `RM:481-485`, called from `_dev_advance` `RM:486-495`

### `L3_step3_captaincy_premium`
- `LCAPT_*` — `RM:380`; `_capt_ruled` — `RM:385-387`; `_softplus` — `RM:383-384`
- `CAPT_GAIN`/`CAPT_EXP`/`CAPT_CAP` — `RM:382`; `_capt_saturating` — `RM:388-392`
- `CAPT_THRESH`/`CAPT_M`/`CAPT_W` — `RM:531`
- dispatcher `capt_prem` — `RM:398-400`; gate `_CAPT` — `RM:381`; `_CAPT_OFF` — `RM:393-397`

### `L3_step4_replacement_netting`
- `REPL_DROP_PTS` / `REPL_DROP` — `DR:35-39`; applied in `price6` — `MR:381-387`
- `S_SH` — `RM:505`; `posval` — `RM:507`
- year-zero dual-bar blend: `RM:614-626` (floor half), `MR:954-966` (proven copy), `DP:272-277` (projection half)
- `futblend` — `RM:115-128`; gate `_FLEX` — `RM:114`

### `L3_step5_aggregation_and_discounts`
- ×21 and the discount exponent — `RM:595-596`, `MR:927-928`, `RM:626`, `MR:966`
- `LENS` — `RM:540`; posture keys — `RM:548-552`; gate `_LEGE` — `RM:547`
- ×1.05 key-position — `RM:597`, `MR:929`
- `PMAX` — `RM:180`; runway/elite — `RM:598`, `MR:930` (form-anchored age `ah` at `MR:913`)

### `L3_step6_currency`
- 7000 anchor / 99th percentile / `SCALE` — `RM:731`; `STBL` toggles `RM:730,732`
- `GAMMA` — `RM:504`; setdefaults `DP:28`, `CP:40`, `DR:24`; manifest `data/model_config.json` `vars.RL_GAMMA`
- `RW_S` / `level_stable` — `RM:409-415`
- `_P1` — `RM:929`; `_load_numeraire` and 1e-9 coherence — `RM:859-904`; `BOARD_FACTOR` — `RM:931`
- `s` / `pooled_head_pre_scale` / `published_pin` — `engine/rl_after/pvc_curve_v2.json` `numeraire`
- `1.0524` — `engine/rl_after/pick_redenomination.json` `factor`, loaded `EX:132`, applied `EX:177,181`; fallback literal at `one_source_selftest.py:65`, `guard_correction_canary.py:112`, `s4_matrix_M1v7.py:129`
- order/ratio gates — `EX:220-239`
- numeraire halt — `EX:161-165`, `RM:981`
- reference-basis constants: `EXP_PEAK_BASE` `RM:639`, `EXP_RETAIN` `RM:640-642`, `EXP_PICK_SLOPE`/`EXP_LOGREF` `RM:643`, `EXP_BLEND_GAMES` `RM:644`, clamp `RM:650`, `V4_SPIKE_RETAIN` `RM:634`, spike guard `RM:676-683`, `cohort_peak` `RM:570-574`, `BETA_POS`/`ICPT_POS` `RM:181-182`, `track_delta` 0.78 `RM:567`, `RWE` `RM:562`
- import-fit dials: `ALPHA` `RM:769`, `PVC_ALPHA_LO/HI` `RM:812`, `PVC_REPL_BUF` `RM:813`, `_alpha_pvc` `RM:819`, `CURVE_H` `RM:906`, ±4 window `RM:776,832`, min 210 `RM:799,858`, `Wf` `RM:836`, parametric top `RM:838-842`, `_deplateau` `RM:936-947`, `DEF_CURVE` `RM:220`

### `L3_step7_demonstrated_floor`
- `prod_floor` — `RM:600-627` (horizon `RM:615`, roll `RM:618`)
- proven-player copy `_prod_floor_w4` — `MR:940-967`, bind `MR:968`
- duplicate-loop hazard note — `RM:611-613`, `MR:947-953`

### `L3_step8_band_averaging`
- `WQ6` — `MR:94`; applied in `price6` with `_det_dot` — `MR:386`; `_det_dot` — `MR:41-42`
- `SCALE_DIST` — `DP:48`
- `v_at_peak` max(prod, floor) — `DP:283`

### `L3_step9_proven_reweighting`
- dials `W4_CRED`/`W4_KPFUP`/`W4_FADE`/`W4_OVPX` — `MR:786-789`; `W4_OVPX_D` — `MR:790`
- `W4_KPFTOP` — `MR:820`; `_KPF_M0`/`_KPF_MS` — `MR:821-822`
- context `_w4_ctx` (`gm`, `kt`, `cw`, `dur`, `sh`, `fadew`, `ovpx`, partial-proven KPF) — `MR:850-892`
- **[R1]** `fadew` None-age fallback `25.0` — `MR:882`
  (`np.clip(((a if a is not None else 25.0)-23.0)/3.0,0.0,1.0)`)
- **[R1]** OVPX scope correction ("a fully proven player of ANY position never carries it"):
  the compress is written only on the sub-proven branch and the partial-proven KPF branch —
  `MR:885` (partial KPF) and `MR:891` (thin-career else-branch); the fully-proven path at
  `MR:868-880` never sets `ctx['ovpx']`, and `_w4_W` applies it at `MR:905-906`.
  `W4_OVPX_D` (`MR:790`) has no KPF/KPD/RUCK key, so those positions are zero by table absence.
- weight `_w4_W` incl. `max(W,0.05)` — `MR:893-907`
- gates `_W4FWD`/`_W4OVP`/`_W4KPF` — `MR:780-783`
- application in `_proj_w4` — `MR:908-932`, bind `MR:932`; in the floor — `MR:966`

### `L3_step10_young_credit`
- `_YC_W` — `MR:998`; `_YC_KPF` — `MR:999`; `_YC_G0`/`_YC_TMIN`/`_YC_TMAX` — `MR:1000`, overwritten from the table at `MR:1006-1009`
- `_ycred_games` and the LTI clock advance — `MR:1010-1022`; `_LTI_CLOCK` — `MR:120`
- `_ycred_mult` (log-pick interp, 6-game blend, clip ≥0, φ) — `MR:1023-1040`
- wrapper — `MR:1041-1045`; gate `_W4YNG` — `MR:781`; halt-if-table-absent — `MR:1003-1005`
- `G0`, `grid_picks` (90), year range 2007–2026 — `engine/rl_after/ycred_table.json`

### `L3_step11_pole`
- `_SCALE` re-level dict — `MR:394`; `par_pole` — `MR:390-395`
- `synth` (2 seasons × 18 games) — `MR:389`
- `RECX`/`RECY` — `MR:94`; `recover` — `MR:388`
- `wage` / `tfade` / `expgate` / `w` and the blend — `MR:457-466`
- **[R1]** `wage` None-age fallback `21` — `MR:461`
  (`0.0 if pos=='RUCK' else float(np.clip(1-((a or 21)-20)/6,0,1))`); `a=MA.age(p)` at `MR:460`
- `POLE_RAMP` — `MR:100`; `_expgate` — `MR:297-300`
- `eff_ten` — `MR:309-311`
- `_lvl_wt` (perf) — `CP:100-104`
- pole table freeze over 1..KMAX × T 1..6 — `MR:498-500`

### `L3_step12_output_proportionality`
- `UNCOMP_DELTA` / `UNCOMP_DECAY` / `UNCOMP_TAU` / `UNCOMP_S_DEFAULT` / `UNCOMP_S` — `RM:524-529`; gates `_UNCOMP` `RM:523`, `_UNCONSERVE` `RM:530`
- `rho_out` — `MR:412-427`
- map `_uncomp_prod` (captain-off, ramp, E, w, log-blend, `C[pos]`, delta) — `MR:428-453`
- reference build `V_ref_b` / `RHO_DEN` / `C[pos]` — `MR:1869-1906`
- hook site in `raw_ev` — `MR:455`

### `L3_step13_pick_order_guard`
- `_ISOFADE_TAU` — `MR:478`; gate `_ISOFADE` — `MR:477`
- table build (PICKS 1..70, T=4 synths, double isotonic) — `MR:485-492`
- `iso_corr` — `MR:493`; `iso_eff` — `MR:494-497`
- six application sites — `MR:1057`, `MR:1165`, `MR:1199`, `MR:1665`, `MR:1674`

### `L3_step15_ruck_caps`
- `RUC_PRIOR_CAP` — `MR:1138`; `RUC_CEIL_HEAD` / `RUC_CEIL_REFPK` / `RUC_YRH` — `MR:1157-1159`; gate `_W4RUC` — `MR:1156`
- grid build `_build_ruc_ceiling` (linspace 15→150, 46 pts, monotonised) — `MR:1161-1169`
- `_ruc_head_core` (fpk/fage knots) — `MR:1170-1174`; age-axis split — `MR:1175-1177`
- `_ruc_ceiling` — `MR:1178-1182`; `_ruc_prior_cap` — `MR:1183-1184`
- bind condition inside `ev` — `MR:1702-1704`
- unconditional start-value cap ordering — `MR:1202-1205`, `MR:1620-1624`

### `L3_step16_kpf_compress`
- `W4_KPFSH` — `MR:791`; `W4_KPFSH_DEM` — `MR:819`
- `_kpf_LD` (window, 12-bar, top-2, fork-v exclusion & +2 extension, fallback) — `MR:823-848`
- `_kpf_prod_efv` — `MR:1051-1058`; `_B6PIN` — `MR:1046-1050`
- gates and split formula — `MR:1712-1724`

### `L3_step17_scrap_and_delisting`
- scrap 0.02 — `MR:1700`
- `delisted` — `MR:1060`
- floor scope exclusions — `MR:1785`
- active/back-board recall — `RM:713-719`, `RM:1312-1353`

### `L3_step18_sitout_retention`
- `R_SURF` — `MR:1104-1106`; `_RS_KNOTS` — `MR:1107`
- `_dv_surf` — `MR:1112-1113`; `_R_surf` with the KPP pointwise-max floor — `MR:1114-1125`
- `LAM_SIT` — `MR:1126`; `_sitout_cls` — `MR:1127`
- `sitout_ev` (tau, exponent 1.5, games-at-pace) — `MR:1650-1655`
- trigger `nseas_pro` — `MR:1066-1067`, used `MR:1728-1730`
- superseded depth-only table (quoted in code) — `MR:1094`
- `_BOARD_PATH` — `MR:1111`

### `L3_step19_staleness`
- onset / stalled / mediocre formulas — `MR:1731-1739`
- `_D8Q` / `_D8G1` / `_D8G2` — `MR:1680-1682`; `_staleness_grade` — `MR:1683-1697`
- tenure + par + `pr` — `MR:1727-1728`
- `PR.tenure` — `PRD:73`; `PR.par_at` — `PRD:68-71`

### `L3_step21_midseason_clock_blend`
- `M3_FE` — `MR:1752`; `M3_DEN` — `MR:1753`; `M3_INPROG_Y` — `MR:725`
- `_m3_s` / `_ev_m3` — `MR:1755-1767`
- pinned clocks `_M3PIN` and wrappers — `MR:724-748`
- season-state read + fenced halt — `MR:6-30`; file `data/season_state.json`

### `L3_step22_start_value_floor`
- `FLOOR_YRS` — `MR:1779`; `FLOOR_TAIL` — `MR:1780`; `floor_frac` — `MR:1781`
- application and scope — `MR:1783-1790`
- basis `v0_start` — `MR:1620-1624`

### `L3_step23_availability_layer`
- `G_FULL` — `LTI:25`; assertion vs `cp.SEASON` — `MR:1922`
- `L` lost fraction — `LTI:117`; `return_arm` — `LTI:123`; sections — `LTI:16,78`; `VALID_DESIG`/`VALID_STATUS` — `LTI:26-27`
- `_avail_hc` init — `RM:1252`; set — `MR:1948`; applied — `RM:593`, `RM:619`, `MR:923`, `MR:959`
- `_fEy` completeness — `MR:123-129`
- `_ret_hc_for` (proven gate `nqual<4 → 0`, age clamp) — `MR:1933-1940`; application at `k=ret_k` — `MR:924`, ctx at `MR:858-860`
- `cap` 0.15, `young_cut` 27, `age_surface` — `engine/rl_after/lti_return_table.json`
- gates `_AVAIL_ON` — `MR:118`; `_LTI_RETURN_ON` — `MR:119`
- register counts 32 A / 11 B — `MR:1970` (print string)

### `L3_step25_forward_view_damper`
- `_LSYM_SEAL` (`r_pop`, `s`, both sha256_8) — `MR:260-262`; load/override — `MR:263-267`
- `_lsym_active` — `MR:268-270`; `_lsym_age` — `MR:271-276`; `_lsym_s` — `MR:277-282`; `_lsym_blend` — `MR:283-292`
- two application sites — `MR:372-379` (band), `MR:944-945` (level roll)
- forward young floor (46 games, φ²) — `EX:201-207`
- form anchor `_LENS_FORM=2026` — `EX:187-189`; consumed `MR:367`, `MR:385`

### `L2_step22_L3_step35_year_zero_lens`
- `_LA_HPICK` / `_LA_HAGE` / `_LA_KCONF` / `_LA_B` / `_LA_TOL` — `MR:1249-1253`
- kernel `_kern` / estimator `_est` / `_shrink` — `MR:1450-1464`
- shrinkage ladder — `MR:1469-1476`
- neutrality iteration (200, 1e-12, applied population) — `MR:1491-1513`
- grids `_AGEG` / `_PK` — `MR:1467`; `_V0_GRIDPK` / `_V0_LGRID` — `MR:1245`
- anchor + tail extrapolation — `MR:1440-1446`
- surface split c18/surfN/surfR — `MR:1515-1522`; `star` lookup — `MR:1608-1616`
- basis file (declared input, self-reference barred) — `MR:1423-1432`
- freeze/HALT and signature — `MR:1271-1313`, `MR:1348-1389`; gate list `_V0SURF_GATES` — `MR:1287-1306`
- pre-#306 control fit — `MR:1315-1346`, `MR:1582-1591`; gate `RL_V0_LENS` — `MR:1393`
- backtest guard — `MR:1213-1224`, `MR:1620-1624`

### `L3_steps27_32_pick_curve_derivation`
- population / class window / `EXPECT_N` / `QUAL_GAMES` / `PW_FLOOR` / `MIN_STRATUM` / `PIN1` / `ND_LAST` / `YR_LO` — `HP:87-98`
- `NMIN` / `HMIN` / `HMAX` / `RANGES` — `HP:100-103`
- establishment + structural values + counted fallback — `HP:109-209`
- `kernel_raw` (growth loop, step 0.02, weighted mean) — `HP:231-247`; `bandwidth_at` — `HP:250-258`
- boundary rule `MISS_TOL` / `_Z_TOL` / `_miss_fraction` / `_local_linear` / degeneracy guard — `FC:35-36`, `FC:57-90`; resolved zone described `FC:38-44`
- loclin-arm dials `RIDGE_REL` / `COND_MAX` / `NEG_CLAMP` — `FL:40-42`
- `pava_ni` (1e-12) — `HP:262-275`
- superseded hard-set `pin_and_check` (EPS 1e-3) — `HP:278-293`; also `PN:56-66`
- ruled `curve_pooled` (no override, EPS 1e-3, global `s`, round min 1, post-round descent) — `PN:53`, `PN:69-83`
- publication asserts — `HP:308-315`; engine-side `_split_ladder` asserts — `RM:957-992`
- folds `K_FOLDS` / `FOLD_SEED` — `HP:91-92`, `HP:213-221`
- shipped ladder + `numeraire` block — `engine/rl_after/pvc_curve_v2.json`; loaded `RM:993-997`, `MR:1838-1850`
- board `RANGES` — `EX:357`
- posture pick discounts 10/15/5% — `EX:590-592`

### `L3_step34_pool_levels`
- `lvl()` (plain mean, never-established 0, `MIN_STRATUM` fallback, ×s, 1.96 CI) — `PN:216-238`
- shared completion table `ctab` — `PN:201-213`
- pool/MSD/SSP scoping — `PN:196-198`, `PN:241-250`
- shipped declared `pool_value` 234.3 — `engine/rl_after/pvc_curve_v2.json`

### `supporting_level_demo_and_role_decay` — **[R1] new group**

Every entry from `RM:408-480`. Read from the code lines; the block comments at `RM:416-417`,
`RM:440-442`, `RM:457-459` and `RM:465-467` were used for intent only, never for a value.

- `STBL` toggle and the `level_stable` branch — `RM:408` (`STBL=False`), `RM:410-415`, taken at `RM:435`
- `SPIKE_CAP={'KPD':0.60}` — `RM:416`; `ROLE_HC_MAX=0.07` — `RM:417`
- `_season_games()` (max `games` at `BASE_REF` over the store, `22` when the season has no rows) — `RM:419-422`
- `_role_decay_hc` — `RM:423-433`: `baseline is None` → 0 `RM:424`; `_season_games()<7` → 0 `RM:425`;
  `gfut`/`_age_at` axis `RM:426`; `a_ < PEAK_AGE[g]+1` → 0 `RM:427`; current row `RM:428`;
  `1<=games<3` window `RM:429`; `games/max(_season_games(),1) >= 0.35` → 0 `RM:430`;
  `drop=clamp((baseline-avg)/baseline,0,1)` `RM:431`; `drop<0.30` → 0 `RM:432`;
  `clamp(ROLE_HC_MAX*drop,0,ROLE_HC_MAX)` `RM:433`
- `level_demo` — `RM:434-480`: truncation `year<=BASE_REF` `RM:436`; `games>=3` qualifier `RM:437`;
  `None` when empty `RM:438`; most-recent row `RM:439`; sub-3-game current-year cameo `0<gm<3`
  `RM:443` and the games-weighted merge `RM:444-445`; single-season early return `RM:446`;
  prior weight `0.60**(ly-y)*min(gm,18)*(0.25 if gm<8 else 1.0)` `RM:448-449`;
  `prior` / `growth` / `base=lg/16.0` `RM:450`; `old = a_ > PEAK_AGE[gfut]+3` `RM:451`;
  `proven = count(gm>=10) >= 4` `RM:452`; robust baseline over `qs[-4:]` with the odd/even median and
  `0.5*prior+0.5*med` `RM:453-455`, else `baseline=prior` `RM:456`;
  B1 breakout (`len(_b1)>=3`, K=3 run, pre-run mean or `prior`, `_rm/_op>=1.4`, only-raise `max`)
  `RM:460-464`; recency floor `_pmass` (no 0.25 factor) and `_cfloor=min(lg,18)/(min(lg,18)+_pmass)`
  `RM:468-469`; improving branch `conf=base*(1+growth/40.0)`, `cap=SPIKE_CAP.get(gfut,0.83)`,
  cap-lift line, `conf=max(conf,_cfloor)` `RM:470-474`; older-decline
  `agef=clamp((a_-pa_)/6.0,0,1)`, `conf=base*(0.60+0.60*agef)`, `cap=0.92` `RM:475-476`;
  prime-dip `conf=base*0.30`, `cap=0.92` `RM:477`; `conf=clamp(conf,0.20,cap)` `RM:478`;
  `lvl=conf*la+(1-conf)*baseline` `RM:479`; `lvl*(1-_role_decay_hc(p,lvl))` `RM:480`
- load-bearing proof: `level_now` — `RM:496`; consumers `RM:584`, `RM:591-592` (`proj_from_peak`),
  `MR:914`, `MR:921-922` (`_proj_w4`), `RM:601`, `RM:618` (`prod_floor`), `MR:943`, `MR:958`
  (`_prod_floor_w4`), `DP:231` (`v_at_peak`)
- previously carried only as an exclusion-table footnote in this file; that footnote is now retired
  (see "Deliberate exclusions" below)

### `supporting_basepk_pedigree_surface` — **[R1] new group**

- `pkbest` (top-2 mean, `games>=10`, `year>=debut`, `None` when empty) — `RM:235-236`
- `bandpeak` and its `75` fallback — `RM:226-227`; `DEF_CURVE` — `RM:220`
- `bandof` (first containing `[lo,hi]`, else last band) — `RM:216-219`
- teaching population `hist` (`_ft`, `_grp in (ND,RD)`, `2003<=year<=2021`, `pos in GRP`) — `RM:283`
- `_rw(y)=1.0` equal year weighting — `RM:333-334`
- band loop: `BPK`/`POOL`/`MIX` init `RM:335`; band membership on `effpk` `RM:338`;
  `MIX[b]` position shares `RM:339`; per-position `pw` on the `gfut` axis `RM:341`;
  minimum-sample rule `len(pw)>=4` and the weighted average `RM:342`;
  all-position `aw` `RM:343`; `POOL[b]` with the `75` empty-band fallback `RM:344`
- `BASEPK_REG` row build — `RM:347-357`: present cell `RM:352`; nearest-populated-band gradient
  scale `rel[b0]*(POOL[b]/POOL[b0])` `RM:353-354`; all-empty fallback `POOL[b]` `RM:355`;
  cross-band monotone clamp `row[b]=min(row[b],row[b-1])` over `1..NB-1` `RM:356`; store `RM:357`
- `basepk(g,b)` three-tier lookup — `RM:358`
- `BANDS` / `NB` / `BAND_ANCHOR` — `RM:58` and `RM:359`, reading `engine/rl_after/rl_passmark.json`
  (`bands` = the 8 `[lo,hi]` pairs, `BAND_ANCHOR` = the 8 anchors)
- `bandcoord` (clamped piecewise-linear over `BAND_ANCHOR`) — `RM:360-366`
- `basepk_c` (linear interp between the two bracketing bands) — `RM:367-369`
- consumption on the value path: `cp=basepk_c(g,effpk(p))` — `RM:492`, used in the `_dev_advance`
  blend at `RM:494`; inert at `AGE_REF==BASE_REF` via the `a1==a0` early return at `RM:489`

### `_omitted_literals_trivial_or_unreachable` — **[R1] new group**

- `build_pvc` NaN-fill sentinel `5000.0` — `RM:779` (loop `RM:778-779`); on the import-time fit chain
  that sets `PVC[1]` → `BOARD_FACTOR` (`RM:931`) → `SCALE`, reachable only when pick 1 has no sample
  inside the ±4 window at `RM:776`
- `_fit_mature` running-min initialisers `1e9` (`mine`) — `MR:1328`; `1e18` (age-monotone `run`) — `MR:1343`
- `_pick_equiv` nearest-search initialiser `bd=1e18` — `RM:1127`
- v7 entry gate `asc<1.0` — `MR:607` (also recorded under `L2_steps11_13_forward_band`)
- dead dials `KAPPA=0.10`, `SCONV=30.0`, `LOWBASE=54.0` — `RM:504` (definition line only; no reader
  anywhere in the tree)

### `supporting_par_surface`
- `H_LOGPICK` / `MIN_GAMES` / `SHRINK_K` / `TEN_MAX` / `GROUPS` / `EVAL_PICKS` — `PB:36-42`; `PAR_DUAL_RULE` — `PB:64`
- **[R1]** fit cohort window `DRAFT_LO, DRAFT_HI = 2003, 2018` — `PB:40`, applied live in `gather()`
  at `PB:80-81` (`DRAFT_LO <= draftyr(p) <= DRAFT_HI`, alongside the `GRP` position filter and the
  `pick or _ft` filter); `draftyr(p) = CP.debutyr(p) - 1` at `PB:44`; per-player tenure rows
  `T = 1..TEN_MAX` read at `Y = draft_year + T` and the pick cap `min(MA.effpk(p), CP.KMAX)` — `PB:85-87`
- `par_at` — `PRD:68-71`; `tenure` — `PRD:73`; `lvl_par` — `PRD:110-113`; `RAMP` — `PRD:44`
- mock-only `MULT` `PRD:42`, `BETA_MARGIN` `PRD:45`, `BETA_POS` `PRD:50`, `TILT_CAP`/`WIDEN_K` `PRD:52-53` (used only under `PRD:139` `__main__`)

### `global_configuration`
- season state — `data/season_state.json`; fallbacks `RM:1011`, `MR:106`, `MR:1752`, `CP:86`, `CP:109`
- `AGE_REF` / `BASE_REF` — `RM:187-188`; `_LENS_FORM` — `RM:189`
- age clock `by` / `_cycle_year` / `_age_at` / `debut` — `RM:191-196`
- manifest `vars` — `data/model_config.json`
- gates not in the manifest — `RM:528` (`RL_UNCOMP_S`), `MR:1393` (`RL_V0_LENS`), `MR:1272` (`RL_V0SURF_REFIT`), `MR:265` (`RL_LSYM_TAB`), `MR:12-13` / `RM:8-9` (`RL_CONFIG_MODE`)
- layer order — `MR:1698-1740` then `MR:1758-1767` then `MR:1783-1790` then `EX:177,181`

---

## Deliberate exclusions

`rl_model.value()` / `proj_value()` is a **superseded** parallel valuation path: `rl_export` renders
`_merged_recover.ev()` (`EX:68-69`, `EX:181`). Its private constants were read and excluded because the
recipe describes none of them:

| constant | line | why excluded |
|---|---|---|
| `GRACE`, `LOS_C`, `LOS_P`, `los_decay` | `RM:401-406` | feeds `unpl_eq` in `value()` only |
| `debut_factor` (`0.58` ref, `Apos`/`Aneg`) | `RM:1012-1020` | `value()` only |
| `SLIP_CAP/REF/CONF/MAXLOS`, `track_slip` | `RM:1021-1026` | not called on any live path |
| `TILT_REF`, `GAIN_UP/DN`, `W_UP/DN`, `UP_MAX`, `DN_MAX`, `TILT_HI/LO`, `NBAD_REF`, `SUS_MIN` | `RM:1029-1051` | `out_tilt` cut at cont.21; not called |
| `survival`, `BUST_BAND` use | `RM:575-580` | removed from the value path at `RM:1078` |
| ~~`SPIKE_CAP`, `ROLE_HC_MAX`, `level_demo` internals~~ | `RM:416-480` | **[R1] NO LONGER EXCLUDED.** Folded into `CONSTANTS.json` as `supporting_level_demo_and_role_decay` on 2026-08-05. It is live via `level_now` and load-bearing on every price, so flagging it here while shipping the rebuilder `CONSTANTS.json` alone left the level input unreproducible. |
| `PRESENT_VAR`, `CVX_CAP`, `_GHx/_GHw`, `_cov_age`, `_cliff_disc` | `RM:1259-1293` | Phase-2 convexity layer; `EX:208` overwrites `_cvx = 1.0` |
| `pedmix` | `RM:538` | no caller |
| establishment-P (`pgrid`, `_PB`, `_PATHK`, `P_estab`) | `RM:1167-1216` | `P_HOOK=None` at `RM:1216` — inert |
| `PRESENT_ID_OVERRIDES` | `RM:1223-1228` | four named players, not a model constant |
| `K_SHRINK`, `_SIG`, `RB_TAPER`, `_AGEMOVE`, `WIDTH_REF`, `RISE_YEARS`, `HP` | `DP:39-253` | the standalone `dist_value` repricer; the board uses `cond_prior_band` + `q97m`, not `DP.build()` |

**[R1] 2026-08-05 — the "flagged, not folded in" carve-out is closed.** `level_demo`'s internals at
`RM:434-480` (prior recency `0.60^(gap)`, games cap 18, thin-season weight 0.25, confidence base
`games/16`, breakout ratio 1.4 over K=3, confidence clamp `[0.20, cap]` with cap 0.83/0.92 and
`SPIKE_CAP['KPD']=0.60`, `ROLE_HC_MAX=0.07` with its 7-game / 0.35 / 0.30 gates) are now **in**
`CONSTANTS.json` as `supporting_level_demo_and_role_decay`, and the `basepk_c` pedigree surface they
sit beside is in `supporting_basepk_pedigree_surface`. Disclosure in this file was not a substitute
for delivery: the rebuilder receives `CONSTANTS.json` alone.

The remaining rows above stay excluded. Two were independently re-verified dead at round 1:
`pedmix` (`RM:538`) has exactly one occurrence in the tree — its own definition — and the `out_tilt`
dial family (`RM:1029-1051`) is referenced only at its definitions, inside `out_tilt`'s own body, and
at `EX:520`, which copies the literals into the exported board JSON as **metadata** without calling
`out_tilt`. Worth recording that those literals are re-published on the board even though they price
nothing. Likewise `survival` (`RM:575-580`) *is* still called at `EX:279`, but the result is
discarded — `EX:286` writes the literal `'surv':1.0` and `RM:1078` sets `surv=1.0` — so `BUST_BAND`
and its multipliers reach no output.
