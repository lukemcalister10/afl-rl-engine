# Theme 07 — Sunset Circuit

A third isolated UI profile study for the AFL RL Engine, inspired by vaporwave / outrun interfaces.

## Design judgement

This version keeps the atmosphere maximal while deliberately restraining typography on data-bearing surfaces:

- player names use tight, near-natural tracking rather than expanded cyberpunk spacing;
- section titles such as **Movement summary** and **Value trajectory** use compact display tracking;
- wide tracking is reserved for small labels, metadata, status bars and terminal chrome;
- player rows, values and signed movement remain static and easy to scan;
- gradients, neon glows, the sunset disc and perspective grid carry the vaporwave identity.

## Bundle

- `vaporwave_showcase.zip` — contains the self-contained showcase and this README.
- `showcase.html` — board, player profile and round review with internal navigation.

Download the ZIP, extract it, then open `showcase.html`. It requires no server, webfont, package, stylesheet or external script.

## Isolation

Everything is design-only and confined to `docs/ui_styles/theme_07_vaporwave/`. It does not edit or import production `ui/`, generated data, engine code, workflows, release state or canonical scoring artifacts. All names and figures are illustrative fixtures.

## Accessibility and motion

- visible keyboard focus;
- full names and signed movement text;
- motion pause/resume control;
- reduced-motion support;
- no animation on data rows;
- responsive desktop and mobile layouts.
