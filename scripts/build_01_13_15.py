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
feats, probs = [], []
for r in rows:
    name = r["Business Name"].strip()
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
