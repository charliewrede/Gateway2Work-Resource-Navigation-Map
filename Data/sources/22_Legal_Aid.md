# Layer 22 — Legal Aid and Record-Sealing Services

**Output:** `Data/Legal_Aid_and_Record_Sealing.geojson` (12 offices) · **Build script:** `scripts/build_22_legal_aid.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
No. data.colorado.gov has nothing; lawhelp.colorado.gov and the Office of Administrative Courts' "Free or Low Cost Legal Services" PDF are on blocked colorado.gov hosts.

**Colorado Legal Services (CLS)** is the single statewide, federally funded (LSC) civil legal aid organization, and it runs a **Record Sealing & Expungement (RSE) clinic**. Its own office list is the authoritative source:
https://www.coloradolegalservices.org/get-help/ (downloaded 2026-11-13 → `Data/raw/cls_get_help.html`).

## 2. Verification
- Addresses were taken from CLS's current page, which a search engine reported as updated about 10 days before collection.
- **Conflicts found and resolved in favor of CLS's own page:** a 2024 Office of Administrative Courts PDF lists the Denver office at 1905 Sherman St (CLS has since moved to **1560 Broadway, Suite 1100**, "now located in the Civic Center"); a 2024 court guide lists Grand Junction at 422 White Ave (CLS now gives 120 West Park Dr **as a mailing address**, flagged); the Secretary of State charity registry still lists old CLS offices (Frisco, 1474 Main Ave Durango, 424 Pine St Fort Collins) that are no longer on CLS's list.
- The `counties_served` property is copied from each office's "Serves people from" text.

## 3. Coordinates
11 by Census geocoder, 1 by OpenStreetMap.

## 4. Record-sealing organizations found but not mapped (no fixed public office)
| Organization | What they do | Source |
|---|---|---|
| Expunge Colorado (Denver metro) | Pro bono record-sealing clinics since 2018; waitlist of 300+ | Westword; Denver7 |
| Colorado Criminal Defense Institute | Free sealing clinics around the state | Colorado Independent; CBS Colorado |
| Second Chance Center (Aurora) | Has hosted sealing events with Expunge Colorado (mapped in Layer 10, Reentry) | CBS Colorado |
| Colorado Judicial Branch Self-Help Centers / Colorado Legal Help Center | Free legal clinics including record sealing; *Sealing Criminal Records* guide (April 2025) | coloradojudicial.gov |

**Follow-up:** add Colorado Judicial Self-Help Centers (one per courthouse) and law school clinics (CU Boulder, DU Sturm) if wanted.
