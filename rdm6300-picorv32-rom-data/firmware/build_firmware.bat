@echo off
rem Build script for PicoRV32 Firmware (Pure GNU Toolchain - No Python required)
echo ========================================================
echo   Compiling PicoRV32 C Firmware to Verilog HEX
echo ========================================================

set "XILINX_RISCV=C:\AMDDesignTools\2025.2\gnu\riscv\nt\bin"
if exist "%XILINX_RISCV%\riscv64-unknown-elf-gcc.exe" (
    set "PATH=%XILINX_RISCV%;%PATH%"
    set "CROSS=riscv64-unknown-elf-"
    goto :compile
)

set "XILINX_RISCV_OLD=D:\Xilinx\2025.1\gnu\riscv\nt\riscv64-unknown-elf\bin"
if exist "%XILINX_RISCV_OLD%\riscv64-unknown-elf-gcc.exe" (
    set "PATH=%XILINX_RISCV_OLD%;%PATH%"
    set "CROSS=riscv64-unknown-elf-"
    goto :compile
)

where riscv32-unknown-elf-gcc >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "CROSS=riscv32-unknown-elf-"
    goto :compile
)

where riscv64-unknown-elf-gcc >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "CROSS=riscv64-unknown-elf-"
    goto :compile
)

echo [ERROR] No RISC-V GCC toolchain found!
exit /b 1

:compile
echo Using toolchain: %CROSS%gcc

%CROSS%gcc -march=rv32i -mabi=ilp32 -Os -ffreestanding -nostdlib -Wl,-Bstatic,-T,sections.lds,--strip-debug -o firmware.elf start.s main.c
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Compilation failed!
    exit /b 1
)

%CROSS%objcopy -O binary firmware.elf firmware.bin
if %ERRORLEVEL% neq 0 (
    echo [ERROR] objcopy to bin failed!
    exit /b 1
)

py bin2hex.py firmware.bin firmware.hex
if %ERRORLEVEL% neq 0 (
    echo [ERROR] bin2hex conversion failed!
    exit /b 1
)

copy /y firmware.hex ..\rtl\firmware.hex >nul
copy /y firmware.hex ..\fpga\rtl\firmware.hex >nul
copy /y firmware.hex ..\tb\firmware.hex >nul
copy /y firmware.hex ..\tb\step6_top_soc_integration\firmware.hex >nul

echo [SUCCESS] firmware.hex generated and copied to rtl/, fpga/rtl/, and tb/ successfully!
exit /b 0
