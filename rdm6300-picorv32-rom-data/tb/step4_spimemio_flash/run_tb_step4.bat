@echo off
rem ==============================================================================
rem Testbench Runner for Step 4: SPI Flash Controller (spimemio.v)
rem ==============================================================================
echo ======================================================================
echo   Step 4: SPI Flash Controller (spimemio.v) Testbench Runner
echo ======================================================================

echo.
echo [1/1] Running Automated Verification Testbench...
py test_spimemio.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Step 4 testbench failed!
    exit /b 1
)

echo.
echo [PASSED] Step 4 tests completed successfully with 100%% PASS!
exit /b 0
