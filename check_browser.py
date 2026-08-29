import sys
import subprocess
import shutil
import importlib.util

print("Python executable:", sys.executable)
for pkg in ["selenium", "playwright", "playwright.sync_api", "playwright.async_api", "playwright._impl", "urllib"]:
    spec = importlib.util.find_spec(pkg)
    print(f"Package {pkg}: {'Available' if spec else 'Not Available'}")

for exe in ["msedge.exe", "chrome.exe", "firefox.exe"]:
    path = shutil.which(exe)
    print(f"Executable {exe}: {path}")

# Check default Edge install location on Windows
edge_default = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
print(f"Edge at {edge_default}: {os.path.exists(edge_default) if 'os' in globals() or __import__('os').path.exists(edge_default) else False}")
