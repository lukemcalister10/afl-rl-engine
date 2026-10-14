#!/usr/bin/env python3
"""tools/restamp.py — THE ONE STAMPED CARRIER, AND EVERY OTHER STAMP DERIVED FROM IT.

  python3 tools/restamp.py check     # read-only: does every stamp agree with the tree?
  python3 tools/restamp.py apply     # bring the divergent ones into line, through their writers

SHRINK REVIEW S6 (owner word 2026-08-30: "S6 we can do after this is all locked away", then
"Alright, so now s6?").

THE PROBLEM THIS EXISTS FOR. One fact — which engine, store, config and board are live — is
written down in several files. Inside `tools/land` that is already safe: the contract step
MEASURES each identity from the tree and refuses if a carrier disagrees, so a landing cannot leave
them out of step. Nothing outside a landing had that. The ORDER 49 dial flip was committed by
hand, and five separate stamps were left behind — the engine_head pin, the release contract's
identities and self-hash, the board-view stamp, the club-valuation projection, and the sibling
sidecar's contract binding. Every one was found by RUNNING A GATE, minutes at a time, rather than
by noticing; the register calls it "five instances" of one class (v882).

WHAT THIS IS, AND WHAT IT IS NOT. It is not a new authority. The tree is the truth, exactly as the
landing transaction already treats it: an identity is the md5 of the artifact that carries it, and
every stamp below is CHECKED against that measurement and, on `apply`, rewritten to it THROUGH ITS
OWN WRITER OF RECORD — never by this file editing someone else's bytes. The manifest gate stays
where it is and remains the enforcement; this is the thing that makes passing it a two-second
matter instead of a five-round hunt.

THE FENCE, AND IT IS THE WHOLE REASON THIS FILE ENUMERATES INSTEAD OF SEARCHING. Plenty of files
carry today's identities WITHOUT being stamps: `data/release_lineage.json` is the chain of past
releases (it still names engine dc7e34b0 and 7c452715 — correctly), `data/gates_snapshots/` is
keyed by the head it recorded, `ui/data/movers.js` and `ui/data/movers_transition.js` record what
the board was at each point, and the value/rank histories are the record itself. A tool that
"updated every file containing the old id" would quietly falsify all of them. So the stamp set is
enumerated with a reason per entry, the history set is enumerated too, and `check` refuses to run
if the two ever overlap.

BAKE-ONLY, DELIBERATELY ABSENT: `data/book_stable_seal.json` moves at bake acts and nowhere else
(shrink S3/S10). It is listed in HISTORY_OR_BAKE so that its absence here is a stated decision
rather than an oversight.

RETIRED 2026-10-14 — THE SIBLING SIDECAR STAMP. The balanced sibling is no longer built by any
landing (owner word), so `engine/rl_after/ingestion/sibling_repin_state.json` stopped being a stamp
and became a record: it is in HISTORY_OR_BAKE, `check` never reads it, and `apply` no longer has a
refusal for it. The "five instances" story above is kept as the history it is.

RETIRED 2026-10-14 — THE LTI REGISTER. `register` (the md5 of LTI_REGISTER.md) was a measured identity
until the owner retired the register the same day the sibling went. The file is deleted, so there is
nothing to measure: `register` is a FROZEN HISTORICAL field in expected_boot / release_contract / the
UI stamp at its last value (652d83e8…), `measure` no longer computes it, no reader here reads it, and
`apply` never re-hashes it. The manifest check asserts the carriers agree on the frozen value.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


# --------------------------------------------------------------------------- the truth, measured
def measure(root):
    """Every identity, read from the artifact that carries it. The SAME measurers the landing
    transaction uses (tools/landing/steps.PIN_MEASURERS) — asserted equal to them in the tests, so
    the two can never drift into disagreeing about what "the tree" means."""
    sys.path.insert(0, root)
    import config_manifest                                    # noqa: E402
    import fv_provenance                                      # noqa: E402
    return {
        'board': md5(os.path.join(root, 'data', 'rl_build', 'rl_app_data.json')),
        'store': md5(os.path.join(root, 'engine', 'rl_after', 'rl_model_data.json')),
        'engine_head': md5(os.path.join(root, 'engine', 'rl_after', '_merged_recover.py')),
        'rl_model': md5(os.path.join(root, 'engine', 'rl_after', 'rl_model.py')),
        'v0surf': md5(os.path.join(root, 'data', 'v0surf.pkl')),
        'config': config_manifest.manifest_hash(root),
        'fv': fv_provenance.fv_identity(fv_provenance.checkout_fv_dir(root)),
    }


# ------------------------------------------------------------------------------- the stamp set
#: name -> (path, reader(root) -> {identity: value_or_None}, writer name)
#: The reader returns SHORT or FULL values as the file actually carries them; comparison is by
#: prefix on the measured value, because several stamps carry a 8- or 12-char form on purpose.
def _boot(root):
    with open(os.path.join(root, 'data', 'expected_boot.json'), encoding='utf-8') as f:
        d = json.load(f)
    return {k: d.get(k) for k in ('board', 'store', 'engine_head', 'rl_model',
                                  'v0surf', 'config', 'fv')}


def _contract(root):
    with open(os.path.join(root, 'data', 'release_contract.json'), encoding='utf-8') as f:
        d = json.load(f)
    ids = d.get('identities') or {}
    return {'board': ids.get('board'), 'store': ids.get('store'),
            'engine_head': ids.get('engine_head'), 'rl_model': ids.get('rl_model'),
            'fv': ids.get('fv'),
            'config': d.get('config_sha256')}


def _js_bundle(path):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    i = s.index('{', s.index('='))
    depth = 0
    for j, ch in enumerate(s[i:], i):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return json.loads(s[i:j + 1])
    raise ValueError('unbalanced bundle in %s' % path)


def _board_view(root, which='working'):
    st = _js_bundle(os.path.join(root, 'ui', 'data', 'board_view_%s.js' % which)).get('stamp') or {}
    return {'board': st.get('board') or st.get('board_md5'), 'store': st.get('store'),
            'engine_head': st.get('engine'),
            'config': st.get('config')}


def _club_valuation(root):
    st = _js_bundle(os.path.join(root, 'ui', 'data', 'club_valuation.js')).get('stamp') or {}
    return {'board': st.get('board'), 'store': st.get('store'), 'engine_head': st.get('engine')}


STAMPS = [
    ('expected_boot', 'data/expected_boot.json', _boot,
     'the CARRIER — every other stamp below is checked against the tree the same way, but this is '
     'the file the boot guard and the manifest read',
     'tools/land (pins step)'),
    ('release_contract', 'data/release_contract.json', _contract,
     'the released identities + config, sealed by contract_sha256',
     'release_contract.restamp_dynamic + release_contract.restamp_bake_identities'),
    ('board_view_working', 'ui/data/board_view_working.js', lambda r: _board_view(r, 'working'),
     'the working board the UI serves, stamped with what produced it',
     'ui/tools/extract_board_view.py'),
    ('club_valuation', 'ui/data/club_valuation.js', _club_valuation,
     'the clubs projection, which names the board it was computed from',
     'ui/tools/ingest_inputs.py'),
    # `sibling_repin_state` was the fifth stamp until 2026-10-14. The balanced sibling is RETIRED
    # (owner word), so the sidecar's store/fv binding is a record of the last reconcile, not a claim
    # about what is live: it is listed under HISTORY_OR_BAKE below and never checked or restamped.
]

#: Files that a reader might expect here and that carry NO identity claim at all, by design. Named
#: so their absence from STAMPS is a stated decision. `board_view_public.js` is the public bundle
#: and the standing design law keeps process off user surfaces: its stamp carries baseYear /
#: nPlayers / maxV / v0 and no engine, store or board id. It is regenerated by the same writer as
#: the working view, so it cannot drift apart from a view that IS checked.
NO_IDENTITY_BY_DESIGN = [
    ('ui/data/board_view_public.js',
     'the public bundle carries no engine/store/board id — process stays off user surfaces'),
]

#: Files that carry the same values and MUST NOT be restamped, each with the reason. A stamp says
#: "this is what is live"; these say "this is what was", and rewriting one falsifies the record.
HISTORY_OR_BAKE = [
    ('data/release_lineage.json', 'the chain of past releases — it names superseded engines on purpose'),
    ('data/gates_snapshots/', 'each snapshot is keyed to the head it recorded'),
    ('ui/data/movers.js', 'every point records the board as it stood at that point'),
    ('ui/data/movers_transition.js', 'the owner-approved provenance transition, a historical record'),
    ('engine/rl_after/ingestion/value_history.json', 'the value record'),
    ('engine/rl_after/ingestion/rank_history.json', 'the rank record'),
    ('engine/rl_after/ingestion/pos_rank_history.json', 'the positional-rank record'),
    ('data/book_stable_seal.json', 'BAKE-ONLY: the seal moves at bake acts and nowhere else (shrink S3/S10)'),
    ('engine/rl_after/ingestion/sibling_repin_state.json',
     'HISTORICAL since 2026-10-14: the balanced sibling is retired; the sidecar records the last '
     'reconcile and no landing step rebuilds it'),
]


def _agrees(stamped, truth):
    """A stamp may carry a short form on purpose (8 or 12 chars). Agreement is prefix agreement on
    a non-empty stamped value; a stamp that carries nothing for an identity is not a disagreement,
    it simply does not make that claim."""
    if stamped is None:
        return True
    s = str(stamped)
    return len(s) > 0 and str(truth).startswith(s)


def check(root, verbose=True):
    truth = measure(root)
    fenced = {p for p, _ in HISTORY_OR_BAKE}
    overlap = [n for n, p, _, _, _ in STAMPS if p in fenced]
    if overlap:
        raise SystemExit('REFUSING: %s is listed as BOTH a stamp and a historical record. One of '
                         'the two tables is wrong and this tool will not guess which.' % overlap)
    rows, bad = [], []
    for name, path, reader, _why, writer in STAMPS:
        full = os.path.join(root, path)
        if not os.path.exists(full):
            rows.append((name, 'ABSENT', '', writer))
            continue
        try:
            got = reader(root)
        except Exception as exc:
            rows.append((name, 'UNREADABLE', str(exc)[:60], writer))
            bad.append((name, 'unreadable', str(exc)[:120]))
            continue
        off = [(k, v, truth[k]) for k, v in got.items()
               if k in truth and not _agrees(v, truth[k])]
        if off:
            bad.append((name, writer, off))
            rows.append((name, 'STALE', ', '.join('%s %s != %s' % (k, str(v)[:12], str(t)[:12])
                                                  for k, v, t in off), writer))
        else:
            claims = len([k for k in got if got[k]])
            if not claims:
                # VACUITY GUARD. A stamp that claims nothing passes every comparison, which is the
                # one way this table can rot without anybody noticing: a writer stops emitting its
                # stamp and the row goes on reporting AGREES forever. A file with no identity claim
                # belongs in NO_IDENTITY_BY_DESIGN, named, or it does not belong in this tool.
                bad.append((name, writer, [('<no identity claim>', None, 'expected at least one')]))
                rows.append((name, 'VACUOUS', 'claims no identity — it cannot disagree, so it '
                                              'proves nothing', writer))
            else:
                rows.append((name, 'AGREES', '%d identity claim(s)' % claims, writer))
    if verbose:
        print('=' * 96)
        print('RESTAMP CHECK — every stamp against the tree it claims to describe')
        print('=' * 96)
        for k in sorted(truth):
            print('  tree %-12s %s' % (k, truth[k]))
        print('-' * 96)
        for name, state, detail, writer in rows:
            print('  %-22s %-11s %s' % (name, state, detail))
            if state == 'STALE':
                print('  %-22s %-11s writer of record: %s' % ('', '', writer))
        print('-' * 96)
        print('  NO IDENTITY CLAIM BY DESIGN (named so the absence is a decision, not an oversight):')
        for p_, why in NO_IDENTITY_BY_DESIGN:
            print('    %-46s %s' % (p_, why))
        print('  FENCED (carry the same values as HISTORY and are never restamped):')
        for p, why in HISTORY_OR_BAKE:
            print('    %-46s %s' % (p, why))
        print('=' * 96)
        print('RESTAMP: %s' % ('ALL %d STAMPS AGREE WITH THE TREE' % len(rows) if not bad
                               else '%d OF %d STAMPS ARE STALE' % (len(bad), len(rows))))
    return truth, bad


# ------------------------------------------------------------------------------------- the writers
def _run(root, argv, env=None):
    e = dict(os.environ)
    e.setdefault('RL_REPO', root)
    if env:
        e.update(env)
    p = subprocess.run(argv, cwd=root, env=e, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True)
    return p.returncode, p.stdout


def apply(root):
    truth, bad = check(root)
    if not bad:
        print('\nNOTHING TO DO — no stamp is stale.')
        return 0
    stale = {n for n, _, _ in bad}
    print('\n' + '=' * 96)
    print('RESTAMP APPLY — each stale stamp through its own writer of record')
    print('=' * 96)

    if 'expected_boot' in stale:
        raise SystemExit(
            'REFUSING: data/expected_boot.json is stale, and it is the CARRIER. Moving the carrier '
            'is a landing act — it is what `tools/land` exists to do, with a prereg, a predicted '
            'board and an abort ladder behind it. This tool derives the OTHER stamps FROM the '
            'carrier; it will not move the carrier itself. Run the landing.')

    if 'release_contract' in stale:
        sys.path.insert(0, root)
        import release_contract as RCT
        rep = RCT.restamp_bake_identities(root, truth)
        for field, was, now in rep['moved']:
            print('  release_contract  %-24s %s -> %s' % (field, str(was)[:12], str(now)[:12]))
        print('  release_contract  contract_sha256          %s -> %s'
              % (rep['seal_before'][:12], rep['seal_after'][:12]))
        print('  release_contract  frozen fields unmoved: %d checked' % rep['frozen_checked'])
        rc, out = _run(root, [sys.executable, 'release_contract.py', 'check'])
        print('  release_contract  release_contract.py check: %s' % ('PASS' if rc == 0 else 'FAIL'))
        if rc != 0:
            raise SystemExit('the contract does not check out after the restamp:\n%s' % out[-1200:])

    if 'board_view_working' in stale:
        rc, out = _run(root, [sys.executable, 'ui/tools/extract_board_view.py'])
        print('  board_view        extract_board_view.py: %s' % ('OK' if rc == 0 else 'FAILED'))
        if rc != 0:
            raise SystemExit(out[-1200:])

    if 'club_valuation' in stale:
        # --clubs-only: the picks bundle re-stamp ONLY. The bare invocation is the FULL ingest, whose step 0
        # applies the owner's locations sheet to the store — on 2026-10-13 that couriered 15 AFL-club changes
        # into the store as a side effect of a re-stamp. A re-stamp never writes the store.
        rc, out = _run(root, [sys.executable, 'ui/tools/ingest_inputs.py', '--clubs-only'])
        print('  club_valuation    ingest_inputs.py: %s' % ('OK' if rc == 0 else 'FAILED'))
        if rc != 0:
            raise SystemExit(out[-1200:])

    print('-' * 96)
    _, bad2 = check(root)
    if bad2:
        raise SystemExit('RESTAMP FAILED — %d stamp(s) still stale after their writers ran.' % len(bad2))
    print('\nRESTAMP APPLIED — every stamp now agrees with the tree.')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('verb', nargs='?', default='check', choices=('check', 'apply'))
    ap.add_argument('--root', default=ROOT)
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    if a.verb == 'check':
        _, bad = check(root)
        return 1 if bad else 0
    return apply(root)


if __name__ == '__main__':
    sys.exit(main())
