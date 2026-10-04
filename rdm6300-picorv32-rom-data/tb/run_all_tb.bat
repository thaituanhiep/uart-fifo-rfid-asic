@echo off
rem ======================================================================
rem  Master Testbench Runner for PicoRV32 RFID SoC
rem  Runs:
rem    1. tb_uart_rtl  (Pure RTL verification of uart_mmio)
rem    2. tb_uart_ping (Full SoC CPU Boot from SPI Flash + Ping-Pong)
rem ======================================================================
echo.
echo ======================================================================
echo   Executing Master Test Suite (tb_uart_rtl + tb_uart_ping)
echo ======================================================================
echo.

echo [1/2] Running tb_uart_rtl...
call run_sim_uart.bat
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] tb_uart_rtl failed with code %ERRORLEVEL%!
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Running tb_uart_ping...
call run_sim_ping.bat
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] tb_uart_ping failed with code %ERRORLEVEL%!
    exit /b %ERRORLEVEL%
)

echo.
echo ======================================================================
echo   [ALL TESTS PASSED] tb_uart_rtl and tb_uart_ping executed successfully!
echo ======================================================================
exit /b 0
