/* Linker script for PicoRV32: XIP SPI Flash (0x00250000) + 1KB Data SRAM (0x00000000) */
MEMORY {
    FLASH (rx) : ORIGIN = 0x00250000, LENGTH = 0x000B0000 /* 704 KB Flash (0x0025_0000 - 0x002F_FFFF) */
    RAM (rwx)  : ORIGIN = 0x00000000, LENGTH = 0x00000400 /* 1 KByte Data SRAM (0x0000_0000 - 0x0000_03FF) */
}

SECTIONS {
    .text : {
        . = ALIGN(4);
        *(.text.start)
        *(.text*)
        *(.rodata*)
        *(.srodata*)
        . = ALIGN(4);
        _etext = .;
    } > FLASH

    /* .data is loaded into FLASH (LMA), but accessed in RAM (VMA) */
    .data : {
        . = ALIGN(4);
        __data_start = .;
        *(.data*)
        *(.sdata*)
        . = ALIGN(4);
        __data_end = .;
    } > RAM AT > FLASH
    __data_load = LOADADDR(.data);

    .bss : {
        . = ALIGN(4);
        __bss_start = .;
        *(.bss*)
        *(.sbss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end = .;
    } > RAM

    _stack_top = 0x00000400; /* Top of 1KB SRAM (0x0000_0000 + 0x0400) */

    /DISCARD/ : {
        *(.note*)
        *(.comment)
        *(.eh_frame)
    }
}

