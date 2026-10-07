import os, subprocess

out = r"c:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\logos"
svg_path = os.path.join(out, "amd_vivado.svg")
html = f"""<!DOCTYPE html><html><body style="margin:0;background:transparent">
<img src="amd_vivado.svg" style="width:600px;display:block"></body></html>"""
html_path = os.path.join(out, "render_vivado.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

png = os.path.join(out, "vivado_full.png")
subprocess.run([
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new", "--disable-gpu", "--hide-scrollbars",
    "--default-background-color=00000000",
    f"--screenshot={png}", "--window-size=600,320",
    "file:///" + html_path.replace(os.sep, "/")
])
print("Saved vivado_full.png")
