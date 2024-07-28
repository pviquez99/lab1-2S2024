# Makefile
export PYTHONPATH := $(PWD):$(PYTHONPATH)

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../full_adder.sv
TOPLEVEL = full_adder
MODULE = full_adder_tb
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
