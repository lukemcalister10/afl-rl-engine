#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI — MOVERS TRANSITION MIRROR GENERATOR (#274 item 1, ERA SUCCESSION).

Projects `data/release_lineage.json` into `ui/data/movers_transition.js`. The lineage file is the
record; this file is a MECHANICAL SERIALIZATION of it carrying ZERO authorship (#271 Addendum 20 —
"a faithful projection or nothing"). It exists because the js header has always said "do not
hand-edit; regenerate from release_lineage.json" while no generator existed in the tree to do it
(Addendum 20 established that; re-confirmed at #274 read-back). A route that only a human can walk
is a route that drifts, so the route is now a script.

WHAT MOVED AT #274 (era succession). The mirror used to carry the CURRENT transition alone, which is
why the owner-approved #271/A17 record could not reach the reader: the single-slot bridge carried one
transition end-to-end. The mirror now serializes the current transition PLUS the append-only
`release_transition_register`, so `round_movers.model_changes()` can find each out-of-round move's own
owner-approved record. See engine/rl_after/ingestion/round_movers.model_changes().

SHAPE — additive, deliberately. The mirrored object IS the `release_transition` record, key-for-key
and byte-for-byte, with ONE key appended: `release_transition_register`. Two reasons:
  * The ITEM 408 record is preserved byte-verbatim (A17/A22: it is sealed history, never rewritten).
    Its serialization is a literal PREFIX of this file's payload — asserted by the validators, not
    promised in prose.
  * Every existing consumer keeps working unchanged. `ui/app/movers.js` core reads kind /
    owner_approved / source / destination / applies_to off the top-level object; a new sibling key is
    invisible to all of them.

READ-ONLY over data/release_lineage.json. This tool NEVER writes the lineage file — the archive
already exists (#271 A17) and the #274 pre-fire audit fences it read-only. It writes exactly one
path: ui/data/movers_transition.js.

Run:  python3 ui/tools/generate_movers_transition.py            (write the mirror)
      python3 ui/tools/generate_movers_transition.py --check    (verify committed == generated; no write)

--check is the drift guard: exit 0 = the committed mirror is exactly what the lineage projects,
exit 1 = it has drifted (hand-edited, or the lineage moved without a regeneration).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LINEAGE = os.path.join(REPO, "data", "release_lineage.json")
OUT = os.path.join(REPO, "ui", "data", "movers_transition.js")

VAR = "window.__MATCHDAY_TRANSITION__"
REGISTER_KEY = "release_transition_register"

HEADER = """\
// GENERATED — owner-approved Movers provenance transition (ITEM 408 Items 6-7, Option A).
// Mirrors data/release_lineage.json `release_transition` + `release_transition_register`
// (#271 Addendum 20: a mechanical projection with ZERO authorship — every content byte is the
// lineage record. The register is READ, not enforced: movers.js:203-206 makes it the register of
// out-of-round moments, and a label never blocks a comparison). Exposes window.__MATCHDAY_TRANSITION__
// so the browser can display the R15-R19 historical reports under the current accepted release.
// Fail-closed bridge (see ui/app/movers.js core).
// ERA SUCCESSION (#274 item 1): the register is serialized ALONGSIDE the current transition, so every
// out-of-round board move — not just the first — can reach the reader with its own owner approval.
// The `release_transition` body below is the ITEM 408 record, byte-verbatim; the register is appended
// as one sibling key. Do not hand-edit; regenerate with ui/tools/generate_movers_transition.py.
"""


def _dump(obj):
    """The mirror's serialization, fixed by the committed file it must reproduce: compact separators,
    non-ASCII kept literal, insertion order preserved (never sorted)."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def build(lineage):
    """The projection. Returns the full file text."""
    trans = lineage.get("release_transition")
    if not isinstance(trans, dict):
        raise SystemExit("■ HALT — data/release_lineage.json declares no `release_transition` object")
    register = lineage.get(REGISTER_KEY)
    if not isinstance(register, list):
        raise SystemExit("■ HALT — data/release_lineage.json declares no `%s` list" % REGISTER_KEY)
    if REGISTER_KEY in trans:
        raise SystemExit("■ HALT — `release_transition` already carries a `%s` key; the projection "
                         "would be ambiguous" % REGISTER_KEY)

    body = _dump(trans)
    # Append the register as one sibling key WITHOUT re-serializing the transition, so the ITEM 408
    # record's bytes are carried through untouched rather than reproduced. `body` ends with '}'.
    assert body.endswith("}"), "transition serialization is not an object"
    payload = body[:-1] + "," + _dump(REGISTER_KEY) + ":" + _dump(register) + "}"

    # Non-negotiable, checked here rather than trusted: the transition's own serialization is a
    # literal prefix of the payload. If this ever fails, the ITEM 408 record has been rewritten.
    assert payload.startswith(body[:-1]), "the ITEM 408 record is not preserved byte-verbatim"

    return HEADER + VAR + " = " + payload + ";\n"


def main(argv):
    check = "--check" in argv[1:]
    unknown = [a for a in argv[1:] if a != "--check"]
    if unknown:
        raise SystemExit("usage: generate_movers_transition.py [--check]")

    with open(LINEAGE, encoding="utf-8") as f:
        lineage = json.load(f)
    text = build(lineage)

    if check:
        if not os.path.exists(OUT):
            print("■ DRIFT — %s does not exist" % os.path.relpath(OUT, REPO))
            return 1
        with open(OUT, encoding="utf-8") as f:
            have = f.read()
        if have != text:
            print("■ DRIFT — %s is not what data/release_lineage.json projects.\n"
                  "  committed %d bytes / projected %d bytes — regenerate with "
                  "python3 ui/tools/generate_movers_transition.py"
                  % (os.path.relpath(OUT, REPO), len(have.encode()), len(text.encode())))
            return 1
        print("mirror OK — committed == projected (%d bytes, %d register entries)"
              % (len(have.encode()), len(lineage.get(REGISTER_KEY) or [])))
        return 0

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote: %s (%d bytes)" % (os.path.relpath(OUT, REPO), len(text.encode())))
    print("register entries mirrored: %d" % len(lineage.get(REGISTER_KEY) or []))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
