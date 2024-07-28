# Makefile
export PYTHONPATH := $(PWD):$(PYTHONPATH)

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../mux_4_1.sv
TOPLEVEL = mux_4_1
MODULE = mux_4_1_tb
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
