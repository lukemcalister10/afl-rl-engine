#!/usr/bin/env python3
"""F1 DECIDING MEASUREMENT (#290, seam word 2026-07-31).

Recompute ev(p,2026) for all 804 in a FRESH PROCESS, order-clean, and compare against the
board (== round(_raw2026 / F), i.e. what the EXPORT saw).

Three modes, each run in its OWN process so no namespace or call-order state is inherited:

  single          ev(p,2026) ONLY, per player. No replayed sequence.
  replay_selftest ev(p,2026); ev(2024); ev(2025); ev(2027); ev(2028)   <- the gate as written
  replay_export   the same, but with MA._LENS_FORM toggled around the forward pair, which is
                  what rl_export.py:187/189 actually does. Note _LENS_FORM is READ as
                  getattr(MA,'_LENS_FORM') — rl_model's namespace — so it must be set THERE.
                  (My earlier probe set it on the _merged_recover exec dict: the wrong object.)

Verdict:
  single == board  ->  the export was right; the gate's replication is the defect.
  single == replay_selftest != board  ->  the export's ev is contaminated: an ENGINE defect.
"""
import json, io, os, sys, contextlib

MODE = sys.argv[1]
OUT = sys.argv[2]

ens = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], ens)

ev = ens['ev']
MA = ens['MA']                      # rl_model — the namespace _LENS_FORM is READ from
players = MA.__dict__['players']

vals = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in players:
        v = ev(p, 2026)
        if MODE == 'replay_selftest':
            ev(p, 2024); ev(p, 2025); ev(p, 2027); ev(p, 2028)
        elif MODE == 'replay_export':
            ev(p, 2024); ev(p, 2025)
            MA._LENS_FORM = 2026            # rl_export.py:187 — set on MA, where it is read
            ev(p, 2027); ev(p, 2028)
            MA._LENS_FORM = None            # rl_export.py:189
        vals[p['key']] = v

json.dump(vals, open(OUT, 'w'))
print("%s: %d players" % (MODE, len(vals)))
