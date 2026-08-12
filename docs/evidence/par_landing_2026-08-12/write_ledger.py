"""ORDER 20C — write the par-fix lever's named per-player ledger: markdown + json.

One lever, one ledger (the owner's standing attribution requirement). Every board row that moves
under the par separation fix, named, before -> after -> delta, both arms, plus ORDER 20B's per-channel
decomposition for the named large movers.
"""
import json, os, shutil

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o20c'
ROOT = '/home/user/afl-rl-engine/.claude/worktrees/agent-a6af0d68789879235'
LED = os.path.join(ROOT, 'docs', 'ledgers')
os.makedirs(LED, exist_ok=True)

d = json.load(open(os.path.join(SP, 'PAR_FIX_MOVERS_2026-08-12.json')))
shutil.copyfile(os.path.join(SP, 'PAR_FIX_MOVERS_2026-08-12.json'),
                os.path.join(LED, 'PAR_FIX_MOVERS_2026-08-12.json'))

CH = ('ISO', 'POLE', 'BLEND', 'BAR', 'BASE', 'LVLPAR')
L = []
P = L.append

P("# PAR-FIX MOVERS LEDGER — the par separation fix, every board row that moves")
P("")
P("**Lever:** the par arm-split separation fix — `engine/forward_valuation/par_build.py` +")
P("`par_redesign.py`, PR #457, `build/nd-pool-separation` `78d5c38`.")
P("**Adopted:** owner ruling 2026-08-12 (*\"Yes, adopt.\"*), issue #334 comment `5261191193`, on ORDER")
P("20B's evidence packet. **Landed:** ORDER 20C, branch `land/par-fix-adoption`.")
P("")
P("**Board `%s` → `%s`.**" % (d['board_before'], d['board_after']))
P("")
P("This is the lever's record. One lever, one ledger — the owner's standing attribution requirement.")
P("Every row below is a board row whose value `v` changed when the fix was applied, with nothing else")
P("changed: same store (`d9a24282`), same config (`cd38fb00`), same frozen pickles, same shipped")
P("defaults. Both boards were rebuilt on the landing tree by ORDER 20B's own harness; the control")
P("reproduced the live board `94f1fec5` byte-identical before the fix was applied.")
P("")
P("Arm predicate is ORDER 20's, verbatim: **NATIONAL** = `ty=='ND' and ep<=64`; **POOL** = everything")
P("else. Values are board `v` (numéraire-rebased SCAR), integers as exported.")
P("")
P("## Totals")
P("")
P("| arm | rows | movers | total before | total after | delta | pct |")
P("|---|---:|---:|---:|---:|---:|---:|")
for arm in ('NATIONAL', 'POOL'):
    a = d['arms'][arm]
    P("| %s | %d | %d | %d | %d | %+d | %+.4f%% |"
      % (arm, a['n'], a['movers'], a['total_before'], a['total_after'], a['delta'], a['pct']))
P("")
P("**%d ledger rows** (%d national + %d pool). The national side is the one-time de-contamination —"
  % (d['ledger_rows'], d['arms']['NATIONAL']['movers'], d['arms']['POOL']['movers']))
P("pool rows leaving the national fit — and it is a *fall* of −1,768 (−0.28%). The pool side rises")
P("+2,305 (+1.86%) as those rows are priced on their own arm. The national pick curve does **not**")
P("move: 0 of 64 PVC points, 0 of 64 `picks[]`, pick 1 = 3000 (the numéraire law holds).")
P("")
P("## Whole-board attribution by par channel (ORDER 20B)")
P("")
P("Source: `docs/evidence/par_adoption_2026-08-12/movers/CHANNEL_DECOMP.json`. Two independent")
P("decompositions — one-at-a-time (switch one channel to the fixed arm split) and leave-one-out")
P("(switch all but one). Units are national-arm board points.")
P("")
P("| channel | one-at-a-time | leave-one-out |")
P("|---|---:|---:|")
for c in CH:
    b = d['board_by_channel'][c]
    P("| `%s` | %s | %s |" % (c, "0" if b['one_at_a_time'] == 0 else "%+d" % b['one_at_a_time'],
                              "0" if b['leave_one_out'] == 0 else "%+d" % b['leave_one_out']))
P("| **residual** | %+d | %+d |" % (d['board_channel_residual']['one_at_a_time'],
                                    d['board_channel_residual']['leave_one_out']))
P("| **board total** | %+d | |" % d['arms']['NATIONAL']['delta'])
P("")
P("Two findings the owner should keep in view, both ORDER 20B's:")
P("")
P("1. **`BASE_RATE` contributes EXACTLY ZERO** — on the whole board and on every decomposed mover.")
P("   It has no board consumer outside `par_redesign.py`'s own `__main__` report block.")
P("2. **`LVLPAR` (`par_redesign.lvl_par:126`) carries −545 of the −1,768** — roughly a third of the")
P("   national move — and it is a par consumer ORDER 20's sixteen-site sweep never named. It is the")
P("   highest-traffic par consumer on the board (38,159 calls).")
P("")
P("## The named large movers, decomposed per channel")
P("")
P("The seven movers ORDER 20B decomposed. `oaat` = one-at-a-time, `loo` = leave-one-out.")
P("")
named = []
for arm in ('NATIONAL', 'POOL'):
    for r in d['arms'][arm]['rows']:
        if 'channels' in r:
            named.append((arm, r))
DEC = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'par_adoption_2026-08-12',
                                  'movers', 'CHANNEL_DECOMP.json')))['movers']


def sg(v):
    return "0" if v == 0 else "%+d" % v


P("| player | arm | pos | pick | before | after | delta | " + " | ".join("`%s`" % c for c in CH) + " |")
P("|---|---|---|---:|---:|---:|---:|" + "---:|" * len(CH))
for arm, r in named:
    cells = " | ".join("%s / %s" % (sg(r['channels'][c]['one_at_a_time']), sg(r['channels'][c]['leave_one_out']))
                       if c in r['channels'] else "—" for c in CH)
    P("| **%s** | %s | %s | %s | %d | %d | %+d (%+.2f%%) | %s |"
      % (r['name'], arm, DEC.get(r['name'], {}).get('pos') or r.get('ty'), r.get('pk'),
         r['before'], r['after'], r['delta'], r['pct'], cells))
P("")
P("Channel cells read `oaat / loo`. Residual (the interaction the single-channel probes cannot see) is")
P("carried per player in the `.json` sidecar.")
P("")

for arm in ('NATIONAL', 'POOL'):
    a = d['arms'][arm]
    P("## %s — all %d movers" % (arm, a['movers']))
    P("")
    P("Sorted by absolute move, largest first. `ty` = intake type, `pk` = draft pick, `ep` = effective")
    P("pick (the board's arm key).")
    P("")
    P("| # | player | ty | pk | ep | before | after | delta | pct |")
    P("|---:|---|---|---:|---:|---:|---:|---:|---:|")
    for i, r in enumerate(a['rows'], 1):
        P("| %d | %s | %s | %s | %s | %d | %d | %+d | %+.2f%% |"
          % (i, r['name'], r.get('ty'), r.get('pk'), r.get('ep'), r['before'], r['after'],
             r['delta'], r['pct']))
    P("")

P("## Provenance")
P("")
P("- Both boards rebuilt on the landing tree with `docs/evidence/par_adoption_2026-08-12/scripts/build_board_o20b.sh`")
P("  (ORDER 20B's harness), shipped defaults, no manifest override.")
P("- Control (unmodified tree) → `94f1fec59f99c59d5890d5975c79fa9b`, byte-identical to the live pinned board.")
P("- Fix (`78d5c38`'s two files) → `1dbd1480a34c7823f330273211cbb76a`, byte-identical to ORDER 20's measured FIX board.")
P("- Delta computed with ORDER 20's own `fix/board_delta.py`; every published figure in its committed")
P("  `BOARD_DELTA_par_armsplit.json` reproduces, and all 40+40 of its named top movers reproduce to the unit.")
P("- Channel decomposition carried unchanged from ORDER 20B's `movers/CHANNEL_DECOMP.json`.")
P("- Machine-readable sidecar: `PAR_FIX_MOVERS_2026-08-12.json` (same directory), which additionally")
P("  carries each row's board `key` and section and each decomposed mover's channel residuals.")
P("")
P("---")
P("")
P("_Generated by [Claude Code](https://claude.ai/code)_")

open(os.path.join(LED, 'PAR_FIX_MOVERS_2026-08-12.md'), 'w').write("\n".join(L) + "\n")
print("ledger rows:", d['ledger_rows'], "| named decomposed:", len(named))
print("wrote", os.path.join(LED, 'PAR_FIX_MOVERS_2026-08-12.md'))
print("wrote", os.path.join(LED, 'PAR_FIX_MOVERS_2026-08-12.json'))
