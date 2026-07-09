# PLAN — UI design pass (FABLE seat) · 2026-07-09
### Job-scoped, per DIRECTIVE_ui_design_pass_fable_v1_1. Auto mode ⇒ this PLAN is the first committed
### artifact. Base read on entry: `main` @ `d4e8f6dc580eccc9bbb3413d324d64ce26bf6b1b`. Branch:
### `claude/new-session-7r7x1k`. Time band confirmed: 1–2 h.

## Inputs read
- DECISIONS v86 · CONSTRAINTS v1.6 + acceptance v1.6 (couriered) · ROADMAP v6 Phase 3 (main).
- Skeleton branches, read-only, tips verified against the directive:
  · `claude/html-cockpit-viewer-xsbfoc` @ 14883c6a (cockpit/: README · DATA_CONTRACT · build · template)
  · `claude/cockpit-core-viewer-9grm1v` @ 79cd21ee (same + fixtures/, DATA_SEAM ring-fence, virtualiser)
- Engine read-only spot-checks for the provenance marker: `rl_model.py` `brodie_sig` ×0.50 cut.

## Deliverables (all under docs/ui_direction/)
1. `DESIGN_DIRECTION.md` — the deliverable: skeleton review (keep/kill with obituaries), aesthetic +
   layout direction, colour semantics (value up/down, provenance/override markers incl. the Brodie
   ×0.50 visual language), attribution display doctrine, information hierarchy for the owner's three
   workflows (board-vs-reads · trade eval in one currency · round-to-round review), view map
   (board / book / player card / trade / round review), implementation-chapter handoff, open design
   questions as symmetric options.
2. `mockups/01_board.html` — board with change column, provenance markers, owner-read pins.
3. `mockups/02_player_card.html` — player card with per-lever attribution waterfall (G-ATTR made visible).
4. `mockups/03_trade.html` — trade evaluation: players + picks in one SCAR currency.
5. `mockups/04_round_review.html` — round-to-round change review (post-weekly-loop shape, designed now).

## Fence respected
Read-only on engine/data; no edits to the two viewer branches (KEEP-listed, review only); no wiring;
no bake/tag/main actions. Mockups are static HTML committed as illustrations only.

## Sequence
PLAN (this commit) → direction doc → mockups → return report ≤30 lines + PR.
