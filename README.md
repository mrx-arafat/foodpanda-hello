# Foodpanda Bangladesh Restaurant Dataset

Complete restaurant data for **5,686 vendors** across **12 cities** in Bangladesh. Includes vendor information, menu details, pricing, customer reviews, ratings, and geographic metadata.

**Latest Update:** May 25, 2025 — Parallel quadrant scraping with 525-point grid coverage achieved **4,806 Dhaka vendors** (89% more than previous extraction).

## Dataset Overview

### Coverage (Latest - May 25, 2025)

| City | Vendors | Status |
|------|---------|--------|
| Dhaka | 4,806 | ✅ Complete (25 core + 500 grid points) |
| Chittagong | 506 | ✅ Complete |
| Sylhet | 213 | ✅ Complete |
| Khulna | 125 | ✅ Complete |
| Rajshahi | 102 | ✅ Complete |
| Barisal | 77 | ✅ Complete |
| Rangpur | 60 | ✅ Complete |
| Mymensingh | 67 | ✅ Complete |
| Comilla | 84 | ✅ Complete |
| Cox's Bazar | 52 | ✅ Complete |
| Bogura | 63 | ✅ Complete |
| Jessore | 37 | ✅ Complete |
| **TOTAL** | **5,686** | **✅ 5,000+ TARGET ACHIEVED** |

### Data Collection Methods

#### Parallel Quadrant Scraping Strategy (Latest)
- **Dhaka Grid:** 525 search points (25 strategic core areas + 500-point 0.01° grid overlay)
- **Quadrant Parallelization:** 4 independent agents scraping NE/NW/SE/SW simultaneously
- **Performance:** 3-4x speedup vs. sequential scraping
- **Coverage:** Captures all delivery hotspots including ECB Chattar, high-density commercial zones

#### APIs Used
- **Vendor List:** Foodpanda's `/vendors-gateway/api/v1/pandora/vendors` (latitude/longitude paginated)
- **Menu Details:** `/api/v5/vendors/{code}` (with menus, bundles, discounts)
- **Customer Reviews:** `/reviews-api-bd.fd-api.com/reviews/vendor/{code}` (aggregated ratings)
- **Geographic Data:** Area centroids + grid coordinates for comprehensive delivery coverage

---

## Data Structure

### Folder Organization

```
foodpanda/
├── README.md                          # This file
├── SETUP.md                           # Complete setup and process guide
├── scripts/
│   ├── cities.py                      # City definitions and area centroids
│   ├── scrape.py                      # Vendor scraper
│   ├── organize.py                    # Organize by area/city/chain
│   ├── fetch_details.py               # Fetch menus and reviews (parallelizable)
│   ├── consolidate_details.py         # Generate CSV reports
│   ├── scrape_all.sh                  # Batch scraper for all cities
│   └── fetch_all_details.sh           # Batch details fetcher with parallel workers
│
└── data-<city>/                       # One folder per city
    ├── all_vendors.json               # All vendors for this city (deduplicated)
    ├── restaurants.csv                # Flat CSV table - easy Excel import
    ├── summary.json                   # Statistics: counts by area/city/chain
    │
    ├── vendor_menus.csv               # Menu items, dishes, prices (if available)
    ├── vendor_reviews_summary.csv     # Consolidated reviews and ratings
    │
    ├── by_area/
    │   ├── area_name.json             # Vendors in specific area
    │   └── ...
    ├── by_city/
    │   ├── city_name.json             # Vendors in city
    │   └── ...
    ├── by_chain/
    │   ├── chain_name.json            # Vendors of specific chain
    │   └── ...
    ├── vendor_details/                # Raw menu/bundle data (JSON)
    │   ├── code1.json
    │   ├── code2.json
    │   └── ...
    └── vendor_reviews/                # Raw review data (JSON)
        ├── code1.json
        ├── code2.json
        └── ...
```

---

## Main Data Files

### 0. `restaurants_all_bangladesh_final.csv` (NEW)

**Master consolidated file with all 5,686 vendors across 12 cities.**

**Format:** CSV with columns: code, id, name, chain, city, area, cuisines, rating, reviews, min_order, delivery_fee, delivery_time, lat, lng, address

**Quick Start:**
```bash
# Import into Excel/Sheets or analyze with Python
import pandas as pd
df = pd.read_csv('restaurants_all_bangladesh_final.csv')
print(f"Total vendors: {len(df)}")
print(f"By city:\n{df['city'].value_counts()}")
```

### 1. `all_vendors.json`

**Complete vendor list for the city** (deduplicated by vendor code).

**File Location:** `data-<city>/all_vendors.json`

**Format:** JSON array of vendor objects

**Sample Entry:**
```json
{
  "code": "tfsc",
  "id": 12345,
  "name": "The Burger Store",
  "cuisines": ["Burgers", "Fast Food"],
  "chain": "The Burger Store",
  "rating": 3.7,
  "reviews": 30,
  "min_order": 99,
  "delivery_fee": 60,
  "delivery_min": 100,
  "latitude": 23.7806,
  "longitude": 90.4193,
  "city": "Dhaka",
  "area": "Dhanmondi",
  "area_distance_km": 1.2,
  "address": "123 Main Street, Dhanmondi, Dhaka",
  "post_code": "1209",
  "url": "https://www.foodpanda.com.bd/restaurant/tfsc/burgers",
  "logo": "https://...",
  "hero_image": "https://...",
  "payment_types": ["Card", "Cash", "bKash"],
  "characteristics": ["Free Delivery", "Fast Delivery"],
  "discounts": [...],
  "vertical": "restaurants"
}
```

**All Available Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | Unique vendor identifier |
| `id` | integer | Numeric vendor ID |
| `name` | string | Restaurant name |
| `cuisines` | array | List of cuisine types (e.g., "Burgers", "Pizza") |
| `chain` | string | Restaurant chain name (if part of chain) |
| `rating` | float | Average customer rating (0-5) |
| `reviews` | integer | Total number of reviews |
| `min_order` | integer | Minimum order amount (BDT) |
| `delivery_fee` | integer | Delivery fee (BDT) |
| `delivery_min` | integer | Minimum delivery amount (BDT) |
| `latitude` | float | Geographic latitude |
| `longitude` | float | Geographic longitude |
| `city` | string | City name |
| `area` | string | Area/locality name |
| `area_distance_km` | float | Distance to area centroid (km) |
| `address` | string | Full address |
| `post_code` | string | Postal code |
| `url` | string | Foodpanda URL link |
| `logo` | string | Logo image URL |
| `hero_image` | string | Banner image URL |
| `payment_types` | array | Accepted payment methods |
| `characteristics` | array | Special features (e.g., "Free Delivery", "24 Hours") |
| `discounts` | array | Active promotional offers |
| `vertical` | string | Business category (usually "restaurants") |

**Use Cases:**
- Get all restaurants in a city
- Search by name, cuisine, or rating
- Find restaurants near a location
- Analyze cuisine distribution

---

### 2. `restaurants.csv`

**Flat, normalized table format** of all vendors — easy to import into Excel, Google Sheets, or databases.

**File Location:** `data-<city>/restaurants.csv`

**Sample Rows:**
```csv
code,id,name,chain,city,area,area_distance_km,cuisines,rating,reviews,min_order,delivery_fee,delivery_min,lat,lng,address,post_code,url
tfsc,12345,The Burger Store,The Burger Store,Dhaka,Dhanmondi,1.2,"[""Burgers"",""Fast Food""]",3.7,30,99,60,100,23.7806,90.4193,123 Main Street,1209,https://...
pc80,54321,Pizza Corner,Pizza Corner,Dhaka,Gulshan,0.8,"[""Pizza"",""Italian""]",3.5,16,150,50,200,23.8106,90.4170,456 Park Road,1212,https://...
```

**Column Descriptions:**

| Column | Type | Example |
|--------|------|---------|
| `code` | string | `tfsc` |
| `id` | integer | `12345` |
| `name` | string | `The Burger Store` |
| `chain` | string | `The Burger Store` |
| `city` | string | `Dhaka` |
| `area` | string | `Dhanmondi` |
| `area_distance_km` | float | `1.2` |
| `cuisines` | string | `["Burgers","Fast Food"]` |
| `rating` | float | `3.7` |
| `reviews` | integer | `30` |
| `min_order` | integer | `99` |
| `delivery_fee` | integer | `60` |
| `delivery_min` | integer | `100` |
| `lat` | float | `23.7806` |
| `lng` | float | `90.4193` |
| `address` | string | `123 Main Street, Dhanmondi` |
| `post_code` | string | `1209` |
| `url` | string | `https://www.foodpanda.com.bd/...` |

**Use Cases:**
- Import into Excel for quick analysis
- Load into databases (SQL, MongoDB)
- Geographic mapping and visualization
- Build restaurant finder apps
- Analyze pricing, ratings, minimum orders

---

### 3. `vendor_reviews_summary.csv`

**Consolidated customer reviews and ratings** for all vendors in the city.

**File Location:** `data-<city>/vendor_reviews_summary.csv`

**Sample Rows:**
```csv
vendor_code,review_count,avg_rating,positive_count,sample_review_text,sample_reviewer,sample_rating
tfsc,30,3.7,54,The burger made me sick 😭,Monir,
pc80,16,3.51,25,"Please..Dakati off koren. you are charging 60tk for a vorta...",Tahseen,
mqt9,15,3.26,18,There is no chicken in the corn soup.,Shagufta,
gdzv,30,3.61,44,The wedges good as always.,Farhan,
```

**Column Descriptions:**

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `vendor_code` | string | `tfsc` | Unique vendor ID |
| `review_count` | integer | `30` | Total number of reviews |
| `avg_rating` | float | `3.7` | Average rating (0-5 scale) |
| `positive_count` | integer | `54` | Count of 4+ star ratings |
| `sample_review_text` | string | "The burger was..." | First review text (200 char limit) |
| `sample_reviewer` | string | "Monir" | Author name of first review |
| `sample_rating` | string | `5` | Rating of first review |

**What the Data Shows:**
- Overall customer satisfaction (via `avg_rating`)
- Review volume and engagement (via `review_count`)
- Quality percentage (via `positive_count` vs `review_count`)
- Typical feedback (via `sample_review_text`)

**Interpretation Guide:**
- **4.0-5.0:** Excellent service and food
- **3.0-3.9:** Good with some issues
- **2.0-2.9:** Below average, frequent complaints
- **Below 2.0:** Poor service, quality issues

**Use Cases:**
- Analyze customer satisfaction by city
- Identify top-rated restaurants
- Find problem restaurants needing improvement
- Sentiment analysis and quality tracking
- Business intelligence dashboards

---

### 4. `vendor_menus.csv`

**Menu items, dishes, categories, and pricing** for vendors (limited availability).

**File Location:** `data-<city>/vendor_menus.csv`

**Note:** This file is sparse because only vendors with successfully fetched details are included. Currently, only ~11 Dhaka vendors have menu data.

**Sample Rows:**
```csv
vendor_code,vendor_name,menu_name,category,dish_name,description,price,currency
tfsc,The Burger Store,Burgers,Specials,Loaded Burger,Double patty with cheese,250,BDT
tfsc,The Burger Store,Burgers,Combos,Burger Combo,Burger + fries + drink,350,BDT
pc80,Pizza Corner,Pizzas,Large,Pepperoni Pizza,12-inch with extra cheese,600,BDT
```

**Column Descriptions:**

| Column | Type | Example |
|--------|------|---------|
| `vendor_code` | string | `tfsc` |
| `vendor_name` | string | `The Burger Store` |
| `menu_name` | string | `Burgers` |
| `category` | string | `Specials` |
| `dish_name` | string | `Loaded Burger` |
| `description` | string | `Double patty with cheese` |
| `price` | integer | `250` |
| `currency` | string | `BDT` |

**Use Cases:**
- Menu comparison across restaurants
- Price analysis by cuisine
- Item popularity tracking
- Restaurant menu mapping
- Food cost analysis

---

### 5. `summary.json`

**Quick statistics** about vendors, areas, and chains in the city.

**File Location:** `data-<city>/summary.json`

**Sample Structure:**
```json
{
  "total_vendors": 2532,
  "by_area": {
    "dhanmondi": 156,
    "gulshan": 234,
    "mirpur": 189,
    ...
  },
  "by_city": {
    "dhaka": 2532
  },
  "by_chain": {
    "burger_king": 8,
    "kfc": 6,
    "dominos": 5,
    ...
  }
}
```

**Use Cases:**
- Quick city overview
- Area popularity ranking
- Chain presence analysis
- Market concentration metrics

---

### 6. Organized Folders

#### `by_area/`

Each area gets its own JSON file with vendors nearest to that area.

```bash
data-dhaka/by_area/
├── dhanmondi.json       # Vendors in Dhanmondi
├── gulshan.json         # Vendors in Gulshan
├── mirpur.json
└── ...
```

**Use:** Geographic filtering, local search, area-specific analysis

#### `by_city/`

Vendors grouped by `city.name` field from API.

```bash
data-dhaka/by_city/
├── dhaka.json
└── ...
```

**Use:** City-level aggregation, cross-city comparison

#### `by_chain/`

Vendors grouped by restaurant chain.

```bash
data-dhaka/by_chain/
├── burger_king.json
├── kfc.json
├── dominos.json
└── ...
```

**Use:** Chain analysis, franchise metrics, competitive intelligence

---

### 7. Raw Data Folders

#### `vendor_details/` (Sparse)

Raw JSON responses from `/api/v5/vendors/{code}?include=menus,bundles,multiple_discounts`

Each file contains: menus, categories, dishes, prices, bundles, discounts.

**Availability:** ~11 files in Dhaka only (API restrictions prevent full download)

#### `vendor_reviews/` (Complete)

Raw JSON responses from `/reviews-api-bd.fd-api.com/reviews/vendor/{code}`

**Sample Structure:**
```json
{
  "data": [
    {
      "text": "Best Sandwich at 60 Taka",
      "reviewerName": "Md.",
      "ratings": [
        { "topic": "overall", "score": 5 },
        { "topic": "restaurant_food", "score": 5 }
      ],
      "createdAt": "2025-08-26T08:37:04Z",
      "likeCount": 0
    },
    ...
  ]
}
```

**Availability:** Complete for all 5,686 vendors across all cities

---

## Usage Examples

### Python / Pandas

```python
import pandas as pd
import json

# Load reviews data
dhaka_reviews = pd.read_csv('data-dhaka/vendor_reviews_summary.csv')

# Load vendors
with open('data-dhaka/all_vendors.json') as f:
    vendors = json.load(f)

# Top 10 restaurants by rating
top_10 = dhaka_reviews.nlargest(10, 'avg_rating')
print(top_10[['vendor_code', 'review_count', 'avg_rating']])

# Average rating by rating tier
dhaka_reviews['rating_tier'] = pd.cut(
    dhaka_reviews['avg_rating'], 
    bins=[0, 2, 3, 4, 5],
    labels=['Poor', 'Fair', 'Good', 'Excellent']
)
print(dhaka_reviews.groupby('rating_tier').size())

# Vendors with most reviews
most_reviewed = dhaka_reviews.nlargest(5, 'review_count')
print(most_reviewed[['vendor_code', 'review_count', 'avg_rating']])
```

### SQL / PostgreSQL

```sql
-- Create table
CREATE TABLE vendors (
  code VARCHAR(10) PRIMARY KEY,
  name VARCHAR(255),
  city VARCHAR(50),
  area VARCHAR(100),
  rating DECIMAL(3,2),
  reviews INT,
  min_order INT,
  delivery_fee INT,
  latitude DECIMAL(10,8),
  longitude DECIMAL(11,8),
  address TEXT
);

-- Import CSV
\COPY vendors FROM 'data-dhaka/restaurants.csv' CSV HEADER;

-- Queries
SELECT * FROM vendors ORDER BY rating DESC LIMIT 10;
SELECT area, COUNT(*) as count, AVG(rating) as avg_rating 
FROM vendors GROUP BY area ORDER BY count DESC;
SELECT city, COUNT(*) FROM vendors GROUP BY city;
```

### Excel / Google Sheets

1. **Open file:** `data-<city>/restaurants.csv`
2. **Import as CSV:** File → Import → Choose CSV
3. **Create charts:**
   - Rating distribution (histogram)
   - Area comparison (bar chart)
   - Price vs rating (scatter plot)
4. **Filter:** Use built-in filters for area, cuisine, rating

### GIS / Mapping

```python
import folium
import pandas as pd

vendors = pd.read_csv('data-dhaka/restaurants.csv')

# Create map centered on Dhaka
map_dhaka = folium.Map(
    location=[23.8103, 90.4125],
    zoom_start=12
)

# Add markers for each vendor
for idx, row in vendors.iterrows():
    color = 'green' if row['rating'] >= 4 else 'orange' if row['rating'] >= 3 else 'red'
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        popup=f"{row['name']}<br>Rating: {row['rating']}/5",
        color=color,
        fill=True,
        radius=5
    ).add_to(map_dhaka)

map_dhaka.save('dhaka_restaurants.html')
```

### JavaScript / Web App

```javascript
// Load vendors
fetch('data-dhaka/restaurants.csv')
  .then(r => r.text())
  .then(csv => {
    const rows = csv.split('\n').slice(1);
    const vendors = rows.map(row => {
      const [code, id, name, chain, city, area, ...rest] = row.split(',');
      return { code, name, chain, city, area };
    });
    
    // Display or process
    console.log(`${vendors.length} vendors loaded`);
  });
```

---

## Data Quality Notes

### Reviews Data
- **Complete:** All 3,238 vendors have review data
- **Quality:** Raw customer feedback, some in Bengali/Bangla
- **Bias:** Likely skewed toward restaurants with active user bases
- **Timeliness:** Reviews up to date as of collection date

### Menu/Details Data
- **Sparse:** Only ~11 vendors in Dhaka (API restrictions)
- **Limitation:** Many vendors don't expose menu details via API
- **Alternative:** Use Foodpanda website scraping for full menus

### Geographic Data
- **Accuracy:** Assigned to nearest area centroid (±2-3km)
- **Limitation:** Only major areas covered
- **Source:** Coordinates from API responses

### Vendor Information
- **Completeness:** All fields from Foodpanda API
- **Updates:** Based on single capture date
- **Chain Info:** May not be updated if restaurants rebrand

---

## Data Refresh & Updates

### Re-scrape a City

```bash
# Update vendor list
python3 scripts/scrape.py dhaka

# Re-organize by area/city/chain
python3 scripts/organize.py dhaka

# Fetch fresh details and reviews
bash scripts/fetch_all_details.sh  # or just for dhaka:
python3 scripts/fetch_details.py dhaka 0 6 &
python3 scripts/fetch_details.py dhaka 1 6 &
# ... 6 workers total
wait

# Regenerate CSVs
python3 scripts/consolidate_details.py dhaka
```

### Add New City

1. **Add city definition** in `scripts/cities.py`:
   ```python
   SYLHET = CityConfig(
       center=(24.8949, 91.8687),
       areas=[
           Area("Sylhet City", 24.8949, 91.8687),
           Area("Moulvibazar", 24.4832, 91.5646),
       ]
   )
   ```

2. **Run scrape workflow:**
   ```bash
   python3 scripts/scrape.py sylhet
   python3 scripts/organize.py sylhet
   python3 scripts/fetch_all_details.sh  # includes new city
   ```

---

## API References

### Endpoints Used

**Vendor List (Public):**
```
GET https://bd.fd-api.com/api/v5/vendors-gateway/api/v1/pandora/vendors?limit=96&offset=0&...
```

**Vendor Details (Limited Access):**
```
GET https://bd.fd-api.com/api/v5/vendors/{code}?include=menus,bundles,multiple_discounts
```

**Reviews (Public):**
```
GET https://reviews-api-bd.fd-api.com/reviews/vendor/{code}?limit=100&has_dish=true
```

### Required Headers

```
x-disco-client-id: pd-microfrontend/web-acquisition
x-fp-api-key: volo
perseus-client-id: <id>
perseus-session-id: <id>
accept: application/json
user-agent: Mozilla/5.0
```

---

## License & Terms

**Data Source:** Foodpanda public APIs (bd.fd-api.com, reviews-api-bd.fd-api.com)

**Restrictions:**
- For personal research and analysis only
- Do not republish or redistribute without attribution
- Respect Foodpanda's terms of service

**Attribution Required:**
> Restaurant data sourced from Foodpanda APIs via Bangladesh food delivery market research.

---

## Support & Issues

### Common Questions

**Q: Why are menus incomplete?**
- A: Foodpanda restricts full menu access via API. Only basic details available.

**Q: Can I get real-time data?**
- A: Use `SETUP.md` to run fresh scrapes anytime.

**Q: How often is data updated?**
- A: Data is static from collection date. Run `scripts/scrape.py <city>` to refresh.

**Q: Can I use this for commercial purposes?**
- A: Check Foodpanda's Terms of Service first.

### Troubleshooting

See `SETUP.md` for complete troubleshooting guide covering:
- mitmproxy certificate issues
- API errors (403 Forbidden, etc.)
- Rate limiting
- Parallel worker failures
- Data consolidation issues

---

## Dataset Statistics (Complete)

```
Total Vendors: 5,686
Total Cities: 12
Geographic Coverage: 525 grid points in Dhaka + strategic areas in all cities
Total Reviews: 5,686 vendors (100% coverage via reviews API)
Average Rating: 3.8/5
Vendors with 4+ rating: ~52%
Top Cuisine: Asian (36.6% in Dhaka), Snacks (30.3%), Rice Dishes (28.8%)
Average Min Order: 50 BDT
Average Delivery Fee: 0 BDT (platform subsidized)
Average Delivery Time: 20 minutes
```

---

## Related Files

- **`SETUP.md`** — Complete setup guide from mitmproxy to data consolidation
- **`scripts/cities.py`** — City and area definitions
- **`scripts/scrape.py`** — Vendor scraper
- **`scripts/organize.py`** — Geographic/chain organization
- **`scripts/fetch_details.py`** — Details and reviews fetcher (parallelizable)
- **`scripts/consolidate_details.py`** — CSV report generator

---

**Last Updated:** May 25, 2025  
**Data Collection Method:** Parallel quadrant scraping with 525-point Dhaka grid + strategic areas for all 12 cities  
**Coverage:** 5,686 vendors across 12 cities (Dhaka: 4,806 vendors)  
**Collection Status:** Complete extraction achieved with parallel 4-agent quadrant strategy
# foodpanda-bd-dataset
