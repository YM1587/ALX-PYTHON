import requests
import zipfile
import os

url = "https://github.com/Explore-AI/Public-Data/raw/master/Maji_Ndogo/modules.zip"
print(f"Downloading from {url}...")
r = requests.get(url)
r.raise_for_status()

with open("modules.zip", "wb") as f:
    f.write(r.content)
print("Download complete.")

with zipfile.ZipFile("modules.zip", "r") as z:
    for f in z.namelist():
        print(f"{f}: {z.getinfo(f).file_size} bytes")
