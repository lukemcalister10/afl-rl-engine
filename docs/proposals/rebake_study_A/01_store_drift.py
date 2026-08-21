"""STORE DRIFT — what the (unstamped) fit-era store said vs what the current store says,
restricted to the attributes the band's training rows actually read.

The band pickles carry NO training-store stamp, so the fit-era store is not RECORDED anywhere.
The best available proxy is the store at the commit that seeded the pickle into the repo
(f4a4d34, "Initial verified seed: final checkpoint 2026-07-02"), which is also the last commit
that touched data/cm_400.pkl. That is a PROXY, not a proof, and it is labelled as such.

READ-ONLY. Writes only into the scratch dir.
"""
import json, os, sys, collections

S = os.path.dirname(os.path.abspath(__file__))
OLD = json.load(open(os.path.join(S, 'out', 'store_fitera.json')))
NEW = json.load(open('/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json'))

out = {}
out['n_old'] = len(OLD)
out['n_new'] = len(NEW)
out['keys_old'] = sorted(OLD[0].keys())
out['keys_new'] = sorted(NEW[0].keys())
out['keys_added'] = sorted(set(NEW[0].keys()) - set(OLD[0].keys()))
out['keys_removed'] = sorted(set(OLD[0].keys()) - set(NEW[0].keys()))


def ident(p):
    """Join key. stable_player_id is the migration-era identity; fall back to name+year."""
    sid = p.get('stable_player_id')
    if sid:
        return ('sid', str(sid))
    return ('nm', (p.get('player') or '').strip().lower(), p.get('year'))


O = {}
for p in OLD:
    O.setdefault(ident(p), p)
N = {}
for p in NEW:
    N.setdefault(ident(p), p)

# name+year fallback index so a sid-only match failure can still be resolved
O_nm = {}
for p in OLD:
    O_nm.setdefault(((p.get('player') or '').strip().lower(), p.get('year')), p)


def old_for(p):
    k = ident(p)
    if k in O:
        return O[k]
    return O_nm.get(((p.get('player') or '').strip().lower(), p.get('year')))


matched = 0
unmatched = []
for p in NEW:
    if old_for(p) is not None:
        matched += 1
    else:
        unmatched.append(p.get('player'))
out['matched'] = matched
out['unmatched_new_rows'] = len(unmatched)
out['unmatched_sample'] = unmatched[:15]

# ---------- the attributes a training row actually reads ----------
# _feat(p,Y) = onehot(gfut(p)) + [log(min(effpk,70)), _exposure(p,Y), tenure, _lvl_eff(p,Y), _age_asof(p,Y)]
#   gfut      <- future_position (new) / raw_multipos-derived pos (old)
#   effpk     <- pick + type  (the ND<=64 / pool split)
#   exposure, lvl_eff <- scoring[] rows (year, games, avg)
#   age       <- _bd (date of birth)
#   tenure, and the row's very existence <- year + type (debutyr)
# target fwd_best3_from  <- scoring[] rows

def pos_old(p):
    # the pre-DPP-strip store: raw_multipos / position column
    for k in ('drafted_position', 'position', 'pos'):
        if p.get(k):
            return p[k]
    rm = p.get('raw_multipos')
    if isinstance(rm, str):
        return rm.split('/')[0].strip()
    return None


def pos_new(p):
    return p.get('drafted_position')


def futpos_new(p):
    return p.get('future_position') or p.get('present_position') or p.get('drafted_position')


drift = collections.Counter()
examples = collections.defaultdict(list)

for p in NEW:
    q = old_for(p)
    if q is None:
        continue
    nm = p.get('player')
    # --- drafted position ---
    a, b = pos_old(q), pos_new(p)
    if a != b:
        drift['drafted_position'] += 1
        examples['drafted_position'].append((nm, a, b))
    # --- future position (what gfut reads; the one the ONE-HOT is built from) ---
    fa = q.get('future_position') or pos_old(q)
    fb = futpos_new(p)
    if fa != fb:
        drift['future_position'] += 1
        examples['future_position'].append((nm, fa, fb))
    # --- pick ---
    if q.get('pick') != p.get('pick'):
        drift['pick'] += 1
        examples['pick'].append((nm, q.get('pick'), p.get('pick')))
    # --- entry type ---
    if q.get('type') != p.get('type'):
        drift['type'] += 1
        examples['type'].append((nm, q.get('type'), p.get('type')))
    # --- draft year ---
    if q.get('year') != p.get('year'):
        drift['year'] += 1
        examples['year'].append((nm, q.get('year'), p.get('year')))
    # --- DOB ---
    if (q.get('_bd') or None) != (p.get('_bd') or None):
        drift['_bd'] += 1
        examples['_bd'].append((nm, q.get('_bd'), p.get('_bd')))
    # --- scoring rows: seasons at or before 2021 (the resolved window) and all seasons ---
    so = {x['year']: (x.get('games'), x.get('avg')) for x in (q.get('scoring') or [])}
    sn = {x['year']: (x.get('games'), x.get('avg')) for x in (p.get('scoring') or [])}
    if so != sn:
        drift['scoring_any'] += 1
        added = sorted(set(sn) - set(so))
        removed = sorted(set(so) - set(sn))
        changed = sorted(y for y in set(so) & set(sn) if so[y] != sn[y])
        if added:
            drift['scoring_seasons_added'] += len(added)
        if removed:
            drift['scoring_seasons_removed'] += len(removed)
        if changed:
            drift['scoring_seasons_changed'] += len(changed)
        # seasons <= 2021 are the ones that can move a RESOLVED career's target
        pre = [y for y in (added + removed + changed) if y <= 2021]
        if pre:
            drift['scoring_pre2022_touched_players'] += 1
            drift['scoring_pre2022_seasons'] += len(pre)
            examples['scoring_pre2022'].append((nm, pre[:6]))

out['drift_counts'] = dict(drift)
out['drift_examples'] = {k: v[:12] for k, v in examples.items()}
out['drift_example_totals'] = {k: len(v) for k, v in examples.items()}

json.dump(out, open(os.path.join(S, 'out', 'store_drift.json'), 'w'), indent=1, default=str)

print('OLD rows %d   NEW rows %d   matched %d   unmatched %d'
      % (out['n_old'], out['n_new'], matched, len(unmatched)))
print('keys added  :', out['keys_added'])
print('keys removed:', out['keys_removed'])
print()
for k, v in sorted(drift.items(), key=lambda kv: -kv[1]):
    print('  %-32s %6d' % (k, v))
print()
for k in ('future_position', 'drafted_position', 'pick', 'type', '_bd', 'scoring_pre2022'):
    ex = examples.get(k) or []
    if ex:
        print('%s  (%d total) e.g.' % (k, len(ex)))
        for e in ex[:6]:
            print('   ', e)
