# Layer 7 — Prisons

**Output:** `Data/Prisons.geojson` (26 points) · **Build script:** `scripts/build_07_prisons.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| Colorado Information Marketplace (data.colorado.gov), "prison", "corrections" | No facility-location dataset. Only population/admission tables. |
| HIFLD Open "Prison Boundaries" (national, DHS) | **Yes, but dated.** 117 Colorado records, mostly from 2015–2018. HIFLD Open was taken offline on 2025-08-26. The copy used here is the public ArcGIS mirror `services.arcgis.com/XG15cJAlne2vxtgt/.../Prison_Points` (polygon centroids of the HIFLD footprints). Archived official copy: DataLumos DOI 10.3886/E240534V1. |
| CDOC website (cdoc.colorado.gov/facilities) | Authoritative, but the site returns HTTP 403 to automated requests, so it could not be downloaded. |

**Decision:** HIFLD is too old to be the facility *list*. For example, it still lists Cheyenne Mountain Re-entry Center and Colorado Correctional Center as open, but neither is on CDOC's 2025 list. So the list comes from current agency sources, and HIFLD is used only for **coordinates** (building-footprint centroids), which are more accurate than geocoding highway addresses like "57500 E Hwy 50".

## 2. Sources used
| Part | Source | Date | Raw copy |
|---|---|---|---|
| 18 CDOC state-operated facilities | *Colorado Department of Corrections Facility Address List*, CDOC document attached to a March 2025 procurement, hosted at https://seams.org/wp-content/uploads/2025/03/Attachment-A-Facilty-Address-List.pdf | Mar 2025 | `Data/raw/cdoc_facility_address_list_2025-03.pdf` |
| 2 private (CoreCivic) prisons holding CDOC inmates | CoreCivic facility pages (Bent County, Crowley County); both name the Colorado DOC as government partner. CDOC also has a "private prisons" page for Bent County. | checked 2026-11-13 | — |
| 4 federal BOP institutions | Federal Bureau of Prisons public locations feed, https://www.bop.gov/PublicInfo/execute/locations?todo=query&output=json | 2026-11-13 | `Data/raw/bop_locations.json` |
| FPC Florence camp, The Beacon at Skyline | HIFLD footprints; Wikipedia "Skyline Correctional Center"; Denver7 (2025) | — | `Data/raw/hifld_prison_points_CO.geojson` |

**About the CDOC PDF's source:** the file is hosted on a third-party site (SEAMS), so it was double-checked. Its 18 facility names match the current CDOC facility roster as described in search results and Wikipedia's CDOC article, and its street addresses geocode to within 2.1 km of the matching HIFLD facility footprints (table below).

## 3. Coordinates and verification
- State and private facilities use **HIFLD footprint centroids**. Each centroid was compared with a Census Bureau geocode of the CDOC street address:

| Facility | HIFLD vs Census distance |
|---|---|
| Colorado State Penitentiary, DRDC | 0.2 km |
| La Vista, Youthful Offender System | 0.3 km |
| Limon, Sterling | 0.4 km |
| Centennial, CTCF | 0.5 km |
| Arkansas Valley, Arrowhead, DWCF, San Carlos | 0.6 km |
| Buena Vista, Four Mile | 1.4 km |
| Fremont | 2.1 km (inside the ~2 km-wide Cañon City East complex) |
| Delta, Rifle, Trinidad, Skyline | address not matchable by Census (rural/highway), HIFLD only |

- Federal: FCI Englewood uses BOP's own coordinates. The BOP feed gives all Florence units **one shared point**, so FCI Florence, USP Florence High, ADX Florence and the FPC camp each use their own HIFLD footprint so they don't stack on top of each other.

## 4. Included and excluded
- **Excluded:** Division of Youth Services centers (juvenile, not prisons); the Aurora ICE Processing Center (immigration detention, not a reentry source); FCC Florence (an administrative record, not a separate facility) and BOP MSTC Aurora (staff training center); facilities HIFLD marks closed (Fort Lyon, High Plains, Huerfano, CWCF); Cheyenne Mountain Re-entry Center and Colorado Correctional Center (absent from CDOC 2025 list).
- County jails are a separate layer (Layer 6).

## 5. Open questions to confirm before publication
- **Rifle Correctional Center**: proposed for closure in budget talks; still operating in late 2025 (evacuated for a wildfire in Aug 2025).
- **Delta Correctional Center**: closure discussed in 2025 (KVNF, 2025-03-06).
- **The Beacon at Skyline**: reported proposed for closure in 2025 and not on the March 2025 address list.
- Each of these has a `status_note` property in the GeoJSON, so the note shows in the map popup.
