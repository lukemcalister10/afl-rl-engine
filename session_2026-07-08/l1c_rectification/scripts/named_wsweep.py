"""L1c TASK 4 (named-player half) — OWNER W-TABLE board rows: named players at w in {0.5,0.6,0.7,0.8},
against baked v2.5 and the W4-pre-L1c candidate. Fresh engine exec per w (the V0 curve refits on credited
inputs, so a post-hoc dial poke would be inconsistent — full reload each time). Guard 5 on entry."""
import io, contextlib, json, os, sys
HERE = '/home/user/afl-rl-engine'
OUT = f'{HERE}/session_2026-07-08/l1c_rectification/out'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('named_wsweep', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json',
                       engine_head_path='/home/claude/rl_workspace/rl_after/_merged_recover.py')
os.chdir('/home/claude/rl_workspace/rl_after')

NAMES = [('Willem Duursma', 'A-DUUR young gun, 2025 pk1 MID, 12g'),
         ('Sam Lalor', 'top-3 pick, 2024 pk1, 18g'),
         ('Errol Gulden', 'Gulden shape: mid-pick instant producer, 2020 pk34, 105g'),
         ('Sam Darcy', 'Darcy shape: young KPF ceiling, 2021 pk2, 51g'),
         ('Taylor Goad', 'Goad shape: sat-out young ruck, 2023 pk20, 1g'),
         ('Dylan Patterson', 'pure sit-out, 2025 pk5, 0 games'),
         ('Riley Bice', 'mature-age pick, 2024 pk41, draft-age 24, 30g')]

baked = {r['key']: r['v'] for r in json.load(open(f'{HERE}/session_2026-07-06/w4_integration/out/baked_board_full.json'))['active']}
pre = {r['key']: r['v'] for r in json.load(open(f'{HERE}/data/rl_build/rl_app_data.json'))['active']}

rows = {nm: {'note': note} for nm, note in NAMES}
for w in ('0.5', '0.6', '0.7', '0.8'):
    os.environ['RL_YCRED_W'] = w
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA = g['MA']; ev = g['ev']
    for nm, _ in NAMES:
        p = next((x for x in MA.data if x['player'] == nm and MA.GRP.get(x.get('pos'))), None)
        if p is None:
            rows[nm][f'w{w}'] = None; continue
        with contextlib.redirect_stdout(io.StringIO()):
            rows[nm][f'w{w}'] = ev(p, 2026)
        rows[nm]['key'] = p.get('key')
    del g

for nm in rows:
    k = rows[nm].get('key')
    rows[nm]['baked_v25'] = baked.get(k)
    rows[nm]['w4_preL1c'] = pre.get(k)
json.dump(rows, open(f'{OUT}/named_wsweep.json', 'w'), indent=1)
print(f"{'player':18s}{'baked':>7s}{'preL1c':>8s}{'w=0.5':>8s}{'w=0.6':>8s}{'w=0.7':>8s}{'w=0.8':>8s}   note")
for nm, note in NAMES:
    r = rows[nm]
    print(f"{nm:18s}{str(r.get('baked_v25')):>7s}{str(r.get('w4_preL1c')):>8s}"
          + ''.join(f"{str(r.get('w'+w)):>8s}" for w in ('0.5', '0.6', '0.7', '0.8')) + f"   {note}")
