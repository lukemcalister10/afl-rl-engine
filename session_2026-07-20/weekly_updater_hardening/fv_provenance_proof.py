"""FORWARD-VALUATION PROVENANCE + CONFIG-POLICY PROOF (gate OFF, SCRATCH only).

Proves the 2026-07-20 provenance hardening (staged_apply):

  GREEN — a staged apply binds RL_FV to the STAGED forward_valuation, builds the board under the
          accepted release config policy (RL_CONFIG_MODE=gate), records distribution_pricing's path +
          full hash in the transaction manifest, passes Guard 5, and commits. The FV module used is the
          staged dd19a234, INSIDE the staged repo.

  RED (the audit's defect) — the stale distribution_pricing 21d530bf sits on the RL_FV DEFAULT path
          (/home/claude/rl_workspace/forward_valuation) in this container. The updater must NEVER
          generate, pin or commit a board from it (the d7a95e8d board):
            R1  the provenance guard, handed the ambient stale module, HALTS (FVProvenanceError);
            R2  a full apply whose FV binding is mis-pointed at the ambient stale dir HALTS before board
                generation (ABORTED_PRECOMMIT) — no board, no pins, no ledger, live files byte-identical;
            R3  a full apply with an ADVERSARIAL inherited RL_FV=<ambient stale> is FORCED back to the
                staged module, builds the CORRECT board (dd19a234), and commits — the stale board is
                never produced.

  CONFIG — an inherited conflicting valuation flag (e.g. RL_LEGE=0) HALTS before any staging
          (ConfigPolicyError); the green build confirms RL_CONFIG_MODE=gate loaded the pinned manifest.

Run:  python3 session_2026-07-20/weekly_updater_hardening/fv_provenance_proof.py [--write]
Exit 0 = ALL PASS.
"""
import os, sys, json, shutil, tempfile, hashlib, argparse, time, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RA = os.path.join(REPO, 'engine', 'rl_after')
ING = os.path.join(RA, 'ingestion')
sys.path.insert(0, RA)
sys.path.insert(0, ING)

import round_entry as RE               # noqa: E402
import staged_apply as SA              # noqa: E402
import score_ingestor as SI            # noqa: E402

AMBIENT_FV = '/home/claude/rl_workspace/forward_valuation'   # the RL_FV default; holds stale 21d530bf here
GEN = "2026-07-20T00:00:00Z"


def md5(path):
    if not os.path.exists(path):
        return None
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def make_scratch(tag):
    dst = tempfile.mkdtemp(prefix='wkfv_%s_' % tag, dir=os.environ.get('WK_SCRATCH_BASE') or tempfile.gettempdir())
    shutil.copytree(RA, os.path.join(dst, 'engine', 'rl_after'))
    shutil.copytree(os.path.join(REPO, 'engine', 'forward_valuation'),
                    os.path.join(dst, 'engine', 'forward_valuation'))
    ws = os.path.join(dst, 'engine', 'rl_after')
    for f in ('config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py', 'boot_guard.py',
              'season_state.py', 'release_contract.py'):
        shutil.copyfile(os.path.join(REPO, f), os.path.join(ws, f))
    for f in ('boot_guard.py', 'config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py',
              'season_state.py', 'release_contract.py'):
        shutil.copyfile(os.path.join(REPO, f), os.path.join(dst, f))
    shutil.copytree(os.path.join(REPO, 'data'), os.path.join(dst, 'data'))
    shutil.copytree(os.path.join(REPO, 'session_2026-07-18', 'legf5'),
                    os.path.join(dst, 'session_2026-07-18', 'legf5'))
    import scratch_fixture as _SF        # coherent engine identities for the fixture's Guard 5
    _SF.install_sibling_support_trees(dst, REPO)   # ITEM 408 item 5: sibling trees (centralised)
    _SF.materialize_r14(dst, REPO)                 # ITEM 408 item 6: reconstruct the accepted R14 baseline
    return dst


def sp(scr):
    return os.path.join(scr, 'engine', 'rl_after', 'rl_model_data.json')


def live_state(scr):
    return {
        'store': md5(sp(scr)),
        'board': md5(os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json')),
        'manifest': md5(os.path.join(scr, 'data', 'expected_boot.json')),
        'ledger': md5(os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json')),
    }


def snapshot(scr, rnd=15, n=4):
    store = json.load(open(sp(scr)))
    active = [r for r in store if r.get('stable_player_id') and not r.get('_retired')][:n]
    body = "\n".join("%s,%s" % (r['player'], 88 + i * 9) for i, r in enumerate(active))
    ent = RE.RoundEntry(rnd, store_path=sp(scr))
    resolved, residue = ent.resolve_body(body)
    assert not residue
    return ent.build_snapshot(resolved, generated_at=GEN)


def arm():
    SI.APPLY_DEFAULT = True
    os.environ['INGEST_SCORE_APPLY'] = 'fv-proof-token'
    os.environ.setdefault('RL_VENDOR', '/home/claude/rl_vendor')


def disarm():
    SI.APPLY_DEFAULT = False
    os.environ.pop('INGEST_SCORE_APPLY', None)


def ledger_count(scr):
    return len(SA.load_ledger(os.path.join(scr, 'engine', 'rl_after', 'ingestion',
                                           'applied_rounds_ledger.json')).get('applied', []))


def last_txn(scr):
    root = os.path.join(scr, 'engine', 'rl_after', 'ingestion', SA.TXN_DIRNAME)
    if not os.path.isdir(root):
        return None
    ds = [os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
    if not ds:
        return None
    d = sorted(ds, key=os.path.getmtime)[-1]
    return json.load(open(os.path.join(d, 'manifest.json')))


def prove_green():
    scr = make_scratch('green')
    try:
        snap = snapshot(scr)
        res = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN)
        man = last_txn(scr)
        fv = (man or {}).get('fv_provenance') or {}
        dp_md5 = fv.get('distribution_pricing_md5', '')
        # the board is built in an isolated workspace (a repo-shaped tempdir); RL_FV is bound INSIDE
        # that workspace (inside_staged_repo=True). The FV module md5 is the true provenance signal.
        r = {
            'store_before': res.store_md5_before[:8], 'store_after': res.store_md5_after[:8],
            'board_after': res.board_md5_after[:8], 'guard5_green': res.guard5_green,
            'fv_inside_staged_repo': bool(fv.get('inside_staged_repo')),
            'fv_distribution_pricing_md5': dp_md5[:8],
            'fv_is_staged_not_stale': dp_md5.startswith('dd19a234'),
            'fv_not_21d530bf': not dp_md5.startswith('21d530bf'),
            'config_hash': (man or {}).get('config_hash', '')[:12],
            'config_gate_loaded': bool(fv.get('config_mode_gate_loaded')),
        }
        r['pass'] = all([res.guard5_green, r['fv_inside_staged_repo'], r['fv_is_staged_not_stale'],
                         r['fv_not_21d530bf'], r['config_gate_loaded'], bool(r['config_hash'])])
        return r
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def prove_red_guard():
    """R1: hand the provenance guard the ambient stale module -> HALT. Documents the real 21d530bf."""
    scr = make_scratch('rg')
    try:
        ap = SA.StagedRoundApplier.for_repo(scr)
        ambient_md5 = md5(os.path.join(AMBIENT_FV, 'distribution_pricing.py'))
        halted = False; msg = None
        try:
            ap._assert_fv_provenance(scr, {'RL_FV': AMBIENT_FV})
        except SA.FVProvenanceError as e:
            halted = True; msg = str(e).splitlines()[0]
        # also: unset RL_FV halts
        unset_halted = False
        try:
            ap._assert_fv_provenance(scr, {})
        except SA.FVProvenanceError:
            unset_halted = True
        return {'ambient_fv_path': AMBIENT_FV, 'ambient_distribution_pricing_md5': (ambient_md5 or '')[:8],
                'is_the_stale_21d530bf': (ambient_md5 or '').startswith('21d530bf'),
                'guard_halted_on_ambient': halted, 'guard_halted_on_unset': unset_halted,
                'first_line': msg, 'pass': halted and unset_halted}
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def prove_red_apply_halt():
    """R2: a full apply whose FV binding is mis-pointed at the ambient stale dir HALTS before board
    generation. No board, no pins, no ledger; live files byte-identical."""
    scr = make_scratch('rh')
    try:
        snap = snapshot(scr)
        before = live_state(scr)
        ap = SA.StagedRoundApplier.for_repo(scr)
        ap.fv_dir_override = AMBIENT_FV     # simulate a broken/adversarial FV binding
        halted = False
        try:
            ap.apply_snapshot(snap, generated_at=GEN)
        except SA.FVProvenanceError:
            halted = True
        after = live_state(scr)
        man = last_txn(scr)
        return {'halted_before_generation': halted, 'files_byte_identical': after == before,
                'board_unchanged': after['board'] == before['board'],
                'no_ledger_entry': ledger_count(scr) == 0,
                'txn_status': (man or {}).get('status'),
                'pass': halted and after == before and ledger_count(scr) == 0
                        and (man or {}).get('status') == SA.STATUS_ABORTED_PRECOMMIT}
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def prove_red_apply_override():
    """R3: an ADVERSARIAL inherited RL_FV=<ambient stale> is FORCED back to the staged module; the
    board built is the CORRECT staged dd19a234, and the apply commits. The stale board is never made."""
    scr = make_scratch('ro')
    prev = os.environ.get('RL_FV')
    try:
        os.environ['RL_FV'] = AMBIENT_FV          # adversarial inherited redirect (the defect condition)
        snap = snapshot(scr)
        res = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN)
        man = last_txn(scr)
        fv = (man or {}).get('fv_provenance') or {}
        dp_md5 = fv.get('distribution_pricing_md5', '')
        return {'committed': True, 'guard5_green': res.guard5_green,
                'fv_forced_to_staged': dp_md5.startswith('dd19a234'),
                'fv_not_ambient_stale': not dp_md5.startswith('21d530bf'),
                'fv_inside_staged_repo': bool(fv.get('inside_staged_repo')),
                'pass': res.guard5_green and dp_md5.startswith('dd19a234')
                        and bool(fv.get('inside_staged_repo'))}
    except Exception as e:
        return {'committed': False, 'error': '%s: %s' % (type(e).__name__, e), 'pass': False}
    finally:
        if prev is None:
            os.environ.pop('RL_FV', None)
        else:
            os.environ['RL_FV'] = prev
        shutil.rmtree(scr, ignore_errors=True)


def prove_config_conflict():
    """ITEM 2: an inherited conflicting valuation flag HALTS before any staging."""
    scr = make_scratch('cc')
    prev = os.environ.get('RL_LEGE')
    try:
        before = live_state(scr)
        os.environ['RL_LEGE'] = '0'         # a model-semantic flag that conflicts with the release manifest
        snap = snapshot(scr)
        halted = False; msg = None
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN)
        except SA.ConfigPolicyError as e:
            halted = True; msg = str(e).splitlines()[0]
        after = live_state(scr)
        return {'conflicting_flag': 'RL_LEGE=0', 'halted': halted, 'first_line': msg,
                'files_byte_identical': after == before,
                'pass': halted and after == before}
    finally:
        if prev is None:
            os.environ.pop('RL_LEGE', None)
        else:
            os.environ['RL_LEGE'] = prev
        shutil.rmtree(scr, ignore_errors=True)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args(argv[1:])
    t0 = time.time()
    run_id = os.environ.get('GITHUB_RUN_ID') or 'local-%s' % uuid.uuid4().hex
    report = {
        'proof_generated_at_epoch': t0,
        'proof_generated_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0)),
        'proof_run_id': run_id,
    }

    real_off = False
    try:
        SI.ScoreIngestor().apply(SI.ScoreIngestor().preview([]))
    except SI.IngestionGatedError:
        real_off = True
    report['gate_off_on_real_store'] = real_off
    print("[gate] real-store apply refused (gate OFF): %s" % real_off)

    arm()
    try:
        rg = prove_red_guard(); report['red_guard'] = rg
        print("[R1 guard] ambient FV md5=%s is_21d530bf=%s halted=%s => %s"
              % (rg['ambient_distribution_pricing_md5'], rg['is_the_stale_21d530bf'],
                 rg['guard_halted_on_ambient'], 'PASS' if rg['pass'] else 'FAIL'))

        cc = prove_config_conflict(); report['config_conflict'] = cc
        print("[cfg] inherited RL_LEGE=0 halted=%s files_unchanged=%s => %s"
              % (cc['halted'], cc['files_byte_identical'], 'PASS' if cc['pass'] else 'FAIL'))

        rh = prove_red_apply_halt(); report['red_apply_halt'] = rh
        print("[R2 apply-halt] halted=%s files_identical=%s no_ledger=%s status=%s => %s"
              % (rh['halted_before_generation'], rh['files_byte_identical'], rh['no_ledger_entry'],
                 rh['txn_status'], 'PASS' if rh['pass'] else 'FAIL'))

        gr = prove_green(); report['green'] = gr
        print("[green] store %s->%s board=%s guard5=%s fv=%s(staged=%s) gate=%s => %s"
              % (gr['store_before'], gr['store_after'], gr['board_after'], gr['guard5_green'],
                 gr['fv_distribution_pricing_md5'], gr['fv_is_staged_not_stale'], gr['config_gate_loaded'],
                 'PASS' if gr['pass'] else 'FAIL'))

        ro = prove_red_apply_override(); report['red_apply_override'] = ro
        print("[R3 override] adversarial RL_FV forced-to-staged=%s guard5=%s => %s"
              % (ro.get('fv_forced_to_staged'), ro.get('guard5_green'), 'PASS' if ro['pass'] else 'FAIL'))
    finally:
        disarm()

    report['elapsed_s'] = round(time.time() - t0, 1)
    all_pass = (real_off and report['red_guard']['pass'] and report['config_conflict']['pass']
                and report['red_apply_halt']['pass'] and report['green']['pass']
                and report['red_apply_override']['pass'])
    report['ALL_PASS'] = all_pass
    print("\n==== FV-PROVENANCE + CONFIG-POLICY PROOF: %s  (%.1fs) ===="
          % ('ALL PASS' if all_pass else 'FAIL', report['elapsed_s']))

    if args.write:
        out_json = os.path.join(HERE, 'fv_proof.json')
        out_md = os.path.join(HERE, 'FV_PROOF.md')
        for out in (out_json, out_md):
            try:
                os.remove(out)
            except FileNotFoundError:
                pass
        with open(out_json, 'x') as f:
            json.dump(report, f, indent=2, sort_keys=True)
        with open(out_md, 'x') as f:
            f.write(_md(report))
        print("wrote fv_proof.json + FV_PROOF.md")
    return 0 if all_pass else 1


def _md(r):
    g, rg, rh, ro, cc = (r['green'], r['red_guard'], r['red_apply_halt'],
                         r['red_apply_override'], r['config_conflict'])
    return "\n".join([
        "# FORWARD-VALUATION PROVENANCE + CONFIG-POLICY PROOF (gate OFF, scratch only)", "",
        "Writes nothing to the real store (gate OFF: real-store apply refused = `%s`)." % r['gate_off_on_real_store'],
        "", "## RESULT: **%s**  (%.1fs)\n\nGenerated at `%s` for proof run `%s`" % ('ALL PASS' if r['ALL_PASS'] else 'FAIL', r['elapsed_s'], r['proof_generated_at_utc'], r['proof_run_id']), "",
        "## RED — the audit's defect (stale `21d530bf` on the RL_FV default path)",
        "| check | value |", "|---|---|",
        "| ambient `%s` distribution_pricing md5 | `%s` |" % (rg['ambient_fv_path'], rg['ambient_distribution_pricing_md5']),
        "| that IS the stale `21d530bf` | %s |" % rg['is_the_stale_21d530bf'],
        "| R1: provenance guard HALTS on the ambient module | %s |" % rg['guard_halted_on_ambient'],
        "| R1: provenance guard HALTS on unset RL_FV | %s |" % rg['guard_halted_on_unset'],
        "| R2: full apply with FV mis-bound to ambient HALTS before generation | %s |" % rh['halted_before_generation'],
        "| R2: live files byte-identical, no ledger entry, txn `%s` | %s |" % (rh['txn_status'], rh['files_byte_identical'] and rh['no_ledger_entry']),
        "| R3: adversarial inherited RL_FV forced back to the staged module | %s |" % ro.get('fv_forced_to_staged'),
        "| R3: board built is the staged module, never the stale one | %s |" % ro.get('fv_not_ambient_stale'),
        "", "**The stale `d7a95e8d` board is never generated, pinned or committed.**",
        "", "## GREEN — staged strict build",
        "| check | value |", "|---|---|",
        "| store `%s` → `%s`, board `%s` | applied |" % (g['store_before'], g['store_after'], g['board_after']),
        "| distribution_pricing used (staged `dd19a234`, inside the staged repo) | `%s` / %s |" % (g['fv_distribution_pricing_md5'], g['fv_inside_staged_repo']),
        "| not the stale `21d530bf` | %s |" % g['fv_not_21d530bf'],
        "| RL_CONFIG_MODE=gate loaded the release manifest (config `%s`) | %s |" % (g['config_hash'], g['config_gate_loaded']),
        "| Guard 5 GREEN on the staged set | %s |" % g['guard5_green'],
        "", "## CONFIG POLICY (item 2)",
        "| check | value |", "|---|---|",
        "| inherited `%s` HALTS before any staging | %s |" % (cc['conflicting_flag'], cc['halted']),
        "| live files byte-identical | %s |" % cc['files_byte_identical'],
        "", "> Scratch-only, gate OFF. No numerical-determinism verdict is claimed; the FV binding "
        "guarantees the board is built from the STAGED valuation module, not an ambient/stale one.", ""])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
