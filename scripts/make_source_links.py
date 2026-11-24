"""
make_source_links.py - write Data/SOURCE_LINKS.md: every source and link used
on the map, layer by layer in framework order (1-25).

    python3 scripts/make_source_links.py

Read straight from the finished GeoJSON (each point's "source" and
"source_url"), so it always matches the data. Runs at the end of run_all.py.
"""
import collections, json, os
from common import DATA

LAYERS = [
    (1, "Recovery-Friendly Employers", "Recovery_Friendly_Employers", "01_Recovery_Friendly_Employers.md"),
    (2, "Workforce Centers", "Workforce_Centers", "02_Workforce_Centers.md"),
    (3, "Workforce Development Training Providers", "Workforce_Development_Training_Providers", "03_Workforce_Development_Providers.md"),
    (4, "Substance Use and Mental Health Treatment", "Substance_Use_and_Mental_Health_Treatment", "04_Treatment_and_Mental_Health.md"),
    (5, "Community Corrections", "Community_Corrections", "05_Community_Corrections.md"),
    (6, "Jails", "Jails", "06_Jails.md"),
    (7, "Prisons", "Prisons", "07_Prisons.md"),
    (8, "IPS Agencies", "IPS_Agencies", "08_IPS.md"),
    (9, "DVR Offices", "DVR_Offices", "09_DVR.md"),
    (10, "Reentry and Transitional Services", "Reentry_and_Transitional_Services", "10_Reentry.md"),
    (11, "Probation and Parole Offices", "Probation_and_Parole_Offices", "11_Probation_and_Parole.md"),
    (12, "Halfway Houses and Transitional Housing", "Halfway_Houses_and_Transitional_Housing", "12_Halfway_Houses.md"),
    (13, "Recovery Community Organizations", "Recovery_Community_Organizations", "13_Recovery_Community_Organizations.md"),
    (14, "Recovery Residences (by city)", "Recovery_Residences_by_City", "14_Recovery_Residences.md"),
    (15, "Homelessness and Housing Services", "Homelessness_and_Housing_Services", "15_Homelessness.md"),
    (16, "Community Colleges and Technical Schools", "Community_Colleges_and_Technical_Schools", "16_Community_Colleges_and_Technical_Schools.md"),
    (17, "Apprenticeship Programs", "Apprenticeship_Programs", "17_Apprenticeship.md"),
    (18, "Adult Education and GED Programs", "Adult_Education_and_GED_Programs", "18_Adult_Education.md"),
    (19, "Human Services (county)", None, "19_and_21_NOT_YET_BUILT.md"),
    (20, "Community and Faith-Based Organizations", "Community_and_Faith_Based_Organizations", "20_Community_and_Faith_Based.md"),
    (21, "Staffing Agencies / Second-Chance Employers", None, "19_and_21_NOT_YET_BUILT.md"),
    (22, "Legal Aid and Record Sealing", "Legal_Aid_and_Record_Sealing", "22_Legal_Aid.md"),
    (23, "Community Mental Health Providers", "Community_Mental_Health_Providers", "23_Community_Mental_Health.md"),
    (24, "Veterans Employment and Reentry", "Veterans_Employment_and_Reentry", "24_Veterans.md"),
    (25, "Social Enterprises and Transitional Employment", "Social_Enterprises_and_Transitional_Employment", "25_Social_Enterprises.md"),
]


def cell(s):
    return str(s or "").replace("|", "\\|").replace("\n", " ")


out = ["# Source links, layer by layer",
       "",
       "Every source and link behind the map points, in framework order (layers 1-25).",
       "Generated from the GeoJSON by `scripts/make_source_links.py`; do not edit by hand.",
       "For how each source was found, checked and corrected, open the layer's write-up.",
       ""]
total_pts = total_src = 0
for num, title, layer, writeup in LAYERS:
    out.append(f"## {num}. {title}")
    out.append(f"Write-up: [sources/{writeup}](sources/{writeup})")
    out.append("")
    if layer is None:
        out += ["**Not built yet** - see the write-up for why and what is needed.", ""]
        continue
    feats = json.load(open(os.path.join(DATA, layer + ".geojson"), encoding="utf-8"))["features"]
    groups = collections.defaultdict(list)
    for f in feats:
        p = f["properties"]
        groups[(p.get("source"), p.get("source_url"))].append(p.get("name"))
    out += [f"`{layer}.geojson` - {len(feats)} points, {len(groups)} source(s)", "",
            "| # | Source | Link | Points | Used for |", "|---|---|---|---|---|"]
    for i, ((src, url), names) in enumerate(sorted(groups.items(), key=lambda g: (-len(g[1]), g[0][0] or "")), 1):
        used = "(all points in this group)" if len(names) > 3 else "; ".join(cell(n) for n in names)
        link = f"[{cell(url)}]({url})" if url else ""
        out.append(f"| {i} | {cell(src)} | {link} | {len(names)} | {used} |")
    out.append("")
    total_pts += len(feats); total_src += len(groups)
out.insert(5, f"**Totals:** {total_pts} points, {total_src} distinct source/link pairs across 23 built layers.")
out.insert(6, "")
open(os.path.join(DATA, "SOURCE_LINKS.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"Wrote Data/SOURCE_LINKS.md ({total_pts} points, {total_src} source/link pairs)")
