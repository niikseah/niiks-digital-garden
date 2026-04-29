# HeyMax map (`map.js`)

Browser-side map for browsing trip locations. It uses [Leaflet](https://leafletjs.com/) with CARTO *Voyager* raster tiles and loads places from `locations.json` next to the page.

All map UI assets live in this **`map/`** directory (`map.html`, `map.js`, data, pins, branding).

## How to run

The map needs a small **local web server** (opening the HTML file directly won’t work). Use **Terminal**, and make sure you’re inside the **Heymax-Planner** folder (the one that contains `map/`) before step 2—for example:

```bash
cd ~/Desktop/heymax/Heymax-Planner
```

Then:

1. **Get your IP address** (macOS):

   ```bash
   ipconfig getifaddr en0
   ```

   Use the number it prints as `<ipaddr>` (for example `192.168.0.12`).

2. **Start the server:**

   ```bash
   python3 -m http.server 8080
   ```

   Leave this window open while you use the map. Press **Ctrl+C** when you’re done to stop it.

3. **Open the map** in a browser (use the same Wi‑Fi as this computer if you’re on a phone or tablet):

   **`http://<ipaddr>:8080/map/map.html`**

   Example: if step 1 printed `192.168.0.12`, open `http://192.168.0.12:8080/map/map.html`.

**On this Mac only**, you can skip the IP and use `http://localhost:8080/map/map.html` instead.

## Data: `locations.json`

Fetched at `./locations.json` (no cache), next to `map.js`. Supported shapes:

- A JSON **array** of location objects, or
- An object with a **`locations`** array (other top-level fields like `trip_id` are ignored by the map).

Each location should include:

| Field | Required | Notes |
|--------|----------|--------|
| `lat`, `lng` | Yes | Numbers; invalid pairs are skipped |
| `name` | Recommended | Shown in popups and search |
| `category` | Optional | Normalized into **food** (includes shopping) or **attractions** (default) |
| `address` | Optional | |
| `openingHours` or `opening_hours` | Optional | |
| `phone` | Optional | |
| `website` | Optional | `http(s)://` added if missing |

## Behavior (summary)

- **Default view:** Singapore-ish center, zoom 12 (see `DEFAULT_VIEW` in `map.js`).
- **Categories:** Filter toggles for Food/Shopping vs Attractions; colors and pin art match category.
- **Pins:** PNGs under `./pins/` (relative to `map.js`). Unknown categories fall back to small colored dots.
- **Clustering:** At zoom ≤ 13, nearby markers in view are grouped into count bubbles; clicking a cluster zooms to fit its members.
- **Search:** Filters the in-memory list by name/address substring (case-insensitive).
- **Status line:** `map.js` calls `setStatus()` which targets `#status` if present; the current `map.html` does not define that element, so status messages are optional/no-op unless you add `<div id="status" …>`.

## Related files

| File / path | Role |
|-------------|------|
| `map.html` | Page shell, styles, Leaflet, loads `map.js` |
| `map.js` | Map logic, markers, clustering, search, filters |
| `locations.json` | Location data |
| `pins/` | Pin images for categories |
| `logo/`, `heymax.png` | Brand images referenced by `map.html` |

For regenerating or syncing `locations.json`, see `../location_parser.py` in the parent folder if you use that workflow.
