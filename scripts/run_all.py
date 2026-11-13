"""
run_all.py - rebuild every layer from its sources, in order.

Usage (from the project folder):   python3 scripts/run_all.py
Each build script prints how many points it wrote and any records it could
not place. Geocoding results are cached in scripts/cache/geocode_cache.json,
so re-runs are fast and reproducible.
"""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["build_07_prisons.py", "build_06_jails.py", "build_05_community_corrections.py",
         "build_04_treatment.py", "build_02_workforce_centers.py", "build_16_colleges.py",
         "build_24_veterans.py", "build_11_probation_parole.py", "build_22_legal_aid.py",
         "build_10_12_reentry_and_transitional_housing.py", "build_18_adult_education.py",
         "build_23_community_mental_health.py", "build_09_dvr.py", "build_14_recovery_residences.py",
         "build_08_ips.py", "build_01_13_15.py"]
extra = sorted(f for f in os.listdir(HERE) if f.startswith("build_") and f not in ORDER)
for script in ORDER + extra:
    t = time.time()
    print(f"\n######## {script}", flush=True)
    r = subprocess.run([sys.executable, script], cwd=HERE)
    print(f"######## {script} finished (exit {r.returncode}, {time.time()-t:.0f}s)", flush=True)
