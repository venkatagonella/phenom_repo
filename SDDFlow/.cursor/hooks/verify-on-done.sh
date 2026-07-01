#!/bin/bash
input=$(cat)
status=$(echo "$input" | jq -r '.status')
 
if [[ "$status" != "completed" ]]; then
  echo '{}'
  exit 0
fi
 
output=$(pnpm verify 2>&1)
exit_code=$?
 
if [[ $exit_code -ne 0 ]]; then
  followup="Verification failed. Fix before declaring done:\n\n$output"
  echo "{\"followup_message\": \"$followup\"}"
else
  echo '{}'
fi
exit 0
