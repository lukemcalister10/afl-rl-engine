"""ITEM 262 stage-1 proof: the board is byte-identical modulo the vocabulary relabel.

METHOD (stated, as acceptance criterion 3 requires). The new board is normalised by mapping the
six new position codes back to their pre-262 spelling wherever a position label can appear:
  * dict KEYS that are a bare token            (REPL, PEAK, BETA_POS, ...)
  * dict KEYS with a token in ANY pipe-separated component ('3|GEN_DEF' in pm_pos,
    'GEN_DEF|0' in BASEPK_REG)
  * string VALUES that are a bare token        (row 'grp', 'gf', and the label inside 'fut')
Nothing else is touched. The normalised new board is then compared to the baseline board
structurally, every scalar. A single differing number is a finding.
"""
import json, sys
REV={'SD':'GEN_DEF','SF':'GEN_FWD','KPD':'KEY_DEF','KPF':'KEY_FWD','MID':'MID','RUCK':'RUC'}
def norm(o):
    if isinstance(o,dict):
        out={}
        for k,v in o.items():
            nk=k
            if isinstance(k,str):
                if '|' in k:
                    # a token may sit on EITHER side of the pipe: pm_pos uses '<band>|<token>',
                    # BASEPK_REG uses '<token>|<ordinal>'. Map every pipe-separated component.
                    nk='|'.join(REV.get(part,part) for part in k.split('|'))
                elif k in REV: nk=REV[k]
            out[nk]=norm(v)
        return out
    if isinstance(o,list): return [norm(v) for v in o]
    if isinstance(o,str): return REV.get(o,o)
    return o

base=json.load(open('baseline/board_baseline.json'))
new =json.load(open('/home/claude/rl_workspace/rl_after/rl_app_data.json'))
newn=norm(new)

diffs=[]; cells=[0]
def walk(a,b,path):
    if isinstance(a,dict) and isinstance(b,dict):
        if set(a)!=set(b):
            diffs.append((path,'KEY SETS DIFFER',sorted(set(a)^set(b))[:8])); return
        for k in a: walk(a[k],b[k],f'{path}.{k}')
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): diffs.append((path,f'len {len(a)}',f'len {len(b)}')); return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,f'{path}[{i}]')
    else:
        cells[0]+=1
        if a!=b: diffs.append((path,repr(a),repr(b)))
walk(base,newn,'')

print(f'scalar cells compared : {cells[0]}')
print(f'differences           : {len(diffs)}')
for d in diffs[:25]: print('   ',d[0],' baseline=',d[1],' new=',d[2])

# explicit value/rank mover report on the active board
def vmap(bd): return {r['key']:r for r in bd['active']}
A,B=vmap(base),vmap(newn)
print(f'\nactive rows: baseline {len(A)}  new {len(B)}   same key set: {set(A)==set(B)}')
vm=[k for k in A if A[k].get('v')!=B[k].get('v')]
print(f'VALUE movers (field v): {len(vm)}')
for k in vm[:20]: print(f"    {k}: {A[k].get('v')} -> {B[k].get('v')}")
ra=[k for k,_ in sorted(A.items(),key=lambda x:(-x[1].get('v',0),x[0]))]
rb=[k for k,_ in sorted(B.items(),key=lambda x:(-x[1].get('v',0),x[0]))]
rm=[(i,x,y) for i,(x,y) in enumerate(zip(ra,rb)) if x!=y]
print(f'RANK movers (order by v desc, key tiebreak): {len(rm)}')
for i,x,y in rm[:20]: print(f'    rank {i}: {x} -> {y}')
# every numeric field, not just v
numf=set()
for r in base['active']:
    for k,v in r.items():
        if isinstance(v,(int,float)) and not isinstance(v,bool): numf.add(k)
moved={f:sum(1 for k in A if A[k].get(f)!=B[k].get(f)) for f in sorted(numf)}
print('\nper-numeric-field movers across all 804 active rows:')
print('   ', {f:c for f,c in moved.items() if c} or 'NONE — every numeric field identical')
sys.exit(1 if diffs else 0)
