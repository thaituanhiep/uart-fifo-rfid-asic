@echo off
rem Batch script to program Basys 3 SPI Flash using Vivado Hardware Manager
echo ========================================================
echo   Programming Basys 3 SPI Flash Memory (Bitstream + FW)
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

call "%VIVADO_BIN%" -mode batch -source program_flash.tcl -notrace
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Programming SPI Flash failed!
    echo Make sure Basys 3 is connected via USB and powered on.
    exit /b 1
)

rem Move Vivado logs to vivado directory
if exist vivado*.log move /y vivado*.log vivado\ >nul
if exist vivado*.jou move /y vivado*.jou vivado\ >nul

echo [SUCCESS] Flash programming completed!
exit /b 0
