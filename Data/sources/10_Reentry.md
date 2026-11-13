# Layer 10 — Reentry and Transitional Services

**Output:** `Data/Reentry_and_Transitional_Services.geojson` (20 organizations) · **Build script:** `scripts/build_10_12_reentry_and_transitional_housing.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
There's no GIS dataset, but there is an **official statewide network roster**. **WAGEES** (Work and Gain Education & Employment Skills, created by HB14-1355) funds 20+ community reentry nonprofits. CDOC's grant intermediary, the **Latino Coalition for Community Leadership (LCCL)**, publishes the partner list at **wageesco.org/community-partners** (© 2025), with a page for each partner. This is the "Colorado WAGEES network" the TSRG PDF lists. Raw pages: `Data/raw/wagees_partners.html`, `Data/raw/wagees/*.html`.

## 2. How each record was sourced
| Organization | Address source |
|---|---|
| 16 WAGEES partners (Second Chance Center, The Reentry Initiative, The Empowerment Program, Life-Line Colorado, Servicios de La Raza, The Don't Look Back Center, Hazelbrook, Elk Meadow Enduring Connections, Homeward Alliance, The Rock Found, Loaves & Fishes, Manna, The Piñon Project, Valley-Wide, Freedom Institute ×2) | The partner's wageesco.org page, either the printed address or the address in the page's Google Maps link. Second Chance Center was also confirmed on its own site (scccolorado.org). |
| Cooperating Ministry of Logan County (WAGEES, Sterling) | The organization's site coopminlc.com; several directories agree. |
| Center for Employment Opportunities – Denver | Second Chance Business Coalition listing and SkillPlum (state Eligible Training Provider List) agree: 3532 N Franklin St Ste S. ceoworks.org returned 403. |
| Center for Employment Opportunities – Colorado Springs | Remerg, findhelp and Women's Directory agree: 888 Garden of the Gods Rd Ste 110 |
| CCJRC | Address in the ccjrc.org site footer |

**Correction:** Valley-Wide's WAGEES page prints ZIP "80150", which is a typo. It was corrected to La Junta's 81050, and the correction is noted in the feature's `verified` property.

## 3. Organizations named in the TSRG PDF
- **Colorado WAGEES network:** mapped (17 partners).
- **CDOC Reentry and Parole Services:** see Layer 11 (parole offices) and Layer 7 (prisons).
- **Center for Employment Opportunities:** mapped (Denver and Colorado Springs).
- **Second Chance Center:** mapped. Also operates Denver's MOORE Center (Layer 5).
- **The Reentry Initiative:** mapped (Longmont).
- **Colorado Recovery Friendly Workplace Initiative:** see Layer 1.
- **Colorado Criminal Justice Reform Coalition:** mapped (Denver).

## 4. Not mapped
- **My Father's House** (WAGEES, Aurora/Denver): publishes only a PO Box. The one directory "physical address" is an apartment unit, likely a private residence, so it was deliberately not mapped.
- **Community Anchor Academy** (WAGEES, Colorado Springs): no confirmed street address. KOAA says it's near S. Circle Drive; an NPI registry entry (121 E Bijou St) may be outdated. Add once confirmed.
- **Bridge House Ready to Work** is in Layer 12 (it's a residential program).

## 5. Coordinates
18 by Census geocoder, 2 by OpenStreetMap.
