# Makefile for PicoRV32 Firmware (No Python required)
CROSS ?= riscv64-unknown-elf-
CC = $(CROSS)gcc
OBJCOPY = $(CROSS)objcopy

CFLAGS = -march=rv32i -mabi=ilp32 -O2 -ffreestanding -nostdlib -Wall -Wextra

all: firmware.hex

firmware.elf: start.s main.c sections.lds
	$(CC) $(CFLAGS) -Wl,-Bstatic,-T,sections.lds,--strip-debug -o $@ start.s main.c

# Direct GNU toolchain export to Verilog memory hex format (no Python needed)
firmware.hex: firmware.elf
	$(OBJCOPY) -O verilog --verilog-data-width=4 $< $@

clean:
	rm -f firmware.elf firmware.bin firmware.hex
