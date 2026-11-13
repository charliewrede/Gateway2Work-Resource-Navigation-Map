# Gateway2Work Colorado GIS Layers: Sources and Methods

Statewide GeoJSON layers for the 25 categories in TSRG's *Colorado Workforce Development Ecosystem: Proposed statewide GIS categories* (Gateway2Work). Built 2026-11-13.

**Totals:** 23 layers built, **1,089 mapped locations**. 2 layers are documented but not yet built (L19, L21).

> **The framework's own caveat applies:** *"This is a proposed classification framework, not a verified statewide inventory. Organization participation, service areas, and current program status should be confirmed before GIS publication."* Every record carries its source so it can be checked.

## How to answer "where did this point come from?"
1. **Click the point on the map.** Every feature has `source`, `source_url`, `retrieved` (date collected), and `geocode` (how its location was found). Many also have `verified` (the cross-check performed) and `status_note` (anything still to confirm).
2. **Open that layer's write-up** in `Data/sources/` (table below). It covers which statewide datasets were searched, what was used and why, every correction made, and the open questions.
3. **Re-run the build:** `python3 scripts/run_all.py` rebuilds every layer from its sources. Original downloads are kept in `Data/raw/`, and every geocoder answer is cached in `scripts/cache/geocode_cache.json`, so results are reproducible.

## Layers
| # | Category | File (`Data/…`) | Points | Statewide dataset? | Primary source | Write-up |
|---|---|---|---|---|---|---|
| 1 | Recovery-Friendly Employers | Recovery_Friendly_Employers.geojson | 147 | **Yes** | CO Recovery Friendly Workplace Initiative participant list (published sheet) | [01](sources/01_Recovery_Friendly_Employers.md) |
| 2 | Workforce Centers | Workforce_Centers.geojson | 54 | Yes, but blocked | US DOL American Job Center list (2022) + each local workforce area's site | [02](sources/02_Workforce_Centers.md) |
| 3 | Workforce Development Providers | Workforce_Development_Training_Providers.geojson | 96 | **Yes** | US DOL TrainingProviderResults.gov, Colorado WIOA ETPL (2024) | [03](sources/03_Workforce_Development_Providers.md) |
| 4 | Substance Use Treatment & Mental Health | Substance_Use_and_Mental_Health_Treatment.geojson | 350 | **Yes** | SAMHSA FindTreatment.gov export API | [04](sources/04_Treatment_and_Mental_Health.md) |
| 5 | Community Corrections | Community_Corrections.geojson | 28 | Partial | DCJ 2017 program list, re-verified program by program (operators and county boards) | [05](sources/05_Community_Corrections.md) |
| 6 | Jails | Jails.geojson | 54 | **Yes** (dated) | HIFLD Prison Boundaries + DCJ HB19-1297 county jail list + closure news | [06](sources/06_Jails.md) |
| 7 | Prisons | Prisons.geojson | 26 | **Yes** (dated) | CDOC facility list (Mar 2025), CoreCivic, BOP feed; HIFLD footprints | [07](sources/07_Prisons.md) |
| 8 | IPS Agencies | IPS_Agencies.geojson | 10 | No | BHA IPS page, SOR IPS evaluation report (2022–23), older state list | [08](sources/08_IPS.md) |
| 9 | DVR Offices | DVR_Offices.geojson | 14 | No (blocked) | Colorado DVR office list | [09](sources/09_DVR.md) |
| 10 | Reentry & Transitional Services | Reentry_and_Transitional_Services.geojson | 20 | Roster | WAGEES Community Partners (LCCL, CDOC intermediary) + CEO, CCJRC | [10](sources/10_Reentry.md) |
| 11 | Probation & Parole Offices | Probation_and_Parole_Offices.geojson | 70 | Roster | Colorado Judicial Branch (64 county pages); WAGEES parole locations | [11](sources/11_Probation_and_Parole.md) |
| 12 | Halfway Houses & Transitional Housing | Halfway_Houses_and_Transitional_Housing.geojson | 3 | **Yes** (federal) | BOP RRC feed; Bridge House Ready to Work. State halfway houses are in L5 | [12](sources/12_Halfway_Houses.md) |
| 13 | Recovery Community Organizations | Recovery_Community_Organizations.geojson | 4 | No | Organization sites; CAPRSS; ARCO | [13](sources/13_Recovery_Community_Organizations.md) |
| 14 | Recovery Residences | Recovery_Residences_by_City.geojson | 22 cities (80 houses) | Blocked | Oxford House directory, **aggregated to city for privacy** | [14](sources/14_Recovery_Residences.md) |
| 15 | Homelessness & Housing Services | Homelessness_and_Housing_Services.geojson | 8 | No (211 needs a browser) | Provider websites | [15](sources/15_Homelessness.md) |
| 16 | Community Colleges & Technical Schools | Community_Colleges_and_Technical_Schools.geojson | 52 | **Yes** | NCES IPEDS 2024 directory | [16](sources/16_Community_Colleges_and_Technical_Schools.md) |
| 17 | Apprenticeship Programs | Apprenticeship_Programs.geojson | 9 | Partial | ETPL apprenticeship programs (WIOA-eligible subset) | [17](sources/17_Apprenticeship.md) |
| 18 | Adult Education & GED | Adult_Education_and_GED_Programs.geojson | 36 | **Yes** | CDE Adult Education Initiatives "Find a Program" map | [18](sources/18_Adult_Education.md) |
| 19 | Human Services Departments | *not built* | — | Blocked | CDHS county directory, manual step needed | [19/21](sources/19_and_21_NOT_YET_BUILT.md) |
| 20 | Community & Faith-Based Orgs | Community_and_Faith_Based_Organizations.geojson | 13 | No | Role-based selection from verified L10/L15 records | [20](sources/20_Community_and_Faith_Based.md) |
| 21 | Staffing & Second-Chance Employers | *not built* | — | No | See L1 and L25; plan in write-up | [19/21](sources/19_and_21_NOT_YET_BUILT.md) |
| 22 | Legal Aid & Record Sealing | Legal_Aid_and_Record_Sealing.geojson | 12 | No | Colorado Legal Services office list | [22](sources/22_Legal_Aid.md) |
| 23 | Community Mental Health & Disability Employment | Community_Mental_Health_Providers.geojson | 17 | Roster | CBHC provider-by-county list + provider sites | [23](sources/23_Community_Mental_Health.md) |
| 24 | Veterans Employment & Reentry | Veterans_Employment_and_Reentry.geojson | 36 | **Yes** | VA VAST database (via HIFLD) + VA Regional Office | [24](sources/24_Veterans.md) |
| 25 | Social Enterprises & Transitional Employment | Social_Enterprises_and_Transitional_Employment.geojson | 8 | No | AG Reentry Report, RCF handout; organization sites | [25](sources/25_Social_Enterprises.md) |

## How locations were found (`geocode` property)
| Method | Count | Meaning |
|---|---|---|
| Source coordinates | 504 | Supplied by the dataset itself (SAMHSA, IPEDS, VA, BOP) or HIFLD facility-footprint centroids (prisons and jails, each checked against a Census geocode) |
| `census-rooftop` | 508 | U.S. Census Bureau geocoder, exact address match |
| `census-nonexact` | 1 | Census geocoder, best of several candidates |
| `osm-nominatim` | 27 | OpenStreetMap, matched the house number (used only when Census failed) |
| approximate | 47 | `osm-street-approx` (on the right street, no house number), `approx-city-center` / `APPROXIMATE - city center` (parole offices without a published street address; recovery residences aggregated by city for privacy) |
| `manual` | 2 | Hand-set and explained in the write-up |

**Quality rules for OpenStreetMap results** (added after a spot-check found errors): city lookups must return a town, not the county of the same name; a match whose ZIP *and* city both disagree with the source is rejected; matches without a house number are labeled approximate.

## Corrections made to source data (all documented in the write-ups)
- CBHC lists **Diversus and Solvista with swapped service areas**, so the providers' own clinic lists were used (L23).
- The RFW participant sheet's **County column is wrong** in places and wasn't used. One row had the unit number in the City column, and another listed Denver for a Golden ZIP (L1).
- CDE's adult education map has **two street typos** ("Caminio", "Illif") (L18).
- The Judicial Branch has a "Las Amimas" typo (L11). The WAGEES page has a "80150" ZIP typo for La Junta (L10).
- The ETPL file marks **out-of-state providers as Colorado**; they were excluded (L3).
- HIFLD's jail/prison records date from 2015–2018: 4 county jails have since closed, 1 opened, and 2 counties never operated jails (L6/L7).
- The 2017 community corrections list had **12+ changed or closed programs** (L5).

## Sources that couldn't be read automatically
Many colorado.gov sites (CDOC, DCJ, BHA, CDHS, CDLE, DVR, CWDC) and careeronestop.org return HTTP 403 to scripts. They were **not** circumvented: no browser impersonation, no staging copies, no API keys taken from web pages. Where a blocked page was the authoritative source, its content was read from search-engine copies and cited as such, or the gap is documented with a manual step to fill it. See [FOLLOW_UP.md](sources/FOLLOW_UP.md).

## Privacy choices
- **Recovery residences** are mapped only as counts per city, and no house addresses or resident contacts were stored.
- **Domestic violence shelters** were deliberately not mapped.
- A reentry program whose only public street address was an apartment unit (My Father's House) was not mapped.
