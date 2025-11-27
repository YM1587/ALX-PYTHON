import requests
import os

# Try TaiwoOmotayo repo
url = "https://github.com/TaiwoOmotayo/Maji-Ndogo-Water-Project/raw/main/Maji_Ndogo_farm_survey_small.db"
print(f"Downloading from {url}...")
r = requests.get(url)

if r.status_code == 200:
    with open("Maji_Ndogo_farm_survey_small.db", "wb") as f:
        f.write(r.content)
    print(f"Download complete. Size: {os.path.getsize('Maji_Ndogo_farm_survey_small.db')} bytes")
else:
    print(f"Failed. Status code: {r.status_code}")
    # Try master branch
    url = "https://github.com/TaiwoOmotayo/Maji-Ndogo-Water-Project/raw/master/Maji_Ndogo_farm_survey_small.db"
    print(f"Downloading from {url}...")
    r = requests.get(url)
    if r.status_code == 200:
        with open("Maji_Ndogo_farm_survey_small.db", "wb") as f:
            f.write(r.content)
        print(f"Download complete. Size: {os.path.getsize('Maji_Ndogo_farm_survey_small.db')} bytes")
    else:
        print(f"Failed. Status code: {r.status_code}")
