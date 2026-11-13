# Layer 20 — Community-Based and Faith-Based Organizations

**Output:** `Data/Community_and_Faith_Based_Organizations.geojson` (13 organizations) · **Build script:** `scripts/build_20_25.py` · **Built:** 2026-11-13

## 1. How this layer was built
There's no statewide dataset of community and faith-based job-readiness organizations. The TSRG framework says categories **are not mutually exclusive**, so this layer is a **role-based selection of organizations already verified in other layers**. **No new or unverified records were added.** Each feature keeps its original source and address, and gains:
- `org_type`: Faith-based, or Community-based (with focus)
- `also_in_layer`: the layer it came from (Reentry, or Homelessness and Housing)

## 2. Included
- **Faith-based:** Loaves & Fishes Ministries (Cañon City), Cooperating Ministry of Logan County (Sterling), Denver Rescue Mission, Springs Rescue Mission, Fort Collins Rescue Mission, Catholic Charities of Denver, Pueblo Rescue Mission (address flagged).
- **Community-based:** Manna Soup Kitchen (Durango), Servicios de La Raza (Denver), The Piñon Project (Cortez), Hazelbrook Community Center (Colorado Springs), Life-Line Colorado (Denver), The Empowerment Program (Denver).

## 3. Follow-up
Statewide faith-based networks with job-readiness programs (Salvation Army Intermountain, Lutheran Family Services Rocky Mountains, Volunteers of America Colorado, Jewish Family Service of Colorado, Catholic Charities in each diocese) are good additions once each location is confirmed on the organization's own site.
