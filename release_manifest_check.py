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
THE IDENTITY SET  (11)                       THE CARRIERS  (8 files, 43 fields)

    store            engine/rl_after/rl_model_data.json   data/expected_boot.json
    board            data/rl_build/rl_app_data.json       data/release_contract.json
    engine_head      engine/rl_after/_merged_recover.py   data/season_state.json
    rl_model         engine/rl_after/rl_model.py          data/rl_build/rl_app_data.json.srcmd5
    fv               engine/forward_valuation/*.py        ui/data/board_view_working.js  (stamp)
    config           data/model_config.json               ui/data/board_view_working.js  (stamp.release)
    register         LTI_REGISTER.md                      data/book_stable_seal.json
    as_of_round      (declared — see below)               data/sheet_pins.json
    sheet            docs/owner_annotations/SITTER_2026_v1.csv   (the file the declaration names)
    sheet_rows       the same file's csv row count
    sheet_injured_y  the same file's injured=Y count

THE SHEET ENTERED THIS TABLE ON 2026-08-21 (PLAN_v6 3a, deferred by its own text to 2b: "the sheet
md5 + the pin file become MANIFEST-CHECKED CARRIER FIELDS with the round lander as sole writer once
2b lands"). Until 3a those three facts were SIX LITERALS IN TWO BLOCKS inside `_merged_recover.py`,
where no gate could see them and the two copies could drift — which is exactly what ERRATUM E4
records happening. They are now ONE declaration, `data/sheet_pins.json`, written by ONE writer
(`land round`, steps.sheet) and CHECKED HERE, computed from the artifact like every other row: a
sheet that moves without its declaration moving is caught by this gate before it halts a build.

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

IDENTITIES = ('store', 'board', 'engine_head', 'rl_model', 'fv', 'config', 'register', 'as_of_round',
              'sheet', 'sheet_rows', 'sheet_injured_y')

# The carrier FILES. The keys are the carrier-group names the runner blocks on.
BOOT_REL = 'data/expected_boot.json'
CONTRACT_REL = 'data/release_contract.json'
SEASON_REL = 'data/season_state.json'
SIDECAR_REL = 'data/rl_build/rl_app_data.json.srcmd5'
BVW_REL = 'ui/data/board_view_working.js'
BOOK_REL = 'data/book_stable_seal.json'
SHEET_PINS_REL = 'data/sheet_pins.json'

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

    # THE SHEET — three facts about ONE artifact, computed from that artifact (PLAN_v6 3a, deferred
    # to 2b: "the sheet md5 + the pin file become MANIFEST-CHECKED CARRIER FIELDS with the round
    # lander as sole writer"). The subject is the file the DECLARATION names, not one hardcoded here:
    # the declaration says what it pins, and this gate measures what it pinned and asserts the three
    # facts about it. Measured the ENGINE'S OWN WAY (see `_sheet_facts`), because a gate that
    # measured the sheet a nearly-identical way would pass a file the build then halts on.
    sheet_md5, sheet_rows, sheet_y = _sheet_facts(root)
    truth['sheet'] = (sheet_md5, 'computed md5 %s' % _sheet_rel(root))
    truth['sheet_rows'] = (str(sheet_rows), 'computed csv row count %s' % _sheet_rel(root))
    truth['sheet_injured_y'] = (str(sheet_y), 'computed injured=Y count %s' % _sheet_rel(root))
    return truth


def _sheet_rel(root):
    """The sheet the pin declaration names. A declaration that names none pins nothing."""
    rel = (_json(os.path.join(root, SHEET_PINS_REL)) or {}).get('sheet_path')
    if not rel:
        raise Halt('%s names no sheet_path. A pin declaration with a hole in it pins nothing, and '
                   'this gate will not invent the subject it is supposed to be checking.'
                   % SHEET_PINS_REL)
    return rel


def _sheet_facts(root):
    """(md5, rows, injured_y) — character for character what ORDER 41 / ORDER 42 compute.

    `_merged_recover.py`'s guards read the raw bytes, md5 them, decode utf-8, count
    `csv.DictReader` rows, and count rows whose `injured` cell strips-and-uppers to 'Y'. Any other
    reading is a different measurement wearing the same name — the failure ERRATUM E1b records, where
    a `.decode("utf-8", errors="replace")` mangled 16 of 411 names on exactly the file it was written
    to check.
    """
    import csv                                                                  # noqa: PLC0415
    raw = open(os.path.join(root, _sheet_rel(root)), 'rb').read()
    rows = list(csv.DictReader(raw.decode('utf-8').splitlines()))
    ys = [r for r in rows if (r.get('injured') or '').strip().upper() == 'Y']
    return hashlib.md5(raw).hexdigest(), len(rows), len(ys)


# --------------------------------------------------------------------------------------- CARRIERS
def read_carriers(root):
    """Enumerate every carrier field, per identity.

    Returns {identity: [(carrier_group, label, value, width, kind), ...]} where `kind` is:

      'live'    the carrier states what the tree IS. It must equal computed truth, now.
      'sealed'  the carrier states what the tree WAS when an artifact was last sealed against it.
                It legitimately lags between seals, and is reported as SEALED-LAG, never as drift.
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
    pins = _json(p(SHEET_PINS_REL))

    def s(v):
        return '' if v is None else str(v)

    G_BOOT, G_RC = 'expected_boot', 'release_contract'
    G_SEASON, G_SIDE = 'season_state', 'board_sidecar'
    G_STAMP, G_REL = 'ui_bundle.stamp', 'ui_bundle.stamp.release'
    G_BOOK, G_PINS = 'book_seal', 'sheet_pins'

    return {
        'store': [
            (G_BOOT, 'expected_boot.store', s(boot.get('store')), MD5, 'live'),
            (G_RC, 'release_contract.identities.store', s(rcid.get('store')), MD5, 'live'),
            (G_SEASON, 'season_state.source_store_md5', s(season.get('source_store_md5')), MD5, 'live'),
            (G_SIDE, 'rl_app_data.srcmd5.source_md5', s(sidecar.get('source_md5')), MD5, 'live'),
            (G_STAMP, 'board_view_working.stamp.store_md5', s(stamp.get('store_md5')), MD5, 'live'),
            (G_STAMP, 'board_view_working.stamp.store', s(stamp.get('store')), 8, 'live'),
            (G_REL, 'board_view_working.stamp.release.store', s(rel.get('store')), MD5, 'live'),
            (G_BOOK, 'book_stable_seal.store_md5', s(book.get('store_md5')), 8, 'sealed'),
        ],
        'board': [
            (G_BOOT, 'expected_boot.board', s(boot.get('board')), MD5, 'live'),
            (G_RC, 'release_contract.identities.board', s(rcid.get('board')), MD5, 'live'),
            (G_SIDE, 'rl_app_data.srcmd5.own_md5', s(sidecar.get('own_md5')), MD5, 'live'),
            (G_STAMP, 'board_view_working.stamp.board_md5', s(stamp.get('board_md5')), MD5, 'live'),
            (G_STAMP, 'board_view_working.stamp.board', s(stamp.get('board')), MD5, 'live'),
            (G_STAMP, 'board_view_working.stamp.srcmd5', s(stamp.get('srcmd5')), MD5, 'live'),
            (G_REL, 'board_view_working.stamp.release.board', s(rel.get('board')), MD5, 'live'),
        ],
        'engine_head': [
            (G_BOOT, 'expected_boot.engine_head', s(boot.get('engine_head')), MD5, 'live'),
            (G_RC, 'release_contract.identities.engine_head', s(rcid.get('engine_head')), MD5, 'live'),
            (G_STAMP, 'board_view_working.stamp.engine', s(stamp.get('engine')), 8, 'live'),
            (G_REL, 'board_view_working.stamp.release.engine_head', s(rel.get('engine_head')), MD5, 'live'),
            (G_BOOK, 'book_stable_seal.head_md5', s(book.get('head_md5')), 8, 'sealed'),
        ],
        'rl_model': [
            (G_BOOT, 'expected_boot.rl_model', s(boot.get('rl_model')), MD5, 'live'),
            (G_RC, 'release_contract.identities.rl_model', s(rcid.get('rl_model')), MD5, 'live'),
            (G_REL, 'board_view_working.stamp.release.rl_model', s(rel.get('rl_model')), MD5, 'live'),
        ],
        'fv': [
            (G_BOOT, 'expected_boot.fv', s(boot.get('fv')), SHA, 'live'),
            (G_RC, 'release_contract.identities.fv', s(rcid.get('fv')), SHA, 'live'),
            (G_REL, 'board_view_working.stamp.release.fv', s(rel.get('fv')), SHA, 'live'),
        ],
        'config': [
            (G_BOOT, 'expected_boot.config', s(boot.get('config')), SHA, 'live'),
            (G_RC, 'release_contract.config_sha256', s(rc.get('config_sha256')), SHA, 'live'),
            (G_STAMP, 'board_view_working.stamp.config', s(stamp.get('config')), 12, 'live'),
            (G_REL, 'board_view_working.stamp.release.config', s(rel.get('config')), SHA, 'live'),
            (G_BOOK, 'book_stable_seal.config', s(book.get('config')), SHA, 'sealed'),
        ],
        'register': [
            (G_BOOT, 'expected_boot.register', s(boot.get('register')), MD5, 'live'),
            (G_RC, 'release_contract.identities.register', s(rcid.get('register')), MD5, 'live'),
            (G_STAMP, 'board_view_working.stamp.register', s(stamp.get('register')), 8, 'live'),
            (G_REL, 'board_view_working.stamp.release.register', s(rel.get('register')), MD5, 'live'),
        ],
        'as_of_round': [
            (G_BOOT, 'expected_boot.as_of_round', s(boot.get('as_of_round')), None, 'live'),
            (G_RC, 'release_contract.as_of_round', s(rc.get('as_of_round')), None, 'live'),
            (G_SEASON, 'season_state.as_of_round', s(season.get('as_of_round')), None, 'live'),
            (G_STAMP, 'board_view_working.stamp.asOfRound', s(stamp.get('asOfRound')), None, 'live'),
            (G_REL, 'board_view_working.stamp.release.as_of_round', s(rel.get('as_of_round')), None, 'live'),
        ],
        # THE SHEET PIN DECLARATION — one carrier each, and one is enough for the assertion to bite:
        # these are the three facts the ORDER 41 and ORDER 42 guards HALT the build on, and until
        # PACKAGE 3a they were six literals inside the engine where no gate could see them. They are
        # `live`, never `sealed`: a sheet that has moved without its declaration moving is not a lag,
        # it is a build that is about to halt.
        'sheet': [
            (G_PINS, 'sheet_pins.sheet_md5', s(pins.get('sheet_md5')), MD5, 'live'),
        ],
        'sheet_rows': [
            (G_PINS, 'sheet_pins.sheet_rows', s(pins.get('sheet_rows')), None, 'live'),
        ],
        'sheet_injured_y': [
            (G_PINS, 'sheet_pins.sheet_injured_y', s(pins.get('sheet_injured_y')), None, 'live'),
        ],
    }


# ------------------------------------------------------------------------------------------ CHECK
def evaluate(root):
    """Compare every carrier to computed truth. Returns (rows, halted_groups, ok).

    rows: [(identity, carrier_group, label, value, expected, status, how)] with status in
          OK / DRIFT / WIDTH / MISSING / SEALED-LAG.

    ------------------------------------------------------------------------------------------
    SEALED-LAG, and why it exists — a correction made BEFORE this gate landed, by measurement.

    The first draft of this file asserted all 40 carriers must equal computed truth, full stop.
    Run against the tree the moment the apply seat moved the store cb38ef11 -> cc02567f, it
    reported `book_stable_seal.store_md5` as DRIFT. That looked like a find. It was not.

    `data/book_stable_seal.json` is a walk-forward book FREEZE-STAMP: it records the identities
    the sealed book was built against, and it is re-stamped when the BOOK is re-sealed (at a
    bake), not when the store moves. Measured across its own history:

        2e49963      seal.store 968de0c7   expected_boot.store 968de0c7   coherent
        f27482f~1    seal.store 968de0c7   expected_boot.store cb38ef11   LAGGING
        f27482f      seal.store cb38ef11   expected_boot.store cb38ef11   coherent  (re-sealed)

    i.e. the tree has been in exactly today's shape before, legitimately, and the lag closed at
    the next bake. Asserting equality here would red this gate on every ordinary store write
    until someone re-sealed a book to silence it — which is precisely the failure mode this file
    was written to end (the panel 10/10, the movers known-red count, the R14 config pin,
    BOARD_MD5_GOOD: each true when written, each a false red the day the tree legitimately moved).

    So sealed carriers get their own status. A lag is REPORTED — loudly, with both values, because
    "ship_gates B3's baseline predates the current store" is real and useful information — but it
    does not halt a carrier and it does not red a run. What a sealed carrier IS still asserted on
    is form: MISSING and WIDTH remain failures, so a seal that loses a field or silently truncates
    one is still caught.
    """
    truth = compute_truth(root)
    carriers = read_carriers(root)
    rows, halted = [], {}

    for ident in IDENTITIES:
        tval, how = truth[ident]
        for group, label, value, width, kind in carriers[ident]:
            expected = tval if width is None else tval[:width]
            if not value:
                status = 'MISSING'
            elif width is not None and len(value) != width:
                status = 'WIDTH'
            elif value != expected:
                status = 'DRIFT' if kind == 'live' else 'SEALED-LAG'
            else:
                status = 'OK'
            rows.append((ident, group, label, value, expected, status, how))
            if status not in ('OK', 'SEALED-LAG'):
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
        bad = [r for r in mine if r[5] not in ('OK', 'SEALED-LAG')]
        lag = [r for r in mine if r[5] == 'SEALED-LAG']
        out.append('  %s  [%s]' % (ident.upper(), how))
        out.append('    %-*s %-64s %s' % (label_w, '(truth)', tval, ''))
        for _i, _g, label, value, expected, status, _h in mine:
            mark = '' if status == 'OK' else '  <<< %s (expected %s)' % (status, expected)
            out.append('    %-*s %-64s %s%s' % (label_w, label, value or '(empty)', status, mark))
        verdict = 'COHERENT' if not bad else 'INCOHERENT (%d)' % len(bad)
        if lag and not bad:
            verdict = 'COHERENT (%d sealed carrier lagging — see below)' % len(lag)
        out.append('    -> %d carriers, %s' % (len(mine), verdict))
        out.append('')

    total = len(rows)
    nbad = sum(1 for r in rows if r[5] not in ('OK', 'SEALED-LAG'))
    nlag = sum(1 for r in rows if r[5] == 'SEALED-LAG')
    nfiles = len({r[1] for r in rows})
    out.append('  %d carrier fields across %d identities and %d files: %d coherent, %d incoherent, '
               '%d sealed-lag' % (total, len(IDENTITIES), nfiles, total - nbad - nlag, nbad, nlag))
    if nlag:
        out.append('')
        out.append('  SEALED-LAG — a freeze-stamp naming the state it was SEALED against, not the')
        out.append('  state the tree is in. Legitimate between seals; reported, never gating:')
        for _i, _g, label, value, expected, status, _h in rows:
            if status == 'SEALED-LAG':
                out.append('    %-44s sealed against %s, tree is now %s' % (label, value, expected))
        out.append('    (i.e. the artifact these stamps belong to has not been re-sealed since the')
        out.append('     tree last moved. That is information, not a defect — but a gate that')
        out.append('     consumes the seal as a baseline is comparing against the older state.)')
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
