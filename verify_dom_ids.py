import re
import os

html_path = r"C:\Users\manik\.gemini\antigravity-ide\scratch\landslide-ner-system\static\index.html"
js_path = r"C:\Users\manik\.gemini\antigravity-ide\scratch\landslide-ner-system\static\js\app.js"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Extract all getElementById calls
get_elem_ids = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js))

# Extract all IDs defined in HTML
html_ids = set(re.findall(r"id=['\"]([^'\"]+)['\"]", html))

missing_in_html = []
for eid in sorted(get_elem_ids):
    if eid not in html_ids:
        missing_in_html.append(eid)

print("Total getElementById queried in JS:", len(get_elem_ids))
print("Total IDs declared in HTML:", len(html_ids))
print("Missing IDs in HTML:", missing_in_html if missing_in_html else "NONE (100% matched)")
