/**
////////////////////////////////////////////////////////////////////////////////////////////////////////////
- Saturation Filter TB

- TB module wrapping the design.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
*/

// Includes are defined in Makefile when using COCOTB
`ifndef COCOTB_SIM
  `include "sat_filter.sv"
`endif

module sat_filter_wrapper #(
    parameter THRESHOLD = 8,   // Threshold value
    parameter DATA_W = 4       // Data signal bit size
  )
  (
    // input   logic               clk,
    input   logic               rst,
    input   logic [DATA_W-1:0]  in_data,    // input data signal
    input   logic               in_valid,   // input data valid signal
    output  logic               ovf,        // overflow signal
    output  logic               out_valid,  // valid output signal
    output  logic [DATA_W-1:0]  out_data    // output signal
  );

  sat_filter #(
    .THRESHOLD(THRESHOLD),
    .DATA_W(DATA_W)
  )
  sat_filter_0 (
    .clk(clk),
    .rst(rst),
    .in_data(in_data),
    .in_valid(in_valid),
    .ovf(ovf),
    .out_valid(out_valid),
    .out_data(out_data)
  );

  // Clock generation
  logic clk;
  initial
  begin
    clk <= 0;
    forever
    begin
      #2.5ns clk = ~clk;
    end
  end

endmodule