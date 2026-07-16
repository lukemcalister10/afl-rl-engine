#!/usr/bin/env python3
"""Frozen July-8 G-COHORT (verbatim from ship_gates_check.py::_b1_july8): read a walk-forward matrix and
print y4/y5/y6 = SUM[N]/min(SUM[1],SUM[2]); hard gate <= 1.30. Usage: july8.py <matrix.json>"""
import sys,json
import numpy as np
def _b1_july8(mpath):
    _m=json.load(open(mpath)); _S={}
    for _k,_v in _m.items():
        if _k.startswith('__'): continue
        _C=int(_v['year'])
        if not _v['incurve'] or not (2004<=_C<=2020): continue
        for _i in range(len(_v['yrs'])):
            _N=_i+1
            if _N>7: break
            _S[(_C,_N)]=_S.get((_C,_N),0.0)+float(_v['Vpath'][_i] or 0.0)
    _co=sorted({c for c,_ in _S})
    _SUM={N:float(np.mean([_S[(C,N)] for C in _co if (C,N) in _S])) for N in range(1,8) if any((C,N) in _S for C in _co)}
    return _SUM,_co
if __name__=='__main__':
    SUM,co=_b1_july8(sys.argv[1])
    den=min(SUM[1],SUM[2]); ds='y1' if SUM[1]<=SUM[2] else 'y2'
    r={N:SUM[N]/den for N in (4,5,6)}
    sys.stderr.write("JULY-8 (%d classes): "%len(co)+' '.join('y%d=%.1f'%(N,SUM[N]) for N in sorted(SUM))+
        "; den=min(y1,y2)=%s=%.1f | ratios y4=%.4f y5=%.4f y6=%.4f | hard<=1.30: %s\n"
        %(ds,den,r[4],r[5],r[6],'PASS x3' if all(r[N]<=1.30 for N in (4,5,6)) else 'BREACH'))
