@echo off
rem ======================================================================
rem  Vivado Batch Simulation for Step 5: RDM6300 5-Stage Hardware Pipeline
rem  Uses AMD Vivado Simulator (xvlog + xelab + xsim)
rem ======================================================================
echo.
echo ======================================================================
echo   Running Step 5 Simulation in AMD Vivado Simulator (xsim)
echo ======================================================================
echo.

set "VIVADO_BIN=D:\Xilinx\2025.1\Vivado\bin"
if not exist "%VIVADO_BIN%\xvlog.bat" set "VIVADO_BIN=C:\AMDDesignTools\2025.2\Vivado\bin"
if exist "%VIVADO_BIN%\xvlog.bat" (
    set "PATH=%VIVADO_BIN%;%PATH%"
) else (
    where xvlog >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Vivado toolchain not found in PATH or %VIVADO_BIN%!
        exit /b 1
    )
)

echo [1/3] Compiling Verilog RTL and Testbench with xvlog...
call xvlog -i ../../rtl ../../rtl/core/sync_2ff.v ../../rtl/rdm6300/uart_rx.v ../../rtl/host/sync_fifo.v ../../rtl/rdm6300/rdm6300_frame_decoder.v tb_rdm6300_pipeline.v
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo [2/3] Elaborating design with xelab...
call xelab -debug typical tb_rdm6300_pipeline -s tb_pipeline_sim
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo [3/3] Running simulation in xsim...
call xsim tb_pipeline_sim -R
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
echo [SUCCESS] Step 5 Vivado Simulation finished successfully!
exit /b 0
