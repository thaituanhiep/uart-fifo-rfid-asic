@echo off
rem ==============================================================================
rem Build & Execute Firmware Unit & Protocol Testbench (Step 2)
rem ==============================================================================
echo ======================================================================
echo   Step 2: Firmware and Protocol Testbench Runner
echo ======================================================================

set "GCC_BIN=D:\Xilinx\2025.1\tps\mingw\10.0.0\win64.o\nt\bin\gcc.exe"
if not exist "%GCC_BIN%" set "GCC_BIN=D:\Xilinx\2025.1\tps\win64\msys64\mingw64\bin\gcc.exe"
if not exist "%GCC_BIN%" set "GCC_BIN=C:\AMDDesignTools\2025.2\tps\mingw\10.0.0\win64.o\nt\bin\gcc.exe"
if exist "%GCC_BIN%" (
    echo [INFO] Compiling tb_firmware.c using MinGW GCC...
    "%GCC_BIN%" -O2 -Wall -Wextra tb_firmware.c -o tb_firmware.exe 2>nul
    if exist tb_firmware.exe (
        echo [INFO] tb_firmware.exe compiled successfully.
    )
)

echo.
echo ======================================================================
echo   Executing 21 Automated Test Cases via Python Test Harness...
echo ======================================================================
py test_firmware.py
if %ERRORLEVEL% neq 0 (
    echo [FAILED] Some test cases in tb_firmware failed!
    exit /b 1
)

echo.
echo [PASSED] Firmware testbench completed with 100%% success!
exit /b 0
