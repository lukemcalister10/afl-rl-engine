#!/usr/bin/env python3
"""Replay captured np.dot operands under whatever kernel the env forces; emit output bits.
Usage: OPENBLAS_CORETYPE=<k> python3 isolate_dot.py <outfile>"""
import sys, pickle, struct
import numpy as np
import math
OUT=sys.argv[1]
cap=pickle.load(open('/tmp/dot_operands.pkl','rb'))
def hx(x): return struct.pack('>d', float(x)).hex()
with open(OUT,'w') as f:
    for site in ('206','910','926'):
        for i,(a,b) in enumerate(cap[site]):
            d=float(np.dot(a,b))
            f.write("%s\t%d\tdot\t%s\n"%(site,i,hx(d)))
