import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
CF = json.load(open(SP + "ruck_cf2_main.json"))
D = json.load(open("/home/user/afl-rl-engine/data/rl_build/rl_app_data.json"))
ACT = {a['key']: a for a in D['active']}
F = 1.0524
live = [r for r in CF if r['key'] in ACT]
print("LIVE BOARD RUCKS (active list) n=%d   [engine currency; board = engine / %.4f]" % (len(live), F))
P = sum(r['price'] for r in live); PA = sum(r['price_A'] for r in live)
PC = sum(r['price_C'] for r in live); PAC = sum(r['price_AC'] for r in live)
V0 = sum(r['v0s'] for r in live); VU = sum(r['v0u'] for r in live)
print("  Sprice   = %9.1f (board %9.1f)" % (P, P / F))
print("  ceiling OFF   %+9.1f (board %+8.1f)   pole ON %+9.1f (board %+8.1f)   both %+9.1f (board %+8.1f)"
      % (PA - P, (PA - P) / F, PC - P, (PC - P) / F, PAC - P, (PAC - P) / F))
print("  Sv0_start=%9.1f  Sv0_uncapped=%9.1f  R=%.4f" % (V0, VU, V0 / VU))
print()
print("  binding rows and every row the pole would move (engine currency):")
print("  %-24s %5s %4s %5s %7s %9s %9s %8s %8s %8s %8s" % ("key","C","epk","games","bestlvl","price","board","+ceilOFF","+poleON","+both","bind"))
for r in sorted(live, key=lambda x: -( (x['price_A']-x['price']) + (x['price_C']-x['price']) )):
    dA = r['price_A'] - r['price']; dC = r['price_C'] - r['price']; dAC = r['price_AC'] - r['price']
    if abs(dA) < 0.5 and abs(dC) < 0.5: continue
    print("  %-24s %5s %4d %5.0f %7.2f %9.1f %9.1f %+8.1f %+8.1f %+8.1f %8s"
          % (r['key'], r['C'], r['epk'], r['games'], r['bestlvl'], r['price'], r['price']/F, dA, dC, dAC, r['bind']))
print()
c3 = [r for r in live if r['C'] and 2023 <= r['C'] <= 2025]
P3 = sum(r['price'] for r in c3); PA3 = sum(r['price_A'] for r in c3)
PC3 = sum(r['price_C'] for r in c3); PAC3 = sum(r['price_AC'] for r in c3)
V03 = sum(r['v0s'] for r in c3); VU3 = sum(r['v0u'] for r in c3)
print("LIVE BOARD, CAREER YEARS 1-3 (classes 2023-2025)  n=%d" % len(c3))
print("  Sprice=%.1f (board %.1f)  mark-up=%.4f  R=%.4f" % (P3, P3/F, P3/V03, V03/VU3))
print("  ceiling OFF %+8.1f | pole ON %+8.1f | both %+8.1f   -> mark-up %.4f / %.4f / %.4f"
      % (PA3-P3, PC3-P3, PAC3-P3, PA3/V03, PC3/V03, PAC3/V03))
print()
print("WHOLE RUCK RECORD SET (216 priced ruck records incl. retired/delisted):")
P = sum(r['price'] for r in CF); PA = sum(r['price_A'] for r in CF)
PC = sum(r['price_C'] for r in CF); PAC = sum(r['price_AC'] for r in CF)
print("  Sprice=%.1f  ceiling OFF %+8.1f  pole ON %+8.1f  both %+8.1f" % (P, PA-P, PC-P, PAC-P))
nb = [r for r in CF if r['bind']]
print("  rows where the ceiling binds: %d of %d  (bite %.1f engine pts)"
      % (len(nb), len(CF), sum(r['price_A']-r['price'] for r in nb)))
