@echo off
rem ======================================================================
rem  Batch runner for Step 6: Full PicoRV32 RFID SoC Integration Testbench
rem ======================================================================
echo.
echo ======================================================================
echo   Running Step 6: Full SoC Integration Testbench
echo ======================================================================
echo.

py test_top_soc.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Step 6 Integration Testbench failed with error code %ERRORLEVEL%!
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] Step 6 Testbench execution completed successfully!
exit /b 0
