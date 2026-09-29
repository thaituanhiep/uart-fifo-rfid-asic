@echo off
rem ======================================================================
rem  Master 1-Click Verification Batch Runner for PicoRV32 RFID SoC
rem  Runs Steps 2 -> 3 -> 4 -> 5 -> 6 Sequentially
rem ======================================================================
echo.
echo ======================================================================
echo   Executing Master Test Suite (All Steps 2, 3, 4, 5, 6)
echo ======================================================================
echo.

py run_all_testbenches.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Test Suite failed with error code %ERRORLEVEL%!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] All testbenches executed successfully!
exit /b 0
