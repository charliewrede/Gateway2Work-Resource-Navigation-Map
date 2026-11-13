"""
Layer 7 - Prisons (state, private-contract and federal correctional facilities)

PROVENANCE SUMMARY (full write-up: Data/sources/07_Prisons.md)
  Facility LIST:
    - CDOC state-operated: "Colorado Department of Corrections Facility Address
      List" (CDOC document, March 2025), saved as
      Data/raw/cdoc_facility_address_list_2025-03.pdf
    - Private prisons holding CDOC inmates: CoreCivic facility pages + CDOC
      "private prisons" pages
    - Federal: Federal Bureau of Prisons public locations feed
      https://www.bop.gov/PublicInfo/execute/locations?todo=query&output=json
  COORDINATES:
    - Federal: taken from the BOP feed, except the Florence units, which share
      one point there, so each unit uses its HIFLD building footprint instead.
    - State/private: HIFLD Prison Boundaries footprint centroids (HIFLD Open,
      decommissioned Aug 2025; read from the public ArcGIS mirror
      "Prison_Points"). Each centroid is checked against the Census geocode of
      the street address where the address can be geocoded.
"""
import math
from common import (arcgis_query, fetch_json, geocode, make_feature,
                    write_layer, RAW)
import json, os

CAT = "Prisons"
HIFLD = ("https://services.arcgis.com/XG15cJAlne2vxtgt/ArcGIS/rest/services/"
         "Prison_Points/FeatureServer/0")
CDOC_PDF = "https://seams.org/wp-content/uploads/2025/03/Attachment-A-Facilty-Address-List.pdf"
CDOC_SITE = "https://cdoc.colorado.gov/facilities"
BOP_FEED = "https://www.bop.gov/PublicInfo/execute/locations?todo=query&output=json"

# --- 1. HIFLD Colorado records (coordinates + cross-check) -------------------
hifld = arcgis_query(HIFLD, where="STATE='CO'", raw_name="hifld_prison_points_CO.geojson")
H = {f["properties"]["NAME"]: f for f in hifld}
print(f"HIFLD Colorado records: {len(hifld)}")

def hifld_xy(name):
    g = H[name]["geometry"]["coordinates"]
    return g[0], g[1]

def km(a, b):
    dx = (a[0] - b[0]) * 111.32 * math.cos(math.radians(a[1]))
    dy = (a[1] - b[1]) * 110.57
    return math.hypot(dx, dy)

# --- 2. CDOC state-operated facilities (March 2025 CDOC list) ---------------
# (name, address as printed, city, zip, HIFLD record used for coordinates)
CDOC = [
 ("Arkansas Valley Correctional Facility", "12750 Hwy 96 at Lane 13", "Ordway", "81034", "ARKANSAS VALLEY CORRECTIONAL FACILITY"),
 ("Arrowhead Correctional Center", "57500 East Highway 50 & Evans Road", "Canon City", "81212", "ARROWHEAD CORRECTIONAL CENTER"),
 ("Buena Vista Correctional Complex", "15125 Hwy 24 & 285", "Buena Vista", "81211", "BUENA VISTA CORRECTIONAL FACILITY"),
 ("Centennial Correctional Facility", "57500 East Highway 50 & Evans Road", "Canon City", "81212", "CENTENNIAL CORRECTIONAL FACILITY"),
 ("Colorado State Penitentiary", "57500 East Highway 50 & Evans Road", "Canon City", "81212", "COLORADO STATE PENITENTIARY"),
 ("Colorado Territorial Correctional Facility", "275 West Hwy 50", "Canon City", "81212", "COLORADO TERRITORIAL CORRECTIONAL FACILITY"),
 ("Delta Correctional Center", "11363 Lockhart Road", "Delta", "81416", "DELTA CORRECTIONAL CENTER"),
 ("Denver Reception & Diagnostic Center", "10900 Smith Road", "Denver", "80239", "DENVER RECEPTION AND DIAGNOSTIC CENTER"),
 ("Denver Women's Correctional Facility", "3600 Havana Street", "Denver", "80239", "DENVER WOMENS CORRECTIONAL FACILITY"),
 ("Four Mile Correctional Center", "57500 East Highway 50 & Evans Road", "Canon City", "81212", "FOUR MILE CORRECTIONAL CENTER"),
 ("Fremont Correctional Facility", "57500 East Highway 50 & Evans Road", "Canon City", "81212", "FREMONT CORRECTIONAL FACILITY"),
 ("La Vista Correctional Facility", "1401 West 17th Street", "Pueblo", "81003", "LA VISTA CORRECTIONAL FACILITY"),
 ("Limon Correctional Facility", "49030 State Hwy 71", "Limon", "80826", "LIMON CORRECTIONAL FACILITY"),
 ("Rifle Correctional Center", "200 County Road 219", "Rifle", "81650", "RIFLE CORRECTIONAL CENTER"),
 ("San Carlos Correctional Facility", "1410 West 13th Street", "Pueblo", "81003", "SAN CARLOS CORRECTIONAL FACILITY"),
 ("Sterling Correctional Facility", "12101 Hwy 61", "Sterling", "80751", "STERLING CORRECTIONAL FACILITY"),
 ("Trinidad Correctional Facility", "21000 Hwy 350 East", "Model", "81059", "TRINIDAD CORRECTIONAL FACILITY"),
 ("Youthful Offender System", "1300 West 13th Street", "Pueblo", "81003", "YOUTHFUL OFFENDER SYSTEM"),
]

NOTES = {
 "Rifle Correctional Center": "Proposed for closure in state budget talks (2025); local officials opposed. Evacuated Aug 2025 due to wildfire. Confirm operating status.",
 "Delta Correctional Center": "Possible closure discussed in 2025 budget (KVNF, 2025-03-06). Confirm operating status.",
}

feats, problems = [], []

for name, addr, city, z, hname in CDOC:
    x, y = hifld_xy(hname)
    glon, glat, gm, _ = geocode(f"{addr}, {city}, CO {z}")
    check = None
    if glon is not None:
        d = km((x, y), (glon, glat))
        check = f"HIFLD centroid is {d:.1f} km from Census geocode of address"
        if d > 3:
            problems.append(f"{name}: HIFLD vs Census differ by {d:.1f} km - reviewed")
    feats.append(make_feature(x, y, name=name, category=CAT,
        operator="Colorado Department of Corrections (state-operated)",
        address=addr, city=city, zip=z,
        source="Colorado Department of Corrections, Facility Address List (Mar 2025)",
        source_url=CDOC_PDF,
        geocode="HIFLD Prison Boundaries footprint centroid",
        verified=check, status_note=NOTES.get(name)))

# The Beacon at Skyline: reopened minimum-security unit on the Canon City
# East complex; not on the March 2025 address list (it shares CTCF's
# administration). Proposed for closure in 2025 budget discussions.
x, y = hifld_xy("SKYLINE CORRECTIONAL CENTER")
feats.append(make_feature(x, y, name="The Beacon at Skyline Correctional Center",
    category=CAT, operator="Colorado Department of Corrections (state-operated)",
    address="East Canon Complex", city="Canon City", zip="81212",
    source="Wikipedia 'Skyline Correctional Center'; Denver7 news report (2025)",
    source_url="https://en.wikipedia.org/wiki/Skyline_Correctional_Center",
    geocode="HIFLD Prison Boundaries footprint centroid",
    status_note="Not on CDOC Mar 2025 address list; reported proposed for closure in 2025. Confirm status before publication."))

# --- 3. Private prisons under contract with CDOC ----------------------------
PRIVATE = [
 ("Bent County Correctional Facility", "11560 Road FF.75", "Las Animas", "81054", "719-456-2610",
  "https://www.corecivic.com/facilities/bent-county-correctional-facility", "BENT COUNTY CORRECTIONAL FACILITY"),
 ("Crowley County Correctional Facility", "6564 Highway 96", "Olney Springs", "81062", "719-267-3548",
  "https://www.corecivic.com/facilities/crowley-county-correctional-facility", "CROWLEY COUNTY CORRECTIONAL FACILITY"),
]
for name, addr, city, z, ph, url, hname in PRIVATE:
    x, y = hifld_xy(hname)
    feats.append(make_feature(x, y, name=name, category=CAT,
        operator="CoreCivic (private) - houses CDOC inmates under contract",
        address=addr, city=city, zip=z, phone=ph,
        source="CoreCivic facility page; CDOC private prisons page", source_url=url,
        geocode="HIFLD Prison Boundaries footprint centroid",
        verified="CoreCivic page lists Colorado DOC as government partner (checked " + feats[0]["properties"]["retrieved"] + ")"))

# --- 4. Federal Bureau of Prisons --------------------------------------------
bop = json.load(open(os.path.join(RAW, "bop_locations.json"), encoding="latin1"))["Locations"]
# FCC Florence (FLX) is the administrative complex record and DET (MSTC) is a
# staff training center - neither holds people, so they are left out.
FLORENCE_HIFLD = {"FLF": "FCI FLORENCE", "FLM": "USP FLORENCE ADMAX", "FLP": "USP FLORENCE HIGH"}
for b in bop:
    if b.get("state") != "CO" or b["code"] in ("FLX", "DET"):
        continue
    if b["code"] in FLORENCE_HIFLD:
        x, y = hifld_xy(FLORENCE_HIFLD[b["code"]])
        gsrc = "HIFLD footprint centroid (BOP feed gives one shared point for all Florence units)"
    else:
        x, y = float(b["longitude"]), float(b["latitude"])
        gsrc = "source (BOP locations feed)"
    feats.append(make_feature(x, y, name=b["nameTitle"].replace("  ", " "),
        category=CAT, operator="Federal Bureau of Prisons",
        facility_type=b["faclTypeDescription"], address=b["address"].title(),
        city=b["city"].title(), zip=b["zipCode"], phone=b["phoneNumber"],
        website="https://www.bop.gov" + b["url"] if b.get("url", "").startswith("/") else b.get("url"),
        source="Federal Bureau of Prisons locations feed", source_url=BOP_FEED,
        geocode=gsrc))

# Federal Prison Camp at Florence (minimum-security satellite camp; listed by
# BOP as part of FCI Florence, has its own HIFLD footprint).
x, y = hifld_xy("FCI FLORENCE CAMP")
feats.append(make_feature(x, y, name="FPC Florence (minimum-security camp)", category=CAT,
    operator="Federal Bureau of Prisons", address="5880 Hwy 67 South", city="Florence",
    zip="81226", phone="719-784-9100", source="HIFLD Prison Boundaries; BOP FCI Florence page",
    source_url="https://www.bop.gov/locations/institutions/flf/",
    geocode="HIFLD Prison Boundaries footprint centroid"))

write_layer("Prisons.geojson", feats, problems)
