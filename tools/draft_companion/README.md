# Draft companion (2026 draft)

A claude.ai artifact for draft night: https://claude.ai/artifact/4EimaHZxtidm27JGiiUarn (private to the owner).

- `extract_v0_tables.py` loads the engine once and writes `v0_tables.json`: the frozen year-zero pick surface
  (national picks 1-64 by position and draft age 18-30), the national pool value for picks 65+, the positional
  rookie-draft values, the flat pathway values (Unregistered, Ireland, NGA = PDN, Academy = PDA) and the board's
  current free agents. It refuses to write unless every active board player's published v0 is reproduced and the
  draft-age rule matches the engine. Indigenous Rookie uses the national pool value until the owner sets one.
- `build_page.py` injects the tables into `template.html` and writes `draft_night.html`, the published page.
- `prospects/` holds the owner's 2026-11-19 prospect handover (99 players, state flags, badge spec); `affl_delisted.json`
  the owner's AFFL delistings shown as free agents. build_page.py merges both.
- Entries save to the artifact's database (collections `slots`, `fa`; anyone the page is shared with can read, only the
  owner and Editors write) and to the browser. Claude reads them back with ArtifactData; the page also exports a CSV.

Re-cut the tables after any act that moves the store or board: run the two scripts, then republish the page.
- `draft_night_standalone.html` is the same page for people without a Claude account: it saves in the viewer's
  browser (not the artifact's database) and downloads the CSV directly. It starts from `board_snapshot.json`, the
  artifact's entries when the file was built; rebuild it to take a newer snapshot.
