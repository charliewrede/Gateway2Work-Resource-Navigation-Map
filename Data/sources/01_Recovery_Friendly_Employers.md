# Layer 1 — Recovery-Friendly Employers (RFE)

**Output:** `Data/Recovery_Friendly_Employers.geojson` (151 employers) · **Build script:** `scripts/build_01_13_15.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
**Yes, an official one.** The **Colorado Recovery Friendly Workplace Initiative®** (RFWI) was created by state law (SB24-048, 2024) and is administered by the Centers for Health, Work & Environment at the Colorado School of Public Health (CU Anschutz). Its "Participating Companies" page (https://corecoveryfriendlyworkplace.org/participating-colorado-companies/) loads its list from a **published Google Sheet**:
`https://docs.google.com/spreadsheets/d/e/2PACX-1vSlU67lHAkf7HUxQsAq3IS-Ev5GfEaiDM5MXbE3eqR4VpaprF0nYHukGGy6PjusUIzuJeXsgIYzWioD/pub?output=csv`
→ `Data/raw/rfwi_participating_companies.csv` (153 rows: name, street, city, ZIP, county, website).

How the source was found: the page's HTML showed the list is filled in by a script, and the script's data URL is that published sheet. The program's pledge says signers agree to have their organization's name published.

## 2. Processing
- **"✪ CERTIFIED"** in a business name means the employer completed RFW certification. This is recorded in `rfw_status` ("Certified Recovery Friendly Workplace" or "Participating (pledged)") and removed from the display name.
- **Data-quality problems in the sheet (found and handled):**
  - The **County column is unreliable** (e.g., "7670 Grill, Hot Sulphur Springs" is labeled Alamosa County), so it was **not used**. Location comes from the street address.
  - One row has "Unit D" in the City column with ZIP 80701, so the city was set to Fort Morgan and the unit moved back into the address.
  - One row (Morris and Mae Food Hall, 18475 W Colfax Ave) says Denver, but ZIP 80401 is **Golden**, so the city was corrected.
- **Manual decisions by project staff (2026-11-17)** for the 6 roster rows that couldn't be geocoded. They're coded in `OVERRIDES` in the build script, so they still apply after a re-pull, and each mapped one carries a `location_note`:
  - **Absolute Caulking and Waterproofing** (certified): address verified as 11919 W Interstate 70 Frontage Rd N, Wheat Ridge 80033 (roster: "11919 I-70 Frontage Rd. N. #112"). Geocoded as "W I-70 Frontage Rd N", an exact house-number match in OpenStreetMap.
  - **Recovery Friendly Leader** (certified): **PO Box only** (PO Box 18770, Denver 80218), with no physical location. Point placed at the center of ZIP 80218. Flagged `po_box_only = Yes`.
  - **Summit County Chamber of Commerce**: no physical location (PO Box 461). Point at Frisco town center.
  - **Hargrove and Kidd Construction Co**: no physical location (roster listed 14 Thomas Ct). Point at Crested Butte town center.
  - **Not mapped:** Growing Our Mindset, LLC dba Arntt Synergy Consulting (couldn't be found or confirmed online) and South Pole Bar (not confirmed; no street address on the roster).

## 3. Coordinates
135 Census exact, 1 Census non-exact, OpenStreetMap for the rest. 3 points are deliberately approximate (ZIP or town center) for organizations with no physical location. OSM results **without a house number** are labeled `osm-street-approx` (e.g., 18475 W Colfax in Golden is placed somewhere along W Colfax in Golden).

## 4. Caveats
- Participation is self-reported through a pledge. Certification is the stronger signal.
- Some small consultancies list what may be a home-office address. They're published by the initiative and kept as-is. Consider hiding the non-certified layer if that's a concern.
- The list changes as employers join, and re-running the script pulls the current sheet.
