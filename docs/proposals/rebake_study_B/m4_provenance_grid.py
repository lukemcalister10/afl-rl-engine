"""STUDY B / M4 — provenance grid. For every committed store version, enumerate the training-row count
under every plausible switch setting of the build_cond_prior / q97m enumerators, and search for the two
row counts baked into the pinned pickles (cm_400 = 13,226; q97m = 13,111).

The eligibility predicate is the engine's own `p.get('pick') or p.get('_ft')`, with _ft reconstructed from
rl_model.py's derivation (True for ND and RD entry types, False otherwise).
READ-ONLY.
"""
import json, re, subprocess, hashlib, itertools

REPO = '/home/user/afl-rl-engine'
STORE = 'engine/rl_after/rl_model_data.json'
TARGETS = {13226: 'cm_400.pkl', 13111: 'q97m.pkl', 13220: 'cm_150.pkl (workspace, unshipped)'}


def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True).stdout


def grp_of(sha):
    m = re.search(r'^GRP\s*=\s*(\{[^}]*\})', git('show', f'{sha}:engine/rl_after/rl_model.py'), re.M)
    return eval(m.group(1)) if m else {}


def pos_token(p):
    return p.get('drafted_position') if p.get('drafted_position') is not None else p.get('pos')


def debutyr(p):
    return p['year'] if p.get('type') == 'MSD' else p['year'] + 1


def ft(p):
    return p.get('type') in ('ND', 'RD')


def count(data, grp, t1, msd_ex, cut, cap, elig, fo):
    n = 0
    for p in data:
        if not grp.get(pos_token(p)):
            continue
        if debutyr(p) > cut:
            continue
        if elig == 'pick_or_ft':
            if not (p.get('pick') or ft(p)):
                continue
        else:
            if not p.get('pick'):
                continue
        if msd_ex and p.get('type') == 'MSD':
            continue
        d0 = debutyr(p) - 1
        last = max([x['year'] for x in (p.get('scoring') or [])] + [d0])
        n += sum(1 for Y in range(d0, min(last, cap) + 1)
                 if not (t1 and fo is not None and d0 < Y < fo))
    return n


shas = [l.split() for l in git('log', '--format=%H %ad', '--date=short', '--', STORE).strip().splitlines()]
shas.reverse()

HITS = []
TABLE = []
for sha, date in shas:
    blob = git('show', f'{sha}:{STORE}')
    data = json.loads(blob)
    grp = grp_of(sha)
    fo = min([x['year'] for p in data for x in (p.get('scoring') or [])] or [None])
    md5 = hashlib.md5(blob.encode()).hexdigest()
    row = {'sha': sha[:8], 'date': date, 'store_md5_8': md5[:8], 'counts': {}}
    for t1, msd_ex, cut, cap, elig in itertools.product(
            (False, True), (False, True), (2020, 2021), (2025, 2026), ('pick_or_ft', 'pick_only')):
        n = count(data, grp, t1, msd_ex, cut, cap, elig, fo)
        key = f'T1{"on" if t1 else "off"}_MSD{"ex" if msd_ex else "in"}_cut{cut}_cap{cap}_{elig}'
        row['counts'][key] = n
        if n in TARGETS:
            HITS.append({'artifact': TARGETS[n], 'rows': n, 'store_md5_8': md5[:8],
                         'store_sha': sha[:8], 'store_date': date, 'switches': key})
    TABLE.append(row)

print(json.dumps({'targets': {str(k): v for k, v in TARGETS.items()},
                  'hits': HITS, 'table': TABLE}, indent=1, sort_keys=True))
