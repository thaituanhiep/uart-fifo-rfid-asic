/* Linker script for PicoRV32 8KB SRAM SoC */
MEMORY {
    RAM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x2000 /* 8 KBytes */
}

SECTIONS {
    .text : {
        . = 0x00000000;
        *(.text.start)
        *(.text*)
        *(.rodata*)
        . = ALIGN(4);
    } > RAM

    .data : {
        *(.data*)
        . = ALIGN(4);
    } > RAM

    .bss : {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end = .;
    } > RAM

    _stack_top = 0x00002000;

    /DISCARD/ : {
        *(.note*)
        *(.comment)
        *(.eh_frame)
    }
}
