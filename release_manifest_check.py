#!/usr/bin/env python3
"""release_manifest_check.py — THE WIDENED COHERENCE GATE (M1a / AUDIT_CI.md gap G1).

    python3 release_manifest_check.py [check|table] [--root DIR] [--json PATH]

--------------------------------------------------------------------------------------------------
WHAT THIS IS, AND WHY IT IS SEPARATE FROM THE OWNERSHIP TOOL

`ui/tools/ownership_store_apply.py` grew a six-way coherence gate (P3 / `verify`) that reads the
STORE identity out of six carriers and halts if they disagree. The audit's finding (AUDIT_CI.md §3,
coverage map row "coherence"):

    "PARTIAL — passes, but covers the **store** identity only."

    "G1 — the release manifest is one-seventh built. Six-way coherence covers `store`. There is no
     equivalent for `board`, `engine_head`, `rl_model`, `fv`, `config`, `register`, `as_of_round`.
     Proof it matters: `release_contract.identities.store` passes the six-way check while
     `identities.engine_head`/`rl_model`/`fv` in the *same file* are stale."

That is the whole case. The six-way check reads one field of `release_contract.json` and certifies
it, standing beside three fields of the same object that are wrong, in the same dict, one line
apart. The shape was right and the carrier set was one-eighth of the tree. This file is that shape,
widened to the full identity set, lifted out of a tool whose real job is applying club moves.

--------------------------------------------------------------------------------------------------
THE LAW THIS FILE IS WRITTEN TO (AUDIT_CI.md §5/EXTEND, the fv-provenance rule):

    "Assert the *relationship*, never this month's number."

There is NOT ONE identity hex literal in this file, and there must never be. Every identity is
COMPUTED from the artifact that defines it — the store file is md5'd, the fv tree hash is
recomputed through `fv_provenance.fv_identity`, the config hash through `config_manifest.
manifest_hash` — and every carrier is then asserted to agree with what was computed. A board move,
a bake, a dial flip, a store write: none of them can red this check. Only DISAGREEMENT can.

That is the difference between this and the four instruments the estate retired for being
hand-typed: the panel 10/10, the movers "exactly two known-reds", the R14 fixture's config pin, and
`BOARD_MD5_GOOD`. Each was true the day it was written and became a false red the day the tree
legitimately moved. This check has no day on which it was written.

--------------------------------------------------------------------------------------------------
THE IDENTITY SET  (8)                        THE CARRIERS  (7 files, 40 fields)

    store         engine/rl_after/rl_model_data.json      data/expected_boot.json
    board         data/rl_build/rl_app_data.json          data/release_contract.json
    engine_head   engine/rl_after/_merged_recover.py      data/season_state.json
    rl_model      engine/rl_after/rl_model.py             data/rl_build/rl_app_data.json.srcmd5
    fv            engine/forward_valuation/*.py           ui/data/board_view_working.js  (stamp)
    config        data/model_config.json                  ui/data/board_view_working.js  (stamp.release)
    register      LTI_REGISTER.md                         data/book_stable_seal.json
    as_of_round   (declared — see below)

TRUTH, per identity, is COMPUTED from the left column. The one exception is `as_of_round`, which
names a fact about the world (which round the league has played) and has no artifact to hash. Its
authority is `data/expected_boot.json` — the same file Guard 5 anchors every other identity on — and
the table marks it `anchor` rather than `computed` so a reader is never misled about which rows are
derived and which are declared.

TRUNCATION. Carriers legitimately store short forms: the UI stamp carries `engine` as 8 hex, the
book seal carries `head_md5` as 8, the UI stamp carries `config` as 12. Each carrier therefore
DECLARES its width, and is asserted against `truth[:width]`. A carrier whose stored value is not
exactly its declared width is itself a failure ("width changed") — that catches a carrier silently
truncating further, which would otherwise weaken the assertion without ever reddening it.

--------------------------------------------------------------------------------------------------
REPORTING — the blocked-once law (register v787)

This check is the FIRST check in `acceptance/runner.py` and the estate's furthest-upstream one:
nearly everything downstream reads one of these carriers. When a carrier disagrees, this file
reports it ONCE, names the carrier, and returns the carrier name so the runner can mark every
downstream check BLOCKED instead of letting each produce its own restatement of the same fact. The
audit measured ~40 reds of which R1 alone produced about 30. That is the number this file exists to
turn back into 1.
"""

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

IDENTITIES = ('store', 'board', 'engine_head', 'rl_model', 'fv', 'config', 'register', 'as_of_round')

# The carrier FILES. The keys are the carrier-group names the runner blocks on.
BOOT_REL = 'data/expected_boot.json'
CONTRACT_REL = 'data/release_contract.json'
SEASON_REL = 'data/season_state.json'
SIDECAR_REL = 'data/rl_build/rl_app_data.json.srcmd5'
BVW_REL = 'ui/data/board_view_working.js'
BOOK_REL = 'data/book_stable_seal.json'

# The artifacts TRUTH is computed from.
STORE_SRC = 'engine/rl_after/rl_model_data.json'
BOARD_SRC = 'data/rl_build/rl_app_data.json'
HEAD_SRC = 'engine/rl_after/_merged_recover.py'
RLMODEL_SRC = 'engine/rl_after/rl_model.py'
REGISTER_SRC = 'LTI_REGISTER.md'

MD5 = 32
SHA = 64


class Halt(RuntimeError):
    """The carriers disagree. Fail closed; never reconcile, never guess, never re-stamp."""


def _md5_file(path):
    with open(path, 'rb') as fh:
        return hashlib.md5(fh.read()).hexdigest()


def _json(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def _bundle_obj(path):
    """The UI bundles are `window.X = {...};` — read the object out, exactly as the UI tools do."""
    with open(path, encoding='utf-8') as fh:
        t = fh.read()
    return json.loads(t[t.index('{'):t.rindex('}') + 1])


# ------------------------------------------------------------------------------------------ TRUTH
def compute_truth(root):
    """Compute each identity from the artifact that DEFINES it. No pins are read here.

    Returns {identity: (value, how)} where `how` is 'computed' or 'anchor'.
    """
    p = lambda rel: os.path.join(root, rel)
    truth = {}

    truth['store'] = (_md5_file(p(STORE_SRC)), 'computed md5 %s' % STORE_SRC)
    truth['board'] = (_md5_file(p(BOARD_SRC)), 'computed md5 %s' % BOARD_SRC)
    truth['engine_head'] = (_md5_file(p(HEAD_SRC)), 'computed md5 %s' % HEAD_SRC)
    truth['rl_model'] = (_md5_file(p(RLMODEL_SRC)), 'computed md5 %s' % RLMODEL_SRC)
    truth['register'] = (_md5_file(p(REGISTER_SRC)), 'computed md5 %s' % REGISTER_SRC)

    # fv: the canonical tree hash over engine/forward_valuation/*.py, through the ONE resolver the
    # engine and Guard 5 both use. Never re-implemented here — a second implementation is exactly
    # the hand-mirror hazard the audit flags as G4.
    sys.path.insert(0, root)
    try:
        import fv_provenance                                                   # noqa: PLC0415
        fv_dir = fv_provenance.checkout_fv_dir(root)
        truth['fv'] = (fv_provenance.fv_identity(fv_dir), 'computed fv tree hash (fv_provenance)')

        import config_manifest                                                 # noqa: PLC0415
        truth['config'] = (config_manifest.manifest_hash(root),
                           'computed manifest hash (config_manifest)')
    finally:
        if sys.path and sys.path[0] == root:
            sys.path.pop(0)

    # as_of_round has no artifact to hash — it is a fact about the league, and expected_boot.json is
    # its declared authority (the same file Guard 5 anchors on). Marked `anchor`, never `computed`.
    truth['as_of_round'] = (str(_json(p(BOOT_REL)).get('as_of_round')), 'anchor %s' % BOOT_REL)
    return truth


# --------------------------------------------------------------------------------------- CARRIERS
def read_carriers(root):
    """Enumerate every carrier field, per identity.

    Returns {identity: [(carrier_group, label, value, width), ...]}.
    """
    p = lambda rel: os.path.join(root, rel)
    boot = _json(p(BOOT_REL))
    rc = _json(p(CONTRACT_REL))
    rcid = rc.get('identities') or {}
    season = _json(p(SEASON_REL))
    sidecar = _json(p(SIDECAR_REL))
    bvw = _bundle_obj(p(BVW_REL))
    stamp = bvw.get('stamp') or {}
    rel = stamp.get('release') or {}
    book = _json(p(BOOK_REL))

    def s(v):
        return '' if v is None else str(v)

    G_BOOT, G_RC = 'expected_boot', 'release_contract'
    G_SEASON, G_SIDE = 'season_state', 'board_sidecar'
    G_STAMP, G_REL = 'ui_bundle.stamp', 'ui_bundle.stamp.release'
    G_BOOK = 'book_seal'

    return {
        'store': [
            (G_BOOT, 'expected_boot.store', s(boot.get('store')), MD5),
            (G_RC, 'release_contract.identities.store', s(rcid.get('store')), MD5),
            (G_SEASON, 'season_state.source_store_md5', s(season.get('source_store_md5')), MD5),
            (G_SIDE, 'rl_app_data.srcmd5.source_md5', s(sidecar.get('source_md5')), MD5),
            (G_STAMP, 'board_view_working.stamp.store_md5', s(stamp.get('store_md5')), MD5),
            (G_STAMP, 'board_view_working.stamp.store', s(stamp.get('store')), 8),
            (G_REL, 'board_view_working.stamp.release.store', s(rel.get('store')), MD5),
            (G_BOOK, 'book_stable_seal.store_md5', s(book.get('store_md5')), 8),
        ],
        'board': [
            (G_BOOT, 'expected_boot.board', s(boot.get('board')), MD5),
            (G_RC, 'release_contract.identities.board', s(rcid.get('board')), MD5),
            (G_SIDE, 'rl_app_data.srcmd5.own_md5', s(sidecar.get('own_md5')), MD5),
            (G_STAMP, 'board_view_working.stamp.board_md5', s(stamp.get('board_md5')), MD5),
            (G_STAMP, 'board_view_working.stamp.board', s(stamp.get('board')), MD5),
            (G_STAMP, 'board_view_working.stamp.srcmd5', s(stamp.get('srcmd5')), MD5),
            (G_REL, 'board_view_working.stamp.release.board', s(rel.get('board')), MD5),
        ],
        'engine_head': [
            (G_BOOT, 'expected_boot.engine_head', s(boot.get('engine_head')), MD5),
            (G_RC, 'release_contract.identities.engine_head', s(rcid.get('engine_head')), MD5),
            (G_STAMP, 'board_view_working.stamp.engine', s(stamp.get('engine')), 8),
            (G_REL, 'board_view_working.stamp.release.engine_head', s(rel.get('engine_head')), MD5),
            (G_BOOK, 'book_stable_seal.head_md5', s(book.get('head_md5')), 8),
        ],
        'rl_model': [
            (G_BOOT, 'expected_boot.rl_model', s(boot.get('rl_model')), MD5),
            (G_RC, 'release_contract.identities.rl_model', s(rcid.get('rl_model')), MD5),
            (G_REL, 'board_view_working.stamp.release.rl_model', s(rel.get('rl_model')), MD5),
        ],
        'fv': [
            (G_BOOT, 'expected_boot.fv', s(boot.get('fv')), SHA),
            (G_RC, 'release_contract.identities.fv', s(rcid.get('fv')), SHA),
            (G_REL, 'board_view_working.stamp.release.fv', s(rel.get('fv')), SHA),
        ],
        'config': [
            (G_BOOT, 'expected_boot.config', s(boot.get('config')), SHA),
            (G_RC, 'release_contract.config_sha256', s(rc.get('config_sha256')), SHA),
            (G_STAMP, 'board_view_working.stamp.config', s(stamp.get('config')), 12),
            (G_REL, 'board_view_working.stamp.release.config', s(rel.get('config')), SHA),
            (G_BOOK, 'book_stable_seal.config', s(book.get('config')), SHA),
        ],
        'register': [
            (G_BOOT, 'expected_boot.register', s(boot.get('register')), MD5),
            (G_RC, 'release_contract.identities.register', s(rcid.get('register')), MD5),
            (G_STAMP, 'board_view_working.stamp.register', s(stamp.get('register')), 8),
            (G_REL, 'board_view_working.stamp.release.register', s(rel.get('register')), MD5),
        ],
        'as_of_round': [
            (G_BOOT, 'expected_boot.as_of_round', s(boot.get('as_of_round')), None),
            (G_RC, 'release_contract.as_of_round', s(rc.get('as_of_round')), None),
            (G_SEASON, 'season_state.as_of_round', s(season.get('as_of_round')), None),
            (G_STAMP, 'board_view_working.stamp.asOfRound', s(stamp.get('asOfRound')), None),
            (G_REL, 'board_view_working.stamp.release.as_of_round', s(rel.get('as_of_round')), None),
        ],
    }


# ------------------------------------------------------------------------------------------ CHECK
def evaluate(root):
    """Compare every carrier to computed truth. Returns (rows, halted_groups, ok).

    rows: [(identity, carrier_group, label, value, expected, status)] with status in
          OK / DRIFT / WIDTH / MISSING.
    """
    truth = compute_truth(root)
    carriers = read_carriers(root)
    rows, halted = [], {}

    for ident in IDENTITIES:
        tval, how = truth[ident]
        for group, label, value, width in carriers[ident]:
            expected = tval if width is None else tval[:width]
            if not value:
                status = 'MISSING'
            elif width is not None and len(value) != width:
                status = 'WIDTH'
            elif value != expected:
                status = 'DRIFT'
            else:
                status = 'OK'
            rows.append((ident, group, label, value, expected, status, how))
            if status != 'OK':
                # Carriers are halted at <file-group>:<identity> granularity, NOT at whole-file
                # granularity. That precision is the difference between honest blocking and
                # collateral damage: `release_contract.identities.engine_head` being stale must not
                # block the six-way STORE check, which reads
                # `release_contract.identities.store` — a field in the same dict that is correct.
                # Blocking a check whose carrier is fine would hide a real red behind someone
                # else's, which is the mirror-image of the failure the blocked-once law prevents.
                halted.setdefault('%s:%s' % (group, ident), []).append(
                    '%s = %s (expected %s)' % (label, value or '(empty)', expected))

    return rows, halted, not halted


def render(rows, halted, truth_by_ident, root):
    """The carrier table — every carrier named, exactly as the six-way check named its six."""
    out = []
    out.append('RELEASE MANIFEST — carrier coherence over the full identity set')
    out.append('  root: %s' % root)
    out.append('')
    label_w = max(len(r[2]) for r in rows) + 1
    for ident in IDENTITIES:
        mine = [r for r in rows if r[0] == ident]
        tval, how = truth_by_ident[ident]
        bad = [r for r in mine if r[5] != 'OK']
        out.append('  %s  [%s]' % (ident.upper(), how))
        out.append('    %-*s %-64s %s' % (label_w, '(truth)', tval, ''))
        for _i, _g, label, value, expected, status, _h in mine:
            mark = '' if status == 'OK' else '  <<< %s (expected %s)' % (status, expected)
            out.append('    %-*s %-64s %s%s' % (label_w, label, value or '(empty)', status, mark))
        out.append('    -> %d carriers, %s' % (len(mine), 'COHERENT' if not bad else
                                               'INCOHERENT (%d)' % len(bad)))
        out.append('')

    total = len(rows)
    nbad = sum(1 for r in rows if r[5] != 'OK')
    out.append('  %d carrier fields across %d identities and %d files: %d coherent, %d incoherent'
               % (total, len(IDENTITIES), 7, total - nbad, nbad))
    if halted:
        out.append('')
        out.append('  HALTED CARRIERS — the blocked-once law reports each of these ONCE, and every')
        out.append('  downstream check that reads one is marked BLOCKED rather than failing again:')
        for carrier, fields in halted.items():
            out.append('    %s' % carrier)
            for f in fields:
                out.append('        %s' % f)
    out.append('')
    out.append('  RELEASE MANIFEST COHERENCE: %s' % ('PASS' if not halted else 'FAIL'))
    return '\n'.join(out)


def check(root=None, verbose=True):
    """Assert the live tree is coherent across all eight identities. Raises Halt on any drift."""
    root = os.path.abspath(root or os.environ.get('RL_REPO') or HERE)
    truth = compute_truth(root)
    rows, halted, ok = evaluate(root)
    text = render(rows, halted, truth, root)
    if verbose:
        print(text)
    if not ok:
        raise Halt('release manifest is incoherent across %d carrier group(s): %s'
                   % (len(halted), ', '.join(halted)))
    return rows, halted, text


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('cmd', nargs='?', default='check', choices=('check', 'table'))
    ap.add_argument('--root', default=os.environ.get('RL_REPO') or HERE)
    ap.add_argument('--json', dest='json_path', default=None)
    a = ap.parse_args(argv)

    root = os.path.abspath(a.root)
    truth = compute_truth(root)
    rows, halted, ok = evaluate(root)
    print(render(rows, halted, truth, root))

    if a.json_path:
        with open(a.json_path, 'w', encoding='utf-8') as fh:
            json.dump({'root': root,
                       'truth': {k: {'value': v[0], 'how': v[1]} for k, v in truth.items()},
                       'carriers': [{'identity': r[0], 'group': r[1], 'label': r[2],
                                     'value': r[3], 'expected': r[4], 'status': r[5]}
                                    for r in rows],
                       'halted_groups': halted,
                       'coherent': ok}, fh, indent=2, sort_keys=True)
        print('\n  JSON: %s' % a.json_path)

    if a.cmd == 'table':
        return 0
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
