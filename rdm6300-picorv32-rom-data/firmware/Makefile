# Makefile for PicoRV32 Firmware (No Python required)
CROSS ?= riscv64-unknown-elf-
CC = $(CROSS)gcc
OBJCOPY = $(CROSS)objcopy

CFLAGS = -march=rv32i -mabi=ilp32 -Os -ffreestanding -nostdlib -Wall -Wextra \
         -I. -Icommon -Idrivers -Iprotocol -Iapp

SRCS = start.s main.c \
       common/hex_utils.c \
       drivers/uart.c \
       drivers/flash.c \
       protocol/rdm6300_parser.c \
       app/access_control.c

all: firmware.bin firmware.hex

firmware.elf: $(SRCS) sections.lds
	$(CC) $(CFLAGS) -Wl,-Bstatic,-T,sections.lds,--strip-debug -o $@ $(SRCS)

firmware.bin: firmware.elf
	$(OBJCOPY) -O binary $< $@

# Direct GNU toolchain export to Verilog memory hex format (no Python needed)
firmware.hex: firmware.elf
	$(OBJCOPY) -O verilog --verilog-data-width=4 $< $@

clean:
	rm -f firmware.elf firmware.bin firmware.hex
