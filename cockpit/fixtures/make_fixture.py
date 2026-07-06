#!/usr/bin/env python3
"""
make_fixture.py — generate the SYNTHETIC placeholder board for the cockpit viewer.

This is 100% invented dev data. It copies NO rows or values from the real board.
It only mirrors the real board's *schema* (field names/types) so the viewer's
loader exercises the true code path. Every value here is fabricated to hit an
edge case; none of it is a real player, club, price, or path.

Outputs (both carry the "_FIXTURE" marker and DELIBERATELY carry NO valid
`.srcmd5` source-stamp — that absence is what the real-mode ring-fence rejects):

  fixtures/fixture.json        curated edge-case rows (small, human-readable)
  fixtures/fixture_large.json  curated rows + ~810 generated rows (~850 total)
                               to exercise virtualization / large-N performance.

Run:  python3 cockpit/fixtures/make_fixture.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# The invented world: fake positions match the viewer's group keys (so the pos
# chips/colours render), but every club and name below is made up.
POS_KEYS = ["MID", "GEN_DEF", "KEY_DEF", "GEN_FWD", "KEY_FWD", "RUC"]
FAKE_CLUBS = ["Testford", "Placeholder Bay", "Fixture United", "Mock Rovers",
              "Synthetic City", "Sample Saints", "Dummy Dockers", "Stub Swifts"]
FAKE_TYPES = ["ND", "RD", "MSD", "SSP", "PSD"]
FAKE_CATS  = ["Father-Son", "Academy", "Next Gen", None, "None"]
BASE_YEAR  = 2026

MARKER = "synthetic dev data — NOT the board"


def track(n, start=40, step=8, jitter=6, rng=None):
    """A fabricated per-career-season score-relativity path: [{s,a}, ...]."""
    rng = rng or random
    out = []
    for i in range(n):
        a = start + i * step + rng.randint(-jitter, jitter)
        out.append({"s": i + 1, "a": round(a, 1)})
    return out


def rec(key, name, grp, v, *, pk=None, yr=2020, club="Testford", ty="ND",
        cat=None, draft="ND", age=24, g=50, cg=None, bk=False,
        vpath=None, fut=None, gf=None, games=6):
    """One synthetic record in the RAW board schema the loader consumes.

    Mirrors the real board record's field set (key/name/grp/gf/fut/pk/yr/cat/
    ty/club/draft/v/vM2..vP2/g/cg/age/bk/track). All values invented.
    """
    if vpath is None:
        vpath = [v - 400, v - 150, v, v + 220, v + 500]
    r = {
        "key": key, "name": name, "grp": grp,
        "v": v,
        "vM2": vpath[0], "vM1": vpath[1], "vP1": vpath[3], "vP2": vpath[4],
        "pk": pk, "yr": yr, "cat": cat, "ty": ty, "club": club, "draft": draft,
        "age": age, "g": g, "cg": cg if cg is not None else g, "bk": bk,
        "fut": fut if fut is not None else [],
        "track": track(games) if games else [],
    }
    # `gf` is the dormant forward-blend field: present in the schema, unused by
    # the pure-view viewer. Carry it on some rows for schema fidelity.
    if gf is not None:
        r["gf"] = gf
    return r


def curated():
    """Hand-built rows, each targeting a specific edge case."""
    R = []

    # --- long name: must not break the layout (ellipsis/max-width) ---
    R.append(rec("syn-longname-wakefield",
                 "Test Player Longname-Wakefield-Cholmondeley-Featherstonehaugh",
                 "MID", 8200, pk=3, yr=2019, club="Placeholder Bay", ty="ND",
                 cat="Academy", age=25, g=110,
                 fut=[["MID", 0.9], ["GEN_FWD", 0.1]]))

    # --- same-display-name collisions, distinguished ONLY by id/key/cohort ---
    R.append(rec("syn-sam-berry-a", "Sam Berry", "MID", 5400, pk=32, yr=2020,
                 club="Mock Rovers", age=24, g=70))
    R.append(rec("syn-sam-berry-b", "Sam Berry", "GEN_FWD", 3100, pk=58, yr=2022,
                 club="Dummy Dockers", age=21, g=28))
    R.append(rec("syn-pickett-a", "Charlie Pickett", "GEN_FWD", 6600, pk=12,
                 yr=2018, club="Synthetic City", age=26, g=120,
                 fut=[["GEN_FWD", 0.7], ["MID", 0.3]]))
    R.append(rec("syn-pickett-b", "Charlie Pickett", "KEY_DEF", 4200, pk=44,
                 yr=2023, club="Sample Saints", age=20, g=15))
    R.append(rec("syn-king-a", "Max King", "KEY_FWD", 7100, pk=4, yr=2019,
                 club="Testford", age=25, g=95))
    R.append(rec("syn-king-b", "Max King", "KEY_DEF", 6900, pk=6, yr=2019,
                 club="Fixture United", age=25, g=97))

    # --- zero / extreme / negative values ---
    R.append(rec("syn-zero", "Zero Valuen", "GEN_DEF", 0, pk=71, yr=2024,
                 club="Stub Swifts", age=19, g=2,
                 vpath=[0, 0, 0, 0, 0]))
    R.append(rec("syn-extreme-high", "Ceiling Maxwell", "MID", 999999, pk=1,
                 yr=2015, club="Synthetic City", age=29, g=210,
                 vpath=[820000, 910000, 999999, 990000, 960000],
                 fut=[["MID", 1.0]]))
    R.append(rec("syn-negative", "Underwater Sub-Zero", "RUC", -500, pk=None,
                 yr=2025, club="Mock Rovers", age=18, g=0, games=0,
                 vpath=[-200, -350, -500, -420, -300]))

    # --- null / missing optional fields ---
    R.append(rec("syn-nulls", "Missing Fields-Jones", "GEN_FWD", 2500, pk=None,
                 yr=2021, club="Placeholder Bay", ty="SSP", cat=None,
                 draft="None", age=None, g=None, games=0, fut=None))
    # cat explicitly None, pk None (SSP/rookie shows —), age/g None, empty track.

    # --- single-position player (fut has one entry) vs dormant-fut player ---
    R.append(rec("syn-singlepos", "Solo Position-Smith", "KEY_DEF", 4800, pk=22,
                 yr=2020, club="Dummy Dockers", age=24, g=80,
                 fut=[["KEY_DEF", 1.0]]))
    R.append(rec("syn-dormant-fut", "Dormant Gf-Taylor", "GEN_DEF", 3900, pk=40,
                 yr=2021, club="Sample Saints", age=23, g=55,
                 fut=[], gf=[["MID", 0.5], ["GEN_DEF", 0.5]]))
    # ^ empty fut (no reclass chip); gf present but the pure-view viewer ignores it.

    # --- reclass case: current group != dominant projected group ---
    R.append(rec("syn-reclass", "Reclass Mover-Brown", "GEN_DEF", 5200, pk=18,
                 yr=2021, club="Testford", age=22, g=48,
                 fut=[["MID", 0.75], ["GEN_DEF", 0.25]]))

    # --- ties: identical value to test STABLE sort (order must stay deterministic) ---
    for i, nm in enumerate(["Tie Alpha-One", "Tie Bravo-Two", "Tie Charlie-Three",
                            "Tie Delta-Four", "Tie Echo-Five"]):
        R.append(rec(f"syn-tie-{i}", nm, "MID", 5000, pk=50 + i, yr=2022,
                     club="Fixture United", age=23, g=40))

    # --- flat value path (retired/back-row style single as-of estimate) ---
    R.append(rec("syn-back-flat", "Recalled Retiree-Green", "RUC", 3600, pk=8,
                 yr=2008, club="Synthetic City", age=38, g=250, bk=True,
                 vpath=[3600, 3600, 3600, 3600, 3600], games=12))

    # --- vpath with embedded nulls (partial history) ---
    R.append(rec("syn-partial-path", "Partial Path-White", "GEN_FWD", 4400,
                 pk=27, yr=2023, club="Stub Swifts", age=20, g=18,
                 vpath=[None, None, 4400, 4700, 5100]))

    # --- a couple of ordinary rows for a normal-looking board ---
    R.append(rec("syn-ord-1", "Ordinary Player-Adams", "MID", 6100, pk=9,
                 yr=2019, club="Mock Rovers", age=25, g=100,
                 fut=[["MID", 0.8], ["GEN_DEF", 0.2]]))
    R.append(rec("syn-ord-2", "Ordinary Player-Baker", "KEY_FWD", 5700, pk=15,
                 yr=2020, club="Sample Saints", age=24, g=85))

    return R


def generated(n, rng):
    """~n bulk synthetic rows to exercise virtualization at scale."""
    first = ["Alden", "Brix", "Corin", "Dax", "Ellis", "Fenn", "Gale", "Hollis",
             "Iver", "Jory", "Kade", "Lorne", "Mace", "Nolan", "Orin", "Pyke",
             "Quill", "Reeve", "Sten", "Torin", "Ulric", "Vane", "Wynn", "Xen",
             "Yorick", "Zeb"]
    last = ["Ashcombe", "Birchwood", "Coldstream", "Darnley", "Everton",
            "Fairholme", "Grimsby", "Harrowgate", "Iveson", "Jarrow", "Keswick",
            "Lyndhurst", "Marlowe", "Netherby", "Oakhurst", "Pendle", "Quorn",
            "Ravenglass", "Stonehaven", "Thornbury", "Ulverston", "Vexley",
            "Wardlow", "Yardley", "Zennor"]
    out = []
    # a block of exact-tie values to stress stable-sort at scale
    tie_val = 4500
    for i in range(n):
        grp = rng.choice(POS_KEYS)
        # every 37th row is a forced tie; otherwise a spread of values
        if i % 37 == 0:
            v = tie_val
        else:
            v = rng.randint(300, 90000)
        nm = f"{rng.choice(first)} {rng.choice(last)}"
        yr = rng.randint(2006, 2025)
        bk = yr <= 2012 and rng.random() < 0.4
        games = 0 if rng.random() < 0.08 else rng.randint(1, 18)
        fut = []
        if rng.random() < 0.3:
            alt = rng.choice([p for p in POS_KEYS if p != grp])
            fut = [[alt, 0.6], [grp, 0.4]]  # dominant alt -> reclass chip
        elif rng.random() < 0.5:
            fut = [[grp, 1.0]]
        out.append(rec(
            f"syn-gen-{i:04d}", nm, grp, v,
            pk=(None if rng.random() < 0.1 else rng.randint(1, 80)),
            yr=yr, club=rng.choice(FAKE_CLUBS), ty=rng.choice(FAKE_TYPES),
            cat=rng.choice(FAKE_CATS), draft=rng.choice(["ND", "RD", "MSD", "None"]),
            age=(None if rng.random() < 0.05 else rng.randint(18, 34)),
            g=(None if games == 0 else rng.randint(1, 240)),
            bk=bk, fut=fut, games=games,
        ))
    return out


def wrap(active, back):
    """Top-level envelope — mirrors the board's shape, minus any source-stamp.

    NOTE: NO ".srcmd5" key is emitted. In real-mode the viewer's ring-fence
    demands a valid source-stamp and rejects this file; in dev-mode it loads.
    That rejection is the contamination guard working.
    """
    return {
        "_FIXTURE": MARKER,
        "BASE_YEAR": BASE_YEAR,
        "active": active,
        "back": back,
    }


def split_back(rows):
    active = [r for r in rows if not r.get("bk")]
    back = [r for r in rows if r.get("bk")]
    return active, back


def main():
    rng = random.Random(20260706)  # deterministic — reproducible fixture

    cur = curated()
    cur_active, cur_back = split_back(cur)
    small = wrap(cur_active, cur_back)

    big_rows = cur + generated(830, rng)
    big_active, big_back = split_back(big_rows)
    large = wrap(big_active, big_back)

    small_path = os.path.join(HERE, "fixture.json")
    large_path = os.path.join(HERE, "fixture_large.json")
    with open(small_path, "w") as f:
        json.dump(small, f, indent=1)
    with open(large_path, "w") as f:
        json.dump(large, f, separators=(",", ":"))

    def total(d):
        return len(d["active"]) + len(d["back"])

    print(f"wrote {small_path}: {total(small)} rows "
          f"(active {len(small['active'])} + back {len(small['back'])})")
    print(f"wrote {large_path}: {total(large)} rows "
          f"(active {len(large['active'])} + back {len(large['back'])})")
    print(f"  marker    : _FIXTURE = {MARKER!r}")
    print(f"  srcmd5    : ABSENT (by design — real-mode ring-fence rejects it)")


if __name__ == "__main__":
    main()
