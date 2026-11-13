"""
Layer 2 - Workforce Centers (Colorado Workforce Centers = American Job Centers)

PROVENANCE SUMMARY (full write-up: Data/sources/02_Workforce_Centers.md)
  Baseline : U.S. DOL CareerOneStop "American Job Center Finder" export for
             Colorado, May 2022 (copy hosted by fairshake.net, saved as
             Data/raw/fairshake_ajc_CO.pdf). CareerOneStop's own bulk download
             and CDLE/WCRA pages return HTTP 403 to automated tools.
  Updates  : every address re-checked against the local workforce area's own
             site or a current listing (2026-11-13). The column `address_status`
             says which.
  Coords   : U.S. Census geocoder (OpenStreetMap fallback).
"""
from common import geocoded_feature, write_layer

CAT = "Workforce Centers"
AJC2022 = "https://www.fairshake.net/pdf/onestop/CO.pdf"
CUR = "current (verified 2026)"
OLD = "from 2022 AJC list - not re-confirmed"

def c(name, address, city, zip, phone, ctype, area, src, url, status=CUR, note=None):
    return dict(name=name, address=address, city=city, zip=zip, phone=phone,
                center_type=ctype, local_area=area, source=src, source_url=url,
                address_status=status, status_note=note)

WCRA = "https://wcra.colorado.gov/contact-us"
C = [
 # ---- Adams County (local area) ----
 c("Adams County Workforce & Business Center", "11860 Pecos Street, Suite 2200", "Westminster", "80234", None,
   "Comprehensive", "Adams County", "Adams County Workforce & Business Center page", "https://adcogov.org/workforce-business-center"),
 # ---- Arapahoe/Douglas ----
 c("Arapahoe/Douglas Works! Workforce Center - Centennial", "6974 S Lima Street", "Centennial", "80112", "303-636-1160",
   "Comprehensive", "Arapahoe/Douglas", "adworks.org Workforce Center Locations", "https://adworks.org/?p=1462"),
 c("Arapahoe/Douglas Works! - Aurora Workforce Center (Altura Plaza)", "15400 E 14th Place", "Aurora", "80011", "303-636-2014",
   "Affiliate", "Arapahoe/Douglas", "adworks.org event listings (2025); Adams County page also lists this site", "https://adworks.org/?p=1462"),
 c("Arapahoe/Douglas Works! - Castle Rock Workforce Center (ACC Sturm Campus)", "4500 Limelight Avenue", "Castle Rock", "80109", "303-636-1160",
   "Affiliate", "Arapahoe/Douglas", "adworks.org (2021 announcement: moved into Arapahoe Community College Sturm Collaboration Campus)", "https://www.adworks.org/venue/castle-rock-sturm-campus/"),
 # ---- Boulder County ----
 c("Workforce Boulder County - Boulder", "2520 55th Street, Suite 100", "Boulder", "80301", "303-301-2900",
   "Comprehensive", "Boulder County", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Workforce Boulder County - Longmont", "515 Coffman Street", "Longmont", "80501", "303-301-2900",
   "Comprehensive", "Boulder County", "Workforce Boulder County Longmont office listing (search result, 2025)", "https://bouldercounty.gov/families/work/",
   "current listing (not on official page fetched)", "2022 AJC list had 1500 Kansas Ave Suite 4D; newer listing gives 515 Coffman St."),
 # ---- Broomfield ----
 c("Broomfield Workforce Center", "100 Spader Way", "Broomfield", "80020", "303-464-5855",
   "Comprehensive", "Broomfield", "City and County of Broomfield Workforce Center page", "https://broomfield.org/3818/Workforce-Center"),
 # ---- Denver ----
 c("Denver Workforce Center - Webb Building", "201 W Colfax Avenue", "Denver", "80202", None,
   "Comprehensive", "Denver", "Denver Economic Development & Opportunity, For Jobseekers page", "https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Economic-Development-Opportunity/Jobseekers-Employers/For-Jobseekers"),
 c("Denver Workforce Center - Montbello", "4685 Peoria Street, Suite 251", "Denver", "80239", "720-337-9675",
   "Comprehensive", "Denver", "Denver Economic Development & Opportunity, For Jobseekers page", "https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Economic-Development-Opportunity/Jobseekers-Employers/For-Jobseekers"),
 c("Denver Workforce Center - Denver International Airport", "8500 Pena Boulevard", "Denver", "80249", "303-342-2590",
   "Affiliate", "Denver", "Denver Economic Development & Opportunity Youth Programs page; AJC list (2022)", "https://denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Economic-Development-Opportunity/Jobseekers-Employers/For-Jobseekers/Youth-Programs"),
 c("Denver Westside Workforce Center", "1200 Federal Boulevard", "Denver", "80204", "720-944-1615",
   "Comprehensive", "Denver", "CareerOneStop AJC list (May 2022)", AJC2022, OLD,
   "Reported temporarily closed for reconstruction until early 2026. Confirm reopening."),
 # ---- Jefferson / Gilpin / Clear Creek (Tri-County) ----
 c("Jefferson County Business & Workforce Center (Workforce Colorado)", "3500 Illinois Street, Suite 1600", "Golden", "80401", "303-271-4755",
   "Comprehensive", "Tri-County (Jefferson, Gilpin, Clear Creek)", "Jefferson County directory - Workforce Colorado", "https://www.jeffco.us/Directory.aspx?did=68"),
 c("Gilpin County Workforce Center", "2960 Dory Hill Road, Suite 100", "Black Hawk", "80422", "303-582-6003",
   "Comprehensive", "Tri-County (Jefferson, Gilpin, Clear Creek)", "Jefferson County Business & Workforce Center listing; AJC list (2022)", "https://www.jeffco.us/Business-Workforce-Center"),
 c("Clear Creek County Workforce Center", "1531 Colorado Boulevard", "Idaho Springs", "80452", "303-670-7548",
   "Affiliate", "Tri-County (Jefferson, Gilpin, Clear Creek)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 # ---- Larimer ----
 c("Larimer County Economic & Workforce Development", "200 W Oak Street, Suite 5000", "Fort Collins", "80521", "970-498-6600",
   "Comprehensive", "Larimer County", "Larimer County Economic and Workforce Development page", "https://www.larimer.gov/ewd",
   note="Loveland: no daily staff; appointments at Loveland Public Library (county page)."),
 # ---- Mesa ----
 c("Mesa County Workforce Center", "512 29 1/2 Road", "Grand Junction", "81504", "970-248-0871",
   "Comprehensive", "Mesa County", "Mesa County Workforce Center contact page", "https://www.mesacounty.us/departments-and-services/wfc/contact-information"),
 # ---- Pikes Peak (El Paso, Teller) ----
 c("Pikes Peak Workforce Center", "1675 Garden of the Gods Road, Suite 1118", "Colorado Springs", "80907", "719-667-3700",
   "Comprehensive", "Pikes Peak (El Paso, Teller)", "Visit COS directory; apprenticeship listing; AJC list (2022)", "https://www.visitcos.com/directory/pikes-peak-workforce-center/"),
 c("Pikes Peak Workforce Center - Fountain (Peak Vista Health Center)", "350 Lyckman Drive", "Fountain", "80817", "719-444-8311",
   "Affiliate", "Pikes Peak (El Paso, Teller)", "Directory listing (2025) and AJC list (2022) agree", AJC2022),
 c("Pikes Peak Workforce Center - Calhan (Community Outreach Center)", "328 10th Street", "Calhan", "80808", "719-520-7895",
   "Affiliate", "Pikes Peak (El Paso, Teller)", "Third-party directory listing (2025)", "https://www.visitcos.com/directory/pikes-peak-workforce-center/",
   "third-party listing only"),
 c("Aspen Mine Center (Teller County workforce services)", "166 E Bennett Avenue", "Cripple Creek", "80813", "719-689-3584",
   "Affiliate", "Pikes Peak (El Paso, Teller)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 # ---- Weld ----
 c("Weld County Workforce Center - Greeley", "315 N 11th Avenue, Building B", "Greeley", "80631", "970-400-3800",
   "Comprehensive", "Weld County", "Weld County Employment Services page", "https://www.weld.gov/Government/Departments/Human-Services/Employment-Services"),
 c("Weld County Workforce Center - Fort Lupton", "2950 9th Street", "Fort Lupton", "80621", "303-857-2725",
   "Affiliate", "Weld County", "Weld County Employment Services page", "https://www.weld.gov/Government/Departments/Human-Services/Employment-Services"),
 # ---- Rural Consortium (Workforce Colorado Rural Alliance, WCRA) ----
 c("Pueblo Workforce Center", "1045 W 6th Street", "Pueblo", "81003", "719-562-3731",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA/CRWC contact page; Pueblo County Human Services page", WCRA,
   note="2022 AJC list had 212 W 3rd St (old address)."),
 c("Alamosa Workforce Center", "305 Murphy Drive, Unit B", "Alamosa", "81101", "719-589-5118",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA contact page", WCRA, note="2022 AJC list had 407 State Ave Suite C."),
 c("Monte Vista Workforce Center", "2079 Sherman Avenue", "Monte Vista", "81144", "719-852-5171",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("San Luis Satellite Workforce Center", "303 Vega Street", "San Luis", "81152", "719-672-3310",
   "Affiliate", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Burlington Workforce Center", "420 S 14th Street, Suite B", "Burlington", "80807", "719-346-5331",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA listing and AJC list (2022) agree", WCRA),
 c("Limon Workforce Center", "285 D Avenue", "Limon", "80828", "719-775-2387",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD,
   "One newer listing gives 333 M Avenue Suite 300. Confirm."),
 c("Elizabeth Workforce Center", "240 Elizabeth Street, Suite A1", "Elizabeth", "80107", "303-646-2783",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Fort Morgan Workforce Center", "426 Ensign Street", "Fort Morgan", "80701", "970-867-9401",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA Northeast listing (2025) and AJC list agree", WCRA),
 c("Sterling Workforce Center", "100 College Avenue", "Sterling", "80751", "970-522-9340",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD,
   "WCRA now says 'inside the CSU Engagement Center', by appointment; a mapping listing shows a temporary move to 304 Main St. Confirm location."),
 c("Yuma Workforce Center", "529 N Albany Street, Suite 1210", "Yuma", "80759", "970-848-3760",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA contact page (by appointment only)", WCRA),
 c("Lamar Workforce Center", "405 E Olive Street", "Lamar", "81052", "719-336-2256",
   "Comprehensive", "Rural Consortium (WCRA)", "CDLE workforce centers page and AJC list agree", "https://cdle.colorado.gov/jobs-training/workforce-centers"),
 c("La Junta Workforce Center", "17 W 4th Street", "La Junta", "81050", "719-383-3191",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA relocation notice (new location on 4th St); mapping listing gives 17 W 4th St", WCRA,
   "listing (relocated)", "Old address 308 Santa Fe Ave."),
 c("Rocky Ford - Southeast Colorado Workforce Center", "801 Chestnut Avenue", "Rocky Ford", "81067", "719-254-3397",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Trinidad Workforce Center", "140 N Commercial Street", "Trinidad", "81082", "719-846-9221",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022); WCRA lists Trinidad", AJC2022, OLD),
 c("Walsenburg Workforce Center (satellite)", "928 Russell Avenue", "Walsenburg", "81089", "719-738-2372",
   "Affiliate", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022); WCRA lists as satellite, by appointment", AJC2022, OLD),
 c("Canon City Workforce Center", "3224B Independence Road", "Canon City", "81212", "719-275-7408",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA phone listing; CDLE page and AJC list agree on address", WCRA,
   note="A CDLE page noted a temporary closure with virtual appointments. Confirm status."),
 c("Salida Workforce Center", "7405 W Highway 50, Suite 122", "Salida", "81201", "719-530-5980",
   "Affiliate", "Rural Consortium (WCRA)", "CDLE workforce centers page (newest source)", "https://cdle.colorado.gov/jobs-training/workforce-centers",
   note="2022 AJC list had 448 E 1st St Suite 201."),
 c("Leadville Workforce Center", "901 S Highway 24", "Leadville", "80461", "719-486-2428",
   "Affiliate", "Rural Consortium (WCRA)", "CDLE page + Leadville Workforce Center booking page (New Discovery Building, CMC)", "https://leadville-workforce-center.youcanbook.me/",
   note="2022 AJC list had 115 W 6th St."),
 c("Gunnison Workforce Center", "109 E Georgia Avenue", "Gunnison", "81230", "970-641-0031",
   "Affiliate", "Rural Consortium (WCRA)", "WCRA phone listing; CDLE page and AJC list agree", WCRA),
 c("Delta Workforce Center", "206 Ute Avenue", "Delta", "81416", "970-874-5781",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA phone listing; CDLE page and AJC list agree", WCRA),
 c("Montrose Workforce Center", "504 N 1st Street", "Montrose", "81401", "970-249-7783",
   "Comprehensive", "Rural Consortium (WCRA)", "Raising Colorado Kids listing; AJC list (2022)", "https://raisingcoloradokids.com/en/services/workforce-center-montrose-office/"),
 c("Durango - Southwest Colorado Workforce Center", "331 S Camino del Rio, Suite C", "Durango", "81303", "970-247-0308",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA phone listing; AJC list and unemployment office listing agree", WCRA,
   note="One listing gives 160 Rock Point Drive Suite A. Confirm."),
 c("Cortez Workforce Center", "22 W North Street", "Cortez", "81321", "970-565-3759",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA listing (moved downtown)", WCRA, note="2022 AJC list had 2208 E Main St."),
 c("Glenwood Springs Workforce Center", "401 23rd Street, Suite 300", "Glenwood Springs", "81601", "970-945-8638",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA contact page", WCRA),
 c("Rifle Workforce Center", "216 W 3rd Street", "Rifle", "81650", "970-625-5627",
   "Affiliate", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Craig Workforce Center", "480 Barclay Street", "Craig", "81625", "970-824-3246",
   "Comprehensive", "Rural Consortium (WCRA)", "WCRA contact page", WCRA),
 c("Meeker Workforce Center", "345 Market Street", "Meeker", "81641", "970-878-4211",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Rangely Workforce Center (Colorado Northwestern Community College)", "500 Kennedy Drive", "Rangely", "81648", "970-675-5072",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Steamboat Springs Workforce Center", "425 Anglers Drive, Suite D-2", "Steamboat Springs", "80487", "970-879-3075",
   "Comprehensive", "Rural Consortium (WCRA)", "Steamboat Magazine/state listing; AJC list (2022)", "https://sbs-workforce-center.youcanbook.me/"),
 c("Granby Workforce Center", "469 E Topaz Avenue", "Granby", "80446", "970-887-1857",
   "Comprehensive", "Rural Consortium (WCRA)", "CareerOneStop AJC list (May 2022)", AJC2022, OLD),
 c("Frisco Workforce Center", "360 Peak One Drive, Suite 370", "Frisco", "80443", "970-668-5360",
   "Comprehensive", "Rural Consortium (WCRA)", "Summit Chamber listing (links to wcra.colorado.gov); CDLE page", "https://www.summitchamber.org/connections/78594-frisco-workforce-center-colorado-workforce/",
   note="Serves Summit, Grand and Lake counties. 2022 AJC list had 602 Galena St."),
 c("Edwards Workforce Center", "69 Edwards Access Road, Suite 9", "Edwards", "81632", "970-926-4440",
   "Comprehensive", "Rural Consortium (WCRA)", "Mapping listing linked to CDLE; AJC list (2022)", WCRA,
   note="WCRA contact page says by appointment / temporarily closed. Confirm status."),
]

feats, problems = [], []
for r in C:
    meta = {k: r.pop(k) for k in ["center_type", "local_area", "address_status", "status_note"]}
    f, prob = geocoded_feature(r, CAT, r["source"], r["source_url"])
    if prob:
        problems.append(prob); continue
    f["properties"].update({k: v for k, v in meta.items() if v})
    feats.append(f)
write_layer("Workforce_Centers.geojson", feats, problems)
