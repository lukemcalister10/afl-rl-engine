#!/usr/bin/env python3
"""ORDER E — the materiality measurement. READ-ONLY, in-memory monkeypatches only.

Usage: measure.py            -> the full site sweep + joints, writes MATERIALITY_E.json
"""
import os, sys, io, json, contextlib, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loadeng, cf

MA, G = loadeng.load()
cf.bind(MA, G)
cp = G['cp']
PLF = G['_PL_F']
LOG = []


def P(s=''):
    print(s, flush=True)
    LOG.append(str(s))


BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), p)

ROWS = [('harry-dean', 'EXHIBIT'), ('cooper-duff-tytler', 'EXHIBIT'),
        ('milan-murdock', 'CONTROL mature 26'), ('levi-ashcroft', 'CONTROL young mid 48g'),
        ('connor-o-sullivan', 'CONTROL young tall 21/47g'), ('logan-morris', 'CONTROL young tall 21/65g')]


def board(p, Y=2026):
    with contextlib.redirect_stdout(io.StringIO()):
        return float(G['ev'](p, Y)) / PLF


def phat(p, Y=2026):
    with contextlib.redirect_stdout(io.StringIO()):
        return float(G['_prod_path'](p, Y)) / PLF


def snap():
    return {k: (board(BY[k]), phat(BY[k])) for k, _ in ROWS}


BASE = snap()
P('=== ORDER E MATERIALITY SWEEP ===  lane RL_O32=1  (board points = ev/%.4f)' % PLF)
P('%-24s %10s %10s' % ('row', 'board', 'Phat'))
for k, r in ROWS:
    P('%-24s %10.1f %10.1f   [%s]' % (k, BASE[k][0], BASE[k][1], r))
P('')
P('BASELINE IDENTITY CONTROL vs PACKET_C §5 repaired-C32 column: dean %d (expect 2400) · '
  'duff-tytler %d (expect 1572) · murdock %d (expect 170)'
  % (round(BASE['harry-dean'][0]), round(BASE['cooper-duff-tytler'][0]), round(BASE['milan-murdock'][0])))
assert round(BASE['harry-dean'][0]) == 2400 and round(BASE['cooper-duff-tytler'][0]) == 1572 \
    and round(BASE['milan-murdock'][0]) == 170, 'BASELINE IDENTITY FAILED'
P('BASELINE IDENTITY: PASS')
P('')

RESULTS = []


def run(name, desc, installer, note=''):
    un = installer()
    try:
        s = snap()
    finally:
        un()
    after = snap()
    for k, _ in ROWS:
        assert abs(after[k][0] - BASE[k][0]) < 1e-9, 'RESTORE FAILED on %s after %s' % (k, name)
    d = {k: (s[k][0] - BASE[k][0], s[k][1] - BASE[k][1]) for k, _ in ROWS}
    RESULTS.append(dict(site=name, desc=desc, note=note,
                        after={k: s[k][0] for k, _ in ROWS},
                        dboard={k: d[k][0] for k, _ in ROWS},
                        dphat={k: d[k][1] for k, _ in ROWS}))
    P('%-14s %-46s' % (name, desc))
    P('     ' + '  '.join('%s %+8.1f' % (k.split('-')[0][:6], d[k][0]) for k, _ in ROWS))
    if note:
        P('     note: ' + note)
    return d


# ---------------- IDENTITY CONTROL for the re-implemented projection loops ----------------
d = run('S1-IDENT', 'S1 loops re-implemented with Delta==0 (must be all-zero)',
        lambda: cf.install_S1(agecorrect=False))
mx = max(abs(v[0]) for v in d.values())
P('     S1 loop-copy identity: max |delta| = %.10f board points  -> %s'
  % (mx, 'PASS (byte-exact re-implementation)' if mx < 1e-9 else 'FAIL'))
assert mx < 1e-9, 'S1 loop copy is not byte-exact'
P('')

# ---------------- the class-(b) sites, one at a time ----------------
run('S1', 'projection replacement bar -> age-referenced', lambda: cf.install_S1(True))
run('S2-V5', 'flat future discount -> owner V5 age ladder', lambda: cf.install_S2('5'))
run('S2-V3', 'flat future discount -> owner V3 age ladder', lambda: cf.install_S2('3'))
run('S3', 'v7 tail-relax gate lcr>4 -> age-referenced', lambda: cf.install_S3())
run('S4', 'un-compress rho margin -> age-referenced', lambda: cf.install_S4())
run('S5', '_lvl_eff exposure shrink neutralized', lambda: cf.install_S5())
run('S6', '_inferM1 upside-fade bar -> age-referenced', lambda: cf.install_S6())
run('S7', '_est decliner-shed bar -> age-referenced', lambda: cf.install_S7())
run('S18', 'D8 staleness qv denominator -> age-referenced', lambda: cf.install_S18())
run('S19', 'decay-gate par -> age-referenced (ORDER C site 2)', lambda: cf.install_S19())
run('S20', 'ITEM C Q denominator -> age-referenced (ORDER C site 1)', lambda: cf.install_S20())
run('S22-off', 'L1c young credit neutralized (sizes what is paid)', lambda: cf.install_S22('off'))
run('S22-full', 'L1c young credit age-keyed (phi=1 under 24)', lambda: cf.install_S22('full'))
run('S25-eta0', 'BOUND ONLY: re-mix g-keyed pedigree de-rate eta=0', lambda: cf.install_S25_eta0())
run('S25-rho1', 'CEILING ONLY (double-counts): rho31 -> 1', lambda: cf.install_S25_rho1())
P('')


# ---------------- joints ----------------
def joint(*installers):
    def _i():
        uns = [f() for f in installers]

        def un():
            for u in reversed(uns):
                u()
        return un
    return _i


run('J-PHAT-B', 'ALL class-(b) sites inside Phat: S1+S3+S4+S5+S6+S7',
    joint(lambda: cf.install_S1(True), cf.install_S3, cf.install_S4, cf.install_S5,
          cf.install_S6, cf.install_S7))
run('J-S1+S4', 'S1 + S4', joint(lambda: cf.install_S1(True), cf.install_S4))
run('J-S1+S2', 'S1 + S2(V5)', joint(lambda: cf.install_S1(True), lambda: cf.install_S2('5')))
run('J-S1+S22', 'S1 + S22-full', joint(lambda: cf.install_S1(True), lambda: cf.install_S22('full')))
run('J-S1+S4+S2', 'S1 + S4 + S2(V5)',
    joint(lambda: cf.install_S1(True), cf.install_S4, lambda: cf.install_S2('5')))
run('J-ALLB', 'every class-(b) site: Phat-B + S18 + S19 + S20 + S22-full',
    joint(lambda: cf.install_S1(True), cf.install_S3, cf.install_S4, cf.install_S5, cf.install_S6,
          cf.install_S7, cf.install_S18, cf.install_S19, cf.install_S20,
          lambda: cf.install_S22('full')))

P('')
P('=== RANKED BY |dean| + |CDT| (board points) ===')
P('%-14s %9s %9s %9s | %9s %9s %9s %9s' %
  ('site', 'dean', 'CDT', 'sum|.|', 'murdock', 'ashcroft', 'osulliv', 'morris'))
for r in sorted(RESULTS, key=lambda r: -(abs(r['dboard']['harry-dean']) + abs(r['dboard']['cooper-duff-tytler']))):
    dd = r['dboard']
    P('%-14s %+9.1f %+9.1f %9.1f | %+9.1f %+9.1f %+9.1f %+9.1f' %
      (r['site'], dd['harry-dean'], dd['cooper-duff-tytler'],
       abs(dd['harry-dean']) + abs(dd['cooper-duff-tytler']),
       dd['milan-murdock'], dd['levi-ashcroft'], dd['connor-o-sullivan'], dd['logan-morris']))

HERE = os.path.dirname(os.path.abspath(__file__))
json.dump(dict(lane='RL_O32=1', PLF=PLF, base={k: BASE[k][0] for k, _ in ROWS},
               base_phat={k: BASE[k][1] for k, _ in ROWS}, results=RESULTS),
          open(os.path.join(HERE, 'MATERIALITY_E.json'), 'w'), indent=1)
open(os.path.join(HERE, 'MEASURE_E_out.txt'), 'w').write('\n'.join(LOG) + '\n')
P('\nwrote MATERIALITY_E.json + MEASURE_E_out.txt')
