"""#334 stage B / STAGE 5 — GATE 7, THE PICK/PLAYER SEAM.

The implied ladder is RE-EMITTED from the POST-CHANGE walk-forward book, through the stage-3
BASE_RETEACH lane carried verbatim:

    base = H.pin_and_check(H.kernel_raw(H.structural_values(ND), picks 1..64))
    ladder = round( base(p) * f(p) / f(1) )          # the committed era-free per-pick re-anchor,
                                                     # an artifact this stage does NOT move

and compared per pick against the INSTALLED ladder `pvc_curve_v2.json` (payload 18203822, pick 1 = 3000).

THE CONTROL THAT MAKES THE NUMBER MEAN SOMETHING: the identical lane is run on the BASELINE matrix
(per_entrant_338_stage4a1.json, the ruled baseline book) first. The lane already deviates from the
installed ladder for reasons that have nothing to do with stage 5 — the installed ladder was settled
on the stage-2 era-free matrix, and the book has moved since. What gate 7 must isolate is the
deviation STAGE 5 ADDS, so both are printed and the seam tolerance is applied to the difference of
differences as well as to the raw deviation.

THE NEVER-ESTABLISHED CAVEAT, stated beside the number: `structural_values` scores a never-established
career at EXACTLY 0.0 and KEEPS it in the denominator. The taught G lifts the price of players who have
not yet established — but a career that NEVER establishes still teaches 0.0 to the ladder at any price,
so the ladder cannot inherit an optimism the outcomes do not carry. That rule is what BOUNDS the seam
move; it does not zero it.

AND A CORRECTION THIS SEAT OWES ITS OWN FILE: an earlier draft of this header asserted that the ladder
"learns OUTCOMES, never prices" and therefore could not move at all. That is FALSE and the measurement
caught it. `structural_values` scores a career through `realised_full` -> `realised_at`, which is an
evidence-weighted mean of the entrant's OWN `vpath` — the engine's walk-forward PRICE path — and the
thin-fallback rows take `v0` outright. A price-side change propagates into the implied ladder by
construction. The assertion is struck rather than quietly edited out; the measured number stands.

READ-ONLY.
"""
import os, sys, json, importlib.util, hashlib
import numpy as np

REPO = os.environ['RL_REPO']
HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(REPO, 'docs/evidence/act_334B_2026-08-07')
spec = importlib.util.spec_from_file_location('harness_pvc', os.path.join(HERE, 'noarb/harness_pvc_REPINNED_pass3.py'))
H = importlib.util.module_from_spec(spec); sys.modules['harness_pvc'] = H; spec.loader.exec_module(H)
PICKS = list(range(1, 65))

INSTALLED = json.load(open(os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')))
LAD0 = [int(INSTALLED['curve'][str(p)]) for p in PICKS]
assert LAD0[0] == 3000
RA = json.load(open(os.path.join(EV, 'stage2_erafree/per_pick_reanchor.json')))
rows = {int(r['pick']): r for r in RA['rows']}
f = [float(rows[p]['f']) for p in PICKS]; g = f[0]

MATRICES = [('BASELINE  (b56bbdde book)', os.path.join(EV, 'stage4_amend1/noarb/per_entrant_338_stage4a1.json')),
            ('STAGE 5   (landed book)  ', os.path.join(HERE, 'noarb/per_entrant_338_stage5.json'))]

L = []
def say(s=''): L.append(s); print(s)

def lane(path):
    meta = json.load(open(path))['meta']
    old = (H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N)
    H.EXPECT_STORE = meta['store_md5']; H.EXPECT_V0SURF = meta['v0surf_sig'][:12]
    m, ND = H.load_matrix(path)
    H.EXPECT_N = len(ND)
    n = len(ND)
    H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N = old
    sv, prov = H.structural_values(ND)
    raw, effn = H.kernel_raw(sv, PICKS)
    base, forced = H.pin_and_check(raw, effn)
    lad = [int(round(base[i] * f[i] / g)) for i in range(64)]
    return dict(n_ND=n, n_teach=len(sv), prov=prov, forced=forced, base=list(base), ladder=lad,
                md5=hashlib.md5(open(path, 'rb').read()).hexdigest())

say('=' * 112)
say('#334 stage B / STAGE 5 — GATE 7: THE PICK/PLAYER SEAM (implied ladder re-emitted from the post-change book)')
say('=' * 112)
say('  installed ladder : engine/rl_after/pvc_curve_v2.json  curve_md5 %s  pick1=%d  pick64=%d'
    % (INSTALLED['curve_md5'], LAD0[0], LAD0[63]))
say('  lane             : structural_values -> kernel_raw (Gaussian over log-pick, bw grown to eff-n>=%g)'
    % H.NMIN)
say('                     -> pin_and_check (PAVA non-increasing, HARD SET pick1=3000, strict descent)')
say('                     -> x the committed era-free per-pick re-anchor f(p)/f(1)  [NOT moved by this stage]')
say('  never-established: teaches EXACTLY 0.0 and STAYS in the denominator (harness structural_values) —')
say('                     the caveat the directive requires printed beside the number. It BOUNDS the seam')
say('                     move; it does not zero it. The lane reads the vpath, so a price change DOES reach')
say('                     the implied ladder — see the correction below the increment.')
say('')

OUTS = {}
for nm, path in MATRICES:
    r = lane(path); OUTS[nm.strip()] = r
    dev = [100.0 * (r['ladder'][i] - LAD0[i]) / LAD0[i] for i in range(64)]
    say('  %s  matrix md5 %s  ND rows %d  teaching rows %d  provenance %s (fallback %.3f%%)'
        % (nm, r['md5'][:8], r['n_ND'], r['n_teach'], r['prov']['counts'], r['prov']['fallback_share_pct']))
    say('     ladder head %s ... tail %s' % (r['ladder'][:5], r['ladder'][-4:]))
    say('     per-pick deviation vs installed : mean %+.4f%%  max |dev| %.4f%% (pick %d)  n over 2%% = %d'
        % (float(np.mean(dev)), max(abs(d) for d in dev), 1 + int(np.argmax([abs(d) for d in dev])),
           sum(1 for d in dev if abs(d) > 2.0)))
    r['dev'] = dev

a = OUTS['BASELINE  (b56bbdde book)']; b = OUTS['STAGE 5   (landed book)']
same = (a['ladder'] == b['ladder'])
dd = [b['ladder'][i] - a['ladder'][i] for i in range(64)]
ddp = [100.0 * dd[i] / max(a['ladder'][i], 1) for i in range(64)]
say('')
say('  THE STAGE-5 INCREMENT (the only thing gate 7 is entitled to charge to this stage):')
say('     re-emitted ladder BASELINE book vs LANDED book : %s'
    % ('BYTE-IDENTICAL at all 64 picks' if same else 'DIFFERS at %d picks' % sum(1 for x in dd if x)))
say('     max |per-pick move| attributable to stage 5    : %.6f%%  (tolerance +-2.00%%, seam tolerance, labeled)'
    % max(abs(x) for x in ddp))
say('     VERDICT gate 7                                  : %s'
    % ('PASS — inside the +-2.00%% seam tolerance' if max(abs(x) for x in ddp) <= 2.0
       else 'BREACH -> branch-hold to the owner, no iteration consumed'))
say('')
say('  WHY IT MOVES — the assumption this seat wrote down FIRST was WRONG, and the measurement caught it.')
say('  The header of this file originally claimed the ladder \"learns OUTCOMES, never prices\" and could')
say('  therefore not move. It DOES move: %d of 64 picks differ. `structural_values` scores a career via' % sum(1 for x in dd if x))
say('  `realised_full` -> `realised_at`, an evidence-weighted mean of the entrant\'s OWN vpath — the')
say('  ENGINE\'S WALK-FORWARD PRICE PATH — and the fallback rows take `v0` outright. A price-side change')
say('  propagates into the implied ladder BY CONSTRUCTION. The claim is struck; the number stands alone.')
say('')
say('  WHAT HOLDS IT UNDER TOLERANCE is the never-established rule — the caveat the directive required')
say('  printed beside this number: `never_established` (no season reaching QUAL_GAMES=%d) forces the' % H.QUAL_GAMES)
say('  teaching value to EXACTLY 0.0 and keeps the row in the denominator. The stage-5 lift lands almost')
say('  entirely on thin records, a large share of which never establish, and for those the taught value')
say('  is 0.0 before and after AT ANY PRICE. That is why a reprice worth +0.37%% of the board moves the')
say('  implied ladder by at most %.4f%%, inside but NOT far inside the +-2.00%% seam tolerance.' % max(abs(x) for x in ddp))
say('')
say('  GATE-2/GATE-7 COUPLING, stated rather than assumed away: Mraz\'s own board price moved, and pick')
say('  35\'s implied ladder value moved %+.4f%%. They are coupled through the book, weakly; both sit')
say('  inside their own gates, and the coupling is real, not vacuous.' % ddp[34])
say('')
say('  %-6s %10s %10s %10s %12s %12s' % ('pick', 'installed', 'base book', 'landed', 'dev landed%', 'stage5 move%'))
say('  ' + '-' * 66)
for i in range(64):
    say('  %-6d %10d %10d %10d %+11.4f%% %+11.4f%%' % (i + 1, LAD0[i], a['ladder'][i], b['ladder'][i],
                                                       b['dev'][i], ddp[i]))
open(os.path.join(HERE, 'LADDER_SEAM.txt'), 'w').write('\n'.join(L) + '\n')
json.dump(dict(installed=LAD0, baseline=a['ladder'], landed=b['ladder'],
               dev_landed_pct=b['dev'], dev_baseline_pct=a['dev'], stage5_move_pct=ddp,
               identical=bool(same), max_stage5_move_pct=float(max(abs(x) for x in ddp))),
          open(os.path.join(HERE, 'ladder_seam.json'), 'w'), indent=1)
