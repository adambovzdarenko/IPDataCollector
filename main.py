import requests
from bs4 import BeautifulSoup
import json
import os
import folium

print("Enter the IP: ")
ip = input().strip()

url = "https://browserleaks.com/ip/" + ip
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

data = {"IP": ip}
lat, lon = None, None

# Trash values
trash_values = {"", "n/a (no js)", "run dns leak test", "*/*", "noscript"}

def clean_value(val: str) -> str | None:
    val = val.strip().lower()
    if val in trash_values:
        return None
    return val

# Collecting data from browserleaks
for table in soup.find_all("table"):
    section = table.find("h3")
    section_name = section.get_text(strip=True) if section else "Unknown Section"

    table_data = {}
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 2:
            key = cols[0].get_text(" ", strip=True)
            value = cols[1].get_text(" ", strip=True)
            value = clean_value(value)
            if value:
                table_data[key] = value

    if table_data:
        data[section_name] = table_data

# Coordinates
coords_tag = soup.find(id="coords-data")
if coords_tag:
    lat = coords_tag.get("data-lat")
    lon = coords_tag.get("data-lon")

# Console output
for section, values in data.items():
    if isinstance(values, dict):
        print(f"\n--- {section} ---")
        for k, v in values.items():
            print(f"[{k}: {v}]")
    else:
        print(f"[{section}: {values}]")

# Data export
save_input = input("\nType 'save' or 'S' to export: ").strip().lower()
if save_input in {"save", "s"}:
    folder_path = os.path.join("ext_data", ip)
    os.makedirs(folder_path, exist_ok=True)

    json_path = os.path.join(folder_path, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\nData saved as {json_path}")

    # Location
    if lat and lon:
        m = folium.Map(location=[float(lat), float(lon)], zoom_start=10)
        folium.Marker([float(lat), float(lon)], popup=ip).add_to(m)

        map_path = os.path.join(folder_path, "map.html")
        m.save(map_path)
        print(f"Location saved as {map_path}")
    else:
        print("Coordinates not found")
else:
    print("No data found")
