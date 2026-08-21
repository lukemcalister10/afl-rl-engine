"""STUDY B / M3 — WHICH STORE FITTED cm_400.pkl?

Replays the training-ROW ENUMERATION over every committed version of engine/rl_after/rl_model_data.json
and looks for the version whose count equals the 13,226 rows measured inside the pinned pickle
(and 13,111 for q97m). Also measures per-store input drift against the current store b745002e.

Handles BOTH store schemas:
  pre  2026-07-05 : single 'pos' token + probabilistic dual-position '_fut' list
  post 2026-07-05 : 'drafted_position' / 'present_position' / 'future_position' (the DPP STRIP)
READ-ONLY: git show into memory only.
"""
import json, os, re, subprocess, hashlib, collections

REPO = '/home/user/afl-rl-engine'
STORE = 'engine/rl_after/rl_model_data.json'
NORM = {'GEN_DEF': 'SD', 'GEN_FWD': 'SF', 'KEY_DEF': 'KPD', 'KEY_FWD': 'KPF', 'RUC': 'RUCK',
        'MID': 'MID', 'SD': 'SD', 'SF': 'SF', 'KPD': 'KPD', 'KPF': 'KPF', 'RUCK': 'RUCK'}


def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True).stdout


def grp_of(sha):
    src = git('show', f'{sha}:engine/rl_after/rl_model.py')
    m = re.search(r'^GRP\s*=\s*(\{[^}]*\})', src, re.M)
    return (eval(m.group(1)) if m else {})


def code_of(sha):
    src = git('show', f'{sha}:engine/forward_valuation/conditional_prior.py')
    m = re.search(r'^GROUPS\s*=\s*(\[[^\]]*\])', src, re.M)
    return (eval(m.group(1)) if m else None), ('_FIRST_OBS' in src)


def pos_token(p):
    """The token that becomes p['pos'] under whichever schema this store record uses."""
    return p.get('drafted_position') if p.get('drafted_position') is not None else p.get('pos')


def gfut_token(p):
    """The token that drives the POSITION ONE-HOT of the band feature vector, per schema."""
    if p.get('future_position') is not None:
        return p['future_position']
    if p.get('present_position') is not None:
        return p['present_position']
    f = p.get('_fut')
    if f:
        try:
            return max(f, key=lambda x: x[1])[0]
        except Exception:
            pass
    return p.get('pos')


def debutyr(p):
    return p['year'] if p.get('type') == 'MSD' else p['year'] + 1


def enumerate_rows(data, grp, first_obs=None, excl_msd=False, resolved_cut=2021, cap=2026):
    n = players = 0
    for p in data:
        if not grp.get(pos_token(p)):
            continue
        if debutyr(p) > resolved_cut:
            continue
        if not (p.get('pick') or p.get('_ft')):
            continue
        if excl_msd and p.get('type') == 'MSD':
            continue
        d0 = debutyr(p) - 1
        last = max([x['year'] for x in (p.get('scoring') or [])] + [d0])
        c = sum(1 for Y in range(d0, min(last, cap) + 1)
                if not (first_obs is not None and d0 < Y < first_obs))
        n += c
        players += 1 if c else 0
    return n, players


CUR = json.loads(git('show', f'HEAD:{STORE}'))
CUR_BY_KEY = {(p.get('key') or p.get('player')): p for p in CUR}

shas = [l.split() for l in git('log', '--format=%H %ad', '--date=short', '--', STORE).strip().splitlines()]
shas.reverse()

OUT = {'_doc': 'STUDY B M3 store sweep. Target row counts read out of the pinned pickles in M1.',
       'target_cm400_rows': 13226, 'target_q97m_rows': 13111, 'stores': []}

for sha, date in shas:
    blob = git('show', f'{sha}:{STORE}')
    data = json.loads(blob)
    grp = grp_of(sha)
    groups, has_t1 = code_of(sha)
    fo = min([x['year'] for p in data for x in (p.get('scoring') or [])] or [None])
    off_in, pl = enumerate_rows(data, grp)
    on_in, _ = enumerate_rows(data, grp, first_obs=fo)
    off_ex, _ = enumerate_rows(data, grp, excl_msd=True)
    on_ex, _ = enumerate_rows(data, grp, first_obs=fo, excl_msd=True)
    schema = 'DPP_STRIP_3col' if any(p.get('drafted_position') is not None for p in data) else 'legacy_pos_plus_fut'

    posch = pickch = bych = scch = onehotch = 0
    both = 0
    for p in data:
        c = CUR_BY_KEY.get(p.get('key') or p.get('player'))
        if c is None:
            continue
        both += 1
        if NORM.get(grp.get(pos_token(p))) != NORM.get(pos_token(c)):
            posch += 1
        if NORM.get(grp.get(gfut_token(p)) or gfut_token(p)) != NORM.get(gfut_token(c)):
            onehotch += 1
        if p.get('pick') != c.get('pick'):
            pickch += 1
        if p.get('_by') != c.get('_by'):
            bych += 1
        if json.dumps(p.get('scoring'), sort_keys=True) != json.dumps(c.get('scoring'), sort_keys=True):
            scch += 1

    OUT['stores'].append({
        'sha': sha[:8], 'date': date,
        'store_md5': hashlib.md5(blob.encode()).hexdigest(),
        'store_rows': len(data), 'schema': schema,
        'first_observable_season': fo,
        'code_GROUPS': groups, 'code_has_T1_dropfix': has_t1,
        'code_pos_vocab': sorted(grp),
        'train_rows': {'T1off_MSDin': off_in, 'T1on_MSDin': on_in,
                       'T1off_MSDex': off_ex, 'T1on_MSDex': on_ex},
        'train_players': pl,
        'MATCHES_cm400_13226': 13226 in (off_in, on_in, off_ex, on_ex),
        'MATCHES_q97m_13111': 13111 in (off_in, on_in, off_ex, on_ex),
        'drift_vs_current_b745002e': {
            'players_in_both': both, 'players_absent_from_current': len(data) - both,
            'draft_position_group_changed': posch,
            'band_onehot_position_changed': onehotch,
            'pick_changed': pickch, 'birthyear_changed': bych, 'scoring_changed': scch},
    })

print(json.dumps(OUT, indent=1, sort_keys=True))
