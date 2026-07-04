#!/bin/bash
# LTI / availability MACHINERY grep-by-concept (READ-ONLY). Reproduces the EXISTS/NOT evidence.
# Run from repo root: bash evidence/lti/grep_machinery.sh
set -u
E=engine/rl_after/_merged_recover.py
M=engine/rl_after/rl_model.py
D=engine/forward_valuation/distribution_pricing.py

echo "=== (1) present-unavailability haircut _b2hc — EXISTS ==="
grep -nE 'B2:|_b2hc|_b2band|pre_hc' "$M" "$D" "$E"
echo
echo "=== (1b) role-decay haircut — EXISTS but explicitly NOT injury ==="
grep -nE 'ROLE_HC_MAX|_role_decay_hc' "$M"
echo
echo "=== (1c) return-season / LTI / layoff discount — expect NO HITS (does not exist) ==="
# concept words for an injury RETURN-SEASON discount; excludes the 'return SEASON*' proration false-positive
grep -rniE 'return[-_ ]?season[-_ ]?(haircut|discount|penalt)|\blayoff\b|out[-_ ]?until[-_ ]?[0-9]|lti[-_ ]?(haircut|layer|overlay|discount)|\b_lti\b|injury[-_ ]?(haircut|discount)' \
  engine/rl_after engine/forward_valuation || echo "  (no hits — return-season/LTI machinery DOES NOT EXIST in the engine)"
echo
echo "=== (2) zero-games / calendar mechanism (M3 clock-pin) ==="
grep -nE 'M3 CLOCK-PIN|_M3PIN|def _m3_s|def _ev_m3|ev_prefloor=' "$E"
echo
echo "=== (3) branches: delist gate / sit-out / staleness ==="
grep -nE 'def delisted|def sitout_ev|SIT-OUT|stalled|mediocre|delist -> ' "$E"
grep -nE 'def _on_board|_last_listed|_retired' "$M" | head
echo
echo "=== (4) interaction surfaces: V0 anchor + retention surface + floor ==="
grep -nE 'def v0_start|LAM_SIT=|R_SURF=|def _R_surf|FLOOR_YRS=' "$E"
