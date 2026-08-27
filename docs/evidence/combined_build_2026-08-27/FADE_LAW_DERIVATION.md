# THE FADE-LAW DERIVATION (build block 2) · 2026-08-27
### PREREG L3 + L4. The derivation's headline: THE STEP-UP NEEDS NO NEW FIT — its levels are the
### existing fitted fade table's own values, and the ruling's asymmetry law selects WHEN a row may
### read them. Zero new constants enter here.

## L3a · The survivorship step-up — the law
The register already carried the derivation (v851: dodson's measured twin ladder **143 / 77 / 106**
at one/two/three sat seasons) and it maps EXACTLY onto the wired table: `O31_FADE_D` has
D(3)=0.2748 (two completed sat seasons) and **D(4)=0.3973 (three completed) — HIGHER**. That
inversion is not a defect: it is the measured survivorship selection (a gameless player still
listed after three sat seasons is positively selected — the Gawn/Goldstein pattern's residue), and
the owner's accrual-asymmetry ruling (v852/v854, "hurt accrues through the season, help steps at
the transition; cut players leave the database; survivors are entitled immediately") is precisely
the licence to pay it AT THE TRANSITION rather than let it leak in through the accrual clock.

**THE LAW (zero new constants):** at a season transition, for a row whose just-completed season was
SAT (<2 games — the ruled word) and who survives it, the unplayed clock SNAPS to the next integer
level IF AND ONLY IF the fade table's value at that level is HIGHER (help steps); in the normal
direction (next level lower) the clock accrues through the season exactly as today (hurt accrues).
Formally: at transition, `c_u := ceil(c_u)` when `D(ceil(c_u)) > D(c_u)`; unchanged otherwise.

**Benchmark check (filed arithmetic, PEDIGREE_DECOMP):** dodson (RUCK pick 53, t3, 1 game, κ=0.871,
D_eff 0.3515, π 0.280, board 85): the step D(2.871)→D(4) scales his pedigree leg ×~1.35-1.38 →
board ~85 → ~105-117 raw against the registered "~85→~100" — same object, "~" on both sides; the
EXACT number is the battery's job on the built lever, and P-2 stands as written.

**Composition with the retention surface — measured, no double-pay:** the two mechanisms meet in a
`max()` (the surface floors π; the step raises π's D term). Of the 21 class rows, **16 are already
floored above their stepped level** (the tall no-games cell 0.70 dominates D(4)^κ≈0.44-0.48) — the
step-up's incremental movers are **~5 rows** (the poor-cameo/mobile members, dodson included). The
joint candidate prices this exactly; the near-absorption is expected and is not a defect.

## L3b · The pool depth-3 cell — the owner's cap, by construction
The measured raw pool ladder wants depth-3/depth-2 relief **2.2635** (n=17 — the inversion,
unwired). The owner's word: **cap at 1.0**. Since the wired `O31_POOL_D` is already flat from
depth 2, cap-at-1.0 means THE REDESIGN NEVER WIRES THE INVERSION and the pool ladder stays flat —
**the 17 rows move ≈0 vs live** (prereg P-3, now true by construction, asserted in the battery).

## L4 · The easing — rule declared, constant from a declared procedure
The kept easing (owner word, v874): the O45 net's hard edge at the first ≥6-game season becomes a
ONE-SEASON TAPER — during a row's FIRST banked season (and only then), the net applies at weight
`w`; after it, zero, exactly as today. Sizing: **w is the largest value on the declared grid
{1.0, 0.75, 0.5, 0.25} that passes F4 on EVERY barely-banked row** — F4 (prereg): the eased price
stays strictly below that row's thin-twin surface price, and the v868/v871 inversion censuses count
zero new pairs. The grid-max rule is declared HERE so the constant that emerges in the battery is
the procedure's output, not a knob turned after seeing movers. (The v871 measurement — barely-banked
mediocre retains 0.26 vs thin 0.93 — is the standing reason the grid runs DOWNWARD from 1.0 and may
land at 0.25; if even 0.25 fails F4, the easing lands at 0 and the owner is told his ruling was
sized out by his own constraint, not overridden.)

## Scope notes closing the redesign's remaining names
- **MSD wrinkle**: the fade clock's MSD +1 (first-playable-season equalizer) is already the wired
  convention (v851 verified artemis-vs-grlj equal) — the redesign CARRIES it; the <2-sat word
  applies to MSD seasons identically. No lever.
- **t5+ group**: v849 M4 resolved this to a SCOPE word (ordinary-vs-mature split; the R3 production
  collector already covers the class) — no lever rides; the label stays on the off-season list.
- **Sat-season rename** (depth → sat-seasons, v851 nomenclature) rides with the repairs.

## What block 3 implements
L1 (surface) + the step-up snap (this doc) + the easing taper with grid-max sizing + the S_LL5G
bake — as dial-gated engine code on an isolated root, byte-exact off; then the battery per the
prereg's falsifiers.
