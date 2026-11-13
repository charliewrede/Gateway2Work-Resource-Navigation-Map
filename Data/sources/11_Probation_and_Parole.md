# Layer 11 — Probation and Parole Offices

**Output:** `Data/Probation_and_Parole_Offices.geojson` (70 offices: 52 probation + 18 parole) · **Build script:** `scripts/build_11_probation_parole.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
No GIS dataset. Two official rosters:
- **Probation** is run by the **Colorado Judicial Branch** (by judicial district). coloradojudicial.gov has a probation location page for each county, with structured address fields.
- **Parole** is run by the **CDOC Division of Adult Parole**. CDOC's "Parole Offices" page (19 offices, Dec 2025) blocks automated access (403).

## 2. Probation: method
1. For each of the 64 counties, the script tried the two URL patterns the Judicial site uses (`/location/<county>-probation`, `/courts/trial-courts/<county>-county/<county>-county-probation`). **All 64 pages were found** and saved to `Data/raw/judicial/` (URL list in `found.json`).
2. Addresses were read from the page's **structured address markup** (`address-line1`, `address-line2`, `locality`, `postal-code`), not from free text. A first attempt that matched free text picked up a building-closure banner instead of the address. That bad attempt was discarded and its cache entries purged.
3. Cleaning: when line 1 was a building name ("Bent County Courthouse", "Montrose County Courts Building", "Woodland Park Professional Building", "Gunnison County Courthouse"), the street in line 2 was used. PO Boxes were dropped for geocoding. The Judicial page's typo "Las Amimas" was corrected to Las Animas.
4. Counties that share an office (e.g., Adams and Broomfield share 12200 Pecos St, Westminster) were merged into one point, with all counties in `counties_served`.
5. **Denver:** the county page lists only phone numbers. The address comes from the Judicial Branch "Denver Adult Probation" listing: 303 W Colfax Ave, 5th Floor (confirmed by the Denver DA's contact page).
6. **11 counties have no probation office of their own.** Their pages list only the district's chief probation officer. Baca, Cheyenne and Kiowa are served from **Prowers** (15th JD), and Hinsdale and Ouray from the **7th JD** offices; those are added to the host office's `counties_served`. Jackson, Mineral, Saguache, San Juan and Sedgwick are served by neighboring offices in their districts. **Otero (16th JD, La Junta)** has no address on its page: the district's chief probation officer is at 719-384-5973. **Add the La Junta office once its address is confirmed.**
7. Note: partway through, coloradojudicial.gov began returning 403 to this session (rate limiting after about 130 page requests). No further requests were made.

## 3. Parole: method
- **Office cities and the counties each covers** come from the WAGEES "Adult Parole Locations" page (`wageesco.org/find-by-location`, © 2025 Latino Coalition for Community Leadership, CDOC's WAGEES intermediary), which lists **18 parole locations**. CDOC says 19, because Denver has both the headquarters and field supervision.
- **Street addresses** were found for only 4: Denver HQ (940 Broadway, the CDOC parole page as seen in search results), Colorado Springs (888 Garden of the Gods Rd, Waze/MapQuest), Fort Collins (3000 S College Ave, MapQuest), and Aurora (14100 E Exposition Ave, a third-party directory, possibly outdated).
- **The other 14 are placed at the city center** and labeled `geocode = "APPROXIMATE - city center (street address not available)"`, with a `status_note`. They show which communities have a parole office, not the building.

## 4. Coordinates
Probation: 51 Census + 0 OSM; Costilla (304 Main, San Luis) didn't geocode, so it's placed at the San Luis town center (`manual`, approximate). Parole: 4 by address, 14 approximate city centers.

## 5. Follow-up
- Get CDOC's parole office street addresses (CDOC parole page, or the parole line 1-800-426-9143) and replace the 14 approximate points.
- Add the 16th JD probation office in La Junta.
