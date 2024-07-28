# Makefile
export PYTHONPATH := $(PWD):$(PYTHONPATH)

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../ALU.sv
TOPLEVEL = ALU
MODULE = ALU_tb
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
