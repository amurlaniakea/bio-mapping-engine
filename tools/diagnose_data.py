import json

with open("data/processed/processed_data.json", encoding="utf-8") as f:
    d = json.load(f)

total_items = len(d)
total_interps = sum(len(i["interpretaciones"]) for i in d)
unspecified = sum(
    1
    for i in d
    for x in i["interpretaciones"]
    if x["autor"] == "General/No especificado"
)
empty = sum(
    1
    for i in d
    for x in i["interpretaciones"]
    if not x["conflicto_emocional"]
    and not x["modelo_mental"]
    and not x["etapa_biologica"]
)
no_zone = sum(1 for i in d if not i["zonas_detectadas"])

print(f"Total items: {total_items}, Total interpretaciones: {total_interps}")
print(
    f"Unspecified Authors: {unspecified}/{total_interps} "
    f"({unspecified/total_interps*100:.2f}%)"
)
print(f"Empty Fields: {empty}/{total_interps} " f"({empty/total_interps*100:.2f}%)")
print(f"Missing Zones: {no_zone}/{total_items} " f"({no_zone/total_items*100:.2f}%)")
