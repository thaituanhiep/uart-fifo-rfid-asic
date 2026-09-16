@echo off
rem Batch script to program Basys 3 FPGA using Vivado Hardware Manager
echo ========================================================
echo   Programming Basys 3 FPGA via USB JTAG
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

call "%VIVADO_BIN%" -mode batch -source program_basys3.tcl -notrace
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Programming Basys 3 failed!
    echo Make sure Basys 3 is connected to PC and powered on.
    exit /b 1
)

echo [SUCCESS] Done!
exit /b 0
