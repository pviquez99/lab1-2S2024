# Makefile
export PYTHONPATH := $(PWD):$(PYTHONPATH)

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../CLA.sv
TOPLEVEL = CLA
MODULE = CLA_tb
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
