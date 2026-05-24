#!/usr/bin/env bash
# Scrape + organize every city in cities.py REGISTRY (skip dhaka, chittagong - already done).
set -e
cd "$(dirname "$0")/.."

CITIES="${@:-sylhet khulna rajshahi barisal rangpur mymensingh comilla coxsbazar bogura jessore}"

for c in $CITIES; do
  echo
  echo "================================================================"
  echo "  $c"
  echo "================================================================"
  python3 scripts/scrape.py "$c" 2>&1 | tail -5
  python3 scripts/organize.py "$c" 2>&1 | grep -E "(BY CITY|Total unique|^  )" | head -15
  rm -rf "data-$c/raw_pages"
done

echo
echo "================================================================"
echo "  SUMMARY (all cities)"
echo "================================================================"
for d in data-*/; do
  n=$(python3 -c "import json; print(len(json.load(open('$d/all_vendors.json'))))")
  printf "  %-15s %5d\n" "${d%/}" "$n"
done
