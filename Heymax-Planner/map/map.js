const DEFAULT_VIEW = { center: [1.3521, 103.8198], zoom: 12 };

const CATEGORY_COLORS = {
  food: "#f97316",
  attractions: "#3b82f6",
};

const CATEGORY_ORDER = ["food", "attractions"];

const PIN_BASE_URL = new URL("./pins/", import.meta.url).href;

function normalizeCategory(input) {
  return String(input ?? "")
    .trim()
    .toLowerCase()
    .replaceAll("&", "and")
    .replaceAll("/", " ")
    .replace(/\s+/g, "_");
}

function categoryKeyFromRaw(rawCategory) {
  const key = normalizeCategory(rawCategory);
  if (key === "food" || key === "shopping") return "food";
  if (key === "attractions") return "attractions";
  return "attractions";
}

function categoryDisplayName(categoryKey) {
  const key = normalizeCategory(categoryKey);
  if (key === "food") return "Food/Shopping";
  return "Attractions";
}

const iconCache = new Map();
function getCategoryIcon(category) {
  const key = normalizeCategory(category) || "other";
  if (iconCache.has(key)) return iconCache.get(key);

  const PIN_FILES = {
    food: { unselected: "food_unselected.png", selected: "food_selected.png.png" },
    attractions: { unselected: "attractions_unselected.png", selected: "attractions_selected.png" },
  };

  const targetIconHeight = 44;
  const PIN_DIMS = {
    selected: { w: 200, h: 287 },
    unselected: { w: 230, h: 317 },
  };

  const pin = PIN_FILES[key];
  if (pin?.unselected) {
    const sizeUn = {
      w: Math.round(PIN_DIMS.unselected.w * (targetIconHeight / PIN_DIMS.unselected.h)),
      h: targetIconHeight,
    };
    const sizeSel = {
      w: Math.round(PIN_DIMS.selected.w * (targetIconHeight / PIN_DIMS.selected.h)),
      h: targetIconHeight,
    };

    const popupOffsetY = -Math.round(targetIconHeight * 0.9);

    const defaultIcon = L.divIcon({
      className: "heymax-pin-icon",
      html: `<img alt="" src="${PIN_BASE_URL}${pin.unselected}" style="width:${sizeUn.w}px;height:${sizeUn.h}px;display:block;" />`,
      iconSize: [sizeUn.w, sizeUn.h],
      iconAnchor: [Math.round(sizeUn.w / 2), sizeUn.h],
      popupAnchor: [0, popupOffsetY],
    });

    iconCache.set(key, {
      defaultIcon,
      selectedIcon: pin.selected
        ? L.divIcon({
            className: "heymax-pin-icon",
            html: `<img alt="" src="${PIN_BASE_URL}${pin.selected}" style="width:${sizeSel.w}px;height:${sizeSel.h}px;display:block;" />`,
            iconSize: [sizeSel.w, sizeSel.h],
            iconAnchor: [Math.round(sizeSel.w / 2), sizeSel.h],
            popupAnchor: [0, popupOffsetY],
          })
        : null,
    });
    return iconCache.get(key);
  }

  const color = CATEGORY_COLORS[key] || "#64748b";
  const fallbackIcon = L.divIcon({
    className: "heymax-pin-icon",
    html: `<div class="pin" style="--pin:${color}"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
    popupAnchor: [0, -9],
  });

  const fallbackSelectedIcon = L.divIcon({
    className: "heymax-pin-icon",
    html: `<div class="pin" style="--pin:${color};outline:4px solid rgba(255, 255, 255, 0.65);outline-offset:2px;box-shadow:0 18px 36px rgba(0, 0, 0, 0.5);transform:translate(-50%, -50%) scale(1.06);"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
    popupAnchor: [0, -9],
  });

  iconCache.set(key, { defaultIcon: fallbackIcon, selectedIcon: fallbackSelectedIcon });
  return iconCache.get(key);
}

function getPopupClass(category) {
  const key = normalizeCategory(category) || "other";
  const supported = key in CATEGORY_COLORS;
  return supported ? `popup popup--${key}` : "popup";
}

function getCategoryColor(category) {
  const key = normalizeCategory(category) || "other";
  return CATEGORY_COLORS[key] || "#64748b";
}

function setStatus(message, { isError = false } = {}) {
  const el = document.getElementById("status");
  if (!el) return;
  el.hidden = !message;
  el.textContent = message || "";
  el.style.borderColor = isError ? "rgba(248,113,113,0.55)" : "rgba(255,255,255,0.12)";
}

function escapeHtml(input) {
  return String(input ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function normalizeUrl(url) {
  const raw = String(url ?? "").trim();
  if (!raw) return "";
  if (/^https?:\/\//i.test(raw)) return raw;
  return `https://${raw}`;
}

function formatPopup(loc) {
  const name = escapeHtml(loc.name || "Unknown location");
  const address = escapeHtml(loc.address || "");
  const hours = escapeHtml(loc.openingHours || loc.opening_hours || "");
  const phone = escapeHtml(loc.phone || "");
  const website = normalizeUrl(loc.website || "");
  const websiteText = escapeHtml(website);
  const categoryKey = categoryKeyFromRaw(loc.category);
  const categoryLabel = escapeHtml(categoryDisplayName(categoryKey));

  const rows = [
    hours && `<div class="popup-row"><span class="popup-label">Hours:</span> ${hours}</div>`,
    phone && `<div class="popup-row"><span class="popup-label">Phone:</span> ${phone}</div>`,
    website &&
      `<div class="popup-row"><span class="popup-label">Website:</span> <a class="popup-link" href="${websiteText}" target="_blank" rel="noopener noreferrer">${websiteText}</a></div>`,
  ]
    .filter(Boolean)
    .join("");

  return `<div>
    <div class="popup-top">
      <div class="popup-title">${name}</div>
      <div class="popup-chip">${categoryLabel}</div>
    </div>
    ${address ? `<div class="popup-address">${address}</div>` : ""}
    ${rows || `<div class="popup-row"><span class="muted">No additional details.</span></div>`}
  </div>`;
}

function isValidLatLng(lat, lng) {
  return (
    Number.isFinite(lat) &&
    Number.isFinite(lng) &&
    Math.abs(lat) <= 90 &&
    Math.abs(lng) <= 180
  );
}

async function loadLocations() {
  const res = await fetch("./locations.json", { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load locations.json (${res.status})`);
  const data = await res.json();
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.locations)) return data.locations;
  throw new Error("locations.json must be an array or { locations: [...] }");
}

function initMap() {
  const map = L.map("map", {
    zoomControl: false,
    closePopupOnClick: false,
    doubleClickZoom: false,
  }).setView(DEFAULT_VIEW.center, DEFAULT_VIEW.zoom);

  L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {
    subdomains: "abcd",
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  }).addTo(map);

  return map;
}

async function main() {
  setStatus("Loading locations…");
  const map = initMap();

  let locations;
  try {
    locations = await loadLocations();
  } catch (err) {
    setStatus(`Error: ${err?.message || String(err)}`, { isError: true });
    return;
  }

  const bounds = L.latLngBounds([]);
  let added = 0;
  let skipped = 0;

  const markerRows = [];
  let selectedMarker = null;

  const markerToCategoryKey = new Map();

  const clusterLayer = L.layerGroup().addTo(map);
  const CLUSTER_MAX_ZOOM = 13;
  const CLUSTER_PIXEL_DISTANCE = 70;
  const CLUSTER_MAINTAIN_SELECTED = true;
  const viewBoundsPadding = 0.25;

  function clearAllMarkersFromMap({ keepSelected = false } = {}) {
    markerRows.forEach(({ marker }) => {
      if (keepSelected && marker === selectedMarker) return;
      if (map.hasLayer(marker)) map.removeLayer(marker);
    });
  }

  let renderTimer = null;
  function scheduleRender() {
    if (renderTimer) window.clearTimeout(renderTimer);
    renderTimer = window.setTimeout(() => {
      renderTimer = null;
      renderMarkers();
    }, 60);
  }

  function setSelectedMarker(marker) {
    if (selectedMarker) {
      const prevCategoryKey = markerToCategoryKey.get(selectedMarker);
      const prevIcons = prevCategoryKey ? getCategoryIcon(prevCategoryKey) : null;
      const prevDefaultIcon = prevIcons?.defaultIcon;
      if (prevDefaultIcon) selectedMarker.setIcon(prevDefaultIcon);
    }

    selectedMarker = marker;
    if (selectedMarker) {
      const categoryKey = markerToCategoryKey.get(selectedMarker);
      const icons = categoryKey ? getCategoryIcon(categoryKey) : null;
      const selectedIcon = icons?.selectedIcon;
      if (selectedIcon) selectedMarker.setIcon(selectedIcon);
    }

    scheduleRender();
  }

  function clearSelectedMarker() {
    if (!selectedMarker) return;
    const markerToClear = selectedMarker;
    const prevCategoryKey = markerToCategoryKey.get(selectedMarker);
    const prevIcons = prevCategoryKey ? getCategoryIcon(prevCategoryKey) : null;
    const prevDefaultIcon = prevIcons?.defaultIcon;
    selectedMarker = null;
    if (prevDefaultIcon) markerToClear.setIcon(prevDefaultIcon);
    markerToClear.closePopup();

    scheduleRender();
  }

  function focusMarker(marker) {
    if (CLUSTER_MAINTAIN_SELECTED && !map.hasLayer(marker)) marker.addTo(map);
    marker.openPopup();
    if (selectedMarker !== marker) setSelectedMarker(marker);

    const ll = marker.getLatLng();
    const isMobile = window.matchMedia?.("(max-width: 480px)")?.matches;
    map.setView(ll, Math.max(map.getZoom(), 15), { animate: true });
    if (!isMobile) return;

    if (typeof focusMarker.adjustToken !== "number") focusMarker.adjustToken = 0;
    focusMarker.adjustToken += 1;

    return;
  }

  locations.forEach((loc) => {
    const lat = Number(loc?.lat);
    const lng = Number(loc?.lng);
    if (!isValidLatLng(lat, lng)) {
      skipped += 1;
      return;
    }

    const categoryKey = categoryKeyFromRaw(loc?.category);
    const icons = getCategoryIcon(categoryKey);
    const marker = L.marker([lat, lng], { icon: icons.defaultIcon });
    markerToCategoryKey.set(marker, categoryKey);

    marker.bindPopup(formatPopup(loc), {
      maxWidth: 340,
      className: getPopupClass(categoryKey),
      closeOnClick: false,
      autoClose: true,
    });
    marker.off("click");
    marker.on("click", () => {
      marker.openPopup();
      if (selectedMarker !== marker) setSelectedMarker(marker);
    });
    marker.on("popupclose", () => {
      if (selectedMarker === marker) clearSelectedMarker();
    });

    bounds.extend([lat, lng]);
    added += 1;

    markerRows.push({ marker, loc, categoryKey });
  });

  const filtersEl = document.getElementById("filters");
  const activeCategories = new Set();
  CATEGORY_ORDER.forEach((c) => activeCategories.add(c));

  function renderMarkers() {
    if (!markerRows.length) return;

    const clusteringOn = map.getZoom() <= CLUSTER_MAX_ZOOM;
    const viewBounds = map.getBounds().pad(viewBoundsPadding);

    if (selectedMarker) {
      const selectedKey = markerToCategoryKey.get(selectedMarker);
      if (selectedKey && !activeCategories.has(selectedKey)) {
        clearSelectedMarker();
      }
    }

    if (!clusteringOn) {
      clusterLayer.clearLayers();
      markerRows.forEach(({ marker, categoryKey }) => {
        const shouldShow = activeCategories.has(categoryKey);
        const isOnMap = map.hasLayer(marker);
        if (shouldShow) {
          if (!isOnMap) marker.addTo(map);
        } else if (isOnMap) {
          marker.closePopup();
          map.removeLayer(marker);
        }
      });
      return;
    }

    clusterLayer.clearLayers();
    clearAllMarkersFromMap({ keepSelected: true });

    const activeInView = markerRows
      .filter(({ marker, categoryKey }) => {
        if (!activeCategories.has(categoryKey)) return false;
        if (marker === selectedMarker) return false;
        return viewBounds.contains(marker.getLatLng());
      })
      .map(({ marker, loc, categoryKey }) => ({ marker, loc, categoryKey }));

    const bucketSize = CLUSTER_PIXEL_DISTANCE;
    const buckets = new Map();

    activeInView.forEach(({ marker, categoryKey }) => {
      const p = map.latLngToLayerPoint(marker.getLatLng());
      const bx = Math.round(p.x / bucketSize);
      const by = Math.round(p.y / bucketSize);
      const key = `${bx}_${by}`;
      const arr = buckets.get(key) ?? [];
      arr.push({ marker, categoryKey });
      buckets.set(key, arr);
    });

    const clusters = [];
    for (const candidates of buckets.values()) {
      for (const c of candidates) {
        const p = map.latLngToLayerPoint(c.marker.getLatLng());
        let assigned = false;
        for (const cluster of clusters) {
          const cp = map.latLngToLayerPoint(cluster.anchorMarker.getLatLng());
          const dx = p.x - cp.x;
          const dy = p.y - cp.y;
          if (Math.sqrt(dx * dx + dy * dy) <= CLUSTER_PIXEL_DISTANCE) {
            cluster.members.push(c);
            cluster.anchorMarker = c.marker;
            assigned = true;
            break;
          }
        }
        if (!assigned) {
          clusters.push({
            anchorMarker: c.marker,
            members: [c],
          });
        }
      }
    }

    clusters.forEach((cluster) => {
      const members = cluster.members;
      if (!members.length) return;

      if (members.length === 1) {
        const m = members[0];
        if (!map.hasLayer(m.marker)) m.marker.addTo(map);
        return;
      }

      let sumLat = 0;
      let sumLng = 0;
      const categoryCounts = new Map();

      members.forEach((m) => {
        const ll = m.marker.getLatLng();
        sumLat += ll.lat;
        sumLng += ll.lng;
        categoryCounts.set(m.categoryKey, (categoryCounts.get(m.categoryKey) ?? 0) + 1);
      });

      const center = [sumLat / members.length, sumLng / members.length];

      let dominantKey = null;
      let dominantCount = -1;
      for (const [k, v] of categoryCounts.entries()) {
        if (v > dominantCount) {
          dominantCount = v;
          dominantKey = k;
        }
      }
      const hasFood = categoryCounts.has("food");
      const hasAttractions = categoryCounts.has("attractions");
      let color;
      if (hasFood && hasAttractions) {
        color = "#8C22FA";
      } else if (hasFood) {
        color = getCategoryColor("food");
      } else if (hasAttractions) {
        color = getCategoryColor("attractions");
      } else if (dominantKey) {
        color = getCategoryColor(dominantKey);
      } else {
        color = "#64748b";
      }

      const count = members.length;
      const size = Math.max(24, Math.min(44, 18 + Math.round(Math.log2(count + 1) * 12)));
      const clusterHtml = `
        <div class="heymax-cluster-pin" style="
          --cluster-color:${color};
          width:${size}px;
          height:${size}px;
          line-height:${size}px;
        ">
          <span class="heymax-cluster-count">${count}</span>
        </div>
      `;

      const icon = L.divIcon({
        className: "heymax-pin-icon",
        html: clusterHtml,
        iconSize: [size, size],
        iconAnchor: [Math.round(size / 2), Math.round(size / 2)],
      });

      const clusterMarker = L.marker(center, { icon });
      clusterMarker.on("click", (ev) => {
        ev.originalEvent?.stopPropagation?.();
        const memberBounds = L.latLngBounds(
          members.map((m) => m.marker.getLatLng()).filter(Boolean),
        );
        clearSelectedMarker();
        hideResults();
        map.fitBounds(memberBounds.pad(0.18), { animate: true, maxZoom: 17 });
      });

      clusterLayer.addLayer(clusterMarker);
    });
  }

  function applyFilters() {
    if (selectedMarker) {
      const selectedKey = markerToCategoryKey.get(selectedMarker);
      if (selectedKey && !activeCategories.has(selectedKey)) clearSelectedMarker();
    }
    scheduleRender();
    hideResults();
  }

  function buildFiltersUi() {
    if (!filtersEl) return;
    filtersEl.innerHTML = "";
    CATEGORY_ORDER.forEach((cat) => {
      const id = `filter-${cat}`;
      const label = document.createElement("label");
      label.setAttribute("for", id);

      const input = document.createElement("input");
      input.type = "checkbox";
      input.id = id;
      input.checked = true;
      input.addEventListener("change", () => {
        if (input.checked) activeCategories.add(cat);
        else activeCategories.delete(cat);
        applyFilters();
      });

      const swatch = document.createElement("span");
      swatch.className = "swatch";
      swatch.style.setProperty("--swatch", getCategoryColor(cat));

      const text = document.createElement("span");
      text.textContent = categoryDisplayName(cat);

      label.appendChild(input);
      label.appendChild(swatch);
      label.appendChild(text);
      filtersEl.appendChild(label);
    });
  }

  buildFiltersUi();
  scheduleRender();

  const searchEl = document.getElementById("search");
  const resultsEl = document.getElementById("results");
  const clearEl = document.getElementById("search-clear");

  function hideResults() {
    if (!resultsEl) return;
    resultsEl.hidden = true;
    resultsEl.innerHTML = "";
  }

  function showResults(rows) {
    if (!resultsEl) return;
    resultsEl.hidden = rows.length === 0;
    resultsEl.innerHTML = "";
    rows.slice(0, 8).forEach(({ marker, loc, categoryKey }) => {
      const item = document.createElement("div");
      item.className = "item";
      item.addEventListener("click", (ev) => {
        ev.stopPropagation();
        ev.preventDefault();
        focusMarker(marker);
        hideResults();
        if (searchEl) searchEl.blur();
      });

      const dot = document.createElement("div");
      dot.className = "dot";
      dot.style.setProperty("--dot", getCategoryColor(categoryKey));

      const body = document.createElement("div");
      const name = document.createElement("p");
      name.className = "name";
      name.textContent = loc?.name || "Unknown";
      const sub = document.createElement("p");
      sub.className = "sub";
      sub.textContent = loc?.address
        ? `${categoryDisplayName(categoryKey)} · ${loc.address}`
        : categoryDisplayName(categoryKey);

      body.appendChild(name);
      body.appendChild(sub);

      item.appendChild(dot);
      item.appendChild(body);
      resultsEl.appendChild(item);
    });
  }

  function searchIndex(query) {
    const q = String(query ?? "").trim().toLowerCase();
    if (!q) return [];
    return markerRows
      .filter(({ loc }) => {
        const n = String(loc?.name ?? "").toLowerCase();
        const a = String(loc?.address ?? "").toLowerCase();
        return n.includes(q) || a.includes(q);
      })
      .sort((a, b) => {
        const an = String(a.loc?.name ?? "");
        const bn = String(b.loc?.name ?? "");
        return an.localeCompare(bn);
      });
  }

  if (searchEl) {
    searchEl.addEventListener("input", () => {
      const matches = searchIndex(searchEl.value);
      showResults(matches);
    });
    searchEl.addEventListener("focus", () => {
      const matches = searchIndex(searchEl.value);
      if (String(searchEl.value || "").trim()) showResults(matches);
    });
    searchEl.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        searchEl.value = "";
        hideResults();
        searchEl.blur();
      }
    });
  }

  if (clearEl) {
    clearEl.addEventListener("click", () => {
      if (searchEl) searchEl.value = "";
      hideResults();
    });
  }

  map.on("click", (e) => {
    const t = e?.originalEvent?.target;
    if (t && typeof t.closest === "function") {
      if (t.closest(".heymax-pin-icon")) return;
      if (t.closest(".controls") || t.closest("#search") || t.closest("#results")) return;
    }
    clearSelectedMarker();
    hideResults();
  });

  map.on("dblclick", () => {
    hideResults();
  });

  map.on("zoomend moveend", () => scheduleRender());

  if (added > 0) {
    map.fitBounds(bounds.pad(0.15), { animate: false });
    setStatus(
      skipped > 0
        ? `Loaded ${added} locations. Skipped ${skipped} with invalid coordinates.`
        : `Loaded ${added} locations.`,
    );
  } else {
    setStatus(
      skipped > 0
        ? `No valid coordinates found. Skipped ${skipped} locations.`
        : "No locations found.",
      { isError: true },
    );
  }

  map.invalidateSize();
}

main().catch((err) => {
  setStatus(`Unexpected error: ${err?.message || String(err)}`, { isError: true });
});
