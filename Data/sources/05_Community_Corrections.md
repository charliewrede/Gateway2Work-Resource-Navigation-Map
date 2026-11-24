# Layer 5: Community Corrections

**Output:** `Data/Community_Corrections.geojson` (25 residential programs) · **Build script:** `scripts/build_05_community_corrections.py` · **Rebuilt:** 2026-11-24

In Colorado, "community corrections" means the residential programs ("halfway houses") regulated by the Division of Criminal Justice (DCJ), Office of Community Corrections (OCC). Placements are approved by each judicial district's Community Corrections Board.

## 1. Source (since 2026-11-24)
**DCJ OCC, "Community Corrections Boards, Program & Specialized Programs":** https://dcj.colorado.gov/dcj-offices/occ/corrections-boards-programs

This is the official state list of every board and program. dcj.colorado.gov blocks automated tools (HTTP 403), so project staff copied the page on **2026-11-24**. The copy is saved unchanged in **`Data/raw/dcj_occ_2026-11-24/`**:

| File | Contents |
|---|---|
| `1_boards_and_programs_1st_JD.txt` | 1st JD (Gilpin and Jefferson): board and programs |
| `2_boards_and_programs_2nd_to_23rd_JD.txt` | 2nd JD (Denver) through the 23rd JD: boards and programs |
| `3_specialized_programs.txt` | Eligibility for the three specialized programs: IRT, SOSTCC and RDDT. |

The build script reads these files directly. Every program on the list is mapped, and no program that is not on the list is mapped. 7 districts have no program: the 3rd, 5th, 11th, 14th, 16th, 22nd and 23rd.

**What each popup shows:**
- **From the program list:** address, phone, population served (male/female), director, and the program's email where one is listed.
- **District:** the judicial district and the counties in it.
- **Board:** the district's Community Corrections Board contacts (names, phone and email), as published by DCJ.
- **Specialized programs (12 facilities):** IRT, SOSTCC or RDDT eligibility from the specialized-programs list. This includes gender, length of stay, substance-use and mental-health levels, sex/violent offender acceptance, notes, and the intake contact. Facility names on that list differ slightly from the program list, so they are matched by an explicit table (`ALIASES` in the build script), and the script stops if any listing doesn't match.

Every feature has `verified` = "Official DCJ OCC list, copied from the DCJ page by project staff 2026-11-24".

## 2. Fixes to the copied text (each recorded in the feature's `corrections_note`)
| Program | DCJ list says | Map uses | Why |
|---|---|---|---|
| Independence House Pecos | ZIP 80218 | 80211 | 4101 Pecos St is in 80211; 80218 is Capitol Hill. |
| Mesa County Community Corrections | ZIP 81502 | 81501 | 81502 is a PO-box ZIP. |
| Garfield County Community Corrections | program at **0224** County Rd 333A; board at **0244** County Road 333A | 0224 shown; placed at the facility's HIFLD footprint | The two numbers on the DCJ page disagree, and the rural address doesn't geocode. The popup says the point was placed by hand. |
| Joe Pelle Center | "Joe Pelle Center- Boulder County" | "Joe Pelle Center - Boulder County" | Spacing only. |

## 3. Changes from the previous version (28 → 25)
The earlier layer (2026-11-13) was built from DCJ's 2017 program list, re-checked against operator sites and county board pages, because the current DCJ page couldn't be read. Compared with the official list:

**Removed (4; not on the DCJ list):**
- CoreCivic – Longmont Community Treatment Center (236 Main St, Longmont)
- Correctional Alternative Placement Services (CAPS), Craig. The DCJ list says the 14th JD has no program.
- Embrave – 3950 N Nevada Ave, Colorado Springs. DCJ lists ComCor/EMBRAVE once, at 3615 Roberts Rd. The 3950 building may still be part of the same program; see §5.
- ICCS – Boulder (1770 21st St)

**Added (1):** Joe Pelle Center – Boulder County, 3260 Airport Rd, Boulder (20th JD).

**Same location, now under the DCJ name (24):** for example, Hilltop House is now listed as Advantage Treatment Center – Durango, and MOORE Center as Moore Center.

**Old open questions settled:**
- **Alamosa** is at 2255 Lava Lane, not 2017.
- **Arapahoe County Residential Center** is operated by GEO.
- **CAPS** is not on the list.
- **Pueblo** has only ICCS–Pueblo; there is no second program.

The old version is in git history.

## 4. Coordinates
- **Census geocoder:** 22.
- **OpenStreetMap:** 2, both matching the house number: 1050 Avenida del Sol, Durango, and 4101 Pecos St, Denver.
- **Manual:** 1. Garfield County, from its HIFLD facility footprint.

## 5. Remaining questions
- **Garfield County:** is the street number 0224 or 0244 County Rd 333A? The map position doesn't depend on it.
- **Embrave 3950 N Nevada:** Embrave's own site listed two residential buildings. Ask the 4th JD board (719-520-6987) whether 3950 N Nevada should be mapped as a second site of ComCor/EMBRAVE.
- **Joe Pelle Center:** the only phone on the DCJ list is the director's (970-449-2781). For referrals, the list gives 303-441-4711, which appears as the board's referral line.
- **Updating:** when the DCJ page changes, copy it into a new `Data/raw/dcj_occ_<date>/` folder with the same three file names, change `DIR` in the build script, and run `python3 scripts/run_all.py`.
- Federal BOP Residential Reentry Centers (halfway houses under federal contract) are in Layer 12, not here.
