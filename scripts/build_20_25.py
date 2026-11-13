"""
Layer 20 - Community-Based and Faith-Based Organizations
Layer 25 - Social Enterprises and Transitional Employment Programs

PROVENANCE SUMMARY (write-ups: Data/sources/20_Community_and_Faith_Based.md,
                    25_Social_Enterprises.md)
  L25 : organizations identified as employment social enterprises / transitional
        jobs programs by the Colorado Attorney General's Reentry Report (2021),
        Rose Community Foundation donor handout (Feb 2024) and news coverage;
        addresses from each organization's own site or GuideStar/ColoradoGives.
  L20 : NOT new research - a role-based selection of already-verified features
        from other layers (WAGEES partners, shelters) whose organizations are
        community- or faith-based. Categories are not mutually exclusive (per
        the TSRG framework), so the same organization can appear in two layers.
"""
import json, os
from common import DATA, geocoded_feature, write_layer

# ---------------------------------------------------------------- Layer 25
SE = [
 ("Goodwill of Colorado - Denver (ReHire Colorado administrator)", "6850 Federal Boulevard", "Denver", "80221",
  "https://goodwillcolorado.org/", "Social enterprises employing people with barriers; administers ReHire Colorado transitional jobs", "own website"),
 ("Goodwill of Colorado - Colorado Springs", "1460 Garden of the Gods Road", "Colorado Springs", "80907",
  "https://goodwillcolorado.org/", "Social enterprises; job training and placement", "own website"),
 ("Bayaud Enterprises", "333 W Bayaud Avenue", "Denver", "80223",
  "https://www.bayaudenterprises.org/", "Social enterprises (Business Solutions) providing supported and transitional employment", "GuideStar, ColoradoGives, NPI registry agree"),
 ("Women's Bean Project", "1300 W Alameda Avenue", "Denver", "80223",
  "https://womensbeanproject.com/", "Full-time paid transitional jobs for women facing barriers", "own website"),
 ("Mile High WorkShop", "3795 E 38th Avenue, Unit A", "Denver", "80205",
  "https://www.coloradogives.org/organization/MileHighWorkShop", "Employment social enterprise and job training for people facing barriers (incl. recovery, reentry)", "ColoradoGives; Second Chance Business Coalition listing"),
 ("Center for Employment Opportunities (CEO) - Denver", "3532 N Franklin Street, Suite S", "Denver", "80205",
  "https://www.ceoworks.org/locations/denver", "Transitional paid work crews for people recently released", "Second Chance Business Coalition; SkillPlum ETPL"),
 ("Center for Employment Opportunities (CEO) - Colorado Springs", "888 Garden of the Gods Road, Suite 110", "Colorado Springs", "80907",
  "https://www.ceoworks.org/locations/colorado-springs", "Transitional paid work crews", "Remerg; findhelp; Women's Directory"),
 ("Bridge House Ready to Work - Boulder", "4747 Table Mesa Drive", "Boulder", "80305",
  "https://boulderbridgehouse.org/", "Paid work in social enterprise + housing (Ready to Work)", "WAGEES partner page"),
]
feats, probs = [], []
for name, a, city, z, web, svc, asrc in SE:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, website=web, services=svc),
                            "Social Enterprises and Transitional Employment",
                            f"CO Attorney General Reentry Report (2021) / Rose Community Foundation handout (2024) / news; address: {asrc}", web)
    if p: probs.append(p); continue
    feats.append(f)
write_layer("Social_Enterprises_and_Transitional_Employment.geojson", feats, probs)

# ---------------------------------------------------------------- Layer 20
PICK = {  # organization name -> (type, from layer file)
 "Loaves & Fishes Ministries": ("Faith-based", "Reentry_and_Transitional_Services.geojson"),
 "Cooperating Ministry of Logan County": ("Faith-based", "Reentry_and_Transitional_Services.geojson"),
 "Manna Soup Kitchen": ("Community-based (meals, reentry)", "Reentry_and_Transitional_Services.geojson"),
 "Servicios de La Raza": ("Community-based (Latino services)", "Reentry_and_Transitional_Services.geojson"),
 "The Pinon Project": ("Community-based (family resource center)", "Reentry_and_Transitional_Services.geojson"),
 "Hazelbrook Community Center": ("Community-based", "Reentry_and_Transitional_Services.geojson"),
 "Life-Line Colorado": ("Community-based (peer mentoring)", "Reentry_and_Transitional_Services.geojson"),
 "The Empowerment Program (women only)": ("Community-based (women)", "Reentry_and_Transitional_Services.geojson"),
 "Denver Rescue Mission (headquarters)": ("Faith-based", "Homelessness_and_Housing_Services.geojson"),
 "Springs Rescue Mission": ("Faith-based", "Homelessness_and_Housing_Services.geojson"),
 "Fort Collins Rescue Mission": ("Faith-based", "Homelessness_and_Housing_Services.geojson"),
 "Catholic Charities of Denver (shelter services, HQ)": ("Faith-based", "Homelessness_and_Housing_Services.geojson"),
 "Pueblo Rescue Mission": ("Faith-based", "Homelessness_and_Housing_Services.geojson"),
}
out = []
for fname in sorted({v[1] for v in PICK.values()}):
    for f in json.load(open(os.path.join(DATA, fname)))["features"]:
        n = f["properties"]["name"]
        if n in PICK:
            g = json.loads(json.dumps(f))
            g["properties"]["category"] = "Community-Based and Faith-Based Organizations"
            g["properties"]["org_type"] = PICK[n][0]
            g["properties"]["also_in_layer"] = fname.replace(".geojson", "").replace("_", " ")
            out.append(g)
missing = sorted(set(PICK) - {f["properties"]["name"] for f in out})
write_layer("Community_and_Faith_Based_Organizations.geojson", out, [f"not found in source layer: {m}" for m in missing])
