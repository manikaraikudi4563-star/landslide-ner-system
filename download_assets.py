"""
Downloads Leaflet and Chart.js into static/vendor for 100% offline self-contained operation.
"""

import urllib.request
import os

VENDOR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "vendor")
os.makedirs(VENDOR_DIR, exist_ok=True)

ASSETS = {
    "leaflet.css": "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
    "leaflet.js": "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
    "chart.umd.min.js": "https://cdn.jsdelivr.net/npm/chart.js/dist/chart.umd.min.js"
}

def download_offline_assets():
    for filename, url in ASSETS.items():
        filepath = os.path.join(VENDOR_DIR, filename)
        if not os.path.exists(filepath):
            try:
                print(f"Downloading {filename} from {url}...")
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as response, open(filepath, "wb") as out_file:
                    out_file.write(response.read())
                print(f"[OK] Saved {filename}")
            except Exception as e:
                print(f"[WARN] Could not fetch {filename}: {e}")

if __name__ == "__main__":
    download_offline_assets()
