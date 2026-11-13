"""
Layer 4 - Substance Use Treatment and Mental Health Centers

PROVENANCE SUMMARY (full write-up: Data/sources/04_Treatment_and_Mental_Health.md)
  Source : SAMHSA FindTreatment.gov official export API (documented in the
           FindTreatment Developer Guide, Data/raw/findtreatment_developer_guide.pdf)
           https://findtreatment.gov/locator/exportsAsJson/v2
           limitType=0 (state search), limitValue=24 (Colorado's ID in the
           guide's State ID table), pageSize=2000.
  Raw    : Data/raw/findtreatment_CO_all.json (also _sa.json, _mh.json)
  Coords : supplied by SAMHSA; a random sample is re-geocoded with the Census
           geocoder as a check.
"""
import json, math, os, random
from common import fetch, geocode, make_feature, write_layer, RAW

CAT = "Substance Use Treatment and Mental Health"
API = ("https://findtreatment.gov/locator/exportsAsJson/v2?sAddr=%2239.7392,-104.9903%22"
       "&limitType=0&limitValue=24&pageSize=2000&page=1&sort=0")
TYPE_LABEL = {"SA": "Substance use treatment", "MH": "Mental health treatment",
              "OTP": "Opioid treatment program (methadone/buprenorphine)"}

rows = json.loads(fetch(API, "findtreatment_CO_all.json"))["rows"]
print("API rows:", len(rows))

# One facility can appear once per type (SA, MH, OTP) -> merge on name+address
merged = {}
for r in rows:
    if r["state"] != "CO":
        print("  dropped out-of-state record:", r["name1"], r["city"], r["state"])
        continue
    key = tuple((r.get(k) or "").strip().lower() for k in ("name1", "street1", "city"))
    m = merged.setdefault(key, {"r": r, "types": set(), "svc": {}})
    m["types"].add(r["typeFacility"])
    for s in (r.get("services") or []):
        m["svc"].setdefault(s["f1"], s["f3"])

def svc(m, code_names):
    """Pick a few readable service fields for the popup."""
    out = {}
    for name in code_names:
        if name in m["svc"]:
            out[name] = m["svc"][name]
    return out

feats, skipped = [], []
for m in merged.values():
    r = m["r"]
    gsrc = "source (SAMHSA)"
    if r.get("latitude") and r.get("longitude"):
        lon, lat = float(r["longitude"]), float(r["latitude"])
    else:
        street = (r.get("street1") or "").strip()
        if not street or street.upper().startswith(("P.O.", "PO BOX")):
            skipped.append(f"{r['name1']} ({r['city']}) - SAMHSA withholds street address")
            continue
        lon, lat, gsrc, _ = geocode(f"{street}, {r['city']}, CO {r['zip']}")
        if lon is None:
            skipped.append(f"{r['name1']} ({r['city']}) - could not geocode {street}")
            continue
    s = m["svc"]
    name = r["name1"] + (f" - {r['name2']}" if r.get("name2") else "")
    feats.append(make_feature(lon, lat, name=name, category=CAT,
        facility_types="; ".join(TYPE_LABEL[t] for t in sorted(m["types"])),
        address=(r.get("street1") or "") + (f", {r['street2']}" if r.get("street2") else ""),
        city=r["city"], zip=r["zip"], phone=r.get("phone") or r.get("intake1"),
        website=r.get("website") if r.get("website") not in ("http://", "") else None,
        services=s.get("Service Setting"), type_of_care=s.get("Type of Care"),
        payment_accepted=s.get("Payment/Insurance/Funding Accepted"),
        special_programs=s.get("Special Programs/Groups Offered"),
        source="SAMHSA FindTreatment.gov (official export API)", source_url=API,
        geocode=gsrc))

# --- Verification: re-geocode a random sample with the Census geocoder -------
random.seed(42)
sample = random.sample([f for f in feats if f['properties']['geocode'].startswith('source')], 30)
d_list = []
for f in sample:
    p = f["properties"]
    glon, glat, gm, _ = geocode(f"{p['address']}, {p['city']}, CO {p['zip']}")
    if glon is None or gm == "osm-nominatim":
        continue
    x, y = f["geometry"]["coordinates"]
    d = math.hypot((x-glon)*111.32*math.cos(math.radians(y)), (y-glat)*110.57)
    d_list.append((d, p["name"]))
d_list.sort()
print(f"\nCoordinate check: {len(d_list)} of 30 sampled addresses geocoded by Census")
print(f"  median distance SAMHSA vs Census: {d_list[len(d_list)//2][0]:.2f} km; max {d_list[-1][0]:.2f} km ({d_list[-1][1]})")
print(f"  within 0.5 km: {sum(d < 0.5 for d, _ in d_list)}/{len(d_list)}")

write_layer("Substance_Use_and_Mental_Health_Treatment.geojson", feats, skipped)
