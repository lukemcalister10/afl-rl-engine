#!/usr/bin/env python3
"""INDEPENDENT AUDIT — C1 (the tracker) and C2 (the per-lever page) re-derived from the boards'
own JSON. Nothing is read from the packet. Written by the AUDIT seat; fixes nothing."""
import json, os, re, html, hashlib, csv, sys

SP='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM=SP+'/asm'
EV='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audit-wt/docs/evidence/assembly_2026-08-19'
ORDER=['IDENT_P','IDENT_K','L0_R','L1_REC','L2_COMP','V750_L2C15','V750_L3MAT','V750_L4SD',
       'V750_L5A','V750_L5B','V750_L5C','V751_CAND','V751_CAND2']
PATHS={}
for t in ORDER:
    q='%s/bb_%s/rl_after/rl_app_data.json'%(ASM,t)
    if os.path.exists(q): PATHS[t]=q
_live=SP+'/o29r/seal/rl_after/rl_app_data.json'
if os.path.exists(_live): PATHS['live']=_live
MD5={t:hashlib.md5(open(q,'rb').read()).hexdigest() for t,q in PATHS.items()}
B={t:{r['key']:r for r in json.load(open(q))['active']} for t,q in PATHS.items()}
V={t:{k:r['v'] for k,r in B[t].items()} for t in B}
TOT={t:sum(V[t].values()) for t in V}
NAME={}
for t in ('V751_CAND','L0_R','IDENT_P','live'):
    for k,r in B.get(t,{}).items(): NAME.setdefault(k,r.get('name') or k)

out=[]
def P(s=''):
    print(s); out.append(str(s))

P('='*100)
P('INDEPENDENT AUDIT · C1 THE TRACKER and C2 THE PER-LEVER PAGE — re-derived from the board JSONs')
P('='*100)
P()
P('Board md5s as read by THIS seat (not copied from any document):')
for t in ORDER+(['live'] if 'live' in MD5 else []):
    P('  %-12s %s  total %s'%(t,MD5.get(t,'MISSING'),'{:,}'.format(TOT[t]) if t in TOT else '-'))
P()

# ---------------- C2 · TELESCOPING ----------------
P('-'*100)
P('C2 · DOES THE LEVER STACK TELESCOPE?  R + sum(marginals) must EQUAL the candidate total exactly.')
P('-'*100)
CHAIN=[('L1_REC','L0_R'),('L2_COMP','L1_REC'),('V750_L2C15','L2_COMP'),('V750_L3MAT','V750_L2C15'),
       ('V750_L4SD','V750_L3MAT'),('V750_L5A','V750_L4SD'),('V750_L5B','V750_L5A'),
       ('V750_L5C','V750_L5B'),('V751_CAND','V750_L5C')]
s=0; rows=[]
for cur,prev in CHAIN:
    m=TOT[cur]-TOT[prev]; s+=m
    moved=sum(1 for k in V[cur] if V[cur][k]!=V[prev].get(k))
    up=sum(1 for k in V[cur] if V[cur][k]>V[prev].get(k,V[cur][k]))
    dn=sum(1 for k in V[cur] if V[cur][k]<V[prev].get(k,V[cur][k]))
    rows.append((cur,m,moved,up,dn))
    P('  %-12s marginal %+8d   moved %4d   up %4d   down %4d'%(cur,m,moved,up,dn))
P()
P('  R (L0_R)            = %s'%'{:,}'.format(TOT['L0_R']))
P('  sum of marginals    = %+d'%s)
P('  R + sum             = %s'%'{:,}'.format(TOT['L0_R']+s))
P('  candidate V751_CAND = %s'%'{:,}'.format(TOT['V751_CAND']))
P('  TELESCOPES EXACTLY: %s'%(TOT['L0_R']+s==TOT['V751_CAND']))
P()

# compare against the per-lever HTML page
P('-'*100)
P('C2 · THE PER-LEVER PAGE vs THESE RE-DERIVED NUMBERS')
P('-'*100)
lt=open(EV+'/LEVERS_ASSEMBLY.html').read()
trs=re.findall(r'<tr>(.*?)</tr>',lt,re.S)
page=[]
for r in trs:
    c=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r,re.S)]
    if len(c)==8 and re.match(r'^[0-9a-f]{8}$',c[1] or ''): page.append(c)
MAP={'b692d709':'L1_REC','c3cb6686':'L2_COMP','3dca39b0':'V750_L2C15','62507bdf':'V750_L3MAT',
     'c3f78667':'V750_L4SD','e1e3d97d':'V750_L5A','b74a2a0e':'V750_L5B','1270991c':'V750_L5C',
     'fbf61d05':'V751_CAND','7f88f509':'L0_R'}
def num(x):
    x=x.replace(',','').replace('+','').replace('−','-').replace('–','-')
    try: return int(x)
    except: return None
bad=0
for c in page:
    t=MAP.get(c[1])
    if t is None: continue
    ptot=num(c[2]); pmarg=num(c[3]); pmoved=num(c[4]); pup=num(c[5]); pdn=num(c[6])
    rtot=TOT.get(t)
    rr=[x for x in rows if x[0]==t]
    ok_t = (ptot==rtot)
    line='  %-12s page_total %-9s mine %-9s %s'%(t,'{:,}'.format(ptot) if ptot is not None else '?','{:,}'.format(rtot),'OK' if ok_t else '*** MISMATCH ***')
    if not ok_t: bad+=1
    if rr:
        _,m,moved,up,dn=rr[0]
        for lbl,pv,mv in (('marg',pmarg,m),('moved',pmoved,moved),('up',pup,up),('down',pdn,dn)):
            if pv!=mv:
                line+='\n      %s page=%s mine=%s *** MISMATCH ***'%(lbl,pv,mv); bad+=1
    P(line)
P('  PER-LEVER PAGE MISMATCHES: %d'%bad)
P()

# ---------------- C2 · named movers for two levers ----------------
P('-'*100)
P('C2 · NAMED MOVERS RE-DERIVED for TWO levers (read from the lever boards, nothing rebuilt)')
P('-'*100)
def movers(cur,prev,n=10):
    d=[(V[cur][k]-V[prev].get(k,V[cur][k]),k) for k in V[cur] if V[cur][k]!=V[prev].get(k)]
    d.sort(key=lambda x:-abs(x[0]))
    return d[:n]
for cur,prev,lbl in (('V750_L4SD','V750_L3MAT','the SD level offset'),
                     ('V751_CAND','V750_L5C','the R3 production fade')):
    P('  LEVER: %s  (%s vs %s)'%(lbl,cur,prev))
    for dv,k in movers(cur,prev):
        P('     %-28s %-24s %6d -> %6d  %+d'%(k,NAME.get(k,'?'),V[prev].get(k),V[cur][k],dv))
    P()

# ---------------- C1 · THE TRACKER ----------------
P('-'*100)
P('C1 · THE TRACKER — CSV and HTML re-verified against the board JSONs')
P('-'*100)
rdr=list(csv.DictReader(open(EV+'/TRACKER_ASSEMBLY.csv')))
P('  CSV rows: %d'%len(rdr))
P('  CSV columns: %s'%(', '.join(rdr[0].keys()) if rdr else 'NONE'))
P()

# name -> key map for the tracker cross-check
N2K={}
for k,n in NAME.items(): N2K.setdefault(n,k)

def gv(t,k):
    return V[t].get(k)

COLS=[('live','live'),('K','IDENT_K'),('P','IDENT_P'),('R','L0_R'),('candidate','V751_CAND')]
DELTAS=[('d_live_K','IDENT_K','live'),('d_K_P','IDENT_P','IDENT_K'),('d_P_R','L0_R','IDENT_P'),
        ('d_R_cand','V751_CAND','L0_R'),('d_live_cand','V751_CAND','live'),('d_K_cand','V751_CAND','IDENT_K')]

def pnum(x):
    if x is None: return None
    x=str(x).strip().replace(',','').replace('+','').replace('−','-').replace('–','-')
    if x in ('','-','—','–'): return None
    try: return int(x)
    except: return None

P('  Verifying EVERY CSV row (values in all five board columns + ALL SIX delta columns):')
badv=0; badd=0; nokey=0; checked=0
examples=[]
for r in rdr:
    k=N2K.get(r['player'])
    if k is None: nokey+=1; continue
    checked+=1
    for cname,t in COLS:
        want=gv(t,k); got=pnum(r.get(cname))
        if want is None and got is None: continue
        if want!=got:
            badv+=1
            if len(examples)<12: examples.append('VALUE %s / %s: csv=%s board=%s'%(r['player'],cname,got,want))
    for dname,a,b in DELTAS:
        wa=gv(a,k); wb=gv(b,k)
        want=(wa-wb) if (wa is not None and wb is not None) else None
        got=pnum(r.get(dname))
        if want is None and got is None: continue
        if want!=got:
            badd+=1
            if len(examples)<12: examples.append('DELTA %s / %s: csv=%s board=%s'%(r['player'],dname,got,want))
P('    rows checked %d   (unmatched player names: %d)'%(checked,nokey))
P('    VALUE cell mismatches : %d'%badv)
P('    DELTA cell mismatches : %d'%badd)
for e in examples: P('      '+e)
P()

# --- the HTML: does it carry all six delta columns, and do its numbers agree with the CSV?
ht=open(EV+'/TRACKER_ASSEMBLY.html').read()
hdr=re.findall(r'<th[^>]*>(.*?)</th>',ht,re.S)
hdrs=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in hdr]
P('  TRACKER HTML header cells: %s'%hdrs)
P()
trs=re.findall(r'<tr[^>]*>(.*?)</tr>',ht,re.S)
hrows=[]
for r in trs:
    c=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)]
    if c: hrows.append(c)
P('  TRACKER HTML data rows: %d  (CSV rows: %d)'%(len(hrows),len(rdr)))
if hrows:
    P('  HTML first data row cells (%d): %s'%(len(hrows[0]),hrows[0]))
P()
# totals in the header
P('  Board totals quoted in the HTML header, vs my own sums:')
for t,lbl in (('live','live'),('IDENT_K','K'),('IDENT_P','P'),('L0_R','R'),('V751_CAND','cand')):
    tot='{:,}'.format(TOT[t])
    P('    %-6s %-9s present in HTML: %s'%(lbl,tot,tot in ht))
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/auditpkg/AUD_DOCS_out.txt','w').write('\n'.join(out))
