# Layer 15 — Homelessness and Housing Service Providers

**Output:** `Data/Homelessness_and_Housing_Services.geojson` (8 providers) · **Build script:** `scripts/build_01_13_15.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| data.colorado.gov "homeless", "shelter" | Nothing for Colorado. |
| HUD Housing Inventory Count (HIC) | Bed counts per Continuum of Care, **no addresses**. |
| **2-1-1 Colorado** shared statewide shelter list (search.211colorado.org/shared/resource-lists/pkdgR43n) | The best statewide source, but it only loads in a browser (built with JavaScript), so it couldn't be downloaded by a script. |
| shelterlist.com, homelessshelters.net, Housing Colorado PDF | Third-party aggregators of mixed age. Used only to find names, not as address sources (one exception, flagged). |

**Decision:** map **regional anchor providers**, with each address confirmed on the provider's own website.

## 2. Mapped
| Provider | Address source |
|---|---|
| Denver Rescue Mission (HQ, 6100 Smith Rd) | own site |
| Colorado Coalition for the Homeless (2111 Champa St) | own site; GuideStar |
| Catholic Charities of Denver (6240 Smith Rd; runs Samaritan House and other shelters) | own site |
| Springs Rescue Mission (5 W Las Vegas St) | own site |
| Boulder Shelter for the Homeless (4869 Broadway) | own site |
| Fort Collins Rescue Mission (316 Jefferson St) | Denver Rescue Mission site |
| Homeward Alliance / Murphy Center (242 Conifer St, Fort Collins) | WAGEES partner page |
| Pueblo Rescue Mission (728 W 4th St) | **third-party directory only**, flagged to confirm |

Coordinates: Census geocoder (8/8).

## 3. Gaps and recommended follow-up
- **Open the 2-1-1 Colorado shelter list in a browser**, export or copy it, and add those shelters. That would make this layer statewide.
- Missing regions: Grand Junction (Grand Valley Catholic Outreach; its site returned 403), Greeley, Durango, Alamosa, the mountain communities.
- Supportive housing operators (e.g., Second Chance Center's Providence at the Heights) and domestic violence shelters (addresses are confidential, **do not map**) were deliberately not included.
