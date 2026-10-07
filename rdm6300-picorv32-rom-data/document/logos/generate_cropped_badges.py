import os, subprocess
from PIL import Image

out = r"c:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\logos"
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

badges = [
    # 1. OpenLane 2
    ("openlane", """
      <svg class="icon" viewBox="0 0 100 100" style="width:36px;height:36px;">
        <path d="M15,15 L15,65 Q15,85 35,85 L85,85" fill="none" stroke="#6366F1" stroke-width="8" stroke-linecap="round"/>
        <path d="M30,15 L30,55 Q30,70 45,70 L85,70" fill="none" stroke="#8B5CF6" stroke-width="8" stroke-linecap="round"/>
        <path d="M45,15 L45,45 Q45,55 55,55 L85,55" fill="none" stroke="#EC4899" stroke-width="8" stroke-linecap="round"/>
      </svg>
      <div class="sep"></div>
      <div class="text">
        <div class="title">Open<span style="color:#6366F1;">Lane</span> 2</div>
        <div class="sub">ASIC Digital Flow</div>
      </div>
    """),

    # 2. Vivado Design Suite
    ("vivado", """
      <div style="font-weight:900;font-size:26px;letter-spacing:-1px;color:#111;">AM<span style="color:#ED1C24;">D</span></div>
      <div class="sep"></div>
      <div class="text">
        <div class="title" style="letter-spacing:0.5px;">VIVADO</div>
        <div class="sub">Design Suite</div>
      </div>
    """),

    # 3. FPGA (Xilinx Artix-7)
    ("fpga", """
      <div style="width:34px;height:34px;background:#D12420;border-radius:6px;display:flex;align-items:center;justify-content:center;color:white;font-weight:900;font-size:22px;">Σ</div>
      <div class="sep"></div>
      <div class="text">
        <div class="title">XILINX <span style="color:#D12420;">FPGA</span></div>
        <div class="sub">Artix-7 XC7A35T</div>
      </div>
    """),

    # 4. RISC-V PicoRV32
    ("riscv", """
      <img src="riscv.png" style="height:28px;width:auto;display:block;" />
      <div class="sep"></div>
      <div class="text">
        <div class="title" style="color:#0F172A;">PicoRV32</div>
        <div class="sub">32-bit RISC-V CPU</div>
      </div>
    """),

    # 5. SkyWater 130nm PDK
    ("skywater", """
      <div style="width:34px;height:34px;background:linear-gradient(135deg, #0EA5E9, #10B981);border-radius:6px;display:flex;align-items:center;justify-content:center;color:white;font-weight:900;font-size:16px;">130</div>
      <div class="sep"></div>
      <div class="text">
        <div class="title">SkyWater <span style="color:#0EA5E9;">130nm</span></div>
        <div class="sub">Open Source PDK</div>
      </div>
    """),
]

for name, inner_html in badges:
    full_html = f"""<!DOCTYPE html><html><head><style>
    body {{ margin: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; display: inline-flex; padding: 20px; }}
    .badge {{ display: inline-flex; align-items: center; gap: 14px; background: white; padding: 12px 22px; border-radius: 12px; border: 1.5px solid #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
    .sep {{ width: 2px; height: 32px; background: #E2E8F0; }}
    .text {{ display: flex; flex-direction: column; white-space: nowrap; }}
    .title {{ font-weight: 800; font-size: 19px; color: #0F172A; line-height: 1.15; }}
    .sub {{ font-weight: 600; font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }}
    </style></head><body>
    <div class="badge">{inner_html}</div>
    </body></html>"""

    html_file = os.path.join(out, f"badge_{name}.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    raw_png = os.path.join(out, f"raw_{name}.png")
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--default-background-color=00000000",
        f"--screenshot={raw_png}", "--window-size=600,200",
        "file:///" + html_file.replace(os.sep, "/")
    ])

    # Crop tightly to non-transparent pixels with 4px margin
    im = Image.open(raw_png)
    bbox = im.getbbox()
    if bbox:
        # add slight padding
        cropped = im.crop(bbox)
        final_png = os.path.join(out, f"badge_{name}.png")
        cropped.save(final_png)
        print(f"Generated {final_png}: size {cropped.size}")

print("Done generating all badges!")
