import json
import sys
import os

# Make sure we are looking at the right data
data_path = os.path.join("data", "processed", "processed_data.json")

try:
    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)
except Exception as e:
    print(f"Error reading file {data_path}: {e}")
    sys.exit(1)

authors_found = set()
unspecified_count = 0
total_interps = 0
for i in d:
    for interp in i["interpretaciones"]:
        total_interps += 1
        authors_found.add(interp["autor"])
        if interp["autor"] == "General/No especificado":
            unspecified_count += 1

print(f"Authors found: {authors_found}")

if total_interps > 0:
    print(
        f"Unspecified: {unspecified_count}/{total_interps} ({unspecified_count/total_interps*100:.2f}%)"
    )
else:
    print("No interpretations found.")
