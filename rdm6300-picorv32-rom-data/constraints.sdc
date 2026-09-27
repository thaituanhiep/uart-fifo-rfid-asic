###############################################################################
# Timing Constraints for rdm6300_picorv32_soc
# Target PDK: Sky130A (sky130_fd_sc_hd)
###############################################################################
current_design rdm6300_picorv32_soc

# -----------------------------------------------------------------------------
# Clock Definition
# -----------------------------------------------------------------------------
create_clock -name clk -period 20.0000 [get_ports {clk}]
set_clock_transition 0.1500 [get_clocks {clk}]
set_clock_uncertainty 0.2500 [get_clocks {clk}]
set_propagated_clock [get_clocks {clk}]

# -----------------------------------------------------------------------------
# Asynchronous Inputs (CDC Synchronized internally via sync_2ff or Async Reset)
# Eliminates false hold violations at 100°C slow corner
# -----------------------------------------------------------------------------
set_false_path -from [get_ports {rst_n rdm6300_rx_i uart_rx_i}]

# -----------------------------------------------------------------------------
# Asynchronous / Static Outputs (LEDs & Status Flags)
# -----------------------------------------------------------------------------
set_false_path -to [get_ports {leds_o[*] card_event_o cpu_trap flash_busy_o flash_done_o}]

# -----------------------------------------------------------------------------
# Synchronous QSPI Flash Interface
# -----------------------------------------------------------------------------
set_input_delay 4.0000 -clock [get_clocks {clk}] [get_ports {flash_io0_di flash_io1_di flash_io2_di flash_io3_di}]
set_output_delay 2.0000 -clock [get_clocks {clk}] [get_ports {flash_csb flash_clk flash_io0_do flash_io1_do flash_io2_do flash_io3_do flash_io0_oe flash_io1_oe flash_io2_oe flash_io3_oe}]

# -----------------------------------------------------------------------------
# Host PC UART Output
# -----------------------------------------------------------------------------
set_output_delay 2.0000 -clock [get_clocks {clk}] [get_ports {uart_tx_o}]

# -----------------------------------------------------------------------------
# Environment & Driving Cell
# -----------------------------------------------------------------------------
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} [all_inputs]
set_load -pin_load 0.0334 [all_outputs]

# -----------------------------------------------------------------------------
# Design Rules
# -----------------------------------------------------------------------------
set_max_transition 0.7500 [current_design]
set_max_capacitance 0.2000 [current_design]
set_max_fanout 16.0000 [current_design]
