# Add the canonical modular RTL to the currently open Vivado project.
# Run from the Vivado Tcl Console:
#   source ../rdm6300_asic_fpga_modular/scripts/sync_vivado_project_sources.tcl

set script_dir [file dirname [file normalize [info script]]]
set root_dir   [file normalize [file join $script_dir ".."]]

# Remove sources retired from the canonical architecture before adding the
# active list. This only removes them from the Vivado project, not from disk.
set obsolete_sources [get_files -quiet [list \
    *card_event_fifo.v \
    *tb_card_event_fifo.v \
    *tb_fifo_sync.v \
    *fifo_sync.v \
    *uart_fifo_core.v \
    *rdm6300_access_core.v]]
if {[llength $obsolete_sources] > 0} {
    remove_files $obsolete_sources
}

set rtl_sources [list \
    [file join $root_dir rtl common sync_2ff.v] \
    [file join $root_dir rtl fifo rx_fifo.v] \
    [file join $root_dir rtl fifo tx_fifo.v] \
    [file join $root_dir rtl uart uart_rx.v] \
    [file join $root_dir rtl uart uart_tx.v] \
    [file join $root_dir rtl rdm6300 rdm6300_frame_decoder.v] \
    [file join $root_dir rtl app card_packet_encoder.v] \
    [file join $root_dir rtl parser rfid_parser.v] \
    [file join $root_dir fpga rtl top_basys3_rdm6300.v]]

foreach source_file $rtl_sources {
    if {![file exists $source_file]} {
        error "Canonical RTL source does not exist: $source_file"
    }
}

add_files -fileset sources_1 -norecurse $rtl_sources
set_property top top_basys3_rdm6300 [get_filesets sources_1]
update_compile_order -fileset sources_1

puts "Canonical modular RTL sources synchronized successfully."
