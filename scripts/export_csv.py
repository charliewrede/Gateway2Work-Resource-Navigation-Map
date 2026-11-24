"""
export_csv.py - write a CSV copy of every GeoJSON layer.

    python3 scripts/export_csv.py

Runs automatically at the end of postprocess_county_and_accuracy.py (and so
at the end of run_all.py), so the CSVs always match the finished GeoJSON.
If you hand-edit a GeoJSON file, run this script afterwards.

Output
  data_csv/<Layer>.csv     one per Data/<Layer>.geojson, one row per point
  data_csv/All_Layers.csv  every point from every layer, with a "layer" column
  Each file is also copied to the OneDrive-synced SharePoint folder
  (a folder named "Data_CSV", found by find_onedrive in common.py) when it
  is synced on this computer. A file is only
  copied when its contents changed, so OneDrive does not re-upload unchanged files.

Columns: the popup fields first (name, category, address, city, zip, county,
location_accuracy, phone, website, services), then the layer's other
attributes, then provenance (source, source_url, retrieved, geocode,
verified), then latitude and longitude (WGS84). Encoded UTF-8 with a byte-order
mark so Excel shows accented characters correctly.
"""
import csv, glob, io, json, os
from common import DATA, ROOT, find_onedrive

OUT = os.path.join(ROOT, "data_csv")
# The SharePoint "Data_CSV" folder, found by name wherever OneDrive syncs it.
SHAREPOINT = (find_onedrive("Data_CSV", want_dir=True)
              or find_onedrive("AmeriCorps VISTA - Workforce Development for People in Recovery - Data_CSV", want_dir=True)
              or "")
FIRST = ["name", "category", "address", "city", "zip", "county", "location_accuracy",
         "phone", "website", "services"]
LAST = ["source", "source_url", "retrieved", "geocode", "verified"]


def columns(rows):
    seen = []
    for r in rows:
        for k in r:
            if k not in seen:
                seen.append(k)
    middle = [k for k in seen if k not in FIRST + LAST + ["latitude", "longitude", "layer"]]
    return ([k for k in FIRST if k in seen] + middle
            + [k for k in LAST if k in seen] + ["latitude", "longitude"])


def to_csv(rows, cols):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    return "﻿" + buf.getvalue()


def save(name, text):
    """Write to data_csv/ and, if changed, to the SharePoint folder."""
    # The SharePoint files are never read: OneDrive keeps them as cloud-only
    # placeholders, and reading one forces a download that can time out.
    # Instead, the SharePoint copy is rewritten whenever the repo copy changes
    # (or is missing from SharePoint).
    data = text.encode("utf-8")
    local = os.path.join(OUT, name)
    repo_changed = not (os.path.exists(local) and open(local, "rb").read() == data)
    copied = []
    if repo_changed:
        with open(local, "wb") as fh:
            fh.write(data)
        copied.append("repo")
    if os.path.isdir(SHAREPOINT):
        remote = os.path.join(SHAREPOINT, name)
        if repo_changed or name in PENDING or not os.path.exists(remote):
            try:
                with open(remote, "wb") as fh:
                    fh.write(data)
                PENDING.discard(name)
                copied.append("SharePoint")
            except OSError as e:
                PENDING.add(name)               # retried on the next run
                copied.append(f"SharePoint FAILED ({e.strerror}) - will retry next run")
    return copied


# Files whose SharePoint copy failed on an earlier run (e.g. OneDrive offline).
PENDING_FILE = os.path.join(OUT, ".sharepoint_pending.txt")
PENDING = set(open(PENDING_FILE).read().split("\n")) - {""} if os.path.exists(PENDING_FILE) else set()


os.makedirs(OUT, exist_ok=True)
all_rows = []
for path in sorted(glob.glob(os.path.join(DATA, "*.geojson"))):
    fname = os.path.basename(path)
    if fname.startswith("example-"):
        continue
    layer = fname[:-len(".geojson")]
    rows = []
    for f in json.load(open(path, encoding="utf-8"))["features"]:
        r = {k: ("; ".join(map(str, v)) if isinstance(v, list) else v)
             for k, v in f["properties"].items()}
        lon, lat = f["geometry"]["coordinates"][:2]
        r["latitude"], r["longitude"] = round(lat, 6), round(lon, 6)
        rows.append(r)
        all_rows.append({"layer": layer, **r})
    changed = save(layer + ".csv", to_csv(rows, columns(rows)))
    print(f"  {layer + '.csv':52} {len(rows):4} rows  {'updated: ' + ', '.join(changed) if changed else 'unchanged'}")

changed = save("All_Layers.csv", to_csv(all_rows, ["layer"] + columns(all_rows)))
print(f"  {'All_Layers.csv':52} {len(all_rows):4} rows  {'updated: ' + ', '.join(changed) if changed else 'unchanged'}")
with open(PENDING_FILE, "w") as fh:
    fh.write("\n".join(sorted(PENDING)))
if PENDING:
    print(f"  WARNING: {len(PENDING)} file(s) not copied to SharePoint yet: {', '.join(sorted(PENDING))}")
    print("           Check that OneDrive is running and online, then run: python3 scripts/export_csv.py")
if not os.path.isdir(SHAREPOINT):
    print("  note: no synced SharePoint Data_CSV folder found on this computer; wrote data_csv/ only")
else:
    print("  SharePoint copy:", SHAREPOINT)
