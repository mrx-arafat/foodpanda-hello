#!/usr/bin/env python3
"""Consolidate vendor_details + reviews into organized summary CSVs.
Usage: python3 scripts/consolidate_details.py <city>
Creates: vendor_menus.csv, vendor_reviews_summary.csv
"""
import json, csv, sys
from pathlib import Path
from collections import defaultdict

if len(sys.argv) < 2:
    print("usage: consolidate_details.py <city>")
    sys.exit(1)

CITY = sys.argv[1].lower()
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / f"data-{CITY}"

print(f"[*] consolidating {CITY}...")

# vendor_menus.csv: code, vendor_name, category, dish_name, price, description
with open(DATA / "vendor_menus.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["vendor_code", "vendor_name", "menu_name", "category", "dish_name", "description", "price", "currency"])

    for jf in (DATA / "vendor_details").glob("*.json"):
        try:
            j = json.load(open(jf))
            data = j.get("data", {})
            v_name = data.get("name", "")
            v_code = jf.stem

            menus = data.get("menus", [])
            for menu in menus:
                menu_name = menu.get("name", "")
                categories = menu.get("categories", [])
                for cat in categories:
                    cat_name = cat.get("name", "")
                    dishes = cat.get("dishes", [])
                    for dish in dishes:
                        d_name = dish.get("name", "")
                        d_desc = dish.get("description", "")
                        prices = dish.get("prices", {})
                        price_val = prices.get("default_price", prices.get("price", ""))
                        w.writerow([v_code, v_name, menu_name, cat_name, d_name, d_desc, price_val, "BDT"])
        except Exception as e:
            pass

# vendor_reviews_summary.csv: code, vendor_name, review_count, avg_rating, sample_reviews
with open(DATA / "vendor_reviews_summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["vendor_code", "review_count", "avg_rating", "positive_count", "sample_review_text", "sample_reviewer", "sample_rating"])

    for jf in (DATA / "vendor_reviews").glob("*.json"):
        try:
            j = json.load(open(jf))
            data = j.get("data", [])
            # data can be either: array of reviews (new API) or dict with 'reviews' key (old API)
            reviews = data if isinstance(data, list) else data.get("reviews", [])

            if reviews:
                # Extract ratings from each review (handle both old and new API structures)
                ratings = []
                for r in reviews:
                    if isinstance(r, dict):
                        # New API: ratings is an array with "score" field
                        if "ratings" in r and isinstance(r["ratings"], list):
                            for rating_obj in r["ratings"]:
                                if isinstance(rating_obj, dict) and "score" in rating_obj:
                                    ratings.append(rating_obj["score"])
                        # Old API: direct "rating" field
                        elif "rating" in r:
                            ratings.append(r.get("rating", 0))

                if ratings:
                    avg = sum(ratings) / len(ratings)
                    positive = sum(1 for r in ratings if r >= 4)
                else:
                    avg = 0
                    positive = 0

                first_review = reviews[0]
                # Handle both old and new API field names
                review_text = first_review.get("comment") or first_review.get("text", "")
                reviewer_name = first_review.get("author") or first_review.get("reviewerName", "")
                review_rating = first_review.get("rating", "")

                w.writerow([
                    jf.stem,
                    len(reviews),
                    round(avg, 2) if ratings else 0,
                    positive,
                    review_text[:200] if review_text else "",
                    reviewer_name,
                    review_rating,
                ])
        except Exception:
            pass

print(f"[✓] {CITY}: vendor_menus.csv, vendor_reviews_summary.csv")
