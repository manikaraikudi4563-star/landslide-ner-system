"""
Native Desktop GUI Application for NER Landslide Early Warning & Risk Monitoring System.
Runs standalone on Windows with Tkinter + Matplotlib (Zero web browser or external links required).
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Ensure root in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.models.ml_engine import ml_engine
from app.models.geotech_engine import geotech_engine
from app.services.telemetry_service import telemetry_service
from app.services.alert_service import alert_service
from app.services.routing_service import routing_service
from app.data.ner_geospatial import NER_STATES, NER_CORRIDORS, IOT_STATIONS, HISTORICAL_LANDSLIDES, EVACUATION_SHELTERS
from app.database import init_db, add_citizen_report, get_all_reports, get_active_alerts

# Initialize Database
init_db()

# Color Palette (Dark Mode)
BG_DARK = "#0f172a"
BG_PANEL = "#1e293b"
BG_CARD = "#334155"
TEXT_LIGHT = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_CYAN = "#06b6d4"
STATUS_GREEN = "#10b981"
STATUS_YELLOW = "#f59e0b"
STATUS_ORANGE = "#f97316"
STATUS_RED = "#ef4444"

class LandslideDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NER-LEWS | AI Landslide Early Warning & Risk Monitoring System")
        self.geometry("1280x820")
        self.configure(bg=BG_DARK)
        self.minsize(1100, 720)

        # Style Configuration
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._configure_styles()

        # State
        self.selected_station = IOT_STATIONS[0]
        self.live_telemetry = telemetry_service.get_all_stations()

        # Build UI
        self._build_header()
        self._build_tabs()

        # Start periodic update timer (every 10s)
        self.after(10000, self._periodic_telemetry_tick)

    def _configure_styles(self):
        self.style.configure(".", background=BG_DARK, foreground=TEXT_LIGHT, font=("Segoe UI", 10))
        self.style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=BG_PANEL, foreground=TEXT_MUTED, padding=[16, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab",
                       background=[("selected", ACCENT_CYAN), ("active", BG_CARD)],
                       foreground=[("selected", "#000000"), ("active", TEXT_LIGHT)])
        self.style.configure("TFrame", background=BG_DARK)
        self.style.configure("Card.TFrame", background=BG_PANEL, relief="flat")
        self.style.configure("TLabel", background=BG_PANEL, foreground=TEXT_LIGHT)
        self.style.configure("Title.TLabel", font=("Segoe UI", 12, "bold"), foreground=ACCENT_CYAN)
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#ffffff", background=BG_DARK)
        self.style.configure("TButton", background=ACCENT_CYAN, foreground="#000000", font=("Segoe UI", 9, "bold"), padding=[10, 5])
        self.style.map("TButton", background=[("active", "#22d3ee"), ("pressed", "#0891b2")])
        self.style.configure("Danger.TButton", background=STATUS_RED, foreground="#ffffff", font=("Segoe UI", 9, "bold"))
        self.style.map("Danger.TButton", background=[("active", "#f87171"), ("pressed", "#b91c1c")])

    def _build_header(self):
        header_frame = tk.Frame(self, bg="#0b0f19", height=65, padx=20, pady=10)
        header_frame.pack(fill="x", side="top")

        title_lbl = tk.Label(header_frame, text="🏔️ NER-LEWS: AI Landslide Early Warning & Risk Monitoring System",
                             font=("Segoe UI", 15, "bold"), fg="#ffffff", bg="#0b0f19")
        title_lbl.pack(side="left")

        sub_lbl = tk.Label(header_frame, text="  [North Eastern Region • 8 States Standalone Desktop Edition]",
                           font=("Segoe UI", 10), fg=ACCENT_CYAN, bg="#0b0f19")
        sub_lbl.pack(side="left", padx=5)

        btn_sync = tk.Button(header_frame, text="🔄 Sync Telemetry", bg=ACCENT_CYAN, fg="#000000",
                             font=("Segoe UI", 9, "bold"), command=self._manual_sync_telemetry, relief="flat", padx=10)
        btn_sync.pack(side="right", padx=5)

        status_badge = tk.Label(header_frame, text="● SYSTEM LIVE", font=("Segoe UI", 9, "bold"),
                                fg=STATUS_GREEN, bg="#0b0f19", padx=10)
        status_badge.pack(side="right")

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=8)

        # Tab 1: GIS Map & Telemetry Dashboard
        self.tab_gis = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_gis, text="🗺️ Geospatial Map & Sensor Telemetry")
        self._build_gis_tab()

        # Tab 2: AI What-If Simulation Sandbox
        self.tab_sim = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sim, text="🧪 AI What-If Simulation Sandbox")
        self._build_simulation_tab()

        # Tab 3: Regional 8-State Profiles
        self.tab_states = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_states, text="🏔️ NER 8-State Geotechnical Matrix")
        self._build_states_tab()

        # Tab 4: CAP Alerts & Bulletins
        self.tab_alerts = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_alerts, text="🚨 Active CAP Early Warnings")
        self._build_alerts_tab()

        # Tab 5: Evacuation Routing & Shelters
        self.tab_evac = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_evac, text="🏃 Safe Evacuation Navigator")
        self._build_evacuation_tab()

        # Tab 6: Incident Reporting & Catalog
        self.tab_rep = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rep, text="📢 Citizen Reporting & Disaster Catalog")
        self._build_reporting_tab()

    # -------------------------------------------------------------
    # TAB 1: GIS Map & Telemetry Dashboard
    # -------------------------------------------------------------
    def _build_gis_tab(self):
        paned = tk.PanedWindow(self.tab_gis, orient="horizontal", bg=BG_DARK, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        # Left: Matplotlib GIS Map
        map_frame = tk.Frame(paned, bg=BG_PANEL, padx=8, pady=8)
        paned.add(map_frame, width=700)

        map_title = tk.Label(map_frame, text="Geospatial Landslide Hazard Map - North Eastern Region (NER)",
                             font=("Segoe UI", 11, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL)
        map_title.pack(anchor="w", pady=(0, 6))

        # Matplotlib Figure for Map
        self.map_fig, self.map_ax = plt.subplots(figsize=(7, 6), facecolor=BG_PANEL)
        self.map_fig.tight_layout(pad=2)
        self._draw_gis_map()

        self.map_canvas = FigureCanvasTkAgg(self.map_fig, master=map_frame)
        self.map_canvas.draw()
        self.map_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Right: Station Telemetry Inspector & Chart
        right_frame = tk.Frame(paned, bg=BG_PANEL, padx=12, pady=10)
        paned.add(right_frame, width=540)

        stn_hdr = tk.Label(right_frame, text="📡 Real-Time Geotechnical Telemetry Inspector",
                           font=("Segoe UI", 12, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL)
        stn_hdr.pack(anchor="w", pady=(0, 6))

        # Station Selector Dropdown
        stn_select_frame = tk.Frame(right_frame, bg=BG_PANEL)
        stn_select_frame.pack(fill="x", pady=4)

        tk.Label(stn_select_frame, text="Select Station:", bg=BG_PANEL, fg=TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.stn_combobox = ttk.Combobox(stn_select_frame, values=[f"{s['name']} ({s['state']})" for s in IOT_STATIONS], state="readonly", width=42)
        self.stn_combobox.current(0)
        self.stn_combobox.pack(side="left", padx=8)
        self.stn_combobox.bind("<<ComboboxSelected>>", self._on_station_selected)

        # KPI Metric Cards
        self.kpi_frame = tk.Frame(right_frame, bg=BG_PANEL)
        self.kpi_frame.pack(fill="x", pady=8)

        self.lbl_fs = self._create_metric_box(self.kpi_frame, "Factor of Safety (Fs)", "1.15", STATUS_ORANGE, 0, 0)
        self.lbl_pwp = self._create_metric_box(self.kpi_frame, "Pore Pressure (kPa)", "24.5 kPa", ACCENT_CYAN, 0, 1)
        self.lbl_tilt = self._create_metric_box(self.kpi_frame, "Inclinometer Tilt Rate", "0.12 mm/h", STATUS_RED, 1, 0)
        self.lbl_rain = self._create_metric_box(self.kpi_frame, "24h Rain Accumulation", "48.2 mm", STATUS_YELLOW, 1, 1)

        # Telemetry History Line Chart
        chart_hdr = tk.Label(right_frame, text="24-Hour Tilt Rate & Pore Water Pressure Dynamics",
                             font=("Segoe UI", 10, "bold"), fg=TEXT_LIGHT, bg=BG_PANEL)
        chart_hdr.pack(anchor="w", pady=(8, 2))

        self.chart_fig, self.chart_ax1 = plt.subplots(figsize=(5, 3.2), facecolor=BG_PANEL)
        self.chart_fig.tight_layout(pad=2)
        self.chart_canvas = FigureCanvasTkAgg(self.chart_fig, master=right_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, pady=4)

        # Action Buttons
        btn_row = tk.Frame(right_frame, bg=BG_PANEL)
        btn_row.pack(fill="x", pady=6)

        btn_spike = tk.Button(btn_row, text="⚡ Simulate Storm Surge", bg=STATUS_RED, fg="#ffffff",
                              font=("Segoe UI", 9, "bold"), command=self._simulate_storm_spike, relief="flat", padx=12, pady=4)
        btn_spike.pack(side="left", padx=4)

        btn_route = tk.Button(btn_row, text="🏃 Plan Evacuation", bg=ACCENT_CYAN, fg="#000000",
                              font=("Segoe UI", 9, "bold"), command=self._plan_evac_for_current_station, relief="flat", padx=12, pady=4)
        btn_route.pack(side="left", padx=4)

        self._update_station_telemetry_ui()

    def _create_metric_box(self, parent, title, val, color, row, col):
        box = tk.Frame(parent, bg=BG_CARD, padx=8, pady=6, relief="groove", bd=1)
        box.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(box, text=title, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")
        val_lbl = tk.Label(box, text=val, font=("Segoe UI", 14, "bold"), fg=color, bg=BG_CARD)
        val_lbl.pack(anchor="w")
        return val_lbl

    def _draw_gis_map(self):
        self.map_ax.clear()
        self.map_ax.set_facecolor("#0b1329")

        # Plot state center points and background terrain bounds
        lats = [s["lat"] for s in NER_STATES.values()]
        lngs = [s["lng"] for s in NER_STATES.values()]

        # Draw State Regions
        for name, info in NER_STATES.items():
            self.map_ax.plot(info["lng"], info["lat"], "o", color="#38bdf8", markersize=6, alpha=0.7)
            self.map_ax.text(info["lng"] + 0.12, info["lat"], name, color="#cbd5e1", fontsize=8, weight="bold")

        # Draw Critical Corridors
        for corr in NER_CORRIDORS:
            c_lats = [p[0] for p in corr["path_coordinates"]]
            c_lngs = [p[1] for p in corr["path_coordinates"]]
            is_crit = corr["vulnerability"] in ["CRITICAL", "EXTREME"]
            color = "#f43f5e" if is_crit else "#0ea5e9"
            ls = "--" if is_crit else "-"
            self.map_ax.plot(c_lngs, c_lats, ls, color=color, linewidth=2.5, alpha=0.85, label=corr["name"].split()[0])

        # Draw IoT Monitoring Stations with Risk Status
        for stn in self.live_telemetry:
            r = stn["current_readings"]
            lvl = r["warning_level"]
            color = STATUS_RED if lvl == "RED" else (STATUS_ORANGE if lvl == "ORANGE" else (STATUS_YELLOW if lvl == "YELLOW" else STATUS_GREEN))
            size = 140 if lvl == "RED" else (100 if lvl == "ORANGE" else 70)
            self.map_ax.scatter(stn["lng"], stn["lat"], s=size, color=color, edgecolors="#ffffff", linewidths=1.5, zorder=5)

        # Draw Shelters
        for shl in EVACUATION_SHELTERS:
            self.map_ax.scatter(shl["lng"], shl["lat"], s=45, color="#10b981", marker="s", edgecolors="#ffffff", zorder=4)

        self.map_ax.set_title("North Eastern Region Landslide Observatories & Corridors", color=TEXT_LIGHT, fontsize=10, weight="bold")
        self.map_ax.set_xlabel("Longitude (°E)", color=TEXT_MUTED, fontsize=8)
        self.map_ax.set_ylabel("Latitude (°N)", color=TEXT_MUTED, fontsize=8)
        self.map_ax.tick_params(colors=TEXT_MUTED, labelsize=8)
        self.map_ax.grid(True, color="#1e293b", linestyle=":", alpha=0.6)
        self.map_fig.tight_layout(pad=1.5)

    def _draw_chart(self, timeseries):
        self.chart_fig.clear()
        ax1 = self.chart_fig.add_subplot(111)
        ax1.set_facecolor("#0b1329")

        if not timeseries:
            self.chart_canvas.draw()
            return

        x_labels = [t["timestamp"] for t in timeseries][-16:]
        pwp = [t["pore_water_pressure"] for t in timeseries][-16:]
        tilt = [t["tilt_rate"] for t in timeseries][-16:]

        x_indices = np.arange(len(x_labels))

        line1 = ax1.plot(x_indices, pwp, color=ACCENT_CYAN, marker="o", markersize=3, linewidth=2, label="Pore Pressure (kPa)")
        ax1.set_ylabel("kPa", color=ACCENT_CYAN, fontsize=8)
        ax1.tick_params(axis="y", labelcolor=ACCENT_CYAN, labelsize=7)
        ax1.tick_params(axis="x", colors=TEXT_MUTED, labelsize=7, rotation=35)
        ax1.set_xticks(x_indices[::2])
        ax1.set_xticklabels(x_labels[::2])

        ax2 = ax1.twinx()
        line2 = ax2.plot(x_indices, tilt, color=STATUS_RED, linestyle="--", marker="s", markersize=3, linewidth=2, label="Tilt (mm/h)")
        ax2.set_ylabel("mm/h", color=STATUS_RED, fontsize=8)
        ax2.tick_params(axis="y", labelcolor=STATUS_RED, labelsize=7)

        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc="upper left", fontsize=7, facecolor=BG_PANEL, edgecolor="#334155", labelcolor=TEXT_LIGHT)
        ax1.grid(True, color="#1e293b", linestyle=":", alpha=0.5)

        self.chart_fig.tight_layout(pad=1.5)
        self.chart_canvas.draw()

    def _on_station_selected(self, event):
        idx = self.stn_combobox.current()
        if idx >= 0:
            self.selected_station = IOT_STATIONS[idx]
            self._update_station_telemetry_ui()

    def _update_station_telemetry_ui(self):
        stn_id = self.selected_station["id"]
        detail = telemetry_service.get_station_details(stn_id)
        if not detail:
            return

        r = detail["current_readings"]
        self.lbl_fs.config(text=f"{r['factor_of_safety']}", fg=STATUS_RED if r["factor_of_safety"] < 1.0 else (STATUS_ORANGE if r["factor_of_safety"] < 1.25 else STATUS_GREEN))
        self.lbl_pwp.config(text=f"{r['pore_water_pressure']} kPa")
        self.lbl_tilt.config(text=f"{r['tilt_rate']} mm/h")
        self.lbl_rain.config(text=f"{r['rainfall_24h']} mm")

        self._draw_chart(detail.get("timeseries_history", []))

    def _simulate_storm_spike(self):
        stn_id = self.selected_station["id"]
        telemetry_service.inject_disaster_scenario(stn_id, "EXTREME_DELUGE")
        self._manual_sync_telemetry()
        messagebox.showwarning("⚠️ Storm Surge Injected", f"Simulated cloudburst deluge at {self.selected_station['name']}.\nSensor thresholds breached and CAP Critical Red Alert triggered!")

    def _plan_evac_for_current_station(self):
        self.notebook.select(self.tab_evac)
        self.evac_combobox.set(f"{self.selected_station['name']} ({self.selected_station['state']})")
        self._run_evacuation_calc()

    def _manual_sync_telemetry(self):
        self.live_telemetry = telemetry_service.update_telemetry_tick(1.1)
        self._draw_gis_map()
        self.map_canvas.draw()
        self._update_station_telemetry_ui()

    def _periodic_telemetry_tick(self):
        try:
            self._manual_sync_telemetry()
        except Exception:
            pass
        self.after(10000, self._periodic_telemetry_tick)

    # -------------------------------------------------------------
    # TAB 2: AI What-If Simulation Sandbox
    # -------------------------------------------------------------
    def _build_simulation_tab(self):
        container = tk.Frame(self.tab_sim, bg=BG_DARK, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        left_frame = tk.Frame(container, bg=BG_PANEL, padx=16, pady=16, relief="ridge", bd=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_frame, text="🧪 AI Stress Simulation Parameters", font=("Segoe UI", 12, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w", pady=(0, 10))

        # Sliders
        self.sim_rain_scale = self._create_slider(left_frame, "Rainfall Intensity (mm/hr):", 0, 120, 35)
        self.sim_dur_scale = self._create_slider(left_frame, "Continuous Duration (Hours):", 1, 48, 6)
        self.sim_slope_scale = self._create_slider(left_frame, "Slope Angle (β°):", 15, 75, 48)
        self.sim_pwp_scale = self._create_slider(left_frame, "Pore Water Pressure (kPa):", 5, 65, 32)
        self.sim_moist_scale = self._create_slider(left_frame, "Soil Moisture Saturation (%):", 20, 98, 80)
        self.sim_seismic_scale = self._create_slider(left_frame, "Seismic Acceleration (kh · g):", 0.0, 0.3, 0.05, is_float=True)

        # Run Button
        btn_calc = tk.Button(left_frame, text="⚡ Run Real-Time AI Inference", bg=ACCENT_CYAN, fg="#000000",
                             font=("Segoe UI", 10, "bold"), command=self._run_simulation, relief="flat", pady=6)
        btn_calc.pack(fill="x", pady=12)

        # Right: Output Results
        right_frame = tk.Frame(container, bg=BG_PANEL, padx=16, pady=16, relief="ridge", bd=1)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right_frame, text="📊 Multi-Model Early Warning Assessment", font=("Segoe UI", 12, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w", pady=(0, 10))

        self.sim_score_lbl = tk.Label(right_frame, text="Risk Index: 88.4 / 100", font=("Segoe UI", 18, "bold"), fg=STATUS_RED, bg=BG_PANEL)
        self.sim_score_lbl.pack(anchor="w", pady=4)

        self.sim_tier_lbl = tk.Label(right_frame, text="🔴 CRITICAL IMMINENT COLLAPSE", font=("Segoe UI", 12, "bold"), fg=STATUS_RED, bg=BG_PANEL)
        self.sim_tier_lbl.pack(anchor="w", pady=2)

        self.sim_fs_lbl = tk.Label(right_frame, text="Factor of Safety (Fs): 0.91 [Active Failure]", font=("Segoe UI", 10, "bold"), fg="#ffffff", bg=BG_PANEL)
        self.sim_fs_lbl.pack(anchor="w", pady=4)

        self.sim_id_lbl = tk.Label(right_frame, text="Rainfall I-D Threshold: 142% Breached", font=("Segoe UI", 10, "bold"), fg=STATUS_ORANGE, bg=BG_PANEL)
        self.sim_id_lbl.pack(anchor="w", pady=2)

        self.sim_advisory = scrolledtext.ScrolledText(right_frame, wrap="word", height=8, bg=BG_CARD, fg="#ffffff", font=("Segoe UI", 9))
        self.sim_advisory.pack(fill="both", expand=True, pady=10)

        self._run_simulation()

    def _create_slider(self, parent, label_text, min_val, max_val, init_val, is_float=False):
        row = tk.Frame(parent, bg=BG_PANEL)
        row.pack(fill="x", pady=4)

        lbl = tk.Label(row, text=f"{label_text} {init_val}", font=("Segoe UI", 9, "bold"), fg=TEXT_LIGHT, bg=BG_PANEL)
        lbl.pack(anchor="w")

        scale = ttk.Scale(row, from_=min_val, to=max_val, orient="horizontal")
        scale.set(init_val)
        scale.pack(fill="x", pady=2)

        def on_change(val):
            v = float(val) if is_float else int(float(val))
            lbl.config(text=f"{label_text} {v:.2f}" if is_float else f"{label_text} {v}")

        scale.configure(command=on_change)
        return scale

    def _run_simulation(self):
        slope = float(self.sim_slope_scale.get())
        rain = float(self.sim_rain_scale.get())
        duration = float(self.sim_dur_scale.get())
        pwp = float(self.sim_pwp_scale.get())
        moisture = float(self.sim_moist_scale.get())
        seismic = float(self.sim_seismic_scale.get())

        id_res = geotech_engine.calculate_id_threshold("Meghalaya", rain, duration)
        fs_res = geotech_engine.calculate_factor_of_safety(slope, pwp, seismic_coeff_kh=seismic)
        ml_res = ml_engine.predict_susceptibility({
            "slope_deg": slope,
            "soil_moisture_pct": moisture,
            "rainfall_7d_mm": rain * 5.0,
            "fault_dist_km": 1.5,
            "lithology_code": 3,
            "lulc_code": 3
        })

        comp_score = round(ml_res["risk_score"] * 0.5 + id_res["threshold_percentage"] * 0.3 + max(0, 1.8 - fs_res["factor_of_safety"]) * 50 * 0.2, 1)
        comp_score = min(100.0, max(0.0, comp_score))

        color = STATUS_RED if comp_score > 85 or fs_res["factor_of_safety"] < 1.0 else (STATUS_ORANGE if comp_score > 60 else STATUS_GREEN)
        tier_text = "🔴 RED: IMMINENT DISASTER" if color == STATUS_RED else ("🟠 ORANGE: SEVERE WARNING" if color == STATUS_ORANGE else "🟢 GREEN: SAFE EQUILIBRIUM")

        self.sim_score_lbl.config(text=f"Composite Risk Index: {comp_score} / 100", fg=color)
        self.sim_tier_lbl.config(text=tier_text, fg=color)
        self.sim_fs_lbl.config(text=f"Infinite Slope Factor of Safety (Fs): {fs_res['factor_of_safety']} ({fs_res['stability_status']})", fg=fs_res["status_color"])
        self.sim_id_lbl.config(text=f"Rainfall I-D Threshold: {id_res['threshold_percentage']}% Capacity ({id_res['stage']})", fg=id_res["color"])

        adv = f"DIRECTIVE FOR DISASTER CONTROLLERS:\n\n"
        adv += f"• Terrain State: Slope Angle {slope:.0f}°, Pore Water Pressure {pwp:.1f} kPa.\n"
        adv += f"• Meteorological Load: {rain:.0f} mm/hr over {duration:.1f} hours ({id_res['cumulative_rainfall_mm']:.0f} mm total).\n"
        adv += f"• Geotechnical Assessment: {fs_res['safety_margin']}\n"
        adv += f"• Immediate Tactical Action: {ml_res['recommended_action']}\n\n"
        adv += f"Explainable AI Factors:\n"
        for f in ml_res["factor_breakdown"]:
            adv += f"  - {f['factor']}: {f['weight']}% weight ({f['impact']} Impact)\n"

        self.sim_advisory.delete("1.0", tk.END)
        self.sim_advisory.insert(tk.END, adv)

    # -------------------------------------------------------------
    # TAB 3: NER 8-State Geotechnical Matrix
    # -------------------------------------------------------------
    def _build_states_tab(self):
        container = tk.Frame(self.tab_states, bg=BG_DARK, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="🏔️ North Eastern Region 8-State Geotechnical & Hazard Profiles",
                 font=("Segoe UI", 13, "bold"), fg=ACCENT_CYAN, bg=BG_DARK).pack(anchor="w", pady=(0, 10))

        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_DARK)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for state_name, info in NER_STATES.items():
            card = tk.Frame(scrollable_frame, bg=BG_PANEL, padx=12, pady=10, relief="ridge", bd=1)
            card.pack(fill="x", expand=True, pady=6)

            header_row = tk.Frame(card, bg=BG_PANEL)
            header_row.pack(fill="x")

            tk.Label(header_row, text=f"{state_name} (Capital: {info['capital']})", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg=BG_PANEL).pack(side="left")
            tk.Label(header_row, text=f"Risk Score: {info['vulnerability_score']}/100 [{info['vulnerability_level']}]",
                     font=("Segoe UI", 9, "bold"), fg=STATUS_RED if info["vulnerability_score"] > 88 else STATUS_ORANGE, bg=BG_PANEL).pack(side="right")

            tk.Label(card, text=f"Geology: {info['geology']} | Annual Rain: {info['annual_rainfall_mm']} mm | Seismic: {info['seismic_zone']}",
                     font=("Segoe UI", 8), fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w", pady=2)
            tk.Label(card, text=f"Critical Districts: {', '.join(info['districts_at_risk'])}",
                     font=("Segoe UI", 8, "bold"), fg="#fca5a5", bg=BG_PANEL).pack(anchor="w", pady=2)
            tk.Label(card, text=info['description'], font=("Segoe UI", 8), fg="#cbd5e1", bg=BG_PANEL, wraplength=1000, justify="left").pack(anchor="w", pady=2)

    # -------------------------------------------------------------
    # TAB 4: Active CAP Early Warnings
    # -------------------------------------------------------------
    def _build_alerts_tab(self):
        container = tk.Frame(self.tab_alerts, bg=BG_DARK, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="🚨 Common Alerting Protocol (CAP v1.2) Official Early Warnings",
                 font=("Segoe UI", 13, "bold"), fg=ACCENT_CYAN, bg=BG_DARK).pack(anchor="w", pady=(0, 10))

        alerts = alert_service.get_all_active_alerts()
        for a in alerts:
            card = tk.Frame(container, bg=BG_PANEL, padx=14, pady=12, relief="ridge", bd=1)
            card.pack(fill="x", pady=6)

            tk.Label(card, text=f"{a['event_type']} • Severity: {a['severity']}", font=("Segoe UI", 9, "bold"), fg=STATUS_RED, bg=BG_PANEL).pack(anchor="w")
            tk.Label(card, text=a['headline'], font=("Segoe UI", 12, "bold"), fg="#ffffff", bg=BG_PANEL).pack(anchor="w", pady=2)
            tk.Label(card, text=f"Region: {a['region_name']}, {a['state']} | Issued: {a['created_at']}", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
            tk.Label(card, text=a['description'], font=("Segoe UI", 9), fg="#cbd5e1", bg=BG_PANEL, wraplength=1050, justify="left").pack(anchor="w", pady=4)

            inst_box = tk.Frame(card, bg="#450a0a", padx=8, pady=4)
            inst_box.pack(fill="x", pady=4)
            tk.Label(inst_box, text=f"Direct Action: {a['instruction']}", font=("Segoe UI", 9, "bold"), fg="#fca5a5", bg="#450a0a").pack(anchor="w")

    # -------------------------------------------------------------
    # TAB 5: Safe Evacuation Navigator
    # -------------------------------------------------------------
    def _build_evacuation_tab(self):
        container = tk.Frame(self.tab_evac, bg=BG_DARK, padx=16, pady=16)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="🏃 Safe Evacuation Routing to Designated Disaster Relief Shelters",
                 font=("Segoe UI", 13, "bold"), fg=ACCENT_CYAN, bg=BG_DARK).pack(anchor="w", pady=(0, 10))

        sel_frame = tk.Frame(container, bg=BG_PANEL, padx=12, pady=10)
        sel_frame.pack(fill="x", pady=4)

        tk.Label(sel_frame, text="Origin Monitoring Station:", font=("Segoe UI", 9, "bold"), fg=TEXT_LIGHT, bg=BG_PANEL).pack(side="left")
        self.evac_combobox = ttk.Combobox(sel_frame, values=[f"{s['name']} ({s['state']})" for s in IOT_STATIONS], state="readonly", width=45)
        self.evac_combobox.current(0)
        self.evac_combobox.pack(side="left", padx=8)

        btn_calc = tk.Button(sel_frame, text="🗺️ Calculate Route", bg=ACCENT_CYAN, fg="#000000",
                             font=("Segoe UI", 9, "bold"), command=self._run_evacuation_calc, relief="flat", padx=10)
        btn_calc.pack(side="left", padx=5)

        self.evac_results_frame = tk.Frame(container, bg=BG_DARK)
        self.evac_results_frame.pack(fill="both", expand=True, pady=10)

        self._run_evacuation_calc()

    def _run_evacuation_calc(self):
        for widget in self.evac_results_frame.winfo_children():
            widget.destroy()

        idx = self.evac_combobox.current()
        stn = IOT_STATIONS[idx if idx >= 0 else 0]

        routes = routing_service.find_nearest_shelters(stn["lat"], stn["lng"], limit=3)
        for i, r in enumerate(routes):
            shl = r["shelter"]
            is_top = (i == 0)

            card = tk.Frame(self.evac_results_frame, bg=BG_PANEL, padx=14, pady=12, relief="ridge", bd=2 if is_top else 1)
            card.pack(fill="x", pady=6)

            hdr = tk.Frame(card, bg=BG_PANEL)
            hdr.pack(fill="x")

            title_text = f"🛡️ {shl['name']} [RECOMMENDED PRIMARY SAFE ZONE]" if is_top else f"🛡️ {shl['name']}"
            tk.Label(hdr, text=title_text, font=("Segoe UI", 11, "bold"), fg=STATUS_GREEN if is_top else "#ffffff", bg=BG_PANEL).pack(side="left")
            tk.Label(hdr, text=f"Road Distance: {r['estimated_road_km']} km (Mountain Tortuosity)", font=("Segoe UI", 10, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL).pack(side="right")

            tk.Label(card, text=f"Location: {shl['district']}, {shl['state']} | Capacity: {shl['capacity']} persons | Helpline: {shl['contact_phone']}",
                     font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=2)
            tk.Label(card, text=f"Est. Vehicle Travel Time: ~{r['drive_time_mins']} mins | On-Foot Evacuation: ~{r['walk_time_mins']} mins",
                     font=("Segoe UI", 9, "bold"), fg="#ffffff", bg=BG_PANEL).pack(anchor="w", pady=2)
            tk.Label(card, text=f"Shelter Amenities: {', '.join(shl['amenities'])}", font=("Segoe UI", 8), fg="#cbd5e1", bg=BG_PANEL).pack(anchor="w", pady=2)

    # -------------------------------------------------------------
    # TAB 6: Incident Reporting & Catalog
    # -------------------------------------------------------------
    def _build_reporting_tab(self):
        paned = tk.PanedWindow(self.tab_rep, orient="horizontal", bg=BG_DARK, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        # Left: Submit Field Report Form
        form_frame = tk.Frame(paned, bg=BG_PANEL, padx=14, pady=12)
        paned.add(form_frame, width=540)

        tk.Label(form_frame, text="📢 Submit Ground Landslide Field Report", font=("Segoe UI", 11, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w", pady=(0, 8))

        tk.Label(form_frame, text="Reporter Name:", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        self.rep_name_entry = tk.Entry(form_frame, bg=BG_CARD, fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.rep_name_entry.insert(0, "Field Officer / Resident")
        self.rep_name_entry.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Location / Highway Milestone:", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(4, 0))
        self.rep_loc_entry = tk.Entry(form_frame, bg=BG_CARD, fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.rep_loc_entry.insert(0, "NH-10 Sevoke-Gangtok Milestone 29")
        self.rep_loc_entry.pack(fill="x", pady=2)

        tk.Label(form_frame, text="State:", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(4, 0))
        self.rep_state_combo = ttk.Combobox(form_frame, values=list(NER_STATES.keys()), state="readonly")
        self.rep_state_combo.current(0)
        self.rep_state_combo.pack(fill="x", pady=2)

        tk.Label(form_frame, text="Incident Observations:", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(4, 0))
        self.rep_desc_text = tk.Text(form_frame, height=4, bg=BG_CARD, fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.rep_desc_text.insert("1.0", "Active debris slide blocking two lanes of national highway.")
        self.rep_desc_text.pack(fill="x", pady=2)

        btn_submit = tk.Button(form_frame, text="Submit Report to Disaster Responder Queue", bg=STATUS_RED, fg="#ffffff",
                               font=("Segoe UI", 9, "bold"), command=self._submit_report, relief="flat", pady=6)
        btn_submit.pack(fill="x", pady=10)

        # Right: Benchmark Historical Disasters
        hist_frame = tk.Frame(paned, bg=BG_PANEL, padx=14, pady=12)
        paned.add(hist_frame, width=680)

        tk.Label(hist_frame, text="📜 Benchmark NER Historical Landslide Disasters", font=("Segoe UI", 11, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL).pack(anchor="w", pady=(0, 8))

        hist_box = scrolledtext.ScrolledText(hist_frame, wrap="word", bg=BG_CARD, fg="#ffffff", font=("Segoe UI", 9))
        hist_box.pack(fill="both", expand=True)

        hist_content = ""
        for h in HISTORICAL_LANDSLIDES:
            dt = h.get('date') or h.get('event_date') or 'Historical Record'
            dist = h.get('district', 'NER')
            st = h.get('state', '')
            cas = h.get('casualties', 0)
            vol = h.get('volume_m3', 0)
            trig = h.get('trigger') or h.get('trigger_factor') or 'Heavy Rainfall'
            dmg = h.get('infrastructure_damage', 'Infrastructure impact recorded.')
            hist_content += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            hist_content += f"📌 {h.get('name', 'Incident')} ({dt})\n"
            hist_content += f"   Location: {dist}, {st} | Fatalities: {cas} | Volume: {vol:,} m³\n"
            hist_content += f"   Trigger: {trig}\n"
            hist_content += f"   Damage: {dmg}\n\n"

        hist_box.insert(tk.END, hist_content)
        hist_box.configure(state="disabled")

    def _submit_report(self):
        name = self.rep_name_entry.get().strip()
        loc = self.rep_loc_entry.get().strip()
        st = self.rep_state_combo.get()
        desc = self.rep_desc_text.get("1.0", tk.END).strip()

        if not name or not loc:
            messagebox.showerror("Error", "Please fill in reporter name and location.")
            return

        report_id = add_citizen_report({
            "reporter_name": name,
            "state": st,
            "location_name": loc,
            "latitude": 25.5,
            "longitude": 92.5,
            "landslide_type": "Debris Slide",
            "estimated_size": "Medium",
            "road_blocked": True,
            "description": desc
        })

        messagebox.showinfo("Report Logged", f"Incident Report ID {report_id} has been submitted and queued for field verification.")

if __name__ == "__main__":
    app = LandslideDesktopApp()
    app.mainloop()
