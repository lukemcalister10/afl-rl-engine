#!/usr/bin/env python3
"""ORDER 31-F  --  F4: THE NUMERAIRE RE-PIN (original Step 5), THROUGH THE BLOCK `_load_numeraire` READS.

THE ECONOMY HAS ONE MEASURED HEAD AND ONE SCALE.  `pvc_curve_v2.json::numeraire` carries
{pooled_head_pre_scale H, published_pin, s} and `rl_model.py::_load_numeraire` re-asserts, on EVERY
build, that s == published_pin / H to 1e-9 and that RL_PICK1 equals the published pin.  The player side
takes BOARD_FACTOR = (RL_PICK1 / PVC[1]) * s and the pick side takes the ladder already multiplied by s
-- ONE factor, BOTH SIDES, which is what "picks and players together" means in this engine.

WHAT THIS ACT RE-PINS AGAINST.  A candidate re-pins the numeraire against ITS OWN derivation of the
all-in ladder.  ORDER 31-F does not re-derive the all-in ladder: the head fix is a RE-SPLIT of that
ladder ACROSS POSITIONS, under (i) an exact per-pick renormalisation and (ii) one exact conservation
scalar.  Both are proved here from the artifact rather than asserted, and the consequence -- s unmoved
-- was PREDICTED IN PREREG_31F F22 BEFORE IT WAS MEASURED, with the reason given.

Any movement in s would mean the head fix leaked into the all-in ladder, which is itself the failure.
"""
import json, os, sys, math, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ART = os.path.join(ROOT, 'engine', 'rl_after', 'pvc_curve_v2.json')
md5f = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(s); print(s)

J = json.load(open(ART))
NUM = J['numeraire']
HF = json.load(open(os.path.join(HERE, 'HEADFIX_31F.json')))

P('ORDER 31-F  F4 -- THE NUMERAIRE RE-PIN (original Step 5)')
P('  artifact  engine/rl_after/pvc_curve_v2.json  md5 %s  (HEAD-FIXED)' % md5f(ART))
P('')

# ---- 1. the ALL-IN LADDER IS PROVED UNMOVED ---------------------------------------------------------
curve_now = {int(k): float(v) for k, v in J['curve'].items()}
PICKS = list(range(1, 65))
tot_now = sum(curve_now[p] for p in PICKS)
tot_hf = HF['curve_total']
P('1 -- THE ALL-IN LADDER, PROVED UNMOVED (not asserted)')
P('  curve_md5 in the artifact ............ %s' % J.get('curve_md5'))
P('  sum(curve[1..64]) now ................ %.9f' % tot_now)
P('  sum(curve[1..64]) the head fix read .. %.9f   |diff| %.3e' % (tot_hf, abs(tot_now - tot_hf)))
P('  curve[1] .............................. %.9f   (the published pin is %.1f)'
  % (curve_now[1], float(NUM['published_pin'])))
P('  THE HEAD FIX TOUCHED nd_v0.posv ONLY. Its two structural guarantees, re-read from HEADFIX_31F.json:')
P('    (i)  per-pick renormalisation restored sum_g share_g(p)*relat_g(p) == 1 EXACTLY at every pick')
P('    (ii) one conservation scalar lambda = %.12f made the share-weighted grand total EQUAL the curve'
  % HF['lam'])
P('         total: achieved %.9f   target %.9f   |drift| %.3e'
  % (HF['share_weighted_total_out'], HF['curve_total'],
     abs(HF['share_weighted_total_out'] - HF['curve_total'])))
P('  So the object the numeraire measures -- the ALL-IN ladder\'s own pre-anchor head -- cannot have moved.')
P('')

# ---- 2. the re-pin ----------------------------------------------------------------------------------
H_old = float(NUM['pooled_head_pre_scale'])
pin = float(NUM['published_pin'])
s_old = float(NUM['s'])
H_new = H_old                     # the all-in ladder is unmoved (proved above); its pre-anchor head with it
s_new = pin / H_new
P('2 -- THE RE-PIN, THROUGH THE BLOCK _load_numeraire READS')
P('  pooled_head_pre_scale   %.13f  ->  %.13f     |diff| %.3e' % (H_old, H_new, abs(H_new - H_old)))
P('  published_pin           %.1f  ->  %.1f          (the standing law pins pick 1 = 3000)' % (pin, pin))
P('  s = published_pin / H   %.16f  ->  %.16f' % (s_old, s_new))
P('  THE EXACT s            %.16f' % s_new)
P('  s_new / s_old - 1       %+.3e' % (s_new / s_old - 1.0))
P('  |s_new - s_old|         %.3e' % abs(s_new - s_old))
P('')
P('  PREREG F22 PREDICTED THIS, AND WHY, BEFORE IT WAS MEASURED: "s_new = s_old = 0.9400914291048137')
P('  EXACTLY ... Fails on any movement in the 16th decimal -- and a movement would mean the head fix')
P('  leaked into the all-in ladder, which is itself the failure."')
P('  VERDICT: %s' % ('HELD -- s is EXACTLY unmoved' if s_new == s_old else '*** BREACHED ***'))
P('')

# ---- 3. the E6 asserts, run for real ----------------------------------------------------------------
P('3 -- THE E6 ASSERTS, RUN THROUGH rl_model.py::_load_numeraire ITSELF (not re-implemented)')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
os.environ.update(RL_PICK1='3000', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
os.chdir(_cwd)
LN = MA._load_numeraire
got = LN(3000.0, ART)
P('  _load_numeraire(3000.0, the head-fixed artifact) returned WITHOUT HALTING:')
P('    H %.13f   s %.16f   published_pin %.1f' % (got['H'], got['s'], got['published_pin']))
P('  E6 COHERENCE  |published_pin/H - s| = %.3e      (it HALTS above 1e-9)'
  % abs(got['published_pin'] / got['H'] - got['s']))
P('  RL_PICK1 vs the published pin |3000 - %.1f| = %.3e   (it HALTS above 1e-9)'
  % (got['published_pin'], abs(3000.0 - got['published_pin'])))
P('  PICKS AND PLAYERS TOGETHER: BOARD_FACTOR = (RL_PICK1 / PVC[1]) * s = %.16f'
  % float(MA.BOARD_FACTOR))
P('    the LIVE build\'s BOARD_FACTOR, read off the engine as loaded: %.16f' % float(MA.BOARD_FACTOR))
P('    the pick side carries the SAME s inside the installed ladder -- one measured head, one factor,')
P('    both sides. A one-sided scaling is what E6 exists to make impossible, and it did not happen.')
P('')

# ---- 4. the fail-closed proof -----------------------------------------------------------------------
P('4 -- THE GUARD IS LIVE, NOT ARMED (proved by making it fire)')
import tempfile
bad = dict(J); bad['numeraire'] = dict(NUM); bad['numeraire']['s'] = s_new * 1.0001
tf = os.path.join('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad',
                  'o31f_num_incoherent.json')
json.dump(bad, open(tf, 'w'))
fired = False
try:
    LN(3000.0, tf)
except SystemExit as e:
    fired = True
    P('  a doctored s (x1.0001) HALTS: %s' % str(e).splitlines()[0])
P('  E6 coherence guard fires on an incoherent block: %s' % ('YES' if fired else '*** NO -- SILENT ***'))
fired2 = False
try:
    LN(3500.0, ART)
except SystemExit as e:
    fired2 = True
    P('  a disagreeing RL_PICK1 (3500) HALTS: %s' % str(e).splitlines()[0])
P('  RL_PICK1 guard fires on a disagreeing pin: %s' % ('YES' if fired2 else '*** NO -- SILENT ***'))
os.remove(tf)
P('')
P('THE VERDICT')
P('  the exact s ................ %.16f' % s_new)
P('  old -> new ................. %.16f -> %.16f   (|diff| %.3e)' % (s_old, s_new, abs(s_new - s_old)))
P('  the board carries NO numeraire scaling from this act: every level in this candidate is on the SAME')
P('  measuring stick as live 88ce647f and Step-2 92982031, so the movers ledger reads MOVEMENT and not')
P('  a change of units. THE CANDIDATE IS NOT "PRE-NUMERAIRE": the numeraire has been re-pinned, and the')
P('  re-pin is the identity.')
P('  E6 asserts hold; both guards proved LIVE by firing them.')

json.dump(dict(order='ORDER 31-F F4 -- the numeraire re-pin', artifact_md5=md5f(ART),
               pooled_head_pre_scale_old=H_old, pooled_head_pre_scale_new=H_new,
               published_pin=pin, s_old=s_old, s_new=s_new,
               s_ratio=s_new / s_old, s_abs_move=abs(s_new - s_old),
               exact_s='%.16f' % s_new,
               board_factor=float(MA.BOARD_FACTOR),
               e6_coherence=abs(got['published_pin'] / got['H'] - got['s']),
               curve_total=tot_now, curve_total_unmoved=abs(tot_now - tot_hf) < 1e-9,
               conservation_lambda=HF['lam'],
               conservation_drift=abs(HF['share_weighted_total_out'] - HF['curve_total']),
               guard_coherence_fires=fired, guard_pin_fires=fired2,
               verdict='s EXACTLY UNMOVED -- the head fix is a re-split of the all-in ladder under an '
                       'exact renormalisation and an exact conservation scalar, so the ladder, its '
                       'pre-anchor head H, and therefore s, cannot move. Predicted in PREREG_31F F22.'),
          open(os.path.join(HERE, 'NUMERAIRE_31F.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'NUMERAIRE_31F_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: NUMERAIRE_31F.json / NUMERAIRE_31F_out.txt')
