@echo off
rem ==============================================================================
rem All-In-One Automated Build & Program Script for PicoRV32 + Basys 3 SoC
rem 1. Build Firmware (C -> firmware.bin, firmware.hex)
rem 2. Build Vivado Bitstream (14 Verilog RTL Modules -> top_basys3_picorv32_rdm6300.bit)
rem 3. Generate Combined Flash Image (.bin & .mcs)
rem 4. (Optional) Program Basys 3 SPI Flash & Boot via QSPI (Non-Volatile)
rem
rem Usage:
rem   build_all.bat             : Build all artifacts and program Basys 3 if connected
rem   build_all.bat --build-only: Build all artifacts (Firmware, Bitstream, Flash Images) only
rem ==============================================================================

if /i "%1"=="/?" goto :show_help
if /i "%1"=="-h" goto :show_help
if /i "%1"=="--help" goto :show_help

set "BUILD_ONLY=0"
if /i "%1"=="--build-only" set "BUILD_ONLY=1"
if /i "%1"=="-b" set "BUILD_ONLY=1"
if /i "%1"=="/b" set "BUILD_ONLY=1"
if /i "%1"=="--no-program" set "BUILD_ONLY=1"

echo ======================================================================
echo   [1/4] Building PicoRV32 Firmware...
echo ======================================================================
cd firmware
call build_firmware.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Firmware build failed!
    cd ..
    exit /b 1
)
cd ..

echo.
echo ======================================================================
echo   [2/4] Building Basys 3 FPGA Bitstream with Vivado (Unified RTL Modules)...
echo ======================================================================
cd fpga
call generate_bitstream.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Vivado bitstream generation failed!
    cd ..
    exit /b 1
)

echo.
echo ======================================================================
echo   [3/4] Generating Combined Flash Image (.bin and .mcs)...
echo ======================================================================
call generate_flash_image.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Flash image generation failed!
    cd ..
    exit /b 1
)

if "%BUILD_ONLY%"=="1" (
    echo.
    echo ======================================================================
    echo   [INFO] --build-only specified. Skipping FPGA hardware programming.
    echo ======================================================================
    goto :cleanup_and_finish
)

echo.
echo ======================================================================
echo   [4/4] Programming Basys 3 Non-Volatile SPI Flash (QSPI Boot)...
echo ======================================================================
call program_flash.bat
if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] Basys 3 hardware programming skipped or failed.
    echo Make sure Basys 3 USB cable is connected and powered on if you wish to program.
    echo (All Firmware, Bitstream, and Flash images were built successfully!)
)

:cleanup_and_finish
rem Clean up Vivado logs
if exist vivado*.log move /y vivado*.log vivado\ >nul 2>nul
if exist vivado*.jou move /y vivado*.jou vivado\ >nul 2>nul
if exist clockInfo.txt move /y clockInfo.txt temp\ >nul 2>nul
if exist dfx_runtime.txt move /y dfx_runtime.txt temp\ >nul 2>nul
cd ..
if exist vivado*.log move /y vivado*.log fpga\vivado\ >nul 2>nul
if exist vivado*.jou move /y vivado*.jou fpga\vivado\ >nul 2>nul
if exist clockInfo.txt move /y clockInfo.txt temp\ >nul 2>nul
if exist dfx_runtime.txt move /y dfx_runtime.txt temp\ >nul 2>nul

echo.
echo ======================================================================
echo   ALL BUILDS COMPLETED SUCCESSFULLY!
echo ======================================================================
echo   - Firmware Binary     : firmware\firmware.bin
echo   - Firmware HEX (Core) : rtl\core\firmware.hex
echo   - FPGA Bitstream      : fpga\top_basys3_picorv32_rdm6300.bit
echo   - Combined Flash Image: fpga\top_basys3_picorv32_rdm6300_flash.bin
echo   - Flash MCS File      : fpga\top_basys3_picorv32_rdm6300_flash.mcs
echo   - Hardware Mode       : QSPI Non-Volatile Boot (Persistent)
echo   [NOTE] With Jumper JP1 set to QSPI, the Basys 3 board will now
echo          boot automatically on power-up without needing Vivado!
echo ======================================================================
exit /b 0

:show_help
echo ======================================================================
echo   PicoRV32 + Basys 3 RFID SoC - Build ^& Program Runner
echo ======================================================================
echo   Usage:
echo     build_all.bat              Run complete flow (Firmware + Bitstream + Flash + Program)
echo     build_all.bat --build-only Build all artifacts only (No board programming)
echo     build_all.bat -b           Alias for --build-only
echo     build_all.bat --help       Display this help message
echo ======================================================================
exit /b 0
