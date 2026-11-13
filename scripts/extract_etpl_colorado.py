"""
extract_etpl_colorado.py - pull Colorado rows out of the national
TrainingProviderResults.gov ETPL file (U.S. DOL, form ETA-9171 data),
https://www.trainingproviderresults.gov/data/DownloadPrograms.xlsx
-> Data/raw/etpl_CO.csv. Uses only built-in modules (xlsx = zipped XML).
"""
import csv, os, re, zipfile, xml.etree.ElementTree as ET
RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data", "raw")
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
z = zipfile.ZipFile(os.path.join(RAW, "etpl_DownloadPrograms.xlsx"))
shared = []
with z.open("xl/sharedStrings.xml") as f:
    for ev, el in ET.iterparse(f):
        if el.tag == NS + "si":
            shared.append("".join(t.text or "" for t in el.iter(NS + "t"))); el.clear()
def col(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0): n = n * 26 + ord(ch) - 64
    return n - 1
header, out, n = None, [], 0
with z.open("xl/worksheets/sheet1.xml") as f:
    for ev, el in ET.iterparse(f):
        if el.tag != NS + "row": continue
        vals = {}
        for c in el.findall(NS + "c"):
            v = c.find(NS + "v")
            if v is None:
                isv = c.find(NS + "is"); val = "".join(t.text or "" for t in isv.iter(NS + "t")) if isv is not None else ""
            else:
                val = shared[int(v.text)] if c.get("t") == "s" else v.text
            vals[col(c.get("r"))] = val
        row = [vals.get(i, "") for i in range(max(vals) + 1)] if vals else []
        el.clear(); n += 1
        if header is None:
            header = row; print("columns:", header); continue
        si, ri = header.index("state"), header.index("reportingstate")
        row += [""] * (len(header) - len(row))
        if row[ri].strip().upper() in ("CO", "COLORADO", "08") or row[si].strip().upper() == "CO":
            out.append(row)
print("rows scanned:", n, "Colorado rows:", len(out))
with open(os.path.join(RAW, "etpl_CO.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(header); w.writerows(out)
