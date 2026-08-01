set ::env(DESIGN_NAME) uart_fifo_core

set ::env(VERILOG_FILES) [glob $::env(DESIGN_DIR)/../../rtl/*.v]

set ::env(CLOCK_PORT) clk
set ::env(CLOCK_PERIOD) 20.0

# Floorplan defaults kept modest for a small digital block.
set ::env(FP_CORE_UTIL) 35
set ::env(PL_TARGET_DENSITY) 0.50

# This is a block-level netlist target (no padframe/top-level IO ring yet).
set ::env(DIODE_INSERTION_STRATEGY) 4
