"""
Layer 9 - DVR Offices and Authorized Service Providers

PROVENANCE SUMMARY (full write-up: Data/sources/09_DVR.md)
  Office list : Colorado Division of Vocational Rehabilitation (CDLE) "DVR Phone
                Numbers" page https://dvr.colorado.gov/dvr-programs-services/dvr-questionnaire/dvr-phone-numbers
                and "Contact Us" page. dvr.colorado.gov returns HTTP 403 to
                automated tools, so the office list was read from search-engine
                copies of those pages; extra offices from Network of Care.
  Coords      : Census geocoder (OSM fallback).
"""
from common import geocoded_feature, write_layer

CAT = "DVR Offices and Authorized Service Providers"
PH = "https://dvr.colorado.gov/dvr-programs-services/dvr-questionnaire/dvr-phone-numbers"
D = [
 # name, address, city, zip, phone, source_url, note
 ("DVR Administrative Office (CDLE)", "707 17th Street, Suite 2700", "Denver", "80202", None, "https://dvr.colorado.gov/contact-us", None),
 ("DVR Alamosa Office", "305 Murphy Drive, Unit B", "Alamosa", "81101", "719-589-5158", PH, "Co-located with Alamosa Workforce Center"),
 ("DVR Colorado Springs Office", "1365 Garden of the Gods Road, Suite 250", "Colorado Springs", "80907", "719-635-3585", PH, None),
 ("DVR Delta Office", "206 Ute Street", "Delta", "81416", "970-874-5781", PH, "Co-located with Delta Workforce Center"),
 ("DVR Durango Office", "160 Rock Point Drive, Suite A", "Durango", "81301", "970-247-3161", PH, None),
 ("DVR Fort Morgan Office", "426 Ensign Street", "Fort Morgan", "80701", "970-867-9401", PH, "Co-located with Fort Morgan Workforce Center"),
 ("DVR Golden Office", "3500 Illinois Street", "Golden", "80401", "303-866-4121", PH, "Suite 400 (DVR page) vs Suite 1400 (other listing)"),
 ("DVR Grand Junction Office", "222 S 6th Street, Suite 215", "Grand Junction", "81501", "970-248-7103", PH, None),
 ("DVR Limon Office", "825 Second Street", "Limon", "80828", "719-775-8819", PH, None),
 ("DVR Northglenn Office", "11990 Grant Street, Suite 201", "Northglenn", "80233", "303-866-2110", PH, None),
 ("DVR Trinidad Office", "140 N Commercial Street", "Trinidad", "81082", "719-220-4354", PH, "Co-located with Trinidad Workforce Center"),
 ("DVR Englewood Office", "750 W Hampden Avenue, Suite 225", "Englewood", "80110", None, "https://dvr.colorado.gov/contact-us", "Listed on DVR Contact Us page; role not stated"),
 ("DVR Aurora Office", "12510 E Iliff Avenue, Suite 303", "Aurora", "80014", "303-671-4160", "https://aging.networkofcare.org/denverregion-co/services/agency?pid=ColoradoDivisionofVocationalRehabilitation_965_1_0", "From Network of Care directory; confirm"),
 ("DVR Montrose Office", "1551 Ogden Road", "Montrose", "81401", "970-249-4468", "https://askjan.org/organizations/Colorado-Division-of-Vocational-Rehabilitation.cfm", "Older listing; confirm"),
]
feats, probs = [], []
for name, a, city, z, ph, url, note in D:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, phone=ph,
                                 website="https://dvr.colorado.gov",
                                 services="Vocational rehabilitation for people with disabilities (incl. mental health and substance use disorders)"),
                            CAT, "Colorado Division of Vocational Rehabilitation office list", url)
    if p: probs.append(p); continue
    if note: f["properties"]["status_note"] = note
    feats.append(f)
write_layer("DVR_Offices.geojson", feats, probs)
