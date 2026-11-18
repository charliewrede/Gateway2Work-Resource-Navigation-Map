"""
sync_tracking_log.py - copy the repo's tracking log into the SharePoint
workbook (synced to this Mac by OneDrive), without touching staff-owned
columns or formatting.

    python3 scripts/sync_tracking_log.py            # dry run: show what would change
    python3 scripts/sync_tracking_log.py --apply    # write changes (backup made first)

Source : Data/Gateway2Work_Data_Dictionary_Resource_Tracking_Log.csv (repo)
Target : the .xlsx in the OneDrive-synced SharePoint folder, found by name (WORKBOOK below)

Rules
  * Rows are matched by the "Resource" name.
  * Sheet "Resource Tracking Log": updates every column EXCEPT
    "Link to File Folder (SharePoint)" (staff-owned).
  * Sheet "Manual Verification": updates only column B ("AI Est Manual
    Verification Time + Needs") from the repo's Notes; "TODO" is never touched.
  * Cell formatting is kept (only values change).
  * Before writing, a timestamped backup is saved in scripts/backups/.
  * Needs: pip install openpyxl
"""
import csv, os, shutil, sys, time
import openpyxl
from common import find_onedrive

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_CSV = os.path.join(ROOT, "Data", "Gateway2Work_Data_Dictionary_Resource_Tracking_Log.csv")
# SharePoint: Gateway2Work Map/Data Dictionary/<WB_NAME>, found by name
# wherever OneDrive syncs it (so moving the SharePoint folder doesn't break this).
WB_NAME = "Gateway2Work_Data_Dictionary_Resource_Tracking_Log.xlsx"
WORKBOOK = find_onedrive(WB_NAME)
if not WORKBOOK:
    sys.exit(f"Could not find {WB_NAME} in any OneDrive folder on this computer.\n"
             "In SharePoint, open 'Gateway2Work Map' and click Sync (or 'Add shortcut to My files'), "
             "wait for the green check in Finder, then run this again.")
print("Workbook:", WORKBOOK)
PROTECTED = {"Link to File Folder (SharePoint)"}

apply = "--apply" in sys.argv
repo = {r["Resource"]: r for r in csv.DictReader(open(REPO_CSV, encoding="utf-8"))}
wb = openpyxl.load_workbook(WORKBOOK)
changes = []

ws = wb["Resource Tracking Log"]
hdr = [c.value for c in ws[1]]
for row in ws.iter_rows(min_row=2):
    res = row[hdr.index("Resource")].value
    if res not in repo:
        continue
    for i, h in enumerate(hdr):
        if h in PROTECTED or h not in repo[res]:
            continue
        new = repo[res][h] or None
        if (row[i].value or None) != new:
            changes.append(f"Resource Tracking Log | {res} | {h}")
            row[i].value = new
missing = set(repo) - {r[hdr.index('Resource')] for r in ws.iter_rows(min_row=2, values_only=True)}
for m in sorted(missing):
    print("  note: in repo but not in workbook (not added automatically):", m)

if "Manual Verification" in wb.sheetnames:
    mv = wb["Manual Verification"]
    for row in mv.iter_rows(min_row=2):
        res = row[0].value
        if res in repo and (row[1].value or None) != (repo[res]["Notes"] or None):
            changes.append(f"Manual Verification | {res} | AI Est Manual Verification Time + Needs")
            row[1].value = repo[res]["Notes"]

print(f"{len(changes)} cell(s) {'updated' if apply else 'would change'}:")
for c in changes:
    print("  -", c)
if apply and changes:
    bdir = os.path.join(ROOT, "scripts", "backups"); os.makedirs(bdir, exist_ok=True)
    backup = os.path.join(bdir, time.strftime("tracking_log_%Y%m%d-%H%M%S.xlsx"))
    shutil.copy2(WORKBOOK, backup)
    wb.save(WORKBOOK)
    print("Saved. Backup of previous version:", os.path.relpath(backup, ROOT))
    print("OneDrive will upload the change; check the green check in Finder or the menu-bar icon.")
elif not apply:
    print("(dry run - add --apply to write)")
