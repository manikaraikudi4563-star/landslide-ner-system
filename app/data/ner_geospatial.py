"""
Geospatial and geotechnical metadata for the North Eastern Region (NER) of India.
Covers Sikkim, Meghalaya, Assam, Arunachal Pradesh, Nagaland, Manipur, Mizoram, and Tripura.
"""

from typing import List, Dict, Any

NER_STATES = {
    "Sikkim": {
        "capital": "Gangtok",
        "lat": 27.5330,
        "lng": 88.5122,
        "zoom": 9,
        "vulnerability_score": 92,
        "vulnerability_level": "VERY HIGH",
        "geology": "Pre-Cambrian Daling Group Phyllites, Schists, Fragile Gneiss",
        "seismic_zone": "Zone IV - Zone V",
        "annual_rainfall_mm": 3400,
        "districts_at_risk": ["Mangan (North Sikkim)", "Gangtok (East Sikkim)", "Namchi (South Sikkim)", "Gyalshing (West Sikkim)"],
        "description": "Steep Himalayan slopes with high seismicity, glacial lake outburst flood (GLOF) vulnerabilities, and heavy monsoonal triggers along the Teesta valley."
    },
    "Meghalaya": {
        "capital": "Shillong",
        "lat": 25.4670,
        "lng": 91.3662,
        "zoom": 9,
        "vulnerability_score": 88,
        "vulnerability_level": "VERY HIGH",
        "geology": "Shillong Group Quartzites, Sedimentary Sandstone, Limestone Karst",
        "seismic_zone": "Zone V",
        "annual_rainfall_mm": 11500,
        "districts_at_risk": ["East Khasi Hills (Sohra/Cherrapunji)", "West Khasi Hills (Mawsynram)", "East Jaintia Hills", "Ri-Bhoi"],
        "description": "Home to the wettest places on Earth (Mawsynram and Cherrapunji). Extreme rainfall intensity triggers deep-seated rockfalls and mudslides on plateau escarpments."
    },
    "Assam": {
        "capital": "Dispur",
        "lat": 26.2006,
        "lng": 92.9376,
        "zoom": 8,
        "vulnerability_score": 85,
        "vulnerability_level": "HIGH",
        "geology": "Barail Group Sandstones, Disang Shales, Alluvial Overburdens",
        "seismic_zone": "Zone V",
        "annual_rainfall_mm": 2800,
        "districts_at_risk": ["Dima Hasao (Haflong)", "Karbi Anglong", "Kamrup Metro (Guwahati Hills)", "Cachar"],
        "description": "Dima Hasao and Karbi Anglong hill tracts suffer catastrophic slope failures during monsoon, frequently snapping railway and highway links between Brahmaputra and Barak valleys."
    },
    "Manipur": {
        "capital": "Imphal",
        "lat": 24.6637,
        "lng": 93.9063,
        "zoom": 9,
        "vulnerability_score": 90,
        "vulnerability_level": "VERY HIGH",
        "geology": "Disang Series splintery shales, Turbidites, Weathered clay layers",
        "seismic_zone": "Zone V",
        "annual_rainfall_mm": 2100,
        "districts_at_risk": ["Noney (Tupul railway section)", "Tamenglong", "Senapati", "Churachandpur"],
        "description": "Fragile shale lithology prone to liquefied mud-debris avalanches, notably the June 2022 Tupul railway construction site tragedy."
    },
    "Nagaland": {
        "capital": "Kohima",
        "lat": 25.6751,
        "lng": 94.1086,
        "zoom": 9,
        "vulnerability_score": 87,
        "vulnerability_level": "VERY HIGH",
        "geology": "Disang & Barail Formations, highly sheared siltstones and sandstones",
        "seismic_zone": "Zone V",
        "annual_rainfall_mm": 2500,
        "districts_at_risk": ["Kohima (NH-29 corridor)", "Phek", "Wokha", "Mokokchung"],
        "description": "Continuous creep and severe sinking zones along the NH-29 Lifeline, exacerbated by active tectonic shearing and hill toe erosion."
    },
    "Mizoram": {
        "capital": "Aizawl",
        "lat": 23.1645,
        "lng": 92.9376,
        "zoom": 9,
        "vulnerability_score": 86,
        "vulnerability_level": "VERY HIGH",
        "geology": "Surma Group Sandstone and Mudstone alternating strata",
        "seismic_zone": "Zone V",
        "annual_rainfall_mm": 2900,
        "districts_at_risk": ["Aizawl (Hunthar & Bawngkawn)", "Lunglei", "Champhai", "Serchhip"],
        "description": "Steep north-south parallel ridges with high urban slope density and fragile sandstone bedding prone to massive translational slides."
    },
    "Arunachal Pradesh": {
        "capital": "Itanagar",
        "lat": 28.2180,
        "lng": 94.7278,
        "zoom": 8,
        "vulnerability_score": 94,
        "vulnerability_level": "EXTREME",
        "geology": "Siwalik Supergroup, Main Boundary Thrust (MBT), Gneissic Complexes",
        "seismic_zone": "Zone V",
        "annual_rainfall_mm": 3800,
        "districts_at_risk": ["Tawang", "West Kameng (Bomdila)", "Subansiri", "Dibang Valley", "Kurung Kumey"],
        "description": "Rugged eastern Himalayan terrain with massive road cutting along strategic mountain highways, heavy cloudbursts, and glacial activity."
    },
    "Tripura": {
        "capital": "Agartala",
        "lat": 23.8438,
        "lng": 91.2868,
        "zoom": 9,
        "vulnerability_score": 68,
        "vulnerability_level": "MODERATE-HIGH",
        "geology": "Tipam Sandstone and Dupitila Formations, unconsolidated silt",
        "seismic_zone": "Zone V",
        "annual_rainfall_mm": 2200,
        "districts_at_risk": ["North Tripura (Jampui Hills)", "Dhalai", "Gomati", "Unakoti"],
        "description": "Low anticline ridges with erosion-prone sandy soils subjected to flash flooding and shallow mudflows during peak depression storms."
    }
}

# Critical Infrastructure Corridors in NER
NER_CORRIDORS = [
    {
        "id": "CORR-NH10",
        "name": "NH-10 Sevoke - Gangtok Lifeline",
        "state": "Sikkim / West Bengal",
        "length_km": 114,
        "vulnerability": "CRITICAL",
        "key_hotspots": ["29th Mile", "Selfie Danda", "Birik Dara", "Singtam"],
        "path_coordinates": [
            [26.8820, 88.4730],
            [26.9600, 88.4400],
            [27.0500, 88.4300],
            [27.1500, 88.5000],
            [27.2300, 88.5200],
            [27.3389, 88.6065]
        ]
    },
    {
        "id": "CORR-NH6",
        "name": "NH-6 Guwahati - Shillong - Silchar Highway",
        "state": "Meghalaya / Assam",
        "length_km": 280,
        "vulnerability": "HIGH",
        "key_hotspots": ["Sonapur Tunnel", "Umsning Bypass", "Khliehriat Slope", "Ratacherra"],
        "path_coordinates": [
            [26.1445, 91.7362],
            [25.9000, 91.8800],
            [25.5788, 91.8933],
            [25.3500, 92.2000],
            [25.1000, 92.4000],
            [24.8333, 92.8000]
        ]
    },
    {
        "id": "CORR-NH27",
        "name": "NH-27 Haflong Hill Railway & Road Corridor",
        "state": "Assam",
        "length_km": 165,
        "vulnerability": "CRITICAL",
        "key_hotspots": ["New Haflong Station", "Jatinga Slips", "Mahur Valley", "Harangajao"],
        "path_coordinates": [
            [25.7500, 93.1800],
            [25.4000, 93.0500],
            [25.1667, 93.0167],
            [24.9800, 92.8500]
        ]
    },
    {
        "id": "CORR-NH29",
        "name": "NH-29 Dimapur - Kohima - Mao Lifeline",
        "state": "Nagaland",
        "length_km": 98,
        "vulnerability": "VERY HIGH",
        "key_hotspots": ["Phesama Sinking Zone", "Dzüdza Bridge", "Sechu Zubza", "Pagla Pahar"],
        "path_coordinates": [
            [25.9064, 93.7275],
            [25.8000, 93.8500],
            [25.7200, 93.9800],
            [25.6751, 94.1086],
            [25.5500, 94.1500]
        ]
    },
    {
        "id": "CORR-NH37",
        "name": "NH-37 & Tupul Railway Corridor",
        "state": "Manipur",
        "length_km": 220,
        "vulnerability": "EXTREME",
        "key_hotspots": ["Tupul Yard (2022 Disaster site)", "Noney Bridge", "Awangkhul", "Makru"],
        "path_coordinates": [
            [24.8000, 93.1200],
            [24.7500, 93.4500],
            [24.7083, 93.6500],
            [24.8170, 93.9368]
        ]
    },
    {
        "id": "CORR-NH13",
        "name": "Trans-Arunachal Highway (Bhalukpong - Tawang)",
        "state": "Arunachal Pradesh",
        "length_km": 320,
        "vulnerability": "EXTREME",
        "key_hotspots": ["Sela Pass Approach", "Bhalukpong Gorge", "Jaswant Garh", "Tenga Valley"],
        "path_coordinates": [
            [27.0100, 92.6500],
            [27.2600, 92.4200],
            [27.4500, 92.1500],
            [27.5861, 91.8653]
        ]
    },
    {
        "id": "CORR-NH54",
        "name": "NH-54 Silchar - Aizawl - Lunglei Corridor",
        "state": "Mizoram",
        "length_km": 190,
        "vulnerability": "HIGH",
        "key_hotspots": ["Hunthar Sinking Area", "Bawngkawn Junction", "Kolasib Cuttings"],
        "path_coordinates": [
            [24.8333, 92.8000],
            [24.2300, 92.6800],
            [23.7307, 92.7173],
            [22.8800, 92.7400]
        ]
    }
]

# Critical Railway Corridors in NER
NER_RAILWAYS = [
    {
        "id": "RLY-MAN-01",
        "name": "Jiribam - Tupul - Imphal Mountain Railway",
        "state": "Manipur",
        "length_km": 111,
        "vulnerability": "EXTREME",
        "key_hotspots": ["Tupul Station Yard (Bridge 164)", "Noney Super Pier 141m", "Haochong Cut", "Awangkhul"],
        "path_coordinates": [
            [24.8000, 93.1300],
            [24.7600, 93.3800],
            [24.7150, 93.6550],
            [24.7800, 93.8500],
            [24.8150, 93.9400]
        ]
    },
    {
        "id": "RLY-ASM-01",
        "name": "NF Railway Lumding - Badarpur Hill Section",
        "state": "Assam",
        "length_km": 185,
        "vulnerability": "CRITICAL",
        "key_hotspots": ["New Haflong Station Submergence", "Jatinga Track Slips", "Mahur Cuttings", "Diteckchera"],
        "path_coordinates": [
            [25.8000, 93.1500],
            [25.5000, 93.0800],
            [25.1700, 93.0100],
            [24.9500, 92.8300]
        ]
    },
    {
        "id": "RLY-SIK-01",
        "name": "Sevoke - Rangpo Himalayan Railway Project",
        "state": "Sikkim / West Bengal",
        "length_km": 45,
        "vulnerability": "VERY HIGH",
        "key_hotspots": ["Tunnel 10 Teesta Bank", "Melli Bridge", "Rangpo Terminus", "Sevoke Gorge"],
        "path_coordinates": [
            [26.8900, 88.4700],
            [27.0200, 88.4400],
            [27.1200, 88.5100],
            [27.1750, 88.5300]
        ]
    }
]

# Regional Risk Summary Statistics (Dynamic Breakdown)
REGIONAL_RISK_SUMMARY = {
    "total_evaluated_hotspots": 147,
    "critical_count": 3,
    "high_risk_count": 12,
    "moderate_risk_count": 28,
    "low_risk_count": 104,
    "iot_stations_online": 12,
    "total_shelters": 12,
    "peak_regional_rainfall_24h_mm": 68.4
}

# Chronological Alert & Event Timeline
CHRONOLOGICAL_ALERT_TIMELINE = [
    {
        "time": "20:48",
        "event": "Risk Tier Upgraded to CRITICAL (RED)",
        "station_id": "STN-MAN-01",
        "location": "Tupul Railway Yard Sentinel, Manipur",
        "severity": "CRITICAL",
        "description": "Composite AI Risk score breached 94.8% due to accelerating deep shear creep."
    },
    {
        "time": "20:35",
        "event": "Pore Water Pressure Surged",
        "station_id": "STN-MAN-01",
        "location": "Tupul Railway Yard Sentinel, Manipur",
        "severity": "HIGH",
        "description": "Vibrating Wire Piezometer reading escalated to 33.27 kPa following storm."
    },
    {
        "time": "20:20",
        "event": "Inclinometer Tilt Rate Accelerated",
        "station_id": "STN-MAN-01",
        "location": "Tupul Railway Yard Sentinel, Manipur",
        "severity": "HIGH",
        "description": "Biaxial MEMS sensor logged 0.341 mm/h creep exceeding yellow advisory threshold."
    },
    {
        "time": "19:55",
        "event": "Heavy Monsoon Cloudburst Detected",
        "station_id": "STN-MEG-01",
        "location": "Sohra Escarpment, Meghalaya",
        "severity": "HIGH",
        "description": "Optical Rain Radar registered 38.5 mm/hr peak cloudburst intensity."
    },
    {
        "time": "19:30",
        "event": "Regional AI Risk Susceptibility Synchronized",
        "station_id": "ALL",
        "location": "NER Central Command Hub",
        "severity": "NORMAL",
        "description": "Multi-criteria geospatial and geotechnical risk grid refreshed for all 8 states."
    }
]

# IoT Sensor Monitoring Stations (Virtual Network of Advanced Geotechnical Nodes)
IOT_STATIONS = [
    {
        "id": "STN-SIK-01",
        "name": "Gangtok - 29th Mile Observatory",
        "state": "Sikkim",
        "district": "East Sikkim",
        "corridor": "NH-10 Sevoke - Gangtok Lifeline",
        "lat": 27.2340,
        "lng": 88.5240,
        "elevation_m": 1680,
        "slope_deg": 48.5,
        "lithology": "Daling Phyllite (Highly Sheared)",
        "sensors": ["Biaxial Inclinometer", "Vibrating Wire Piezometer", "Tipping Bucket Rain Gauge", "Triaxial Geophone"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.05, "pwp": 18.0, "soil_moisture": 42.0, "vibration": 1.2}
    },
    {
        "id": "STN-SIK-02",
        "name": "Mangan - Chungthang Fault Node",
        "state": "Sikkim",
        "district": "Mangan (North Sikkim)",
        "corridor": "North Sikkim Highway",
        "lat": 27.5120,
        "lng": 88.5410,
        "elevation_m": 2150,
        "slope_deg": 52.0,
        "lithology": "Chungthang Gneiss & Mica Schist",
        "sensors": ["MEMS Tilt Meter", "Piezometer", "Rain Gauge", "Soil Moisture TDR"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.08, "pwp": 22.0, "soil_moisture": 48.0, "vibration": 1.5}
    },
    {
        "id": "STN-MEG-01",
        "name": "Sohra (Cherrapunji) Escarpment",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "corridor": "Sohra-Shella Rim",
        "lat": 25.2986,
        "lng": 91.7180,
        "elevation_m": 1430,
        "slope_deg": 61.0,
        "lithology": "Therria Sandstone overlying Limestone",
        "sensors": ["Acoustic Emission Sensor", "Piezometer", "Optical Rain Radar Gauge", "Crackmeter"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.02, "pwp": 15.0, "soil_moisture": 55.0, "vibration": 0.8}
    },
    {
        "id": "STN-MEG-02",
        "name": "Sonapur Tunnel Cliff Observatory",
        "state": "Meghalaya",
        "district": "East Jaintia Hills",
        "corridor": "NH-6 Shillong-Silchar",
        "lat": 25.1230,
        "lng": 92.3680,
        "elevation_m": 820,
        "slope_deg": 56.0,
        "lithology": "Kopili Shale & Sandstone",
        "sensors": ["Inclinometer", "Piezometer", "Rain Gauge", "Debris Flow Wire Detector"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.12, "pwp": 26.0, "soil_moisture": 52.0, "vibration": 2.1}
    },
    {
        "id": "STN-ASM-01",
        "name": "Haflong Hill Station - Jatinga Spur",
        "state": "Assam",
        "district": "Dima Hasao",
        "corridor": "NH-27 / NF Railway Hill Section",
        "lat": 25.1840,
        "lng": 93.0310,
        "elevation_m": 960,
        "slope_deg": 44.0,
        "lithology": "Disang Shale (Heavy Weathering)",
        "sensors": ["Deep Hole Inclinometer", "Multipoint Piezometer", "Ultrasonic Rain Gauge"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.10, "pwp": 24.0, "soil_moisture": 46.0, "vibration": 1.1}
    },
    {
        "id": "STN-ASM-02",
        "name": "Guwahati Narakasur Hill Sentinel",
        "state": "Assam",
        "district": "Kamrup Metro",
        "corridor": "Guwahati Urban Slope",
        "lat": 26.1550,
        "lng": 91.7820,
        "elevation_m": 240,
        "slope_deg": 38.0,
        "lithology": "Granite Gneiss with Red Clay Overburden",
        "sensors": ["Tilt Sensor", "Soil Moisture Probe", "Digital Rain Gauge"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.01, "pwp": 10.0, "soil_moisture": 35.0, "vibration": 0.5}
    },
    {
        "id": "STN-MAN-01",
        "name": "Tupul Railway Yard Sentinel",
        "state": "Manipur",
        "district": "Noney",
        "corridor": "NH-37 & Jiribam-Imphal Railway",
        "lat": 24.7083,
        "lng": 93.6500,
        "elevation_m": 780,
        "slope_deg": 49.0,
        "lithology": "Disang Formation splintery shales and mudstones",
        "sensors": ["MEMS Inclinometer Array", "Piezometer", "Micro-seismic Geophone", "Tipping Rain Gauge"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.15, "pwp": 28.0, "soil_moisture": 58.0, "vibration": 2.4}
    },
    {
        "id": "STN-NAG-01",
        "name": "Kohima - Phesama Sinking Zone",
        "state": "Nagaland",
        "district": "Kohima",
        "corridor": "NH-29 Dimapur-Kohima-Mao",
        "lat": 25.6320,
        "lng": 94.1180,
        "elevation_m": 1440,
        "slope_deg": 42.0,
        "lithology": "Crushed Sandstone-Shale Alternation",
        "sensors": ["GNSS Real-Time Displacement", "Inclinometer", "Piezometer", "Rain Gauge"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.09, "pwp": 20.0, "soil_moisture": 44.0, "vibration": 1.0}
    },
    {
        "id": "STN-MIZ-01",
        "name": "Aizawl Hunthar Sinking Slopes",
        "state": "Mizoram",
        "district": "Aizawl",
        "corridor": "NH-54 Aizawl Arterial Link",
        "lat": 23.7420,
        "lng": 92.7090,
        "elevation_m": 1130,
        "slope_deg": 46.0,
        "lithology": "Bhuban Sandstone with Interbedded Mudstone",
        "sensors": ["Fiber Optic Strain Sensor", "Piezometer", "Rain Gauge", "Soil Moisture TDR"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.07, "pwp": 19.0, "soil_moisture": 41.0, "vibration": 0.9}
    },
    {
        "id": "STN-ARU-01",
        "name": "Tawang - Sela Pass Avalanche & Slide Post",
        "state": "Arunachal Pradesh",
        "district": "Tawang",
        "corridor": "Trans-Arunachal Highway (NH-13)",
        "lat": 27.5020,
        "lng": 92.1030,
        "elevation_m": 3150,
        "slope_deg": 55.0,
        "lithology": "Se La Group High-Grade Gneiss",
        "sensors": ["Laser Distance Meter", "Inclinometer", "Cryo-Heated Rain/Snow Gauge", "Piezometer"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.06, "pwp": 16.0, "soil_moisture": 39.0, "vibration": 1.8}
    },
    {
        "id": "STN-ARU-02",
        "name": "Bhalukpong Himalayan Foothill Gate",
        "state": "Arunachal Pradesh",
        "district": "West Kameng",
        "corridor": "Bhalukpong - Bomdila Sector",
        "lat": 27.0250,
        "lng": 92.6380,
        "elevation_m": 380,
        "slope_deg": 51.0,
        "lithology": "Siwalik Fragile Soft Sandstone & Conglomerate",
        "sensors": ["Inclinometer", "Piezometer", "Rain Gauge", "Soil Moisture Probe"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.04, "pwp": 14.0, "soil_moisture": 37.0, "vibration": 0.7}
    },
    {
        "id": "STN-TRI-01",
        "name": "Jampui Hills Ridge Observatory",
        "state": "Tripura",
        "district": "North Tripura",
        "corridor": "Vanghmun - Kanchanpur Road",
        "lat": 23.9550,
        "lng": 92.2780,
        "elevation_m": 880,
        "slope_deg": 36.0,
        "lithology": "Tipam Sandstone and Silt Layer",
        "sensors": ["MEMS Tilt Meter", "Soil Moisture Probe", "Digital Rain Gauge"],
        "status": "ONLINE",
        "baseline": {"tilt_rate": 0.02, "pwp": 12.0, "soil_moisture": 33.0, "vibration": 0.4}
    }
]

# Historical Landslides Catalog in NER
HISTORICAL_LANDSLIDES = [
    {
        "id": "HIST-NER-01",
        "name": "Tupul Railway Yard Debris Avalanche",
        "state": "Manipur",
        "district": "Noney",
        "date": "2022-06-30",
        "lat": 24.7083,
        "lng": 93.6500,
        "casualties": 61,
        "volume_m3": 1500000,
        "trigger": "Continuous 7-Day Monsoon Rain (340mm) + Cut-Slope Saturation",
        "type": "Rotational Rock-Debris Avalanche",
        "infrastructure_damage": "Wiped out 107 Territorial Army camp, submerged Ijai river channel, damaged railway yard."
    },
    {
        "id": "HIST-NER-02",
        "name": "Sikkim Teesta GLOF & Cascade Slides",
        "state": "Sikkim",
        "district": "Mangan & Chungthang",
        "date": "2023-10-04",
        "lat": 27.5350,
        "lng": 88.6480,
        "casualties": 42,
        "volume_m3": 4200000,
        "trigger": "South Lhonak Glacial Lake Outburst + Cloudburst",
        "type": "Hyper-concentrated Debris Flow & Slope Undermining",
        "infrastructure_damage": "Destroyed Chungthang Dam (Teesta III), washed out NH-10 bridges at Singtam and Rangpo."
    },
    {
        "id": "HIST-NER-03",
        "name": "Dima Hasao Haflong Railway Collapse",
        "state": "Assam",
        "district": "Dima Hasao",
        "date": "2022-05-15",
        "lat": 25.1780,
        "lng": 93.0250,
        "casualties": 18,
        "volume_m3": 850000,
        "trigger": "Premonsoon Extreme Deluge (480mm in 48 hrs)",
        "type": "Complex Translational Earth Slide & Washout",
        "infrastructure_damage": "New Haflong Railway Station buried in debris, train overturned, railway lines hanging in mid-air."
    },
    {
        "id": "HIST-NER-04",
        "name": "Sohra (Cherrapunji) Cliff Collapse",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "date": "2024-06-18",
        "lat": 25.2910,
        "lng": 91.7220,
        "casualties": 8,
        "volume_m3": 320000,
        "trigger": "Rainfall Intensity 620mm in 24 hrs",
        "type": "Topple and Debris Slide",
        "infrastructure_damage": "Snapped road connection to Shella border trade post, severed power lines."
    },
    {
        "id": "HIST-NER-05",
        "name": "Kohima Phesama Sinking Disaster",
        "state": "Nagaland",
        "district": "Kohima",
        "date": "2015-08-19",
        "lat": 25.6320,
        "lng": 94.1180,
        "casualties": 0,
        "volume_m3": 600000,
        "trigger": "Deep seated shearing and prolonged torrential precipitation",
        "type": "Slow-moving Creep to Rapid Earth Flow",
        "infrastructure_damage": "Cut off NH-29 lifeline to Manipur for 23 days, displaced 50+ homesteads."
    },
    {
        "id": "HIST-NER-06",
        "name": "Aizawl Hunthar Sinking Slips",
        "state": "Mizoram",
        "district": "Aizawl",
        "date": "2017-06-09",
        "lat": 23.7420,
        "lng": 92.7090,
        "casualties": 12,
        "volume_m3": 210000,
        "trigger": "Cyclonic Mora Depression Rainfall (280mm)",
        "type": "Translational Sandstone-Shale Slide",
        "infrastructure_damage": "Collapsed 15 multi-storey RC structures, damaged national highway bypass."
    }
]

# Designated Evacuation and Emergency Relief Shelters (NER Operational Grid)
EVACUATION_SHELTERS = [
    {
        "id": "SHL-MAN-01",
        "name": "Noney District Headquarter Safe Relief Shelter",
        "state": "Manipur",
        "district": "Noney",
        "location": "Longmai Ward-3, Noney Hill Top, NH-37 Bypass",
        "lat": 24.7150,
        "lng": 93.6620,
        "capacity": 850,
        "available_capacity": 580,
        "availability_status": "AVAILABLE (580 Free Slots)",
        "contact_phone": "+91-385-244199",
        "contact_authority": "Manipur SDMA & Noney District Collectorate / SDRF Post",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Potable Water Tankers", "SDRF Triage Unit", "Community Hot Kitchen", "Clean Washroom Blocks", "50kVA Diesel Generator", "Helipad Landing Area"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-MAN-02",
        "name": "Tupul Sub-Divisional Emergency High Ground Shelter",
        "state": "Manipur",
        "district": "Noney",
        "location": "Upper Tupul Ridge Safe Crest, Off NF Railway Line",
        "lat": 24.7320,
        "lng": 93.6780,
        "capacity": 500,
        "available_capacity": 340,
        "availability_status": "AVAILABLE (340 Free Slots)",
        "contact_phone": "+91-385-244220",
        "contact_authority": "Noney Disaster Management Cell & 107th Territorial Army Camp",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": False,
        "amenities": ["Drinking Water Filters", "Emergency Medical Kit", "Pre-cooked Dry Rations", "Field Toilets", "Solar Power Array"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-MAN-03",
        "name": "Imphal Khuman Lampak Sports Complex Relief Hub",
        "state": "Manipur",
        "district": "Imphal East",
        "location": "Khuman Lampak Main Stadium, Imphal",
        "lat": 24.8180,
        "lng": 93.9480,
        "capacity": 3500,
        "available_capacity": 2800,
        "availability_status": "AVAILABLE (2,800 Free Slots)",
        "contact_phone": "+91-385-222401",
        "contact_authority": "Manipur State Disaster Response Force (SDRF) HQ",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["NDRF Tactical Base", "100-Bed Field Hospital", "Continuous Water Filtration", "Large Dining Hall", "Dedicated Sanitation Blocks"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-SIK-01",
        "name": "Gangtok Paljor Stadium Safe Relief Centre",
        "state": "Sikkim",
        "district": "Gangtok",
        "location": "Paljor Stadium Upper Deck, Gangtok",
        "lat": 27.3290,
        "lng": 88.6140,
        "capacity": 1500,
        "available_capacity": 980,
        "availability_status": "AVAILABLE (980 Free Slots)",
        "contact_phone": "+91-3592-202244",
        "contact_authority": "Sikkim State Disaster Management Authority (SSDMA) & Indian Army 17 Mountain Div",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Army Medical Bay", "Helipad Access", "Emergency Generators", "Satellite Phone Link", "Filtered Mountain Spring Water"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-SIK-02",
        "name": "Mangan Community Disaster Hall",
        "state": "Sikkim",
        "district": "Mangan (North Sikkim)",
        "location": "Mangan Bazaar High Ground, North Sikkim",
        "lat": 27.5080,
        "lng": 88.5320,
        "capacity": 650,
        "available_capacity": 410,
        "availability_status": "AVAILABLE (410 Free Slots)",
        "contact_phone": "+91-3592-234211",
        "contact_authority": "District Collectorate Mangan & ITBP Base Camp",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Emergency Dry Rations", "Triage First Aid", "UV Water Purification", "Radio Communication Node"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-MEG-01",
        "name": "Cherrapunji Multi-Purpose Cyclone & Disaster Shelter",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "location": "Sohra Plateau Safe Elevation, Cherrapunji",
        "lat": 25.3020,
        "lng": 91.7310,
        "capacity": 900,
        "available_capacity": 620,
        "availability_status": "AVAILABLE (620 Free Slots)",
        "contact_phone": "+91-364-250100",
        "contact_authority": "Meghalaya SDMA & BSF Sector HQ",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Reinforced High Ground Foundation", "Medical Emergency Team", "Community Pantry", "Separate Men/Women Sanitation Blocks"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-MEG-02",
        "name": "Shillong JN Stadium Indoor Disaster Complex",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "location": "Polo Grounds, Shillong",
        "lat": 25.5860,
        "lng": 91.8980,
        "capacity": 2200,
        "available_capacity": 1750,
        "availability_status": "AVAILABLE (1,750 Free Slots)",
        "contact_phone": "+91-364-222330",
        "contact_authority": "East Khasi Hills District Emergency Operation Centre",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Civil Defense Field Hospital", "Ambulance Fleet", "Centralized Food Distribution", "Generator Backup"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-ASM-01",
        "name": "Haflong Government College Safe Complex",
        "state": "Assam",
        "district": "Dima Hasao",
        "location": "Council Road, Haflong High Ridge",
        "lat": 25.1750,
        "lng": 93.0200,
        "capacity": 1200,
        "available_capacity": 850,
        "availability_status": "AVAILABLE (850 Free Slots)",
        "contact_phone": "+91-3673-236222",
        "contact_authority": "Dima Hasao Disaster Management Authority & NDRF 1st Bn",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Emergency Power Generator", "Potable Water Tankers", "NDRF Command Camp", "Medical Aid Clinic", "Sanitation Modules"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-NAG-01",
        "name": "Kohima Indira Gandhi Stadium Disaster Shelter",
        "state": "Nagaland",
        "district": "Kohima",
        "location": "Meriema High Plateau, Kohima",
        "lat": 25.6880,
        "lng": 94.1020,
        "capacity": 1800,
        "available_capacity": 1320,
        "availability_status": "AVAILABLE (1,320 Free Slots)",
        "contact_phone": "+91-370-227003",
        "contact_authority": "Nagaland State Disaster Management Authority (NSDMA)",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Medical Triage Station", "Command Center Wireless Link", "Solar + Diesel Generator", "Bulk Water Reservoirs"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-MIZ-01",
        "name": "Aizawl Rajiv Gandhi Indoor Stadium Shelter",
        "state": "Mizoram",
        "district": "Aizawl",
        "location": "Khatla Safe Ridge Zone, Aizawl",
        "lat": 23.7250,
        "lng": 92.7230,
        "capacity": 1600,
        "available_capacity": 1150,
        "availability_status": "AVAILABLE (1,150 Free Slots)",
        "contact_phone": "+91-389-233400",
        "contact_authority": "Mizoram Disaster Management & Rehabilitation Dept",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Emergency Bedding & Rations", "Geotechnical Structural Sentinel", "Standby Ambulances", "Pure Water Dispensers"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-ARU-01",
        "name": "Tawang Higher Secondary Disaster Safe Shelter",
        "state": "Arunachal Pradesh",
        "district": "Tawang",
        "location": "Old Market Upper Ridge, Tawang",
        "lat": 27.5900,
        "lng": 91.8600,
        "capacity": 900,
        "available_capacity": 620,
        "availability_status": "AVAILABLE (620 Free Slots)",
        "contact_phone": "+91-3794-222201",
        "contact_authority": "Arunachal Pradesh SDMA & Indian Army High Altitude Brigade",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": True,
        "amenities": ["Heated Indoor Halls", "Army Medical Aid", "Satellite Communications", "Freeze-Proof Potable Water"],
        "is_verified": True,
        "is_demo": True
    },
    {
        "id": "SHL-TRI-01",
        "name": "Vanghmun Community Cyclone & Slide Safe Shelter",
        "state": "Tripura",
        "district": "North Tripura",
        "location": "Jampui Ridge Top, Vanghmun",
        "lat": 23.9620,
        "lng": 92.2850,
        "capacity": 550,
        "available_capacity": 420,
        "availability_status": "AVAILABLE (420 Free Slots)",
        "contact_phone": "+91-3824-222110",
        "contact_authority": "North Tripura District Disaster Authority",
        "drinking_water": True,
        "first_aid": True,
        "food": True,
        "toilets": True,
        "emergency_power": True,
        "satellite_comms": False,
        "amenities": ["Clean Water Storage", "Solar Power System", "First Aid Triage", "Sanitation Facilities"],
        "is_verified": True,
        "is_demo": True
    }
]

# ==============================================================================
# FEATURE 1: Satellite Change Detection Records (Terrain & Land Cover Analysis)
# ==============================================================================
SATELLITE_CHANGE_RECORDS = [
    {
        "id": "SAT-CHG-MAN-01",
        "location_id": "STN-MAN-01",
        "name": "Tupul Railway Yard Mountain Scarp",
        "state": "Manipur",
        "district": "Noney",
        "latitude": 24.7083,
        "longitude": 93.6500,
        "before_date": "2026-05-15 (Dry Season Pre-Monsoon)",
        "after_date": "2026-08-20 (Post-Cloudburst Satellite Pass)",
        "change_pct": 18.4,
        "change_class": "Significant Crown Scarp Retrogression & Debris Fan Spread",
        "risk_indicator": "HIGH",
        "before_desc": "Intact vegetated forest canopy with stable highway cut benches.",
        "after_desc": "Bare shear scar exposed over 18.4% of slope surface. Tension fissure propagation observed.",
        "polygon_coordinates": [
            [24.7060, 93.6470],
            [24.7110, 93.6480],
            [24.7120, 93.6530],
            [24.7070, 93.6540]
        ],
        "is_demo": True
    },
    {
        "id": "SAT-CHG-SIK-01",
        "location_id": "STN-SIK-01",
        "name": "Mangan North Teesta Valley Flank",
        "state": "Sikkim",
        "district": "Mangan",
        "latitude": 27.5020,
        "longitude": 88.5280,
        "before_date": "2026-04-10",
        "after_date": "2026-08-18",
        "change_pct": 22.1,
        "change_class": "Upper Talus Toe Scour & Hydro-Erosion",
        "risk_indicator": "CRITICAL",
        "before_desc": "Dense sub-alpine vegetation and stabilized road embankments.",
        "after_desc": "Major debris cone accumulation on NH-10 approach. River bank undercut active.",
        "polygon_coordinates": [
            [27.4990, 88.5240],
            [27.5050, 88.5250],
            [27.5060, 88.5310],
            [27.5000, 88.5300]
        ],
        "is_demo": True
    },
    {
        "id": "SAT-CHG-MEG-01",
        "location_id": "STN-MEG-01",
        "name": "Sohra Plateau Rim Ravine",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "latitude": 25.2800,
        "longitude": 91.7250,
        "before_date": "2026-05-01",
        "after_date": "2026-08-22",
        "change_pct": 12.8,
        "change_class": "Karst Sinkhole Expansion & Waterfall Lip Creep",
        "risk_indicator": "MODERATE",
        "before_desc": "Grassland and sandstone caprock with standard canyon drainage.",
        "after_desc": "Subsurface piping collapse identified along rim road shoulder.",
        "polygon_coordinates": [
            [25.2770, 91.7220],
            [25.2830, 91.7230],
            [25.2840, 91.7280],
            [25.2780, 91.7270]
        ],
        "is_demo": True
    }
]

# ==============================================================================
# FEATURE 2: Infrastructure Assets & Risk Exposure Dataset
# ==============================================================================
NER_INFRASTRUCTURE = [
    {
        "id": "INF-MAN-01",
        "name": "NH-37 Mountain Highway Section (km 48 - 56)",
        "type": "National Highway",
        "category": "Highway",
        "state": "Manipur",
        "district": "Noney",
        "latitude": 24.7120,
        "longitude": 93.6520,
        "criticality": "HIGH",
        "status": "THREATENED / RESTRICTED ACCESS",
        "description": "Primary trade lifeline connecting Imphal to Silchar and national railhead."
    },
    {
        "id": "INF-MAN-02",
        "name": "Jiribam-Imphal Railway Bridge 164 & Super Pier 141m",
        "type": "Railway Infrastructure",
        "category": "Railway",
        "state": "Manipur",
        "district": "Noney",
        "latitude": 24.7160,
        "longitude": 93.6580,
        "criticality": "CRITICAL",
        "status": "ACTIVE VIBRATION MONITORING",
        "description": "World's tallest railway girder bridge pier (141m) in fragile Disang shale formation."
    },
    {
        "id": "INF-MAN-03",
        "name": "132kV Imphal-Leimatak High Voltage Power Transmission Line",
        "type": "Power Grid",
        "category": "Power",
        "state": "Manipur",
        "district": "Noney",
        "latitude": 24.7220,
        "longitude": 93.6650,
        "criticality": "MODERATE",
        "status": "OPERATIONAL / TOWER FOUNDATION MONITORED",
        "description": "Lattice transmission towers located 2.4 km uphill on stable ridge bedrock."
    },
    {
        "id": "INF-MAN-04",
        "name": "Noney River RCC Concrete Road Bridge",
        "type": "Road Bridge",
        "category": "Bridge",
        "state": "Manipur",
        "district": "Noney",
        "latitude": 24.7140,
        "longitude": 93.6610,
        "criticality": "HIGH",
        "status": "WATCH LIST (SCOUR THREAT)",
        "description": "Critical river crossing providing primary evacuation access to Noney DHQ shelter."
    },
    {
        "id": "INF-SIK-01",
        "name": "NH-10 Sevoke-Gangtok Highway Lifeline",
        "type": "National Highway",
        "category": "Highway",
        "state": "Sikkim",
        "district": "Mangan",
        "latitude": 27.5050,
        "longitude": 88.5260,
        "criticality": "CRITICAL",
        "status": "FREQUENT CLOSURES / ACTIVE CLEARANCE",
        "description": "Sole arterial supply corridor connecting Sikkim to mainland West Bengal."
    },
    {
        "id": "INF-SIK-02",
        "name": "Teesta Stage V Hydroelectric Dam Power Duct",
        "type": "Power Dam",
        "category": "Power",
        "state": "Sikkim",
        "district": "Gangtok",
        "latitude": 27.4200,
        "longitude": 88.5100,
        "criticality": "HIGH",
        "status": "PROTECTED WATERWAY",
        "description": "510 MW run-of-the-river hydroelectric power generation complex."
    },
    {
        "id": "INF-MEG-01",
        "name": "NH-6 Sonapur Tunnel Approach Road",
        "type": "Highway Tunnel",
        "category": "Highway",
        "state": "Meghalaya",
        "district": "East Jaintia Hills",
        "latitude": 25.1050,
        "longitude": 92.3800,
        "criticality": "CRITICAL",
        "status": "VULNERABLE TO MUD OVERFLOW",
        "description": "Key tunnel bypassing recurrent landslide zone connecting Meghalaya to Barak Valley."
    },
    {
        "id": "INF-ASM-01",
        "name": "New Haflong Railway Terminal Complex",
        "type": "Railway Terminal",
        "category": "Railway",
        "state": "Assam",
        "district": "Dima Hasao",
        "latitude": 25.1680,
        "longitude": 93.0180,
        "criticality": "HIGH",
        "status": "DRAINAGE REINFORCED",
        "description": "Major passenger and freight mountain rail interchange station."
    }
]

# ==============================================================================
# FEATURE 3: Known Sensor Anomalies Dataset
# ==============================================================================
KNOWN_SENSOR_ANOMALIES = [
    {
        "id": "ANOM-MAN-001",
        "station_id": "STN-MAN-01",
        "station_name": "Tupul Railway Yard Sentinel",
        "sensor_type": "Soil Volumetric Moisture TDR Probe",
        "previous_val": "72.4 %",
        "anomalous_val": "999.0 %",
        "unit": "%",
        "detection_reason": "Value exceeds physical moisture saturation limit (>100%). Out-of-bounds electrical spike.",
        "severity": "CRITICAL",
        "status": "ANOMALY DETECTED",
        "detected_at": "2026-08-28 20:45:12 UTC+05:30",
        "recommended_action": "Isolate probe data stream from ML model. Schedule on-site sensor recalibration."
    },
    {
        "id": "ANOM-MEG-002",
        "station_id": "STN-MEG-02",
        "station_name": "Mawsynram Crest Observatory",
        "sensor_type": "Vibrating Wire Piezometer",
        "previous_val": "18.2 kPa",
        "anomalous_val": "-45.0 kPa",
        "unit": "kPa",
        "detection_reason": "Negative hydrostatic pressure breach in saturated soil horizon.",
        "severity": "WARNING",
        "status": "MAINTENANCE SCHEDULED",
        "detected_at": "2026-08-28 19:30:00 UTC+05:30",
        "recommended_action": "Check grounding cable and lightning arrestor surge suppressor."
    }
]

# ==============================================================================
# Historical Landslides Archive
# ==============================================================================
HISTORICAL_LANDSLIDES = [
    {
        "id": "EV-MAN-2022",
        "name": "Tupul Railway Construction Site Disaster",
        "state": "Manipur",
        "district": "Noney",
        "event_date": "2022-06-30",
        "latitude": 24.7083,
        "longitude": 93.6500,
        "casualties": 61,
        "volume_m3": 1200000,
        "trigger_factor": "Excess Monsoonal Infiltration & Unconsolidated Disang Slope Cuttings",
        "landslide_type": "Rotational Debris Avalanche / Mudflow",
        "infrastructure_damage": "Damaged Ijei River bridge pier, railway construction yard, and blocked river valley."
    },
    {
        "id": "EV-MEG-2020",
        "name": "Sohra-Shella Escarpment Slope Failure",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "event_date": "2020-09-18",
        "latitude": 25.2800,
        "longitude": 91.7200,
        "casualties": 4,
        "volume_m3": 450000,
        "trigger_factor": "Extreme Monsoonal Cloudburst (>350 mm / 24h)",
        "landslide_type": "Planar Bedrock Glide",
        "infrastructure_damage": "Breached arterial border highway and severed telecommunication lines."
    },
    {
        "id": "EV-SIK-2023",
        "name": "Teesta River Basin Multi-Site Slide Series",
        "state": "Sikkim",
        "district": "Mangan",
        "event_date": "2023-10-04",
        "latitude": 27.5100,
        "longitude": 88.5400,
        "casualties": 42,
        "volume_m3": 2800000,
        "trigger_factor": "GLOF Surge & Hydro-Mechanical Toe Erosion",
        "landslide_type": "Complex Debris Flow & Toe Scour",
        "infrastructure_damage": "Destroyed Chungthang dam spillways, washed away NH-10 road segments."
    },
    {
        "id": "EV-ASM-2022",
        "name": "New Haflong Railway Submergence & Mudslide",
        "state": "Assam",
        "district": "Dima Hasao",
        "event_date": "2022-05-15",
        "latitude": 25.1840,
        "longitude": 93.0310,
        "casualties": 8,
        "volume_m3": 650000,
        "trigger_factor": "Continuous Torrential Rainfall Infiltration",
        "landslide_type": "Debris Mudflow & Track Submergence",
        "infrastructure_damage": "Severed Lumding-Badarpur hill railway lifeline for over 60 days."
    },
    {
        "id": "EV-NAG-2021",
        "name": "Pagla Pahar Rockfall & Mudslide",
        "state": "Nagaland",
        "district": "Chümoukedima",
        "event_date": "2021-07-22",
        "latitude": 25.7900,
        "longitude": 93.7500,
        "casualties": 2,
        "volume_m3": 180000,
        "trigger_factor": "Pore Pressure Saturation along Joint Planes",
        "landslide_type": "Rockfall / Topple",
        "infrastructure_damage": "Crushed vehicles on NH-29 and closed Dimapur-Kohima arterial corridor."
    },
    {
        "id": "EV-MIZ-2024",
        "name": "Melthum Quarry Collapse & Debris Slide",
        "state": "Mizoram",
        "district": "Aizawl",
        "event_date": "2024-05-28",
        "latitude": 23.7000,
        "longitude": 92.7000,
        "casualties": 17,
        "volume_m3": 320000,
        "trigger_factor": "Cyclone Remal Torrential Precipitation",
        "landslide_type": "Slope Failure & Quarry Surcharge Slide",
        "infrastructure_damage": "Destroyed 12 residential structures and severed municipal access roads."
    }
]


