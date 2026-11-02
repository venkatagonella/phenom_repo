#!/bin/bash
input=$(cat)
prompt=$(echo "$input" | jq -r '.prompt // empty')
 
# Block obvious credential patterns
if echo "$prompt" | grep -qE '(sk-[a-zA-Z0-9]{32,}|AKIA[0-9A-Z]{16}|-----BEGIN.*PRIVATE KEY-----)'; then
  echo '{"permission":"deny","userMessage":"Blocked: credential pattern detected in prompt."}'
  exit 0
fi
 
echo '{"permission":"allow"}'
exit 0

