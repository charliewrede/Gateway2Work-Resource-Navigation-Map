# Layer 4 — Substance Use Treatment and Mental Health Centers

**Output:** `Data/Substance_Use_and_Mental_Health_Treatment.geojson` (350 facilities) · **Build script:** `scripts/build_04_treatment.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| data.colorado.gov "behavioral health", "substance", "treatment" | Nothing for Colorado (results were other states). |
| Colorado Behavioral Health Administration (BHA): LADDERS licensing database, OwnPath directory | Official and complete for state-licensed providers, but **search-only, no download or export**. |
| **SAMHSA FindTreatment.gov** (federal) | **Yes.** An official export API, documented in SAMHSA's *FindTreatment Developer Guide* (`Data/raw/findtreatment_developer_guide.pdf`). |

**Decision:** Use SAMHSA FindTreatment.gov, the federal government's official locator, built from the annual National Substance Use and Mental Health Services Survey (N-SUMHSS).

## 2. How the data was pulled
```
https://findtreatment.gov/locator/exportsAsJson/v2?sAddr="39.7392,-104.9903"
    &limitType=0        (0 = state search, per Developer Guide Table 2)
    &limitValue=24      (Colorado's ID in Developer Guide Appendix B, State ID Table)
    &pageSize=2000&page=1&sort=0
```
- Raw responses: `Data/raw/findtreatment_CO_all.json` (512 rows), plus `_sa.json` (269 substance-use rows) and `_mh.json` (203 mental-health rows).
- **Completeness check:** a 1,000 km radius search around Denver returned the same 269 Colorado substance-use facilities, so the state query isn't truncated.

## 3. Processing
1. **Merged duplicates:** a facility appears once per type (substance use, mental health, opioid treatment program). Rows with the same name, street and city were combined into one point, and its `facility_types` property lists every type. 512 rows became 365 Colorado facilities.
2. **Removed** 1 out-of-state row (Solari Inc, Tempe AZ, a statewide crisis-line contractor).
3. **Missing coordinates:** SAMHSA withholds the street address for some providers, such as small private practices and confidential sites. 9 that had a street address were geocoded (8 Census, 1 OpenStreetMap). **15 were left out**: 14 with no published street address or only a PO box, and 1 rural address that wouldn't geocode (Healing Pines Recovery, 5550 County Rd 124, Elizabeth). The script prints the full list. Aurora Mental Health & Recovery and Centennial Mental Health Center are among them, and both appear in Layer 23 (Community Mental Health Centers).
4. Kept popup fields: types, service setting, type of care, payment accepted, special programs (which includes "Clients referred from the court/judicial system" where offered).

## 4. Coordinate verification
A random sample of 30 SAMHSA-supplied coordinates (seed 42) was re-geocoded with the U.S. Census geocoder. 28 had a Census match, and **all 28 were within 0.5 km** (median 0.05 km, max 0.48 km).

## 5. Caveats
- The SAMHSA locator only includes facilities that respond to the federal survey and are licensed, certified or approved by the state. Some BHA-licensed providers may be missing. BHA's LADDERS search can be used to spot-check particular providers.
- Data refreshes as SAMHSA updates facility records. Re-running the script pulls the current data.
