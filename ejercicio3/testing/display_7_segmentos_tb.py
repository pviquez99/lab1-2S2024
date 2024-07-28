import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_7_segmentos(dut):
    """Test del display de 7 segmentos"""
    def mapeo_7_segmentos(segmento):
        mapeo = {
        '0000': int('1000000', 2),  # 0
        '0001': int('1111001', 2),  # 1
        '0010': int('0100100', 2),  # 2
        '0011': int('0110000', 2),  # 3
        '0100': int('0011001', 2),  # 4
        '0101': int('0010010', 2),  # 5
        '0110': int('0000010', 2),  # 6
        '0111': int('1111000', 2),  # 7
        '1000': int('0000000', 2),  # 8
        '1001': int('0010000', 2),  # 9
        '1010': int('0001000', 2),  # A
        '1011': int('0000011', 2),  # B
        '1100': int('0100111', 2),  # C
        '1101': int('0100001', 2),  # D
        '1110': int('0000110', 2),  # E
        '1111': int('0001110', 2)   # F
    }
        return mapeo.get(segmento, int('1111111', 2))

    for combinacion in range (2**16):
        valor_switches = combinacion
        dut.sw_pi.value = valor_switches

        #Caso 1
        dut.boton_izquierda_pi.value = 0
        dut.boton_derecha_pi.value = 0
        segmento = valor_switches & 0xF
        segmento_binario = f'{segmento:04b}'
        LED = mapeo_7_segmentos(segmento_binario)
        await Timer(1, 'ps')
        assert dut.LED_o.value == LED, f"El valor de LED_o es incorrecto. Se recibió {dut.LED_o.value}, esperaba {LED}" 

        #Caso 2
        dut.boton_izquierda_pi.value = 0
        dut.boton_derecha_pi.value = 1
        segmento = (valor_switches >> 4) & 0xF
        segmento_binario = f'{segmento:04b}'
        LED = mapeo_7_segmentos(segmento_binario)
        await Timer(1, 'ps')
        assert dut.LED_o.value == LED, f"El valor de LED_o es incorrecto. Se recibió {dut.LED_o.value}, esperaba {LED}" 

        #Caso 3
        dut.boton_izquierda_pi.value = 1
        dut.boton_derecha_pi.value = 0
        segmento = (valor_switches >> 8) & 0xF
        segmento_binario = f'{segmento:04b}'
        LED = mapeo_7_segmentos(segmento_binario)
        await Timer(1, 'ps')
        assert dut.LED_o.value == LED, f"El valor de LED_o es incorrecto. Se recibió {dut.LED_o.value}, esperaba {LED}" 

        #Caso 4
        dut.boton_izquierda_pi.value = 1
        dut.boton_derecha_pi.value = 1
        segmento = (valor_switches >> 12) & 0xF
        segmento_binario = f'{segmento:04b}'
        LED = mapeo_7_segmentos(segmento_binario)
        await Timer(1, 'ps')
        assert dut.LED_o.value == LED, f"El valor de LED_o es incorrecto. Se recibió {dut.LED_o.value}, esperaba {LED}" 