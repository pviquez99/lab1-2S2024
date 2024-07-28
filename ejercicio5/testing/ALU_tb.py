import cocotb
from cocotb.triggers import Timer

RANGO = 2**4
valores_b = [0, 8, 12, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]

@cocotb.test()
async def test_AND(dut):
    '''Prueba de la operación AND'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 0

    for valor_a in range(RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range(RANGO):
            dut.ALUControl.value = 0
            dut.ALUB.value = valor_b
            await Timer(1, 'ns')
            assert dut.ALUResult.value == valor_a & valor_b, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {valor_a & valor_b}"

@cocotb.test()
async def test_OR(dut):
    '''Prueba de la operación OR'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 1

    for valor_a in range(RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range(RANGO):
            dut.ALUB.value = valor_b
            await Timer(1, 'ns')
            assert dut.ALUResult.value == valor_a | valor_b, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {valor_a | valor_b}"

@cocotb.test()
async def prueba_suma_sin_carry(dut):
    '''Prueba de la operación suma sin carry in'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 2

    for valor_a in range(RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range(RANGO):
            dut.ALUB.value = valor_b
            resultado_suma = (valor_a + valor_b) & 0xF
            resultado_carry = ((valor_b + valor_a) >> 4) & 1
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado_suma, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_suma}"
            assert dut.ALUFlags.value == resultado_carry, f"El valor de la salida ALUFlags es incorrecto. Se obtuvo {dut.ALUFlags.value}, se esperaba {resultado_carry}"

@cocotb.test()
async def prueba_suma_con_carry(dut):
    '''Prueba de la operación suma con carry in'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 1
    dut.ALUControl.value = 2

    for valor_a in range(RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range(RANGO):
            dut.ALUB.value = valor_b
            resultado_suma = (valor_a + valor_b + 1) & 0xF
            resultado_carry = ((valor_a + valor_b + 1) >> 4) & 1
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado_suma, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_suma}"
            assert dut.ALUFlags.value == resultado_carry, f"El valor de la salida ALUFlags es incorrecto. Se obtuvo {dut.ALUFlags.value}, se esperaba {resultado_carry}"

@cocotb.test()
async def test_incrementar_1(dut):
    '''Prueba de la operación incrementar en 1'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 3

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        dut.ALUFlagIn.value = 0
        resultado_a1 = (valor_a + 1) & 0xF
        await Timer(1, 'ns')
        assert dut.ALUResult.value == resultado_a1, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_a1}"

    for valor_b in range (RANGO):
        dut.ALUB.value = valor_b
        dut.ALUFlagIn.value = 1
        resultado_b1 = (valor_b + 1) & 0xF
        await Timer(1, 'ns')
        assert dut.ALUResult.value == resultado_b1, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_b1}"

@cocotb.test()
async def test_decrementar_1(dut):
    '''Prueba de la operación decrementar en 1'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 4

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        resultado_am1 = (valor_a - 1) & 0xF
        await Timer(1, 'ns')
        assert dut.ALUResult.value == resultado_am1, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_am1}"

    for valor_b in range (RANGO):
        dut.ALUB.value = valor_b
        dut.ALUFlagIn.value = 1
        resultado_bm1 = (valor_b - 1) & 0xF
        await Timer(1, 'ns')
        assert dut.ALUResult.value == resultado_bm1, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_bm1}"


@cocotb.test()
async def test_NOT(dut):
    '''Prueba de la operación NOT'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 5

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        resultado_not_a = ~valor_a & 0xF
        await Timer(1, 'ns')
        assert dut.ALUResult.value == resultado_not_a, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_not_a}"

    for valor_b in range (RANGO):
        dut.ALUB.value = valor_b
        dut.ALUFlagIn.value = 1
        resultado_not_b = ~valor_b & 0xF
        await Timer(1, 'ns')
        assert dut.ALUResult.value == resultado_not_b, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_not_b}"

@cocotb.test()
async def prueba_resta_sin_carry(dut):
    '''Prueba de la operación resta sin carry in'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 6

    for valor_a in range(RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range(RANGO):
            dut.ALUB.value = valor_b
            resultado_resta = (valor_a - valor_b) & 0xF
            resultado_carry_resta = ((valor_a - valor_b) >> 4) & 1
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado_resta, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_resta}"
            assert dut.ALUFlags.value == resultado_carry_resta, f"El valor de la salida ALUFlags es incorrecto. Se obtuvo {dut.ALUFlags.value}, se esperaba {resultado_carry_resta}"

@cocotb.test()
async def prueba_resta_con_carry(dut):
    '''Prueba de la operación suma con carry in'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 1
    dut.ALUControl.value = 6

    for valor_a in range(RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range(RANGO):
            dut.ALUB.value = valor_b
            resultado_resta = (valor_a - valor_b - 1) & 0xF
            resultado_carry_resta = ((valor_a - valor_b - 1) >> 4) & 1
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado_resta, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {resultado_resta}"
            assert dut.ALUFlags.value == resultado_carry_resta, f"El valor de la salida ALUFlags es incorrecto. Se obtuvo {dut.ALUFlags.value}, se esperaba {resultado_carry_resta}"

@cocotb.test()
async def test_XOR(dut):
    '''Prueba de la operación XOR'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 7

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range (RANGO):
            dut.ALUB.value = valor_b
            await Timer(1, 'ns')
            assert dut.ALUResult.value == valor_a ^ valor_b, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {(valor_a ^ valor_b)}"

@cocotb.test()
async def test_corrimiento_izquierda_ceros(dut):
    '''Prueba de la operación corrimiento a la izquierda con ceros'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 8

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range (RANGO):
            dut.ALUB.value = valor_b
            resultado = (valor_a << valor_b) & 0xF
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {(resultado)}"

@cocotb.test()
async def test_corrimiento_izquierda_unos(dut):
    '''Prueba de la operación corrimiento a la izquierda con unos'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 1
    dut.ALUControl.value = 8

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range (RANGO):
            dut.ALUB.value = valor_b
            resultado_esperado = ((valor_a << valor_b) | ((1 << valor_b) - 1)) & 0xF
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado_esperado, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {(resultado_esperado)}"

@cocotb.test()
async def test_corrimiento_derecha_ceros(dut):
    '''Prueba de la operación corrimiento a la derecha con ceros'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 0
    dut.ALUControl.value = 9

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        for valor_b in range (RANGO):
            dut.ALUB.value = valor_b
            resultado = (valor_a >> valor_b) & 0xF
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {(resultado)}"

@cocotb.test()
async def test_corrimiento_derecha_unos(dut):
    '''Prueba de la operación corrimiento a la izquierda con unos'''
    dut.ALUA.value = 0
    dut.ALUB.value = 0
    dut.ALUFlagIn.value = 1
    dut.ALUControl.value = 9

    c = 0

    for valor_a in range (RANGO):
        dut.ALUA.value = valor_a
        c = 0
        for valor_b in range (RANGO):
            dut.ALUB.value = valor_b
            resultado = ((valor_a >> valor_b) | valores_b[c]) & 0xF
            await Timer(1, 'ns')
            assert dut.ALUResult.value == resultado, f"El valor de la salida ALUResult es incorrecto. Se obtuvo {dut.ALUResult.value}, se esperaba {(resultado)}"
            
            if c <= 13:
                c = c + 1