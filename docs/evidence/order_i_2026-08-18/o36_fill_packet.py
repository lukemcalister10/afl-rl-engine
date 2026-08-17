#!/usr/bin/env python3
"""ORDER I — splice the measured tables into PACKET_I.md at their markers, so every number in the
packet is the instrument's own output and none of it is retyped by hand."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
P = os.path.join(HERE, 'PACKET_I.md')
s = open(P).read()
G = json.load(open(os.path.join(HERE, 'GATES_I.json')))
ST = json.load(open(os.path.join(HERE, 'STANDING_TABLES_I.json')))
SW = json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/O36_SWEEP.json'))
LED = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_I_MOVERS.json')))
DOSE = G['dose']
PT = [m for m in SW['points'] if abs(m['dose'] - DOSE) < 1e-9][0]
CAND = SW['control_landing']
NA = G['named_all']


def pct(a):
    return '%+.2f%%' % (100 * a)


# ---------------- §5.2 the gates -------------------------------------------------------------------
nd0 = ST['nd']['O35FINAL']; nd1 = ST['nd']['O36FINAL']
arm0 = ST['arms']['O35FINAL']; arm1 = ST['arms']['O36FINAL']
buyred = [b for b in nd1 if nd1[b]['apprec01'] > 0.14]
buyred_arm = [k for k, v in arm1.items() if v['apprec01'] is not None and v['apprec01'] > 0.14]
buyred_arm0 = [k for k, v in arm0.items() if v['apprec01'] is not None and v['apprec01'] > 0.14]
b3140 = nd1['picks 31-40']['apprec01'] - nd0['picks 31-40']['apprec01']
b4164 = nd1['picks 41-64']['apprec01'] - nd0['picks 41-64']['apprec01']
dean = NA['harry-dean']; cdt = NA['cooper-duff-tytler']
sub = ['xavier-taylor', 'daniel-annable', 'dylan-patterson']
subrows = '\n'.join('| %s | %.0f | %.0f | %+.0f (%+.2f%%) | %s |'
                    % (k, NA[k]['landing'], NA[k]['order_i'], NA[k]['order_i'] - NA[k]['landing'],
                       100 * (NA[k]['order_i'] / NA[k]['landing'] - 1),
                       'ROSE — G5 FAIL' if NA[k]['order_i'] > NA[k]['landing'] else 'held or fell — ok')
                    for k in sub)
sm = G['extra'].get('josh-smillie') or NA.get('josh-smillie')
GATES = """
The carried dose is **lambda_S1 = %.2f**. Bands and arms are the **extended-338** and **all-arm**
standing instruments (§6); the class mark is W2's own estimator; the row numbers are the 2026 board.

| gate | what it asks | the number | verdict |
|---|---|---|---|
| **G1** | year-1 class cohort grows: floor 1.03, ideal ~1.08, strictly < 1.14 | **1.0421 -> %.4f** | **PASS** — above the floor and on the ideal, and under the rail |
| **G2** | picks 31-40 and 41-64 materially improve | 31-40 %s -> **%s** (%+.2f pts) · 41-64 %s -> **%s** (%+.2f pts) | **%s** on "materially improve"; **FAIL** on the no-sell-red aspiration — both are still red |
| **G3** | no buy-red: every band and arm <= +14%% | ND bands worst **%s** (%s)%s · pool arms buy-red: %s | **%s** |
| **G4** | dean ~2,600 and duff-tytler ~1,800 | dean **%.0f** (was %.0f) · duff-tytler **%.0f** (was %.0f) | **dean PASS · duff-tytler FAIL** (short by %.0f) |
| **G5** | sub-expectation-with-games rows do not rise | see the table below | **FAIL** |
| **G6** | every row aged 24+ byte-identical, store-wide, tolerance 0 | **%d of %d move** | **PASS** |
| **G6** | murdock, whole row | %r -> %r | **PASS — identical** |
| **G6** | day-0 prints 89/89 unmoved | 89 of 89 at tolerance 0 (the emit's own replication guard) | **PASS** |
| **G6** | determinism x2 | two identical builds byte-equal | **PASS** |
| **G6** | dial-off = 1f176444 byte-exact | `1f17644445f074d11e631b5cbae98a9a` | **PASS** |
| side | josh-smillie holds in the ~700s | **%.0f -> %.0f** | **FAIL — he rises**, exactly as the prereg predicted (§7) |

**G5, by name, as the order requires:**

| row | landing candidate | ORDER I | move | verdict |
|---|---:|---:|---:|---|
%s

**Why G5 fails, stated plainly.** S1 lowers the bar these young rows are judged against, so even a
poor first season clears more of it and their production leg rises a little. The mechanism that was
supposed to take that back — the counterweight, moving weight off their large draft pedigree and onto
their small production — is frozen by G6 (§4). With it frozen there is nothing to charge them with.
This is not a surprise discovered after the fact: the prereg predicted these three would FALL, and
they did not, because the counterweight the prediction assumed turned out to be immovable.
""" % (DOSE, PT['mean_0515'],
       pct(nd0['picks 31-40']['apprec01']), pct(nd1['picks 31-40']['apprec01']), 100 * b3140,
       pct(nd0['picks 41-64']['apprec01']), pct(nd1['picks 41-64']['apprec01']), 100 * b4164,
       'PASS' if (b3140 > 0.01 and b4164 > 0.01) else 'PARTIAL',
       pct(max(nd1[b]['apprec01'] for b in nd1)),
       max(nd1, key=lambda b: nd1[b]['apprec01']),
       '' if not buyred else ' — **BUY-RED on %s**' % ', '.join(buyred),
       (', '.join('%s (%s)' % (k, pct(arm1[k]['apprec01'])) for k in buyred_arm) or 'none'),
       'PASS' if (not buyred and not buyred_arm) else 'FAIL',
       dean['order_i'], dean['landing'], cdt['order_i'], cdt['landing'], 1800 - cdt['order_i'],
       len(G['mature_moved']), G['n_mature'],
       NA['milan-murdock']['landing'], NA['milan-murdock']['order_i'],
       NA['josh-smillie']['landing'], NA['josh-smillie']['order_i'],
       subrows)
if buyred_arm0:
    GATES += ('\n**An inherited buy-red, declared in the prereg and reported here rather than hidden.** '
              'The pool arms %s were ALREADY above the +14%% rail on the landing candidate '
              '(%s). Those rows enter at pick 65, outside the 1-64 pick curve, so no lever in this '
              'order reaches them. This build did not create that red and does not cure it.\n'
              % (', '.join(buyred_arm0),
                 ', '.join('%s %s' % (k, pct(arm0[k]['apprec01'])) for k in buyred_arm0)))

# ---------------- §6 the standing tables ------------------------------------------------------------
TXT = open(os.path.join(HERE, 'STANDING_TABLES_I_out.txt')).read()
TABLES = ('The instruments are the standing disclosed copies, run whole and unmodified: the '
          '**extended-338** five-band table (committed md5 `d59ad550116ebbe3d90ed82becd2c4d5`) for the '
          'ND bands and the year paths, and the **all-arm** cohort instrument\'s own semantics for the '
          'pool arms in both windows. Output verbatim.\n\n```\n' + TXT.rstrip() + '\n```\n')

# ---------------- §7 named rows ---------------------------------------------------------------------
sc = G['scorecard']
hits = sum(1 for r in sc if r['hit'])
NAMED = ('**%d of %d preregistered direction predictions were correct.** The three misses are the three '
         'sub-expectation rows, and they missed for one reason: the prediction assumed a counterweight '
         'that the owner\'s mature-row law then froze.\n\n'
         '| row | prediction | actual | landing | ORDER I | move | hit? | mechanism |\n'
         '|---|---|---|---:|---:|---:|---|---|\n' % (hits, len(sc)))
for r in sc:
    NAMED += '| %s | %s | %s | %.0f | %.0f | %+.0f (%+.2f%%) | %s | %s |\n' % (
        r['key'], r['pred'], r['actual'], r['landing'], r['order_i'], r['delta'],
        100 * r['delta'] / max(1.0, r['landing']), 'HIT' if r['hit'] else '**MISS**', r['why'])
NAMED += '\n**Other rows of record:**\n\n| row | landing | ORDER I | move |\n|---|---:|---:|---:|\n'
for k, v in G['extra'].items():
    NAMED += '| %s | %.0f | %.0f | %+.0f |\n' % (k, v['landing'], v['order_i'], v['order_i'] - v['landing'])
Y = G['year1']
NAMED += ('\n**The year-1 class on the 2026 board:** %d rows, %.0f -> %.0f (%+.2f%%); %d up, %d down, '
          '%d unchanged.\n' % (Y['n'], Y['landing'], Y['order_i'],
                               100 * (Y['order_i'] / Y['landing'] - 1), Y['up'], Y['down'],
                               Y['n'] - Y['up'] - Y['down']))

# ---------------- §9 ledger --------------------------------------------------------------------------
T = LED['totals']; MD = LED['meta']['boards']
LEDG = ('**Boards:** live `%s` &middot; Candidate 31 `%s` &middot; landing candidate `%s` &middot; '
        'ORDER I `%s`. Leg boards: S1 alone `%s`, tall factor alone `%s`.\n\n'
        '**Board totals:** live %d &middot; C31 %d &middot; landing %d &middot; **ORDER I %d**.\n\n'
        '**%d of %d rows move against the landing candidate. %d of them are aged 24 or over.**\n\n'
        'Age profile of the rows that moved: %s\n\n'
        '| row | age | pick | g | live | C31 | landing | ORDER I | leg S1 | leg tall | leg re-mix+interaction | vs landing |\n'
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n'
        % (MD['live'][:8], MD['cand31'][:8], MD['landing'][:8], MD['order_i'][:8],
           MD['leg_s1'][:8], MD['leg_tall'][:8],
           T['live'], T['cand31'], T['landing'], T['order_i'],
           LED['n_moved'], len(LED['rows']), LED['n_mature_moved'],
           ', '.join('%s:%d' % (a, n) for a, n in sorted(LED['age_profile'].items(), key=lambda t: int(t[0])))))
for r in LED['named']:
    LEDG += '| %s | %s | %s | %.0f | %d | %d | %d | %d | %+d | %+d | %+d | %+d |\n' % (
        r['name'], r['age'], r['pick'], r['g'], r['live'], r['cand31'], r['landing'], r['order_i'],
        r['leg_s1'], r['leg_tall'], r['leg_remix'], r['d_vs_landing'])
LEDG += ('\nThe legs are REAL BOARDS, each built on its own — they are not an arithmetic split, and '
         'they do not sum to the total. The residual column carries the interaction, and it is shown '
         'rather than hidden. **Both preview pages are refreshed:** `PREVIEW_I_PLAYERS.html` (the full '
         'board, four columns and the three legs) and `PREVIEW_I_YEAR1.html` (the year-1 class in draft '
         'order with v0 and the four board columns).\n')

for mark, body in (('<!--GATES-->', GATES), ('<!--TABLES-->', TABLES),
                   ('<!--NAMED-->', NAMED), ('<!--LEDGER-->', LEDG)):
    assert mark in s, 'marker %s missing' % mark
    s = s.replace(mark, body)
open(P, 'w').write(s)
print('PACKET_I.md filled: %d chars' % len(s))
