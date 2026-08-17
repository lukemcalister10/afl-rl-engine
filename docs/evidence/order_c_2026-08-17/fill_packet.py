#!/usr/bin/env python3
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
p = os.path.join(HERE, 'PACKET_C.md')
s = open(p).read()
s = s.replace("board `ORDERC_MD5` / matrix\n`per_entrant_O34FINAL.json` in the scratchpad.",
              "board `7773b0dc` (total 665,979) / matrix `per_entrant_O34FINAL.json` (`0889c6ac`) in\nthe scratchpad.")
J = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_C_MOVERS.json')))
BY = {r['key']: r for r in J['rows']}
for key, slot in (('alix-tauru', 'LIVE_TAURU'), ('jordan-croft', 'LIVE_CROFT'),
                  ('ethan-read', 'LIVE_READ'), ('vigo-visentini', 'LIVE_VIGO')):
    lv = BY[key]['live']
    s = s.replace(slot, str(lv) if lv is not None else '—')
s = s.replace('C31_VIGO', str(BY['vigo-visentini']['c31']))
open(p, 'w').write(s)
print({k: (BY[k]['live'], BY[k]['c31'], round(BY[k]['g'])) for k in
       ('alix-tauru', 'jordan-croft', 'ethan-read', 'vigo-visentini', 'nick-madden', 'harry-dean',
        'cooper-duff-tytler', 'ty-gallop', 'charlie-west', 'jedd-busslinger')})
