# Layer 2 — Workforce Centers (Colorado Workforce Centers / American Job Centers)

**Output:** `Data/Workforce_Centers.geojson` (54 centers) · **Build script:** `scripts/build_02_workforce_centers.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| data.colorado.gov "workforce" | No location dataset. (A "Workforce Centers" dataset in Socrata search turned out to be Chicago's.) |
| CDLE workforce center page, Workforce Colorado Rural Alliance (wcra.colorado.gov), CWDC | Authoritative, but **all colorado.gov pages return HTTP 403** to automated tools. Read only through search-engine snippets. |
| **U.S. DOL CareerOneStop "Comprehensive and Affiliate American Job Centers" download** (national, updated twice a year, with lat/long) | **The official statewide dataset**, but careeronestop.org also returns 403, and data.gov's catalog entry returned 404. |
| CareerOneStop AJC Finder export for Colorado, copy hosted by fairshake.net | **Downloaded** (`Data/raw/fairshake_ajc_CO.pdf`, created 2022-05-21): 52 centers with type (Comprehensive or Affiliate), address, phone, hours. |

**Decision:** Use the May 2022 federal AJC list as the **baseline roster** and update each center from the local workforce area's own website or a newer listing. Every feature has an `address_status` property:
- `current (verified 2026)`: address confirmed by the local area or WCRA page, or by two agreeing current sources.
- `from 2022 AJC list - not re-confirmed`: no newer source found. **Call before publishing.**

## 2. Colorado's 10 local workforce areas and their sources
| Local area | Centers | Source checked |
|---|---|---|
| Adams County | Westminster (11860 Pecos St) | adcogov.org Workforce & Business Center page. The 2022 Aurora (3155 N Chambers) site is gone: CBS reported the Chambers Rd human services center closing. |
| Arapahoe/Douglas | Centennial, Aurora (Altura Plaza), Castle Rock | adworks.org. Castle Rock moved in 2021 from 100 S Wilcox to the ACC Sturm Campus. |
| Boulder County | Boulder, Longmont | 2022 list; newer listing for Longmont (515 Coffman St) |
| Broomfield | 100 Spader Way | broomfield.org (2022 list had the old 120th Ave address) |
| Denver | Webb (201 W Colfax), Montbello, DIA, Westside | denvergov.org For Jobseekers page. The Speer Blvd center from the 2022 list is replaced by the Webb Building; Westside was under reconstruction until early 2026. |
| Tri-County (Jefferson, Gilpin, Clear Creek) | Golden, Black Hawk, Idaho Springs | jeffco.us directory |
| Larimer | Fort Collins | larimer.gov/ewd. Loveland no longer has daily staff (appointments at the library), so it isn't mapped. |
| Mesa | Grand Junction | mesacounty.us contact page |
| Pikes Peak (El Paso, Teller) | Colorado Springs, Fountain, Calhan, Cripple Creek | visitcos.com directory; 2022 list |
| Weld | Greeley, Fort Lupton | weld.gov Employment Services page |
| Rural Consortium (WCRA), ~30 centers | Pueblo through Steamboat | WCRA/CRWC contact page via search snippets; CDLE page; individual booking pages |

**Addresses changed since 2022** (newer source used): Pueblo (212 W 3rd → **1045 W 6th St**, per CRWC contact page and Pueblo County), Alamosa (→ 305 Murphy Dr Unit B), La Junta (→ 17 W 4th St), Cortez (→ 22 W North St), Glenwood Springs (→ 401 23rd St Ste 300), Salida (→ 7405 W Hwy 50 Ste 122), Leadville (→ 901 S Hwy 24, CMC New Discovery Building), Frisco (→ 360 Peak One Dr Ste 370), Broomfield (→ 100 Spader Way), Castle Rock (→ 4500 Limelight Ave).

## 3. Coordinates
48 by Census geocoder; 6 by OpenStreetMap. Five of those matched the exact building (ACC Sturm Campus; Broomfield HHS building; DIA 8500 Peña Blvd; 331 S Camino del Rio; 360 Peak One Dr). **San Luis** matched only the street (Vega St), so its position is approximate. Suite and unit numbers are removed before geocoding.

## 4. Open items (each in the feature's `status_note`)
Denver Westside (reopening?), Canon City (temporary closure reported), Edwards (temporarily closed per WCRA), Sterling (moved into the CSU Engagement Center; exact address unconfirmed), Limon (285 D Ave vs 333 M Ave), Durango (331 S Camino del Rio vs 160 Rock Point Dr). 17 centers are still at their 2022 address.

**Recommended follow-up:** download the current CareerOneStop AJC file in a browser (careeronestop.org → Developers → Data Downloads → *Comprehensive and Affiliate American Job Centers*, `XLS_AJC_Data_ACC.xlsx`), filter it to Colorado, and compare it with this layer.
