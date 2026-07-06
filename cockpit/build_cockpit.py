#!/usr/bin/env python3
"""
build_cockpit.py — bake the self-contained RL Value Cockpit.

Injects ONE seam object (DATA_SEAM) into template.html and writes a single
self-contained cockpit HTML. The seam's `mode` is the only place the data
source is chosen:

  dev  (default)  -> the SYNTHETIC fixture (cockpit/fixtures/fixture.json).
                     No source-stamp required; loads and renders.
  real            -> the real board (data/rl_build/rl_app_data.json). The viewer
                     REQUIRES a valid `.srcmd5` source-stamp and REJECTS a source
                     without one. The published board currently ships unstamped,
                     so real-mode has nothing valid to load yet (expected — the
                     companion published-stamp job makes real data pass).

READ-ONLY on the engine + data. Writes only the chosen cockpit HTML output.
This job (fixture-only) defaults to dev so the shipped cockpit.html is a working
demo carrying NO real data.

Usage:
  python3 cockpit/build_cockpit.py                 # dev, fixture.json  -> cockpit.html
  python3 cockpit/build_cockpit.py --large         # dev, fixture_large.json (perf)
  python3 cockpit/build_cockpit.py --mode real     # real, board (rejects until stamped)
  python3 cockpit/build_cockpit.py --source PATH --out FILE --mode {dev,real}
"""
import argparse, json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ============================================================================
# THE DATA SEAM — the ONE seam. In real-mode this points at a stable,
# unversioned board filename so an overhaul re-bake (rl_export.py rewrites this
# path in place) auto-updates the cockpit with no code change. In dev-mode it
# points at the synthetic fixture. See DATA_CONTRACT.md.
# ============================================================================
REAL_SOURCE = "data/rl_build/rl_app_data.json"          # real board (real-mode)
FIXTURE      = "fixtures/fixture.json"                    # synthetic (dev-mode)
FIXTURE_LARGE = "fixtures/fixture_large.json"            # synthetic large-N

TEMPLATE = os.path.join(HERE, "template.html")

# The exact seam placeholder default in template.html (must match verbatim so the
# injection replaces it). Keep in sync with template.html's DATA_SEAM literal.
SEAM_DEFAULT = ('/*__SEAM__*/ {\n'
                '  mode: "dev",\n'
                '  data: null,\n'
                '  url:  "fixtures/fixture.json",\n'
                '  meta: {baseYear:2026, source:"fixtures/fixture.json", generated:"(dev)", counts:{}}\n'
                '}')


def main():
    ap = argparse.ArgumentParser(description="Bake the self-contained RL Value Cockpit.")
    ap.add_argument("--mode", choices=["dev", "real"], default="dev",
                    help="dev = synthetic fixture (default); real = the real board (needs a valid .srcmd5).")
    ap.add_argument("--large", action="store_true",
                    help="dev-mode: use the ~850-row large-N fixture (performance).")
    ap.add_argument("--source", default=None,
                    help="Override the source path (relative to repo root).")
    ap.add_argument("--out", default=None,
                    help="Override the output HTML path (default cockpit.html).")
    args = ap.parse_args()

    if args.mode == "real":
        # real board lives under repo root; the app would fetch it via ../<path>
        source = args.source or REAL_SOURCE
        src_path = os.path.join(ROOT, source)
        url = "../" + source
        source_label = source
    else:
        # fixtures live under cockpit/, so paths are relative to this dir
        source = args.source or (FIXTURE_LARGE if args.large else FIXTURE)
        src_path = os.path.join(HERE, source)
        url = source
        source_label = "cockpit/" + source

    out = args.out or os.path.join(HERE, "cockpit.html")

    with open(src_path) as f:
        raw = json.load(f)

    base_year = raw.get("BASE_YEAR", 2026)
    counts = {"active": len(raw.get("active", [])), "back": len(raw.get("back", []))}

    meta = {
        "baseYear": base_year,
        "source": source_label,
        "generated": datetime.date.today().isoformat(),
        "counts": counts,
        "mode": args.mode,
    }

    # The whole raw payload is inlined as `data` so the file is self-contained
    # (opens with no server). The viewer's stamp-check + normaliser run on it at
    # boot — one code path for both dev and real.
    seam = {
        "mode": args.mode,
        "data": raw,
        "url": url,
        "meta": meta,
    }

    tpl = open(TEMPLATE).read()
    assert SEAM_DEFAULT in tpl, "SEAM placeholder not found in template.html (drifted from build_cockpit.py)"

    seam_json = "/*__SEAM__*/ " + json.dumps(seam, separators=(",", ":"))
    html = tpl.replace(SEAM_DEFAULT, seam_json, 1)

    # sanity: the seam must have been filled exactly once, no default left behind
    assert '/*__SEAM__*/ {\n  mode: "dev"' not in html, "SEAM default still present"
    assert html.count("/*__SEAM__*/") == 1, "seam marker count wrong after inject"

    doc = '<!DOCTYPE html><html lang="en">\n' + html + "\n</html>\n"
    with open(out, "w") as f:
        f.write(doc)

    print(f"cockpit built: {out}")
    print(f"  mode        : {args.mode}")
    print(f"  source      : {source_label}")
    print(f"  players     : {counts['active'] + counts['back']}  (active {counts['active']} + back {counts['back']})")
    print(f"  base year   : {base_year}")
    print(f"  fixture      : {'yes (synthetic)' if args.mode == 'dev' else 'NO (real board)'}")
    print(f"  html bytes  : {len(doc):,}")


if __name__ == "__main__":
    main()
