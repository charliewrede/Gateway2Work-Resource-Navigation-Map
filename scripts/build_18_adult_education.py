"""
Layer 18 - Adult Education and GED Programs

PROVENANCE SUMMARY (full write-up: Data/sources/18_Adult_Education.md)
  Source : Colorado Department of Education, Adult Education Initiatives,
           official "Find a Program" Google My Map linked from
           https://ed.cde.state.co.us/cdeadult/grantees/grantees-current-grantees
           KML export: https://www.google.com/maps/d/kml?mid=1YCoTGtwGf6FmQ_Ruzj32FwtXwxNunlI&forcekml=1
           Raw: Data/raw/cde_adulted_sites.kml
           Folder used: "Program Locations" (current AEFLA/AELA-funded sites).
  Coords : the KML stores addresses only -> Census geocoder (OSM fallback).
"""
import re, xml.etree.ElementTree as ET, os
from common import fetch, geocode, make_feature, write_layer, in_colorado, RAW

CAT = "Adult Education and GED Programs"
KML = "https://www.google.com/maps/d/kml?mid=1YCoTGtwGf6FmQ_Ruzj32FwtXwxNunlI&forcekml=1"
PAGE = "https://ed.cde.state.co.us/cdeadult/grantees/grantees-current-grantees"
fetch(KML, "cde_adulted_sites.kml")
ns = {"k": "http://www.opengis.net/kml/2.2"}
root = ET.parse(os.path.join(RAW, "cde_adulted_sites.kml")).getroot()

feats, probs = [], []
for fo in root.iter("{http://www.opengis.net/kml/2.2}Folder"):
    if fo.find("k:name", ns).text != "Program Locations":
        continue
    for p in fo.findall("k:Placemark", ns):
        data = {d.get("name"): (d.find("k:value", ns).text or "").strip()
                for d in p.findall(".//k:Data", ns)}
        program = p.find("k:name", ns).text.strip()
        addr = (p.find("k:address", ns).text or data.get("Address", "")).strip()
        # Typos in CDE's map, corrected (documented in 18_Adult_Education.md)
        for bad, good in (("Caminio del Rio", "Camino del Rio"), ("E Illif Avenue", "E Iliff Avenue")):
            addr = addr.replace(bad, good)
        # drop "Suite 110" / "Unit C" / "Room 5" for the lookup only
        lookup = re.sub(r",?\s+(?:Suite|Ste\.?|Unit|#|Room)\s*[\w-]+", "", addr, flags=re.I)
        lon, lat, gm, _ = geocode(lookup)
        if not in_colorado(lon, lat):
            probs.append(f"UNMATCHED: {program} | {addr}"); continue
        site = data.get("Site Name") or program
        feats.append(make_feature(lon, lat,
            name=f"{program} - {site}" if site and site != program else program,
            category=CAT, program=program, site_name=site, address=addr,
            county=data.get("County/Counties"), phone=data.get("Phone Number"),
            website=data.get("Website"), services=data.get("Services Available") or "Adult basic/secondary education, ESL, HSE (GED/HiSET) prep",
            source="Colorado Department of Education, Adult Education Initiatives 'Find a Program' map",
            source_url=PAGE, geocode=gm))
# Current grantees on CDE's grantee page with no site on CDE's map - added:
from common import geocoded_feature
ADD = [
 dict(name="Asian Pacific Development Center (adult education, now via Aurora Mental Health & Recovery)",
      address="1537 Alton Street", city="Aurora", zip="80010", phone="303-923-6320",
      source="CDE 2024-28 AEFLA grantee list; address from Aurora Mental Health & Recovery program page",
      source_url="https://auroramhr.org/?p=17271"),
 dict(name="Community Educational Outreach", address="7251 E 49th Avenue", city="Commerce City", zip="80022",
      phone="303-921-8600", source="CDE 2024-28 AEFLA grantee list; address from CDE adult ed program directory (2015)",
      source_url="https://www.cde.state.co.us/sites/default/files/docs/cdeadult/CO%20Adult%20Ed%20Programs_9%2025%2015%20(2).pdf",
      status_note="Address from a 2015 CDE directory; confirm."),
 dict(name="Larimer County Economic & Workforce Development (adult education)", address="200 W Oak Street, Suite 5000",
      city="Fort Collins", zip="80521", phone="970-498-6600",
      source="CDE 2025-29 AELA grantee list; address from larimer.gov/ewd", source_url="https://www.larimer.gov/ewd"),
]
for r in ADD:
    note = r.pop("status_note", None)
    f, p = geocoded_feature(r, CAT, r["source"], r["source_url"])
    if p: probs.append(p); continue
    if note: f["properties"]["status_note"] = note
    feats.append(f)
write_layer("Adult_Education_and_GED_Programs.geojson", feats, probs)
