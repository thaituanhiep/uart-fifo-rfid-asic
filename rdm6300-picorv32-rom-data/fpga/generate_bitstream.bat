@echo off
rem Batch script to run Vivado in batch mode and generate Bitstream for Basys 3
echo ========================================================
echo   Building Basys 3 Bitstream with Vivado
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

call "%VIVADO_BIN%" -mode batch -source build_vivado_basys3.tcl -notrace
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Vivado bitstream generation failed!
    exit /b 1
)

echo.
echo [SUCCESS] Bitstream generated: top_basys3_picorv32_rdm6300.bit
echo You can now program the Basys 3 board using Vivado Hardware Manager.
exit /b 0
