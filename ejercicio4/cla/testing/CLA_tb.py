import cocotb
import random
from cocotb.triggers import Timer

PRUEBAS = 2**8

@cocotb.test()
async def prueba_CLA_sin_carry_in(dut):
    dut.c_in.value = 0

    for valor_a in range(PRUEBAS):
        dut.a.value = valor_a
        for valor_b in range(PRUEBAS):
            dut.b.value = valor_b

            resultado = (valor_a + valor_b) & 0xFF
            carry_out = ((valor_a + valor_b) >> 8) & 1

            await Timer(1, 'ns')

            assert dut.sum.value == resultado, f"Resultado de la suma incorrecto. Se obtuvo {dut.sum.value}, esperaba {resultado}"
            assert dut.c_out.value == carry_out, f"Resultado del carry out incorrecto. Se obtuvo {dut.c_out.value}, esperaba {carry_out}"

@cocotb.test()
async def prueba_CLA_con_carry_in(dut):
    dut.c_in.value = 1

    for valor_a in range(PRUEBAS):
        dut.a.value = valor_a
        for valor_b in range(PRUEBAS):
            dut.b.value = valor_b

            resultado = (valor_a + valor_b + 1) & 0xFF
            carry_out = ((valor_a + valor_b + 1) >> 8) & 1

            await Timer(1, 'ns')

            assert dut.sum.value == resultado, f"Resultado de la suma incorrecto. Se obtuvo {dut.sum.value}, esperaba {resultado}"
            assert dut.c_out.value == carry_out, f"Resultado del carry out incorrecto. Se obtuvo {dut.c_out.value}, esperaba {carry_out}"