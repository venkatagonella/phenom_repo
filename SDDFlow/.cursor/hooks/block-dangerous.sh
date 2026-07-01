#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.command')
 
if echo "$command" | grep -qE '(rm -rf /|git push --force|DROP TABLE|TRUNCATE TABLE|sudo)'; then
  echo '{"permission":"deny","agentMessage":"Blocked: destructive command. Propose a safer alternative."}'
  exit 0
fi
 
echo '{"permission":"allow"}'
exit 0

