"""
Layer 5 - Community Corrections (residential programs / "halfway houses"
regulated by the Colorado Division of Criminal Justice, Office of Community
Corrections)

PROVENANCE SUMMARY (full write-up: Data/sources/05_Community_Corrections.md)
  Baseline list : DCJ OCC "Colorado Community Corrections Programs 02-13-2017"
                  (Data/raw/dcj_occ_residential_program_list_2017-02-13.pdf)
  Current status: each program re-checked against the operator's own website
                  or the county Community Corrections Board page (2026-11-13).
                  The DCJ current program page (dcj.colorado.gov) blocks
                  automated access, so it was used only through search results.
  Coordinates   : U.S. Census geocoder.
"""
from common import geocoded_feature, write_layer, set_manual

CAT = "Community Corrections"
DCJ2017 = "https://cdpsdocs.state.co.us/occ/Programs/Updated-ResidentialProgramList-021317.pdf"

P = [
 # ---- 1st JD (Jefferson/Gilpin) - ICCS (int-cjs.org/locations; Jeffco Community Corrections page)
 dict(name="ICCS - Kendall (Intervention Community Corrections Services)", address="1651 Kendall Street", city="Lakewood", zip="80214", county="Jefferson",
      phone="303-232-4002", operator="Intervention Community Corrections Services (nonprofit)", judicial_district="1st",
      source="ICCS locations page; Jefferson County Community Corrections page", source_url="https://int-cjs.org/locations"),
 dict(name="ICCS - West (Intervention Community Corrections Services)", address="11500 W Security Avenue", city="Lakewood", zip="80215", county="Jefferson",
      phone="303-407-6200", operator="Intervention Community Corrections Services (nonprofit)", judicial_district="1st",
      source="ICCS locations page; Jefferson County Community Corrections page", source_url="https://int-cjs.org/locations"),
 # ---- 2nd JD (Denver) - City and County of Denver Community Corrections Facilities page
 dict(name="MOORE Center (Men Overcoming Obstacles Reentry Center)", address="570 W 44th Avenue", city="Denver", zip="80216", county="Denver",
      phone="720-913-8243", operator="City and County of Denver with Second Chance Center", population="Adult men", judicial_district="2nd",
      source="City and County of Denver, Community Corrections Facilities page",
      source_url="https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Department-of-Public-Safety/Community-Corrections/Residential-Programs/Community-Corrections-Facilities"),
 dict(name="Project: Elevate", address="4280 Kearney Street", city="Denver", zip="80216", county="Denver",
      phone="720-337-2240", operator="City and County of Denver with The Empowerment Program", population="Adult women", judicial_district="2nd",
      source="City and County of Denver, Community Corrections Facilities page",
      source_url="https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Department-of-Public-Safety/Community-Corrections/Residential-Programs/Community-Corrections-Facilities"),
 dict(name="IMPACT Center", address="10500 E Smith Road", city="Denver", zip="80239", county="Denver",
      phone="720-913-3825", operator="City and County of Denver", population="Adult men", judicial_district="2nd",
      source="City and County of Denver, Community Corrections Facilities page",
      source_url="https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Department-of-Public-Safety/Community-Corrections/Residential-Programs/Community-Corrections-Facilities"),
 dict(name="Independence House - Pecos", address="4101 Pecos Street", city="Denver", zip="80211", county="Denver",
      operator="Independence House Inc. (nonprofit)", population="Adult men", judicial_district="2nd",
      source="City and County of Denver, Community Corrections Facilities page",
      source_url="https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Department-of-Public-Safety/Community-Corrections/Residential-Programs/Community-Corrections-Facilities"),
 # ---- 4th JD (El Paso/Teller) - El Paso County Justice Services page + embrave.org/facilities
 dict(name="Embrave - Roberts Road Residential Facility", address="3615 Roberts Road", city="Colorado Springs", zip="80907", county="El Paso",
      phone="719-473-3033", operator="Embrave (formerly ComCor Inc., nonprofit)", judicial_district="4th",
      source="Embrave facilities page; El Paso County Justice Services Community Corrections page", source_url="https://embrave.org/facilities"),
 dict(name="Embrave - 3950 Residential Facility", address="3950 N Nevada Avenue", city="Colorado Springs", zip="80907", county="El Paso",
      phone="719-260-8002", operator="Embrave (formerly ComCor Inc., nonprofit)", judicial_district="4th",
      source="Embrave facilities page", source_url="https://embrave.org/facilities"),
 dict(name="Community Alternatives of El Paso County (CAE)", address="2945 E Las Vegas Street", city="Colorado Springs", zip="80906", county="El Paso",
      phone="719-318-5586", operator="GEO Group (GEO Reentry)", judicial_district="4th",
      source="El Paso County Justice Services Community Corrections page", source_url="https://justiceservices.elpasoco.com/community-corrections/"),
 # ---- 6th JD (La Plata) - Hilltop House
 dict(name="Hilltop House", address="1050 Avenida Del Sol", city="Durango", zip="81301", county="La Plata",
      phone="970-247-1342", operator="Southwest Colorado Community Corrections Center Inc. (nonprofit)", judicial_district="6th",
      source="DCJ 2017 program list; ColoradoGives nonprofit profile; Feb 2025 job posting confirms operating",
      source_url="https://www.coloradogives.org/organization/Southwest-Colorado-Community-Corrections-Center"),
 # ---- 7th JD (Montrose) / 12th (SLV) / 13th (Sterling) / 15th (Lamar) - Advantage Treatment Centers
 dict(name="Advantage Treatment Centers - Montrose", address="1230 N Grand Avenue", city="Montrose", zip="81401", county="Montrose",
      phone="970-964-2777", operator="Advantage Treatment Centers Inc.", judicial_district="7th",
      source="Advantage Treatment Centers location page (lists community corrections in Montrose, Lamar, Alamosa, Sterling)",
      source_url="https://atreatmentcenters.com/montrose-co/"),
 dict(name="Advantage Treatment Centers - Alamosa (San Luis Valley Community Corrections)", address="2017 Lava Lane", city="Alamosa", zip="81101", county="Alamosa",
      phone="719-589-7500", operator="Advantage Treatment Centers Inc.", judicial_district="12th",
      source="Advantage Treatment Centers location page; DCJ 2017 list had SLV Community Corrections at 2255 Lava Lane",
      source_url="https://atreatmentcenters.com/alamosa-co/"),
 dict(name="Advantage Treatment Centers - Sterling", address="12220 Highway 61", city="Sterling", zip="80751", county="Logan",
      phone="970-522-7383", operator="Advantage Treatment Centers Inc.", judicial_district="13th",
      source="Advantage Treatment Centers location page", source_url="https://atreatmentcenters.com/sterling-co/"),
 dict(name="Advantage Treatment Centers - Lamar", address="800 E Maple Street", city="Lamar", zip="81052", county="Prowers",
      phone="719-336-0650", operator="Advantage Treatment Centers Inc.", judicial_district="15th",
      source="Advantage Treatment Centers location page", source_url="https://atreatmentcenters.com/lamar-co/"),
 # ---- 8th JD (Larimer) - Larimer County Community Justice Alternatives
 dict(name="Larimer County Community Corrections (Residential)", address="2255 Midpoint Drive", city="Fort Collins", zip="80525", county="Larimer",
      phone="970-498-7530", operator="Larimer County Community Justice Alternatives (county)", population="Men and women (434-bed capacity, 2025)", judicial_district="8th",
      source="Larimer County Community Corrections 2025 Annual Report", source_url="https://www.larimer.gov/cja/comcor/annual-report"),
 # ---- 9th JD (Garfield) - Garfield County Criminal Justice Services
 dict(name="Garfield County Community Corrections", address="0244 County Road 333A", city="Rifle", zip="81650", county="Garfield",
      phone="970-625-0334", operator="Garfield County (county)", population="Men and women, 60 beds", judicial_district="9th",
      source="Garfield County Criminal Justice Services (2026 residential handbook; PREA report 2025-26)",
      source_url="https://www.garfieldcountyco.gov/criminal-justice"),
 # ---- 10th JD (Pueblo) - ICCS
 dict(name="ICCS - Pueblo (Intervention Community Corrections Services)", address="1901 N Hudson Avenue", city="Pueblo", zip="81001", county="Pueblo",
      phone="719-569-3020", operator="Intervention Community Corrections Services (nonprofit)", judicial_district="10th",
      source="ICCS locations page", source_url="https://int-cjs.org/locations"),
 # ---- 14th JD (Moffat/Routt/Grand) - CAPS
 dict(name="Correctional Alternative Placement Services (CAPS)", address="445 Ranney Street", city="Craig", zip="81625", county="Moffat",
      phone="970-824-8166", operator="GEO Group (GEO Reentry)", judicial_district="14th",
      source="DCJ 2017 program list; reentry directory listing updated 2025-07-21 (third-party)",
      source_url=DCJ2017,
      status_note="No official 2024-26 source found confirming current operation; confirm with 14th JD Community Corrections Board."),
 # ---- 17th JD (Adams/Broomfield) - Adams County Community Corrections page + operators
 dict(name="ICCS - Adams County Opportunity Center", address="8031 I-76 Frontage Road", city="Henderson", zip="80640", county="Adams",
      phone="720-523-7463", operator="Intervention Community Corrections Services (nonprofit)", population="Men and women, 184 beds", judicial_district="17th",
      source="Adams County Community Corrections page; ICCS locations page", source_url="https://adamscountyco.gov/our-county/community-safety-wellbeing/community-corrections/"),
 dict(name="CoreCivic - Adams Transitional Center (Time to Change)", address="1450 E 62nd Avenue", city="Denver", zip="80216", county="Adams",
      phone="720-377-0900", operator="CoreCivic (private)", population="Men, 102 beds", judicial_district="17th",
      source="CoreCivic facility page; Adams County Community Corrections page", source_url="https://www.corecivic.com/facilities/adams-transitional-center"),
 dict(name="CoreCivic - Commerce Transitional Center", address="4901 Krameria Street", city="Commerce City", zip="80022", county="Adams",
      phone="720-407-8061", operator="CoreCivic (private)", population="Men, 136 beds", judicial_district="17th",
      source="CoreCivic facility page; Adams County Community Corrections page", source_url="https://www.corecivic.com/facilities/commerce-transitional-center"),
 # ---- 18th JD (Arapahoe) - CoreCivic + GEO
 dict(name="CoreCivic - Arapahoe Community Treatment Center", address="3265 W Girard Avenue", city="Englewood", zip="80110", county="Arapahoe",
      phone="303-761-7685", operator="CoreCivic (private)", judicial_district="18th",
      source="CoreCivic facility page", source_url="https://www.corecivic.com/facilities/arapahoe-community-treatment-center"),
 dict(name="CoreCivic - Centennial Community Transition Center", address="14485 E Fremont Avenue", city="Englewood", zip="80112", county="Arapahoe",
      phone="303-627-0987", operator="CoreCivic (private)", judicial_district="18th",
      source="CoreCivic facility page", source_url="https://www.corecivic.com/facilities/centennial-community-transition-center"),
 dict(name="Arapahoe County Residential Center (ACRC)", address="2135 W Chenango Avenue", city="Littleton", zip="80120", county="Arapahoe",
      phone="303-795-6975", operator="GEO Group (GEO Reentry) - one directory says CoreCivic; not on CoreCivic's own facility list", judicial_district="18th",
      source="DCJ 2017 program list; Remerg/GEO listing; reentry directory updated 2025-07-21",
      source_url="https://remerg.com/resources/geo-arapahoe-county-residential-center/",
      status_note="Operator reported inconsistently; confirm with 18th JD Community Corrections Board."),
 # ---- 19th JD (Weld) - ICCS
 dict(name="ICCS - Weld (Intervention Community Corrections Services)", address="1101 H Street", city="Greeley", zip="80631", county="Weld",
      phone="970-584-2520", operator="Intervention Community Corrections Services (nonprofit)", judicial_district="19th",
      source="Weld County Community Corrections page; ICCS locations page", source_url="https://weld.gov/government/departments/justice-services/community-corrections"),
 # ---- 20th JD (Boulder) - Boulder County Halfway Houses page
 dict(name="ICCS - Boulder (formerly Boulder Community Treatment Center)", address="1770 21st Street", city="Boulder", zip="80302", county="Boulder",
      phone="303-449-2539", operator="Intervention Community Corrections Services (nonprofit)", judicial_district="20th",
      source="Boulder County Community Justice Services - Halfway Houses page", source_url="https://bouldercounty.gov/safety/community-justice-services/community-corrections/halfway-houses/"),
 dict(name="CoreCivic - Longmont Community Treatment Center", address="236 Main Street", city="Longmont", zip="80501", county="Boulder",
      phone="303-651-7071", operator="CoreCivic (private)", judicial_district="20th",
      source="Boulder County Halfway Houses page; CoreCivic facility page", source_url="https://www.corecivic.com/facilities/longmont-community-treatment-center"),
 # ---- 21st JD (Mesa) - Mesa County Criminal Justice Services
 dict(name="Mesa County Community Corrections (Residential Services)", address="650 South Avenue", city="Grand Junction", zip="81501", county="Mesa",
      phone="970-244-3301", operator="Mesa County Criminal Justice Services (county)", population="Men and women", judicial_district="21st",
      source="Mesa County Criminal Justice Services contact page", source_url="https://www.mesacounty.us/departments-and-services/criminal-justice-services/contact-information-cjsd"),
]

# Garfield County's rural road address can't be geocoded; HIFLD has the
# facility footprint ("GARFIELD COUNTY COMMUNITY CORRECTIONS FACILITY").
import json, os
from common import RAW
_h = {f["properties"]["NAME"]: f["geometry"]["coordinates"] for f in
      json.load(open(os.path.join(RAW, "hifld_prison_points_CO.geojson")))["features"]}
_g = _h["GARFIELD COUNTY COMMUNITY CORRECTIONS FACILITY"]
set_manual("0244 County Road 333A, Rifle, CO 81650", _g[0], _g[1],
           "HIFLD Prison Boundaries footprint centroid")

feats, problems = [], []
for r in P:
    meta = {k: r.pop(k) for k in ["operator", "population", "judicial_district", "status_note"] if k in r}
    f, prob = geocoded_feature(r, CAT, r["source"], r["source_url"])
    if prob:
        problems.append(prob)
        continue
    f["properties"].update({k: v for k, v in meta.items() if v})
    feats.append(f)

write_layer("Community_Corrections.geojson", feats, problems)
