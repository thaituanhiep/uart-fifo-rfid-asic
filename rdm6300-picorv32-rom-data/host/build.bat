@echo off
rem Build script for Host PC C program (rdm6300_manager.exe)
echo ========================================================
echo   Compiling Host PC C Console Application (Windows)
echo ========================================================

set "XILINX_MINGW=D:\Xilinx\2025.1\tps\win64\msys64\mingw64\bin"
if exist "%XILINX_MINGW%\gcc.exe" (
    set "PATH=%XILINX_MINGW%;%PATH%"
)

where gcc >nul 2>nul
if %ERRORLEVEL% equ 0 (
    gcc -O2 -Wall main.c -o rdm6300_manager.exe
    if %ERRORLEVEL% equ 0 (
        echo [SUCCESS] Compiled rdm6300_manager.exe successfully using GCC!
        echo You can now run:
        echo   rdm6300_manager.exe
        exit /b 0
    )
)

where cl >nul 2>nul
if %ERRORLEVEL% equ 0 (
    cl /O2 /Fe:rdm6300_manager.exe main.c
    if %ERRORLEVEL% equ 0 (
        echo [SUCCESS] Compiled rdm6300_manager.exe successfully using MSVC!
        exit /b 0
    )
)

echo [ERROR] No C compiler found!
exit /b 1
