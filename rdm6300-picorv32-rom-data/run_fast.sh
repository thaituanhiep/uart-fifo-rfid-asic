#!/bin/bash
# ==============================================================================
# Script: run_fast.sh
# Project: rdm6300-picorv32-rom-data
# Description: Chay OpenLane (--dockerized) tren o dia sieu toc noi bo Linux (/tmp)
#              de tranh nghen I/O qua sharefolder (/mnt/hgfs), sau do tu dong
#              dong bo ket qua ve Windows.
# ==============================================================================

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="/tmp/rdm6300-build"

echo "======================================================================"
echo "  OPENLANE FAST RUNNER (DOCKERIZED)"
echo "  Nguon (Windows Share): $SRC_DIR"
echo "  Vung chay sieu toc (Linux): $BUILD_DIR"
echo "======================================================================"

# 1. Kich hoat virtual environment neu co
if [ -f "$HOME/openlane-venv/bin/activate" ]; then
    echo "[INFO] Kich hoat virtual environment: $HOME/openlane-venv"
    source "$HOME/openlane-venv/bin/activate"
fi

# Kiem tra openlane
if ! python3 -m openlane --version &> /dev/null && ! command -v openlane &> /dev/null; then
    echo "[LOI] Khong tim thay Python module 'openlane'!"
    echo "Vui long kiem tra lai: source ~/openlane-venv/bin/activate"
    exit 127
fi

echo "[INFO] Phien ban OpenLane: $(python3 -m openlane --version 2>/dev/null || openlane --version)"

# 2. Dong bo code moi nhat tu Windows sang Linux /tmp
echo "[1/3] Dang dong bo ma nguon sang $BUILD_DIR..."
mkdir -p "$BUILD_DIR"
rsync -av --exclude 'runs' "$SRC_DIR/" "$BUILD_DIR/" > /dev/null

# 3. Chay OpenLane voi co --dockerized tren o dia sieu toc cua Linux
echo "[2/3] Dang chay OpenLane (--dockerized) voi toc do toi da tren SSD Linux..."
cd "$BUILD_DIR"

python3 -m openlane --dockerized config.json
STATUS=$?

# 4. Luon dong bo ket qua va log ve lai Windows ke ca khi co loi
if [ -d "$BUILD_DIR/runs" ]; then
    echo "[3/3] Dang dong bo ket qua va log ve lai Windows ($SRC_DIR/runs)..."
    mkdir -p "$SRC_DIR/runs"
    rsync -av "$BUILD_DIR/runs/" "$SRC_DIR/runs/"
fi

echo "======================================================================"
if [ $STATUS -eq 0 ]; then
    echo "  [THANH CONG] Hoan tat OpenLane! File GDSII va bao cao da co tren Windows."
else
    echo "  [CANH BAO] OpenLane dung voi ma: $STATUS. Log da duoc chep ve Windows de kiem tra."
fi
echo "======================================================================"

exit $STATUS
