import random
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def prueba_mux_comb(dut):
    """Prueba de todas las combinaciones del multiplexor 4 a 1 de 8 bits"""
    dut.entrada0_i.value = 0
    dut.entrada1_i.value = 0
    dut.entrada2_i.value = 0
    dut.entrada3_i.value = 0
    dut.seleccion_i.value = 0
    
    for prueba in range (2**8):
        for i in range (4):
            dut.__getattr__(f"entrada{i}_i").value = prueba
        for sel in range (4):
            dut.seleccion_i.value = sel
            await Timer(1, 'ns')
            assert dut.salida_o.value == prueba, f"El valor de salida_o es incorrecto. Se obtuvo {dut.salida_o.value}, esperaba {prueba}"

@cocotb.test()
async def prueba_mux_random(dut):
    """Prueba del multiplexor 4 a 1 con valores aleatorios en las entradas"""
    dut.entrada0_i.value = 0
    dut.entrada1_i.value = 0
    dut.entrada2_i.value = 0
    dut.entrada3_i.value = 0
    dut.seleccion_i.value = 0

    valores_entrada = []

    for n in range (4096):
        for i in range (4):
            valorentrada = random.randint(0,255)
            valores_entrada.append(valorentrada)
            dut.__getattr__(f"entrada{i}_i").value = valorentrada      
        for sel in range (4):
            dut.seleccion_i.value = sel
            await Timer(1, 'ns')
            assert dut.salida_o.value == valores_entrada[sel], f"El valor de salida_o es incorrecto. Se obtuvo {dut.salida_o.value}, esperaba {valores_entrada[sel]}"
        valores_entrada = []

