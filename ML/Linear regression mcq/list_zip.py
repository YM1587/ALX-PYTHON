import zipfile

with zipfile.ZipFile("modules.zip", "r") as z:
    for f in z.namelist():
        print(f"{f}: {z.getinfo(f).file_size} bytes")
