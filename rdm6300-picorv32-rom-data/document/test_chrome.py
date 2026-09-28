import subprocess
import os

html_content = """<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; background: white; font-family: Segoe UI, Arial, sans-serif; }
.card { width: 400px; height: 200px; border: 2px solid #2B579A; background: #EEF3F8; border-radius: 8px; margin: 50px; padding: 20px; box-sizing: border-box; }
h2 { margin: 0 0 10px 0; color: #2B579A; font-size: 24px; }
p { margin: 0; font-size: 16px; color: #333; }
</style>
</head>
<body>
<div class="card">
  <h2>Draw.io Style Card</h2>
  <p>Clean fonts, perfect borders, modern aesthetic!</p>
</div>
</body>
</html>
"""

with open("test.html", "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = os.path.abspath("test.html")
out_img = os.path.abspath("test_chrome.png")

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--force-device-scale-factor=2",
    f"--screenshot={out_img}",
    "--window-size=600,400",
    f"file:///{html_path.replace(os.sep, '/')}"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome return code:", res.returncode)
print("Output file exists:", os.path.exists(out_img), os.path.getsize(out_img) if os.path.exists(out_img) else 0)
