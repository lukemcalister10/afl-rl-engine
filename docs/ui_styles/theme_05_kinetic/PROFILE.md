# Kinetic Matchday — profile specification

## Intent

Kinetic Matchday combines the existing Matchday UI's dark field, volt accent, hard structure,
full-name rule and signed numerical grammar with a more expressive public presentation layer.
Typography creates the visual hierarchy; motion supplies rhythm around the data rather than
making the data itself appear unstable.

## Visual rules

- Rich black `#09090B`, off-white `#F5F5EF`, acid yellow `#DFE104`.
- Sharp two-pixel structural borders and no shadows.
- Uppercase display typography with extreme scale contrast.
- Monospaced, tabular numerical values.
- Full-width marquees only for summaries and framing.
- Board rows remain static until intentional hover or keyboard focus.
- No decorative gradients. Semantic visual encodings may survive a later production adaptation.
- Hard black/yellow or black/off-white inversions are reserved for intentional interaction.

## Motion rules

- Motion is decorative and non-essential.
- A visible pause/play control is present on every screen.
- `prefers-reduced-motion` removes marquee and transition movement.
- Values, ranks and signed movement remain fully understandable in the static fallback.
- Production board rows, provenance stamps, warnings and working controls should not move continuously.

## Public versus working tiers

This first study covers only the **public** tier. A future working-tier companion should reuse tokens
and typography while reducing continuous motion, increasing density and preserving all provenance,
ring-fence and fail-closed states.

## Production adaptation constraints

Any later production implementation must:

1. remain a read-only view;
2. compute no price or rank;
3. preserve fail-closed board rejection;
4. preserve working/public data boundaries;
5. preserve full player names and comma digit grouping;
6. keep signed figures so colour is never the sole carrier;
7. remain compatible with the repository's dependency-free HTML/CSS/vanilla-JavaScript architecture;
8. preserve direct `file://` operation;
9. introduce no package manager or runtime dependency solely for animation;
10. be implemented on a fresh owner-approved branch from the then-current accepted production SHA.
