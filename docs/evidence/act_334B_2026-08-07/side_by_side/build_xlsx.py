"""#334 stage B — THE SIDE-BY-SIDE WORKBOOK, regenerated with STAGE 5 (the QUIET-STARTER REPRICE) as a
SIXTH stage column. Per-row stage deltas sum EXACTLY to the total, and that identity is both asserted in
Python and carried as a live formula column in the sheet so a reader can see it hold.

Supersedes the five-column build (stage 4 amendment 1). Stage 5's landed board is `13f8c2e0`; it is the
consistency-pass solve, owner-authorized at #334 comment 5217293177.
"""
import json, csv, os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

SBS = '/home/claude/sbs'
HERE = os.path.dirname(os.path.abspath(__file__))
ACT = os.path.dirname(HERE)
S5 = os.path.join(ACT, 'stage5')
S4 = os.path.join(ACT, 'stage4')
A1 = os.path.join(ACT, 'stage4_amend1')
OUT = os.path.join(HERE, 'board_before_after.xlsx')
REBASE = 0.891738          # stage-3 uniform numeraire re-base; unmoved by stages 4, 4a1 and 5

NAMES = ['shipped', 'stage1', 'eraremoval', 'stage3', 'stage4', 'final']
B = {n: json.load(open(os.path.join(SBS, 'board_%s.json' % n))) for n in NAMES}
B['stage5'] = json.load(open(os.path.join(S5, 'noarb', 'board_STAGE5_13f8c2e0.json')))
V = {n: {r['key']: r['v'] for r in B[n]['active'] if r.get('v') is not None} for n in B}
keys = [r['key'] for r in B['stage5']['active'] if r.get('v') is not None]
meta = {r['key']: r for r in B['stage5']['active']}
for n in V:
    assert set(V[n]) == set(keys), 'roster differs at %s: %d vs %d' % (n, len(V[n]), len(keys))
print('roster identical across all SEVEN boards: %d players' % len(keys))

HDR = Font(name='Arial', sz=10, b=True, color='FFFFFF')
NRM = Font(name='Arial', sz=10)
FILL = PatternFill('solid', fgColor='1F3864')
INT = '#,##0;(#,##0);-'
PCT = '0.00%;(0.00%);-'

wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'players'
cols = [('key', 26), ('name', 24), ('club', 20), ('pos', 7), ('age', 6), ('entry', 26),
        ('OLD — shipped board 113b36f8', 17), ('NEW — final board 13f8c2e0', 17),
        ('abs Δ (NEW − OLD)', 13), ('% Δ (of OLD)', 12),
        ('% change beyond the currency re-base', 29),
        ('Δ reference layer (de5110bb − 113b36f8)', 18),
        ('Δ era removal (f94e0778 − de5110bb)', 18),
        ('Δ curve+surface+numéraire (6c9f8d3a − f94e0778)', 22),
        ('Δ reactivity (b490ae8b − 6c9f8d3a)', 18),
        ('Δ surprise-trust (b56bbdde − b490ae8b)', 20),
        ('Δ quiet-starter reprice (13f8c2e0 − b56bbdde)', 24),
        ('STAGE SUM CHECK (ΣΔ stages − abs Δ; must be 0)', 26)]
for i, (h, w) in enumerate(cols, 1):
    c = ws.cell(1, i, h); c.font = HDR; c.fill = FILL
    c.alignment = Alignment(horizontal='center', wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width = w


def entry_label(r):
    ty = r.get('ty') or '?'; pk = r.get('pk')
    if ty == 'ND' and pk and pk <= 64: return 'National pick %d' % pk
    return '%s %s' % (r.get('draft') or ty, ('pick %d' % pk) if pk else '(pool)')


bad = 0
for i, k in enumerate(keys, 2):
    r = meta[k]
    ws.cell(i, 1, k).font = NRM; ws.cell(i, 2, r.get('name')).font = NRM
    ws.cell(i, 3, r.get('club')).font = NRM; ws.cell(i, 4, r.get('gf')).font = NRM
    ws.cell(i, 5, r.get('age')).font = NRM; ws.cell(i, 6, entry_label(r)).font = NRM
    o, n = V['shipped'][k], V['stage5'][k]
    c = ws.cell(i, 7, o); c.font = NRM; c.number_format = INT
    c = ws.cell(i, 8, n); c.font = NRM; c.number_format = INT
    c = ws.cell(i, 9, '=H%d-G%d' % (i, i)); c.font = NRM; c.number_format = INT
    c = ws.cell(i, 10, '=IF(G%d=0,"",(H%d-G%d)/G%d)' % (i, i, i, i)); c.font = NRM; c.number_format = PCT
    c = ws.cell(i, 11, '=IF(G%d=0,"",(H%d-G%d*%s)/(G%d*%s))' % (i, i, i, REBASE, i, REBASE))
    c.font = NRM; c.number_format = PCT
    d = [V['stage1'][k] - V['shipped'][k], V['eraremoval'][k] - V['stage1'][k],
         V['stage3'][k] - V['eraremoval'][k], V['stage4'][k] - V['stage3'][k],
         V['final'][k] - V['stage4'][k], V['stage5'][k] - V['final'][k]]
    for j, x in enumerate(d):
        c = ws.cell(i, 12 + j, x); c.font = NRM; c.number_format = INT
    if sum(d) != n - o: bad += 1
    c = ws.cell(i, 18, '=SUM(L%d:Q%d)-I%d' % (i, i, i)); c.font = NRM; c.number_format = INT
assert bad == 0, 'PER-ROW STAGE SUM FAILED on %d rows' % bad
print('PER-ROW STAGE SUM ASSERT: PASS on all %d rows (Σ of the SIX stage deltas == NEW − OLD, exactly)' % len(keys))
ws.freeze_panes = 'A2'; ws.auto_filter.ref = 'A1:R%d' % (len(keys) + 1)

# ---- picks ----
ps = wb.create_sheet('picks')
lad = json.load(open('/home/claude/s5_landing/engine/rl_after/pvc_curve_v2.json'))
pn = {int(k): v for k, v in lad['curve'].items()}
po = {int(k): v for k, v in json.load(open(os.path.join(SBS, 'pvc_shipped.json')))['curve'].items()}
p4 = {int(k): v for k, v in json.load(open(os.path.join(SBS, 'pvc_final.json')))['curve'].items()}
assert pn == p4, 'stage 5 moved the settled ladder — it must not'
for i, (h, w) in enumerate([('pick', 8), ('OLD ladder value — shipped', 26),
                            ('NEW ladder value — final (curve_md5 %s)' % lad['curve_md5'], 30),
                            ('abs Δ (NEW − OLD)', 16), ('% Δ (of OLD)', 14),
                            ('Δ from stage 4 amendment 1 (stage 5 moves none)', 30)], 1):
    c = ps.cell(1, i, h); c.font = HDR; c.fill = FILL
    c.alignment = Alignment(horizontal='center', wrap_text=True)
    ps.column_dimensions[get_column_letter(i)].width = w
for i, nn in enumerate(sorted(set(po) & set(pn)), 2):
    ps.cell(i, 1, nn).font = NRM
    c = ps.cell(i, 2, po[nn]); c.font = NRM; c.number_format = INT
    c = ps.cell(i, 3, pn[nn]); c.font = NRM; c.number_format = INT
    c = ps.cell(i, 4, '=C%d-B%d' % (i, i)); c.font = NRM; c.number_format = INT
    c = ps.cell(i, 5, '=IF(B%d=0,"",(C%d-B%d)/B%d)' % (i, i, i, i)); c.font = NRM; c.number_format = PCT
    c = ps.cell(i, 6, pn[nn] - p4[nn]); c.font = NRM; c.number_format = INT
ps.freeze_panes = 'A2'
print('picks sheet: %d picks (curve_md5 %s); the ladder is UNMOVED by stage 5.'
      % (len(set(po) & set(pn)), lad['curve_md5']))


def _num(v):
    try:
        float(v); return True
    except Exception:
        return False


def movers_sheet(title, banner, note, csvpath):
    sh = wb.create_sheet(title)
    c = sh.cell(1, 1, banner); c.font = Font(name='Arial', sz=11, b=True)
    c = sh.cell(2, 1, note); c.font = Font(name='Arial', sz=9, i=True)
    rows = list(csv.reader(open(csvpath)))
    for ri, row in enumerate(rows, 4):
        for ci, val in enumerate(row, 1):
            cc = sh.cell(ri, ci, val if ri == 4 else (float(val) if _num(val) else val))
            cc.font = HDR if ri == 4 else NRM
            if ri == 4:
                cc.fill = FILL; cc.alignment = Alignment(horizontal='center', wrap_text=True)
    for ci in range(1, len(rows[0]) + 1):
        sh.column_dimensions[get_column_letter(ci)].width = 17
    sh.column_dimensions['A'].width = 26; sh.column_dimensions['B'].width = 24
    sh.freeze_panes = 'A5'
    return len(rows) - 1


n4 = movers_sheet('reactivity movers',
                  'STAGE 4 — PEDIGREE-CONDITIONED REACTIVITY: every moved player (6c9f8d3a -> b490ae8b)',
                  'Verbatim from docs/evidence/act_334B_2026-08-07/stage4/movers_full.csv. No cap.',
                  os.path.join(S4, 'movers_full.csv'))
n1 = movers_sheet('surprise movers',
                  'STAGE 4 AMENDMENT 1 — SURPRISE-SCALED EVIDENCE TRUST: every moved player (b490ae8b -> b56bbdde)',
                  'Verbatim from docs/evidence/act_334B_2026-08-07/stage4_amend1/movers_full.csv. No cap. '
                  's = |log(e_full/anchor_full)| is the size of the re-rate the record claims; u is its unresolved share.',
                  os.path.join(A1, 'movers_full.csv'))
n5 = movers_sheet('quiet-starter movers',
                  'STAGE 5 — THE QUIET-STARTER REPRICE: every moved player (b56bbdde -> 13f8c2e0)',
                  'Verbatim from docs/evidence/act_334B_2026-08-07/stage5/movers_full.csv. No cap. '
                  'G is the taught anchor factor at that player\'s OWN cell, recomputed from his record to date.',
                  os.path.join(S5, 'movers_full.csv'))
print('movers sheets: stage 4 = %d rows, amendment 1 = %d rows, stage 5 = %d rows' % (n4, n1, n5))

# ---- readme ----
rm = wb.create_sheet('readme')
rm.column_dimensions['A'].width = 5; rm.column_dimensions['B'].width = 132
LINES = [
    ('', 'READ ME — what each sheet is, and how to read the columns'), ('', ''),
    ('1.', 'This workbook is the owner review set for act #334 stage B. It puts the ADOPTED board next to the board this act produces.'),
    ('', 'OLD = the shipped board 113b36f8 (commit f8fe8361, on main today). NEW = the final board 13f8c2e0 on branch landing/334-stage-b.'),
    ('', "Nothing here is adopted. Adoption is the owner's word. No PR, no tag, no main merge."), ('', ''),
    ('2.', 'SEVEN boards, SIX of which moved; each mover has its own delta column on the players sheet:'),
    ('', '   Δ reference layer          de5110bb − 113b36f8   the adopted #336 reference layer'),
    ('', '   Δ era removal              f94e0778 − de5110bb   era normalization stripped (owner ruling)'),
    ('', '   Δ curve+surface+numéraire  6c9f8d3a − f94e0778   base curve re-teach, per-pick re-anchor, year-zero surface refit, numéraire re-base'),
    ('', '   Δ reactivity               b490ae8b − 6c9f8d3a   stage 4, the pedigree-conditioned evidence bar (RL_PED_BAR = 0.5)'),
    ('', '   Δ surprise-trust           b56bbdde − b490ae8b   stage 4 AMENDMENT 1, the surprise-scaled evidence trust (RL_SUR_W = 5.0)'),
    ('', '   Δ quiet-starter reprice    13f8c2e0 − b56bbdde   STAGE 5, the taught anchor factor G (RL_G5_W = 1.0)'), ('', ''),
    ('3.', 'The per-row identity Σ(six stage deltas) == (NEW − OLD) is asserted in Python at build time on all 804 rows, and carried as a live'),
    ('', 'formula in the STAGE SUM CHECK column so a reader can watch it hold. verify_xlsx.py re-checks it from the written file'),
    ('', '(LibreOffice is non-functional in this sandbox, so formulas are verified in Python — the convention amendment 1 established).'), ('', ''),
    ('4.', 'Stage 5 moves NO ladder, NO numéraire, NO store and NO pole. It moves 65 of 804 board rows; every one moves UP; zero rows fall.'),
    ('', 'Its landing and the ONE law that binds it are in docs/evidence/act_334B_2026-08-07/stage5/CONSISTENCY_PASS.md — read that before ruling.'),
]
for i, (a, b_) in enumerate(LINES, 1):
    rm.cell(i, 1, a).font = Font(name='Arial', sz=10, b=True)
    rm.cell(i, 2, b_).font = Font(name='Arial', sz=10)

wb.save(OUT)
print('wrote %s' % OUT)
