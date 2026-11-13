# Layers 19 and 21 — not built yet (and why)

Both layers were researched on 2026-11-13. **No GeoJSON was created**, because no verifiable source could be downloaded, and padding the layers with unverified records would undermine the rest of the map.

## Layer 19 — Human Services Departments (64 county departments)
- **Authoritative source:** Colorado Department of Human Services, *Contact your county human services department*, https://cdhs.colorado.gov/contact-your-county-human-services-department. It lists every county department's office, phone and website.
- **Why not built:** cdhs.colorado.gov returns HTTP 403 to automated tools. A CDHS **development/staging copy** of the same page was reachable, but using it to get around the production block was declined (and that's the right call). Search-engine copies show county names but not reliable addresses. Third-party directories found were 1,000+ days old. The APHSA "Colorado Contacts" PDF (Feb 2026) also returned 403.
- **How to finish it (about 5 minutes):**
  1. Open the CDHS page above in a browser and save it as *Web Page, HTML Only* to `Data/raw/cdhs_contact_your_county.html`.
  2. Ask for `scripts/build_19_human_services.py` to be written to parse that file (64 offices; Grand and Jackson share a department), geocode it, and write `Data/Human_Services_Departments.geojson`.

## Layer 21 — Staffing Agencies and Second-Chance Employers
- **Searched:** data.colorado.gov; Second Chance Business Coalition (its Colorado listings are service providers, not employers); fair-chance employer directories (commercial, unverified). No official Colorado roster of second-chance employers exists.
- **What already covers this role:**
  - **Layer 1:** 147 Recovery Friendly Workplace employers, with certified ones flagged.
  - **Layer 25:** employers that directly hire people with barriers (Goodwill, Bayaud, Women's Bean Project, Mile High WorkShop, CEO).
- **How to finish it:** build the list from (a) employers that have hired through WAGEES or CEO (ask the program staff), (b) ReHire Colorado host-site employers (CDHS), and (c) staffing agencies that place justice-involved workers, confirmed by phone. Then add them with a `source` note for each.
