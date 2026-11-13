# Layer 5 — Community Corrections

**Output:** `Data/Community_Corrections.geojson` (28 residential facilities) · **Build script:** `scripts/build_05_community_corrections.py` · **Built:** 2026-11-13

In Colorado, "community corrections" means the residential programs ("halfway houses") regulated by the Division of Criminal Justice (DCJ), Office of Community Corrections (OCC). Placements are approved by each judicial district's Community Corrections Board.

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| data.colorado.gov | No location dataset (only client counts and fees). |
| DCJ OCC "Community Corrections Boards, Programs & Specialized Programs" page | The current official list, but dcj.colorado.gov returns HTTP 403 to automated requests. It was seen only through search-engine snippets. |
| DCJ OCC FY24 Annual Report (Colorado State Publications Library) | spl.cde.state.co.us refused connections from both tools, so it couldn't be read. |
| DCJ OCC "Colorado Community Corrections Programs 02-13-2017" (cdpsdocs.state.co.us) | **Downloaded** (`Data/raw/dcj_occ_residential_program_list_2017-02-13.pdf`): 33 programs with director, address and phone. **Nine years old**, so used only as a baseline. |
| HIFLD Prison Boundaries | Has 6 community corrections buildings (Mesa, Garfield, Colorado Springs). Incomplete. |

**Decision:** Start from the 2017 DCJ list and **re-verify every program** against the operator's own website or the county Community Corrections Board page. Programs that couldn't be confirmed were dropped, and replacements were added.

## 2. What changed since 2017 (verified)
| 2017 entry | Status in 2026 | Evidence |
|---|---|---|
| CoreCivic Columbine, Dahlia, Ulster (Denver) | Closed; Denver ended private contracts in 2019–20 | CCJRC 2021 report; Gazette; Denver facilities page |
| CoreCivic Fox, 570 W 44th Ave | Now the city's **MOORE Center** (with Second Chance Center) | denvergov.org Community Corrections Facilities page |
| CEC/GEO Tooley Hall, 4280 Kearney | Bought by Denver in 2019, now **Project: Elevate** (with The Empowerment Program), for women | denvergov.org; NextCity |
| CEC/GEO Williams Street Center | Closed (2020) | Gazette 2020 |
| Peer I, The Haven, Independence House Fillmore | Not on Denver's current list; Independence House consolidated at Pecos | denvergov.org |
| (new) IMPACT Center, 10500 Smith Rd | Added | denvergov.org |
| Com Cor Inc. (Colorado Springs) | Rebranded **Embrave**: Roberts Rd (225 beds) + 3950 N Nevada (135 beds) | embrave.org/facilities; El Paso County Justice Services page; Gazette |
| Gateway: Through the Rockies (El Paso) | Not on El Paso County's current list (only Embrave and CAE) | justiceservices.elpasoco.com |
| CoreCivic Boulder Community Treatment Center | Now **ICCS-Boulder** | bouldercounty.gov Halfway Houses page |
| Time to Change – Adams / Commerce City | Now listed by CoreCivic as **Adams Transitional Center** and **Commerce Transitional Center** | corecivic.com; Adams County page (102 and 136 beds) |
| Time to Change – Henderson | Now **ICCS Adams County Opportunity Center** (184 beds) | Adams County page; int-cjs.org/locations |
| San Luis Valley Community Corrections, 2255 Lava Lane | Now Advantage Treatment Centers, 2017 Lava Lane | atreatmentcenters.com/alamosa-co; Alamosa News ("New corrections owner") |
| (new) Advantage Treatment Centers – Lamar | Added: Advantage's site lists community corrections in Montrose, Lamar, Alamosa, Sterling | atreatmentcenters.com |

## 3. Sources for each facility (in each feature's `source` / `source_url` properties)
- **Operator sites:** int-cjs.org/locations (ICCS: Kendall, West, Weld, Pueblo, Adams); corecivic.com facility pages (Adams TC, Commerce TC, Arapahoe CTC, Centennial CTC, Longmont CTC; CoreCivic's Colorado list was checked to confirm these are its only community corrections sites); embrave.org/facilities; atreatmentcenters.com location pages (Montrose, Alamosa, Sterling, Lamar).
- **County/city board pages:** denvergov.org (4 facilities); bouldercounty.gov; adamscountyco.gov; justiceservices.elpasoco.com; weld.gov; larimer.gov (2025 annual report); garfieldcountyco.gov (2026 handbooks, 2025–26 PREA report); mesacounty.us.

## 4. Coordinates
- 25 by Census geocoder (exact match).
- 2 by OpenStreetMap Nominatim (Census found no match). Both matched the exact house number: "1050 Avenida del Sol, Durango" and "4101 North Pecos Street, Denver".
- 1 (Garfield County, rural road address) from its HIFLD facility footprint.

## 5. Open items (flagged with `status_note`)
- **CAPS, Craig (14th JD):** the only recent evidence is a third-party directory updated July 2025. Confirm with the 14th JD board.
- **Arapahoe County Residential Center:** the operator is listed as GEO by GEO-affiliated listings and as CoreCivic by one directory, and it isn't on CoreCivic's own list. Confirm with the 18th JD board.
- **Pueblo (10th JD):** Pueblo County says it contracts with **two** private programs. Only ICCS-Pueblo could be confirmed. "Minnequa Community Corrections" appears in directories with no address, so it's not mapped.
- DCJ's FAQ says there are **33 residential programs**. Several sites run more than one program (e.g., separate men's and women's programs at Larimer), so 28 facilities is consistent with that.
- Federal BOP Residential Reentry Centers (halfway houses under federal contract) are in Layer 12, not here.
