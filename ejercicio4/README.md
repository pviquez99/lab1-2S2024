# Ejercicio 4: Ripple Carry Adder 

## 1. Abreviaturas y definiciones
- **FPGA**: Field Programmable Gate Arrays

## 2. Referencias
[0] David Harris y Sarah Harris. *Digital Design and Computer Architecture. RISC-V Edition.* Morgan Kaufmann, 2022. ISBN: 978-0-12-820064-3

## 3. Desarrollo

### 3.1 Módulo "ripple_carry_adder"

El Ripple Carry Adder es un sumador de acarreo en cascada parametrizable que utiliza instancias del sumador completo para realizar la suma bit a bit. Cada uno de los sumadores toma dos bits de entrada a y b, un acarreo de entrada cin, y produce un bit de suma y un acarreo de salida que se propaga a lo largo de cada uno de los sumadores. 

#### 1. Encabezado del módulo
```SystemVerilog
module ripple_carry_adder #(
    parameter N = 8  // Tamaño de palabra, por defecto 8 bits
) (
    input  wire [N-1:0] a,       // Primer sumando de N bits
    input  wire [N-1:0] b,       // Segundo sumando de N bits
    input  wire cin,             // Bit de acarreo de entrada
    output wire [N-1:0] sum,     // Resultado de la suma de N bits
    output wire cout             // Acarreo de salida
);
```
#### 2. Parámetros

- `N`: tamaño de palabra

#### 3. Entradas y salidas

- `a`: Primer sumando de N bits
- `b`: Segundo sumando de N bits
- `cin`: Bit de acarreo de entrada
- `sum`: Resultado de la suma de N bits
- `cout`: Acarreo de salida

#### 4. Criterios de diseño

El siguiente diagrama muestra cómo se ve un Ripple Carry Adder de 4 bits. 

<div align="center">
  <img src="https://github.com/EL3313/laboratorio-1-pviquez99/blob/main/Ejercicio%204/E4.png" width="500px">
</div>

En la tabla adjunta se muestra la tabla de verdad de los sumadores de 1 bit. 

<div align="center">
  <img src="https://github.com/EL3313/laboratorio-1-pviquez99/blob/main/Ejercicio%204/2-41.jpg">
</div>

Para generar un Ripple Carry Adder parametrizable se necesita crear un loop que itere sobre cada uno de los bits de los datos que se desean sumar.


#### 5. Testbench

El testbench desarrollado muestra 6 casos de prueba autoverificables que arroja un mensaje de error cuando alguno de los resultados obtenidos no coincide con el esperado. 

```SystemVerilog
module tb_carry_lookahead_adder_8bit;

    // Declaración de señales
    logic [7:0] A, B;
    logic Cin;
    logic [7:0] Sum;
    logic Cout;

     ripple_carry_adder #(
        .N(8)
    ) uut (
        .a(A),
        .b(B),
        .cin(Cin),
        .sum(Sum),
        .cout(Cout)
    );


    // Proceso de test
    initial begin
        // Sección de inicialización
        $display("Iniciando la simulación del Carry Lookahead Adder de 8 bits...");

        // Test case 1: A = 8'h00, B = 8'h00, Cin = 0
        A = 8'h00; B = 8'h00; Cin = 0;
        #10;
        check_result(8'h00, 0, "Test Case 1");

        // Test case 2: A = 8'hFF, B = 8'h01, Cin = 0
        A = 8'hFF; B = 8'h01; Cin = 0;
        #10;
        check_result(8'h00, 1, "Test Case 2");

        // Test case 3: A = 8'hAA, B = 8'h55, Cin = 1
        A = 8'hAA; B = 8'h55; Cin = 1;
        #10;
        check_result(8'h00, 1, "Test Case 3");

        // Test case 4: A = 8'h0F, B = 8'hF0, Cin = 1
        A = 8'h0F; B = 8'hF0; Cin = 1;
        #10;
        check_result(8'h00, 1, "Test Case 4");

        // Test case 5: A = 8'h3C, B = 8'hC3, Cin = 0
        A = 8'h3C; B = 8'hC3; Cin = 0;
        #10;
        check_result(8'hFF, 0, "Test Case 5");

        // Test case 6: A = 8'h7E, B = 8'h81, Cin = 1
        A = 8'h7E; B = 8'h81; Cin = 1;
        #10;
        check_result(8'h00, 1, "Test Case 6");

        // Finalización de la simulación
        $display("Simulación completa.");
        $finish;
    end

    // Función para verificar resultados
    task check_result(input logic [7:0] expected_sum, input logic expected_cout, input string test_case_name);
        if (Sum !== expected_sum || Cout !== expected_cout) begin
            $display("Error en %s: Esperado {Sum: %h, Cout: %b}, Obtenido {Sum: %h, Cout: %b}", 
                test_case_name, expected_sum, expected_cout, Sum, Cout);
        end else begin
            $display("%s: Correcto {Sum: %h, Cout: %b}", test_case_name, Sum, Cout);
        end
    endtask

endmodule

```

### 3.2 Módulo "carry_lookahead_adder_8bit"

El Carry Lookahead Adder (CLA) es un tipo de sumador digital diseñado para realizar operaciones de suma de manera más rápida que un sumador tradicional, como el Ripple Carry Adder (RCA). El CLA mejora la velocidad del proceso de suma al calcular el acarreo (carry) en paralelo, en lugar de esperar a que el acarreo se propague de un bit a otro a través de cada etapa de la suma.

#### 1. Encabezado del módulo
```SystemVerilog
module carry_lookahead_adder_8bit (
    input  logic [7:0] A,
    input  logic [7:0] B,
    input  logic       Cin,
    output logic [7:0] Sum,
    output logic       Cout
);
```
#### 2. Parámetros

- `N`: tamaño de palabra

#### 3. Entradas y salidas

- `A`: Primer sumando de N bits
- `B`: Segundo sumando de N bits
- `Cin`: Bit de acarreo de entrada
- `Sum`: Resultado de la suma de N bits
- `Cout`: Acarreo de salida


#### 5. Testbench

El testbench desarrollado muestra 6 casos de prueba autoverificables que arroja un mensaje de error cuando alguno de los resultados obtenidos no coincide con el esperado. 

```SystemVerilog
module tb_carry_lookahead_adder_8bit;

    // Declaración de señales
    logic [7:0] A, B;
    logic Cin;
    logic [7:0] Sum;
    logic Cout;

    // Instancia del Carry Lookahead Adder
    carry_lookahead_adder_8bit cla (
        .A(A),
        .B(B),
        .Cin(Cin),
        .Sum(Sum),
        .Cout(Cout)
    );

    // Proceso de test
    initial begin
        // Sección de inicialización
        $display("Iniciando la simulación del Carry Lookahead Adder de 8 bits...");

        // Test case 1: A = 8'h00, B = 8'h00, Cin = 0
        A = 8'h00; B = 8'h00; Cin = 0;
        #10;
        check_result(8'h00, 0, "Test Case 1");

        // Test case 2: A = 8'hFF, B = 8'h01, Cin = 0
        A = 8'hFF; B = 8'h01; Cin = 0;
        #10;
        check_result(8'h00, 1, "Test Case 2");

        // Test case 3: A = 8'hAA, B = 8'h55, Cin = 1
        A = 8'hAA; B = 8'h55; Cin = 1;
        #10;
        check_result(8'h00, 1, "Test Case 3");

        // Test case 4: A = 8'h0F, B = 8'hF0, Cin = 1
        A = 8'h0F; B = 8'hF0; Cin = 1;
        #10;
        check_result(8'h00, 1, "Test Case 4");

        // Test case 5: A = 8'h3C, B = 8'hC3, Cin = 0
        A = 8'h3C; B = 8'hC3; Cin = 0;
        #10;
        check_result(8'hFF, 0, "Test Case 5");

        // Test case 6: A = 8'h7E, B = 8'h81, Cin = 1
        A = 8'h7E; B = 8'h81; Cin = 1;
        #10;
        check_result(8'h00, 1, "Test Case 6");

        // Finalización de la simulación
        $display("Simulación completa.");
        $finish;
    end

    // Función para verificar resultados
    task check_result(input logic [7:0] expected_sum, input logic expected_cout, input string test_case_name);
        if (Sum !== expected_sum || Cout !== expected_cout) begin
            $display("Error en %s: Esperado {Sum: %h, Cout: %b}, Obtenido {Sum: %h, Cout: %b}", 
                test_case_name, expected_sum, expected_cout, Sum, Cout);
        end else begin
            $display("%s: Correcto {Sum: %h, Cout: %b}", test_case_name, Sum, Cout);
        end
    endtask

endmodule


```
