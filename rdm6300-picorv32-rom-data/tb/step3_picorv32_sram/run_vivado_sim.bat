@echo off
rem ======================================================================
rem  Vivado Batch Simulation for Step 3: 1KB Data SRAM
rem  Uses AMD Vivado Simulator (xvlog + xelab + xsim)
rem ======================================================================
echo.
echo ======================================================================
echo   Running Step 3 Simulation in AMD Vivado Simulator (xsim)
echo ======================================================================
echo.

set "VIVADO_BIN=C:\AMDDesignTools\2025.2\Vivado\bin"
if not exist "%VIVADO_BIN%\xvlog.bat" (
    where xvlog >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Vivado toolchain not found in PATH or %VIVADO_BIN%!
        exit /b 1
    )
) else (
    set "PATH=%VIVADO_BIN%;%PATH%"
)

echo [1/3] Compiling Verilog RTL and Testbench with xvlog...
call xvlog -i ../../rtl ../../rtl/data_sram.v tb_data_sram.v
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo [2/3] Elaborating design with xelab...
call xelab -debug typical tb_data_sram -s tb_data_sram_sim
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo [3/3] Running simulation in xsim...
call xsim tb_data_sram_sim -R
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo.
echo [4/4] Moving generated simulation artifacts to temp/ folder...
if not exist "temp" mkdir temp
move /y *.log temp\ >nul 2>nul
move /y *.pb temp\ >nul 2>nul
move /y *.jou temp\ >nul 2>nul
move /y *.wdb temp\ >nul 2>nul
move /y dfx_runtime.txt temp\ >nul 2>nul
if exist "xsim.dir" (
    if exist "temp\xsim.dir" rmdir /s /q temp\xsim.dir >nul 2>nul
    move xsim.dir temp\ >nul 2>nul
)

echo.
echo [SUCCESS] Step 3 Vivado Simulation finished successfully!
exit /b 0
