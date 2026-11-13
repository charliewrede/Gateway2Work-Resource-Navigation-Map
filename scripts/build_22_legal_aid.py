"""
Layer 22 - Legal Aid and Record-Sealing Services

PROVENANCE SUMMARY (full write-up: Data/sources/22_Legal_Aid.md)
  Colorado Legal Services (CLS) - the statewide LSC-funded civil legal aid
  provider; runs a Record Sealing & Expungement (RSE) clinic. Office list
  from CLS's own "Get Help" page (https://www.coloradolegalservices.org/get-help/),
  downloaded 2026-11-13 to Data/raw/cls_get_help.html.
"""
from common import geocoded_feature, write_layer

CAT = "Legal Aid and Record-Sealing Services"
SRC = "Colorado Legal Services 'Get Help' office list"
URL = "https://www.coloradolegalservices.org/get-help/"
SVC = "Free civil legal aid for eligible low-income clients; Record Sealing & Expungement (RSE) clinic (apply via CLS)"

O = [
 ("Colorado Legal Services - Denver (main office)", "1560 Broadway, Suite 1100", "Denver", "80203", "303-837-1313", "Denver metro"),
 ("Colorado Legal Services - Alamosa", "715 Main Street", "Alamosa", "81101", "719-589-4993", "Alamosa, Conejos, Costilla, Mineral, Rio Grande, Saguache"),
 ("Colorado Legal Services - Boulder", "2935 Baseline Road, Suite 301", "Boulder", "80303", "303-449-7575", "Boulder, Broomfield"),
 ("Colorado Legal Services - Colorado Springs", "102 S Tejon Street, Suite 430", "Colorado Springs", "80903", "719-471-0380", "El Paso, Lincoln, and nearby counties"),
 ("Colorado Legal Services - Craig (Northwest Colorado Legal Services Project)", "1111 W Victory Way, Suite 109", "Craig", "81625", "1-800-521-6968", "Northwest counties incl. Moffat, Pitkin, Rio Blanco, Routt, Summit"),
 ("Colorado Legal Services - Durango", "679 E 2nd Avenue, Suite B", "Durango", "81301", "970-247-0266", "Archuleta, Dolores, Hinsdale, La Plata, Montezuma, San Juan; Ute Mountain Ute and Southern Ute"),
 ("Colorado Legal Services - Fort Collins", "215 W Oak Street, Suite 800", "Fort Collins", "80521", "970-493-2891", "Larimer, Logan, Phillips, Sedgwick"),
 ("Colorado Legal Services - Grand Junction", "120 West Park Drive, Suite 205", "Grand Junction", "81505", "970-243-7940", "Delta, Garfield, Mesa and nearby counties"),
 ("Colorado Legal Services - Greeley", "912 8th Avenue", "Greeley", "80631", "970-353-7554", "Weld, Kit Carson, Morgan, Washington and nearby counties"),
 ("Colorado Legal Services - La Junta", "401 Santa Fe Avenue", "La Junta", "81050", "719-384-5438", "Baca, Bent, Cheyenne, Crowley, Kiowa, Otero, Prowers"),
 ("Colorado Legal Services - Pueblo", "1000 W 6th Street, Suite I", "Pueblo", "81003", "719-545-6708", "Huerfano, Las Animas, Pueblo"),
 ("Colorado Legal Services - Salida", "1604 H Street, Suite 201", "Salida", "81201", "719-539-4251", "Park, Chaffee, Custer"),
]
feats, probs = [], []
for name, a, city, z, ph, area in O:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, phone=ph,
                                 website="https://www.coloradolegalservices.org", services=SVC), CAT, SRC, URL)
    if p: probs.append(p); continue
    f["properties"]["counties_served"] = area
    if "Grand Junction" in name:
        f["properties"]["status_note"] = "CLS lists this as a MAILING address; call or apply online (applyonlinecls.org)."
    feats.append(f)
write_layer("Legal_Aid_and_Record_Sealing.geojson", feats, probs)
