# ITEM C — COMPOSITION WIRING PREP (code reading, no measurement)

Non-gated prep while the ITEM A ablation and the Mraz trace run, and while the owner's word on the
ITEM I reading is out. **Nothing here is a decision.** It pins down, from the engine source, what
C-Q1's "the taught year-1 level" can and cannot bind to, so the wiring target is chosen on evidence
rather than on a name — the same discipline the ITEM A ramp is being identified under.

## 1. EVERY CAP ON THE PRICING PATH, AND WHETHER IT TOUCHES A YEAR-1 ND ROW

`ev()` (`_merged_recover.py` 1895-1935) and the floor wrapper (1988-2005), in execution order:

| # | object | site | binds on a YEAR-1 ND row with games? |
|---|---|---|---|
| 1 | delist scrap `0.02 × v0_start` | 1897 | no — `delisted(p)` false |
| 2 | **RUCK ceiling** `_cpv = _ruc_ceiling(p,Y)`, binds iff `_cpv < e ≤ _v0_uncapped` | 1899-1901 | **rucks only** — this is ITEM **E2**'s object |
| 3 | KPF residual compression | 1910-1922 | no — requires `nqual ≥ 4` **and** `age ≥ 24` |
| 4 | sit-out blend `(1-λ)·R·entry_anchor + λ·e` | 1925 → `sitout_ev` 1847 | **only when `ns == 0`** |
| 5 | stalled cap `v0 × frac` | 1929 | no — requires `el ≥ onset` (3, or 4 for KPF/KPD/RUCK); a year-1 row has `el = 1` |
| 6 | mediocre cap `v0 × frac` | 1932 | no — requires `el ≥ onset + 2` |
| 7 | year-zero floor `floor_frac(yis) × entry_anchor` | 1999-2003 | yes, but it is a **one-sided LOWER bound** (0.45 × anchor at year 1) |

**The finding that matters: for a year-1 ND non-ruck row with games, NO upper cap in `ev()` binds
at all.** The only anchor-linked objects on that row are a lower bound (7) and, for a *sitter*,
the sit-out blend (4).

## 2. WHAT THAT MEANS FOR C-Q1

Two things follow, and they are consistent with the directive's own assembly flag 1 ("no engine
object is literally 'the year-1+ ND ceiling'"):

**(a) C's ceiling is a NEW object on the played rows.** There is no existing clamp there to
"release". The design's own algebra — `w = 0` → the old cap exactly — resolves cleanly only on the
**sitters**: their price is `(1-λ)·R·anchor + λ·e` with `R ≤ 1`, i.e. already anchor-bounded, and
the 24 `g = 0` rows of the 58-row year-1 cohort are exactly the `w = 0` rows. So "w=0 → untouched"
is true by construction for the sit-out population, and says nothing about the played population.

**(b) Applied literally to live `ev()`, the ceiling is a large CUT, not a release.** Measured
already in phase 1: Mraz's `entry_anchor` is 487.5 and his `ev(2026)` is 3741. A ceiling of
`anchor × (1 + w(H−1))` at his `w = 0.488`, `H = 1.13` is **510.0** — a **−86%** cut. The directive
ruled this out in advance ("that cannot be the intent"), and the measurement confirms the size.

So C-Q1's "the taught year-1 level" is **not** a clamp on live `ev()` and **not** any existing
engine object. It is the level the landing is measured on — which is precisely the object **ITEM A
changes**. That is a real ordering constraint, not an excuse:

> **C cannot be wired before A, because A defines the surface C's ceiling binds.**

This is why the build order is I → B → A + re-teach → C/D/E/H, and it is why C's wiring is
currently blocked behind the owner's word on the ITEM I reading (which gates A), and behind the
ablation (which gates A's ramp).

## 3. WHAT IS READY NOW, AND NEEDS NO FURTHER DECISION

- **C's weight `w = G·Q·gate`** — reproduced exactly on all six worked rows, phase 1 (`README.md`
  §2.2). Conventions pinned by evidence: `T = clip(draft_age − 18, 1, 6)`; `g`/`sa` are career
  quantities.
- **H's ladder and the admissible window** `H ∈ [1.103, 1.335]`, recommendation **H = 1.13**
  (played-only landing 1.0505, all-rows 1.0296 — both matching the filed figures to 4dp).
  *Re-derivation of the landing is required after A moves the level; the weight itself does not
  move, because `w` reads games, `sa`, `par` and `ev/anchor`, and only the last is A-sensitive.*
- **C-Q3** — settled in phase 1: the drafted z gate ships (23 of 67 top-10 rows protected,
  materially); the `sa` fallback does **not** install and would protect the wrong rows.
- **The double-counting assertion** — holds by construction on the shipped gate: `w` reads `sa`
  exactly once, through `Q`; the z gate reads `ev` and `entry_anchor`, never `sa`. One reader.

## 4. E2 IS READY AND IS INDEPENDENT OF A

ITEM E2 ("the ruck prior cap becomes releasable via C's w") has a **real existing object** —
row 2 above, `_ruc_prior_cap` (1200) / `_ruc_ceiling` (1195), `RUC_PRIOR_CAP = 1.4 × _cap_basis(p)`.
Releasing it via `w` is the one C-family change that does not wait on A:

    RUC_PRIOR_CAP × _cap_basis(p) × _ruc_head_v0(p) × (1 + w × (H − 1))

`w = 0` → byte-identical to today, which is the required inertness on the sit-out ruck population
(Goad/Green class). The directive's own worked case stands: Conway's ruck cap 1307.8 sits above his
ITEM C ceiling at every H, so his ruck cap remains his binding object — i.e. E2 is, as filed,
"cheap, mostly symbolic".

## 5. NOT DECIDED HERE

The choice of the object C's ceiling binds to. It needs A landed first, and it needs the owner's
ITEM I reading word. Recorded so the next step is unambiguous, not resolved by the seat.
