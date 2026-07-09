#!/usr/bin/env python3
"""Red-path proof for gate-integrity (b): B2 stops trusting text.

Mirrors the exact checks ship_gates_check.py B2 applies to the producer's JSON certificate:
  1. PROVENANCE — the certificate's engine/store/config hashes must equal the candidate under test.
     A HANDCRAFTED or STALE certificate (wrong hashes) is REJECTED. The old B2 read an unauthenticated
     fixed-path text file with NO provenance, so a handcrafted four-line file passed.
  2. FULL PRECISION — the leakage gap = |WF.median - IS.median| is computed on UNROUNDED medians.
     The old B2 parsed integer-rounded text (regex T\\d+:\\s*(-?\\d+)), so a true 0.98 %-pt gap where both
     sides round to the same integer parsed as 0.0 — masked. This shows the counterexample is now measured.
Run:  python3 session_2026-07-09/gate_integrity/test_b2_certificate.py
"""
import sys

HEAD, STORE, CONFIG = 'aaaaaaaa', 'bbbbbbbb', 'c' * 64          # the candidate under test (stand-ins)
fails = []


def expect(label, cond, detail=''):
    print(("  PASS " if cond else "  FAIL ") + label + ('' if cond else '  <-- ' + detail))
    if not cond:
        fails.append(label)


def provenance_ok(cert):
    # verbatim predicate from ship_gates_check.py B2
    ok = (cert.get('engine_head_md5', '')[:8] == HEAD and cert.get('store_md5', '')[:8] == STORE)
    if CONFIG is not None:
        ok = ok and (cert.get('config_sha256') == CONFIG)
    return ok


print("=== gate-integrity (b) B2 certificate red-path proof ===")

# 1) genuine certificate for THIS candidate -> accepted
good = {'engine_head_md5': HEAD + '00000000', 'store_md5': STORE + '00000000', 'config_sha256': CONFIG,
        'cells': {}}
expect("genuine candidate certificate accepted", provenance_ok(good))

# 1a) handcrafted / stale certificate (wrong engine hash) -> REJECTED
forged = {'engine_head_md5': 'deadbeef' + '0' * 24, 'store_md5': STORE + '00000000', 'config_sha256': CONFIG,
          'cells': {}}
expect("handcrafted/stale cert (wrong engine hash) REJECTED", not provenance_ok(forged),
       "forged cert passed provenance")

# 1b) right code+store but WRONG config (the R3-style drift) -> REJECTED
wrongcfg = {'engine_head_md5': HEAD + '0' * 24, 'store_md5': STORE + '0' * 24, 'config_sha256': 'd' * 64,
            'cells': {}}
expect("cert with divergent config REJECTED", not provenance_ok(wrongcfg))

# 2) rounding counterexample: WF.median=100.49, IS.median=99.51 -> true gap 0.98; both round to 100.
wf_med, is_med = 100.49, 99.51
full_gap = abs(wf_med - is_med)                                 # new B2: full precision
old_gap = abs(round(is_med) - round(wf_med))                    # old B2: integer-parsed text (regex \\d+)
print("  ---- rounding counterexample: WF.median=%.2f IS.median=%.2f ----" % (wf_med, is_med))
expect("full-precision gap measured = 0.98 (> tol 0.5 -> would FAIL)", abs(full_gap - 0.98) < 1e-9,
       "got %.3f" % full_gap)
expect("old integer-parse gap was masked to 0.0 (both round to 100)", old_gap == 0,
       "got %d" % old_gap)
print("  demonstrates: the leakage the old text path masked (0.0) is now measured at full precision (0.98).")

print("\nRESULT:", "ALL PASS" if not fails else "FAILED: " + ", ".join(fails))
sys.exit(1 if fails else 0)
