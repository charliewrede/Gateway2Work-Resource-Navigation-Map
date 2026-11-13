# Layer 12 — Halfway Houses and Transitional Housing

**Output:** `Data/Halfway_Houses_and_Transitional_Housing.geojson` (3 sites) · **Build script:** `scripts/build_10_12_reentry_and_transitional_housing.py` · **Built:** 2026-11-13

## 1. How this layer relates to others
In Colorado, most "halfway houses" are **state community corrections** facilities. Those 28 facilities are in **Layer 5**. Recovery residences and sober living are **Layer 14**, and homeless shelters and supportive housing are **Layer 15**. This layer holds what's left:
1. **Federal halfway houses** (BOP Residential Reentry Centers).
2. **Reentry transitional housing programs** that aren't community corrections.

## 2. Sources
| Site | Source |
|---|---|
| Independence House (RRK Enterprise), 2765 S Federal Blvd, Denver: BOP RRC/home confinement, 25 beds (20 M / 5 F), contract 15BRRC20D00000120 expires 05-31-2030 | **BOP RRC public feed**, `https://www.bop.gov/PublicInfo/execute/rrc?todo=query&output=json` → `Data/raw/bop_rrc.json`. The feed has 154 RRCs nationally and **this is the only one in Colorado**. Pagination was checked: a single page holds the complete list. Coordinates come from BOP. |
| Bridge House **Ready to Work**, Boulder (4747 Table Mesa Dr) and Aurora (3176 S Peoria Ct): paid work plus transitional housing | WAGEES partner page `wageesco.org/community-partners/bridge-house-ready-to-work-boulder/` |

## 3. Searched but not added
- **HUD Housing Inventory Count:** has transitional housing bed counts by Continuum of Care, but no addresses.
- **Second Chance Center CREW transitional housing:** program site addresses aren't published (the HQ is in Layer 10).
- **Arapahoe County reentry housing community (Aurora, 60 residents):** reported by Denver7 as groundbreaking. Add when it opens.
- Directory sites (secondchanceguide.com, helpforfelons.org) were **not** used as sources because they're unverified aggregators.

## 4. Coordinates
BOP coordinates (1); Census (1); OpenStreetMap (1).
