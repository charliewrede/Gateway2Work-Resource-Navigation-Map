# Layer 14 — Recovery Residences / Sober Living

**Output:** `Data/Recovery_Residences_by_City.geojson` (22 city points: 80 Oxford Houses, 655 beds) · **Build script:** `scripts/build_14_recovery_residences.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| **BHA "Certified Recovery Residences"** (bha.colorado.gov) | The official list of state-certified residences (certification administered under BHA contract by **Ohio Recovery Housing**, per BHA's page updated 2025-11-04; earlier the **Colorado Association of Recovery Residences, CARR**, was the certifying body). **Blocked (403).** |
| CARR (carrcolorado.org) | Blocked (403). CARR reported **283 certified homes / 3,027 beds** in July 2023 (legislative interim committee report). |
| **Oxford House vacancy directory** (oxfordvacancies.com) | **Reachable.** Public, current listing of Oxford Houses (peer-run recovery homes). Lists 82 Colorado houses. |

## 2. Privacy decision (important)
Recovery residences are **people's homes**, and Oxford's listings include residents' first names and phone numbers. Putting individual homes on a public map could expose residents' recovery status. So:
- **Individual houses are not mapped.** Only **counts per city** (number of houses, beds, and house types: men, women, with children) were stored, at the city's center point.
- **No names, addresses or contacts were saved.** The raw file `Data/raw/oxford_house_CO_by_city.json` contains only the aggregates.
- Each feature links to the Oxford vacancy site, where applicants can find a house.

## 3. Method
The statewide page shows only 60 houses at a time, so the directory was queried **once per county** (15 counties in the site's county filter) and de-duplicated: 79 houses. The Douglas County query returned no rows, but the statewide page showed one Castle Rock house (9 beds), which was added. **Total: 80 of the 82 listed houses**, in 22 cities.

## 4. Gaps
- **This is Oxford House only.** Most of Colorado's ~283 certified recovery residences are run by other operators, and the state-certified list couldn't be obtained. **Recommended:** request the certified list from BHA or Ohio Recovery Housing and add it **aggregated to city or county**, following the same privacy rule.
