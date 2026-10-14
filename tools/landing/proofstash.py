"""tools/landing/proofstash.py — THE PROOF STASH (shrink review S13, owner word 2026-08-28).

RETIRED 2026-10-14: THE SIBLING SLICE (shrink S8, `sibling_key` + the `sibling` stash kind). The
balanced sibling is no longer built by any landing (owner word, 2026-10-14), so there is nothing to
cache for it. Entries written under `sibling_<key>` in an existing stash directory are inert.

THE LANDING INSTALLS PROVEN ARTIFACTS RATHER THAN RE-PROVING THEM. The combined-build landing
re-proved the same board identity FOUR times (77 minutes) and re-ran the identical 43-leg
selftest ~10 times (~1.7 hours) across its takes, because every abort correctly restored the
tree and every relaunch then started from zero (the cost ledger, register v880's review). The
stash keeps a successful proof OUTSIDE the repo, keyed on every INPUT identity, so a relaunch
whose inputs are byte-identical installs the stashed artifacts and VERIFIES them instead of
rebuilding. The assurance model is unchanged in kind: a cache hit still hashes the artifact
against the prereg prediction, the abort ladder still restores, and the gates still run — what
is skipped is only the re-derivation of a result whose inputs have not moved.

DISCIPLINE:
  * The stash lives under /home/user (LANDING_PROOF_STASH overrides) — it survives the platform
    reclaims that killed two takes; /tmp does not.
  * NEVER consulted in a selftest or fault-injected run: those runs exist to exercise the real
    machinery, and a cached proof would hollow out the 43 legs (ctx.opts.selftest / ctx.fault
    guard at the call sites).
  * The key covers every measurable identity the build READS (everything in PIN_MEASURERS that
    the act does not declare as moving) plus the spec's prereg block and the act name — any
    input moving misses the cache and the full proof runs. Since Phase 0.5 (2026-10-13) it also
    covers the build inputs PIN_MEASURERS never did: data/season_state.json, the pinned sitter
    sheet and the three surface pickles (`BUILD_INPUT_FILES`, `_build_inputs`).
  * Entries are content-addressed and verified on load (each stashed file's md5 is recorded and
    re-hashed); a corrupt entry is discarded, never trusted.
"""
import hashlib
import json
import os
import shutil

DEFAULT_DIR = '/home/user/.landing_proof_stash'


def stash_dir():
    d = os.environ.get('LANDING_PROOF_STASH') or DEFAULT_DIR
    os.makedirs(d, exist_ok=True)
    return d


def _md5_bytes(b):
    return hashlib.md5(b).hexdigest()


#: THE KEY SCHEMA. Bumped whenever what the key covers changes, so every stash written under the
#: old coverage misses rather than confirms. 2 = Phase 0.5 (2026-10-13), `_build_inputs` added.
KEY_SCHEMA = 2

#: Inputs the build READS that PIN_MEASURERS does not cover, each md5'd into both keys (Phase 0.5,
#: 2026-10-13). Before this the sitter sheet and season_state.json were outside the key, so a cached
#: board could "confirm" a prediction made against a sheet or a season state that had since moved.
#: The sheet is whichever file data/sheet_pins.json names; the three pickles are the surfaces the
#: build loads (v0surf is also a PIN_MEASURERS entry — it is repeated here so it is in the key even
#: when the act declares it as moving).
BUILD_INPUT_FILES = ('data/season_state.json', 'data/q97m.pkl', 'data/cm_400.pkl', 'data/v0surf.pkl')
SHEET_PINS = 'data/sheet_pins.json'


def _md5_file(path):
    try:
        with open(path, 'rb') as f:
            return _md5_bytes(f.read())
    except OSError:
        return '<absent>'


def _build_inputs(ctx):
    """{rel: md5} for every file in BUILD_INPUT_FILES plus the pinned sitter sheet, read from
    ctx.root. An absent file hashes as '<absent>', which is still an identity — a build that read
    nothing where a sheet should be is not the build that read the sheet."""
    out = {}
    for rel in BUILD_INPUT_FILES:
        out[rel] = _md5_file(os.path.join(ctx.root, rel))
    sheet = None
    try:
        with open(os.path.join(ctx.root, SHEET_PINS), encoding='utf-8') as f:
            sheet = (json.load(f) or {}).get('sheet_path')
    except (OSError, ValueError):
        pass
    if sheet:
        out['sheet:' + sheet] = _md5_file(os.path.join(ctx.root, sheet))
    else:
        out['sheet:<unpinned>'] = '<absent>'
    return out


def build_key(ctx):
    """The input-identity key for a build proof: every PIN_MEASURERS identity the act declares
    UNMOVED (the build's inputs), the prereg block verbatim, and the act name."""
    from tools.landing import steps as ST
    moves = set((ctx.spec.get('identities') or {}).get('moves') or ())
    inputs = {}
    for k, fn in ST.PIN_MEASURERS.items():
        if k in moves:
            continue
        try:
            inputs[k] = str(fn(ctx))
        except Exception:
            inputs[k] = '<unmeasurable>'
    basis = {'inputs': inputs, 'build_inputs': _build_inputs(ctx), 'prereg': ctx.spec.get('prereg'),
             'act': ctx.spec.get('act'), 'act_kind': ctx.spec.get('act_kind'),
             'day0_rebase': ctx.spec.get('day0_rebase'), 'key_schema': KEY_SCHEMA}
    return hashlib.sha256(json.dumps(basis, sort_keys=True).encode()).hexdigest()[:24]


def save(kind, key, files, facts):
    """files: {name: absolute_source_path}. Copies each into the entry and records its md5."""
    ent = os.path.join(stash_dir(), '%s_%s' % (kind, key))
    tmp = ent + '.tmp'
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    manifest = {'facts': facts, 'files': {}}
    for name, src in files.items():
        with open(src, 'rb') as f:
            b = f.read()
        with open(os.path.join(tmp, name), 'wb') as f:
            f.write(b)
        manifest['files'][name] = _md5_bytes(b)
    with open(os.path.join(tmp, 'MANIFEST.json'), 'w') as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    if os.path.isdir(ent):
        shutil.rmtree(ent)
    os.replace(tmp, ent)
    return ent


def load(kind, key):
    """-> (files {name: path}, facts) with every file re-hashed against the manifest, or None."""
    ent = os.path.join(stash_dir(), '%s_%s' % (kind, key))
    mp = os.path.join(ent, 'MANIFEST.json')
    if not os.path.isfile(mp):
        return None
    try:
        manifest = json.load(open(mp))
        out = {}
        for name, want in manifest['files'].items():
            p = os.path.join(ent, name)
            with open(p, 'rb') as f:
                if _md5_bytes(f.read()) != want:
                    return None                       # corrupt entry: discarded, never trusted
            out[name] = p
        return out, manifest['facts']
    except Exception:
        return None


# ---- the selftest pass marker (the S7 half of S13) -------------------------------------------
def lander_fingerprint(lander_dir, spec_path, base):
    """md5 over every tools/landing/*.py byte + the spec bytes + the coherent base — the selftest
    proves THE LANDER against a spec on a base; unchanged all three, the proof stands."""
    h = hashlib.md5()
    for name in sorted(os.listdir(lander_dir)):
        if name.endswith('.py'):
            with open(os.path.join(lander_dir, name), 'rb') as f:
                h.update(name.encode() + b'\0' + f.read() + b'\0')
    with open(spec_path, 'rb') as f:
        h.update(f.read())
    h.update((base or 'HEAD').encode())
    return h.hexdigest()


def selftest_marker(fp):
    return os.path.join(stash_dir(), 'selftest_pass_%s' % fp)


def selftest_passed(fp):
    return os.path.isfile(selftest_marker(fp))


def record_selftest_pass(fp, detail):
    with open(selftest_marker(fp), 'w') as f:
        json.dump(detail, f)
