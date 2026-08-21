"""STUDY B / M6 — THE DOB COURIER BLAST RADIUS on the fitted estate.

The 2026-08-10 DOB courier (commit 064abca) wrote 302 birth years into the store. Every model fitted
BEFORE it carries a GUESSED age (cp._age_asof / build_peak_model_v4.age_at fall back to
18 + years-since-debut) for those players. This measures how many training rows of each fitted artifact
were taught a guessed age, and by how much the guess was wrong.
READ-ONLY.
"""
import json, subprocess, collections, statistics

REPO = '/home/user/afl-rl-engine'
STORE = 'engine/rl_after/rl_model_data.json'
PRE = '7cbadb5eab84b3f3690d004eb2ece25041ce1abd'   # 2026-08-10 store 0dd6b4a0, the last pre-courier store
POST = 'HEAD'


def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True).stdout


pre = {(p.get('key') or p['player']): p for p in json.loads(git('show', f'{PRE}:{STORE}'))}
post = {(p.get('key') or p['player']): p for p in json.loads(git('show', f'{POST}:{STORE}'))}


def debutyr(p):
    return p['year'] if p.get('type') == 'MSD' else p['year'] + 1


def pos_tok(p):
    return p.get('drafted_position') or p.get('pos')


GRP = {'MID', 'RUCK', 'SF', 'KPF', 'SD', 'KPD'}
courier = [k for k in post if k in pre and pre[k].get('_by') != post[k].get('_by')]

R = {'courier_players': len(courier),
     'pre_store': '0dd6b4a0 (2026-08-10, commit 7cbadb5e)',
     'post_store': 'b745002e (HEAD)'}


def rows_of(p, cut, cap=2026):
    if pos_tok(p) not in GRP:
        return 0, []
    if debutyr(p) > cut:
        return 0, []
    if not (p.get('pick') or p.get('type') in ('ND', 'RD')):
        return 0, []
    d0 = debutyr(p) - 1
    last = max([x['year'] for x in (p.get('scoring') or [])] + [d0])
    ys = list(range(d0, min(last, cap) + 1))
    return len(ys), ys


# --- band model (cm_400 / q97m): training window debut <= 2021 ---
band_rows = band_players = 0
errs = []
for k in courier:
    n, ys = rows_of(post[k], 2021)
    if n:
        band_players += 1
        band_rows += n
        by = post[k].get('_by')
        if by:
            for Y in ys:
                guessed = 18.0 + max(0, Y - (debutyr(post[k]) - 1))
                true_age = Y - by
                errs.append(true_age - guessed)
R['band_model_cm400_q97m'] = {
    'training_window': 'debut <= 2021',
    'courier_players_in_training_pool': band_players,
    'training_rows_taught_a_guessed_age': band_rows,
    'pct_of_13220_row_design': round(100.0 * band_rows / 13220, 2),
    'age_error_years_true_minus_guessed': {
        'n': len(errs),
        'mean': round(statistics.fmean(errs), 3) if errs else None,
        'median': round(statistics.median(errs), 3) if errs else None,
        'min': round(min(errs), 2) if errs else None,
        'max': round(max(errs), 2) if errs else None,
        'pct_off_by_1yr_or_more': round(100.0 * sum(1 for e in errs if abs(e) >= 1.0) / len(errs), 2) if errs else None,
        'pct_off_by_2yr_or_more': round(100.0 * sum(1 for e in errs if abs(e) >= 2.0) / len(errs), 2) if errs else None,
    }}

# --- sibling: peak_model_v4, training window debut 2006-2015 ---
pk_rows = pk_players = 0
for k in courier:
    p = post[k]
    d = debutyr(p)
    if not (2006 <= d <= 2015):
        continue
    if pos_tok(p) not in GRP:
        continue
    ys = [x['year'] for x in (p.get('scoring') or []) if x['games'] > 0]
    if ys:
        pk_players += 1
        pk_rows += 1 + len(set(ys))     # the draft row + one per played season (build_peak_model_v4.build)
R['sibling_peak_model_v4'] = {
    'training_window': 'debut 2006-2015',
    'artifact_committed': '2026-08-05 (dab9657) — five days BEFORE the DOB courier',
    'courier_players_in_training_window': pk_players,
    'training_rows_taught_a_guessed_age_upper_bound': pk_rows,
    '_note': 'build_peak_model_v4.py emits WATCHED_NUMBER_fallback and states it "must fall by EXACTLY '
             'the number of rows the DOB courier writes" — that fall has not been taken: no rebuild of '
             'peak_model_v4.pkl has been committed since the courier landed.'}

# --- how many players still have no birth year at HEAD ---
R['head_store'] = {
    'rows': len(post),
    'missing_birthyear': sum(1 for p in post.values() if not p.get('_by')),
    'missing_birthdate': sum(1 for p in post.values() if not p.get('_bd')),
}
print(json.dumps(R, indent=1, sort_keys=True))
