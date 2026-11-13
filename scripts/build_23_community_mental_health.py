"""
Layer 23 - Community Mental Health and Disability Employment Providers

PROVENANCE SUMMARY (full write-up: Data/sources/23_Community_Mental_Health.md)
  Provider roster + county coverage : Colorado Behavioral Healthcare Council
      (CBHC, the association of Colorado's community mental health centers /
      safety-net providers), "Behavioral Health Providers" by county:
      https://www.cbhc.org/find-services/behavioral-health-providers/
      Raw: Data/raw/cbhc_providers.html
  Main-office address : each provider's own website (footer/locations page),
      or a cited directory where the site showed none.
  Counties CBHC leaves blank are served by non-member safety-net providers
  (Axis Health System, AllHealth Network) - added and flagged.
"""
from common import geocoded_feature, write_layer

CAT = "Community Mental Health and Disability Employment Providers"
CBHC = "https://www.cbhc.org/find-services/behavioral-health-providers/"
P = [
 # name, address, city, zip, phone, website, counties (from CBHC), address source
 ("Community Reach Center", "8989 Huron Street", "Thornton", "80260", "303-853-3500", "https://www.communityreachcenter.org", "Adams", "provider website"),
 ("San Luis Valley Behavioral Health Group", "8745 County Road 9 South", "Alamosa", "81101", "719-589-3671", "https://www.slvbhg.org", "Alamosa, Conejos, Costilla, Mineral, Rio Grande, Saguache", "provider website"),
 ("Aurora Mental Health and Recovery", "1290 S Potomac Street", "Aurora", "80012", "303-617-2300", "https://www.auroramhr.org", "Arapahoe (Aurora)", "provider website"),
 ("Valley-Wide Health Systems", "128 Market Street", "Alamosa", "81101", "833-350-1113", "https://valley-widehealth.org", "Baca, Bent, Crowley, Kiowa, Otero, Prowers", "provider website"),
 ("Clinica Family Health & Wellness (behavioral health, formerly Mental Health Partners)", "1735 S Public Road", "Lafayette", "80026", "303-650-4460", "https://www.clinica.org", "Boulder, Broomfield", "provider website"),
 ("Diversus Health", "115 S Parkside Drive", "Colorado Springs", "80910", "719-572-6100", "https://diversushealth.org", "El Paso, Teller, Park (from provider's own site list; CBHC page lists these two providers swapped)", "provider website"),
 ("Centennial Mental Health Center (administration)", "211 W Main Street, Suite 1", "Sterling", "80751", "970-522-4549", "https://www.centennialmhc.org", "Cheyenne, Elbert, Kit Carson, Lincoln, Logan, Morgan, Phillips, Sedgwick, Washington, Yuma", "provider website"),
 ("Jefferson Center for Mental Health", "4851 Independence Street", "Wheat Ridge", "80033", "303-425-0300", "https://www.jcmh.org", "Jefferson, Clear Creek, Gilpin", "provider website"),
 ("WellPower", "4141 E Dickenson Place", "Denver", "80222", "303-504-6500", "https://www.wellpower.org", "Denver", "provider website"),
 ("Servicios de La Raza (behavioral health)", "3131 W 14th Avenue", "Denver", "80204", "303-458-5851", "https://serviciosdelaraza.org", "Denver, Pueblo", "WAGEES partner page"),
 ("Health Solutions West (formerly Mind Springs Health)", "515 28 3/4 Road", "Grand Junction", "81501", "877-603-7045", "https://www.healthsolutionswest.org", "Eagle, Garfield, Grand, Jackson, Mesa, Moffat, Pitkin, Rio Blanco, Routt, Summit", "NPI registry + directory listings (acquired by Health Solutions)"),
 ("Solvista Health", "3225 Independence Road", "Canon City", "81212", "719-275-2351", "https://solvistahealth.org", "Chaffee, Custer, Fremont, Lake (from provider's own site list; CBHC page lists these two providers swapped)", "provider website"),
 ("Health Solutions", "41 Montebello Road", "Pueblo", "81001", "719-545-2746", "https://www.health.solutions", "Huerfano, Las Animas, Pueblo", "provider website"),
 ("SummitStone Health Partners", "1217 Riverside Avenue", "Fort Collins", "80524", "970-494-4200", "https://www.summitstone.org", "Larimer", "provider website"),
 ("North Range Behavioral Health", "1306 11th Avenue", "Greeley", "80631", "970-347-2120", "https://northrange.org", "Weld", "provider website"),
 ("AllHealth Network (not a CBHC member)", "116 Inverness Drive E", "Englewood", "80112", None, "https://www.allhealthnetwork.org", "Douglas, Arapahoe (non-Aurora)", "provider website"),
 ("Axis Health System (not a CBHC member)", "1125 Three Springs Boulevard", "Durango", "81301", "970-259-2162", "https://www.axishealthsystem.org", "Archuleta, Dolores, La Plata, Montezuma, San Juan", "NPI registry practice address - CONFIRM (other listings: 185 Suttle St, 281 Sawyer Dr)"),
]
feats, probs = [], []
for name, a, city, z, ph, web, counties, asrc in P:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, phone=ph, website=web,
                                 services="Community mental health / safety-net behavioral health; many run IPS supported employment"),
                            CAT, f"CBHC provider-by-county list; main-office address from {asrc}", CBHC)
    if p: probs.append(p); continue
    f["properties"]["counties_served"] = counties
    if "CONFIRM" in asrc: f["properties"]["status_note"] = "Main office address conflicting across sources; confirm."
    feats.append(f)
write_layer("Community_Mental_Health_Providers.geojson", feats, probs)
