"""
Layer 24 - Veterans Employment and Reentry Programs

PROVENANCE SUMMARY (full write-up: Data/sources/24_Veterans.md)
  VA health sites : HIFLD "Veterans Health Administration Medical Facilities"
                    (from VA's VAST site database, data last edited 2023-05-22),
                    ArcGIS layer published by account basemaps_IHS:
                    https://services2.arcgis.com/VFLAJVozK0rtzQmT/arcgis/rest/services/Veterans_Health_Administration_Medical_Facilities/FeatureServer/0
                    Raw: Data/raw/hifld_vha_facilities_CO.json
  VA benefits     : Denver VA Regional Benefit Office (Veteran Readiness &
                    Employment, VR&E) - va.gov facility page.
"""
import json, os
from common import make_feature, geocoded_feature, write_layer, RAW

CAT = "Veterans Employment and Reentry"
URL = ("https://services2.arcgis.com/VFLAJVozK0rtzQmT/arcgis/rest/services/"
       "Veterans_Health_Administration_Medical_Facilities/FeatureServer/0")
TYPE = {"VAMC": "VA Medical Center", "CLC": "VA Community Living Center",
        "MSCBOC": "VA Multi-Specialty Community Clinic", "PCCBOC": "VA Primary Care Community Clinic",
        "OOS": "VA Other Outpatient Clinic", "VTCR": "Vet Center (readjustment counseling, employment referral)",
        "DRRTP": "VA Domiciliary Residential Rehabilitation (incl. homeless veterans)"}

d = json.load(open(os.path.join(RAW, "hifld_vha_facilities_CO.json")))
feats, skipped = [], []
for f in d["features"]:
    a = f["attributes"]
    if a["S_ABBR"] == "MVCTR":           # mobile vet centers have no fixed site
        skipped.append(a["STA_NAME"] + " (mobile)")
        continue
    addr = a["S_ADD1"] if a["S_ADD1"] not in (None, "", "None") else None
    feats.append(make_feature(a["LON"], a["LAT"], name=a["STA_NAME"], category=CAT,
        facility_type=TYPE.get(a["S_ABBR"], a["S_ABBR"]),
        address=addr, address_note=a.get("S_ADD2") if a.get("S_ADD2") not in (None, "None", "") else None,
        city=a["S_CITY"], zip=a.get("S_ZIP"), va_station=a["STA_NO"],
        homeless_point_of_contact=a.get("Homeless_POC") or None,
        source="U.S. Dept. of Veterans Affairs VAST database via HIFLD VHA Medical Facilities (May 2023)",
        source_url=URL, geocode="source (VA VAST)"))

ADD = [dict(name="Denver VA Regional Benefit Office (Veteran Readiness & Employment, VR&E)",
            address="155 Van Gordon Street", city="Lakewood", zip="80228", phone="303-914-5832",
            source="va.gov Denver VA Regional Benefit Office page; Colorado Division of Veterans Affairs (phone)",
            source_url="https://www.va.gov/denver-va-regional-benefit-office/")]
probs = []
for r in ADD:
    f, p = geocoded_feature(r, CAT, r["source"], r["source_url"])
    if p: probs.append(p); continue
    f["properties"]["facility_type"] = "VA benefits office (VR&E Chapter 31 employment services)"
    feats.append(f)

write_layer("Veterans_Employment_and_Reentry.geojson", feats, probs + ["skipped " + s for s in skipped])
