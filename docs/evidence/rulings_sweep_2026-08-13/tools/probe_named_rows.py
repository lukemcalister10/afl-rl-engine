#!/usr/bin/env python3
"""ORDER 27 verification probe: owner-ruled NAMED ROWS, checked against the landed store.

READ-ONLY. Each row below is an owner ruling recorded in the register with its version.
Vocabulary note: the 2026-07-29 rename (#262) replaced K-FWD->KPF, K-DEF->KPD, G-DEF->SD,
G-FWD->SF, so a ruling worded in the old vocabulary is checked against its new token.
"""
import json

STORE = 'engine/rl_after/rl_model_data.json'
d = {p.get('key'): p for p in json.load(open(STORE, encoding='utf-8'))}

CASES = [
    ('sam-flanders',   'v216/v217: eligibilities SD+SF (was G-DEF,G-FWD); present_position -> SD (GDEF)'),
    ('oskar-baker',    'v216: eligibilities SD+SF, NOT mid'),
    ('ed-langdon',     'v216: eligibilities SD+SF, NOT mid'),
    ('matt-whitlock',  'v216/item20: KPD + KPF (genuine key swingman)'),
    ('darcy-gardiner', 'item20: -> KPD (both raw tags wrong)'),
    ('lukas-cooke',    'item20: -> KPD'),
    ('colby-mckercher','item296: eligibilities SD,MID (was G-DEF,MID)'),
    ('jake-lloyd',     'item296: eligibilities SD,SF (was G-DEF,G-FWD)'),
    ('aiden-odriscoll','v430: O\'Driscoll GDEF; item275: future 100% MID'),
    ('jack-carroll',   'v503: present SD and future SD (owner per-player bucket-2 ruling)'),
    ('flynn-perez',    'item10a re-entry trio: record LATER entry (SSP 2025)'),
    ('lachlan-mcandrew','item10a re-entry trio: later entry (SSP 2024); _by 2000'),
    ('mark-keane',     'item10a re-entry trio: later entry (SSP 2022)'),
    ('luke-nankervis', 'item10b: truth is PSD, store keeps PSD pick 2'),
    ('matt-maguire',   'v430 / #146: Maguire removed from the store'),
    ('paddy-mccartin', 'v533(2): force-majeure EXCLUDE from the pick curve, whole-draft slide'),
    ('thomas-boyd',    'v533(2): force-majeure EXCLUDE from the pick curve, whole-draft slide'),
    ('jeremy-cameron', 'v533(1): INCLUDE in the PVC going forward (GWS concession, notional pick)'),
    ('dylan-shiel',    'v533(1): INCLUDE in the PVC going forward'),
    ('adam-treloar',   'v533(1): INCLUDE in the PVC going forward'),
    ('will-brodie',    'DECISIONS v85 s20: owner display override x0.50'),
    ('harrison-himmelberg', 'v531: is_key blanket rule EXCEPTED - graded per season in the sheet'),
    ('bailey-williams','v582/v616: the two Bailey Williamses disambiguated (wc / wb)'),
]

FIELDS = ('key', 'name', 'type', 'year', 'pick', 'drafted_position', 'present_position',
          'future_position', 'alternate_position', 'p_dual_stream', 'eligibilities',
          '_pvc_exclude', '_retired', '_by', 'affl_team')

for key, ruling in CASES:
    p = d.get(key)
    print('--- %s' % key)
    print('    RULING: %s' % ruling)
    if p is None:
        cand = [k for k in d if key.split('-')[-1] in k]
        print('    STORE : ABSENT (near keys: %s)' % cand[:6])
        continue
    print('    STORE : %s' % {f: p.get(f) for f in FIELDS if f in p})
