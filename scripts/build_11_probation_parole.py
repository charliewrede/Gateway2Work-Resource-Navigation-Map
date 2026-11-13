"""
Layer 11 - Probation and Parole Offices

PROVENANCE SUMMARY (full write-up: Data/sources/11_Probation_and_Parole.md)
  Probation : Colorado Judicial Branch probation location page for each of the
              64 counties (coloradojudicial.gov), downloaded 2026-11-13 to
              Data/raw/judicial/*.html; list of URLs in Data/raw/judicial/found.json.
              Address parsed from each page's "Address ... CO 8xxxx" block.
  Parole    : CDOC Division of Adult Parole - 19 offices (cdoc.colorado.gov
              parole-offices page, Dec 2025; page blocks automated access, office
              cities taken from search-engine copy). Street addresses only where
              an independent listing gave one; otherwise city-level (flagged).
  Coords    : Census geocoder (OpenStreetMap fallback).
"""
import glob, html, json, os, re
from common import geocoded_feature, geocode, make_feature, write_layer, RAW

CAT = "Probation and Parole Offices"
JD = os.path.join(RAW, "judicial")
found = json.load(open(os.path.join(JD, "found.json")))

def page_for(county):
    for fn in glob.glob(os.path.join(JD, "*.html")):
        b = os.path.basename(fn)
        if b.startswith(county + "-"):
            return fn

feats, probs, seen, no_office = [], [], {}, []
for county, url in sorted(found.items()):
    fn = page_for(county)
    t = open(fn, encoding="utf-8", errors="ignore").read()
    # Pages use structured address markup (Drupal address field):
    #   <span class="address-line1">, <span class="locality">, <span class="postal-code">
    def field(cls):
        m = re.search(r'class="[^"]*\b' + cls + r'\b[^"]*"[^>]*>([^<]*)', t)
        return html.unescape(m.group(1)).strip() if m else ""
    street, city, z = field("address-line1"), field("locality"), field("postal-code")
    line2 = field("address-line2")
    tm = re.search(r"<title>([^<|]+)", t)
    title = html.unescape(tm.group(1)).strip() if tm else county.title() + " Probation"
    if not (street and city):
        no_office.append(county)
        continue
    if line2 and not street[0].isdigit() and line2[0].isdigit():
        street, line2 = line2, street            # line1 was a building name
    if line2 and not re.match(r"P\.?\s?O\.?\s*Box", line2, re.I):
        street = f"{street}, {line2}"
    if city == "Las Amimas":                     # typo on the Judicial page
        city = "Las Animas"
    key = (street.lower(), city.lower())
    cname = county.replace("-", " ").title()
    if key in seen:                       # several counties share one office
        seen[key]["properties"]["counties_served"] += ", " + cname
        continue
    rec = dict(name=title, address=street, city=city, zip=z, county=cname)
    f, p = geocoded_feature(rec, CAT, "Colorado Judicial Branch, county probation location page", url)
    if p: probs.append(p); continue
    f["properties"].update(office_type="Probation (Colorado Judicial Branch)", counties_served=cname)
    seen[key] = f
    feats.append(f)
# Denver: county page lists phone numbers only; address from the Judicial
# Branch "Denver Adult Probation" location listing (via search; site later
# rate-limited this session) - 303 W. Colfax Ave., 5th Floor.
f, p = geocoded_feature(dict(name="Denver Adult Probation", address="303 W Colfax Avenue, 5th Floor", city="Denver",
                             zip="80204", county="Denver", phone="303-607-7104"), CAT,
                        "Colorado Judicial Branch, Denver Adult Probation location listing",
                        "https://www.coloradojudicial.gov/location/denver-adult-probation")
if not p:
    f["properties"].update(office_type="Probation (Colorado Judicial Branch)", counties_served="Denver (district court); Denver County Court probation: 720-913-8300")
    feats.append(f)
# Counties whose page names the district office that serves them
SERVED = {"baca": "Prowers", "cheyenne": "Prowers", "kiowa": "Prowers",
          "hinsdale": "Montrose", "ouray": "Montrose"}
for c, host in SERVED.items():
    for f in feats:
        if f["properties"].get("county") == host:
            f["properties"]["counties_served"] += ", " + c.title()
print("probation offices:", len(feats))
print("counties with no office page address:", no_office)

# ---- CDOC Adult Parole -------------------------------------------------------
PAROLE_URL = "https://cdoc.colorado.gov/parole-and-re-entry-services/general-information/parole-offices"
# Parole office cities + coverage counties: WAGEES "Adult Parole Locations" page
# (wageesco.org/find-by-location, (c) 2025 Latino Coalition for Community
# Leadership, CDOC's WAGEES intermediary). 18 locations; CDOC says 19 offices
# (Denver has headquarters + field office). Street addresses only where an
# independent listing provides one.
WAGEES_URL = "https://wageesco.org/find-by-location/"
STREET = {
 "Denver": ("940 Broadway", "80203", "CDOC parole offices page (Adult Parole Headquarters, 303-763-2420)"),
 "Colorado Springs": ("888 Garden of the Gods Road", "80907", "Waze/MapQuest listings 'Adult Parole Supervision Division'"),
 "Fort Collins": ("3000 S College Avenue", "80525", "MapQuest listing 'Adult Parole Division'"),
 "Aurora": ("14100 E Exposition Avenue", "80012", "third-party reentry directory (possibly dated)"),
}
COVER = {
 "Alamosa": "Alamosa, Conejos, Costilla, Mineral, Rio Grande, Saguache", "Aurora": "Aurora",
 "Canon City": "Fremont area", "Colorado Springs": "El Paso area", "Craig": "Eagle, Moffat, Rio Blanco, Routt",
 "Denver": "Denver", "Durango": "Archuleta, Dolores, La Plata, Montezuma, San Juan",
 "Englewood": "Arapahoe, Douglas, Elbert, south Jefferson", "Fort Collins": "Larimer, Jackson",
 "Grand Junction": "Delta, Garfield, Gunnison, Hinsdale, Mesa, Montrose, Ouray, Pitkin, San Miguel",
 "Greeley": "Northern and eastern Weld", "La Junta": "Baca, Bent, Cheyenne, Crowley, Huerfano, Kiowa, Kit Carson, Las Animas, Lincoln, Otero, Prowers",
 "Longmont": "Boulder, southern Weld", "Montrose": "Montrose area", "Pueblo": "Pueblo area",
 "Rifle": "Eagle, Garfield", "Sterling": "Morgan, Logan, Sedgwick, Phillips, Washington, Yuma",
 "Westminster": "Adams, Broomfield, Clear Creek, Gilpin, Grand, north Jefferson, Summit",
}
for city, cover in COVER.items():
    name = f"{city} Parole Office (CDOC Division of Adult Parole)"
    if city in STREET:
        street, z, ssrc = STREET[city]
        f, p = geocoded_feature(dict(name=name, address=street, city=city, zip=z), CAT,
                                "WAGEES Adult Parole Locations list; street address: " + ssrc, WAGEES_URL)
        if p: probs.append(p); continue
    else:
        ssrc = None
        lon, lat, gm, _ = geocode(f"{city}, Colorado")
        f = make_feature(lon, lat, name=name, category=CAT, city=city,
                         source="WAGEES Adult Parole Locations list (office city only)", source_url=WAGEES_URL,
                         geocode="APPROXIMATE - city center (street address not available)")
    f["properties"]["office_type"] = "Parole (CDOC Division of Adult Parole)"
    f["properties"]["counties_served"] = cover
    if not ssrc or "dated" in ssrc:
        f["properties"]["status_note"] = "Street address not confirmed; parole 24-hr line 1-800-426-9143."
    feats.append(f)

write_layer("Probation_and_Parole_Offices.geojson", feats, probs)
