#!/bin/bash
input=$(cat)
file=$(echo "$input" | jq -r '.file_path')
 
if [[ "$file" =~ \.(ts|tsx|js|jsx)$ ]]; then
  npx prettier --write "$file" > /dev/null 2>&1
  npx eslint --fix "$file" > /dev/null 2>&1
fi
exit 0

