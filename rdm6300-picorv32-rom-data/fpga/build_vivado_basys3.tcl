# ==============================================================================
# Vivado TCL Build Script for PicoRV32 + RDM6300 + SPI Flash on Basys 3
# Target: Digilent Basys 3 (XC7A35T-CPG236-1)
# ==============================================================================

set proj_dir [file dirname [info script]]
set root_dir [file normalize "$proj_dir/.."]

puts "======================================================================"
puts "  Starting Vivado Synthesis & Bitstream Generation for Basys 3"
puts "  Root directory: $root_dir"
puts "======================================================================"

# 1. Create In-Memory Project
create_project -in_memory -part xc7a35tcpg236-1

# 2. Add Verilog RTL Source Files
read_verilog [list \
    "$root_dir/rtl/sync_2ff.v" \
    "$root_dir/rtl/uart_rx.v" \
    "$root_dir/rtl/rdm6300_frame_decoder.v" \
    "$root_dir/rtl/simpleuart.v" \
    "$root_dir/rtl/spi_flash_controller.v" \
    "$root_dir/rtl/mask_rom.v" \
    "$root_dir/rtl/data_sram.v" \
    "$root_dir/rtl/picorv32.v" \
    "$root_dir/rtl/rdm6300_picorv32_soc.v" \
    "$root_dir/fpga/rtl/top_basys3_picorv32_rdm6300.v" \
]

# 3. Add Memory Initialization (.hex)
read_mem [list "$root_dir/rtl/firmware.hex"]

# 4. Add Constraints File (XDC)
read_xdc "$root_dir/fpga/constraints/basys3_picorv32_rdm6300.xdc"

# 5. Synthesis
puts "\n=== STEP 1/4: Running Synthesis ==="
synth_design -top top_basys3_picorv32_rdm6300 -part xc7a35tcpg236-1 -flatten_hierarchy rebuilt

# 6. Optimization & Placement
puts "\n=== STEP 2/4: Running Optimization & Placement ==="
opt_design
place_design

# 7. Routing
puts "\n=== STEP 3/4: Running Routing ==="
route_design
report_timing_summary -file "$proj_dir/timing_summary.rpt"

# 8. Bitstream Generation
puts "\n=== STEP 4/4: Generating Bitstream ==="
set output_bit "$proj_dir/top_basys3_picorv32_rdm6300.bit"
write_bitstream -force $output_bit

puts "\n======================================================================"
puts "  BITSTREAM GENERATION COMPLETED SUCCESSFULLY!"
puts "  Output file: $output_bit"
puts "======================================================================"
exit
