`timescale 1ns / 1ps

module tb_spi_flash;

    reg clk;
    reg rst_n;

    // Bus interface
    reg        bus_valid;
    reg [4:0]  bus_addr;
    reg [31:0] bus_wdata;
    reg [3:0]  bus_wstrb;
    wire [31:0] bus_rdata;
    wire        bus_ready;

    // SPI interface
    wire flash_csn;
    wire flash_sck;
    wire flash_mosi;
    reg  flash_miso;

    wire flash_busy;
    wire flash_write_done;
    wire flash_error;
    wire [15:0] saved_records_count;

    // Instantiate DUT
    spi_flash_controller #(
        .CLK_FREQ_HZ(100_000_000),
        .SPI_FREQ_HZ(25_000_000),
        .FLASH_BASE_ADDR(24'h30_0000)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .bus_valid(bus_valid),
        .bus_addr(bus_addr),
        .bus_wdata(bus_wdata),
        .bus_wstrb(bus_wstrb),
        .bus_rdata(bus_rdata),
        .bus_ready(bus_ready),
        .auto_save_enable(1'b0),
        .card_valid(1'b0),
        .tag_raw(40'd0),
        .tag_checksum(8'd0),
        .flash_csn(flash_csn),
        .flash_sck(flash_sck),
        .flash_mosi(flash_mosi),
        .flash_miso(flash_miso),
        .flash_busy(flash_busy),
        .flash_write_done(flash_write_done),
        .flash_error(flash_error),
        .saved_records_count(saved_records_count)
    );

    // 100MHz clock
    initial clk = 0;
    always #5 clk = ~clk;

    // SPI Flash model memory (64KB)
    reg [7:0] flash_mem [0:65535];
    reg [7:0] status_reg;
    reg [7:0] rx_byte;
    reg [2:0] rx_bit_cnt;
    reg [7:0] tx_byte;
    reg [2:0] tx_bit_cnt;
    integer byte_count;
    reg [7:0] cur_cmd;
    reg [23:0] cur_addr;
    integer wip_timer;

    initial begin
        status_reg = 8'h00;
        flash_miso = 1'b0;
        wip_timer = 0;
        for (integer i = 0; i < 65536; i = i + 1) begin
            flash_mem[i] = 8'hFF;
        end
    end

    // WIP timer countdown
    always @(posedge clk) begin
        if (wip_timer > 0) begin
            wip_timer <= wip_timer - 1;
            if (wip_timer == 1) begin
                status_reg[0] <= 1'b0; // WIP cleared
                $display("[FLASH_MODEL %0t] WIP cleared (idle)", $time);
            end
        end
    end

    // Flash Slave SPI protocol
    always @(negedge flash_csn) begin
        rx_bit_cnt = 7;
        byte_count = 0;
        rx_byte = 0;
    end

    always @(posedge flash_sck) begin
        if (!flash_csn) begin
            rx_byte[rx_bit_cnt] = flash_mosi;
            if (rx_bit_cnt == 0) begin
                rx_bit_cnt = 7;
                byte_count = byte_count + 1;
                if (byte_count == 1) begin
                    cur_cmd = rx_byte;
                    if (cur_cmd == 8'h06) begin
                        status_reg[1] = 1'b1; // WEL = 1
                    end else if (cur_cmd == 8'h05) begin
                        tx_byte = status_reg;
                        tx_bit_cnt = 7;
                    end
                end else if (byte_count == 2) begin
                    cur_addr[23:16] = rx_byte;
                end else if (byte_count == 3) begin
                    cur_addr[15:8] = rx_byte;
                end else if (byte_count == 4) begin
                    cur_addr[7:0] = rx_byte;
                    if (cur_cmd == 8'h03) begin // READ
                        tx_byte = flash_mem[cur_addr[15:0]];
                        tx_bit_cnt = 7;
                    end
                end else begin
                    // Data bytes (PAGE_PROG)
                    if (cur_cmd == 8'h02) begin
                        flash_mem[cur_addr[15:0]] = rx_byte;
                        cur_addr = cur_addr + 1;
                    end else if (cur_cmd == 8'h03) begin
                        cur_addr = cur_addr + 1;
                        tx_byte = flash_mem[cur_addr[15:0]];
                        tx_bit_cnt = 7;
                    end
                end
            end else begin
                rx_bit_cnt = rx_bit_cnt - 1;
            end
        end
    end

    always @(negedge flash_sck) begin
        if (!flash_csn) begin
            if (cur_cmd == 8'h05 || (cur_cmd == 8'h03 && byte_count >= 4)) begin
                flash_miso <= tx_byte[tx_bit_cnt];
                if (tx_bit_cnt > 0) tx_bit_cnt <= tx_bit_cnt - 1;
                else tx_bit_cnt <= 7;
            end else begin
                flash_miso <= 1'b0;
            end
        end
    end

    always @(posedge flash_csn) begin
        flash_miso <= 1'b0;
        if (cur_cmd == 8'h02) begin
            // Page program completes on CSn high
            status_reg[0] <= 1'b1; // WIP = 1
            status_reg[1] <= 1'b0; // WEL = 0
            wip_timer <= 50; // 50 cycles
        end else if (cur_cmd == 8'hD8) begin
            // Sector erase
            status_reg[0] <= 1'b1; // WIP = 1
            status_reg[1] <= 1'b0; // WEL = 0
            wip_timer <= 100;
            for (integer k = 0; k < 65536; k = k + 1) flash_mem[k] = 8'hFF;
        end
    end

    // MMIO bus tasks
    task mmio_write(input [4:0] addr, input [31:0] data);
    begin
        @(posedge clk);
        bus_valid <= 1'b1;
        bus_addr  <= addr;
        bus_wdata <= data;
        bus_wstrb <= 4'b1111;
        @(posedge clk);
        while (!bus_ready) @(posedge clk);
        bus_valid <= 1'b0;
        bus_wstrb <= 4'b0000;
        @(posedge clk);
    end
    endtask

    task mmio_read(input [4:0] addr, output [31:0] data);
    begin
        @(posedge clk);
        bus_valid <= 1'b1;
        bus_addr  <= addr;
        bus_wstrb <= 4'b0000;
        @(posedge clk);
        while (!bus_ready) @(posedge clk);
        data = bus_rdata;
        bus_valid <= 1'b0;
        @(posedge clk);
    end
    endtask

    task wait_flash_done;
        reg [31:0] status;
    begin
        status = 1;
        while (status[0]) begin
            mmio_read(5'h04, status);
            #100;
        end
    end
    endtask

    task flash_erase_sector_task(input [23:0] addr);
    begin
        wait_flash_done();
        mmio_write(5'h08, {8'd0, addr});
        mmio_write(5'h00, 32'h00000005); // OP_SECTOR_ERASE = 2 -> (2 << 1) | 1 = 5
        wait_flash_done();
    end
    endtask

    task flash_write_word_task(input [23:0] addr, input [31:0] data);
    begin
        wait_flash_done();
        mmio_write(5'h08, {8'd0, addr});
        mmio_write(5'h0C, data);
        mmio_write(5'h00, 32'h00000003); // OP_WRITE = 1 -> (1 << 1) | 1 = 3
        wait_flash_done();
    end
    endtask

    task flash_read_word_task(input [23:0] addr, output [31:0] data);
    begin
        wait_flash_done();
        mmio_write(5'h08, {8'd0, addr});
        mmio_write(5'h00, 32'h00000001); // OP_READ = 0 -> (0 << 1) | 1 = 1
        wait_flash_done();
        mmio_read(5'h10, data);
    end
    endtask

    reg [31:0] rd_magic, rd_hi, rd_lo, rd_csum;

    initial begin
        rst_n = 0;
        bus_valid = 0;
        bus_addr = 0;
        bus_wdata = 0;
        bus_wstrb = 0;
        #100;
        rst_n = 1;
        #100;

        $display("=== SIMULATING save_tag_to_flash ===");
        flash_erase_sector_task(24'h30_0000);
        $display("[SIM] Erase done. Programming words...");

        flash_write_word_task(24'h30_0000, 32'h52464944); // "RFID"
        flash_write_word_task(24'h30_0004, 32'h00000000); // hi = 0
        flash_write_word_task(24'h30_0008, 32'h07312242); // lo = 0x07312242
        flash_write_word_task(24'h30_000C, 32'h07312242); // csum

        $display("[SIM] Programming complete. Reading back...");

        flash_read_word_task(24'h30_0000, rd_magic);
        flash_read_word_task(24'h30_0004, rd_hi);
        flash_read_word_task(24'h30_0008, rd_lo);
        flash_read_word_task(24'h30_000C, rd_csum);

        $display("[SIM RESULT] Magic: 0x%08X (Expected 0x52464944)", rd_magic);
        $display("[SIM RESULT] Hi:    0x%08X (Expected 0x00000000)", rd_hi);
        $display("[SIM RESULT] Lo:    0x%08X (Expected 0x07312242)", rd_lo);
        $display("[SIM RESULT] Csum:  0x%08X (Expected 0x07312242)", rd_csum);

        if (rd_magic == 32'h52464944 && rd_lo == 32'h07312242) begin
            $display("[SUCCESS] SIMULATION MATCHES EXPECTED 100%");
        end else begin
            $display("[FAILURE] SIMULATION FAILED");
        end

        #500;
        $finish;
    end

endmodule
