import requests
import zipfile
import io
import os

url = "https://github.com/Explore-AI/Public-Data/raw/master/Maji_Ndogo/modules.zip"
print(f"Downloading from {url}...")
r = requests.get(url)
r.raise_for_status()
print("Download complete.")

z = zipfile.ZipFile(io.BytesIO(r.content))
print("Extracting files...")
z.extractall(".")
print("Extraction complete.")

# Check if DB exists and has size
db_path = "Maji_Ndogo_farm_survey_small.db"
if os.path.exists(db_path):
    print(f"DB size: {os.path.getsize(db_path)} bytes")
else:
    print("DB file not found after extraction.")
