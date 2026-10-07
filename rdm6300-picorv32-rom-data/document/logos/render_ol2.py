import urllib.request, os, subprocess

out = r"c:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\logos"
svg_url = "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenLane/master/docs/_static/ol2_banner.svg"
svg = urllib.request.urlopen(urllib.request.Request(svg_url, headers={"User-Agent": "Mozilla/5.0"})).read()
svg_path = os.path.join(out, "ol2_banner.svg")
with open(svg_path, "wb") as f:
    f.write(svg)

html = """<!DOCTYPE html><html><body style="margin:0;background:transparent">
<img src="ol2_banner.svg" style="width:800px;display:block"></body></html>"""
html_path = os.path.join(out, "render_ol2.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

png = os.path.join(out, "openlane_banner.png")
subprocess.run([
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new", "--disable-gpu", "--hide-scrollbars",
    "--default-background-color=00000000",
    f"--screenshot={png}", "--window-size=800,200",
    "file:///" + html_path.replace(os.sep, "/")
])
print("Saved openlane_banner.png:", os.path.exists(png))
