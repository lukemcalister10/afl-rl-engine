# Theme 08 — Editorial Force

A fourth isolated UI profile study for the AFL RL Engine, inspired by bold editorial typography and poster design.

## Design judgement

This version deliberately removes the atmospheric effects used by the Cyber Signal and Sunset Circuit studies. Hierarchy is carried by type scale, asymmetric composition, negative space, thin rules and one vermillion accent.

- hero statements use very tight display tracking;
- player names and section titles use a more moderate compact setting so letterforms do not feel cramped;
- small labels and technical metadata use wider tracking;
- values, ranks and signed movement remain static and easy to scan;
- no shadows, glow, gradients, rounded corners or decorative animation;
- hover and keyboard states use decisive colour inversion and underlines.

## Bundle

- `bold_typography_showcase.zip` — contains this README and the self-contained showcase.
- `showcase.html` — board, player profile and round review with internal navigation.

Download the ZIP, extract it, then open `showcase.html`. It requires no server, webfont, package, stylesheet or external script.

## Isolation

Everything is design-only and confined to `docs/ui_styles/theme_08_bold_typography/`. It does not edit or import production `ui/`, generated data, engine code, workflows, release state or canonical scoring artifacts. All names and figures are illustrative fixtures.

## Accessibility

- visible keyboard focus;
- full player names and signed movement text;
- body text remains at least 16px;
- colour is never the only movement indicator;
- data rows do not animate;
- responsive desktop and mobile layouts.
