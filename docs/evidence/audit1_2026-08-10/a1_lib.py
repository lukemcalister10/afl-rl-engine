import json, math, random

SC = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/'
H = 1.0939

def load(f='stage4a1.json'):
    return json.load(open(SC+f))['recs']

def v4(rec):
    """realized no-arb value at career year 4 (index 3); bust/short career -> 0"""
    vp = rec.get('vpath') or []
    if len(vp) >= 4:
        return float(vp[3])
    return 0.0

def f0(rec):
    return v4(rec)/(H**4)/rec['v0']

def pop(recs, y0=2004, y1=2022):
    return [x for x in recs if y0 <= x['year'] <= y1 and x.get('v0')]
