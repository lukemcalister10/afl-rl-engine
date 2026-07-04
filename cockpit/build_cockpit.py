#!/usr/bin/env python3
"""
build_cockpit.py — bake the self-contained RL Value Cockpit.

Reads the STABLE board app-data file (the same file the existing HTML build
consumes), slims it to the viewer model, and injects it into template.html to
produce a single self-contained cockpit.html.

Why this file exists: the deliverable is a self-contained HTML daily-driver, so
the board data is inlined rather than fetched. To keep "a re-bake auto-updates
the cockpit with no code change", the ONLY thing that ever changes is the data
under DATA_SOURCE below — re-run this one command after a re-bake and the
cockpit refreshes. DATA_SOURCE is the single, clearly-marked seam.

READ-ONLY on the engine + data. Writes only cockpit/cockpit.html.
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ============================================================================
# DATA_SOURCE — the ONE seam. A stable, unversioned filename so an overhaul
# re-bake (rl_export.py rewrites this path in place) auto-updates the cockpit
# with no code change here. Chosen over data/s4_matrix_baked_<md5>.json because
# that filename is version-stamped (breaks on re-bake) and keyed by unstable
# python id(); rl_app_data.json is what the existing HTML output already reads
# and carries a stable per-player `key`. See DATA_CONTRACT.md.
# ============================================================================
DATA_SOURCE = "data/rl_build/rl_app_data.json"

TEMPLATE = os.path.join(HERE, "template.html")
OUT      = os.path.join(HERE, "cockpit.html")


def to_viewer_model(d):
    """Map the stable app-data schema -> compact viewer contract.

    Tolerant by design: if a record already carries the richer baked-matrix
    contract (pos/cpos/cur/Vpath/Ppath/yrs), those are preferred so a future
    re-bake that enriches the stable file wires in with no change here.
    """
    BY = d.get("BASE_YEAR", 2026)
    years = [BY - 2, BY - 1, BY, BY + 1, BY + 2]

    def m(r, src):
        grp  = r.get("pos",  r.get("grp"))      # current position group
        cpos = r.get("cpos", r.get("grp"))
        fut  = [[x[0], x[1]] for x in (r.get("fut") or [])]
        vpath = r.get("Vpath")
        if vpath is None:
            vpath = [r.get("vM2"), r.get("vM1"), r.get("v"),
                     r.get("vP1"), r.get("vP2")]
        if "Ppath" in r:
            ppath = [[i + 1, a] for i, a in enumerate(r["Ppath"])]
        else:
            ppath = [[t["s"], t["a"]] for t in (r.get("track") or [])]
        return {
            "k":   r.get("key"),
            "n":   r.get("name"),
            "pos": grp,
            "cpos": cpos,
            "fut": fut,
            "pk":  r.get("pk",   r.get("pick")),
            "yr":  r.get("yr",   r.get("year")),
            "cat": r.get("cat"),
            "ty":  r.get("ty",   r.get("type")),
            "club": r.get("club"),
            "draft": r.get("draft"),
            "v":   r.get("cur", r.get("v")),
            "vpath": vpath,
            "years": r.get("yrs", years),
            "ppath": ppath,
            "g":   r.get("g"),
            "cg":  r.get("cg"),
            "age": r.get("age"),
            "bk":  bool(r.get("bk")),
            "src": src,
        }

    players = ([m(r, "active") for r in d.get("active", [])] +
               [m(r, "back")   for r in d.get("back", [])])
    return players, BY, years


def main():
    src_path = os.path.join(ROOT, DATA_SOURCE)
    with open(src_path) as f:
        d = json.load(f)

    players, base_year, years = to_viewer_model(d)

    counts = {"active": len(d.get("active", [])), "back": len(d.get("back", []))}
    meta = {
        "baseYear": base_year,
        "years": years,
        "dataSource": DATA_SOURCE,
        "generated": datetime.date.today().isoformat(),
        "counts": counts,
    }

    tpl = open(TEMPLATE).read()
    data_json = json.dumps({"players": players}, separators=(",", ":"))
    meta_json = json.dumps(meta, separators=(",", ":"))

    html = (tpl
            .replace("/*__DATA__*/ null", "/*__DATA__*/ " + data_json)
            .replace("/*__META__*/ {baseYear:2026, dataSource:\"data/rl_build/rl_app_data.json\", generated:\"(dev)\", counts:{}}",
                     "/*__META__*/ " + meta_json))

    # sanity: both seams must have been filled
    assert "/*__DATA__*/ null" not in html, "DATA seam not injected"
    assert "generated:\"(dev)\"" not in html, "META seam not injected"

    # prepend the doctype/html wrapper the template omits (it is a fragment)
    doc = "<!DOCTYPE html><html lang=\"en\">\n" + html + "\n</html>\n"
    with open(OUT, "w") as f:
        f.write(doc)

    print(f"cockpit built: {OUT}")
    print(f"  source      : {DATA_SOURCE}")
    print(f"  players     : {len(players)}  (active {counts['active']} + back {counts['back']})")
    print(f"  base year   : {base_year}")
    print(f"  html bytes  : {len(doc):,}")


if __name__ == "__main__":
    main()
