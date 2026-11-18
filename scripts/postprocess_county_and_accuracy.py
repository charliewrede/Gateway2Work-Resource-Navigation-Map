"""
postprocess_county_and_accuracy.py - runs after all build scripts (run_all.py).

Adds two popup fields to every layer in Data/:

  county             The county the point falls in (city-summary points in
                     Recovery_Residences_by_City keep the source's county), from official U.S. Census
                     TIGERweb county boundaries (point-in-polygon). Replaces
                     the mixed-source county values some layers had.
                     Boundaries saved to Data/raw/census_tiger_counties_CO.geojson
                     Source: https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/1

  location_accuracy  ONLY set on points whose location or address is uncertain.
                     Points with a confirmed street address get no flag.
                     Rules (applied in this order):
                       1. geocode method says the point is a city/town/ZIP
                          center, street-level match, or best-guess match
                       2. explicit list below (UNSURE) of addresses that came
                          from old, third-party or conflicting sources, or were
                          set by project-staff decision
                       3. Workforce Centers whose address is still from the
                          2022 American Job Center list (address_status)
"""
import glob, json, os, urllib.parse
from common import DATA, RAW, fetch_json

# ---------------------------------------------------------------- counties
CFILE = os.path.join(RAW, "census_tiger_counties_CO.geojson")
if not os.path.exists(CFILE):
    url = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/1/query?"
           + urllib.parse.urlencode({"where": "STATE='08'", "outFields": "NAME,GEOID",
                                     "outSR": 4326, "f": "geojson", "returnGeometry": "true"}))
    json.dump(fetch_json(url), open(CFILE, "w"))
counties = json.load(open(CFILE))["features"]

def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return polys

def inside(x, y, ring):
    c = False
    for i in range(len(ring)):
        x1, y1 = ring[i - 1][:2]; x2, y2 = ring[i][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def county_of(x, y):
    for c in counties:
        for poly in rings(c["geometry"]):
            if inside(x, y, poly[0]) and not any(inside(x, y, h) for h in poly[1:]):
                return c["properties"]["NAME"].replace(" County", "")
    return None

# ---------------------------------------------------------------- accuracy
def from_geocode(g):
    g = (g or "")
    if "ZIP" in g and "APPROX" in g.upper():
        return "Approximate - center of ZIP code (PO Box, no physical location)"
    if "no physical location" in g:
        return "Approximate - town center (no physical location)"
    if "individual homes intentionally not mapped" in g:
        return "Approximate - city center (summary of homes in this city; individual homes not mapped for privacy)"
    if "city center" in g.lower() or "approx-city-center" in g:
        return "Approximate - city center (street address not available)"
    if g == "osm-street-approx":
        return "Approximate - on the correct street; exact building not confirmed"
    if g == "census-nonexact":
        return "Approximate - best match among several possible addresses"
    if g == "manual":
        return "Approximate - placed by hand (address did not geocode; see layer write-up)"
    return None

# (layer file, feature name) -> flag text. Addresses I am not sure about.
UNSURE = {
 ("Recovery_Friendly_Employers.geojson", "Absolute Caulking and Waterproofing Inc."):
     "Address verified by project staff (2026-11-17)",
 ("Probation_and_Parole_Offices.geojson", "Aurora Parole Office (CDOC Division of Adult Parole)"):
     "Address unconfirmed - from an older third-party directory",
 ("Probation_and_Parole_Offices.geojson", "Colorado Springs Parole Office (CDOC Division of Adult Parole)"):
     "Address unconfirmed - from map listings, not CDOC",
 ("Probation_and_Parole_Offices.geojson", "Fort Collins Parole Office (CDOC Division of Adult Parole)"):
     "Address unconfirmed - from map listings, not CDOC",
 ("Homelessness_and_Housing_Services.geojson", "Pueblo Rescue Mission"):
     "Address unconfirmed - from a third-party shelter directory",
 ("Community_and_Faith_Based_Organizations.geojson", "Pueblo Rescue Mission"):
     "Address unconfirmed - from a third-party shelter directory",
 ("Adult_Education_and_GED_Programs.geojson", "Community Educational Outreach"):
     "Address unconfirmed - from a 2015 CDE directory",
 ("Community_Mental_Health_Providers.geojson", "Axis Health System (not a CBHC member)"):
     "Address unconfirmed - sources list three different main offices",
 ("IPS_Agencies.geojson", "Axis Health System - IPS"):
     "Address unconfirmed - sources list three different main offices",
 ("DVR_Offices.geojson", "DVR Aurora Office"):
     "Address unconfirmed - from a regional directory, not DVR",
 ("DVR_Offices.geojson", "DVR Montrose Office"):
     "Address unconfirmed - from an older listing",
 ("Community_Corrections.geojson", "Advantage Treatment Centers - Alamosa (San Luis Valley Community Corrections)"):
     "Address partly unconfirmed - operator lists 2017 Lava Lane; 2017 state list had 2255 Lava Lane",
 ("Community_Corrections.geojson", "Correctional Alternative Placement Services (CAPS)"):
     "Location unconfirmed - only recent source is a third-party directory; program may not be operating",
 ("Workforce_Centers.geojson", "Durango - Southwest Colorado Workforce Center"):
     "Address unconfirmed - another listing gives 160 Rock Point Drive",
 ("Workforce_Centers.geojson", "Sterling Workforce Center"):
     "Address unconfirmed - center reported to have moved (CSU Engagement Center / 304 Main St)",
 ("Workforce_Centers.geojson", "Limon Workforce Center"):
     "Address unconfirmed - another listing gives 333 M Avenue",
}

stats = {}
for path in sorted(glob.glob(os.path.join(DATA, "*.geojson"))):
    fname = os.path.basename(path)
    if fname.startswith("example-"):
        continue
    d = json.load(open(path))
    n_flag = 0
    for f in d["features"]:
        p = f["properties"]
        x, y = f["geometry"]["coordinates"][:2]
        c = county_of(x, y)
        # Recovery-residence points summarize a whole city (e.g. Aurora spans
        # 3 counties), so keep the county given by the Oxford House listings.
        if c and not (fname == "Recovery_Residences_by_City.geojson" and p.get("county")):
            p["county"] = c
        flag = from_geocode(p.get("geocode"))
        flag = UNSURE.get((fname, p.get("name")), flag) if not flag else flag
        if not flag and fname == "Workforce_Centers.geojson":
            st = p.get("address_status", "")
            if st.startswith("from 2022"):
                flag = "Address unconfirmed - from the 2022 American Job Center list, not re-checked"
            elif "third-party" in st:
                flag = "Address unconfirmed - from a third-party listing"
        if flag:
            p["location_accuracy"] = flag; n_flag += 1
        else:
            p.pop("location_accuracy", None)
    json.dump(d, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    stats[fname] = (len(d["features"]), n_flag, sum(1 for f in d["features"] if not f["properties"].get("county")))
for k, (n, fl, nc) in stats.items():
    print(f"{k:58} {n:4} points | flagged {fl:3} | no county {nc}")

# Keep the CSV copies (data_csv/ and SharePoint Data_CSV) in step with the GeoJSON.
import subprocess, sys
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "export_csv.py")], check=False)
