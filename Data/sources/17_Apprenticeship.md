# Layer 17 — Apprenticeship and Pre-Apprenticeship Programs

**Output:** `Data/Apprenticeship_Programs.geojson` (9 providers) · **Build script:** `scripts/build_03_17_etpl.py` · **Built:** 2026-11-13

## 1. Is there a statewide dataset?
| Searched | Result |
|---|---|
| data.colorado.gov "CDLE – apprenticeship.gov – Apprentices by Location (March 2025)" (bgbq-h7em) | Official RAPIDS extract, but **one row per apprentice** (9.7 M rows nationally) with **no sponsor names or addresses**. Can't map sponsors. |
| apprenticeship.gov Partner Finder | Searchable in a browser. Its data comes from a search index queried with keys built into the web page. **Using those keys for bulk extraction was deliberately avoided.** |
| **DOL TrainingProviderResults.gov ETPL file** | Registered apprenticeship and pre-apprenticeship programs that are WIOA-eligible appear here. Used (see Layer 3 for how the file was processed). |

## 2. Selection
An ETPL provider is included when any of its programs mentions "apprentice" in the program name, provider name or description. Result:
- **Registered apprenticeship sponsors / programs:** UCCS Colorado Cybersecurity Apprenticeship Program (C-CAP), Western Slope Plumbers & Pipefitters Joint Apprenticeship (Grand Junction).
- **Pre-apprenticeship:** The Master's Apprentice (Denver, skilled-trades pre-apprenticeship), Colorado Center for Nursing Excellence (Health Careers Pre-Apprentice Academy).
- **Colleges with apprenticeship-linked programs:** Colorado Mountain College, Red Rocks CC, Pikes Peak State College, Trinidad State, CMU Tech (Western Colorado CC).

`apprenticeship_program_names` lists the matching programs. "(apprenticeship named in description)" means the word appears only in the program description.

## 3. Gaps and recommended follow-up
This is **only the WIOA-eligible subset.** Colorado has many more registered apprenticeship sponsors (union JATCs, employers, the Colorado State Apprenticeship Agency's programs). To complete the layer, export sponsors for Colorado from **apprenticeship.gov → Partner Finder** in a browser (or request a sponsor list from CDLE's State Apprenticeship Agency) and add them.
