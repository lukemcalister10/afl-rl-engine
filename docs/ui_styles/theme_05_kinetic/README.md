# Theme 05 — Kinetic Matchday

Standalone visual study for an alternative public UI graphics profile.

## Scope

This package is deliberately isolated under `docs/ui_styles/theme_05_kinetic/`.
It does **not** edit or import the production `ui/` application, generated board bundles,
engine code, workflows, release state or canonical scoring artifacts.

All displayed names and figures are illustrative design fixtures. Every screen carries an
explicit **invented figures / not the board** banner.

## Screens

- `index.html` — study hub
- `board_public.html` — public player-value board
- `player_card_public.html` — public player profile
- `round_review_public.html` — public round movement report

Open any file directly with `file://`; no server, package manager or third-party dependency is required.

## Technical posture

- static HTML;
- shared CSS token and component layer;
- small dependency-free JavaScript fixture renderer;
- no React, Tailwind, Framer Motion or marquee package;
- CSS-transform marquee motion;
- persistent pause/play control;
- `prefers-reduced-motion` static fallback;
- full names, comma grouping and signed movement;
- colour is never the sole carrier of movement.

## Review questions

1. Is the visual intensity appropriate for the public tier?
2. Does the board remain easy to scan despite the enlarged hierarchy?
3. Should the acid-yellow framing be retained, softened or made club-variable?
4. Is the player profile sufficiently informative without exposing working-tier internals?
5. Should a later pass explore a restrained working-tier companion profile?

No production integration is implied by approval of these screens.
