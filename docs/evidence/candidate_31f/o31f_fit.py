#!/usr/bin/env python3
"""ORDER 31-F  --  F1(e): THE ONE LAW's FITTED OBJECTS, RE-FITTED ON THE HEAD-FIXED RULER.  READ-ONLY.

    price(p,Y) = rho(g) * Phat  +  [ D(c_u)*(1-rho(g)) + Phi(g,s)*beta_mono(g)*rho(g) ] * V0

Every input object has been re-measured against the head-fixed v0 surface under R1 ruler discipline:

    D(c)        FADE_31F.json      (o30a2_recut.py, whole, output dir re-pointed only)
    backbone    FADE_31F.json      (the same run's T4 cumulative "<= k games by depth 2")
    beta(g)     BETA_31F.json      (o30bm_measure.py, whole, v0 source re-pointed)
    beta_stall  PHI_31F.json       (o30bc_circ.py,   whole, v0 source re-pointed)

THE FIT ITSELF IS NOT RE-IMPLEMENTED.  `o31_fit.py`'s computational core -- the monotone projection, the
log-linear interpolation, PhiStall, the exact rho targets, the Nelder-Mead fit, pi, and EVERY ONE of its
declared checks -- is LIFTED BY SOURCE TEXT and exec'd VERBATIM against the re-measured inputs.  The
lifted text is md5'd and printed.  Only the INPUTS change; not one line of the arithmetic.
"""
import json, math, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
FITSRC = os.path.join(EV, 'candidate_31', 'o31_fit.py')
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

FADE = json.load(open(os.path.join(HERE, 'FADE_31F.json')))
BETA = json.load(open(os.path.join(HERE, 'BETA_31F.json')))
PHI = json.load(open(os.path.join(HERE, 'PHI_31F.json')))

# ---- the re-measured inputs, in o31_fit.py's own variable names -------------------------------------
BETA_POOLED = [(float(g), float(b)) for g, b in BETA['rederived_points']]
BACKBONE = {int(k): float(v) for k, v in FADE['backbone_31f'].items()}
FADE_D = {int(k): float(v) for k, v in FADE['wired'].items()}
D2 = FADE_D[2]
MIDPOINTS = [2.5, 10.5, 25.5, 53.0, 85.5]
BANDS_ORDER = ['0-5', '6-15', '16-35', '36-70', '71+']
STALL_SRC = {BANDS_ORDER[i]: float(PHI['beta_stall_31f'][str(MIDPOINTS[i])]) for i in range(5)}
BETA_STALL_RAW = [(MIDPOINTS[i], STALL_SRC[BANDS_ORDER[i]]) for i in range(5)]
BETA_STALL = [(g, max(0.0, b)) for g, b in BETA_STALL_RAW]
BAND_N = {2.5: 382, 10.5: 591, 25.5: 834, 53.0: 887, 85.5: 1339}

assert abs(BACKBONE[0] - D2) < 1e-9, 'backbone B(0) is not D(2): the RAW(1) normalisation moved'

# ---- THE COMPUTATIONAL CORE, LIFTED BY SOURCE TEXT AND EXEC'D VERBATIM ------------------------------
_src = open(FITSRC).read()
_core = _src.split('# ---- monotone non-increasing projection (running minimum) ---')[1]
_core = ('# ---- monotone non-increasing projection (running minimum) ---'
         + _core.split('\nOUT = {')[0])
CORE_MD5 = hashlib.md5(_core.encode()).hexdigest()

NS = dict(math=math, json=json, os=os, sys=sys, hashlib=hashlib,
          BETA_POOLED=BETA_POOLED, BACKBONE=BACKBONE, D2=D2, FADE_D=FADE_D,
          BETA_STALL_RAW=BETA_STALL_RAW, BETA_STALL=BETA_STALL, BAND_N=BAND_N,
          MIDPOINTS=MIDPOINTS, BANDS_ORDER=BANDS_ORDER, STALL_SRC=STALL_SRC)
exec(_core, NS)

BETA_MONO_PTS = NS['BETA_MONO_PTS']; STALL_MONO_PTS = NS['STALL_MONO_PTS']
PHI_STALL_PTS = NS['PHI_STALL_PTS']; PHI_RAMP = NS['PHI_RAMP']
TAU_RHO = NS['TAU_RHO']; B_RHO = NS['B_RHO']; SSE_RHO = NS['SSE_RHO']
RHO_TARGETS = NS['RHO_TARGETS']; RHO_ROWS = NS['RHO_ROWS']; RMS_RHO = NS['RMS_RHO']
CHK = NS['CHK']; rho = NS['rho']; pi = NS['pi']; beta_mono = NS['beta_mono']
phi_stall_c = NS['phi_stall_c']

OLD = json.load(open(os.path.join(EV, 'candidate_31', 'LAW31.json')))

print('=== ORDER 31-F  F1(e) -- THE ONE LAW, RE-FITTED ON THE HEAD-FIXED RULER =====================')
print('  fit core lifted from %s   core md5 %s   (%d lines, exec\'d VERBATIM)'
      % (os.path.relpath(FITSRC, ROOT), CORE_MD5, _core.count('\n')))
print('  committed o31_fit.py md5 %s' % md5(FITSRC))
print()
print('THE INPUTS, COMMITTED -> RE-MEASURED')
print('  %-14s %-34s %-34s' % ('object', 'ORDER 31 (pre-head-fix ruler)', 'ORDER 31-F (head-fixed ruler)'))
print('  %-14s %-34s %-34s'
      % ('D(2)/D(3)/D(4)', '0.5502 / 0.2628 / 0.3460',
         '%.4f / %.4f / %.4f' % (FADE_D[2], FADE_D[3], FADE_D[4])))
print('  %-14s %-34s %-34s'
      % ('backbone', '0.5502 0.6485 0.6887 0.8223',
         ' '.join('%.4f' % BACKBONE[k] for k in (0, 2, 5, 10))))
print('  %-14s %-34s %-34s'
      % ('beta measured', ' '.join('%.4f' % b for _, b in OLD['beta_mono']['points_measured']),
         ' '.join('%.4f' % b for _, b in BETA_POOLED)))
print('  %-14s %-34s %-34s'
      % ('beta monotone', ' '.join('%.4f' % b for _, b in OLD['beta_mono']['points_monotone']),
         ' '.join('%.4f' % b for _, b in BETA_MONO_PTS)))
print('  %-14s %-34s %-34s'
      % ('PhiStall', ' '.join('%.4f' % y for _, y in OLD['phi']['PhiStall_knots']),
         ' '.join('%.4f' % y for _, y in PHI_STALL_PTS)))
print()
print('rho(g) = 1 - exp(-(g/TAU)^B)')
print('  ORDER 31   TAU %.10f   B %.10f   RMS %.6f'
      % (OLD['rho']['TAU_RHO'], OLD['rho']['B_RHO'], OLD['rho']['rms_D_units']))
print('  ORDER 31-F TAU %.10f   B %.10f   RMS %.6f   SSE %.3e'
      % (TAU_RHO, B_RHO, RMS_RHO, SSE_RHO))
for r in RHO_ROWS:
    print('    backbone g=%2.0f  B %.6f   rho* %.6f  rho_fit %.6f   B_fit %.6f   resid %+.6f'
          % (r['g'], r['B_target'], r['rho_target_exact'], r['rho_fit'], r['B_fit'], r['resid_D_units']))
print('  RMS residual %.6f D units   (the Step-3 calibration bar is 0.05)' % RMS_RHO)
print()
print('   g    rho     beta_mono  PhiStall   pi(D=1)   pi(D(2))  pi(D(4))  pi(D(4),s=2)')
TABLE = []
for g in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 25, 36, 50, 71, 100, 150, 200, 300):
    row = {'g': g, 'rho': rho(g), 'beta_mono': beta_mono(g), 'PhiStall': phi_stall_c(g),
           'pi_D1_s0': pi(g, 1.0, 0), 'pi_D2_s0': pi(g, FADE_D[2], 0),
           'pi_D4_s0': pi(g, FADE_D[4], 0), 'pi_D4_s2': pi(g, FADE_D[4], 2)}
    TABLE.append(row)
    print(' %4g  %.5f   %.5f   %.5f   %.5f   %.5f   %.5f   %.5f'
          % (g, row['rho'], row['beta_mono'], row['PhiStall'], row['pi_D1_s0'], row['pi_D2_s0'],
             row['pi_D4_s0'], row['pi_D4_s2']))
print()
for k, v in CHK.items():
    print('  %-30s %s' % (k, 'PASS' if v else '*** FAIL ***'))
if not all(CHK.values()):
    sys.exit('ORDER 31-F FIT HALT: a declared check failed on the re-fitted law.')

OUT = {
    'order': 'ORDER 31-F -- THE ONE LAW, RE-FITTED ON THE HEAD-FIXED RULER',
    'law': 'price = rho(g)*Phat + [ D(c_u)*(1-rho(g)) + Phi(g,s)*beta_mono(g)*rho(g) ]*V0',
    'fit_core': {'lifted_from': os.path.relpath(FITSRC, ROOT), 'core_md5': CORE_MD5,
                 'o31_fit_md5': md5(FITSRC)},
    'inputs': {'FADE_31F.json': {'D': FADE_D, 'backbone': BACKBONE, 'flat_from': FADE['flat_from']},
               'BETA_31F.json': {'points': BETA_POOLED},
               'PHI_31F.json': {'beta_stall_raw': BETA_STALL_RAW}, 'band_n': BAND_N},
    'beta_mono': {'points_measured': BETA_POOLED, 'points_monotone': BETA_MONO_PTS,
                  'projection': 'running minimum (monotone non-increasing projection)',
                  'interpolation': 'log-linear in log(g) between midpoints, flat outside'},
    'rho': {'form': 'rho(g) = 1 - exp(-(g/TAU_RHO)^B_RHO)', 'TAU_RHO': TAU_RHO, 'B_RHO': B_RHO,
            'sse': SSE_RHO, 'rms_D_units': RMS_RHO, 'targets_exact': RHO_TARGETS, 'rows': RHO_ROWS},
    'phi': {'beta_stall_raw': BETA_STALL_RAW, 'beta_stall_floored': BETA_STALL,
            'beta_stall_monotone': STALL_MONO_PTS, 'PhiStall_knots': PHI_STALL_PTS,
            'ramp_denominator': PHI_RAMP},
    'checks': CHK, 'curve_table': TABLE,
    'drift_vs_order31': {
        'TAU_RHO': TAU_RHO - OLD['rho']['TAU_RHO'], 'B_RHO': B_RHO - OLD['rho']['B_RHO'],
        'rms': RMS_RHO - OLD['rho']['rms_D_units'],
        'D': {str(k): FADE_D[k] - v for k, v in
              {1: 1.0, 2: 0.5501935857356868, 3: 0.26278629823610156, 4: 0.3460004697526451}.items()},
        'beta_monotone': [[m, b - ob] for (m, b), (_, ob) in
                          zip(BETA_MONO_PTS, OLD['beta_mono']['points_monotone'])],
        'PhiStall': [[m, y - oy] for (m, y), (_, oy) in zip(PHI_STALL_PTS, OLD['phi']['PhiStall_knots'])]},
}
json.dump(OUT, open(os.path.join(HERE, 'LAW31F.json'), 'w'), indent=1, sort_keys=True)
print('\nLAW31F.json written.')
print('\nTHE CONSTANTS TO WIRE (transcribe EXACTLY into _merged_recover.py):')
print('  O31_TAU_RHO=%r; O31_B_RHO=%r' % (TAU_RHO, B_RHO))
print('  O31_BETA=(' + ','.join('(%r,%r)' % (m, b) for m, b in BETA_MONO_PTS) + ')')
print('  O31_PHIST=(' + ','.join('(%r,%r)' % (m, b) for m, b in PHI_STALL_PTS) + ')')
print('  FADE30B  D(2)=%r  D(3)=%r  D(4+)=%r' % (FADE_D[2], FADE_D[3], FADE_D[4]))
