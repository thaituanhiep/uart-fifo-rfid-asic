# Usage from Vivado Tcl console:
#   source fpga/vivado/create_project.tcl
# Then set your board part if needed and add/create top later.

set proj_name "uart_fifo_basys3"
set proj_dir "./fpga/vivado/build"
set part_name "xc7a35tcpg236-1"

create_project $proj_name $proj_dir -part $part_name -force

set rtl_files [glob ./rtl/*.v]
add_files -norecurse $rtl_files
set_property top top_basys3_rdm6300 [current_fileset]

# Basys3 constraints for top_basys3_rdm6300.
add_files -fileset constrs_1 ./constraints/basys3_template.xdc

update_compile_order -fileset sources_1
puts "Project created with top module top_basys3_rdm6300. Run synthesis/implementation/bitstream."
