@echo off
rem ==============================================================================
rem Testbench Runner for Step 5: RDM6300 5-Stage Autonomous Pipeline
rem ==============================================================================
echo ======================================================================
echo   Step 5: RDM6300 5-Stage Autonomous Pipeline Testbench Runner
echo ======================================================================

echo.
echo [1/1] Running Automated Verification Testbench...
py test_rdm6300_pipeline.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Step 5 testbench failed!
    exit /b 1
)

echo.
echo [PASSED] Step 5 tests completed successfully with 100%% PASS!
exit /b 0
