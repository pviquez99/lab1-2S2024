`timescale 1ns / 1ps

module mux_4_1 #(
    parameter int ANCHO = 8
)(
    input  logic [1:0]       seleccion_i,
    input  logic [ANCHO-1:0] entrada0_i,
    input  logic [ANCHO-1:0] entrada1_i, 
    input  logic [ANCHO-1:0] entrada2_i, 
    input  logic [ANCHO-1:0] entrada3_i,  
    output logic [ANCHO-1:0] salida_o
    );

endmodule