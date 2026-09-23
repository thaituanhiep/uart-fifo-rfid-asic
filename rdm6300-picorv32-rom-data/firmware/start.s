/* Startup assembly for PicoRV32 with Mask ROM & Data SRAM */
.section .text.start
.global _start

_start:
    /* 1. Initialize stack pointer to top of 1KB Data SRAM (0x00010400) */
    lui sp, %hi(_stack_top)
    addi sp, sp, %lo(_stack_top)

    /* 2. Copy .data section from Mask ROM to Data SRAM */
    la a0, __data_start
    la a1, __data_end
    la a2, __data_load
copy_data_loop:
    bge a0, a1, copy_data_done
    lw t0, 0(a2)
    sw t0, 0(a0)
    addi a0, a0, 4
    addi a2, a2, 4
    j copy_data_loop
copy_data_done:

    /* 3. Zero BSS section in Data SRAM */
    la a0, __bss_start
    la a1, __bss_end
zero_bss_loop:
    bge a0, a1, bss_done
    sw zero, 0(a0)
    addi a0, a0, 4
    j zero_bss_loop
bss_done:

    /* 4. Call C main() */
    call main

    /* 5. Trap/Hang loop if main returns */
hang:
    j hang
