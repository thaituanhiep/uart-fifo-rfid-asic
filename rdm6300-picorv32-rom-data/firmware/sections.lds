/* Linker script for PicoRV32: 8KB Mask ROM + 2KB Data SRAM */
MEMORY {
    ROM (rx)  : ORIGIN = 0x00000000, LENGTH = 0x2000 /* 8 KBytes Mask ROM */
    RAM (rwx) : ORIGIN = 0x00010000, LENGTH = 0x0400 /* 1 KByte Data SRAM */
}

SECTIONS {
    .text : {
        . = 0x00000000;
        *(.text.start)
        *(.text*)
        *(.rodata*)
        . = ALIGN(4);
    } > ROM

    /* .data is loaded into ROM (LMA), but accessed in RAM (VMA) */
    .data : {
        __data_start = .;
        *(.data*)
        . = ALIGN(4);
        __data_end = .;
    } > RAM AT > ROM
    __data_load = LOADADDR(.data);

    .bss : {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end = .;
    } > RAM

    _stack_top = 0x00010400; /* Top of 1KB SRAM (0x00010000 + 0x0400) */

    /DISCARD/ : {
        *(.note*)
        *(.comment)
        *(.eh_frame)
    }
}
