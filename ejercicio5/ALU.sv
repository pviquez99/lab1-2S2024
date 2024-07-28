`timescale 1ns / 1ps

module ALU #(
    parameter ANCHO = 4
)(
    input  logic signed [ANCHO-1:0]  ALUA,
    input  logic signed [ANCHO-1:0]  ALUB,
    input  logic                     ALUFlagIn,
    input  logic        [3:0]        ALUControl,
    
    output logic        [ANCHO-1:0]  ALUResult,
    output logic                     ALUFlags,
    output logic                     ALUZero
    );

endmodule
