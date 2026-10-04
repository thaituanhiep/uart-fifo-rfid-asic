@echo off
set "DIAGRAM_PATH=%~dp0document\soc_codesign_architecture.drawio"

echo ========================================================
echo MO SO DO DRAW.IO CO-DESIGN HOAN TOAN TU DONG:
echo ========================================================
echo 1. Dang mo thu muc chua file so do trong Windows Explorer...
explorer /select,"%DIAGRAM_PATH%"

echo 2. Dang mo trang app.diagrams.net tren trinh duyet...
start "" "https://app.diagrams.net"

echo.
echo ========================================================
echo BAN CHI CAN KEO THA FILE "soc_codesign_architecture.drawio"
echo DANG DUOC CHON TRONG EXPLORER VAO TRINH DUYET LA XONG!
echo ========================================================
pause
exit
