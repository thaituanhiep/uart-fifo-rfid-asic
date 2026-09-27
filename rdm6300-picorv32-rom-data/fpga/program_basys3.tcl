# ==============================================================================
# Vivado TCL Script: Program Basys 3 FPGA via USB JTAG
# ==============================================================================

set bitfile [file normalize "top_basys3_picorv32_rdm6300.bit"]
if {![file exists $bitfile]} {
    puts "ERROR: Bitstream file $bitfile does not exist! Please generate bitstream first."
    exit 1
}

open_hw_manager
connect_hw_server -allow_non_jtag
open_hw_target

set dev [lindex [get_hw_devices] 0]
if {$dev == ""} {
    puts "ERROR: No JTAG device found! Please check Basys 3 USB connection."
    exit 1
}
current_hw_device $dev
refresh_hw_device -update_hw_probes false $dev

set_property PROGRAM.FILE $bitfile $dev
puts "Programming device with $bitfile..."
program_hw_devices $dev
refresh_hw_device $dev

puts "======================================================================"
puts "  SUCCESS: Basys 3 FPGA Programmed Successfully!"
puts "======================================================================"
exit 0
