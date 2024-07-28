# Makefile
export PYTHONPATH := $(PWD):$(PYTHONPATH)

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../switches_leds.sv
TOPLEVEL = switches_leds
MODULE = switches_leds_tb
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
