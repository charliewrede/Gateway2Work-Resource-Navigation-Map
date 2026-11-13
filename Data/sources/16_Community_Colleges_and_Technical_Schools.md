# Layer 16 — Community Colleges and Technical Schools

**Output:** `Data/Community_Colleges_and_Technical_Schools.geojson` (52 institutions) · **Build script:** `scripts/build_16_colleges.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
**Yes:** the U.S. Department of Education's **IPEDS** (Integrated Postsecondary Education Data System) institutional directory, which every Title IV institution must report. It was pulled for Colorado (FIPS 08), 2024 collection year, through the Urban Institute Education Data API (a free republication of NCES data):
`https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2024/?fips=8` → `Data/raw/ipeds_dir_CO_2024.json` (86 institutions).

Other sources checked: data.colorado.gov had nothing usable; the Colorado Community College System site (cccs.edu) returned 403.

## 2. Selection rules
| Included | How selected | Count |
|---|---|---|
| **Public community and technical colleges** | IPEDS sector 4 (public 2-yr) or 7 (public <2-yr), **plus** public "4-year" colleges whose `inst_system_name` = Colorado Community College System, plus Aims CC and Colorado Mountain College. Most Colorado community colleges now award a few bachelor's degrees, so IPEDS labels them 4-year. | 18 |
| Added by hand | **CMU Tech** (formerly Western Colorado Community College, renamed 2023-08-01; part of Colorado Mesa University in IPEDS), address from coloradomesa.edu contact page. **San Juan Basin Technical College** (Mancos), from the U.S. Dept. of Education DAPIP accreditation database via a SkillPlum listing. | 2 |
| Private career/technical schools | IPEDS sectors 5, 6, 8, 9 (2-year and less-than-2-year) | 18 |
| Cosmetology/beauty schools | sector 9 schools whose names show they're beauty or salon schools (tagged separately so they can be filtered) | 14 |

**Check:** the 13 CCCS colleges (Arapahoe, Colorado Northwestern, Aurora, Denver, Front Range, Lamar, Morgan, Northeastern JC, Otero, Pikes Peak State, Pueblo, Red Rocks, Trinidad State) are all present. That matches CCCS's published count of 13 colleges.

**Excluded:** public and private universities (they mostly award bachelor's and graduate degrees) and system offices.

## 3. Coordinates
50 from IPEDS's own latitude/longitude (NCES geocodes each institution's address); 2 additions by Census geocoder.

## 4. Caveats / follow-up
- **IPEDS lists main campuses only.** Branch campuses (Front Range CC's Longmont/Fort Collins/Brighton campuses, CMC's 11 campuses, Aims's Fort Lupton/Loveland/Windsor, Pueblo CC's Fremont and Southwest campuses, Trinidad State's Alamosa campus, CNCC Craig, ACC Castle Rock/Parker, Pikes Peak State's Rampart Range/Centennial campuses, etc.) **aren't mapped yet.** They should be added from each college's website.
- `school_type` lets the map show only public colleges if preferred.
