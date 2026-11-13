# Layer 9 — DVR Offices and Authorized Service Providers

**Output:** `Data/DVR_Offices.geojson` (14 offices) · **Build script:** `scripts/build_09_dvr.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
No downloadable dataset. The authoritative list is the Colorado **Division of Vocational Rehabilitation (DVR, part of CDLE)** "DVR Phone Numbers" page and "Contact Us" page on dvr.colorado.gov. **Both return HTTP 403 to automated tools**, so the office list was read from search-engine copies of those pages.

## 2. Offices and sources
| Office | Source |
|---|---|
| Administrative office (707 17th St Ste 2700, Denver); Englewood (750 W Hampden Ave Ste 225) | DVR "Contact Us" page |
| Alamosa, Colorado Springs, Delta, Durango, Fort Morgan, Golden, Grand Junction, Limon, Northglenn, Trinidad | DVR "Phone Numbers" page |
| Aurora (12510 E Iliff Ave Ste 303) | Network of Care (DRCOG) directory, **confirm** |
| Montrose (1551 Ogden Rd) | AskJAN listing, older, **confirm** |

Several DVR offices share an address with a workforce center (Alamosa, Delta, Fort Morgan, Trinidad, Golden). That's consistent with Layer 2 and adds confidence in both.

## 3. Known gaps and conflicts
- **Longmont:** the DVR page gives "Suite 101" with no street address, so it isn't mapped.
- **Salida:** "US Hwy 50, Suites 214 and 216" has no house number, so it isn't mapped.
- **Steamboat Springs, Craig, Boulder:** found only in old listings, so not mapped.
- **Golden:** the suite conflicts (400 vs 1400). The building is the same, so the point is unaffected.
- **Authorized service providers (DVR vendors)** aren't published as a public list, so they aren't mapped. Many workforce, IPS (Layer 8) and community mental health (Layer 23) organizations are DVR vendors.

## 4. Coordinates
14 Census geocoder (exact match).
