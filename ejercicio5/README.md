# Ejercicio 5: Unidad aritmética lógica (ALU)

## 1. Abreviaturas y definiciones
- **FPGA**: Field Programmable Gate Arrays

## 2. Referencias
[0] David Harris y Sarah Harris. *Digital Design and Computer Architecture. RISC-V Edition.* Morgan Kaufmann, 2022. ISBN: 978-0-12-820064-3

## 3. Desarrollo

### 3.1 Módulo "alu"

La Unidad Aritmético Lógica desarrollada se encarga de realizar las operaciones: AND, OR, SUMA, INCREMENTO EN 1, DECREMENTO EN 1, NOR, RESTA, XOR, DESPLAZO A LA IZQUIERDA Y DESPLAZO A LA DERECHA sobre datos binarios de entrada.


#### 1. Encabezado del módulo
```SystemVerilog
module alu #(parameter WIDTH = 4  // Parámetro para el ancho de las entradas y salida
)(
    input  wire [3:0]  ALUControl,    // Código de operación (hexadecimal)
    input  wire [WIDTH-1:0]  ALUA,         // Primer operando (8 bits)
    input  wire [WIDTH-1:0]  ALUB,         // Segundo operando (8 bits, opcional según la operación)
    input wire ALUFlagIn,
    output reg [WIDTH-1:0]  ALUResult,    // Resultado de la operación (8 bits)
    output reg [1:0] ALUFlags  // Señal de acarreo (para operaciones de suma/resta)
); 
```
#### 2. Parámetros

- `WIDTH`: Define el ancho de las entradas y salidas de la ALU

#### 3. Entradas y salidas

- `ALUControl`: Selecciona la operación que se desea ejecutar
- `ALUA`: Primer operando
- `ALUB`: Segundo operando
- `ALUFlagIn`: Acarreo o selección de bits (según sea la operación)
- `ALUResult`: Resultado de la operación
- `ALUFlags`: Señal de acarreo de salida y bandera de cero

#### 4. Criterios de diseño

En la siguiente imagen se muestra un diagrama que describe la distribución interna de la ALU desarrollada.

![imagen](https://github.com/user-attachments/assets/6c16f0c8-f9a5-4024-b059-79936412f02a)

Cada una de las operaciones se desarrolló en un case diferente lo que permite disminuir la cantidad de archivos del proyecto.




#### 5. Testbench


El siguiente testbench prueba todos los posibles casos de operación existentes y realiza una autoverificación interna que despliega un mensaje de error si el dato obtenido es diferente del esperado. 

```SystemVerilog

module tb_alu;

    // Parámetros
    parameter WIDTH = 4;

    // Entradas
    reg [3:0] ALUControl;
    reg [WIDTH-1:0] ALUA;
    reg [WIDTH-1:0] ALUB;
    reg ALUFlagIn;

    // Salidas
    wire [WIDTH-1:0] ALUResult;
    wire ALUFlag;
    wire cero;

    // Instancia del módulo ALU
    alu #(WIDTH) uut (
        .ALUControl(ALUControl),
        .ALUA(ALUA),
        .ALUB(ALUB),
        .ALUFlagIn(ALUFlagIn),
        .ALUResult(ALUResult),
        .ALUFlag(ALUFlag),
        .cero(cero)
    );

    // Proceso de prueba
    initial begin
        // Inicialización de variables
        ALUControl = 4'h0;
        ALUA = 4'b0000;
        ALUB = 4'b0000;
        ALUFlagIn = 0;
        
        // Tiempo para cada operación: 10 unidades de tiempo
        #10; ALUControl = 4'h0; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de AND
        #10;
        check_result(ALUA&ALUB, 0, "Test Case 1");
        #10; ALUControl = 4'h1; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de OR
        #10;
        check_result(ALUA|ALUB, 0, "Test Case 2");
        
        #10; ALUControl = 4'h2; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de suma
        #10;
        check_result(ALUA+ALUB+ALUFlagIn, 0, "Test Case 3");
        #10; ALUControl = 4'h2; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 1;  // Prueba de suma
        #10;
        check_result(ALUA+ALUB+ALUFlagIn, 0, "Test Case 4");
        
        #10; ALUControl = 4'h3; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de +1
        #10;
        check_result(ALUA+1, 0, "Test Case 5");
        #10; ALUControl = 4'h3; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 1;  // Prueba de +1
        #10;
        check_result(ALUB+1, 0, "Test Case 6");
        
        #10; ALUControl = 4'h4; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de -1
        #10;
        check_result(ALUA-1, 0, "Test Case 7");
        #10; ALUControl = 4'h4; ALUA = 4'b0011; ALUB = 4'b0101; ALUFlagIn = 1;  // Prueba de -1
        #10;
        check_result(ALUB-1, 0, "Test Case 8");
        
        #10; ALUControl = 4'h5; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de NOT
        #10;
        check_result(~ALUA, 0, "Test Case 9");
        #10; ALUControl = 4'h5; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 1;  // Prueba de NOT
        #10;
        check_result(~ALUB, 0, "Test Case 10");
        
        #10; ALUControl = 4'h6; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de RESTA
        #10;
        check_result(ALUA-ALUB+ALUFlagIn, 0, "Test Case 11");
        #10; ALUControl = 4'h6; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 1;  // Prueba de RESTA
        #10;
        check_result(ALUA-ALUB+ALUFlagIn, 0, "Test Case 12");
        
        #10; ALUControl = 4'h7; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de XOR
        #10;
        check_result(ALUA^ALUB, 0, "Test Case 13");
        
        #10; ALUControl = 4'h8; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de IZQ
        #10;
        check_result((ALUA << ALUB) | (ALUFlagIn << (ALUB-1)), 0, "Test Case 14");
        #10; ALUControl = 4'h8; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 1;  // Prueba de IZQ
        #10;
        check_result((ALUA << ALUB) | (ALUFlagIn << (ALUB-1)), 0, "Test Case 15");
        
        #10; ALUControl = 4'h9; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 0;  // Prueba de DER
        #10;
        check_result((ALUA >> ALUB) | (ALUFlagIn << (WIDTH-ALUB)), 1, "Test Case 16");
        #10; ALUControl = 4'h9; ALUA = 4'b0011; ALUB = 4'b0001; ALUFlagIn = 1;  // Prueba de DER
        #10;
        check_result((ALUA >> ALUB) | (ALUFlagIn << (WIDTH-ALUB)), 1, "Test Case 17");
       

        // Finalizar simulación
        #10 $finish;
    end

    // Monitor para observar los resultados
//    initial begin
//        $monitor("Time=%0t | ALUControl=%h | ALUA=%b | ALUB=%b | ALUFlagIn=%b | ALUResult=%b | ALUFlag=%b | cero=%b",
//                 $time, ALUControl, ALUA, ALUB, ALUFlagIn, ALUResult, ALUFlag, cero);
//    end
    
    // Función para verificar resultados
    task check_result(input logic [3:0] expected_op, input logic expected_out, input string test_case_name);
        if (ALUResult !== expected_op || ALUFlag !== expected_out) begin
            $display("Error en %s: Esperado {ALUResult: %h, ALUFlag: %b}, Obtenido {ALUResult: %h, ALUFlag: %b}", 
                test_case_name, expected_op, expected_out, ALUResult, ALUFlag);
        end else begin
            $display("%s: Correcto {ALUResult: %h, ALUFlag: %b}", test_case_name, ALUResult, ALUFlag);
        end
    endtask

endmodule

```
