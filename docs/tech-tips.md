# Tech tips and tricks

This is a casual page for team members to document helpful tips and tricks.

## Compiling recent GitHub activity for reporting

Here's a bash script that can be modified to get pull request and issue activity for one or more users over a given time frame:

```bash
#!/bin/bash

AUTHORS=(maxrjones)
DATE_RANGE="2026-02-02..2026-02-08"
OUTPUT="output.md"

PR_JQ='
  group_by(.repository.nameWithOwner) |
  .[] |
  "\n### \(.[0].repository.nameWithOwner) (\(length) PRs)\n" + (
    .[] | "#\(.number) [\(.state)] \(.author.login): \(.title)\n  Created: \(.createdAt | split("T")[0]) | Closed: \(if .closedAt then (.closedAt | split("T")[0]) else "—" end)\n  \(.url)"
  )
'

ISSUE_JQ='
  group_by(.repository.nameWithOwner) |
  .[] |
  "\n### \(.[0].repository.nameWithOwner) (\(length) issues)\n" + (
    .[] | "#\(.number) [\(.state)] \(.author.login): \(.title)\n  Created: \(.createdAt | split("T")[0]) | Closed: \(if .closedAt then (.closedAt | split("T")[0]) else "—" end)\n  \(.url)"
  )
'

> "$OUTPUT"

for author in "${AUTHORS[@]}"; do
  echo "# Contributions: $author" >> "$OUTPUT"
  echo "**Period:** $DATE_RANGE" >> "$OUTPUT"

  # --- Authored PRs ---
  echo -e "\n## Authored PRs" >> "$OUTPUT"
  gh search prs \
    --limit 1000 \
    --author="$author" \
    --updated="$DATE_RANGE" \
    --json number,title,state,createdAt,closedAt,url,repository,author \
  | jq -r "$PR_JQ" >> "$OUTPUT"

  # --- PR Reviews (PRs reviewed by the author, excluding self-authored) ---
  echo -e "\n## PR Reviews" >> "$OUTPUT"
  gh search prs \
    --limit 1000 \
    --reviewed-by="$author" \
    --updated="$DATE_RANGE" \
    --json number,title,state,url,repository,author \
  | jq -r --arg self "$author" '
    [ .[] | select(.author.login != $self) ] |
    if length == 0 then "No reviews found"
    else
      group_by(.repository.nameWithOwner) |
      .[] |
      "\n### \(.[0].repository.nameWithOwner) (\(length) PRs reviewed)\n" + (
        .[] | "#\(.number) [\(.state)] by \(.author.login): \(.title)\n  \(.url)"
      )
    end
  ' >> "$OUTPUT"

  # --- Issue Engagement (authored) ---
  echo -e "\n## Issues Authored" >> "$OUTPUT"
  gh search issues \
    --limit 1000 \
    --author="$author" \
    --updated="$DATE_RANGE" \
    --json number,title,state,createdAt,closedAt,url,repository,author \
  | jq -r "$ISSUE_JQ" >> "$OUTPUT"

  # --- Issue Engagement (involved — commented, mentioned, assigned) ---
  echo -e "\n## Issues Engaged (commented/assigned/mentioned)" >> "$OUTPUT"
  gh search issues \
    --limit 1000 \
    --involves="$author" \
    --updated="$DATE_RANGE" \
    --json number,title,state,createdAt,closedAt,url,repository,author \
  | jq -r --arg self "$author" '
    [ .[] | select(.author.login != $self) ] |
    if length == 0 then "No engagement found"
    else
      group_by(.repository.nameWithOwner) |
      .[] |
      "\n### \(.[0].repository.nameWithOwner) (\(length) issues)\n" + (
        .[] | "#\(.number) [\(.state)] by \(.author.login): \(.title)\n  \(.url)"
      )
    end
  ' >> "$OUTPUT"

done
```
