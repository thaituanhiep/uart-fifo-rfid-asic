# ==============================================================================
# Vivado TCL Script: Program Basys 3 Onboard SPI Flash (Spansion S25FL032P)
# Writes both FPGA Bitstream (at 0x0) and PicoRV32 Firmware (at 0x250000)
# ==============================================================================

set binfile [file normalize "top_basys3_picorv32_rdm6300_flash.bin"]
if {![file exists $binfile]} {
    puts "ERROR: Flash image $binfile not found! Please run generate_flash_image.bat first."
    exit 1
}

open_hw_manager
connect_hw_server -allow_non_jtag
open_hw_target

set dev [lindex [get_hw_devices] 0]
if {$dev == ""} {
    puts "ERROR: No JTAG device found! Please check Basys 3 USB connection and power."
    exit 1
}
current_hw_device $dev
refresh_hw_device -update_hw_probes false $dev

set existing_cfgmem [get_property -quiet PROGRAM.HW_CFGMEM $dev]
if {$existing_cfgmem != ""} {
    delete_hw_cfgmem $existing_cfgmem
}

set mem_part [lindex [get_cfgmem_parts {mx25l3273f-spi-x1_x2_x4}] 0]
if {$mem_part == ""} {
    set mem_part [lindex [get_cfgmem_parts {s25fl032p-spi-x1_x2_x4}] 0]
}

puts "Attaching SPI Flash memory device ($mem_part)..."
set cfgmem [create_hw_cfgmem -hw_device $dev $mem_part]

set_property PROGRAM.BLANK_CHECK  0 $cfgmem
set_property PROGRAM.ERASE        1 $cfgmem
set_property PROGRAM.CFG_PROGRAM  1 $cfgmem
set_property PROGRAM.VERIFY       1 $cfgmem
set_property PROGRAM.CHECKSUM     0 $cfgmem
set_property PROGRAM.ADDRESS_RANGE  {use_file} $cfgmem
set_property PROGRAM.FILES [list $binfile] $cfgmem
set_property PROGRAM.UNUSED_PIN_TERMINATION {pull-none} $cfgmem

puts "Programming device with SPI Flash programming helper core..."
create_hw_bitstream -hw_device $dev [get_property PROGRAM.HW_CFGMEM_BITFILE $dev]
program_hw_devices $dev

puts "Programming SPI Flash (Erase, Program, Verify)..."
program_hw_cfgmem $cfgmem

puts "Triggering Non-Volatile FPGA Boot from SPI Flash (QSPI Mode)..."
catch {
    boot_hw_device $dev
}

puts "======================================================================"
puts "  SUCCESS: Basys 3 SPI Flash Programmed Successfully!"
puts "  The FPGA is now configured to boot directly from SPI Flash (QSPI)."
puts "  Configuration is PERMANENT: No reprogramming needed on power-cycle!"
puts "======================================================================"
exit 0
