"""ORDER 25 — run the repo's own boot guard against the LANDED tree, both halves, fail-closed."""
import os, sys
ROOT = '/home/user/afl-rl-engine/.claude/worktrees/agent-ae867318eb00a513e'
os.environ['RL_REPO'] = ROOT
os.environ['RL_FV'] = os.path.join(ROOT, 'engine', 'forward_valuation')
sys.path.insert(0, ROOT)
import boot_guard

print("repo_root resolved:", boot_guard.repo_root())
print()
print("--- (A) forward-valuation provenance, both halves (checkout + loaded-path) ---")
fails = boot_guard.fv_provenance_fails(ROOT)
print("PASS — no failures" if not fails else "FAIL:\n  " + "\n  ".join(fails))
print()
print("--- (B) assert_boot: store / register / config / board / rl_model / fitted / load-path ---")
ok = boot_guard.assert_boot('order25_pool_landing_v2',
                            store_path=os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json'),
                            engine_head_path=os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py'),
                            register_path=os.path.join(ROOT, 'LTI_REGISTER.md'),
                            halt=True)
print("assert_boot returned:", ok)
print()
print("BOOT GUARD: PASS on the landed tree." if (ok and not fails) else "BOOT GUARD: FAIL")
sys.exit(0 if (ok and not fails) else 1)
