# FOODPANDA DHAKA - COMPLETE SECURITY RESEARCH DATA EXTRACT

## 📊 Executive Summary
- **Total Vendors Scraped**: 1,892 unique restaurants
- **Total Records**: 1,978 vendor entries (with duplicates/branches)
- **Coverage**: Dhaka + 5 adjacent cities (Narayanganj, Savar, Gazipur, Chittagong, Naogaon)
- **Data Completeness**: 95%+ structured data, 100% location data, 73% review data
- **Extraction Date**: May 24-25, 2025

---

## 🗺️ GEOGRAPHIC COVERAGE

### Primary Market (Dhaka Proper)
- **1,805 vendors** in Dhaka city proper
- **138 neighborhoods** mapped with vendor distribution
- **Highest Density Areas**:
  1. Gulshan 1: 74 vendors
  2. Gulshan 2: 68 vendors
  3. Uttara Sector 6: 56 vendors
  4. Link Road: 45 vendors
  5. Uttara Sector 1: 42 vendors
  6. Monipur: 42 vendors
  7. West Rampura: 39 vendors
  8. Mirpur 1: 38 vendors
  9. Narayanganj (outside): 37 vendors
  10. Bashundhara R/A: 32 vendors

### Secondary Markets
- **Narayanganj**: 53 vendors (logistics hub nearby Dhaka)
- **Savar**: 19 vendors
- **Gazipur**: 11 vendors
- **Chittagong**: 2 vendors (overlapping chains)
- **Naogaon**: 1 vendor

---

## 🏪 RESTAURANT ECOSYSTEM

### Chain vs Independent
- **Chain Restaurants**: 478 (25.3%)
- **Independent Vendors**: 1,414 (74.7%)

### Top 15 Restaurant Chains
| Rank | Chain Name | Locations |
|------|-----------|-----------|
| 1 | Mithai - Dhaka | 63 |
| 2 | Shumi's Hot Cake | 25 |
| 3 | CP Five Star | 15 |
| 4 | Puro Pastry & Bakery - Dhaka | 14 |
| 5 | Domino's Pizza | 11 |
| 6 | Indulge | 9 |
| 7 | Tehari Ghar | 7 |
| 8 | Delifrance Gulshan Avenue | 7 |
| 9 | Tasty Treat | 6 |
| 10 | Tabaq | 6 |
| 11 | Chatime | 6 |
| 12 | Cheez | 5 |
| 13 | THE BIG Q | 5 |
| 14 | Greens & Seeds | 5 |
| 15 | UTSHOB | 5 |

---

## ⭐ RATING & QUALITY METRICS

### Rating Distribution (1,894 rated vendors)
- **Average Rating**: 4.2/5.0
- **Median Rating**: 4.2/5.0
- **Rating Range**: 0.0 - 4.9 (scale out of 5)
- **Unrated Vendors**: 84 (4.2%)

### Customer Review Data
- **Vendors with Reviews**: 1,413 (74.6%)
- **Total Reviews Analyzed**: 1.3M+ individual review records
- **Avg Reviews per Vendor**: ~900 reviews
- **Avg Rating from Reviews**: 3.8/5.0
- **Positive Reviews Ratio**: ~64%

---

## 🍜 CUISINE PREFERENCES IN DHAKA

### Top 15 Cuisine Categories
| Ranking | Cuisine | Vendor Count |
|---------|---------|--------------|
| 1 | Asian | 692 |
| 2 | Snacks | 574 |
| 3 | Rice Dishes | 544 |
| 4 | Bangladeshi | 470 |
| 5 | Fast Food | 420 |
| 6 | Curry | 366 |
| 7 | Western | 354 |
| 8 | Beverage | 291 |
| 9 | Dessert | 288 |
| 10 | Burgers | 195 |
| 11 | Mediterranean | 181 |
| 12 | Italian | 181 |
| 13 | Pizza | 140 |
| 14 | Cakes | 138 |
| 15 | Chinese | 123 |

**Insights**: Traditional Bengali/Asian cuisines dominate (55%+ of market), Western cuisines strong in upmarket areas.

---

## 💰 PRICING & ORDER ECONOMICS

### Order Value Requirements
- **Avg Minimum Order**: 50 BDT (~$0.50 USD)
- **Avg Delivery Fee**: 0.25 BDT (~negligible)
- **Avg Delivery Time**: 20.2 minutes
- **Price Distribution**:
  - 94 vendors: 0-49 BDT minimum
  - 1,881 vendors: 50-99 BDT minimum
  - 2 vendors: 1,200+ BDT minimum

---

## 📱 VENDOR CONTACT & LOCATION DATA

### Data Density
- **Latitude/Longitude**: 100% coverage (1,978 vendors)
- **Phone Numbers**: Present in vendor_details/
- **URLs**: All vendors have Foodpanda profile links
- **Address Data**: 100% coverage (with varying quality)
- **Postal Codes**: Majority available

### Location Precision
- **Accuracy**: +/- 50-100 meters (GPS coordinates provided)
- **Area Classification**: 138 sub-areas within Dhaka
- **Distance from Reference Point**: Calculated (area_dist_km field)

---

## 📊 DATA STRUCTURE & FILES

### Primary Data Files
| File | Size | Records | Purpose |
|------|------|---------|---------|
| all_vendors.json | 9.1 MB | 1,978 | Complete vendor database with nested data |
| restaurants.csv | 499 KB | 1,978 | Flat structure with all core fields |
| vendor_reviews_summary.csv | 162 KB | 1,413 | Aggregated review metrics |
| vendor_reviews/ | 30 MB | 1,300K+ | Individual review data by vendor |

### Secondary Organization
- **by_area/**: 138 JSON files (vendors grouped by neighborhood)
- **by_chain/**: 236 JSON files (vendors grouped by chain affiliation)
- **raw_pages/**: 395 JSON files (original scrape page data)
- **vendor_details/**: Vendor contact & details

---

## 🔑 KEY INSIGHTS FOR ANALYSIS

### Market Concentration
- **Top 10 Chains**: ~200 locations (10.6% of market)
- **Top 100 Vendors**: Likely 40-50% of order volume
- **Fragmented Market**: 74.7% independent operators

### Geographic Hotspots
- **Premium Areas**: Gulshan, Banani, Dhanmondi (200+ vendors) = affluent customer base
- **Mass Market**: Uttara, Mirpur, Rampura (300+ vendors) = high density residential
- **Commercial**: Link Road, Farmgate, Kawran Bazar = business district

### Service Level
- **Minimum Order**: Uniformly 50 BDT (std minimum across app)
- **Delivery Fee**: Free/negligible (probably subsidized by app)
- **Delivery Speed**: 20 min avg = good infrastructure coverage

### Data Quality Issues
- Some vendors have junk data in "city" field (URLs, addresses)
- A small fraction of ratings appear corrupted/misformatted
- Postal code field contains non-postal codes in some cases

---

## 📈 EXTRACTION STATISTICS

**Total Data Points Extracted**: ~2.3 million individual records  
**Files Analyzed**: 2,669 JSON/CSV files  
**Coverage**: 100% of Foodpanda Dhaka catalog (as of scrape date: May 24-25, 2025)

---

## ⚠️ RESEARCH LIMITATIONS

- **Snapshot in Time**: Data from May 24-25, 2025 (not real-time)
- **Inactive Vendors**: Some entries may be inactive/closed
- **Review Sample Bias**: Review data samples, not complete history
- **Geographic Accuracy**: ±50-100m, some addresses incomplete
- **Rate Data**: May include outliers/corrupted entries

---

## 💡 USE CASES

1. **Market Analysis**: Understand Dhaka's food delivery market structure
2. **Competitive Intelligence**: Identify market gaps and opportunities
3. **Location-Based Services**: Map restaurant density and coverage
4. **Consumer Research**: Analyze cuisine preferences and ratings
5. **Business Analytics**: Order economics, delivery logistics simulation
6. **Quality Metrics**: Customer satisfaction by vendor/category
7. **Trend Analysis**: Which areas/cuisines are gaining traction

---

## 🔍 AVAILABLE DATA TABLES

### Vendor Records (restaurants.csv)
Columns: code, id, name, chain, city, area, area_dist_km, cuisines, rating, reviews, min_order, delivery_fee, delivery_min, lat, lng, address, post_code, url

**Example Record**:
```
oid3,76661,Dibbles,Dibbles Gulshan,Dhaka,Uttara Sector 6,0.62,"Chicken|Snacks|Meat|Burgers|Western|Fast Food",4.7,745,50.0,0.0,35.0,23.86918812,90.38888949,"SH Tower, 4th Floor, House: 35, Gawsul azom avenue, Sector: 14, Uttara, Dhaka 1230",1230,https://foodpanda.com.bd/restaurant/oid3/dibbles
```

### Review Summary Data (vendor_reviews_summary.csv)
Columns: vendor_code, review_count, avg_rating, positive_count, sample_review_text, sample_reviewer, sample_rating

### All Vendors JSON (all_vendors.json)
Complete nested JSON structure with all vendor metadata, ratings, reviews aggregates

---

## 🛠️ Data Access Methods

### Query by Area
```bash
cat data-dhaka/by_area/Gulshan_1.json
```

### Query by Chain
```bash
cat data-dhaka/by_chain/Mithai_-_Dhaka.json
```

### Query Individual Reviews
```bash
ls data-dhaka/vendor_reviews/ | head
```

### Analyze CSV Data
```bash
head -100 data-dhaka/restaurants.csv | cut -d',' -f3,9,10
```

---

Generated: 2025-05-25 01:30 UTC
