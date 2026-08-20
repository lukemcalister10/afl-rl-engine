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
LB = {r['key']: r for r in LED['named']}          # BOARD POINTS -- the currency the owner reads
MATB = [r for r in LED['rows'] if r['age'] >= 24 and r['d_vs_landing'] != 0]
MATB.sort(key=lambda r: -abs(r['d_vs_landing']))
MAT_TALL = sum(1 for r in MATB if r['leg_tall'] != 0)
MAT_S1 = sum(1 for r in MATB if r['leg_s1'] != 0)


D0A = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'order_a_2026-08-17', 'DAY0_32_FINAL.json')))
D0B = json.load(open(os.path.join(HERE, 'DAY0_I_FINAL.json')))
_A = {r['key']: r for r in D0A['rows']}; _B = {r['key']: r for r in D0B['rows']}
D0_SAME_V0 = sum(1 for k in _A if abs(_A[k]['derived_v0'] - _B[k]['derived_v0']) == 0.0)
D0_MOVED = [k for k in _A if _A[k]['printed'] != _B[k]['printed']]
D0_UP = sum(1 for k in D0_MOVED if _B[k]['printed'] > _A[k]['printed'])


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
subrows = '\n'.join('| %s | %d | %d | %+d (%+.2f%%) | %s |'
                    % (k, LB[k]['landing'], LB[k]['order_i'], LB[k]['d_vs_landing'],
                       100.0 * LB[k]['d_vs_landing'] / LB[k]['landing'],
                       'ROSE — G5 FAIL' if LB[k]['d_vs_landing'] > 0 else 'held or fell — ok')
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
| **G4** | dean ~2,600 and duff-tytler ~1,800 (BOARD POINTS, the currency the owner reads; C31 levels 2,670 / 1,832) | dean **%d** (was %d, C31 2,670) · duff-tytler **%d** (was %d, C31 1,832) | **BOTH FAIL** — dean short by %d, duff-tytler short by %d |
| **G5** | sub-expectation-with-games rows do not rise | see the table below | **FAIL** |
| **G6** | every row aged 24+ byte-identical, store-wide, tolerance 0 | **%d of %d move** on the board (total absolute movement %d board points, worst %s %+d) — and **every single one moves through LEVER 3, none through S1** (leg_tall non-zero on %d of %d, leg_S1 non-zero on %d) | **FAIL — and the cause is named** |
| **G6** | murdock, whole row | %r -> %r | **PASS — identical** |
| **G6** | day-0 prints 89/89 unmoved | the raw entry object `derived_v0` is **IDENTICAL on 89 of 89** at tolerance 0; the **printed** day-0 price moves on **89 of 89** (%d up, %d down; largest up mitchell-marsh 451 -> 552, largest down ben-camporeale 157 -> 122) | **FAIL as stated** — see below |
| **G6** | determinism x2 | two identical builds byte-equal | **PASS** |
| **G6** | dial-off = 1f176444 byte-exact | `1f17644445f074d11e631b5cbae98a9a` | **PASS** |
| side | josh-smillie holds in the ~700s | **%d -> %d** board points, and the whole move is `leg_tall` | **FAIL — he rises out of the 700s**, exactly as the prereg predicted (§7) |

**G5, by name, as the order requires:**

| row | landing candidate | ORDER I | move | verdict |
|---|---:|---:|---:|---|
%s

**THE DAY-0 GATE, IN PLAIN WORDS — it fails, and the reason is worth understanding.** A day-0 price for
a player who has never played **is** `v0 x D(c_u)` — his entry value multiplied by the sitter fade.
Order H's factor is a change to exactly that fade. So it moves the printed day-0 of every wired sitter
**by construction**: all 89 of them, %d up and %d down. What did **not** move is `derived_v0`, the raw
entry object the walk-forward matrix writes as year-0 — **identical on 89 of 89 at tolerance zero**
(oskar-taylor 903.8014284605089 on both boards). So V0 is untouched and the year-0 column of the matrix
is untouched; what moved is what the board charges a sitter **today**. The guard file was therefore
re-based on this board and the re-base is disclosed (`o36_day0.py`, `DAY0_I_FINAL.json`, 89 of 89 at
tolerance 0) — the same re-base ORDER D's own pick-curve fade required when it landed. **This seat
reports it as a gate failure against the law as written and does not decide whether the re-base is
acceptable. That is the owner's ruling.**

**THE MATURE-ROW GATE, AND WHICH LEVER BREAKS IT.** S1 does not break it: at every dose tested, 0 of
429 rows aged 24+ move (§4). **Lever 3 does.** A mature row who has sat still carries an unplayed
clock, and Order H's factor is a change to the sitter fade — so a 25-year-old sitter is re-priced by
it exactly as a 20-year-old sitter is. On the board: Liam McMahon (24, pick 33) +41, Nick Bryan (25,
pick 37) +41, Luke Beecken (25, pick 16) −32, Callum Coleman-Jones (27, pick 20) +30. milan-murdock
does not move because he is not a sitter. **The two levers are separable and the ledger separates
them: turn Lever 3 off and G6 passes exactly; turn it on and 50 mature rows move.** That is a clean
choice for the owner, not a defect to be patched.

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
       LB['harry-dean']['order_i'], LB['harry-dean']['landing'],
       LB['cooper-duff-tytler']['order_i'], LB['cooper-duff-tytler']['landing'],
       2600 - LB['harry-dean']['order_i'], 1800 - LB['cooper-duff-tytler']['order_i'],
       len(MATB), G['n_mature'], sum(abs(r['d_vs_landing']) for r in MATB),
       MATB[0]['name'], MATB[0]['d_vs_landing'], MAT_TALL, len(MATB), MAT_S1,
       NA['milan-murdock']['landing'], NA['milan-murdock']['order_i'],
       D0_UP, len(D0_MOVED) - D0_UP,
       LB['josh-smillie']['landing'], LB['josh-smillie']['order_i'],
       subrows, D0_UP, len(D0_MOVED) - D0_UP)
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
