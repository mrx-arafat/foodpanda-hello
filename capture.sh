#!/usr/bin/env bash
# One-shot capture: launches mitmweb + isolated Chrome on foodpanda.
# Ctrl+C -> auto-stops, generates OpenAPI spec + HAR + endpoint list.
set -e
cd "$(dirname "$0")"

TARGET="https://www.foodpanda.com.bd/"
HOST_FILTER="foodpanda"
FLOW="captures/foodpanda.mitm"
SPEC="specs/foodpanda.yaml"
HAR="exports/foodpanda.har"
ENDPOINTS="exports/endpoints.txt"
CHROME_PROFILE="$HOME/.mitmproxy/chrome-foodpanda"
LOG="captures/mitmweb.log"

mkdir -p captures specs exports "$CHROME_PROFILE"

cleanup() {
  echo
  echo "[*] Stopping capture..."
  [[ -n "${MITM_PID:-}" ]] && kill "$MITM_PID" 2>/dev/null || true
  wait "$MITM_PID" 2>/dev/null || true

  if [[ ! -s "$FLOW" ]]; then
    echo "[!] No flows captured. Done."
    exit 0
  fi

  echo "[*] Generating OpenAPI spec..."
  mitmproxy2swagger -i "$FLOW" -o "$SPEC" -p "https://www.foodpanda.com.bd" -f flow --examples >/dev/null 2>&1 || true
  mitmproxy2swagger -i "$FLOW" -o "$SPEC" -p "https://www.foodpanda.com.bd" -f flow --examples >/dev/null 2>&1 || true

  echo "[*] Exporting HAR..."
  mitmdump -q -nr "$FLOW" --set hardump="$HAR" >/dev/null 2>&1 || true

  echo "[*] Listing endpoints (API-only, foodpanda hosts)..."
  mitmdump -q -nr "$FLOW" -s <(cat <<'PY'
import re
from mitmproxy import http
SKIP = re.compile(r"\.(png|jpg|jpeg|gif|svg|woff2?|ttf|css|ico|webp|mp4|js|map)(\?|$)", re.I)
def response(flow: http.HTTPFlow):
    r = flow.request
    if "foodpanda" not in r.pretty_host: return
    if SKIP.search(r.path.split("?")[0]): return
    ct = (flow.response.headers.get("content-type","") if flow.response else "")
    if flow.response and not any(t in ct for t in ("json","xml","graphql","text/plain")): return
    s = flow.response.status_code if flow.response else "-"
    print(f"{r.method:6} {s} {r.pretty_url}")
PY
) 2>/dev/null | sort -u > "$ENDPOINTS" || true

  echo
  echo "[✓] Done."
  echo "    Flows:     $FLOW ($(du -h "$FLOW" | cut -f1))"
  echo "    Spec:      $SPEC"
  echo "    HAR:       $HAR"
  echo "    Endpoints: $ENDPOINTS ($(wc -l < "$ENDPOINTS" | tr -d ' ') unique)"
  echo
  echo "    Edit $SPEC: remove 'ignore:' from paths you want, then re-run:"
  echo "    mitmproxy2swagger -i $FLOW -o $SPEC -p https://www.foodpanda.com.bd -f flow --examples"
}
trap cleanup EXIT INT TERM

echo "[*] Starting mitmweb on :8080 (UI :8081)..."
mitmweb \
  --listen-port 8080 \
  --web-port 8081 \
  --no-web-open-browser \
  --save-stream-file "$FLOW" \
  > "$LOG" 2>&1 &
MITM_PID=$!

sleep 2
if ! kill -0 "$MITM_PID" 2>/dev/null; then
  echo "[!] mitmweb failed. Log:"
  cat "$LOG"
  exit 1
fi

echo "[*] Launching isolated Chrome -> $TARGET"
open -na "Google Chrome" --args \
  --user-data-dir="$CHROME_PROFILE" \
  --proxy-server="127.0.0.1:8080" \
  "$TARGET" 2>/dev/null || {
    echo "[!] Chrome not found. Manual: configure browser proxy 127.0.0.1:8080 and visit $TARGET"
  }

echo
echo "[✓] Capturing. mitmweb UI: http://127.0.0.1:8081"
echo "    Browse the site. Press Ctrl+C here when done."
echo

wait "$MITM_PID"
