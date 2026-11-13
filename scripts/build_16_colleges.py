"""
Layer 16 - Community Colleges and Technical Schools

PROVENANCE SUMMARY (full write-up: Data/sources/16_Community_Colleges_and_Technical_Schools.md)
  Source : U.S. Dept. of Education, NCES IPEDS Institutional Characteristics
           (Directory) 2024, via the Urban Institute Education Data API
           https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2024/?fips=8
           Raw: Data/raw/ipeds_dir_CO_2024.json
  Coords : IPEDS latitude/longitude (supplied by NCES).
  Added  : CMU Tech (formerly Western Colorado Community College) and San Juan
           Basin Technical College, which are not separate IPEDS institutions.
"""
import json, os
from common import fetch, make_feature, geocoded_feature, write_layer, RAW

CAT = "Community Colleges and Technical Schools"
API = "https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2024/?fips=8"
rows = json.loads(fetch(API, "ipeds_dir_CO_2024.json"))["results"]

# Public institutions that are community/technical colleges but report as
# "4-year" in IPEDS because they now award a few bachelor's degrees.
PUBLIC_CC = {"Aims Community College", "Colorado Mountain College"}
SECTOR = {4: "Public 2-year", 5: "Private nonprofit 2-year", 6: "Private for-profit 2-year",
          7: "Public less-than-2-year", 8: "Private nonprofit less-than-2-year",
          9: "Private for-profit less-than-2-year"}

feats = []
for r in rows:
    if r.get("currently_active_ipeds") != 1:
        continue
    cccs = r.get("inst_system_name") == "Colorado Community College System"
    if r["sector"] in SECTOR:
        kind = SECTOR[r["sector"]]
        group = ("Public community/technical college" if r["sector"] in (4, 7)
                 else "Cosmetology/beauty school" if r["sector"] == 9 and any(w in r["inst_name"].lower() for w in ("beauty", "salon", "paul mitchell", "aveda", "hair", "cheeks", "tigi", "stacey james", "avalon"))
                 else "Private career/technical school")
    elif r["sector"] == 1 and (cccs or r["inst_name"] in PUBLIC_CC):
        kind, group = "Public (IPEDS 4-year; primarily associate/certificate)", "Public community/technical college"
    else:
        continue
    feats.append(make_feature(float(r["longitude"]), float(r["latitude"]),
        name=r["inst_name"], category=CAT, school_type=group, ipeds_sector=kind,
        system="Colorado Community College System" if cccs else None,
        address=r["address"], city=r["city"].replace("  ", " "), zip=str(r["zip"])[:5],
        county=(r.get("county_name") or "").replace(" County", "") or None,
        phone=r.get("phone_number"), website=r.get("url_school"),
        ipeds_unitid=r["unitid"],
        source="NCES IPEDS Directory 2024 (via Urban Institute Education Data API)",
        source_url=API, geocode="source (IPEDS)"))

ADD = [
 dict(name="CMU Tech (formerly Western Colorado Community College) - Bishop Campus", address="2508 Blichmann Avenue",
      city="Grand Junction", zip="81505", phone="970-255-2600", school_type="Public community/technical college",
      source="Colorado Mesa University contact page; CMU Tech campus map (renamed from WCCC Aug 1, 2023)",
      source_url="https://www.coloradomesa.edu/campus-info/contact.html"),
 dict(name="San Juan Basin Technical College", address="33057 Highway 160", city="Mancos", zip="81328",
      phone="970-565-8457", school_type="Public community/technical college",
      source="U.S. Dept. of Education DAPIP accreditation database (via SkillPlum listing)",
      source_url="https://skillplum.com/school/san-juan-basin-technical-college-mancos-co"),
]
probs = []
for r in ADD:
    st = r.pop("school_type")
    f, p = geocoded_feature(r, CAT, r["source"], r["source_url"])
    if p: probs.append(p); continue
    f["properties"]["school_type"] = st
    feats.append(f)

write_layer("Community_Colleges_and_Technical_Schools.geojson", feats, probs)
import collections
print(collections.Counter(f["properties"]["school_type"] for f in feats))
