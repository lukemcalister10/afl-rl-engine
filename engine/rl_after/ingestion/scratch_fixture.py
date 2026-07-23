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
import shutil
import subprocess


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


# ================================================================================================
# ITEM 408 item 6 — shared, fail-closed R14 disposable-fixture materialisation.
# ------------------------------------------------------------------------------------------------
# Every Live Scoring proof declares an R14 baseline and applies R15 (or R15..R19) onto a DISPOSABLE
# scratch. After the repository was materialised at R19 ("Materialize verified Round 19 MVP state"), a
# plain copytree of the checkout carries the R15-R19 applied-round LEDGER + histories + finalization +
# movers + .weekly_txn residue, so a proof that tries to apply R15/R16 is CORRECTLY refused by the
# PRODUCTION duplicate-round gate. That is fixture drift, not a dedup defect: the fixture no longer
# reconstructs its declared R14 baseline.
#
# `materialize_r14` restores the EXACT historical R14 dynamic state (git bytes read from the R14
# authority anchor) into the scratch, reproduces R14 ABSENCE for the completed-run artifacts, keeps the
# CURRENT implementation code + CURRENT immutable model inputs (directive: current code, historical
# dynamic state), stamps ONLY the engine-head CODE identity coherent (the fixture runs the current
# engine — the documented accepted seam), re-seals the release contract, and VERIFIES every R14
# authority. It is fail-closed: any wrong path / identity / relationship raises FixtureError and never
# synthesizes or guesses a historical artifact. It never touches the real checkout.
#
# The R14 authority (git bytes are the restoration source; these constants are the verification targets):
R14_ANCHOR = '93bd01af86db00c169714652714a364bd2635764'
R14_STORE_MD5 = '968de0c7a0183ca3914165536f39607a'
R14_BOARD_MD5 = '2ab73a6fed1f06fc8eecc2ce597c2aec'
R14_BALANCED_BOARD_MD5 = '06d8af60b679a12db07c064c60c065f9'
R14_AS_OF_ROUND = 14

# Historical DYNAMIC release/runtime state present at R14 -> restore EXACT anchor bytes.
_R14_RESTORE = (
    'engine/rl_after/rl_model_data.json',            # the R14 player store (968de0c7)
    'data/rl_build/rl_app_data.json',                # the R14 canonical board (2ab73a6f)
    'data/rl_build/rl_app_data.json.srcmd5',         # the R14 board source-stamp sidecar
    'data/expected_boot.json',                       # the R14 boot manifest (as_of_round 14)
    'data/season_state.json',                        # the R14 dynamic season state (as_of_round 14)
    'data/release_contract.json',                    # the R14 sealed release contract
    'engine/rl_after/ingestion/applied_rounds_ledger.json',  # R14 dedup ledger (applied == [])
)
# Completed-run artifacts ABSENT at R14 -> remove from the scratch, PROVEN absent at the anchor.
_R14_ABSENT_FILES = (
    'engine/rl_after/ingestion/value_history.json',
    'engine/rl_after/ingestion/rank_history.json',
    'engine/rl_after/ingestion/pos_rank_history.json',
    'engine/rl_after/ingestion/finalization_state.json',
    'engine/rl_after/ingestion/finalization_journal.jsonl',
    'engine/rl_after/ingestion/sibling_repin_state.json',
)
# Committed R15-R19 runtime residue / movers outputs ABSENT at R14 -> clear from the scratch.
_R14_ABSENT_DIRS = (
    'engine/rl_after/ingestion/movers',
    'engine/rl_after/ingestion/.weekly_txn',
)
# CURRENT source trees the ITEM 408 item-5 sibling-integrated staged transaction needs in the scratch
# root: staged_apply._prepare_workspace copies them into the txn workspace to build the balanced/strict
# sibling from the SAME staged store/config/FV as the canonical board + regenerate the board-view. These
# are CURRENT source (not R14 dynamic state) and are installed centrally here, not per-proof.
_SIBLING_TREES = (
    os.path.join('session_2026-07-20', 'fv_provenance_remediation'),
    'ui',
    os.path.join('session_2026-07-17', 'legd_derivation'),
)


class FixtureError(RuntimeError):
    """A historical-restoration invariant is wrong. Fail closed — never synthesize/approximate/guess."""


def _git(repo_root, *args):
    return subprocess.run(['git', '-C', repo_root, *args], capture_output=True)


def _git_ok(repo_root, *args):
    return _git(repo_root, *args).returncode == 0


def _anchor_present_ancestor(repo_root):
    """The R14 anchor must resolve locally AND be an ancestor of the current checkout — else the scratch
    would restore state from an unrelated commit. Fail closed (a shallow clone needs fetch-depth 0)."""
    if not _git_ok(repo_root, 'cat-file', '-e', R14_ANCHOR + '^{commit}'):
        raise FixtureError(
            "R14 anchor %s does not resolve to a commit in %s — the disposable fixture reads EXACT R14 "
            "git bytes and cannot reconstruct the baseline without it. In CI, check out with full history "
            "(fetch-depth: 0)." % (R14_ANCHOR, repo_root))
    if not _git_ok(repo_root, 'merge-base', '--is-ancestor', R14_ANCHOR, 'HEAD'):
        raise FixtureError(
            "R14 anchor %s is NOT an ancestor of HEAD — refusing to restore historical state from an "
            "unrelated commit." % R14_ANCHOR)


def _exists_at_anchor(repo_root, rel):
    return _git_ok(repo_root, 'cat-file', '-e', '%s:%s' % (R14_ANCHOR, rel))


def _tree_present_at_anchor(repo_root, rel):
    r = _git(repo_root, 'ls-tree', '-r', '--name-only', R14_ANCHOR, '--', rel)
    return r.returncode == 0 and bool(r.stdout.strip())


def _read_anchor_bytes(repo_root, rel):
    r = _git(repo_root, 'show', '%s:%s' % (R14_ANCHOR, rel))
    if r.returncode != 0:
        raise FixtureError("could not read %s at R14 anchor %s: %s"
                           % (rel, R14_ANCHOR, r.stderr.decode('utf-8', 'replace').strip()))
    return r.stdout


def _make_writable(path):
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass


def _contract_seal(contract):
    """Byte-for-byte the same deterministic self-hash release_contract.contract_hash computes (sha256
    over the contract minus contract_sha256/_doc, sorted keys, tight separators)."""
    body = {k: v for k, v in contract.items() if k not in ('contract_sha256', '_doc')}
    payload = json.dumps(body, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode()).hexdigest()


def install_sibling_support_trees(scratch_root, repo_root):
    """Copy the CURRENT source trees the item-5 sibling-integrated staged transaction needs into the
    scratch root (centralised — no per-proof ad hoc copies). Fail-closed: a required tree missing at the
    CURRENT checkout raises rather than producing a scratch that would fail the sibling advance late."""
    for rel in _SIBLING_TREES:
        src = os.path.join(repo_root, rel)
        if not os.path.isdir(src):
            raise FixtureError(
                "sibling support tree %r is missing at the checkout %s — the balanced/strict sibling "
                "advance cannot be built in the scratch." % (rel, repo_root))
        dst = os.path.join(scratch_root, rel)
        if os.path.isdir(dst):
            shutil.rmtree(dst, ignore_errors=True)
        os.makedirs(os.path.dirname(dst) or scratch_root, exist_ok=True)
        shutil.copytree(src, dst)


def _restamp_contract_code_identity(scratch_root, pins):
    """Bind the restored R14 contract's CODE identities (engine_head / rl_model) to the CURRENT engine
    the fixture runs, then re-seal. Every OTHER identity (store/board/balanced/fv/register/band) is left
    exactly as restored from R14. release_contract.verify (5) requires each contract identity to equal
    the expected_boot pin; the engine-head stamp on expected_boot must be mirrored here or verify HALTS."""
    cp = os.path.join(scratch_root, 'data', 'release_contract.json')
    with open(cp) as f:
        c = json.load(f)
    ids = c.get('identities')
    if not isinstance(ids, dict) or 'engine_head' not in ids or 'rl_model' not in ids:
        raise FixtureError("restored R14 release_contract has no identities.engine_head/rl_model to bind")
    ids['engine_head'] = pins['engine_head']
    ids['rl_model'] = pins['rl_model']
    c.pop('contract_sha256', None)
    c['contract_sha256'] = _contract_seal(c)
    _make_writable(cp)
    tmp = cp + '.tmp_r14seal'
    with open(tmp, 'w') as f:
        json.dump(c, f, indent=2)
    os.replace(tmp, cp)


def _verify_r14(scratch_root):
    """Fail-closed verification of every R14 authority the directive requires before the fixture is
    handed to a proof. Any wrong identity/relationship is collected and raised together."""
    R = scratch_root
    ra = os.path.join(R, 'engine', 'rl_after')
    fails = []

    store_p = os.path.join(ra, 'rl_model_data.json')
    board_p = os.path.join(R, 'data', 'rl_build', 'rl_app_data.json')
    store_md5 = _md5(store_p)
    board_md5 = _md5(board_p)
    if store_md5 != R14_STORE_MD5:
        fails.append("store md5 %s != R14 authority %s" % (store_md5, R14_STORE_MD5))
    if board_md5 != R14_BOARD_MD5:
        fails.append("canonical board md5 %s != R14 authority %s" % (board_md5, R14_BOARD_MD5))

    boot = json.load(open(os.path.join(R, 'data', 'expected_boot.json')))
    if boot.get('as_of_round') != R14_AS_OF_ROUND:
        fails.append("expected_boot as_of_round %s != 14" % boot.get('as_of_round'))
    if boot.get('store') != R14_STORE_MD5:
        fails.append("expected_boot store pin %s != R14" % boot.get('store'))
    if boot.get('board') != R14_BOARD_MD5:
        fails.append("expected_boot board pin %s != R14" % boot.get('board'))
    if boot.get('balanced_board_md5') != R14_BALANCED_BOARD_MD5:
        fails.append("expected_boot balanced_board_md5 %s != R14" % boot.get('balanced_board_md5'))

    ss = json.load(open(os.path.join(R, 'data', 'season_state.json')))
    if ss.get('as_of_round') != R14_AS_OF_ROUND:
        fails.append("season_state as_of_round %s != 14" % ss.get('as_of_round'))
    if ss.get('source_store_md5') != R14_STORE_MD5:
        fails.append("season_state source_store_md5 %s != R14 store (binding drift)" % ss.get('source_store_md5'))

    c = json.load(open(os.path.join(R, 'data', 'release_contract.json')))
    if c.get('as_of_round') != R14_AS_OF_ROUND:
        fails.append("release_contract as_of_round %s != 14" % c.get('as_of_round'))
    ids = c.get('identities') or {}
    if ids.get('store') != R14_STORE_MD5:
        fails.append("contract identities.store != R14")
    if ids.get('board') != R14_BOARD_MD5:
        fails.append("contract identities.board != R14")
    if ids.get('balanced_board_md5') != R14_BALANCED_BOARD_MD5:
        fails.append("contract identities.balanced_board_md5 != R14")
    if c.get('contract_sha256') != _contract_seal(c):
        fails.append("release_contract self-seal does not verify after re-stamp")
    # release_contract.verify(5) parity: every contract identity must equal the expected_boot pin.
    for k, v in ids.items():
        if str(boot.get(k)) != str(v):
            fails.append("contract identity %s=%s != expected_boot %s (would fail release_contract.verify)"
                         % (k, str(v)[:12], str(boot.get(k))[:12]))

    # engine-head CODE coherence: the manifest + contract pin the CURRENT engine the fixture runs.
    cur_eng = _md5(os.path.join(ra, '_merged_recover.py'))
    cur_rlm = _md5(os.path.join(ra, 'rl_model.py'))
    if boot.get('engine_head') != cur_eng:
        fails.append("expected_boot engine_head != scratch _merged_recover.py md5 (stamp did not apply)")
    if boot.get('rl_model') != cur_rlm:
        fails.append("expected_boot rl_model != scratch rl_model.py md5")

    # CURRENT immutable model inputs must remain coherent with the restored R14 release authority.
    reg_p = os.path.join(R, 'LTI_REGISTER.md')
    if os.path.exists(reg_p) and boot.get('register') != _md5(reg_p):
        fails.append("expected_boot register pin != scratch LTI_REGISTER.md md5 (immutable input drift)")
    mc_p = os.path.join(R, 'data', 'model_config.json')
    if os.path.exists(mc_p):
        try:
            mvars = json.load(open(mc_p)).get('vars', {})
            man_hash = hashlib.sha256(
                '\n'.join('%s=%s' % (k, mvars[k]) for k in sorted(mvars)).encode()).hexdigest()
            if boot.get('config') != man_hash:
                fails.append("expected_boot config pin != scratch model_config vars hash (config drift)")
        except (ValueError, KeyError) as e:
            fails.append("could not verify config coherence: %s" % e)

    # dedup ledger: NO R15+ applied entries may leak into the R14 scratch (the whole point).
    led = json.load(open(os.path.join(ra, 'ingestion', 'applied_rounds_ledger.json')))
    applied = led.get('applied', [])
    leaked = [x for x in applied if isinstance(x, str) and x.rsplit('|', 1)[-1] in ('15', '16', '17', '18', '19')]
    if leaked:
        fails.append("dedup ledger carries %d R15+ applied entries (R19 leak): e.g. %s"
                     % (len(leaked), leaked[:2]))
    if applied != []:
        fails.append("R14 dedup ledger must be empty (applied == []); found %d entries" % len(applied))

    # completed-run artifacts must be ABSENT (no R15-R19 residue in an R14 scratch).
    for rel in _R14_ABSENT_FILES:
        if os.path.exists(os.path.join(R, rel)):
            fails.append("R19 artifact still present in the R14 scratch: %s" % rel)
    for rel in _R14_ABSENT_DIRS:
        if os.path.isdir(os.path.join(R, rel)):
            fails.append("R19 residue dir still present in the R14 scratch: %s/" % rel)

    if fails:
        raise FixtureError("R14 fixture verification FAILED (%d issue(s)):\n  - %s"
                           % (len(fails), "\n  - ".join(fails)))


def materialize_r14(scratch_root, repo_root):
    """Reconstruct the accepted R14 baseline INSIDE the disposable scratch. `repo_root` is the REAL
    checkout (the source of the anchor git bytes and the current code/inputs already copied into the
    scratch by the proof's make_scratch). Returns the restored code identities. Fail-closed throughout;
    NEVER touches the real checkout."""
    if os.path.abspath(scratch_root) == os.path.abspath(repo_root):
        raise FixtureError("refusing to materialize R14 over the REAL checkout %s" % repo_root)
    _anchor_present_ancestor(repo_root)

    # (1) restore EXACT R14 bytes for the historical dynamic state.
    for rel in _R14_RESTORE:
        if not _exists_at_anchor(repo_root, rel):
            raise FixtureError("expected R14 dynamic path %s is ABSENT at anchor %s — restoration map is "
                               "wrong; refusing to guess." % (rel, R14_ANCHOR))
        data = _read_anchor_bytes(repo_root, rel)
        dst = os.path.join(scratch_root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            _make_writable(dst)
        with open(dst, 'wb') as f:
            f.write(data)

    # (2) reproduce R14 ABSENCE for the completed-run artifacts (PROVEN absent at the anchor first).
    for rel in _R14_ABSENT_FILES:
        if _exists_at_anchor(repo_root, rel):
            raise FixtureError("%s is PRESENT at R14 anchor but the absent-list expects it gone — the "
                               "restoration map is wrong; refusing to guess." % rel)
        p = os.path.join(scratch_root, rel)
        if os.path.exists(p):
            _make_writable(p)
            os.remove(p)
    for rel in _R14_ABSENT_DIRS:
        if _tree_present_at_anchor(repo_root, rel):
            raise FixtureError("%s/ exists at R14 anchor but the absent-list expects it gone." % rel)
        d = os.path.join(scratch_root, rel)
        if os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)

    # (3) engine-head CODE coherence: the fixture runs the CURRENT engine, so the manifest + contract
    #     pin the CURRENT _merged_recover.py / rl_model.py md5 (the documented accepted seam). This is
    #     the ONLY identity moved; every immutable model input (fv/config/register/band/q97m/v0surf/...)
    #     is byte-coherent R14==checkout and is left exactly as restored — no silent immutable re-stamp.
    pins = stamp_release_identities(scratch_root)     # expected_boot engine_head + rl_model
    _restamp_contract_code_identity(scratch_root, pins)

    # (4) VERIFY — fail closed on any wrong R14 identity/relationship.
    _verify_r14(scratch_root)
    return {'anchor': R14_ANCHOR, 'engine_head': pins['engine_head'], 'rl_model': pins['rl_model'],
            'store_md5': R14_STORE_MD5, 'board_md5': R14_BOARD_MD5, 'as_of_round': R14_AS_OF_ROUND}
