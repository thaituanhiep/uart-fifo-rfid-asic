## ============================================================================
## File: basys3_picorv32_rdm6300.xdc
## Project: rdm6300-picorv32-rom-data
## Target: Digilent Basys 3 (AMD Xilinx Artix-7 XC7A35T-CPG236-1)
## Description: Physical & Timing Constraints for PicoRV32 SoC with RFID & Flash
## ============================================================================

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]

## ----------------------------------------------------------------------------
## 100 MHz Clock (W5)
## ----------------------------------------------------------------------------
set_property -dict { PACKAGE_PIN W5   IOSTANDARD LVCMOS33 } [get_ports clk]
create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports clk]

## ----------------------------------------------------------------------------
## Center Pushbutton (Reset)
## ----------------------------------------------------------------------------
set_property -dict { PACKAGE_PIN U18  IOSTANDARD LVCMOS33 } [get_ports btnC]

## ----------------------------------------------------------------------------
## RDM6300 RFID UART RX (PMOD Header JA1 - Pin J1)
## PULLUP is strictly required to prevent floating UART line false start-bits
## ----------------------------------------------------------------------------
set_property -dict { PACKAGE_PIN J1   IOSTANDARD LVCMOS33 PULLUP TRUE } [get_ports rdm6300_rx_i]

## ----------------------------------------------------------------------------
## Onboard USB-UART Bridge to PC (FTDI)
## ----------------------------------------------------------------------------
set_property -dict { PACKAGE_PIN A18  IOSTANDARD LVCMOS33 } [get_ports uart_tx_o]
set_property -dict { PACKAGE_PIN B18  IOSTANDARD LVCMOS33 } [get_ports uart_rx_i]

## ----------------------------------------------------------------------------
## Spansion S25FL032P QSPI Flash Memory
## ----------------------------------------------------------------------------
set_property -dict { PACKAGE_PIN K19  IOSTANDARD LVCMOS33 } [get_ports qspi_cs]
set_property -dict { PACKAGE_PIN D18  IOSTANDARD LVCMOS33 } [get_ports {qspi_dq[0]}]
set_property -dict { PACKAGE_PIN D19  IOSTANDARD LVCMOS33 } [get_ports {qspi_dq[1]}]
set_property -dict { PACKAGE_PIN G18  IOSTANDARD LVCMOS33 } [get_ports {qspi_dq[2]}]
set_property -dict { PACKAGE_PIN F18  IOSTANDARD LVCMOS33 } [get_ports {qspi_dq[3]}]

## ----------------------------------------------------------------------------
## 16 Status LEDs on Basys 3
## ----------------------------------------------------------------------------
set_property -dict { PACKAGE_PIN U16  IOSTANDARD LVCMOS33 } [get_ports {led[0]}]
set_property -dict { PACKAGE_PIN E19  IOSTANDARD LVCMOS33 } [get_ports {led[1]}]
set_property -dict { PACKAGE_PIN U19  IOSTANDARD LVCMOS33 } [get_ports {led[2]}]
set_property -dict { PACKAGE_PIN V19  IOSTANDARD LVCMOS33 } [get_ports {led[3]}]
set_property -dict { PACKAGE_PIN W18  IOSTANDARD LVCMOS33 } [get_ports {led[4]}]
set_property -dict { PACKAGE_PIN U15  IOSTANDARD LVCMOS33 } [get_ports {led[5]}]
set_property -dict { PACKAGE_PIN U14  IOSTANDARD LVCMOS33 } [get_ports {led[6]}]
set_property -dict { PACKAGE_PIN V14  IOSTANDARD LVCMOS33 } [get_ports {led[7]}]
set_property -dict { PACKAGE_PIN V13  IOSTANDARD LVCMOS33 } [get_ports {led[8]}]
set_property -dict { PACKAGE_PIN V3   IOSTANDARD LVCMOS33 } [get_ports {led[9]}]
set_property -dict { PACKAGE_PIN W3   IOSTANDARD LVCMOS33 } [get_ports {led[10]}]
set_property -dict { PACKAGE_PIN U3   IOSTANDARD LVCMOS33 } [get_ports {led[11]}]
set_property -dict { PACKAGE_PIN P3   IOSTANDARD LVCMOS33 } [get_ports {led[12]}]
set_property -dict { PACKAGE_PIN N3   IOSTANDARD LVCMOS33 } [get_ports {led[13]}]
set_property -dict { PACKAGE_PIN P1   IOSTANDARD LVCMOS33 } [get_ports {led[14]}]
set_property -dict { PACKAGE_PIN L1   IOSTANDARD LVCMOS33 } [get_ports {led[15]}]
