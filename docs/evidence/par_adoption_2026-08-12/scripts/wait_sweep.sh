#!/bin/bash
# ORDER 20B — block until the 14-config channel sweep has produced all its artifacts.
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
while true; do
  n=$(ls "$SP"/chan_*.json 2>/dev/null | wc -l)
  [ "$n" -ge 14 ] && break
  sleep 15
done
echo "SWEEP COMPLETE: 14 configs"
