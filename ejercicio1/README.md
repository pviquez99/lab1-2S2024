# Ejercicio 1

## 1. Abreviaturas y definiciones
- **FPGA**: Field Programmable Gate Arrays

## 2. Referencias
[0] David Harris y Sarah Harris. *Digital Design and Computer Architecture. RISC-V Edition.* Morgan Kaufmann, 2022. ISBN: 978-0-12-820064-3

## 3. Desarrollo

### 3.1 Switches, botones y LEDs

El módulo *sbl* representa un sistema digital que lee el estado de interruptores y botones para controlar el estado de un conjunto de LEDs, apagando grupos específicos de LEDs según los botones presionados. La lógica es combinacional y la actualización de las salidas se realiza en respuesta a cambios en las entradas. Dado que la FPGA cuenta con 16 switches y 16 leds, cada uno de los leds representa el estado de los switches, y cada uno de los 4 botones se encarga de apagar un grupo de 4 leds. El módulo tiene la capacidad de apagar varios grupos de leds al mismo tiempo.

#### 1. Encabezado del módulo
```SystemVerilog
module sbl(
    input wire [15:0] sw,    // Entradas de los interruptores
    input wire [3:0]  buttons,     // Botones para seleccionar el grupo de interruptores
    output reg [15:0] led         // Salidas a los LEDs
);

```


#### 3. Entradas y salidas

- `switches`: Entradas de los interruptores
- `buttons`: Entrada de botones para seleccionar el grupo de interruptores
- `leds`: Salidas a los LEDs


#### 4. Criterios de diseño

Para llevar a cabo la implementación de esta aplicación, se requirió la configuración de los switches Y botones como entradas, así como los leds como salidas para el módulo. Esta configuración implicó asignar ubicaciones físicas específicas a estos componentes mediante un mapeo que se establece en el archivo de restricciones (constraints). A continuación, se detallan las asignaciones individuales para los switches, botones y LEDs, asegurando así una conexión precisa entre las variables utilizadas por el módulo y los pines físicos correspondientes en la FPGA.

```SystemVerilog
## Switches
set_property -dict { PACKAGE_PIN V17   IOSTANDARD LVCMOS33 } [get_ports {switches[0]}]
set_property -dict { PACKAGE_PIN V16   IOSTANDARD LVCMOS33 } [get_ports {switches[1]}]
set_property -dict { PACKAGE_PIN W16   IOSTANDARD LVCMOS33 } [get_ports {switches[2]}]
set_property -dict { PACKAGE_PIN W17   IOSTANDARD LVCMOS33 } [get_ports {switches[3]}]
set_property -dict { PACKAGE_PIN W15   IOSTANDARD LVCMOS33 } [get_ports {switches[4]}]
set_property -dict { PACKAGE_PIN V15   IOSTANDARD LVCMOS33 } [get_ports {switches[5]}]
set_property -dict { PACKAGE_PIN W14   IOSTANDARD LVCMOS33 } [get_ports {switches[6]}]
set_property -dict { PACKAGE_PIN W13   IOSTANDARD LVCMOS33 } [get_ports {switches[7]}]
set_property -dict { PACKAGE_PIN V2    IOSTANDARD LVCMOS33 } [get_ports {switches[8]}]
set_property -dict { PACKAGE_PIN T3    IOSTANDARD LVCMOS33 } [get_ports {switches[9]}]
set_property -dict { PACKAGE_PIN T2    IOSTANDARD LVCMOS33 } [get_ports {switches[10]}]
set_property -dict { PACKAGE_PIN R3    IOSTANDARD LVCMOS33 } [get_ports {switches[11]}]
set_property -dict { PACKAGE_PIN W2    IOSTANDARD LVCMOS33 } [get_ports {switches[12]}]
set_property -dict { PACKAGE_PIN U1    IOSTANDARD LVCMOS33 } [get_ports {switches[13]}]
set_property -dict { PACKAGE_PIN T1    IOSTANDARD LVCMOS33 } [get_ports {switches[14]}]
set_property -dict { PACKAGE_PIN R2    IOSTANDARD LVCMOS33 } [get_ports {switches[15]}]


## LEDs
set_property -dict { PACKAGE_PIN U16   IOSTANDARD LVCMOS33 } [get_ports {leds[0]}]
set_property -dict { PACKAGE_PIN E19   IOSTANDARD LVCMOS33 } [get_ports {leds[1]}]
set_property -dict { PACKAGE_PIN U19   IOSTANDARD LVCMOS33 } [get_ports {leds[2]}]
set_property -dict { PACKAGE_PIN V19   IOSTANDARD LVCMOS33 } [get_ports {leds[3]}]
set_property -dict { PACKAGE_PIN W18   IOSTANDARD LVCMOS33 } [get_ports {leds[4]}]
set_property -dict { PACKAGE_PIN U15   IOSTANDARD LVCMOS33 } [get_ports {leds[5]}]
set_property -dict { PACKAGE_PIN U14   IOSTANDARD LVCMOS33 } [get_ports {leds[6]}]
set_property -dict { PACKAGE_PIN V14   IOSTANDARD LVCMOS33 } [get_ports {leds[7]}]
set_property -dict { PACKAGE_PIN V13   IOSTANDARD LVCMOS33 } [get_ports {leds[8]}]
set_property -dict { PACKAGE_PIN V3    IOSTANDARD LVCMOS33 } [get_ports {leds[9]}]
set_property -dict { PACKAGE_PIN W3    IOSTANDARD LVCMOS33 } [get_ports {leds[10]}]
set_property -dict { PACKAGE_PIN U3    IOSTANDARD LVCMOS33 } [get_ports {leds[11]}]
set_property -dict { PACKAGE_PIN P3    IOSTANDARD LVCMOS33 } [get_ports {leds[12]}]
set_property -dict { PACKAGE_PIN N3    IOSTANDARD LVCMOS33 } [get_ports {leds[13]}]
set_property -dict { PACKAGE_PIN P1    IOSTANDARD LVCMOS33 } [get_ports {leds[14]}]
set_property -dict { PACKAGE_PIN L1    IOSTANDARD LVCMOS33 } [get_ports {leds[15]}]

##Buttons
set_property -dict { PACKAGE_PIN W19   IOSTANDARD LVCMOS33 } [get_ports buttons[0]]
set_property -dict { PACKAGE_PIN T18   IOSTANDARD LVCMOS33 } [get_ports buttons[1]]
set_property -dict { PACKAGE_PIN T17   IOSTANDARD LVCMOS33 } [get_ports buttons[2]]
set_property -dict { PACKAGE_PIN U17   IOSTANDARD LVCMOS33 } [get_ports buttons[3]]

```

#### 5. Testbench

El testbench `sbl_tb.sv` genera una instancia del módulo *sbl* y genera también las entradas de los botones para todas las combinaciones posibles. A continuación se incluye el código del testbench.


```SystemVerilog

module sbl_tb ();
    reg   [15:0] sw;  
    reg   [3:0]  buttons;
    wire  [15:0] led;
    integer i;
    
    // Instanciación del dispositivo bajo prueba (DUT)
    sbl dut (
        .sw(sw),
        .buttons(buttons),
        .led(led)
    );
      
    initial begin
        // Inicializar las señales
        sw = 16'b1010101010101010;
        
        // Ciclo para probar diferentes valores de 'buttons'
        for (i = 0; i < 16; i = i + 1) begin
            buttons = i;    // Asignar el valor de 'i' a 'buttons'
            $display(buttons);
            $display(led);
            #10;                 // Esperar 10 unidades de tiempo entre cada iteración
           
        end
    end
endmodule

```




