/* Startup assembly for PicoRV32: XIP SPI Flash + 1KB Data SRAM */
.section .text.start
.global _start

_start:
    /* 1. Initialize stack pointer to top of 1KB Data SRAM (0x00000400) */
    lui sp, %hi(_stack_top)
    addi sp, sp, %lo(_stack_top)

    /* 2. Copy .data section from Flash to Data SRAM */
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

/* ----------------------------------------------------------------------------
 * flashio_worker: Executed from SRAM to send raw SPI Flash commands
 * (Erase, Program, Read SR/ID) while spimemio XIP is temporarily disabled.
 * ---------------------------------------------------------------------------- */
.global flashio_worker_begin
.global flashio_worker_end

.balign 4

flashio_worker_begin:
    # a0 ... data pointer
    # a1 ... data length
    # a2 ... optional WREN cmd (0 = disable)

    # address of SPI ctrl reg (0x02000000)
    li   t0, 0x02000000

    # Set CS high, IO0 is output
    li   t1, 0x120
    sh   t1, 0(t0)

    # Enable Manual SPI Ctrl
    sb   zero, 3(t0)

    # Send optional WREN cmd
    beqz a2, flashio_worker_L1
    li   t5, 8
    andi t2, a2, 0xff
flashio_worker_L4:
    srli t4, t2, 7
    sb   t4, 0(t0)
    ori  t4, t4, 0x10
    sb   t4, 0(t0)
    slli t2, t2, 1
    andi t2, t2, 0xff
    addi t5, t5, -1
    bnez t5, flashio_worker_L4
    sb   t1, 0(t0)

    # SPI transfer
flashio_worker_L1:
    beqz a1, flashio_worker_L3
    li   t5, 8
    lbu  t2, 0(a0)
flashio_worker_L2:
    srli t4, t2, 7
    sb   t4, 0(t0)
    ori  t4, t4, 0x10
    sb   t4, 0(t0)
    lbu  t4, 0(t0)
    andi t4, t4, 2
    srli t4, t4, 1
    slli t2, t2, 1
    or   t2, t2, t4
    andi t2, t2, 0xff
    addi t5, t5, -1
    bnez t5, flashio_worker_L2
    sb   t2, 0(a0)
    addi a0, a0, 1
    addi a1, a1, -1
    j    flashio_worker_L1
flashio_worker_L3:
    # Set CS high (commits write/erase command, deselects chip)
    li   t1, 0x120
    sh   t1, 0(t0)

    # If no WREN command was sent (a2 == 0), no write/erase in progress
    beqz a2, flashio_worker_done

flashio_worker_wait_wip:
    # Pull CS low, send RDSR (0x05)
    li   t2, 0x05
    li   t5, 8
flashio_worker_rdsr_cmd:
    srli t4, t2, 7
    sb   t4, 0(t0)
    ori  t4, t4, 0x10
    sb   t4, 0(t0)
    slli t2, t2, 1
    andi t2, t2, 0xff
    addi t5, t5, -1
    bnez t5, flashio_worker_rdsr_cmd

    # Read status register byte (8 bits)
    li   t5, 8
    li   t2, 0
flashio_worker_rdsr_rx:
    sb   zero, 0(t0)
    ori  t4, zero, 0x10
    sb   t4, 0(t0)
    lbu  t4, 0(t0)
    andi t4, t4, 2
    srli t4, t4, 1
    slli t2, t2, 1
    or   t2, t2, t4
    addi t5, t5, -1
    bnez t5, flashio_worker_rdsr_rx

    # Set CS high
    li   t1, 0x120
    sh   t1, 0(t0)

    # Check WIP bit (bit 0 of status register)
    andi t2, t2, 1
    bnez t2, flashio_worker_wait_wip

flashio_worker_done:
    # Back to MEMIO mode (0x80 written to byte 3 of 0x02000000)
    li   t1, 0x80
    sb   t1, 3(t0)

    ret

.balign 4
flashio_worker_end:

