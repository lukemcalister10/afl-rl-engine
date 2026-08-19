#!/usr/bin/env python3
"""INDEPENDENT AUDIT · C4 — THE NO-ARB PAGE vs THE RAW BAND/ARM OUTPUTS.
Every band and ARM row, both windows, five boards; the path-test verdicts RECOMPUTED from the year
paths and the 14%/yr carry rail. Nothing is taken from the page's own prose."""
import json,re,html,os

EV='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audit-wt/docs/evidence/assembly_2026-08-19'
out=[]
def P(s=''):
    print(s); out.append(str(s))

ST=json.load(open(EV+'/STANDING_TABLES_ASM.json'))
BA=json.load(open(EV+'/BANDS_ASM.json'))
CHARGE=ST['charge']
CARRY=[1.140,1.300,1.482,1.689,1.925,2.195,2.502]
P('='*100)
P('INDEPENDENT AUDIT · C4 — THE NO-ARB TABLES')
P('='*100)
P('  carry charge read from the raw output: %.2f/yr'%CHARGE)
P('  carry rail recomputed 1.14^k, k=1..7: %s'%(' '.join('%.3f'%(1.14**k) for k in range(1,8))))
P('  rail as wired in as_tables.py           : %s'%(' '.join('%.3f'%c for c in CARRY)))
P('  rail matches compounding 14%%: %s'%all(abs(CARRY[k-1]-1.14**k)<6e-4 for k in range(1,8)))
P()
P('  boards in the arm tables: %s  (%d — spec: five)'%(ST['labels'],len(ST['labels'])))
P()

# ---- recompute every path-test verdict from the paths ----
def verdict(path):
    beat=[k for k in range(2,min(8,len(path))) if path[k] is not None and path[k]>CARRY[k-1]]
    la=(len(beat)==0)
    p7=path[7] if len(path)>7 else None
    p6=path[6] if len(path)>6 else None
    lb=(p7 is not None and p6 is not None and p7<=p6 and p7<=CARRY[6])
    return dict(limb_a=la,limb_b=lb,both=(la and lb),beat=beat)

P('-'*100)
P('C4 · PATH-TEST VERDICTS RECOMPUTED FROM THE YEAR PATHS AND THE CARRY RAIL')
P('-'*100)
bad=0; n=0
for lab in ST['labels']:
    for cell,pub in sorted(ST['pathtest'].get(lab,{}).items()):
        arm=ST['arms'][lab].get(cell)
        if arm is None:
            P('  %-9s %-16s *** NO ARM ROW FOR A PUBLISHED VERDICT ***'%(lab,cell)); bad+=1; continue
        mine=verdict(arm['path']); n+=1
        same=all(mine[k]==pub[k] for k in ('limb_a','limb_b','both')) and mine['beat']==pub['beat']
        if not same: bad+=1
        P('  %-9s %-16s published a=%-5s b=%-5s both=%-5s beat=%-8s | mine a=%-5s b=%-5s both=%-5s beat=%-8s %s'
          %(lab,cell,pub['limb_a'],pub['limb_b'],pub['both'],pub['beat'],
            mine['limb_a'],mine['limb_b'],mine['both'],mine['beat'],'OK' if same else '*** MISMATCH ***'))
P('  verdicts recomputed: %d   mismatches: %d'%(n,bad))
P()

# ---- every breaching cell must have a published verdict ----
P('-'*100)
P('C4 · IS EVERY BREACHING ARM CELL SCORED? (a breach with no path-test line is a gap)')
P('-'*100)
gap=0
for lab in ST['labels']:
    for cell,arm in sorted(ST['arms'][lab].items()):
        if arm.get('verdict') in ('BUY-RED','SELL-RED') and arm.get('margin') is not None:
            pass
    br=[c for c,a in ST['arms'][lab].items() if a.get('verdict')=='BUY-RED']
    scored=set(ST['pathtest'].get(lab,{}))
    miss=[c for c in br if c not in scored]
    P('  %-9s BUY-RED cells %-2d   scored %-2d   unscored: %s'%(lab,len(br),len(scored),miss or 'none'))
    gap+=len(miss)
P('  unscored breaching cells: %d'%gap)
P()

# ---- the page itself ----
P('-'*100)
P('C4 · THE PAGE (ASSEMBLY_NOARB.html) vs THESE RAW NUMBERS')
P('-'*100)
t=open(EV+'/ASSEMBLY_NOARB.html').read()
rows=[]
for r in re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S):
    c=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r,re.S)]
    if c: rows.append(c)
P('  page table rows: %d'%len(rows))
for lab in ST['labels']:
    P('  board label %-9s appears on the page: %s'%(lab,lab in t))
for w in ('PRIMARY','MODERN'):
    P('  window %-8s appears on the page: %s'%(w,w in t))
P('  MSD exclusion note present: %s'%bool(re.search(r'(?i)MSD',t)))
for m in re.finditer(r'(?i)[^<>]{0,160}MSD[^<>]{0,160}',t):
    P('    NOTE: '+m.group(0).strip()[:220])
    break
# arm cells on the page
armnames=set()
for lab in ST['labels']:
    armnames|=set(k.split('|')[1] for k in ST['arms'][lab])
P('  arm/pool types in the raw output: %s'%sorted(armnames))
missing=[a for a in sorted(armnames) if a not in t]
P('  arm types NOT found anywhere on the page: %s'%(missing or 'none'))
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/auditpkg/AUD_NOARB_out.txt','w').write('\n'.join(out))
