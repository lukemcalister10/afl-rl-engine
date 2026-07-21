"""GENERIC RELEASE-METADATA CONTRACT PROOF — the release contract copies VERIFIED manifest fields.

Tests GENERIC release-metadata behavior WITHOUT inventing semantics and WITHOUT claiming final RC
compatibility (addendum 2026-07-20). Using a SYNTHETIC PR #127-style release manifest (release_version,
balanced_board_md5, the fixed model pins) plus a boot manifest carrying the CURRENT weekly board/store,
it proves the movers/UI release identity. The fixture remains NEUTRAL: it treats balanced_board_md5 as
the fixed PRESENT-LENS baseline (never the final full-board hash), treats the moving `board` field as
the complete CURRENT board artifact, encodes NO release-policy switch posture (RL_PVC2/RL_LEGE/RL_LEGF),
and makes no assumption about the final full-board hash. It proves the movers/UI release identity:

  1. copies the FIXED release-baseline fields (release_version + balanced_board_md5) VERBATIM from the
     release manifest — it does NOT synthesize balanced_board_md5 from the weekly board;
  2. copies the FIXED model pins (engine_head / rl_model / fv / config / register) from the boot manifest;
  3. tracks as_of_round from the APPLIED round — after R15 as_of_round is 15, never left at 14, and it
     is NOT taken blindly from a CLI argument (it equals the round the report is built for);
  4. carries the CURRENT weekly board + store as the DYNAMIC fields (they move each round; the fixed
     baseline does not);
  5. treats balanced_board_md5 as an IMMUTABLE release-baseline identity: two different weekly rounds on
     the same release carry the SAME balanced_board_md5 (the current board differs; the baseline does not).

SEMANTICS (owner/supervisor rulings 2026-07-20): balanced_board_md5 is the immutable accepted
PRESENT-LENS baseline identity (06d8af60...), constant across weekly score updates — NOT the current
weekly balanced board and NOT assumed to be the final complete board-file hash. This proof does not
claim final RC compatibility; final switch-manifest closure + Leg E/F acceptance + final full-board
pinning + RC-lineage integration are external dependencies.

Run:  python3 session_2026-07-20/weekly_updater_hardening/rc_manifest_compat_proof.py [--write]
Exit 0 = ALL PASS. No board build; writes NOTHING outside a throwaway tempdir.
"""
import argparse
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ING = os.path.join(REPO, 'engine', 'rl_after', 'ingestion')
sys.path.insert(0, ING)
import round_movers as MV   # noqa: E402

# a SYNTHETIC PR #127-style release manifest (test-only present-lens baseline; NOT the real RC, NOT a
# claim of final RC compatibility). release_version + balanced_board_md5 are explicit verified fields
# the proof checks are COPIED verbatim (never synthesized).
RC_RELEASE = {
    'release_version': 'synthetic-baseline-v1',
    'balanced_board_md5': '06d8af60b679a12db07c064c60c065f9',
}
RC_MODEL_PINS = {
    'engine_head': 'a1b2c3d4e5f60718293a4b5c6d7e8f90',
    'rl_model': '112233445566778899aabbccddeeff00',
    'fv': 'ffeeddccbbaa99887766554433221100ffeeddccbbaa99887766554433221100',
    'config': 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc0',
    'register': 'aaaabbbbccccddddeeeeffff0000111',
}


def _fixture(board, store, round_n):
    """A throwaway repo-shaped fixture with a PR #127-style release manifest + a boot manifest whose
    board/store are the CURRENT weekly ones for `round_n`."""
    root = tempfile.mkdtemp(prefix='rc_compat_')
    os.makedirs(os.path.join(root, 'data'))
    lineage = dict(RC_RELEASE)
    lineage['_doc'] = 'synthetic PR #127-style RC release baseline (test fixture)'
    with open(os.path.join(root, 'data', 'release_lineage.json'), 'w') as f:
        json.dump(lineage, f, indent=2)
    boot = {'board': board, 'store': store}
    boot.update(RC_MODEL_PINS)
    with open(os.path.join(root, 'data', 'expected_boot.json'), 'w') as f:
        json.dump(boot, f, indent=2)
    return root


def main(argv):
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true')
    args = ap.parse_args(argv[1:])
    report = {}

    # R15 on the current weekly board B15/store S15, R16 on B16/S16 (the fixed baseline is unchanged)
    r15_root = _fixture('b15b15b15b15b15b15b15b15b15b15b1', 's15s15s15s15s15s15s15s15s15s15s1', 15)
    r16_root = _fixture('b16b16b16b16b16b16b16b16b16b16b1', 's16s16s16s16s16s16s16s16s16s16s1', 16)
    try:
        rel15 = MV.release_identity(r15_root, 15)
        rel16 = MV.release_identity(r16_root, 16)
    finally:
        shutil.rmtree(r15_root, ignore_errors=True)
        shutil.rmtree(r16_root, ignore_errors=True)

    # 1: fixed baseline fields copied VERBATIM (not synthesized)
    report['1_fixed_baseline_copied'] = {
        'release_version': rel15['release_version'], 'balanced_board_md5': rel15['balanced_board_md5'],
        'pass': (rel15['release_version'] == RC_RELEASE['release_version']
                 and rel15['balanced_board_md5'] == RC_RELEASE['balanced_board_md5'])}

    # 2: balanced_board_md5 is NOT synthesized from the weekly board
    report['2_balanced_not_synthesized'] = {
        'balanced': rel15['balanced_board_md5'], 'weekly_board': rel15['board'],
        'pass': rel15['balanced_board_md5'] != rel15['board']
        and rel15['balanced_board_md5'] == RC_RELEASE['balanced_board_md5']}

    # 3: model pins copied from the boot manifest
    report['3_model_pins_copied'] = {
        'pass': all(rel15[k] == v for k, v in RC_MODEL_PINS.items())}

    # 4: as_of_round tracks the applied round (15 after R15, never left at 14)
    report['4_as_of_round_tracks_round'] = {
        'r15': rel15['as_of_round'], 'r16': rel16['as_of_round'],
        'pass': rel15['as_of_round'] == 15 and rel16['as_of_round'] == 16 and rel15['as_of_round'] != 14}

    # 5: dynamic weekly fields move; the fixed baseline does NOT (immutable across rounds)
    report['5_baseline_immutable_board_moves'] = {
        'r15_board': rel15['board'][:8], 'r16_board': rel16['board'][:8],
        'balanced_r15': rel15['balanced_board_md5'][:8], 'balanced_r16': rel16['balanced_board_md5'][:8],
        'pass': (rel15['board'] != rel16['board'] and rel15['store'] != rel16['store']
                 and rel15['balanced_board_md5'] == rel16['balanced_board_md5']
                 and rel15['release_version'] == rel16['release_version'])}

    order = ['1_fixed_baseline_copied', '2_balanced_not_synthesized', '3_model_pins_copied',
             '4_as_of_round_tracks_round', '5_baseline_immutable_board_moves']
    all_pass = all(report[k]['pass'] for k in order)
    report['ALL_PASS'] = all_pass
    print("\n==== GENERIC RELEASE-METADATA CONTRACT PROOF (copies verified fields; present-lens baseline) ====")
    for k in order:
        print("  [%s] %s" % ('PASS' if report[k]['pass'] else 'FAIL', k))
    print("==== %s ====" % ('ALL PASS' if all_pass else 'FAIL'))
    if args.write:
        with open(os.path.join(HERE, 'rc_manifest_compat_proof.json'), 'w') as f:
            json.dump(report, f, indent=2, sort_keys=True, default=str)
        print("wrote rc_manifest_compat_proof.json")
    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
