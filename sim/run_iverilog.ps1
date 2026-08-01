$ErrorActionPreference = 'Stop'

Set-Location $PSScriptRoot

iverilog -g2005-sv -o tb_uart_fifo_core.vvp `
    ../rtl/fifo_sync.v `
    ../rtl/uart_rx.v `
    ../rtl/uart_tx.v `
    ../rtl/uart_fifo_core.v `
    tb_uart_fifo_core.v

vvp tb_uart_fifo_core.vvp
