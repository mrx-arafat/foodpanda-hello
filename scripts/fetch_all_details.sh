#!/usr/bin/env bash
# Fetch vendor details for all cities in parallel (6 workers per city).
set -e
cd "$(dirname "$0")/.."

CITIES="${@:-dhaka chittagong sylhet khulna rajshahi barisal rangpur bogura mymensingh comilla coxsbazar jessore}"
WORKERS=6

for city in $CITIES; do
  [ -d "data-$city" ] || { echo "skip $city (not scraped)"; continue; }
  echo "[*] $city - launching $WORKERS parallel workers..."

  for w in $(seq 0 $((WORKERS-1))); do
    python3 scripts/fetch_details.py "$city" "$w" "$WORKERS" &
  done
  wait
  echo "[✓] $city done"
done

echo "[✓] all vendors: details + reviews fetched"
