"""
Layer 1  - Recovery-Friendly Employers (RFE)
Layer 13 - Recovery Community Organizations (RCOs)
Layer 15 - Homelessness and Housing Service Providers

PROVENANCE SUMMARY (write-ups: Data/sources/01_Recovery_Friendly_Employers.md,
                    13_Recovery_Community_Organizations.md, 15_Homelessness.md)
  L1  : Colorado Recovery Friendly Workplace Initiative (created by state law
        SB24-048, administered by CU Anschutz CHWE) - participating companies,
        published Google Sheet that feeds corecoveryfriendlyworkplace.org/participating-colorado-companies/
        Raw: Data/raw/rfwi_participating_companies.csv
  L13 : organizations named consistently by Faces & Voices of Recovery (ARCO map),
        CAPRSS accreditation list and CARS directory; addresses from own sites.
  L15 : regional anchor shelter/housing providers; addresses from own sites.
"""
import csv, os, re
from common import fetch, geocoded_feature, write_layer, RAW

# ---------------------------------------------------------------- Layer 1
RFW_CSV = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vSlU67lHAkf7HUxQsAq3IS-Ev5GfEaiDM5MXbE3eqR4VpaprF0nYHukGGy6PjusUIzuJeXsgIYzWioD/pub?output=csv")
RFW_PAGE = "https://corecoveryfriendlyworkplace.org/participating-colorado-companies/"
fetch(RFW_CSV, "rfwi_participating_companies.csv")
rows = list(csv.DictReader(open(os.path.join(RAW, "rfwi_participating_companies.csv"), encoding="utf-8-sig")))

# Manual decisions by project staff (2026-11-17) for roster rows that could not
# be geocoded. "place" = how the point is located:
#   ("address", street)      geocode a corrected street address
#   ("zip", zip)             no physical location: point at the ZIP code's center
#   ("city", city)           no physical location: point at the town center
#   ("skip", reason)         not mapped
OVERRIDES = {
 "Absolute Caulking and Waterproofing Inc.": dict(place=("address", "11919 W I-70 Frontage Rd N"), display="11919 W Interstate 70 Frontage Rd N", city="Wheat Ridge", zip="80033",
     note="Address verified by project staff 2026-11-17 (roster listed '11919 I-70 Frontage Rd. N. #112'); geocoded as '11919 W I-70 Frontage Rd N' (OSM exact house-number match)."),
 "Recovery Friendly Leader": dict(place=("zip", "80218"), address="PO Box 18770", city="Denver", zip="80218",
     note="PO BOX ONLY - no physical location (verified by project staff 2026-11-17). Point placed at the center of ZIP 80218."),
 "Summit County Chamber of Commerce": dict(place=("city", "Frisco"), address="PO Box 461", city="Frisco", zip="80443",
     note="No physical location; mailing address is PO Box 461 (project staff 2026-11-17). Point placed at Frisco town center."),
 "Hargrove and Kidd Construction Co": dict(place=("city", "Crested Butte"), address="No physical location", city="Crested Butte", zip="81224",
     note="No physical location (project staff 2026-11-17); roster listed 14 Thomas Ct. Point placed at Crested Butte town center."),
 "Growing Our Mindset, LLC Dba Arntt Synergy Consulting": dict(place=("skip", "could not be found or confirmed online (project staff 2026-11-17)")),
 "South Pole Bar": dict(place=("skip", "not confirmed (project staff 2026-11-17); roster has no street address")),
}

def zip_center(z):
    """Center of a ZIP code from OpenStreetMap Nominatim (structured postal-code search)."""
    import time, urllib.parse
    from common import fetch_json, set_manual, _load_cache
    key = f"ZIP {z}, Colorado"
    cached = _load_cache().get(key.upper())
    if cached:
        return cached["lon"], cached["lat"]
    time.sleep(1.1)
    res = fetch_json("https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"postalcode": z, "country": "USA", "format": "json", "limit": 1}))
    lon, lat = round(float(res[0]["lon"]), 6), round(float(res[0]["lat"]), 6)
    set_manual(key, lon, lat, f"center of ZIP {z} (OSM)")
    return lon, lat

from common import geocode, make_feature
feats, probs = [], []
for r in rows:
    name = r["Business Name"].strip()
    clean0 = re.sub(r"\s*\(✪\s*CERTIFIED\)", "", name).strip()
    if clean0 in OVERRIDES:
        o = OVERRIDES[clean0]
        kind, val = o["place"]
        if kind == "skip":
            probs.append(f"not mapped by decision: {clean0} - {val}"); continue
        if kind == "address":
            f, p = geocoded_feature(dict(name=clean0, address=val, city=o["city"], zip=o["zip"],
                                         website=r.get("Website") or None),
                                    "Recovery-Friendly Employers",
                                    "Colorado Recovery Friendly Workplace Initiative - participating companies list", RFW_PAGE)
            if p: probs.append(p); continue
            if o.get("display"):
                f["properties"]["address"] = o["display"]
        else:
            if kind == "zip":
                lon, lat = zip_center(val); gm = f"APPROXIMATE - center of ZIP {val} (PO Box, no physical location)"
            else:
                lon, lat, _, _ = geocode(f"{val}, Colorado"); gm = "APPROXIMATE - town center (no physical location)"
            f = make_feature(lon, lat, name=clean0, category="Recovery-Friendly Employers", address=o["address"],
                             city=o["city"], zip=o["zip"], website=r.get("Website") or None,
                             source="Colorado Recovery Friendly Workplace Initiative - participating companies list",
                             source_url=RFW_PAGE, geocode=gm)
        f["properties"]["rfw_status"] = "Certified Recovery Friendly Workplace" if "CERTIFIED" in name else "Participating (pledged)"
        f["properties"]["location_note"] = o["note"]
        if kind == "zip":
            f["properties"]["po_box_only"] = "Yes"
        feats.append(f)
        continue
    if not name or not r.get("Street Address", "").strip():
        probs.append(f"no street address: {name}"); continue
    if r["City"].strip().lower().startswith("unit") and r["Zip Code"].strip() == "80701":
        # sheet row has the unit in the City column; ZIP 80701 = Fort Morgan
        r["Street Address"] = r["Street Address"].strip() + ", " + r["City"].strip()
        r["City"] = "Fort Morgan"
    if r["City"].strip() == "Denver" and r["Zip Code"].strip() == "80401":
        r["City"] = "Golden"               # sheet says Denver but ZIP 80401 is Golden (18475 W Colfax)
    certified = "CERTIFIED" in name
    clean = re.sub(r"\s*\(✪\s*CERTIFIED\)", "", name).strip()
    f, p = geocoded_feature(dict(name=clean, address=r["Street Address"].strip(), city=r["City"].strip(),
                                 zip=r["Zip Code"].strip(), website=r.get("Website") or None),
                            "Recovery-Friendly Employers",
                            "Colorado Recovery Friendly Workplace Initiative - participating companies list", RFW_PAGE)
    if p: probs.append(p); continue
    f["properties"]["rfw_status"] = "Certified Recovery Friendly Workplace" if certified else "Participating (pledged)"
    feats.append(f)
write_layer("Recovery_Friendly_Employers.geojson", feats, probs)

# ---------------------------------------------------------------- Layer 13
RCO = [
 ("Advocates for Recovery Colorado (headquarters)", "3440 W 71st Place", "Westminster", "80030", "https://advocatesforrecovery.org/",
  "Peer-run RCO; peer & family recovery support (BHA-licensed per CARS); RFW certified", "https://advocatesforrecovery.org/"),
 ("Advocates for Recovery Colorado - Aurora hub", "1445 Dayton Street", "Aurora", "80010", "https://advocatesforrecovery.org/",
  "Peer recovery support hub", "https://advocatesforrecovery.org/"),
 ("Serenity Recovery Connection", "985 W Fillmore Street", "Colorado Springs", "80907", "https://www.coloradogives.org/organization/Serenityrecoveryconnection",
  "Peer-led RCO (CAPRSS accredited; ARCO member); RFW certified", "https://caprss.org/accredited-organizations/"),
 ("Free Recovery Community (Free Cafe)", "2122 S Lafayette Street", "Denver", "80210", "https://freerecoverycommunity.org/",
  "Peer recovery community center", "https://freerecoverycommunity.org/"),
]
feats, probs = [], []
for name, a, city, z, web, svc, src in RCO:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, website=web, services=svc),
                            "Recovery Community Organizations", "Organization website; ARCO / CAPRSS / CARS directories", src)
    if p: probs.append(p); continue
    feats.append(f)
write_layer("Recovery_Community_Organizations.geojson", feats, probs)

# ---------------------------------------------------------------- Layer 15
H = [
 ("Denver Rescue Mission (headquarters)", "6100 Smith Road", "Denver", "80216", "https://denverrescuemission.org/", "Emergency shelter, recovery & workforce programs", "provider website"),
 ("Colorado Coalition for the Homeless", "2111 Champa Street", "Denver", "80205", "https://www.coloradocoalition.org/", "Supportive housing, health care, housing navigation", "provider website"),
 ("Catholic Charities of Denver (shelter services, HQ)", "6240 Smith Road", "Denver", "80216", "https://ccdenver.org/", "Samaritan House and other shelters", "provider website"),
 ("Springs Rescue Mission", "5 W Las Vegas Street", "Colorado Springs", "80903", "https://springsrescuemission.org/", "Emergency shelter, recovery, workforce development", "provider website"),
 ("Boulder Shelter for the Homeless", "4869 Broadway", "Boulder", "80304", "https://www.bouldershelter.org/", "Shelter and housing-focused case management", "provider website"),
 ("Fort Collins Rescue Mission", "316 Jefferson Street", "Fort Collins", "80524", "https://denverrescuemission.org/", "Emergency shelter (Denver Rescue Mission affiliate)", "provider website"),
 ("Homeward Alliance (Murphy Center)", "242 Conifer Street", "Fort Collins", "80524", "https://www.homewardalliance.org/", "Day center, housing navigation, reentry (WAGEES)", "WAGEES partner page"),
 ("Pueblo Rescue Mission", "728 W 4th Street", "Pueblo", "81003", None, "Emergency shelter", "third-party directory (shelterlist.com) - confirm"),
]
feats, probs = [], []
for name, a, city, z, web, svc, asrc in H:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, website=web, services=svc),
                            "Homelessness and Housing Service Providers", f"Address source: {asrc}", web or "https://www.shelterlist.com/state/colorado")
    if p: probs.append(p); continue
    if "confirm" in asrc: f["properties"]["status_note"] = "Address from third-party directory only; confirm."
    feats.append(f)
write_layer("Homelessness_and_Housing_Services.geojson", feats, probs)
