## Basys3 constraint template for future top module integration.
## Keep this file as reference until top.v and final port list are ready.

## Clock 100MHz
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property -dict { PACKAGE_PIN W5   IOSTANDARD LVCMOS33 } [get_ports clk]
create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports clk]

## UART TX to PC via onboard USB-UART bridge (Putty reads this line)
set_property -dict { PACKAGE_PIN A18 IOSTANDARD LVCMOS33 } [get_ports uart_tx_o]

## RDM6300 TX -> FPGA RX on JA1 (J1)
## PULLUP required: UART idle = HIGH; without pullup the floating pin is read as permanent start-bit (all-zeros spam)
set_property -dict { PACKAGE_PIN J1 IOSTANDARD LVCMOS33 PULLUP TRUE } [get_ports rdm6300_rx_i]
