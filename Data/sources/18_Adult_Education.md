# Layer 18 — Adult Education and GED Programs

**Output:** `Data/Adult_Education_and_GED_Programs.geojson` (36 sites) · **Build script:** `scripts/build_18_adult_education.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
**Yes, an official one.** The Colorado Department of Education, Office of Adult Education Initiatives, maintains a **"Find a Program" Google My Map**, linked from its Current Grantees page (https://ed.cde.state.co.us/cdeadult/grantees/grantees-current-grantees). Its KML export was downloaded:
`https://www.google.com/maps/d/kml?mid=1YCoTGtwGf6FmQ_Ruzj32FwtXwxNunlI&forcekml=1` → `Data/raw/cde_adulted_sites.kml`
The map covers programs funded by federal **AEFLA** and state **AELA** grants, plus the Colorado Adult High School program.

## 2. What was used
The KML has four folders:
| Folder | Count | Used? |
|---|---|---|
| **Program Locations** | 33 | **Yes:** current funded sites |
| X_Sample Find a Program Map.xlsx | 96 | **No.** Its name marks it as a sample/old import, and it includes programs not on the current grantee list (e.g., Adams 14) |
| Workforce Center Locations | 55 | No (Layer 2 has its own sources). It still shows older addresses, e.g. Adams County at 3155 N Chambers Rd, which helped confirm Layer 2's updates were needed |
| Counties and Workforce Areas | 64 polygons | No |

## 3. Cross-check against CDE's current grantee list
CDE's grantee page lists 2024-28 AEFLA, 2025-29 AELA, and Colorado Adult High School grantees. Every grantee has a site in the map **except three**, which were added:
- **Asian Pacific Development Center:** its adult education program now runs through Aurora Mental Health & Recovery at 1537 Alton St, Aurora (AuMHR page: "registration in person only at 1537 Alton St.").
- **Community Educational Outreach:** 7251 E 49th Ave, Commerce City, from a **2015** CDE program directory (flagged; confirm).
- **Larimer County Economic & Workforce Development:** 200 W Oak St, Fort Collins (larimer.gov/ewd).

## 4. Corrections to the source
Two **typos in CDE's map** prevented geocoding and were corrected: "701 **Caminio** del Rio" → Camino del Rio (Durango Adult Education Center); "15445 E **Illif** Avenue" → Iliff (Goodwill EXCEL Center).

## 5. Coordinates
The KML has addresses only, no coordinates. 34 Census geocoder, 2 OpenStreetMap.

## 6. Note
GED/HiSET **testing centers** (Pearson VUE / ETS) are a separate list and aren't included.
