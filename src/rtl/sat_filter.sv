/**
////////////////////////////////////////////////////////////////////////////////////////////////////////////

- Saturation Filter:
  - This module receives a signal and filters it.
  - It can either saturate the output or pass the signal through.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
*/

module sat_filter #(
    parameter THRESHOLD = 8,   // Threshold value
    parameter DATA_W = 4       // Data signal bit size
  )
  (
    input   logic               clk,
    input   logic               rst,
    input   logic [DATA_W-1:0]  in_data,    // input data signal
    input   logic               in_valid,   // input data valid signal
    output  logic               ovf,        // overflow signal
    output  logic               out_valid,  // valid output signal
    output  logic [DATA_W-1:0]  out_data    // output signal
  );

  localparam threshold_val = THRESHOLD;

  // Generate dump files because of Icarus.
  initial
  begin
    $dumpfile ("sim_build/sat_filter_waves.vcd");
    $dumpvars (0, sat_filter);
  end

  // Main loop
  always_ff @(posedge clk, posedge rst)
  begin
    if (rst === 1'b1)
    begin
      ovf <= 'b0;
      out_valid <= 'b0;
      out_data <= 'b0;
    end
    else
    begin
      if (in_valid === 1'b1)
      begin
        if (in_data > threshold_val)
        begin
          out_data <= threshold_val;
          ovf <= 'b1;
        end
        else // Valid output: (in_data <= threshold_val)
        begin
          out_data <= in_data;
          ovf <= 'b0;
        end
        out_valid <= 'b1;
      end
      else
        begin
        out_valid <= 'b0;
        out_data <= 'b0;
        ovf <= 'b0;
        end
    end
  end

endmodule