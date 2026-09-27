@echo off
rem Batch script to generate combined Flash image (.mcs / .bin)
echo ========================================================
echo   Generating Combined Flash Image for Basys 3
echo ========================================================

set "VIVADO_BIN=D:\Xilinx\2025.1\Vivado\bin\vivado.bat"
if not exist "%VIVADO_BIN%" (
    where vivado >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "VIVADO_BIN=vivado"
    ) else (
        echo [ERROR] Vivado not found in D:\Xilinx\2025.1\Vivado\bin or PATH!
        exit /b 1
    )
)

call "%VIVADO_BIN%" -mode batch -source generate_flash_image.tcl -notrace
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Flash image generation failed!
    exit /b 1
)

rem Move Vivado logs to vivado directory
if exist vivado*.log move /y vivado*.log vivado\ >nul
if exist vivado*.jou move /y vivado*.jou vivado\ >nul

echo.
echo [SUCCESS] Flash images generated:
echo   - top_basys3_picorv32_rdm6300_flash.bin
echo   - top_basys3_picorv32_rdm6300_flash.mcs
exit /b 0
