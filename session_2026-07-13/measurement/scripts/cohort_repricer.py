"""Cohort walk-forward re-pricer that MIRRORS s4_matrix_M1v7.py's per-(p,Y) setup, so my value at
default capt == the official matrix Vpath (validated). Used for the D4.4 capt sensitivity ladder via a
DELTA on the official baseline sums."""
import io, contextlib, copy, json
import harness as H
MA = H.MA; cp = H.cp; ev = H.ev; G = H.G

def price_asof(p, Y):
    """== s4_matrix ASOF[(id(p),Y)] : truncate scoring<=Y, neutralise retirement as-of Y, BOARD_PATH iff Y==2026."""
    q = copy.deepcopy(p)
    LL = q.get('_last_listed'); RET = q.get('_retired')
    lastscore = max((r['year'] for r in q['scoring']), default=0)
    q['scoring'] = [r for r in q['scoring'] if r['year'] <= Y]
    eff_last = LL if LL is not None else (lastscore if RET else None)
    q['_retired'] = False
    q['_last_listed'] = eff_last if (eff_last is not None and eff_last < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    G['_BOARD_PATH'] = (Y == 2026)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return float(ev(q, Y))
    except Exception:
        return None
    finally:
        MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear(); G['_BOARD_PATH'] = True

def cohort_cells(matrix_path):
    """returns list of (key, C, N, year, Vpath_matrix) for incurve 2004-2020, depths 1-7."""
    m = json.load(open(matrix_path)); cells = []
    for k, v in m.items():
        if k.startswith('__'): continue
        C = int(v['year'])
        if not v['incurve'] or not (2004 <= C <= 2020): continue
        for i, y in enumerate(v['yrs']):
            N = i + 1
            if N > 7: break
            cells.append((v.get('key'), C, N, y, float(v['Vpath'][i] or 0.0)))
    return cells

def sums_from(triples):
    """triples: list of (C,N,value) -> figure(N)=mean over classes-observed-at-N of class-sum; ratios."""
    import numpy as np
    S = {}
    for C, N, val in triples:
        S[(C, N)] = S.get((C, N), 0.0) + (val or 0.0)
    co = sorted({C for C, _ in S})
    figure = {N: float(np.mean([S[(C, N)] for C in co if (C, N) in S]))
              for N in range(1, 8) if any((C, N) in S for C in co)}
    denom = min(figure[1], figure[2])
    return figure, denom, {N: figure[N] / denom for N in figure}, co
