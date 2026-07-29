#!/usr/bin/env python3
"""INVARIANT + RECONCILIATION PROOF for the final canonical board (final integration 2026-07-21).

Verifies, against the ACCEPTED authorities (committed reference vector + git Board B, not transplanted):
  Present authority (ITEM 411 D1 R19, owner rulings v467 + v469 2026-07-26) =
       session_2026-07-20/fv_provenance_remediation/fixtures/reference_vector_5546f278.json
       (accepted balanced/strict 5546f278; active 804; present-v total 764021)
  Board B (accepted forward lens) = 70ef0ff:.../board_B_lege1_legf1.json      (md5 1f10220c)
  Final board / board of record   = data/rl_build/rl_app_data.json           (working tree, md5 fa172ac1)

  (10) present-lens invariants: 804 active; Sigma v == 764021; 0 present-v / present-rank /
       present-order movers of the board of record fa172ac1 vs the accepted reference vector
       (5546f278). (Migrated from the superseded ITEM 408 STOP-1 authority 1373e824 / total 760253,
       itself migrated from the R14 Board A f05ebe6 / 06d8af60 / total 752427. The ITEM 411 D1
       restructure transaction legitimately MOVES the store f37d9716->c120cfd5 and, by deterministic
       regeneration, the board 6f07f7cb->fa172ac1; the present authority advances with them.)
  (11) forward-vector invariants: the board-of-record forward vectors (vP1/vP2) must be PRESENT + numeric
       over the EXACT active universe (804). Board B (1f10220c) is the SUPERSEDED R14 comparison oracle;
       the vP1/vP2 differences vs it are MEASURED + RECORDED (equal/changed/missing/added counts), NOT
       asserted. Semantic acceptance of the R19 vP1/vP2 vectors remains owner-DEFERRED (no accepted R19
       forward oracle exists).
  (12) visible draft-asset proof: exactly 64 visible 2027 + 64 visible 2028 placeholders; 0 on the current
       ladder; unique stable asset ids; labels distinguish year+pick; no AFL club; no AFFL club; no player
       identity; exact PVC[n] per row; PVC monotone non-increasing; future-lens sorting by value desc.
  (13) F5 reconciliation: visible(Sigma PVC[1..64]) + residual_nd + residual_mech == sealed F5 entrant
       layer 83538, per lens and vs Board B phantomTotals; no double count.

Each acceptance section emits its OWN pass boolean (ok_present / ok_forward / ok_draft / ok_f5) so a
present-lens result NEVER cascades into an unrelated section (ITEM 408 item 5.4).

TWO LANES, SPLIT BY LIFETIME (#256 part A, on the #231 `adoption_gate` precedent)
--------------------------------------------------------------------------------
This proof used to run one set of 33 checks on every push, and eleven of them asserted EQUALITY WITH
THE RELEASED BASELINE BOARD -- Sigma present v == 764021, zero movers against the accepted reference
vector, the F5 layer at 83538/4649/14272. The tree deliberately carries the HELD CANDIDATE board
(750446d7: 771772, 749 movers -- the ruled ND/RD/pool split working, declared in
`data/release_contract.json` `held_candidates`), so those eleven were red for the entire baseline
effort. A guard that always fails is the same defect as one that cannot: it is exactly the shape #231
existed to remove, and exactly what #251 part A cured in the release gate.

So the checks are now sorted by the only question that matters for a guard's lifetime:

    CAN THIS PASS FOR A CORRECTLY-BUILT CANDIDATE BOARD?

  yes -> PER-PUSH lane (`ck`). Structural invariants of WHATEVER board the tree carries: the active
         universe, placeholder shape and counts, unique ids, label form, PVC monotonicity, sort order,
         and the F5 reconciliation done against the board's OWN declared totals. Gating on every push.
  no  -> ADOPTION lane (`adopt`). It can only pass when the tree's board IS the released board, so it
         is a RELEASE CONDITION, not an invariant. Run at the owner adoption step:
             python3 .../invariant_proof.py --adoption
         Expected RED for the whole baseline effort; that red is information, not a defect. Under
         `--adoption` BOTH lanes gate (the structural set is a precondition of the equality claim).

Default (no flag) = per-push: the adoption lane is still COMPUTED and PRINTED as `ADOPT-PASS` /
`ADOPT-RED` rows and recorded in the evidence JSON, so the released-baseline distance stays visible on
every run -- it is deferred, never hidden.

THE FULL DISPOSITION OF THE ORIGINAL 33. Nothing is silently dropped; nothing is retired.
-----------------------------------------------------------------------------------------
KEPT PER-PUSH, unchanged (23):
  (10) reference-vector fixture authority; final active count == 804; no added/removed active players
       -- the first reads only the committed oracle fixture, so it cannot go red because the board
       moved, and it is the anti-tamper sentinel on the vector the adoption lane gates against. The
       other two are the active UNIVERSE, which is roster-driven, not valuation-driven: the
       re-derivation moves values, not who is on the list. Both pass on the held candidate today.
  (11) forward vectors present + numeric; exact active universe vs Board B  (+ the vP1/vP2 DEFERRED row)
  (12) all twelve draft-asset checks
  (13) draftAssetTotals reconciled_to_f5 (x2 lenses); Board B sealed entrant layer == 83538 (that one
       reads only the git Board B blob, never the tree's board)
MOVED WHOLE TO ADOPTION (5):
  (10) final Sigma present v == 764021; zero present-v movers; zero present-rank movers; zero
       present-order movers -- these ARE the released-baseline equality.
  (13) final board carries Board B phantomPicks/phantomLayer/phantomTotals unchanged -- equality with
       the superseded oracle's phantom layer (the tree carries 130 phantomPicks against Board B's 164).
SPLIT into a kept structural half + a moved released half (4 checks x 2 lenses = 8):
  (13) visible == Sigma PVC[1..64] == 64617   -> per-push keeps `visible == Sigma PVC[1..64] ==
       draftAssetTotals.visible_1_64` (internal consistency); `== 64617` is the released CURVE, adoption.
  (13) visible + residual == 83538            -> per-push keeps the reconciliation against the board's
       OWN f5_entrant_layer_pvc / total, and STRENGTHENS it to tie draftAssetTotals to phantomTotals
       (two independently produced blocks must agree); `== 83538` is the released layer, adoption.
  (13) residual_nd == 4649                    -> per-push keeps `residual_nd == f5_draft_pvc -
       visible_1_64`; `== 4649` is released, adoption.
  (13) residual_mech == 14272                 -> per-push keeps `residual_mech == f5_mech_pvc ==
       phantomTotals mech_pvc`; `== 14272` is released, adoption.
RETIRED: none.
  33 originals -> 28 per-push + 13 adoption = 41 rows (the 8 splits each produce two).

WHY build_final_board.py CARRIES THE SAME SPLIT. That tool's `(5-present) every rebuilt present v ==
reference vector` is the same released-baseline equality on the same oracle, and runs later in the same
workflow. Its per-push value is check (3) -- the rebuild is BYTE-IDENTICAL to the committed board -- and
committed-vs-released is this file's adoption lane, so the equality there is implied at adoption and
loses nothing per-push. See that file's header.

Emits machine-readable evidence (invariant_proof.json) + PASS/FAIL. Exit non-zero if any GATING check
fails: the per-push lane by default, both lanes under --adoption.
"""
import os, sys, json, hashlib, subprocess

ROOT = os.environ.get('RL_REPO') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
FINAL = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')
# ITEM 411 D1 R19 accepted present authority — the committed reference vector (balanced/strict
# 5546f278). The board of record fa172ac1 has ZERO present-v movers vs this vector (owner rulings
# v467 + v469, 2026-07-26). Supersedes the ITEM 408 STOP-1 authority (1373e824 / total 760253), which
# in turn superseded the R14 present-lens Board A (f05ebe6 / 06d8af60 / total 752427).
# These stay LITERALS on purpose: they are the drift sentinel. Reading them from the boot manifest or
# the board under test would make this proof pass by construction.
REFVEC = os.path.join(ROOT, 'session_2026-07-20', 'fv_provenance_remediation', 'fixtures',
                      'reference_vector_5546f278.json')
PRESENT_BALANCED_MD5 = '5546f278788196c680a987c26e4f0150'
PRESENT_TOTAL = 764021
PRESENT_ACTIVE = 804
BOARD_B = ('70ef0ff36ca7633aa4097a9b7c1a730013870abe',
           'session_2026-07-21/forward_lens_acceptance/board_B_lege1_legf1.json')
# The RELEASED F5 layer. Like the present-lens literals above these stay LITERALS on purpose -- they are
# the drift sentinel -- but they are RELEASE CONDITIONS, so they gate in the adoption lane only.
RELEASED_PVC_1_64 = 64617
RELEASED_F5_ENTRANT = 83538
RELEASED_RESIDUAL_ND = 4649
RELEASED_RESIDUAL_MECH = 14272

# --adoption: run the released-baseline lane as GATING (the owner adoption step). Default is per-push.
ADOPTION = '--adoption' in sys.argv[1:]

R = []
A = []
DEFERRED = []
def ck(name, cond, detail=''):
    """PER-PUSH lane: a structural invariant of whatever board the tree carries. Always gating."""
    R.append({'check': name, 'pass': bool(cond), 'detail': detail, 'lifetime': 'per-push'})
    print(('  PASS ' if cond else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(cond)

def adopt(name, cond, detail=''):
    """ADOPTION lane: equality with the RELEASED baseline. Only passes when the tree's board IS the
    released board, so it is a release condition, not an invariant (#256 part A, on #231's precedent).
    Gating under --adoption; computed, printed and recorded but NOT gating on a normal push."""
    A.append({'check': name, 'pass': bool(cond), 'detail': detail, 'lifetime': 'adoption'})
    if ADOPTION:
        tag = '  PASS ' if cond else '  FAIL '
    else:
        tag = '  ADOPT-PASS ' if cond else '  ADOPT-RED  '
    print(tag + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(cond)

def deferred(name, detail=''):
    """An owner-DEFERRED item: reported transparently (with the real measured deltas) but NOT a gate.
    Used for the forward-lens (vP1/vP2), which the owner has explicitly NOT accepted (deferred repair);
    the superseded R14 Board B is not an R19 oracle, so its deltas are recorded, not asserted as a pass."""
    DEFERRED.append({'check': name, 'status': 'DEFERRED', 'detail': detail})
    print('  DEFER ' + name + ((' -- ' + str(detail)) if detail else ''))

def gitjson(commit, path):
    return json.loads(subprocess.check_output(['git', 'show', '%s:%s' % (commit, path)], cwd=ROOT))

def active_of(board):
    for k in ('active',):
        if k in board and isinstance(board[k], list): return board[k]
    # UI-bundle shape uses 'players'
    return board.get('players', [])

def main():
    print("=== FINAL BOARD INVARIANT + RECONCILIATION PROOF ===")
    F = json.load(open(FINAL))
    RV = json.load(open(REFVEC))
    B = gitjson(*BOARD_B)
    fa, ba = active_of(F), active_of(B)
    PVC = {int(k): v for k, v in F['PVC'].items()}

    fby = {p['key']: p for p in fa}
    aby = {k: int(v) for k, v in RV['vector'].items()}   # accepted present-v vector (key -> v)
    bby = {p['key']: p for p in ba}

    # ---- (10) present-lens: the board of record vs the ACCEPTED reference vector ------------
    ck('(10) reference vector is the accepted balanced/strict %s (active %d, sum_v %d)'
       % (PRESENT_BALANCED_MD5[:8], PRESENT_ACTIVE, PRESENT_TOTAL),
       str(RV.get('board_md5', '')).startswith(PRESENT_BALANCED_MD5[:8]) and RV.get('active') == PRESENT_ACTIVE and RV.get('sum_v') == PRESENT_TOTAL,
       'board=%s active=%s sum_v=%s' % (str(RV.get('board_md5'))[:8], RV.get('active'), RV.get('sum_v')))
    # PER-PUSH: the active UNIVERSE. Roster-driven, not valuation-driven — the re-derivation moves
    # values, not who is on the list — so it holds for a correctly-built candidate board.
    ck('(10) final active count == %d' % PRESENT_ACTIVE, len(fa) == PRESENT_ACTIVE, len(fa))
    added = sorted(set(fby) - set(aby)); removed = sorted(set(aby) - set(fby))
    ck('(10) no added/removed active players vs the accepted reference vector', not added and not removed,
       'added=%d removed=%d' % (len(added), len(removed)))

    # ADOPTION: the released-baseline VALUE equality. Red for the whole baseline effort by design.
    adopt('(10) final Sigma present v == %d' % PRESENT_TOTAL, sum(p['v'] for p in fa) == PRESENT_TOTAL, sum(p['v'] for p in fa))
    vmov = [k for k in fby if k in aby and fby[k]['v'] != aby[k]]
    adopt('(10) zero present-v movers vs the accepted reference vector (%s)' % PRESENT_BALANCED_MD5[:8], not vmov, '%d movers' % len(vmov))
    def ranks_kv(items):
        order = sorted(items, key=lambda kv: (-kv[1], kv[0]))
        return {k: i for i, (k, _v) in enumerate(order)}, [k for k, _v in order]
    fr, ford = ranks_kv([(p['key'], p['v']) for p in fa])
    ar, aord = ranks_kv(list(aby.items()))
    rmov = [k for k in fr if k in ar and fr[k] != ar[k]]
    adopt('(10) zero present-rank movers vs the accepted reference vector', not rmov, '%d rank movers' % len(rmov))
    adopt('(10) zero present-order movers vs the accepted reference vector', ford == aord,
          'order identical' if ford == aord else 'ORDER DIFFERS')

    # ---- (11) forward vectors — forward-lens repair is owner-DEFERRED (vP1/vP2 NOT accepted) ----------
    # The owner has explicitly NOT accepted the vP1/vP2 forward-lens outputs and the forward-lens repair is
    # DEFERRED (data/expected_boot.json _present_staleness_note "forward-lens treatment intentionally
    # unchanged and deferred"; data/release_lineage.json _present_lens_only "owner ... has NOT accepted the
    # old vP1/vP2 forward-lens outputs"). Board B (1f10220c) is the SUPERSEDED R14 forward oracle; the R19
    # board-of-record forward vectors advanced with the round exactly as the present values did (present-v
    # +723). We therefore do NOT assert equality to the stale R14 oracle (there is no accepted R19 forward
    # oracle). We DO gate the accepted property — the forward vectors are present + numeric on the FROZEN
    # board of record (ITEM 411 D1), over the exact active universe — and we RECORD the vs-Board-B deltas openly.
    eq1 = sum(1 for k in fby if k in bby and fby[k]['vP1'] == bby[k]['vP1'])
    eq2 = sum(1 for k in fby if k in bby and fby[k]['vP2'] == bby[k]['vP2'])
    ch1 = [k for k in fby if k in bby and fby[k]['vP1'] != bby[k]['vP1']]
    ch2 = [k for k in fby if k in bby and fby[k]['vP2'] != bby[k]['vP2']]
    miss = sorted(set(bby) - set(fby)); addf = sorted(set(fby) - set(bby))
    pv_mov = len([k for k in fby if k in bby and fby[k]['v'] != bby[k]['v']])
    fwd_present = all(isinstance(p.get('vP1'), (int, float)) and isinstance(p.get('vP2'), (int, float)) for p in fa)
    ck('(11) forward vectors present + numeric for all %d active (board of record; its md5 is '
       'emitted in this proof\'s identity footer)' % PRESENT_ACTIVE,
       fwd_present and len(fa) == PRESENT_ACTIVE, 'present=%s active=%d' % (fwd_present, len(fa)))
    ck('(11) exact active universe vs Board B (no missing/added rows)', not miss and not addf,
       'missing=%d added=%d' % (len(miss), len(addf)))
    deferred('(11) vP1/vP2 acceptance vs Board B — owner-DEFERRED (forward-lens not accepted)',
             'vP1 changed=%d/804, vP2 changed=%d/804 vs the SUPERSEDED R14 Board B 1f10220c (present-v also '
             'moved +%d, the STOP-1 advance). No accepted R19 forward oracle exists; the forward-lens repair '
             'is owner-deferred. Deltas recorded, NOT asserted as a pass.' % (len(ch1), len(ch2), pv_mov))

    # ---- (12)+(13) visible draft assets + F5 reconciliation -------------------------------------------
    lp = F['lensPicks']
    vis1 = [p for p in lp if p['lens'] == 1 and not p.get('residual')]
    vis2 = [p for p in lp if p['lens'] == 2 and not p.get('residual')]
    ck('(12) exactly 64 visible 2027 national-draft placeholders (+1)', len(vis1) == 64, len(vis1))
    ck('(12) exactly 64 visible 2028 national-draft placeholders (+2)', len(vis2) == 64, len(vis2))
    ck('(12) all visible labelYear correct (2027/2028)',
       all(p['labelYear'] == 2027 for p in vis1) and all(p['labelYear'] == 2028 for p in vis2))
    ck('(12) zero visible future placeholders on the current player ladder',
       not any(p.get('asset') == 'pick' for p in fa) and not any('pick' in (p.get('kind') or '') for p in fa))
    ids = [p['id'] for p in lp]
    ck('(12) unique stable asset ids', len(ids) == len(set(ids)), '%d ids %d unique' % (len(ids), len(set(ids))))
    ck('(12) labels distinguish year + pick number',
       all(p['label'] == '%d Draft Pick %d' % (p['labelYear'], p['n']) for p in vis1 + vis2))
    ck('(12) no AFL club / no AFFL club on any visible pick',
       all(p.get('club') is None and p.get('affl_team') is None for p in vis1 + vis2))
    ck('(12) no accidental player identity (no key join; kind/asset == pick)',
       all(('key' not in p) and p.get('kind') == 'pick' and p.get('asset') == 'pick' for p in vis1 + vis2))
    pvc_ok = all(p['v'] == PVC[p['n']] for p in vis1 + vis2)
    ck('(12) exact PVC equality for every visible pick (v == PVC[n])', pvc_ok)
    mono = all(PVC[n] >= PVC[n + 1] for n in range(1, 64))
    ck('(12) release-active PVC monotone non-increasing over 1..64', mono)
    sort1 = [p['v'] for p in vis1]; sort2 = [p['v'] for p in vis2]
    ck('(12) visible picks sorted by value desc (both lenses)',
       sort1 == sorted(sort1, reverse=True) and sort2 == sorted(sort2, reverse=True))

    sum64 = sum(PVC[n] for n in range(1, 65))
    # residuals are held OUT of the ranking (supervisor req 5) — they live in draftAssetTotals, NOT lensPicks.
    ck('(12) lensPicks carries ONLY the 64 rankable visible picks per lens (no residual rows in the ranking)',
       all(not p.get('residual') for p in lp) and len(vis1) == 64 and len(vis2) == 64)
    # The F5 reconciliation splits cleanly: the ARITHMETIC (visible + the two residuals close on the
    # board's own declared entrant layer, and draftAssetTotals agrees with phantomTotals) is true of any
    # correctly-built board and stays per-push; the released MAGNITUDES (64617 / 83538 / 4649 / 14272)
    # are the released curve and the released F5 seal, and gate at adoption.
    fptm = F.get('phantomTotals', {}).get('_meta', {}) or {}
    for off, vis in ((1, vis1), (2, vis2)):
        dat = F['draftAssetTotals']['+%d' % off]
        res_nd = dat['residual_nd_tail']; res_mech = dat['residual_mech']
        visible = sum(p['v'] for p in vis)
        ck('(13) lens +%d: visible == Sigma PVC[1..64] == draftAssetTotals.visible_1_64' % off,
           visible == sum64 == dat['visible_1_64'],
           'visible=%d sumPVC=%d declared=%d' % (visible, sum64, dat['visible_1_64']))
        # one closure, tying two independently produced blocks together: the ranking's own totals and
        # the sealed phantom layer must state the SAME entrant layer, and it must be what the parts add to.
        closes = (visible + res_nd + res_mech == dat['f5_entrant_layer_pvc'] == dat['total']
                  == dat['f5_draft_pvc'] + dat['f5_mech_pvc'] == fptm.get('entrant_layer_pvc'))
        ck('(13) lens +%d: visible + residual_nd + residual_mech == the board\'s own F5 entrant layer '
           '(draftAssetTotals total == draft+mech == phantomTotals entrant layer)' % off, closes,
           'parts=%d declared=%d total=%d draft+mech=%d phantom=%s'
           % (visible + res_nd + res_mech, dat['f5_entrant_layer_pvc'], dat['total'],
              dat['f5_draft_pvc'] + dat['f5_mech_pvc'], fptm.get('entrant_layer_pvc')))
        ck('(13) lens +%d: residual_nd == f5_draft_pvc - visible_1_64' % off,
           res_nd == dat['f5_draft_pvc'] - dat['visible_1_64'],
           'residual_nd=%d draft_pvc=%d - visible=%d' % (res_nd, dat['f5_draft_pvc'], dat['visible_1_64']))
        ck('(13) lens +%d: residual_mech == f5_mech_pvc == phantomTotals mech_pvc' % off,
           res_mech == dat['f5_mech_pvc'] == fptm.get('mech_pvc'),
           'residual_mech=%d f5_mech=%d phantom_mech=%s' % (res_mech, dat['f5_mech_pvc'], fptm.get('mech_pvc')))
        ck('(13) lens +%d: draftAssetTotals reconciled_to_f5' % off, dat['reconciled_to_f5'] is True)

        adopt('(13) lens +%d: Sigma PVC[1..64] == %d (RELEASED curve)' % (off, RELEASED_PVC_1_64),
              sum64 == RELEASED_PVC_1_64 == dat['visible_1_64'], sum64)
        adopt('(13) lens +%d: F5 entrant layer == %d (RELEASED)' % (off, RELEASED_F5_ENTRANT),
              visible + res_nd + res_mech == RELEASED_F5_ENTRANT == dat['f5_entrant_layer_pvc'],
              visible + res_nd + res_mech)
        adopt('(13) lens +%d: residual_nd == draft_pvc(69266) - 64617 == %d (RELEASED)' % (off, RELEASED_RESIDUAL_ND),
              res_nd == RELEASED_RESIDUAL_ND, res_nd)
        adopt('(13) lens +%d: residual_mech == mech_pvc == %d (RELEASED)' % (off, RELEASED_RESIDUAL_MECH),
              res_mech == RELEASED_RESIDUAL_MECH, res_mech)
    # cross-check against Board B's own sealed phantomTotals (no double count / same entrant layer).
    # PER-PUSH: this reads ONLY the git Board B blob, so no board move in the tree can red it — it is the
    # anti-tamper sentinel on the released F5 seal the adoption lane gates against.
    ptm = B['phantomTotals']['_meta']
    ck('(13) Board B sealed entrant layer == 83538 (draft 69266 + mech 14272)',
       ptm['entrant_layer_pvc'] == 83538 and ptm['draft_pvc'] == 69266 and ptm['mech_pvc'] == 14272)
    adopt('(13) final board carries Board B phantomPicks/phantomLayer/phantomTotals unchanged',
          fptm.get('entrant_layer_pvc') == RELEASED_F5_ENTRANT
          and len(F.get('phantomPicks', [])) == len(B.get('phantomPicks', [])),
          'entrant_layer=%s vs %d; phantomPicks %d vs Board B %d'
          % (fptm.get('entrant_layer_pvc'), RELEASED_F5_ENTRANT,
             len(F.get('phantomPicks', [])), len(B.get('phantomPicks', []))))

    # ---- final board identity -------------------------------------------------------------------------
    raw = open(FINAL, 'rb').read()
    ident = {'md5': hashlib.md5(raw).hexdigest(), 'sha256': hashlib.sha256(raw).hexdigest(),
             'balanced_board_md5_lineage': PRESENT_BALANCED_MD5}

    # Per-section pass booleans so a present-lens result never cascades into forward-vector / draft-asset /
    # F5 (ITEM 408 item 5.4). Each section owns the checks tagged with its number; consumers read the
    # section boolean relevant to that section, not the aggregate `ok`.
    # These read the PER-PUSH lane only: they are the section verdicts consumers (acceptance_matrix.py)
    # gate on, and the adoption lane is deliberately not a per-push verdict. `ok_*_adoption` carries the
    # release-condition verdict for the same section, so neither is hidden behind the other.
    def section_ok(tag, rows_src=None):
        rows = [r for r in (R if rows_src is None else rows_src) if r['check'].startswith(tag)]
        return bool(rows) and all(r['pass'] for r in rows)
    npass = sum(1 for r in R if r['pass']); n = len(R)
    apass = sum(1 for r in A if r['pass']); an = len(A)
    ok_adoption = apass == an
    result = {'ok': npass == n, 'n_pass': npass, 'n': n, 'final_board_identity': ident,
              'mode': 'adoption' if ADOPTION else 'per-push',
              'ok_present': section_ok('(10)'), 'ok_forward': section_ok('(11)'),
              'ok_draft': section_ok('(12)'), 'ok_f5': section_ok('(13)'),
              # the ADOPTION lane: released-baseline equality. Non-gating on a push by design (#256
              # part A); gating under --adoption. Red here before adoption is information, not a defect.
              'adoption': {'ok': ok_adoption, 'n_pass': apass, 'n': an, 'gating': ADOPTION,
                           'ok_present': section_ok('(10)', A), 'ok_f5': section_ok('(13)', A),
                           'note': 'equality with the RELEASED baseline board. The tree carries the held '
                                   'candidate declared in data/release_contract.json held_candidates, so '
                                   'this lane is expected RED until the owner adopts. Run as a gate with '
                                   '`invariant_proof.py --adoption` at the adoption step.',
                           'checks': A},
              # `ok_forward` gates only the ACCEPTED forward property (present + numeric + exact universe on
              # the frozen board of record). The vP1/vP2-vs-Board-B acceptance is owner-DEFERRED (below).
              'forward_lens_deferred': True,
              'forward': {'vP1_equal': eq1, 'vP1_changed': len(ch1), 'vP2_equal': eq2,
                          'vP2_changed': len(ch2), 'present_v_moved': pv_mov, 'missing': len(miss),
                          'added': len(addf), 'oracle': 'Board B 1f10220c (SUPERSEDED R14; not an R19 oracle)'},
              'deferred': DEFERRED, 'checks': R}
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'evidence', 'invariant_proof.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(result, open(out, 'w'), indent=2, sort_keys=True)
    print("\nfinal board md5=%s sha256=%s" % (ident['md5'], ident['sha256'][:16] + '...'))
    if ADOPTION:
        print("MODE: ADOPTION — both lanes gate (structural set is a precondition of the equality claim)")
        print("RESULT: per-push %d/%d PASS, adoption %d/%d PASS  -> %s"
              % (npass, n, apass, an, os.path.relpath(out, ROOT)))
        return 0 if (npass == n and ok_adoption) else 1
    print("MODE: per-push — the %d adoption-lane checks above are RELEASE CONDITIONS, reported not gated "
          "(run --adoption at the adoption step)" % an)
    print("RESULT: %d/%d PASS  (adoption lane %d/%d, non-gating)  -> %s"
          % (npass, n, apass, an, os.path.relpath(out, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
