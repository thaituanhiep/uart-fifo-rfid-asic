/* Startup assembly for PicoRV32 */
.section .text.start
.global _start

_start:
    /* Initialize stack pointer to top of 8KB SRAM */
    lui sp, %hi(_stack_top)
    addi sp, sp, %lo(_stack_top)

    /* Zero BSS section */
    la a0, __bss_start
    la a1, __bss_end
zero_bss_loop:
    bge a0, a1, bss_done
    sw zero, 0(a0)
    addi a0, a0, 4
    j zero_bss_loop
bss_done:

    /* Call main() */
    call main

    /* Trap/Hang loop if main returns */
hang:
    j hang
