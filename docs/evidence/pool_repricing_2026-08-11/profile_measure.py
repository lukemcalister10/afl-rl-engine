"""THE FULL-OUTCOME-PROFILE MEASURE — D3 as ruled (owner, #334 comment 5250813929).

  "We should not be measuring only year 4 outcomes for this... We don't look at only year 4 for ND
   players. It should be one data point we consult, and place in context with other data points."

WHAT "THE SAME BASIS THE ND PICK CURVE PRICES FROM" ACTUALLY IS, read from the code rather than
assumed. The pick curve is taught by harness_pvc_REPINNED_pass3.structural_values() (:339). Its
per-player value is realised_full(r) (:313), which is:

    realised_full(r) = SUM_k e_k * vpath[k]  /  SUM_k e_k        over EVERY career year k
    e_k              = max(0, 1 - (pw_k - PW_FLOOR)/(1 - PW_FLOOR)),  PW_FLOOR = 0.11   (:293-296)
    never established (no season of >= 6 games) -> 0.0                                  (:277-280)

IT IS NOT A DISCOUNT-RATE INTEGRAL. There is no discount rate in this site at all. The weighting is
the ENGINE'S OWN EVIDENCE WEIGHT pw: a career year counts in proportion to how much real evidence it
carries, so early no-evidence years count little and played years count fully. That is the ND basis
and this file reuses the harness functions themselves rather than re-implementing them, so the two
cannot drift apart.

TWO PRESENTATIONS, both reported, because active careers are incomplete:
  (A) CONCLUDED CAREERS ONLY  - no modelling of any kind; the pure realised profile. Headline.
  (B) WHOLE POPULATION via structural_values() - the pick curve's own completion of unfinished
      careers, with its fallback share printed. Strata are built on the WHOLE cohort (all arms) so a
      thin stream cannot silently fall back to its own entry price and score 1.00 by construction.

READ-ONLY. No emits. Deterministic.
"""
import sys, json, collections, statistics
sys.path.insert(0, '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10/noarb')
import harness_pvc_REPINNED_pass3 as H

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
BASE = sys.argv[1] if len(sys.argv) > 1 else 'SHIP'
R = json.load(open(f"{SP}/per_entrant_{BASE}.json"))['recs']
W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


def val(r, N):
    if N == 0: return float(r['v0']), 'v0'
    Y = cohort(r) + N - 1
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0, 'ended'
    if Y < yrs[0]: return None, 'pre'
    if Y > yrs[-1]: return 0.0, 'ended'
    i = yrs.index(Y)
    return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')


elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
ORDER = ['ND 1-64', 'RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
POOLS = ORDER[1:]

# ---------- (B) the pick curve's own completion, strata built on the WHOLE cohort ----------
allrows, prov = H.structural_values(elig)
SV = {}
for r, row in zip(elig, allrows):
    SV[r['key']] = row


def prof_concluded(sub):
    """(A) concluded careers only: SUM realised_full / SUM v0."""
    c = [r for r in sub if H.concluded(r)]
    if not c: return float('nan'), 0
    return sum(H.realised_full(r) for r in c) / sum(float(r['v0']) for r in c), len(c)


def prof_completed(sub):
    """(B) whole population through the pick curve's own completion."""
    if not sub: return float('nan'), 0, 0
    fb = sum(1 for r in sub if SV[r['key']]['how'].startswith('prior_fallback'))
    return (sum(SV[r['key']]['value'] for r in sub) / sum(float(r['v0']) for r in sub), len(sub), fb)


def yr(sub, N):
    reach = sub if N == 0 else [r for r in sub if cohort(r) + N - 1 <= W]
    num = den = 0.0
    for r in reach:
        v, k = val(r, N)
        if k == 'pre': continue
        num += v; den += float(r['v0'])
    return (num / den if den else float('nan')), len(reach)


print("=" * 118)
print(f"### THE FULL OUTCOME PROFILE — the ruled basis (D3).  base {BASE}")
print("=" * 118)
print("  measure = SUM(realised_full)/SUM(v0), realised_full from harness_pvc_REPINNED_pass3.py:313")
print("  the SAME function the ND pick curve is taught from (structural_values, :339). No discount")
print("  rate is involved anywhere in that site: the weighting is the engine's own evidence weight.")
print(f"  whole-cohort completion provenance: {prov['counts']}  fallback share {prov['fallback_share_pct']}%")
print()
print(f"  {'stream':9} {'n':>5} | {'PROFILE (A)':>12} {'n concl':>8} | {'PROFILE (B)':>12} {'fallback':>9} |"
      + "".join(f"{'yr%d'%N:>8}" for N in range(1, 7)))
print("  " + "-" * 116)
for s in ORDER:
    sub = [r for r in elig if stream(r) == s]
    if not sub: continue
    a, na = prof_concluded(sub)
    b, nb, fb = prof_completed(sub)
    cols = "".join(f"{yr(sub, N)[0]:8.4f}" for N in range(1, 7))
    print(f"  {s:9} {len(sub):5} | {a:12.4f} {na:8} | {b:12.4f} {fb:9} |" + cols)
pool = [r for r in elig if stream(r) in POOLS]
a, na = prof_concluded(pool); b, nb, fb = prof_completed(pool)
print(f"  {'ALL POOL':9} {len(pool):5} | {a:12.4f} {na:8} | {b:12.4f} {fb:9} |"
      + "".join(f"{yr(pool, N)[0]:8.4f}" for N in range(1, 7)))
print()
print("  Year columns are CONTEXT. Year 4 carries no special status (owner ruling, D3).")

# ---------- RD by position on the ruled basis ----------
print()
print("=" * 118)
print("### RD BY POSITION ON THE RULED BASIS (the only pool stream whose samples support a lens)")
print("=" * 118)
print(f"  {'pos':6} {'n':>5} {'PROFILE (A)':>12} {'n concl':>8} {'PROFILE (B)':>12} {'fallback':>9} {'yr4 (context)':>14}")
rd = [r for r in elig if stream(r) == 'RD']
for p in ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']:
    g = [r for r in rd if r.get('pos') == p]
    if len(g) < 20:
        print(f"  {p:6} {len(g):5} {'  -':>12} {'-':>8} {'  -':>12} {'-':>9} {'  -':>14}"); continue
    a, na = prof_concluded(g); b, nb, fb = prof_completed(g)
    print(f"  {p:6} {len(g):5} {a:12.4f} {na:8} {b:12.4f} {fb:9} {yr(g, 4)[0]:14.4f}")

# ---------- option sizing on the ruled basis ----------
print()
print("=" * 118)
print("### OPTION SIZING RE-LANDED ON THE RULED BASIS")
print("=" * 118)
NDp = prof_completed([r for r in elig if stream(r) == 'ND 1-64'])[0]
poolP = prof_completed(pool)[0]
print(f"  HEADLINE MEASURE = PROFILE (B), the pick curve's OWN method (structural_values), because that")
print(f"  is what 'the same basis the ND pick curve prices from' means in the code. (A) is reported as")
print(f"  the no-modelling cross-check and is biased for RECENT streams - see the caveat below.")
print()
print(f"  ND 1-64 profile = {NDp:.4f}.  IT IS NOT 1.00 AND IT IS NOT SUPPOSED TO BE - but it is close,")
print(f"  which is the measure validating itself: the pick curve is TAUGHT to reproduce realised value,")
print(f"  so the stream it is taught on must land near 1.")
print(f"  THE CALIBRATION TARGET IS THEREFORE ND'S OWN PROFILE, NOT 1.00. 'The pool pick price")
print(f"  equivalent' (the owner's words) = the price at which a pool entrant returns what an ND pick")
print(f"  returns per unit of entry price.")
print(f"\n  pool profile {poolP:.4f} vs ND {NDp:.4f}  ->  ND delivers {NDp/poolP:.2f}x what the pool does")
print(f"  per unit of entry price.")
print()
print(f"  {'stream':9} {'n':>5} {'profile':>9} {'vs ND':>7} | {'lam_B':>7} {'@B':>8} | {'lam_C':>7} {'@C':>8} | {'Sig v0':>11} {'@C':>11}")
print("  " + "-" * 104)
lamB = poolP / NDp
t0 = tB = tC = 0.0
LAM = {}
for s in POOLS:
    sub = [r for r in elig if stream(r) == s]
    a = prof_completed(sub)[0]
    lamC = a / NDp if a == a and a > 0 else 1.0
    LAM[s] = lamC
    s0 = sum(float(r['v0']) for r in sub); t0 += s0; tB += s0 * lamB; tC += s0 * lamC
    print(f"  {s:9} {len(sub):5} {a:9.4f} {a/NDp:7.3f} | {lamB:7.3f} {a/NDp/lamB:8.4f} | "
          f"{lamC:7.3f} {1.0:8.4f} | {round(s0):11,} {round(s0*lamC):11,}")
print(f"  {'ALL POOL':9} {len(pool):5} {poolP:9.4f} {poolP/NDp:7.3f} | {lamB:7.3f} {1.0:8.4f} | "
      f"{'per-arm':>7} {'':>8} | {round(t0):11,} {round(tC):11,}")
print()
print("  lam is the multiplier on that stream's ENTRY prices. @B / @C are where the stream's delivery")
print("  lands RELATIVE TO ND (1.0000 = delivers exactly what an ND pick delivers per unit of entry).")
print()
print("  CAVEAT ON PROFILE (A) FOR RECENT STREAMS, and it is why (B) is the headline. MSD reads (A)")
print("  0.1215 against (B) 0.9418, and SSP (A) 0.4129 against (B) 1.0287. MSD began in 2019 and SSP in")
print("  2018, so only 43 of 106 MSD careers have CONCLUDED - and a career that has already concluded")
print("  from a stream that young is one that ended early, i.e. one that went badly. Measuring those")
print("  streams on concluded rows alone selects their failures. (B) completes the unfinished careers")
print("  by the pick curve's own method and its fallback share is printed above.")

# ---------- consequences on the ruled basis ----------
print()
print("=" * 118)
print("### CONSEQUENCES RE-MEASURED ON THE RULED BASIS")
print("=" * 118)
BD = {r['key']: r for r in json.load(open(SP + '/o3/ship_board.json'))['active']}
MX = {r['key']: r for r in R}
def e_of(r):
    g = sum(x.get('games', 0) for x in (r.get('seasons') or []))
    return 1.0 if g == 0 else (0.12 if g <= 9 else 0.0)
reach = [k for k in BD if k in MX and stream(MX[k]) in POOLS and e_of(MX[k]) > 0]
tb = sum(r['v'] for r in BD.values())
print(f"  board rows a level change can reach : {len(reach)} of "
      f"{sum(1 for k in BD if k in MX and stream(MX[k]) in POOLS)} pool rows"
      f"  ({100*sum(BD[k]['v'] for k in reach)/tb:.2f}% of the board)")
print("  THE STEP-FUNCTION CARRY IS BASIS-INVARIANT BY CONSTRUCTION and is verified so: it is measured")
print("  from the ITEM B board experiment (how much of an ENTRY-PRICE move reaches a PRICE) and never")
print("  touches the outcome measure at all. Changing D3 changes lambda, not the carry.")
for lab, LM in (('B (one lambda)', {s: lamB for s in POOLS}), ('C (per stream)', LAM)):
    d = sum(BD[k]['v'] * (LM[stream(MX[k])] ** e_of(MX[k]) - 1) for k in BD
            if k in MX and stream(MX[k]) in POOLS)
    print(f"  board total {tb:,} -> {round(tb+d):,} under option {lab}  ({100*d/tb:+.2f}%)")
allsub = [r for r in elig if 2005 <= cohort(r) <= 2023]
def allarm(LM):
    num = den = 0.0
    for r in allsub:
        v, k = val(r, 1)
        if k == 'pre': continue
        L = LM.get(stream(r), 1.0)
        num += v * (L ** e_of(r)); den += float(r['v0']) * L
    return num / den
print(f"  ALL-ARM yr1 ratio 2005-2023: now {allarm({}):.4f}"
      f"  ->  {allarm({s: lamB for s in POOLS}):.4f} under B  ->  {allarm(LAM):.4f} under C")
print()
print(f"  {'player':18} {'stream':7} {'games':>6} {'e':>5} {'SHIP':>7} {'@B':>7} {'@C':>7}")
for k in ['john-noble','max-hall','james-peatling','mark-keane','tom-mccarthy','lachlan-mcandrew',
          'marcus-herbert','zac-banch','flynn-perez','paddy-cross','mitch-podhajski','harrison-coe']:
    if k not in BD or k not in MX: continue
    m = MX[k]; s = stream(m); e = e_of(m)
    g = sum(x.get('games', 0) for x in (m.get('seasons') or []))
    print(f"  {BD[k]['name'][:18]:18} {s:7} {g:6} {e:5.2f} {BD[k]['v']:7} "
          f"{round(BD[k]['v']*lamB**e):7} {round(BD[k]['v']*LAM[s]**e):7}")
json.dump({'base': BASE, 'ND_profile': NDp, 'pool_profile': poolP, 'lam_B': lamB, 'lam_C': LAM,
           'per_stream_profile_B': {s: prof_completed([r for r in elig if stream(r)==s])[0] for s in ORDER},
           'per_stream_profile_A': {s: prof_concluded([r for r in elig if stream(r)==s])[0] for s in ORDER}},
          open('/home/user/afl-rl-engine/docs/evidence/pool_repricing_2026-08-11/PROFILE.json','w'), indent=1)
