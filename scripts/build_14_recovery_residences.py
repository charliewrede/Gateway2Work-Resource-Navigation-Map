"""
Layer 14 - Recovery Residences / Sober Living  (PRIVACY-PROTECTED, CITY LEVEL)

PROVENANCE SUMMARY (full write-up: Data/sources/14_Recovery_Residences.md)
  Source  : Oxford House vacancy directory, Colorado, queried by county
            (https://www.oxfordvacancies.com/?state=CO&county=...), 2026-11-13.
            Only aggregated counts per city were stored
            (Data/raw/oxford_house_CO_by_city.json); house names, street
            addresses and resident contact details were deliberately NOT saved.
  Points  : one point per city at the city center (OpenStreetMap), showing
            number of houses and beds.
  Why not the state list : BHA's certified recovery residence list
            (bha.colorado.gov/certified-recovery-residences) blocks automated access.
"""
import json, os
from common import geocode, make_feature, write_layer, RAW

d = json.load(open(os.path.join(RAW, "oxford_house_CO_by_city.json")))
cities = dict(d["by_city"])
# The Douglas County query returned no rows; the statewide page showed one
# Castle Rock house (9 beds, men) - added from that first statewide pull.
cities.setdefault("Castle Rock", {"county": "Douglas", "houses": 1, "beds": 9, "types": {"Men": 1}})

feats = []
for city, v in sorted(cities.items()):
    lon, lat, gm, _ = geocode(f"{city}, Colorado")
    feats.append(make_feature(lon, lat, name=f"Oxford Houses - {city} ({v['houses']} houses, {v['beds']} beds)",
        category="Recovery Residences / Sober Living", city=city, county=v["county"],
        oxford_houses=v["houses"], beds=v["beds"],
        house_types=", ".join(f"{k}: {n}" for k, n in v["types"].items()),
        website="https://www.oxfordvacancies.com/?state=CO",
        services="Peer-run, self-supporting recovery homes (Oxford House model); apply online",
        source="Oxford House vacancy directory (aggregated to city)", source_url=d["source"],
        geocode="APPROXIMATE - city center (individual homes intentionally not mapped)"))
write_layer("Recovery_Residences_by_City.geojson", feats)
print("houses:", sum(v["houses"] for v in cities.values()), "beds:", sum(v["beds"] for v in cities.values()))
