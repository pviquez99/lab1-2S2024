`timescale 1ns / 1ps

module RCA #(
  parameter BITS = 8
)(
  input  logic [BITS-1:0] a,
  input  logic [BITS-1:0] b,
  input  logic            cin,
  output logic [BITS-1:0] sum,
  output logic            cout
);

endmodule
