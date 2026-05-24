#!/usr/bin/env python3
"""Scrape foodpanda vendors for a city.
Usage: python3 scripts/scrape.py <city>     # e.g. dhaka | chittagong
Saves into data-<city>/all_vendors.json + raw_pages/
"""
import json, time, sys, hashlib
from pathlib import Path
from urllib.parse import urlencode
import urllib.request, urllib.error

from cities import REGISTRY

if len(sys.argv) < 2:
    print("usage: scrape.py <city>  (cities: " + ", ".join(REGISTRY) + ")")
    sys.exit(1)

CITY = sys.argv[1].lower()
if CITY not in REGISTRY:
    print(f"unknown city: {CITY}. known: {list(REGISTRY)}")
    sys.exit(1)
POINTS = REGISTRY[CITY]

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / f"data-{CITY}"
OUT.mkdir(exist_ok=True)
(OUT / "raw_pages").mkdir(exist_ok=True)

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
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
}

BASE = "https://bd.fd-api.com/vendors-gateway/api/v1/pandora/vendors"
PAGE_SIZE = 96
SLEEP = 0.3
VERTICAL = "restaurants"


def fetch(lat, lng, offset, limit):
    q = {
        "latitude": lat, "longitude": lng, "language_id": 1,
        "include": "characteristics", "configuration": "Original",
        "country": "bd", "customer_id": "", "customer_hash": "",
        "budgets": "", "cuisine": "", "sort": "", "payment_type": "",
        "food_characteristic": "", "use_free_delivery_label": "true",
        "tag_label_metadata": "false", "limit": limit,
        "vertical": VERTICAL, "vertical_type_ids": "",
        "offset": offset, "customer_type": "regular",
    }
    url = f"{BASE}?{urlencode(q)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  ! HTTP {e.code}: {e.read()[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ! err {e}", file=sys.stderr)
        return None


def main():
    print(f"[*] City: {CITY} | {len(POINTS)} search points")
    all_vendors = {}

    for area_name, lat, lng in POINTS:
        print(f"\n[*] {area_name} ({lat},{lng})")
        offset = 0
        fetched = 0
        available = None
        while True:
            j = fetch(lat, lng, offset, PAGE_SIZE)
            if not j or j.get("status_code") != 200:
                print(f"  ! bad response, stop")
                break
            data = j.get("data", {})
            items = data.get("items", [])
            if available is None:
                available = data.get("available_count", 0)
                print(f"  available_count={available}")
            page_id = hashlib.md5(f"{area_name}-{offset}".encode()).hexdigest()[:8]
            safe_name = area_name.replace(' ','_').replace('/', '-').replace('.', '')
            (OUT / "raw_pages" / f"{safe_name}-{offset}-{page_id}.json").write_text(json.dumps(j))
            for v in items:
                code = v.get("code")
                if not code: continue
                if code not in all_vendors:
                    v["_discovered_area"] = area_name
                    all_vendors[code] = v
            fetched += len(items)
            print(f"  offset={offset} got={len(items)} dedup_total={len(all_vendors)}")
            if not items or len(items) < PAGE_SIZE or fetched >= (available or 0):
                break
            offset += PAGE_SIZE
            time.sleep(SLEEP)

    (OUT / "all_vendors.json").write_text(json.dumps(list(all_vendors.values()), indent=2, ensure_ascii=False, default=str))
    print(f"\n[✓] {len(all_vendors)} unique vendors -> {OUT}/all_vendors.json")
    print(f"    next: python3 scripts/organize.py {CITY}")

if __name__ == "__main__":
    main()
