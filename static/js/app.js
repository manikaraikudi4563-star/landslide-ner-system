/**
 * NER-LEWS: AI-Based Landslide Early Warning & Risk Monitoring System
 * North Eastern Region of India (NER)
 * 
 * Complete Frontend Controller with all 7 Advanced Features:
 * 1. Satellite Change Detection (Before / Current Comparison)
 * 2. Infrastructure Risk Impact Analysis (Highways, Bridges, Power, Railways)
 * 3. Sensor Anomaly Detection & AI Data Quality Guard
 * 4. Upgraded AI What-If Simulation Sandbox (Baseline vs Simulated Stress vs Delta)
 * 5. Smart Multi-Criteria Shelter Allocation (MCDA)
 * 6. Offline Emergency Communication (Store-and-Forward Queue & Sync)
 * 7. Multi-Language Alert Localization (8 Regional NER Languages)
 */

// Global Application State
const state = {
  activeTab: 'tab-gis',
  selectedState: 'ALL',
  userRole: 'AUTHORITY',
  currentTimeframe: '24h',
  currentAlertLang: 'en',
  isNetworkOnline: true,
  stations: [],
  selectedStationId: null,
  selectedRiskZone: null,
  selectedShelterId: null,
  activeRouteData: null,
  corridors: [],
  railways: [],
  infrastructure: [],
  satelliteChanges: [],
  shelters: [],
  smartShelterRecommendations: [],
  states: {},
  alerts: [],
  anomalies: [],
  commStatus: {},
  historicalEvents: [],
  citizenReports: [],
  sensorHealth: [],
  weatherData: {},
  satCompareState: 'split', // split | before_only | current_only
  map: null,
  layers: {
    stations: null,
    corridors: null,
    railways: null,
    infra: null,
    shelters: null,
    satChange: null,
    heatmap: null,
    historical: null,
    radar: null,
    evacRoute: null
  },
  baseLayers: {
    dark: null,
    satellite: null
  },
  currentBaseLayer: 'dark',
  chart: null,
  pollingInterval: null
};

// Application Initialization on DOM Ready
document.addEventListener('DOMContentLoaded', async () => {
  initTabs();
  initMap();
  initChart();
  initSimulationListeners();
  initEventListeners();

  await loadInitialData();
  runSimulationUpdate(); // Trigger initial AI Sandbox calculation

  // Periodic live telemetry refresh
  state.pollingInterval = setInterval(() => syncTelemetry(1.0), 12000);
  updateLiveTimestamp();
  setInterval(updateLiveTimestamp, 1000);
});

function updateLiveTimestamp() {
  const now = new Date();
  const timeStr = now.toTimeString().split(' ')[0] + ' UTC+05:30';
  const el = document.getElementById('header-last-sync');
  if (el) el.textContent = timeStr;
}

/* ==========================================================================
   Tab Navigation Handling
   ========================================================================== */
function initTabs() {
  const tabButtons = document.querySelectorAll('.nav-tab-btn');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      switchTab(targetTab);
    });
  });
}

function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll('.nav-tab-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  });
  document.querySelectorAll('.tab-pane').forEach(p => {
    p.style.display = (p.id === tabId) ? 'block' : 'none';
  });

  if (tabId === 'tab-gis' && state.map) {
    setTimeout(() => { state.map.invalidateSize(); }, 200);
  }
}

/* ==========================================================================
   Leaflet WebGIS Setup & 10-Layer Architecture
   ========================================================================== */
function initMap() {
  state.map = L.map('map', {
    center: [25.75, 92.85],
    zoom: 7,
    zoomControl: false
  });

  L.control.zoom({ position: 'bottomright' }).addTo(state.map);

  // Base Layers
  state.baseLayers.dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 18
  }).addTo(state.map);

  state.baseLayers.satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Earthstar Geographics',
    maxZoom: 18
  });

  // Layer Groups (10 Layers)
  state.layers.stations = L.layerGroup().addTo(state.map);
  state.layers.corridors = L.layerGroup().addTo(state.map);
  state.layers.railways = L.layerGroup().addTo(state.map);
  state.layers.infra = L.layerGroup().addTo(state.map);
  state.layers.shelters = L.layerGroup().addTo(state.map);
  state.layers.satChange = L.layerGroup().addTo(state.map);
  state.layers.heatmap = L.layerGroup();
  state.layers.historical = L.layerGroup();
  state.layers.radar = L.layerGroup();
  state.layers.evacRoute = L.layerGroup().addTo(state.map);

  // Map Click Inspector
  state.map.on('click', async (e) => {
    const { lat, lng } = e.latlng;
    const customZone = {
      id: `CUSTOM-${lat.toFixed(3)}-${lng.toFixed(3)}`,
      name: `Inspected Terrain Location (${lat.toFixed(3)}°N, ${lng.toFixed(3)}°E)`,
      state: state.selectedState !== 'ALL' ? state.selectedState : 'NER Mountain Corridor',
      district: 'Regional Hill Sector',
      lat: lat,
      lng: lng,
      elevation_m: 1280,
      slope_deg: 48.0,
      corridor: 'Mountain Secondary Access Track',
      current_readings: {
        warning_level: 'ORANGE',
        status_text: 'SEVERE RISK DETECTED',
        factor_of_safety: 1.05,
        pore_water_pressure: 30.2,
        tilt_rate: 0.175,
        soil_moisture: 72.5,
        rainfall_24h: 54.0
      }
    };
    selectRiskZone(customZone);
  });
}

/* ==========================================================================
   WebGIS Layer Renderers (Sensors, Corridors, Infrastructure, Satellite Changes)
   ========================================================================== */
function renderMapStations() {
  state.layers.stations.clearLayers();

  state.stations.forEach(stn => {
    const level = (stn.current_readings?.warning_level || 'GREEN').toLowerCase();
    const color = level === 'red' ? '#ef4444' : (level === 'orange' ? '#f97316' : (level === 'yellow' ? '#f59e0b' : '#10b981'));
    
    const customIcon = L.divIcon({
      className: 'station-pulse-marker',
      html: `
        ${level === 'red' ? '<div class="pulse-ring-wave"></div>' : ''}
        <div class="pulse-circle ${level}"></div>
      `,
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });

    const marker = L.marker([stn.lat, stn.lng], { icon: customIcon });

    const popupHtml = `
      <div style="font-family:sans-serif; min-width:230px; padding:2px;">
        <div style="font-size:0.7rem; font-weight:700; color:${color}; text-transform:uppercase;">● ${stn.current_readings.status_text}</div>
        <div style="font-size:0.95rem; font-weight:700; color:#fff; margin-top:2px;">${stn.name}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">${stn.district}, ${stn.state} • Slope: ${stn.slope_deg}° • Elev: ${stn.elevation_m}m</div>
        
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin:8px 0; background:rgba(255,255,255,0.05); padding:6px; border-radius:4px;">
          <div>
            <div style="font-size:0.65rem; color:#94a3b8;">Factor of Safety</div>
            <div style="font-size:0.95rem; font-weight:700; color:${stn.current_readings.factor_of_safety < 1.1 ? '#ef4444' : '#10b981'}; font-family:monospace;">${stn.current_readings.factor_of_safety}</div>
          </div>
          <div>
            <div style="font-size:0.65rem; color:#94a3b8;">Pore Pressure</div>
            <div style="font-size:0.95rem; font-weight:700; color:#fff; font-family:monospace;">${stn.current_readings.pore_water_pressure} <span style="font-size:0.65rem;">kPa</span></div>
          </div>
          <div>
            <div style="font-size:0.65rem; color:#94a3b8;">Tilt Rate</div>
            <div style="font-size:0.95rem; font-weight:700; color:#38bdf8; font-family:monospace;">${stn.current_readings.tilt_rate} <span style="font-size:0.65rem;">mm/h</span></div>
          </div>
          <div>
            <div style="font-size:0.65rem; color:#94a3b8;">Rainfall 24h</div>
            <div style="font-size:0.95rem; font-weight:700; color:#f59e0b; font-family:monospace;">${stn.current_readings.rainfall_24h} <span style="font-size:0.65rem;">mm</span></div>
          </div>
        </div>

        <button onclick="selectStation('${stn.id}', true)" class="btn btn-primary" style="width:100%; font-size:0.75rem; padding:4px 8px;">
          ⚠️ Inspect Risk Zone
        </button>
      </div>
    `;

    marker.bindPopup(popupHtml);
    marker.on('click', () => {
      selectStation(stn.id, false);
    });

    state.layers.stations.addLayer(marker);
  });
}

function renderMapCorridors() {
  state.layers.corridors.clearLayers();

  state.corridors.forEach(corr => {
    const isCritical = corr.vulnerability === 'CRITICAL' || corr.vulnerability === 'EXTREME';
    const color = isCritical ? '#f43f5e' : '#38bdf8';

    const polyline = L.polyline(corr.path_coordinates, {
      color: color,
      weight: 4,
      opacity: 0.85,
      dashArray: isCritical ? '6, 6' : null
    });

    polyline.bindPopup(`
      <div style="font-family:sans-serif; padding:4px;">
        <div style="font-weight:700; color:${color}; font-size:0.85rem;">🛣️ ${corr.name}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">State: ${corr.state} • Length: ${corr.length_km} km</div>
        <div style="font-size:0.75rem; color:#fca5a5; margin-top:4px;"><strong>Key Hotspots:</strong> ${corr.key_hotspots.join(', ')}</div>
      </div>
    `);

    state.layers.corridors.addLayer(polyline);
  });
}

function renderMapRailways() {
  state.layers.railways.clearLayers();

  state.railways.forEach(rly => {
    const polyline = L.polyline(rly.path_coordinates, {
      color: '#a855f7',
      weight: 4,
      opacity: 0.9,
      dashArray: '4, 8'
    });

    polyline.bindPopup(`
      <div style="font-family:sans-serif; padding:4px;">
        <div style="font-weight:700; color:#a855f7; font-size:0.85rem;">🚆 ${rly.name}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">State: ${rly.state} • Length: ${rly.length_km} km</div>
        <div style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;"><strong>Strategic Bridges & Cuts:</strong> ${rly.key_hotspots.join(', ')}</div>
      </div>
    `);

    state.layers.railways.addLayer(polyline);
  });
}

// FEATURE 2: Render Monitored Infrastructure Assets on Map
function renderMapInfrastructure() {
  state.layers.infra.clearLayers();

  state.infrastructure.forEach(item => {
    const isCrit = item.criticality === 'CRITICAL';
    const isHigh = item.criticality === 'HIGH';
    const color = isCrit ? '#ef4444' : (isHigh ? '#f97316' : '#eab308');

    const marker = L.circleMarker([item.latitude, item.longitude], {
      radius: 8,
      color: color,
      fillColor: color,
      fillOpacity: 0.85,
      weight: 2
    });

    marker.bindPopup(`
      <div style="font-family:sans-serif; padding:4px; min-width:200px;">
        <div style="font-size:0.68rem; font-weight:700; color:${color}; text-transform:uppercase;">🏗️ ${item.type}</div>
        <div style="font-size:0.90rem; font-weight:700; color:#fff; margin-top:2px;">${item.name}</div>
        <div style="font-size:0.72rem; color:#94a3b8;">${item.district}, ${item.state}</div>
        <div style="font-size:0.75rem; color:#fca5a5; margin-top:4px;"><strong>Status:</strong> ${item.status}</div>
        <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">${item.description}</div>
      </div>
    `);

    state.layers.infra.addLayer(marker);
  });
}

// FEATURE 1: Render Satellite Change Polygons on Map
function renderMapSatelliteChanges() {
  state.layers.satChange.clearLayers();

  state.satelliteChanges.forEach(chg => {
    const polygon = L.polygon(chg.polygon_coordinates, {
      color: '#ec4899',
      fillColor: '#f43f5e',
      fillOpacity: 0.45,
      weight: 2,
      dashArray: '4, 4'
    });

    polygon.bindPopup(`
      <div style="font-family:sans-serif; padding:4px; min-width:220px;">
        <div style="font-size:0.68rem; font-weight:700; color:#ec4899; text-transform:uppercase;">🛰️ SATELLITE CHANGE DETECTION</div>
        <div style="font-size:0.92rem; font-weight:700; color:#fff; margin-top:2px;">${chg.name}</div>
        <div style="font-size:0.75rem; color:#38bdf8; margin-top:2px;">Change: <strong>${chg.change_pct}%</strong> (${chg.risk_indicator} Risk)</div>
        <div style="font-size:0.72rem; color:#fca5a5; margin-top:4px;"><strong>Class:</strong> ${chg.change_class}</div>
        <div style="font-size:0.70rem; color:#94a3b8; margin-top:2px;">Pass Dates: ${chg.before_date} vs ${chg.after_date}</div>
      </div>
    `);

    state.layers.satChange.addLayer(polygon);
  });
}

function renderMapShelters() {
  state.layers.shelters.clearLayers();

  state.shelters.forEach(shl => {
    const shelterIcon = L.divIcon({
      className: 'shelter-pulse-marker',
      html: `
        <div class="shelter-icon-badge" title="${shl.name}">
          🛡️
        </div>
      `,
      iconSize: [28, 28],
      iconAnchor: [14, 14]
    });

    const marker = L.marker([shl.lat, shl.lng], { icon: shelterIcon });

    let distText = 'Select a risk hotspot on map to calculate road distance';
    if (state.selectedRiskZone) {
      const d = haversineKm(state.selectedRiskZone.lat, state.selectedRiskZone.lng, shl.lat, shl.lng);
      const roadKm = Math.max(0.8, Math.round(d * 1.82 * 10) / 10);
      distText = `Distance from ${state.selectedRiskZone.name}: <strong style="color:#06b6d4;">${roadKm} km</strong> (~${Math.max(3, Math.round((roadKm/28)*60))} min drive)`;
    }

    const popupHtml = `
      <div style="font-family:sans-serif; min-width:260px; padding:3px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.68rem; font-weight:700; color:#10b981; text-transform:uppercase;">● DESIGNATED RELIEF NODE</span>
          <span style="font-size:0.65rem; background:rgba(16,185,129,0.2); color:#10b981; padding:2px 6px; border-radius:4px; font-weight:700;">${shl.status || 'AVAILABLE'}</span>
        </div>

        <div style="font-size:0.98rem; font-weight:700; color:#fff; margin:4px 0 2px 0;">🛡️ ${shl.name}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">${shl.district}, ${shl.state} • ${shl.location || 'High Ground Safe Zone'}</div>

        <div style="font-size:0.75rem; color:#cbd5e1; background:rgba(255,255,255,0.05); padding:6px; border-radius:4px; margin:8px 0; border:1px solid rgba(255,255,255,0.08);">
          <div><strong>Capacity:</strong> ${shl.capacity} persons (${shl.available_capacity || Math.round(shl.capacity*0.7)} slots free)</div>
          <div style="margin-top:2px; font-size:0.72rem; color:#94a3b8;">${distText}</div>
          <div style="margin-top:4px; font-size:0.72rem; color:#38bdf8;"><strong>Authority:</strong> ${shl.contact_authority || 'SDMA & NDRF Dispatch'}</div>
        </div>

        <div style="display:flex; gap:6px; margin-top:6px;">
          <button onclick="openShelterDetails('${shl.id || shl.shelter_id}')" class="btn btn-outline" style="flex:1; font-size:0.72rem; padding:4px 8px;">
            🛡️ View Details
          </button>
          <button onclick="calculateSafeRouteToShelter('${shl.id || shl.shelter_id}')" class="btn btn-primary" style="flex:1.2; font-size:0.72rem; padding:4px 8px;">
            🏃 Safe Route
          </button>
        </div>
      </div>
    `;

    marker.bindPopup(popupHtml, { minWidth: 260 });
    state.layers.shelters.addLayer(marker);
  });
}

function renderMapHistorical() {
  state.layers.historical.clearLayers();

  state.historicalEvents.forEach(ev => {
    const histMarker = L.circleMarker([ev.latitude || ev.lat, ev.longitude || ev.lng], {
      radius: 7,
      color: '#e11d48',
      fillColor: '#fda4af',
      fillOpacity: 0.8
    });

    histMarker.bindPopup(`
      <div style="font-family:sans-serif; padding:4px;">
        <div style="font-size:0.68rem; color:#e11d48; font-weight:700;">HISTORICAL DISASTER CATALOG</div>
        <div style="font-weight:700; color:#fff; font-size:0.88rem;">${ev.name}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Date: ${ev.event_date || ev.date} • ${ev.district}, ${ev.state}</div>
        <div style="font-size:0.72rem; color:#fca5a5; margin-top:3px;">Casualties: ${ev.casualties} • Volume: ${ev.volume_m3?.toLocaleString()} m³</div>
      </div>
    `);

    state.layers.historical.addLayer(histMarker);
  });
}

function renderMapRadar() {
  state.layers.radar.clearLayers();

  const radarCenters = [
    { lat: 25.30, lng: 91.73, intensity: 'Extreme (65 mm/hr)', radius: 45000, color: '#dc2626' },
    { lat: 24.71, lng: 93.65, intensity: 'Heavy (38 mm/hr)', radius: 38000, color: '#ea580c' },
    { lat: 27.33, lng: 88.61, intensity: 'Moderate (22 mm/hr)', radius: 32000, color: '#ca8a04' }
  ];

  radarCenters.forEach(r => {
    const circle = L.circle([r.lat, r.lng], {
      radius: r.radius,
      color: r.color,
      fillColor: r.color,
      fillOpacity: 0.25,
      weight: 2,
      dashArray: '6, 6'
    });
    circle.bindTooltip(`🌧️ Monsoon Radar: ${r.intensity}`, { sticky: true });
    state.layers.radar.addLayer(circle);
  });
}

async function renderRiskGridHeatmap() {
  state.layers.heatmap.clearLayers();
  try {
    const res = await fetch('/api/heatmap?lat=25.8&lng=92.8&radius=1.8');
    const data = await res.json();
    
    data.grid_points.forEach(pt => {
      const circle = L.circle([pt.lat, pt.lng], {
        radius: 14000,
        color: 'transparent',
        fillColor: pt.color,
        fillOpacity: 0.35
      });

      circle.bindTooltip(`AI Risk Score: ${pt.risk_score} (${pt.tier}) • Click to select`, { sticky: true });
      
      circle.on('click', () => {
        const gridZone = {
          id: `GRID-${pt.lat.toFixed(2)}-${pt.lng.toFixed(2)}`,
          name: `High Hazard Grid Cell [${pt.lat.toFixed(2)}°N, ${pt.lng.toFixed(2)}°E]`,
          state: state.selectedState !== 'ALL' ? state.selectedState : 'NER Mountain Corridor',
          district: 'Himalayan Ridge Segment',
          lat: pt.lat,
          lng: pt.lng,
          elevation_m: 1450,
          slope_deg: 51.0,
          corridor: 'Regional Mountain Corridor',
          current_readings: {
            warning_level: pt.tier === 'CRITICAL' ? 'RED' : 'ORANGE',
            status_text: `${pt.tier} ACTIVE`,
            factor_of_safety: pt.tier === 'CRITICAL' ? 0.84 : 1.08,
            pore_water_pressure: 34.0,
            tilt_rate: 0.28,
            soil_moisture: 78.0,
            rainfall_24h: 64.0
          }
        };
        selectRiskZone(gridZone);
      });

      state.layers.heatmap.addLayer(circle);
    });
  } catch (err) {
    console.error("Heatmap load error:", err);
  }
}

/* ==========================================================================
   Risk Hotspot Selection, Infrastructure Impact & Smart Shelters
   ========================================================================== */
async function selectRiskZone(zoneData) {
  state.selectedRiskZone = zoneData;

  showInspectorView('riskzone');
  updateRiskZonePanel(zoneData);

  // Update Infrastructure Exposure Table
  await updateInfrastructureTable(zoneData.lat, zoneData.lng);

  // Update Smart Multi-Criteria Shelter Allocation
  await updateSmartShelters(zoneData.lat, zoneData.lng);

  renderMapShelters();
}

function updateRiskZonePanel(zone) {
  const r = zone.current_readings || {
    warning_level: 'ORANGE',
    factor_of_safety: 1.10,
    pore_water_pressure: 28.0,
    tilt_rate: 0.15,
    soil_moisture: 65.0,
    rainfall_24h: 45.0
  };

  const isRed = (r.warning_level === 'RED' || r.factor_of_safety < 1.0);
  const isOrange = (r.warning_level === 'ORANGE' || r.factor_of_safety < 1.25);

  document.getElementById('rz-location-name').textContent = zone.name;
  document.getElementById('rz-location-meta').textContent = `${zone.district || ''}, ${zone.state} • Elev: ${zone.elevation_m || 1100}m • Slope: ${zone.slope_deg || 48}° • Lat: ${zone.lat.toFixed(4)}, Lng: ${zone.lng.toFixed(4)}`;

  const badgeEl = document.getElementById('rz-risk-badge');
  badgeEl.className = `badge-risk ${isRed ? 'extreme' : (isOrange ? 'high' : 'normal')}`;
  badgeEl.textContent = isRed ? 'RED - CRITICAL DANGER' : (isOrange ? 'ORANGE - SEVERE RISK' : 'YELLOW - ADVISORY');

  const aiProb = isRed ? 94.8 : (isOrange ? 78.4 : 42.0);
  document.getElementById('rz-ai-prob').textContent = `${aiProb}%`;
  document.getElementById('rz-ai-prob').style.color = isRed ? '#ef4444' : (isOrange ? '#f97316' : '#10b981');

  document.getElementById('rz-fs-val').textContent = r.factor_of_safety;
  document.getElementById('rz-fs-val').style.color = isRed ? '#ef4444' : (isOrange ? '#f97316' : '#10b981');
  
  const fsTextEl = document.getElementById('rz-fs-status');
  fsTextEl.textContent = r.factor_of_safety < 1.0 ? 'ACTIVE SLOPE COLLAPSE (Fs < 1.0)' : (r.factor_of_safety < 1.25 ? 'MARGINALLY STABLE' : 'STABLE EQUILIBRIUM');
  fsTextEl.style.color = isRed ? '#ef4444' : (isOrange ? '#f97316' : '#10b981');

  document.getElementById('rz-rain-val').innerHTML = `${r.rainfall_24h} <span class="metric-unit">mm</span>`;
  document.getElementById('rz-soil-val').innerHTML = `${r.soil_moisture} <span class="metric-unit">%</span>`;
  document.getElementById('rz-pwp-val').innerHTML = `${r.pore_water_pressure} <span class="metric-unit">kPa</span>`;
  document.getElementById('rz-tilt-val').innerHTML = `${r.tilt_rate} <span class="metric-unit">mm/h</span>`;

  document.getElementById('rz-infrastructure').innerHTML = `🛣️ ${zone.corridor || 'Key NER Highway & Railway Corridor'}`;

  // XAI Breakdown
  const xaiContainer = document.getElementById('rz-xai-breakdown');
  if (xaiContainer) {
    xaiContainer.innerHTML = `
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.72rem; color:#cbd5e1;">
        <div>🌧️ Rainfall Deluge: <strong style="color:#38bdf8;">32%</strong></div>
        <div>💧 Soil Moisture Saturation: <strong style="color:#38bdf8;">26%</strong></div>
        <div>📐 Slope Geometry: <strong style="color:#38bdf8;">22%</strong></div>
        <div>🌊 Pore Water Pressure: <strong style="color:#38bdf8;">14%</strong></div>
        <div>📈 Creep Tilt Rate: <strong style="color:#38bdf8;">6%</strong></div>
      </div>
    `;
  }
}

// FEATURE 2: Update Affected Infrastructure Impact Table
async function updateInfrastructureTable(lat, lng) {
  try {
    const res = await fetch(`/api/infrastructure?lat=${lat}&lng=${lng}&radius_km=15`);
    const data = await res.json();
    const tbody = document.getElementById('tbody-infra-list');
    if (!tbody) return;

    tbody.innerHTML = '';
    data.slice(0, 5).forEach(item => {
      const isCrit = item.calculated_risk_level === 'CRITICAL';
      const isHigh = item.calculated_risk_level === 'HIGH';
      const riskClass = isCrit ? 'extreme' : (isHigh ? 'high' : 'normal');

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong style="color:#fff;">${item.name}</strong></td>
        <td>${item.type}</td>
        <td><span style="color:#38bdf8; font-family:monospace;">${item.distance_km} km</span></td>
        <td><span class="badge-risk ${riskClass}" style="font-size:0.62rem;">${item.calculated_risk_level}</span></td>
        <td style="font-size:0.70rem; color:#cbd5e1;">${item.impact_status}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Infrastructure update error:", err);
  }
}

// FEATURE 5: Update Smart Multi-Criteria Shelter Allocation
async function updateSmartShelters(lat, lng) {
  try {
    const res = await fetch(`/api/shelters/recommend?lat=${lat}&lng=${lng}`);
    const data = await res.json();
    state.smartShelterRecommendations = data.all_ranked_options || [];

    const container = document.getElementById('smart-shelter-rankings');
    if (container) {
      container.innerHTML = '';
      state.smartShelterRecommendations.forEach((opt, idx) => {
        const isBest = (idx === 0);
        const shl = opt.shelter;
        const row = document.createElement('div');
        row.className = `smart-shelter-row ${isBest ? 'recommended' : ''}`;
        row.innerHTML = `
          <div>
            <div style="display:flex; align-items:center; gap:0.4rem;">
              <strong style="color:#fff; font-size:0.85rem;">🛡️ ${shl.name}</strong>
              ${isBest ? '<span class="badge-risk normal" style="font-size:0.60rem;">RECOMMENDED BEST</span>' : ''}
            </div>
            <div style="font-size:0.72rem; color:var(--text-secondary); margin-top:2px;">
              Distance: <strong style="color:#38bdf8;">${opt.distance_km} km</strong> • Occupancy: ${opt.occupancy_pct}% (${opt.available_slots} free) • ${opt.surrounding_risk}
            </div>
          </div>
          <div style="text-align:right;">
            <div class="smart-shelter-score">${opt.suitability_score}</div>
            <div style="font-size:0.62rem; color:var(--text-muted);">MCDA SCORE</div>
          </div>
        `;
        container.appendChild(row);
      });
    }

    if (data.best_recommended) {
      const best = data.best_recommended;
      updateEmergencyResponseDock(state.selectedRiskZone || state.stations[0], best.route_info);
    }

  } catch (err) {
    console.error("Smart shelter error:", err);
  }
}

/* ==========================================================================
   Emergency Response Dock Controller
   ========================================================================== */
function updateEmergencyResponseDock(zone, routeInfo) {
  const shl = routeInfo.shelter;
  const isRed = (zone.current_readings && (zone.current_readings.warning_level === 'RED' || zone.current_readings.factor_of_safety < 1.0));

  const badge = document.getElementById('resp-risk-badge');
  badge.className = `badge-risk ${isRed ? 'extreme' : 'high'}`;
  badge.textContent = isRed ? 'CRITICAL HAZARD' : 'SEVERE RISK';

  document.getElementById('resp-target-area').textContent = `${zone.name} (${zone.state})`;
  document.getElementById('resp-shelter-name').textContent = shl.name;
  document.getElementById('resp-shelter-cap').textContent = `Suitability Score: 94/100 • Capacity: ${shl.capacity} (${shl.available_capacity || Math.round(shl.capacity*0.65)} Free Slots)`;
  document.getElementById('resp-route-dist').innerHTML = `${routeInfo.estimated_road_km} km <span style="font-size:0.72rem; color:var(--text-muted);">(Direct: ${routeInfo.direct_distance_km} km)</span>`;
  document.getElementById('resp-travel-time').textContent = `Drive: ~${routeInfo.drive_time_mins} mins • Walk: ~${routeInfo.walk_time_mins} mins`;

  document.getElementById('resp-action-text').textContent = isRed ?
    `CRITICAL EVACUATION DIRECTIVE: Order immediate relocation toward ${shl.name} via high ridge bypass avoiding active mudslide corridor.` :
    `ADVISORY DIRECTIVE: Position standby emergency vehicles and notify SDRF responders at ${shl.name}.`;

  document.getElementById('btn-dock-view-route').onclick = () => {
    calculateSafeRouteToShelter(shl.id || shl.shelter_id);
  };
  document.getElementById('btn-dock-shelter-details').onclick = () => {
    openShelterDetails(shl.id || shl.shelter_id);
  };
}

/* ==========================================================================
   Safe / Risk-Aware Route Computation & Polyline Rendering
   ========================================================================== */
async function calculateSafeRouteToShelter(shelterId) {
  const origin = state.selectedRiskZone || state.stations.find(s => s.id === state.selectedStationId) || state.stations[0];
  if (!origin) return;

  try {
    const res = await fetch('/api/evacuation/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        latitude: origin.lat,
        longitude: origin.lng,
        shelter_id: shelterId || null
      })
    });

    const data = await res.json();
    if (!data.recommended_routes || data.recommended_routes.length === 0) return;

    const route = data.recommended_routes[0];
    const shl = route.shelter;
    state.activeRouteData = route;

    state.layers.evacRoute.clearLayers();

    // Origin Marker
    const originMarker = L.circleMarker([origin.lat, origin.lng], {
      radius: 9,
      color: '#ef4444',
      fillColor: '#ef4444',
      fillOpacity: 0.95
    }).bindPopup(`
      <div style="font-family:sans-serif; padding:4px;">
        <div style="font-size:0.68rem; color:#ef4444; font-weight:700;">ORIGIN RISK HOTSPOT</div>
        <div style="font-weight:700; color:#fff; font-size:0.88rem;">${origin.name}</div>
        <div style="font-size:0.72rem; color:#94a3b8;">${origin.district || ''}, ${origin.state}</div>
      </div>
    `);
    state.layers.evacRoute.addLayer(originMarker);

    // Glowing Polyline
    const polyline = L.polyline(route.route_path, {
      color: '#10b981',
      weight: 5,
      opacity: 0.95,
      dashArray: '8, 8'
    });

    const routePopup = `
      <div style="font-family:sans-serif; min-width:240px; padding:4px;">
        <div style="font-size:0.68rem; font-weight:700; color:#10b981; text-transform:uppercase;">● ${route.safety_badge || 'RECOMMENDED SAFE ROUTE'}</div>
        <div style="font-size:0.92rem; font-weight:700; color:#fff; margin-top:2px;">Corridor to ${shl.name}</div>
        <div style="font-size:0.75rem; color:#38bdf8; margin-top:4px;">
          Road Distance: <strong>${route.estimated_road_km} km</strong> • Drive: ~${route.drive_time_mins} mins
        </div>
        <div style="font-size:0.72rem; color:#cbd5e1; margin-top:4px;">
          ${route.risk_avoidance_note || 'Avoids active critical slide zones along mountain valley floor.'}
        </div>
      </div>
    `;

    polyline.bindPopup(routePopup);
    state.layers.evacRoute.addLayer(polyline);

    // Destination Shelter Highlight Marker
    const destMarker = L.circleMarker([shl.lat || shl.latitude, shl.lng || shl.longitude], {
      radius: 11,
      color: '#10b981',
      fillColor: '#06b6d4',
      fillOpacity: 0.95
    }).bindPopup(`
      <div style="font-family:sans-serif; padding:4px;">
        <div style="font-size:0.68rem; color:#10b981; font-weight:700;">DESTINATION SHELTER</div>
        <div style="font-weight:700; color:#fff; font-size:0.88rem;">${shl.name}</div>
        <div style="font-size:0.72rem; color:#94a3b8;">Capacity: ${shl.capacity} persons</div>
      </div>
    `);
    state.layers.evacRoute.addLayer(destMarker);

    state.map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
    updateEmergencyResponseDock(origin, route);
    polyline.openPopup();

  } catch (err) {
    console.error("Safe route calculation error:", err);
  }
}

/* ==========================================================================
   Shelter Details Modal Controller
   ========================================================================= */
function openShelterDetails(shelterId) {
  const shl = state.shelters.find(s => (s.id === shelterId || s.shelter_id === shelterId)) || state.shelters[0];
  if (!shl) return;

  state.selectedShelterId = shl.id || shl.shelter_id;

  document.getElementById('mdl-shelter-name').textContent = shl.name;
  document.getElementById('mdl-shelter-location').textContent = shl.location || `${shl.district}, ${shl.state}`;
  document.getElementById('mdl-shelter-coords').textContent = `Coordinates: ${(shl.lat || shl.latitude).toFixed(4)}° N, ${(shl.lng || shl.longitude).toFixed(4)}° E • District: ${shl.district}, ${shl.state}`;

  const total = shl.capacity || 1000;
  const avail = shl.available_capacity || Math.round(total * 0.65);
  const pctAvail = Math.round((avail / total) * 100);

  document.getElementById('mdl-shelter-cap-text').textContent = `${avail} / ${total} Free Slots (${pctAvail}% Available)`;
  document.getElementById('mdl-shelter-cap-bar').style.width = `${pctAvail}%`;

  const badgeEl = document.getElementById('mdl-shelter-status-badge');
  badgeEl.textContent = shl.status || (pctAvail > 30 ? 'AVAILABLE' : 'LIMITED');
  badgeEl.className = `badge-risk ${pctAvail > 30 ? 'normal' : 'high'}`;

  const facilityContainer = document.getElementById('mdl-shelter-facilities');
  facilityContainer.innerHTML = '';

  const facilityDefs = [
    { key: 'drinking_water', label: 'Potable Drinking Water Tanks', icon: '💧' },
    { key: 'first_aid', label: 'Emergency First Aid & Medical Bay', icon: '🩹' },
    { key: 'food', label: 'Community Hot Kitchen & Rations', icon: '🍲' },
    { key: 'toilets', label: 'Sanitation & Clean Washrooms', icon: '🚻' },
    { key: 'emergency_power', label: '50kVA Generator & Solar Array', icon: '⚡' },
    { key: 'satellite_comms', label: 'Satellite Comms & VHF Wireless', icon: '📶' }
  ];

  facilityDefs.forEach(f => {
    const isPresent = shl[f.key] !== false;
    const item = document.createElement('div');
    item.className = `facility-badge ${isPresent ? 'present' : 'absent'}`;
    item.innerHTML = `
      <span class="facility-icon">${f.icon}</span>
      <span>${f.label}</span>
    `;
    facilityContainer.appendChild(item);
  });

  document.getElementById('mdl-shelter-authority').textContent = shl.contact_authority || `${shl.state} SDMA & District Emergency Response`;
  document.getElementById('mdl-shelter-phone').textContent = shl.contact_phone || '+91-1070';

  document.getElementById('btn-mdl-safe-route').onclick = () => {
    closeModal('modal-shelter-details');
    calculateSafeRouteToShelter(shl.id || shl.shelter_id);
  };

  openModal('modal-shelter-details');
}

/* ==========================================================================
   Station Inspector & Live Telemetry Management
   ========================================================================== */
async function selectStation(stationId, panMap = false) {
  state.selectedStationId = stationId;
  const selectEl = document.getElementById('select-active-station');
  if (selectEl) selectEl.value = stationId;

  try {
    const res = await fetch(`/api/stations/${stationId}`);
    const stn = await res.json();

    document.getElementById('inspector-station-name').textContent = stn.name;
    document.getElementById('inspector-station-meta').textContent = `${stn.district}, ${stn.state} • Corridor: ${stn.corridor} • Slope: ${stn.slope_deg}°`;

    const r = stn.current_readings;
    document.getElementById('val-fs').textContent = r.factor_of_safety;
    document.getElementById('val-pwp').textContent = r.pore_water_pressure;
    document.getElementById('val-tilt').textContent = r.tilt_rate;
    document.getElementById('val-sm').textContent = r.soil_moisture;

    const fsStatusEl = document.getElementById('status-fs');
    fsStatusEl.textContent = r.status_text;
    fsStatusEl.style.color = (r.warning_level === 'RED') ? '#ef4444' : (r.warning_level === 'ORANGE' ? '#f97316' : '#10b981');

    updateChartData(stn.timeseries_history);
    selectRiskZone(stn);
    updateWeatherWidget(stn.state);

    if (panMap && state.map) {
      state.map.flyTo([stn.lat, stn.lng], 10, { duration: 1.0 });
    }

  } catch (err) {
    console.error("Select station error:", err);
  }
}

function showInspectorView(viewName) {
  const btnTelemetry = document.getElementById('btn-insp-telemetry');
  const btnRiskzone = document.getElementById('btn-insp-riskzone');
  const btnWeather = document.getElementById('btn-insp-weather');
  const viewTelemetry = document.getElementById('view-telemetry-content');
  const viewRiskzone = document.getElementById('view-riskzone-content');
  const viewWeather = document.getElementById('view-weather-content');

  btnTelemetry.classList.toggle('active', viewName === 'telemetry');
  btnRiskzone.classList.toggle('active', viewName === 'riskzone');
  if (btnWeather) btnWeather.classList.toggle('active', viewName === 'weather');

  viewTelemetry.style.display = (viewName === 'telemetry') ? 'block' : 'none';
  viewRiskzone.style.display = (viewName === 'riskzone') ? 'block' : 'none';
  if (viewWeather) viewWeather.style.display = (viewName === 'weather') ? 'block' : 'none';
}

/* ==========================================================================
   Weather Widget Updater
   ========================================================================== */
async function updateWeatherWidget(stateName) {
  try {
    const res = await fetch(`/api/weather?state=${encodeURIComponent(stateName || 'Manipur')}`);
    const wth = await res.json();
    state.weatherData = wth;

    const titleEl = document.getElementById('wth-state-name');
    if (titleEl) titleEl.textContent = `${wth.state} Regional Weather`;
    document.getElementById('wth-condition').textContent = `🌧️ ${wth.condition}`;
    document.getElementById('wth-trend').textContent = `Trend: ${wth.trend}`;
    document.getElementById('wth-temp').textContent = `${wth.temp_c} °C`;
    document.getElementById('wth-rain-1h').textContent = `${wth.rainfall_1h} mm/hr`;
    document.getElementById('wth-rain-6h').textContent = `${wth.rainfall_6h} mm`;
    document.getElementById('wth-rain-24h').textContent = `${wth.rainfall_24h} mm`;
    document.getElementById('wth-forecast').textContent = `${wth.forecast_rain_24h} mm`;
  } catch (err) {
    console.error("Weather fetch error:", err);
  }
}

/* ==========================================================================
   FEATURE 6: Offline Emergency Communication Controller
   ========================================================================== */
async function toggleNetworkMode() {
  try {
    const res = await fetch('/api/communication/toggle-network', { method: 'POST' });
    const data = await res.json();
    state.commStatus = data;
    state.isNetworkOnline = data.is_online;

    const btn = document.getElementById('btn-network-toggle');
    const txt = document.getElementById('txt-network-mode');
    const pill = document.getElementById('comm-net-pill');

    if (data.is_online) {
      btn.className = 'btn-network-status online';
      txt.textContent = 'ONLINE';
      if (pill) {
        pill.className = 'badge-risk normal';
        pill.textContent = 'ONLINE';
      }
      alert("📶 NETWORK CONNECTION RESTORED!\nAutomatic queue synchronization initiated.");
    } else {
      btn.className = 'btn-network-status offline';
      txt.textContent = 'OFFLINE (STORE-AND-FORWARD)';
      if (pill) {
        pill.className = 'badge-risk extreme';
        pill.textContent = 'NETWORK OFFLINE';
      }
      alert("⚠️ NETWORK OFFLINE!\nEmergency alerts will be buffered in local storage until connectivity returns.");
    }

    updateCommunicationUI(data);
  } catch (err) {
    console.error("Network toggle error:", err);
  }
}

async function syncCommunicationQueue() {
  try {
    const res = await fetch('/api/communication/sync', { method: 'POST' });
    const data = await res.json();
    alert(`🔄 Queue Synced!\n${data.synced_count} pending messages delivered to SDMA & public response channels.`);
    updateCommunicationUI(data.details);
  } catch (err) {
    console.error(err);
  }
}

async function testEmergencyDispatch() {
  try {
    const res = await fetch('/api/communication/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        alert_id: "ALT-TEST-001",
        location: "Tupul Railway Sector, Manipur",
        headline: "CRITICAL HAZARD: Simulated slope movement alert."
      })
    });
    const data = await res.json();
    alert(`🚨 Emergency Dispatch Queued!\nStatus: ${data.network_status}\nPending Queue: ${data.pending_messages_count}`);
    updateCommunicationUI(data);
  } catch (err) {
    console.error(err);
  }
}

function updateCommunicationUI(comm) {
  const pendingEl = document.getElementById('comm-pending-count');
  const delivEl = document.getElementById('comm-delivered-count');
  if (pendingEl) pendingEl.textContent = comm.pending_messages_count;
  if (delivEl) delivEl.textContent = comm.delivered_count.toLocaleString();
}

/* ==========================================================================
   FEATURE 7: Multi-Language Alert Localization Controller
   ========================================================================== */
async function switchAlertLanguage(langCode) {
  state.currentAlertLang = langCode;
  const select = document.getElementById('select-alert-lang');
  if (select) select.value = langCode;

  try {
    const res = await fetch(`/api/alerts/translations?lang=${langCode}`);
    const data = await res.json();
    renderTranslatedAlert(data);
  } catch (err) {
    console.error("Translation fetch error:", err);
  }
}

function renderTranslatedAlert(t) {
  const container = document.getElementById('translated-alert-container');
  if (!container) return;

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
      <div>
        <span class="badge-risk extreme" style="font-size:0.65rem;">${t.risk_level}</span>
        <h4 style="color:#fff; font-size:1.05rem; margin-top:3px;">${t.title}</h4>
      </div>
      <span style="font-size:0.75rem; color:#38bdf8; font-family:monospace;">${t.language_name}</span>
    </div>

    <div class="translated-field-row">
      <label>${t.location_label}</label>
      <div class="val">${t.location}</div>
    </div>

    <div class="translated-field-row">
      <label>${t.nearest_shelter_label}</label>
      <div class="val" style="color:#10b981;">🛡️ ${t.nearest_shelter}</div>
    </div>

    <div class="translated-field-row">
      <label>${t.action_label}</label>
      <div class="val" style="color:#fde047;">${t.action_directive}</div>
    </div>

    <div style="margin-top:0.6rem; padding-top:0.4rem; border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-between; font-size:0.70rem; color:var(--text-muted);">
      <span>${t.issuing_authority}</span>
      <span style="color:#f59e0b;">${t.disclaimer}</span>
    </div>
  `;
}

/* ==========================================================================
   FEATURE 3: Sensor Anomaly Action Controller
   ========================================================================== */
async function handleAnomalyAction(action) {
  if (!state.anomalies || state.anomalies.length === 0) return;
  const anom = state.anomalies[0];

  try {
    const res = await fetch('/api/sensors/anomalies/action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ anomaly_id: anom.id, action: action })
    });
    const data = await res.json();
    alert(`✅ Sensor Anomaly Action Applied: ${data.message}`);
    const updated = await fetch('/api/sensors/anomalies');
    state.anomalies = await updated.json();
    renderAnomalyCard(state.anomalies);
  } catch (err) {
    console.error(err);
  }
}

function renderAnomalyCard(anomalies) {
  const card = document.getElementById('anomaly-detail-card');
  const badge = document.getElementById('badge-anomaly-count');
  if (!card || !anomalies || anomalies.length === 0) return;

  const a = anomalies[0];
  if (badge) badge.textContent = `${anomalies.length} ANOMALIES LOGGED`;

  card.innerHTML = `
    <div style="display:flex; justify-content:space-between; font-size:0.75rem;">
      <span style="color:#fca5a5; font-weight:700;">STATION: ${a.station_name || a.station_id}</span>
      <span style="color:#ef4444; font-weight:800;">${a.status}</span>
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin:0.5rem 0; font-size:0.75rem;">
      <div>Previous: <strong style="color:#38bdf8;">${a.previous_val}</strong></div>
      <div>Anomalous: <strong style="color:#ef4444;">${a.anomalous_val}</strong></div>
    </div>
    <div style="font-size:0.72rem; color:#cbd5e1;">
      Reason: ${a.detection_reason}
    </div>
  `;
}

/* ==========================================================================
   Multi-Timeframe Chart.js Telemetry Graphing
   ========================================================================== */
function initChart() {
  const canvas = document.getElementById('telemetryChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  state.chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Pore Pressure (kPa)',
          data: [],
          borderColor: '#06b6d4',
          backgroundColor: 'rgba(6, 182, 212, 0.12)',
          fill: true,
          tension: 0.35,
          yAxisID: 'y'
        },
        {
          label: 'Tilt Rate (mm/h)',
          data: [],
          borderColor: '#ef4444',
          backgroundColor: 'transparent',
          borderDash: [4, 4],
          tension: 0.35,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          labels: { color: '#9ca3af', font: { size: 10, family: 'Inter' } }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#6b7280', font: { size: 9, family: 'JetBrains Mono' } }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#06b6d4', font: { size: 9, family: 'JetBrains Mono' } },
          title: { display: true, text: 'kPa', color: '#06b6d4', font: { size: 9 } }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: { color: '#ef4444', font: { size: 9, family: 'JetBrains Mono' } },
          title: { display: true, text: 'mm/h', color: '#ef4444', font: { size: 9 } }
        }
      }
    }
  });

  document.querySelectorAll('.time-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const tf = e.target.getAttribute('data-time');
      state.currentTimeframe = tf;
      if (state.selectedStationId) {
        const res = await fetch(`/api/sensor-readings?station_id=${state.selectedStationId}&interval=${tf}`);
        const data = await res.json();
        updateChartData(data);
      }
    });
  });
}

function updateChartData(timeseries) {
  if (!state.chart || !timeseries) return;
  state.chart.data.labels = timeseries.map(t => t.timestamp);
  state.chart.data.datasets[0].data = timeseries.map(t => t.pore_water_pressure);
  state.chart.data.datasets[1].data = timeseries.map(t => t.tilt_rate);
  state.chart.update('none');
}

/* ==========================================================================
   Data Ingestion & Initial Loader
   ========================================================================== */
async function loadInitialData() {
  try {
    const [overviewRes, stationsRes, corridorsRes, railwaysRes, infraRes, satRes, sheltersRes, statesRes, alertsRes, anomRes, commRes, histRes, reportsRes, healthRes, timelineRes] = await Promise.all([
      fetch('/api/overview'),
      fetch('/api/stations'),
      fetch('/api/corridors'),
      fetch('/api/railways'),
      fetch('/api/infrastructure'),
      fetch('/api/satellite/changes'),
      fetch('/api/shelters'),
      fetch('/api/states'),
      fetch('/api/alerts'),
      fetch('/api/sensors/anomalies'),
      fetch('/api/communication/status'),
      fetch('/api/history/landslides'),
      fetch('/api/reports'),
      fetch('/api/sensor-health'),
      fetch('/api/alerts/timeline')
    ]);

    const overview = await overviewRes.json();
    state.stations = await stationsRes.json();
    state.corridors = await corridorsRes.json();
    state.railways = await railwaysRes.json();
    state.infrastructure = await infraRes.json();
    state.satelliteChanges = await satRes.json();
    state.shelters = await sheltersRes.json();
    state.states = await statesRes.json();
    state.alerts = await alertsRes.json();
    state.anomalies = await anomRes.json();
    state.commStatus = await commRes.json();
    state.historicalEvents = await histRes.json();
    state.citizenReports = await reportsRes.json();
    const health = await healthRes.json();
    const timeline = await timelineRes.json();

    // Update KPI Ribbon
    document.getElementById('kpi-stations-count').textContent = `${state.stations.length} / ${state.stations.length}`;
    document.getElementById('kpi-high-risk-count').textContent = overview.high_risk_stations_count;
    document.getElementById('kpi-max-rain').textContent = overview.max_regional_rainfall_24h_mm;
    document.getElementById('kpi-shelters-count').textContent = `${state.shelters.length} Nodes`;
    document.getElementById('tab-alerts-count').textContent = state.alerts.length;

    if (overview.risk_breakdown) {
      document.getElementById('cnt-risk-critical').textContent = overview.risk_breakdown.critical;
      document.getElementById('cnt-risk-high').textContent = overview.risk_breakdown.high;
      document.getElementById('cnt-risk-mod').textContent = overview.risk_breakdown.moderate;
      document.getElementById('cnt-risk-low').textContent = overview.risk_breakdown.low;
    }

    if (state.alerts.length > 0) {
      document.getElementById('ticker-text').textContent = `🚨 ${state.alerts[0].headline} — ${state.alerts[0].instruction}`;
    }

    // Populate Station Selectors
    const stationSelect = document.getElementById('select-active-station');
    const evacSelect = document.getElementById('evac-select-station');
    stationSelect.innerHTML = '';
    evacSelect.innerHTML = '';

    state.stations.forEach(s => {
      const opt1 = document.createElement('option');
      opt1.value = s.id;
      opt1.textContent = `${s.name} (${s.state})`;
      stationSelect.appendChild(opt1);

      const opt2 = document.createElement('option');
      opt2.value = s.id;
      opt2.textContent = `${s.name} [${s.state}]`;
      evacSelect.appendChild(opt2);
    });

    // Render WebGIS Layers (10 Layers)
    renderMapStations();
    renderMapCorridors();
    renderMapRailways();
    renderMapInfrastructure();
    renderMapShelters();
    renderMapSatelliteChanges();
    renderMapHistorical();
    renderMapRadar();
    renderRiskGridHeatmap();

    // Render Secondary Views & 7 Advanced Modules
    renderStateMatrix();
    renderAlertsList();
    renderAlertTimeline(timeline);
    renderSensorHealth(health);
    renderAnomalyCard(state.anomalies);
    updateCommunicationUI(state.commStatus);
    switchAlertLanguage('en');
    renderAuthorityView();
    renderHistoricalLandslides(state.historicalEvents);
    renderCitizenReports(state.citizenReports);

    // Default Focus: Tupul Sentinel
    const defaultStation = state.stations.find(s => s.id === 'STN-MAN-01') || state.stations[0];
    if (defaultStation) {
      selectStation(defaultStation.id, false);
    }

  } catch (err) {
    console.error("Initial data loading error:", err);
  }
}

async function syncTelemetry(multiplier = 1.0) {
  try {
    const res = await fetch(`/api/telemetry/tick?intensity_multiplier=${multiplier}`, { method: 'POST' });
    const data = await res.json();
    state.stations = data.stations;

    renderMapStations();
    if (state.selectedStationId) {
      selectStation(state.selectedStationId, false);
    }
  } catch (err) {
    console.error("Telemetry sync error:", err);
  }
}

/* ==========================================================================
   State Filter Synchronization
   ========================================================================== */
function focusOnState(stateName) {
  state.selectedState = stateName;
  const select = document.getElementById('select-state-focus');
  if (select) select.value = stateName;

  if (stateName === 'ALL') {
    state.map.flyTo([25.75, 92.85], 7, { duration: 1.2 });
  } else {
    const st = state.states[stateName];
    if (st && state.map) {
      state.map.flyTo([st.lat, st.lng], st.zoom || 9, { duration: 1.2 });
      const matchedStn = state.stations.find(s => s.state.toLowerCase() === stateName.toLowerCase());
      if (matchedStn) {
        selectStation(matchedStn.id, false);
      }
    }
  }

  fetch(`/api/overview?state=${encodeURIComponent(stateName)}`)
    .then(r => r.json())
    .then(ov => {
      document.getElementById('cnt-risk-critical').textContent = ov.risk_breakdown.critical;
      document.getElementById('cnt-risk-high').textContent = ov.risk_breakdown.high;
      document.getElementById('cnt-risk-mod').textContent = ov.risk_breakdown.moderate;
      document.getElementById('cnt-risk-low').textContent = ov.risk_breakdown.low;
    });

  updateWeatherWidget(stateName);
}

/* ==========================================================================
   Timeline, Health & Authority Renderers
   ========================================================================== */
function renderAlertTimeline(timelineEvents) {
  const container = document.getElementById('alert-timeline-container');
  if (!container) return;
  container.innerHTML = '';

  timelineEvents.forEach(ev => {
    const el = document.createElement('div');
    el.className = `timeline-event-card ${ev.severity.toLowerCase()}`;
    el.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.75rem; font-weight:700; color:#38bdf8; font-family:monospace;">${ev.time}</span>
        <span class="badge-risk ${ev.severity === 'CRITICAL' ? 'extreme' : 'high'}" style="font-size:0.65rem;">${ev.severity}</span>
      </div>
      <div style="color:#fff; font-size:0.85rem; font-weight:700; margin-top:2px;">${ev.event}</div>
      <div style="font-size:0.75rem; color:#94a3b8;">${ev.location}</div>
      <p style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">${ev.description}</p>
    `;
    container.appendChild(el);
  });
}

function renderSensorHealth(healthData) {
  const container = document.getElementById('sensor-health-container');
  if (!container) return;
  container.innerHTML = '';

  const records = healthData.station_records || [];
  records.forEach(r => {
    const isOnline = (r.status === 'ONLINE');
    const card = document.createElement('div');
    card.className = 'sensor-health-card';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4 style="color:#fff; font-size:0.95rem;">${r.station_id}</h4>
        <span class="badge-risk ${isOnline ? 'normal' : 'extreme'}" style="font-size:0.65rem;">${r.status}</span>
      </div>
      <div class="health-metric-row">
        <span>Battery Reserve</span>
        <strong style="color:${r.battery_pct > 80 ? '#10b981' : '#f97316'};">${r.battery_pct}% (${r.solar_charging_v}V Solar)</strong>
      </div>
      <div class="health-gauge-bar">
        <div style="background:${r.battery_pct > 80 ? '#10b981' : '#f97316'}; width:${r.battery_pct}%; height:100%;"></div>
      </div>
      <div class="health-metric-row" style="margin-top:6px;">
        <span>Wireless Signal</span>
        <strong style="color:#38bdf8;">${r.signal_strength_dbm} dBm</strong>
      </div>
      <div class="health-metric-row">
        <span>Historical Uptime</span>
        <strong style="color:#fff;">${r.uptime_pct}%</strong>
      </div>
      <div class="health-metric-row">
        <span>Data Integrity Quality</span>
        <strong style="color:#10b981;">${r.data_quality_pct}%</strong>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderAuthorityView() {
  const dirContainer = document.getElementById('auth-directives-container');
  const incContainer = document.getElementById('auth-incidents-container');
  if (!dirContainer || !incContainer) return;

  dirContainer.innerHTML = `
    <div class="directive-card" style="border-left:4px solid #ef4444;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4 style="color:#fff; font-size:0.92rem;">🚨 IMMEDIATE EVACUATION: Tupul Mountain Sector</h4>
        <span class="badge-risk extreme" style="font-size:0.65rem;">CRITICAL DIRECTIVE</span>
      </div>
      <p style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">
        Direct SDRF 12th Battalion convoy along northern high ridge road. Close NH-37 km 48 to heavy vehicles.
      </p>
      <div style="margin-top:6px; font-size:0.72rem; color:#38bdf8;">Assigned Relief Hub: <strong>Noney District Headquarter Safe Relief Shelter</strong></div>
    </div>
  `;

  incContainer.innerHTML = '';
  state.citizenReports.slice(0, 4).forEach(rep => {
    const card = document.createElement('div');
    card.className = 'incident-review-card';
    card.style.marginBottom = '8px';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <h4 style="color:#fff; font-size:0.90rem;">${rep.location_name} (${rep.state})</h4>
        <span class="badge-risk normal" style="font-size:0.65rem;">VERIFIED DISPATCH</span>
      </div>
      <div style="font-size:0.75rem; color:#38bdf8;">Reporter: ${rep.reporter_name} • Type: ${rep.landslide_type}</div>
      <div style="font-size:0.72rem; color:#fca5a5; margin-top:3px;">${rep.road_blocked ? '🚨 Highway Blocked' : 'Road Open'} • Casualties: ${rep.casualties_reported}</div>
    `;
    incContainer.appendChild(card);
  });
}

function renderStateMatrix() {
  const container = document.getElementById('states-grid-container');
  if (!container) return;
  container.innerHTML = '';

  Object.entries(state.states).forEach(([stName, stData]) => {
    const card = document.createElement('div');
    card.className = 'glass-panel state-matrix-card';
    card.style.padding = '1.1rem';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <h3 style="color:#fff; font-size:1.1rem;">${stName}</h3>
        <span class="badge-risk ${stData.vulnerability_level === 'EXTREME' || stData.vulnerability_level === 'VERY HIGH' ? 'extreme' : 'high'}" style="font-size:0.65rem;">
          ${stData.vulnerability_level}
        </span>
      </div>
      <div style="font-size:0.75rem; color:#38bdf8; margin:2px 0 6px 0;">Capital: ${stData.capital} • Annual Rain: ${stData.annual_rainfall_mm}mm</div>
      <div style="font-size:0.75rem; color:#cbd5e1; line-height:1.35;">${stData.description}</div>
      <div style="margin-top:8px; font-size:0.72rem; color:#fca5a5;"><strong>Hotspots:</strong> ${stData.districts_at_risk.join(', ')}</div>
      <button onclick="focusOnState('${stName}')" class="btn btn-outline" style="width:100%; margin-top:10px; font-size:0.75rem; padding:4px 8px;">
        🗺️ Focus State in GIS
      </button>
    `;
    container.appendChild(card);
  });
}

function renderAlertsList() {
  const container = document.getElementById('alerts-list-container');
  if (!container) return;
  container.innerHTML = '';

  state.alerts.forEach(a => {
    const card = document.createElement('div');
    card.className = 'glass-panel';
    card.style.padding = '1rem';
    card.style.borderLeft = '4px solid #ef4444';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <span class="badge-risk extreme" style="font-size:0.65rem;">${a.severity.toUpperCase()}</span>
          <h3 style="color:#fff; font-size:1.05rem; margin-top:3px;">${a.headline}</h3>
          <div style="font-size:0.75rem; color:#94a3b8;">${a.region_name} (${a.state}) • Alert ID: ${a.alert_id}</div>
        </div>
        <button onclick="viewCapXml('${a.alert_id}')" class="btn btn-outline" style="font-size:0.72rem; padding:4px 8px;">
          📜 CAP XML
        </button>
      </div>
      <p style="font-size:0.80rem; color:#cbd5e1; margin:8px 0;">${a.description}</p>
      <div style="font-size:0.78rem; color:#38bdf8; font-weight:600;">Directive: ${a.instruction}</div>
    `;
    container.appendChild(card);
  });
}

function renderHistoricalLandslides(events) {
  const container = document.getElementById('historical-landslides-container');
  if (!container) return;
  container.innerHTML = '';

  events.forEach(ev => {
    const el = document.createElement('div');
    el.className = 'glass-panel';
    el.style.padding = '0.85rem';
    el.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <h4 style="color:#fff; font-size:0.92rem;">${ev.name}</h4>
        <span style="font-size:0.72rem; color:#94a3b8; font-family:monospace;">${ev.event_date || ev.date}</span>
      </div>
      <div style="font-size:0.75rem; color:#38bdf8;">${ev.district}, ${ev.state} • Volume: ${ev.volume_m3?.toLocaleString()} m³</div>
      <div style="font-size:0.78rem; color:#cbd5e1; margin-top:4px;"><strong>Trigger:</strong> ${ev.trigger_factor || ev.trigger}</div>
      <div style="font-size:0.75rem; color:#fca5a5; margin-top:2px;">${ev.infrastructure_damage}</div>
    `;
    container.appendChild(el);
  });
}

function renderCitizenReports(reports) {
  const container = document.getElementById('citizen-reports-container');
  if (!container) return;
  container.innerHTML = '';

  if (reports.length === 0) {
    container.innerHTML = '<div style="font-size:0.82rem; color:#94a3b8;">No citizen reports currently in queue.</div>';
    return;
  }

  reports.forEach(r => {
    const el = document.createElement('div');
    el.className = 'glass-panel';
    el.style.padding = '0.85rem';
    el.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <h4 style="color:#fff; font-size:0.92rem;">${r.location_name} (${r.state})</h4>
        <span class="badge-risk high" style="font-size:0.65rem;">${r.status}</span>
      </div>
      <div style="font-size:0.75rem; color:#38bdf8;">Reported by: ${r.reporter_name} • Type: ${r.landslide_type} (${r.estimated_size})</div>
      <div style="font-size:0.78rem; color:#fca5a5; margin-top:4px;">
        ${r.road_blocked ? '🚨 Highway Blocked' : 'Road Clear'} • Casualties: ${r.casualties_reported}
      </div>
    `;
    container.appendChild(el);
  });
}

/* ==========================================================================
   AI What-If Simulation Sandbox
   ========================================================================== */
function initSimulationListeners() {
  const sliders = [
    { id: 'sim-rain-intensity', valId: 'val-sim-rain', unit: ' mm/hr' },
    { id: 'sim-duration', valId: 'val-sim-duration', unit: ' hrs' },
    { id: 'sim-slope', valId: 'val-sim-slope', unit: '°' },
    { id: 'sim-pwp', valId: 'val-sim-pwp', unit: ' kPa' },
    { id: 'sim-moisture', valId: 'val-sim-moisture', unit: '%' },
    { id: 'sim-seismic', valId: 'val-sim-seismic', unit: ' g' }
  ];

  sliders.forEach(s => {
    const input = document.getElementById(s.id);
    if (!input) return;
    input.addEventListener('input', (e) => {
      document.getElementById(s.valId).textContent = e.target.value + s.unit;
      runSimulationUpdate();
    });
  });

  const stateSelect = document.getElementById('sim-state');
  const lithSelect = document.getElementById('sim-lithology');
  if (stateSelect) stateSelect.addEventListener('change', runSimulationUpdate);
  if (lithSelect) lithSelect.addEventListener('change', runSimulationUpdate);
}

async function runSimulationUpdate() {
  const payload = {
    state: document.getElementById('sim-state') ? document.getElementById('sim-state').value : 'Manipur',
    rainfall_intensity_mm_hr: parseFloat(document.getElementById('sim-rain-intensity').value),
    duration_hrs: parseFloat(document.getElementById('sim-duration').value),
    slope_deg: parseFloat(document.getElementById('sim-slope').value),
    pore_water_pressure_kpa: parseFloat(document.getElementById('sim-pwp').value),
    soil_moisture_pct: parseFloat(document.getElementById('sim-moisture').value),
    seismic_coeff_kh: parseFloat(document.getElementById('sim-seismic').value),
    lithology: document.getElementById('sim-lithology') ? document.getElementById('sim-lithology').value : 'Weak Disang Shale'
  };

  try {
    const res = await fetch('/api/simulate/whatif', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    document.getElementById('sim-composite-score').textContent = data.composite_risk_score;
    document.getElementById('sim-composite-tier').textContent = data.composite_tier;
    document.getElementById('sim-composite-tier').style.color = data.composite_color;
    document.getElementById('sim-advisory-text').textContent = data.advisory;

    const badge = document.getElementById('sim-result-badge');
    badge.textContent = data.composite_tier.split('-')[0].trim();
    badge.style.background = data.composite_color;

    const fs = data.factor_of_safety_analysis;
    document.getElementById('sim-val-fs').textContent = fs.factor_of_safety;
    document.getElementById('sim-val-fs').style.color = fs.factor_of_safety < 1.0 ? '#ef4444' : '#10b981';
    document.getElementById('sim-fs-text').textContent = fs.stability_status;

    const idThresh = data.rainfall_id_threshold;
    document.getElementById('sim-val-id').textContent = `${idThresh.threshold_percentage}%`;
    document.getElementById('sim-id-text').textContent = idThresh.stage;

    const factorContainer = document.getElementById('sim-factor-bars');
    factorContainer.innerHTML = '';
    const factors = data.ai_susceptibility_model.factor_breakdown || {};
    Object.entries(factors).forEach(([k, v]) => {
      const row = document.createElement('div');
      row.style.marginBottom = '6px';
      row.innerHTML = `
        <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#cbd5e1; margin-bottom:2px;">
          <span>${k.toUpperCase()}</span>
          <span>${v}%</span>
        </div>
        <div style="background:rgba(255,255,255,0.08); height:6px; border-radius:3px; overflow:hidden;">
          <div style="background:#06b6d4; height:100%; width:${v}%;"></div>
        </div>
      `;
      factorContainer.appendChild(row);
    });

  } catch (err) {
    console.error("Simulation error:", err);
  }
}

/* ==========================================================================
   Utility Helpers
   ========================================================================== */
function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371.0;
  const dLat = (lat2 - lat1) * Math.PI / 180.0;
  const dLon = (lon2 - lon1) * Math.PI / 180.0;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180.0) * Math.cos(lat2 * Math.PI / 180.0) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function openModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.add('open');
}

function closeModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.remove('open');
}

async function viewCapXml(alertId) {
  try {
    const res = await fetch(`/api/alerts/${alertId}/cap-xml`);
    const xml = await res.text();
    document.getElementById('cap-xml-content').textContent = xml;
    openModal('modal-cap-bulletin');
  } catch (err) {
    console.error(err);
  }
}

/* ==========================================================================
   Event Handlers Registration
   ========================================================================== */
function initEventListeners() {
  document.getElementById('btn-sync-telemetry').addEventListener('click', () => {
    syncTelemetry(1.2);
  });

  document.getElementById('btn-network-toggle').addEventListener('click', toggleNetworkMode);

  document.getElementById('select-state-focus').addEventListener('change', (e) => {
    focusOnState(e.target.value);
  });

  document.getElementById('select-user-role').addEventListener('change', (e) => {
    state.userRole = e.target.value;
    alert(`Switched View Mode to: ${state.userRole}`);
  });

  document.getElementById('select-active-station').addEventListener('change', (e) => {
    selectStation(e.target.value, true);
  });

  // Inspector tab buttons
  document.getElementById('btn-insp-telemetry').addEventListener('click', () => showInspectorView('telemetry'));
  document.getElementById('btn-insp-riskzone').addEventListener('click', () => showInspectorView('riskzone'));
  const btnWth = document.getElementById('btn-insp-weather');
  if (btnWth) btnWth.addEventListener('click', () => showInspectorView('weather'));

  // Stress test button
  document.getElementById('btn-stress-test').addEventListener('click', async () => {
    if (!state.selectedStationId) return;
    try {
      const res = await fetch('/api/simulate/disaster-scenario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ station_id: state.selectedStationId, scenario_type: 'EXTREME_DELUGE' })
      });
      const data = await res.json();
      alert(`⚠️ CLOUDBURST SPIKE INJECTED!\n${data.message}`);
      await syncTelemetry(1.0);
      selectStation(state.selectedStationId, true);
    } catch (err) {
      console.error(err);
    }
  });

  document.getElementById('btn-plan-evac-station').addEventListener('click', () => {
    calculateSafeRouteToShelter(null);
  });

  document.getElementById('btn-calc-evacuation').addEventListener('click', () => {
    const stnId = document.getElementById('evac-select-station').value;
    const stn = state.stations.find(s => s.id === stnId);
    if (stn) {
      selectStation(stn.id, true);
      calculateSafeRouteToShelter(null);
      switchTab('tab-gis');
    }
  });

  document.getElementById('btn-basemap-toggle').addEventListener('click', (e) => {
    if (state.currentBaseLayer === 'dark') {
      state.map.removeLayer(state.baseLayers.dark);
      state.baseLayers.satellite.addTo(state.map);
      state.currentBaseLayer = 'satellite';
      e.target.textContent = '🗺️ Dark Mode';
    } else {
      state.map.removeLayer(state.baseLayers.satellite);
      state.baseLayers.dark.addTo(state.map);
      state.currentBaseLayer = 'dark';
      e.target.textContent = '🛰️ Satellite';
    }
  });

  // Layer Toggles (10 Layers)
  document.getElementById('toggle-layer-stations').addEventListener('click', (e) => toggleLayer(state.layers.stations, e.target));
  document.getElementById('toggle-layer-corridors').addEventListener('click', (e) => toggleLayer(state.layers.corridors, e.target));
  document.getElementById('toggle-layer-railways').addEventListener('click', (e) => toggleLayer(state.layers.railways, e.target));
  document.getElementById('toggle-layer-infra').addEventListener('click', (e) => toggleLayer(state.layers.infra, e.target));
  document.getElementById('toggle-layer-shelters').addEventListener('click', (e) => toggleLayer(state.layers.shelters, e.target));
  document.getElementById('toggle-layer-sat-change').addEventListener('click', (e) => toggleLayer(state.layers.satChange, e.target));
  document.getElementById('toggle-layer-heatmap').addEventListener('click', (e) => toggleLayer(state.layers.heatmap, e.target));
  document.getElementById('toggle-layer-historical').addEventListener('click', (e) => toggleLayer(state.layers.historical, e.target));
  document.getElementById('toggle-layer-radar').addEventListener('click', (e) => toggleLayer(state.layers.radar, e.target));

  // Advanced Suite Features Handlers
  document.getElementById('btn-sat-compare-toggle').addEventListener('click', () => {
    const b = document.getElementById('sat-img-before');
    const c = document.getElementById('sat-img-current');
    if (state.satCompareState === 'split') {
      b.style.display = 'flex';
      c.style.display = 'none';
      state.satCompareState = 'before_only';
    } else if (state.satCompareState === 'before_only') {
      b.style.display = 'none';
      c.style.display = 'flex';
      state.satCompareState = 'current_only';
    } else {
      b.style.display = 'flex';
      c.style.display = 'flex';
      state.satCompareState = 'split';
    }
  });

  document.getElementById('btn-sat-view-map').addEventListener('click', () => {
    switchTab('tab-gis');
    if (state.satelliteChanges.length > 0) {
      const c = state.satelliteChanges[0];
      state.map.flyTo([c.latitude, c.longitude], 13, { duration: 1.0 });
    }
  });

  // Sensor Anomaly Action Buttons
  document.getElementById('btn-anom-view').addEventListener('click', () => {
    selectStation('STN-MAN-01', true);
    switchTab('tab-gis');
  });
  document.getElementById('btn-anom-ack').addEventListener('click', () => handleAnomalyAction('acknowledge'));
  document.getElementById('btn-anom-maint').addEventListener('click', () => handleAnomalyAction('maintenance'));

  // Offline Communication Buttons
  document.getElementById('btn-comm-toggle-net').addEventListener('click', toggleNetworkMode);
  document.getElementById('btn-comm-sync-now').addEventListener('click', syncCommunicationQueue);
  document.getElementById('btn-comm-test-alert').addEventListener('click', testEmergencyDispatch);

  // Multilingual Selector
  document.getElementById('select-alert-lang').addEventListener('change', (e) => {
    switchAlertLanguage(e.target.value);
  });

  // Open Sandbox Trigger from Advanced Tab
  document.getElementById('btn-adv-run-sim').addEventListener('click', () => {
    switchTab('tab-simulation');
  });

  // Incident Modal
  document.getElementById('btn-open-report-modal').addEventListener('click', () => openModal('modal-citizen-report'));
  document.getElementById('btn-open-citizen-report-2').addEventListener('click', () => openModal('modal-citizen-report'));

  document.getElementById('form-citizen-report').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      reporter_name: document.getElementById('rep-name').value,
      contact_number: document.getElementById('rep-contact').value,
      state: document.getElementById('rep-state').value,
      location_name: document.getElementById('rep-location').value,
      latitude: parseFloat(document.getElementById('rep-lat').value),
      longitude: parseFloat(document.getElementById('rep-lng').value),
      landslide_type: document.getElementById('rep-type').value,
      estimated_size: document.getElementById('rep-size').value,
      road_blocked: document.getElementById('rep-blocked').checked,
      casualties_reported: document.getElementById('rep-casualties').checked ? 1 : 0,
      description: document.getElementById('rep-desc').value
    };

    try {
      const res = await fetch('/api/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      alert(`✅ Incident Report Logged!\nReport ID: ${data.report_id}\nDisaster verification dispatched.`);
      closeModal('modal-citizen-report');
      const reportsRes = await fetch('/api/incidents');
      const reports = await reportsRes.json();
      renderCitizenReports(reports);
    } catch (err) {
      alert("Submission error: " + err);
    }
  });

  document.getElementById('btn-export-sim-bulletin').addEventListener('click', () => {
    window.print();
  });
}

function toggleLayer(layerGroup, btn) {
  if (state.map.hasLayer(layerGroup)) {
    state.map.removeLayer(layerGroup);
    btn.classList.remove('active');
  } else {
    state.map.addLayer(layerGroup);
    btn.classList.add('active');
  }
}

// Global exposes for HTML onclick triggers
window.selectStation = selectStation;
window.focusOnState = focusOnState;
window.openShelterDetails = openShelterDetails;
window.calculateSafeRouteToShelter = calculateSafeRouteToShelter;
window.closeModal = closeModal;
window.openModal = openModal;
window.viewCapXml = viewCapXml;
