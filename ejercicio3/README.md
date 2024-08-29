# Ejercicio 3: Decodificador para display de 7 segmentos

## 1. Abreviaturas y definiciones
- **FPGA**: Field Programmable Gate Arrays

## 2. Referencias
[0] David Harris y Sarah Harris. *Digital Design and Computer Architecture. RISC-V Edition.* Morgan Kaufmann, 2022. ISBN: 978-0-12-820064-3

## 3. Desarrollo

Este archivo incluye las definiciones para el funcionamiento del sistema. La lista completa:

#### Tipos de variables
- `out`: Se utiliza para conectar la salida del multiplexor con el decodificador.

### 3.1 Módulo "mux4to1"

El módulo *mux* se encarga de multiplexar las entradas aplicadas a los 16 switches de la FPGA, donde solo 4 de ellos corresponderán al número mostrado en el display de 7 segmentos. Para este módulo se hizo la documentación respectiva en el Ejercicio 2 de este laboratorio por lo que se omite en este documento. 

### 3.2 Módulo "seven_segment_decoder"

#### 1. Encabezado del módulo
```SystemVerilog
module seven_segment_decoder (
    input logic [3:0] bin_in,     // Entrada de 4 bits
    output logic [6:0] seg_out,    // Salida para los 7 segmentos: abcdefg
    output logic [3:0] an
);
```
#### 2. Parámetros

El módulo no posee parámetros. 

#### 3. Entradas y salidas

- `bin_in`: Número en binario que representa la entrada del módulo
- `seg_out`: Salida que se conecta a cada uno de los segmentos del display (abcdefg).
- `an`: Anodo del display de 7 segmentos.

#### 4. Criterios de diseño

Para el diseño del decodificador primeramente se desarrolló una tabla que resume cada uno de los digitos representables por el display así como su representación en cada uno de los segmentos, la misma se muestra a continuación:

<div align="center">
  
| Decimal    | Binario | Hexadecimal   | Display |
| --------- | ---- | -------- |-------- |
| 0      | 0000   | 0   | 7'b1000000|
| 1     | 0001   | 1| 7'b1111001 |
| 2      | 0010   | 2   |7'b0100100|
| 3     | 0011   | 3|7'b0110000|
| 4      | 0100   | 4   |7'b0011001|
| 5     | 0101   | 5|7'b0010010|
| 6      | 0110   | 6   |7'b0000010|
| 7     | 0111   | 7|7'b1111000|
| 8      | 1000   | 8   |7'b0000000|
| 9     | 1001   | 9|7'b0010000|
| 10      | 1010   | A   |7'b0001000|
| 11     | 1011   | B|7'b0000011|
| 12      | 1100   | C   |7'b1000110|
| 13     | 1101   | D|7'b0100001|
| 14      | 1110   | E   |7'b0000110|
| 15    | 1111   | F|7'b0001110|

</div>

Para poder obtener un bloque que cumpla la función de multiplexar 4 números a 1 y luego mostrarlo en un display de 7 segmentos se crea un módulo top que conecta el módulo multiplexor con el decodificardor mostrado previamente. 


#### 5. Testbench

El testbench desarrollado prueba todas las combinaciones posibles en las entradas y además realiza una autoverificación interna que muestra un mensaje de error cuando en alguna de las iteraciones el resultado obtenido es diferente del esperado. A continuación se muestra el código del testbench. 

```SystemVerilog

module tb_TOP;

    // Inputs
    reg [1:0] sel;
    reg [15:0] sw;

    // Outputs
    wire [15:0] led;
    wire [6:0] seg;
    wire [3:0] an;

    // Instantiate the Unit Under Test (UUT)
    TOP uut (
        .sel(sel),
        .sw(sw),
        .led(led),
        .seg(seg),
        .an(an)
    );

    // Expected BCD outputs
    reg [6:0] expected_seg;

    initial begin
        // Inicializar las señales
        sel = 2'b00;
        sw = 16'b0000_0000_0000_0000;

        // Probar todas las combinaciones posibles de entradas
        for (int i = 0; i < 4; i = i + 1) begin
            sel = i;  // Cambiar el valor de selección

            for (int j = 0; j < 16; j = j + 1) begin
                sw[4*i +: 4] = j; // Asignar los 4 bits correspondientes al mux
                #10; // Esperar para que la señal se propague

                // Asignar el valor esperado según la tabla BCD
                case (sw[4*i +: 4])
                    4'b0000: expected_seg = 7'b1000000; // 0
                    4'b0001: expected_seg = 7'b1111001; // 1
                    4'b0010: expected_seg = 7'b0100100; // 2
                    4'b0011: expected_seg = 7'b0110000; // 3
                    4'b0100: expected_seg = 7'b0011001; // 4
                    4'b0101: expected_seg = 7'b0010010; // 5
                    4'b0110: expected_seg = 7'b0000010; // 6
                    4'b0111: expected_seg = 7'b1111000; // 7
                    4'b1000: expected_seg = 7'b0000000; // 8
                    4'b1001: expected_seg = 7'b0010000; // 9
                    4'b1010: expected_seg = 7'b0001000; // A
                    4'b1011: expected_seg = 7'b0000011; // b
                    4'b1100: expected_seg = 7'b1000110; // C
                    4'b1101: expected_seg = 7'b0100001; // d
                    4'b1110: expected_seg = 7'b0000110; // E
                    4'b1111: expected_seg = 7'b0001110; // F
                    default: expected_seg = 7'b1111111; // Error
                endcase

                // Comprobar la salida
                if (seg !== expected_seg) begin
                    $display("Error: sel=%b, sw=%b, expected seg=%b but got %b", sel, sw, expected_seg, seg);
                end else begin
                    $display("Test passed: sel=%b, sw=%b, seg=%b", sel, sw, seg);
                end
            end
        end

        $stop; // Terminar la simulación
    end

endmodule
```
