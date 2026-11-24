# Layer 2: Workforce Centers (Colorado Workforce Centers / American Job Centers)

**Output:** `Data/Workforce_Centers.geojson` (44 centers) · **Build script:** `scripts/build_02_workforce_centers.py` · **Rebuilt:** 2026-11-24

## 1. Source (since 2026-11-24)
**Colorado Department of Labor and Employment (CDLE), Workforce Centers contact list:** https://cdle.colorado.gov/jobs-training/workforce-centers

This is the official state list of every workforce center. cdle.colorado.gov blocks automated tools (HTTP 403), so project staff copied the list from the page on **2026-11-24**. The copy is saved unchanged as **`Data/raw/cdle_workforce_centers_2026-11-24.txt`**. The build script reads that file directly. Every center on the list is mapped, and no center that is not on the list is mapped.

Each center's popup shows the list's address, phone, email, fax, hours, TDD, mailing address (PO Box), employer line and notes. The CDLE office ID is kept in the data but hidden in the popup. Every feature has `verified` = "Official CDLE list, copied from the CDLE page by project staff 2026-11-24".

**Websites:** the copied text names each center's website ("Workforce Colorado Rural Alliance Website") but has no links. The `website` field is filled with each local area's own page, which this project had used as sources earlier. Those links are not from the CDLE list. Pikes Peak, Fort Morgan and Woodland Park have no link because none was confirmed.

## 2. Fixes to the copied text (each recorded in the feature's `corrections_note`)
| Center | CDLE list says | Map shows | Why |
|---|---|---|---|
| Denver Workforce at Montebello | "Montebello" | Montbello | The neighborhood is Montbello. The original spelling is kept in `cdle_name`. |
| Montrose Workforce Center | hours "8:00 PM - 12:00 PM" | 8:00 AM | Typo. |
| Woodland Park Office | city "South Woodland Park" | Woodland Park | The mailing city is Woodland Park, and the geocoder can't find "South Woodland Park". |
| Larimer County EWD - Fort Collins | ZIP 80522 | 80522 shown; 80521 used to locate it | 80522 is a PO-box ZIP; the building is in 80521. |

## 3. Changes from the previous version (54 → 44 centers)
The earlier layer (2026-11-13) was built from the May 2022 federal American Job Center list plus local workforce area pages. Compared with the official CDLE list:

**Removed (14; not on the CDLE list):** Burlington, Clear Creek County (Idaho Springs), Gilpin County (Black Hawk), Denver Westside (1200 Federal Blvd), Denver International Airport, Edwards, Elizabeth, Granby, Rangely, Rifle, Rocky Ford, San Luis, Pikes Peak at Calhan, Pikes Peak at Fountain.

**Replaced (1):** Aspen Mine Center, 166 E Bennett Ave, Cripple Creek → **Pikes Peak Workforce Center at Cripple Creek, 100 W Bennett Ave**.

**Address changed (8):**
| Center | Old address | CDLE address |
|---|---|---|
| Cañon City | 3224B Independence Rd | 248 Dozier Ave |
| Durango | 331 S Camino del Rio, Ste C | 160 Rock Point Dr |
| Limon | 285 D Ave | 333 M Ave, Ste 300 |
| Montrose | 504 N 1st St | 1551 Ogden Rd |
| Sterling | 100 College Ave | 111 N 3rd St |
| Walsenburg | 928 Russell Ave | 201 E 5th St, Ste 19 |
| Workforce Boulder County - Boulder | 2520 55th St, Ste 100 | 1333 Iris Ave (by appointment) |
| Denver Montbello | 4685 Peoria St, Ste 251 | 4685 Peoria St, Ste 201 (same building) |

**Added (4):** Adams County at Aurora (3155 N Chambers Rd, Unit C), Adams County at Brighton (36 S 18th Ave, Unit A), Arapahoe/Douglas Works! Littleton satellite (5933 S Fairfield St), Woodland Park Office (701 Gold Hill Pl).

The six open status questions from the old layer are settled by the CDLE list: Denver Westside and Edwards are not on it, and Cañon City, Sterling, Limon and Durango have the addresses above. The old version is in git history (commit before 2026-11-24).

## 4. Coordinates
- **Census geocoder:** 39 centers. **OpenStreetMap:** 5 (Castle Rock, Broomfield, Frisco, Woodland Park, Limon). Each OpenStreetMap point was checked and is in the right town.
- **Limon** matched only the street (M Avenue), so its popup is flagged "Approximate - on the correct street".
- Suite, unit and building text is removed before geocoding only; the full address is shown.

## 5. Remaining questions
- **Adams County at Aurora, 3155 N Chambers Rd:** this is on the CDLE list. When building the earlier version, I found news reports that the Chambers Rd human services building was closing, so I had left it off. It is mapped now because the official list includes it. Call (720) 523-2580 to confirm.
- **Updating:** when the CDLE page changes, copy it into a new `Data/raw/cdle_workforce_centers_<date>.txt`, change `RAW_FILE` in the build script, and run `python3 scripts/run_all.py`, or run the build script and then `postprocess_county_and_accuracy.py`.
