# Reproducible non-project build using the canonical modular RTL sources.
set script_dir [file dirname [file normalize [info script]]]
set root_dir   [file normalize [file join $script_dir ".."]]
set build_dir  [file join $root_dir "build" "basys3"]
file mkdir $build_dir

read_verilog [list \
    [file join $root_dir rtl common sync_2ff.v] \
    [file join $root_dir rtl fifo rx_fifo.v] \
    [file join $root_dir rtl fifo tx_fifo.v] \
    [file join $root_dir rtl uart uart_rx.v] \
    [file join $root_dir rtl uart uart_tx.v] \
    [file join $root_dir rtl rdm6300 rdm6300_frame_decoder.v] \
    [file join $root_dir rtl app card_packet_encoder.v] \
    [file join $root_dir rtl parser rfid_parser.v] \
    [file join $root_dir fpga rtl top_basys3_rdm6300.v]]
read_xdc [file join $root_dir fpga constraints basys3_rdm6300.xdc]

synth_design -top top_basys3_rdm6300 -part xc7a35tcpg236-1
opt_design
place_design
phys_opt_design
route_design

report_timing_summary -file [file join $build_dir timing_summary.rpt]
report_utilization -file [file join $build_dir utilization.rpt]
report_drc -file [file join $build_dir drc.rpt]
write_checkpoint -force [file join $build_dir top_basys3_rdm6300_routed.dcp]
write_bitstream -force [file join $build_dir top_basys3_rdm6300.bit]
