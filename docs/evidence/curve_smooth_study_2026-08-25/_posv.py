#!/usr/bin/env python3
"""The positional rebuild: the 31-F shrunk relativities REUSED (never refitted), then the committed
ORDER-30B stages 1-4 LIFTED BY SOURCE TEXT and exec'd verbatim.  PREREG §3."""
import os, json, hashlib, collections
import _common as C

REFIT_SRC = os.path.join(C.ROOT, 'docs/evidence/one_machinery_2026-08-14/o30b_v0refit.py')
FLOOR = 100.0

# ---- the 30B pipeline, stages 1..4 + the residual disclosure, lifted exactly as 31-F lifts it ----
_src = open(REFIT_SRC).read()
_blk = _src.split("# ---- 1. weighted PAVA, non-increasing ")[1]
_blk = '# ---- 1. weighted PAVA, non-increasing ' + _blk.split('# ---- OUTPUT ')[0]
PIPE_MD5 = hashlib.md5(_blk.encode()).hexdigest()
PIPE_LINES = _blk.count('\n')

# For candidate X the domain runs past 64.  The lifted text hardcodes the floor-plateau anchor as
# `FLOOR + float(64 - p)` -- the endpoint.  PREREG §3.2 declares this ONE re-basing for X and NO edit
# at all for S.  The substitution is applied to the lifted TEXT so it stays auditable.
def pipeline_text(end):
    if end == 64:
        return _blk, 0
    t = _blk.replace('tb[g][p] = FLOOR + float(64 - p)', 'tb[g][p] = FLOOR + float(END - p)')
    return t, (1 if t != _blk else 0)


def shrunk_relativities():
    """The 31-F shrunk relativity rel2, reconstructed ARITHMETICALLY from stored artifact values only.
    No estimator is run; credibility_w is READ from the artifact, not recomputed.  PREREG §3.1."""
    picks = list(range(1, 65))
    relat = {g: {p: C.POSV_RAW[g][p] / C.CURVE_SHIPPED[p] for p in picks} for g in C.POSN}
    w = C.CRED_W
    rel1 = {g: {p: w[g][p] * relat[g][p] + (1.0 - w[g][p]) * 1.0 for p in picks} for g in C.POSN}
    nrm = {p: sum(C.SHARE[g][p] * rel1[g][p] for g in C.POSN) for p in picks}
    rel2 = {g: {p: rel1[g][p] / nrm[p] for p in picks} for g in C.POSN}
    ident = max(abs(sum(C.SHARE[g][p] * rel2[g][p] for g in C.POSN) - 1.0) for p in picks)
    return rel2, relat, ident


def run_pipeline(posv_in, share, curve, picks, end, quiet=True):
    """Execute the lifted 30B stages 1..4 on a supplied surface."""
    text, edits = pipeline_text(end)
    CURVE_TOT = sum(curve[p] for p in picks)

    def ascents_of(tab):
        return [p for p in picks[1:] if tab[p] > tab[p - 1] + 1e-12]

    sink = (lambda s='': None) if quiet else print
    NS = dict(PICKS=picks, POS=C.POSN, posv=posv_in, share=share, curve=curve, CURVE_TOT=CURVE_TOT,
              FLOOR=FLOOR, P=sink, ascents_of=ascents_of,
              asc_in={g: ascents_of(posv_in[g]) for g in C.POSN},
              json=json, collections=collections, END=end)
    exec(text, NS)
    return dict(fin=NS['fin'], LAM=NS['LAM'], resid=NS['resid'], sw_fin=NS['sw_fin'],
                curve_tot=CURVE_TOT, tb=NS['TB_LOG'], joins=NS['JOIN_SHIFTS'],
                pipeline_md5=hashlib.md5(text.encode()).hexdigest(), text_edits=edits)


def extend_relativity(rel2, picks_ext, share_ext):
    """For candidate X the surface must cover picks 65-70, where the artifact's 31-F relativities do
    not exist.  DECLARED CHOICE: carry the pick-64 shrunk relativity FLAT into 65-70 (a hold, not an
    extrapolation), then re-apply the 31-F per-pick renormalisation against the extended share so the
    identity sum_g share_g(p) rel_g(p) = 1 is restored EXACTLY at the new picks too."""
    out = {g: dict(rel2[g]) for g in C.POSN}
    for g in C.POSN:
        for p in picks_ext:
            if p > 64:
                out[g][p] = rel2[g][64]
    for p in picks_ext:
        nrm = sum(share_ext[g][p] * out[g][p] for g in C.POSN)
        for g in C.POSN:
            out[g][p] = out[g][p] / nrm
    return out
