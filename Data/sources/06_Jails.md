# Layer 6 — Jails

**Output:** `Data/Jails.geojson` (54 points, 50 counties + Aurora and Broomfield municipal facilities) · **Build script:** `scripts/build_06_jails.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| data.colorado.gov "jail" | No location dataset. |
| DCJ Office of Research & Statistics jail dashboard (HB19-1297) | Lists which counties report and which have **no jail**, but no addresses. The dcj.colorado.gov pages return HTTP 403 to automated requests, so the list was read from search-engine snippets plus the 2020 report PDF on the reachable cdpsdocs.state.co.us server. |
| HIFLD Prison Boundaries (TYPE = COUNTY / LOCAL) | **Yes**, 66 Colorado records with addresses, phones and footprints, but dated 2015–2018. |

**Decision:** HIFLD provides the records and coordinates. **Whether each county still operates a jail** was checked against DCJ's official county list and then updated for later changes.

## 2. Verification of which counties have a jail
1. **DCJ 2020 report** (`Data/raw/dcj_2020_HB19-1297_jail_data_report.pdf`, p. 6, footnote 3): *"There are 64 counties in Colorado. Of those, 53 operate a county jail. Counties not operating a jail: Archuleta, Cheyenne, Dolores, Hinsdale, Kiowa, Lake, Mineral, Ouray, Phillips, San Juan, Sedgwick."* Appendix C lists each reporting county's jail management system. It includes Bent, Custer, Jackson, Rio Blanco, Saguache and Yuma.
2. **DCJ's current jail-data page** (seen via search snippets) lists as non-operating: Cheyenne, Custer, Dolores, Hinsdale, Kiowa, Lake, Mineral, Ouray, Phillips, Rio Blanco, Saguache, San Juan, Sedgwick, Yuma. Compared with 2020, Archuleta has dropped off and Custer, Rio Blanco, Saguache and Yuma are new. Each change was confirmed separately:

| County | Change | Evidence |
|---|---|---|
| Archuleta | New 54-bed jail opened | Pagosa Springs SUN, "Archuleta County jail now operating", 2020-11-25; site at 125 Harman Park Dr (county resolution, Pagosa SUN) |
| Custer | Closed 2023-01-06; inmates go to Fremont County | KRDO 2023-01-06; KOAA |
| Rio Blanco | Closed 2021; inmates go to Moffat County | Herald Times ("Jail closure expected to save county $500K"); IGA renewed Sept 2025; April 2026 letter says reopening isn't cost-effective |
| Saguache | Closed; inmates go to Rio Grande County | Saguache County Sheriff page (updated 2024-07-25) |
| Yuma | Closed permanently (staffing); arrestees go to Logan County | Yuma Pioneer ("YC Sheriff can't find jailers, permanently closing jail"); 9News |

3. Result: 53 − 4 + 1 = **50 counties with jails**, which equals the number of counties in the output.

## 3. Changes to the HIFLD records
- **Removed** (no longer a jail or not a jail): Lake and Phillips (DCJ: no jail; HIFLD's points were sheriff's offices); Custer, Rio Blanco, Saguache, Yuma (closed); old Archuleta jail; Mesa Alternative Sentencing Unit (closed); Boulder County Juvenile Center (juvenile).
- **Moved to Layer 5 (Community Corrections):** Garfield County Community Corrections, Mesa County Community Corrections (Powell & Chipeta), Roberts Road and 3808 N Nevada residential facilities (Colorado Springs ComCor).
- **Renamed:** El Paso County "Metro Detention Facility" → **Metro Work Release Facility** (the Gazette reports work release moved into the former Metro jail; the EPSO Detention Bureau page lists the MWRF).
- **Address fixes:** Douglas County "4000 Justice Center" → 4000 Justice Way; Gilpin County Justice Center city → Black Hawk.
- **Added** (missing from HIFLD): Archuleta County Detention Center; Bent County Jail (bentsheriff.gov contact page: 11100 County Road GG.5, Las Animas; not to be confused with CoreCivic's Bent County Correctional Facility); Jackson County Jail (jacksoncounty.colorado.gov sheriff-jail page: 396 Lafever St, Walden).

## 4. Coordinates
- 51 HIFLD footprint centroids. Every one was compared with a Census geocode of its address, and **all were within 2 km**. The distance for each record is in its `verified` property.
- 3 additions were geocoded by the Census geocoder (exact address match).

## 5. Caveats
- HIFLD phone numbers and capacities date from 2015–2018 (the `hifld_source_date` property). Confirm before publishing.
- Several third-party "inmate lookup" sites give conflicting phone numbers and capacities. They were **not** used as sources.
- Counties without a jail send detainees to a neighboring county. That is noted here, not mapped.
