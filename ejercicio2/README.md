# Ejercicio 2: Multiplexor 4-to-1

## 1. Abreviaturas y definiciones
- **FPGA**: Field Programmable Gate Arrays

## 2. Referencias
[0] David Harris y Sarah Harris. *Digital Design and Computer Architecture. RISC-V Edition.* Morgan Kaufmann, 2022. ISBN: 978-0-12-820064-3

## 3. Desarrollo

### 3.1 Multiplexor 4 to 1

El módulo *mux4to1* representa un multiplexor de 4 entradas a 1 salida con un ancho de bus configurable. 


#### 1. Encabezado del módulo
```SystemVerilog
module mux4to1 #(
parameter WIDTH = 4  // Parámetro para el ancho de las entradas y salida
)( 
    input  logic [1:0] sel,   // Señal de selección de 2 bits
    input  logic [WIDTH-1:0] in0,   // Entrada 0 de WIDTH bits
    input  logic [WIDTH-1:0] in1,   // Entrada 1 de WIDTH bits
    input  logic [WIDTH-1:0] in2,   // Entrada 2 de WIDTH bits
    input  logic [WIDTH-1:0] in3,   // Entrada 3 de WIDTH bits
    output logic [WIDTH-1:0] out    // Salida de WIDTH bits
);
```
#### 2. Parámetros

- `WIDTH`: Parámetro que define el ancho del bus de datos en el multiplexor. Tiene un valor predeterminado de 4, pero en el test bench este toma valores de 4, 8 y 16.

#### 3. Entradas y salidas

- `in0`, `in1`, `in2`, `in3`: Entradas de datos (ancho WIDTH) al multiplexor.
- `sel`: Entrada de 2 bits que especifica qué entrada del multiplexor se seleccionará.
- `out`: Salida del módulo, representa el dato seleccionado por el multiplexor según la entrada `sel`.


#### 4. Criterios de diseño

Como parte del diseño planteado, se desarrolló un diagrama que ilustrata el sistema junto con sus entradas y salidas. La imagen adjunta ilustra a nivel de bloques el sistema:


<div align="center">
  <img src="https://github.com/EL3313/laboratorio1-grupo-6/blob/main/ejercicio2/E2.png">
</div>

Y la tabla de verdad que determina su comportamiento corresponde a: 


<div align="center">
  <img src="https://github.com/EL3313/laboratorio1-grupo-6/blob/main/ejercicio2/table.jpg">
</div>


#### 5. Testbench

El testbench desarrollado aparte de probar todas las posibles combinaciones de entrada, también es autoverificable lo que quiere decir que si se encontrase algún error en las iteraciones, es capaz de identificar el número de iteración y despliega un mensaje de error. A continuación se incluye el código del testbench junto con el mensaje de salida en la terminal una vez realizado el test.


```SystemVerilog

module tb_multiplexor #(parameter WIDTH = 8) ();
    reg   [WIDTH-1:0]   in0, in1, in2, in3;  
    reg   [1:0]         sel;
    wire   [WIDTH-1:0]   out;
    integer i;
    
    mux4to1 #(WIDTH) dut(sel, in0, in1, in2, in3, out);
   
    initial begin
    $display("Empezando simulacion para un ancho de: %d", WIDTH);
   
    for (i = 0; i < 50; i=i+1) begin
        in0 = $random;
        in1 = $random;
        in2 = $random;
        in3 = $random;


        sel = 2'b00; // Se pone la se?al de selecci?n en 00
        #5; // Esperar 5 unidades de tiempo        

        // Verificar que data_o y data_0_i son iguales 
        if (out != in0) begin
            $display("Error en iteracion %0d: El valor a la entrada es %b y el obtenido a la salida fue %b, no son iguales", i, in0, out);
        end
        //$display("Iteraci?n %0d: Verificaci?n 1 pasada", i);

        sel = 2'b01; // Se pone la se?al de selecci?n en 01
        #5; 

        // Verificar que data_o y data_1_i son iguales 
        if (out != in1) begin
            $display("Error en iteracion %0d: El valor a la entrada es %b y el obtenido a la salida fue %b, no son iguales", i, in1, out);
        end
        //$display("Iteraci?n %0d: Verificaci?n 2 pasada", i);

        sel = 2'b10; // Se pone la se?al de selecci?n en 10
        #5; 

        // Verificar que data_o y data_2_i son iguales 
        if (out != in2) begin
            $display("Error en iteracion %0d: El valor a la entrada es %b y el obtenido a la salida fue %b, no son iguales", i, in2, out);
        end
        //$display("Iteraci?n %0d: Verificaci?n 3 pasada", i);

        sel = 2'b11; // Se pone la se?al de selecci?n en 11
        #5; 

        // Verificar que data_o y data_3_i son iguales 
        if (out != in3) begin
            $display("Error en iteracion %0d: El valor a la entrada es %b y el obtenido a la salida fue %b, no son iguales", i, in3, out);
        end
        //$display("Iteraci?n %0d: Verificaci?n 4 pasada", i);
    end

    // Si la simulaci?n llega aqu?, es porque se complet? correctamente
    $display("Simulacion terminada correctamente para un ancho de: %d", WIDTH);
    //$finish;
end

endmodule

// Modulo que envuelve el test bench para cambiar el valor de ANCHO
module tb_wrapper;
    tb_multiplexor #(4) tb_4();
    tb_multiplexor #(8) tb_8();
    tb_multiplexor #(16) tb_16();
endmodule

```



Luego de correr el test bench, se muestra en la terminal:
```
Empezando simulación para un ancho de:           4
Empezando simulación para un ancho de:           8
Empezando simulación para un ancho de:          16
Simulación terminada correctamente para un ancho de:           4
Simulación terminada correctamente para un ancho de:           8
Simulación terminada correctamente para un ancho de:          16
```
