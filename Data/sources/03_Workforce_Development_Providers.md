# Layer 3 — Competitors / Workforce Development Providers

**Output:** `Data/Workforce_Development_Training_Providers.geojson` (96 provider locations) · **Build scripts:** `scripts/extract_etpl_colorado.py`, `scripts/build_03_17_etpl.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
**Yes:** Colorado's **WIOA Eligible Training Provider List (ETPL)**. These are the training providers approved to receive WIOA Individual Training Account funds through workforce centers. The CWDC's ETPL platform is on a blocked colorado.gov host, but the U.S. Department of Labor publishes every state's ETPL in one national file:
- **TrainingProviderResults.gov program file**: https://www.trainingproviderresults.gov/data/DownloadPrograms.xlsx (36 MB; programs on state lists **as of June 30, 2024**; form ETA-9171 data; dictionary in `Data/raw/etpl_data_dictionary.pdf`).
- `scripts/extract_etpl_colorado.py` streams the 77,086-row file using only built-in Python and keeps rows where **reportingstate = CO and provider state = CO**. Result: 1,625 programs → `Data/raw/etpl_CO.csv`.
- DOL lists Colorado among "states with known data quality concerns" for this file, which is consistent with the problems below.

## 2. Processing
- Programs grouped into **one point per provider + street address**, with `program_count`, top-3 fields of study (`main_fields`, from CIP titles), `entity_type`, and whether any program is an apprenticeship.
- **Address cleanup:** removed placeholder tokens "N/a" and "Null"; fixed the file's typos ("Drrive", "Suiter", "Av"); removed stray tokens such as "100college" and "Box 35".
- **Out-of-state rows wrongly marked CO were left off.** Heavy Equipment College of Oklahoma, Penn Foster (Scranton PA), SnapIT (Overland Park KS), Mountain States Line Constructors (West Jordan UT), University of West Florida, and San Juan College (Farmington NM) are online or out-of-state providers, so the Colorado bounding-box check rejected them.
- **Not placed (no geocodable address):** Morgan CC (Hwy 34, Wray), Colorado Firecamp (County Road 240), US Truck Driving School Fountain (Wigwam Rd), CU Boulder ("43 UCB" campus mail code), Sage Truck Driving Schools Grand Junction, UCH Memorial Hospital EMS. The colleges among these are in Layer 16.

## 3. Coordinates
Census geocoder (93) and OpenStreetMap (2–3). The file's own lat/long are rounded to 2 decimals (~1 km) and weren't used.

## 4. Scope note (important for "Competitors")
The ETPL covers **training** providers. The PDF also means nonprofit **employment, coaching and placement** providers, which aren't on the ETPL. Those are in:
- Layer 10 (Reentry: CEO, Second Chance Center, WAGEES partners).
- Layer 25 (Social enterprises).
- Layer 8 (IPS).

A dedicated list of placement-focused nonprofits (e.g., Goodwill of Colorado, Bayaud Enterprises, CWEE, Mi Casa, Work Options for Women) is a **recommended follow-up**.
