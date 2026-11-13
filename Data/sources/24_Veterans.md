# Layer 24 — Veterans Employment and Reentry Programs

**Output:** `Data/Veterans_Employment_and_Reentry.geojson` (36 sites) · **Build script:** `scripts/build_24_veterans.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| data.colorado.gov "veteran" | Only statistics (veteran counts, veteran-owned businesses). |
| VA.gov facility locator API | Needs a browser session token. Not used. |
| **HIFLD "Veterans Health Administration Medical Facilities"** (from VA's own **VAST** site database) | **Yes.** ArcGIS Online copy published by account `basemaps_IHS`, data last edited 2023-05-22. 37 Colorado sites. Raw: `Data/raw/hifld_vha_facilities_CO.json`. |
| Colorado Division of Veterans Affairs, County Veterans Service Offices directory (vets.colorado.gov) | The official list of 64 county offices, but blocked (403). |

## 2. Contents
- **35 VA health care sites** from VAST: 2 medical centers (Rocky Mountain Regional VAMC in Aurora, Grand Junction VAMC), community clinics, 5 **Vet Centers** (Boulder, Denver, Colorado Springs, Fort Collins, Grand Junction, Pueblo; these offer readjustment counseling and employment referrals), the **Valor Point Domiciliary** (residential rehab including homeless veterans), the York Street **Community Resource & Referral Center** (homeless veterans), and the Pueblo Community Living Center.
- **Removed:** 2 mobile Vet Centers (no fixed location).
- **Added:** Denver VA Regional Benefit Office, 155 Van Gordon St, Lakewood. This is where **Veteran Readiness & Employment (VR&E, Chapter 31)** is administered. Address from va.gov; phone from the Colorado Division of Veterans Affairs.
- The `homeless_point_of_contact` property (from VAST) names each site's homeless-program contact where one is listed.

## 3. Coordinates
VA's own VAST coordinates; the Regional Office was geocoded by Census.

## 4. Gaps / follow-up
- **County Veterans Service Officers (64)**: the state law (C.R.S. 28-5-801) requires every county to have one, and they're key referral points. The official directory couldn't be downloaded. Add them from vets.colorado.gov/services/county-veterans-service-offices.
- **Workforce center veteran representatives:** the 2022 American Job Center list marks which workforce centers have a Veterans Rep (see Layer 2).
- Veteran-focused nonprofits (e.g., reentry and employment programs for veterans) can be added as they're identified.
