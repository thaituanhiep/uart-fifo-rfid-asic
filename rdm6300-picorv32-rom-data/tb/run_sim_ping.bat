@echo off
rem ======================================================================
rem  Vivado Simulator Runner for tb_uart_ping (Full PicoRV32 SoC)
rem ======================================================================
echo.
echo ======================================================================
echo   Running tb_uart_ping Simulation in AMD Vivado Simulator (xsim)
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

echo [1/3] Compiling RTL and tb_uart_ping.v with xvlog...
call xvlog -i ../rtl ^
    ../rtl/uart/sync_2ff.v ^
    ../rtl/core/spimemio.v ^
    ../rtl/core/data_sram.v ^
    ../rtl/core/soc_gpio_mmio.v ^
    ../rtl/core/picorv32.v ^
    ../rtl/core/soc_interconnect.v ^
    ../rtl/uart/sync_fifo.v ^
    ../rtl/uart/simpleuart.v ^
    ../rtl/uart/simpleuart_fifo.v ^
    ../rtl/uart/uart_mmio.v ^
    ../rtl/rdm6300_picorv32_soc.v ^
    tb_uart_ping.v
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo [2/3] Elaborating design with xelab...
call xelab -debug typical tb_uart_ping -s tb_ping_sim
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo [3/3] Running simulation with xsim...
call xsim tb_ping_sim -R
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

rem Clean simulation artifacts
if not exist "temp" mkdir temp
move /y *.log temp\ >nul 2>nul
move /y *.pb temp\ >nul 2>nul
move /y *.jou temp\ >nul 2>nul
move /y *.wdb temp\ >nul 2>nul
if exist "xsim.dir" (
    if exist "temp\xsim.dir" rmdir /s /q temp\xsim.dir >nul 2>nul
    move xsim.dir temp\ >nul 2>nul
)

echo.
echo [SUCCESS] tb_uart_ping finished successfully!
exit /b 0
