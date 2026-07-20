"""SCRATCH-FIXTURE support for the weekly-updater proofs — coherent release identities, gate OFF.

The updater's proofs run against disposable SCRATCH repos (never the real single source). Guard 5
validates the STAGED board against the release identities the fixture carries in its
data/expected_boot.json. For that validation to be meaningful, the fixture's boot pins must be
COHERENT with the fixture's own engine — otherwise Guard 5 halts on a pin that describes a different
engine, not on anything the updater did.

WHY THIS EXISTS (the accepted-foundation seam). The accepted df5066a foundation's committed
data/expected_boot.json carries STALE engine identities: engine_head 40f43772 / rl_model a5fd3d7d,
while the checked-out engine hashes 904722cd / cc626d7d. (store / board / fv / register pins are all
coherent.) The updater must NEVER re-stamp engine pins on the real store — a weekly round merges
SCORES; it does not move the engine, and the pre-remediation engine-pin re-stamp is explicitly
excluded from this workstream. So the *fixture* supplies coherent engine identities here, in a
disposable copy, and the real manifest is left byte-untouched. The stale real pins are reported as a
remaining blocker to production acceptance (an owner/bake re-stamp, outside this workstream).

This module ONLY rewrites two pin values in a scratch copy. It touches no real file, computes no
value, and arms no gate.
"""
import hashlib
import json
import os
import re


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def stamp_release_identities(scratch_root):
    """Make a scratch fixture's data/expected_boot.json COHERENT with its own engine: move the
    `engine_head` and `rl_model` pins to the scratch's actual _merged_recover.py / rl_model.py md5s.
    Preserves the file's exact formatting (surgical regex, like the applier's store/board re-stamp) so
    only the two pin values change. Returns {'engine_head':..., 'rl_model':...} — the coherent release
    identities the fixture now supplies. Idempotent; raises if a pin is not present exactly once."""
    ra = os.path.join(scratch_root, 'engine', 'rl_after')
    pins = {
        'engine_head': _md5(os.path.join(ra, '_merged_recover.py')),
        'rl_model': _md5(os.path.join(ra, 'rl_model.py')),
    }
    bootp = os.path.join(scratch_root, 'data', 'expected_boot.json')
    with open(bootp) as f:
        text = f.read()
    for field, val in pins.items():
        pat = r'("%s":\s*")[0-9a-f]+(")' % field
        text, n = re.subn(pat, lambda m, v=val: m.group(1) + v + m.group(2), text, count=1)
        if n != 1:
            raise RuntimeError("expected exactly one %r pin in %s, found %d" % (field, bootp, n))
    with open(bootp, 'w') as f:
        f.write(text)
    return pins


def real_manifest_engine_pins(repo_root):
    """The (pinned, actual) engine identities in the REAL committed manifest — for the blocker report.
    Returns {'engine_head': (pinned, actual, coherent), 'rl_model': (pinned, actual, coherent)}."""
    ra = os.path.join(repo_root, 'engine', 'rl_after')
    boot = json.load(open(os.path.join(repo_root, 'data', 'expected_boot.json')))
    out = {}
    for field, src in (('engine_head', '_merged_recover.py'), ('rl_model', 'rl_model.py')):
        pinned = boot.get(field)
        actual = _md5(os.path.join(ra, src))
        out[field] = (pinned, actual, pinned == actual)
    return out
