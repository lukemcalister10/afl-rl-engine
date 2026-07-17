#!/usr/bin/env bash
# Re-runnable driver for riders (i)-(iii). READ-ONLY. Silence is a red (S1): every rider must print
# its asserted completion marker AND exit 0, or this script HALTs non-zero. Stamps are asserted inside
# each rider at load (common.load_frozen); a stamp mismatch HALTs there.
set -euo pipefail
cd "$(dirname "$0")"
SC=scripts
declare -A MARK=( [rider_i_calibration]=RIDER_I_COMPLETE
                  [rider_ii_bootstrap]=RIDER_II_COMPLETE
                  [rider_iii_uncertainty]=RIDER_III_COMPLETE )
ORDER=(rider_i_calibration rider_ii_bootstrap rider_iii_uncertainty)   # iii depends on i,ii outputs
fail=0
for r in "${ORDER[@]}"; do
  echo "== running $r =="
  out="$(python3 "$SC/$r.py")"; rc=$?
  echo "$out"
  if [ $rc -ne 0 ]; then echo "HALT: $r exit $rc"; exit $rc; fi
  if ! grep -q "${MARK[$r]}" <<<"$out"; then echo "HALT: $r missing completion marker ${MARK[$r]}"; exit 4; fi
  echo "-- $r OK (marker ${MARK[$r]} asserted) --"
done
echo "ALL_RIDERS_COMPLETE (i,ii,iii — markers asserted, exit codes 0)"
