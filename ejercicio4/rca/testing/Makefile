# Makefile
export PYTHONPATH := $(PWD):$(PYTHONPATH)

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../full_adder.sv \
		  $(PWD)/../RCA.sv
TOPLEVEL = RCA
MODULE = RCA_tb
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
