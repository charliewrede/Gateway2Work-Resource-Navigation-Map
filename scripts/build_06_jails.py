"""
Layer 6 - Jails (county and municipal detention facilities)

PROVENANCE SUMMARY (full write-up: Data/sources/06_Jails.md)
  Base records : HIFLD Prison Boundaries, Colorado records with TYPE COUNTY or
                 LOCAL (Data/raw/hifld_prison_points_CO.geojson, built by
                 build_07_prisons.py).
  Which counties operate a jail : Colorado Division of Criminal Justice,
                 "Summary of County Jail Data Pursuant to HB 19-1297" (2020),
                 footnote 3 + Appendix C (Data/raw/dcj_2020_HB19-1297_jail_data_report.pdf),
                 updated with DCJ's current jail-data page list and local news on
                 closures since 2020 (Custer 2023, Rio Blanco 2021, Saguache,
                 Yuma) and the Archuleta jail opening (Nov 2020).
  Coordinates  : HIFLD footprint centroid, cross-checked with the Census
                 geocoder; new records geocoded with the Census geocoder.
"""
import json, math, os
from common import geocode, make_feature, write_layer, RAW, RETRIEVED

CAT = "Jails"
HIFLD_SRC = "HIFLD Prison Boundaries (DHS), via public ArcGIS mirror 'Prison_Points'"
HIFLD_URL = "https://services.arcgis.com/XG15cJAlne2vxtgt/ArcGIS/rest/services/Prison_Points/FeatureServer/0"
DCJ_URL = "https://cdpsdocs.state.co.us/ORS/Docs/Reports/2020_HB19-1297_Jail_Data_Rpt.pdf"

hifld = json.load(open(os.path.join(RAW, "hifld_prison_points_CO.geojson")))["features"]

# HIFLD records that are NOT jails, or no longer operate as jails ---------------
EXCLUDE = {
    # closed / county has no jail per DCJ (2020 report and current list)
    "ARCHULETA COUNTY JAIL": "old jail closed; replaced by new detention center (added below)",
    "MESA COUNTY ALTERNATIVE SENTENCING UNIT": "HIFLD status CLOSED",
    "LAKE COUNTY JAIL": "DCJ: Lake County does not operate a jail",
    "PHILLIPS COUNTY SHERIFF'S OFFICE": "DCJ: Phillips County does not operate a jail",
    "CUSTER COUNTY JAIL / SHERIFF": "closed permanently 2023-01-06 (KRDO/KOAA); inmates housed in Fremont County",
    "RIO BLANCO COUNTY DETENTION CENTER": "closed 2021; inmates housed in Moffat County (IGA renewed Sept 2025)",
    "SAGUACHE COUNTY JAIL": "closed; inmates held at Rio Grande County jail (Saguache Sheriff site, July 2024)",
    "YUMA COUNTY JAIL / SHERIFF": "closed permanently (staffing); arrestees taken to Logan County jail (Yuma Pioneer)",
    # not adult jails -> other layers
    "BOULDER COUNTY JUVENILE CENTER": "juvenile facility",
    "GARFIELD COUNTY COMMUNITY CORRECTIONS FACILITY": "community corrections (Layer 5)",
    "MESA COUNTY COMMUNITY CORRECTIONS - POWELL BUILDING": "community corrections (Layer 5)",
    "MESA COUNTY COMMUNITY CORRECTIONS - CHIPETA BUILDING": "community corrections (Layer 5)",
    "ROBERTS ROAD RESIDENTIAL FACILITY": "community corrections, ComCor (Layer 5)",
    "3808 RESIDENTIAL FACILITY": "community corrections (Layer 5)",
}

# Corrections to HIFLD names/addresses ------------------------------------------
FIX = {
    "EL PASO COUNTY METRO DETENTION FACILITY": {
        "name": "El Paso County Metro Work Release Facility",
        "note": "Former Metro Detention Facility building, now the Sheriff's work-release facility (Gazette; EPSO Detention Bureau page)"},
    "DOUGLAS COUNTY SHERIFFS OFFICE JAIL": {"address": "4000 Justice Way"},
    "GILPIN COUNTY JUSTICE CENTER": {"city": "Black Hawk"},
}

def km(a, b):
    return math.hypot((a[0]-b[0])*111.32*math.cos(math.radians(a[1])), (a[1]-b[1])*110.57)

feats, problems, excluded = [], [], []
for f in hifld:
    p = f["properties"]
    if p["TYPE"] not in ("COUNTY", "LOCAL"):
        continue
    if p["NAME"] in EXCLUDE:
        excluded.append(f"{p['NAME']}: {EXCLUDE[p['NAME']]}")
        continue
    if p["STATUS"] != "OPEN":
        excluded.append(f"{p['NAME']}: HIFLD status {p['STATUS']}")
        continue
    fx = FIX.get(p["NAME"], {})
    name = fx.get("name", p["NAME"].title().replace("'S", "'s").replace(" / Sheriff", ""))
    addr = fx.get("address", p["ADDRESS"].title())
    city = fx.get("city", p["CITY"].title())
    x, y = f["geometry"]["coordinates"]
    glon, glat, gm, _ = geocode(f"{addr}, {city}, CO {p['ZIP']}")
    check = None
    if glon is not None:
        d = km((x, y), (glon, glat))
        check = f"HIFLD point {d:.1f} km from Census geocode of address"
        if d > 2:
            problems.append(f"{name}: HIFLD vs Census differ {d:.1f} km")
    feats.append(make_feature(x, y, name=name, category=CAT,
        operator=("Municipal" if p["TYPE"] == "LOCAL" else "County Sheriff"),
        address=addr, city=city, zip=p["ZIP"], county=p["COUNTY"].title(),
        phone=None if p["TELEPHONE"] == "NOT AVAILABLE" else p["TELEPHONE"],
        capacity=p["CAPACITY"] if p["CAPACITY"] and p["CAPACITY"] > 0 else None,
        source=HIFLD_SRC + "; operating status checked against DCJ jail-data county list",
        source_url=HIFLD_URL, geocode="HIFLD Prison Boundaries footprint centroid",
        verified=check, status_note=fx.get("note"),
        hifld_source_date="2015-2018 (phone/capacity may be outdated)"))

# Jails missing from HIFLD ------------------------------------------------------
ADD = [
 dict(name="Archuleta County Detention Center", address="125 Harman Park Drive", city="Pagosa Springs",
      zip="81147", county="Archuleta",
      source="Pagosa Springs SUN, 'Archuleta County jail now operating' (2020-11-25); address from county jail-site resolution (Pagosa SUN)",
      source_url="https://www.pagosasun.com/stories/archuleta-county-jail-now-operating,14769"),
 dict(name="Bent County Jail (Sheriff's Office)", address="11100 County Road GG.5", city="Las Animas",
      zip="81054", county="Bent", phone="719-456-1363",
      source="Bent County Sheriff's Office official site (contact page); DCJ 2020 report Appendix C lists Bent as reporting jail",
      source_url="https://bentsheriff.gov/contact-us/"),
 dict(name="Jackson County Jail (Sheriff's Office)", address="396 Lafever Street", city="Walden",
      zip="80480", county="Jackson", phone="970-723-4242",
      source="Jackson County official site, Sheriff - Jail page; DCJ 2020 report Appendix C lists Jackson as reporting jail",
      source_url="https://jacksoncounty.colorado.gov/sheriff-jail"),
]
for r in ADD:
    lon, lat, gm, matched = geocode(f"{r['address']}, {r['city']}, CO {r['zip']}")
    if lon is None:
        problems.append(f"UNMATCHED (needs manual coordinates): {r['name']} | {r['address']}, {r['city']}")
        continue
    feats.append(make_feature(lon, lat, category=CAT, operator="County Sheriff", geocode=gm, **r))

write_layer("Jails.geojson", feats, problems)
print("\nExcluded HIFLD records:")
for e in excluded:
    print("  -", e)
print("\nCounties with a jail:", len({f['properties'].get('county') for f in feats}))
