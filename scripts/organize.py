#!/usr/bin/env python3
"""Regroup vendors by nearest area (haversine) + by city + by chain.
Usage: python3 scripts/organize.py <city>
"""
import json, csv, math, shutil, sys
from pathlib import Path
from collections import defaultdict, Counter

from cities import REGISTRY

if len(sys.argv) < 2:
    print("usage: organize.py <city>")
    sys.exit(1)
CITY = sys.argv[1].lower()
POINTS = REGISTRY[CITY]

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / f"data-{CITY}"

def hav(lat1, lng1, lat2, lng2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1); dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
    return 2*R*math.asin(math.sqrt(a))

def nearest(lat, lng):
    if lat is None or lng is None: return ("Unknown", None)
    best = min(POINTS, key=lambda p: hav(lat, lng, p[1], p[2]))
    return (best[0], hav(lat, lng, best[1], best[2]))

vendors = json.loads((DATA / "all_vendors.json").read_text())
print(f"loaded {len(vendors)} vendors from {DATA}")

for d in ["by_area", "by_city", "by_chain"]:
    p = DATA / d
    if p.exists(): shutil.rmtree(p)
    p.mkdir()

by_area = defaultdict(list)
by_city = defaultdict(list)
by_chain = defaultdict(list)
chain_counts = Counter()

for v in vendors:
    area, dist = nearest(v.get("latitude"), v.get("longitude"))
    v["_area"] = area
    v["_area_distance_km"] = round(dist, 2) if dist is not None else None
    by_area[area].append(v)
    city = (v.get("city") or {}).get("name") or "Unknown"
    by_city[city].append(v)
    chain = (v.get("chain") or {}).get("name")
    if chain:
        by_chain[chain].append(v)
        chain_counts[chain] += 1

for k in by_area: by_area[k].sort(key=lambda v: (v.get("_area_distance_km") or 99))
for k in by_city: by_city[k].sort(key=lambda v: -(v.get("rating") or 0))
for k in by_chain: by_chain[k].sort(key=lambda v: v.get("name",""))

def safe(s): return "".join(c if c.isalnum() or c in "._- " else "_" for c in s).replace(" ","_")

for area, vs in by_area.items():
    (DATA / "by_area" / f"{safe(area)}.json").write_text(json.dumps(vs, indent=2, ensure_ascii=False, default=str))
for city, vs in by_city.items():
    (DATA / "by_city" / f"{safe(city)}.json").write_text(json.dumps(vs, indent=2, ensure_ascii=False, default=str))
for chain, vs in by_chain.items():
    (DATA / "by_chain" / f"{safe(chain)}.json").write_text(json.dumps(vs, indent=2, ensure_ascii=False, default=str))

(DATA / "all_vendors.json").write_text(json.dumps(vendors, indent=2, ensure_ascii=False, default=str))

with open(DATA / "restaurants.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["code","id","name","chain","city","area","area_dist_km","cuisines","rating","reviews",
                "min_order","delivery_fee","delivery_min","lat","lng","address","post_code","url"])
    for v in vendors:
        chain = (v.get("chain") or {}).get("name") or ""
        city = (v.get("city") or {}).get("name") or ""
        cuisines = "|".join(c.get("name","") for c in (v.get("cuisines") or []))
        url = v.get("web_path") or v.get("redirection_url") or ""
        if url and url.startswith("/"): url = "https://www.foodpanda.com.bd" + url
        w.writerow([
            v.get("code"), v.get("id"), v.get("name"), chain, city,
            v.get("_area"), v.get("_area_distance_km"), cuisines,
            v.get("rating"), v.get("review_number"),
            v.get("minimum_order_amount"), v.get("minimum_delivery_fee"),
            v.get("minimum_delivery_time"),
            v.get("latitude"), v.get("longitude"),
            v.get("address"), v.get("post_code"), url,
        ])

print("\n=== BY AREA ===")
for a, vs in sorted(by_area.items(), key=lambda x: -len(x[1])):
    print(f"  {a:20} {len(vs):4}")
print("\n=== BY CITY ===")
for c, vs in sorted(by_city.items(), key=lambda x: -len(x[1])):
    print(f"  {c:20} {len(vs):4}")
print(f"\n=== TOP 15 CHAINS ===")
for chain, n in chain_counts.most_common(15):
    print(f"  {chain:35} {n:3}")
print(f"\nIndependents: {sum(1 for v in vendors if not (v.get('chain') or {}).get('name'))}")
print(f"Total unique: {len(vendors)}")

summary = {
    "city_scraped": CITY,
    "total_unique_vendors": len(vendors),
    "by_area": {a: len(vs) for a, vs in by_area.items()},
    "by_city": {c: len(vs) for c, vs in by_city.items()},
    "top_chains": dict(chain_counts.most_common(30)),
    "independents": sum(1 for v in vendors if not (v.get("chain") or {}).get("name")),
}
(DATA / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
