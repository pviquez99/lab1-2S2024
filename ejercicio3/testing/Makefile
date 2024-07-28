# Makefile
export PYTHONPATH := $(PWD):$(PYTHONPATH)

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../display_7_segmentos.sv
TOPLEVEL = display_7_segmentos
MODULE = display_7_segmentos_tb
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
