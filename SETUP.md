# Foodpanda Data Collection - Complete Setup Guide

A comprehensive guide to capturing Foodpanda APIs and scraping restaurant data across Bangladesh using mitmproxy and parallel workers.

## Table of Contents

1. [Prerequisites & Installation](#prerequisites--installation)
2. [Phase 1: API Capture with mitmproxy](#phase-1-api-capture-with-mitmproxy)
3. [Phase 2: Vendor Discovery & Organization](#phase-2-vendor-discovery--organization)
4. [Phase 3: Details & Reviews Fetching](#phase-3-details--reviews-fetching)
5. [Phase 4: Data Consolidation](#phase-4-data-consolidation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites & Installation

### System Requirements

- **macOS/Linux** (tested on macOS 12+)
- **Python 3.12+** with `uv` package manager
- **mitmproxy 11+** - MITM proxy tool
- **Chrome/Chromium** - Real browser for browsing (headless doesn't work due to PerimeterX anti-bot)
- **4GB RAM minimum** (6GB+ recommended for parallel processing)

### Installation Steps

#### 1. Install mitmproxy

```bash
# On macOS (Homebrew)
brew install mitmproxy

# Or with pip
pip install mitmproxy

# Verify installation
mitmproxy --version
```

#### 2. Clone/Setup Project

```bash
# Navigate to project directory
cd /path/to/foodpanda

# Create data directories
mkdir -p captures exports specs data-{dhaka,chittagong,sylhet,khulna,rajshahi,barisal,rangpur,mymensingh,comilla,coxsbazar,bogura,jessore}

# Create scripts directories
mkdir -p scripts
```

#### 3. Install Python Dependencies

```bash
# Using uv (recommended)
uv pip install -q \
    mitmproxy \
    mitmproxy2swagger \
    pyyaml \
    requests \
    urllib3

# Or with pip
pip install mitmproxy mitmproxy2swagger pyyaml requests urllib3
```

---

## Phase 1: API Capture with mitmproxy

### Goal

Intercept all API calls to Foodpanda and extract endpoint information, request/response structures, and authentication headers.

### Step 1: Start mitmproxy in Web UI Mode

```bash
# Start mitmweb on port 8080 (proxy) and 8081 (web UI)
mitmweb --listen-host 127.0.0.1 --listen-port 8080
```

The web UI will open at `http://localhost:8081`. Leave this running.

### Step 2: Configure System Proxy (macOS)

```bash
# Set HTTP and HTTPS proxy to localhost:8080
networksetup -setwebproxy "Wi-Fi" 127.0.0.1 8080
networksetup -setsecurewebproxy "Wi-Fi" 127.0.0.1 8080

# Enable proxy
networksetup -setwebproxystate "Wi-Fi" on
networksetup -setsecurewebproxystate "Wi-Fi" on
```

### Step 3: Install mitmproxy Certificate

```bash
# Trust the mitmproxy CA certificate
open /Users/$USER/.mitmproxy/mitmproxy-ca-cert.pem

# In Keychain:
# 1. Double-click the certificate
# 2. Trust section -> set "When using this certificate" to "Always Trust"
# 3. Close and enter password
```

### Step 4: Browse Foodpanda and Capture Traffic

```bash
# Open Chrome (with proxy configured)
open "https://www.foodpanda.com.bd"
```

**Important:** Real Chrome is required. Headless browsers trigger PerimeterX anti-bot protection.

In the browser:
1. **Search for restaurants** — generates vendor list API calls
2. **Visit vendor pages** — captures menu/details endpoints
3. **Scroll through reviews** — captures reviews API calls
4. **Check different areas** — generates geographic search queries
5. **Try filtering** — captures search and filter endpoints

Let traffic accumulate for **5-10 minutes** with various interactions.

### Step 5: Stop Capture and Save

```bash
# In mitmweb UI:
# 1. Go to File menu
# 2. Click "Save" or use Ctrl+S
# 3. Save to: captures/foodpanda.mitm

# Or save via command line (if using capture.sh)
# Press Ctrl+C in terminal running mitmweb
```

### Step 6: Verify Capture

```bash
# Check capture file size
ls -lh captures/foodpanda.mitm

# Should be 10MB+ if you captured sufficient traffic
# Expected: 50-150MB depending on browsing time
```

### Step 7: Generate API Documentation

```bash
# Extract endpoint list (filter for API hosts only)
mitmdump -q -nr captures/foodpanda.mitm -s scripts/filter.py | sort -u > exports/endpoints.txt

# Generate HAR file (for Postman/Insomnia import)
mitmdump -q -nr captures/foodpanda.mitm --set hardump=exports/foodpanda.har

# Generate OpenAPI specs for each host
for HOST in bd.fd-api.com reviews-api-bd.fd-api.com disco.deliveryhero.io geocoder.deliveryhero.io; do
  echo "Generating spec for $HOST..."
  mitmproxy2swagger -i captures/foodpanda.mitm -o specs/$HOST.yaml -p https://$HOST -f flow --examples
  sed -i '' 's|- ignore:|- |' specs/$HOST.yaml
  # Run again to fill in request/response schemas
  mitmproxy2swagger -i captures/foodpanda.mitm -o specs/$HOST.yaml -p https://$HOST -f flow --examples
done
```

### What You Should Have Now

```
captures/
└── foodpanda.mitm           # Raw captured flows (50-150MB)

exports/
├── endpoints.txt            # List of all discovered endpoints
└── foodpanda.har            # All requests/responses in HAR format

specs/
├── bd.fd-api.com.yaml       # Main vendor/menu API spec
├── reviews-api-bd.fd-api.com.yaml
├── disco.deliveryhero.io.yaml
├── geocoder.deliveryhero.io.yaml
└── www.foodpanda.com.bd.yaml
```

---

## Phase 2: Vendor Discovery & Organization

### Goal

Scrape all vendors across 12 Bangladesh cities, deduplicate them, and organize by geographic area, city, and chain.

### Step 1: Configure Cities

Edit `scripts/cities.py` and ensure all city centroids are defined:

```python
REGISTRY = {
    "dhaka": CityConfig(
        center=(23.8103, 90.4125),
        areas=[
            Area("Dhanmondi", 23.7478, 90.3745),
            Area("Gulshan", 23.8106, 90.4170),
            # ... more areas
        ],
    ),
    "chittagong": CityConfig(...),
    # ... 10 more cities
}
```

### Step 2: Scrape Vendors for Each City

```bash
# Single city
python3 scripts/scrape.py dhaka

# All cities (sequential)
for city in dhaka chittagong sylhet khulna rajshahi barisal rangpur mymensingh comilla coxsbazar bogura jessore; do
  echo "[*] Scraping $city..."
  python3 scripts/scrape.py "$city"
done

# Or use batch script
bash scripts/scrape_all.sh
```

**What this does:**
- Fetches vendors from `/vendors-gateway/api/v1/pandora/vendors` endpoint
- Uses pagination (limit=96, offset increments)
- Deduplicates by vendor `code`
- Saves to `data-<city>/all_vendors.json`

**Expected output:**
```
data-dhaka/all_vendors.json       # 2,532 vendors
data-chittagong/all_vendors.json  # 287 vendors
# ... etc
```

### Step 3: Organize Vendors by Area/City/Chain

```bash
# Single city
python3 scripts/organize.py dhaka

# All cities
for city in dhaka chittagong sylhet khulna rajshahi barisal rangpur mymensingh comilla coxsbazar bogura jessore; do
  echo "[*] Organizing $city..."
  python3 scripts/organize.py "$city"
done
```

**What this does:**
- Assigns vendors to nearest geographic area (haversine distance)
- Groups vendors by `city.name` field
- Groups vendors by `chain` name
- Generates `restaurants.csv` with all vendor metadata
- Creates `summary.json` with statistics

**Output structure:**
```
data-<city>/
├── all_vendors.json           # All vendors (deduplicated)
├── restaurants.csv            # Flat table format
├── summary.json               # Area/city/chain counts
├── by_area/
│   ├── dhanmondi.json         # Vendors in this area
│   ├── gulshan.json
│   └── ...
├── by_city/
│   ├── dhaka.json
│   └── ...
└── by_chain/
    ├── barisal_food_court.json
    ├── burger_king.json
    └── ...
```

### Step 4: Verify Organization

```bash
# Check vendor counts
for city in dhaka chittagong sylhet; do
  count=$(python3 -c "import json; print(len(json.load(open('data-$city/all_vendors.json'))))")
  echo "$city: $count vendors"
done

# View summary
cat data-dhaka/summary.json | head -30
```

---

## Phase 3: Details & Reviews Fetching

### Goal

Fetch menu details and customer reviews for all 3,238 vendors across 12 cities using parallel workers.

### Step 1: Understand the Script

`scripts/fetch_details.py` fetches:
- **Vendor details** — full menus, categories, dishes, prices from `/api/v5/vendors/{code}`
- **Reviews** — customer ratings and comments from `/reviews-api-bd.fd-api.com/reviews/vendor/{code}`

Saves to:
- `data-<city>/vendor_details/{code}.json`
- `data-<city>/vendor_reviews/{code}.json`

### Step 2: Run Single City with Parallel Workers

```bash
# Dhaka has 2,532 vendors. Use 6 parallel workers.
# Each worker processes a batch: vendors divided into 6 segments

python3 scripts/fetch_details.py dhaka 0 6 &  # Worker 1: vendors 0-420
python3 scripts/fetch_details.py dhaka 1 6 &  # Worker 2: vendors 421-840
python3 scripts/fetch_details.py dhaka 2 6 &  # Worker 3: vendors 841-1260
python3 scripts/fetch_details.py dhaka 3 6 &  # Worker 4: vendors 1261-1680
python3 scripts/fetch_details.py dhaka 4 6 &  # Worker 5: vendors 1681-2100
python3 scripts/fetch_details.py dhaka 5 6 &  # Worker 6: vendors 2101-2532

# Wait for all to complete
wait
echo "Dhaka complete!"
```

### Step 3: Run All Cities (Automated)

```bash
# Use the batch script for all 12 cities
bash scripts/fetch_all_details.sh

# This:
# 1. Loops through all 12 cities
# 2. Launches 6 workers per city
# 3. Workers process in parallel
# 4. Waits for city to complete before moving to next
# 5. Logs progress to /tmp/fetch_progress.log
```

**Timing estimate:**
- Small cities (30-100 vendors): 1-2 minutes per city
- Medium cities (100-300 vendors): 2-5 minutes per city
- Large cities (Dhaka with 2,532): 4-6 minutes per city
- **Total: 30-45 minutes** for all 12 cities

### Step 4: Monitor Progress

```bash
# Watch progress in real-time
tail -f /tmp/fetch_progress.log

# Expected output:
# [*] dhaka - launching 6 parallel workers...
# [*] dhaka batch 0/6: 422 vendors
#   [50/422] a19x
#   [100/422] a2dq
#   ...
#   [✓] batch 0 done
# [✓] dhaka done
# [*] chittagong - launching 6 parallel workers...
# ...
```

### Step 5: Verify Fetch Completion

```bash
# Count fetched details and reviews per city
for city in dhaka chittagong sylhet khulna rajshahi barisal rangpur mymensingh comilla coxsbazar bogura jessore; do
  det=$(find data-$city/vendor_details -name "*.json" 2>/dev/null | wc -l)
  rev=$(find data-$city/vendor_reviews -name "*.json" 2>/dev/null | wc -l)
  echo "$city: $det details, $rev reviews"
done

# Expected (all vendors should have reviews):
# dhaka: 11 details, 2532 reviews
# chittagong: 0 details, 287 reviews
# ... etc
# (Some details may fail due to API restrictions, but reviews should be complete)
```

---

## Phase 4: Data Consolidation

### Goal

Consolidate scattered JSON files into organized CSV tables for easy analysis and export.

### Step 1: Generate Consolidated CSVs

```bash
# Single city
python3 scripts/consolidate_details.py dhaka

# All cities
for city in dhaka chittagong sylhet khulna rajshahi barisal rangpur mymensingh comilla coxsbazar bogura jessore; do
  echo "[*] Consolidating $city..."
  python3 scripts/consolidate_details.py "$city"
done
```

**What this generates:**

#### `vendor_reviews_summary.csv`
Consolidated reviews for all vendors in the city.

Columns:
- `vendor_code` — Unique vendor ID
- `review_count` — Total reviews for this vendor
- `avg_rating` — Average rating (0-5)
- `positive_count` — Count of 4+ star ratings
- `sample_review_text` — First review text (first 200 chars)
- `sample_reviewer` — Author of first review
- `sample_rating` — Rating of first review

#### `vendor_menus.csv`
Menu items and pricing (if vendor details were fetched).

Columns:
- `vendor_code` — Unique vendor ID
- `vendor_name` — Restaurant name
- `menu_name` — Menu category name
- `category` — Dish category (e.g., "Mains", "Appetizers")
- `dish_name` — Dish/item name
- `description` — Item description
- `price` — Item price
- `currency` — Currency (BDT)

### Step 2: Verify Consolidation

```bash
# Check file sizes and row counts
for city in dhaka chittagong sylhet; do
  rev_lines=$(wc -l < data-$city/vendor_reviews_summary.csv)
  menu_lines=$(wc -l < data-$city/vendor_menus.csv)
  echo "$city: $rev_lines reviews, $menu_lines menu items"
done

# Sample data
head -5 data-dhaka/vendor_reviews_summary.csv
```

### Step 3: Export and Analyze

```bash
# Open in Excel
open data-dhaka/vendor_reviews_summary.csv

# Or process with Python/R
python3 << 'EOF'
import pandas as pd

# Load all city reviews
dhaka = pd.read_csv('data-dhaka/vendor_reviews_summary.csv')
chittagong = pd.read_csv('data-chittagong/vendor_reviews_summary.csv')

# Statistics
print(f"Dhaka avg rating: {dhaka['avg_rating'].mean():.2f}")
print(f"Chittagong avg rating: {chittagong['avg_rating'].mean():.2f}")

# Top rated vendors
print("\nTop 5 Dhaka vendors:")
print(dhaka.nlargest(5, 'avg_rating')[['vendor_code', 'review_count', 'avg_rating']])
EOF
```

---

## Complete Workflow Summary

### Quick Reference Commands

```bash
# Phase 1: Capture APIs
mitmweb --listen-host 127.0.0.1 --listen-port 8080
# Browse foodpanda.com.bd, then Ctrl+C and save

# Phase 2: Scrape & Organize
bash scripts/scrape_all.sh

# Phase 3: Fetch Details & Reviews
bash scripts/fetch_all_details.sh

# Phase 4: Consolidate
for city in dhaka chittagong sylhet khulna rajshahi barisal rangpur mymensingh comilla coxsbazar bogura jessore; do
  python3 scripts/consolidate_details.py "$city"
done
```

### One-Liner (After Initial Setup)

```bash
# Run complete workflow for a fresh city
python3 scripts/scrape.py newcity && \
python3 scripts/organize.py newcity && \
python3 scripts/fetch_details.py newcity 0 6 && \
python3 scripts/fetch_details.py newcity 1 6 && \
python3 scripts/fetch_details.py newcity 2 6 && \
python3 scripts/fetch_details.py newcity 3 6 && \
python3 scripts/fetch_details.py newcity 4 6 && \
python3 scripts/fetch_details.py newcity 5 6 && \
wait && \
python3 scripts/consolidate_details.py newcity
```

---

## Troubleshooting

### Common Issues

#### Issue: "PerimeterX Challenge" Blocking Requests

**Cause:** Headless Chrome or curl requests trigger anti-bot protection.

**Solution:**
- Use real Chrome browser for all browsing
- Don't use headless mode
- Use mitmproxy to intercept real browser traffic

#### Issue: "Invalid Client Id" or HTTP 403 Errors

**Cause:** Missing or incorrect headers in API requests.

**Solution:** Ensure these headers are included in `fetch_details.py`:
```python
HEADERS = {
    "x-disco-client-id": "pd-microfrontend/web-acquisition",
    "x-fp-api-key": "volo",
    "perseus-client-id": "1779641842526.699457642050832131.6divzs17ry",
    "perseus-session-id": "1779641842526.510124908442144053.x8eq8cfci0",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0",
}
```

#### Issue: mitmproxy Certificate Not Trusted

**Cause:** SSL certificate not properly installed.

**Solution:**
```bash
# Re-install certificate
open /Users/$USER/.mitmproxy/mitmproxy-ca-cert.pem
# In Keychain, set to "Always Trust"

# Or restart mitmweb
pkill mitmweb
rm -rf /Users/$USER/.mitmproxy/mitmproxy-ca-cert.*
mitmweb
```

#### Issue: Reviews/Details Fetch Hangs

**Cause:** Network timeout or API rate limiting.

**Solution:**
- Check network connection
- Reduce worker count (use 3 instead of 6)
- Increase sleep time in `fetch_details.py` (line 77: change 0.15 to 0.5)

```python
# In fetch_details.py, line 77
time.sleep(0.5)  # Increase from 0.15 to reduce rate limit errors
```

#### Issue: Empty vendor_reviews_summary.csv

**Cause:** Review JSON structure changed or consolidation script expects old format.

**Solution:**
- Check actual review JSON structure:
  ```bash
  head -20 data-dhaka/vendor_reviews/a19x.json
  ```
- Update `consolidate_details.py` to match actual API response format
- Re-run consolidation

### Performance Optimization

**Increase Speed:**
```bash
# Use more workers (if system has RAM)
for i in {0..11}; do
  python3 scripts/fetch_details.py dhaka $i 12 &
done
wait
```

**Reduce Rate Limiting Errors:**
```bash
# Edit fetch_details.py: increase sleep time
sed -i '' 's/time.sleep(0.15)/time.sleep(0.5)/' scripts/fetch_details.py
```

**Monitor Memory Usage:**
```bash
# Watch system resources during fetch
top -o MEM -o CPU

# If memory low, reduce workers:
# Use 3 workers instead of 6
```

---

## Next Steps

Once data is consolidated:

1. **Analyze in Spreadsheet** — Open CSVs in Excel/Google Sheets
2. **Build Database** — Import CSVs to PostgreSQL/MongoDB
3. **Create API** — Build REST API serving the data
4. **Visualize** — Create dashboards with restaurant metrics
5. **Machine Learning** — Train models on reviews/ratings

See `README.md` for data documentation and usage examples.
