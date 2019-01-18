#! /bin/sh
set -e

find . -name '*.tf' -type f -print0 | xargs -0 -n1 dirname | sort -u | while read file; do
  terraform validate $file
  if [[ $? -eq 1 ]]; then
    exit 1;
  fi
done

echo "Terraform files linted, no failures detected"
