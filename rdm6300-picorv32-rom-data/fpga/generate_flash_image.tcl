# ==============================================================================
# Generate Combined Flash Image (.bin & .mcs) for Spansion S25FL032P (4MB)
# 0x0000_0000: Artix-7 FPGA Bitstream
# 0x0025_0000: PicoRV32 RISC-V Firmware Binary
# ==============================================================================
set proj_dir [file dirname [info script]]
set root_dir [file normalize "$proj_dir/.."]

set bitfile "$proj_dir/top_basys3_picorv32_rdm6300.bit"
set binfile "$root_dir/firmware/firmware.bin"

if {![file exists $bitfile]} {
    puts "ERROR: Bitstream file $bitfile not found!"
    exit 1
}
if {![file exists $binfile]} {
    puts "ERROR: Firmware binary $binfile not found!"
    exit 1
}

puts "Generating Flash memory images for S25FL032P (4MB SPIx4)..."
write_cfgmem -format bin -size 4 -interface SPIx4 \
    -loadbit "up 0x00000000 $bitfile" \
    -loaddata "up 0x00250000 $binfile" \
    -file "$proj_dir/top_basys3_picorv32_rdm6300_flash.bin" -force

write_cfgmem -format mcs -size 4 -interface SPIx4 \
    -loadbit "up 0x00000000 $bitfile" \
    -loaddata "up 0x00250000 $binfile" \
    -file "$proj_dir/top_basys3_picorv32_rdm6300_flash.mcs" -force

puts "======================================================================"
puts "  FLASH MEMORY IMAGES GENERATED SUCCESSFULLY!"
puts "  BIN file: $proj_dir/top_basys3_picorv32_rdm6300_flash.bin"
puts "  MCS file: $proj_dir/top_basys3_picorv32_rdm6300_flash.mcs"
puts "======================================================================"
exit 0
