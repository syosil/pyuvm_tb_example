/**
////////////////////////////////////////////////////////////////////////////////////////////////////////////

- Dummy SSDT module to be used for the B2B test.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
*/

module ssdt_b2b #(
    parameter DATA_W = 4       // Data signal bit size
  )
  (
    input   logic               rst,
    input   logic [DATA_W-1:0]  in_data,    // input data signal
    input   logic               in_valid,   // input data valid signal
    output  logic               out_valid,  // valid output signal
    output  logic [DATA_W-1:0]  out_data    // output signal
  );

  // Generate dump files because of Icarus.
  initial
  begin
    $dumpfile ("sim_build/ssdt_b2b_waves.vcd");
    $dumpvars (0, ssdt_b2b);
  end

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