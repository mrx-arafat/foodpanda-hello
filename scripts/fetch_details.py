#!/usr/bin/env python3
"""Fetch vendor details (menus, reviews, photos) for a batch of vendors.
Usage: python3 scripts/fetch_details.py <city> <batch_num> <total_batches>
Saves to data-<city>/vendor_details/*.json and vendor_reviews/*.json
"""
import json, time, sys
from pathlib import Path
from urllib.parse import urlencode
import urllib.request, urllib.error

if len(sys.argv) < 4:
    print("usage: fetch_details.py <city> <batch_num> <total_batches>")
    print("       e.g. fetch_details.py dhaka 1 6")
    sys.exit(1)

CITY = sys.argv[1].lower()
BATCH_NUM = int(sys.argv[2])
TOTAL_BATCHES = int(sys.argv[3])

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / f"data-{CITY}"
if not DATA.exists():
    print(f"error: {DATA} not found")
    sys.exit(1)

(DATA / "vendor_details").mkdir(exist_ok=True)
(DATA / "vendor_reviews").mkdir(exist_ok=True)

HEADERS = {
    "x-disco-client-id": "pd-microfrontend/web-acquisition",
    "x-fp-api-key": "volo",
    "perseus-client-id": "1779641842526.699457642050832131.6divzs17ry",
    "perseus-session-id": "1779641842526.510124908442144053.x8eq8cfci0",
    "user-logged-in": "false",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "origin": "https://www.foodpanda.com.bd",
    "referer": "https://www.foodpanda.com.bd/",
    "user-agent": "Mozilla/5.0",
}

def fetch(url, timeout=30):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=timeout)
        return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return None
    except Exception:
        return None

vendors = json.loads((DATA / "all_vendors.json").read_text())
# chunk vendors across batches
batch_size = (len(vendors) + TOTAL_BATCHES - 1) // TOTAL_BATCHES
batch_vendors = vendors[BATCH_NUM*batch_size : (BATCH_NUM+1)*batch_size]

print(f"[*] {CITY} batch {BATCH_NUM+1}/{TOTAL_BATCHES}: {len(batch_vendors)} vendors")

for i, v in enumerate(batch_vendors):
    code = v.get("code")
    if not code: continue

    # fetch vendor details with menus
    details_url = f"https://bd.fd-api.com/api/v5/vendors/{code}?include=menus,bundles,multiple_discounts&language_id=1&opening_type=delivery&basket_currency=BDT&latitude={v.get('latitude',23.7806)}&longitude={v.get('longitude',90.4193)}"
    details_j = fetch(details_url)
    if details_j:
        (DATA / "vendor_details" / f"{code}.json").write_text(json.dumps(details_j, indent=2, ensure_ascii=False, default=str))

    # fetch reviews
    reviews_url = f"https://reviews-api-bd.fd-api.com/reviews/vendor/{code}?global_entity_id=FP_BD&limit=100&has_dish=true"
    reviews_j = fetch(reviews_url)
    if reviews_j:
        (DATA / "vendor_reviews" / f"{code}.json").write_text(json.dumps(reviews_j, indent=2, ensure_ascii=False, default=str))

    if (i+1) % 50 == 0:
        print(f"  [{i+1}/{len(batch_vendors)}] {code}")
        time.sleep(1)
    time.sleep(0.15)

print(f"[✓] batch {BATCH_NUM+1} done")
