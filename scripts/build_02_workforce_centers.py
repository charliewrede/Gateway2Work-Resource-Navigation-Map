"""
Layer 2 - Workforce Centers (Colorado Workforce Centers = American Job Centers)

PROVENANCE SUMMARY (full write-up: Data/sources/02_Workforce_Centers.md)
  Source : Colorado Department of Labor and Employment (CDLE), official
           workforce center contact list, https://cdle.colorado.gov/jobs-training/workforce-centers
           cdle.colorado.gov blocks automated tools (HTTP 403), so project
           staff copied the list from the page on 2026-11-24. The copy is saved
           unchanged as Data/raw/cdle_workforce_centers_2026-11-24.txt and
           this script parses it. Every center on that list is mapped and no
           others. (Before 2026-11-24 the layer was built from the May 2022
           federal AJC list plus local pages; see git history.)
  Coords : U.S. Census geocoder (OpenStreetMap fallback).

To update: copy the CDLE page into a new Data/raw/cdle_workforce_centers_<date>.txt
and change RAW_FILE below.
"""
import os, re
from common import RAW, geocoded_feature, write_layer

CAT = "Workforce Centers"
RAW_FILE = os.path.join(RAW, "cdle_workforce_centers_2026-11-24.txt")
SRC = "Colorado Department of Labor and Employment (CDLE), Workforce Centers contact list"
URL = "https://cdle.colorado.gov/jobs-training/workforce-centers"
VERIFIED = "Official CDLE list, copied from the CDLE page by project staff 2026-11-24"

# The CDLE list names each center's website but the copied text has no links.
# These URLs are each local area's own page (used as sources earlier in this
# project); they were NOT part of the copied list.
WEBSITES = {
    "Adams County": "https://adcogov.org/workforce-business-center",
    "Arapahoe/Douglas": "https://www.adworks.org/",
    "Broomfield": "https://broomfield.org/3818/Workforce-Center",
    "Denver": "https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Economic-Development-Opportunity/Jobseekers-Employers/For-Jobseekers",
    "Weld County": "https://www.weld.gov/Government/Departments/Human-Services/Employment-Services",
    "Jefferson County (Tri-County)": "https://www.jeffco.us/Directory.aspx?did=68",
    "Larimer County": "https://www.larimer.gov/ewd",
    "Mesa County": "https://www.mesacounty.us/departments-and-services/wfc/contact-information",
    "Pikes Peak (El Paso, Teller)": None,
    "Boulder County": "https://bouldercounty.gov/families/work/",
    "Rural Consortium (Workforce Colorado Rural Alliance)": "https://wcra.colorado.gov/",
}
# website label on the CDLE list -> local workforce area
AREA_BY_LABEL = [
    ("Adams County", "Adams County"), ("Arapahoe/Douglas", "Arapahoe/Douglas"),
    ("Broomfield", "Broomfield"), ("Denver", "Denver"), ("Weld County", "Weld County"),
    ("Jefferson County", "Jefferson County (Tri-County)"), ("Larimer County", "Larimer County"),
    ("Mesa County", "Mesa County"), ("Pikes Peak", "Pikes Peak (El Paso, Teller)"),
    ("Woodland Park", "Pikes Peak (El Paso, Teller)"), ("Boulder County", "Boulder County"),
    ("Rural Alliance", "Rural Consortium (Workforce Colorado Rural Alliance)"),
    ("Fort Morgan", "Rural Consortium (Workforce Colorado Rural Alliance)"),
]
# Fixes to the copied text, each noted on the feature (corrections_note).
FIXES = {
    "Denver Workforce at Montebello": dict(
        name="Denver Workforce at Montbello",
        note="Name spelled 'Montebello' on the CDLE list; the neighborhood is Montbello."),
    "Montrose Workforce Center": dict(
        hours_fix=("8:00 PM - 12:00 PM", "8:00 AM - 12:00 PM"),
        note="CDLE list says '8:00 PM - 12:00 PM'; shown as 8:00 AM (typo)."),
    "Woodland Park Office in Community Partnership Family Resource Center": dict(
        city="Woodland Park",
        note="CDLE list gives the city as 'South Woodland Park'; the mailing city is Woodland Park."),
    "Larimer County Economic & Workforce Development - Fort Collins": dict(
        geocode_zip="80521",
        note="CDLE list gives ZIP 80522 (a PO-box ZIP); the building is in 80521, used for locating it."),
}

CITY_LINE = re.compile(r"^(?:(\d.*\.)\s+)?([A-Za-zñÑ ]+),\s*CO\s+(\d{5})$")   # optional "1333 Iris Ave." before the city
LABEL = re.compile(r"^(Phone Number|Phone|Fax Number|Fax|TDD|E-mail|Email|Office ID|Job Hotline|Hours|Note)\s*:\s*(.*)$", re.I)
DAY = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Closed|1st)", re.I)
POBOX = re.compile(r"^P\.?\s*O\.?\s*Box", re.I)


def clean(s):
    s = s.replace("(opens in new window)", "").replace("–", "-")
    return re.sub(r"\s+", " ", s).strip()


def phone(s):
    d = re.sub(r"\D", "", s.split("Ext")[0])
    ext = re.search(r"Ext\.?\s*(\d+)", s, re.I)
    p = f"{d[0:3]}-{d[3:6]}-{d[6:10]}" if len(d) == 10 else clean(s)
    return p + (f" ext. {ext.group(1)}" if ext else "")


def parse(block):
    lines = [clean(l) for l in block.splitlines() if clean(l)]
    r = dict(name=lines[0], street=[], building=[], mailing=[], hours=[])
    section = ""
    seen_city = False
    for l in lines[1:]:
        m = LABEL.match(l)
        if l.lower().startswith("serving"):
            r["area_served"] = l.split(":", 1)[-1].replace("Serving", "").strip()
        elif l.rstrip(":").lower() in ("business services", "employers"):
            section = "employer_"
        elif m:
            key, val = m.group(1).lower(), m.group(2).strip()
            if key.startswith("phone"):
                r[section + "phone"] = phone(val)
            elif key.startswith("fax"):
                r[section + "fax"] = phone(val)
            elif key == "tdd":
                r["tdd"] = phone(val)
            elif key in ("e-mail", "email"):
                r["email"] = val
            elif key == "office id":
                r["office_id"] = val
            elif key == "job hotline":
                r["job_hotline"] = phone(val)
            elif key == "hours":
                r["hours"].append(val)
            elif key == "note":
                r["note"] = val
        elif POBOX.match(l):
            r["mailing"].append(re.sub(r"^P\.?\s*O\.?\s*Box:?", "PO Box", l, flags=re.I))
        elif CITY_LINE.match(l):
            pre, city, zip_ = CITY_LINE.match(l).groups()
            if seen_city:                       # second city line = mailing address city
                r["mailing"].append(l)
                continue
            if pre:                             # "1333 Iris Ave. Boulder, CO 80304"
                r["street"].append(pre)
            r["city"], r["zip"], seen_city = city.strip(), zip_, True
        elif l.lower().endswith("website"):
            r.setdefault("website_label", l)
        elif DAY.match(l):
            r["hours"].append(l)
        elif not seen_city:
            # street lines: building names have no house number
            parts = [p.strip() for p in l.split(",")]
            if not re.match(r"^\d", parts[0]) and len(parts) > 1 and re.match(r"^\d", parts[1]):
                r["building"].append(parts[0]); r["street"].append(", ".join(parts[1:]))
            elif re.match(r"^\d", l):
                r["street"].append(l)
            else:
                r["building"].append(l)
        else:
            raise ValueError(f"Unrecognized line in '{r['name']}': {l}")
    return r


blocks = [b for b in re.split(r"\n\s*\n", open(RAW_FILE, encoding="utf-8").read()) if b.strip()]
feats, problems = [], []
for b in blocks:
    r = parse(b)
    official_name = r["name"]
    fix = FIXES.get(official_name, {})
    label = r.get("website_label", "")
    area = next((a for k, a in AREA_BY_LABEL if k.lower() in label.lower()), None)
    if not area:
        problems.append(f"NO LOCAL AREA for {official_name} (website label '{label}')")
    hours = "; ".join(r["hours"])
    if "hours_fix" in fix:
        hours = hours.replace(*fix["hours_fix"])
    rec = dict(name=fix.get("name", official_name),
               address=", ".join(r["street"]) or None,
               city=fix.get("city", r.get("city")), zip=r.get("zip"),
               phone=r.get("phone"), website=WEBSITES.get(area), verified=VERIFIED)
    geo = dict(rec, zip=fix.get("geocode_zip", rec["zip"]))
    f, prob = geocoded_feature(geo, CAT, SRC, URL)
    if prob:
        problems.append(prob); continue
    p = f["properties"]
    p["zip"] = rec["zip"]                         # show the ZIP as CDLE lists it
    extra = dict(building=", ".join(r["building"]) or None,
                 mailing_address=", ".join(r["mailing"]) or None,
                 email=r.get("email"), fax=r.get("fax"), tdd=r.get("tdd"),
                 employer_phone=r.get("employer_phone"), employer_fax=r.get("employer_fax"),
                 job_hotline=r.get("job_hotline"), hours=hours or None,
                 appointment_note=r.get("note"), area_served=r.get("area_served"),
                 local_area=area, office_id=r.get("office_id"),
                 cdle_name=official_name if fix.get("name") else None,
                 corrections_note=fix.get("note"))
    p.update({k: v for k, v in extra.items() if v})
    feats.append(f)

print(f"Parsed {len(blocks)} centers from {os.path.basename(RAW_FILE)}")
write_layer("Workforce_Centers.geojson", feats, problems)
