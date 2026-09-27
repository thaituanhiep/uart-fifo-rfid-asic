@echo off
rem ==============================================================================
rem All-In-One Automated Build & Program Script for PicoRV32 + Basys 3 SoC
rem 1. Build Firmware (C -> firmware.bin)
rem 2. Build Vivado Bitstream (Verilog RTL -> top_basys3_picorv32_rdm6300.bit)
rem 3. Generate Combined Flash Image (.bin & .mcs)
rem 4. Automatically Program Basys 3 SPI Flash & Boot via QSPI (Non-Volatile)
rem ==============================================================================

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
echo   [2/4] Building Basys 3 FPGA Bitstream with Vivado...
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

echo.
echo ======================================================================
echo   [4/4] Programming Basys 3 Non-Volatile SPI Flash (QSPI Boot)...
echo ======================================================================
call program_flash.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Flash programming failed!
    echo Please make sure Basys 3 USB cable is connected and board is powered on.
    cd ..
    exit /b 1
)

rem Clean up Vivado logs
if exist vivado*.log move /y vivado*.log vivado\ >nul
if exist vivado*.jou move /y vivado*.jou vivado\ >nul
if exist clockInfo.txt move /y clockInfo.txt temp\ >nul
if exist dfx_runtime.txt move /y dfx_runtime.txt temp\ >nul
cd ..
if exist vivado*.log move /y vivado*.log fpga\vivado\ >nul
if exist vivado*.jou move /y vivado*.jou fpga\vivado\ >nul
if exist clockInfo.txt move /y clockInfo.txt temp\ >nul
if exist dfx_runtime.txt move /y dfx_runtime.txt temp\ >nul

echo.
echo ======================================================================
echo   ALL BUILDS AND NON-VOLATILE FLASH PROGRAMMING COMPLETED!
echo ======================================================================
echo   - Firmware Binary     : firmware\firmware.bin
echo   - FPGA Bitstream      : fpga\top_basys3_picorv32_rdm6300.bit
echo   - Combined Flash Image: fpga\top_basys3_picorv32_rdm6300_flash.bin
echo   - Hardware Mode       : QSPI Non-Volatile Boot (Persistent)
echo.
echo   [NOTE] With Jumper JP1 set to QSPI, the Basys 3 board will now
echo          boot automatically on power-up without needing Vivado!
echo ======================================================================
exit /b 0
