"""
Layer 8 - IPS (Individual Placement and Support) Supported-Employment Agencies

PROVENANCE SUMMARY (full write-up: Data/sources/08_IPS.md)
  Rosters (three, compared):
    A. BHA IPS page (bha.colorado.gov/individual-placement-and-support-ips-supported-employment),
       current; read via search-engine copy (site blocks automated access).
    B. "Individual Placement and Support (IPS) Program, Year 5 Evaluation Report"
       (State Opioid Response grant, prepared for BHA, Feb 2024) -
       Data/raw/sor_ips_annual_report_22-23.pdf, Exhibit 1 & 3: SOR-funded IPS sites.
    C. Older state IPS provider list (colorado.gov/pacific/cdhs/..., ~2020).
  Addresses: SAMHSA FindTreatment (Layer 4) record for the agency in that town,
             or the agency main office from Layer 23.
"""
from common import geocoded_feature, write_layer

CAT = "IPS Agencies"
A = "https://bha.colorado.gov/individual-placement-and-support-ips-supported-employment"
B = "https://www.sorcolorado.org/wp-content/uploads/2024/03/SOR_IPS-Annual-Report-22-23_Final_for-BHA.pdf"
C = "https://www.colorado.gov/pacific/cdhs/individual-placement-and-support-ips-supported-employment"
IPS = [
 # name, address, city, zip, phone, area served, listed-in, source_url, address source
 ("AllHealth Network - IPS (Littleton)", "5500 S Sycamore Street", "Littleton", "80120", "303-730-8858", "Arapahoe and Douglas counties",
  "BHA IPS page (current); SOR IPS report 2022-23", A, "SAMHSA FindTreatment record"),
 ("Axis Health System - IPS", "1125 Three Springs Boulevard", "Durango", "81301", "970-259-2162",
  "Durango, Montrose, Gunnison, Crested Butte, Telluride, Pagosa Springs", "BHA IPS page (current)", A, "main office (Layer 23; confirm)"),
 ("Behavioral Health Group (BHG) Longmont - IPS", "850 23rd Avenue", "Longmont", "80501", "303-245-0123", "Longmont / Boulder County",
  "BHA IPS page (current); SOR IPS report 2022-23", A, "SAMHSA FindTreatment record (BHG Longmont Treatment Center)"),
 ("Diversus Health - IPS (SUD)", "115 S Parkside Drive", "Colorado Springs", "80910", "719-572-6100", "Colorado Springs, El Paso, Park, Teller",
  "BHA IPS page (current); older state list", A, "main office (Layer 23)"),
 ("SummitStone Health Partners - IPS", "1217 Riverside Avenue", "Fort Collins", "80524", "970-494-4200", "Fort Collins, Loveland, Estes Park",
  "SOR IPS report 2022-23; older state list", B, "main office (Layer 23)"),
 ("Crossroads Turning Points - IPS (Pueblo)", "509 E 13th Street", "Pueblo", "81001", "719-546-6666", "Pueblo area",
  "SOR IPS report 2022-23; older state list", B, "SAMHSA FindTreatment record"),
 ("Community Reach Center - IPS", "8989 Huron Street", "Thornton", "80260", "303-853-3500", "Adams County",
  "older state list only", C, "main office (Layer 23)"),
 ("Jefferson Center for Mental Health - IPS", "4851 Independence Street", "Wheat Ridge", "80033", "303-425-0300", "Jefferson County",
  "older state list only", C, "main office (Layer 23)"),
 ("North Range Behavioral Health - IPS", "1306 11th Avenue", "Greeley", "80631", "970-347-2120", "Weld County",
  "older state list only", C, "main office (Layer 23)"),
 ("Colorado Coalition for the Homeless - IPS", "2111 Champa Street", "Denver", "80205", None, "Denver metro",
  "older state list only", C, "organization headquarters (GuideStar profile: 2111 Champa St, 80205)"),
]
feats, probs = [], []
for name, a, city, z, ph, area, listed, url, asrc in IPS:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, phone=ph,
                                 services="IPS supported employment (rapid job search, competitive jobs, integrated with treatment)"),
                            CAT, f"Colorado IPS rosters: {listed}; address: {asrc}", url)
    if p: probs.append(p); continue
    f["properties"].update(area_served=area, listed_in=listed)
    if "older state list only" in listed:
        f["properties"]["status_note"] = "Listed only on ~2020 state IPS list; confirm program is still active."
    feats.append(f)
write_layer("IPS_Agencies.geojson", feats, probs)
