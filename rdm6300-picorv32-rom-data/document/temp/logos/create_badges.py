import os, subprocess
from PIL import Image

out = r"c:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\logos"
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 1. Vivado Logo (AMD Vivado with brand red accent / dark text on white)
html_vivado = """<!DOCTYPE html><html><head><style>
body { margin: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; }
.badge { display: flex; align-items: center; gap: 14px; background: white; padding: 12px 24px; border-radius: 12px; border: 1.5px solid #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.amd { font-weight: 900; font-size: 28px; letter-spacing: -1px; color: #111; }
.amd span { color: #ED1C24; }
.sep { width: 2px; height: 32px; background: #E2E8F0; }
.text { display: flex; flex-direction: column; }
.title { font-weight: 800; font-size: 20px; color: #0F172A; line-height: 1.1; }
.sub { font-weight: 600; font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
</style></head><body>
<div class="badge">
  <div class="amd">AM<span>D</span></div>
  <div class="sep"></div>
  <div class="text">
    <div class="title">VIVADO</div>
    <div class="sub">Design Suite</div>
  </div>
</div>
</body></html>"""
with open(os.path.join(out, "card_vivado.html"), "w", encoding="utf-8") as f: f.write(html_vivado)
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                f"--screenshot={os.path.join(out, 'badge_vivado.png')}", "--window-size=340,110",
                "file:///" + os.path.join(out, "card_vivado.html").replace(os.sep, "/")])

# 2. OpenLane Logo (OpenLane 2 with EDA route lanes icon)
html_openlane = """<!DOCTYPE html><html><head><style>
body { margin: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; }
.badge { display: flex; align-items: center; gap: 14px; background: white; padding: 12px 24px; border-radius: 12px; border: 1.5px solid #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.icon { width: 36px; height: 36px; }
.sep { width: 2px; height: 32px; background: #E2E8F0; }
.text { display: flex; flex-direction: column; }
.title { font-weight: 800; font-size: 20px; color: #1E293B; line-height: 1.1; }
.title span { color: #6366F1; }
.sub { font-weight: 600; font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
</style></head><body>
<div class="badge">
  <svg class="icon" viewBox="0 0 100 100">
    <path d="M15,15 L15,65 Q15,85 35,85 L85,85" fill="none" stroke="#6366F1" stroke-width="8" stroke-linecap="round"/>
    <path d="M30,15 L30,55 Q30,70 45,70 L85,70" fill="none" stroke="#8B5CF6" stroke-width="8" stroke-linecap="round"/>
    <path d="M45,15 L45,45 Q45,55 55,55 L85,55" fill="none" stroke="#EC4899" stroke-width="8" stroke-linecap="round"/>
  </svg>
  <div class="sep"></div>
  <div class="text">
    <div class="title">Open<span>Lane</span> 2</div>
    <div class="sub">ASIC Flow</div>
  </div>
</div>
</body></html>"""
with open(os.path.join(out, "card_openlane.html"), "w", encoding="utf-8") as f: f.write(html_openlane)
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                f"--screenshot={os.path.join(out, 'badge_openlane.png')}", "--window-size=340,110",
                "file:///" + os.path.join(out, "card_openlane.html").replace(os.sep, "/")])

# 3. Xilinx Artix-7 FPGA Logo
html_fpga = """<!DOCTYPE html><html><head><style>
body { margin: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; }
.badge { display: flex; align-items: center; gap: 14px; background: white; padding: 12px 24px; border-radius: 12px; border: 1.5px solid #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.xilinx-icon { width: 34px; height: 34px; background: #D12420; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 22px; }
.sep { width: 2px; height: 32px; background: #E2E8F0; }
.text { display: flex; flex-direction: column; }
.title { font-weight: 800; font-size: 19px; color: #0F172A; line-height: 1.1; }
.title span { color: #D12420; }
.sub { font-weight: 600; font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; }
</style></head><body>
<div class="badge">
  <div class="xilinx-icon">Σ</div>
  <div class="sep"></div>
  <div class="text">
    <div class="title">XILINX <span>FPGA</span></div>
    <div class="sub">Artix-7 XC7A35T</div>
  </div>
</div>
</body></html>"""
with open(os.path.join(out, "card_fpga.html"), "w", encoding="utf-8") as f: f.write(html_fpga)
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                f"--screenshot={os.path.join(out, 'badge_fpga.png')}", "--window-size=350,110",
                "file:///" + os.path.join(out, "card_fpga.html").replace(os.sep, "/")])

# 4. RISC-V Logo (using official logo)
html_riscv = """<!DOCTYPE html><html><head><style>
body { margin: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; }
.badge { display: flex; align-items: center; gap: 14px; background: white; padding: 12px 24px; border-radius: 12px; border: 1.5px solid #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.logo-img { height: 28px; width: auto; display: block; }
.sep { width: 2px; height: 32px; background: #E2E8F0; }
.text { display: flex; flex-direction: column; }
.title { font-weight: 800; font-size: 18px; color: #0F172A; line-height: 1.1; }
.sub { font-weight: 600; font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; }
</style></head><body>
<div class="badge">
  <img class="logo-img" src="riscv.png" />
  <div class="sep"></div>
  <div class="text">
    <div class="title">PicoRV32</div>
    <div class="sub">32-bit RISC-V CPU</div>
  </div>
</div>
</body></html>"""
with open(os.path.join(out, "card_riscv.html"), "w", encoding="utf-8") as f: f.write(html_riscv)
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                f"--screenshot={os.path.join(out, 'badge_riscv.png')}", "--window-size=370,110",
                "file:///" + os.path.join(out, "card_riscv.html").replace(os.sep, "/")])

# 5. SkyWater 130nm ASIC Logo
html_sky130 = """<!DOCTYPE html><html><head><style>
body { margin: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; }
.badge { display: flex; align-items: center; gap: 14px; background: white; padding: 12px 24px; border-radius: 12px; border: 1.5px solid #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.sky-icon { width: 34px; height: 34px; background: linear-gradient(135deg, #0EA5E9, #10B981); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 18px; }
.sep { width: 2px; height: 32px; background: #E2E8F0; }
.text { display: flex; flex-direction: column; }
.title { font-weight: 800; font-size: 18px; color: #0F172A; line-height: 1.1; }
.title span { color: #0EA5E9; }
.sub { font-weight: 600; font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; }
</style></head><body>
<div class="badge">
  <div class="sky-icon">130</div>
  <div class="sep"></div>
  <div class="text">
    <div class="title">SkyWater <span>130nm</span></div>
    <div class="sub">ASIC Standard Cell</div>
  </div>
</div>
</body></html>"""
with open(os.path.join(out, "card_sky130.html"), "w", encoding="utf-8") as f: f.write(html_sky130)
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                f"--screenshot={os.path.join(out, 'badge_sky130.png')}", "--window-size=370,110",
                "file:///" + os.path.join(out, "card_sky130.html").replace(os.sep, "/")])

print("All badges rendered!")
