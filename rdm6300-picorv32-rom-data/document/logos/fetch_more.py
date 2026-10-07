import urllib.request, json, os

out = r"c:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\logos"
headers = {"User-Agent": "Mozilla/5.0"}

urls = {
    # Vivado
    "vivado_wiki": "https://commons.wikimedia.org/wiki/Special:FilePath/Vivado_Design_Suite_logo.png?width=500",
    "xilinx_wiki": "https://commons.wikimedia.org/wiki/Special:FilePath/Xilinx_logo.svg?width=500",
    "riscv_wiki": "https://commons.wikimedia.org/wiki/Special:FilePath/RISC-V-logo.svg?width=500",
    "efabless": "https://raw.githubusercontent.com/efabless/openlane/master/docs/_static/openlane_logo.png",
    "openlane_gh": "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenLane/master/docs/_static/ol2_banner.png",
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req, timeout=10).read()
        ext = "png"
        path = os.path.join(out, f"{name}.{ext}")
        with open(path, "wb") as f:
            f.write(data)
        print(f"Downloaded {name}: {len(data)} bytes")
    except Exception as e:
        print(f"Error {name}: {e}")
