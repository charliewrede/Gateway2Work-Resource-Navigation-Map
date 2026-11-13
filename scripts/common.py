"""
common.py - shared helpers for building the Gateway2Work GeoJSON layers.

Every build script in this folder imports this file. It only uses Python's
built-in modules, so nothing has to be installed.

What lives here:
  fetch()          download a URL (and save a raw copy in Data/raw/)
  geocode()        turn a street address into longitude/latitude using the
                   free U.S. Census Bureau geocoder. Every answer is cached in
                   scripts/cache/geocode_cache.json so re-running a script
                   gives the same coordinates and doesn't re-query the web.
  make_feature()   build one GeoJSON point with the standard properties
  write_layer()    save a FeatureCollection to Data/ and print a summary

Standard properties on every point (so popups look the same in every layer):
  name, category, address, city, zip, county, phone, website, services,
  source           - who published the record (e.g. "SAMHSA FindTreatment.gov")
  source_url       - the exact page or dataset the record came from
  retrieved        - date the record was collected (YYYY-MM-DD)
  geocode          - how the coordinates were obtained:
                       "source"         coordinates supplied by the dataset
                       "census-rooftop" Census geocoder, exact address match
                       "census-nonexact" Census geocoder, approximate match
                       "manual"         looked up by hand (see the provenance file)
  verified         - optional note on any cross-check performed
"""

import json
import os
import re
import ssl
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "Data")
RAW = os.path.join(DATA, "raw")
CACHE_DIR = os.path.join(ROOT, "scripts", "cache")
GEOCODE_CACHE = os.path.join(CACHE_DIR, "geocode_cache.json")

RETRIEVED = time.strftime("%Y-%m-%d")

# An honest, generic client name; no personal details are sent anywhere.
UA = "Gateway2Work-map-builder/1.0 (python-urllib; research GIS project)"

# Colorado's bounding box (a little padding). Used to catch bad geocodes.
CO_BBOX = (-109.1, 36.95, -102.0, 41.05)   # west, south, east, north

_ctx = ssl.create_default_context()


def fetch(url, raw_name=None, data=None, headers=None, retries=3):
    """Download url and return the body as text. If raw_name is given, also
    save the response to Data/raw/<raw_name> so the original is kept."""
    h = {"User-Agent": UA, "Accept": "*/*"}
    if headers:
        h.update(headers)
    if data is not None and not isinstance(data, bytes):
        data = data.encode()
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=25, context=_ctx) as r:
                body = r.read()
            break
        except Exception as e:          # network hiccup: wait and retry
            last = e
            time.sleep(2 * (attempt + 1))
    else:
        raise RuntimeError(f"Could not download {url}: {last}")
    text = body.decode("utf-8", errors="replace")
    if raw_name:
        os.makedirs(RAW, exist_ok=True)
        with open(os.path.join(RAW, raw_name), "w", encoding="utf-8") as f:
            f.write(text)
    return text


def fetch_json(url, raw_name=None, **kw):
    return json.loads(fetch(url, raw_name, **kw))


def arcgis_query(layer_url, where="1=1", raw_name=None, out_fields="*"):
    """Download every feature from an ArcGIS REST layer as GeoJSON points
    (WGS84), paging through results. Returns a list of GeoJSON features."""
    feats, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "where": where, "outFields": out_fields, "outSR": 4326,
            "returnGeometry": "true", "f": "geojson",
            "resultOffset": offset, "resultRecordCount": 1000,
        })
        page = fetch_json(f"{layer_url}/query?{q}")
        batch = page.get("features", [])
        feats += batch
        if len(batch) < 1000 or not page.get("properties", {}).get("exceededTransferLimit", len(batch) == 1000):
            break
        offset += len(batch)
    if raw_name:
        with open(os.path.join(RAW, raw_name), "w") as f:
            json.dump({"type": "FeatureCollection", "features": feats}, f)
    return feats


# ---------------------------------------------------------------------------
# Geocoding
# ---------------------------------------------------------------------------
_cache = None


def _load_cache():
    global _cache
    if _cache is None:
        os.makedirs(CACHE_DIR, exist_ok=True)
        if os.path.exists(GEOCODE_CACHE):
            with open(GEOCODE_CACHE) as f:
                _cache = json.load(f)
        else:
            _cache = {}
    return _cache


def _save_cache():
    with open(GEOCODE_CACHE, "w") as f:
        json.dump(_cache, f, indent=1, sort_keys=True)


def geocode(address):
    """Return (lon, lat, method, matched_address) for a one-line address
    using the U.S. Census Bureau geocoder, or (None, None, 'unmatched', '')."""
    cache = _load_cache()
    key = address.strip().upper()
    if os.environ.get("G2W_VERBOSE"):
        print("   geocode:", address, flush=True)
    if key in cache:
        c = cache[key]
        return c["lon"], c["lat"], c["method"], c.get("matched", "")
    url = ("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?"
           + urllib.parse.urlencode({"address": address,
                                     "benchmark": "Public_AR_Current",
                                     "format": "json"}))
    try:
        res = fetch_json(url)
        matches = res["result"]["addressMatches"]
    except Exception:
        matches = []
    if matches:
        m = matches[0]
        lon, lat = m["coordinates"]["x"], m["coordinates"]["y"]
        method = "census-rooftop" if len(matches) == 1 else "census-nonexact"
        out = {"lon": round(lon, 6), "lat": round(lat, 6), "method": method,
               "matched": m.get("matchedAddress", "")}
    else:
        out = _nominatim(address)
    cache[key] = out
    _save_cache()
    time.sleep(0.2)
    return out["lon"], out["lat"], out["method"], out["matched"]


def _nominatim(address):
    """Fallback geocoder: OpenStreetMap Nominatim (used only when the Census
    geocoder finds no match). Respects the 1 request/second usage policy.

    Quality rules (added after a spot-check found problems):
      * Reject a match only when BOTH the ZIP and the city disagree with the
        request (OSM postcodes are often imprecise within the right city).
      * "City, Colorado" lookups ask for a settlement (city/town), not the
        county of the same name (e.g. Alamosa, Gunnison, Montrose).
      * A street-address result WITHOUT a house number is labelled
        "osm-street-approx" (point is somewhere on that street).
      * A result whose ZIP code differs from the ZIP in the request is
        rejected (prevents e.g. Golden's W Colfax landing in Denver).
    """
    time.sleep(1.1)
    m_city = re.fullmatch(r"\s*([A-Za-z .'-]+),\s*Colorado\s*", address)
    if m_city:
        params = {"city": m_city.group(1), "state": "Colorado", "country": "USA",
                  "format": "json", "limit": 5, "addressdetails": 1}
    else:
        params = {"q": address, "format": "json", "limit": 1,
                  "countrycodes": "us", "addressdetails": 1}
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(params)
    try:
        res = fetch_json(url)
    except Exception:
        res = []
    if m_city:
        kinds = ("city", "town", "village", "hamlet", "municipality")
        res = [r for r in res if r.get("addresstype") in kinds or r.get("type") in kinds]
    if not res:
        return {"lon": None, "lat": None, "method": "unmatched", "matched": ""}
    r = res[0]
    ad = r.get("address", {})
    if m_city:
        method = "approx-city-center (OSM)"
    else:
        want = re.findall(r"\b(8\d{4})\b", address)
        got = (ad.get("postcode") or "")[:5]
        m_c = re.search(r",\s*([A-Za-z .'-]+),\s*CO\b", address)
        want_city = (m_c.group(1) if m_c else "").strip().lower().replace("canon", "cañon")
        got_city = (ad.get("city") or ad.get("town") or ad.get("village") or ad.get("municipality") or "").lower()
        if want and got and want[-1] != got and want_city and want_city not in got_city and got_city not in want_city:
            return {"lon": None, "lat": None, "method": "unmatched",
                    "matched": f"rejected OSM match (ZIP {got} != {want[-1]} and city differs): {r.get('display_name','')}"}
        method = "osm-nominatim" if ad.get("house_number") else "osm-street-approx"
    return {"lon": round(float(r["lon"]), 6), "lat": round(float(r["lat"]), 6),
            "method": method, "matched": r.get("display_name", "")}


def set_manual(address, lon, lat, note="manual"):
    """Record hand-checked coordinates for an address the Census geocoder
    could not match (rural routes, PO boxes, new buildings)."""
    cache = _load_cache()
    cache[address.strip().upper()] = {"lon": lon, "lat": lat,
                                      "method": "manual", "matched": note}
    _save_cache()


CHARITY_URL = "https://data.colorado.gov/resource/3qtu-edua.json"


def charity_lookup(name_fragment, limit=10):
    """Look up a nonprofit in the Colorado Secretary of State 'Charitable
    Organizations' Offices in Colorado' dataset (data.colorado.gov 3qtu-edua,
    updated daily). Used to VERIFY nonprofit names/addresses. Returns rows."""
    frag = name_fragment.upper().replace("'", "''")
    q = urllib.parse.urlencode({"$where": f"upper(organizationname) like '%{frag}%'",
                                "$limit": limit})
    try:
        return fetch_json(f"{CHARITY_URL}?{q}")
    except Exception:
        return []


def in_colorado(lon, lat):
    w, s, e, n = CO_BBOX
    return lon is not None and w <= lon <= e and s <= lat <= n


# ---------------------------------------------------------------------------
# GeoJSON output
# ---------------------------------------------------------------------------
FIELDS = ["name", "category", "address", "city", "zip", "county", "phone",
          "website", "services", "source", "source_url", "retrieved",
          "geocode", "verified"]


def make_feature(lon, lat, **props):
    p = {k: props.get(k) for k in FIELDS}
    for k, v in props.items():            # keep any extra fields too
        if k not in p:
            p[k] = v
    p = {k: v for k, v in p.items() if v not in (None, "", [])}
    p.setdefault("retrieved", RETRIEVED)
    return {"type": "Feature", "properties": p,
            "geometry": {"type": "Point",
                         "coordinates": [round(lon, 6), round(lat, 6)]}}


def geocoded_feature(rec, category, source, source_url, verified=None):
    """rec: dict with name, address, city, zip (+ optional phone, website,
    services, county). Geocodes the address and returns (feature, problem)."""
    # Suite/unit/building text confuses geocoders; drop it for the lookup only
    # (the full address is still shown in the popup).
    street = re.split(r",?\s+(?:Suite|Ste\.?|Unit|Building|Bldg\.?|Room|Rm\.?|Floor)\b|,?\s*#\s*\w",
                      rec["address"], flags=re.I)[0]
    full = f"{street}, {rec['city']}, CO {rec.get('zip', '') or ''}".strip()
    lon, lat, method, matched = geocode(full)
    if not in_colorado(lon, lat):
        return None, f"UNMATCHED: {rec['name']} | {full}"
    f = make_feature(lon, lat, name=rec["name"], category=category,
                     address=rec["address"], city=rec["city"],
                     zip=rec.get("zip"), county=rec.get("county"),
                     phone=rec.get("phone"), website=rec.get("website"),
                     services=rec.get("services"), source=source,
                     source_url=rec.get("source_url", source_url),
                     geocode=method, verified=rec.get("verified", verified))
    return f, None


def write_layer(filename, features, problems=()):
    path = os.path.join(DATA, filename)
    features = sorted(features, key=lambda f: f["properties"].get("name", ""))
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f,
                  indent=1, ensure_ascii=False)
    print(f"\nWrote {len(features)} features -> Data/{filename}")
    methods = {}
    for ft in features:
        m = ft["properties"].get("geocode", "?")
        methods[m] = methods.get(m, 0) + 1
    print("  coordinates:", methods)
    for p in problems:
        print("  !", p)
