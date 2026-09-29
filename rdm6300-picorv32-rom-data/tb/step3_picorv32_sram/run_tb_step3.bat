@echo off
rem ==============================================================================
rem Testbench Runner for Step 3: PicoRV32 Core & 1KB Data SRAM
rem ==============================================================================
echo ======================================================================
echo   Step 3: PicoRV32 & 1KB Data SRAM Testbench
echo ======================================================================

echo.
echo [1/1] Running Automated Verification Testbench...
py test_picorv32_sram.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Step 3 testbench failed!
    exit /b 1
)

echo.
echo [PASSED] Step 3 tests completed successfully with 100%% PASS!
exit /b 0
