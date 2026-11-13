"""
Layer 10 - Reentry and Transitional Services
Layer 12 - Halfway Houses and Transitional Housing

PROVENANCE SUMMARY (full write-ups: Data/sources/10_Reentry.md, 12_Halfway_Houses.md)
  WAGEES network : official partner roster + each partner's page on wageesco.org
                   (Latino Coalition for Community Leadership, CDOC's WAGEES
                   grant intermediary). Raw: Data/raw/wagees_partners.html,
                   Data/raw/wagees/*.html. Addresses from the page text or the
                   page's embedded Google Maps link.
  Named in PDF   : Center for Employment Opportunities, Second Chance Center,
                   The Reentry Initiative, CCJRC (own sites / directories).
  Halfway houses : BOP Residential Reentry Center feed
                   https://www.bop.gov/PublicInfo/execute/rrc?todo=query&output=json
                   (Data/raw/bop_rrc.json) + Bridge House Ready-to-Work residences.
"""
import json, os
from common import geocoded_feature, make_feature, write_layer, RAW

W = "https://wageesco.org/community-partners/"
WSRC = "Colorado WAGEES Community Partners roster (wageesco.org, LCCL)"

REENTRY = [
 # name, address, city, zip, phone, website, source_url, services, wagees
 ("Second Chance Center", "224 Potomac Street", "Aurora", "80011", "303-909-0813", "https://www.scccolorado.org/", W+"second-chance-center/",
  "Reentry case management, employment prep, housing (CREW transitional housing), record-sealing events; WAGEES partner (Aurora, Englewood, Westminster)", True),
 ("The Reentry Initiative", "402 Kimbark Street", "Longmont", "80501", "720-640-9513", "https://www.reentryinitiative.org/", W+"the-reentry-initiative/",
  "Reentry mentoring, employment and transitional support; WAGEES partner (Boulder, Longmont)", True),
 ("Center for Employment Opportunities (CEO) - Denver", "3532 N Franklin Street, Suite S", "Denver", "80205", "720-279-8489", "https://www.ceoworks.org/locations/denver", "https://www.ceoworks.org/locations/denver",
  "Transitional paid employment, job coaching and placement, retention services for people recently released", False),
 ("Center for Employment Opportunities (CEO) - Colorado Springs", "888 Garden of the Gods Road, Suite 110", "Colorado Springs", "80907", "719-694-5450", "https://www.ceoworks.org/locations/colorado-springs", "https://remerg.com/resources/center-for-employment-opportunities-3/",
  "Transitional paid employment, job coaching and placement, retention services", False),
 ("Colorado Criminal Justice Reform Coalition (CCJRC)", "821 22nd Street", "Denver", "80205", None, "https://www.ccjrc.org/", "https://www.ccjrc.org/wagees",
  "Reentry resources, advocacy and justice-system connections; helped create WAGEES", False),
 ("The Empowerment Program (women only)", "1600 York Street", "Denver", "80206", "303-320-1989", "https://www.empowermentprogram.org/", W+"the-empowerment-program/",
  "Gender-responsive reentry, housing, employment and health services for women; WAGEES partner", True),
 ("Life-Line Colorado", "1240 W Bayaud Avenue", "Denver", "80223", "720-328-5650", "https://life-linecolorado.org/", W+"life-line-colorado/",
  "Peer reentry mentoring and support; WAGEES partner (Denver, Englewood, Westminster)", True),
 ("Servicios de La Raza", "3131 W 14th Avenue", "Denver", "80204", "303-953-5918", "https://serviciosdelaraza.org/", W+"servicios-de-la-raza/",
  "Culturally responsive reentry and employment services; WAGEES partner", True),
 ("The Don't Look Back Center", "14211 E 4th Avenue, Building 3, Suite 305", "Aurora", "80011", "720-638-8397", "https://thedontlookbackcenter.org/", W+"tdlbc/",
  "Gender-responsive reentry services; WAGEES partner (Aurora)", True),
 ("Hazelbrook Community Center", "1120 N Circle Drive, Suite 120", "Colorado Springs", "80909", "719-748-7285", "https://hazelbrookcommunity.org", W+"hazelbrook/",
  "Reentry services; WAGEES partner (Colorado Springs, Englewood)", True),
 ("Elk Meadow Enduring Connections", "685 Citadel Drive East, Suite 510", "Colorado Springs", "80909", "719-452-0393", None, "https://wageesco.org/community-partners/elk-meadow-enduring-connections/",
  "Reentry services; WAGEES partner (Colorado Springs)", True),
 ("Homeward Alliance", "242 Conifer Street", "Fort Collins", "80524", "970-658-9878", "https://www.homewardalliance.org/", W+"homeward-alliance/",
  "Reentry and housing navigation; WAGEES partner (Larimer, Jackson)", True),
 ("The Rock Found", "1542 7th Avenue", "Greeley", "80631", "970-352-9571", "https://www.therockfound.org/", W+"the-rock-found/",
  "Reentry employment, transitional housing, community reintegration; WAGEES partner (Weld)", True),
 ("Cooperating Ministry of Logan County", "230 N 10th Avenue", "Sterling", "80751", "970-522-6405", "https://www.coopminlc.com/", "https://www.coopminlc.com/",
  "Reentry support; WAGEES partner (Sterling parole area)", True),
 ("Loaves & Fishes Ministries", "241 Justice Center Road", "Canon City", "81212", "719-275-0593", "http://lfministries.org/", W+"loaves-and-fishes/",
  "Reentry support; WAGEES partner (Canon City)", True),
 ("Manna Soup Kitchen", "1100 Avenida Del Sol", "Durango", "81301", "970-385-5095", "https://www.mannasoupkitchen.org/", W+"manna/",
  "Reentry and basic-needs support; WAGEES partner (Durango)", True),
 ("The Pinon Project", "210 E Main Street", "Cortez", "81321", "970-564-3811", "https://www.pinonproject.org/", W+"the-pinon-project/",
  "Reentry and family services; WAGEES partner (Cortez/Durango area)", True),
 ("Valley-Wide Health Systems (WAGEES reentry)", "711 Barnes Avenue", "La Junta", "81050", "719-384-5446", "https://valley-widehealth.org/", "https://wageesco.org/valley-wide",
  "Reentry services; WAGEES partner (La Junta parole area)", True),
 ("The Freedom Institute - Grand Junction (Western Slope WAGEES)", "930 Main Street", "Grand Junction", "81501", "970-778-5558", None, "https://wageesco.org/community-partners/freedom-institute-grand-junction/",
  "Reentry services; WAGEES partner (Grand Junction, Rifle, Craig by appointment)", True),
 ("The Freedom Institute - Montrose (Western Slope WAGEES)", "307 E Main Street", "Montrose", "81401", "970-787-5972", None, "https://wageesco.org/community-partners/freedom-institute-montrose/",
  "Reentry services; WAGEES partner (Montrose)", True),
]

feats, probs = [], []
for name, a, city, z, ph, web, url, svc, wag in REENTRY:
    src = WSRC if wag else "Organization website / directory listing (see source_url)"
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, phone=ph, website=web, services=svc),
                            "Reentry and Transitional Services", src, url)
    if p: probs.append(p); continue
    f["properties"]["wagees_partner"] = "Yes" if wag else "No"
    if "Valley-Wide" in name:
        f["properties"]["verified"] = "WAGEES page printed ZIP as 80150 (typo); corrected to La Junta's 81050"
    feats.append(f)
write_layer("Reentry_and_Transitional_Services.geojson", feats, probs)

# ---------------- Layer 12: Halfway houses & transitional housing -------------
rrc = json.load(open(os.path.join(RAW, "bop_rrc.json"), encoding="latin1"))["RRC"]
hh, probs = [], []
for r in rrc:
    if r["state"] != "CO":
        continue
    hh.append(make_feature(float(r["longitude"]), float(r["latitude"]), name=r["name"],
        category="Halfway Houses and Transitional Housing", housing_type="Federal Residential Reentry Center (BOP halfway house)",
        address=r["address"], city=r["city"].title(), zip=r["zipCode"], phone=r["phoneNum"], website=r.get("contractWebSite"),
        beds=f"{r['totalBeds']} ({r['maleBeds']} male, {r['femaleBeds']} female)", contract_expires=r["expirationDate"],
        source="Federal Bureau of Prisons RRC feed", source_url="https://www.bop.gov/PublicInfo/execute/rrc?todo=query&output=json",
        geocode="source (BOP)"))
for name, a, city, z in [("Bridge House Ready to Work - Boulder", "4747 Table Mesa Drive", "Boulder", "80305"),
                         ("Bridge House Ready to Work - Aurora", "3176 S Peoria Court", "Aurora", "80014")]:
    f, p = geocoded_feature(dict(name=name, address=a, city=city, zip=z, phone="303-575-4962",
                                 website="https://boulderbridgehouse.org/",
                                 services="Paid work + transitional housing program; WAGEES partner (Boulder, Aurora, Englewood)"),
                            "Halfway Houses and Transitional Housing", WSRC, W + "bridge-house-ready-to-work-boulder/")
    if p: probs.append(p); continue
    f["properties"]["housing_type"] = "Reentry transitional housing with employment (Ready to Work)"
    hh.append(f)
write_layer("Halfway_Houses_and_Transitional_Housing.geojson", hh, probs)
