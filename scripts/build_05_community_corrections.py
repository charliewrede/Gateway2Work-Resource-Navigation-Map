"""
Layer 5 - Community Corrections (residential programs / "halfway houses"
regulated by the Colorado Division of Criminal Justice, Office of Community
Corrections)

PROVENANCE SUMMARY (full write-up: Data/sources/05_Community_Corrections.md)
  Source : DCJ Office of Community Corrections, "Community Corrections Boards,
           Program & Specialized Programs" page
           https://dcj.colorado.gov/dcj-offices/occ/corrections-boards-programs
           dcj.colorado.gov blocks automated tools (HTTP 403), so project staff
           copied the page on 2026-11-24. The copy is saved unchanged in
           Data/raw/dcj_occ_2026-11-24/ (3 files) and parsed here:
             1_boards_and_programs_1st_JD.txt        (1st JD - Gilpin and Jefferson)
             2_boards_and_programs_2nd_to_23rd_JD.txt (2nd JD - Denver through 23rd JD)
             3_specialized_programs.txt              (IRT, SOSTCC, RDDT)
           Every program on the list is mapped and no others. (Before 2026-11-24
           the layer was built from the 2017 DCJ list re-checked against operator
           sites; see git history.)
  Coords : U.S. Census geocoder (OpenStreetMap fallback); Garfield County from
           its HIFLD facility footprint (rural road address).
"""
import json, os, re
from common import RAW, geocoded_feature, write_layer, set_manual

CAT = "Community Corrections"
SRC = "Colorado Division of Criminal Justice, Office of Community Corrections - Community Corrections Boards, Program & Specialized Programs"
URL = "https://dcj.colorado.gov/dcj-offices/occ/corrections-boards-programs"
VERIFIED = "Official DCJ OCC list, copied from the DCJ page by project staff 2026-11-24"
DIR = os.path.join(RAW, "dcj_occ_2026-11-24")

# Fixes to the copied text: program name -> (field, value used, note)
FIXES = {
    "Independence House Pecos": ("zip", "80211",
        "DCJ list gives ZIP 80218; 4101 Pecos St is in ZIP 80211 (80218 is Capitol Hill)."),
    "Mesa County Community Corrections": ("zip", "81501",
        "DCJ list gives ZIP 81502 (a PO-box ZIP); the building at 650 South Ave is in 81501."),
    "Garfield County Community Corrections": (None, None,
        "DCJ list gives the program at 0224 County Rd 333A and the board at 0244 County Road 333A; "
        "placed at the facility's HIFLD footprint."),
}
# Specialized-program listings use slightly different names than the program list.
ALIASES = {
    "Larimer County Community Corrections": "Larimer County Residential Facility",
    "Mesa County Community Corrections (MCCC)": "Mesa County Community Corrections",
    "ComCor, Inc./EMBRAVE": "ComCor Inc./EMBRAVE",
    "Advantage Treatment Center (ATC) - Sterling": "Advantage Treatment Center - Sterling",
    "Advantage Treatment Center (ATC) - Alamosa": "Advantage Treatment Center - Alamosa",
    "Advantage Treatment Center (ATC) - Lamar": "Advantage Treatment Center - Lamar",
    "GEO - Community Alternatives of El Paso County (CAE)": "GEO - Community Alternatives of El Paso County, Inc",
    "CoreCivic Arapahoe Community Treatment Center (ACTC)": "CoreCivic - Arapahoe Community Treatment Center",
    "Intervention Community Corrections Services - Adams": "ICCS - Adams",
}
SPECIAL = {"Intensive Residential Treatment (IRT)": "irt",
           "Sex Offender Supervision and Treatment in Community Corrections (SOSTCC)": "sostcc",
           "Residential Dual Diagnosis Treatment (RDDT)": "rddt"}


def clean(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def split_address(a):
    """'1651 Kendall St., Lakewood, CO 80214' or '3260 Airport Rd Boulder, CO 80301'."""
    m = re.match(r"^(.*?),\s*([A-Za-z .]+),\s*CO\s+(\d{5})$", a)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3)
    m = re.match(r"^(.*\b(?:Rd|St|Ave|Dr|Road|Street|Avenue|Drive)\.?)\s+([A-Z][A-Za-z ]+),\s*CO\s+(\d{5})$", a)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3)
    raise ValueError("Can't split address: " + a)


# ------------------------------------------------------------ boards + programs
def parse_boards(text):
    """Yield one dict per program, with its district's board contact attached."""
    district, area = None, None
    board = dict(lines=[], phones=[], emails=[])
    mode, prog, out = "board", None, []
    for raw in text.splitlines():
        l = clean(raw)
        if not l:
            continue
        h = re.match(r"^(\d+)(?:st|nd|rd|th) Judicial District - (.*)$", l)
        if h:
            district, area = ordinal(int(h.group(1))), h.group(2)
            board, mode, prog = dict(lines=[], phones=[], emails=[]), "board", None
            continue
        if re.match(r"^(Referrals/)?Board Contact:?$", l):
            if l.startswith("Referrals"):
                board["referral"] = True
            mode = "board"; continue
        if re.match(r"^Programs?:?$", l):
            mode = "program"; continue
        if l.startswith("This Judicial District does not have a program"):
            continue
        if mode == "board":
            if l.lower().startswith("phone:"):
                ph = l.split(":", 1)[1].strip()
                board["phones"].append(("Referrals: " if board.get("referral") else "") + ph)
            elif l.lower().startswith("email:"):
                board["emails"].append(l.split(":", 1)[1].strip())
            elif "fax" not in l.lower():
                board["lines"].append(l)
            continue
        # program section: label lines attach to the current program, other lines start one
        m = re.match(r"^(Population Served|Phone|Address|Director|Email):\s*(.*)$", l)
        if m and prog is not None:
            prog[m.group(1).lower()] = m.group(2).strip()
        else:
            assert district, f"Program before any district heading: {l}"
            prog = dict(name=re.sub(r"(\S)- ", r"\1 - ", l), district=district, area=area, board=board)
            out.append(prog)
    return out


# ------------------------------------------------------------ specialized programs
def parse_special(text):
    """{program name: {"irt": "...", "sostcc": "...", "rddt": "..."}}"""
    res, section, cur = {}, None, None
    keys = ("Location", "Gender", "Length", "Substance Abuse", "Mental Health", "Medical",
            "Sex Offenders", "Violent Offenders", "SVP", "Outside Jurisdiction", "Additional Information")
    for raw in text.splitlines():
        l = clean(raw)
        if not l:
            continue
        if l in SPECIAL:
            section = SPECIAL[l]; continue
        m = re.match(r"^(%s)\s*[:\-]\s*(.*)$" % "|".join(map(re.escape, keys)), l)
        contact = re.match(r"^(.+?)\s*[|:]\s*(\d{3}-\d{3}-\d{4}.*)$", l)
        if m and cur is not None:
            cur["fields"][m.group(1)] = m.group(2).strip().rstrip("-").strip() or "-"
        elif contact and cur is not None:
            cur["contact"] = f"{contact.group(1).strip()}, {contact.group(2).strip()}"
        else:
            name = ALIASES.get(l, l)
            cur = dict(fields={}, contact=None)
            res.setdefault(name, {})[section] = cur
    return res


def summarize(entry):
    f = dict(entry["fields"])
    f.pop("Location", None)
    parts = [f"{k}: {v}" for k, v in f.items() if v and v != "-"]
    if entry["contact"]:
        parts.append("Contact: " + entry["contact"])
    return "; ".join(parts)


progs = (parse_boards(open(os.path.join(DIR, "1_boards_and_programs_1st_JD.txt"), encoding="utf-8").read())
         + parse_boards(open(os.path.join(DIR, "2_boards_and_programs_2nd_to_23rd_JD.txt"), encoding="utf-8").read()))
special = parse_special(open(os.path.join(DIR, "3_specialized_programs.txt"), encoding="utf-8").read())
unmatched = set(special) - {p["name"] for p in progs}
assert not unmatched, f"Specialized programs with no matching program: {unmatched}"

# Garfield County's rural road address can't be geocoded; HIFLD has the facility footprint.
_h = {f["properties"]["NAME"]: f["geometry"]["coordinates"] for f in
      json.load(open(os.path.join(RAW, "hifld_prison_points_CO.geojson")))["features"]}
_g = _h["GARFIELD COUNTY COMMUNITY CORRECTIONS FACILITY"]
set_manual("0224 County Rd. 333A, Rifle, CO 81650", _g[0], _g[1], "HIFLD Prison Boundaries footprint centroid")

feats, problems = [], []
for p in progs:
    street, city, zip_ = split_address(p["address"])
    fix_field, fix_value, fix_note = FIXES.get(p["name"], (None, None, None))
    rec = dict(name=p["name"], address=street, city=city,
               zip=fix_value if fix_field == "zip" else zip_,
               phone=p.get("phone"), verified=VERIFIED)
    f, prob = geocoded_feature(rec, CAT, SRC, URL)
    if prob:
        problems.append(prob); continue
    sp = special.get(p["name"], {})
    b = p["board"]
    extra = dict(
        population=p.get("population served"), director=p.get("director"), email=p.get("email"),
        judicial_district=p["district"], district_counties=p["area"],
        specialized_programs="; ".join(n for n, k in (("IRT", "irt"), ("SOSTCC", "sostcc"), ("RDDT", "rddt")) if k in sp) or None,
        irt=summarize(sp["irt"]) if "irt" in sp else None,
        sostcc=summarize(sp["sostcc"]) if "sostcc" in sp else None,
        rddt=summarize(sp["rddt"]) if "rddt" in sp else None,
        board_contact="; ".join(b["lines"]) or None, board_phone="; ".join(b["phones"]) or None,
        board_email="; ".join(b["emails"]) or None,
        corrections_note=fix_note)
    f["properties"].update({k: v for k, v in extra.items() if v})
    feats.append(f)

print(f"Parsed {len(progs)} programs; {len(special)} have specialized programs")
write_layer("Community_Corrections.geojson", feats, problems)
