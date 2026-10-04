import json
import html

with open(r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\soc_codesign_architecture.drawio", "r", encoding="utf-8") as f:
    xml_str = f.read()

config = {
    "highlight": "#0284c7",
    "nav": True,
    "resize": True,
    "toolbar": "pages zoom layers tags fullscreen",
    "edit": "https://app.diagrams.net",
    "xml": xml_str
}

config_json = json.dumps(config)
escaped_config = html.escape(config_json)

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SoC PicoRV32 Co-Design Architecture (Draw.io Viewer)</title>
    <style>
        body, html {{
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .top-bar {{
            height: 48px;
            background: #0f172a;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .title {{
            font-size: 15px;
            font-weight: 700;
        }}
        .btn {{
            background: #0284c7;
            color: #ffffff;
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
        }}
        .btn:hover {{
            background: #0369a1;
        }}
        #container {{
            width: 100%;
            height: calc(100% - 48px);
        }}
        .mxgraph {{
            width: 100%;
            height: 100%;
        }}
    </style>
    <script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
</head>
<body>
    <div class="top-bar">
        <div class="title">📐 SoC PicoRV32 Co-Design Architecture - Draw.io Interactive Viewer</div>
        <div>
            <a class="btn" href="https://app.diagrams.net" target="_blank">Mở trên App.Diagrams.Net để Chỉnh Sửa ↗</a>
        </div>
    </div>
    <div id="container">
        <div class="mxgraph" data-mxgraph="{escaped_config}"></div>
    </div>
</body>
</html>
"""

with open(r"d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\xem_drawio_ngay.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("[SUCCESS] Created xem_drawio_ngay.html with embedded Draw.io Viewer!")
