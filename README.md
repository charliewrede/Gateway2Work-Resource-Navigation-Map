# Gateway2Work Resource Navigation Map

An interactive map of Gateway2Work resources, built from the Leaflet map template.

## The data: statewide Colorado layers

`Data/` holds 23 GeoJSON layers (1,089 locations) for the categories in TSRG's *Colorado Workforce Development Ecosystem* GIS framework: referral sources, employment service providers, employment destinations and community supports.

- **[Data/SOURCES.md](Data/SOURCES.md)**: start here. Every layer, its source, and how its locations were found.
- **`Data/sources/`**: one write-up per layer: what was searched, what was used and why, corrections, open questions.
- **[Data/sources/FOLLOW_UP.md](Data/sources/FOLLOW_UP.md)**: remaining manual steps (including L19 and L21).
- **`scripts/`**: the build scripts (Python, built-in modules only). `python3 scripts/run_all.py` rebuilds everything. Original downloads are kept in `Data/raw/`, and geocoder answers are cached in `scripts/cache/`.

Every map point's popup shows its `source`, `source_url`, `retrieved` date, and `geocode` method.

## About the template

A ready-made interactive map. It includes address search, a layer list with collapsible groups, a legend that updates as layers are switched on and off, show/hide switches, popups, hover highlights and name labels that fit inside areas. Add your own GeoJSON files and the map builds itself.

> **New to JavaScript, HTML or CSS?** Start with **[LEARNING-GUIDE.md](LEARNING-GUIDE.md)**. Every file is commented in plain language, and words tagged like **[📖 Closure]** are explained in **[GLOSSARY.md](GLOSSARY.md)**.

## Add a layer in two steps

1. Put the `.geojson` file in the `Data/` folder.
2. Open `js/config.js` and add one line to `LAYERS`:

   ```js
   export const LAYERS = [
       { file: "Parks.geojson" },
   ];
   ```

Refresh the page. The engine reads the file and fills in everything else:

| What                  | Automatic choice                                |
|-----------------------|-------------------------------------------------|
| Points, lines, areas? | Read from the file                              |
| Name in list/legend   | From the file name (`Grocery_Stores` → "Grocery Stores") |
| Color & point shape   | Picked in turn from a built-in set              |
| Popup                 | Every property with a value; web addresses become links |
| Layer list & legend   | Same order as `LAYERS`                          |
| Starting view         | Zooms to fit everything that is switched on     |

## Customize when you want to

Add settings to a layer only to change the automatic choices:

```js
{ file: "Grocery_Stores.geojson",
  label: "Grocery Stores",
  color: "#7CB342",
  shape: "diamond",          // circle, square, diamond, triangle, star, hexagon, cross, drop, book
  group: "Food Access",      // layers with the same group share a collapsible section
  visible: false,            // start switched off
  popup: POPUPS.grocery }    // a custom popup from section 4 of config.js
```

Other features:

- **Name labels inside areas:** `{ file: "Neighborhoods.geojson", type: "outline", labelField: "NBHD_NAME" }`
- **Color areas by a 0–1 score:** `type: "scorePolygons", scoreField: "SVI"`
- **Color points by a 0–1 score:** `type: "scorePoints", scoreField: "SRI_score"`
- **Numbered top-5 markers:** `type: "rankedPoints", sourceLayer: "schools", rankField: "SRI_score"`

`js/config.js` has a commented example for each one, plus optional settings for the title, start view, search area, color scale, and a hand-arranged layer list or legend.

## Run it

Browsers block data files on a page opened by double-clicking, so serve the folder instead:

- **VS Code:** right-click `index.html` → "Open with Live Server"
- **Terminal:** `python3 -m http.server 8000` in this folder, then open http://localhost:8000
- **Online:** GitHub Pages works as-is

## If something is wrong

- **A red box on the map** names each file that failed and why. The other layers still load.
- **Coordinates must be WGS84 longitude/latitude (EPSG:4326).** In ArcGIS or QGIS, export with that CRS. Data in another CRS ends up in the wrong place or doesn't appear.
- **Address search** uses a Geoapify key in `SEARCH.apiKey`. Set it to `""` to remove the search box.

## Files

```
index.html          page frame
js/config.js        ← edit this: your layers, colors, popups, search area
js/main.js          builds the map step by step
js/layers.js        loads data, fills in defaults, draws layers
js/popups.js        popup helpers (field, address, link, formatters)
js/labels.js        fits name labels inside areas
js/controls.js      layer list and show/hide switches
js/legend.js        legend
js/search.js        address search
css/styles.css      look and feel
Data/               your GeoJSON files (delete the two example-* files)
```
