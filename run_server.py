"""
One-click Launcher for the AI-Based Early Warning & Landslide Risk Monitoring System in NER.
Starts the FastAPI application on http://127.0.0.1:8000
"""

import uvicorn
import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print("=" * 75)
    print("  AI-BASED LANDSLIDE RISK & EARLY WARNING SYSTEM - NER INDIA")
    print("=" * 75)
    print("  Coverage: Sikkim, Meghalaya, Assam, Manipur, Nagaland, Mizoram, Arunachal, Tripura")
    print("  Geotechnical Models: Infinite Slope Fs, Rainfall I-D Threshold, ML Susceptibility")
    print("  Sensors: Biaxial Inclinometers, Vibrating Wire Piezometers, Rain Gauges, Geophones")
    print(f"  Web GIS UI: http://{host}:{port}")
    print("=" * 75)
    
    uvicorn.run("app.main:app", host=host, port=port, reload=False)
