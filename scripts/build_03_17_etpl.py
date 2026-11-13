"""
Layer 3  - Workforce Development / Training Providers (WIOA Eligible Training Providers)
Layer 17 - Apprenticeship and Pre-Apprenticeship Programs

PROVENANCE SUMMARY (write-ups: Data/sources/03_Workforce_Development_Providers.md,
                    17_Apprenticeship.md)
  Source : U.S. Department of Labor, TrainingProviderResults.gov - national
           Eligible Training Provider (ETP) program file (ETA-9171 data,
           programs on state ETP lists as of June 30, 2024):
           https://www.trainingproviderresults.gov/data/DownloadPrograms.xlsx
           Colorado rows extracted by scripts/extract_etpl_colorado.py to
           Data/raw/etpl_CO.csv (reportingstate = CO and provider state = CO).
  Grouping: one point per provider + street address, with program counts.
  Coords : Census geocoder from the street address (the file's own lat/long
           are rounded to 2 decimals, ~1 km).
"""
import csv, collections, os, re
from common import geocoded_feature, write_layer, RAW

URL = "https://www.trainingproviderresults.gov/data/DownloadPrograms.xlsx"
rows = [r for r in csv.DictReader(open(os.path.join(RAW, "etpl_CO.csv")))
        if r["reportingstate"] == "CO" and r["state"] == "CO"]

def clean_addr(a):
    a = re.sub(r"\b(N/a|Null)\b", "", a, flags=re.I)
    a = re.sub(r"\s+\d+(college|cr\d+|curtis|ab pk)\b.*$", "", a, flags=re.I)   # stray tokens seen in file
    a = a.replace("Drrive", "Drive").replace("Suiter", "Suite")
    a = re.sub(r"\bAv\b", "Ave", a)
    a = re.sub(r"\s+Box\s+\d+\b", "", a, flags=re.I)              # "13300 W 6th Av Box 35"
    return re.sub(r"\s{2,}", " ", a).strip(" ,")

groups = collections.OrderedDict()
for r in rows:
    key = (r["d101_eligible_training_provider"].strip(), clean_addr(r["address"]).lower(), r["city"].strip().lower())
    g = groups.setdefault(key, {"r": r, "programs": [], "fields": collections.Counter(), "appr": False})
    g["programs"].append(r["d105_program_name"].strip())
    g["fields"][r["CIP_Title"].strip().rstrip(".")] += 1
    txt = (r["d105_program_name"] + " " + r["d101_eligible_training_provider"] + " " + r["d106_program_description"]).lower()
    if "apprentic" in txt:
        g["appr"] = True

# merge rows that are the same provider at the same place but spelled slightly differently
feats3, feats17, probs = [], [], []
seen = {}
for (prov, addr, city), g in groups.items():
    r = g["r"]
    k2 = (re.sub(r"[^a-z]", "", prov.lower())[:20], re.sub(r"[^0-9]", "", addr)[:6], city)
    if k2 in seen:
        f = seen[k2]
        f["properties"]["program_count"] += len(g["programs"])
        continue
    rec = dict(name=prov, address=clean_addr(r["address"]), city=r["city"].strip(), zip=r["zip"].strip()[:5],
               website=None if r["d107_program_url"] in ("", "Unknown") else r["d107_program_url"])
    f, p = geocoded_feature(rec, "Workforce Development / Training Providers",
                            "U.S. DOL TrainingProviderResults.gov - Colorado Eligible Training Provider List (as of 2024-06-30)", URL)
    if p: probs.append(p); continue
    top = ", ".join(n for n, _ in g["fields"].most_common(3))
    f["properties"].update(program_count=len(g["programs"]), main_fields=top,
                           entity_type=r["d104_entity_type"] or None,
                           apprenticeship_programs="Yes" if g["appr"] else "No")
    seen[k2] = f
    feats3.append(f)
    if g["appr"]:
        a = dict(f, properties=dict(f["properties"]))
        a["properties"]["category"] = "Apprenticeship and Pre-Apprenticeship Programs"
        a["properties"]["apprenticeship_program_names"] = "; ".join(
            sorted({p for p in g["programs"] if "apprentic" in p.lower()})) or "(apprenticeship named in description)"
        feats17.append(a)

write_layer("Workforce_Development_Training_Providers.geojson", feats3, probs)
write_layer("Apprenticeship_Programs.geojson", feats17)
