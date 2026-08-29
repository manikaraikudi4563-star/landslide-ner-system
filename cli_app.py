"""
Interactive Terminal CLI Command Center for NER Landslide Early Warning & Risk Monitoring System.
100% self-contained terminal interface (Zero browser, zero links, pure console execution).
"""

import os
import sys
import time

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.models.ml_engine import ml_engine
from app.models.geotech_engine import geotech_engine
from app.services.telemetry_service import telemetry_service
from app.services.alert_service import alert_service
from app.services.routing_service import routing_service
from app.data.ner_geospatial import NER_STATES, NER_CORRIDORS, IOT_STATIONS, HISTORICAL_LANDSLIDES, EVACUATION_SHELTERS
from app.database import init_db, add_citizen_report, get_all_reports

init_db()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("=" * 80)
    print("  🏔️  NER-LEWS: AI LANDSLIDE EARLY WARNING & RISK MONITORING SYSTEM  🏔️")
    print("  North Eastern Region of India • Standalone Terminal Command Center")
    print("=" * 80)

def show_telemetry_table():
    stations = telemetry_service.update_telemetry_tick(1.0)
    print("\n--- LIVE GEOTECHNICAL TELEMETRY STATIONS (NER) ---")
    header_fmt = "{:<12} {:<28} {:<12} {:<8} {:<10} {:<10} {:<12} {:<10}"
    row_fmt = "{:<12} {:<28} {:<12} {:<8.2f} {:<10.1f} {:<10.3f} {:<12.1f} {:<10}"
    
    print(header_fmt.format("STATION ID", "NAME", "STATE", "Fs", "PWP (kPa)", "TILT (mm/h)", "RAIN 24h", "STATUS"))
    print("-" * 105)

    for s in stations:
        r = s["current_readings"]
        name_short = s["name"][:26]
        print(row_fmt.format(
            s["id"], name_short, s["state"],
            r["factor_of_safety"], r["pore_water_pressure"],
            r["tilt_rate"], r["rainfall_24h"], r["warning_level"]
        ))
    print("-" * 105)

def run_cli_simulation():
    print("\n--- AI WHAT-IF SCENARIO SIMULATION SANDBOX ---")
    try:
        slope = float(input("Enter Slope Angle in degrees [15 - 75, default 48]: ") or "48")
        rain = float(input("Enter Rainfall Intensity in mm/hr [0 - 120, default 35]: ") or "35")
        dur = float(input("Enter Storm Duration in hours [1 - 48, default 6]: ") or "6")
        pwp = float(input("Enter Pore Water Pressure in kPa [5 - 65, default 32]: ") or "32")
        moist = float(input("Enter Soil Moisture in % [20 - 98, default 80]: ") or "80")
        seismic = float(input("Enter Seismic Coeff kh (0.0 to 0.3g, default 0.05): ") or "0.05")
    except ValueError:
        print("Invalid input, using defaults.")
        slope, rain, dur, pwp, moist, seismic = 48.0, 35.0, 6.0, 32.0, 80.0, 0.05

    id_res = geotech_engine.calculate_id_threshold("Meghalaya", rain, dur)
    fs_res = geotech_engine.calculate_factor_of_safety(slope, pwp, seismic_coeff_kh=seismic)
    ml_res = ml_engine.predict_susceptibility({
        "slope_deg": slope,
        "soil_moisture_pct": moist,
        "rainfall_7d_mm": rain * 5.0,
        "fault_dist_km": 1.5,
        "lithology_code": 3,
        "lulc_code": 3
    })

    comp_score = round(ml_res["risk_score"] * 0.5 + id_res["threshold_percentage"] * 0.3 + max(0, 1.8 - fs_res["factor_of_safety"]) * 50 * 0.2, 1)
    comp_score = min(100.0, max(0.0, comp_score))

    print("\n" + "=" * 65)
    print(f"  AI COMPOSITE RISK SCORE : {comp_score} / 100")
    print(f"  FACTOR OF SAFETY (Fs)   : {fs_res['factor_of_safety']} [{fs_res['stability_status']}]")
    print(f"  RAINFALL I-D THRESHOLD  : {id_res['threshold_percentage']}% Capacity [{id_res['stage']}]")
    print(f"  AI SUSCEPTIBILITY TIER  : {ml_res['tier']}")
    print("=" * 65)
    print(f"TACTICAL DIRECTIVE:\n  {ml_res['recommended_action']}")
    print(f"\nGEOTECHNICAL MARGIN:\n  {fs_res['safety_margin']}")
    print("\nEXPLAINABLE AI FACTOR BREAKDOWN:")
    for f in ml_res["factor_breakdown"]:
        print(f"  • {f['factor']:<30}: {f['weight']:>5.1f}% weight ({f['impact']} Impact)")
    print("=" * 65)

def show_cap_alerts():
    print("\n--- ACTIVE COMMON ALERTING PROTOCOL (CAP v1.2) WARNINGS ---")
    alerts = alert_service.get_all_active_alerts()
    for a in alerts:
        print("\n" + "─" * 70)
        print(f"🚨 [{a['severity'].upper()}] {a['event_type']}")
        print(f"HEADLINE: {a['headline']}")
        print(f"AREA    : {a['region_name']}, {a['state']}")
        print(f"DETAILS : {a['description']}")
        print(f"ACTION  : {a['instruction']}")
    print("─" * 70)

def show_evacuation_routes():
    print("\n--- SAFE EVACUATION NAVIGATOR ---")
    print("Select an Origin Monitoring Station:")
    for i, s in enumerate(IOT_STATIONS):
        print(f"  [{i + 1}] {s['name']} ({s['state']})")
    
    try:
        choice = int(input("\nEnter station number: ") or "1") - 1
        stn = IOT_STATIONS[max(0, min(len(IOT_STATIONS) - 1, choice))]
    except ValueError:
        stn = IOT_STATIONS[0]

    routes = routing_service.find_nearest_shelters(stn["lat"], stn["lng"], limit=3)
    print(f"\nNearest Safe Evacuation Shelters for {stn['name']}:")
    print("-" * 80)
    for i, r in enumerate(routes):
        shl = r["shelter"]
        is_primary = "★ PRIMARY SAFE ZONE" if i == 0 else ""
        print(f"{i + 1}. 🛡️  {shl['name']} {is_primary}")
        print(f"   Road Distance : {r['estimated_road_km']} km (Mountain Tortuosity Adjusted)")
        print(f"   Drive Time    : ~{r['drive_time_mins']} minutes | Walk Time: ~{r['walk_time_mins']} minutes")
        print(f"   Capacity      : {shl['capacity']} persons | Helpline: {shl['contact_phone']}")
        print(f"   Amenities     : {', '.join(shl['amenities'])}")
        print("-" * 80)

def submit_field_report():
    print("\n--- SUBMIT CITIZEN / FIELD OFFICER LANDSLIDE REPORT ---")
    name = input("Reporter Name: ") or "Field Officer"
    loc = input("Location / Road Segment: ") or "NH-10 Milestone 29"
    state = input("State (Sikkim, Meghalaya, Assam, Manipur, etc.): ") or "Sikkim"
    desc = input("Incident Description: ") or "Slope failure with rock boulders blocking carriageway."

    rep_id = add_citizen_report({
        "reporter_name": name,
        "state": state,
        "location_name": loc,
        "latitude": 25.5,
        "longitude": 92.5,
        "landslide_type": "Debris Slide",
        "estimated_size": "Medium",
        "road_blocked": True,
        "description": desc
    })
    print(f"\n✅ Report Logged successfully! Reference ID: {rep_id}")

def main():
    while True:
        print_header()
        print("\nMain Menu:")
        print("  [1] 📡 View Live Geotechnical Telemetry Table")
        print("  [2] 🧪 Run AI What-If Scenario Stress Simulation")
        print("  [3] 🚨 View Active CAP v1.2 Disaster Warnings")
        print("  [4] 🏃 Calculate Safe Evacuation Routes to Shelters")
        print("  [5] 📢 Submit Ground Landslide Field Report")
        print("  [6] 📜 View Historical NER Landslide Catalog")
        print("  [7] 🏔️  View 8-State NER Geotechnical Vulnerability Matrix")
        print("  [0] 🚪 Exit")
        
        choice = input("\nEnter choice [0-7]: ").strip()
        if choice == "1":
            show_telemetry_table()
        elif choice == "2":
            run_cli_simulation()
        elif choice == "3":
            show_cap_alerts()
        elif choice == "4":
            show_evacuation_routes()
        elif choice == "5":
            submit_field_report()
        elif choice == "6":
            print("\n--- HISTORICAL NER LANDSLIDE CATALOG ---")
            for h in HISTORICAL_LANDSLIDES:
                print(f"\n📌 {h['name']} ({h['date']}) - {h['state']}")
                print(f"   Fatalities: {h['casualties']} | Volume: {h['volume_m3']:,} m³ | Trigger: {h['trigger']}")
                print(f"   Impact: {h['infrastructure_damage']}")
        elif choice == "7":
            print("\n--- 8-STATE NER GEOTECHNICAL VULNERABILITY MATRIX ---")
            for name, info in NER_STATES.items():
                print(f"\n🏔️  {name.upper()} (Risk: {info['vulnerability_score']}/100 [{info['vulnerability_level']}])")
                print(f"   Geology     : {info['geology']}")
                print(f"   Seismic Zone: {info['seismic_zone']} | Annual Rain: {info['annual_rainfall_mm']} mm")
                print(f"   Districts   : {', '.join(info['districts_at_risk'])}")
        elif choice == "0":
            print("\nExiting NER Landslide Early Warning Console. Stay safe.")
            break
        else:
            print("Invalid selection.")

        input("\nPress Enter to return to main menu...")
        clear_screen()

if __name__ == "__main__":
    main()
