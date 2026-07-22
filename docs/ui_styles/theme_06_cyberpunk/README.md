# Theme 06 — Cyber Signal

A second isolated UI profile study for the AFL RL Engine, inspired by cyberpunk / glitch interfaces.

## Why this version exists

The Kinetic prototype used shared `styles/` and `scripts/` files. Downloading an individual HTML file without its adjacent assets produces an unstyled document. Theme 06 removes that failure mode: **the showcase is a self-contained HTML file with its CSS and JavaScript embedded**.

The typography is also deliberately wider and calmer than Theme 05:

- `Segoe UI` / `Trebuchet MS` display stack;
- materially increased tracking on headings and labels;
- normal proportional body type rather than monospace everywhere;
- stable rows and figures with glitch effects confined to decorative headlines.

## Bundle

- `cyberpunk_showcase.zip` — contains `showcase.html` and this README.
- `showcase.html` — self-contained board, player profile and round review with internal navigation.

Download `cyberpunk_showcase.zip`, extract it, then open `showcase.html`. No server, webfont, package, stylesheet or script file is required.

## Isolation

This folder is a design-only study. It does not edit or import production `ui/`, generated data, engine code, workflows, release state or canonical scoring artifacts. All names and figures shown are illustrative fixtures and the showcase says so explicitly.

## Accessibility and motion

- visible keyboard focus;
- signed movement text as well as colour;
- full player names;
- a persistent pause/resume signal control;
- `prefers-reduced-motion` disables glitch, cursor and scrolling signal animations;
- data rows remain stable even when decorative elements animate.
