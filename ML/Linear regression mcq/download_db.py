import requests
import os

url = "https://github.com/Explore-AI/Public-Data/raw/master/Maji_Ndogo/Maji_Ndogo_farm_survey_small.db"
print(f"Checking {url}...")
r = requests.head(url)
if r.status_code == 200:
    print("File found. Downloading...")
    r = requests.get(url)
    with open("Maji_Ndogo_farm_survey_small.db", "wb") as f:
        f.write(r.content)
    print(f"Download complete. Size: {os.path.getsize('Maji_Ndogo_farm_survey_small.db')} bytes")
else:
    print(f"File not found. Status code: {r.status_code}")
