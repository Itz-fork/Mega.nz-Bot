#!/bin/bash

# Header
echo -e "\e[1m\e[101m Generating update log file... \e[0m"

# Get the latest commit message
commit_message=$(git log -1 --pretty=%B)

# Extract the version and the message from the commit message
version=$(echo "$commit_message" | awk 'NR==1' | cut -d':' -f2 | tr -d '[]')
message=$(echo "$commit_message" | awk 'NR==2')

# Get the commit hash and date
commit=$(git log -1 --pretty=%H)
date=$(git log -1 --pretty=%cd --date=short)

# Create the JSON file
jq -n \
  --arg version "$version" \
  --arg commit "$commit" \
  --arg date "$date" \
  --arg message "$message" \
  '{
    version: $version,
    commit: $commit,
    date: $date,
    message: $message
  }' > updates.json

# End
echo -e "\r\033[1A\033[2K\e[1m\e[101m Done \e[0m"