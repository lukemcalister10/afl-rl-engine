"""Child process for the finalization HARD-TERMINATION case (point 8). Runs finalize_round(round) on a
scratch with a fault that HARD-EXITS mid-pass (os._exit, skipping any journal cleanup) — exactly a
power-loss during finalization. The parent then proves a restart detects the FINALIZING round and
repairs it, with the canonical commit (store/board/ledger/history) untouched and no score re-applied.

Usage:  _finalize_crash_child.py <scratch_root> <round> <fault_point>
"""
import os
import sys

scr, round_n, point = sys.argv[1], int(sys.argv[2]), sys.argv[3]
RA = os.path.join(scr, 'engine', 'rl_after')
ING = os.path.join(RA, 'ingestion')
sys.path.insert(0, RA)
sys.path.insert(0, ING)
import round_finalize as FZ   # noqa: E402


def fault(p):
    if p == point:
        sys.stdout.flush()
        os._exit(137)          # hard kill mid-finalization (no rollback, no journal close)


fz = FZ.RoundFinalizer(scr, fault=fault)
fz.finalize_round(round_n, generated_at="2026-07-20T23:00:00Z")
# never reaches here for the injected point
print("child finished without crashing (unexpected)")
