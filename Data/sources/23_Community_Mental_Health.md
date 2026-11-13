# Layer 23 — Community Mental Health and Disability Employment Providers

**Output:** `Data/Community_Mental_Health_Providers.geojson` (17 providers, main offices) · **Build script:** `scripts/build_23_community_mental_health.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
No GIS dataset. The authoritative roster is the **Colorado Behavioral Healthcare Council (CBHC)**, the association of Colorado's community mental health centers and safety-net behavioral health providers. Its "Behavioral Health Providers" page lists the member provider(s) for **every county** (https://www.cbhc.org/find-services/behavioral-health-providers/ → `Data/raw/cbhc_providers.html`). BHA's safety-net provider list is on blocked colorado.gov pages.

## 2. Method
1. Provider roster and county coverage from CBHC (15 member organizations).
2. **Main-office address from each provider's own website.** The script downloaded each site's home and locations pages and extracted Colorado addresses. Where a site listed many clinics, the administrative or main office was used.
3. Counties CBHC leaves blank (Archuleta, Delta, Dolores, Douglas, Gunnison, Hinsdale, La Plata, Montezuma, Montrose, Ouray, San Juan, San Miguel) are served by **non-member** safety-net providers. Two were added: **AllHealth Network** (Douglas/Arapahoe; site address) and **Axis Health System** (southwest). Axis's address conflicts across listings (1125 Three Springs Blvd, 185 Suttle St, 281 Sawyer Dr), so the NPI-registry practice address was used and **flagged to confirm**. The Delta/Gunnison/Montrose/Ouray/San Miguel safety-net provider still needs to be identified.

## 3. Source problem found and corrected
CBHC's page assigns **Solvista Health** to El Paso, Park and Teller and **Diversus Health** to Chaffee, Custer, Fremont and Lake. **The two are swapped.** Diversus's own site lists clinics in Colorado Springs, Woodland Park, Cripple Creek, Calhan, Bailey and Fairplay (El Paso, Teller, Park). Solvista's lists Cañon City, Salida, Westcliffe and Leadville (Fremont, Chaffee, Custer, Lake). The providers' own site lists were used, and the correction is written into each feature's `counties_served`.

## 4. Other details
- **Health Solutions West** = the former **Mind Springs Health** (acquired by Pueblo's Health Solutions; Business Times, Post Independent). Address 515 28 3/4 Rd, Grand Junction, from the NPI registry and directory listings, because the new site showed no address.
- **Clinica Family Health & Wellness** now provides the behavioral health services formerly run by Mental Health Partners (Boulder/Broomfield).
- Many of these centers run **IPS supported employment** (see Layer 8).
- **Disability employment providers** (DVR vendors, Community Centered Boards / Case Management Agencies) aren't in this layer. DVR offices are in Layer 9.

## 5. Coordinates
16 Census, 1 OpenStreetMap. Each provider has many clinic sites. Only main offices are mapped here, and the site lists saved during collection could be added later.
