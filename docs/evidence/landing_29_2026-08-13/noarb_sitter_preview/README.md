# THE SITTER-LAW PREVIEW — the candidate fade applied to the landed-law no-arb reading

**A PREVIEW, NOT A LANDING.** Run in-session by the supervisor seat (2026-08-14) at the owner's
request ("So I don't get to see the no arb table change under the sitter law change?"), disclosed
here in full. **Nothing is wired**; the board is unmoved; the candidate law awaits the owner's
ruling on `../..//sitter_fade_2026-08-14/SITTER_FADE_PACKET_2.md`; the old `los_decay` schedule
remains the operative fallback.

## Method (the whole transform, `sitter_preview_transform.py` beside this file)

Base matrix: `per_entrant_O29CFINAL.json` (`6db06e40`, the ORDER 29C landed-law basis — the merge
criterion). For every record with `v0 > 0`, every cohort-year cell whose `games_by[N] == 0`
(zero career games as of that year) is replaced by `v0 × D(N+1)`:

- **ND rows**: the packet-2 listed-conditional candidate — D(2)=0.5684 · D(3)=0.3600 · D(≥4)=0.3073
  (the depth-4 bound held flat; the deep-end rule is one of the owner's open words).
- **Pool rows** (the `SITALL` variant only): PROVISIONAL values from the landed pool ψ surface —
  D(2)=0.624 · D(≥3)=0.380 — pending ORDER 30B's own pool derivation under the one-machinery law.
  The `SITND` variant leaves pool rows untouched.

Cells moved: `SITND` 626 rows / 1,042 cells · `SITALL` 1,432 rows / 2,504 cells. Year-0 cells and
every played-player cell are byte-identical to the base. Instruments: the ORDER 29 disclosed copies
under `../noarb/`, byte-unmodified (`noarb_table_338.py` md5 `0f822035…`).

## The readings (margins v 14%; full outputs beside this file)

| reading | landed law (base) | SITND | SITALL |
|---|---:|---:|---:|
| all-arm PRIMARY | −19.10% ARB | −9.41% ARB | −4.39% ARB |
| all-arm MODERN | −12.48% ARB | −1.27% ARB | **+2.13% no arb** |
| ND ALL 1–64 | −16.74% ARB | −4.76% ARB | −4.76% ARB |
| ND 1–20 | −17.12% ARB | −11.28% ARB | −11.28% ARB |
| ND 21–64 | −16.12% ARB | **+5.67% no arb** | **+5.67% no arb** |

The fade flips two readings green and halves the rest. The residual sits with PLAYED players — the
evidence machinery's year-1 re-ratings, strongest at picks 1–20 — which is the remaining scope of
ORDER 30B (the evidence blend + the pool re-referencing), not of the fade ruling.

Matrix md5s: `MATRIX_MD5S.txt`. One committed file (`../noarb/noarb_table_338.json`) was transiently
overwritten by these reruns and restored from git before this commit — noted for the record.
