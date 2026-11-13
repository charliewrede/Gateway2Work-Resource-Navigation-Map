# Layer 8 — IPS (Individual Placement and Support) Agencies

**Output:** `Data/IPS_Agencies.geojson` (10 agencies) · **Build script:** `scripts/build_08_ips.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
No. The IPS Employment Center (ipsworks.org) confirms Colorado joined the International IPS Learning Community in **2013**, but it doesn't publish program locations. Colorado's program roster is kept by the **Behavioral Health Administration (BHA)**, whose site blocks automated access.

## 2. Three rosters compared
| Roster | Date | Agencies |
|---|---|---|
| **A. BHA IPS page** (via search snippets) | current (~2026) | AllHealth Network (Arapahoe/Douglas); Axis Health System (Durango, Montrose, Gunnison, Crested Butte, Telluride, Pagosa Springs); Behavioral Health Group (Longmont); Diversus Health SUD (Colorado Springs) |
| **B. SOR "IPS Program Year 5 Evaluation Report"** prepared for BHA (`Data/raw/sor_ips_annual_report_22-23.pdf`, Exhibits 1–3) | 2022–23 | 4 SOR-funded sites: **SummitStone** (Fort Collins), **AllHealth Network** (Littleton), **BHG** (Longmont), **Crossroads Turning Points** (Pueblo). Notes that the Denver site stopped serving clients in Oct 2022. |
| **C. Older state IPS provider list** (colorado.gov/pacific/cdhs) | ~2020 | Colorado Coalition for the Homeless, Community Reach Center, Crossroads Turning Points, Diversus, Jefferson Center, North Range, SummitStone |

All 10 agencies on any list are mapped. Each feature's `listed_in` property says which list(s) it appears on. The four that appear **only** on the ~2020 list are flagged (`status_note`) to confirm they're still active.

## 3. Addresses (cross-referenced with other layers)
- AllHealth (5500 S Sycamore St, Littleton), BHG Longmont (850 23rd Ave), Crossroads (509 E 13th St, Pueblo): **SAMHSA FindTreatment records** (Layer 4) in the town the IPS roster names.
- Axis, Diversus, SummitStone, Community Reach, Jefferson Center, North Range: **main office** (Layer 23, from each provider's site).
- Colorado Coalition for the Homeless: GuideStar profile (2111 Champa St, 80205).
- Coordinates: Census geocoder (10/10).

## 4. Note
IPS employment specialists work out of treatment sites. The points show the agency or site, and services may be offered at several of an agency's clinics.
