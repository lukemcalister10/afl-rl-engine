#!/usr/bin/env python3
"""THE FINAL JOINT MOVERS LIST — the owner's landing document (his word, verbatim: "one candidate
board that tracks all direct movers, from live, to the end candidate result, tracking their change
attributable to each new mechanism being added. At the end, list their v0, and change under the
candidate from live and from v0").

Sources: the live board (3167cba6) · the FINAL candidate board (530a4053) · the approved v872/v875
waterfall (per-row smoothing/surface attribution) · BOARD_VERIFY.json (step-up/easing/ripple
classifications, every one instrument-verified) · optionally the candidate walk-forward matrix for
v0 on rows the waterfall did not carry.

  usage: build_final_movers.py LIVE.json CAND.json WATERFALL.json BOARD_VERIFY.json OUT_BASE
         [--matrix per_entrant_CAND.json]
"""
import json, sys

args = list(sys.argv[1:])
matrix_p = None
if '--matrix' in args:
    i = args.index('--matrix'); matrix_p = args[i + 1]; del args[i:i + 2]
live_p, cand_p, wf_p, bv_p, out_base = args[:5]

LB = json.load(open(live_p)); CB = json.load(open(cand_p))
WF = json.load(open(wf_p)); BV = json.load(open(bv_p))

def rows(d):
    return {r['key']: r for L in ('active', 'back') for r in d[L]}
lv, cv = rows(LB), rows(CB)
wf = {m['key']: m for m in WF['movers']}
stepup = {r['key']: r for r in BV['stepup_landed']}
# THE EASING CLASS, DATA-DERIVED FROM THE STORE (blind-review finding 1, law 11): the O48 taper's
# own scope is exactly one banked (>=6-game) season AND it is the CURRENT season. The first cut of
# this document borrowed BOARD_VERIFY's classifier, whose `g` field turned out to be CAREER games —
# it labeled 13 career-banked veterans (boak, hawkins, heppell ...) "easing" by sign alone. The
# battery's own instruments (F2 O48-only sweep: 3 movers; F4 grid: n_up=3 at every weight) and the
# reviewer's independent read of the wrapper's scope test agree: the class is computed here from
# the store's scoring records, not inferred from a display field.
STORE = json.load(open('/home/user/cand_build/ws/rl_after/rl_model_data.json'))
def _sc(rec):
    return [x for x in (rec.get('scoring') or []) if x.get('year', 0) <= 2026]
easing_keys = set()
for _rec in (STORE.values() if isinstance(STORE, dict) else STORE):
    if not isinstance(_rec, dict) or not _rec.get('key'):
        continue
    _b = [x for x in _sc(_rec) if x.get('games', 0) >= 6]
    if len(_b) == 1 and _b[0].get('year') == 2026:
        easing_keys.add(_rec['key'])
easing = {r['key']: r for r in BV['easing_candidates'] if r['key'] in easing_keys}
mx = {}
if matrix_p:
    try:
        _m = json.load(open(matrix_p))
        _recs = _m if isinstance(_m, list) else _m.get('rows') or _m.get('entrants') or []
        for r in _recs:
            k = r.get('key')
            if k and r.get('v0') is not None:
                mx[k] = r['v0']
    except Exception:
        pass

out = []
for k in cv:
    if k not in lv:
        continue
    d_total = cv[k]['v'] - lv[k]['v']
    if d_total == 0:
        continue
    m = wf.get(k)
    d_smooth = m['d_smooth'] if m else 0
    d_surface = m['d_surface'] if m else 0
    d_step = stepup.get(k, {}).get('d_beyond_wf', 0)
    d_ease = easing.get(k, {}).get('d_vs_wf', easing.get(k, {}).get('d', 0)) if k in easing else 0
    d_ripple = d_total - d_smooth - d_surface - d_step - d_ease
    v0 = (m and m.get('v0_cand')) or mx.get(k)
    out.append({
        'key': k, 'player': cv[k].get('name') or (m and m.get('player')) or k,
        'pos': cv[k].get('grp'), 'route': cv[k].get('ty'), 'pick': cv[k].get('pk'),
        'entry': cv[k].get('yr'),
        'live': lv[k]['v'], 'cand': cv[k]['v'],
        'd_smoothing': d_smooth, 'd_surface': d_surface, 'd_stepup': d_step,
        'd_easing': d_ease, 'd_residual': d_ripple, 'd_total': d_total,
        'v0': v0, 'd_from_v0': (cv[k]['v'] - v0) if v0 is not None else None,
        'flag': ('STEP-UP' if d_step else '') + ('EASING' if k in easing else '')
                + ('RIPPLE' if (d_ripple and not d_step and k not in easing) else ''),
    })
out.sort(key=lambda r: -abs(r['d_total']))
tot_l = sum(r['v'] for r in lv.values()); tot_c = sum(r['v'] for r in cv.values())
_rip = [r for r in out if r['d_residual'] and not r['d_stepup'] and r['key'] not in easing]
_rip_txt = ('v0surf refit ripple (the residual column): %d rows within the +/-6 bound, net %+d — '
            'the mandatory fitted-surface regeneration under the smoothed curve; the studies '
            'predate it. [Corrected at blind review: the first draft classified 13 of these — '
            'career-banked veterans — as easing off a career-games field; the easing class is now '
            'derived from the store\'s own scoring records.]'
            % (len(_rip), sum(r['d_residual'] for r in _rip)))

meta = {
    'title': 'THE FINAL JOINT MOVERS LIST — every mechanism built, every mover attributed',
    'board_live': '3167cba6', 'board_cand': '530a4053',
    'engine': '856e8328', 'config': 'f233d160', 'curve': '1c3b22d1 (S_LL5G)',
    'net_pre_level': tot_c - tot_l, 'n_movers': len(out),
    'headline_disclosures': [
        'JOSH SMILLIE +%d — the survivorship step-up (the derived clock law) on a pick-3 pedigree; '
        'the class was predicted, this size was not: the law pays a tenure-3 survivor the D(4) level '
        'and his pedigree is the largest in the class.' % (stepup.get('josh-smillie', {}).get('d_beyond_wf', 0)),
        'EASING AT FULL WEIGHT (W=1.0): the declared sizing procedure (largest grid weight under '
        'which no eased row reaches its thin twin) passed at every weight, so it selects 1.0. It '
        'reaches exactly THREE rows (pickett +135, dawson +110, croft +31 — first banked season in '
        'progress), not the ~28 small ups the prereg predicted, and moir is NOT among them (he moves '
        '-1 through the ripple). The sizes exceed the +28/+34 seen at the 0.25 placeholder; the '
        'constraint you set is the only thing that binds them.',
        _rip_txt,
        'F3 AS PREREGISTERED FIRED: the pairwise thin-above-any-banked census GREW 345 -> 399 '
        '(+54). The battery gate was re-instrumented to the ruled construction — no thin row the '
        'lift touches may load above the banked-mediocre ceiling you set the cells at (0.81 mobile '
        '/ 0.92 tall, tall ruled AT equality) — and that gate is clean (zero breaches; newton '
        'disclosed: his 0.93 loading is standing MSD route floors, lift capped at his stamp). The '
        '+54 pairs are thin rows floored above rows that RESOLVED DOWN (busts and poor outcomes; '
        'the blind review independently recomputed the censuses: ~51 of ~55 fit that description '
        'cleanly, the remainder ride the step-up/smoothing and the disclosed newton standing row) '
        '— the six-game step you ruled — but the prereg falsifier as WRITTEN failed and the '
        're-instrumentation is named here, not buried.',
    ],
    'columns': 'live -> +smoothing -> +surface -> +step-up -> +easing -> +residual = candidate; '
               'v0 = the smoothed draft-day stamp; d_from_v0 = candidate minus draft day',
}
json.dump({'meta': meta, 'movers': out}, open(out_base + '.json', 'w'), indent=1)

H = ['<!doctype html><meta charset="utf-8"><title>Final joint movers</title>',
     '<style>body{font:13px/1.45 system-ui;margin:24px;max-width:1200px}table{border-collapse:collapse;width:100%}'
     'td,th{border:1px solid #ccc;padding:3px 7px;text-align:right;white-space:nowrap}'
     'td:nth-child(-n+5),th:nth-child(-n+5){text-align:left}tr:nth-child(even){background:#f6f6f6}'
     '.pos{color:#0a7a2f}.neg{color:#b00020}.hl{background:#fff8dc;border:1px solid #e0d090;padding:10px 14px;margin:8px 0}</style>',
     '<h2>%s</h2>' % meta['title'],
     '<p>board %s → <b>%s</b> · engine %s · config %s · curve %s · net pre-level <b>%+d</b> · %d movers</p>'
     % (meta['board_live'], meta['board_cand'], meta['engine'], meta['config'], meta['curve'],
        meta['net_pre_level'], meta['n_movers'])]
for hd in meta['headline_disclosures']:
    H.append('<div class="hl">%s</div>' % hd)
H.append('<table><tr><th>player</th><th>pos</th><th>route</th><th>pick</th><th>entry</th>'
         '<th>live</th><th>smooth</th><th>surface</th><th>step-up</th><th>easing</th><th>resid</th>'
         '<th>CAND</th><th>Δ total</th><th>v0 (draft)</th><th>Δ from v0</th></tr>')

def c(v, always=False):
    if v is None:
        return '<td>—</td>'
    if v == 0 and not always:
        return '<td></td>'
    cls = 'pos' if v > 0 else ('neg' if v < 0 else '')
    return '<td class="%s">%+d</td>' % (cls, v) if not always else '<td>%d</td>' % v
for r in out:
    H.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>%s%s%s%s%s%s%s%s%s%s</tr>' % (
        r['player'], r['pos'], r['route'], r['pick'] or '', r['entry'],
        c(r['live'], True), c(r['d_smoothing']), c(r['d_surface']), c(r['d_stepup']),
        c(r['d_easing']), c(r['d_residual']), c(r['cand'], True), c(r['d_total']),
        c(r['v0'], True) if r['v0'] is not None else '<td>—</td>', c(r['d_from_v0'])))
H.append('</table>')
open(out_base + '.html', 'w').write('\n'.join(H))
print('FINAL MOVERS: %d movers, net %+d -> %s.{json,html}' % (len(out), meta['net_pre_level'], out_base))
