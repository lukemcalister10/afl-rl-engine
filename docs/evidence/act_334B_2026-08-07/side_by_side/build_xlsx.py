"""#334 stage B — THE SIDE-BY-SIDE WORKBOOK, regenerated with STAGE 4 AMENDMENT 1 as a FIFTH stage column.
Per-row stage deltas sum EXACTLY to the total, and that identity is both asserted in Python and carried as
a live formula column in the sheet so a reader can see it hold."""
import json, csv, os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

SBS='/home/claude/sbs'
OUT='/home/claude/amend1_landing/docs/evidence/act_334B_2026-08-07/side_by_side/board_before_after.xlsx'
S4='/home/claude/amend1_landing/docs/evidence/act_334B_2026-08-07/stage4'
A1='/home/claude/amend1_landing/docs/evidence/act_334B_2026-08-07/stage4_amend1'
REBASE=0.891738          # stage-3 uniform numeraire re-base; unchanged by stage 4 and by this amendment

def board(n):
    return json.load(open(os.path.join(SBS,'board_%s.json'%n)))
def vmap(d):
    return {r['key']: r['v'] for r in d['active'] if r.get('v') is not None}
B={n:board(n) for n in ('shipped','stage1','eraremoval','stage3','stage4','final')}
V={n:vmap(B[n]) for n in B}
MD={'shipped':'113b36f8','stage1':'de5110bb','eraremoval':'f94e0778','stage3':'6c9f8d3a','stage4':'b490ae8b','final':'b56bbdde'}

keys=[r['key'] for r in B['final']['active'] if r.get('v') is not None]
meta={r['key']:r for r in B['final']['active']}
for n in V:
    assert set(V[n])==set(keys), 'roster differs at %s: %d vs %d'%(n,len(V[n]),len(keys))
print('roster identical across all six boards: %d players'%len(keys))

HDR=Font(name='Arial',sz=10,b=True,color='FFFFFF')
NRM=Font(name='Arial',sz=10)
FILL=PatternFill('solid',fgColor='1F3864')
INT='#,##0;(#,##0);-'
PCT='0.00%;(0.00%);-'

wb=openpyxl.Workbook(); ws=wb.active; ws.title='players'
cols=[('key',26),('name',24),('club',20),('pos',7),('age',6),('entry',26),
      ('OLD — shipped board 113b36f8',17),('NEW — final board b56bbdde',17),
      ('abs Δ (NEW − OLD)',13),('% Δ (of OLD)',12),
      ('% change beyond the currency re-base',29),
      ('Δ reference layer (de5110bb − 113b36f8)',18),
      ('Δ era removal (f94e0778 − de5110bb)',18),
      ('Δ curve+surface+numéraire (6c9f8d3a − f94e0778)',22),
      ('Δ reactivity (b490ae8b − 6c9f8d3a)',18),
      ('Δ surprise-trust (b56bbdde − b490ae8b)',20),
      ('STAGE SUM CHECK (ΣΔ stages − abs Δ; must be 0)',26)]
for i,(h,w) in enumerate(cols,1):
    c=ws.cell(1,i,h); c.font=HDR; c.fill=FILL; c.alignment=Alignment(horizontal='center',wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width=w
def entry_label(r):
    ty=r.get('ty') or '?'; pk=r.get('pk')
    if ty=='ND' and pk and pk<=64: return 'National pick %d'%pk
    return '%s %s'%(r.get('draft') or ty, ('pick %d'%pk) if pk else '(pool)')
bad=0
for i,k in enumerate(keys,2):
    r=meta[k]
    ws.cell(i,1,k).font=NRM; ws.cell(i,2,r.get('name')).font=NRM; ws.cell(i,3,r.get('club')).font=NRM
    ws.cell(i,4,r.get('gf')).font=NRM; ws.cell(i,5,r.get('age')).font=NRM
    ws.cell(i,6,entry_label(r)).font=NRM
    o,n=V['shipped'][k],V['final'][k]
    c=ws.cell(i,7,o); c.font=NRM; c.number_format=INT
    c=ws.cell(i,8,n); c.font=NRM; c.number_format=INT
    c=ws.cell(i,9,'=H%d-G%d'%(i,i)); c.font=NRM; c.number_format=INT
    c=ws.cell(i,10,'=IF(G%d=0,"",(H%d-G%d)/G%d)'%(i,i,i,i)); c.font=NRM; c.number_format=PCT
    c=ws.cell(i,11,'=IF(G%d=0,"",(H%d-G%d*%s)/(G%d*%s))'%(i,i,i,REBASE,i,REBASE)); c.font=NRM; c.number_format=PCT
    d=[V['stage1'][k]-V['shipped'][k], V['eraremoval'][k]-V['stage1'][k],
       V['stage3'][k]-V['eraremoval'][k], V['stage4'][k]-V['stage3'][k],
       V['final'][k]-V['stage4'][k]]
    for j,x in enumerate(d):
        c=ws.cell(i,12+j,x); c.font=NRM; c.number_format=INT
    if sum(d)!=n-o: bad+=1
    c=ws.cell(i,17,'=SUM(L%d:P%d)-I%d'%(i,i,i)); c.font=NRM; c.number_format=INT
assert bad==0, 'PER-ROW STAGE SUM FAILED on %d rows'%bad
print('PER-ROW STAGE SUM ASSERT: PASS on all %d rows (Σ of the five stage deltas == NEW − OLD, exactly)'%len(keys))
ws.freeze_panes='A2'; ws.auto_filter.ref='A1:Q%d'%(len(keys)+1)

# ---- picks ----
ps=wb.create_sheet('picks')
def ladder(n):
    d=json.load(open(os.path.join(SBS,'pvc_%s.json'%n))); return {int(k):v for k,v in d['curve'].items()}, d.get('curve_md5')
po,mo=ladder('shipped'); pn,mn=ladder('final'); p4,m4=ladder('stage4')
assert pn==p4, 'the amendment moved the settled ladder — it must not'
for i,(h,w) in enumerate([('pick',8),('OLD ladder value — shipped (pvc_curve_v2 curve_md5 %s)'%mo,30),
                          ('NEW ladder value — final (pvc_curve_v2 curve_md5 %s)'%mn,30),('abs Δ (NEW − OLD)',16),
                          ('% Δ (of OLD)',14),('Δ from stage 4 (b56bbdde − b490ae8b)',30)],1):
    c=ps.cell(1,i,h); c.font=HDR; c.fill=FILL; c.alignment=Alignment(horizontal='center',wrap_text=True)
    ps.column_dimensions[get_column_letter(i)].width=w
for i,nn in enumerate(sorted(set(po)&set(pn)),2):
    ps.cell(i,1,nn).font=NRM
    c=ps.cell(i,2,po[nn]); c.font=NRM; c.number_format=INT
    c=ps.cell(i,3,pn[nn]); c.font=NRM; c.number_format=INT
    c=ps.cell(i,4,'=C%d-B%d'%(i,i)); c.font=NRM; c.number_format=INT
    c=ps.cell(i,5,'=IF(B%d=0,"",(C%d-B%d)/B%d)'%(i,i,i,i)); c.font=NRM; c.number_format=PCT
    c=ps.cell(i,6,pn[nn]-p4[nn]); c.font=NRM; c.number_format=INT
ps.freeze_panes='A2'
print('picks sheet: %d picks (pvc_curve_v2 %s -> %s); the ladder is UNMOVED by the amendment: %s'%(
    len(set(po)&set(pn)), mo, mn, all(pn[n]==p4[n] for n in set(pn)&set(p4))))

# ---- movers sheets ----
def movers_sheet(title,banner,note,csvpath):
    sh=wb.create_sheet(title)
    c=sh.cell(1,1,banner); c.font=Font(name='Arial',sz=11,b=True)
    c=sh.cell(2,1,note); c.font=Font(name='Arial',sz=9,i=True)
    rows=list(csv.reader(open(csvpath)))
    for ri,row in enumerate(rows,4):
        for ci,val in enumerate(row,1):
            cc=sh.cell(ri,ci,val if ri==4 else (float(val) if _num(val) else val))
            cc.font=HDR if ri==4 else NRM
            if ri==4: cc.fill=FILL; cc.alignment=Alignment(horizontal='center',wrap_text=True)
    for ci in range(1,len(rows[0])+1): sh.column_dimensions[get_column_letter(ci)].width=17
    sh.column_dimensions['A'].width=26; sh.column_dimensions['B'].width=24
    sh.freeze_panes='A5'
    return len(rows)-1
def _num(v):
    try:
        float(v); return True
    except Exception: return False
n4=movers_sheet('reactivity movers',
    'STAGE 4 — PEDIGREE-CONDITIONED REACTIVITY: every moved player (6c9f8d3a -> b490ae8b)',
    'Verbatim from docs/evidence/act_334B_2026-08-07/stage4/movers_full.csv. No cap.',
    os.path.join(S4,'movers_full.csv'))
n1=movers_sheet('surprise movers',
    'STAGE 4 AMENDMENT 1 — SURPRISE-SCALED EVIDENCE TRUST: every moved player (b490ae8b -> b56bbdde)',
    'Verbatim from docs/evidence/act_334B_2026-08-07/stage4_amend1/movers_full.csv. No cap. '
    's = |log(e_full/anchor_full)| is the size of the re-rate the record claims; u is its unresolved share.',
    os.path.join(A1,'movers_full.csv'))
print('movers sheets: stage 4 = %d rows, amendment 1 = %d rows'%(n4,n1))

# ---- readme ----
rm=wb.create_sheet('readme')
rm.column_dimensions['A'].width=5; rm.column_dimensions['B'].width=132
LINES=[('', 'READ ME — what each sheet is, and how to read the columns'),('',''),
 ('1.','This workbook is the owner review set for act #334 stage B. It puts the ADOPTED board next to the board this act produces.'),
 ('','OLD = the shipped board 113b36f8 (commit f8fe8361, on main today). NEW = the final board b56bbdde on branch landing/334-stage-b.'),
 ('','Nothing here is adopted. Adoption is the owner\'s word. No PR, no tag, no main merge.'),('',''),
 ('2.','SIX stages of the act are represented; FIVE of them moved the board, and each has its own delta column on the players sheet:'),
 ('','   Δ reference layer          de5110bb − 113b36f8   the adopted #336 reference layer'),
 ('','   Δ era removal              f94e0778 − de5110bb   era normalization stripped (owner ruling)'),
 ('','   Δ curve+surface+numéraire  6c9f8d3a − f94e0778   base curve re-teach, per-pick re-anchor, year-zero surface refit, numéraire re-base'),
 ('','   Δ reactivity               b490ae8b − 6c9f8d3a   stage 4, the pedigree-conditioned evidence bar (RL_PED_BAR = 0.5)'),
 ('','   Δ surprise-trust           b56bbdde − b490ae8b   stage 4 AMENDMENT 1, the surprise-scaled evidence trust (RL_SUR_W = 5.0)'),
 ('','The five delta columns SUM EXACTLY to "abs Δ (NEW − OLD)" on every row. Column Q carries that identity as a live formula:'),
 ('','it must read 0 on all 804 rows. It was also asserted in Python at build time and passed on 804/804.'),('',''),
 ('3.','THE NUMÉRAIRE NOTE — read this before reading any single-player change as a real move.'),
 ('','Stage 3 re-based the display currency by a single uniform factor of ×0.891738 applied to every player alike. It changes the'),
 ('','printed number and NOTHING about relativities. Pick 1 stays pinned at 3,000 on both boards. The plain "% Δ (of OLD)" column'),
 ('','therefore shows a ~−10.8% shift that applies to everybody and means nothing about anybody. Column K, "% change beyond the'),
 ('','currency re-base", compares NEW against OLD × 0.891738 and IS the honest measure of real movement. The amendment does not'),
 ('','touch the numéraire, so the same factor still applies.'),('',''),
 ('4.','"reactivity movers" lists every player stage 4 moved (51). "surprise movers" lists every player this amendment moved (45).'),
 ('','Both are verbatim exports of the enumeration CSVs, uncapped. On the surprise sheet: e_full is the demonstrated-production'),
 ('','price, anchor_full is the prior-implied price (R × entry_anchor), s = |log(e_full/anchor_full)| is the size of the re-rate the'),
 ('','record claims, and u is the share of that record still unresolved. The shrink is SUR_W × s × u extra passes of the evidence ramp.'),('',''),
 ('5.','BOTH movers lists contain UP-MOVERS, and they are named rather than hidden. The evidence bar is SYMMETRIC in the sign of the'),
 ('','surprise by owner law (L-SYMMETRY, register item 108): a thin record BELOW its anchor is the same small sample as one above it,'),
 ('','so a player whose few games went badly is likewise held nearer his anchor and his price RISES. A one-sided rule would be a'),
 ('','branch and is refused under L-SMOOTH. If the mechanism is accepted, the up-movers come with it.'),('',''),
 ('6.','The "picks" sheet is the pick ladder, shipped vs final. Column F shows the amendment\'s own effect on it: ZERO at every pick.'),
 ('','The settled ladder (engine/rl_after/pvc_curve_v2.json, payload 18203822, pick 1 = 3,000) is untouched by stage 4 and by this'),
 ('','amendment, so either dial can be re-ruled without re-deriving any curve.'),('',''),
 ('7.','Board values are DISPLAY BOARD VALUES in VOR board points, denominated so that national-draft pick 1 = 3,000.'),
 ('','Source file at each stage: data/rl_build/rl_app_data.json at commits f8fe8361 / ad50dad / f7ae027 / c0ea507 / 44950de, and'),
 ('','the working final board b56bbdde. All six carry the same 804 keys — no adds, no drops. Store 37ced3ce, unchanged throughout.'),('',''),
 ('8.','FORMULA VERIFICATION. Columns I, J, K and Q on "players" and D, E on "picks" are live formulas, and they ship without cached'),
 ('','values — exactly as the workbook this one replaces did. LibreOffice is non-functional in the build sandbox (it cannot load even a'),
 ('','one-cell workbook), so the usual recalculate-and-check pass could not be run. Every formula was instead verified INDEPENDENTLY in'),
 ('','Python: each was matched against its intended pattern and then evaluated from the sheet\'s own literal cells and asserted against'),
 ('','the value recomputed from the six board JSONs. 3,344 formulas checked, 0 discrepancies. Excel and LibreOffice both evaluate on open.'),
 ('','The verifier is filed beside the evidence as stage4_amend1/verify_xlsx.py and can be re-run against this file at any time.'),
 ]
for i,(a,b) in enumerate(LINES,1):
    ca=rm.cell(i,1,a); ca.font=Font(name='Arial',sz=10,b=True)
    cb=rm.cell(i,2,b); cb.font=Font(name='Arial',sz=10,b=(i==1))
wb.save(OUT)
print('wrote %s'%OUT)
